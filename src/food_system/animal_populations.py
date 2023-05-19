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
    def __init__(self, animal_type, population, slaughter, animal_function, feed_LSU, digestion_type, approximate_feed_conversion, digestion_efficiency = 0.5, carb_requirement=-1, protein_requirement=-1, fat_requirement=-1):
        # basic attributes
        self.animal_type = animal_type
        self.population = [population] # this is a list so that it can be appended to later
        self.baseline_slaughter = slaughter/12 # static, initial value as it gets called to set other attributes, it's handy to have it simplified
        self.animal_function = animal_function
        # other slauhter attributes are set in a different function

        # FEED attributes
        self.feed_LSU = feed_LSU
        self.digestion_type = digestion_type
        self.approximate_feed_conversion = approximate_feed_conversion # note this only used for ranking the efficiency, not used for calculating the feed required
        self.digestion_efficiency = digestion_efficiency # this is the conversion from gross energy to net energy
        self.feed_balance = self.feed_required_per_month_species() # this is the feed required per month for the species
        self.population_fed = 0
        self.population_starving = 0

        # slaughtering attributes
        if slaughter>0:
            self.statistical_lifetime = population/slaughter # this is the statistical lifetime of the animal, used to calculate the number of animals slaughtered per month
        self.retiring_milk_animals = [None]

        # not currently used, used for meat production information
        self.carcass_weight = None # update to include this in the csv file
        self.offal_percentage = None # update to include this in the csv file
        self.fat_percentage = None # update to include this in the csv file
        if self.carcass_weight and self.offal_percentage and self.fat_percentage:
            self.carcass_weight = self.carcass_weight
            self.offal_percentage = self.offal_percentage
            self.fat_percentage = self.fat_percentage
        
        # not currently used, for carb/fat/protein requirements
        # not currently used
        self.nutrition_ratio = Food(carb_requirement, fat_requirement, protein_requirement) if carb_requirement and fat_requirement and protein_requirement else None
        if self.nutrition_ratio:
            self.nutrition_ratio.set_units(
                kcals_units='ratio of carbs in diet required',
                fat_units='ratio of fat in diet required',
                protein_units='ratio of protein in diet required',
            )

    def set_species_milk_attributes(self, productive_milk_age_start, productive_milk_age_end, milk_production_per_month=None):

        # Milk attributes
        self.productive_milk_age_start = productive_milk_age_start
        self.productive_milk_age_end = productive_milk_age_end
        self.population_proportion_productive_milk = (productive_milk_age_end - productive_milk_age_start) / productive_milk_age_end
        self.milk_production_per_month = milk_production_per_month # update to include this in the csv file
        self.retiring_milk_animals = [self.population[0] / productive_milk_age_end]

    def set_species_slaughter_attributes(self, gestation, other_animal_death_rate_annual, animals_per_pregnancy, animal_slaughter_hours, change_in_slaughter_rate, pregnant_animal_slaughter_percent, reduction_in_animal_breeding, target_population):
        # attributes of the animal species
        self.gestation =  gestation # gestation period in months
        self.other_animal_death_rate_annual = other_animal_death_rate_annual # annual death rate of animals
        self.animals_per_pregnancy = animals_per_pregnancy # number of animals per pregnancy

        # attributes of the slaughterers/society
        self.animal_slaughter_hours = animal_slaughter_hours # hours per animal spent slaughtering 
        self.change_in_slaughter_rate = change_in_slaughter_rate # change in slaughter rate (a static value, given by assumptions of loss of industry etc...)

        # options of the scenario
        self.pregnant_animal_slaughter_percent = pregnant_animal_slaughter_percent # this is the percent of pregnant animals that are attempted to be slaughtered each month
        self.reduction_in_animal_breeding = reduction_in_animal_breeding
        self.target_population = target_population # acts as a minimum, will not be used to increase pops in current version
        
        # calculations based off of the above
        self.other_animal_death_rate_monthly =  other_animal_death_rate_annual / 12
        self.other_animal_death_basline_head_monthly = self.other_animal_death_rate_monthly * self.population[0]
        self.total_animal_death_head_monthly = [self.other_animal_death_basline_head_monthly + self.baseline_slaughter] # this will change, maybe should be list
        self.other_animal_death = [self.other_animal_death_basline_head_monthly] # this will change, maybe should be list
        if self.animal_function == 'milk':
            birth_ratio = 1
        else:   
            birth_ratio = 1
        self.births_animals_month = self.total_animal_death_head_monthly*birth_ratio # this will be a list because  total death is a list
        self.slaughter = [self.baseline_slaughter*change_in_slaughter_rate] # is list
        self.pregnant_animals_total = [self.births_animals_month[-1] / self.animals_per_pregnancy * self.gestation] # assumes even distribution of births, this is not true. OPTIONAL TODO, update this to be more accurate and deal with seasonal births. Can be done by chaning the "gestation" to be a complicated value based on month/season
        self.pregnant_animals_birthing_this_month = [self.pregnant_animals_total[-1] /  self.gestation] 
        self.slaughtered_pregnant_animals = [self.pregnant_animals_total[-1] * pregnant_animal_slaughter_percent]


    def net_energy_required_per_month(self):
        # this section based on:
        # Livestock unit calculation: a method based on energy requirements to refine the study of livestock farming systems
        # NRAE Prod. Anim., 2021, 34 (2), 139e-160e
        # https://productions-animales.org/article/view/4855/17716

        # consider adopting their method for a finer grain analysis if required.
        # probably over-estimates the energy required for chickens...

        one_year_NEt =  29000 # Mcal per year #NEt = Net Energy Total for maintenance

        # one billion kcals is the default unit for the food object
        # 1*10^9 kcal = 1 billion kcal = 1*10^6 Mcal
        # convert to billion kcals
        one_LSU_monthly_billion_kcal = (one_year_NEt / 12) / 4.187 * 1000 / 1e9 # 12 months ina  year, 4.187 to convert to kcal, 1000 to convert to kcal from Mcal
        
        return self.feed_LSU * one_LSU_monthly_billion_kcal

    def feed_required_per_month_individual(self):
        # function to calculate the total feed for this month for the species
        #     (defaults to billion kcals, thousand tons monthly fat, thousand tons monthly protein)
        # protein and fat is not currently used
        # uses the net energy required per month function and the digestion efficiency
        return Food(self.net_energy_required_per_month()/self.digestion_efficiency, -1, -1)
    
    def feed_required_per_month_species(self):
        # function to calculate the total feed for this month for the species
        #     (defaults to billion kcals, thousand tons monthly fat, thousand tons monthly protein)
        # protein and fat is not currently used
        # uses the net energy required per month function and the digestion efficiency
        return Food(self.net_energy_required_per_month()/self.digestion_efficiency * self.population[-1], -1, -1)
    
    def feed_the_species(self, food_input):

        # function to feed the species
        feed_required = self.feed_balance

        if self.feed_balance.kcals == 0:
            # no food required
            # print('no food required for ' + self.animal_type)

            return food_input

        # if protein and fats are used NOT IMPLEMENTED AS OF 17th May 2023
        if self.feed_balance.fat>0 and self.feed_balance.protein>0:
            # still need more thought on how to deal with this. Units of food aren't fungible neccesarily, can't easily moce macros between
            if food_input.kcals > self.feed_balance.kcals & food_input.fat > self.feed_balance.fat & food_input.protein > self.feed_balance.protein:
                # whole population is fed
                self.population_fed = self.population
                # update the food object
                food_input.kcals -= self.feed_balance.kcals
                food_input.fat -= self.feed_balance.fat
                food_input.protein -= self.feed_balance.protein
                self.feed_balance = Food(0,0,0)
            else:
                # not enough food to feed the whole population
                # calculate the number of animals that can be fed
                self.population_fed = round(food_input.kcals / feed_required.kcals * self.population[-1])
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
                self.feed_balance = Food(0,0,0)

            else:
                # not enough food to feed the whole population
                # calculate the number of animals that can be fed
                self.population_fed = round(food_input.kcals / self.feed_balance.kcals * self.population[-1])
                # update the food object
                self.feed_balance = self.feed_balance - food_input
                food_input.kcals = 0

        # calculate the starving population based on the population fed
        # don't forget that population is a list of the population over time
        self.population_starving = self.population[-1] - self.population_fed

        return food_input
        
