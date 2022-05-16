# this program runs the optimizer model, and ensures that all the results are
# reasonable using a couple useful checks to make sure there's nothing wacky
# going on:

# 1) check that as time increases, more people can be fed

# 2) check that stored food plus meat is always used at the
# highest rate during the largest food shortage.

from datetime import datetime
import numpy as np
import os
import sys
import copy
module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)
from src.plotter import Plotter
from src.optimizer import Optimizer

constants = {}
constants['CHECK_CONSTRAINTS'] = False

inputs_to_optimizer = {}

inputs_to_optimizer['NMONTHS'] = 84
inputs_to_optimizer['LIMIT_SEAWEED_AS_PERCENT_KCALS'] = True

inputs_to_optimizer['NUTRITION'] = {}
inputs_to_optimizer['NUTRITION']['KCALS_DAILY'] = 2100  # kcals per person per day
inputs_to_optimizer['NUTRITION']['FAT_DAILY'] = 47  # 35 #grams per person per day
inputs_to_optimizer['NUTRITION']['PROTEIN_DAILY'] = 51  # 46 #grams per person per day

inputs_to_optimizer['MAX_SEAWEED_AS_PERCENT_KCALS'] = 10
inputs_to_optimizer['SEAWEED_NEW_AREA_PER_DAY'] = 2.0765  # 1000 km^2 (seaweed)
inputs_to_optimizer['SEAWEED_PRODUCTION_RATE'] = 10  # percent (seaweed)

# "Outputs" https://docs.google.com/spreadsheets/d/19kzHpux690JTCo2IX2UA1faAd7R1QcBK/edit#gid=1815939673 cell G12-G14
inputs_to_optimizer['TONS_DRY_CALORIC_EQIVALENT_SF'] = 1360e6 * 0.96
# these fat and protein ratios do not produce realistic outputs in before resilient food case, so outdoor growing ratios were used instead
inputs_to_optimizer['INITIAL_SF_FAT'] = 166.07e3 * 0.96
inputs_to_optimizer['INITIAL_SF_PROTEIN'] = 69.25e3 * 0.96

inputs_to_optimizer["OG_USE_BETTER_ROTATION"] = True
inputs_to_optimizer["ROTATION_IMPROVEMENTS"] = {}
inputs_to_optimizer["ROTATION_IMPROVEMENTS"]["KCALS_REDUCTION"] = .93
inputs_to_optimizer["ROTATION_IMPROVEMENTS"]["FAT_RATIO"] = 1.487
inputs_to_optimizer["ROTATION_IMPROVEMENTS"]["PROTEIN_RATIO"] = 1.108

inputs_to_optimizer['INCLUDE_PROTEIN'] = True
inputs_to_optimizer['INCLUDE_FAT'] = True

inputs_to_optimizer['GREENHOUSE_GAIN_PCT'] = 50

# half values from greenhouse paper due to higher cost
inputs_to_optimizer['GREENHOUSE_AREA_MULTIPLIER'] = 1/2
inputs_to_optimizer['INDUSTRIAL_FOODS_SLOPE_MULTIPLIER'] = 1  # default values from CS and SCP papers


inputs_to_optimizer['INITIAL_HARVEST_DURATION_IN_MONTHS'] = 7 + 1

inputs_to_optimizer['IS_NUCLEAR_WINTER'] = True
inputs_to_optimizer['FLUCTUATION_LIMIT'] = 1.5
inputs_to_optimizer['KCAL_SMOOTHING'] = True
inputs_to_optimizer['MEAT_SMOOTHING'] = True
inputs_to_optimizer['STORED_FOOD_SMOOTHING'] = True

inputs_to_optimizer['ADD_CELLULOSIC_SUGAR'] = True
inputs_to_optimizer['ADD_DAIRY'] = True
inputs_to_optimizer['ADD_FISH'] = True
inputs_to_optimizer['ADD_GREENHOUSES'] = True
inputs_to_optimizer['ADD_OUTDOOR_GROWING'] = True
inputs_to_optimizer['ADD_MEAT'] = True
inputs_to_optimizer['ADD_METHANE_SCP'] = True
inputs_to_optimizer['ADD_SEAWEED'] = True
inputs_to_optimizer['ADD_STORED_FOOD'] = True

