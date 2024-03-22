import pandas as pd
import git
from pathlib import Path
import numpy as np

repo_root = git.Repo(".", search_parent_directories=True).working_dir

print("importing seaweed...")

# minimum fraction of global seaweed in any country with coastline to start with
MIN_FRACTION_OF_GLOBAL_SEAWEED = 0.0005

NO_TRADE_XLS = (
    Path(repo_root)
    / "data"
    / "no_food_trade"
    / "raw_data"
    / "Integrated Model With No Food Trade.xlsx"
)

xls = pd.ExcelFile(NO_TRADE_XLS)

df_seaweed = pd.read_excel(xls, "Seaweed")

# Only use flag 0 and flag 1 countries
# Flag 2 countries are overestimates
# df_seaweed = df_seaweed[df_seaweed["Flags"] < 2]
# del df_seaweed["Flags"]

# drop all rows that have NaN values to remove
# the countries that are not able to grow seaweed
# df_seaweed = df_seaweed.dropna()
# Rename column ISO3 Country Code to iso3
df_seaweed = df_seaweed.rename(columns={"ISO3 Country Code": "iso3"})
# Change country column to all lower case
df_seaweed = df_seaweed.rename(columns={"Country": "country"})

df_seaweed_new = pd.DataFrame()
df_seaweed_new["iso3"] = df_seaweed["iso3"]
df_seaweed_new["country"] = df_seaweed["country"]
df_seaweed_new["max_area_fraction"] = 0
df_seaweed_new["new_area_fraction"] = 0
df_seaweed_new["initial_built_fraction"] = 0
df_seaweed_new["initial_seaweed_fraction"] = 0

# estimate seaweed maximum area limitations based on the fraction of available coast
total_coast = 0
for i in range(0, len(df_seaweed)):
    coast = df_seaweed["Length of coastline"].values[i]
    if not np.isnan(coast):
        total_coast += coast


growth_cols = df_seaweed.loc[
    :,
    ~df_seaweed.columns.isin(
        ["iso3", "country", "index", "Length of coastline", "Flags"]
    ),
].columns


# initialize to zero
for col in growth_cols:
    df_seaweed_new["seaweed_growth_per_day_" + str(col)] = 0

for i in range(0, len(df_seaweed)):
    coast_fraction = df_seaweed["Length of coastline"].values[i] / total_coast
    if (
        coast_fraction > 0
        and not df_seaweed.iloc[i].isnull().any()
        and df_seaweed["Flags"].values[i] < 2
    ):
        df_seaweed_new.loc[i, "new_area_fraction"] = coast_fraction
        df_seaweed_new.loc[i, "max_area_fraction"] = coast_fraction
        # make sure seaweed at start is at least 0.05% of global total in all countries
        df_seaweed_new.loc[i, "initial_seaweed_fraction"] = max(
            MIN_FRACTION_OF_GLOBAL_SEAWEED, coast_fraction
        )
        df_seaweed_new.loc[i, "initial_built_fraction"] = coast_fraction
        for col in growth_cols:
            df_seaweed_new.loc[i, "seaweed_growth_per_day_" + str(col)] = (
                df_seaweed.loc[i, col]
            )

# Save to file
df_seaweed_new.to_csv(
    Path(repo_root) / "data" / "no_food_trade" / "processed_data" / "seaweed_csv.csv",
    sep=",",
    index=False,
)
