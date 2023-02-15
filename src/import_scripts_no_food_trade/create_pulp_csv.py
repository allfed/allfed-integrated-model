import pandas as pd
import numpy as np
import git
from pathlib import Path
from src.utilities.import_utilities import ImportUtilities

repo_root = git.Repo(".", search_parent_directories=True).working_dir

print("importing wood pulp production...")

PULP_CSV = (
    Path(repo_root)
    / "data"
    / "no_food_trade"
    / "raw_data"
    / "FAOSTAT_wood_pulp_2020.csv"
)

country_codes = ImportUtilities.country_codes
country_names = ImportUtilities.country_names

df_pulp_countries = pd.read_csv(PULP_CSV)[
    ["Area Code (ISO3)", "Area", "Element", "Unit", "Value"]
]

# for each country create a list of macronutrient values
pulp_csv = np.array([])

for i in range(0, len(country_codes)):
    pulp_country = country_codes[i]
    country_name = country_names[i]
    if pulp_country not in list(df_pulp_countries["Area Code (ISO3)"]):
        PRINT_ALL_THE_MISSING_WOOD_PULP_COUNTRIES = False
        if PRINT_ALL_THE_MISSING_WOOD_PULP_COUNTRIES:
            print("missing " + country_name)
        pulp = 0.0
    else:
        pulp = float(
            df_pulp_countries[df_pulp_countries["Area Code (ISO3)"] == pulp_country][
                "Value"
            ]
        )
    pulp_csv = ImportUtilities.stack_on_list(
        pulp_csv, [pulp_country, country_name, pulp]
    )


pulp_csv = ImportUtilities.clean_up_eswatini(pulp_csv)

pulp_csv = pd.DataFrame(pulp_csv, columns=["iso3", "country", "wood_pulp_tonnes"])
pulp_csv["wood_pulp_tonnes"] = pulp_csv["wood_pulp_tonnes"].astype(float)

pulp_csv["percent_of_global_production"] = pulp_csv["wood_pulp_tonnes"] / (
    pulp_csv["wood_pulp_tonnes"].sum()
)

pulp_csv.to_csv(
    Path(repo_root) / "data" / "no_food_trade" / "processed_data" / "pulp_csv.csv",
    sep=",",
    index=False,
)
