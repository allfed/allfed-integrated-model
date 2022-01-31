"""
 this program runs the worst case and best case plausibly likely outcomes for 
 the monte carlo model, and prints the outcomes for 1000 runs in a row, then 
 plots a histogram of the results
"""

from datetime import datetime
from matplotlib.ticker import MaxNLocator
import matplotlib.pyplot as plt
import random
import itertools
import numpy as np
import os
import sys
module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)
from src.optimizer import Optimizer
from src.plotter import Plotter
import matplotlib
matplotlib.use('Svg')


c = {}
c['inputs'] = {}

c['inputs']['NMONTHS'] = 84
c['inputs']['LIMIT_SEAWEED_AS_PERCENT_KCALS'] = True

c['inputs']['NUTRITION'] = {
    'FAT_DAILY': 47, 'KCALS_DAILY': 2100, 'PROTEIN_DAILY': 51}

c['inputs']['INITIAL_SF_FAT'] = 166.07e3 * 0.96
c['inputs']['INITIAL_SF_PROTEIN'] = 69.25e3 * 0.96

c['inputs']['MAX_SEAWEED_AS_PERCENT_KCALS'] = 10
c['inputs']['NEW_AREA_PER_DAY'] = 2.0765 / 2  # 1000 km^2 (seaweed)
c['inputs']['SEAWEED_PRODUCTION_RATE'] = 10  # percent (seaweed)

# "Outputs" https://docs.google.com/spreadsheets/d/19kzHpux690JTCo2IX2UA1faAd7R1QcBK/edit#gid=1815939673 cell G12-G14
c['inputs']['TONS_DRY_CALORIC_EQIVALENT_SF'] = 1360e6
c["inputs"]["OG_USE_BETTER_ROTATION"] = True
c['inputs']['INCLUDE_PROTEIN'] = True
c['inputs']['INCLUDE_FAT'] = True
c['inputs']['WASTE'] = {}
c['inputs']['WASTE']['SUGAR'] = 14.47  # %
c['inputs']['WASTE']['MEAT'] = 15.17  # %
c['inputs']['WASTE']['DAIRY'] = 16.49  # %
c['inputs']['WASTE']['SEAFOOD'] = 14.55  # %
c['inputs']['WASTE']['CROPS'] = 19.33  # %
c['inputs']['WASTE']['SEAWEED'] = 14.37  # %
c["inputs"]["CULL_DURATION"] = 12  # analysis.c["CULL_DURATION"]
c['inputs']['RECALCULATE_CULL_DURATION'] = False  # thousand tons

c['inputs']['IS_NUCLEAR_WINTER'] = True
excess_per_month = np.array([0] * c['inputs']['NMONTHS'])
c["inputs"]["EXCESS_CALORIES"] = excess_per_month


optimizer = Optimizer()

c['inputs']['ADD_FISH'] = True
c['inputs']['ADD_SEAWEED'] = True
c['inputs']['ADD_CELLULOSIC_SUGAR'] = True
c['inputs']['ADD_METHANE_SCP'] = True
c['inputs']['ADD_GREENHOUSES'] = True
c['inputs']['ADD_DAIRY'] = True
c['inputs']['ADD_STORED_FOOD'] = True
c['inputs']['ADD_MEAT'] = True
c['inputs']['ADD_OUTDOOR_GROWING'] = True
c['inputs']['INITIAL_HARVEST_DURATION'] = 7 + 1  # months
c['inputs']['STORED_FOOD_SMOOTHING'] = False
c['inputs']['KCAL_SMOOTHING'] = False
c['inputs']['MEAT_SMOOTHING'] = False

c['CHECK_CONSTRAINTS'] = False

nsamples = 100
# all_fed = stats.norm.rvs(size=nsamples)


