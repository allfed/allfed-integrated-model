################################Optimizer Model################################
##                                                                            #
##                   Convert everything into consistent units                 #
##                and import the spreadsheet into a program-readable          #
##                                                                            #
###############################################################################


import pandas as pd
import numpy as np
import requests
import json
import os
import matplotlib.pyplot as plt
import matplotlib.colors as colors

import geopandas as gpd
import copy

from functools import reduce


NO_TRADE_XLS = "../../data/no_food_trade/Integrated Model With No Food Trade.xlsx"

# create some simpler, more readable names for the columns stored in a dictionary
# of dictionaries
col_names = {}

col_names["population"] = {
    "ISO3 Country Code": "iso3",
    "Country": "country",
    "Population (millions), 2020": "population",
}

col_names["aquaculture"] = {
    "ISO3 Country Code": "iso3",
    "Seafood calories - million tonnes dry caloric, 2020": "aq_kcals",
    "Seafood fat - million tonnes, 2020": "aq_fat",
    "Seafood protein - million tonnes, 2020": "aq_protein",
}

col_names["grasses"] = {
    "ISO3 Country Code": "iso3",
    "Inedible food for ruminants - Baseline 2020 - '000 tonnes": "grasses_baseline",
    "Inedible food for ruminants - Year 1 - '000 tonnes": "grasses_y1",
    "Inedible food for ruminants - Year 2 - '000 tonnes": "grasses_y2",
    "Inedible food for ruminants - Year 3 - '000 tonnes": "grasses_y3",
    "Inedible food for ruminants - Year 4 - '000 tonnes": "grasses_y4",
    "Inedible food for ruminants - Year 5 - '000 tonnes": "grasses_y5",
    "Inedible food for ruminants - Year 6 - '000 tonnes": "grasses_y6",
    "Inedible food for ruminants - Year 7 - '000 tonnes": "grasses_y7",
    "Inedible food for ruminants - Year 8 - '000 tonnes": "grasses_y8",
    "Inedible food for ruminants - Year 9 - '000 tonnes": "grasses_y9",
    "Inedible food for ruminants - Year 10 - '000 tonnes": "grasses_y10",
}

col_names["dairy"] = {
    "ISO3 Country Code": "iso3",
    "Current milk output - '000 tonnes wet value": "dairy",
}

col_names["meat"] = {
    "ISO3 Country Code": "iso3",
    "Chicken production in 2020 (tonnes)": "chicken",
    "Pork production in 2020 (tonnes)": "pork",
    "Beef production in 2020 (tonnes)": "beef",
}

col_names["head_counts"] = {
    "ISO3 Country Code": "iso3",
    "Small animal count": "small_animals",
    "Medium animal count": "medium_animals",
    "Large animal count": "large_animals",
    "Dairy cow count": "dairy_cows",
}

col_names["biofuel"] = {
    "ISO3 Country Code": "iso3",
    "Biofuel/other caloric consumption in 2020 (million dry caloric tons)": "biofuel_kcals",
    "Biofuel/other fat consumption in 2020 (tonnes)": "biofuel_fat",
    "Biofuel/other protein consumption in 2020 (tonnes)": "biofuel_protein",
}

col_names["feed"] = {
    "ISO3 Country Code": "iso3",
    "Animal feed caloric consumption in 2020 (dry caloric tons)": "feed_kcals",
    "Animal feed fat consumption in 2020 (tonnes)": "feed_fat",
    "Animal feed protein consumption in 2020 (tonnes)": "feed_protein",
}

col_names["crop_baseline"] = {
    "ISO3 Country Code": "iso3",
    "Outdoor crop caloric production in 2020 (dry caloric tons)": "crop_kcals",
    "Outdoor crop fat production in 2020 (tonnes)": "crop_fat",
    "Outdoor crop protein production in 2020 (tonnes)": "crop_protein",
}

col_names["crop_seasonality"] = {
    "ISO3 Country Code": "iso3",
    "January": "seasonality_m1",
    "February": "seasonality_m2",
    "March": "seasonality_m3",
    "April": "seasonality_m4",
    "May": "seasonality_m5",
    "June": "seasonality_m6",
    "July": "seasonality_m7",
    "August": "seasonality_m8",
    "September": "seasonality_m9",
    "October": "seasonality_m10",
    "November": "seasonality_m11",
    "December": "seasonality_m12",
}

col_names["food_stocks"] = {
    "ISO3 Country Code": "iso3",
    """Food Stocks calories,\
 approximate, May 2016-2020 average, million tonnes dry caloric value""": "stocks_kcals",
    "Food Stocks fat, approximate, May 2016-2020 average, million tonnes fat": "stocks_fat",
    """Food Stocks protein,\
 approximate, May 2016-2020 average, million tonnes protein""": "stocks_protein",
}


col_names["cellulosis_sugar"] = {
    "ISO3 Country Code": "iso3",
    "Country chemical wood pulp 2020 (tonnes)": "wood_pulp_tonnes",
    "Ratio to sum total": "percent_of_global_production",
}


