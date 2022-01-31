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
c = {} #c = constants
c['CHECK_CONSTRAINTS'] = False

c['inputs'] = {}

c['inputs']['NMONTHS'] = 84
c['inputs']['LIMIT_SEAWEED_AS_PERCENT_KCALS'] = True

c['inputs']['NUTRITION'] = {}
c['inputs']['NUTRITION']['KCALS_DAILY'] = 2100  #kcals per person per day
c['inputs']['NUTRITION']['FAT_DAILY'] = 47  # 35 #grams per person per day
c['inputs']['NUTRITION']['PROTEIN_DAILY'] = 51  # 46 #grams per person per day

c['inputs']['MAX_SEAWEED_AS_PERCENT_KCALS'] = 10
c['inputs']['NEW_AREA_PER_DAY'] = 2.0765  # 1000 km^2 (seaweed)
c['inputs']['SEAWEED_PRODUCTION_RATE'] = 10  # percent (seaweed)

# "Outputs" https://docs.google.com/spreadsheets/d/19kzHpux690JTCo2IX2UA1faAd7R1QcBK/edit#gid=1815939673 cell G12-G14
c['inputs']['TONS_DRY_CALORIC_EQIVALENT_SF'] = 1360e6 * 0.96

c["inputs"]["OG_USE_BETTER_ROTATION"] = False

c['inputs']['INCLUDE_PROTEIN'] = True
c['inputs']['INCLUDE_FAT'] = True

c['inputs']['GREENHOUSE_GAIN_PCT'] = 0

c['inputs']['GREENHOUSE_SLOPE_MULTIPLIER'] = 1  #default values from greenhouse paper
c['inputs']['INDUSTRIAL_FOODS_SLOPE_MULTIPLIER'] = 1  #default values from CS paper

c['inputs']['INITIAL_HARVEST_DURATION'] = 7  # months

c['inputs']['IS_NUCLEAR_WINTER'] = True
c['inputs']['FLUCTUATION_LIMIT'] = 1.5
c['inputs']['KCAL_SMOOTHING'] = False
c['inputs']['MEAT_SMOOTHING'] = True
c['inputs']['STORED_FOOD_SMOOTHING'] = True

c['inputs']['ADD_CELLULOSIC_SUGAR'] = False
c['inputs']['ADD_DAIRY'] = True
c['inputs']['ADD_FISH'] = True
c['inputs']['ADD_GREENHOUSES'] = False
c['inputs']['ADD_OUTDOOR_GROWING'] = True
c['inputs']['ADD_MEAT'] = True
c['inputs']['ADD_METHANE_SCP'] = False
c['inputs']['ADD_SEAWEED'] = False
c['inputs']['ADD_STORED_FOOD'] = True

c["inputs"]["EXCESS_CALORIES"] = np.array([0] * c['inputs']['NMONTHS'])
c['inputs']["DELAY"] = {}
c['inputs']["DELAY"]['FEED_SHUTOFF'] = 0  # months
c['inputs']["DELAY"]['BIOFUEL_SHUTOFF'] = 0  # months

c["inputs"]["CULL_DURATION"] = 12

c['inputs']['WASTE'] = {}
# c['inputs']['WASTE']['CEREALS'] = 0  # %
c['inputs']['WASTE']['SUGAR'] = 0  # %
c['inputs']['WASTE']['MEAT'] = 0  # %
c['inputs']['WASTE']['DAIRY'] = 0  # %
c['inputs']['WASTE']['SEAFOOD'] = 0  # %
c['inputs']['WASTE']['CROPS'] = 0  # %
c['inputs']['WASTE']['SEAWEED'] = 0  # %

optimizer = Optimizer()
[time_months, time_months_middle, analysis] = optimizer.optimize(c)

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

Plotter.plot_people_fed_combined(time_months_middle, analysis)
Plotter.plot_people_fed_kcals(time_months_middle, analysis, \
    'Primary production before waste, no resilient foods')

# nuclear winter 150 tab, cell G30-G38  https://docs.google.com/spreadsheets/d/14t3_PUIky6aNiBvw8q24sj6QYxCN9s_VddLY2-eJuPE/edit#gid=1637082097
#overall waste, on farm+distribution+retail
#2x prices (note, currently set to 2019, not 2020)
c['inputs']['WASTE'] = {}
# c['inputs']['WASTE']['CEREALS'] = 14.46  # %
c['inputs']['WASTE']['SUGAR'] = 9.91  # %
c['inputs']['WASTE']['MEAT'] = 10.61  # %
c['inputs']['WASTE']['DAIRY'] = 11.93  # %
c['inputs']['WASTE']['SEAFOOD'] = 9.99  # %
c['inputs']['WASTE']['CROPS'] = 14.78  # %
c['inputs']['WASTE']['SEAWEED'] = 9.81  # %

c["inputs"]["EXCESS_CALORIES"] = np.array([0] * c['inputs']['NMONTHS'])
c['inputs']['FEED_SHUTOFF_DELAY'] = 3  # months
c['inputs']['BIOFUEL_SHUTOFF_DELAY'] = 2  # months

c["inputs"]["CULL_DURATION"] = 3
c['inputs']['RECALCULATE_CULL_DURATION'] = False  # thousand tons

[time_months, time_months_middle, analysis] = optimizer.optimize(c)

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

if(c['inputs']['ADD_OUTDOOR_GROWING']):
    Plotter.plot_OG_no_resilient_foods(time_months_middle, analysis)

Plotter.plot_people_fed_combined(time_months_middle, analysis)
Plotter.plot_people_fed_kcals(time_months_middle, analysis, "Food minus waste & delayed halt \nof nonhuman consumption, no resilient foods")