def read_animal_population_data():
    """
    Read animal population data from CSV file

    Returns
    -------
    df_animal_stock_info : pandas dataframe
        Dataframe containing animal population data
    
    """

    repo_root = git.Repo(".", search_parent_directories=True).working_dir
    # Load data
    animal_feed_data_dir = Path(repo_root) / "data" / "no_food_trade" / "animal_feed_data"

    FAO_data = Path.joinpath(
        Path(animal_feed_data_dir), "FAOSTAT_head_and_slaughter.csv"
    )
    
    # Load data
    df_animal_stock_info = pd.read_csv(FAO_data, index_col="iso3")

    # merge the two dataframes on index

    return df_animal_stock_info

def read_animal_nutrition_data():
    """"
    Read animal nutrition data from CSV file

    Returns
    -------
    df_animal_nutrition : pandas dataframe
        Dataframe containing animal nutrition data
    """
    repo_root = git.Repo(".", search_parent_directories=True).working_dir
    # Load data
    animal_feed_data_dir = Path(repo_root) / "data" / "no_food_trade" / "animal_feed_data"

    animal_nutrition_data_location = Path.joinpath(
        Path(animal_feed_data_dir), "species_attributes.csv"
    )

    df_animal_attributes = pd.read_csv(animal_nutrition_data_location, index_col="animal")

    return df_animal_attributes


