import pandas as pd
import pathlib
import re
import pycountry


def add_alpha_codes(df, col):
    """
    adds a column of alpha3 codes to a dataframe with country name in column 'col'
    uses fuzzy logic to match countries
    """
    input_countries = df[col]
    countries = []
    for input_country in input_countries:
        try:
            country = pycountry.countries.search_fuzzy(input_country)
            alpha3 = country[0].alpha_3
        except:
            alpha3 = "unk_" + input_country
        countries.append(alpha3)
    df["alpha3"] = countries
    return df


# Import CSV to dataframes
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath(".").resolve()


# df = parse_country_region_mappings(DATA_PATH.joinpath("FAO Country List Regions.txt"))
# print(df)

# Read the text file
with open(DATA_PATH.joinpath("FAO Country List Regions.txt"), "r") as file:
    text = file.read()


# Split the text into lines
lines = text.split("\n")

# for each line, split by before the first colon, and define as the region
regions = []
countries_list = []
for line in lines:
    countries = []
    if len(line) > 0:
        region = line.split(":")[0]
        regions.append(region)

        # now another loop to split by the comma, and define as the country
        for country in line.split(":")[1].split(","):
            countries.append(country.strip())
    # save the countries as a list
    countries_list.append(countries)

# drop any empty coutnries
countries_list = [x for x in countries_list if x != []]

# now create a dataframe with the regions and countries
# format long, so that the regions are repeated for each country in the final dataframe
regions_list = []
for region in regions:
    regions_list.extend([region] * len(countries_list[regions.index(region)]))

countries_list = [item for sublist in countries_list for item in sublist]

df = pd.DataFrame({"region": regions_list, "country": countries_list})

output_df = add_alpha_codes(df, "country")

# export to csv
output_df.to_csv(DATA_PATH.joinpath("FAO_country_region_mappings.csv"), index=False)
