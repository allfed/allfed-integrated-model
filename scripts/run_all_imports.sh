#!/bin/bash

#@author Morgan Rivers
#@date 10-25-22

# This script creates all the imported .csv files in the 
# data/no_food_trade/processed_data folder




cd ../src/import_scripts_no_food_trade
python create_aquaculture_csv.py
python create_grasses_baseline_csv.py
python create_scp_csv.py
python create_biofuel_csv.py
python create_greenhouse_csv.py
python create_seasonality_csv.py
python create_crop_macros_csv.py
python create_head_count_csv.py
python create_seaweed_csv.py
python create_relocation_improvement_csv.py
python create_dairy_csv.py
python create_meat_csv.py
python create_feed_csv.py
python create_nuclear_winter_csv.py
python create_food_stock_csv.py
python create_population_csv.py
python create_food_waste_csv.py
python create_pulp_csv.py
python create_milk_per_animal_csv.py
python create_meat_per_animal_csv.py
python import_food_data.py
cd ../../scripts