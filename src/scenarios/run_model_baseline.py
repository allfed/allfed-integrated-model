import os
import sys
import numpy as np

module_path = os.path.abspath(os.path.join("../.."))
if module_path not in sys.path:
    sys.path.append(module_path)

# import some python files from this integrated model repository
from src.utilities.plotter import Plotter
from src.optimizer.optimizer import Optimizer
from src.optimizer.parameters import Parameters
from src.scenarios.scenarios import Scenarios


def run_model_baseline(plot_figures=True):
    """
    this program runs the optimizer model, and ensures that all the results are
    reasonable using a couple useful checks to make sure there's nothing wacky
    going on:
    
    1) check that as time increases, more people can be fed
    
    2) check that stored food plus meat is always used at the
    highest rate during the largest food shortage.
    
    Arguments:
        
    Returns:
        None    
    """
    scenarios_loader = Scenarios()

    constants = {}
    constants["CHECK_CONSTRAINTS"] = False

    # initialize global food system properties
    inputs_to_optimizer = scenarios_loader.init_global_food_system_properties()

    # set params that are true for baseline regardless of whether country or global

    inputs_to_optimizer = scenarios_loader.get_baseline_scenario(inputs_to_optimizer)

    inputs_to_optimizer = scenarios_loader.set_baseline_nutrition_profile(
        inputs_to_optimizer
    )

    inputs_to_optimizer = scenarios_loader.set_stored_food_buffer_as_baseline(
        inputs_to_optimizer
    )

    inputs_to_optimizer = scenarios_loader.set_global_seasonality_baseline(
        inputs_to_optimizer
    )

    inputs_to_optimizer = scenarios_loader.set_fish_baseline(inputs_to_optimizer)

    inputs_to_optimizer = scenarios_loader.set_waste_to_zero(inputs_to_optimizer)

    inputs_to_optimizer = scenarios_loader.set_immediate_shutoff(inputs_to_optimizer)

    inputs_to_optimizer = scenarios_loader.set_disruption_to_crops_to_zero(
        inputs_to_optimizer
    )

    # No excess calories
    inputs_to_optimizer["EXCESS_CALORIES"] = np.array(
        [0] * inputs_to_optimizer["NMONTHS"]
    )

    constants_loader = Parameters()
    optimizer = Optimizer()

    constants["inputs"] = inputs_to_optimizer
    (
        single_valued_constants,
        multi_valued_constants,
    ) = constants_loader.computeParameters(constants)

    single_valued_constants["CHECK_CONSTRAINTS"] = False
    [time_months, time_months_middle, analysis] = optimizer.optimize(
        single_valued_constants, multi_valued_constants
    )

    print("")
    print("Maximum usable kcals/capita/day 2020, no waste, primary production")
    print(analysis.percent_people_fed / 100 * 2100)
    print("")

    analysis1 = analysis

    inputs_to_optimizer = scenarios_loader.set_continued_feed_biofuels(
        inputs_to_optimizer
    )

    inputs_to_optimizer = scenarios_loader.set_waste_to_baseline_prices(
        inputs_to_optimizer
    )

    # No excess calories -- excess calories is set when the model is run and needs to be reset each time.
    inputs_to_optimizer["EXCESS_CALORIES"] = np.array(
        [0] * inputs_to_optimizer["NMONTHS"]
    )

    optimizer = Optimizer()
    constants["inputs"] = inputs_to_optimizer
    (
        single_valued_constants,
        multi_valued_constants,
    ) = constants_loader.computeParameters(constants)

    single_valued_constants["CHECK_CONSTRAINTS"] = False

    [time_months, time_months_middle, analysis] = optimizer.optimize(
        single_valued_constants, multi_valued_constants
    )

    analysis2 = analysis

    if plot_figures:
        Plotter.plot_fig_s1abcd(analysis1, analysis2, 72)


if __name__ == "__main__":
    run_model_baseline(False)
