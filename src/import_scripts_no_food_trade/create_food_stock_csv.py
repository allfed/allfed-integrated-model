import pandas as pd

NO_TRADE_XLS = "data/no_food_trade/raw_data/Integrated Model With No Food Trade.xlsx"

xls = pd.ExcelFile(NO_TRADE_XLS)

df_stock = pd.read_excel(xls, "Food Stocks")[
    [
        "ISO3 Country Code",
        "Country",
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    ]
]

# Rename columns
df_stock.columns = [
    "iso3",
    "country",
    "stocks_kcals_jan",
    "stocks_kcals_feb",
    "stocks_kcals_mar",
    "stocks_kcals_apr",
    "stocks_kcals_may",
    "stocks_kcals_jun",
    "stocks_kcals_jul",
    "stocks_kcals_aug",
    "stocks_kcals_sep",
    "stocks_kcals_oct",
    "stocks_kcals_nov",
    "stocks_kcals_dec",
]

df_stock["stocks_kcals_jan"] = df_stock["stocks_kcals_jan"] * 1e6
df_stock["stocks_kcals_feb"] = df_stock["stocks_kcals_feb"] * 1e6
df_stock["stocks_kcals_mar"] = df_stock["stocks_kcals_mar"] * 1e6
df_stock["stocks_kcals_apr"] = df_stock["stocks_kcals_apr"] * 1e6
df_stock["stocks_kcals_may"] = df_stock["stocks_kcals_may"] * 1e6
df_stock["stocks_kcals_jun"] = df_stock["stocks_kcals_jun"] * 1e6
df_stock["stocks_kcals_jul"] = df_stock["stocks_kcals_jul"] * 1e6
df_stock["stocks_kcals_aug"] = df_stock["stocks_kcals_aug"] * 1e6
df_stock["stocks_kcals_sep"] = df_stock["stocks_kcals_sep"] * 1e6
df_stock["stocks_kcals_oct"] = df_stock["stocks_kcals_oct"] * 1e6
df_stock["stocks_kcals_nov"] = df_stock["stocks_kcals_nov"] * 1e6
df_stock["stocks_kcals_dec"] = df_stock["stocks_kcals_dec"] * 1e6


df_stock = df_stock.iloc[
    0:138,
]

print("Food stocks")
print(df_stock.head())
df_stock.to_csv(
    "data/no_food_trade/processed_data/food_stock_csv.csv", sep=",", index=False
)
