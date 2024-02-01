"""Function which initiliases all of the animal population data Working file for now, may be broken up.

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

# TODO:
 # check that we line up with actual FAO usage. Do this straight away, and then consider doing it after adjysting for the LSU variation
 # fix the transfer births, milk behaving weirdly
 # DONE: fixed the milk birth... as animals need to give birth constantly to produce milk. THis is now refectyed
 # fix the pregannt population to be effected by homekill and other death from starvation (currently only effected by slaughter)
 # how to allocate when human edible feed is sent to animals? 20% starvation?
 # change how feed is attributed, make the DI% occur in a modular way, remove from the feed required calauclations (use net energy there, not gross energy)

"""
from pathlib import Path
import pandas as pd
import git
from src.food_system.food import Food
import pdb
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import os
import numpy as np


"""
Start main function
"""


class CalculateFeedAndMeat:
    def __init__(self, country_code, available_feed, available_grass, scenario):
        """
        Call the main function to calculate the feed and meat produced

        all animals is a list of animal objects feed used is a food object (of length (NMONTHS)) grass used is a food
        object (of length (NMONTHS))
        """

        self.all_animals, self.feed_used, self.grass_used = main(
            country_code,
            available_feed,
            available_grass,
            scenario,
            remove_first_month=1,
        )
        fig = go.Figure()

        # plot all the animals without detail
        # exclude chicken from output list
        ignore_chicken_graph = 0
        if ignore_chicken_graph == 1:
            animal_list = [
                animal
                for animal in self.all_animals
                if "chicken" not in animal.animal_type
            ]
        else:
            animal_list = [animal for animal in self.all_animals]

        for animal in animal_list:
            fig.add_trace(
                go.Scatter(
                    y=animal.slaughter,
                    mode="lines",
                    name=animal.animal_type + " slaughter",
                )
            )
            fig.add_trace(
                go.Scatter(
                    y=animal.population,
                    mode="lines",
                    name=animal.animal_type + " population",
                )
            )

        # fig2 = go.Figure()

        # # Plot one animal
        # k = 0
        # # Add detailed lines to the plot
        # fig2.add_trace(go.Scatter(y=animal_list[k].births_animals_month, mode="lines", name="births"))
        # fig2.add_trace(go.Scatter(y=animal_list[k].slaughter, mode="lines", name="slaughter"))
        # fig2.add_trace(go.Scatter(y=animal_list[k].total_homekill_this_month, mode="lines", name="homekill"))
        # fig2.add_trace(go.Scatter(y=animal_list[k].other_death_total, mode="lines", name="other death total"))
        # fig2.add_trace(go.Scatter(y=animal_list[k].population, mode="lines", name="population"))
        # fig2.add_trace(
        #     go.Scatter(y=animal_list[k].pregnant_animals_birthing_this_month, mode="lines", name="preg this month")
        # )
        # fig2.add_trace(go.Scatter(y=animal_list[k].pregnant_animals_total, mode="lines", name="preg total"))
        # fig2.add_trace(go.Scatter(y=animal_list[k].transfer_population, mode="lines", name="transfer pop"))
        # fig2.add_trace(go.Scatter(y=animal_list[k].transfer_births, mode="lines", name="transfer births"))

        # print("Baseline slaughter: ", animal_list[k].baseline_slaughter, animal_list[k].animal_type)
        # print("Target population: ", animal_list[k].target_population_head)
        # print(
        #     "Final population: ",
        #     animal_list[k].current_population,
        # )
        # # print("Difference: ", animal_list[k].current_population - animal_list[k].target_population_head)

        # # add title to the figure, and set the x axis title
        # fig2.update_layout(title=animal_list[k].animal_type, xaxis_title="Month")

        # # Show figures
        # fig2.show()
        # fig.show()

    def get_meat_produced(self):
        # set monthly values to zero with one example object from  all_animals
        # (all such objects should be same number of months)
        animals_killed_for_meat_small = np.zeros(len(self.all_animals[0].slaughter))
        animals_killed_for_meat_medium = np.zeros(len(self.all_animals[0].slaughter))
        animals_killed_for_meat_large = np.zeros(len(self.all_animals[0].slaughter))
        # add up all the numbers of animals slaughtered and feed

        # get the total slaughter by animal size from the all_animals list of animal objects
        for animal in self.all_animals:
            if animal.animal_size == "small":
                animals_killed_for_meat_small += np.array(
                    animal.slaughter
                )  # + np.array(animal.total_homekill_this_month))
            elif animal.animal_size == "medium":
                animals_killed_for_meat_medium += np.array(
                    animal.slaughter
                )  # + np.array(animal.total_homekill_this_month))
            elif animal.animal_size == "large":
                animals_killed_for_meat_large += np.array(
                    animal.slaughter
                )  # + np.array(animal.total_homekill_this_month))

        SHOW_ANIMAL_SLAUGHTER_PLOT = False
        if SHOW_ANIMAL_SLAUGHTER_PLOT:
            plt.figure()
            plt.title("animal slaughter")
            labels = []  # to collect labels for the legend
            for animal in self.all_animals:
                plt.plot(animal.slaughter)
                labels.append(animal.animal_type)
            plt.legend(labels)
            plt.show()

            plt.figure()
            plt.title("homekill")
            labels = []  # to collect labels for the legend
            for animal in self.all_animals:
                plt.plot(animal.total_homekill_this_month)
                labels.append(animal.animal_type)
            plt.legend(labels)
            plt.show()

            plt.figure()
            plt.title("animal pops ratio to beginning")
            labels = []  # to collect labels for the legend
            for animal in self.all_animals:
                plt.plot(animal.population / animal.population[0])
                labels.append(animal.animal_type)
            plt.legend(labels)
            plt.show()
        # convert the animals slaughtered list
        return (
            animals_killed_for_meat_small,
            animals_killed_for_meat_medium,
            animals_killed_for_meat_large,
        )

    def get_total_dairy_cows(self):
        # set to zero at first
        total_dairy_cows = np.zeros(len(self.all_animals[0].population))
        # print("total_dairy_cows")
        # print(len(total_dairy_cows))
        for animal in self.all_animals:
            # if animal.function == "milk":
            if animal.animal_type == "milk_cattle":
                # print("MILK COW len(animal.population)")
                # print(len(animal.population))
                total_dairy_cows += np.array(
                    animal.population
                )  # + np.array(animal.total_homekill_this_month))
        return total_dairy_cows


