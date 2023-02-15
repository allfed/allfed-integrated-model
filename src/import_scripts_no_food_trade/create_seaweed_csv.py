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

df_seaweed = pd.read_excel(xls, "Seaweed")
# Remove unused columns
del df_seaweed["Length of coastline"]

# Only use flag 0 and flag 1 countries
# Flag 2 countries are overestimates
df_seaweed = df_seaweed[df_seaweed["Flags"] < 2]
del df_seaweed["Flags"]

# drop all rows that have NaN values to remove
# the countries that are not able to grow seaweed
df_seaweed = df_seaweed.dropna()

# Rename column ISO3 Country Code to iso3
df_seaweed = df_seaweed.rename(columns={"ISO3 Country Code": "iso3"})
# Change country column to all lower case
df_seaweed = df_seaweed.rename(columns={"Country": "country"})

# Save to file
df_seaweed.to_csv(
    Path(repo_root) / "data" / "no_food_trade" / "processed_data" / "seaweed_csv.csv",
    sep=",",
    index=False,
)
