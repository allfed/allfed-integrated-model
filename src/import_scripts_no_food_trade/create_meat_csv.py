from pathlib import Path
import pandas as pd
import numpy as np
import git
from src.utilities.import_utilities import ImportUtilities

repo_root = git.Repo(".", search_parent_directories=True).working_dir

MEAT_CSV = (
    Path(repo_root) / "data" / "no_food_trade" / "raw_data" / "FAOSTAT_meat_2020.csv"
)

print("importing meat data...")


TONS_TO_KG = 1e3
KCALS_TO_DRY_CALORIC_TONS = 1 / (4000 * 1000)

KCALS_PER_PERSON = 2100
FAT_PER_PERSON = 47
PROTEIN_PER_PERSON = 53

countries = ImportUtilities.country_codes

country_names = ImportUtilities.country_names

csv_loc = MEAT_CSV
col_names = ["Area Code (ISO3)", "Item", "Unit", "Value"]
iso3_col_name = "Area Code (ISO3)"

df_dict = ImportUtilities.import_csv(csv_loc, col_names, iso3_col_name)

# for each country create a list of macronutrient values
meat_csv = np.array(
    [
        "iso3",
        "country",
        "chicken",
        "pork",
        "beef",
    ]
)

chicken_sum_global = 0
pork_sum_global = 0
beef_sum_global = 0
for i in range(0, len(countries)):
    country = countries[i]
    country_name = country_names[i]
    if country not in df_dict.keys():
        print("missing" + country)
        continue

    meat_for_country = df_dict[country]
    chicken = 0
    beef = 0
    pork = 0

    # for each food product, add to each macronutrient total
    for index, meat in meat_for_country.iterrows():
        assert meat["Unit"] == "tonnes"

        if np.isnan(meat["Value"]):
            continue

        if meat["Item"] == "Meat, chicken":
            chicken = meat["Value"]
            chicken_sum_global += chicken

        if meat["Item"] == "Meat, pig":
            pork = meat["Value"]
            pork_sum_global += pork

        if meat["Item"] == "Meat, cattle":
            beef = meat["Value"]
            beef_sum_global += beef

    meat_csv = ImportUtilities.stack_on_list(
        meat_csv, [country, country_name, chicken, pork, beef]
    )

PRINT_MEAT_DATA = False
if PRINT_MEAT_DATA:
    print("chicken")
    print(chicken_sum_global / 1e9)
    print("pork")
    print(pork_sum_global / 1e9)
    print("beef")
    print(beef_sum_global / 1e9)

meat_csv = ImportUtilities.clean_up_eswatini(meat_csv)

np.savetxt(
    Path(repo_root) / "data" / "no_food_trade" / "processed_data" / "meat_csv.csv",
    meat_csv,
    delimiter=",",
    fmt="%s",
)
