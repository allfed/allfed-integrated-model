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
module_path = os.path.abspath(os.path.join('../..'))
if module_path not in sys.path:
    sys.path.append(module_path)

#import some python files from this integrated model repository
from src.utilities.plotter import Plotter
from src.optimizer.optimizer import Optimizer
from src.optimizer.parameters import Parameters
from src.scenarios.scenarios import Scenarios 

scenarios_loader = Scenarios()

constants = {}
constants['CHECK_CONSTRAINTS'] = False

inputs_to_optimizer = \
    scenarios_loader.init_global_food_system_properties()

inputs_to_optimizer = \
    scenarios_loader.get_resilient_food_scenario(inputs_to_optimizer)

inputs_to_optimizer = \
    scenarios_loader.set_catastrophe_nutrition_profile(inputs_to_optimizer)

inputs_to_optimizer = \
    scenarios_loader.set_global_seasonality_nuclear_winter(inputs_to_optimizer)

inputs_to_optimizer = \
    scenarios_loader.set_stored_food_all_used(inputs_to_optimizer)

inputs_to_optimizer = \
    scenarios_loader.set_fish_nuclear_winter_reduction(inputs_to_optimizer)

inputs_to_optimizer = \
    scenarios_loader.set_nuclear_winter_global_disruption_to_crops(
        inputs_to_optimizer
    )

# No excess calories
inputs_to_optimizer["EXCESS_CALORIES"] = \
    np.array([0] * inputs_to_optimizer['NMONTHS'])

inputs_to_optimizer = scenarios_loader.set_waste_to_zero(inputs_to_optimizer)
inputs_to_optimizer = scenarios_loader.set_short_delayed_shutoff(inputs_to_optimizer)

optimizer = Optimizer()
constants_loader = Parameters()
constants['inputs'] = inputs_to_optimizer
constants_for_optimizer = copy.deepcopy(constants)
single_valued_constants, multi_valued_constants = \
    constants_loader.computeParameters(constants_for_optimizer)

single_valued_constants["CHECK_CONSTRAINTS"] = False
[time_months, time_months_middle, analysis] = \
    optimizer.optimize(single_valued_constants, multi_valued_constants)


print("")
print("no waste estimated people fed (kcals/capita/day)")
print(analysis.percent_people_fed/100*2100)
print("")

np.save('../../data/resilient_food_primary_analysis.npy',
        analysis,
        allow_pickle=True)

# No excess calories
inputs_to_optimizer["EXCESS_CALORIES"] = \
    np.array([0] * inputs_to_optimizer['NMONTHS'])

optimizer = Optimizer()
constants['inputs'] = inputs_to_optimizer
constants_for_optimizer = copy.deepcopy(constants)
single_valued_constants, multi_valued_constants = \
    constants_loader.computeParameters(constants_for_optimizer)
    
inputs_to_optimizer = \
    scenarios_loader.set_waste_to_doubled_prices(inputs_to_optimizer)

single_valued_constants["CHECK_CONSTRAINTS"] = False
[time_months, time_months_middle, analysis] = \
    optimizer.optimize(single_valued_constants, multi_valued_constants)


analysis1 = analysis
print("Food available after waste, feed ramp down and biofuel ramp down, with resilient foods (kcals per capita per day)")
print(analysis.percent_people_fed/100*2100)
print("")

constants['inputs'] = inputs_to_optimizer
constants_for_optimizer = copy.deepcopy(constants)
single_valued_constants, multi_valued_constants = \
    constants_loader.computeParameters(constants_for_optimizer)

single_valued_constants["CHECK_CONSTRAINTS"] = False
[time_months, time_months_middle, analysis] = \
    optimizer.optimize(single_valued_constants, multi_valued_constants)


people_fed = analysis.percent_people_fed/100*7.8
feed_delay = inputs_to_optimizer["DELAY"]['FEED_SHUTOFF_MONTHS']

# these months are used to estimate the diet before the full scale-up of resilient foods makes there be way too much food to make sense economically
N_MONTHS_TO_CALCULATE_DIET = 49

excess_per_month = np.array([0] * inputs_to_optimizer['NMONTHS'])

# don't try to feed more animals in the  months before feed shutoff
excess_per_month[feed_delay:N_MONTHS_TO_CALCULATE_DIET] = \
    excess_per_month[feed_delay:N_MONTHS_TO_CALCULATE_DIET]\
    + analysis.excess_after_run[feed_delay:N_MONTHS_TO_CALCULATE_DIET]

feed_delay = inputs_to_optimizer["DELAY"]['FEED_SHUTOFF_MONTHS']

n = 0
print("Calculating 2100 calorie diet, excess feed to animals")
while(True):

    constants['inputs'] = inputs_to_optimizer
    single_valued_constants, multi_valued_constants = \
        constants_loader.computeParameters(constants)
    print(multi_valued_constants['excess_kcals'])
    # print(excess_per_month)
    single_valued_constants["CHECK_CONSTRAINTS"] = False
    [time_months, time_months_middle, analysis] = \
        optimizer.optimize(single_valued_constants, multi_valued_constants)
    print("analysis.kcals_fed")
    print(analysis.kcals_fed)

    if(people_fed > 7.79 and people_fed < 7.81):
        break

    assert(feed_delay >= inputs_to_optimizer["DELAY"]['BIOFUEL_SHUTOFF_MONTHS'])

    # rapidly feed more to people until it's close to 2100 kcals, then
    # slowly feed more to people 
    if(people_fed < 8.3 and people_fed > 7.8):
        excess_per_month[feed_delay:N_MONTHS_TO_CALCULATE_DIET] = \
            excess_per_month[feed_delay:N_MONTHS_TO_CALCULATE_DIET]\
            + np.linspace(500, 500, N_MONTHS_TO_CALCULATE_DIET - feed_delay)
    else:
        excess_per_month[feed_delay:N_MONTHS_TO_CALCULATE_DIET] = \
            excess_per_month[feed_delay:N_MONTHS_TO_CALCULATE_DIET]\
            + np.linspace(25000, 25000, N_MONTHS_TO_CALCULATE_DIET - feed_delay)
    inputs_to_optimizer["EXCESS_CALORIES"] = excess_per_month
    Plotter.plot_fig_2abcd(analysis1, analysis, 48)
    print("Diet computation complete")

    n = n + 1

analysis2 = analysis

# last month plotted is month 48
Plotter.plot_fig_2abcd(analysis1, analysis2, 48)
print("Diet computation complete")
