import pandas as pd
import git
from pathlib import Path

repo_root = git.Repo(".", search_parent_directories=True).working_dir

print("importing baseline grass production data...")

NO_TRADE_XLS = (
    Path(repo_root)
    / "data"
    / "no_food_trade"
    / "raw_data"
    / "Integrated Model With No Food Trade.xlsx"
)

xls = pd.ExcelFile(NO_TRADE_XLS)

df_grasses = pd.read_excel(xls, "Grazing Baseline")[
    [
        "ISO3 Country Code",
        "Country",
        "Inedible food for ruminants - Baseline 2020 - '000 tonnes",
    ]
]

# rename the columns
df_grasses.columns = ["iso3", "country", "grasses_baseline"]

# convert from thousand tons to million tons
df_grasses["grasses_baseline"] = df_grasses["grasses_baseline"] / 1000

df_grasses.to_csv(
    Path(repo_root)
    / "data"
    / "no_food_trade"
    / "processed_data"
    / "grasses_baseline_csv.csv",
    sep=",",
    index=False,
)
