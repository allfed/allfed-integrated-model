# this program runs the optimizer model, and ensures that all the results are
# reasonable using a couple useful checks to make sure there's nothing wacky
# going on:

# 1) check that as time increases, more people can be fed

# 2) check that stored food plus meat is always used at the
# highest rate during the largest food shortage.

import os
import sys
module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)
from src.optimizer import Optimizer
from src.plotter import Plotter
import numpy as np

constants = {}

constants['CHECK_CONSTRAINTS'] = False

inputs_to_optimizer = {}

inputs_to_optimizer['NMONTHS'] = 84
inputs_to_optimizer['LIMIT_SEAWEED_AS_PERCENT_KCALS'] = True

inputs_to_optimizer['NUTRITION'] = {}
inputs_to_optimizer['NUTRITION']['KCALS_DAILY'] = 2100  #kcals per person per day
inputs_to_optimizer['NUTRITION']['FAT_DAILY'] = 47  # 35 #grams per person per day
inputs_to_optimizer['NUTRITION']['PROTEIN_DAILY'] = 51  # 46 #grams per person per day

inputs_to_optimizer['MAX_SEAWEED_AS_PERCENT_KCALS'] = 0
inputs_to_optimizer['SEAWEED_NEW_AREA_PER_DAY'] = 0  # 1000 km^2 (seaweed)
inputs_to_optimizer['SEAWEED_PRODUCTION_RATE'] = 0  # percent (seaweed)

# "Outputs" https://docs.google.com/spreadsheets/d/19kzHpux690JTCo2IX2UA1faAd7R1QcBK/edit#gid=1815939673 cell G12-G14
inputs_to_optimizer['TONS_DRY_CALORIC_EQIVALENT_SF'] = 0*1360e6 * 0.96

inputs_to_optimizer["OG_USE_BETTER_ROTATION"] = False
# inputs_to_optimizer["ROTATION_IMPROVEMENTS"] = {}
# inputs_to_optimizer["ROTATION_IMPROVEMENTS"]["KCALS_REDUCTION"] = .93
# inputs_to_optimizer["ROTATION_IMPROVEMENTS"]["FAT_RATIO"] = 1.487
# inputs_to_optimizer["ROTATION_IMPROVEMENTS"]["PROTEIN_RATIO"] = 1.108

inputs_to_optimizer['INCLUDE_PROTEIN'] = True
inputs_to_optimizer['INCLUDE_FAT'] = True

inputs_to_optimizer['GREENHOUSE_GAIN_PCT'] = 0

inputs_to_optimizer['GREENHOUSE_SLOPE_MULTIPLIER'] = 1  # default values from greenhouse paper
inputs_to_optimizer['INDUSTRIAL_FOODS_SLOPE_MULTIPLIER'] = 1  # default values from CS paper

inputs_to_optimizer['INITIAL_HARVEST_DURATION_IN_MONTHS'] = 7

inputs_to_optimizer['IS_NUCLEAR_WINTER'] = True
inputs_to_optimizer['FLUCTUATION_LIMIT'] = 1.5
inputs_to_optimizer['KCAL_SMOOTHING'] = False
inputs_to_optimizer['MEAT_SMOOTHING'] = True
inputs_to_optimizer['STORED_FOOD_SMOOTHING'] = True

inputs_to_optimizer['ADD_CELLULOSIC_SUGAR'] = False
inputs_to_optimizer['ADD_DAIRY'] = False
inputs_to_optimizer['ADD_FISH'] = True
inputs_to_optimizer['ADD_GREENHOUSES'] = False
inputs_to_optimizer['ADD_OUTDOOR_GROWING'] = True
inputs_to_optimizer['ADD_MEAT'] = False
inputs_to_optimizer['ADD_METHANE_SCP'] = False
inputs_to_optimizer['ADD_SEAWEED'] = False
inputs_to_optimizer['ADD_STORED_FOOD'] = True

