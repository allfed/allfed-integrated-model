from src.food_system.animal_populations import AnimalSpecies
from src.food_system.animal_populations import read_animal_population_data
from src.food_system.animal_populations import read_animal_nutrition_data
from src.food_system.animal_populations import read_animal_options
from src.food_system.animal_populations import create_animal_objects
from src.food_system.food import Food

import plotly.express as px
import pandas as pd
import git
from pathlib import Path
import pycountry



def add_alpha_codes_from_ISO(df, incol,outcol="iso3"):
    """
    adds a column of alpha3 codes to a dataframe with country name in column 'col'
    uses fuzzy logic to match countries
    """
    input_countries = df[incol]
    countries = []
    for input_country in input_countries:
        try:
            country = pycountry.countries.get(numeric=str(input_country).zfill(3))
            alpha3 = country.alpha_3
        except:
            alpha3 = "NA"
            print("unable to match " + str(input_country))
        countries.append(alpha3)
    df[outcol] = countries
    # remove original country column
    df = df.drop([incol], axis=1)
    return df


def add_alpha_codes_fuzzy(df, incol,outcol="iso3"):
    """
    adds a column of alpha3 codes to a dataframe with country name in column 'col'
    uses fuzzy logic to match countries
    """
    input_countries = df[incol]
    countries = []
    for input_country in input_countries:
        try:
            country = pycountry.countries.search_fuzzy(input_country)
            alpha3 = country[0].alpha_3
        except:
            alpha3 = "unk_" + input_country
        countries.append(alpha3)
    df["alpha3"] = countries
    # remove original country column
    df = df.drop([incol], axis=1)
    return df

def read_csv_values(path, country_code_col="Code",  year_col="Year", value_col=None,output_syntax="iso3"):
    """
    reads csv files downloaded from our world in data, isolates the ISO alpga 3 country code, and keeps only the most recent data per country
    """
    df = pd.read_csv(path)
    df.rename(columns={country_code_col: output_syntax}, inplace=True)
    df = df.set_index(output_syntax)
    try:
        df = df.sort_values(by=year_col)  # sort ascending
        df = df[
            ~df.index.duplicated(keep="last")
        ]  # delete duplicate entries from countries, keep the most recent data
    except:
        print("no year column")
    try:
        df = df.drop(["Entity", year_col], axis=1)
    except:
        print("no entity or year column to drop")
        
    if value_col is not None:
        # only keep the value column and the iso3 column
        df = df[[value_col]]
    return df

## import data
repo_root = git.Repo(".", search_parent_directories=True).working_dir

animal_pop_analysis_dir = Path(repo_root) / "scripts" / "animal_population_analysis"
processed_data_dir = Path(repo_root) / "data" / "no_food_trade" / "processed_data"

country_feed_data_location = Path.joinpath(
    Path(animal_pop_analysis_dir), "country_feed_data.csv"
)
pop_csv_location = Path.joinpath(
    Path(processed_data_dir), "population_csv.csv"
)
ag_area_csv_location = Path.joinpath(
    Path(animal_pop_analysis_dir), "total-agricultural-area-over-the-long-term.csv"
)
grazing_area_csv_location = Path.joinpath(
    Path(animal_pop_analysis_dir), "UNdata_Export_20230612_101954125.csv"
)       
grazing_area_owid_csv_location = Path.joinpath(
    Path(animal_pop_analysis_dir), "grazing-land-use-over-the-long-term.csv"
)       


df_feed_country = pd.read_csv(country_feed_data_location, index_col="ISO3 Country Code")
df_pop_country = pd.read_csv(pop_csv_location, index_col="iso3", )
df_grazing = read_csv_values(grazing_area_csv_location, country_code_col="Country or Area", value_col="Value", output_syntax="CountryName")


df_grazing = df_grazing.reset_index()
add_alpha_codes_fuzzy(df_grazing,"CountryName",outcol="iso3")

