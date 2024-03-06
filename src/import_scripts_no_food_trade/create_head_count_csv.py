from src.utilities.import_utilities import ImportUtilities
from pathlib import Path
import pandas as pd
import numpy as np
import git

repo_root = git.Repo(".", search_parent_directories=True).working_dir

print("importing animal stocks data...")

HEAD_COUNT_CSV = (
    Path(repo_root)
    / "data"
    / "no_food_trade"
    / "raw_data"
    / "FAOSTAT_animal_stocks_2020.csv"
)
DAIRY_HEAD_COUNT_CSV = (
    Path(repo_root)
    / "data"
    / "no_food_trade"
    / "raw_data"
    / "FAOSTAT_cow_heads_2020.csv"
)

TONS_TO_KG = 1e3
KCALS_TO_DRY_CALORIC_TONS = 1 / (4000 * 1000)

KCALS_PER_PERSON = 2100
FAT_PER_PERSON = 47
PROTEIN_PER_PERSON = 53

countries = ImportUtilities.country_codes
country_names = ImportUtilities.country_names

df_head_counts = pd.read_csv(HEAD_COUNT_CSV)[
    ["Area Code (ISO3)", "Item", "Unit", "Value"]
]
df_dairy_cow_counts = pd.read_csv(DAIRY_HEAD_COUNT_CSV)[
    ["Area Code (ISO3)", "Item", "Unit", "Value"]
]

merge_on = ["Area Code (ISO3)", "Item Code (FAO)", "Item", "Unit"]

# tacks on a column at the end with dairy cow for that country.
# The same dairy cow count is made to be repeated on all the
# rows of a given country in the left merge.

df_merge = df_head_counts.merge(df_dairy_cow_counts, on="Area Code (ISO3)", how="left")

df_dict = ImportUtilities.import_csv_from_df(df_merge, "Area Code (ISO3)")

# for each country create a list of macronutrient values
head_count_csv = np.array(
    [
        "iso3",
        "country",
        "small_animals",
        "medium_animals",
        "large_animals",
        "dairy_cows",
    ]
)

large_animals = ["Asses", "Buffaloes", "Camels", "Cattle", "Horses", "Mules"]

medium_animals = ["Goats", "Pigs", "Sheep"]

small_animals = [
    "Chickens",
    "Ducks",
    "Geese and guinea fowls",
    "Rabbits and hares",
    "Rodents, other",
    "Turkeys",
]

small_animal_sum_global = 0
medium_animal_sum_global = 0
large_animal_sum_global = 0
dairy_cow_count_global = 0

for i in range(0, len(countries)):
    country = countries[i]
    country_name = country_names[i]

    if country not in df_dict.keys():
        print("missing" + country)
        continue

    head_counts = df_dict[country]

    small_animal_sum = 0
    medium_animal_sum = 0
    large_animal_sum = 0

    # for each food product, add to each macronutrient total
    for index, head_count in head_counts.iterrows():
        if "1000" in head_count["Unit_x"]:
            multiplier = 1000
        else:
            multiplier = 1

        if np.isnan(head_count["Value_x"]):
            continue
        if head_count["Item_x"] in small_animals:
            small_animal_sum += multiplier * int(head_count["Value_x"])
            small_animal_sum_global += multiplier * int(head_count["Value_x"])

        if head_count["Item_x"] in medium_animals:
            medium_animal_sum += multiplier * int(head_count["Value_x"])
            medium_animal_sum_global += multiplier * int(head_count["Value_x"])

        if head_count["Item_x"] in large_animals:
            large_animal_sum += multiplier * int(head_count["Value_x"])
            large_animal_sum_global += multiplier * int(head_count["Value_x"])

    if np.isnan(head_counts.iloc[0]["Value_y"]):
        dairy_cow_count = 0
    else:
        dairy_cow_count = head_counts.iloc[0]["Value_y"]
        dairy_cow_count_global += head_counts.iloc[0]["Value_y"]

    head_count_csv = ImportUtilities.stack_on_list(
        head_count_csv,
        [
            country,
            country_name,
            small_animal_sum,
            medium_animal_sum,
            large_animal_sum,
            dairy_cow_count,
        ],
    )

PRINT_ALL_THE_GLOBAL_ANIMALS_FLAG = False
if PRINT_ALL_THE_GLOBAL_ANIMALS_FLAG:
    print("small_animal_sum_global")
    print(small_animal_sum_global / 1e9)
    print("medium_animal_sum_global")
    print(medium_animal_sum_global / 1e9)
    print("large_animal_sum_global")
    print(large_animal_sum_global / 1e9)
    print("dairy_cow_count_global")
    print(dairy_cow_count_global / 1e9)

head_count_csv = ImportUtilities.clean_up_eswatini(head_count_csv)

np.savetxt(
    Path(repo_root)
    / "data"
    / "no_food_trade"
    / "processed_data"
    / "head_count_csv.csv",
    head_count_csv,
    delimiter=",",
    fmt="%s",
)
