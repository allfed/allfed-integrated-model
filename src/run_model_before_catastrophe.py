# this program runs the optimizer model, and ensures that all the results are
# reasonable using a couple useful checks to make sure there's nothing wacky
# going on:

# 1) check that as time increases, more people can be fed

# 2) check that stored food plus meat is always used at the
# highest rate during the largest food shortage.

import os
import sys
import numpy as np
module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)
from src.optimizer import Optimizer
from src.plotter import Plotter

constants = {}
constants['CHECK_CONSTRAINTS'] = False

inputs_to_optimizer = {}

inputs_to_optimizer['NMONTHS'] = 84
inputs_to_optimizer['LIMIT_SEAWEED_AS_PERCENT_KCALS'] = True

inputs_to_optimizer['NUTRITION'] = {}
inputs_to_optimizer['NUTRITION']['KCALS_DAILY'] = 2100  # kcals per person per day
inputs_to_optimizer['NUTRITION']['FAT_DAILY'] = 61.7  # 47#35 #grams per person per day
inputs_to_optimizer['NUTRITION']['PROTEIN_DAILY'] = 59.5  # 51#46 #grams per person per day

inputs_to_optimizer['MAX_SEAWEED_AS_PERCENT_KCALS'] = 0
inputs_to_optimizer['SEAWEED_NEW_AREA_PER_DAY'] = 0
inputs_to_optimizer['SEAWEED_PRODUCTION_RATE'] = 0
inputs_to_optimizer['INDUSTRIAL_FOODS_SLOPE_MULTIPLIER'] = 0
# "Outputs" https://docs.google.com/spreadsheets/d/19kzHpux690JTCo2IX2UA1faAd7R1QcBK/edit#gid=1815939673 cell G12-G14
inputs_to_optimizer['TONS_DRY_CALORIC_EQIVALENT_SF'] = 0.96 * 351.433 * 1e6

# these fat and protein values do not produce realistic outputs, so outdoor growing ratios were used instead
# inputs_to_optimizer['INITIAL_SF_FAT'] = 166.07e3 * 351e6/1360e6
# inputs_to_optimizer['INITIAL_SF_PROTEIN'] = 69.25e3 * 351e6/1360e6

inputs_to_optimizer["OG_USE_BETTER_ROTATION"] = False

inputs_to_optimizer['INCLUDE_PROTEIN'] = True
inputs_to_optimizer['INCLUDE_FAT'] = True


inputs_to_optimizer['INITIAL_HARVEST_DURATION_IN_MONTHS'] = 7  # (no difference between harvests!)

inputs_to_optimizer['FLUCTUATION_LIMIT'] = 1.5  # not used unless smoothing true
inputs_to_optimizer['IS_NUCLEAR_WINTER'] = False
inputs_to_optimizer['KCAL_SMOOTHING'] = False
inputs_to_optimizer['MEAT_SMOOTHING'] = False
inputs_to_optimizer['STORED_FOOD_SMOOTHING'] = False

inputs_to_optimizer['ADD_CELLULOSIC_SUGAR'] = False
inputs_to_optimizer['ADD_DAIRY'] = True
inputs_to_optimizer['ADD_FISH'] = True
inputs_to_optimizer['ADD_GREENHOUSES'] = False
inputs_to_optimizer['ADD_OUTDOOR_GROWING'] = True
inputs_to_optimizer['ADD_MEAT'] = True
inputs_to_optimizer['ADD_METHANE_SCP'] = False
inputs_to_optimizer['ADD_SEAWEED'] = False
inputs_to_optimizer['ADD_STORED_FOOD'] = True

inputs_to_optimizer["EXCESS_CALORIES"] = np.array([0] * inputs_to_optimizer['NMONTHS'])
inputs_to_optimizer["DELAY"] = {}
inputs_to_optimizer["DELAY"]['FEED_SHUTOFF_MONTHS'] = 0
inputs_to_optimizer["DELAY"]['BIOFUEL_SHUTOFF_MONTHS'] = 0

inputs_to_optimizer["CULL_DURATION_MONTHS"] = np.nan  # not used unless nuclear winter

inputs_to_optimizer['WASTE'] = {}
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
print("Maximum usable kcals/capita/day 2020, no waste, primary production")
print(analysis.people_fed_billions/7.8*2100)
print("")

analysis1 = analysis

# Plotter.plot_people_fed_combined(time_months_middle, analysis)
# Plotter.plot_people_fed_kcals(time_months_middle, analysis,
    # 'Primary production before waste, baseline',78)

# nuclear winter 150 tab, cell G30-G38  https://docs.google.com/spreadsheets/d/14t3_PUIky6aNiBvw8q24sj6QYxCN9s_VddLY2-eJuPE/edit#gid=1637082097
# overall waste, on farm+distribution+retail
# 1x prices (note, currently set to 2019, not 2020)
inputs_to_optimizer['WASTE'] = {}
inputs_to_optimizer['WASTE']['CEREALS'] = 28.52  # %
inputs_to_optimizer['WASTE']['SUGAR'] = 23.96  # %
inputs_to_optimizer['WASTE']['MEAT'] = 24.67  # %
inputs_to_optimizer['WASTE']['DAIRY'] = 25.99  # %
inputs_to_optimizer['WASTE']['SEAFOOD'] = 24.04  # %
inputs_to_optimizer['WASTE']['CROPS'] = 28.83  # %
inputs_to_optimizer['WASTE']['SEAWEED'] = 23.87  # %

inputs_to_optimizer["EXCESS_CALORIES"] = np.array([0] * inputs_to_optimizer['NMONTHS'])
inputs_to_optimizer["DELAY"]['FEED_SHUTOFF_MONTHS'] = inputs_to_optimizer['NMONTHS']
inputs_to_optimizer["DELAY"]['BIOFUEL_SHUTOFF_MONTHS'] = inputs_to_optimizer['NMONTHS']

inputs_to_optimizer["CULL_DURATION_MONTHS"] = np.nan  # not used unless nuclear winter

optimizer = Optimizer()
constants['inputs'] = inputs_to_optimizer
[time_months, time_months_middle, analysis] = optimizer.optimize(constants)

analysis2 = analysis

# Plotter.plot_people_fed_combined(time_months_middle, analysis)
# Plotter.plot_people_fed_kcals(time_months_middle, analysis, "Baseline around 2020 average diet", inputs_to_optimizer['NMONTHS'])

Plotter.plot_fig_s1abcd(analysis1, analysis2, 72)
