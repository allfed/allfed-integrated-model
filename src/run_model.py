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
c = {}
c['CHECK_CONSTRAINTS'] = False

c['inputs'] = {}

c['inputs']['NMONTHS'] = 84
c['inputs']['LIMIT_SEAWEED_AS_PERCENT_KCALS'] = True

c['inputs']['NUTRITION'] = {}
c['inputs']['NUTRITION']['KCALS_DAILY'] = 2100  # kcals per person per day
c['inputs']['NUTRITION']['FAT_DAILY'] = 47  # 35 #grams per person per day
c['inputs']['NUTRITION']['PROTEIN_DAILY'] = 51  # 46 #grams per person per day

c['inputs']['MAX_SEAWEED_AS_PERCENT_KCALS'] = 10
c['inputs']['NEW_AREA_PER_DAY'] = 2.0765  # 1000 km^2 (seaweed)
c['inputs']['SEAWEED_PRODUCTION_RATE'] = 10  # percent (seaweed)

# "Outputs" https://docs.google.com/spreadsheets/d/19kzHpux690JTCo2IX2UA1faAd7R1QcBK/edit#gid=1815939673 cell G12-G14
c['inputs']['TONS_DRY_CALORIC_EQIVALENT_SF'] = 1360e6 * 0.96
# these fat and protein ratios do not produce realistic outputs in before resilient food case, so outdoor growing ratios were used instead
c['inputs']['INITIAL_SF_FAT'] = 166.07e3 * 0.96
c['inputs']['INITIAL_SF_PROTEIN'] = 69.25e3 * 0.96

c["inputs"]["OG_USE_BETTER_ROTATION"] = True
c["inputs"]["ROTATION_IMPROVEMENTS"] = {}
c["inputs"]["ROTATION_IMPROVEMENTS"]["KCALS_REDUCTION"] = .808
c["inputs"]["ROTATION_IMPROVEMENTS"]["FAT_RATIO"] = 1.861
c["inputs"]["ROTATION_IMPROVEMENTS"]["PROTEIN_RATIO"] = 1.062

c['inputs']['INCLUDE_PROTEIN'] = True
c['inputs']['INCLUDE_FAT'] = True

c['inputs']['GREENHOUSE_GAIN_PCT'] = 50

# half values from greenhouse paper due to higher cost
c['inputs']['GREENHOUSE_AREA_MULTIPLIER'] = 1/2
c['inputs']['INDUSTRIAL_FOODS_SLOPE_MULTIPLIER'] = 1  # default values from CS and SCP papers


c['inputs']['INITIAL_HARVEST_DURATION'] = 7 + 1  # months

c['inputs']['IS_NUCLEAR_WINTER'] = True
c['inputs']['FLUCTUATION_LIMIT'] = 1.1
c['inputs']['KCAL_SMOOTHING'] = True
c['inputs']['MEAT_SMOOTHING'] = True
c['inputs']['STORED_FOOD_SMOOTHING'] = True

c['inputs']['ADD_CELLULOSIC_SUGAR'] = True
c['inputs']['ADD_DAIRY'] = True
c['inputs']['ADD_FISH'] = True
c['inputs']['ADD_GREENHOUSES'] = True
c['inputs']['ADD_OUTDOOR_GROWING'] = True
c['inputs']['ADD_MEAT'] = True
c['inputs']['ADD_METHANE_SCP'] = True
c['inputs']['ADD_SEAWEED'] = True
c['inputs']['ADD_STORED_FOOD'] = True

c["inputs"]["EXCESS_CALORIES"] = np.array([0] * c['inputs']['NMONTHS'])
c['inputs']["DELAY"] = {}
c['inputs']["DELAY"]['ROTATION_CHANGE'] = 2  # months
c['inputs']["DELAY"]['INDUSTRIAL_FOODS'] = 3  # months
c['inputs']["DELAY"]['GREENHOUSE'] = 2  # months
c['inputs']["DELAY"]['SEAWEED'] = 1  # months
c['inputs']["DELAY"]['FEED_SHUTOFF'] = 0  # months
c['inputs']["DELAY"]['BIOFUEL_SHUTOFF'] = 0  # months

c["inputs"]["CULL_DURATION"] = 0

c['inputs']['WASTE'] = {}
# c['inputs']['WASTE']['CEREALS'] = 0 #%
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
Plotter.plot_people_fed_kcals(time_months_middle, analysis,
        'Primary production before waste, + resilient foods')

# nuclear winter 150 tab, cell G30-G38  https://docs.google.com/spreadsheets/d/14t3_PUIky6aNiBvw8q24sj6QYxCN9s_VddLY2-eJuPE/edit#gid=1637082097
# overall waste, on farm+distribution+retail
# 3x prices (note, currently set to 2019, not 2020)
c['inputs']['WASTE'] = {}
# c['inputs']['WASTE']['CEREALS'] = 19.02 #%
c['inputs']['WASTE']['SUGAR'] = 14.47  # %
c['inputs']['WASTE']['MEAT'] = 15.17  # %
c['inputs']['WASTE']['DAIRY'] = 16.49  # %
c['inputs']['WASTE']['SEAFOOD'] = 14.55  # %
c['inputs']['WASTE']['CROPS'] = 19.33  # %
c['inputs']['WASTE']['SEAWEED'] = 14.37  # %


excess_per_month = np.array([0] * c['inputs']['NMONTHS'])
c["inputs"]["EXCESS_CALORIES"] = excess_per_month
c['inputs']["DELAY"]['FEED_SHUTOFF'] = 2  # months
c['inputs']["DELAY"]['BIOFUEL_SHUTOFF`'] = 1  # months

c["inputs"]["CULL_DURATION"] = 12

optimizer = Optimizer()
[time_months, time_months_middle, analysis] = optimizer.optimize(c)
Plotter.plot_people_fed_combined(time_months_middle, analysis)
Plotter.plot_people_fed_kcals(time_months_middle, analysis,
                              "Food available after waste, feed ramp down \n and biofuel ramp down, + resilient foods")

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

c['inputs']['INCLUDE_PROTEIN'] = True
c['inputs']['INCLUDE_FAT'] = True


[time_months, time_months_middle, analysis] = optimizer.optimize(c)
Plotter.plot_people_fed_combined(time_months_middle, analysis)

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

feed_delay = c['inputs']["DELAY"]['FEED_SHUTOFF']

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
    c['inputs']["DELAY"]['FEED_SHUTOFF'] = 2  # months
    c['inputs']["DELAY"]['BIOFUEL_SHUTOFF'] = 1  # months
    # "Sources/summary" tab cell I14.  https://docs.google.com/spreadsheets/d/1tLFHJpXTStxyfNojP_Wrj0MQowfyKujJUA37ZG1q6pk/edit#gid=0

    c["inputs"]["CULL_DURATION"] = 12

    [time_months, time_months_middle, analysis] = optimizer.optimize(c)
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
    c['inputs']['INCLUDE_PROTEIN'] = True
    c['inputs']['INCLUDE_FAT'] = True

    feed_delay = c['inputs']["DELAY"]['FEED_SHUTOFF']

    if(people_fed > 7.79 and people_fed < 7.81):
        break

    assert(feed_delay > c['inputs']["DELAY"]['BIOFUEL_SHUTOFF'])

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
Plotter.plot_people_fed_combined(time_months_middle, analysis)
Plotter.plot_people_fed_kcals(time_months_middle, analysis,
                              "Average diet, excess production used for feed, + resilient foods")
