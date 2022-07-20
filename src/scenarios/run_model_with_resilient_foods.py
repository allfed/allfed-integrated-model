import numpy as np
import os
import sys
import copy

module_path = os.path.abspath(os.path.join("../.."))
if module_path not in sys.path:
    sys.path.append(module_path)

# import some python files from this integrated model repository
from src.utilities.plotter import Plotter
from src.optimizer.optimizer import Optimizer
from src.optimizer.parameters import Parameters
from src.scenarios.scenarios import Scenarios


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

    scenarios_loader = Scenarios()

    constants = {}
    constants["CHECK_CONSTRAINTS"] = False

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

    # No excess calories
    constants_for_params["EXCESS_FEED_KCALS"] = np.array(
        [0] * constants_for_params["NMONTHS"]
    )

    constants_for_params = scenarios_loader.set_waste_to_zero(constants_for_params)
    constants_for_params = scenarios_loader.set_short_delayed_shutoff(
        constants_for_params
    )

    optimizer = Optimizer()
    constants_loader = Parameters()
    constants["inputs"] = constants_for_params
    constants_for_optimizer = copy.deepcopy(constants)
    (
        single_valued_constants,
        multi_valued_constants,
    ) = constants_loader.computeParameters(constants_for_optimizer)

    single_valued_constants["CHECK_CONSTRAINTS"] = False
    [time_months, time_months_middle, analysis] = optimizer.optimize(
        single_valued_constants, multi_valued_constants
    )

    print("")
    print("no waste estimated people fed (kcals/capita/day)")
    print(analysis.percent_people_fed / 100 * 2100)
    print("")

    np.save(
        "../../data/resilient_food_primary_analysis.npy", analysis, allow_pickle=True
    )

    # No excess calories
    constants_for_params["EXCESS_FEED_KCALS"] = np.array(
        [0] * constants_for_params["NMONTHS"]
    )

    optimizer = Optimizer()
    constants["inputs"] = constants_for_params
    constants_for_optimizer = copy.deepcopy(constants)
    (
        single_valued_constants,
        multi_valued_constants,
    ) = constants_loader.computeParameters(constants_for_optimizer)

    constants_for_params = scenarios_loader.set_global_waste_to_doubled_prices(
        constants_for_params
    )

    single_valued_constants["CHECK_CONSTRAINTS"] = False
    [time_months, time_months_middle, analysis] = optimizer.optimize(
        single_valued_constants, multi_valued_constants
    )

    analysis1 = analysis
    print(
        "Food available after waste, feed ramp down and biofuel ramp down, with resilient foods (kcals per capita per day)"
    )
    print(analysis.percent_people_fed / 100 * 2100)
    print("")

    constants["inputs"] = constants_for_params
    constants_for_optimizer = copy.deepcopy(constants)
    (
        single_valued_constants,
        multi_valued_constants,
    ) = constants_loader.computeParameters(constants_for_optimizer)

    single_valued_constants["CHECK_CONSTRAINTS"] = False
    [time_months, time_months_middle, analysis] = optimizer.optimize(
        single_valued_constants, multi_valued_constants
    )

    people_fed = analysis.percent_people_fed / 100 * 7.8
    feed_delay = constants_for_params["DELAY"]["FEED_SHUTOFF_MONTHS"]

    # these months are used to estimate the diet before the full scale-up of resilient foods makes there be way too much food to make sense economically
    N_MONTHS_TO_CALCULATE_DIET = 49

    excess_per_month = np.array([0] * constants_for_params["NMONTHS"])

    # don't try to feed more animals in the  months before feed shutoff
    excess_per_month[feed_delay:N_MONTHS_TO_CALCULATE_DIET] = (
        excess_per_month[feed_delay:N_MONTHS_TO_CALCULATE_DIET]
        + analysis.excess_after_run[feed_delay:N_MONTHS_TO_CALCULATE_DIET]
    )

    feed_delay = constants_for_params["DELAY"]["FEED_SHUTOFF_MONTHS"]

    n = 0
    print("Calculating 2100 calorie diet, excess feed to animals")
    while True:

        constants["inputs"] = constants_for_params
        (
            single_valued_constants,
            multi_valued_constants,
        ) = constants_loader.computeParameters(constants)

        single_valued_constants["CHECK_CONSTRAINTS"] = False
        [time_months, time_months_middle, analysis] = optimizer.optimize(
            single_valued_constants, multi_valued_constants
        )

        if people_fed > 7.79 and people_fed < 7.81:
            break

        assert feed_delay >= constants_for_params["DELAY"]["BIOFUEL_SHUTOFF_MONTHS"]

        # rapidly feed more to people until it's close to 2100 kcals, then
        # slowly feed more to people
        if people_fed < 8.3 and people_fed > 7.8:
            excess_per_month[feed_delay:N_MONTHS_TO_CALCULATE_DIET] = excess_per_month[
                feed_delay:N_MONTHS_TO_CALCULATE_DIET
            ] + np.linspace(200, 200, N_MONTHS_TO_CALCULATE_DIET - feed_delay)
        else:
            excess_per_month[feed_delay:N_MONTHS_TO_CALCULATE_DIET] = excess_per_month[
                feed_delay:N_MONTHS_TO_CALCULATE_DIET
            ] + np.linspace(15000, 15000, N_MONTHS_TO_CALCULATE_DIET - feed_delay)
        constants_for_params["EXCESS_FEED_KCALS"] = excess_per_month
        print("Diet computation complete")

        people_fed = analysis.percent_people_fed / 100 * 7.8

        excess_per_month = excess_per_month + analysis.excess_after_run

        n = n + 1

    analysis2 = analysis

    # last month plotted is month 48
    if plot_figures:
        Plotter.plot_fig_2abcd(analysis1, analysis2, 48)
    print("Diet computation complete")


if __name__ == "__main__":
    run_model_with_resilient_foods()
