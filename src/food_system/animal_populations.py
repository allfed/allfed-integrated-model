"""
This is a function used to quickly estimate the feed usage and resulting meat when
breeding is changed and slaughter is increased somewhat (or whatever reasonable result
is to be expected in the scenario in question).
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
class SpeciesCurrentState:
    def __init__(self, animal_type, population, slaughter, pregnant):
        self.animal_type = animal_type
        self.population = population
        self.slaughter = slaughter
        self.pregnant = pregnant



# create function that reads CSV info and populates the classes
def read_animal_population_data(country_code):

    repo_root = git.Repo(".", search_parent_directories=True).working_dir
    # Load data
    animal_feed_data_dir = Path(repo_root) / "data" / "no_food_trade" / "animal_feed_data"

    FAO_stat_slaughter_counts_processed_location = Path.joinpath(
        Path(animal_feed_data_dir), "FAO_stat_slaughter_counts_processed.csv"
    )
    head_count_csv_location = Path.joinpath(
        Path(animal_feed_data_dir), "head_count_csv.csv"
    )

    # TODO import animal nutirtion data


    # Load data
    df_head_country = pd.read_csv(head_count_csv_location, index_col="iso3")
    df_slaughter_country = pd.read_csv(FAO_stat_slaughter_counts_processed_location, index_col="iso3")

    # merge the two dataframes on index
    df_animal_stock_info = pd.merge(df_head_country, df_slaughter_country, left_index=True, right_index=True)
    
    # only keep the rows that match the country code
    # df_animal_stock_info = df_animal_stock_info.loc[country_code]

    # Create obnjects for each animal type, using the class SpeciesCurrentState, and populate with data from the dataframe
    cattle_beef = SpeciesCurrentState(
        animal_type="beef",
        population=df_animal_stock_info.loc[country_code]["large_animals"],
        slaughter=df_animal_stock_info.loc[country_code]["large_animal_slaughter"],
        pregnant=0,
    )
    # now the same for pigs
    pigs = SpeciesCurrentState(
        animal_type="pigs",
        population=df_animal_stock_info.loc[country_code]["medium_animals"],
        slaughter=df_animal_stock_info.loc[country_code]["medium_animal_slaughter"],
        pregnant=0,
    )
    # and chickens
    chickens = SpeciesCurrentState(
        animal_type="chickens",
        population=df_animal_stock_info.loc[country_code]["small_animals"],
        slaughter=df_animal_stock_info.loc[country_code]["small_animal_slaughter"],
        pregnant=0,
    )
    # and dairy
    dairy = SpeciesCurrentState(
        animal_type="dairy",
        population=df_animal_stock_info.loc[country_code]["dairy_cows"],
        slaughter=0,
        pregnant=0,
    )

    # create a list of the objects
    animal_list = [cattle_beef, pigs, chickens, dairy]

    # return the list
    return animal_list



    




# create instance of class
cattle_beef = SpeciesCurrentState(
    animal_type="beef",
    population=100,
    slaughter=100,
    pregnant=100,
)


total_feed_available = Food(
    kcals=1000,
    fat=1000,
    protein=1000,
    kcals_units="thousand dry caloric tons per year",
    fat_units="tons per year",
    protein_units="tons per year",
)








animals = read_animal_population_data("USA")

# sum the populations of all animals
total_animal_population = sum([animal.population for animal in animals])

print(total_animal_population)
