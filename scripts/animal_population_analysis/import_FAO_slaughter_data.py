import pathlib
import pandas as pd
import numpy as np
import pycountry




## function to get slaughterdataframe
def get_slaughter_dataframe(df):

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
        small_animal_slaughter = chicken_slaughter + rabbit_slaughter + ducks_slaughter + geese_slaughter + turkeys_slaughter + other_rodents_slaughter

        #medium animals, pig, goat, sheep, camelids
        pig_slaughter = get_max_from_species(slaughter_head_for_country, pig)
        goat_slaughter = get_max_from_species(slaughter_head_for_country, goat)
        sheep_slaughter = get_max_from_species(slaughter_head_for_country, sheep)
        camelids_slaughter = get_max_from_species(slaughter_head_for_country, camelids)
        medium_animal_slaughter = pig_slaughter + goat_slaughter + sheep_slaughter + camelids_slaughter

        #large animals, cattle, camel, buffalo
        cattle_slaughter = get_max_from_species(slaughter_head_for_country, cattle)
        camel_slaughter = get_max_from_species(slaughter_head_for_country, camel)
        buffalo_slaughter = get_max_from_species(slaughter_head_for_country, buffalo)
        mule_slaughter = get_max_from_species(slaughter_head_for_country, mules_and_hinnies)
        asses_slughter = get_max_from_species(slaughter_head_for_country, asses)
        horse_slaughter = get_max_from_species(slaughter_head_for_country, horses)

        #  horses/donkeys/asses/mules excluded as they are not used for meat ######
        large_animal_slaughter = cattle_slaughter + camel_slaughter + buffalo_slaughter #+ mule_slaughter + asses_slughter + horse_slaughter

        # add to list
        d.append(

                    {
                        "iso3": country,
                        "country": country_name,
                        "small_animal_slaughter": small_animal_slaughter,
                        "medium_animal_slaughter": medium_animal_slaughter,
                        "large_animal_slaughter": large_animal_slaughter,
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

# Add alpha3 codes to dataframe
iso_num_col = "Area Code (M49)"
new_col_name = "Area Code (ISO3)"



df_slaughter = add_alpha_codes_from_ISO(df_import_slaughter, iso_num_col,new_col_name)
#find area code iso3 with no match and drop them, for this dataset it's just "China", which is instead split in to China Mainlaind, Hong kong etc.
df = df_slaughter.drop(df_slaughter[df_slaughter["Area Code (ISO3)"] == "NA"].index)

# filter dataframe by elemenmt which conatins milking
df_milking = df_slaughter[df_slaughter["Element"].str.contains("Milk")]
df_milking.to_csv("FAO_stat_milk_production.csv")





df_out_slaughter = get_slaughter_dataframe(df_slaughter)




df_out.to_csv("FAO_stat_slaughter_counts_processed.csv")