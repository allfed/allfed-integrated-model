import pandas as pd
import numpy as np
import os

NO_TRADE_XLS = "data/no_food_trade/raw_data/Integrated Model With No Food Trade.xlsx"

xls = pd.ExcelFile(NO_TRADE_XLS)

df_seaweed = pd.read_excel(xls, "Seaweed")[
    ["ISO3 Country Code", "Country", "Fraction of total seaweed grown today -2019"]
]

# Rename columns
df_seaweed.columns = ["iso3", "country", "percent_of_seaweed"]
df_seaweed = df_seaweed.iloc[
    0:138,
]

print("Seaweed")
print(df_seaweed.head())
df_seaweed.to_csv(
    "data/no_food_trade/processed_data/seaweed_csv.csv", sep=",", index=False
)