def read_animal_options():
    """"
    Read animal nutrition data from CSV file

    Returns
    -------
    df_animal_nutrition : pandas dataframe
        Dataframe containing animal nutrition data
    """
    repo_root = git.Repo(".", search_parent_directories=True).working_dir
    # Load data
    animal_feed_data_dir = Path(repo_root) / "data" / "no_food_trade" / "animal_feed_data"

    animal_options_location = Path.joinpath(
        Path(animal_feed_data_dir), "species_options.csv"
    )

    df_animal_options = pd.read_csv(animal_options_location, index_col="animal")

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

    # use loops to populate all the different species:
    # headers for the slaughter and head data are:
    # iso3,country,chicken_head,rabbit_head,duck_head,goose_head,turkey_head,other_rodents_head,pig_head,meat_goat_head,meat_sheep_head,camelids_head,meat_cattle_head,meat_camel_head,meat_buffalo_head,mule_head,horse_head,asses_head,milk_sheep_head,milk_cattle_head,milk_goats_head,milk_camel_head,milk_buffalo_head,large_animals,medium_animals,small_animals,large_milk_animals,medium_milk_animals,small_milk_animals,chicken_slaughter,rabbit_slaughter,duck_slaughter,goose_slaughter,turkey_slaughter,other_rodents_slaughter,pig_slaughter,goat_slaughter,sheep_slaughter,camelids_slaughter,cattle_slaughter,camel_slaughter,buffalo_slaughter,mule_slaughter,horse_slaughter,asses_slaughter,large_animals_slaughter,medium_animals_slaughter,small_animals_slaughter

    # create objects for each animal type
    # create a dict of the objects
    # return the dict

    # create assertion to check that the number of columns containing the word "head" is equal to the number of columns containing the word "slaughter"
    assert (
        (~(df_animal_stock_info.index.str.contains("milk")) * df_animal_stock_info.index.str.contains("head")).sum()
        == df_animal_stock_info.index.str.contains("slaughter").sum()
    )
    # create a list of the animal types (use index not columns, because it is a series that is passed in)
    animal_types = df_animal_stock_info.index[
        df_animal_stock_info.index.str.contains("head")
    ].str.replace("_head", "")

    # create dict to store the animal objects
    animal_objects = {}


    # loop through the animal types and create objects for each
    for animal_type in animal_types:
        
        # if animal type contains the word "milk" then it is a dairy animal
        if "milk" in animal_type:
            slaughter_input = 0
            animal_function = "milk"
        else:
            # remove "meat_" from the animal type
            slaughter_input = df_animal_stock_info.loc[animal_type.replace("meat_", "") + "_slaughter"]
            animal_function = "meat"

        animal_species = AnimalSpecies(
            animal_type=animal_type,
            population=df_animal_stock_info.loc[animal_type + "_head"],
            slaughter=slaughter_input,
            animal_function=animal_function,
            feed_LSU=df_animal_attributes.loc[animal_type]["LSU"],
            digestion_type=df_animal_attributes.loc[animal_type]["digestion type"],
            approximate_feed_conversion=df_animal_attributes.loc[animal_type]["approximate feed conversion"],
        )
        animal_objects[animal_type] = animal_species

    return animal_objects




