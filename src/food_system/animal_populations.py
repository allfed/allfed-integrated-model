"""

Function which initiliases all of the animal population data
Working file for now, may be broken up. 

Requierments:
    - animal population data
    - animal slaughter data
    - animal feed data
    - animal nutrition data
    - RATIO_GRASSES_YEAR coupled with 

Functionality required
    - read in animal population data
    - read in animal slaughter data
    - read in animal feed data
    - read in animal nutrition data
    - create animal population classes

Ideal for the future:
    - maintain ability for 'efficient' or 'inefficient' farming, that is the difference between focusing on dairy vs business as usual
    - 


"""
from pathlib import Path
import pandas as pd
import numpy as np
import git
from src.food_system.food import Food
import pdb
import matplotlib.pyplot as plt


"""
Start main function
"""


# create class to store animal population data in. Needs to store the following: animal type, population, and slaughter.
class AnimalSpecies:
    """
    Class to store animal population data in. Needs to store the following: animal type, population, and slaughter.

    Parameters
    ----------
    animal_type : str
        Type of animal (beef, pork, chicken etc...)
        population : int
        Number of animals (total)
        slaughter : int
        Number of animals slaughtered this month
        pregnant : int
        Number of animals pregnant this month
        starving : int
        Number of animals starving this month
        feed_required : int
        Amount of feed required this month
        nutrition_ratio : object
        Object containing the nutrition ratio for the animal type

    """

    def __init__(
        self,
        animal_type,
        animal_species,
        population,
        slaughter,
        animal_function,
        feed_LSU,
        digestion_type,
        approximate_feed_conversion,
        digestion_efficiency=0.5,
        carb_requirement=-1,
        protein_requirement=-1,
        fat_requirement=-1,
    ):
        """
        Initializes an Animal object with various attributes.

        Args:
            animal_type (str): The type of animal (e.g. cow, pig, chicken)
            animal_species (str): The species of animal (e.g. Holstein, Berkshire, Leghorn)
            population (int): The initial population of the animal
            slaughter (int): The number of animals slaughtered per year
            animal_function (str): The function of the animal (e.g. milk production, meat production, egg production)
            feed_LSU (float): The Livestock Unit (LSU) value of the feed
            digestion_type (str): The type of digestion (e.g. monogastric, ruminant)
            approximate_feed_conversion (float): The approximate feed conversion ratio
            digestion_efficiency (float): The conversion from gross energy to net energy (default 0.5)
            carb_requirement (float): The required ratio of carbohydrates in the animal's diet (default -1)
            protein_requirement (float): The required ratio of protein in the animal's diet (default -1)
            fat_requirement (float): The required ratio of fat in the animal's diet (default -1)

        Returns:
            None

        Example:
            >>> cow = Animal('cow', 'Holstein', 100, 10, 'milk production', 1.0, 'ruminant', 0.1, carb_requirement=0.5, protein_requirement=0.3, fat_requirement=0.2)
        """
        # basic attributes
        self.animal_type = animal_type
        self.animal_species = animal_species
        self.population = [
            population
        ]  # this is a list so that it can be appended to later
        self.baseline_slaughter = (
            slaughter / 12
        )  # static, initial value as it gets called to set other attributes, it's handy to have it simplified
        self.animal_function = animal_function
        # other slaughtering attributes are set in a different function

        # FEED attributes
        self.feed_LSU = feed_LSU
        self.digestion_type = digestion_type
        self.approximate_feed_conversion = approximate_feed_conversion  # note this only used for ranking the efficiency, not used for calculating the feed required
        self.digestion_efficiency = digestion_efficiency  # this is the conversion from gross energy to net energy
        self.feed_balance = (
            self.feed_required_per_month_species()
        )  # this is the feed required per month for the species
        self.population_fed = 0
        self.population_starving = 0

        # slaughtering attributes
        if slaughter > 0:
            self.statistical_lifetime = (
                population / slaughter
            )  # this is the statistical lifetime of the animal, used to calculate the number of animals slaughtered per month
        self.retiring_milk_animals = [None]

        # not currently used, used for meat production information
        self.carcass_weight = None  # update to include this in the csv file
        self.offal_percentage = None  # update to include this in the csv file
        self.fat_percentage = None  # update to include this in the csv file
        if self.carcass_weight and self.offal_percentage and self.fat_percentage:
            self.carcass_weight = self.carcass_weight
            self.offal_percentage = self.offal_percentage
            self.fat_percentage = self.fat_percentage

        # not currently used, for carb/fat/protein requirements
        # not currently used
        self.nutrition_ratio = (
            Food(carb_requirement, fat_requirement, protein_requirement)
            if carb_requirement and fat_requirement and protein_requirement
            else None
        )
        if self.nutrition_ratio:
            self.nutrition_ratio.set_units(
                kcals_units="ratio of carbs in diet required",
                fat_units="ratio of fat in diet required",
                protein_units="ratio of protein in diet required",
            )

    def set_species_milk_attributes(
        self,
        productive_milk_age_start,
        productive_milk_age_end,
        milk_production_per_month=None,
    ):
        """
        Sets milk-related attributes for a given species of animal.

        Args:
            productive_milk_age_start (int): The age at which an animal starts producing milk.
            productive_milk_age_end (int): The age at which an animal stops producing milk.
            milk_production_per_month (float, optional): The amount of milk produced per month by the animal. Defaults to None.

        Returns:
            None

        Example:
            >>> cow = Animal()
            >>> cow.set_species_milk_attributes(2, 5, 50.0)
        """

        # Set the productive milk age range
        self.productive_milk_age_start = productive_milk_age_start
        self.productive_milk_age_end = productive_milk_age_end

        # Calculate the proportion of the population that is productive for milk
        self.population_proportion_productive_milk = (
            productive_milk_age_end - productive_milk_age_start
        ) / productive_milk_age_end

        # Set the milk production per month
        self.milk_production_per_month = (
            milk_production_per_month  # update to include this in the csv file
        )

        # Set the statistical lifetime of the animal
        self.statistical_lifetime = productive_milk_age_end

        # Calculate the fraction of animals that retire each month
        self.retiring_milk_animals_fraction = 1 / productive_milk_age_end

        # Set the list of retiring milk animals
        self.retiring_milk_animals = [self.retiring_milk_head_monthly()]

    def retiring_milk_head_monthly(self):
        """
        Calculates the number of retiring milk animals per month based on the fraction of retiring milk animals
        in the population.

        Args:
            self (object): An instance of the class containing the population and fraction of retiring milk animals.

        Returns:
            float: The number of retiring milk animals per month.

        Example:
            >>> farm = Farm(100, 0.1)
            >>> farm.retiring_milk_head_monthly()
            10.0
        """
        # The number of retiring milk animals per month is equal to the product of the current population and the fraction
        # of retiring milk animals.
        return self.population[-1] * self.retiring_milk_animals_fraction

    def set_species_slaughter_attributes(
        self,
        gestation,
        other_animal_death_rate_annual,
        animals_per_pregnancy,
        animal_slaughter_hours,
        change_in_slaughter_rate,
        pregnant_animal_slaughter_fraction,
        reduction_in_animal_breeding,
        target_population_fraction,
        transfer_births_or_head=0,
    ):
        """
        Function to set the attributes of the animal species that are related to slaughter

        Args:
            gestation (int): gestation period in months
            other_animal_death_rate_annual (float): annual death rate of animals
            animals_per_pregnancy (int): number of animals per pregnancy
            animal_slaughter_hours (int): hours per animal spent slaughtering
            change_in_slaughter_rate (float): change in slaughter rate (a static value, given by assumptions of loss of industry etc...)
            pregnant_animal_slaughter_fraction (float): this is the fraction of pregnant animals that are attempted to be slaughtered each month
            reduction_in_animal_breeding (float): this is the reduction in animal breeding (a static value, given by assumptions of loss of industry etc...)
            target_population_fraction (float): this is the target population fraction (a static value, given by assumptions of loss of industry etc...)
            transfer_births_or_head (int): this is head of increased population due to either male offspring of milk animals being added toa meat population or head imported from other countries

        Returns:
            None

        Description:
            This function sets the attributes of the animal species that are related to slaughter. It takes in various parameters and calculates the values of different attributes based on them.

        """

        # attributes of the animal species
        self.gestation = gestation  # gestation period in months
        self.other_animal_death_rate_annual = (
            other_animal_death_rate_annual  # annual death rate of animals
        )
        self.animals_per_pregnancy = (
            animals_per_pregnancy  # number of animals per pregnancy
        )

        # attributes of the slaughterers/society
        self.animal_slaughter_hours = (
            animal_slaughter_hours  # hours per animal spent slaughtering
        )
        self.change_in_slaughter_rate = change_in_slaughter_rate  # change in slaughter rate (a static value, given by assumptions of loss of industry etc...)

        # options of the scenario
        self.pregnant_animal_slaughter_fraction = pregnant_animal_slaughter_fraction  # this is the fraction of pregnant animals that are attempted to be slaughtered each month
        self.reduction_in_animal_breeding = reduction_in_animal_breeding
        self.target_population_fraction = target_population_fraction  # acts as a minimum, will not be used to increase pops in current version
        self.target_population_head = (
            self.target_population_fraction * self.population[0]
        )  # this is the target population head, used to calculate the number of animals slaughtered per month

        # calculations based off of the above
        self.other_animal_death_rate_monthly = other_animal_death_rate_annual / 12
        self.other_animal_death_basline_head_monthly = (
            self.other_animal_death_rate_monthly * self.population[0]
        )
        self.total_animal_death_head_monthly = [
            self.other_animal_death_basline_head_monthly + self.baseline_slaughter
        ]  # this will change, maybe should be list
        self.other_animal_death = [
            self.other_animal_death_basline_head_monthly
        ]  # this will change, maybe should be list
        if self.animal_function == "milk":
            self.birth_ratio = 2  # number of animals born per milk animal
        else:
            self.birth_ratio = 1  # number of animals born (total from population) per milk animal. I.e all male milk animals are not considered milk anaimls and need to be moved over to meat
        self.transfer_births_or_head = [transfer_births_or_head]
        self.births_animals_month = [
            self.total_animal_death_head_monthly[0] - transfer_births_or_head
        ]
        self.slaughter = [self.baseline_slaughter * change_in_slaughter_rate]  # is list
        self.pregnant_animals_total = self.birth_ratio * [
            self.births_animals_month[-1] / self.animals_per_pregnancy * self.gestation
        ]  # assumes even distribution of births, this is not true. OPTIONAL TODO, update this to be more accurate and deal with seasonal births. Can be done by chaning the "gestation" to be a complicated value based on month/season
        self.pregnant_animals_birthing_this_month = [
            self.pregnant_animals_total[-1] / self.gestation
        ]
        self.slaughtered_pregnant_animals = [
            self.pregnant_animals_total[-1] * pregnant_animal_slaughter_fraction
        ]

        return

    def exported_births(self):
        """
        Calculates the number of births exported from the animal population.

        Args:
            None

        Returns:
            exported_births (int): the number of births exported from the animal population

        Explanation:
            This function calculates the number of births exported from the animal population
            by multiplying the number of births per month by the birth ratio minus 1.

        Example:
            If the animal population has 100 births per month and a birth ratio of 2, then
            the number of exported births would be 100 * (2-1) = 100.

        """

        exported_births = self.births_animals_month * (self.birth_ratio - 1)

        return exported_births

    def net_energy_required_per_month(self):
        """
        Calculates the net energy required per month for a given feed and livestock unit (LSU).
        The calculation is based on the method described in the article "Livestock unit calculation: a method based on energy requirements to refine the study of livestock farming systems" by NRAE Prod. Anim., 2021, 34 (2), 139e-160e.
        Args:
            self (object): An instance of the class containing the feed and LSU information.
        Returns:
            float: The net energy required per month in billion kcal for the given feed and LSU.
        """
        # Define the net energy required per year for one LSU
        one_year_NEt = 29000  # Mcal per year #NEt = Net Energy Total for maintenance

        # Convert the net energy required per LSU per month to billion kcal
        # One billion kcals is the default unit for the food object
        # 1*10^9 kcal = 1 billion kcal = 1*10^6 Mcal
        # Convert to billion kcals
        one_LSU_monthly_billion_kcal = (
            (one_year_NEt / 12) / 4.187 * 1000 / 1e9
        )  # 12 months in a year, 4.187 to convert to kcal, 1000 to convert to kcal from Mcal

        # Calculate the net energy required per month for the given feed and LSU
        return self.feed_LSU * one_LSU_monthly_billion_kcal

    def feed_required_per_month_individual(self):
        """
        Calculates the total feed required for this month for the species.
        The function uses the net energy required per month function and the digestion efficiency to calculate the total feed.
        Args:
            self: an instance of the Animal class
        Returns:
            Food: an instance of the Food class representing the total feed required for the species for this month.
                  The instance contains the following attributes:
                  - kcal: billion kcals
                  - fat: thousand tons monthly fat (default value of -1)
                  - protein: thousand tons monthly protein (default value of -1)
        """
        # protein and fat is not currently used
        # calculate the total feed required using the net energy required per month function and the digestion efficiency
        return Food(
            self.net_energy_required_per_month() / self.digestion_efficiency, -1, -1
        )

    def feed_required_per_month_species(self):
        """
        Calculates the total feed required for this month for the species.
        The function uses the net energy required per month function and the digestion efficiency to calculate the feed.
        Args:
            self: an instance of the Animal class
        Returns:
            Food: an instance of the Food class representing the total feed required for the species for this month.
                  The instance contains the following attributes:
                  - kcal: billion kcals
                  - fat: thousand tons monthly fat
                  - protein: thousand tons monthly protein
        """
        # Calculate the total feed required for the species for this month
        # The calculation is based on the net energy required per month and the digestion efficiency
        total_feed = (
            self.net_energy_required_per_month()
            / self.digestion_efficiency
            * self.population[-1]
        )

        # Create an instance of the Food class representing the total feed required for the species for this month
        # The instance contains the following attributes:
        # - kcal: billion kcals
        # - fat: thousand tons monthly fat
        # - protein: thousand tons monthly protein
        return Food(total_feed, -1, -1)

    def feed_the_species(self, food_input):
        """
        Feeds the species with the given food input and updates the feed balance and population fed/starving accordingly.
        Args:
            food_input (Food): The food object containing the amount of kcals, fat, and protein to feed the species.

        Returns:
            Food: The remaining food object after feeding the species.

        Example:
            >>> food = Food(1000, 50, 20)
            >>> species = Species('lion', 10, Food(500, 25, 10))
            >>> remaining_food = species.feed_the_species(food)
        """

        # calculate the feed required based on the current feed balance
        feed_required = self.feed_balance

        # check if no food is required
        if self.feed_balance.kcals == 0:
            # no food required
            return food_input

        # if protein and fats are used NOT IMPLEMENTED AS OF 17th May 2023
        if self.feed_balance.fat > 0 and self.feed_balance.protein > 0:
            # still need more thought on how to deal with this. Units of food aren't fungible necessarily, can't easily move macros between
            if (
                food_input.kcals > self.feed_balance.kcals
                and food_input.fat > self.feed_balance.fat
                and food_input.protein > self.feed_balance.protein
            ):
                # whole population is fed
                self.population_fed = self.population
                # update the food object
                food_input.kcals -= self.feed_balance.kcals
                food_input.fat -= self.feed_balance.fat
                food_input.protein -= self.feed_balance.protein
                self.feed_balance = Food(0, 0, 0)
            else:
                # not enough food to feed the whole population
                # calculate the number of animals that can be fed
                self.population_fed = round(
                    food_input.kcals / feed_required.kcals * self.population[-1]
                )
                # update the food object
                food_input.kcals = 0
                food_input.fat = 0
                food_input.protein = 0
                self.feed_balance = feed_required - food_input
        else:
            # only using kcals
            if food_input.kcals > self.feed_balance.kcals:
                # whole population is fed
                self.population_fed = self.population
                # update the food object
                food_input.kcals -= self.feed_balance.kcals
                self.feed_balance = Food(0, 0, 0)
            else:
                # not enough food to feed the whole population
                # calculate the number of animals that can be fed
                self.population_fed = round(
                    food_input.kcals / self.feed_balance.kcals * self.population[-1]
                )
                # update the food object
                self.feed_balance = self.feed_balance - food_input
                food_input.kcals = 0

        # calculate the starving population based on the population fed
        # don't forget that population is a list of the population over time
        self.population_starving = self.population[-1] - self.population_fed

        # return the remaining food object
        return food_input


