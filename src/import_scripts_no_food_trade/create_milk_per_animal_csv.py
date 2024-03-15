from pathlib import Path
import pandas as pd
import git

repo_root = git.Repo(".", search_parent_directories=True).working_dir

print("importing milk yield per animal...")

NO_TRADE_XLS = (
    Path(repo_root)
    / "data"
    / "no_food_trade"
    / "raw_data"
    / "Integrated Model With No Food Trade.xlsx"
)

xls = pd.ExcelFile(NO_TRADE_XLS)

df_milk = pd.read_excel(xls, "Milk per animal")[
    [
        "ISO3 Country Code",
        "Country",
        "Yield (kg/animal/yr)",
    ]
]
df_milk.columns = ["iso3", "country", "milk_yield_kg_per_milk_bearing_animal_per_year"]

# only keep rows where iso3 is also in head_count_csv.csv
df_head_counts = pd.read_csv(
    Path(repo_root) / "data" / "no_food_trade" / "processed_data" / "head_count_csv.csv"
)
df_milk = df_milk[df_milk["iso3"].isin(df_head_counts["iso3"])]


df_milk.to_csv(
    Path(repo_root)
    / "data"
    / "no_food_trade"
    / "processed_data"
    / "milk_per_animal_csv.csv",
    sep=",",
    index=False,
)
