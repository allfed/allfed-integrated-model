import pandas as pd
import git
from pathlib import Path

repo_root = git.Repo(".", search_parent_directories=True).working_dir

print("importing relocation improvement...")

NO_TRADE_XLS = (
    Path(repo_root)
    / "data"
    / "no_food_trade"
    / "raw_data"
    / "Integrated Model With No Food Trade.xlsx"
)

xls = pd.ExcelFile(NO_TRADE_XLS)

df_improvement = pd.read_excel(xls, "Relocation Improvements")[
    ["ISO3 Country Code", "Country", "power_law_improvement"]
]

# Rename columns
df_improvement.columns = [
    "iso3",
    "country",
    "power_law_improvement",
]

df_improvement.to_csv(
    Path(repo_root)
    / "data"
    / "no_food_trade"
    / "processed_data"
    / "improvement_csv.csv",
    sep=",",
    index=False,
)
