from pathlib import Path
import pandas as pd
import git

repo_root = git.Repo(".", search_parent_directories=True).working_dir

print("importing meat yield per animal...")

NO_TRADE_XLS = (
    Path(repo_root)
    / "data"
    / "no_food_trade"
    / "raw_data"
    / "Integrated Model With No Food Trade.xlsx"
)

xls = pd.ExcelFile(NO_TRADE_XLS)

df_meat = pd.read_excel(xls, "Meat per animal")[
    [
        "ISO3 Country Code",
        "Country",
        "Meat per pig (kg)",
        "Meat per chicken (kg)",
    ]
]
df_meat.columns = ["iso3", "country", "kg_meat_per_pig", "kg_meat_per_chicken"]

# only keep rows where iso3 is also in head_count_csv.csv
df_head_counts = pd.read_csv(
    Path(repo_root) / "data" / "no_food_trade" / "processed_data" / "head_count_csv.csv"
)
df_meat = df_meat[df_meat["iso3"].isin(df_head_counts["iso3"])]


df_meat.to_csv(
    Path(repo_root)
    / "data"
    / "no_food_trade"
    / "processed_data"
    / "meat_per_animal_csv.csv",
    sep=",",
    index=False,
)
