import pandas as pd
import git

repo_root = git.Repo(".", search_parent_directories=True).working_dir

print("importing dairy data...")

NO_TRADE_XLS = (
    repo_root + "/data/no_food_trade/raw_data/Integrated Model With No Food Trade.xlsx"
)

xls = pd.ExcelFile(NO_TRADE_XLS)

df_dairy = pd.read_excel(xls, "Grazing Baseline")[
    ["ISO3 Country Code", "Country", "Current milk output - '000 tonnes wet value"]
]

# rename the columns and select the first 138 rows
df_dairy.columns = ["iso3", "country", "dairy"]
df_dairy["dairy"] = df_dairy["dairy"] * 1000
df_dairy = df_dairy.iloc[
    0:138,
]

df_dairy.to_csv(
    repo_root + "/data/no_food_trade/processed_data/dairy_csv.csv", sep=",", index=False
)
