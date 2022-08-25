import pandas as pd
import git

repo_root = git.Repo(".", search_parent_directories=True).working_dir

print("importing seaweed...")

NO_TRADE_XLS = (
    repo_root + "/data/no_food_trade/raw_data/Integrated Model With No Food Trade.xlsx"
)

xls = pd.ExcelFile(NO_TRADE_XLS)

df_seaweed = pd.read_excel(xls, "Seaweed")[
    [
        "ISO3 Country Code",
        "Country",
        "Fraction of total seaweed grown today -2019",
        "Within latitude where seaweed could be grown (30)",
        "Length of coastline",
    ]
]

# Rename columns
df_seaweed.columns = ["iso3", "country", "percent_of_seaweed"]
df_seaweed = df_seaweed.iloc[
    0:138,
]
for i in range(0, len(df_seaweed)):
    percent = df_seaweed.percent_of_seaweed.values[i]
    # make sure seaweed is at least 0.05% of global total in all countrie4s
    df_seaweed.loc[i, "initial_seaweed_percent"] = max(0.0005, percent)3
print(sum(df_seaweed["initial_seaweed_percent"].values))
# quit()

# df_seaweed.to_csv(
#     repo_root + "/data/no_food_trade/processed_data/seaweed_csv.csv",
#     sep=",",
#     index=False,
# )
