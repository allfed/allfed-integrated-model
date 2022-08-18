import pandas as pd
import numpy as np
import os

NO_TRADE_XLS = (
    "../../data/no_food_trade/raw_data/Integrated Model With No Food Trade.xlsx"
)

xls = pd.ExcelFile(NO_TRADE_XLS)

df_seasonality = pd.read_excel(xls, "Outdoor Crop Seasonality")[
    [
        "ISO3 Country Code",
        "Country",
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]
]

# Rename columns
df_seasonality.columns = [
    "iso3",
    "country",
    "seasonality_m1",
    "seasonality_m2",
    "seasonality_m3",
    "seasonality_m4",
    "seasonality_m5",
    "seasonality_m6",
    "seasonality_m7",
    "seasonality_m8",
    "seasonality_m9",
    "seasonality_m10",
    "seasonality_m11",
    "seasonality_m12",
]

print("Crop seasonality")
print(df_seasonality.head())
df_seasonality.to_csv(
    "../../data/no_food_trade/processed_data/seasonality_csv.csv", sep=",", index=False
)