col_names["methane_scp"] = {
    "ISO3 Country Code": "iso3",
    "Estimated Capex for related industries - Average 2014-2018 - 2015 US$ billion basis": "capex_dollar",
    "% of global chemical and related CAPEX": "percent_of_global_capex",
}


col_names["greenhouses"] = {
    "ISO3 Country Code": "iso3",
    "Country Crop Area ('000 Hectares)": "crop_area_1000ha",
    "Latitude": "Latitude",
    "Whether above latitude threshold (23)": "above_lat_23_boolean",
    "Fraction of total crop area - below 23 latitude": "fraction_crop_area_below_lat_23",
}


# import raw data from the dowloaded spreadsheet


xls = pd.ExcelFile(NO_TRADE_XLS)


# Load all dataframes into a dictionary, so we can iterate over it
dataframe_dict = {}
# A dictionary with the name of the food in excel as the value and the name we use in pandas as key
food_names = {
    "population": "Population",
    "aquaculture": "Seafood - excluding seaweeds",
    "grasses": "Grazing",
    "dairy": "Grazing",
    "meat": "Meat Production",
    "head_counts": "Head Counts",
    "biofuel": "Biofuel",
    "feed": "Feed",
    "crop_baseline": "Outdoor Crop Baseline",
    "crop_seasonality": "Outdoor Crop Seasonality",
    "food_stocks": "Food Stocks",
    "cellulosis_sugar": "Cellulosic Sugar",
    "methane_scp": "Methane SCP",
    "greenhouses": "Greenhouses",
}

for pandas_name, excel_name in food_names.items():
    # Only take the first 138 rows, as this includes all countries, but excludes
    # the calculations done below it.
    temp_df = pd.read_excel(xls, excel_name, nrows=137)[
        list(col_names[pandas_name].keys())
    ]

    # Rename columns to nicer names
    temp_df.rename(columns=col_names[pandas_name], inplace=True)

    # make the country name the index
    temp_df.index = temp_df["iso3"]

    del temp_df["iso3"]
    # print(temp_df.head())

    dataframe_dict[pandas_name] = temp_df


# make the units compatible with the units used in the constants.py model


# convert to per person units
dataframe_dict["population"]["population"] = (
    dataframe_dict["population"]["population"] * 1e6
)

# convert to tons dry caloric
dataframe_dict["aquaculture"]["aq_kcals"] = (
    dataframe_dict["aquaculture"]["aq_kcals"] * 1e6
)

# convert to tons fat
dataframe_dict["aquaculture"]["aq_fat"] = dataframe_dict["aquaculture"]["aq_fat"] * 1e6

# convert to tons protein
dataframe_dict["aquaculture"]["aq_protein"] = (
    dataframe_dict["aquaculture"]["aq_protein"] * 1e6
)


# convert to tons dry caloric equivalent annually
dataframe_dict["grasses"]["grasses_baseline"] = (
    dataframe_dict["grasses"]["grasses_baseline"] * 1000
)
for i in range(1, 11):
    dataframe_dict["grasses"]["grasses_y" + str(i)] = (
        dataframe_dict["grasses"]["grasses_y" + str(i)] * 1000
    )


# convert to tons wet annually
dataframe_dict["dairy"]["dairy"] = dataframe_dict["dairy"]["dairy"] * 1000


# convert to tons dry caloric
dataframe_dict["food_stocks"]["stocks_kcals"] = (
    dataframe_dict["food_stocks"]["stocks_kcals"] * 1e3
)

# convert to tons fat
dataframe_dict["food_stocks"]["stocks_fat"] = (
    dataframe_dict["food_stocks"]["stocks_fat"] * 1e3
)

# convert to tons protein
dataframe_dict["food_stocks"]["stocks_protein"] = (
    dataframe_dict["food_stocks"]["stocks_protein"] * 1e3
)


# biofuel
dataframe_dict["biofuel"]["biofuel_kcals"] = (
    dataframe_dict["biofuel"]["biofuel_kcals"] * 1e6
)

# biofuel
dataframe_dict["biofuel"]["biofuel_fat"] = (
    dataframe_dict["biofuel"]["biofuel_fat"] * 1e6
)

# biofuel
dataframe_dict["biofuel"]["biofuel_protein"] = (
    dataframe_dict["biofuel"]["biofuel_protein"] * 1e6
)


# #combine the data frames from all the tabs into a giant dataframe

# everestial007 explains the merge quite neatly https://stackoverflow.com/questions/44327999/python-pandas-merge-multiple-dataframes
df_merged = reduce(
    lambda left, right: pd.merge(  # Merge DataFrames in list
        left, right, right_index=True, left_index=True, how="outer"
    ),
    dataframe_dict.values(),
)


df_merged.to_csv("../../data/no_food_trade/computer_readable_combined.csv")
