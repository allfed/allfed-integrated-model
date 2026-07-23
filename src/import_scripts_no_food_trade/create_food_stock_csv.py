from pathlib import Path
import pandas as pd
import git

repo_root = git.Repo(".", search_parent_directories=True).working_dir

print("importing food stocks data...")

BASE_STOCKS_CSV = (
    Path(repo_root) / "data" / "no_food_trade" / "raw_data" / "base_stocks.csv"
)

df_stock = pd.read_csv(BASE_STOCKS_CSV)

# The base stocks dataset provides a single stock level per country in millions
# of tonnes (dry caloric equivalent). The model's data schema expects end-of-month
# stocks for all 12 months in tonnes, so the base value is applied to every month.
MONTH_COLUMNS = [
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

for month_column in MONTH_COLUMNS:
    df_stock[month_column] = df_stock["base_stocks_million_tonnes"] * 1e6

df_stock = df_stock[["iso3", "country"] + MONTH_COLUMNS]

df_stock.to_csv(
    Path(repo_root)
    / "data"
    / "no_food_trade"
    / "processed_data"
    / "food_stock_csv.csv",
    sep=",",
    index=False,
)