def update_animal_objects_with_slaughter(animal_list,df_animal_attributes,df_animal_options):
    """
    This function updates the animal objects with the slaughter data

    Parameters
    ----------
    animal_list : list
        List of animal objects
    df_animal_attributes : pandas dataframe
        Dataframe containing animal attibute data
    df_animal_options : pandas dataframe
        Dataframe containing animal options data

    Returns
    -------
    animal_list : list
        List of animal objects


    """

    # set the species slaughter attributes
    # for animal in animal_list:

    # loop through the dict of animal objects
    for animal in animal_list:
        # this list of variables will be a csv file in the future
        gestation = df_animal_attributes.loc[animal.animal_type]["gestation"]
        animal_slaughter_hours = df_animal_attributes.loc[animal.animal_type]["animal_slaughter_hours"]
        other_animal_death_rate_annual = df_animal_attributes.loc[animal.animal_type]["other_animal_death_rate_annual"]
        animals_per_pregnancy = df_animal_attributes.loc[animal.animal_type]["animals_per_pregnancy"]
        reduction_in_animal_breeding = df_animal_options.loc[animal.animal_type]["reduction_in_animal_breeding"]
        change_in_slaughter_rate = df_animal_options.loc[animal.animal_type]["change_in_slaughter_rate"]
        pregnant_animal_slaughter_percent = df_animal_options.loc[animal.animal_type]["pregnant_animal_slaughter_percent"]
        target_population = df_animal_options.loc[animal.animal_type]["target_population"]
        animal.set_species_slaughter_attributes(
            gestation, 
            other_animal_death_rate_annual, 
            animals_per_pregnancy,
            animal_slaughter_hours,
            change_in_slaughter_rate,
            pregnant_animal_slaughter_percent,
            reduction_in_animal_breeding,
            target_population
            )
    return

def update_animal_objects_with_milk(animal_list,df_animal_attributes):
    """
    This function updates the animal objects with the slaughter data

    Parameters
    ----------
    animal_list : list
        List of animal objects
    df_animal_attributes : pandas dataframe
        Dataframe containing animal attibute data
    df_animal_options : pandas dataframe
        Dataframe containing animal options data

    Returns
    -------
    animal_list : list
        List of animal objects


    """

    # set the species slaughter attributes
    # for animal in animal_list:

    # loop through the dict of animal objects
    for animal in animal_list:
        # this list of variables will be a csv file in the future
        productive_milk_age_start = df_animal_attributes.loc[animal.animal_type]["productive_milk_age_start"]
        productive_milk_age_end = df_animal_attributes.loc[animal.animal_type]["productive_milk_age_end"]
        milk_production_per_month = df_animal_attributes.loc[animal.animal_type]["milk_production_per_month"]
        animal.set_species_milk_attributes(
            productive_milk_age_start, 
            productive_milk_age_end, 
            milk_production_per_month,
            )   
    return

def food_conversion():
    # convert food to animal feed

    return

def available_feed():
    """
    Energy is expressed as digestible (DE), metabolizable (ME), or net energy (NE) by considering the loss of energy during digestion and metabolism from gross energy (GE) in the feed, as follows:

    Gross energy (GE): the amount of energy in the feed.
    Digestible energy (DE): the amount of energy in the feed minus the amount of energy lost in the feces.
    Metabolizable energy (ME): the amount of energy in the feed minus the energy lost in the feces and urine.
    Net energy (NE): the amount of energy in the feed minus the energy lost in the feces, urine, and in heat production through digestive and metabolic processes, i.e. heat increment.
    """
    # import feed data from model
    ### TODO: import feed data from model

    # calculate kcals in feed, don't use protein/fats just yet. That's for a revision
    # all imports should be in GE, gross energy
    # calacuklation of NE is done in the feed animals function

    # create food objects (EXAMPLE)
    example_food1=Food(1000,-1,-1)
    example_food2=Food(100,-1,-1)

    # add the food objects together (EXAMPLE)
    feed = example_food1 + example_food2

    return feed

def available_grass():
    """
    Energy is expressed as digestible (DE), metabolizable (ME), or net energy (NE) by considering the loss of energy during digestion and metabolism from gross energy (GE) in the feed, as follows:

    Gross energy (GE): the amount of energy in the feed.
    Digestible energy (DE): the amount of energy in the feed minus the amount of energy lost in the feces.
    Metabolizable energy (ME): the amount of energy in the feed minus the energy lost in the feces and urine.
    Net energy (NE): the amount of energy in the feed minus the energy lost in the feces, urine, and in heat production through digestive and metabolic processes, i.e. heat increment.
    """

    # calculate available grass
    # import grass data

    # convert grass to animal feed
    # units idealy in kcal
    # all imports should be in GE, gross energy
    # calacuklation of NE is done in the feed animals function
    grass=Food(1000,-1,-1)

    return grass

