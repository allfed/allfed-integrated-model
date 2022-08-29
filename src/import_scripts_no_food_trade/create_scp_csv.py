from pathlib import Path
import pandas as pd
import git

repo_root = git.Repo(".", search_parent_directories=True).working_dir

print("importing single cell protein...")

NO_TRADE_XLS = (
    Path(repo_root)
    / "data"
    / "no_food_trade"
    / "raw_data"
    / "Integrated Model With No Food Trade.xlsx"
)

xls = pd.ExcelFile(NO_TRADE_XLS)

df_scp = pd.read_excel(xls, "Methane SCP")[
    [
        "ISO3 Country Code",
        "Country",
        "Estimated Capex for related industries - Average 2014-2018 - 2015 US$ billion basis",
        "% of global chemical and related CAPEX",
    ]
]
df_scp.columns = ["iso3", "country", "capex_dollar", "percent_of_global_capex"]


df_scp = df_scp.iloc[
    0:138,
]

df_scp.to_csv(
    Path(repo_root) / "data" / "no_food_trade" / "processed_data" / "scp_csv.csv",
    sep=",",
    index=False,
)
