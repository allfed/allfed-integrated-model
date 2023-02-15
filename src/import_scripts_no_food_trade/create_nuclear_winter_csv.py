"""
This file contains the code for creating the nuclear winter crop production csv
originally imported from data from the Rutgers team (xia et al).

@author: morgan
"""

import pandas as pd
import numpy as np
from src.utilities.import_utilities import ImportUtilities
from src.import_scripts_no_food_trade.create_crop_macros_csv import CropMacros
import git
from pathlib import Path

repo_root = git.Repo(".", search_parent_directories=True).working_dir

print("importing nuclear winter crop and grass data...")

# COUNTRY SPECIFIC DATA


def get_crop_ratios_this_country(country_id, crop_macros):
    """
    get the kcal ratios production for wheat, rice, soy, spring wheat each country
    We assume some similar crops will count towards these ratios, in order to get
    a better approximation of how the reduction will affect the country.

    """
    products = crop_macros.products[country_id]
    kcals_check, fat, protein = crop_macros.get_nutrients(products)

    corn_like = ["maize", "millet"]
    kcals_corn_sum = crop_macros.get_kcals_matching(corn_like, products)

    # [kcals_sum, fat_sum, protein_sum] = crop_macros.get_nutrients(products)

    wheat_like = ["wheat", "rye", "barley", "oats", "triticale"]
    kcals_wheat_sum = crop_macros.get_kcals_matching(wheat_like, products)

    rice_like = ["rice"]
    kcals_rice_sum = crop_macros.get_kcals_matching(rice_like, products)

    soy_like = ["soybean", "beans", "pulses", "peas"]
    kcals_soy_sum = crop_macros.get_kcals_matching(soy_like, products)

    all_relevant_sum = kcals_corn_sum + kcals_wheat_sum + kcals_rice_sum + kcals_soy_sum

    assert kcals_check >= all_relevant_sum >= 0, "Error: Nonsense sum for production"
    MIN_ACCEPTABLE_REPRESENTATIVE_RATIO = 0.33
    if all_relevant_sum == 0 or (
        all_relevant_sum / kcals_check <= MIN_ACCEPTABLE_REPRESENTATIVE_RATIO
    ):
        # use the global number
        crops = {
            "corn": 0.332020251571745,
            "rice": 0.300642569104085,
            "soy": 0.09385529821812,
            "spring_wheat": 0.27348188110605,
        }
    else:
        crops = {
            "corn": kcals_corn_sum / all_relevant_sum,
            "rice": kcals_rice_sum / all_relevant_sum,
            "soy": kcals_soy_sum / all_relevant_sum,
            "spring_wheat": kcals_wheat_sum / all_relevant_sum,
        }

    return crops


def get_overall_reduction(country_data, country_id, crop_macros):
    """
    determine the total reduction in production using the relative reduction
    in corn, rice, soy, and spring wheat

    also separately assigns the grass reduction appropriately
    """

    years = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # 10 years of data exist
    yearly_reductions = {}  # average yearly reduction for crop production

    crop_ratios = get_crop_ratios_this_country(country_id, crop_macros)
    for year in years:
        reductions = []
        for crop in crop_ratios:
            col_name = crop + "_year" + str(year)

            reduction = country_data[col_name]

            # the overall ratio is the sum of the reduction of each crop,
            # times the ratio of calories that this crop represents
            # (crop relocation in nuclear winter is not considered here)
            reductions.append(float(reduction))
        weightings = list(crop_ratios.values())
        year_avg = ImportUtilities.weighted_average_percentages(reductions, weightings)
        yearly_reductions["crop_reduction_year" + str(year)] = year_avg

        col_name = "grasses_year" + str(year)
        yearly_reductions["grasses_reduction_year" + str(year)] = country_data[col_name]
    return yearly_reductions


def calculate_reductions(country_data, country_id, crop_macros):
    """
    calculate the crop reduction percentage for each year and aggregate as array
    """
    yearly_reductions = get_overall_reduction(country_data, country_id, crop_macros)
    reductions = [
        float(yearly_reductions["crop_reduction_year1"]),
        float(yearly_reductions["crop_reduction_year2"]),
        float(yearly_reductions["crop_reduction_year3"]),
        float(yearly_reductions["crop_reduction_year4"]),
        float(yearly_reductions["crop_reduction_year5"]),
        float(yearly_reductions["crop_reduction_year6"]),
        float(yearly_reductions["crop_reduction_year7"]),
        float(yearly_reductions["crop_reduction_year8"]),
        float(yearly_reductions["crop_reduction_year9"]),
        float(yearly_reductions["crop_reduction_year10"]),
        float(yearly_reductions["grasses_reduction_year1"]),
        float(yearly_reductions["grasses_reduction_year2"]),
        float(yearly_reductions["grasses_reduction_year3"]),
        float(yearly_reductions["grasses_reduction_year4"]),
        float(yearly_reductions["grasses_reduction_year5"]),
        float(yearly_reductions["grasses_reduction_year6"]),
        float(yearly_reductions["grasses_reduction_year7"]),
        float(yearly_reductions["grasses_reduction_year8"]),
        float(yearly_reductions["grasses_reduction_year9"]),
        float(yearly_reductions["grasses_reduction_year10"]),
    ]

    return reductions


