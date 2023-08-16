from src.food_system.calculate_animals_and_feed_over_time import CalculateAnimalOutputs
import plotly.express as px
import pandas as pd
import git
from pathlib import Path

## import data
repo_root = git.Repo(".", search_parent_directories=True).working_dir
animal_feed_data_dir = Path(repo_root) / "data" / "no_food_trade" / "animal_feed_data"
country_feed_data_location = Path.joinpath(
    Path(animal_feed_data_dir), "country_feed_data.csv"
)
FAO_stat_slaughter_counts_processed_location = Path.joinpath(
    Path(animal_feed_data_dir), "FAO_stat_slaughter_counts_processed.csv"
)
head_count_csv_location = Path.joinpath(
    Path(animal_feed_data_dir), "head_count_csv.csv"
)

gdp_csv_location = Path.joinpath(
    Path(animal_feed_data_dir), "gdp_owid_2018.csv"
)

# Load data
processed_data_dir = Path(repo_root) / "data" / "no_food_trade" / "processed_data"
pop_csv_location = Path.joinpath(
    Path(processed_data_dir), "population_csv.csv"
)



df_feed_country = pd.read_csv(country_feed_data_location, index_col="ISO3 Country Code")
df_fao_animals = pd.read_csv(head_count_csv_location, index_col="iso3")
df_gdp = pd.read_csv(gdp_csv_location, index_col="iso3")
df_fao_slaughter = pd.read_csv(
    FAO_stat_slaughter_counts_processed_location, index_col="iso3"
)
df_pop_country = pd.read_csv(pop_csv_location, index_col="iso3")


# join on inner to only calauclate for countries that all three of the datatsets exist
df_fao_slaughter = df_fao_slaughter.join(df_fao_animals, how="inner", rsuffix="_animals")
df_fao_slaughter = df_fao_slaughter.join(df_feed_country, how="inner", rsuffix="_feed")




# keep only the first 20 countries
# df_fao_slaughter = df_fao_slaughter.iloc[:20]


# initiliase class
cao = CalculateAnimalOutputs()

# create dictionary to emulate scenarios in integrated
constants_inputs = {}

# create lists to store output populations
country_list = []
max_month_list = []
initial_beef = []
initial_beef_slaughter = []
initial_pig = []
initial_pig_slaughter = []
initial_poultry = []
initial_poultry_slaughter = []

# error countries
error_countries = []



#reate for loop to iterate through all countries
for country in df_fao_slaughter.index:

    # small_animal_slaughter,medium_animal_slaughter,large_animal_slaughter,
    constants_inputs["COUNTRY_CODE"] = country
    constants_inputs["NMONTHS"] = 120
    reduction_in_dairy_calves = 0
    use_grass_and_residues_for_dairy = False
    feed_ratio = 1

    data = {
        "country_code": constants_inputs["COUNTRY_CODE"],
        "reduction_in_beef_calves": 90,
        "reduction_in_dairy_calves": reduction_in_dairy_calves,
        "increase_in_slaughter": 110,
        "reduction_in_pig_breeding": 90,
        "reduction_in_poultry_breeding": 90,
        "months": constants_inputs["NMONTHS"],
        "discount_rate": 30,
        "mother_slaughter": 0,
        "use_grass_and_residues_for_dairy": use_grass_and_residues_for_dairy,
        "keep_dairy": True,
        "feed_ratio": feed_ratio,
    }

    feed_dairy_meat_results, feed = cao.calculate_feed_and_animals(data)


    try:
    #find month when poultry pop is less than 10 
        poultry_pop_less_than_10 = feed_dairy_meat_results[feed_dairy_meat_results["Poultry Pop"] < 10]
        zero_poultry_month = poultry_pop_less_than_10.index[0]

        #find month when pig pop is less than 10
        pig_pop_less_than_10 = feed_dairy_meat_results[feed_dairy_meat_results["Pigs Pop"] < 10]
        zero_pig_month = pig_pop_less_than_10.index[0]


        #find month when beef pop is less than 10
        beef_pop_less_than_10 = feed_dairy_meat_results[feed_dairy_meat_results["Beef Pop"] < 10]
        zero_beef_month = beef_pop_less_than_10.index[0]

        # find max month
        max_month = max(zero_poultry_month, zero_pig_month, zero_beef_month)
        

        # # append results to lists
        country_list.append(country)
        max_month_list.append(max_month)
        initial_beef.append(feed_dairy_meat_results["Beef Pop"][0])
        initial_pig.append(feed_dairy_meat_results["Pigs Pop"][0])
        initial_poultry.append(feed_dairy_meat_results["Poultry Pop"][0])
        initial_beef_slaughter.append(df_fao_slaughter.loc[country, "large_animal_slaughter"])
        initial_pig_slaughter.append(df_fao_slaughter.loc[country, "medium_animal_slaughter"])
        initial_poultry_slaughter.append(df_fao_slaughter.loc[country, "small_animal_slaughter"])
    except:
        error_countries.append(country)
        pass



# create dataframe from lists
df = pd.DataFrame(
    {
        "country": country_list,
        "max_month": max_month_list,
        "initial_beef": initial_beef,
        "initial_pig": initial_pig,
        "initial_poultry": initial_poultry,
        "initial_beef_slaughter": initial_beef_slaughter,
        "initial_pig_slaughter": initial_pig_slaughter,
        "initial_poultry_slaughter": initial_poultry_slaughter,
        
    }
)
# merge gdp dataframe
df = df.merge(df_gdp, left_on="country", right_on="iso3", how="left")

# merge population dataframe
df = df.merge(df_pop_country, left_on="country_x", right_on="iso3", how="left")


# create population to slaughter ratio
df["beef_ratio"] = df["initial_beef_slaughter"] / df["initial_beef"]
df["pig_ratio"] = df["initial_pig_slaughter"] / df["initial_pig"]
df["poultry_ratio"] = df["initial_poultry_slaughter"] / df["initial_poultry"]

# create gdp per capita
df["GDP_per_capita"] = df["GDP"] / df["population"]


#plot max month er country, sorted by max month
fig = px.bar(
    df.sort_values("max_month"),
    x="max_month",
    y="country",
    title="Time to zero population",
    orientation="h",
)
fig.show()


#plot beef population against beef salughter, with country labels
fig = px.scatter(
    df,
    x="initial_beef",
    y="initial_beef_slaughter",
    color="country",
    title="Beef population vs slaughter",
)
fig.show()


# plot beef ratio against time to zero population (max_month)
fig = px.scatter(
    df,     
    x="max_month",
    y="GDP_per_capita",
    color="country_x",
    title="Beef ratio vs time to zero population",
    # use the beef pop as the size of the marker, with a min size of 10 and max size of 100
    size="initial_beef",
    size_max=40,
    


)
fig.show()


