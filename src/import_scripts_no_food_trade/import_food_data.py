"""
################################Optimizer Model################################
##                                                                            #
##                merge all the csv files together to a computer readable     #
##                                                                            #
###############################################################################
"""


import pandas as pd
from functools import reduce
import git

repo_root = git.Repo(".", search_parent_directories=True).working_dir

print("")
print("chunking all the cvs's into computer_readable_combined...")
print("")


df1 = pd.read_csv(repo_root + "/data/no_food_trade/processed_data/population_csv.csv")
df2 = pd.read_csv(repo_root + "/data/no_food_trade/processed_data/aquaculture_csv.csv")
df3 = pd.read_csv(
    repo_root + "/data/no_food_trade/processed_data/grasses_baseline_csv.csv"
)
df4 = pd.read_csv(repo_root + "/data/no_food_trade/processed_data/dairy_csv.csv")
df5 = pd.read_csv(repo_root + "/data/no_food_trade/processed_data/meat_csv.csv")
df6 = pd.read_csv(repo_root + "/data/no_food_trade/processed_data/head_count_csv.csv")
df7 = pd.read_csv(repo_root + "/data/no_food_trade/processed_data/biofuel_csv.csv")
df8 = pd.read_csv(repo_root + "/data/no_food_trade/processed_data/feed_csv.csv")
df9 = pd.read_csv(repo_root + "/data/no_food_trade/processed_data/macros_csv.csv")
df10 = pd.read_csv(
    repo_root + "/data/no_food_trade/processed_data/nuclear_winter_csv.csv"
)
df11 = pd.read_csv(repo_root + "/data/no_food_trade/processed_data/seasonality_csv.csv")
df12 = pd.read_csv(repo_root + "/data/no_food_trade/processed_data/food_stock_csv.csv")
df13 = pd.read_csv(repo_root + "/data/no_food_trade/processed_data/food_waste_csv.csv")
df14 = pd.read_csv(repo_root + "/data/no_food_trade/processed_data/pulp_csv.csv")
df15 = pd.read_csv(repo_root + "/data/no_food_trade/processed_data/scp_csv.csv")
df16 = pd.read_csv(repo_root + "/data/no_food_trade/processed_data/greenhouse_csv.csv")
df17 = pd.read_csv(repo_root + "/data/no_food_trade/processed_data/seaweed_csv.csv")


dataframes = [
    df1,
    df2,
    df3,
    df4,
    df5,
    df6,
    df7,
    df8,
    df9,
    df10,
    df11,
    df12,
    df13,
    df14,
    df15,
    df16,
    df17,
]

# everestial007 explains the merge quite neatly
# https://stackoverflow.com/questions/44327999/python-pandas-merge-multiple-dataframes
df_merged = reduce(
    lambda left, right: pd.merge(  # Merge DataFrames in list
        left, right, on=["iso3", "country"], how="left"
    ),
    dataframes,
)


df_merged.to_csv(
    repo_root + "/data/no_food_trade/computer_readable_combined.csv",
    sep=",",
    index=False,
)
