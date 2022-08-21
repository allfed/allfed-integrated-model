import pandas as pd

print("importing seafood data...")

NO_TRADE_XLS = (
    "../../data/no_food_trade/raw_data/Integrated Model With No Food Trade.xlsx"
)

xls = pd.ExcelFile(NO_TRADE_XLS)

df_aquaculture = pd.read_excel(xls, "Seafood - excluding seaweeds")[
    [
        "ISO3 Country Code",
        "Country",
        "Seafood calories - million tonnes dry caloric, 2020",
        "Seafood fat - million tonnes, 2020",
        "Seafood protein - million tonnes, 2020",
    ]
]

# rename the columns and select the first 138 rows
df_aquaculture.columns = ["iso3", "country", "aq_kcals", "aq_fat", "aq_protein"]
df_aquaculture["aq_kcals"] = df_aquaculture["aq_kcals"] * 1e6
df_aquaculture["aq_fat"] = df_aquaculture["aq_fat"] * 1e6
df_aquaculture["aq_protein"] = df_aquaculture["aq_protein"] * 1e6

df_aquaculture = df_aquaculture.iloc[
    0:138,
]

df_aquaculture.to_csv(
    "../../data/no_food_trade/processed_data/aquaculture_csv.csv", sep=",", index=False
)