def read_animal_population_data():
    """
    Read animal population data from CSV file

    Returns
    -------
    df_animal_stock_info : pandas dataframe
        Dataframe containing animal population data

    """
    # Get the root directory of the repository
    repo_root = git.Repo(".", search_parent_directories=True).working_dir

    # Define the directory containing the animal feed data
    animal_feed_data_dir = (
        Path(repo_root) / "data" / "no_food_trade" / "animal_feed_data"
    )

    # Define the path to the FAO data file
    FAO_data = Path.joinpath(
        Path(animal_feed_data_dir), "FAOSTAT_head_and_slaughter.csv"
    )

    # Load the animal population data from the FAO data file
    df_animal_stock_info = pd.read_csv(FAO_data, index_col="iso3")

    # Return the dataframe containing the animal population data
    return df_animal_stock_info


def read_animal_nutrition_data():
    """
    Reads animal nutrition data from CSV file and returns a pandas dataframe.

    Returns
    -------
    df_animal_nutrition : pandas dataframe
        Dataframe containing animal nutrition data

    Raises
    ------
    FileNotFoundError
        If the CSV file containing animal nutrition data is not found.

    """

    # Get the root directory of the repository
    repo_root = git.Repo(".", search_parent_directories=True).working_dir

    # Define the directory containing animal feed data
    animal_feed_data_dir = (
        Path(repo_root) / "data" / "no_food_trade" / "animal_feed_data"
    )

    # Define the location of the CSV file containing animal nutrition data
    animal_nutrition_data_location = Path.joinpath(
        Path(animal_feed_data_dir), "species_attributes.csv"
    )

    try:
        # Read the CSV file containing animal nutrition data into a pandas dataframe
        df_animal_attributes = pd.read_csv(
            animal_nutrition_data_location, index_col="animal"
        )
    except FileNotFoundError:
        # Raise an error if the CSV file is not found
        raise FileNotFoundError("CSV file containing animal nutrition data not found.")

    return df_animal_attributes


