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

countries = [
    "AFG",
    "ALB",
    "DZA",
    "AGO",
    "ARG",
    "ARM",
    "AUS",
    "AZE",
    "BHR",
    "BGD",
    "BRB",
    "BLR",
    "BEN",
    "BTN",
    "BOL",
    "BIH",
    "BWA",
    "BRA",
    "BRN",
    "BFA",
    "MMR",
    "BDI",
    "CPV",
    "KHM",
    "CMR",
    "CAN",
    "CAF",
    "TCD",
    "CHL",
    "CHN",
    "COL",
    "COD",
    "COG",
    "CRI",
    "CIV",
    "CUB",
    "DJI",
    "DOM",
    "ECU",
    "EGY",
    "SLV",
    "ERI",
    "SWZ",
    "ETH",
    "F5707",
    "GBR",
    "FJI",
    "GAB",
    "GMB",
    "GEO",
    "GHA",
    "GTM",
    "GIN",
    "GNB",
    "GUY",
    "HTI",
    "HND",
    "IND",
    "IDN",
    "IRN",
    "IRQ",
    "ISR",
    "JAM",
    "JPN",
    "JOR",
    "KAZ",
    "KEN",
    "KOR",
    "PRK",
    "KWT",
    "KGZ",
    "LAO",
    "LBN",
    "LSO",
    "LBR",
    "LBY",
    "MDG",
    "MWI",
    "MYS",
    "MLI",
    "MRT",
    "MUS",
    "MEX",
    "MDA",
    "MNG",
    "MAR",
    "MOZ",
    "NAM",
    "NPL",
    "NZL",
    "NIC",
    "NER",
    "NGA",
    "MKD",
    "NOR",
    "OMN",
    "PAK",
    "PAN",
    "PNG",
    "PRY",
    "PER",
    "PHL",
    "QAT",
    "RUS",
    "RWA",
    "SAU",
    "SEN",
    "SRB",
    "SLE",
    "SGP",
    "SOM",
    "ZAF",
    "SSD",
    "LKA",
    "SDN",
    "SUR",
    "CHE",
    "SYR",
    "TWN",
    "TJK",
    "TZA",
    "THA",
    "TGO",
    "TTO",
    "TUN",
    "TUR",
    "TKM",
    "UGA",
    "UKR",
    "ARE",
    "USA",
    "URY",
    "UZB",
    "VEN",
    "VNM",
    "YEM",
    "ZMB",
    "ZWE",
]

country_names = [
    "Afghanistan",
    "Albania",
    "Algeria",
    "Angola",
    "Argentina",
    "Armenia",
    "Australia",
    "Azerbaijan",
    "Bahrain",
    "Bangladesh",
    "Barbados",
    "Belarus",
    "Benin",
    "Bhutan",
    "Bolivia (Plurinational State of)",
    "Bosnia and Herzegovina",
    "Botswana",
    "Brazil",
    "Brunei Darussalam",
    "Burkina Faso",
    "Myanmar",
    "Burundi",
    "Cabo Verde",
    "Cambodia",
    "Cameroon",
    "Canada",
    "Central African Republic",
    "Chad",
    "Chile",
    "China",
    "Colombia",
    "Congo",
    "Democratic Republic of the Congo",
    "Costa Rica",
    "Cote d'Ivoire",
    "Cuba",
    "Djibouti",
    "Dominican Republic",
    "Ecuador",
    "Egypt",
    "El Salvador",
    "Eritrea",
    "Eswatini",
    "Ethiopia",
    "European Union (27) + UK",
    "UK",
    "Fiji",
    "Gabon",
    "Gambia",
    "Georgia",
    "Ghana",
    "Guatemala",
    "Guinea",
    "Guinea-Bissau",
    "Guyana",
    "Haiti",
    "Honduras",
    "India",
    "Indonesia",
    "Iran (Islamic Republic of)",
    "Iraq",
    "Israel",
    "Jamaica",
    "Japan",
    "Jordan",
    "Kazakhstan",
    "Kenya",
    "Democratic People's Republic of Korea",
    "Republic of Korea",
    "Kuwait",
    "Kyrgyzstan",
    "Lao People's Democratic Republic",
    "Lebanon",
    "Lesotho",
    "Liberia",
    "Libya",
    "Madagascar",
    "Malawi",
    "Malaysia",
    "Mali",
    "Mauritania",
    "Mauritius",
    "Mexico",
    "Republic of Moldova",
    "Mongolia",
    "Morocco",
    "Mozambique",
    "Namibia",
    "Nepal",
    "New Zealand",
    "Nicaragua",
    "Niger",
    "Nigeria",
    "North Macedonia",
    "Norway",
    "Oman",
    "Pakistan",
    "Panama",
    "Papua New Guinea",
    "Paraguay",
    "Peru",
    "Philippines",
    "Qatar",
    "Russian Federation",
    "Rwanda",
    "Saudi Arabia",
    "Senegal",
    "Serbia",
    "Sierra Leone",
    "Singapore",
    "Somalia",
    "South Africa",
    "South Sudan",
    "Sri Lanka",
    "Sudan",
    "Suriname",
    "Switzerland",
    "Syrian Arab Republic",
    "Taiwan",
    "Tajikistan",
    "United Republic of Tanzania",
    "Thailand",
    "Togo",
    "Trinidad and Tobago",
    "Tunisia",
    "Turkiye",
    "Turkmenistan",
    "Uganda",
    "Ukraine",
    "United Arab Emirates",
    "United States of America",
    "Uruguay",
    "Uzbekistan",
    "Venezuela (Bolivarian Republic of)",
    "Viet Nam",
    "Yemen",
    "Zambia",
    "Zimbabwe",
]

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

