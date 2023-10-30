import pandas as pd
import numpy as np
import pycountry
from pathlib import Path
import git


"""
This script imports the FAO animal data and converts it into a simple csv format
Should be mostly evergreen, but needs to be updated if FAO changes their data format
Created Early 2023 - Kevin
"""


def add_alpha_codes_from_ISO(df, incol, outcol):
    """
    adds a column of alpha3 codes to a dataframe with country name in column 'col'
    uses the ISO numeric code in column 'col' to match the alpha3 code
    """
    input_countries = df[incol]
    # strip any whitesapce AND non-digits from the input country codes
    input_countries = [str(country).strip().strip("'") for country in input_countries]
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


def import_FAO_general_data(path_to_csv, item_codes, element_codes, alpha3_col="iso3"):

    # try latin-1 encoding first (For FAO data)
    try:
        df = pd.read_csv(path_to_csv, encoding="latin-1")
    except:
        # try ISO-8859-1
        df = pd.read_csv(path_to_csv)

    # get the name of the last column
    check_for_flag_col = df.columns[-1]
    # if the name contains an "F", remove it from the dataframe
    if "F" in check_for_flag_col:
        df = df.drop(columns=check_for_flag_col)
    # get the name of the last column
    value_col = df.columns[-1]

    # keepn only the columns we need, Area Code (M49)	,Item Code,	Item,	Element Code,	Element	Unit, value_col
    df = df[
        [
            "Area Code (M49)",
            "Item Code",
            "Item",
            "Element Code",
            "Element",
            "Unit",
            value_col,
        ]
    ]

    # for each item code, grab the first row that matches and extract the "Item" and "element" strings and combine them to a new column name
    new_col_names = []
    for i in range(0, len(item_codes)):
        item_code = item_codes[i]
        element_code = element_codes[i]
        try:

            new_col_names.append(
                df.loc[
                    (df["Item Code"] == item_code)
                    & (df["Element Code"] == element_code),
                    "Item",
                ].values[0]
                + "_"
                + df.loc[
                    (df["Item Code"] == item_code)
                    & (df["Element Code"] == element_code),
                    "Element",
                ].values[0]
            )
        except:
            # print error message shwoing which codes didn't work
            print("unable to find " + str(item_code) + " " + str(element_code))

    # create new dataframe with each of the unique country codes
    df_out = pd.DataFrame(df["Area Code (M49)"].unique(), columns=["Area Code (M49)"])

    # Iterate over each new column
    for i in range(len(new_col_names)):
        new_col_name = new_col_names[i]
        item_code = item_codes[i]
        element_code = element_codes[i]

        # Merge the original DataFrame with df_out on "Area Code (M49)"
        merged_df = pd.merge(
            df_out,
            df.loc[
                (df["Item Code"] == item_code) & (df["Element Code"] == element_code),
                ["Area Code (M49)", value_col],
            ],
            on="Area Code (M49)",
            how="left",
        )

        # Rename the value column to the desired new column name
        merged_df.rename(columns={value_col: new_col_name}, inplace=True)

        # Update df_out with the merged DataFrame
        df_out = merged_df

    # finally, add the alpha3 codes
    df_out = add_alpha_codes_from_ISO(df_out, "Area Code (M49)", alpha3_col)

    # remove any countries that don't have an alpha3 code (labelled as "NA")
    df_out = df_out[df_out[alpha3_col] != "NA"]

    # set the index to the alpha3 codes
    df_out.set_index(alpha3_col, inplace=True)

    # Output the resulting DataFrame
    return df_out


if __name__ == "__main__":

    ## import data
    repo_root = git.Repo(".", search_parent_directories=True).working_dir

    animal_pop_analysis_dir = Path(repo_root) / "scripts" / "animal_population_analysis"

    csv_location = Path.joinpath(
        Path(animal_pop_analysis_dir),
        "Environment_Emissions_intensities_E_All_Data.csv",
    )

    # select the rows we need, you must select a combo of Item Code and Element Code
    item_codes = [1058, 1058]
    element_codes = [71761, 723113]

    df = import_FAO_general_data(csv_location, item_codes, element_codes)
