import pandas as pd
import numpy as np
import os

NO_TRADE_XLS = "data/no_food_trade/raw_data/Integrated Model With No Food Trade.xlsx"

xls = pd.ExcelFile(NO_TRADE_XLS)

df_feed = pd.read_excel(xls, "Feed")[
    [
        "ISO3 Country Code",
        "Country",
        "Animal feed caloric consumption in 2020 (million dry caloric tons)",
        "Animal feed fat consumption in 2020 (million tonnes)",
        "Animal feed protein consumption in 2020 (million tonnes)",
    ]
]

# Rename columns
df_feed.columns = ["iso3", "country", "feed_kcals", "feed_fat", "feed_protein"]


df_feed["feed_kcals"] = df_feed["feed_kcals"] * 1e6
df_feed["feed_fat"] = df_feed["feed_fat"] * 1e6
df_feed["feed_protein"] = df_feed["feed_protein"] * 1e6
df_feed = df_feed.iloc[
    0:138,
]

print("Feed")
print(df_feed.head())
df_feed.to_csv("data/no_food_trade/processed_data/feed_csv.csv", sep=",", index=False)
