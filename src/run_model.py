# this program runs the optimizer model, and ensures that all the results are
# reasonable using a couple useful checks to make sure there's nothing wacky
# going on.

# check that as time increases, more people can be fed

# check that stored food plus meat is always used at the
# highest rate during the largest food shortage.

from datetime import datetime
import numpy as np
import os
import sys
module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)
from src.plotter import Plotter
from src.optimizer import Optimizer
constants = {}
constants['CHECK_CONSTRAINTS'] = False

cin = {}

cin['NMONTHS'] = 84
cin['LIMIT_SEAWEED_AS_PERCENT_KCALS'] = True

cin['NUTRITION'] = {}
cin['NUTRITION']['KCALS_DAILY'] = 2100  # kcals per person per day
cin['NUTRITION']['FAT_DAILY'] = 47  # 35 #grams per person per day
cin['NUTRITION']['PROTEIN_DAILY'] = 51  # 46 #grams per person per day

cin['MAX_SEAWEED_AS_PERCENT_KCALS'] = 10
cin['SEAWEED_NEW_AREA_PER_DAY'] = 2.0765  # 1000 km^2 (seaweed)
cin['SEAWEED_PRODUCTION_RATE'] = 10  # percent (seaweed)

# "Outputs" https://docs.google.com/spreadsheets/d/19kzHpux690JTCo2IX2UA1faAd7R1QcBK/edit#gid=1815939673 cell G12-G14
cin['TONS_DRY_CALORIC_EQIVALENT_SF'] = 1360e6 * 0.96
# these fat and protein ratios do not produce realistic outputs in before resilient food case, so outdoor growing ratios were used instead
cin['INITIAL_SF_FAT'] = 166.07e3 * 0.96
cin['INITIAL_SF_PROTEIN'] = 69.25e3 * 0.96

cin["OG_USE_BETTER_ROTATION"] = True
cin["ROTATION_IMPROVEMENTS"] = {}
cin["ROTATION_IMPROVEMENTS"]["KCALS_REDUCTION"] = .808
cin["ROTATION_IMPROVEMENTS"]["FAT_RATIO"] = 1.861
cin["ROTATION_IMPROVEMENTS"]["PROTEIN_RATIO"] = 1.062

cin['INCLUDE_PROTEIN'] = True
cin['INCLUDE_FAT'] = True

cin['GREENHOUSE_GAIN_PCT'] = 50

# half values from greenhouse paper due to higher cost
cin['GREENHOUSE_AREA_MULTIPLIER'] = 1/2
cin['INDUSTRIAL_FOODS_SLOPE_MULTIPLIER'] = 1  # default values from CS and SCP papers


cin['INITIAL_HARVEST_DURATION'] = 7 + 1  # months

cin['IS_NUCLEAR_WINTER'] = True
cin['FLUCTUATION_LIMIT'] = 1.1
cin['KCAL_SMOOTHING'] = True
cin['MEAT_SMOOTHING'] = True
cin['STORED_FOOD_SMOOTHING'] = True

cin['ADD_CELLULOSIC_SUGAR'] = True
cin['ADD_DAIRY'] = True
cin['ADD_FISH'] = True
cin['ADD_GREENHOUSES'] = True
cin['ADD_OUTDOOR_GROWING'] = True
cin['ADD_MEAT'] = True
cin['ADD_METHANE_SCP'] = True
cin['ADD_SEAWEED'] = True
cin['ADD_STORED_FOOD'] = True

cin["EXCESS_CALORIES"] = np.array([0] * cin['NMONTHS'])
cin["DELAY"] = {}
cin["DELAY"]['ROTATION_CHANGE'] = 2  # months
cin["DELAY"]['INDUSTRIAL_FOODS'] = 3  # months
cin["DELAY"]['GREENHOUSE'] = 2  # months
cin["DELAY"]['SEAWEED'] = 1  # months
cin["DELAY"]['FEED_SHUTOFF'] = 0  # months
cin["DELAY"]['BIOFUEL_SHUTOFF'] = 0  # months

cin["CULL_DURATION"] = 0

cin['WASTE'] = {}
# cin['WASTE']['CEREALS'] = 0 #%
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

# Plotter.plot_people_fed_combined(time_months_middle, analysis)
Plotter.plot_people_fed_kcals(time_months_middle, analysis,
        'Primary production before waste, + resilient foods', 79)

# nuclear winter 150 tab, cell G30-G38  https://docs.google.com/spreadsheets/d/14t3_PUIky6aNiBvw8q24sj6QYxCN9s_VddLY2-eJuPE/edit#gid=1637082097
# overall waste, on farm+distribution+retail
# 3x prices (note, currently set to 2019, not 2020)
cin['WASTE'] = {}
# cin['WASTE']['CEREALS'] = 19.02 #%
cin['WASTE']['SUGAR'] = 14.47  # %
cin['WASTE']['MEAT'] = 15.17  # %
cin['WASTE']['DAIRY'] = 16.49  # %
cin['WASTE']['SEAFOOD'] = 14.55  # %
cin['WASTE']['CROPS'] = 19.33  # %
cin['WASTE']['SEAWEED'] = 14.37  # %

excess_per_month = np.array([0] * cin['NMONTHS'])
cin["EXCESS_CALORIES"] = excess_per_month
cin["DELAY"]['FEED_SHUTOFF'] = 2  # months
cin["DELAY"]['BIOFUEL_SHUTOFF'] = 1  # months

cin["CULL_DURATION"] = cin['NMONTHS'] - cin["DELAY"]['FEED_SHUTOFF']

optimizer = Optimizer()
constants['inputs'] = cin
[time_months, time_months_middle, analysis] = optimizer.optimize(constants)

