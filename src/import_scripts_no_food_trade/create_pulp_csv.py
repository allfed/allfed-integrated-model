import pandas as pd
import numpy as np
import os


PULP_CSV = "../../data/no_food_trade/raw_data/FAOSTAT_wood_pulp_2020.csv"

pulp_countries = [
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

df_pulp_countries = pd.read_csv(PULP_CSV)[
    ["Area Code (ISO3)", "Area", "Element", "Unit", "Value"]
]

# for each country create a list of macronutrient values
pulp_csv = np.array(["iso3", "country", "wood_pulp_tonnes"])

for i in range(0, len(pulp_countries)):
    pulp_country = pulp_countries[i]
    country_name = country_names[i]
    if pulp_country not in list(df_pulp_countries["Area Code (ISO3)"]):
        print("missing " + country_name)
        pulp = 0
    else:
        pulp = float(
            df_pulp_countries[df_pulp_countries["Area Code (ISO3)"] == pulp_country][
                "Value"
            ]
        )
    pulp_csv = np.vstack([pulp_csv, [pulp_country, country_name, pulp]])


# add up GBR and F5707 (EU+27) to incorporate GBR (which is the UK),
# and delete GBR

F5707_index = np.where(pulp_csv[:, 0] == "F5707")
GBR_index = np.where(pulp_csv[:, 0] == "GBR")
F5707_name = pulp_csv[F5707_index][0][1]
F5707_tons = float(pulp_csv[F5707_index][0][2])

GBR_name = pulp_csv[GBR_index][0][1]
GBR_tons = float(pulp_csv[GBR_index][0][2])


pulp_csv[F5707_index, 0] = "F5707+GBR"
pulp_csv[F5707_index, 2] = str(F5707_tons + GBR_tons)


swaziland_index = np.where(pulp_csv[:, 0] == "SWZ")
# eswatini recently changed from swaziland
pulp_csv[swaziland_index, 0] = "SWT"
pulp_csv = np.delete(pulp_csv, (GBR_index), axis=0)
pulp_csv = pd.DataFrame(pulp_csv, columns=["iso3", "country", "wood_pulp_tonnes"])
pulp_csv = pulp_csv.iloc[
    1:,
]

pulp_csv["wood_pulp_tonnes"] = pulp_csv["wood_pulp_tonnes"].astype(float)

pulp_csv["percent_of_global_production"] = pulp_csv["wood_pulp_tonnes"] / (
    pulp_csv["wood_pulp_tonnes"].sum()
)
print("pulp_csv")
print(pulp_csv.head())

pulp_csv.to_csv(
    "../../data/no_food_trade/processed_data/pulp_csv.csv", sep=",", index=False
)
