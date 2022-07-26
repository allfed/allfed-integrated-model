import pandas as pd
import numpy as np
import os


NUTRITION_XLS = "../../Supplemental_Data.xlsx"
PRODUCTION_CSV = "../../data/no_food_trade/FAOSTAT_food_production_2020.csv"

TONS_TO_KG = 1e3
KCALS_TO_DRY_CALORIC_TONS = 1 / (4000 * 1000)

KCALS_PER_PERSON = 2100
FAT_PER_PERSON = 47
PROTEIN_PER_PERSON = 53

prod_iso3 = [
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
    "C?te d'Ivoire",
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
# Data Inspection

xls = pd.ExcelFile(NUTRITION_XLS)
nutrition = pd.read_excel(xls, "Nutrition")[["Item", "Calories", "Protein", "Fat"]]

df_prod = pd.read_csv(PRODUCTION_CSV)[
    ["Area Code (ISO3)", "Area", "Element", "Item Code (FAO)", "Item", "Unit", "Value"]
]

countries = list(df_prod["Area Code (ISO3)"].unique())
# create dictionary containing each table, remove Area column
df_dict = {
    k: df_prod[df_prod["Area Code (ISO3)"] == k].drop(columns="Area Code (ISO3)")
    for k in countries
}

# for each country create a list of macronutrient values
macros_csv = np.array(
    [
        "ISO3 Country Code",
        "Country",
        "Outdoor crop caloric production in 2020 (dry caloric tons)",
        "Outdoor crop fat production in 2020 (tonnes)",
        "Outdoor crop protein production in 2020 (tonnes)",
    ]
)

for i in range(0, len(prod_iso3)):
    prod_country = prod_iso3[i]
    country_name = country_names[i]
    if prod_country not in df_dict.keys():
        print("missing" + prod_country)
        continue

    products = df_dict[prod_country]
    kcals_sum = 0
    fat_sum = 0
    protein_sum = 0

    # for each food product, add to each macronutrient total
    for index, product in products.iterrows():
        # find the particular icountry_names = [tem.
        n = nutrition[nutrition["Item"] == product["Item"]]

        # if the match could not be found, continue
        if len(n) == 0:
            continue

        # there should never be any duplicate nutrition items
        assert len(n) == 1

        kcals_per_kg = float(n["Calories"])  # kcals / kg
        fat_frac = float(n["Fat"])  # fraction by weight
        protein_frac = float(n["Protein"])  # fraction by weight

        # production Calories is units tons per year
        if np.isnan(product["Value"]):
            tons = 0
        else:
            tons = product["Value"]

        # dry caloric tons per year
        kcals = tons * TONS_TO_KG * kcals_per_kg * KCALS_TO_DRY_CALORIC_TONS

        # nutrition Fat and protein are percent by weight, converting to grams
        fat = tons * fat_frac  # tons per year
        protein = tons * protein_frac  # tons per year

        kcals_sum += kcals
        fat_sum += fat
        protein_sum += protein

    macros_csv = np.vstack(
        [
            macros_csv,
            [
                prod_country,
                country_name,
                str(kcals_sum),
                str(fat_sum),
                str(protein_sum),
            ],
        ]
    )

# add up GBR and F5707 (EU+27) to incorporate GBR (which is the UK),
# and delete GBR

F5707_index = np.where(macros_csv[:, 0] == "F5707")
GBR_index = np.where(macros_csv[:, 0] == "GBR")

F5707_name = macros_csv[F5707_index][0][1]
F5707_kcals = float(macros_csv[F5707_index][0][2])
F5707_fat = float(macros_csv[F5707_index][0][3])
F5707_protein = float(macros_csv[F5707_index][0][4])

GBR_name = macros_csv[GBR_index][0][1]
GBR_kcals = float(macros_csv[GBR_index][0][2])
GBR_fat = float(macros_csv[GBR_index][0][3])
GBR_protein = float(macros_csv[GBR_index][0][4])


macros_csv[F5707_index, 0] = "F5707+GBR"
macros_csv[F5707_index, 2] = str(F5707_kcals + GBR_kcals)
macros_csv[F5707_index, 3] = str(F5707_fat + GBR_fat)
macros_csv[F5707_index, 4] = str(F5707_protein + GBR_protein)


swaziland_index = np.where(macros_csv[:, 0] == "SWZ")
# eswatini recently changed from swaziland
macros_csv[swaziland_index, 0] = "SWT"
macros_csv = np.delete(macros_csv, (GBR_index), axis=0)


print("macros_csv")
print(macros_csv)

np.savetxt(
    "../../data/no_food_trade/macros_csv.csv", macros_csv, delimiter=",", fmt="%s"
)
