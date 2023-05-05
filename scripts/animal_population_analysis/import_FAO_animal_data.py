import pathlib
import pandas as pd
import numpy as np
import pycountry




## function to get slaughterdataframe
def get_slaughter_dataframe(df):
    """
    puts the slaughter count of animals into a dataframe
    Hardcoded to use FAO element codes

    :df: dataframe containing meat production of animals in FAO format
    :return: dataframe containing slaughtercount of animals in simple csv format
    """

    # Get list of countries
    countries = list(df[new_col_name].unique())
    country_names = list(df["Area"].unique())

    # create dictionary containing each table, remove Area column
    df_dict = {
        k: df[df[new_col_name] == k].drop(columns=new_col_name)
        for k in countries
    }

    # FAO Element codes for small/medium/large animal slaughter numbers
    ########### START CODES #####################
    chicken_1000_head = [21121]
    ducks_1000_head	 = 	[21122]
    geese_1000_head	 = 	[21123]
    turkeys_1000_head	 = 	[21124]
    rabbit_1000_head = [21114.0]
    other_rodents_1000_head	 = 	[21119.01]
    sheep =  [ 21115.0, 21155.0 , 21514.0]
    pig = [21113.01 , 21170.01, 21511.01]
    goat = [ 21116, 21116.0, 21156.0, 21515.0]
    camelids =[ 21117.02] # alpacaes, llamas etc.
    cattle =[ 2951.01 , 21111.01 , 21151.0 , 21512.0 ]
    camel = [21117.01 ,21159.02 ,21519.02]
    buffalo = [2951.03, 21112.0, 21152.0, 21513.0]
    asses	 = 	[21118.02]
    horses	 = 	[21159.01, 21118.01]
    mules_and_hinnies	 = 	[21118.03]
    ########### FINISH CODES #####################

    # create empty list to store data
    d = []

    for i in range(0, len(countries)):
        country = countries[i]
        country_name = country_names[i]
        if country not in df_dict.keys():
            print("missing" + country)
            continue

        slaughter_head_for_country = df_dict[country]

        #small animals, chicken, rabbit
        chicken_slaughter = get_max_from_species(slaughter_head_for_country, chicken_1000_head) * 1000
        ducks_slaughter = get_max_from_species(slaughter_head_for_country, ducks_1000_head) * 1000
        geese_slaughter = get_max_from_species(slaughter_head_for_country, geese_1000_head) * 1000
        rabbit_slaughter = get_max_from_species(slaughter_head_for_country, rabbit_1000_head) * 1000
        turkeys_slaughter = get_max_from_species(slaughter_head_for_country, turkeys_1000_head) * 1000
        other_rodents_slaughter = get_max_from_species(slaughter_head_for_country, other_rodents_1000_head) * 1000

        #medium animals, pig, goat, sheep, camelids
        pig_slaughter = get_max_from_species(slaughter_head_for_country, pig)
        goat_slaughter = get_max_from_species(slaughter_head_for_country, goat)
        sheep_slaughter = get_max_from_species(slaughter_head_for_country, sheep)
        camelids_slaughter = get_max_from_species(slaughter_head_for_country, camelids)

        #large animals, cattle, camel, buffalo
        cattle_slaughter = get_max_from_species(slaughter_head_for_country, cattle)
        camel_slaughter = get_max_from_species(slaughter_head_for_country, camel)
        buffalo_slaughter = get_max_from_species(slaughter_head_for_country, buffalo)
        mule_slaughter = get_max_from_species(slaughter_head_for_country, mules_and_hinnies)
        asses_slughter = get_max_from_species(slaughter_head_for_country, asses)
        horse_slaughter = get_max_from_species(slaughter_head_for_country, horses)

        # add to list
        d.append(

                    {
                        "iso3": country,
                        "country": country_name,
                        "chicken_slaughter": chicken_slaughter,
                        "rabbit_slaughter": rabbit_slaughter,
                        "duck_slaughter": ducks_slaughter,
                        "goose_slaughter": geese_slaughter,
                        "turkey_slaughter": turkeys_slaughter,
                        "other_rodents_slaughter": other_rodents_slaughter,
                        "pig_slaughter": pig_slaughter,
                        "goat_slaughter": goat_slaughter,
                        "sheep_slaughter": sheep_slaughter,
                        "camelids_slaughter": camelids_slaughter,
                        "cattle_slaughter": cattle_slaughter,
                        "camel_slaughter": camel_slaughter,
                        "buffalo_slaughter": buffalo_slaughter,
                        "mule_slaughter": mule_slaughter,
                        "horse_slaughter": horse_slaughter,
                        "asses_slaughter": asses_slughter,
                    }
                )
        
    df_out = pd.DataFrame(d)
    return df_out

