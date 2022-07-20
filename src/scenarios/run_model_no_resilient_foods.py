import os
import sys
import numpy as np


module_path = os.path.abspath(os.path.join("../.."))
if module_path not in sys.path:
    sys.path.append(module_path)

# import some python files from this integrated model repository
from src.optimizer.optimizer import Optimizer
from src.utilities.plotter import Plotter
from src.optimizer.parameters import Parameters
from src.scenarios.scenarios import Scenarios


def run_model_no_resilient_foods(plot_figures=True):
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

    constants_for_params = scenarios_loader.init_global_food_system_properties()

    constants_for_params = scenarios_loader.get_no_resilient_food_scenario(
        constants_for_params
    )

    constants_for_params = scenarios_loader.set_catastrophe_nutrition_profile(
        constants_for_params
    )

    constants_for_params = scenarios_loader.set_global_seasonality_nuclear_winter(
        constants_for_params
    )
    constants_for_params = scenarios_loader.set_stored_food_buffer_zero(
        constants_for_params
    )

    constants_for_params = scenarios_loader.set_fish_nuclear_winter_reduction(
        constants_for_params
    )

    constants_for_params = (
        scenarios_loader.set_nuclear_winter_global_disruption_to_crops(
            constants_for_params
        )
    )

    constants_for_params["EXCESS_FEED_KCALS"] = np.array(
        [0] * constants_for_params["NMONTHS"]
    )

    constants_for_params = scenarios_loader.get_no_resilient_food_scenario(
        constants_for_params
    )

    constants_for_params = scenarios_loader.set_immediate_shutoff(constants_for_params)

    constants_for_params = scenarios_loader.set_waste_to_zero(constants_for_params)

    constants_loader = Parameters()
    optimizer = Optimizer()
    constants["inputs"] = constants_for_params
    (
        single_valued_constants,
        multi_valued_constants,
    ) = constants_loader.computeParameters(constants)

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

    constants_for_params["EXCESS_FEED_KCALS"] = np.array(
        [0] * constants_for_params["NMONTHS"]
    )
    scenarios = Scenarios()
    constants_for_params = scenarios.set_long_delayed_shutoff(constants_for_params)

    constants_for_params = scenarios.set_global_waste_to_tripled_prices(
        constants_for_params
    )

    constants["inputs"] = constants_for_params

    optimizer = Optimizer()

    (
        single_valued_constants,
        multi_valued_constants,
    ) = constants_loader.computeParameters(constants)

    single_valued_constants["CHECK_CONSTRAINTS"] = False
    [time_months, time_months_middle, analysis] = optimizer.optimize(
        single_valued_constants, multi_valued_constants
    )

    print(
        "Estimated Kcals/capita/day, no resilient foods, minus waste & delayed halt of nonhuman consumption "
    )

    print(analysis.percent_people_fed / 100 * 2100)
    print("")

    if plot_figures:
        Plotter.plot_fig_1ab(analysis, 77)


if __name__ == "__main__":
    run_model_no_resilient_foods()
