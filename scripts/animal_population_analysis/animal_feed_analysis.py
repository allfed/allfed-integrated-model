from src.food_system.animal_populations import AnimalSpecies
from src.food_system.animal_populations import AnimalDataReader
from src.food_system.animal_populations import AnimalModelBuilder
from src.food_system.animal_populations import CountryData
from src.food_system.food import Food
from scripts.animal_population_analysis.import_FAO_general_data import (
    import_FAO_general_data,
)
from scipy import stats
import statsmodels.stats.power as smp
import plotly.express as px
import pandas as pd
import git
import numpy as np
from pathlib import Path
import pycountry


def add_alpha_codes_from_ISO(
    df,
    incol,
    outcol="iso3",
    unmatched_value="NA",
    keep_original=False,
    unmatched_alert=False,
):
    """
    adds a column of alpha3 codes to a dataframe with country name in column 'col'
    uses fuzzy logic to match countries
    """
    input_countries = df[incol]
    input_countries = input_countries.fillna(0)
    countries = []
    for input_country in input_countries:
        try:
            country = pycountry.countries.get(numeric=str(int(input_country)).zfill(3))
            alpha3 = country.alpha_3
        except:
            alpha3 = unmatched_value
            if unmatched_alert:
                print("unable to match " + str(input_country))
        countries.append(alpha3)
    df[outcol] = countries
    # remove original country column
    if not keep_original:
        df = df.drop([incol], axis=1)
    return df


def add_alpha_codes_fuzzy(
    df,
    incol,
    outcol="iso3",
    unmatched_value="NA",
    keep_original=False,
    unmatched_alert=True,
):
    """
    adds a column of alpha3 codes to a dataframe with country name in column 'col'
    uses fuzzy logic to match countries
    """
    # handle empty dataframe
    if df.empty:
        return df

    # return error if incol or outcol not strings
    if not isinstance(incol, str):
        raise TypeError("incol must be a string")
    if not isinstance(outcol, str):
        raise TypeError("outcol must be a string")

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


def read_csv_values(
    path, country_code_col="Code", year_col="Year", value_col=None, output_syntax="iso3"
):
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

    AnimalDataReader.read_animal_regional_factors()
    AnimalDataReader.read_country_data()


def species_baseline_feed(
    total_net_energy_demand, feed_DI, roughages_DI, roughages_percentage=0.8
):

    """
    Eq1:
    DI_r * DM_r * GE/Kg_r + DI_f * DM_f * GE/Kg_f = NE_req
    [%] * [kg] * [MJ/kg] + [%] * [kg] * [MJ/kg] = [MJ]
    Digestibility, dry matter, gross energy per kg of feed, net energy required per animal

    Combine the GE and DM to gt dry matter energy equivalent

    DI_r * GE_r + DI_f * GE_f = NE_req

    From GLEAM, we know that the baseline breakdown is approx
    https://docs.google.com/spreadsheets/d/1XUWmHfq8yeYRePtHMfQ_AV7V0AzVVcCGzEhEJor-48o/edit?usp=sharing

    80% roughages
    20% feed
    for ruminants
    AND
    100% feed
    for monogastrics

    So for ruminants, we can assume that 80% of the GROSS energy comes from roughages, and 20% from feed, as the GE/KG is approximately the same for both

    ==== Equations ====
    GE_r = 80/20 * GE_f                 And we can substitute this into the equation above to get:

    NE_req = GE_r * (DI_r + 0.25 * DI_f)
    ==== End Equations ====

    ### ASSUMES THAT KJ/KG of FEED and ROUGHAGE is approximately the same.
    If you want to remove this assumption, you'll need to add terms (see eq1 above)
    """
    DI_r = roughages_DI
    DI_f = feed_DI
    feed_percentage = 1 - roughages_percentage
    NE_req = total_net_energy_demand
    GE_r = NE_req / (DI_r + feed_percentage / roughages_percentage * DI_f)
    GE_f = feed_percentage / roughages_percentage * GE_r

    return GE_r, GE_f


def bulk_correlation_analysis(df, target_column):
    # Check if the DataFrame is empty
    if df.empty:
        return

    # Drop the target column and index from the DataFrame
    columns_to_check = df.columns.drop(target_column)

    # Iterate over the remaining columns and calculate correlations
    for column in columns_to_check:
        correlation = df[target_column].corr(df[column])
        print(f"Correlation between {target_column} and {column}: {correlation}")

        # Create a scatter plot to visualize the correlation using Plotly
        fig = px.scatter(df, x=target_column, y=column)
        fig.show()