def get_headcount_dataframe(df):
    """
    puts the headcount of animals into a dataframe
    Hardcoded to use FAO element codes

    :df: dataframe containing headcount of animals in FAO format
    :return: dataframe containing headcount of animals in simple csv format
    """


    # Get list of countries
    countries = list(df[new_col_name].unique())
    country_names = list(df["Area"].unique())

    # create dictionary containing each table, remove Area column
    df_dict = {
        k: df[df[new_col_name] == k].drop(columns=new_col_name)
        for k in countries
    }

    # FAO Element codes for small/medium/large animal slaughter numbers
    # https://www.fao.org/faostat/en/#definitions
    ########### START CODES #####################
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
    ########### END CODES #####################

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

        #small animals, chicken, rabbit, rodents (only in Peru and Bolivia), duck, goose, turkey
        chicken_head = get_max_from_species(pop_head_for_country, Chickens_1000_head) * 1000
        rabbit_head = get_max_from_species(pop_head_for_country, Rabbits_and_hares_1000_head) * 1000
        duck_head = get_max_from_species(pop_head_for_country, Ducks_1000_head) * 1000
        goose_head = get_max_from_species(pop_head_for_country, Geese_1000_head) * 1000
        turkey_head = get_max_from_species(pop_head_for_country, Turkeys_1000_head) * 1000
        other_rodents_head = get_max_from_species(pop_head_for_country, Other_rodents_1000_head) * 1000

        #medium animals, pig, goat, sheep, camelids
        pig_head = get_max_from_species(pop_head_for_country, Swine_or_pigs)
        goat_head = get_max_from_species(pop_head_for_country, Goats)
        sheep_head = get_max_from_species(pop_head_for_country, Sheep)
        camelids_head = get_max_from_species(pop_head_for_country, Other_camelids)

        #large animals, cattle, camel, buffalo, horses/donkleys
        cattle_head = get_max_from_species(pop_head_for_country, Cattle)
        camel_head = get_max_from_species(pop_head_for_country, Camels)
        buffalo_head = get_max_from_species(pop_head_for_country, Buffalo)
        mule_head = get_max_from_species(pop_head_for_country, Mules_and_hinnies)
        horse_head = get_max_from_species(pop_head_for_country, Horses)
        asses_head = get_max_from_species(pop_head_for_country, Asses) 

        # add to list
        d.append(
                    {
                        "iso3": country,
                        "country": country_name,
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

    return df_out

def get_milk_headcount(df):
    """
    puts the headcount of milk producing animals into a dataframe
    Hardcoded to use FAO element codes for milk producing animals

    :df: dataframe containing headcount of animals in FAO format
    :return: dataframe containing headcount of milk producing animals in simple csv format
    """

    # Get list of countries
    countries = list(df[new_col_name].unique())
    country_names = list(df["Area"].unique())

    # create dictionary containing each table, remove Area column
    df_dict = {
        k: df[df[new_col_name] == k].drop(columns=new_col_name)
        for k in countries
    }

    # FAO Element codes for small/medium/large animal slaughter numbers
    # https://www.fao.org/faostat/en/#definitions
    ########### START CODES #####################
    sheep = [2291.0]
    cattle = [2211.0]
    goats = [2292.0]
    camel = [2293.0]
    buffalo = [2212.0]
    ########### END CODES #####################

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
        milk_sheep = get_max_from_species(pop_head_for_country, sheep)
        milk_cattle = get_max_from_species(pop_head_for_country, cattle)
        milk_goats = get_max_from_species(pop_head_for_country, goats)
        milk_camel = get_max_from_species(pop_head_for_country, camel)
        milk_buffalo = get_max_from_species(pop_head_for_country, buffalo)
 
        # add to list
        d.append(
                    {
                        "iso3": country,
                        "country": country_name,
                        "milk_sheep_head": milk_sheep,
                        "milk_cattle_head": milk_cattle,
                        "milk_goats_head": milk_goats,
                        "milk_camel_head": milk_camel,
                        "milk_buffalo_head": milk_buffalo,
                    }
                )
    df_out = pd.DataFrame(d)

    return df_out

def subtract_milk_from_head(df, meat_col, milk_col):
    """
    subtracts milk head from meat head AND renames meat head column
    
    df: dataframe
    meat_col: column name for meat head
    milk_col: column name for milk head

    returns: dataframe with milk head subtracted from meat head
    """
    df[meat_col] = df[meat_col] - df[milk_col]
    df = df.rename(columns={meat_col: "meat_" + meat_col})
    return df

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
    return df

# Import CSV to dataframes
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath(".").resolve()
df_import_slaughter = pd.read_csv(
    DATA_PATH.joinpath("FAO_stat_slaughter_counts.csv")
)
df_importhead = pd.read_csv(
    DATA_PATH.joinpath("FAOSTAT_data_en_4-14-2023_head_counts.csv") # change this to the file you want to import
)


#### HARDCODE DEFINTION OF ANIMAL SIZE ####

#animal size keywords
# milk and meat are include in these keywords, thjey are filtered out later to determine correct headcount
# removing animals from these keywords will remove them from the head and slaughter counts
# if you remove the milk animals, they will be considered as meat animals
# if you remove the meat animals, it will break the code
small_animal_keywords = ["chicken" , "rabbit", "duck", "goose", "turkey", "other_rodents"]
medium_animal_keywords = ["pig", "meat_goat", "meat_sheep", "camelids", "milk_goat", "milk_sheep"]
large_animal_keywords = ["meat_cattle", "meat_camel","meat_buffalo","milk_cattle", "milk_camel", "milk_buffalo"] #, "mule", "horse", "asses"]
# hardcode exclusion of horse like animals from meat (even though they are used for meat in some countries?)
# it is difficult to distinguish between horse like animals used for meat and those used for work, so the slaiughter 
# so the slaughter numbers are not a reliable indicator of meat production, and inclusion would skey the "large animal" category
small_animal_keywords_slaughter = ["chicken" , "rabbit", "duck", "goose", "turkey", "other_rodents"]
medium_animal_keywords_slaughter = ["pig", "goat", "sheep", "camelids"]
large_animal_keywords_slaughter = ["cattle", "camel","buffalo"] #, "mule", "horse", "asses"]


# Add alpha3 codes to dataframe
iso_num_col = "Area Code (M49)"
new_col_name = "Area Code (ISO3)"
df_slaughter = add_alpha_codes_from_ISO(df_import_slaughter, iso_num_col,new_col_name)
df_slaughter = df_slaughter.drop(df_slaughter[df_slaughter["Area Code (ISO3)"] == "NA"].index)

df_head = add_alpha_codes_from_ISO(df_importhead, iso_num_col,new_col_name)
df_head = df_head.drop(df_head[df_head["Area Code (ISO3)"] == "NA"].index)

#find area code iso3 with no match and drop them, for this dataset it's just "China", which is instead split in to China Mainlaind, Hong kong etc.

# filter dataframe by elemenmt which conatins milking
df_milking = df_slaughter[df_slaughter["Element"].str.contains("Milk")]

# simplify the dataframe to only include the columns we need (this is the heavy lifting)
df_out_slaughter = get_slaughter_dataframe(df_slaughter)
df_out_head = get_headcount_dataframe(df_head)
df_out_milking = get_milk_headcount(df_milking)

#merge dataframes milk and head, to get all headcounts in one dataframe, prvenet duplication of columns
# i.e merge but prevent _x, _y stuff from happeing
# drop the country column from the milk dataframe, as it is already in the head dataframe
df_out_head = df_out_head.merge(df_out_milking.drop(columns=["country"]), on="iso3", how="left")

# subtract milk species from headcounts
# this is because the milk headcounts are already included in the total headcounts
# rename the columns to meat_cattle_head etc.
df_out_head = subtract_milk_from_head(df_out_head, "sheep_head", "milk_sheep_head")
df_out_head = subtract_milk_from_head(df_out_head, "goat_head", "milk_goats_head")
df_out_head = subtract_milk_from_head(df_out_head, "camel_head", "milk_camel_head")
df_out_head = subtract_milk_from_head(df_out_head, "buffalo_head", "milk_buffalo_head")
df_out_head = subtract_milk_from_head(df_out_head, "cattle_head", "milk_cattle_head")


#### Create summary columns ####
# based on the keywords defined above, create summary columns for animal size and milk animals
df_out_head["large_animals"] = df_out_head.apply(
    lambda x: sum(x.filter(like=keyword).sum() for keyword in large_animal_keywords if 'milk' not in keyword), axis=1
)
df_out_head["medium_animals"] = df_out_head.apply(
    lambda x: sum(x.filter(like=keyword).sum() for keyword in medium_animal_keywords if 'milk' not in keyword), axis=1
)
df_out_head["small_animals"] = df_out_head.apply(
    lambda x: sum(x.filter(like=keyword).sum() for keyword in small_animal_keywords if 'milk' not in keyword), axis=1
)

# create summary columns for milk animals
df_out_head["large_milk_animals"] = df_out_head.apply(
    lambda x: sum(x.filter(like=keyword).sum() for keyword in large_animal_keywords if 'milk' in keyword), axis=1
)
df_out_head["medium_milk_animals"] = df_out_head.apply(
    lambda x: sum(x.filter(like=keyword).sum() for keyword in medium_animal_keywords if 'milk' in keyword), axis=1
)
df_out_head["small_milk_animals"] = df_out_head.apply(
    lambda x: sum(x.filter(like=keyword).sum() for keyword in small_animal_keywords if 'milk' in keyword), axis=1
)

# summary columns for slaughter
df_out_slaughter["large_animals_slaughter"] = df_out_slaughter.apply(
    lambda x: sum(x.filter(like=keyword).sum() for keyword in large_animal_keywords_slaughter), axis=1
)
df_out_slaughter["medium_animals_slaughter"] = df_out_slaughter.apply(
    lambda x: sum(x.filter(like=keyword).sum() for keyword in medium_animal_keywords_slaughter), axis=1
)
df_out_slaughter["small_animals_slaughter"] = df_out_slaughter.apply(
    lambda x: sum(x.filter(like=keyword).sum() for keyword in small_animal_keywords_slaughter), axis=1
)


# merge the head and slaughter dataframes
df_out = df_out_head.merge(df_out_slaughter.drop(columns=["country"]), on="iso3", how="left")

# export to csv
df_out.to_csv("FAOSTAT_head_and_slaughter.csv", index=False)