def feed_animals(animal_list, available_feed, available_grass):
    """
    This function will feed the animals
    It will do so by allocating the grass first to those animals that can eat it,
    and then allocating the remaining feed to the remaining animals

    It will also priotiise the animals that are most efficient at converting feed,
    This means starting with milk.

    List needs to be sorted in the oprder you want the animals to be prioritised for feed
    """

    # grass to rumiants, milk first
    # feed to milk animals
    for milk_animal in milk_animals:
        # print(f"trying to feed grass to " + milk_animal.animal_type)
        available_grass = milk_animal.feed_the_species(available_grass)
    
    for milk_animal in milk_animals:
        # print(f"trying to feed feed to " + milk_animal.animal_type)
        available_feed = milk_animal.feed_the_species(available_feed)

    for ruminant in non_milk_ruminants:
        # print(f"trying to feed grass to " + ruminant.animal_type)
        available_grass = ruminant.feed_the_species(available_grass)

    for non_milk_animal in non_milk_animals:
        # print(f"trying to feed feed to " + non_milk_animal.animal_type)
        available_feed = non_milk_animal.feed_the_species(available_feed)

    return available_feed, available_grass




def change_in_animal_population(animal_object,current_month, spare_slaughter_hours, target_animal_population=0):
    """
    
    This function will calculate the change in animal population for a given animal type
    It will do so by calculating the number of new births, the number of deaths, and the number of animals slaughtered
    It will then update the animal object with the new population

    It will also update the animal object with the number of animals that are pregnant, and the number of animals that are lactating

    Some parameters are calulctaed before the 'slaughter event' where the populations change, some are calculated after
    Those that are calulcated before are:
        - the new births this month (based on the number of animals that are pregnant)
        - other deaths this month
        - the slauhter rate this month  
        - spare slaughter hours this month
    Those that are calculated after are:
        - the number of animals that are lactating
        - the new population this month
        - the population of animals that are pregnant for next month


    Parameters
    ----------
    animal_object : AnimalSpecies
        The animal object for the animal type that you want to calculate the change in population for
    current_month : int 
        The current month of the model
    spare_slaughter_hours : float
        The number of spare slaughter hours available this month
    target_animal_population : int, optional
        The target animal population for this animal type, by default 0

    Returns
    -------
    animal_object : AnimalSpecies
        The updated animal object for the animal type that you want to calculate the change in population for
    spare_slaughter_hours : float
        The number of spare slaughter hours available this month

    """

    # if non milk animal
    if animal_object.animal_function != "milk":
        spare_slaughter_hours = calculate_meat_change_in_population(animal_object,current_month, spare_slaughter_hours, target_animal_population)
    # if milk animal
    else:
        # calculate pops
        spare_slaughter_hours = calculate_milk_change_in_population(animal_object,current_month, spare_slaughter_hours, target_animal_population)
        # do transfer of retired milk animlas to meat

    return animal_object.retiring_milk_animals[-1], spare_slaughter_hours



