"""
 this program runs the worst case and best case plausibly likely outcomes for 
 the monte carlo model, and prints the outcomes for 1000 runs in a row, then 
 plots a histogram of the results
"""

from datetime import datetime
from matplotlib.ticker import MaxNLocator
import matplotlib
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

from scipy.stats import uniform
from scipy.stats import norm
from scipy.stats import lognorm
from scipy.stats import truncnorm
import statsmodels
import statsmodels.api as sm
import matplotlib.pyplot as plt

matplotlib.use('Svg')


cin = {}  # constants as inputs to optimizer

cin['NMONTHS'] = 84
cin['LIMIT_SEAWEED_AS_PERCENT_KCALS'] = True

cin['NUTRITION'] = {
    'FAT_DAILY': 47, 'KCALS_DAILY': 2100, 'PROTEIN_DAILY': 51}

cin['INITIAL_SF_FAT'] = 166.07e3 * 0.96
cin['INITIAL_SF_PROTEIN'] = 69.25e3 * 0.96


# "Outputs" https://docs.google.com/spreadsheets/d/19kzHpux690JTCo2IX2UA1faAd7R1QcBK/edit#gid=1815939673 cell G12-G14
cin['TONS_DRY_CALORIC_EQIVALENT_SF'] = 1360e6
cin["OG_USE_BETTER_ROTATION"] = True
cin['INCLUDE_PROTEIN'] = True
cin['INCLUDE_FAT'] = True
cin['WASTE'] = {}
cin['WASTE']['SUGAR'] = 14.47  # %
cin['WASTE']['MEAT'] = 15.17  # %
cin['WASTE']['DAIRY'] = 16.49  # %
cin['WASTE']['SEAFOOD'] = 14.55  # %
cin['WASTE']['CROPS'] = 19.33  # %
cin['WASTE']['SEAWEED'] = 14.37  # %
cin["CULL_DURATION"] = 12  # analysis.c["CULL_DURATION"]
cin['RECALCULATE_CULL_DURATION'] = False  # thousand tons

cin['IS_NUCLEAR_WINTER'] = True
excess_per_month = np.array([0] * cin['NMONTHS'])
cin["EXCESS_CALORIES"] = excess_per_month


optimizer = Optimizer()

cin['ADD_FISH'] = True
cin['ADD_SEAWEED'] = True
cin['ADD_CELLULOSIC_SUGAR'] = True
cin['ADD_METHANE_SCP'] = True
cin['ADD_GREENHOUSES'] = True
cin['ADD_DAIRY'] = True
cin['ADD_STORED_FOOD'] = True
cin['ADD_MEAT'] = True
cin['ADD_OUTDOOR_GROWING'] = True
cin['INITIAL_HARVEST_DURATION'] = 7 + 1  # months
cin['STORED_FOOD_SMOOTHING'] = False
cin['KCAL_SMOOTHING'] = False
cin['MEAT_SMOOTHING'] = False