def read_animal_options():
    """
    Read animal nutrition data from CSV file

    Returns
    -------
    df_animal_nutrition : pandas dataframe
        Dataframe containing animal nutrition data
    """
    # Get the root directory of the repository
    repo_root = git.Repo(".", search_parent_directories=True).working_dir

    # Define the directory containing the animal feed data
    animal_feed_data_dir = (
        Path(repo_root) / "data" / "no_food_trade" / "animal_feed_data"
    )

    # Define the location of the CSV file containing the animal options
    animal_options_location = Path.joinpath(
        Path(animal_feed_data_dir), "species_options.csv"
    )

    # Read the CSV file into a pandas dataframe
    df_animal_options = pd.read_csv(animal_options_location, index_col="animal")

    # Return the dataframe
    return df_animal_options


def create_animal_objects(df_animal_stock_info, df_animal_attributes):
    """
    Create animal objects from dataframes

    Parameters
    ----------
    df_animal_stock_info : pandas dataframe
        Single dimension Dataframe containing animal population data for each country
    df_animal_attributes : pandas dataframe
        Dataframe containing animal nutrition data

    Returns
    -------
    animal_objects : list
        List of animal objects
    """

    # Check that the number of columns containing the word "head" is equal to the number of columns containing the word "slaughter"
    assert (
        ~(df_animal_stock_info.index.str.contains("milk"))
        * df_animal_stock_info.index.str.contains("head")
    ).sum() == df_animal_stock_info.index.str.contains("slaughter").sum()

    # Create a list of the animal types (use index not columns, because it is a series that is passed in)
    animal_types = df_animal_stock_info.index[
        df_animal_stock_info.index.str.contains("head")
    ].str.replace("_head", "")

    # Create dict to store the animal objects
    animal_objects = {}

    # Loop through the animal types and create objects for each
    for animal_type in animal_types:
        # If animal type contains the word "milk" then it is a dairy animal
        if "milk" in animal_type:
            slaughter_input = 0
            animal_function = "milk"
        else:
            # Remove "meat_" from the animal type
            slaughter_input = df_animal_stock_info.loc[
                animal_type.replace("meat_", "") + "_slaughter"
            ]
            animal_function = "meat"

        # Create string of animal species (remove milk or meat from the animal type)
        animal_species = animal_type.replace("milk_", "").replace("meat_", "")

        # Create an AnimalSpecies object for the current animal type
        animal_object = AnimalSpecies(
            animal_type=animal_type,
            animal_species=animal_species,
            population=df_animal_stock_info.loc[animal_type + "_head"],
            slaughter=slaughter_input,
            animal_function=animal_function,
            feed_LSU=df_animal_attributes.loc[animal_type]["LSU"],
            digestion_type=df_animal_attributes.loc[animal_type]["digestion type"],
            approximate_feed_conversion=df_animal_attributes.loc[animal_type][
                "approximate feed conversion"
            ],
        )

        # Add the AnimalSpecies object to the animal_objects dictionary
        animal_objects[animal_type] = animal_object

    # Return the dictionary of animal objects
    return animal_objects