# Plotter.plot_people_fed_combined(time_months_middle, analysis)
Plotter.plot_people_fed_kcals(time_months_middle, analysis,
                              "Food available after waste, feed ramp down \n and biofuel ramp down, + resilient foods",48)
print("")
print("")
print("")
print("")
print("")
print("")
print("==========Running diet balancer=========")
print("")
print("")
print("")

# billions of kcals
# "Sources/summary" tab cell I14.  https://docs.google.com/spreadsheets/d/1tLFHJpXTStxyfNojP_Wrj0MQowfyKujJUA37ZG1q6pk/edit#gid=0

cin['INCLUDE_PROTEIN'] = True
cin['INCLUDE_FAT'] = True

constants['inputs'] = cin
[time_months, time_months_middle, analysis] = optimizer.optimize(constants)

# Plotter.plot_people_fed_combined(time_months_middle, analysis)

people_fed = analysis.people_fed_billions  # np.min(analysis.people_fed)
print("")
print("")
print("")
print("")
print("billions of people fed from kcals")
print(people_fed)
print("")
print("")
print("")
print("")

feed_delay = cin["DELAY"]['FEED_SHUTOFF']

# these months are used to estimate the diet before the full scale-up of resilient foods makes there be way too much food to make sense economically
N_MONTHS_TO_CALCULATE_DIET = 49

# don't try to feed more animals in the  months before feed shutoff

excess_per_month[feed_delay:N_MONTHS_TO_CALCULATE_DIET] = \
    excess_per_month[feed_delay:N_MONTHS_TO_CALCULATE_DIET]\
    + analysis.excess_after_run[feed_delay:N_MONTHS_TO_CALCULATE_DIET]

# =================
tstart = datetime.now()
n = 0
# people_fed = 0
while(True):
    import matplotlib.pyplot as plt
    # plt.plot(excess_per_month*1e9/4e6/1e6)
    # plt.show()
    # Plotter.plot_people_fed_combined(time_months_middle,analysis)
    # Plotter.plot_people_fed_kcals(time_months_middle,analysis,"dumb stuff")

    # import matplotlib.pyplot as plt
    # # print("excess_per_month")
    # # print(excess_per_month)
    # plt.plot(excess_per_month)
    # plt.show()

    # billions of kcals
    cin["DELAY"]['FEED_SHUTOFF'] = 2  # months
    cin["DELAY"]['BIOFUEL_SHUTOFF'] = 1  # months
    # "Sources/summary" tab cell I14.  https://docs.google.com/spreadsheets/d/1tLFHJpXTStxyfNojP_Wrj0MQowfyKujJUA37ZG1q6pk/edit#gid=0

    cin["CULL_DURATION"] =cin['NMONTHS'] - cin["DELAY"]['FEED_SHUTOFF']

    constants['inputs'] = cin
    [time_months, time_months_middle, analysis] = optimizer.optimize(constants)
    people_fed = analysis.people_fed_billions  # np.min(analysis.people_fed)

    print("")
    print("")
    print("")
    print("")
    print("people_fed")
    print(people_fed)
    print("")
    print("")
    print("")
    print("")

    # the rebalancer is only responsible for balancing calories, and is unable to operate unless the assumption that fat and protein are limiting values is invalid.
    cin['INCLUDE_PROTEIN'] = True
    cin['INCLUDE_FAT'] = True

    feed_delay = cin["DELAY"]['FEED_SHUTOFF']

    if(people_fed > 7.79 and people_fed < 7.81):
        break

    assert(feed_delay > cin["DELAY"]['BIOFUEL_SHUTOFF'])

    # don't try to feed more animals in the  months before feed shutoff
    # excess_per_month[feed_delay:N_MONTHS_TO_CALCULATE_DIET] = \
    #   excess_per_month[feed_delay:N_MONTHS_TO_CALCULATE_DIET]\
    #   + analysis.excess_after_run[feed_delay:N_MONTHS_TO_CALCULATE_DIET]
    if(people_fed < 8.0 and people_fed > 7.8):
        excess_per_month[feed_delay:N_MONTHS_TO_CALCULATE_DIET] = \
            excess_per_month[feed_delay:N_MONTHS_TO_CALCULATE_DIET]\
            + np.linspace(200, 500, N_MONTHS_TO_CALCULATE_DIET - feed_delay)
    else:
        excess_per_month[feed_delay:N_MONTHS_TO_CALCULATE_DIET] = \
            excess_per_month[feed_delay:N_MONTHS_TO_CALCULATE_DIET]\
            + np.linspace(5000, 5000, N_MONTHS_TO_CALCULATE_DIET - feed_delay)
        # /+ analysis.excess_after_run[feed_delay:N_MONTHS_TO_CALCULATE_DIET]

    print("excess_per_month")
    print(excess_per_month)
    # excess_per_month = excess_per_month+ analysis.excess_after_run

    # if(n>30):
    #   break
    n = n + 1

    # if(n==3):
    #   c['CHECK_CONSTRAINTS'] = True

tend = datetime.now()
diff = tend - tstart
print("duration seconds diet calculator")
print(diff.seconds)
print("duration microseconds diet calculator")
print(diff.microseconds)

plt.title("Excess kcals used for feed and biofuel")
plt.ylabel("million dry caloric tons monthly")
plt.xlabel("Months after May nuclear event")
plt.plot(np.array(optimizer.s["excess_kcals"]) * 1e9 / 4e6 / 1e6)
plt.show()
# Plotter.plot_people_fed_combined(time_months_middle, analysis)
Plotter.plot_people_fed_kcals(time_months_middle, analysis,
                              "Average diet, excess production used for feed, + resilient foods",48)