## import data
repo_root = git.Repo(".", search_parent_directories=True).working_dir

animal_pop_analysis_dir = Path(repo_root) / "scripts" / "animal_population_analysis"
processed_data_dir = Path(repo_root) / "data" / "no_food_trade" / "processed_data"


country_gdp_data_location = Path.joinpath(
    Path(animal_pop_analysis_dir), "gdp_owid_2018.csv"
)
country_feed_data_location = Path.joinpath(
    Path(animal_pop_analysis_dir), "country_feed_data.csv"
)
pop_csv_location = Path.joinpath(Path(processed_data_dir), "population_csv.csv")
ag_area_csv_location = Path.joinpath(
    Path(animal_pop_analysis_dir), "total-agricultural-area-over-the-long-term.csv"
)
total_energy_csv_location = Path.joinpath(
    Path(animal_pop_analysis_dir), "FAO_total_energy_use_in_ag.csv"
)


df_energy = pd.read_csv(total_energy_csv_location)
df_energy = add_alpha_codes_from_ISO(df_energy, incol="Area Code (M49)", outcol="iso3")
# df_energy = df_energy.dropna(subset=["iso3"])

df_energy = df_energy[df_energy["iso3"] != "NA"]
df_energy = df_energy.set_index("iso3")
df_energy = df_energy.drop(
    ["Area", "Element Code", "Element", "Unit", "Area Code", "Item Code", "Item"],
    axis=1,
)
df_energy = df_energy.rename(columns={"Y2021": "total_energy_use_in_ag"})


df_feed_country = pd.read_csv(country_feed_data_location, index_col="ISO3 Country Code")
df_pop_country = pd.read_csv(
    pop_csv_location,
    index_col="iso3",
)
df_gdp = read_csv_values(
    country_gdp_data_location,
    country_code_col="Iso3",
    value_col="GDP",
    output_syntax="iso3",
)


# merge the four dataframes above
df_country_macro_indicators = pd.merge(
    df_pop_country, df_feed_country, left_index=True, right_index=True
)
df_country_macro_indicators = pd.merge(
    df_country_macro_indicators, df_gdp, left_index=True, right_index=True
)


### Create secondary attributes ####
# GDP per capita
df_country_macro_indicators["GDP per capita"] = (
    df_country_macro_indicators["GDP"] / df_country_macro_indicators["population"]
)
# create gdp rank
df_country_macro_indicators["GDP per capita rank"] = df_country_macro_indicators[
    "GDP per capita"
].rank(ascending=False)
df_country_macro_indicators["GDP rank"] = df_country_macro_indicators["GDP"].rank(
    ascending=False
)


## Populate animal objects ##
# create animal objects
df_animal_stock_info = AnimalDataReader.read_animal_population_data()
df_animal_attributes = AnimalDataReader.read_animal_nutrition_data()
df_animal_options = AnimalDataReader.read_animal_options()

df_regional_conversion_factors = AnimalDataReader.read_animal_regional_factors()
df_country_info = AnimalDataReader.read_country_data()

# create date frame with the column names as the species (from df_animal_stock_info)
# but remove the columns that have "salughter" in the name
# and remove "_head" from all columns that have it in the name
col_list = df_animal_stock_info.columns
col_list = [col for col in col_list if "_head" in col]
col_list = [col.replace("_head", "") for col in col_list]
# copy the list so it has two of each, and add "_grass" and "_feed" to the end of each
col_list_grass = [col + "_grass" for col in col_list]
col_list_feed = [col + "_feed" for col in col_list]
# comebine the two lists
col_list = col_list_grass + col_list_feed

df_feed = pd.DataFrame(columns=col_list, index=df_animal_stock_info.index)

# create empty list to store the total food consumed per country
total_food_consumed = []

