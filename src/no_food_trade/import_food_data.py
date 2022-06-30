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
import geoplot as gplt
import copy

from functools import reduce


NO_TRADE_XLS = \
    '../../data/no_food_trade/Integrated Model With No Food Trade.xlsx'

# create some simpler, more readable names for the columns stored in a list
# of dictionaries
col_names = {}

col_names['population'] = {
    'ISO3 Country Code': "iso3",
    "Country": "country",
    "Population (millions), 2020": "population"
}

col_names['aquaculture'] = {
    'ISO3 Country Code': "iso3",
    "Seafood calories - million tonnes dry caloric, 2020": "aq_kcals",
    "Seafood fat - million tonnes, 2020": "aq_fat",
    "Seafood protein - million tonnes, 2020": "aq_protein"
}

col_names['grasses'] = {
    'ISO3 Country Code': 'iso3',
    "Inedible food for ruminants - Baseline 2020 - '000 tonnes"
        : "grasses_baseline",
    "Inedible food for ruminants - Year 1 - '000 tonnes": 'grasses_y1',
    "Inedible food for ruminants - Year 2 - '000 tonnes": 'grasses_y2',
    "Inedible food for ruminants - Year 3 - '000 tonnes": 'grasses_y3',
    "Inedible food for ruminants - Year 4 - '000 tonnes": 'grasses_y4',
    "Inedible food for ruminants - Year 5 - '000 tonnes": 'grasses_y5',
    "Inedible food for ruminants - Year 6 - '000 tonnes": 'grasses_y6',
    "Inedible food for ruminants - Year 7 - '000 tonnes": 'grasses_y7',
    "Inedible food for ruminants - Year 8 - '000 tonnes": 'grasses_y8',
    "Inedible food for ruminants - Year 9 - '000 tonnes": 'grasses_y9',
    "Inedible food for ruminants - Year 10 - '000 tonnes": 'grasses_y10',
}

col_names['dairy'] = {
    'ISO3 Country Code': 'iso3',
    "Current milk output - '000 tonnes wet value": 'dairy'
}

col_names['meat'] = {
    'ISO3 Country Code': 'iso3',
    "Chicken production in 2020 (tonnes)": 'chicken',
    "Pork production in 2020 (tonnes)": 'pork',
    "Beef production in 2020 (tonnes)": 'beef'
}

col_names['head_counts'] = {
    'ISO3 Country Code': 'iso3',
    "Small animal count": 'small_animals',
    "Medium animal count": 'medium_animals',
    "Large animal count": 'large_animals',
    "Dairy cow count": 'dairy_cows'
}

col_names['biofuel'] = {
    'ISO3 Country Code': 'iso3',
    "Biofuel/other caloric consumption in 2020 (million dry caloric tons)": 'biofuel_kcals',
    "Biofuel/other fat consumption in 2020 (tonnes)": 'biofuel_fat',
    "Biofuel/other protein consumption in 2020 (tonnes)": 'biofuel_protein'
}

col_names['feed'] = {
    'ISO3 Country Code': 'iso3',
    "Animal feed caloric consumption in 2020 (dry caloric tons)": 'feed_kcals',
    "Animal feed fat consumption in 2020 (tonnes)": 'feed_fat',
    "Animal feed protein consumption in 2020 (tonnes)": 'feed_protein'
}

col_names['crop_baseline'] = {
    'ISO3 Country Code': 'iso3',
    "Outdoor crop caloric production in 2020 (dry caloric tons)": 'crop_kcals',
    "Outdoor crop fat production in 2020 (tonnes)": 'crop_fat',
    "Outdoor crop protein production in 2020 (tonnes)": 'crop_protein'
}

col_names['crop_seasonality'] = {
    'ISO3 Country Code': 'iso3',
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
    "December": "seasonality_m12"
}

col_names['food_stocks'] = {
    'ISO3 Country Code': 'iso3',
    """Food Stocks calories,\
 approximate, May 2016-2020 average, million tonnes dry caloric value""":
        'stocks_kcals',
    "Food Stocks fat, approximate, May 2016-2020 average, million tonnes fat":
        'stocks_fat',
"""Food Stocks protein,\
 approximate, May 2016-2020 average, million tonnes protein""":
        'stocks_protein'
}


# import raw data from the dowloaded spreadsheet


xls = pd.ExcelFile(NO_TRADE_XLS)

population = pd.read_excel(xls, 'Population')[
    list(col_names['population'].keys())
]

population.rename(columns=col_names['population'], inplace=True)


aquaculture = pd.read_excel(xls, 'Seafood - excluding seaweeds')[
    list(col_names['aquaculture'].keys())
]