countries_unique = list(df_merge["Area Code (ISO3)"].unique())

# create dictionary containing each table, remove Area column
df_dict = {
    k: df_merge[df_merge["Area Code (ISO3)"] == k].drop(columns="Area Code (ISO3)")
    for k in countries_unique
}

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

    head_count_csv = np.vstack(
        [
            head_count_csv,
            [
                country,
                country_name,
                small_animal_sum,
                medium_animal_sum,
                large_animal_sum,
                dairy_cow_count,
            ],
        ]
    )

PRINT_ALL_THE_GLOBAL_ANIMALS = False
if PRINT_ALL_THE_GLOBAL_ANIMALS:
    print("small_animal_sum_global")
    print(small_animal_sum_global / 1e9)
    print("medium_animal_sum_global")
    print(medium_animal_sum_global / 1e9)
    print("large_animal_sum_global")
    print(large_animal_sum_global / 1e9)
    print("dairy_cow_count_global")
    print(dairy_cow_count_global / 1e9)


# add up GBR and F5707 (EU+27) to incorporate GBR (which is the UK),
# and delete GBR

F5707_index = np.where(head_count_csv[:, 0] == "F5707")
GBR_index = np.where(head_count_csv[:, 0] == "GBR")
F5707_name = head_count_csv[F5707_index][0][1]
F5707_small = float(head_count_csv[F5707_index][0][2])
F5707_medium = float(head_count_csv[F5707_index][0][3])
F5707_large = float(head_count_csv[F5707_index][0][4])
F5707_dairy = float(head_count_csv[F5707_index][0][5])

GBR_name = head_count_csv[GBR_index][0][1]
GBR_small = float(head_count_csv[GBR_index][0][2])
GBR_medium = float(head_count_csv[GBR_index][0][3])
GBR_large = float(head_count_csv[GBR_index][0][4])
GBR_dairy = float(head_count_csv[GBR_index][0][5])


head_count_csv[F5707_index, 0] = "F5707+GBR"
head_count_csv[F5707_index, 2] = str(F5707_small + GBR_small)
head_count_csv[F5707_index, 3] = str(F5707_medium + GBR_medium)
head_count_csv[F5707_index, 4] = str(F5707_large + GBR_large)
head_count_csv[F5707_index, 5] = str(F5707_dairy + GBR_dairy)

swaziland_index = np.where(head_count_csv[:, 0] == "SWZ")

# eswatini recently changed from swaziland
head_count_csv[swaziland_index, 0] = "SWT"
head_count_csv = np.delete(head_count_csv, (GBR_index), axis=0)


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
