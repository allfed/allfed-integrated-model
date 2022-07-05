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

from scipy.stats import uniform
from scipy.stats import norm
from scipy.stats import lognorm
from scipy.stats import truncnorm
import statsmodels
import statsmodels.api as sm
import matplotlib.pyplot as plt
import multiprocessing as mp
from multiprocessing import Pool
from multiprocessing import set_start_method
# matplotlib.use('Svg')

module_path = os.path.abspath(os.path.join('../..'))
if module_path not in sys.path:
    sys.path.append(module_path)

#import some python files from this integrated model repository
from src.optimizer.optimizer import Optimizer
from src.utilities.plotter import Plotter


class MonteCarlo:
    def __init__(self):
        pass

    def run_all_scenarios(N_monte_carlo, N_comparison, load_saved_mc, load_saved_comp):
        inputs_to_optimizer = {}  # constants as inputs to optimizer

        inputs_to_optimizer['NMONTHS'] = 84
        inputs_to_optimizer['LIMIT_SEAWEED_AS_PERCENT_KCALS'] = True

        inputs_to_optimizer['NUTRITION'] = {
            'FAT_DAILY': 47, 'KCALS_DAILY': 2100, 'PROTEIN_DAILY': 51}

        inputs_to_optimizer['INITIAL_SF_FAT'] = 166.07e3 * 0.96
        inputs_to_optimizer['INITIAL_SF_PROTEIN'] = 69.25e3 * 0.96


        # "Outputs" https://docs.google.com/spreadsheets/d/19kzHpux690JTCo2IX2UA1faAd7R1QcBK/edit#gid=1815939673 cell G12-G14
        inputs_to_optimizer['TONS_DRY_CALORIC_EQIVALENT_SF'] = 1360e6 * 0.96
        inputs_to_optimizer['INCLUDE_PROTEIN'] = True
        inputs_to_optimizer['INCLUDE_FAT'] = True
        inputs_to_optimizer['WASTE'] = {}
        inputs_to_optimizer['WASTE']['SUGAR'] = 14.47  # %
        inputs_to_optimizer['WASTE']['MEAT'] = 15.17  # %
        inputs_to_optimizer['WASTE']['DAIRY'] = 16.49  # %
        inputs_to_optimizer['WASTE']['SEAFOOD'] = 14.55  # %
        inputs_to_optimizer['WASTE']['CROPS'] = 19.33  # %
        inputs_to_optimizer['WASTE']['SEAWEED'] = 14.37  # %
        inputs_to_optimizer["CULL_DURATION_MONTHS"] = 60

        inputs_to_optimizer['IS_NUCLEAR_WINTER'] = True
        excess_per_month = np.array([0] * inputs_to_optimizer['NMONTHS'])
        inputs_to_optimizer["EXCESS_CALORIES"] = excess_per_month

        inputs_to_optimizer['ADD_STORED_FOOD'] = True
        inputs_to_optimizer['ADD_OUTDOOR_GROWING'] = True
        inputs_to_optimizer['ADD_MEAT'] = True
        inputs_to_optimizer['ADD_FISH'] = True
        inputs_to_optimizer['ADD_SEAWEED'] = True
        inputs_to_optimizer['ADD_CELLULOSIC_SUGAR'] = True
        inputs_to_optimizer['ADD_METHANE_SCP'] = True
        inputs_to_optimizer['ADD_GREENHOUSES'] = True
        inputs_to_optimizer['ADD_DAIRY'] = True
        inputs_to_optimizer['OG_USE_BETTER_ROTATION'] = True
        inputs_to_optimizer['INITIAL_HARVEST_DURATION_IN_MONTHS'] = 8
        inputs_to_optimizer['FLUCTUATION_LIMIT'] = 1.5
        inputs_to_optimizer['KCAL_SMOOTHING'] = True
        inputs_to_optimizer['MEAT_SMOOTHING'] = True
        inputs_to_optimizer['STORED_FOOD_SMOOTHING'] = True
        inputs_to_optimizer['ROTATION_IMPROVEMENTS'] = {}

        # resilient foods used for simulation
        res_foods = ("greenhouses",
                     "cellulosic sugar",
                     "methane SCP",
                     'seaweed',
                     "relocated crops")

        if(load_saved_mc):
            mc_variables = np.load(
                '../data/mc_variables_'+str(N_monte_carlo)+'.npy',
                allow_pickle=True).item()
            print("Computing input variables")
        else:
            mc_variables = MonteCarlo.get_variables(N_monte_carlo, inputs_to_optimizer)
            np.save('../data/mc_variables_'+str(N_monte_carlo)+'.npy',
                    mc_variables, allow_pickle=True)
            print('MonteCarlo variables')
            Plotter.plot_fig_s1(mc_variables, N_monte_carlo)
        if(load_saved_comp):
            comp_variables = np.load(
                '../data/comp_variables_'+str(N_comparison)+'.npy',
                allow_pickle=True).item()
        else:
            print("Computing input variables")
            comp_variables = MonteCarlo.get_variables(N_comparison, inputs_to_optimizer)
            np.save('../data/comp_variables_'+str(N_comparison)+'.npy',
                    comp_variables, allow_pickle=True)
            print('Comparison variables')
            Plotter.plot_fig_s1(comp_variables, N_monte_carlo)

        # default to show monte carlo variables
        if(load_saved_comp and load_saved_mc):
            print('Monte Carlo variables')
            Plotter.plot_fig_s1(mc_variables, N_monte_carlo)


        if(load_saved_mc):
            all_fed = np.load('../data/all_fed_'+str(N_monte_carlo)+'.npy',
                              allow_pickle=True)
        else:
            print("Running Monte Carlo")
            all_fed = MonteCarlo.monte_carlo(mc_variables, N_monte_carlo, inputs_to_optimizer)
            np.save('../data/all_fed_'+str(N_monte_carlo)+'.npy', all_fed,
                    allow_pickle=True)

        if(load_saved_comp):
            removed = np.load('../data/removed_'+str(N_comparison)+'.npy',
                              allow_pickle=True).item()
            added = np.load('../data/added_'+str(N_comparison)+'.npy',
                            allow_pickle=True).item()
        else:
            print("Running Comparison")
            removed, added = MonteCarlo.compare_resilient_foods(comp_variables,
                                                                N_comparison,
                                                                inputs_to_optimizer,
                                                                res_foods)

            np.save('../data/removed_'+str(N_comparison)+'.npy', removed, allow_pickle=True)
            np.save('../data/added_'+str(N_comparison)+'.npy', added, allow_pickle=True)

        Plotter.plot_fig_3ab(all_fed, res_foods, removed, added)

    def get_variables(N, inputs_to_optimizer):

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
        delay_normal = norm.rvs(size=N, scale=np.log(M), loc=0)
        # delay_normal = np.array([0]*N)
        # round distributions
        # generate std of 2 data, mean of 2
        delay_2 = 2 * np.exp(delay_normal)
        # generate std of 3 data, mean of 3
        delay_3 = 3 * np.exp(delay_normal * 3/2)

        # set the max value so industrial foods delay doesn't exceed NMONTHS/2
        max_value = inputs_to_optimizer["NMONTHS"]/2

        # set the mean value (in months), and round to an integer

        industrial_foods_delay = (np.rint(delay_3)).astype(int)
        greenhouse_delay = (np.rint(delay_2)).astype(int)
        feed_shutoff_delay_months = (np.rint(delay_2)).astype(int)
        ROTATION_CHANGE_IN_MONTHS_delay = (np.rint(delay_2)).astype(int)
        seaweed_delay = (np.rint(delay_2 / 2)).astype(int)
        BIOFUEL_SHUTOFF_MONTHS_delay = (np.rint(delay_2 / 2)).astype(int)

        industrial_foods_delay[industrial_foods_delay > max_value] = max_value
        greenhouse_delay[greenhouse_delay > max_value] = max_value
        feed_shutoff_delay_months[feed_shutoff_delay_months > max_value] = max_value
        ROTATION_CHANGE_IN_MONTHS_delay[ROTATION_CHANGE_IN_MONTHS_delay > max_value] = max_value
        seaweed_delay[seaweed_delay > max_value] = max_value
        BIOFUEL_SHUTOFF_MONTHS_delay[BIOFUEL_SHUTOFF_MONTHS_delay > max_value] = max_value

        one_standard_deviation = 1
        mean_value = 0
        min_value_std = -2.38  # min value in standard deviations from mean
        max_value_std = 31.51  # max value in standard deviations from mean
        rotation_outcome_unit = truncnorm.rvs(
            min_value_std,
            max_value_std,
            size=N,
            scale=one_standard_deviation,
            loc=mean_value
        )

        # mean ratio of baseline year 3 reduction
        kcal_mean = 0.930

        # macronutrient ratio of the food
        fat_mean = 1.487
        protein_mean = 1.108

        # 1 standard deviation change in ratio
        kcal_std = -0.0234
        fat_std = 0.177
        # protein gets worse compared to kcals with otherwise improved rotation
        protein_std = -0.0595

        rotation_outcome_kcals = np.array(rotation_outcome_unit)\
            * kcal_std + kcal_mean
        rotation_outcome_fat = np.array(rotation_outcome_unit)\
            * fat_std + fat_mean
        rotation_outcome_protein = np.array(rotation_outcome_unit)\
            * protein_std + protein_mean

        variables = {}
        variables['seaweed_production_rate'] = seaweed_production_rate
        variables['seaweed_new'] = seaweed_new
        variables['max_seaweed'] = max_seaweed
        variables['rotation_outcome_kcals'] = rotation_outcome_kcals
        variables['rotation_outcome_fat'] = rotation_outcome_fat
        variables['rotation_outcome_protein'] = rotation_outcome_protein
        variables['greenhouse_gain'] = greenhouse_gain
        variables['greenhouse_area'] = greenhouse_area
        variables['industrial_foods'] = industrial_foods
        variables['industrial_foods_delay'] = industrial_foods_delay
        variables['greenhouse_delay'] = greenhouse_delay
        variables['feed_shutoff_delay_months'] = feed_shutoff_delay_months
        variables['ROTATION_CHANGE_IN_MONTHS_delay'] = ROTATION_CHANGE_IN_MONTHS_delay
        variables['seaweed_delay'] = seaweed_delay
        variables['BIOFUEL_SHUTOFF_MONTHS_delay'] = BIOFUEL_SHUTOFF_MONTHS_delay
        return variables
 
    def run_scenario(variables, inputs_to_optimizer, i, N):
        inputs_to_optimizer['MAX_SEAWEED_AS_PERCENT_KCALS'] = variables['max_seaweed'][i]
        inputs_to_optimizer['SEAWEED_PRODUCTION_RATE'] = variables['seaweed_production_rate'][i]
        inputs_to_optimizer['SEAWEED_NEW_AREA_PER_DAY'] = variables['seaweed_new'][i]
        inputs_to_optimizer['GREENHOUSE_GAIN_PCT'] = variables['greenhouse_gain'][i]
        inputs_to_optimizer['GREENHOUSE_AREA_MULTIPLIER'] = variables['greenhouse_area'][i]
        inputs_to_optimizer['INDUSTRIAL_FOODS_SLOPE_MULTIPLIER'] = variables['industrial_foods'][i]
        inputs_to_optimizer['ROTATION_IMPROVEMENTS']['KCALS_REDUCTION'] = \
            variables['rotation_outcome_kcals'][i]
        inputs_to_optimizer['ROTATION_IMPROVEMENTS']['FAT_RATIO'] = \
            variables['rotation_outcome_fat'][i]
        inputs_to_optimizer['ROTATION_IMPROVEMENTS']['PROTEIN_RATIO'] = \
            variables['rotation_outcome_protein'][i]

        inputs_to_optimizer["DELAY"] = {}
        inputs_to_optimizer["DELAY"]["INDUSTRIAL_FOODS_MONTHS"] = variables['industrial_foods_delay'][i]
        inputs_to_optimizer["DELAY"]["GREENHOUSE_MONTHS"] = variables['greenhouse_delay'][i]
        inputs_to_optimizer["DELAY"]["FEED_SHUTOFF_MONTHS"] = variables['feed_shutoff_delay_months'][i]
        inputs_to_optimizer["DELAY"]["ROTATION_CHANGE_IN_MONTHS"] = variables['ROTATION_CHANGE_IN_MONTHS_delay'][i]
        inputs_to_optimizer["DELAY"]["SEAWEED_MONTHS"] = variables['seaweed_delay'][i]
        inputs_to_optimizer["DELAY"]["BIOFUEL_SHUTOFF_MONTHS"] = variables['BIOFUEL_SHUTOFF_MONTHS_delay'][i]

        constants = {}
        constants['inputs'] = inputs_to_optimizer
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
            Plotter.plot_people_fed_combined(analysis)
            Plotter.plot_people_fed_kcals(analysis,
                                          'People fed minus waste and biofuels',
                                          84)

        fed = analysis.people_fed_billions
        if(np.isnan(fed)):
            failed_to_optimize = True
            print("Warning: Total people fed could not be calculated. Continuing.")

        if(failed_to_optimize):
            failed_index = i
        else:
            failed_index = -1
        VERBOSE = True
        MAX_TO_PRINT = int(N / 10)
        if(i % MAX_TO_PRINT == 0 and VERBOSE):
            print(str(i + 1)
                  + ' out of '
                  + str(N)
                  + ', '
                  + str(fed / 7.8 * 2100)
                  + ' kcals')
        return (analysis.people_fed_billions, failed_index)

    # https://www.kth.se/blogs/pdc/2019/02/parallel-programming-in-python-multiprocessing-part-1/
    def slice_data(data, nprocs):
        aver, res = divmod(len(data), nprocs)
        nums = []
        for proc in range(nprocs):
            if proc < res:
                nums.append(aver + 1)
            else:
                nums.append(aver)
        count = 0
        slices = []
        for proc in range(nprocs):
            slices.append(data[count: count+nums[proc]])
            count += nums[proc]
        return slices

    def run_scenarios(variables, inputs_to_optimizer, N):
        all_fed = []
        failed_indices = []
        USE_MULTICORES = False
        # latest time test on my machine: 21.5 seconds for 100 items

        # easiest way to do this is to run 100 at a time
        if(USE_MULTICORES):
            all_fed = []
            pool = mp.Pool(processes=mp.cpu_count())
            inp_lists = MonteCarlo.slice_data(range(N), 100)
            print(inp_lists)
            for ilist in inp_lists:
                result = pool.starmap(MonteCarlo.run_scenario,
                                  [(variables, inputs_to_optimizer, i, N) for i in list(ilist)])

                # multi_result = [pool.apply_async(MonteCarlo.run_scenario, ( variables, inputs_to_optimizer, inp, N)) for inp in inp_lists]
                # result = [x for p in multi_result for x in p.get()]
                print(result)
                # print(result)
                # quit()
                fed_list=[]
                for i in range(0, len(result)):
                    (fed, failed_index) = result[i]

                    if(failed_index != -1):
                        failed_indices.append(failed_index)
                        fed_list.append(np.nan)
                        continue
                    # convert people fed to calories per capita in 2020
                    fed_list.append(fed / 7.8 * 2100)
            all_fed = all_fed + fed_list
        else:  # latest time test on my machine: 94.41 seconds for 100 items
            for i in range(0, N):
                (fed, failed_index) = MonteCarlo.run_scenario(variables, inputs_to_optimizer, i, N)
                if(failed_index != -1):
                    failed_indices.append(failed_index)
                    all_fed.append(np.nan)
                    continue
                # convert people fed to calories per capita in 2020
                all_fed.append(fed / 7.8 * 2100)
        return all_fed, failed_indices

    def monte_carlo(variables, N, inputs_to_optimizer):
        all_fed, failed_indices = MonteCarlo.run_scenarios(variables, inputs_to_optimizer, N)
        succeeded = np.delete(all_fed, np.array(failed_indices).astype(int))

        print("fraction failed to optimize")
        print(len(failed_indices)/N)
        print("failed_indices")
        print(failed_indices)

        return succeeded

    def compare_resilient_foods(variables, N, inputs_to_optimizer, foods):
        # try removing each resilient food and see
        # the effect size on total people fed
        removed = {}
        for i, label in enumerate(foods):
            # run a baseline scenario
            inputs_to_optimizer['ADD_SEAWEED'] = True
            inputs_to_optimizer['ADD_CELLULOSIC_SUGAR'] = True
            inputs_to_optimizer['ADD_METHANE_SCP'] = True
            inputs_to_optimizer['ADD_GREENHOUSES'] = True
            inputs_to_optimizer['OG_USE_BETTER_ROTATION'] = True

            print("Remove baseline " + label)

            baseline_fed, failed_runs_baseline_r = MonteCarlo.run_scenarios(variables, inputs_to_optimizer, N)

            #run a scenario not involving
            inputs_to_optimizer['ADD_SEAWEED'] = ('seaweed' not in label)
            inputs_to_optimizer['ADD_CELLULOSIC_SUGAR'] = ('sugar' not in label)
            inputs_to_optimizer['ADD_METHANE_SCP'] = ('methane' not in label)
            inputs_to_optimizer['ADD_GREENHOUSES'] = ('greenhouse' not in label)
            inputs_to_optimizer['OG_USE_BETTER_ROTATION'] = ('relocated' not in label)

            print("Remove trial " + label)
            removed_fed, failed_runs_r = MonteCarlo.run_scenarios(variables, inputs_to_optimizer, N)

            print("failed_indices")
            print(failed_runs_baseline_r)
            print(failed_runs_r)

            baseline_fed = np.delete(baseline_fed,
                                     np.append(failed_runs_baseline_r,
                                               failed_runs_r).astype(int))
            removed_fed = np.delete(removed_fed, 
                                    np.append(failed_runs_baseline_r,
                                              failed_runs_r).astype(int))
            assert(not np.isnan(np.array(removed_fed)).any())
            assert(not np.isnan(np.array(baseline_fed)).any())
            removed[label] = np.subtract(np.array(baseline_fed),
                                         np.array(removed_fed))

        # try removing all but this resilient food and adding only this one and see
        # the effect size on total people fed
        added = {}
        for i, label in enumerate(foods):
            inputs_to_optimizer['ADD_SEAWEED'] = False
            inputs_to_optimizer['ADD_CELLULOSIC_SUGAR'] = False
            inputs_to_optimizer['ADD_METHANE_SCP'] = False
            inputs_to_optimizer['ADD_GREENHOUSES'] = False
            inputs_to_optimizer['OG_USE_BETTER_ROTATION'] = False

            print("Added baseline " + label)

            baseline_fed, failed_runs_baseline_a = MonteCarlo.run_scenarios(variables, inputs_to_optimizer, N)

            inputs_to_optimizer['ADD_SEAWEED'] = ('seaweed' in label)
            inputs_to_optimizer['ADD_CELLULOSIC_SUGAR'] = ('sugar' in label)
            inputs_to_optimizer['ADD_METHANE_SCP'] = ('methane' in label)
            inputs_to_optimizer['ADD_GREENHOUSES'] = ('greenhouse' in label)
            inputs_to_optimizer['OG_USE_BETTER_ROTATION'] = ('relocated' in label)

            print("Added trial " + label)
            added_fed, failed_runs_a = MonteCarlo.run_scenarios(variables, inputs_to_optimizer, N)

            baseline_fed = np.delete(baseline_fed,
                                     np.append(failed_runs_baseline_a,
                                               failed_runs_a).astype(int))
            added_fed = np.delete(added_fed,
                                  np.append(failed_runs_baseline_a,
                                            failed_runs_a).astype(int))

            added[label] = np.subtract(np.array(added_fed),
                                       np.array(baseline_fed))
        return removed, added

#MonteCarlo.run_all_scenarios(10,100,False,False)