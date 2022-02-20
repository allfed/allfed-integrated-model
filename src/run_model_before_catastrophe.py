# this program runs the optimizer model, and ensures that all the results are 
# reasonable using a couple useful checks to make sure there's nothing wacky 
# going on.

#check that as time increases, more people can be fed

#check that stored food plus meat is always used at the 
#highest rate during the largest food shortage.

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

cin = {}

cin['NMONTHS'] = 84
cin['LIMIT_SEAWEED_AS_PERCENT_KCALS'] = True

cin['NUTRITION'] = {}
cin['NUTRITION']['KCALS_DAILY'] = 2100  # kcals per person per day
cin['NUTRITION']['FAT_DAILY'] = 61.7  # 47#35 #grams per person per day
cin['NUTRITION']['PROTEIN_DAILY'] = 59.5  # 51#46 #grams per person per day

cin['MAX_SEAWEED_AS_PERCENT_KCALS'] = 0
cin['SEAWEED_NEW_AREA_PER_DAY'] = 0
cin['SEAWEED_PRODUCTION_RATE'] = 0
cin['INDUSTRIAL_FOODS_SLOPE_MULTIPLIER'] = 0
# "Outputs" https://docs.google.com/spreadsheets/d/19kzHpux690JTCo2IX2UA1faAd7R1QcBK/edit#gid=1815939673 cell G12-G14
cin['TONS_DRY_CALORIC_EQIVALENT_SF'] = 0.96 * 351.433 * 1e6

#these fat and protein values do not produce realistic outputs, so outdoor growing ratios were used instead
# cin['INITIAL_SF_FAT'] = 166.07e3 * 351e6/1360e6
# cin['INITIAL_SF_PROTEIN'] = 69.25e3 * 351e6/1360e6

cin["OG_USE_BETTER_ROTATION"] = False

cin['INCLUDE_PROTEIN'] = True
cin['INCLUDE_FAT'] = True


cin['INITIAL_HARVEST_DURATION'] = 7  # (no difference between harvests!)

cin['FLUCTUATION_LIMIT'] = 1.5  # not used unless smoothing true
cin['IS_NUCLEAR_WINTER'] = False
cin['KCAL_SMOOTHING'] = False
cin['MEAT_SMOOTHING'] = False
cin['STORED_FOOD_SMOOTHING'] = False

cin['ADD_CELLULOSIC_SUGAR'] = False
cin['ADD_DAIRY'] = True
cin['ADD_FISH'] = True
cin['ADD_GREENHOUSES'] = False
cin['ADD_OUTDOOR_GROWING'] = True
cin['ADD_MEAT'] = True
cin['ADD_METHANE_SCP'] = False
cin['ADD_SEAWEED'] = False
cin['ADD_STORED_FOOD'] = True

cin["EXCESS_CALORIES"] = np.array([0] * cin['NMONTHS'])
cin["DELAY"] = {}
cin["DELAY"]['FEED_SHUTOFF'] = 0  # months
cin["DELAY"]['BIOFUEL_SHUTOFF'] = 0  # months

cin["CULL_DURATION"] = np.nan  # not used unless nuclear winter

cin['WASTE'] = {}
cin['WASTE']['SUGAR'] = 0  # %
cin['WASTE']['MEAT'] = 0  # %
cin['WASTE']['DAIRY'] = 0  # %
cin['WASTE']['SEAFOOD'] = 0  # %
cin['WASTE']['CROPS'] = 0  # %
cin['WASTE']['SEAWEED'] = 0  # %

optimizer = Optimizer()
constants['inputs'] = cin
[time_months, time_months_middle, analysis] = optimizer.optimize(constants)

print("")
print("")
print("")
print("")
print("people_fed_billions")
print(analysis.people_fed_billions)
print("")
print("")
print("")
print("")

analysis1 = analysis

# Plotter.plot_people_fed_combined(time_months_middle, analysis)
# Plotter.plot_people_fed_kcals(time_months_middle, analysis,
    # 'Primary production before waste, baseline',78)

# nuclear winter 150 tab, cell G30-G38  https://docs.google.com/spreadsheets/d/14t3_PUIky6aNiBvw8q24sj6QYxCN9s_VddLY2-eJuPE/edit#gid=1637082097
#overall waste, on farm+distribution+retail
#1x prices (note, currently set to 2019, not 2020)
cin['WASTE'] = {}
cin['WASTE']['CEREALS'] = 28.52  # %
cin['WASTE']['SUGAR'] = 23.96  # %
cin['WASTE']['MEAT'] = 24.67  # %
cin['WASTE']['DAIRY'] = 25.99  # %
cin['WASTE']['SEAFOOD'] = 24.04  # %
cin['WASTE']['CROPS'] = 28.83  # %
cin['WASTE']['SEAWEED'] = 23.87  # %

cin["EXCESS_CALORIES"] = np.array([0] * cin['NMONTHS'])
cin["DELAY"]['FEED_SHUTOFF'] = cin['NMONTHS']
cin["DELAY"]['BIOFUEL_SHUTOFF'] = cin['NMONTHS']

cin["CULL_DURATION"] = np.nan  # not used unless nuclear winter

optimizer = Optimizer()
constants['inputs'] = cin
[time_months, time_months_middle, analysis] = optimizer.optimize(constants)

print("")
print("")
print("")
print("")
print("people_fed_billions")
print(analysis.people_fed_billions)
print("")
print("")
print("")
print("")

analysis2 = analysis

# Plotter.plot_people_fed_combined(time_months_middle, analysis)
# Plotter.plot_people_fed_kcals(time_months_middle, analysis, "Baseline around 2020 average diet", cin['NMONTHS'])

Plotter.plot_figure_supplement_before_catastrophe_abcd(analysis1, analysis2, 72)