# create country calss to store country data in
class CountryData:
    """
    Main functionalities:
    CountryData is a class that represents data for a specific country in the food system model. It contains fields
    for various data points such as slaughter hours, homekill hours, and meat output. The class has methods
    for setting livestock unit factors, calculating homekill hours, and calculating total slaughter hours.

    Methods:
    - __init__(self, country_name): initializes the CountryData object with the given country name and sets
        various fields to empty lists or 0.
    - set_livestock_unit_factors(self, df_country_info, df_regional_conversion_factors): sets the
         LSU conversion factors for the country based on the given dataframes.
    - homekill_desperation_parameters(self): sets the homekill fraction and other death homekill rate.
    - calculate_homekill_hours(self): calculates the number of hours required to slaughter homekill animals.
    - calculate_total_slaughter_hours(self, all_animals): calculates the total slaughter hours for all animals in
        the given list.

    Fields:
    - country_name: the name of the country.
    - slaughter_hours: a list of total slaughter hours for each month.
    - homekill_hours_total_month: a list of total homekill hours for each month.
    - homekill_hours_budget: a list of budgeted homekill hours for each month.
    - meat_output: a list of meat output for each month.
    - spare_slaughter_hours: the number of spare slaughter hours for the country.
    - EK_region: the FAO region for the country.
    - LSU_conversion_factors: a dictionary of livestock unit conversion factors for the country.

    """

    def __init__(self, country_name):
        if not isinstance(country_name, str):
            raise TypeError("Country name must be a string")
        self.country_name = country_name
        self.slaughter_hours = []
        self.homekill_hours_total_month = []
        self.homekill_hours_budget = []
        self.meat_output = []
        self.spare_slaughter_hours = 0

    def set_livestock_unit_factors(
        self, df_country_info, df_regional_conversion_factors
    ):
        """Requires inputs of the country info dataframe, and the regional conversion factors dataframe
        df_regional_conversion_factors dataframe contains the conversion factors for the LSU for each animal type, based
        on ther region. And the other, df_country_info contains the mapping from the country to the region.

        Country Name needs to be the index of the df_country_info dataframe
        """

        # raise type error if the df_country_info is not a dtaaframe with alpha3 as the index
        if not isinstance(df_country_info, pd.DataFrame):
            raise TypeError("df_country_info must be a dataframe")
        if not isinstance(df_regional_conversion_factors, pd.DataFrame):
            raise TypeError("df_regional_conversion_factors must be a dataframe")
        if not isinstance(self.country_name, str):
            raise TypeError("Country name must be a string")
        # if country name not 3 letters, raise error
        if not self.country_name.isalpha():
            raise ValueError("Country name must be 3 letters")
        if len(self.country_name) != 3:
            raise ValueError("Country name must be 3 letters")

        # get region from country info dataframe
        try:
            self.EK_region = df_country_info[
                df_country_info.index == self.country_name
            ]["FAO-region-EK"].values[0]
        except BaseException:
            self.EK_region = "Other"

        # now given the region, get the conversion factors for the LSU
        # store them in a dict with the species:value format
        # in this imnstance, the columns are the regions and the index is the animal type (so the index needs to be
        # saved in to the dict as the 'species')
        try:
            conversion_factors = df_regional_conversion_factors[
                self.EK_region
            ].to_dict()
            self.LSU_conversion_factors = {
                key: value for key, value in conversion_factors.items()
            }
        except BaseException:
            raise ValueError(
                "Region not found in the regional conversion factors dataframe"
            )

    def homekill_desperation_parameters(self):
        """"""
        self.other_death_homekill_rate = 0.5  #
        self.homekill_fraction = (
            0.00  # fraction of population that is healthy that will be homekilled (max)
        )

    def calculate_homekill_hours(self):
        """Function to calculate the number of hours required to slaughter the homekill animals."""
        # TODO: bring in the population of the country here, and create an algo to work this out.
        # could also do it based off 'desperation' as in normal conditions, this will be very low/non-existant/illegal
        self.homekill_hours_total_month.append(10000)

    def calculate_total_slaughter_hours(self, all_animals):
        """Probably unneccesary, but could be sueful to ibnterogate the number of salughter hours to compare between
        countries.

        Not required for the program to work (and not called)
        """

        # same for slaughter hours
        slaughter_baseline = np.array(
            [animal.baseline_slaughter for animal in all_animals]
        )

        # multiply the slaughter baseline by the number of slaughter hours required per species (animal_slaughter_hours)
        slaughter_hours = np.array(
            [animal.animal_slaughter_hours for animal in all_animals]
        )

        # calculate the total slaughter hours by multiplying the animal population by the slaughter hours
        total_slaughter_hours = sum(
            np.array(slaughter_baseline) * np.array(slaughter_hours)
        )

        # append the total slaughter hours to the country data
        return total_slaughter_hours


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
        feed_balance : int
        Amount of feed required this month
        nutrition_ratio : object
        Object containing the nutrition ratio for the animal type

    """

    def __init__(self, animal_type, animal_species):
        # basic attributes
        self.animal_type = animal_type
        self.animal_species = animal_species

    # general method for updating attributes
    def update_attributes(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def set_animal_attributes(
        self,
        population,
        slaughter,
        animal_function,
        livestock_unit,
        digestion_type,
        animal_size,
        approximate_feed_conversion,
        digestion_efficiency_grass=0.6,
        digestion_efficiency_feed=0.8,
        carb_requirement=-1,
        protein_requirement=-1,
        fat_requirement=-1,
    ):
        if population < 0:
            raise ValueError("Population input must be non-negative")
        if slaughter < 0:
            raise ValueError("slaughter input must be non-negative")
        if livestock_unit < 0:
            raise ValueError("livestock_unit input must be non-negative")

        self.population = []  # this is a list so that it can be appended to later
        self.population_starving_pre_slaughter = (
            []
        )  # will be appended to, population - population fed each month.
        self.population_starving_month = []

        self.animal_size = animal_size
        self.current_population = population
        self.initital_population = population
        self.initial_slaughter = (
            slaughter / 12
        )  # static, initial value as it gets called to set other attributes.
        self.transfer_culling_fraction = 0.9  # what fraction of the transfer population is culled (i.e calves are killed and not counted in the slaughter stats)

        self.animal_function = animal_function
        # other slauhter attributes are set in a different function

        # FEED attributes
        self.livestock_unit = livestock_unit
        self.LSU_factor = 1  # default value gets set at init. In most scenarios this will be overwritten by "set_LSU_factor" function
        self.digestion_type = digestion_type
        self.approximate_feed_conversion = approximate_feed_conversion  # note this only used for ranking the efficiency, not used for calculating the feed required
        self.digestion_efficiency = {
            "grass": digestion_efficiency_grass,
            "feed": digestion_efficiency_feed,
        }  # this is the conversion from gross energy to net energy
        self.population_fed = 0  # a variable to store the number of animals fed this month, overwritten and not a list (useful for handling the case where animals are fed more than once per month (i.e a ruminent eats grass and grain))

        # slaughtering attributes
        if slaughter > 0:
            self.statistical_lifetime = (
                population / slaughter
            )  # this is the statistical lifetime of the animal, used to calculate the number of animals slaughtered per month

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

    def set_LSU_attributes(self, country_object):
        self.LSU_factor = country_object.LSU_conversion_factors[self.animal_species]
        self.NE_balance = (
            self.reset_NE_balance()
        )  # this is the feed required per month for the species

    def set_species_milk_attributes(
        self,
        productive_milk_age_start,
        productive_milk_age_end,
        insemination_cycle_time_for_milk,
        milk_production_per_month_per_head=None,
    ):
        # check that the population exists
        if not hasattr(self, "current_population"):
            raise AttributeError(
                "Population must be set before milk attributes can be set"
            )
        if productive_milk_age_start < 0 or productive_milk_age_end < 0:
            raise ValueError("milk age input must be non-negative")
        if productive_milk_age_end < productive_milk_age_start:
            raise ValueError("milk age end must be greater than milk age start")

        self.retiring_milk_animals = []

        # Milk attributes
        self.productive_milk_age_start = productive_milk_age_start
        self.productive_milk_age_end = productive_milk_age_end
        self.insemination_cycle_time_for_milk = insemination_cycle_time_for_milk
        self.population_proportion_productive_milk = (
            productive_milk_age_end - productive_milk_age_start
        ) / productive_milk_age_end
        self.population_producing_milk = (
            self.current_population * self.population_proportion_productive_milk
        )
        self.milk_production_per_month_per_head = (
            milk_production_per_month_per_head  # update to include this in the csv file
        )
        self.statistical_lifetime = productive_milk_age_end
        self.retiring_milk_animals_fraction = (1 / productive_milk_age_end) / 12

    def retiring_milk_head_monthly(self):
        """
        Function to calculate the number of retiring milk animals per month
        """
        return self.current_population * self.retiring_milk_animals_fraction

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
        starvation_death_fraction,
        transfer_births_or_head,
    ):
        """
        Function to set the attributes of the animal species that are related to slaughter

        Parameters
        ----------
        gestation : int
            gestation period in months
        other_animal_death_rate_annual : float
            annual death rate of animals
        animals_per_pregnancy : int
            number of animals per pregnancy
        animal_slaughter_hours : int
            hours per animal spent slaughtering
        change_in_slaughter_rate : float
            change in slaughter rate (a static value, given by assumptions of loss of industry etc...), 1 = no change, 0.5 = half of animals slaughtered
        pregnant_animal_slaughter_fraction : float
            this is the fraction of pregnant animals that are attempted to be slaughtered each month, 1= all pregnant animals are attempted to be slaughtered, 0.5 = half of pregnant animals
        reduction_in_animal_breeding : float
            this is the reduction in animal breeding (a static value, given by assumptions of loss of industry etc...) 1 = no reduction, 0.5 = half of animals are bred
        target_population_fraction : float
            this is the target population fraction (a static value, given by assumptions of loss of industry etc...) 1 = target population is equal to the iniitla population, 0 = targetting to kill all animals
        transfer_births_or_head : int
            this is head of increased population due to either male offspring of milk animals being added toa meat population or head imported from other countries

        Returns
        -------
        None


        """
        if not hasattr(self, "current_population"):
            raise AttributeError(
                "Population must be set before slaughter attributes can be set"
            )
        if reduction_in_animal_breeding < 0 or reduction_in_animal_breeding > 1:
            raise ValueError("reduction in animal breeding must be between 0 and 1")
        if target_population_fraction < 0:
            raise ValueError("target population fraction must be non-negative")
        if (
            pregnant_animal_slaughter_fraction < 0
            or pregnant_animal_slaughter_fraction > 1
        ):
            raise ValueError(
                "pregnant animal slaughter fraction must be between 0 and 1"
            )
        if change_in_slaughter_rate < 0:
            raise ValueError("change in slaughter rate must be non-negative")
        if other_animal_death_rate_annual < 0:
            raise ValueError("other animal death rate must be non-negative")
        if animals_per_pregnancy < 0:
            raise ValueError("animals per pregnancy must be non-negative")
        if animal_slaughter_hours < 0:
            raise ValueError("animal slaughter hours must be non-negative")
        if gestation < 0:
            raise ValueError("gestation must be non-negative")
        if starvation_death_fraction < 0 or starvation_death_fraction > 1:
            raise ValueError("starvation death fraction must be between 0 and 1")
        # transfer births can be negative or positive

        self.other_death_causes_other_than_starving = (
            []
        )  # this is calculated now, as it occurs BEFORE the first month (i.e is independent of feed)
        self.other_death_starving = (
            []
        )  # this one starts empty because it is worked out AFTER the first month
        self.other_death_total = []
        self.slaughter = []  # is list
        self.births_animals_month = []
        self.pregnant_animals_birthing_this_month = []
        self.pregnant_animals_total = []
        self.slaughtered_pregnant_animals = []
        self.transfer_population = (
            []
        )  # positive means animals transferred IN from, milk, negative means animals transferred OUT (i.e milk animals should always have a negative IF treansfer population is only related to male dairy animals). Could be psotivie IF transfer population is used to capture live imported head from somewhere
        self.transfer_births = []

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
        self.baseline_slaughter = (
            self.initial_slaughter * change_in_slaughter_rate
        )  # is list

        # options of the scenario
        self.pregnant_animal_slaughter_fraction = pregnant_animal_slaughter_fraction  # this is the fraction of pregnant animals that are attempted to be slaughtered each month
        self.reduction_in_animal_breeding = reduction_in_animal_breeding
        self.target_population_fraction = target_population_fraction  # acts as a minimum, will not be used to increase pops in current version
        self.target_population_head = (
            self.target_population_fraction * self.initital_population
        )  # this is the target population head, used to calculate the number of animals slaughtered per month
        # calculations based off of the above
        self.other_animal_death_rate_monthly = other_animal_death_rate_annual / 12
        self.other_animal_death_basline_head_monthly = (
            self.other_animal_death_rate_monthly * self.initital_population
        )

        if self.animal_function == "milk":
            self.birth_ratio = 2  # number of (total) animals born per milk animal. E.g as all milk animals are female, and 50% of births are female, then 2 = milk animal, and 1 = meat animal
            # births_animals_month_baseline is the number of female milk animals born. NOT total births.
            self.births_animals_month_baseline = (
                (1 / self.insemination_cycle_time_for_milk)
                * (self.population_producing_milk)
                * (1 / self.birth_ratio)  # does this do nothing now? BUG
            )  # SET MILK BIRTHS HERE # if a milk animal, this is JUST the milk animals born (meat transfer accounted for in pregnancy attribute)
        else:
            self.birth_ratio = 1  # number of animals born (total from population) per milk animal. I.e all male milk animals are not considered milk anaimls and need to be moved over to meat
            self.births_animals_month_baseline = (
                self.other_animal_death_basline_head_monthly
                + self.initial_slaughter
                - transfer_births_or_head
            )
            assert (
                self.births_animals_month_baseline >= 0
            ), "births_animals_month_baseline is negative, this is probably because transfer births are too high or slaughter too low - check the data inputs"
            # if a milk animal, this is JUST the milk animals born (meat transfer accounted for in pregnancy attribute)

        # next we need add slaughter to milk animals to account for calf culling
        if self.animal_function == "milk":
            calf_slaughter = (
                self.births_animals_month_baseline * 2
                - transfer_births_or_head
                - self.other_animal_death_basline_head_monthly
            )  ## DESCIBR WHY 2x HERE. BEcause of transfer pop already having births. (So need to add them in again otherwise this goes negative)
            self.initial_slaughter += calf_slaughter
            self.baseline_slaughter = (
                self.initial_slaughter * change_in_slaughter_rate
            )  # is list

        # positive means animals transferred IN from, milk, negative means animals transferred OUT (i.e milk animals should always have a negative IF treansfer population is only related to male dairy animals). Could be psotivie IF transfer population is used to capture live imported head from somewhere
        # pregnant_animals_total_baseline is the TOTAL number of pregnant animals (regardless of whether the offspring will be female or male)
        self.pregnant_animals_total_baseline = (
            self.birth_ratio
            * self.births_animals_month_baseline
            / self.animals_per_pregnancy
            * self.gestation
        )  # assumes even distribution of births, this is not true. OPTIONAL TODO, update this to be more accurate and deal with seasonal births. Can be done by chaning the "gestation" to be a complicated value based on month/season
        self.pregnant_animals_birthing_this_month_baseline = (
            self.pregnant_animals_total_baseline / self.gestation
        )
        self.slaughtered_pregnant_animals_baseline = (
            self.births_animals_month_baseline * pregnant_animal_slaughter_fraction
        )

        # Homekill
        self.homekill_other_death_this_month = []
        self.homekill_healthy_this_month = []
        self.homekill_starving_this_month = []
        self.total_homekill_this_month = []

        # starvation
        self.starvation_death_fraction = starvation_death_fraction

        return

    def set_milk_birth(self):
        # number of (total) animals born per milk animal.
        # E.g as all milk animals are female, and 50% of births are female, then 2 = milk animal, and 1 = meat animal
        self.birth_ratio = 2
        # births_animals_month_baseline is the number of female milk animals born. NOT total births.
        # SET MILK BIRTHS HERE
        # if a milk animal, this is JUST the milk animals born (meat transfer accounted for in pregnancy attribute)
        self.births_animals_month_baseline = (
            (1 / self.insemination_cycle_time_for_milk)
            * (self.population_producing_milk)
            * (1 / self.birth_ratio)  # does this do nothing now? BUG
        )

    def set_initial_milk_transfer(self):
        retiring_milk_first_month = (
            self.retiring_milk_animals_fraction * self.initital_population
        )
        transfer_pop = self.births_animals_month_baseline + retiring_milk_first_month
        return transfer_pop * (
            1 - self.transfer_culling_fraction
        )  # add in the culling fraction here

    def total_homekill(self):
        """Function to calculate the total homekill per month.

        Parameters
        ----------
        None

        Returns
        -------
        total_homekill : int
            the total homekill per month
        """

        total_homekill = (
            self.homekill_other_death_this_month[-1]
            + self.homekill_healthy_this_month[-1]
            + self.homekill_starving_this_month[-1]
        )

        return total_homekill

    def exported_births(self):
        """Function to calculate the number of births exported from the animal population.

        Parameters
        ----------
        None

        Returns
        -------
        exported_births : int
            the number of births exported from the animal population
        """

        exported_births = self.births_animals_month * (self.birth_ratio - 1)

        return exported_births

    def one_LSU_monthly_billion_kcal(self):
        # Livestock unit calculation: a method based on energy requirements to refine the study of livestock farming systems
        # NRAE Prod. Anim., 2021, 34 (2), 139e-160e
        # https://productions-animales.org/article/view/4855/17716

        one_year_NEt = 29000  # MJ per year NEt = Net Energy Total (MJ/year)

        # one billion kcals is the default unit for the food object
        # 1*10^9 kcal = 1 billion kcal = 1*10^6 Mcal

        # convert to billion kcals
        one_LSU_monthly_billion_kcal = (
            ((one_year_NEt / 12) / 4.187) * 1000 / 1e9
        )  # 12 months ina  year, 4.187 to convert to kcal, 1000 to convert to kcal from Mcal
        return one_LSU_monthly_billion_kcal

    def net_energy_required_per_month(self):
        """
        Function to calculate the total net energy required per month for the species
        """

        return (
            self.livestock_unit * self.one_LSU_monthly_billion_kcal() * self.LSU_factor
        )

    def net_energy_required_per_species(self):
        """
        Function to calculate the total net energy required per month for the species
        """

        return self.net_energy_required_per_month() * self.current_population

    def reset_NE_balance(self):
        """
        This function resets the feed balance to the feed required per month for the species
        Needs to be run before feeding the animals each month.

        """
        self.NE_balance = Food(
            self.net_energy_required_per_species(), 0, 0
        )  # this is the feed required per month for the species

    def feed_the_species(self, food_input, feed_type="feed"):
        """
        Main function to feed the species

        Attempts to work with a food object with all three macros and one with only kcals
        Not tested with the three macros, and also not sure how to handle fungibility of macros

        Also, some confusion currently with what to expect as an input, will it be a food object with numpy lists?
        Or will it be a food object with a single value? Single value is good, but the nature of the object
        is that it is passed as a reference, so it will be changed in this function. This is not ideal.

        Anyway, this works for now but will require attention to properly integrate with the rest of the model

        Parameters
        ----------
        food_input : Food
            the food object to be used to feed the species - currently assumed to be a single value (not numpy list)

        Returns
        -------
        food_input : Food
            the food object after feeding the species

        Also updates the population_fed variable


        """
        # check that it is a valid food object
        if not isinstance(food_input, Food):
            raise TypeError("food_input is not a Food object")

        # function to feed the species
        NE_required = self.NE_balance.kcals

        if NE_required == 0:
            # no food required
            # print('no food required for ' + self.animal_type)

            return food_input
        else:
            DI_for_species = self.digestion_efficiency[feed_type]
            NE_in_food = food_input.kcals * DI_for_species

            # only using kcals
            if NE_in_food > NE_required:
                # whole population is fed
                self.population_fed = self.current_population
                # update the food object
                NE_in_food -= NE_required
                self.NE_balance = Food(0, 0, 0)
                food_input.kcals = NE_in_food / DI_for_species

            else:
                # not enough food to feed the whole population
                # calculate the number of animals that can be fed
                self.population_fed = round(
                    NE_in_food / NE_required * self.current_population
                )
                # update the food object
                NE_required -= NE_in_food
                food_input.kcals = 0
                self.NE_balance = Food(NE_required, 0, 0)

        return food_input

    def append_month_zero(self):
        """
        Objective:
            - The objective of the 'append_month_zero' method is to append the baseline values of various attributes of the animal species to their respective lists. These values will be used as a reference point for future calculations.

        Inputs:
        - The method takes no external inputs. It uses the instance variables of the class 'AnimalSpecies' to calculate and append the baseline values.
        """

        # check attributes are not empty
        # check attributes are not empty
        # check if attributes exist
        if not hasattr(self, "current_population"):
            raise AttributeError(
                "current_population must be set before calling the append month zero"
            )
        if not hasattr(self, "other_animal_death_basline_head_monthly"):
            raise AttributeError(
                "other_animal_death_basline_head_monthly must be set before calling the append month zero"
            )
        if not hasattr(self, "births_animals_month_baseline"):
            raise AttributeError(
                "births_animals_month_baseline must be set before calling the append month zero"
            )
        if not hasattr(self, "initial_slaughter"):
            raise AttributeError(
                "initial_slaughter must be set before calling the append month zero"
            )
        if not hasattr(self, "pregnant_animals_total_baseline"):
            raise AttributeError(
                "pregnant_animals_total_baseline must be set before calling the append month zero"
            )
        if not hasattr(self, "pregnant_animals_birthing_this_month_baseline"):
            raise AttributeError(
                "pregnant_animals_birthing_this_month_baseline must be set before calling the append month zero"
            )
        if not hasattr(self, "population"):
            raise AttributeError(
                "population must be set before calling the append month zero"
            )
        if not hasattr(self, "other_death_causes_other_than_starving"):
            raise AttributeError(
                "other_death_causes_other_than_starving must be set before calling the append month zero"
            )
        if not hasattr(self, "other_death_total"):
            raise AttributeError(
                "other_death_total must be set before calling the append month zero"
            )
        if not hasattr(self, "births_animals_month"):
            raise AttributeError(
                "births_animals_month must be set before calling the append month zero"
            )
        if not hasattr(self, "slaughter"):
            raise AttributeError(
                "slaughter must be set before calling the append month zero"
            )
        if not hasattr(self, "pregnant_animals_total"):
            raise AttributeError(
                "pregnant_animals_total must be set before calling the append month zero"
            )
        if not hasattr(self, "pregnant_animals_birthing_this_month"):
            raise AttributeError(
                "pregnant_animals_birthing_this_month must be set before calling the append month zero"
            )
        if not hasattr(self, "transfer_population"):
            raise AttributeError(
                "transfer_population must be set before calling the append month zero"
            )
        if not hasattr(self, "transfer_births"):
            raise AttributeError(
                "transfer_births must be set before calling the append month zero"
            )
        if not hasattr(self, "slaughtered_pregnant_animals"):
            raise AttributeError(
                "slaughtered_pregnant_animals must be set before calling the append month zero"
            )
        if not hasattr(self, "population_starving_pre_slaughter"):
            raise AttributeError(
                "population_starving_pre_slaughter must be set before calling the append month zero"
            )
        if not hasattr(self, "population_starving_month"):
            raise AttributeError(
                "population_starving_month must be set before calling the append month zero"
            )
        if not hasattr(self, "other_death_starving"):
            raise AttributeError(
                "other_death_starving must be set before calling the append month zero"
            )
        if not hasattr(self, "homekill_other_death_this_month"):
            raise AttributeError(
                "homekill_other_death_this_month must be set before calling the append month zero"
            )
        if not hasattr(self, "homekill_healthy_this_month"):
            raise AttributeError(
                "homekill_healthy_this_month must be set before calling the append month zero"
            )
        if not hasattr(self, "homekill_starving_this_month"):
            raise AttributeError(
                "homekill_starving_this_month must be set before calling the append month zero"
            )
        if not hasattr(self, "total_homekill_this_month"):
            raise AttributeError(
                "total_homekill_this_month must be set before calling the append month zero"
            )

        ## FINISH ATTRIBUTE CHECKS HERE

        self.population += [self.current_population]
        self.other_death_causes_other_than_starving += [
            self.other_animal_death_basline_head_monthly
        ]
        self.other_death_total += [self.other_animal_death_basline_head_monthly]
        # self.births_animals_month += [self.births_animals_month_baseline]

        self.slaughter += [
            self.initial_slaughter
        ]  # probably should be "initial_slaughter"to reflect ex ante slaughter, but needs to be baseline (incoroprating slaughter changes), to work with the current model
        self.pregnant_animals_total += [self.pregnant_animals_total_baseline]
        self.pregnant_animals_birthing_this_month += [
            self.pregnant_animals_birthing_this_month_baseline
        ]

        # set arbitrary zereo values to the transfer variables as it does not impact
        self.transfer_population += []
        self.transfer_births += []

        # assume no slaughter of pregnant animals at baseline
        self.slaughtered_pregnant_animals += [0]

        # assume no starvation at baseline
        self.population_starving_pre_slaughter += [0]
        self.population_starving_month += [0]
        self.other_death_starving += [0]

        # assume no homekill at baseline
        self.homekill_other_death_this_month += [0]
        self.homekill_healthy_this_month += [0]
        self.homekill_starving_this_month += [0]
        self.total_homekill_this_month += [0]


class AnimalPopulation:
    def calculate_additive_births(animal, current_month):
        # First, check if breeding intervention has kicked in (based on gestation period)
        # If so, bring the reduction in breeding into impact the new births
        # Also turn off the need to slaughter pregnant animals (as we have already reduced the pregnant animals through the breeding intervention)
        if np.abs(current_month - animal.gestation) <= 0.5:
            AnimalPopulation.calculate_breeding_changes(animal)

        # Calculate the number of new animals born this month given the number of pregnant animals
        # (must run after calculate_breeding_changes)
        # MILK only half of new births will be milk animals (captured in export animals)
        new_births_animals_month, new_export_births = AnimalPopulation.calculate_births(
            animal
        )

        return new_births_animals_month, new_export_births

    def calculate_change_in_population(
        animal, country_object, new_additive_animals_month
    ):
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
        """
        if animal.animal_function == "milk":
            # they turn in to meat animls, this is done in a previous step already
            # incoming retiring animals (that is, those going from milk -> meat), are already contained in the
            # new_additive_animals_month variable
            retiring_animals = animal.retiring_milk_animals[-1]
            # problem here? TODO. THe problem could be that retiring milk anilas is gfreat than the population (and doesn't scale)
        else:
            retiring_animals = 0

        target_animal_population = animal.target_population_head

        # Calculate other deaths
        new_other_animal_death = AnimalPopulation.calculate_other_deaths(animal)

        # Determine slaughter rates (USE spare slaughter hours)
        # Each call of this function is "greedy" and will take as many slaughter hours as possible until the species is at the target population
        # This means that the slaughter hours are used in the order that the species are listed in the animal_types list
        current_slaughter_rate = AnimalPopulation.calculate_slaughter_rate(
            animal,
            country_object,
            new_additive_animals_month,
            new_other_animal_death,
        )

        # This is the main calculation of the population, update the slaughter rate if there are not enough animals
        current_slaughter_rate = AnimalPopulation.calculate_animal_population(
            animal,
            country_object,
            new_additive_animals_month,
            new_other_animal_death + retiring_animals,
            current_slaughter_rate,
        )  ##TODO BUG here, what happens if retiring animals is huge, then even at slaughter = 0 we will get to negative pop

        # Determine how many of the animals who died this month were pregnant
        # Check if the number of pregnant animals set for slaughter is less than the number of animals slaughtered this month
        # If so, proceed to calculate the number of pregnant animals slaughtered
        # Otherwise, set the number of pregnant animals slaughtered to the number of animals slaughtered this month
        (
            new_pregnant_animals_total,
            new_slaughtered_pregnant_animals,
        ) = AnimalPopulation.calculate_pregnant_slaughter(
            animal, current_slaughter_rate
        )

        # Calculate the number of pregnant animals birthing this month, based on the number of pregnant animals remaining
        # This is effectively the pregnant animals _next_ month
        new_pregnant_animals_birthing = (
            AnimalPopulation.calculate_pregnant_animals_birthing(
                animal, new_pregnant_animals_total
            )
        )

        # quick check to fix any overshoots
        if (
            new_pregnant_animals_total < 0
        ):  # this is to avoid negative numbers of pregnant animals
            new_pregnant_animals_total = 0

        # don't need to return much as the animal object is passed by reference, so the changes are made to the object itself
        # append new values to the animal object
        # don't append to population list, this is done after homekill in it's own fucntion
        animal.slaughter.append(current_slaughter_rate)
        animal.pregnant_animals_total.append(new_pregnant_animals_total)
        animal.pregnant_animals_birthing_this_month.append(
            new_pregnant_animals_birthing
        )
        animal.other_death_causes_other_than_starving.append(new_other_animal_death)
        animal.slaughtered_pregnant_animals.append(new_slaughtered_pregnant_animals)

        return

    def calculate_pregnant_animals_birthing(animal, new_pregnant_animals_total):
        """
        This function will calculate the number of pregnant animals birthing this month, based on the number of pregnant animals remaining
        Uses a simple calculation of the number of pregnant animals divided by the gestation period
        This is not a perfect calculation, as it assumes that an even distribution of animals will birth each month
        However, it is a good approximation for the purposes of this model

        Parameters
        ----------
        animal : AnimalSpecies
            The animal object for the animal type that you want to calculate the change in population for
        new_pregnant_animals_total : int
            The number of pregnant animals remaining this month

        Returns
        -------
        new_pregnant_animals_birthing_this_month : int
            The number of pregnant animals birthing this month

        """
        new_pregnant_animals_birthing_this_month = (
            new_pregnant_animals_total / animal.gestation
        )
        return new_pregnant_animals_birthing_this_month

    def calculate_pregnant_slaughter(animal, new_slaughter_rate):
        """

        This function will determine how many of the animals who died this month were pregnant
        Check if the number of pregnant animals set for slaughter is less than the number of animals slaughtered this month
        If so, proceed to calculate the number of pregnant animals slaughtered
        Otherwise, set the number of pregnant animals slaughtered to the number of animals slaughtered this month

        """

        new_pregnant_animals_total = animal.pregnant_animals_total[-1]
        # if the fraction of preg * total preg is less than the slaughter rate,
        # proceed as normal and reduce the number of pregnant animals by the slaughter farction
        if animal.pregnant_animal_slaughter_fraction == 0:
            new_slaughtered_pregnant_animals = 0
        elif (
            animal.pregnant_animal_slaughter_fraction
            * animal.pregnant_animals_total[-1]
            < new_slaughter_rate
        ):
            new_slaughtered_pregnant_animals = (
                animal.pregnant_animal_slaughter_fraction
                * animal.pregnant_animals_total[-1]
            )
            # subtract the number of slaughtered pregnant animals from the total number of pregnant animals
            # also subtract other_death
            new_pregnant_animals_total -= (
                new_slaughtered_pregnant_animals
                + animal.other_animal_death_rate_monthly
                * animal.pregnant_animals_total[-1]
            )
        else:
            new_slaughtered_pregnant_animals = new_slaughter_rate
            new_pregnant_animals_total -= new_slaughtered_pregnant_animals

        assert new_pregnant_animals_total >= 0, "new pregnant animals total is negative"
        assert (
            new_slaughtered_pregnant_animals >= 0
        ), "new slaughtered pregnant animals is negative"
        return new_pregnant_animals_total, new_slaughtered_pregnant_animals

    def calculate_animal_population(
        animal,
        country_object,
        new_additive_animals_month,
        new_other_animal_death,
        new_slaughter_rate,
    ):
        new_animal_population_pre_slaughter = (
            animal.current_population
            - new_other_animal_death
            + new_additive_animals_month
        )

        # check if the slaughtering is greater than the target population, create a temporary 'actual' rate.
        # usew this actual rate to calculate the number of animals slaughtered
        # and the difference between the actual and the previous slaughtering rate to calculate spare hours

        if new_animal_population_pre_slaughter < animal.target_population_head:
            # already below target, do no slaughtering
            actual_slaughter_rate = 0
        elif (
            new_animal_population_pre_slaughter - new_slaughter_rate
            < animal.target_population_head
        ):
            # contiuning to slaughter as planned would drop below target, modify slaughtering rate
            actual_slaughter_rate = (
                new_animal_population_pre_slaughter - animal.target_population_head
            )
        else:
            # no change to slaughtering rate required, will not dip below target rate
            actual_slaughter_rate = new_slaughter_rate

        # check if the actual slaughter rate is less than zero, if so, set it to zero
        if actual_slaughter_rate < 0:
            actual_slaughter_rate = 0

        country_object.spare_slaughter_hours = (
            new_slaughter_rate - actual_slaughter_rate
        ) * animal.animal_slaughter_hours

        animal.current_population = (
            new_animal_population_pre_slaughter - actual_slaughter_rate
        )
        # check if the population is below zero
        # BUG this might fix it, but will still overestimate the number of animals retiring (as they might be dead, not retiring (milk only))
        if animal.current_population < 0:
            animal.current_population = 0
            actual_slaughter_rate = 0

        return actual_slaughter_rate

    # def calculate_imported_and_transfer_population(animal):

    #     animal.transfer_births_or_head

    def calculate_births(animal):
        """
        This function calculates the number of new births this month

        Parameters
        ----------
        animal : object
            The animal object that is being calculated

        Returns
        -------
        new_births_animals_month : int
            The number of new births this month (just of this animal type i.e new biths ONLY realtes to milk births from milk animals, not total births (meat and milk))
        new_export_births_animals_month : int
            The number of new births that are exported this month (just of this animal type i.e new biths ONLY realtes to meat births from milk animals, not total births (meat and milk))
        """
        new_births_animals_month = (
            animal.pregnant_animals_birthing_this_month[-1]
            * animal.animals_per_pregnancy
        ) / animal.birth_ratio
        new_export_births_animals_month = new_births_animals_month * (
            animal.birth_ratio - 1
        )
        # new export births will be an optional return. Birth ratio is defined in the class
        # for milk animals "export births = new births" for meat animals "export births = 0"
        return new_births_animals_month, new_export_births_animals_month * (
            1 - animal.transfer_culling_fraction
        )  # added transfer culling fraction here, to represent culling of calves

    def calculate_breeding_changes(animal):
        """
        This function calculates the changes in breeding for the animal type
        This is *only* called after the gestation period is over
        It will update the animal object with the new number of pregnant animals
        Based on the reduction in breeding

        Pregnant slaughter is halted, as breeding changes have taken place from the breeding intervention

        Parameters
        ----------
        animal : object
            The animal object that is being calculated

        Returns
        -------
        None
        """

        animal.pregnant_animals_birthing_this_month[-1] *= (
            1 - animal.reduction_in_animal_breeding
        )  # consider doing this as a list?
        animal.pregnant_animals_total[-1] *= (
            1 - animal.reduction_in_animal_breeding
        )  # consider doing this as a list?
        animal.pregnant_animal_slaughter_fraction = (
            0  # this seems a bit risky for the mode, it's simplistic
        )
        return

    def calculate_other_deaths(animal):
        new_other_animal_death = (
            animal.current_population * animal.other_animal_death_rate_monthly
        )
        return new_other_animal_death

    def calculate_slaughter_rate(
        animal, country_object, new_births_animals_month, new_other_animal_death
    ):
        """
        This function calculates the new slaughter rate based on the spare slaughter hours and the target animal population

        Parameters
        ----------
        animal : object
            The animal object that is being calculated
        country_object.spare_slaughter_hours : int
            The number of spare slaughter hours generated
        target_animal_population : int
            The target animal population

        Returns
        -------
        new_slaughter_rate : int
            The new slaughter rate
        country_object.spare_slaughter_hours : int
            The number of spare slaughter hours remaining after the new slaughter rate is calculated

        """
        # 0th month is ex ante, so need a step change to change from "initial slaughter" to "baseline slaughter"
        if country_object.month == 0:
            current_slaughter = animal.baseline_slaughter
        else:
            current_slaughter = animal.slaughter[-1]
            # BUG do we need this^^^ ? baseline slaughter IS affected by the change in slaughter rate

        # for dealing with milk, if slaughter hours is nan, then set it to 0
        if np.isnan(current_slaughter):
            print("slaughter hours is nan")
            # animal.slaughter[-1] = 0
            new_slaughter_rate = 0
            return new_slaughter_rate

        else:
            # if there are no spare slaughter hours, then set the slaughter rate to the previous slaughter rate, this will
            # will happen becuase the numerator will be 0
            new_slaughter_rate = (
                current_slaughter
                + country_object.spare_slaughter_hours / animal.animal_slaughter_hours
            )
            country_object.spare_slaughter_hours = 0

            return new_slaughter_rate

    def calculate_other_death_homekill_head(animal, country_object):
        recoverable_meat_other_death_fraction = (
            country_object.other_death_homekill_rate
        )  # TODO this needs to be imported too from the model
        # set this yo ZERO to not recover any grom other death. Could also scale with #desperation
        other_death = animal.other_death_causes_other_than_starving[-1]
        max_homekill_head = other_death * recoverable_meat_other_death_fraction
        home_kill_capacity = (
            country_object.homekill_hours_budget[-1] / animal.animal_slaughter_hours
        )
        actual_homekill_head = min(max_homekill_head, home_kill_capacity)
        # the above is the actual homemkill, based on the homekill capacity and the max homekill head
        # max homemkill head is how many animals that died due to other causes can be homekilled/butchered/recovered
        # the the homekill capacity is the number of animals that can be homekilled based on the number of hours available
        # actual homekill head is the minimum of the two
        # don't remove the actual homekill from this fucntion from the population, as they were already dead

        animal.homekill_other_death_this_month.append(actual_homekill_head)
        country_object.homekill_hours_budget[-1] -= (
            actual_homekill_head * animal.animal_slaughter_hours
        )

    def calculate_healthy_homekill_head(animal, country_object):
        # population after slaughter
        starting_population = animal.current_population

        # TODO: update to inlcude a desperation metric @kevin @morgan
        # this desperation metric could act on the homekill fraction variable

        # homekill max slauhter species head
        home_kill_capacity = (
            country_object.homekill_hours_budget[-1] / animal.animal_slaughter_hours
        )

        # TODO can be replaced by directly importing a 'head' number too
        homekill_demand = country_object.homekill_fraction * starting_population

        # actual homekill head
        actual_homekill_head = min(homekill_demand, home_kill_capacity)

        # update animal object
        animal.homekill_healthy_this_month.append(actual_homekill_head)
        country_object.homekill_hours_budget[-1] -= (
            actual_homekill_head * animal.animal_slaughter_hours
        )

        return

    def calculate_starving_pop_post_slaughter_healthy_homekill(animal):
        # get the new starving population:
        starving_head_post_slaughter_and_healthy_homekill = (
            animal.population_starving_pre_slaughter[-1]
            - animal.slaughter[-1]
            - animal.homekill_healthy_this_month[-1]
        )

        if starving_head_post_slaughter_and_healthy_homekill < 0:
            starving_head_post_slaughter_and_healthy_homekill = 0
            # all the starving animals have been killed, so no starving animals are left

        return starving_head_post_slaughter_and_healthy_homekill
        # subtract starving population

    def calculate_starving_homekill_head(
        animal,
        country_object,
        population_starving_post_slaughter_and_healthy_homekill,
    ):
        # put any limitations of how many head can be slaughtered in here
        # probably none here as if they are starving, you'll want to slaughter them

        # homekill max slaughter species head
        home_kill_capacity = (
            country_object.homekill_hours_budget[-1] / animal.animal_slaughter_hours
        )
        max_homekill_head = population_starving_post_slaughter_and_healthy_homekill

        # check homekill capacity is not negative
        if home_kill_capacity < 0:
            home_kill_capacity = 0

        # assert home_kill_capacity >= 0
        # should be no way for this to be negative, as it is checked if there is sufficient capacity in the homekill healthy function
        # I guess if the capacity between homekill healthy and homemkill staving is different we should remove this assertion
        # this couold happen if we change 'desperation' to mean that people will 'find a way' despite the lack of capacity
        # seems quite realistic that this might happen, so have a low bar for updating this assertion and making a scaling factor or similar
        # to increase the slaughter capacity for the starving animals

        actual_homekill_head = min(max_homekill_head, home_kill_capacity)

        animal.homekill_starving_this_month.append(actual_homekill_head)
        country_object.homekill_hours_budget[-1] -= (
            actual_homekill_head * animal.animal_slaughter_hours
        )

        return

    def calculate_starving_pop_post_all_slaughter_homekill(
        animal, population_starving_post_slaughter_and_healthy_homekill
    ):
        # return zero if negative
        pop_starving = (
            population_starving_post_slaughter_and_healthy_homekill
            - animal.homekill_starving_this_month[-1]
        )

        return max(pop_starving, 0)

    def other_death_pregnant_adjustment(animal):
        # find proportion of population that has died from starvation
        # this is only relevant in non-baseline scenarios
        # the scenarios where this is relevant are:
        # rapid depop
        # trying to maintain a population with low food availability
        # where this just ruins things is:
        # baseline

        if animal.population[-1] == 0:
            other_death_fraction = 1
        else:
            other_death_fraction = animal.other_death_total[-1] / animal.population[-1]

        # use this to adjust the number of pregnant animals that die from starvation
        # this is done by multiplying the number of pregnant animals by the fraction of the population that died from starvation
        # this is a simple assumption that the number of pregnant animals that die from starvation is proportional to the number of animals that die from starvation
        # this is not a perfect assumption, but it is a good approximation for the purposes of this model
        pregnant_other_death = animal.pregnant_animals_total[-1] * other_death_fraction
        pregnant_birthing_this_month_other_death = (
            animal.pregnant_animals_birthing_this_month[-1] * other_death_fraction
        )

        # update the number of pregnant animals that die from starvation
        animal.pregnant_animals_total[-1] -= pregnant_other_death
        animal.pregnant_animals_birthing_this_month[
            -1
        ] -= pregnant_birthing_this_month_other_death

        # check if the number of pregnant animals is below zero
        # if so, set the number of pregnant animals to zero
        if animal.pregnant_animals_total[-1] < 0:
            animal.pregnant_animals_total[-1] = 0
        if animal.pregnant_animals_birthing_this_month[-1] < 0:
            animal.pregnant_animals_birthing_this_month[-1] = 0

        return

    def calculate_starving_other_death_head(
        animal, population_starving_post_slaughter_and_all_homekill
    ):
        """
        This function calculates the number of animals that die from starvation in a month.

        It takes the population of animals that are starving after slaughter and homekill, and calculates the number of animals that die from starvation.
        In terms of physical relevance - the animals that don't die from starvation are the ones that are able to find enough other food to survive or have fat stores etc.
        These animals ARE NOT turned in to meat.
        Those that are turned in to meat are captured in the homekill functions.


        Parameters
        ----------
        animal : Animal
            The animal object that is being calculated for.
        population_starving_post_slaughter_and_all_homekill : float
            The number of animals that are starving after slaughter and homekill.

        Returns
        -------
        float
            The number of animals that die from starvation in a month.

        """

        return (
            population_starving_post_slaughter_and_all_homekill
            * animal.starvation_death_fraction
        )

    def calculate_final_population(animal):
        """
        This function calculates the final population of the animal after all the slaughter and homekill has been done.

        Parameters
        ----------
        animal : Animal
            The animal object that is being calculated for.

        Returns
        -------
        float
            The final population of the animal.

        """

        animal.current_population -= (
            animal.other_death_starving[-1]
            + animal.homekill_healthy_this_month[-1]
            + animal.homekill_starving_this_month[-1]
        )

        # check if the population is below zero

        if animal.current_population < 0:
            animal.current_population = 0
            # and BUG might exist, if this override happens, what happens to the homemkill? Could be overestimated
            # THIS HAS FIXED THE BELOW ZERO PROBLEM.

        return

    def feed_animals(animal_list, ruminants, available_feed, available_grass):
        """
        This function will feed the animals
        It will do so by allocating the grass first to those animals that can eat it,
        and then allocating the remaining feed to the remaining animals

        It will also priotiise the animals that are most efficient at converting feed,
        This means starting with milk.

        List needs to be sorted in the oprder you want the animals to be prioritised for feed
        """

        # reset the feed balance
        for animal in animal_list:
            animal.reset_NE_balance()

        # feed the ruminants grass
        for ruminant in ruminants:
            available_grass = ruminant.feed_the_species(
                available_grass, "grass"
            )  # TODO: Currently feed type is onyl defined here, might be more sensible to attach it to the FOOD object.

        # feed everything grain
        for animal in animal_list:
            available_feed = animal.feed_the_species(available_feed, "feed")

        # all feeding is done in the order of the lists supplied.
        return available_feed, available_grass

    def calculate_starving_animals_after_feed(animal_list):
        """
        This function will calculate the number of animals that are starving after feeding
        It iterates through the animal list and calculates the number of animals that are starving
        result is appended to the animal object
        """
        for animal in animal_list:
            animal.population_starving_pre_slaughter.append(
                animal.current_population - animal.population_fed
            )

    def set_current_populations(animal_objects):
        """
        Sets the current population of each animal object
        This simply sets the current population to the value at the end of the previous month.
        This value is then updated during the month loop.
        Runs at the start opf the month before any changes to population are made.
        """
        # create checks for valid data and raise errors
        if len(animal_objects) == 0:
            raise ValueError("No animal objects supplied to set_current_populations")
        if not isinstance(animal_objects, list):
            raise TypeError("animal_objects must be a list")
        if not all(isinstance(animal, AnimalSpecies) for animal in animal_objects):
            raise TypeError("animal_objects must be a list of Animal objects")
        if not all(isinstance(animal.population, list) for animal in animal_objects):
            raise TypeError("population must be a list")
        if not all(len(animal.population) > 0 for animal in animal_objects):
            raise ValueError("population must be a non-empty list")

        for animal in animal_objects:
            animal.current_population = animal.population[-1]

    def appened_current_populations(animal_objects):
        """
        Appends the current population of each animal object to its population list.
        Runs at the end of the month loop once currrent population has been updated

        Args:
            animal_objects (_type_): _description_

        """
        for animal in animal_objects:
            animal.population.append(animal.current_population)


