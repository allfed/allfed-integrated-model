"""
 this program runs the worst case and best case plausibly likely outcomes for 
 the monte carlo model, and prints the outcomes for 1000 runs in a row, then 
 plots a histogram of the results
"""

import matplotlib
import matplotlib.pyplot as plt
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

class MonteCarlo:
    def __init__(self):
        pass

    def run_all_scenarios():
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

        cin['ADD_SEAWEED'] = True
        cin['ADD_CELLULOSIC_SUGAR'] = True
        cin['ADD_METHANE_SCP'] = True
        cin['ADD_GREENHOUSES'] = True
        cin['ADD_STORED_FOOD'] = True
        cin['ADD_OUTDOOR_GROWING'] = True
        cin['ADD_MEAT'] = True
        cin['ADD_FISH'] = True
        cin['ADD_SEAWEED'] = True
        cin['ADD_CELLULOSIC_SUGAR'] = True
        cin['ADD_METHANE_SCP'] = True
        cin['ADD_GREENHOUSES'] = True
        cin['ADD_DAIRY'] = True
        cin['OG_USE_BETTER_ROTATION'] = True
        cin['INITIAL_HARVEST_DURATION'] = 8
        cin['STORED_FOOD_SMOOTHING'] = True
        cin['FLUCTUATION_LIMIT'] = 1.5
        cin['KCAL_SMOOTHING'] = False
        cin['MEAT_SMOOTHING'] = True
        cin['STORED_FOOD_SMOOTHING'] = True
        foods = ("methane SCP", "greenhouses", "cellulosic sugar", 'seaweed', "relocation")

        N = 1000  # number of scenarios simulated in the monte carlo

        #variables = MonteCarlo.get_variables(N,cin)

        #np.save('variables_1000.npy', variables, allow_pickle=True)
        variables = np.load('../reports/variables_1000.npy', allow_pickle=True).item()

        #all_fed = MonteCarlo.monte_carlo(variables, N, cin)
        #np.save('all_fed_1000.npy', all_fed, allow_pickle=True)
        all_fed = np.load('../reports/all_fed_10000.npy', allow_pickle=True)

        #removed, added = MonteCarlo.compare_resilient_foods(variables,
        #                                         N, cin, foods)
        #np.save('removed_1000.npy', removed, allow_pickle=True)
        removed = np.load('../reports/removed_1000.npy', allow_pickle=True).item()
        #np.save('added_1000.npy', added, allow_pickle=True)
        added = np.load('../reports/added_1000.npy', allow_pickle=True).item()

        Plotter.plot_fig_4ab(all_fed, N, foods, removed, added)

    def get_variables(N, cin):

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
        max_value = 80
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

        mean_value = 2  # this is e^(mean(underlying normal distribution))
        # set the max value so industrial foods delay doesn't exceed NMONTHS
        max_value = cin["NMONTHS"] / 2  # scaled by max 1.5, or min 1/2

        b = np.log((max_value - mean_value)/6)
        print(b)
        print(np.exp(b))
        delay_normal_2 = truncnorm.rvs(
            -1e9,
            b,
            size=N,
            loc=0
        )
        # round distributions
        delay_2 = np.exp(delay_normal_2)  # generate std of 2 data
        delay_3 = np.exp(delay_normal_2 * 1.5)  # generate std of 3 data

        # set the mean value (in months), and round to an integer
        industrial_foods_delay = (np.rint(delay_3 * 1.5)).astype(int)
        print(np.max(industrial_foods_delay))
        print(cin["NMONTHS"]/2*1.5)
        assert((industrial_foods_delay <= cin["NMONTHS"]/2*1.5+1).all())
        greenhouse_delay = (np.rint(delay_2)).astype(int)
        feed_shutoff_delay = (np.rint(delay_2)).astype(int)
        rotation_change_delay = (np.rint(delay_2)).astype(int)
        seaweed_delay = (np.rint(delay_2 / 2)).astype(int)
        biofuel_shutoff_delay = (np.rint(delay_2 / 2)).astype(int)

        M = 2
        mean_value = 10
        max_value = 20  # so 1/10th of this value rounds to 2
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

        variables = {}
        variables['seaweed_production_rate'] = seaweed_production_rate
        variables['seaweed_new'] = seaweed_new
        variables['max_seaweed'] = max_seaweed
        variables['rotation_outcome'] = rotation_outcome
        variables['greenhouse_gain'] = greenhouse_gain
        variables['greenhouse_area'] = greenhouse_area
        variables['industrial_foods'] = industrial_foods
        variables['industrial_foods_delay'] = industrial_foods_delay
        variables['greenhouse_delay'] = greenhouse_delay
        variables['feed_shutoff_delay'] = feed_shutoff_delay
        variables['rotation_change_delay'] = rotation_change_delay
        variables['seaweed_delay'] = seaweed_delay
        variables['biofuel_shutoff_delay'] = biofuel_shutoff_delay
        return variables


    def run_scenario(variables, cin, i):
        print("i")
        print(i)
        cin['MAX_SEAWEED_AS_PERCENT_KCALS'] = variables['max_seaweed'][i]
        cin['SEAWEED_PRODUCTION_RATE'] = variables['seaweed_production_rate'][i]
        cin['SEAWEED_NEW_AREA_PER_DAY'] = variables['seaweed_new'][i]
        cin['GREENHOUSE_GAIN_PCT'] = variables['greenhouse_gain'][i]
        cin['GREENHOUSE_AREA_MULTIPLIER'] = variables['greenhouse_area'][i]
        cin['INDUSTRIAL_FOODS_SLOPE_MULTIPLIER'] = variables['industrial_foods'][i]

        if(variables['rotation_outcome'][i] >= 2):
            cin['ROTATION_IMPROVEMENTS'] = {
                "KCALS_REDUCTION": .799,
                "FAT_RATIO": 1.928,
                "PROTEIN_RATIO": 1.067
            }
        elif(variables['rotation_outcome'][i] == 1):
            cin['ROTATION_IMPROVEMENTS'] = {
                "KCALS_REDUCTION": .808,
                "FAT_RATIO": 1.861,
                "PROTEIN_RATIO": 1.062
            }
        elif(variables['rotation_outcome'][i] == 0):
            cin['ROTATION_IMPROVEMENTS'] = {
                "KCALS_REDUCTION": .822,
                "FAT_RATIO": 1.746,
                "PROTEIN_RATIO": 1.063
            }
        cin["DELAY"] = {}
        cin["DELAY"]["INDUSTRIAL_FOODS"] = variables['industrial_foods_delay'][i]
        cin["DELAY"]["GREENHOUSE"] = variables['greenhouse_delay'][i]
        cin["DELAY"]["FEED_SHUTOFF"] = variables['feed_shutoff_delay'][i]
        cin["DELAY"]["ROTATION_CHANGE"] = variables['rotation_change_delay'][i]
        cin["DELAY"]["SEAWEED"] = variables['seaweed_delay'][i]
        cin["DELAY"]["BIOFUEL_SHUTOFF"] = variables['biofuel_shutoff_delay'][i]

        constants = {}
        constants['inputs'] = cin
        constants['CHECK_CONSTRAINTS'] = False
        failed_to_optimize = False  # until proven otherwise
        optimizer = Optimizer()

        try:
            [time_months, time_months_middle, analysis] = \
                optimizer.optimize(constants)
        except AssertionError as msg:
            print(msg)
            failed_to_optimize = True
            print("Warning: Optimization failed. Continuing.")
            return (np.nan, i)
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
            failed_to_optimize = True
            print("Warning: Optimization failed. Continuing.")
            return (np.nan, i)

        PLOT_EACH_SCENARIO = False
        if(PLOT_EACH_SCENARIO):
            Plotter.plot_people_fed_combined(time_months_middle, analysis)
            Plotter.plot_people_fed_kcals(time_months_middle, analysis,
                                          'People fed minus waste and biofuels')

        fed = analysis.people_fed_billions
        if(np.isnan(fed)):
            failed_to_optimize = True
            print("Warning: Total people fed could not be calculated. Continuing.")

        if(failed_to_optimize):
            failed_index = i
        else:
            failed_index = -1
        return (analysis.people_fed_billions, failed_index)

    def run_scenarios(variables, cin, N):
        all_fed = []
        failed_indices = []
        for i in range(0, N):
            (fed, failed_index) = MonteCarlo.run_scenario(variables, cin, i)
            if(failed_index != -1):
                failed_indices.append(failed_index)
                all_fed.append(np.nan)
                continue
            # convert people fed to calories per capita in 2020
            all_fed.append(fed / 7.8 * 2100)
        return all_fed, failed_indices

    def monte_carlo(variables, N, cin):

        Plotter.plot_all_histograms(variables, N)

        all_fed, failed_indices = MonteCarlo.run_scenarios(variables, cin, N)
        succeeded = np.delete(all_fed, np.array(failed_indices).astype(int))

        print("fraction failed to optimize")
        print(len(failed_indices)/N)
        print("failed_indices")
        print(failed_indices)

        return succeeded

    def compare_resilient_foods(variables, N, cin, foods):
        # try removing each resilient food and see
        # the effect size on total people fed
        removed = {}
        for i, label in enumerate(foods):
            cin['ADD_SEAWEED'] = True
            cin['ADD_CELLULOSIC_SUGAR'] = True
            cin['ADD_METHANE_SCP'] = True
            cin['ADD_GREENHOUSES'] = True
            cin['OG_USE_BETTER_ROTATION'] = True

            baseline_fed, failed_runs_baseline_r = MonteCarlo.run_scenarios(variables, cin, N)

            cin['ADD_SEAWEED'] = ('seaweed' not in label)
            cin['ADD_CELLULOSIC_SUGAR'] = ('sugar' not in label)
            cin['ADD_METHANE_SCP'] = ('methane' not in label)
            cin['ADD_GREENHOUSES'] = ('greenhouse' not in label)
            cin['OG_USE_BETTER_ROTATION'] = ('relocation' not in label)

            removed_fed, failed_runs_r = MonteCarlo.run_scenarios(variables, cin, N)

            print("failed_indices")
            print(failed_runs_baseline_r)
            print(failed_runs_r)

            baseline_fed = np.delete(baseline_fed,
                                     np.append(failed_runs_baseline_r,
                                               failed_runs_r).astype(int))
            removed_fed = np.delete(removed_fed, 
                                    np.append(failed_runs_baseline_r,
                                              failed_runs_r).astype(int))

            removed[label] = np.subtract(np.array(baseline_fed),
                                         np.array(removed_fed))

        # try removing all but this resilient food and adding only this one and see
        # the effect size on total people fed
        added = {}
        for i, label in enumerate(foods):

            cin['ADD_SEAWEED'] = False
            cin['ADD_CELLULOSIC_SUGAR'] = False
            cin['ADD_METHANE_SCP'] = False
            cin['ADD_GREENHOUSES'] = False
            cin['OG_USE_BETTER_ROTATION'] = False

            baseline_fed, failed_runs_baseline_a = MonteCarlo.run_scenarios(variables, cin, N)

            cin['ADD_SEAWEED'] = ('seaweed' in label)
            cin['ADD_CELLULOSIC_SUGAR'] = ('sugar' in label)
            cin['ADD_METHANE_SCP'] = ('methane' in label)
            cin['ADD_GREENHOUSES'] = ('greenhouse' in label)
            cin['OG_USE_BETTER_ROTATION'] = ('relocation' in label)

            added_fed, failed_runs_a = MonteCarlo.run_scenarios(variables, cin, N)

            baseline_fed = np.delete(baseline_fed,
                                     np.append(failed_runs_baseline_a,
                                               failed_runs_a).astype(int))
            added_fed = np.delete(added_fed,
                                  np.append(failed_runs_baseline_a,
                                            failed_runs_a).astype(int))

            added[label] = np.subtract(np.array(added_fed),
                                       np.array(baseline_fed))

        return removed, added




























MonteCarlo.run_all_scenarios()































