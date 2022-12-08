import pandas as pd
import git
from pathlib import Path

repo_root = git.Repo(".", search_parent_directories=True).working_dir

print("importing seaweed...")

NO_TRADE_XLS = (
    Path(repo_root)
    / "data"
    / "no_food_trade"
    / "raw_data"
    / "Integrated Model With No Food Trade.xlsx"
)

xls = pd.ExcelFile(NO_TRADE_XLS)

df_seaweed = pd.read_excel(xls, "Seaweed")[
    [
        "ISO3 Country Code",
        "Country",
        "Fraction of total seaweed grown today -2019",
        "Within latitude where seaweed could be grown (30)",
        "Length of coastline",
    ]
]

# Rename columns
df_seaweed.columns = [
    "iso3",
    "country",
    "fraction_of_seaweed",
    "within_latitude",
    "coastline",
]
df_seaweed = df_seaweed.iloc[
    0:137,
]

df_seaweed_new = df_seaweed.copy()
df_seaweed_new.drop("fraction_of_seaweed", axis=1, inplace=True)
df_seaweed_new.drop("within_latitude", axis=1, inplace=True)
df_seaweed_new.drop("coastline", axis=1, inplace=True)
df_seaweed_new["max_area_fraction"] = 0
df_seaweed_new["new_area_fraction"] = 0
df_seaweed_new["initial_built_fraction"] = 0
df_seaweed_new["initial_seaweed_fraction"] = 0

total_coast = 0
for i in range(0, len(df_seaweed)):
    in_latitude_range = df_seaweed.within_latitude.values[i]
    coast = df_seaweed.coastline.values[i]
    if in_latitude_range == 1:  # and coast_fraction > 0:
        total_coast += coast
for i in range(0, len(df_seaweed)):
    seaweed_fraction = df_seaweed.fraction_of_seaweed.values[i]
    in_latitude_range = df_seaweed.within_latitude.values[i]
    coast_fraction = df_seaweed.coastline.values[i] / total_coast

    if in_latitude_range == 1:  # and coast_fraction > 0:
        df_seaweed_new.loc[i, "new_area_fraction"] = coast_fraction
        df_seaweed_new.loc[i, "max_area_fraction"] = coast_fraction
        # make sure seaweed at start is at least 0.05% of global total in all countries
        df_seaweed_new.loc[i, "initial_seaweed_fraction"] = max(
            0.0005, seaweed_fraction
        )
        df_seaweed_new.loc[i, "initial_built_fraction"] = coast_fraction
    else:
        df_seaweed_new.loc[i, "max_area_fraction"] = 0
        df_seaweed_new.loc[i, "new_area_fraction"] = 0
        df_seaweed_new.loc[i, "initial_seaweed_fraction"] = 0
        df_seaweed_new.loc[i, "initial_built_fraction"] = 0

df_seaweed_new.to_csv(
    Path(repo_root) / "data" / "no_food_trade" / "processed_data" / "seaweed_csv.csv",
    sep=",",
    index=False,
)