for country_code in df_animal_stock_info.index:
    animal_list = AnimalModelBuilder.create_animal_objects(
        df_animal_stock_info.loc[country_code], df_animal_attributes
    )
    country_object = CountryData(country_code)
    country_object.set_livestock_unit_factors(
        df_country_info, df_regional_conversion_factors
    )

    # create empty list to store the food consumed by each animal
    calculated_feed_demand = Food(0, 0, 0)
    calculated_grass_demand = Food(0, 0, 0)
    calculated_feed_by_species = {}
    calculated_grass_by_species = {}
    animal_pop = 0

    # constants from gleam.
    ruminant_DI_grass = 0.56
    ruminant_DI_feed = 0.8
    ruminant_grass_fraction = 0.8
    monogastric_DI_feed = 0.7

    # calculate consumed food in the animla list for this country
    for animal in animal_list:
        animal_object = animal_list[animal]
        net_energy_demand = animal_object.net_energy_required_per_species()

        if animal_object.digestion_type == "ruminant":
            # input the roughage and feed digestion indeces and the percentage intake  of roughage
            GE_roughage, GE_feed = species_baseline_feed(
                net_energy_demand,
                ruminant_DI_feed,
                ruminant_DI_grass,
                ruminant_grass_fraction,
            )
        else:
            GE_roughage = 0
            GE_feed = net_energy_demand * monogastric_DI_feed

        df_feed.loc[country_code, animal_object.animal_type + "_grass"] = GE_roughage
        df_feed.loc[country_code, animal_object.animal_type + "_feed"] = GE_feed

        ### NEXT TODO: deal with this grass and feed usage. Combine fed to compare to world average.
        # ALSO GO BACK AND DO THE REGIONAL VARIATION IN LSU
        # Thern MEssga emorgan and mike. Morgan re: merge. Mike re: data check.

# merge with the df_feed_country dataframe, keep the index of df_feed:
df_feed = df_feed.merge(df_country_macro_indicators, left_index=True, right_index=True)

conversion_factor = 4000 / 12
df_feed["Animal feed consumption Billion kcals"] = (
    df_feed["Animal feed caloric consumption in 2020 (million dry caloric tons)"]
    * conversion_factor
)

# drop rows with zero values for feed consumption
df_feed = df_feed[df_feed["Animal feed consumption Billion kcals"] != 0]

# calculate the total feed demand for each country, the sum of all columns with "_feed" in the name
df_feed["feed_calculated_demand"] = df_feed.filter(regex="_feed").sum(axis=1)
df_feed["grass_calculated_demand"] = df_feed.filter(regex="_grass").sum(axis=1)
df_feed["difference"] = (
    df_feed["feed_calculated_demand"] - df_feed["Animal feed consumption Billion kcals"]
)
df_feed["fudge_factor"] = (
    df_feed["Animal feed consumption Billion kcals"] / df_feed["feed_calculated_demand"]
)
df_feed["fudge_difference"] = (
    df_feed["feed_calculated_demand"] * df_feed["fudge_factor"]
    - df_feed["Animal feed consumption Billion kcals"]
)

# merge with the animal stock info dataframe
df_merged = df_feed.merge(df_animal_stock_info, left_index=True, right_index=True)

# plot the countries using the calculated_feed_by_species as a bar chart segmented by species

print(df_feed["fudge_factor"].describe())


###### find sum ######

# sum df_merged for all countires
df_merged_sum = df_merged.sum(axis=0)
df_merged_sum = pd.DataFrame(df_merged_sum).T

df_merged_sum["fudge_factor"] = (
    df_merged_sum["Animal feed consumption Billion kcals"]
    / df_merged_sum["feed_calculated_demand"]
)

# print results using f print
print(
    f'Global Average Fudge Factor: {df_merged_sum["fudge_factor"].loc[0]:.2f}\nFAO Monthly Feed: {df_merged_sum["Animal feed consumption Billion kcals"].loc[0]:.2f}\nCalculated Feed: {df_merged_sum["feed_calculated_demand"].loc[0]:.2f}'
)


# sort by gdp
df_merged = df_merged.sort_values(by="GDP per capita", ascending=True)


###### Start Correlation Section ######

### NEXT DO CORR OF LOG OF FUDGE FACTOR