def monte_carlo():

    variables = {}

    N = 1000  # number of scenarios simulated in the monte carlo
    # NOTE ON DISTRIBUTION PROBABILITIES
    # if r=norm.rvs(size=N,scale=np.log(M),loc=0),
    # for large N:
    #   len(r[np.exp(r)<=1/M])/N ~ len(r[np.exp(r)>=M])/N ~ 15.9%
    # because the occurrence of a multiplier higher than M happens
    # only (100%-68.2%)/2 = 15.9% of the time for a lognormal distribution
    # with an underlying normal distribution r
    # and with standard deviation log(M).

    # generate sets of independent variables for monte carlo

    M = 3  # 1 std probability of multiplier M or multiplier 1/M
    mean_value = 10  # this is e^(mean(underlying normal distribution))
    max_value = 100
    truncnormal_dist = truncnorm.rvs(
        -1e9,
        np.log(max_value) / np.log(mean_value),
        size=N,
        scale=np.log(M),
        loc=0
    )
    max_seaweed = np.exp(truncnormal_dist) * mean_value

    M = 2
    mean_value = 2.0765
    normal_dist = norm.rvs(size=N, scale=np.log(M), loc=0)
    seaweed_new = np.exp(normal_dist) * mean_value

    M = 2
    mean_value = 50
    normal_dist = norm.rvs(size=N, scale=np.log(M), loc=0)
    greenhouse_gain = np.exp(normal_dist) * mean_value

    one_standard_deviation = 5
    mean_value = 10
    min_value_std = -1  # min value in standard deviations from mean
    max_value_std = 3  # max value in standard deviations from mean
    seaweed_production_rate = truncnorm.rvs(
        min_value_std,
        max_value_std,
        size=N,
        scale=one_standard_deviation,
        loc=mean_value
    )

    M = 2
    mean_value = 1 / 2
    normal_dist = norm.rvs(size=N, scale=np.log(M), loc=0)
    greenhouse_area = np.exp(normal_dist) * mean_value

    M = 1.4
    mean_value = 1
    normal_dist = norm.rvs(size=N, scale=np.log(M), loc=0)
    industrial_foods = np.exp(normal_dist) * mean_value

    # delays are assumed to be perfectly correlated

    M = 2
    delay_normal_2 = norm.rvs(size=N, scale=np.log(M), loc=0)

    # round distributions
    delay_2 = np.exp(delay_normal_2)  # generate std of 2 data
    delay_3 = np.exp(delay_normal_2 * 1.5)  # generate std of 3 data

    # set the mean value (in months), and round to an integer
    industrial_foods_delay = (np.rint(delay_3 * 3)).astype(int)
    greenhouse_delay = (np.rint(delay_2 * 2)).astype(int)
    feed_shutoff_delay = (np.rint(delay_2 * 2)).astype(int)
    rotation_change_delay = (np.rint(delay_2 * 2)).astype(int)
    seaweed_delay = (np.rint(delay_2 * 1)).astype(int)
    biofuel_shutoff_delay = (np.rint(delay_2 * 1)).astype(int)

    M = 2
    mean_value = 10
    max_value = 20 # so 1/10th of this value rounds to 2
    truncnorm_dist = truncnorm.rvs(
        -1e9,
        np.log(max_value) / np.log(mean_value),
        size=N,
        scale=np.log(M),
        loc=0
    )

    # only 0, 1, or 2 allowed
    rotation_outcome = np.rint(
        np.exp(truncnorm_dist) * mean_value / 10).astype(int)

    #create histogram of inputs

    fig, axs = plt.subplots(2, 4, figsize=(10,7))

    Plotter.plot_histogram(axs[0,0], seaweed_production_rate, N, "seaweed growth per day\n (%)","number of scenarios","")
    Plotter.plot_histogram(axs[0,1], seaweed_new, N, "seaweed area built \n(1000s km^2/month)","number of scenarios","seaweed new area built monthly")
    Plotter.plot_histogram(axs[0,2], max_seaweed, N, "seaweed calories in diet \n (%)","number of scenarios","Seaweed percent dietary calories ")
    Plotter.plot_histogram(axs[0,3], rotation_outcome, 100, "rotation outcome\n 0=50% relocated\n1=80% relocated\n2=100% relocated","number of scenarios","")
    Plotter.plot_histogram(axs[1,0], greenhouse_gain, N, "greenhouse yield gain \n(%)","number of scenarios","gain (%)")
    Plotter.plot_histogram(axs[1,1], greenhouse_area, N, "greenhouse area scale factor","number of scenarios","seaweed new area built monthly")
    Plotter.plot_histogram(axs[1,2], industrial_foods, N, "industrial foods scale factor","number of scenarios","")
    Plotter.plot_histogram(axs[1,3], industrial_foods_delay, N, "delay industrial construction\n (months)","number of scenarios","months delayed starting")
    plt.tight_layout()
    plt.rcParams["figure.figsize"] = [12, 9]
    plt.savefig("plot.svg")
    os.system('xdg-open plot.svg')

    all_fed = []
    failed_to_optimize = 0
    for i in range(0, N):
        print("i")
        print(i)
        cin['MAX_SEAWEED_AS_PERCENT_KCALS'] = max_seaweed[i]
        cin['SEAWEED_PRODUCTION_RATE'] = seaweed_production_rate[i]
        cin['SEAWEED_NEW_AREA_PER_DAY'] = seaweed_new[i]
        cin['GREENHOUSE_GAIN_PCT'] = greenhouse_gain[i]
        cin['GREENHOUSE_AREA_MULTIPLIER'] = greenhouse_area[i]
        cin['INDUSTRIAL_FOODS_SLOPE_MULTIPLIER'] = industrial_foods[i]

        if(rotation_outcome[i] >= 2):
            cin['ROTATION_IMPROVEMENTS'] = {
                "KCALS_REDUCTION": .799,
                "FAT_RATIO": 1.928,
                "PROTEIN_RATIO": 1.067
            }
        elif(rotation_outcome[i] == 1):
            cin['ROTATION_IMPROVEMENTS'] = {
                "KCALS_REDUCTION": .808,
                "FAT_RATIO": 1.861,
                "PROTEIN_RATIO": 1.062
            }
        elif(rotation_outcome[i] == 0):
            cin['ROTATION_IMPROVEMENTS'] = {
                "KCALS_REDUCTION": .822,
                "FAT_RATIO": 1.746,
                "PROTEIN_RATIO": 1.063
            }
        cin["DELAY"] = {}
        cin["DELAY"]["INDUSTRIAL_FOODS"] = industrial_foods_delay[i]
        cin["DELAY"]["GREENHOUSE"] = greenhouse_delay[i]
        cin["DELAY"]["FEED_SHUTOFF"] = feed_shutoff_delay[i]
        cin["DELAY"]["ROTATION_CHANGE"] = rotation_change_delay[i]
        cin["DELAY"]["SEAWEED"] = seaweed_delay[i]
        cin["DELAY"]["BIOFUEL_SHUTOFF"] = biofuel_shutoff_delay[i]

        constants = {}
        constants['inputs'] = cin
        constants['CHECK_CONSTRAINTS'] = False
        try:
            [time_months, time_months_middle, analysis] = \
                optimizer.optimize(constants)
        except:
            print(cin)
            failed_to_optimize = failed_to_optimize + 1
            print("Warning: Optimization failed. Continuing.")
            continue


        PLOT_EACH_SCENARIO = False
        if(PLOT_EACH_SCENARIO):
            Plotter.plot_people_fed_combined(time_months_middle, analysis)
            Plotter.plot_people_fed_kcals(time_months_middle, analysis,
                'People fed minus waste and biofuels')

        fed = analysis.people_fed_billions
        if(np.isnan(fed)):
            failed_to_optimize = failed_to_optimize + 1
            print("Warning: Total people fed could not be calculated. Continuing.")
            continue
        # convert people fed to calories per capita in 2020
        all_fed.append(fed / 7.8 * 2100)

    title = "Monte Carlo results"
    xlabel = "kcals per capita per day"
    Plotter.plot_histogram_with_boxplot(
        all_fed,
        N,
        xlabel,
        title
    )

    print("number failed to optimize")
    print(failed_to_optimize)


monte_carlo()
