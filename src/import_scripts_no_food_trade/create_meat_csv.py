from pathlib import Path
import pandas as pd
import numpy as np
import git

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

df_meat = pd.read_csv(MEAT_CSV)[["Area Code (ISO3)", "Item", "Unit", "Value"]]

countries_unique = list(df_meat["Area Code (ISO3)"].unique())
# create dictionary containing each table, remove Area column
df_dict = {
    k: df_meat[df_meat["Area Code (ISO3)"] == k].drop(columns="Area Code (ISO3)")
    for k in countries_unique
}

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

    meat_csv = np.vstack([meat_csv, [country, country_name, chicken, pork, beef]])

PRINT_MEAT_DATA = False
if PRINT_MEAT_DATA:
    print("chicken")
    print(chicken_sum_global / 1e9)
    print("pork")
    print(pork_sum_global / 1e9)
    print("beef")
    print(beef_sum_global / 1e9)

# add up GBR and F5707 (EU+27) to incorporate GBR (which is the UK),
# and delete GBR

F5707_index = np.where(meat_csv[:, 0] == "F5707")
GBR_index = np.where(meat_csv[:, 0] == "GBR")
F5707_name = meat_csv[F5707_index][0][1]
F5707_chicken = float(meat_csv[F5707_index][0][2])
F5707_pork = float(meat_csv[F5707_index][0][3])
F5707_beef = float(meat_csv[F5707_index][0][4])

GBR_name = meat_csv[GBR_index][0][1]
GBR_chicken = float(meat_csv[GBR_index][0][2])
GBR_pork = float(meat_csv[GBR_index][0][3])
GBR_beef = float(meat_csv[GBR_index][0][4])


meat_csv[F5707_index, 0] = "F5707+GBR"
meat_csv[F5707_index, 2] = str(F5707_chicken + GBR_chicken)
meat_csv[F5707_index, 3] = str(F5707_pork + GBR_pork)
meat_csv[F5707_index, 4] = str(F5707_beef + GBR_beef)


swaziland_index = np.where(meat_csv[:, 0] == "SWZ")
# eswatini recently changed from swaziland
meat_csv[swaziland_index, 0] = "SWT"
meat_csv = np.delete(meat_csv, (GBR_index), axis=0)


np.savetxt(
    Path(repo_root) / "data" / "no_food_trade" / "processed_data" / "meat_csv.csv",
    meat_csv,
    delimiter=",",
    fmt="%s",
)
