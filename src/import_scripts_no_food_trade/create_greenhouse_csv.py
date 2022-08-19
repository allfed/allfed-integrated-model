import pandas as pd
import numpy as np
import os

NO_TRADE_XLS = (
    "data/no_food_trade/raw_data/Integrated Model With No Food Trade.xlsx"
)

xls = pd.ExcelFile(NO_TRADE_XLS)

df_greenhouse = pd.read_excel(xls, "Greenhouses")[
    [
        "ISO3 Country Code",
        "Country",
        "Country Crop Area ('000 Hectares)",
        "Latitude",
        "Whether above latitude threshold (23)",
        "Fraction of total crop area - below 23 latitude",
    ]
]
# rename columns
df_greenhouse.columns = [
    "iso3",
    "country",
    "crop_area_1000ha",
    "latitude",
    "above_lat_23_boolean",
    "fraction_crop_area_below_lat_23",
]


print("Greenhouse")
print(df_greenhouse.head())
df_greenhouse.to_csv(
    "data/no_food_trade/processed_Data/greenhouse_csv.csv", sep=",", index=False
)