def calculate_milk_change_in_population(animal_object,current_month, spare_slaughter_hours, target_animal_population):
    # First, check if breeding intervention has kicked in (based on gestation period)
    # If so, bring the reduction in breeding into impact the new births
    # Also turn off the need to slaughter pregnant animals (as we have already reduced the pregnant animals through the breeding intervention)
    if np.abs(current_month - animal_object.gestation) <= 0.5:
        calculate_breeding_changes(animal_object)

    # Calculate the number of new animals born this month given the number of pregnant animals
    # (must run after calculate_breeding_changes and pregnant animals)
    # MILK only half of new births will be milk animals
    new_births_animals_month = calculate_births(animal_object)
    new_births_meat_animals = new_births_animals_month * 0.5
    new_births_milk_animals = new_births_animals_month * 0.5
    retiring_animals = calculate_retiring_milk_animals(animal_object)
    # this Is mkind of broken, but it's definitely TODO broken at line 133 in the if statement doubling the breeding



    # Calculate other deaths
    new_other_animal_death = calculate_other_deaths(animal_object)

    # Determine slaughter rates (USE spare slaughter hours)
    # Each call of this function is "greedy" and will take as many slaughter hours as possible until the species is at the target population
    # This means that the slaughter hours are used in the order that the species are listed in the animal_types list
    new_slaughter_rate, spare_slaughter_hours = calculate_slaughter_rate(animal_object, spare_slaughter_hours, target_animal_population, new_births_milk_animals, new_other_animal_death)

    # retiring milk animals (if they are too old)
    # they turn in to meat animls, returned from this function as an int
    new_retiring_milk_animals = calculate_retiring_milk_animals(animal_object)

    # This is the main calculation of the population
    new_animal_population = calculate_animal_population(animal_object, new_births_milk_animals, new_other_animal_death, new_slaughter_rate)
    new_animal_population -= new_retiring_milk_animals

    # Determine how many of the animals who died this month were pregnant
    # Check if the number of pregnant animals set for slaughter is less than the number of animals slaughtered this month
    # If so, proceed to calculate the number of pregnant animals slaughtered
    # Otherwise, set the number of pregnant animals slaughtered to the number of animals slaughtered this month
    new_pregnant_animals_total, new_slaughtered_pregnant_animals = calculate_pregnant_slaughter(animal_object, new_slaughter_rate)

    # Calculate the number of pregnant animals birthing this month, based on the number of pregnant animals remaining
    # This is effectively the pregnant animals _next_ month
    new_pregnant_animals_birthing = calculate_pregnant_animals_birthing(animal_object, new_pregnant_animals_total)


    # quick check to fix any overshoots
    if new_pregnant_animals_total < 0: # this is to avoid negative numbers of pregnant animals
        new_pregnant_animals_total = 0

    if new_animal_population < target_animal_population:
        new_animal_population = target_animal_population


    # don't need to return much as the animal object is passed by reference, so the changes are made to the object itself
    # just need to return the spare slaughter hours

    # append new values to the animal object
    animal_object.population.append(new_animal_population)
    animal_object.slaughter.append(new_slaughter_rate)
    animal_object.pregnant_animals_total.append(new_pregnant_animals_total)
    animal_object.pregnant_animals_birthing_this_month.append(new_pregnant_animals_birthing)
    animal_object.other_animal_death.append(new_other_animal_death)
    animal_object.slaughtered_pregnant_animals.append(new_slaughtered_pregnant_animals)
    animal_object.retiring_milk_animals.append(new_retiring_milk_animals)

    return spare_slaughter_hours

def calculate_meat_change_in_population(animal_object,current_month, spare_slaughter_hours, target_animal_population):
    # First, check if breeding intervention has kicked in (based on gestation period)
    # If so, bring the reduction in breeding into impact the new births
    # Also turn off the need to slaughter pregnant animals (as we have already reduced the pregnant animals through the breeding intervention)
    if np.abs(current_month - animal_object.gestation) <= 0.5:
        calculate_breeding_changes(animal_object)

    # Calculate the number of new animals born this month given the number of pregnant animals
    # (must run after calculate_breeding_changes and pregnant animals)
    new_births_animals_month = calculate_births(animal_object)

    # Calculate other deaths
    new_other_animal_death = calculate_other_deaths(animal_object)

    # Determine slaughter rates (USE spare slaughter hours)
    # Each call of this function is "greedy" and will take as many slaughter hours as possible until the species is at the target population
    # This means that the slaughter hours are used in the order that the species are listed in the animal_types list
    new_slaughter_rate, spare_slaughter_hours = calculate_slaughter_rate(animal_object, spare_slaughter_hours, target_animal_population, new_births_animals_month, new_other_animal_death)

    # This is the main calculation of the population
    new_animal_population = calculate_animal_population(animal_object, new_births_animals_month, new_other_animal_death, new_slaughter_rate)

    # Determine how many of the animals who died this month were pregnant
    # Check if the number of pregnant animals set for slaughter is less than the number of animals slaughtered this month
    # If so, proceed to calculate the number of pregnant animals slaughtered
    # Otherwise, set the number of pregnant animals slaughtered to the number of animals slaughtered this month
    new_pregnant_animals_total, new_slaughtered_pregnant_animals = calculate_pregnant_slaughter(animal_object, new_slaughter_rate)

    # Calculate the number of pregnant animals birthing this month, based on the number of pregnant animals remaining
    # This is effectively the pregnant animals _next_ month
    new_pregnant_animals_birthing = calculate_pregnant_animals_birthing(animal_object, new_pregnant_animals_total)

    

    # quick check to fix any overshoots
    if new_pregnant_animals_total < 0: # this is to avoid negative numbers of pregnant animals
        new_pregnant_animals_total = 0

    if new_animal_population < target_animal_population:
        new_animal_population = target_animal_population


    # don't need to return much as the animal object is passed by reference, so the changes are made to the object itself
    # just need to return the spare slaughter hours

    # append new values to the animal object
    animal_object.population.append(new_animal_population)
    animal_object.slaughter.append(new_slaughter_rate)
    animal_object.pregnant_animals_total.append(new_pregnant_animals_total)
    animal_object.pregnant_animals_birthing_this_month.append(new_pregnant_animals_birthing)
    animal_object.other_animal_death.append(new_other_animal_death)
    animal_object.slaughtered_pregnant_animals.append(new_slaughtered_pregnant_animals)

    return spare_slaughter_hours