inputs_to_optimizer["EXCESS_CALORIES"] = np.array([0] * inputs_to_optimizer['NMONTHS'])
inputs_to_optimizer["DELAY"] = {}
inputs_to_optimizer["DELAY"]['ROTATION_CHANGE_IN_MONTHS'] = 2
inputs_to_optimizer["DELAY"]['INDUSTRIAL_FOODS_MONTHS'] = 3
inputs_to_optimizer["DELAY"]['GREENHOUSE_MONTHS'] = 2
inputs_to_optimizer["DELAY"]['SEAWEED_MONTHS'] = 1
inputs_to_optimizer["DELAY"]['FEED_SHUTOFF_MONTHS'] = 0
inputs_to_optimizer["DELAY"]['BIOFUEL_SHUTOFF_MONTHS'] = 0

inputs_to_optimizer["CULL_DURATION_MONTHS"] = 60

inputs_to_optimizer['WASTE'] = {}
# inputs_to_optimizer['WASTE']['CEREALS'] = 0 #%
inputs_to_optimizer['WASTE']['SUGAR'] = 0  # %
inputs_to_optimizer['WASTE']['MEAT'] = 0  # %
inputs_to_optimizer['WASTE']['DAIRY'] = 0  # %
inputs_to_optimizer['WASTE']['SEAFOOD'] = 0  # %
inputs_to_optimizer['WASTE']['CROPS'] = 0  # %
inputs_to_optimizer['WASTE']['SEAWEED'] = 0  # %

optimizer = Optimizer()
constants['inputs'] = inputs_to_optimizer
constants_for_optimizer = copy.deepcopy(constants)
[time_months, time_months_middle, analysis] = optimizer.optimize(constants_for_optimizer)
print("")
print("no waste estimated people fed (kcals/capita/day)")
print(analysis.people_fed_billions/7.8*2100)
print("")

np.save('../data/resilient_food_primary_analysis.npy',
        analysis,
        allow_pickle=True)

inputs_to_optimizer['WASTE'] = {}
# inputs_to_optimizer['WASTE']['CEREALS'] = 19.02 #%
inputs_to_optimizer['WASTE']['SUGAR'] = 14.47  # %
inputs_to_optimizer['WASTE']['MEAT'] = 15.17  # %
inputs_to_optimizer['WASTE']['DAIRY'] = 16.49  # %
inputs_to_optimizer['WASTE']['SEAFOOD'] = 14.55  # %
inputs_to_optimizer['WASTE']['CROPS'] = 19.33  # %
inputs_to_optimizer['WASTE']['SEAWEED'] = 14.37  # %

excess_per_month = np.array([0] * inputs_to_optimizer['NMONTHS'])
inputs_to_optimizer["EXCESS_CALORIES"] = excess_per_month
inputs_to_optimizer["DELAY"]['FEED_SHUTOFF_MONTHS'] = 2
inputs_to_optimizer["DELAY"]['BIOFUEL_SHUTOFF_MONTHS'] = 1

inputs_to_optimizer["CULL_DURATION_MONTHS"] = 60

optimizer = Optimizer()
constants['inputs'] = inputs_to_optimizer
constants_for_optimizer = copy.deepcopy(constants)
[time_months, time_months_middle, analysis] = optimizer.optimize(constants_for_optimizer)

analysis1 = analysis
print("Food available after waste, feed ramp down and biofuel ramp down, with resilient foods (kcals per capita per day)")
print(analysis.people_fed_billions/7.8*2100)
print("")

# billions of kcals
# "Sources/summary" tab cell I14.  https://docs.google.com/spreadsheets/d/1tLFHJpXTStxyfNojP_Wrj0MQowfyKujJUA37ZG1q6pk/edit#gid=0

