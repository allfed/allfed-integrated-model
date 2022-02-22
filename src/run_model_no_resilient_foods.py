# this program runs the optimizer model, and ensures that all the results are 
# reasonable using a couple useful checks to make sure there's nothing wacky 
# going on.

#check that as time increases, more people can be fed

#check that stored food plus meat is always used at the 
#highest rate during the largest food shortage.

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

cin = {}

cin['NMONTHS'] = 84
cin['LIMIT_SEAWEED_AS_PERCENT_KCALS'] = True

cin['NUTRITION'] = {}
cin['NUTRITION']['KCALS_DAILY'] = 2100  #kcals per person per day
cin['NUTRITION']['FAT_DAILY'] = 47  # 35 #grams per person per day
cin['NUTRITION']['PROTEIN_DAILY'] = 51  # 46 #grams per person per day

cin['MAX_SEAWEED_AS_PERCENT_KCALS'] = 0
cin['SEAWEED_NEW_AREA_PER_DAY'] = 0  # 1000 km^2 (seaweed)
cin['SEAWEED_PRODUCTION_RATE'] = 0  # percent (seaweed)

# "Outputs" https://docs.google.com/spreadsheets/d/19kzHpux690JTCo2IX2UA1faAd7R1QcBK/edit#gid=1815939673 cell G12-G14
cin['TONS_DRY_CALORIC_EQIVALENT_SF'] = 1360e6 * 0.96

cin["OG_USE_BETTER_ROTATION"] = False

cin['INCLUDE_PROTEIN'] = True
cin['INCLUDE_FAT'] = True

cin['GREENHOUSE_GAIN_PCT'] = 0

cin['GREENHOUSE_SLOPE_MULTIPLIER'] = 1  # default values from greenhouse paper
cin['INDUSTRIAL_FOODS_SLOPE_MULTIPLIER'] = 1  # default values from CS paper

cin['INITIAL_HARVEST_DURATION'] = 7  # months

cin['IS_NUCLEAR_WINTER'] = True
cin['FLUCTUATION_LIMIT'] = 1.5
cin['KCAL_SMOOTHING'] = False
cin['MEAT_SMOOTHING'] = True
cin['STORED_FOOD_SMOOTHING'] = True

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

cin["CULL_DURATION"] = cin['NMONTHS'] - cin["DELAY"]['FEED_SHUTOFF']

cin['WASTE'] = {}
# cin['WASTE']['CEREALS'] = 0  # %
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
print("Estimated people fed, no resilient foods, no waste")
print(analysis.people_fed_billions)
print("")

np.save('../data/no_resilient_food_primary_analysis.npy',
        analysis,
        allow_pickle=True)

# Plotter.plot_people_fed_combined(time_months_middle, analysis)
# Plotter.plot_people_fed_kcals(time_months_middle, analysis, \
#     'Primary production before waste, no resilient foods',79)

# nuclear winter 150 tab, cell G30-G38  https://docs.google.com/spreadsheets/d/14t3_PUIky6aNiBvw8q24sj6QYxCN9s_VddLY2-eJuPE/edit#gid=1637082097
#overall waste, on farm+distribution+retail
#2x prices (note, currently set to 2019, not 2020)
cin['WASTE'] = {}
# cin['WASTE']['CEREALS'] = 14.46  # %
cin['WASTE']['SUGAR'] = 9.91  # %
cin['WASTE']['MEAT'] = 10.61  # %
cin['WASTE']['DAIRY'] = 11.93  # %
cin['WASTE']['SEAFOOD'] = 9.99  # %
cin['WASTE']['CROPS'] = 14.78  # %
cin['WASTE']['SEAWEED'] = 9.81  # %

cin["EXCESS_CALORIES"] = np.array([0] * cin['NMONTHS'])
cin['DELAY']['FEED_SHUTOFF'] = 3  # months
cin['DELAY']['BIOFUEL_SHUTOFF'] = 2  # months

cin["CULL_DURATION"] = cin['NMONTHS'] - cin["DELAY"]['FEED_SHUTOFF']
cin['RECALCULATE_CULL_DURATION'] = False  # thousand tons

constants['inputs'] = cin
[time_months, time_months_middle, analysis] = optimizer.optimize(constants)
print("Estimated people fed, no resilient foods, minus waste & delayed halt of nonhuman consumption ")
print(analysis.people_fed_billions)
print("")

# Plotter.plot_people_fed_combined(time_months_middle, analysis)
Plotter.plot_fig_1ab(analysis, 77)

# Plotter.plot_people_fed_kcals(time_months_middle, analysis, "Food minus waste & delayed halt \nof nonhuman consumption, no resilient foods",79)