def calculate_pregnant_animals_birthing(animal_object, new_pregnant_animals_total):
    """
    
    This function will calculate the number of pregnant animals birthing this month, based on the number of pregnant animals remaining
    Uses a simple calculation of the number of pregnant animals divided by the gestation period
    This is not a perfect calculation, as it assumes that an even distribution of animals will birth each month
    However, it is a good approximation for the purposes of this model

    Parameters
    ----------
    animal_object : AnimalSpecies
        The animal object for the animal type that you want to calculate the change in population for
    new_pregnant_animals_total : int
        The number of pregnant animals remaining this month

    Returns
    -------
    new_pregnant_animals_birthing_this_month : int
        The number of pregnant animals birthing this month

    """
    new_pregnant_animals_birthing_this_month = new_pregnant_animals_total / animal_object.gestation
    return new_pregnant_animals_birthing_this_month

def calculate_pregnant_slaughter(animal_object, new_slaughter_rate):
    """
    
    This function will determine how many of the animals who died this month were pregnant
    Check if the number of pregnant animals set for slaughter is less than the number of animals slaughtered this month
    If so, proceed to calculate the number of pregnant animals slaughtered
    Otherwise, set the number of pregnant animals slaughtered to the number of animals slaughtered this month

    """
    new_pregnant_animals_total = animal_object.pregnant_animals_total[-1]
    if animal_object.pregnant_animal_slaughter_percent * animal_object.pregnant_animals_total[-1]  < new_slaughter_rate:
        new_slaughtered_pregnant_animals = animal_object.pregnant_animal_slaughter_percent * animal_object.pregnant_animals_total[-1]
        new_pregnant_animals_total -= ( 
            new_slaughtered_pregnant_animals +
            animal_object.other_animal_death_rate_monthly * animal_object.pregnant_animals_total[-1]
        )
    else:
        new_slaughtered_pregnant_animals = new_slaughter_rate
        new_pregnant_animals_total -= new_slaughtered_pregnant_animals
    return new_pregnant_animals_total,new_slaughtered_pregnant_animals

def calculate_animal_population(animal_object, new_births_animals_month, new_other_animal_death, new_slaughter_rate):
    new_animal_population = animal_object.population[-1]  - new_slaughter_rate - new_other_animal_death + new_births_animals_month
    return new_animal_population

def calculate_retiring_milk_animals(animal_object):
    """
    This function calculates the number of animals retiring from milk production this month
    
    Parameters
    ----------
    animal_object : object
        The animal object that is being calculated

    Returns
    -------
    new_retiring_milk_animals : int
        The number of animals retiring from milk production this month        
    """
    # calculate the number of animals retiring from milk production this month
    # this is the number of animals that are at the end of their productive life
    new_retiring_milk_animals = animal_object.population[-1] / animal_object.productive_milk_age_end
    return new_retiring_milk_animals

def calculate_births(animal_object):
    """
    This function calculates the number of new births this month
    
    Parameters
    ----------
    animal_object : object
        The animal object that is being calculated

    Returns
    -------
    new_births_animals_month : int
        The number of new births this month        
    """
    new_births_animals_month = animal_object.pregnant_animals_birthing_this_month[-1] * animal_object.animals_per_pregnancy
    return new_births_animals_month

def calculate_breeding_changes(animal_object):
    animal_object.pregnant_animals_birthing_this_month[-1] *= 1 - animal_object.reduction_in_animal_breeding #consider doing this as a list? 
    animal_object.pregnant_animals_total[-1] *= 1 - animal_object.reduction_in_animal_breeding #consider doing this as a list? 
    animal_object.pregnant_animal_slaughter_percent = 0 # this seems a bit risky for the mode, it's simplistic
    return 

def calculate_other_deaths(animal_object):
    new_other_animal_death = animal_object.population[-1] * animal_object.other_animal_death_rate_monthly
    return new_other_animal_death


