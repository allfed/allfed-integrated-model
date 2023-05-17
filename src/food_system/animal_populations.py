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
    def __init__(self, animal_type, population, slaughter, feed_LSU, digestion_type, approximate_feed_conversion, pregnant=None, carb_requirement=-1, protein_requirement=-1, fat_requirement=-1):
            self.animal_type = animal_type
            self.population = [population] # this is a list so that it can be appended to later
            self.slaughter = [slaughter] # this is a list so that it can be appended to later
            self.feed_LSU = feed_LSU
            self.digestion_type = digestion_type
            self.approximate_feed_conversion = approximate_feed_conversion

            # set by default to 50%, can be changed if species specific data is available
            self.digestion_efficiency = 0.5 # this is the conversion from gross energy to net energy
            # to be set later (but leaving here so it could be set on initialisation)
            self.pregnant = pregnant
            # not currently used
            self.nutrition_ratio = Food(carb_requirement, fat_requirement, protein_requirement) if carb_requirement and fat_requirement and protein_requirement else None
            if self.nutrition_ratio:
                self.nutrition_ratio.set_units(
                    kcals_units='ratio of carbs in diet required',
                    fat_units='ratio of fat in diet required',
                    protein_units='ratio of protein in diet required',
                )
            if slaughter>0:
                self.statistical_lifetime = population/slaughter # this is the statistical lifetime of the animal, used to calculate the number of animals slaughtered per month

            self.feed_balance = self.feed_required_per_month_species() # this is the feed required per month for the species
            self.population_fed = 0
            self.population_starving = 0

            # not currently used, used for meat production information
            self.carcass_weight = None # update to include this in the csv file
            self.offal_percentage = None # update to include this in the csv file
            self.fat_percentage = None # update to include this in the csv file
            if self.carcass_weight and self.offal_percentage and self.fat_percentage:
                self.carcass_weight = self.carcass_weight
                self.offal_percentage = self.offal_percentage
                self.fat_percentage = self.fat_percentage


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
        Path(animal_feed_data_dir), "livestock_unit_species.csv"
    )

    df_animal_nutrition = pd.read_csv(animal_nutrition_data_location, index_col="animal")

    return df_animal_nutrition

def create_animal_objects(df_animal_stock_info, df_animal_nutrition):
    """
    Create animal objects from dataframes

    Parameters
    ----------
    df_animal_stock_info : pandas dataframe
        Single dimension Dataframe containing animal population data for each country 
    df_animal_nutrition : pandas dataframe
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
        else:
            # remove "meat_" from the animal type
            slaughter_input = df_animal_stock_info.loc[animal_type.replace("meat_", "") + "_slaughter"]

        animal_species = AnimalSpecies(
            animal_type=animal_type,
            population=df_animal_stock_info.loc[animal_type + "_head"],
            slaughter=slaughter_input,
            feed_LSU=df_animal_nutrition.loc[animal_type]["LSU"],
            digestion_type=df_animal_nutrition.loc[animal_type]["digestion type"],
            approximate_feed_conversion=df_animal_nutrition.loc[animal_type]["approximate feed conversion"],
        )
        animal_objects[animal_type] = animal_species

    return animal_objects

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
    

    # create food objects
    example_food1=Food(1000,-1,-1)
    example_food2=Food(100,-1,-1)

    # add the food objects together
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
    #consider if ME or DE is more appropriate
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
df_animal_nutrition = read_animal_nutrition_data()

## Populate animal objects ##

# create animal objects
animal_list = create_animal_objects(df_animal_stock_info.loc[country_code], df_animal_nutrition)

# sort the animal objects by approximate feed conversion
animal_list = dict(
    sorted(
        animal_list.items(),
        key=lambda item: item[1].approximate_feed_conversion,
    )
)


# create available feed object
feed_MJ_available_this_month = available_feed()
grass_MJ_available_this_month = available_grass()

# get list of milk animals, 
milk_animals = [animal for animal in animal_list.values() if "milk" in animal.animal_type]
# get list of non-milk animals
non_milk_animals = [animal for animal in animal_list.values() if "milk" not in animal.animal_type]
# non milk runminants
non_milk_ruminants = [animal for animal in animal_list.values() if "milk" not in animal.animal_type and animal.digestion_type == "ruminant"]
# get list of all ruminants
ruminants = [animal for animal in animal_list.values() if animal.digestion_type == "ruminant"]
# get list of non-ruminants
non_ruminants = [animal for animal in animal_list.values() if animal.digestion_type == "non-ruminant"]

## Do the feeding
# feed the animals
feed_MJ_available_this_month, grass_MJ_available_this_month = feed_animals(animal_list, feed_MJ_available_this_month, grass_MJ_available_this_month)

#### Just printing stuff, not needed for the model
print(f"feed_MJ_available_this_month is {feed_MJ_available_this_month.kcals}")
print(f"grass_MJ_available_this_month is {grass_MJ_available_this_month.kcals}")
# print the results
for animal in animal_list.values():
    print(f"{animal.animal_type} total pop: {animal.population}, fed: {animal.population_fed}, starving: {animal.population_starving}")


## OKAY SO NOW WE HAVE THE ANIMALS FED, WE NEED TO LOOK AT SLAUGHTERING






## At the end of the month, reset the feed balance with the new popluaton and feed required