def update_animal_objects_with_slaughter(
    animal_list, df_animal_attributes, df_animal_options
):
    """
    This function updates the animal objects with the slaughter data

    Args:
        animal_list (list): List of animal objects
        df_animal_attributes (pandas dataframe): Dataframe containing animal attibute data
        df_animal_options (pandas dataframe): Dataframe containing animal options data

    Returns:
        list: List of animal objects

    This function updates the animal objects with the slaughter data by setting the species slaughter attributes
    for each animal in the animal_list.

    The function loops through the dict of animal objects and sets the species slaughter attributes for each animal
    using the data from the df_animal_attributes and df_animal_options dataframes.

    Args:
        animal (Animal): An animal object from the animal_list
    """
    for animal in animal_list:
        # get the species slaughter attributes from the dataframes
        gestation = df_animal_attributes.loc[animal.animal_type]["gestation"]
        animal_slaughter_hours = df_animal_attributes.loc[animal.animal_type][
            "animal_slaughter_hours"
        ]
        other_animal_death_rate_annual = df_animal_attributes.loc[animal.animal_type][
            "other_animal_death_rate_annual"
        ]
        animals_per_pregnancy = df_animal_attributes.loc[animal.animal_type][
            "animals_per_pregnancy"
        ]
        reduction_in_animal_breeding = df_animal_options.loc[animal.animal_type][
            "reduction_in_animal_breeding"
        ]
        change_in_slaughter_rate = df_animal_options.loc[animal.animal_type][
            "change_in_slaughter_rate"
        ]
        pregnant_animal_slaughter_fraction = df_animal_options.loc[animal.animal_type][
            "pregnant_animal_slaughter_fraction"
        ]
        target_population_fraction = df_animal_options.loc[animal.animal_type][
            "target_population_fraction"
        ]

        # set the species slaughter attributes for the animal
        animal.set_species_slaughter_attributes(
            gestation,
            other_animal_death_rate_annual,
            animals_per_pregnancy,
            animal_slaughter_hours,
            change_in_slaughter_rate,
            pregnant_animal_slaughter_fraction,
            reduction_in_animal_breeding,
            target_population_fraction,
        )
    return animal_list


def update_animal_objects_with_milk(animal_list, df_animal_attributes):
    """
    This function updates the animal objects with the milk production data.

    Args:
        animal_list (list): List of animal objects.
        df_animal_attributes (pandas dataframe): Dataframe containing animal attribute data.

    Returns:
        animal_list (list): List of animal objects updated with milk production data.

    """

    # Loop through the list of animal objects
    for animal in animal_list:
        # Get the milk production attributes for the animal's species
        productive_milk_age_start = df_animal_attributes.loc[animal.animal_type][
            "productive_milk_age_start"
        ]
        productive_milk_age_end = df_animal_attributes.loc[animal.animal_type][
            "productive_milk_age_end"
        ]
        milk_production_per_month = df_animal_attributes.loc[animal.animal_type][
            "milk_production_per_month"
        ]
        # Set the milk production attributes for the animal
        animal.set_species_milk_attributes(
            productive_milk_age_start,
            productive_milk_age_end,
            milk_production_per_month,
        )
    return animal_list