def calculate_slaughter_rate(animal_object, spare_slaughter_hours, target_animal_population, new_births_animals_month, new_other_animal_death):
    """
    This function calculates the new slaughter rate based on the spare slaughter hours and the target animal population

    Parameters
    ----------
    animal_object : object
        The animal object that is being calculated
    spare_slaughter_hours : int
        The number of spare slaughter hours generated
    target_animal_population : int
        The target animal population

    Returns
    -------
    new_slaughter_rate : int
        The new slaughter rate
    spare_slaughter_hours : int
        The number of spare slaughter hours remaining after the new slaughter rate is calculated

    """
    # for dealing with milk, if slaughter hours is nan, then set it to 0
    if np.isnan(animal_object.slaughter[-1]):
        print('slaughter hours is nan')
        animal_object.slaughter[-1] = 0 
        new_slaughter_rate = 0
        return new_slaughter_rate, spare_slaughter_hours
    
    else:
        print(animal_object.slaughter[-1])
        # if there are no spare slaughter hours, then set the slaughter rate to the previous slaughter rate, this will 
        # will happen becuase the numerator will be 0
        new_slaughter_rate = animal_object.slaughter[-1] + round(spare_slaughter_hours/animal_object.animal_slaughter_hours)
        spare_slaughter_hours = 0

        # if population will be below target, then slaughter rate is set to the difference and the new births minus other deaths
        if animal_object.population[-1]-new_slaughter_rate < target_animal_population + new_births_animals_month - new_other_animal_death:
            new_slaughter_rate = animal_object.population[-1] - target_animal_population + new_births_animals_month - new_other_animal_death
            # spare slaugthter hours ae calculated based on the new (reduced) slaughter rate
            spare_slaughter_hours = (
                abs(new_slaughter_rate - animal_object.slaughter[-1])
            ) * animal_object.animal_slaughter_hours

        return new_slaughter_rate, spare_slaughter_hours


## At the end of the month, reset the feed balance with the new popluaton and feed required


def main(country_code):
    """
    Main function to be called by the user. This function will call the other functions in this file.
    """

# if __name__ == "__main__":
#     main("USA")


country_code="AUS"


## IMPORT DATA

# read animal population data
df_animal_stock_info = read_animal_population_data()

# read animal nutrition data
df_animal_attributes = read_animal_nutrition_data()


df_animal_options = read_animal_options()


## Populate animal objects ##

# create animal objects
animal_list = create_animal_objects(df_animal_stock_info.loc[country_code], df_animal_attributes)

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
milk_animals = [animal for animal in animal_dict.values() if "milk" in animal.animal_type]
# get list of non-milk animals
non_milk_animals = [animal for animal in animal_dict.values() if "milk" not in animal.animal_type]
# non milk runminants
non_milk_ruminants = [animal for animal in animal_dict.values() if "milk" not in animal.animal_type and animal.digestion_type == "ruminant"]
# get list of all ruminants
ruminants = [animal for animal in animal_dict.values() if animal.digestion_type == "ruminant"]
# get list of non-ruminants
non_ruminants = [animal for animal in animal_dict.values() if animal.digestion_type != "ruminant"]
# all animals
all_animals = [animal for animal in animal_dict.values()]

## Do the feeding
# feed the animals
feed_MJ_available_this_month, grass_MJ_available_this_month = feed_animals(animal_dict, feed_MJ_available_this_month, grass_MJ_available_this_month)

## OKAY SO NOW WE HAVE THE ANIMALS FED, WE NEED TO LOOK AT SLAUGHTERING

update_animal_objects_with_slaughter(all_animals,df_animal_attributes,df_animal_options)
update_animal_objects_with_milk(milk_animals,df_animal_attributes)



spare_slaughter_hours = 0 
for month in range(0,12):
    for animal in all_animals:
        retired_animals, spare_slaughter_hours = change_in_animal_population(animal,month,spare_slaughter_hours,0) # TARGET POPS IS BROKEN
        # if milk animal, update corresponding meat animal with theadded population from the retired animals
        if animal.animal_type == 'milk':
            for meat_animal in non_milk_animals:
                if meat_animal.animal_type == animal.animal_type.replace('milk','meat'):
                    meat_animal.population[month] += retired_animals


#plot the results
for animal in all_animals:
    plt.plot(animal.population, label=animal.animal_type)
plt.legend()
plt.show()
