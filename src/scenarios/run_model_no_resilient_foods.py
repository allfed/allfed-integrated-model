# this program runs the optimizer model, and ensures that all the results are
# reasonable using a couple useful checks to make sure there's nothing wacky
# going on:

# 1) check that as time increases, more people can be fed

# 2) check that stored food plus meat is always used at the
# highest rate during the largest food shortage.


import os
import sys

module_path = os.path.abspath(os.path.join("../.."))
if module_path not in sys.path:
    sys.path.append(module_path)
import numpy as np

# import some python files from this integrated model repository
from src.optimizer.optimizer import Optimizer
from src.utilities.plotter import Plotter
from src.optimizer.parameters import Parameters
from src.scenarios.scenarios import Scenarios

scenarios_loader = Scenarios()

constants = {}

constants["CHECK_CONSTRAINTS"] = False

inputs_to_optimizer = scenarios_loader.init_global_food_system_properties()

inputs_to_optimizer = scenarios_loader.get_no_resilient_food_scenario(
    inputs_to_optimizer
)

inputs_to_optimizer = scenarios_loader.set_catastrophe_nutrition_profile(
    inputs_to_optimizer
)

inputs_to_optimizer = scenarios_loader.set_global_seasonality_nuclear_winter(
    inputs_to_optimizer
)

inputs_to_optimizer = scenarios_loader.set_stored_food_buffer_zero(inputs_to_optimizer)

inputs_to_optimizer = scenarios_loader.set_fish_nuclear_winter_reduction(
    inputs_to_optimizer
)

inputs_to_optimizer = scenarios_loader.set_nuclear_winter_global_disruption_to_crops(
    inputs_to_optimizer
)


inputs_to_optimizer["EXCESS_CALORIES"] = np.array([0] * inputs_to_optimizer["NMONTHS"])

inputs_to_optimizer = scenarios_loader.get_no_resilient_food_scenario(
    inputs_to_optimizer
)

inputs_to_optimizer = scenarios_loader.set_immediate_shutoff(inputs_to_optimizer)

inputs_to_optimizer = scenarios_loader.set_waste_to_zero(inputs_to_optimizer)

constants_loader = Parameters()
optimizer = Optimizer()
constants["inputs"] = inputs_to_optimizer
single_valued_constants, multi_valued_constants = constants_loader.computeParameters(
    constants
)

single_valued_constants["CHECK_CONSTRAINTS"] = False
[time_months, time_months_middle, analysis] = optimizer.optimize(
    single_valued_constants, multi_valued_constants
)


print("")
print("Estimated Kcals/capita/day, no resilient foods, no waste")
print(analysis.percent_people_fed / 100 * 2100)
print("")

np.save(
    "../../data/no_resilient_food_primary_analysis.npy", analysis, allow_pickle=True
)


inputs_to_optimizer["EXCESS_CALORIES"] = np.array([0] * inputs_to_optimizer["NMONTHS"])
scenarios = Scenarios()
inputs_to_optimizer = scenarios.set_long_delayed_shutoff(inputs_to_optimizer)

inputs_to_optimizer = scenarios.set_waste_to_tripled_prices(inputs_to_optimizer)

constants["inputs"] = inputs_to_optimizer

optimizer = Optimizer()

single_valued_constants, multi_valued_constants = constants_loader.computeParameters(
    constants
)

single_valued_constants["CHECK_CONSTRAINTS"] = False
[time_months, time_months_middle, analysis] = optimizer.optimize(
    single_valued_constants, multi_valued_constants
)

print(
    "Estimated Kcals/capita/day, no resilient foods, minus waste & delayed halt of nonhuman consumption "
)

print(analysis.percent_people_fed / 100 * 2100)
print("")

Plotter.plot_fig_1ab(analysis, 77)
