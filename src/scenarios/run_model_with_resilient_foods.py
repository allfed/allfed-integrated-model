import numpy as np
import os
import sys
import copy

from pulp import const

module_path = os.path.abspath(os.path.join("../.."))
if module_path not in sys.path:
    sys.path.append(module_path)

# import some python files from this integrated model repository
from src.utilities.plotter import Plotter
from src.scenarios.scenarios import Scenarios
from src.scenarios.run_scenario import ScenarioRunner
from src.optimizer.optimizer import Optimizer


def run_model_with_resilient_foods(plot_figures=True):
    """
    Runs the model in nuclear winter with resilient foods, then calculates a diet
    The diet is 2100 kcals, determined by feeding any excess to animals
    This currently runs for the whole earth, and does not run on a by-country
    basis.

    Arguments:

    Returns:
        None
    """

    scenarios_loader, constants_for_params = set_common_resilient_properties()

    constants = {}
    constants["CHECK_CONSTRAINTS"] = False

    # No excess calories
    constants_for_params["EXCESS_FEED_KCALS"] = np.array(
        [0] * constants_for_params["NMONTHS"]
    )

    constants_for_params = scenarios_loader.set_waste_to_zero(constants_for_params)
    constants_for_params = scenarios_loader.set_immediate_shutoff(constants_for_params)

    scenario_runner = ScenarioRunner()
    results = scenario_runner.run_and_analyze_scenario(
        constants_for_params, scenarios_loader
    )
    print("")
    print("no waste estimated people fed (percent)")
    print(results.percent_people_fed)
    print("")

    np.save("../../data/resilient_food_primary_results.npy", results, allow_pickle=True)

    # No excess calories
    constants_for_params["EXCESS_FEED_KCALS"] = np.array(
        [0] * constants_for_params["NMONTHS"]
    )

    scenarios_loader, constants_for_params = set_common_resilient_properties()

    constants_for_params = scenarios_loader.set_global_waste_to_doubled_prices(
        constants_for_params
    )
    constants_for_params = scenarios_loader.set_short_delayed_shutoff(
        constants_for_params
    )

    # No excess calories
    constants_for_params["EXCESS_FEED_KCALS"] = np.array(
        [0] * constants_for_params["NMONTHS"]
    )

    scenario_runner = ScenarioRunner()
    results = scenario_runner.run_and_analyze_scenario(
        constants_for_params, scenarios_loader
    )

    results1 = results
    print(
        "Food available after waste, feed ramp down and biofuel ramp down, with resilient foods (percent)"
    )
    print(results.percent_people_fed / 100 * 2100)
    print("")

    scenario_runner = ScenarioRunner()
    results = scenario_runner.run_and_analyze_scenario(
        constants_for_params, scenarios_loader
    )

    scenarios_loader, constants_for_params = set_common_resilient_properties()

    constants_for_params = scenarios_loader.set_global_waste_to_doubled_prices(
        constants_for_params
    )
    constants_for_params = scenarios_loader.set_short_delayed_shutoff(
        constants_for_params
    )

    percent_fed = results.percent_people_fed
    feed_delay = constants_for_params["DELAY"]["FEED_SHUTOFF_MONTHS"]

    # these months are used to estimate the diet before the full scale-up of resilient foods makes there be way too much food to make sense economically
    N_MONTHS_TO_CALCULATE_DIET = 49

    excess_per_month = np.array([0] * constants_for_params["NMONTHS"])

    # No excess calories
    constants_for_params["EXCESS_FEED_KCALS"] = excess_per_month

    feed_delay = constants_for_params["DELAY"]["FEED_SHUTOFF_MONTHS"]

    n = 0
    print("Calculating 2100 calorie diet, excess feed to animals")
    while True:

        scenario_runner = ScenarioRunner()
        results = scenario_runner.run_and_analyze_scenario(
            constants_for_params, scenarios_loader
        )

        if percent_fed > 99.9 and percent_fed < 100.1:
            break

        assert feed_delay >= constants_for_params["DELAY"]["BIOFUEL_SHUTOFF_MONTHS"]

        # rapidly feed more to people until it's close to 2100 kcals, then
        # slowly feed more to people
        SMALL_INCREASE_IN_EXCESS = 0.1
        LARGE_INCREASE_IN_EXCESS = 3
        if percent_fed < 106 and percent_fed > 100:
            excess_per_month[feed_delay:N_MONTHS_TO_CALCULATE_DIET] = excess_per_month[
                feed_delay:N_MONTHS_TO_CALCULATE_DIET
            ] + np.linspace(
                SMALL_INCREASE_IN_EXCESS,
                SMALL_INCREASE_IN_EXCESS,
                N_MONTHS_TO_CALCULATE_DIET - feed_delay,
            )
        else:
            excess_per_month[feed_delay:N_MONTHS_TO_CALCULATE_DIET] = excess_per_month[
                feed_delay:N_MONTHS_TO_CALCULATE_DIET
            ] + np.linspace(
                LARGE_INCREASE_IN_EXCESS,
                LARGE_INCREASE_IN_EXCESS,
                N_MONTHS_TO_CALCULATE_DIET - feed_delay,
            )
        constants_for_params["EXCESS_FEED_KCALS"] = excess_per_month
        print("Diet computation complete")

        percent_fed = results.percent_people_fed

        excess_per_month = excess_per_month + results.excess_after_run

        n = n + 1

    results2 = results

    # last month plotted is month 48
    if plot_figures:
        Plotter.plot_fig_2abcd(results1, results2, 48)
    print("Diet computation complete")


def set_common_resilient_properties():
    scenarios_loader = Scenarios()

    constants_for_params = scenarios_loader.init_global_food_system_properties()

    constants_for_params = scenarios_loader.get_resilient_food_scenario(
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

    return scenarios_loader, constants_for_params


if __name__ == "__main__":
    run_model_with_resilient_foods()