cols_of_interest = [
    "fudge_factor",
    "GDP rank",
    "GDP per capita rank",
    "chicken_feed",
    "rabbit_feed",
    "duck_feed",
    "goose_feed",
    "turkey_feed",
    "other_rodents_feed",
    "pig_feed",
    "meat_goat_feed",
    "meat_sheep_feed",
    "camelids_feed",
    "meat_cattle_feed",
    "meat_camel_feed",
    "meat_buffalo_feed",
    "mule_feed",
    "horse_feed",
    "asses_feed",
    "milk_sheep_feed",
    "milk_cattle_feed",
    "milk_goat_feed",
    "milk_camel_feed",
    "milk_buffalo_feed",
    "population",
    "Animal feed caloric consumption in 2020 (million dry caloric tons)",
    "Animal feed fat consumption in 2020 (million tonnes)",
    "Animal feed protein consumption in 2020 (million tonnes)",
    "GDP",
    "feed_calculated_demand",
    "grass_calculated_demand",
    "chicken_head",
    "rabbit_head",
    "duck_head",
    "goose_head",
    "turkey_head",
    "other_rodents_head",
    "pig_head",
    "meat_goat_head",
    "meat_sheep_head",
    "camelids_head",
    "meat_cattle_head",
    "meat_camel_head",
    "meat_buffalo_head",
    "mule_head",
    "horse_head",
    "asses_head",
    "milk_sheep_head",
    "milk_cattle_head",
    "milk_goat_head",
    "milk_camel_head",
    "milk_buffalo_head",
    "GDP per capita",
]


dataframe_corr = df_merged[cols_of_interest].copy()

#  log of the fudge factor
dataframe_corr["log_fudge_factor"] = np.log(dataframe_corr["fudge_factor"])
target_column = "log_fudge_factor"

df = dataframe_corr


# Drop the target column and index from the DataFrame
columns_to_check = df.columns.drop(target_column)

df = df.apply(pd.to_numeric, errors="coerce")

# create an empty dictionary to store the correlations and statistical power
correlations = {}

# Iterate over the remaining columns and calculate correlations
for column in columns_to_check:
    correlation = df[target_column].corr(df[column])
    # find number of non-null values
    non_null_non_zero = (df[column] > 0).sum()
    # and percentage of non-null values
    non_null_percentage = non_null_non_zero / len(df)

    # calculate statistical power if there are missing data points
    if non_null_percentage < 1.0:
        nobs1 = non_null_non_zero
        alpha = 0.05  # significance level
        effect_size = correlation * np.sqrt(
            (1 - correlation**2) / (1 - non_null_percentage)
        )
        power = smp.tt_ind_solve_power(effect_size, nobs1=nobs1, alpha=alpha)
    else:
        power = 1.0  # set power to 1 when there are no missing data points

    # add the correlation and percent non-null to dictionary
    correlations[column] = [correlation, non_null_percentage, power]


# create a dataframe from the dictionary of correlations
df_correlation = pd.DataFrame.from_dict(
    correlations,
    orient="index",
    columns=["correlation", "non_null_percentage", "power"],
)

# sort by abs(correlation)
df_correlation = df_correlation.reindex(
    df_correlation["correlation"].abs().sort_values(ascending=False).index
)

# only show correlations with a power of 0.8 or higher
df_correlation = df_correlation[df_correlation["power"] >= 0.8]

df_correlation


#### Present day
# break out each animal
# how many cows
# how much feed is going in


figure_toggle = False

if figure_toggle:

    fig = px.scatter(
        df_merged,
        x="Country",
        y="fudge_factor",
        # log_y=True,
    )

    fig.show()

    country_selection = "USA"
    # plot mongoloia feed usage by species
    fig2 = px.bar(
        df_feed.loc[country_selection].filter(regex="_feed"),
        x=df_feed.loc[country_selection].filter(regex="_feed").index,
        y=df_feed.loc[country_selection].filter(regex="_feed").values,
    )

    fig2.show()


# # # mike is familiar with the datasets
# # # also the lily paper, grass growing... maybe in supplements?


# # # (feed + grass + residues) * growth_factor <- gdp = total demand (currenlty calculated on "maintenance" requirements, i.e no growth)
# # # growth could be twice as much
# # # conversion efficiency is really terrible for beef...


# # #


# # # livestock units are defined differently based on region, so apply this first before introducing other factors.

# # # residues will be proportional to crop area... so we can use the crop area data to estimate residues


# # # glean database only broken down by OECD and non OEXD. But it has the consumption of grazed material as well as residues.


# # # 1 ha = 0.8 tonne of residues produced by hectare. https://www.sciencedirect.com/science/article/abs/pii/S2211912416300013#preview-section-introduction
# # # some are used for toher things
# # # sugar (burnt for the factory)
# # #


# # #