def available_feed():
    """
    This function imports feed data from a model and calculates the available feed for animals.
    Energy is expressed as digestible (DE), metabolizable (ME), or net energy (NE) by considering the loss of energy during digestion and metabolism from gross energy (GE) in the feed, as follows:

    Gross energy (GE): the amount of energy in the feed.
    Digestible energy (DE): the amount of energy in the feed minus the amount of energy lost in the feces.
    Metabolizable energy (ME): the amount of energy in the feed minus the energy lost in the feces and urine.
    Net energy (NE): the amount of energy in the feed minus the energy lost in the feces, urine, and in heat production through digestive and metabolic processes, i.e. heat increment.

    Args:
        None

    Returns:
        Food: A Food object representing the available feed for animals.

    Example:
        >>> available_feed()
        <Food object at 0x7f8d5c6d7c50>
    """

    # import feed data from model
    ### TODO: import feed data from model

    # calculate kcals in feed, don't use protein/fats just yet. That's for a revision
    # all imports should be in GE, gross energy
    # calacuklation of NE is done in the feed animals function

    # create food objects (EXAMPLE)
    example_food1 = Food(1000, -1, -1)
    example_food2 = Food(100, -1, -1)

    # add the food objects together (EXAMPLE)
    feed = example_food1 + example_food2

    return feed


def available_grass():
    """
    Calculates the amount of available grass as animal feed in kcal.
    Energy is expressed as digestible (DE), metabolizable (ME), or net energy (NE) by considering the loss of energy during digestion and metabolism from gross energy (GE) in the feed, as follows:

    Gross energy (GE): the amount of energy in the feed.
    Digestible energy (DE): the amount of energy in the feed minus the amount of energy lost in the feces.
    Metabolizable energy (ME): the amount of energy in the feed minus the energy lost in the feces and urine.
    Net energy (NE): the amount of energy in the feed minus the energy lost in the feces, urine, and in heat production through digestive and metabolic processes, i.e. heat increment.
    """

    # NOTE THIS GRASS COULD BE LIMITED to ration etc.
    # This function only calculates the amount of grass available as animal feed, not how much grass is generally available.

    # Import grass data
    # Units should be in GE, gross energy
    # Calculation of NE is done in the feed animals function
    grass = Food(1000, -1, -1)  # 1000 units of grass in GE

    return grass


def feed_animals(
    animal_list,
    milk_animals,
    non_milk_ruminants,
    non_milk_animals,
    available_feed,
    available_grass,
):
    """
    This function feeds the animals in the farm by allocating the grass first to those animals that can eat it,
    and then allocating the remaining feed to the remaining animals. It prioritizes the animals that are most efficient
    at converting feed, starting with milk.

    Args:
        animal_list (list): A list of all the animals in the farm
        milk_animals (list): A list of all the milk-producing animals in the farm
        non_milk_ruminants (list): A list of all the non-milk-producing ruminant animals in the farm
        non_milk_animals (list): A list of all the non-milk-producing non-ruminant animals in the farm
        available_feed (int): The amount of feed available to be distributed
        available_grass (int): The amount of grass available to be distributed

    Returns:
        tuple: A tuple containing the remaining available feed and grass after distribution

    Example:
        >>> cow = MilkAnimal('cow', 100, 10)
        >>> goat = MilkAnimal('goat', 50, 5)
        >>> sheep = NonMilkRuminant('sheep', 75, 7)
        >>> pig = NonMilkNonRuminant('pig', 80, 8)
        >>> animal_list = [cow, goat, sheep, pig]
        >>> milk_animals = [cow, goat]
        >>> non_milk_ruminants = [sheep]
        >>> non_milk_animals = [pig]
        >>> available_feed = 1000
        >>> available_grass = 500
        >>> feed_animals(animal_list, milk_animals, non_milk_ruminants, non_milk_animals, available_feed, available_grass)
        (0, 0)
    """
    # Allocate grass to ruminants, milk first
    for milk_animal in milk_animals:
        available_grass = milk_animal.feed_the_species(available_grass)

    # Allocate feed to milk animals
    for milk_animal in milk_animals:
        available_feed = milk_animal.feed_the_species(available_feed)

    # Allocate grass to non-milk ruminants
    for ruminant in non_milk_ruminants:
        available_grass = ruminant.feed_the_species(available_grass)

    # Allocate feed to non-milk non-ruminants
    for non_milk_animal in non_milk_animals:
        available_feed = non_milk_animal.feed_the_species(available_feed)

    return available_feed, available_grass


def calculate_additive_births(animal_object, current_month):
    """
    Calculates the number of new animals born this month given the number of pregnant animals.
    If breeding intervention has kicked in, the reduction in breeding is taken into account for new births.
    Args:
        animal_object (Animal): an instance of the Animal class containing information about the animal population
        current_month (int): the current month of the simulation
    Returns:
        tuple: a tuple containing the number of new animals born this month and the number of new export births
    """
    # First, check if breeding intervention has kicked in (based on gestation period)
    # If so, bring the reduction in breeding into impact the new births
    # Also turn off the need to slaughter pregnant animals (as we have already reduced the pregnant animals through the breeding intervention)
    if np.abs(current_month - animal_object.gestation) <= 0.5:
        calculate_breeding_changes(animal_object)

    # Calculate the number of new animals born this month given the number of pregnant animals
    # (must run after calculate_breeding_changes)
    # MILK only half of new births will be milk animals (captured in export animals)
    new_births_animals_month, new_export_births = calculate_births(animal_object)

    return new_births_animals_month, new_export_births