df_grazing.to_csv(Path.joinpath(Path(animal_pop_analysis_dir), "grazing_area.csv"), index=False)

## Populate animal objects ##
# create animal objects
df_animal_stock_info = read_animal_population_data()
df_animal_attributes = read_animal_nutrition_data()
df_animal_options = read_animal_options()




# create empty list to store the total food consumed per country
total_food_consumed = []



for country_code in df_animal_stock_info.index:
    animal_list = create_animal_objects(df_animal_stock_info.loc[country_code], df_animal_attributes)
    
    # create empty list to store the food consumed by each animal
    calculated_feed_demand = Food(0,0,0)
    animal_pop = 0
    
    # calculate consumed food in the animla list for this country
    for animal in animal_list:
        animal_object = animal_list[animal]
        calculated_feed_demand += animal_object.feed_required_per_month_species()
        animal_pop += animal_object.current_population
        
        
    
    total_food_consumed.append(
                    {
                        "iso3": country_code,
                        "calculated_feed_demand": calculated_feed_demand.kcals,
                        "animal_pop": animal_pop,
                    }
                )

# create dataframe from the list
df_feed = pd.DataFrame(total_food_consumed)

# merge with the df_feed_country dataframe
df_feed = df_feed.merge(
    df_feed_country, left_on="iso3", right_on="ISO3 Country Code"
)

# conversion from million dry caloric tons to billion kcal
# 1 gram of dry food = 4.184 kJ
# so 1 million tonnes of dry food = 4.184e9 kJ or 4184 billion kJ
conversion_factor = 4184

df_feed["Animal feed consumption Billion kcals"] = (
    df_feed["Animal feed caloric consumption in 2020 (million dry caloric tons)"] * conversion_factor
)

#drop rows with zero values for feed consumption
df_feed = df_feed[df_feed["Animal feed consumption Billion kcals"] != 0]

# merge with the animal stock info dataframe
df_merged = df_feed.merge(
    df_animal_stock_info, left_on="iso3", right_on="iso3"
)

# merge with grazing df
df_merged = df_merged.merge(
    df_grazing, left_on="iso3", right_on="iso3"
)



df_feed["difference"] = df_feed["calculated_feed_demand"] - df_feed["Animal feed consumption Billion kcals"]
df_feed["ratio"] = df_feed["calculated_feed_demand"] / df_feed["Animal feed consumption Billion kcals"]


# plot the dat using plotly
fig = px.scatter(
    df_feed,
    x="Animal feed consumption Billion kcals",
    y="calculated_feed_demand",
    hover_name="Country",
    log_x=True,
    log_y=True,
)

fig.show()

# and plot the ratio, sorted by the ratio, color by the population
fig2 = px.bar(
    df_feed.sort_values("ratio"),
    x="Country",
    y="ratio",
    hover_name="Country",
    log_y=True,
)

fig2.show()


#plot the feed consumption and the population
fig3 = px.scatter(
    df_feed,
    x="Animal feed consumption Billion kcals",
    y="animal_pop",
    hover_name="Country",
    log_x=True,
    log_y=True,
)

fig3.show()

# print the ratio stats
print(df_feed["ratio"].describe())


# mike is familiar with the datasets
# also the lily paper, grass growing... maybe in supplements?



# (feed + grass + residues) * growth_factor <- gdp = total demand (currenlty calculated on "maintenance" requirements, i.e no growth)
# growth could be twice as much
# conversion efficiency is really terrible for beef...


# 


# livestock units are defined differently based on region, so apply this first before introducing other factors.

# residues will be proportional to crop area... so we can use the crop area data to estimate residues


# glean database only broken down by OECD and non OEXD. But it has the consumption of grazed material as well as residues.


# 1 ha = 0.8 tonne of residues produced by hectare. https://www.sciencedirect.com/science/article/abs/pii/S2211912416300013#preview-section-introduction
# some are used for toher things
# sugar (burnt for the factory)
# 



# 
