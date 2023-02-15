from pathlib import Path
import pandas as pd
import git

repo_root = git.Repo(".", search_parent_directories=True).working_dir

print("importing greenhouse relevant data...")


NO_TRADE_XLS = (
    Path(repo_root)
    / "data"
    / "no_food_trade"
    / "raw_data"
    / "Integrated Model With No Food Trade.xlsx"
)

xls = pd.ExcelFile(NO_TRADE_XLS)

df_greenhouse = pd.read_excel(xls, "Greenhouses")[
    [
        "ISO3 Country Code",
        "Country",
        "Country Crop Area ('000 Hectares)",
        "Whether to assess greenhouse improvement",
        "Fraction of total crop area",
    ]
]
# rename columns
df_greenhouse.columns = [
    "iso3",
    "country",
    "crop_area_1000ha",
    "include_greenhouse",
    "fraction_crop_area",
]


df_greenhouse.to_csv(
    Path(repo_root)
    / "data"
    / "no_food_trade"
    / "processed_data"
    / "greenhouse_csv.csv",
    sep=",",
    index=False,
)
