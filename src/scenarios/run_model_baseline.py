import os
import sys
import numpy as np

module_path = os.path.abspath(os.path.join("../.."))
if module_path not in sys.path:
    sys.path.append(module_path)

# import some python files from this integrated model repository
from src.utilities.plotter import Plotter
from src.scenarios.scenarios import Scenarios
from src.scenarios.run_scenario import ScenarioRunner


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

    constants = {}
    constants["CHECK_CONSTRAINTS"] = False

    scenarios_loader, constants_for_params = set_common_baseline_properties()

    constants_for_params = scenarios_loader.set_waste_to_zero(constants_for_params)

    constants_for_params = scenarios_loader.set_immediate_shutoff(constants_for_params)

    scenario_runner = ScenarioRunner()
    results = scenario_runner.run_and_analyze_scenario(
        constants_for_params, scenarios_loader
    )

    print("")
    print("")
    print("")

    print("")
    print("Maximum usable kcals/capita/day 2020, no waste, primary production")
    print(results.percent_people_fed / 100 * 2100)
    print("")

    results1 = results

    scenarios_loader, constants_for_params = set_common_baseline_properties()

    constants_for_params = scenarios_loader.set_continued_feed_biofuels(
        constants_for_params
    )

    constants_for_params = scenarios_loader.set_global_waste_to_baseline_prices(
        constants_for_params
    )

    # No excess calories -- excess calories is set when the model is run and needs to be reset each time.
    constants_for_params["EXCESS_FEED_KCALS"] = np.array(
        [0] * constants_for_params["NMONTHS"]
    )

    scenario_runner = ScenarioRunner()
    results = scenario_runner.run_and_analyze_scenario(
        constants_for_params, scenarios_loader
    )

    results2 = results

    if plot_figures:
        Plotter.plot_fig_s1abcd(results1, results2, 72)


def set_common_baseline_properties():
    scenarios_loader = Scenarios()
    # initialize global food system properties
    constants_for_params = scenarios_loader.init_global_food_system_properties()

    # set params that are true for baseline regardless of whether country or global

    constants_for_params = scenarios_loader.get_baseline_climate_scenario(
        constants_for_params
    )

    constants_for_params = scenarios_loader.set_baseline_nutrition_profile(
        constants_for_params
    )

    constants_for_params = scenarios_loader.set_stored_food_buffer_as_baseline(
        constants_for_params
    )

    constants_for_params = scenarios_loader.set_global_seasonality_baseline(
        constants_for_params
    )

    constants_for_params = scenarios_loader.set_fish_baseline(constants_for_params)

    constants_for_params = scenarios_loader.set_disruption_to_crops_to_zero(
        constants_for_params
    )

    # No excess calories
    constants_for_params["EXCESS_FEED_KCALS"] = np.array(
        [0] * constants_for_params["NMONTHS"]
    )
    return scenarios_loader, constants_for_params


if __name__ == "__main__":
    run_model_baseline(True)