def calculate_change_in_population(
    animal_object, spare_slaughter_hours, new_additive_animals_month
):
    """
    This function will calculate the change in animal population for a given animal type
    It will do so by calculating the number of new births, the number of deaths, and the number of animals slaughtered
    It will then update the animal object with the new population

    It will also update the animal object with the number of animals that are pregnant, and the number of animals that are lactating

    Some parameters are calculated before the 'slaughter event' where the populations change, some are calculated after
    Those that are calculated before are:
        - the new births this month (based on the number of animals that are pregnant)
        - other deaths this month
        - the slaughter rate this month
        - spare slaughter hours this month
    Those that are calculated after are:
        - the number of animals that are lactating
        - the new population this month
        - the population of animals that are pregnant for next month

    Args:
        animal_object (Animal): an instance of the Animal class
        spare_slaughter_hours (float): the number of slaughter hours left over from the previous month
        new_additive_animals_month (int): the number of new animals added to the population this month

    Returns:
        float: the number of slaughter hours left over after the calculations have been made

    Example:
        >>> animal_object = Animal('cows', 100, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5)
        >>> spare_slaughter_hours = 10.0
        >>> new_additive_animals_month = 5
        >>> calculate_change_in_population(animal_object, spare_slaughter_hours, new_additive_animals_month)
        0.0
    """
    if animal_object.animal_function == "milk":
        # they turn in to meat animls, this is done in a previous step already
        # incoming retiring animals (that is, those going from milk -> meat), are already contained in the
        # new_additive_animals_month variable
        retiring_animals = calculate_retiring_milk_animals(animal_object)
        animal_object.retiring_milk_animals.append(retiring_animals)

    else:
        retiring_animals = 0

    target_animal_population = animal_object.target_population_head

    # Calculate other deaths
    new_other_animal_death = calculate_other_deaths(animal_object)

    # Determine slaughter rates (USE spare slaughter hours)
    # Each call of this function is "greedy" and will take as many slaughter hours as possible until the species is at the target population
    # This means that the slaughter hours are used in the order that the species are listed in the animal_types list
    new_slaughter_rate, spare_slaughter_hours = calculate_slaughter_rate(
        animal_object,
        spare_slaughter_hours,
        target_animal_population,
        new_additive_animals_month,
        new_other_animal_death,
    )

    # This is the main calculation of the population
    new_animal_population = calculate_animal_population(
        animal_object,
        new_additive_animals_month,
        new_other_animal_death + retiring_animals,
        new_slaughter_rate,
    )

    # Determine how many of the animals who died this month were pregnant
    # Check if the number of pregnant animals set for slaughter is less than the number of animals slaughtered this month
    # If so, proceed to calculate the number of pregnant animals slaughtered
    # Otherwise, set the number of pregnant animals slaughtered to the number of animals slaughtered this month
    (
        new_pregnant_animals_total,
        new_slaughtered_pregnant_animals,
    ) = calculate_pregnant_slaughter(animal_object, new_slaughter_rate)

    # Calculate the number of pregnant animals birthing this month, based on the number of pregnant animals remaining
    # This is effectively the pregnant animals _next_ month
    new_pregnant_animals_birthing = calculate_pregnant_animals_birthing(
        animal_object, new_pregnant_animals_total
    )

    # quick check to fix any overshoots
    if (
        new_pregnant_animals_total < 0
    ):  # this is to avoid negative numbers of pregnant animals
        new_pregnant_animals_total = 0

    if new_animal_population < target_animal_population:
        new_animal_population = target_animal_population

    # don't need to return much as the animal object is passed by reference, so the changes are made to the object itself
    # just need to return the spare slaughter hours

    # append new values to the animal object
    animal_object.population.append(new_animal_population)
    animal_object.slaughter.append(new_slaughter_rate)
    animal_object.pregnant_animals_total.append(new_pregnant_animals_total)
    animal_object.pregnant_animals_birthing_this_month.append(
        new_pregnant_animals_birthing
    )
    animal_object.other_animal_death.append(new_other_animal_death)
    animal_object.slaughtered_pregnant_animals.append(new_slaughtered_pregnant_animals)

    return spare_slaughter_hours


def calculate_pregnant_animals_birthing(animal_object, new_pregnant_animals_total):
    """
    Calculates the number of pregnant animals birthing this month, based on the number of pregnant animals remaining.
    Uses a simple calculation of the number of pregnant animals divided by the gestation period.
    This is not a perfect calculation, as it assumes that an even distribution of animals will birth each month.
    However, it is a good approximation for the purposes of this model.

    Args:
        animal_object (AnimalSpecies): The animal object for the animal type that you want to calculate the change in population for.
        new_pregnant_animals_total (int): The number of pregnant animals remaining this month.

    Returns:
        int: The number of pregnant animals birthing this month.

    """
    # Calculate the number of pregnant animals birthing this month
    new_pregnant_animals_birthing_this_month = (
        new_pregnant_animals_total / animal_object.gestation
    )

    # Return the result
    return new_pregnant_animals_birthing_this_month


def calculate_pregnant_slaughter(animal_object, new_slaughter_rate):
    """
    This function calculates the number of pregnant animals that were slaughtered in a given month.

    Args:
        animal_object (object): An object containing information about the animal population.
        new_slaughter_rate (float): The number of animals slaughtered in the current month.

    Returns:
        tuple: A tuple containing the new total number of pregnant animals and the number of pregnant animals slaughtered.

    """

    # Get the total number of pregnant animals from the previous month
    new_pregnant_animals_total = animal_object.pregnant_animals_total[-1]

    # Check if the number of pregnant animals set for slaughter is less than the number of animals slaughtered this month
    if (
        animal_object.pregnant_animal_slaughter_fraction
        * animal_object.pregnant_animals_total[-1]
        < new_slaughter_rate
    ):
        # If so, calculate the number of pregnant animals slaughtered
        new_slaughtered_pregnant_animals = (
            animal_object.pregnant_animal_slaughter_fraction
            * animal_object.pregnant_animals_total[-1]
        )
        # Subtract the number of slaughtered pregnant animals and other animal deaths from the total number of pregnant animals
        new_pregnant_animals_total -= (
            new_slaughtered_pregnant_animals
            + animal_object.other_animal_death_rate_monthly
            * animal_object.pregnant_animals_total[-1]
        )
    else:
        # If the number of pregnant animals set for slaughter is greater than or equal to the number of animals slaughtered this month,
        # set the number of pregnant animals slaughtered to the number of animals slaughtered this month
        new_slaughtered_pregnant_animals = new_slaughter_rate
        # Subtract the number of slaughtered pregnant animals from the total number of pregnant animals
        new_pregnant_animals_total -= new_slaughtered_pregnant_animals

    # Return the new total number of pregnant animals and the number of pregnant animals slaughtered
    return new_pregnant_animals_total, new_slaughtered_pregnant_animals


