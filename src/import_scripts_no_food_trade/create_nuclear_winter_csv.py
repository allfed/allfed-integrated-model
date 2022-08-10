x  #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This file contains the code for creating the nuclear winter crop production csv 
originally imported from data from the Rutgers team (xia et al).

Created on Wed Jul 15
@author: morgan
"""

import pandas as pd
import numpy as np
import os

# COUNTRY SPECIFIC DATA

eu_27_p_uk_codes = [
    "AUT",
    "BEL",
    "BGR",
    "HRV",
    "CYP",
    "CZE",
    "DNK",
    "EST",
    "FIN",
    "FRA",
    "DEU",
    "GRC",
    "HUN",
    "IRL",
    "ITA",
    "LVA",
    "LTU",
    "LUX",
    "MLT",
    "NLD",
    "POL",
    "PRT",
    "ROU",
    "SVK",
    "SVN",
    "ESP",
    "SWE",
]

countries = eu_27_p_uk_codes + [
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

country_names = eu_27_p_uk_codes + [
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
    "C?te d'Ivoire",
    "Cuba",
    "Djibouti",
    "Dominican Republic",
    "Ecuador",
    "Egypt",
    "El Salvador",
    "Eritrea",
    "Eswatini",
    "Ethiopia",
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


def import_csv(csv_loc):
    """
    import the csv and load into a dictionary
    """
    iso3_col_name = "iso3"
    df_nw = pd.read_csv(csv_loc)[
        [
            iso3_col_name,
            "corn_year1",
            "corn_year2",
            "corn_year3",
            "corn_year4",
            "corn_year5",
            "rice_year1",
            "rice_year2",
            "rice_year3",
            "rice_year4",
            "rice_year5",
            "soy_year1",
            "soy_year2",
            "soy_year3",
            "soy_year4",
            "soy_year5",
            "spring_wheat_year1",
            "spring_wheat_year2",
            "spring_wheat_year3",
            "spring_wheat_year4",
            "spring_wheat_year5",
        ]
    ]

    # create dictionary containing each table, remove Area Code column
    input_table = {
        k: df_nw[df_nw[iso3_col_name] == k].drop(columns=iso3_col_name)
        for k in countries
    }

    return input_table


def clean_up_eswatini(nw_csv):
    """
    change the swaziland country code from the FAOSTAT default to the USDA
    standard for compatibility with other datasets
    """
    swaziland_index = np.where(nw_csv[:, 0] == "SWZ")
    # eswatini recently changed from swaziland
    nw_csv[swaziland_index, 0] = "SWT"

    return nw_csv


# UTILITIES


def stack_on_list(list, layer):
    """
    create another layer on an existing stack of layers, or create the first
    layer in the stack

    example: adding [d,e,f] to a stack

    [
        [a,b,c]
    ]

    gives you

    [
        [a,b,c],
        [d,e,f]
    ]

    gets: the original list and the layer
    returns: the combined original and layer with the list stacked down below it

    """
    if len(list) == 0:
        list = layer
    else:
        list = np.vstack([list, layer])

    return list


def add_row_to_csv(nw_csv, country, country_name, reductions):

    # convert to list of strings for saving as csv
    reduction_strings = [str(item) for item in reductions]

    to_save_row = np.append(country, np.append(country_name, reduction_strings))

    nw_csv = stack_on_list(nw_csv, to_save_row)

    return nw_csv


def average_columns(vstack):
    """
    average all the columns and return the result as a row

    gets: vertical stack of columns

    returns: a single row with the averages

    """
    row = []
    for i in range(0, len(vstack[0])):
        reduction = average_percentages(vstack[i, :])
        row.append(reduction)
    return row


def average_percentages(percentages):
    """
    set up even weightings for the weighted average
    """

    array_length = len(percentages)

    even_weightings = [1 / array_length] * array_length
    assert sum(even_weightings) == 1
    return weighted_average_percentages(percentages, even_weightings)


def weighted_average_percentages(percentages, weights):
    """
    create a weighted average of percentages

    creates an average for a list of percentage reductions.
    Any non-possible number is removed. The remaining are averaged.
    If only non-possible numbers are included, then the result is a non-possible number
    """
    assert len(percentages) == len(weights)
    assert sum(weights) <= 1.00001 and sum(weights) > 0.99999

    N_valid_percentages = 0
    mean_value = 0
    rejected_weighting_sum = 0
    non_rejected_weighting_sum = 0
    for i in range(0, len(percentages)):

        percentage = percentages[i]
        weight = weights[i]

        assert 0 <= weight <= 1

        if percentage > 1e5 or percentage < -100:
            # if this is a nonsensical percentage reduction
            rejected_weighting_sum += weight
        else:
            # if this is a sensical percentage reduction
            N_valid_percentages += 1
            mean_value += percentage * weight
            non_rejected_weighting_sum += weight

    if N_valid_percentages == 0:
        return 9.37e36

    # everything not rejected needs to be renormalized
    renormalization = 1 - rejected_weighting_sum

    # make sure everything not rejected adds up to a weighting of 1
    assert (
        non_rejected_weighting_sum / renormalization >= 0.9999
        and non_rejected_weighting_sum / renormalization <= 1.0001
    )

    return mean_value / renormalization


# MAIN PROGRAM LOGIC FLOW


def get_overall_reduction(country_data):
    """
    determine the total reduction in production using the relative reduction
    in corn, rice, soy, and spring wheat
    """

    # see supplementary information xlsx "summary" tab
    # to see how these ratios are calculated
    crops = {
        "corn": 0.332020251571745,
        "rice": 0.300642569104085,
        "soy": 0.09385529821812,
        "spring_wheat": 0.27348188110605,
    }

    years = [1, 2, 3, 4, 5]  # 5 years of data exist
    yearly_avg_reductions = {}  # average yearly reduction for crop production

    for year in years:
        crops_to_use = []

        reductions = []
        for crop, ratio in crops.items():
            col_name = crop + "_" + "year" + str(year)

            reduction = country_data[col_name]
            # the overall ratio is the sum of the reduction of each crop,
            # times the ratio of calories that this crop represents
            # (crop relocation in nuclear winter is not considered here)
            reductions.append(float(reduction))

        weightings = list(crops.values())
        year_avg = weighted_average_percentages(reductions, weightings)
        yearly_avg_reductions["reduction_year" + str(year)] = year_avg

    return yearly_avg_reductions


def calculate_reductions(country_data):
    """
    calculate the crop reduction percentage for each year and aggregate as array
    """
    yearly_reductions = get_overall_reduction(country_data)

    reductions = [
        float(yearly_reductions["reduction_year1"]),
        float(yearly_reductions["reduction_year2"]),
        float(yearly_reductions["reduction_year3"]),
        float(yearly_reductions["reduction_year4"]),
        float(yearly_reductions["reduction_year5"]),
    ]

    return reductions


def get_all_crops_correct_countries(input_table):
    """
    get the columns with all the reductions for every crop, with the
    countries properly aggregated (eu27+uk combined)
    """

    non_eu_reductions = []
    eu_27_p_uk_to_average = []
    country_ids = []
    for i in range(0, len(countries)):
        country = countries[i]
        country_name = country_names[i]

        # skip missing country
        if country not in input_table.keys():
            print("missing" + country)
            continue

        country_data = input_table[country]

        # skip if there's no data for this country
        # (corn_year1 is just one example)
        if len(country_data["corn_year1"]) == 0:
            continue

        reductions = calculate_reductions(country_data)

        # if one of the EU 27 countries, will process after loop
        if country in eu_27_p_uk_codes:

            eu_27_p_uk_to_average = stack_on_list(eu_27_p_uk_to_average, reductions)

        else:

            non_eu_reductions = stack_on_list(non_eu_reductions, reductions)

            country_ids = stack_on_list(country_ids, (country, country_name))

    eu_27_p_uk_reductions = average_columns(eu_27_p_uk_to_average)

    all_reductions_processed = stack_on_list(non_eu_reductions, eu_27_p_uk_reductions)

    # average all the eu27 and uk together by averaging each column
    country_ids = stack_on_list(country_ids, ("F5707+GBR", "European Union (27) + UK"))

    return country_ids, all_reductions_processed


def main():
    """
    saves a csv with all the countries' crop reductions in nuclear winter
    averaged
    """
    NW_CSV = "../../data/no_food_trade/rutgers_nw_crops_raw.csv"

    input_table = import_csv(NW_CSV)

    country_ids, all_reductions_processed = get_all_crops_correct_countries(input_table)

    # this is the list of headers in the output csv
    nw_csv = np.array(
        [
            "ISO3 Country Code",
            "Country",
            "reduction_year1",
            "reduction_year2",
            "reduction_year3",
            "reduction_year4",
            "reduction_year5",
        ]
    )

    for i in range(0, len(country_ids)):

        country_id = country_ids[i]
        country_reductions = all_reductions_processed[i]

        nw_csv = add_row_to_csv(
            nw_csv, country_id[0], country_id[1], country_reductions
        )

    nw_csv = clean_up_eswatini(nw_csv)

    np.savetxt(
        "../../data/no_food_trade/nuclear_winter_csv.csv",
        nw_csv,
        delimiter=",",
        fmt="%s",
    )


if __name__ == "__main__":
    main()
