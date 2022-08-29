from pathlib import Path
import pandas as pd
import git

repo_root = git.Repo(".", search_parent_directories=True).working_dir

print("importing population...")

NO_TRADE_XLS = (
    Path(repo_root)
    / "data"
    / "no_food_trade"
    / "raw_data"
    / "Integrated Model With No Food Trade.xlsx"
)

xls = pd.ExcelFile(NO_TRADE_XLS)

df_pop = pd.read_excel(xls, "Population")[
    ["ISO3 Country Code", "Country", "Population (millions), 2020"]
]

# Rename columns
df_pop.columns = ["iso3", "country", "population"]


df_pop["population"] = df_pop["population"] * 1e6
df_pop = df_pop.iloc[
    0:138,
]

df_pop.to_csv(
    Path(repo_root)
    / "data"
    / "no_food_trade"
    / "processed_data"
    / "population_csv.csv",
    sep=",",
    index=False,
)
