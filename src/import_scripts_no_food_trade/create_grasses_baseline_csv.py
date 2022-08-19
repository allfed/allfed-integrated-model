import pandas as pd
import numpy as np
import os

NO_TRADE_XLS = "data/no_food_trade/raw_data/Integrated Model With No Food Trade.xlsx"

xls = pd.ExcelFile(NO_TRADE_XLS)

df_grasses = pd.read_excel(xls, "Grazing Baseline")[
    [
        "ISO3 Country Code",
        "Country",
        "Inedible food for ruminants - Baseline 2020 - '000 tonnes",
    ]
]

# rename the columns and select the first 138 rows
df_grasses.columns = ["iso3", "country", "grasses_baseline"]
df_grasses["grasses_baseline"] = df_grasses["grasses_baseline"] * 1000
df_grasses = df_grasses.iloc[
    0:138,
]

print("Grasses baseline")
print(df_grasses.head())
df_grasses.to_csv(
    "data/no_food_trade/processed_data/grasses_baseline_csv.csv",
    sep=",",
    index=False,
)