inputs_to_optimizer['INCLUDE_PROTEIN'] = True
inputs_to_optimizer['INCLUDE_FAT'] = True
# Plotter.plot_people_fed_combined(analysis)
# Plotter.plot_people_fed_kcals(analysis,
#                               'People fed minus waste and biofuels',
#                               84)

constants['inputs'] = inputs_to_optimizer
constants_for_optimizer = copy.deepcopy(constants)
[time_months, time_months_middle, analysis] = optimizer.optimize(constants_for_optimizer)

# Plotter.plot_people_fed_combined(time_months_middle, analysis)
# Plotter.plot_people_fed_kcals(time_months_middle, analysis,
                              # "Food available after waste, feed ramp down \n and biofuel ramp down, + resilient foods",72)

# Plotter.plot_people_fed_combined(time_months_middle, analysis)

people_fed = analysis.people_fed_billions  # np.min(analysis.people_fed)
feed_delay = inputs_to_optimizer["DELAY"]['FEED_SHUTOFF_MONTHS']

# these months are used to estimate the diet before the full scale-up of resilient foods makes there be way too much food to make sense economically
N_MONTHS_TO_CALCULATE_DIET = 49

# don't try to feed more animals in the  months before feed shutoff

excess_per_month[feed_delay:N_MONTHS_TO_CALCULATE_DIET] = \
    excess_per_month[feed_delay:N_MONTHS_TO_CALCULATE_DIET]\
    + analysis.excess_after_run[feed_delay:N_MONTHS_TO_CALCULATE_DIET]
# =================
tstart = datetime.now()
n = 0
print("Calculating 2100 calorie diet, excess feed to animals")
# people_fed = 0
while(True):

    # billions of kcals
    inputs_to_optimizer["DELAY"]['FEED_SHUTOFF_MONTHS'] = 2
    inputs_to_optimizer["DELAY"]['BIOFUEL_SHUTOFF_MONTHS'] = 1
    # "Sources/summary" tab cell I14.  https://docs.google.com/spreadsheets/d/1tLFHJpXTStxyfNojP_Wrj0MQowfyKujJUA37ZG1q6pk/edit#gid=0

    inputs_to_optimizer["CULL_DURATION_MONTHS"] = 60

    constants['inputs'] = inputs_to_optimizer
    [time_months, time_months_middle, analysis] = optimizer.optimize(constants)
    people_fed = analysis.people_fed_billions  # np.min(analysis.people_fed)
    
    # the rebalancer is only responsible for balancing calories, and is unable to operate unless the assumption that fat and protein are limiting values is invalid.
    inputs_to_optimizer['INCLUDE_PROTEIN'] = True
    inputs_to_optimizer['INCLUDE_FAT'] = True

    feed_delay = inputs_to_optimizer["DELAY"]['FEED_SHUTOFF_MONTHS']

    if(people_fed > 7.79 and people_fed < 7.81):
        break

    assert(feed_delay > inputs_to_optimizer["DELAY"]['BIOFUEL_SHUTOFF_MONTHS'])

    # rapidly feed more to people until it's close to 2100 kcals, then
    # slowly feed more to people 
    if(people_fed < 8.0 and people_fed > 7.8):
        excess_per_month[feed_delay:N_MONTHS_TO_CALCULATE_DIET] = \
            excess_per_month[feed_delay:N_MONTHS_TO_CALCULATE_DIET]\
            + np.linspace(200, 500, N_MONTHS_TO_CALCULATE_DIET - feed_delay)
    else:
        excess_per_month[feed_delay:N_MONTHS_TO_CALCULATE_DIET] = \
            excess_per_month[feed_delay:N_MONTHS_TO_CALCULATE_DIET]\
            + np.linspace(5000, 5000, N_MONTHS_TO_CALCULATE_DIET - feed_delay)

    n = n + 1

tend = datetime.now()
diff = tend - tstart

analysis2 = analysis

# last month plotted is month 48
Plotter.plot_fig_2abcd(analysis1, analysis2, 48)
print("Diet computation complete")
