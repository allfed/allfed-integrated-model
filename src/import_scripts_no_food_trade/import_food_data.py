"""
Created on Tues Oct 25 2022
@author: Morgan Rivers

Merge all the csv files together to a computer readable file.
The output is saved in data/no_food_trade/computer_readable_file.py.

"""


from pathlib import Path
import pandas as pd
from functools import reduce
import git
from src.utilities.import_utilities import ImportUtilities

repo_root = git.Repo(".", search_parent_directories=True).working_dir

print("")
print("chunking all the cvs's into computer_readable_combined...")
print("")


df1 = pd.read_csv(
    Path(repo_root) / "data" / "no_food_trade" / "processed_data" / "population_csv.csv"
)
df2 = pd.read_csv(
    Path(repo_root)
    / "data"
    / "no_food_trade"
    / "processed_data"
    / "aquaculture_csv.csv"
)
df3 = pd.read_csv(
    Path(repo_root)
    / "data"
    / "no_food_trade"
    / "processed_data"
    / "grasses_baseline_csv.csv"
)
df4 = pd.read_csv(
    Path(repo_root) / "data" / "no_food_trade" / "processed_data" / "dairy_csv.csv"
)
df5 = pd.read_csv(
    Path(repo_root) / "data" / "no_food_trade" / "processed_data" / "meat_csv.csv"
)
df6 = pd.read_csv(
    Path(repo_root) / "data" / "no_food_trade" / "processed_data" / "head_count_csv.csv"
)
df7 = pd.read_csv(
    Path(repo_root) / "data" / "no_food_trade" / "processed_data" / "biofuel_csv.csv"
)
df8 = pd.read_csv(
    Path(repo_root) / "data" / "no_food_trade" / "processed_data" / "feed_csv.csv"
)
df9 = pd.read_csv(
    Path(repo_root) / "data" / "no_food_trade" / "processed_data" / "macros_csv.csv"
)
df10 = pd.read_csv(
    Path(repo_root)
    / "data"
    / "no_food_trade"
    / "processed_data"
    / "nuclear_winter_csv.csv"
)
df11 = pd.read_csv(
    Path(repo_root)
    / "data"
    / "no_food_trade"
    / "processed_data"
    / "seasonality_csv.csv"
)
df12 = pd.read_csv(
    Path(repo_root) / "data" / "no_food_trade" / "processed_data" / "food_stock_csv.csv"
)
df13 = pd.read_csv(
    Path(repo_root) / "data" / "no_food_trade" / "processed_data" / "food_waste_csv.csv"
)
df14 = pd.read_csv(
    Path(repo_root) / "data" / "no_food_trade" / "processed_data" / "pulp_csv.csv"
)
df15 = pd.read_csv(
    Path(repo_root) / "data" / "no_food_trade" / "processed_data" / "scp_csv.csv"
)
df16 = pd.read_csv(
    Path(repo_root) / "data" / "no_food_trade" / "processed_data" / "greenhouse_csv.csv"
)
df17 = pd.read_csv(
    Path(repo_root) / "data" / "no_food_trade" / "processed_data" / "seaweed_csv.csv"
)
df18 = pd.read_csv(
    Path(repo_root)
    / "data"
    / "no_food_trade"
    / "processed_data"
    / "improvement_csv.csv"
)

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
    df18,
]


# df1 (population) has ground truth country names
# and any null rows in the "population" dataframe is dropped, as the merge will
# only keep rows which exist in df1
dataframes_for_merge = [df1.dropna()]  # will add the rest soon


# replace eswatini country code in the list (proper code is SWT now, not swaziland SWZ)
expected_country_codes = ImportUtilities.country_codes
for i in range(len(expected_country_codes)):
    expected_country_codes[i] = expected_country_codes[i].replace("SWZ", "SWT")


index = 0
for df in dataframes:
    # go through to clean up the dataframes by removing the "country" column
    # this is because it messes up the merge when a column repeats with different
    # values. Country names vary a bit in the raw data (ie, Cabo Verde vs Cape Verde)

    index += 1

    # useful if there's something going on with the data and we want to see what is
    # going wrong
    PRINT_ABOUT_IMPORTED_DATA = False
    if PRINT_ABOUT_IMPORTED_DATA:
        print("df index:" + str(index))
        print("df columns")
        print(df.columns)
        print("in country_codes but not the dataframe")
        print(set(expected_country_codes) - set(df["iso3"].values))
        print("rows with NaN in this dataframe")
        print(pd.concat([df, df.dropna()]).drop_duplicates(keep=False))
        print("")

    if index >= 2:  # already added the first one
        # drop country column if exists
        df_dropped_country = (
            df.drop("country", axis=1) if ("country" in df.columns) else df
        )

        # build up the cleaned data frame which will merge all the columns
        dataframes_for_merge.append(df_dropped_country)

# just add all the columns to a big df_merged dataframe, as long as the dataframes
# being merged have matching "iso3" codes with all the others.
# Any dataframes with missing iso3 country code will remove that row from the combined
# merge.
# everestial007 explains the merge quite neatly
# https://stackoverflow.com/questions/44327999/python-pandas-merge-multiple-dataframes
df_merged = reduce(
    lambda left, right: pd.merge(  # Merge DataFrames in list
        left, right, on=["iso3"], how="inner"
    ),
    dataframes_for_merge,
)

assert (
    not df_merged.isnull().values.any()
), "Error: there were null values in computer_readable_combined dataframe"

assert set(df_merged["iso3"].values) == set(
    expected_country_codes
), """Error: number of countries imported disagrees from "ground truth" countries to
import, specified in ImportUtilities file"""

df_merged.to_csv(
    Path(repo_root) / "data" / "no_food_trade" / "computer_readable_combined.csv",
    sep=",",
    index=False,
)