def calculate_animal_population(
    animal_object, new_births_animals_month, new_other_animal_death, new_slaughter_rate
):
    """
    Calculates the new animal population based on the previous population, new births, deaths, and slaughter rate.
    Args:
        animal_object (Animal): an object representing the animal population
        new_births_animals_month (int): the number of new births in a month
        new_other_animal_death (int): the number of deaths from other causes in a month
        new_slaughter_rate (int): the number of animals slaughtered in a month
    Returns:
        int: the new animal population after accounting for births, deaths, and slaughter rate
    """
    # Get the previous population from the animal object
    previous_population = animal_object.population[-1]

    # Calculate the new population by subtracting deaths and slaughter rate and adding new births
    new_population = (
        previous_population
        - new_slaughter_rate
        - new_other_animal_death
        + new_births_animals_month
    )

    # Return the new population
    return new_population


# def calculate_imported_and_transfer_population(animal_object):


#     animal_object.transfer_births_or_head


def calculate_retiring_milk_animals(animal_object):
    """
    This function calculates the number of animals retiring from milk production this month

    Args:
    animal_object (object): The animal object that is being calculated

    Returns:
    int: The number of animals retiring from milk production this month
    """
    # Calculate the number of animals retiring from milk production this month
    # This is the number of animals that are at the end of their productive life
    # We get the last element of the population list and multiply it by the retiring_milk_animals_fraction
    new_retiring_milk_animals = (
        animal_object.population[-1] * animal_object.retiring_milk_animals_fraction
    )

    # Return the calculated value
    return new_retiring_milk_animals


def calculate_births(animal_object):
    """
    This function calculates the number of new births this month

    Args:
        animal_object (object): The animal object that is being calculated

    Returns:
        tuple: A tuple containing two integers:
            - new_births_animals_month: The number of new births this month
            - new_export_births_animals_month: The number of new export births this month (optional)

    Raises:
        None

    Example:
        >>> cow = Animal('cow', 10, 2, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5)
        >>> calculate_births(cow)
        (10, 0)

    """
    # Calculate the number of new births this month
    new_births_animals_month = (
        animal_object.pregnant_animals_birthing_this_month[-1]
        * animal_object.animals_per_pregnancy
    )

    # Calculate the number of new export births this month (optional)
    new_export_births_animals_month = new_births_animals_month * (
        animal_object.birth_ratio - 1
    )
    # new export births will be an optional return. Birth ratio is defined in the class
    # for milk animals "export births = new births" for meat animals "export births = 0"

    # Return the results as a tuple
    return new_births_animals_month, new_export_births_animals_month


def calculate_breeding_changes(animal_object):
    """
    Calculates changes in animal breeding based on the reduction in animal breeding rate.
    Args:
        animal_object (Animal): An instance of the Animal class containing information about the animal population.

    Returns:
        None

    Example:
        >>> animal = Animal()
        >>> calculate_breeding_changes(animal)
    """
    # Reduce the number of pregnant animals birthing this month based on the reduction in animal breeding rate
    animal_object.pregnant_animals_birthing_this_month[-1] *= (
        1 - animal_object.reduction_in_animal_breeding
    )

    # Reduce the total number of pregnant animals based on the reduction in animal breeding rate
    animal_object.pregnant_animals_total[-1] *= (
        1 - animal_object.reduction_in_animal_breeding
    )

    # Set the fraction of pregnant animals slaughtered to 0
    # Note: This is a simplistic approach and may not be appropriate for all scenarios
    animal_object.pregnant_animal_slaughter_fraction = 0

    # The function does not return anything, it simply updates the animal_object
    return


def calculate_other_deaths(animal_object):
    """
    Calculates the number of deaths of animals due to factors other than predation or birth.
    Args:
        animal_object (Animal): An instance of the Animal class containing the population and other_animal_death_rate_monthly attributes.
    Returns:
        float: The number of deaths due to other factors.
    """
    # Calculate the number of deaths due to other factors
    new_other_animal_death = (
        animal_object.population[-1] * animal_object.other_animal_death_rate_monthly
    )

    # Return the result
    return new_other_animal_death


def calculate_slaughter_rate(
    animal_object,
    spare_slaughter_hours,
    target_animal_population,
    new_births_animals_month,
    new_other_animal_death,
):
    """
    This function calculates the new slaughter rate based on the spare slaughter hours and the target animal population

    Args:
        animal_object (object): The animal object that is being calculated
        spare_slaughter_hours (int): The number of spare slaughter hours generated
        target_animal_population (int): The target animal population
        new_births_animals_month (int): The number of new births of animals per month
        new_other_animal_death (int): The number of deaths of other animals per month

    Returns:
        new_slaughter_rate (int): The new slaughter rate
        spare_slaughter_hours (int): The number of spare slaughter hours remaining after the new slaughter rate is calculated

    """
    # for dealing with milk, if slaughter hours is nan, then set it to 0
    if np.isnan(animal_object.slaughter[-1]):
        print("slaughter hours is nan")
        animal_object.slaughter[-1] = 0
        new_slaughter_rate = 0
        return new_slaughter_rate, spare_slaughter_hours

    else:
        # if there are no spare slaughter hours, then set the slaughter rate to the previous slaughter rate, this will
        # will happen becuase the numerator will be 0
        new_slaughter_rate = animal_object.slaughter[-1] + round(
            spare_slaughter_hours / animal_object.animal_slaughter_hours
        )
        spare_slaughter_hours = 0

        # if population will be below target, then slaughter rate is set to the difference and the new births minus other deaths
        if (
            animal_object.population[-1] - new_slaughter_rate
            < target_animal_population
            + new_births_animals_month
            - new_other_animal_death
        ):
            new_slaughter_rate = (
                animal_object.population[-1]
                - target_animal_population
                + new_births_animals_month
                - new_other_animal_death
            )
            # spare slaugthter hours ae calculated based on the new (reduced) slaughter rate
            if new_slaughter_rate < 0:
                new_slaughter_rate = 0
            spare_slaughter_hours = (
                abs(new_slaughter_rate - animal_object.slaughter[-1])
            ) * animal_object.animal_slaughter_hours

        return new_slaughter_rate, spare_slaughter_hours


## At the end of the month, reset the feed balance with the new popluaton and feed required