class AnimalDataReader:
    def read_animal_population_data(filename):
        """
        Read animal population data from CSV file

        Returns
        -------
        df_animal_stock_info : pandas dataframe
            Dataframe containing animal population data

        """

        repo_root = git.Repo(".", search_parent_directories=True).working_dir
        # Load data
        animal_feed_data_dir = (
            Path(repo_root) / "data" / "no_food_trade" / "animal_feed_data"
        )

        FAO_data = Path.joinpath(Path(animal_feed_data_dir), filename)

        # Load data
        df_animal_stock_info = pd.read_csv(FAO_data, index_col="iso3")

        # merge the two dataframes on index

        return df_animal_stock_info

    def read_animal_nutrition_data(filename):
        """ "
        Read animal nutrition data from CSV file

        Returns
        -------
        df_animal_nutrition : pandas dataframe
            Dataframe containing animal nutrition data
        """
        repo_root = git.Repo(".", search_parent_directories=True).working_dir
        # Load data
        animal_feed_data_dir = (
            Path(repo_root) / "data" / "no_food_trade" / "animal_feed_data"
        )

        animal_nutrition_data_location = Path.joinpath(
            Path(animal_feed_data_dir), filename
        )

        df_animal_attributes = pd.read_csv(
            animal_nutrition_data_location, index_col="animal"
        )

        return df_animal_attributes

    def read_animal_options(filename):
        """ "
        Read animal nutrition data from CSV file

        Returns
        -------
        df_animal_nutrition : pandas dataframe
            Dataframe containing animal nutrition data
        """
        repo_root = git.Repo(".", search_parent_directories=True).working_dir
        # Load data
        animal_feed_data_dir = (
            Path(repo_root) / "data" / "no_food_trade" / "animal_feed_data"
        )

        animal_options_location = Path.joinpath(Path(animal_feed_data_dir), filename)

        df_animal_options = pd.read_csv(animal_options_location, index_col="animal")

        return df_animal_options

    def read_animal_regional_factors(filename):
        """ "
        Read animal nutrition data from CSV file

        Returns
        -------
        df_animal_nutrition : pandas dataframe
            Dataframe containing animal nutrition data
        """
        repo_root = git.Repo(".", search_parent_directories=True).working_dir
        # Load data
        animal_feed_data_dir = (
            Path(repo_root) / "data" / "no_food_trade" / "animal_feed_data"
        )

        regional_coeffs_location = Path.joinpath(Path(animal_feed_data_dir), filename)

        df_regional_coeffs = pd.read_csv(regional_coeffs_location, index_col="animal")

        return df_regional_coeffs

    def read_country_data(filename):
        """ "
        Read animal nutrition data from CSV file

        Returns
        -------
        df_animal_nutrition : pandas dataframe
            Dataframe containing animal nutrition data
        """
        repo_root = git.Repo(".", search_parent_directories=True).working_dir
        # Load data
        animal_feed_data_dir = (
            Path(repo_root) / "data" / "no_food_trade" / "animal_feed_data"
        )

        country_info_location = Path.joinpath(Path(animal_feed_data_dir), filename)

        df_country_info = pd.read_csv(country_info_location, index_col="alpha3")

        return df_country_info