def monte_carlo():

    variables = {}

    variables['MAX_SEAWEED_AS_PERCENT_KCALS'] = [5,7.5,10,20,30]
    variables['SEAWEED_PRODUCTION_RATE'] = [5, 7.5, 10, 12.5, 15]
    variables['SEAWEED_NEW_AREA'] = [2.0765 / 2, 2.0765, 2.0765 * 2]
    variables['GREENHOUSE_GAIN_PCT'] = [50 / 2, 50, 50 * 2]
    variables['GREENHOUSE_AREA_MULTIPLIER'] = [1 / 4, 1 / 2, 1]
    variables['INDUSTRIAL_FOODS_SLOPE_MULTIPLIER'] = [0.6, .8, 1, 1.2, 1.4]
    variables["DELAY"] = [
        {
            "SEAWEED": 2,
            'INDUSTRIAL_FOODS': 6,
            'GREENHOUSE': 4,
            'FEED_SHUTOFF': 4,
            'BIOFUEL_SHUTOFF': 2,
            'ROTATION_CHANGE': 4
        },
        {
            "SEAWEED": 1,
            'INDUSTRIAL_FOODS': 4,
            'GREENHOUSE': 3,
            'FEED_SHUTOFF': 3,
            'BIOFUEL_SHUTOFF': 1,
            'ROTATION_CHANGE': 3
        },
        {
            "SEAWEED": 1,
            'INDUSTRIAL_FOODS': 3,
            'GREENHOUSE': 2,
            'FEED_SHUTOFF': 2,
            'BIOFUEL_SHUTOFF': 1,
            'ROTATION_CHANGE': 2
        },
        {
            "SEAWEED": 0,
            'INDUSTRIAL_FOODS': 1,
            'GREENHOUSE': 1,
            'FEED_SHUTOFF': 1,
            'BIOFUEL_SHUTOFF': 0,
            'ROTATION_CHANGE': 1
        }
    ]

    variables["ROTATION_IMPROVEMENTS"] = \
        [
        {
            "KCALS_REDUCTION": .822,
            "FAT_RATIO": 1.746,
            "PROTEIN_RATIO": 1.063
        },
        {
            "KCALS_REDUCTION": .808,
            "FAT_RATIO": 1.861,
            "PROTEIN_RATIO": 1.062
        },
        {
            "KCALS_REDUCTION": .799,
            "FAT_RATIO": 1.928,
            "PROTEIN_RATIO": 1.067
        }
    ]
    nsamples = 1000

    # worst plausibly likely variables all in one case
    sample_c = c
    for i in variables.items():
        sample_c["inputs"][i[0]] = i[1][0]
    print("")
    print("worst case: ")
    tstart = datetime.now()
    [time_months, time_months_middle, analysis] = optimizer.optimize(sample_c)
    tend = datetime.now()
    diff = tend - tstart
    print("seconds worst case")
    print(diff.seconds)
    print("microseconds worst case")
    print(diff.microseconds)

    # best plausibly likely variables all in one case
    for i in variables.items():
        sample_c["inputs"][i[0]] = i[1][-1]
    print("")
    print("best case: ")
    tstart = datetime.now()
    [time_months, time_months_middle, analysis] = optimizer.optimize(sample_c)
    tend = datetime.now()
    diff = tend - tstart
    print("seconds best case")
    print(diff.seconds)
    print("microseconds best case")
    print(diff.microseconds)

    input("Press enter to continue")
    all_vars = list(variables.values())
    all_keys = [list(variables.keys())] * nsamples
    all_combos = list(itertools.product(*all_vars))
    random_sample = random.sample(all_combos, nsamples)
    sample_c = c

    all_fed = []
    for i in range(0, len(random_sample)):

        s = random_sample[i]
        keylist = all_keys[i]
        for j in range(0, len(keylist)):
            key = keylist[j]
            value = s[j]

            sample_c['inputs'][key] = value

        [time_months, time_months_middle, analysis] = \
            optimizer.optimize(sample_c)
        # Plotter.plot_people_fed_combined(time_months_middle, analysis)
        # Plotter.plot_people_fed_kcals(time_months_middle, analysis,
        #         'People fed minus waste and biofuels')

        all_fed.append(analysis.people_fed_billions)

    # https://stackoverflow.com/questions/61940618/how-do-i-draw-a-histogram-for-a-normal-distribution-using-python-matplotlib
    # plt.scatter(all_fed,all_fed)
    # https://stackoverflow.com/questions/12050393/how-to-force-the-y-axis-to-only-use-integers-in-matplotlib

    num_bins = int(nsamples / 5)
    plt.hist(all_fed, bins=num_bins, facecolor='blue', alpha=0.5)
    plt.title("Food Available After Delayed Shutoff and Waste ")
    plt.xlabel("Maximum people fed, billions")
    plt.ylabel("Number of Scenarios")
    ax = plt.gca()
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))

    plt.rcParams["figure.figsize"] = [17.50, 9]
    # plt.tight_layout()
    plt.savefig("plot.svg")
    os.system('xdg-open plot.svg')
    # plt.show()


monte_carlo()