def main(country_code):
    """
    Main function to be called by the user. This function will call the other functions in this file.
    """

    ## IMPORT DATA

    # read animal population data
    df_animal_stock_info = read_animal_population_data()

    # read animal nutrition data
    df_animal_attributes = read_animal_nutrition_data()

    df_animal_options = read_animal_options()

    # months to run the model for
    months_to_run = 12

    ## Populate animal objects ##

    # create animal objects
    animal_list = create_animal_objects(
        df_animal_stock_info.loc[country_code], df_animal_attributes
    )

    # sort the animal objects by approximate feed conversion
    animal_dict = dict(
        sorted(
            animal_list.items(),
            key=lambda item: item[1].approximate_feed_conversion,
        )
    )

    # create available feed object
    feed_MJ_available_this_month = available_feed()
    grass_MJ_available_this_month = available_grass()

    # get list of milk animals,
    milk_animals = [
        animal for animal in animal_dict.values() if "milk" in animal.animal_type
    ]
    # get list of non-milk animals
    non_milk_animals = [
        animal for animal in animal_dict.values() if "milk" not in animal.animal_type
    ]
    # non milk runminants
    non_milk_ruminants = [
        animal
        for animal in animal_dict.values()
        if "milk" not in animal.animal_type and animal.digestion_type == "ruminant"
    ]
    # get list of all ruminants
    ruminants = [
        animal for animal in animal_dict.values() if animal.digestion_type == "ruminant"
    ]
    # get list of non-ruminants
    non_ruminants = [
        animal for animal in animal_dict.values() if animal.digestion_type != "ruminant"
    ]
    # all animals
    all_animals = [animal for animal in animal_dict.values()]

    ## Do the feeding
    # feed the animals
    feed_MJ_available_this_month, grass_MJ_available_this_month = feed_animals(
        animal_dict,
        milk_animals,
        non_milk_ruminants,
        non_milk_animals,
        feed_MJ_available_this_month,
        grass_MJ_available_this_month,
    )

    ## OKAY SO NOW WE HAVE THE ANIMALS FED, WE NEED TO LOOK AT SLAUGHTERING

    update_animal_objects_with_slaughter(
        all_animals, df_animal_attributes, df_animal_options
    )
    update_animal_objects_with_milk(milk_animals, df_animal_attributes)

    spare_slaughter_hours = (
        0  # this should be stored somewqhere betterthat stays persietnt over the months
    )

    # THIS month for loop won't reallt exist here, i will be called in a loop somewhere else
    # this is required as the I/O needs to interact with the rest of the model each month
    for month in range(0, months_to_run):
        # create a list of transfer populations, based on all the different animal species, use for loop to create a dict that can be used to store the transfer populations
        # important that these are zero as default
        transfer_populations = {}
        for animal in all_animals:
            transfer_populations[animal.animal_species] = 0

        # TODO:  the feed should go above here, worked out every month
        # INSRET FEED STUFF HERE###

        # this next loop is run first to populate the birth/retiurement tasnfers.
        # working out the transfer populations requires the milk animals birt rate / retuirmenet rates
        # this needs to be done first as the transfer population is used in the next loop
        # and the next loop will be run in order of slaughter preference, so we can't put the birth rates in there
        # so the first loop can be run in any order, but the second loop needs to be run in order of slaughter preference
        for animal in all_animals:
            # additive population

            new_births, new_transfer_births = calculate_additive_births(animal, month)
            # add new population to the animal object
            if animal.animal_type == "milk":
                transfer_populations[animal.animal_species] = (
                    animal.retiring_milk_head_monthly() + new_transfer_births
                )
                # add to tranfser population

        # this loop run in order of species slaughhter prefernce
        # TODO: what is this? provide an option to the user
        for animal in all_animals:
            if animal.animal_type != "milk":
                # if not a milk animal add
                new_additive_animals_month = (
                    new_births + transfer_populations[animal.animal_species]
                )
            else:
                new_additive_animals_month = new_births

            spare_slaughter_hours = calculate_change_in_population(
                animal, spare_slaughter_hours, new_additive_animals_month
            )

            # TODO:
            # do the slaughter transfer in a more robust way, but this currently works

        # then new loop...
        # NEXT DO POPULATIUON STARVING AFTER SLAUGHTER
        # AND HOMEKILL
        # do starving pop minus sluaghtr pop (assume starving animals are preferntially slaughtered i.e food is directed to thos not being slaughtered)
        # HOMEKILL HEALTHY POP = HOMEKILL RATE * NEW POP
        # OR HOMEKILL HEALTHY POP just equls a demand number not from percentage rate

        # NEW STARVIONG POP = STARVIN POP - #SLAUGHTER POP - HOMEKILL HEALTHY POP
        # HOMEKILL_STARVING = NEW STARVING POP * HOMEKILL STRVING RATE
        # OTHER_DEATH_STARVING = (NEW STARVING POP - HOMEKILL_STARVING)* STARVING DEATH RATE (this should be very high? 100%? at least leave the option there though)
        # NEW STARVING POP = NEW STARVING POP - HOMEKILL_STARVING - OTHER_DEATH_STARVING
        # NEW POP = NEW POP - HOMEKILL_STARVING - OTHER_DEATH_STARVING - HOMEKILL HEALTHY POP

        # note pregannt animals have already been calculated in the slaughter loop
        # this seems realistic tha policy would not flow down to homekill etc.
        # I'll leave it in there for now, if we want to change it, down the track. It probably makes zero difference but I haven't tested sesiticity yet

    # plot the results
    for animal in all_animals:
        plt.plot(animal.population, label=animal.animal_type)
    plt.legend()
    plt.show()

    return


if __name__ == "__main__":
    main("USA")


##### TESTS #####


# Functions:
# AnimalSpecies.__init__
# AnimalSpecies.feed_required_per_month_individual
# AnimalSpecies.feed_required_per_month_species
# AnimalSpecies.feed_the_species
# AnimalSpecies.net_energy_required_per_month
# AnimalSpecies.set_species_milk_attributes
# AnimalSpecies.set_species_slaughter_attributes
# available_feed
# available_grass
# calculate_animal_population
# calculate_births
# calculate_breeding_changes
# calculate_meat_change_in_population
# calculate_milk_change_in_population
# calculate_other_deaths
# calculate_pregnant_animals_birthing
# calculate_pregnant_slaughter
# calculate_retiring_milk_animals
# calculate_slaughter_rate
# change_in_animal_population
# create_animal_objects
# feed_animals
# food_conversion
# read_animal_nutrition_data
# read_animal_options
# read_animal_population_data
# update_animal_objects_with_milk
# update_animal_objects_with_slaughter