inputs_to_optimizer["EXCESS_CALORIES"] = np.array([0] * inputs_to_optimizer['NMONTHS'])
inputs_to_optimizer["DELAY"] = {}
inputs_to_optimizer["DELAY"]['FEED_SHUTOFF_MONTHS'] = 0
inputs_to_optimizer["DELAY"]['BIOFUEL_SHUTOFF_MONTHS'] = 0
inputs_to_optimizer["DELAY"]['ROTATION_CHANGE_IN_MONTHS'] = 2

inputs_to_optimizer["CULL_DURATION_MONTHS"] = 60

inputs_to_optimizer['WASTE'] = {}
# inputs_to_optimizer['WASTE']['CEREALS'] = 0  # %
inputs_to_optimizer['WASTE']['SUGAR'] = 0  # %
inputs_to_optimizer['WASTE']['MEAT'] = 0  # %
inputs_to_optimizer['WASTE']['DAIRY'] = 0  # %
inputs_to_optimizer['WASTE']['SEAFOOD'] = 0  # %
inputs_to_optimizer['WASTE']['CROPS'] = 0  # %
inputs_to_optimizer['WASTE']['SEAWEED'] = 0  # %

optimizer = Optimizer()
constants['inputs'] = inputs_to_optimizer
[time_months, time_months_middle, analysis] = optimizer.optimize(constants)

print("")
print("Estimated Kcals/capita/day, no resilient foods, no waste")
print(analysis.people_fed_billions/7.8*2100)
print("")

np.save('../data/no_resilient_food_primary_analysis.npy',
        analysis,
        allow_pickle=True)

# Plotter.plot_people_fed_combined(time_months_middle, analysis)
# Plotter.plot_people_fed_kcals(time_months_middle, analysis, \
#     'Primary production before waste, no resilient foods',79)

# nuclear winter 150 tab, cell G30-G38  https://docs.google.com/spreadsheets/d/14t3_PUIky6aNiBvw8q24sj6QYxCN9s_VddLY2-eJuPE/edit#gid=1637082097
# overall waste, on farm + distribution + retail
# 2x prices (note, currently set to 2019, not 2020)
inputs_to_optimizer['WASTE'] = {}
# inputs_to_optimizer['WASTE']['CEREALS'] = 14.46  # %
inputs_to_optimizer['WASTE']['SUGAR'] = 9.91  # %
inputs_to_optimizer['WASTE']['MEAT'] = 10.61  # %
inputs_to_optimizer['WASTE']['DAIRY'] = 11.93  # %
inputs_to_optimizer['WASTE']['SEAFOOD'] = 9.99  # %
inputs_to_optimizer['WASTE']['CROPS'] = 14.78  # %
inputs_to_optimizer['WASTE']['SEAWEED'] = 9.81  # %

inputs_to_optimizer["EXCESS_CALORIES"] = np.array([0] * inputs_to_optimizer['NMONTHS'])
inputs_to_optimizer['DELAY']['FEED_SHUTOFF_MONTHS'] = 3
inputs_to_optimizer['DELAY']['BIOFUEL_SHUTOFF_MONTHS'] = 2

inputs_to_optimizer["CULL_DURATION_MONTHS"] = 60 # inputs_to_optimizer['NMONTHS'] - inputs_to_optimizer["DELAY"]['FEED_SHUTOFF_MONTHS']
inputs_to_optimizer['RECALCULATE_CULL_DURATION_MONTHS'] = False  # thousand tons

constants['inputs'] = inputs_to_optimizer
[time_months, time_months_middle, analysis] = optimizer.optimize(constants)
print("Estimated Kcals/capita/day, no resilient foods, minus waste & delayed halt of nonhuman consumption ")

print(analysis.people_fed_billions/7.8*2100)

print("")

# Plotter.plot_people_fed_combined(time_months_middle, analysis)
Plotter.plot_fig_1ab(analysis, 77)

# Plotter.plot_people_fed_kcals(time_months_middle, analysis, "Food minus waste & delayed halt \nof nonhuman consumption, no resilient foods",79)