aquaculture.rename(columns=col_names['aquaculture'], inplace=True)


grasses = pd.read_excel(xls, 'Grazing')[
    list(col_names['grasses'].keys())
]

grasses.rename(columns=col_names['grasses'], inplace=True)


dairy = pd.read_excel(xls, 'Grazing')[
    list(col_names['dairy'].keys())
]

dairy.rename(columns=col_names['dairy'], inplace=True)


meat = pd.read_excel(xls, 'Meat Production')[
    list(col_names['meat'].keys())
]

meat.rename(columns=col_names['meat'], inplace=True)


head_counts = pd.read_excel(xls, 'Head Counts')[
    list(col_names['head_counts'].keys())
]

head_counts.rename(columns=col_names['head_counts'], inplace=True)


biofuel = pd.read_excel(xls, 'Biofuel')[
    list(col_names['biofuel'].keys())
]

biofuel.rename(columns=col_names['biofuel'], inplace=True)


feed = pd.read_excel(xls, 'Feed')[
    list(col_names['feed'].keys())
]

feed.rename(columns=col_names['feed'], inplace=True)


crop_baseline = pd.read_excel(xls, 'Outdoor Crop Baseline')[
    list(col_names['crop_baseline'].keys())
]

crop_baseline.rename(columns=col_names['crop_baseline'], inplace=True)


crop_seasonality = pd.read_excel(xls, 'Outdoor Crop Seasonality')[
    list(col_names['crop_seasonality'].keys())
]

crop_seasonality.rename(
    columns=col_names['crop_seasonality'],
    inplace=True
)


food_stocks = pd.read_excel(xls, 'Food Stocks')[
    list(col_names['food_stocks'].keys())
]

# Rename columns to nicer names
food_stocks.rename(columns=col_names['food_stocks'], inplace=True)



# make the units compatible with the units used in the constants.py model



# convert to per person units
population['population'] = population['population'] * 1e6

# convert to tons dry caloric
aquaculture['aq_kcals'] = aquaculture['aq_kcals'] * 1e6

# convert to tons fat
aquaculture['aq_fat'] = aquaculture['aq_fat'] * 1e6

# convert to tons protein
aquaculture['aq_protein'] = aquaculture['aq_protein'] * 1e6


# convert to tons dry caloric equivalent annually
grasses['grasses_baseline'] = grasses['grasses_baseline'] * 1000
grasses['grasses_y1'] = grasses['grasses_y1'] * 1000
grasses['grasses_y2'] = grasses['grasses_y2'] * 1000
grasses['grasses_y3'] = grasses['grasses_y3'] * 1000
grasses['grasses_y4'] = grasses['grasses_y4'] * 1000
grasses['grasses_y5'] = grasses['grasses_y5'] * 1000
grasses['grasses_y6'] = grasses['grasses_y6'] * 1000
grasses['grasses_y7'] = grasses['grasses_y7'] * 1000
grasses['grasses_y8'] = grasses['grasses_y8'] * 1000
grasses['grasses_y9'] = grasses['grasses_y9'] * 1000
grasses['grasses_y10'] = grasses['grasses_y10'] * 1000


# convert to tons wet annually
dairy['dairy'] = dairy['dairy'] * 1000


# convert to tons dry caloric
food_stocks['stocks_kcals'] = food_stocks['stocks_kcals'] * 1e3

# convert to tons fat
food_stocks['stocks_fat'] = food_stocks['stocks_fat'] * 1e3

# convert to tons protein
food_stocks['stocks_protein'] = food_stocks['stocks_protein'] * 1e3


# biofuel
biofuel['biofuel_kcals'] = biofuel['biofuel_kcals'] * 1e6

# biofuel
biofuel['biofuel_fat'] = biofuel['biofuel_fat'] * 1e6

# biofuel
biofuel['biofuel_protein'] = biofuel['biofuel_protein'] * 1e6


# combine the data frames from all the tabs into a giant dataframe
data_frames = [population, aquaculture, grasses, dairy, meat, head_counts,
               biofuel, feed, crop_baseline, crop_seasonality, food_stocks]

# everestial007 explains the merge quite neatly https://stackoverflow.com/questions/44327999/python-pandas-merge-multiple-dataframes
df_merged = reduce(lambda left, right: pd.merge(left, right, on=['iso3'],
                                                how='outer'), data_frames)

# get rid of empty row countries
df_merged.dropna(subset=["iso3"], inplace=True)

df_merged.to_csv("../../data/no_food_trade/computer_readable_combined.csv")