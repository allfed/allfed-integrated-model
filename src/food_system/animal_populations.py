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

# TODO: fix the csv file column and row naming convention. uniformity between files (i.e dairy_cattle vs dairy_cows)



# create class to store animal population data in. Needs to store the following: animal type, population, and slaughter. 
class SpeciesCurrentState:
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
    def __init__(self, animal_type, population, slaughter, pregnant, starving, livestock_unit, carb_requirement, protein_requirement, fat_requirement):
        self.animal_type = animal_type  # beef, pork, chicken etc...
        self.population = population # number of animals (total)
        self.slaughter = slaughter # number of animals slaughtered this month
        self.pregnant = pregnant # number of animals pregnant this month
        self.starving = starving # number of animals starving this month
        self.feed_LSU = livestock_unit # amount of feed required this month
        self.nutrition_ratio=Food(carb_requirement,fat_requirement,protein_requirement)
        self.nutrition_ratio.set_units(
                kcals_units = 'ratio of carbs in diet required',
                fat_units = 'ratio of fat in diet required',
                protein_units = 'ratio of protein in diet required',
        )
        # now do calculations for the feed required, 

        ## then consider a further food object for the actual feed, this having kcals etc. as the units.
        ## this will be able to be changed based on the LSU for that particualr heopgraphy etc.
    
    def __repr__(self):
        # function to print the class
        return f"SpeciesCurrentState(animal_type='{self.animal_type}', population={self.population}, slaughter={self.slaughter}, pregnant={self.pregnant}, starving={self.starving}, feed_required={self.feed_required}, nutrition_ratio={self.nutrition_ratio})"
    
    def feed_use_this_month(self):
        # function to calculate the total feed for this month for the species
        #     (defaults to billion kcals, thousand tons monthly fat, thousand tons monthly protein)
        kcal_feed_use = self.feed_LSU * self.nutrition_ratio.kcals
        fat_feed_use = self.feed_LSU * self.nutrition_ratio.fat
        protein_feed_use = self.feed_LSU * self.nutrition_ratio.protein

        feed_use = Food(kcal_feed_use, fat_feed_use, protein_feed_use)
        feed_use.set_units(
                kcals_units = 'billion kcals',
                fat_units = 'thousand tons',
                protein_units = 'thousand tons',
        )
        return feed_use



# create function that reads CSV info and populates the classes
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

    FAO_stat_slaughter_counts_processed_location = Path.joinpath(
        Path(animal_feed_data_dir), "FAO_stat_slaughter_counts_processed.csv"
    )
    head_count_csv_location = Path.joinpath(
        Path(animal_feed_data_dir), "head_count_csv.csv"
    )

    # TODO import animal nutrition data


    # Load data
    df_head_country = pd.read_csv(head_count_csv_location, index_col="iso3")
    df_slaughter_country = pd.read_csv(FAO_stat_slaughter_counts_processed_location, index_col="iso3")

    # merge the two dataframes on index
    df_animal_stock_info = pd.merge(df_head_country, df_slaughter_country, left_index=True, right_index=True)

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
        Path(animal_feed_data_dir), "animal_nutrition.csv"
    )

    df_animal_nutrition = pd.read_csv(animal_nutrition_data_location, index_col="animal_type")

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
    cattle_beef : object
        Object containing animal population data for beef cattle
    pigs : object
        Object containing animal population data for pigs
    chickens : object
        Object containing animal population data for chickens
    """

    
    # Create obnjects for each animal type, using the class SpeciesCurrentState, and populate with data from the dataframe
    cattle_beef = SpeciesCurrentState(
        animal_type="beef",
        population=df_animal_stock_info.loc["large_animals"],
        slaughter=df_animal_stock_info.loc["large_animal_slaughter"],
        pregnant=0,
        starving=0,
        feed_required=df_animal_nutrition.loc["beef_cattle"]["livestock_unit"],
        carb_requirement=df_animal_nutrition.loc["beef_cattle"]["carbohydrates_ratio"],
        protein_requirement=df_animal_nutrition.loc["beef_cattle"]["protein_ratio"],
        fat_requirement=df_animal_nutrition.loc["beef_cattle"]["fat_ratio"],
    )
    # now the same for pigs
    pigs = SpeciesCurrentState(
        animal_type="pigs",
        population=df_animal_stock_info.loc["medium_animals"],
        slaughter=df_animal_stock_info.loc["medium_animal_slaughter"],
        pregnant=0,
        starving=0,
        feed_required=df_animal_nutrition.loc["pigs"]["livestock_unit"],
        carb_requirement=df_animal_nutrition.loc["pigs"]["carbohydrates_ratio"],
        protein_requirement=df_animal_nutrition.loc["pigs"]["protein_ratio"],
        fat_requirement=df_animal_nutrition.loc["pigs"]["fat_ratio"],
    )
    # and chickens
    chickens = SpeciesCurrentState(
        animal_type="chickens",
        population=df_animal_stock_info.loc["small_animals"],
        slaughter=df_animal_stock_info.loc["small_animal_slaughter"],
        pregnant=0,
        starving=0,
        feed_required=df_animal_nutrition.loc["meat_chicken"]["livestock_unit"],
        carb_requirement=df_animal_nutrition.loc["meat_chicken"]["carbohydrates_ratio"],
        protein_requirement=df_animal_nutrition.loc["meat_chicken"]["protein_ratio"],
        fat_requirement=df_animal_nutrition.loc["meat_chicken"]["fat_ratio"],
    )
    # and dairy
    dairy = SpeciesCurrentState(
        animal_type="dairy",
        population=df_animal_stock_info.loc["dairy_cows"],
        slaughter=0,
        pregnant=0,
        starving=0,
        feed_required=df_animal_nutrition.loc["dairy_cattle"]["livestock_unit"],
        carb_requirement=df_animal_nutrition.loc["dairy_cattle"]["carbohydrates_ratio"],
        protein_requirement=df_animal_nutrition.loc["dairy_cattle"]["protein_ratio"],
        fat_requirement=df_animal_nutrition.loc["dairy_cattle"]["fat_ratio"],
    )

    # create a list of the objects
    animal_list = [cattle_beef, pigs, chickens, dairy]

    # return the list
    return animal_list


def create_available_feed_object():
    example_food1=Food(10,3,1)
    example_food2=Food(3,1,1)
    example_food3=Food(1,1,1)

    # add the food objects togetehr
    available_feed = example_food1 + example_food2 + example_food3

    return available_feed


def food_conversion():
    # convert food to animal feed

    return



def main(country_code):
    """
    Main function to be called by the user. This function will call the other functions in this file.
    """

    # read animal population data
    df_animal_stock_info = read_animal_population_data()

    # read animal nutrition data
    df_animal_nutrition = read_animal_nutrition_data()

    # create animal objects
    animal_list = create_animal_objects(df_animal_stock_info.loc[country_code], df_animal_nutrition)

    # create available feed object
    available_feed = create_available_feed_object()



# if __name__ == "__main__":
#     main("USA")

LSU = 1
kcal_per_LSU = 1
fatpercent = 0.05
carbpercent = 0.45
proteinpercent = 0.5

total_energy = Food.total_energy_in_food(Food(1,1,1))
print(total_energy)

# default cows eat 2% DM of fat, so 98g carbs/protein, 2g fat = 
# 18kcal from fat, 392 from carbs