class AnimalModelBuilder:
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
            ~(df_animal_stock_info.index.str.contains("milk"))
            * df_animal_stock_info.index.str.contains("head")
        ).sum() == df_animal_stock_info.index.str.contains("slaughter").sum()
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
                slaughter_input = 0  # set to zero for now, but will be updated to non zero due to dairy calf culling
                animal_function = "milk"
            else:
                # remove "meat_" from the animal type
                slaughter_input = df_animal_stock_info.loc[
                    animal_type.replace("meat_", "") + "_slaughter"
                ]
                animal_function = "meat"

            # create string of animal species (remove milk or meat from the animal type)
            animal_species = animal_type.replace("milk_", "").replace("meat_", "")

            # only create an animal object if the number of animals is greater than 0
            if df_animal_stock_info.loc[animal_type + "_head"] > 0:
                # initialise the animal object
                animal = AnimalSpecies(
                    animal_type=animal_type, animal_species=animal_species
                )
                # set the animal attributes
                animal.set_animal_attributes(
                    population=df_animal_stock_info.loc[animal_type + "_head"],
                    slaughter=slaughter_input,
                    animal_function=animal_function,
                    livestock_unit=df_animal_attributes.loc[animal_type]["LSU"],
                    digestion_type=df_animal_attributes.loc[animal_type][
                        "digestion type"
                    ],
                    animal_size=df_animal_attributes.loc[animal_type]["animal size"],
                    approximate_feed_conversion=df_animal_attributes.loc[animal_type][
                        "approximate feed conversion"
                    ],
                )
                animal_objects[animal_type] = animal
            else:
                pass
                # otherwise, don't create an object

        return animal_objects

    def update_animal_objects_with_slaughter(
        animal_list, df_animal_attributes, df_animal_options, scenario
    ):
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

        # Start transfer stuff
        transfer_populations = {}
        for animal in animal_list:
            transfer_populations[animal.animal_species] = 0

        # order animal_list with milk first, in order to calculate transfer head appropriately
        animal_list = sorted(animal_list, key=lambda x: x.animal_function, reverse=True)

        selected_scenario = df_animal_options.loc[
            df_animal_options["scenario"] == scenario
        ]

        # loop through the dict of animal objects
        for animal in animal_list:
            # this list of variables will be a csv file in the future
            gestation = df_animal_attributes.loc[animal.animal_type]["gestation"]
            animal_slaughter_hours = df_animal_attributes.loc[animal.animal_type][
                "animal_slaughter_hours"
            ]
            other_animal_death_rate_annual = df_animal_attributes.loc[
                animal.animal_type
            ]["other_animal_death_rate_annual"]
            animals_per_pregnancy = df_animal_attributes.loc[animal.animal_type][
                "animals_per_pregnancy"
            ]
            reduction_in_animal_breeding = selected_scenario.loc[animal.animal_type][
                "reduction_in_animal_breeding"
            ]
            change_in_slaughter_rate = selected_scenario.loc[animal.animal_type][
                "change_in_slaughter_rate"
            ]
            pregnant_animal_slaughter_fraction = selected_scenario.loc[
                animal.animal_type
            ]["pregnant_animal_slaughter_fraction"]
            target_population_fraction = selected_scenario.loc[animal.animal_type][
                "target_population_fraction"
            ]
            starvation_death_fraction = selected_scenario.loc[animal.animal_type][
                "starvation_death_fraction"
            ]

            # if milk animal, set the transfer population
            if animal.animal_function == "milk":
                animal.set_milk_birth()
                transfer_populations[
                    animal.animal_species
                ] = animal.set_initial_milk_transfer()
                transfer_pop = -transfer_populations[animal.animal_species]
            else:
                # is not milk, recieve the transfer population (if no correspiodning milk animal, this will be zero)
                transfer_pop = transfer_populations[animal.animal_species]
                # check if transfer population is very high compared to the population, use assert
                assert (
                    transfer_pop < animal.initital_population
                ), "transfer pop is greater than population"
                # BUG: What to do? The transfer populationd ominates the emat goat population. What is a good response?

            # need to do transfer populations here...
            # start with milk

            animal.set_species_slaughter_attributes(
                gestation,
                other_animal_death_rate_annual,
                animals_per_pregnancy,
                animal_slaughter_hours,
                change_in_slaughter_rate,
                pregnant_animal_slaughter_fraction,
                reduction_in_animal_breeding,
                target_population_fraction,
                starvation_death_fraction,
                transfer_pop,
            )
        return

    def update_animal_objects_with_milk(animal_list, df_animal_attributes):
        """This function updates the animal objects with the slaughter data.

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
            productive_milk_age_start = df_animal_attributes.loc[animal.animal_type][
                "productive_milk_age_start"
            ]
            productive_milk_age_end = df_animal_attributes.loc[animal.animal_type][
                "productive_milk_age_end"
            ]
            insemination_cycle_time_for_milk = df_animal_attributes.loc[
                animal.animal_type
            ]["insemination_cycle_time_for_milk"]
            milk_production_per_month_per_head = df_animal_attributes.loc[
                animal.animal_type
            ]["milk_production_per_month_per_head"]
            animal.set_species_milk_attributes(
                productive_milk_age_start,
                productive_milk_age_end,
                insemination_cycle_time_for_milk,
                milk_production_per_month_per_head,
            )
        return

    def update_animal_objects_LSU_factor(animal_list, country_object):
        """
        This function updates the animal objects with the LSU factors

        Parameters
        ----------
        animal_list : list
            List of animal objects
        country_object : object
            Object containing country data

        Returns
        -------
        animal_list : list
            List of animal objects

        """
        # loop through the dict of animal objects
        for animal in animal_list:
            animal.set_LSU_attributes(country_object)
        return

    def remove_first_month(animal):
        attributes = vars(animal)
        for attr_name, attr_value in attributes.items():
            if isinstance(attr_value, list) and attr_value:
                attr_value.pop(0)


## Debug and Meta tools
class Debugging:
    def print_list_lengths(obj):
        attributes = vars(obj)
        for attr_name, attr_value in attributes.items():
            if isinstance(attr_value, list):
                print(f"{attr_name}: {len(attr_value)}")

    # Import csv module for writing CSV files

    def save_single_animal_data_to_csv(
        animal, output_path="animal_single_data_to_csv.csv"
    ):
        # Initialize an empty list to store the rows for the CSV
        import csv

        rows = []

        # Initialize an empty list to store the headers
        headers = ["animal_type"]

        # Initialize a dictionary to hold attribute data for the current animal
        row_data = {"animal_type": animal.animal_type}

        # Iterate through each attribute of the object
        for attr, value in vars(animal).items():
            # Check if the attribute's value is a list of numbers
            if isinstance(value, list) and all(
                isinstance(x, (int, float)) for x in value
            ):
                # Add attribute name to headers if not already present
                headers.append(attr)

                # Assign the list to the corresponding key in the row_data dictionary
                row_data[attr] = value

        # Determine the maximum list length for any attribute of the animal
        max_len = max(len(value) for value in row_data.values())

        # Initialize a list to store the final rows for the CSV
        final_rows = []

        # Convert the row data to the final format, filling in missing values with 'N/A'
        for i in range(max_len):
            final_row = {}
            for header in headers:
                final_row[header] = (
                    row_data.get(header, ["N/A"])[i]
                    if i < len(row_data.get(header, []))
                    else "N/A"
                )
            final_rows.append(final_row)

        # Write the data to a CSV file
        with open(output_path, "w", newline="") as csvfile:
            csv_writer = csv.DictWriter(csvfile, fieldnames=headers)
            csv_writer.writeheader()
            csv_writer.writerows(final_rows)

    def print_list_any(animal_list):
        # Importing the csv module
        import csv

        attributes = [
            "population",
            "slaughter",
            "other_death_total",
            "births_animals_month",
            "transfer_population",
            "transfer_births",
            "retiring_milk_animals",
        ]

        # Initialize a list to store the rows and a set to collect all unique headers
        rows = []
        all_headers = set()

        # Loop through each object in the animal_list to extract and format the attributes
        for animal in animal_list:
            # Initialize a dictionary to store attribute data for each animal
            row_data = {}

            # Extract attributes and populate the row_data dictionary
            for attr in attributes:
                value = getattr(animal, attr, "N/A")
                row_data[attr] = value if not isinstance(value, list) else value

            # Get the animal_type attribute
            animal_type = getattr(animal, "animal_type", "Unknown")

            # Generate the headers for the CSV based on animal_type and add them to the set of all headers
            current_headers = [f"{animal_type}_{attr}" for attr in attributes]
            all_headers.update(current_headers)

            # Determine the maximum list length among all attributes for this animal
            max_len = max(
                len(val) if isinstance(val, list) else 1 for val in row_data.values()
            )

            # Create rows by expanding lists into individual rows, and add them to the list of all rows
            for i in range(max_len):
                row = {header: "N/A" for header in all_headers}
                for attr in attributes:
                    header = f"{animal_type}_{attr}"
                    val = row_data[attr]
                    row[header] = (
                        val[i] if isinstance(val, list) and i < len(val) else val
                    )
                rows.append(row)

        # Sort headers for a more organized CSV
        sorted_headers = sorted(list(all_headers))

        # Write to CSV
        output_path = "animal_data_expanded_corrected.csv"
        with open(output_path, "w", newline="") as csvfile:
            csv_writer = csv.DictWriter(csvfile, fieldnames=sorted_headers)
            csv_writer.writeheader()
            for row in rows:
                csv_writer.writerow(row)

        print(output_path)

    def available_feed_function(billion_kcals, months_to_run=120):
        """

        Energy is expressed as digestible (DE), metabolizable (ME), or net energy (NE) by considering the loss of energy during digestion and metabolism from gross energy (GE) in the feed, as follows:

        Gross energy (GE): the amount of energy in the feed.
        Digestible energy (DE): the amount of energy in the feed minus the amount of energy lost in the feces.
        Metabolizable energy (ME): the amount of energy in the feed minus the energy lost in the feces and urine.
        Net energy (NE): the amount of energy in the feed minus the energy lost in the feces, urine, and in heat production through digestive and metabolic processes, i.e. heat increment.
        """
        # import feed data from model
        ### TODO: import feed data from model

        # calculate billion kcals in feed, don't use protein/fats just yet. That's for a revision
        # all imports should be in GE, gross energy
        # calacuklation of NE is done in the feed animals function

        # animal_feed = Food(billion_kcals, -1, -1)
        # animal_feed.type = "feed"
        animal_feed = Food(
            kcals=[billion_kcals] * months_to_run,
            fat=[0] * months_to_run,
            protein=[0] * months_to_run,
            kcals_units="billion kcals each month",
            fat_units="thousand tons each month",
            protein_units="thousand tons each month",
        )

        return animal_feed

    def available_grass_function(billion_kcals, months_to_run=120):
        """### CHECK IS BILLION KCALS

        Energy is expressed as digestible (DE), metabolizable (ME), or net energy (NE) by considering the loss of energy
        during digestion and metabolism from gross energy (GE) in the feed, as follows:

        Gross energy (GE): the amount of energy in the feed. Digestible energy (DE): the amount of energy in the feed
        minus the amount of energy lost in the feces. Metabolizable energy (ME): the amount of energy in the feed minus
        the energy lost in the feces and urine. Net energy (NE): the amount of energy in the feed minus the energy lost
        in the feces, urine, and in heat production through digestive and metabolic processes, i.e. heat increment.
        """

        # NOTE THIS GRASS COULD BE LIMITED to ration etc.
        # this just knows how much grass is given, not how much grass is generally avialable.

        # calculate available grass
        # import grass data

        # units idealy in billion kcal
        # all imports should be in GE, gross energy
        # calacuklation of NE is done in the feed animals function
        # grass = Food(billion_kcals, -1, -1)
        # grass.type = "grass"

        grass = Food(
            kcals=[billion_kcals] * months_to_run,
            fat=[0] * months_to_run,
            protein=[0] * months_to_run,
            kcals_units="billion kcals each month",
            fat_units="thousand tons each month",
            protein_units="thousand tons each month",
        )

        return grass


def main(country_code, available_feed, available_grass, scenario, remove_first_month=0):
    """Main function to be called by the user.

    This function will call the other functions in this file.
    """
    # IMPORT DATA
    # Data file defaults TODO: imnclude as args, just not yet to not break things
    population_csv = "FAOSTAT_head_and_slaughter.csv"
    options_csv = "species_options.csv"
    attributes_csv = "species_attributes.csv"
    regional_csv = "regional_conversion_factors.csv"
    country_csv = "FAO_country_region_mappings.csv"

    # read animal population data
    df_animal_stock_info = AnimalDataReader.read_animal_population_data(population_csv)

    # read animal nutrition data
    df_animal_attributes = AnimalDataReader.read_animal_nutrition_data(attributes_csv)
    df_animal_options = AnimalDataReader.read_animal_options(options_csv)
    df_regional_conversion_factors = AnimalDataReader.read_animal_regional_factors(
        regional_csv
    )
    df_country_info = AnimalDataReader.read_country_data(country_csv)

    # months to run the model for
    months_to_run = (
        available_feed.NMONTHS
    )  # will be inherited from the calling function

    # WHEN INTEGRATING, THESE CREATION OF OBJECTS SHOULD BE DONE OUTSIDE OF THE MAIN FUNCTION
    # AND ONLY ON THE FIRST RUN OF THE MODEL

    # # Populate animal objects ##
    # create animal objects
    animal_list = AnimalModelBuilder.create_animal_objects(
        df_animal_stock_info.loc[country_code], df_animal_attributes
    )

    # sort the animal objects by approximate feed conversion
    # ## TODO: look at my dual use of lists and dicts here, probably unneccesary ###
    # Should standardise, although no biggie as it is passing pointers not the actual data so cost is low
    animal_dict = dict(
        sorted(
            animal_list.items(),
            key=lambda item: item[1].approximate_feed_conversion,
        )
    )

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

    AnimalModelBuilder.update_animal_objects_with_milk(
        milk_animals, df_animal_attributes
    )
    AnimalModelBuilder.update_animal_objects_with_slaughter(
        all_animals, df_animal_attributes, df_animal_options, scenario
    )

    # create country object
    country_object = CountryData(country_code)
    country_object.calculate_homekill_hours()
    country_object.homekill_desperation_parameters()
    country_object.set_livestock_unit_factors(
        df_country_info, df_regional_conversion_factors
    )

    # with the country object, update the animal objects with the LSU factors
    AnimalModelBuilder.update_animal_objects_LSU_factor(all_animals, country_object)

    # create output feed and grass objects
    feed_used = Food(np.zeros(len(available_feed.kcals)))
    grass_used = Food(np.zeros(len(available_feed.kcals)))

    #### END CREATION OF OBJECTS ####

    # do month zero baseline appends
    for animal in all_animals:
        animal.append_month_zero()

    # THIS month for loop won't reallt exist here, i will be called in a loop somewhere else
    # this is required as the I/O needs to interact with the rest of the model each month
    for month in range(0, months_to_run):
        country_object.month = month
        if month != 0:
            AnimalPopulation.set_current_populations(all_animals)

        ## THESE FEED OBJECTS WILL BE PASSED IN ####
        # create available feed object
        feed_available_this_month = available_feed[month]
        grass_available_this_month = available_grass[month]

        ## Do the feeding
        # feed the animals

        (
            feed_available_this_month,
            grass_available_this_month,
        ) = AnimalPopulation.feed_animals(
            all_animals,
            ruminants,
            feed_available_this_month,
            grass_available_this_month,
        )
        AnimalPopulation.calculate_starving_animals_after_feed(all_animals)

        # update the feed and grass objects with the amount used
        # @MORGAN TODO:, I couldn't work out how to assign the values to the feed_used object without doing this
        # (breaking it out in to kcals)
        feed_used.kcals[month] = (
            available_feed.kcals[month] - feed_available_this_month.kcals
        )
        grass_used.kcals[month] = (
            available_grass.kcals[month] - grass_available_this_month.kcals
        )

        ## OKAY SO NOW WE HAVE THE ANIMALS FED, WE NEED TO LOOK AT SLAUGHTERING

        # create a list of transfer populations, based on all the different animal species, use for loop to create a dict that can be used to store the transfer populations
        # important that these are zero as default
        # resets to zero each month (i.e not cumulative, )
        transfer_populations = {}
        births = {}
        for animal in all_animals:
            transfer_populations[animal.animal_species] = 0

        ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### #####
        # this next loop is run first to populate the birth/retiurement tasnfers.
        # working out the transfer populations requires the milk animals birt rate / retuirmenet rates
        # this needs to be done first as the transfer population is used in the next loop
        # and the next loop will be run in order of slaughter preference, so we can't put the birth rates in there
        # so the first loop can be run in any order, but the second loop needs to be run in order of slaughter preference
        ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### #####
        for animal in all_animals:
            # additive population

            (
                new_births,
                new_transfer_births,
            ) = AnimalPopulation.calculate_additive_births(animal, month)
            # add new population to the animal object
            births[animal.animal_type] = new_births
            animal.births_animals_month.append(new_births)

            if animal.animal_function == "milk":
                transfer_populations[animal.animal_species] = (
                    animal.retiring_milk_head_monthly() + new_transfer_births
                )
                animal.retiring_milk_animals.append(animal.retiring_milk_head_monthly())
                animal.transfer_births.append(new_transfer_births)

                # add to tranfser population
                ##### THIS ISN'T WORKING CHANGED TO FUCNTION, MAYBE GOOD NOW

        ##### ##### ##### ##### ##### ##### ##### ##### ##### #####
        # this loop below needs to run in order of species slaughhter prefernce
        # TODO: what is the order required? provide an option to the user
        # consider, total feed usage, feed per head, or feed conversion
        # if we are looking for efficiency feed voncersion  head species
        # if we are looking for total feed usage, feed usage per head
        # or maybe feed usage per slaughter hour is the best use?
        ##### ##### ##### ##### ##### ##### ##### ##### ##### #####

        for animal in all_animals:
            if "milk" not in animal.animal_type:
                # if not a milk animal add
                # divide by two as the transfer population is split between meat and milk
                new_additive_animals_month = (
                    births[animal.animal_type]
                    + transfer_populations[animal.animal_species]
                )
                animal.transfer_population.append(
                    transfer_populations[animal.animal_species]
                )

            else:
                new_additive_animals_month = births[animal.animal_type]
                animal.transfer_population.append(
                    -transfer_populations[animal.animal_species]
                )

            AnimalPopulation.calculate_change_in_population(
                animal, country_object, new_additive_animals_month
            )

        # then new loop... for homekill
        # reset the homekill hours for the coming month
        country_object.homekill_hours_budget.append(
            country_object.homekill_hours_total_month[-1]
        )

        for animal in all_animals:
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

            # note pregant animals have already been calculated in the slaughter loop
            # this seems realistic tha policy would not flow down to homekill etc.
            # I'll leave it in there for now, if we want to change it, down the track. It probably makes zero difference but I haven't tested sensitivity yet

            AnimalPopulation.calculate_other_death_homekill_head(
                animal, country_object
            )  # how many of the animals that died due to natural causes (injuries etc.) were butchered and turned in to meat?
            AnimalPopulation.calculate_healthy_homekill_head(
                animal, country_object
            )  # no return, as updates animal object
            population_starving_post_slaughter_and_healthy_homekill = (
                AnimalPopulation.calculate_starving_pop_post_slaughter_healthy_homekill(
                    animal
                )
            )
            AnimalPopulation.calculate_starving_homekill_head(
                animal,
                country_object,
                population_starving_post_slaughter_and_healthy_homekill,
            )  # this could be a hard limit based on capacity of the homekill system. Could take in to account healthy homekill (to see if there is capacity for more)
            population_starving_post_all_slaughter_homekill = (
                AnimalPopulation.calculate_starving_pop_post_all_slaughter_homekill(
                    animal, population_starving_post_slaughter_and_healthy_homekill
                )
            )
            # the end of this section returns the population of animals that are starving after all the homekill and slaughtering. This will be used o calculate the other death from starving

            # OTHER DEATH resulting from starvation of the 'starving' population
            animal.other_death_starving.append(
                AnimalPopulation.calculate_starving_other_death_head(
                    animal, population_starving_post_all_slaughter_homekill
                )
            )
            # next do the other death from starving.
            # might be zero if all of starving is dead

            animal.other_death_total.append(
                animal.other_death_starving[-1]
                + animal.other_death_causes_other_than_starving[-1]
            )
            # reduce pregnant animals by the other death rate (proportional to the population)
            # only do this if not a baseline scenario
            # determine if baseline scenario-like from options and absence of starvation
            if (
                animal.reduction_in_animal_breeding == 0
                and animal.target_population_fraction == 1
                and animal.other_death_starving[-1] < 10
            ):
                # if baseline, then don't reduce the pregnant animals
                pass
            else:
                AnimalPopulation.other_death_pregnant_adjustment(animal)

            animal.total_homekill_this_month.append(animal.total_homekill())

            # FINALLY WE CAN Calculate THE NEW POPULATION
            AnimalPopulation.calculate_final_population(animal)

            ### FINALLY, we have it all
            # New population
            # animal.slaughter is the professionally slaughtered animals
            # animal.total_homekill_this_month is the unprofessinlally slaughtered (can apply weighting/wastage factor)
            # animal.other_death_total is the other death (basically non-recoverable - lost due to sickness/loss - no meat from here)
            #

            # Homekill notes:
            # homekill healthy is demand driven homekill. This will be higher if the population is despereate. It is a 'pull factor'
            # homekill starving is a 'push factor' it's not that the human population desperatly needs the food, but the animal has a high chance of dying and it's good to get some meat out of it
            # important to run the homemkill functions in the right order, as they all draw on the homekill capacity, and healthy homekill
            # should come last (as I think it's sensible to assume people will buthcer sick/dead animals first)

        # and for cleanliness, the population is appended here right at the end
        AnimalPopulation.appened_current_populations(all_animals)

    # remove first month (as it's just the initial population)
    if remove_first_month == 1:
        for animal in all_animals:
            AnimalModelBuilder.remove_first_month(animal)

    return all_animals, feed_used, grass_used


if __name__ == "__main__":
    feed = (
        0  # billion kcals, shorthand way toa pply consistent supply over whole period
    )
    grass = (
        0  # billion kcals, shorthand way toa pply consistent supply over whole period
    )
    months = 10
    output_list, feed_used, grass_used = main(
        "JAM",
        Debugging.available_feed_function(feed, months),
        Debugging.available_grass_function(grass, months),
        "baseline",
        remove_first_month=1,
    )
    # Initialize figure
    fig = go.Figure()

    # plot all the animals without detail
    # exclude chicken from output list
    ignore_chicken_graph = 0
    if ignore_chicken_graph == 1:
        animal_list = [
            animal for animal in output_list if "chicken" not in animal.animal_type
        ]
    else:
        animal_list = [animal for animal in output_list]

    for animal in animal_list:
        # fig.add_trace(go.Scatter(y=animal.slaughter, mode='lines', name=animal.animal_type + " slaughter"))
        fig.add_trace(
            go.Scatter(
                y=animal.population,
                mode="lines",
                name=animal.animal_type + " population",
            )
        )

    fig2 = go.Figure()

    # Plot one animal
    k = 3
    # Add detailed lines to the plot
    fig2.add_trace(
        go.Scatter(y=animal_list[k].births_animals_month, mode="lines", name="births")
    )
    fig2.add_trace(
        go.Scatter(y=animal_list[k].slaughter, mode="lines", name="slaughter")
    )
    fig2.add_trace(
        go.Scatter(
            y=animal_list[k].total_homekill_this_month, mode="lines", name="homekill"
        )
    )
    fig2.add_trace(
        go.Scatter(
            y=animal_list[k].other_death_total, mode="lines", name="other death total"
        )
    )
    fig2.add_trace(
        go.Scatter(y=animal_list[k].population, mode="lines", name="population")
    )
    fig2.add_trace(
        go.Scatter(
            y=animal_list[k].pregnant_animals_birthing_this_month,
            mode="lines",
            name="preg this month",
        )
    )
    fig2.add_trace(
        go.Scatter(
            y=animal_list[k].pregnant_animals_total, mode="lines", name="preg total"
        )
    )
    fig2.add_trace(
        go.Scatter(
            y=animal_list[k].transfer_population, mode="lines", name="transfer pop"
        )
    )
    fig2.add_trace(
        go.Scatter(
            y=animal_list[k].transfer_births, mode="lines", name="transfer births"
        )
    )

    print(
        "Baseline slaughter: ",
        animal_list[k].baseline_slaughter,
        animal_list[k].animal_type,
    )
    print("Target population: ", animal_list[k].target_population_head)
    print(
        "Final population: ",
        animal_list[k].current_population,
    )
    # print("Difference: ", animal_list[k].current_population - animal_list[k].target_population_head)

    # add title to the figure, and set the x axis title
    fig2.update_layout(title=animal_list[k].animal_type, xaxis_title="Month")

    # Show figure
    fig2.show()
    fig.show()