def clean_up_nw_csv(nw_csv, nw_csv_cols):
    nw_csv = pd.DataFrame(
        nw_csv,
        columns=nw_csv_cols,
    )

    for i in range(1, 11):
        nw_csv["crop_reduction_year" + str(i)] = nw_csv[
            "crop_reduction_year" + str(i)
        ].astype(float)
        nw_csv["crop_reduction_year" + str(i)] = nw_csv[
            "crop_reduction_year" + str(i)
        ].div(100)
        nw_csv["crop_reduction_year" + str(i)] = np.where(
            nw_csv["crop_reduction_year" + str(i)] > 9.36e34,
            -1,
            nw_csv["crop_reduction_year" + str(i)],
        )

        nw_csv["grasses_reduction_year" + str(i)] = nw_csv[
            "grasses_reduction_year" + str(i)
        ].astype(float)
        nw_csv["grasses_reduction_year" + str(i)] = nw_csv[
            "grasses_reduction_year" + str(i)
        ].div(100)
        nw_csv["grasses_reduction_year" + str(i)] = np.where(
            nw_csv["grasses_reduction_year" + str(i)] > 9.36e34,
            -1,
            nw_csv["grasses_reduction_year" + str(i)],
        )

    return nw_csv


def get_all_crops_correct_countries(input_table):
    """
    get the columns with all the reductions for every crop, with the
    countries properly aggregated (eu27+uk combined) and Taiwan reductions
    equal to China's (Rutgers dataset doesn't include Taiwan as a distinct entity)
    """
    crop_macros = CropMacros()

    all_except_taiwan = []
    taiwan_reductions = []
    country_ids = []
    country_codes = ImportUtilities.country_codes
    country_names = ImportUtilities.country_names
    for i in range(0, len(country_codes)):
        country = country_codes[i]
        country_name = country_names[i]

        # skip missing country
        if country not in input_table.keys():
            if country != "TWN":
                print("ERROR: missing" + country)
                quit()
            continue

        country_data = input_table[country]

        # skip if there's no data for this country
        # (corn_year1 is just one example)
        if len(country_data["corn_year1"]) == 0:
            continue

        reductions = calculate_reductions(country_data, country, crop_macros)

        if country == "CHN":
            # Taiwan reductions set equal to China's
            taiwan_reductions = ImportUtilities.stack_on_list(
                taiwan_reductions, reductions
            )

        all_except_taiwan = ImportUtilities.stack_on_list(all_except_taiwan, reductions)

        country_ids = ImportUtilities.stack_on_list(
            country_ids, (country, country_name)
        )

    all_reductions_processed = ImportUtilities.stack_on_list(
        all_except_taiwan, taiwan_reductions
    )

    country_ids = ImportUtilities.stack_on_list(country_ids, ("TWN", "Taiwan"))

    return country_ids, all_reductions_processed


def main():
    """
    saves a csv with all the countries' crop reductions in nuclear winter
    averaged
    """
    NW_CSV = (
        Path(repo_root)
        / "data"
        / "no_food_trade"
        / "raw_data"
        / "rutgers_nw_production_raw.csv"
    )

    iso3_col_name = "ISO3 Country Code"

    col_names = [
        iso3_col_name,
        "corn_year1",
        "corn_year2",
        "corn_year3",
        "corn_year4",
        "corn_year5",
        "corn_year6",
        "corn_year7",
        "corn_year8",
        "corn_year9",
        "corn_year10",
        "rice_year1",
        "rice_year2",
        "rice_year3",
        "rice_year4",
        "rice_year5",
        "rice_year6",
        "rice_year7",
        "rice_year8",
        "rice_year9",
        "rice_year10",
        "soy_year1",
        "soy_year2",
        "soy_year3",
        "soy_year4",
        "soy_year5",
        "soy_year6",
        "soy_year7",
        "soy_year8",
        "soy_year9",
        "soy_year10",
        "spring_wheat_year1",
        "spring_wheat_year2",
        "spring_wheat_year3",
        "spring_wheat_year4",
        "spring_wheat_year5",
        "spring_wheat_year6",
        "spring_wheat_year7",
        "spring_wheat_year8",
        "spring_wheat_year9",
        "spring_wheat_year10",
        "grasses_year1",
        "grasses_year2",
        "grasses_year3",
        "grasses_year4",
        "grasses_year5",
        "grasses_year6",
        "grasses_year7",
        "grasses_year8",
        "grasses_year9",
        "grasses_year10",
    ]

    nw_csv_cols = [
        "iso3",
        "country",
        "crop_reduction_year1",
        "crop_reduction_year2",
        "crop_reduction_year3",
        "crop_reduction_year4",
        "crop_reduction_year5",
        "crop_reduction_year6",
        "crop_reduction_year7",
        "crop_reduction_year8",
        "crop_reduction_year9",
        "crop_reduction_year10",
        "grasses_reduction_year1",
        "grasses_reduction_year2",
        "grasses_reduction_year3",
        "grasses_reduction_year4",
        "grasses_reduction_year5",
        "grasses_reduction_year6",
        "grasses_reduction_year7",
        "grasses_reduction_year8",
        "grasses_reduction_year9",
        "grasses_reduction_year10",
    ]

    input_table = ImportUtilities.import_csv(NW_CSV, col_names, iso3_col_name)

    country_ids, all_reductions_processed = get_all_crops_correct_countries(input_table)

    nw_csv = pd.DataFrame(
        columns=nw_csv_cols,
    )

    # this is the list of headers in the output csv

    for i in range(0, len(country_ids)):
        country_id = country_ids[i]
        country_reductions = all_reductions_processed[i]

        nw_csv = ImportUtilities.add_row_to_csv(
            nw_csv, country_id[0], country_id[1], country_reductions
        )

    nw_csv = ImportUtilities.clean_up_eswatini(nw_csv)

    cleaned_nw_csv = clean_up_nw_csv(nw_csv, nw_csv_cols)

    cleaned_nw_csv.to_csv(
        Path(repo_root)
        / "data"
        / "no_food_trade"
        / "processed_data"
        / "nuclear_winter_csv.csv",
        sep=",",
        index=False,
    )


if __name__ == "__main__":
    main()
