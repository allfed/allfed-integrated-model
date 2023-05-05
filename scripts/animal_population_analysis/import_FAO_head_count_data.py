import pathlib
import pandas as pd
import numpy as np
import pycountry


def get_max_from_species(df, species):
    """
    returns the max value from a dataframe for a given species

    df: dataframe
    species: list of species codes

    returns: max value for species, returns 0 if no value

    """
    species_slaughter_head = df[df["Item Code (CPC)"].isin(species)]
    if not np.isnan(species_slaughter_head["Value"].max()):
        return species_slaughter_head["Value"].max()
    return 0

def add_alpha_codes_from_ISO(df, incol,outcol):
    """
    adds a column of alpha3 codes to a dataframe with country name in column 'col'
    uses M49 numeric codes to match countries
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
    return df

##########################
### Start Main Script ####
##########################

# Import CSV to dataframes
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath(".").resolve()
df_import = pd.read_csv(
    DATA_PATH.joinpath("FAOSTAT_data_en_4-14-2023_head_counts.csv") # change this to the file you want to import
)

# Add alpha3 codes to dataframe
iso_num_col = "Area Code (M49)"
new_col_name = "Area Code (ISO3)"
df = add_alpha_codes_from_ISO(df_import, iso_num_col,new_col_name)
#find area code iso3 with no match and drop them, for this dataset it's just "China", which is instead split in to China Mainlaind, Hong kong etc.
df = df.drop(df[df["Area Code (ISO3)"] == "NA"].index)

# Get list of countries
countries = list(df[new_col_name].unique())
country_names = list(df["Area"].unique())

# create dictionary containing each table, remove Area column
df_dict = {
    k: df[df[new_col_name] == k].drop(columns=new_col_name)
    for k in countries
}

# FAO Element codes for small/medium/large animal slaughter numbers
Chickens_1000_head	 = 	[2151.0]
Ducks_1000_head	 = 	[2154.0]
Geese_1000_head	 = 	[2153.0]
Turkeys_1000_head	 = 	[2152.0]
Rabbits_and_hares_1000_head	 = 	[2191.0]
Other_rodents_1000_head	 = 	[2192.01]
Asses	 = 	[2132.0]
Camels	 = 	[2121.01]
Cattle	 = 	[2111.0]
Goats	 = 	[2123.0]
Horses	 = 	[2131.0]
Mules_and_hinnies	 = 	[2133.0]
Sheep	 = 	[2122.0]
Buffalo	 = 	[2112.0]
Swine_or_pigs	 = 	[2140.0]
Other_camelids	 = 	[2121.02]
Bees	 = 	[2196.0]

# create empty list to store data
d = []

for i in range(0, len(countries)):
    country = countries[i]
    country_name = country_names[i]
    if country not in df_dict.keys():
        print("missing" + country)
        continue

    # get population head for country
    pop_head_for_country = df_dict[country]


    # this is where we define the species we want to include in each category
    #small animals, chicken, rabbit, rodents (only in Peru and Bolivia), duck, goose, turkey
    chicken_head = get_max_from_species(pop_head_for_country, Chickens_1000_head) * 1000
    rabbit_head = get_max_from_species(pop_head_for_country, Rabbits_and_hares_1000_head) * 1000
    duck_head = get_max_from_species(pop_head_for_country, Ducks_1000_head) * 1000
    goose_head = get_max_from_species(pop_head_for_country, Geese_1000_head) * 1000
    turkey_head = get_max_from_species(pop_head_for_country, Turkeys_1000_head) * 1000
    other_rodents_head = get_max_from_species(pop_head_for_country, Other_rodents_1000_head) * 1000
    small_animal_head = chicken_head + rabbit_head + duck_head + goose_head + turkey_head + other_rodents_head

    #medium animals, pig, goat, sheep, camelids
    pig_head = get_max_from_species(pop_head_for_country, Swine_or_pigs)
    goat_head = get_max_from_species(pop_head_for_country, Goats)
    sheep_head = get_max_from_species(pop_head_for_country, Sheep)
    camelids_head = get_max_from_species(pop_head_for_country, Other_camelids)
    medium_animal_head = pig_head + goat_head + sheep_head + camelids_head

    #large animals, cattle, camel, buffalo, horses/donkleys
    cattle_head = get_max_from_species(pop_head_for_country, Cattle)
    camel_head = get_max_from_species(pop_head_for_country, Camels)
    buffalo_head = get_max_from_species(pop_head_for_country, Buffalo)
    mule_head = get_max_from_species(pop_head_for_country, Mules_and_hinnies)
    horse_head = get_max_from_species(pop_head_for_country, Horses)
    asses_head = get_max_from_species(pop_head_for_country, Asses) 
    #######  horses/donkeys/asses/mules excluded as they are not used for meat ######
    large_animal_head = cattle_head + camel_head + buffalo_head #+ mule_head + horse_head + asses_head

    # add to list
    d.append(
                {
                    "iso3": country,
                    "country": country_name,
                    "small_animal_head": small_animal_head,
                    "medium_animal_head": medium_animal_head,
                    "large_animal_head": large_animal_head,
                    "chicken_head": chicken_head,
                    "rabbit_head": rabbit_head,
                    "duck_head": duck_head,
                    "goose_head": goose_head,
                    "turkey_head": turkey_head,
                    "other_rodents_head": other_rodents_head,
                    "pig_head": pig_head,
                    "goat_head": goat_head,
                    "sheep_head": sheep_head,
                    "camelids_head": camelids_head,
                    "cattle_head": cattle_head,
                    "camel_head": camel_head,
                    "buffalo_head": buffalo_head,
                    "mule_head": mule_head,
                    "horse_head": horse_head,
                    "asses_head": asses_head,
                }
            )
df_out = pd.DataFrame(d)
df_out.to_csv("FAO_stat_head_counts_processed.csv")