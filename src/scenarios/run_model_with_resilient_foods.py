import numpy as np
from src.utilities.plotter import Plotter
from src.scenarios.scenarios import Scenarios
from src.scenarios.run_scenario import ScenarioRunner


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

    constants_for_params = scenarios_loader.set_waste_to_zero(constants_for_params)
    constants_for_params = scenarios_loader.set_immediate_shutoff(constants_for_params)

    constants_for_params = scenarios_loader.set_excess_to_zero(constants_for_params)

    scenario_runner = ScenarioRunner()
    results = scenario_runner.run_and_analyze_scenario(
        constants_for_params, scenarios_loader
    )
    print("")
    print("no waste estimated people fed (percent)")
    print(results.percent_people_fed)
    print("")

    np.save("../../data/resilient_food_primary_results.npy", results, allow_pickle=True)

    scenarios_loader, constants_for_params = set_common_resilient_properties()

    constants_for_params = scenarios_loader.set_global_waste_to_doubled_prices(
        constants_for_params
    )
    constants_for_params = scenarios_loader.set_short_delayed_shutoff(
        constants_for_params
    )

    constants_for_params = scenarios_loader.set_excess_to_zero(constants_for_params)

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

    constants_for_params = scenarios_loader.set_excess_to_zero(constants_for_params)

    percent_fed = results.percent_people_fed
    feed_delay = constants_for_params["DELAY"]["FEED_SHUTOFF_MONTHS"]

    # No excess calories
    feed_delay = constants_for_params["DELAY"]["FEED_SHUTOFF_MONTHS"]

    n = 0
    print("Calculating 2100 calorie diet, excess feed to animals")
    while True:

        scenario_runner = ScenarioRunner()
        results = scenario_runner.run_and_analyze_scenario(
            constants_for_params, scenarios_loader
        )
        print("percent_fed")
        print(percent_fed)

        if percent_fed > 99.8 and percent_fed < 100.2:
            break

        assert feed_delay >= constants_for_params["DELAY"]["BIOFUEL_SHUTOFF_MONTHS"]

        scenarios_loader, constants_for_params = set_common_resilient_properties()

        constants_for_params = scenarios_loader.set_global_waste_to_doubled_prices(
            constants_for_params
        )
        constants_for_params = scenarios_loader.set_short_delayed_shutoff(
            constants_for_params
        )

        excess_per_month = results.get_increased_excess_to_feed(feed_delay, percent_fed)

        constants_for_params = scenarios_loader.set_excess(
            constants_for_params, excess_per_month
        )

        percent_fed = results.percent_people_fed

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

    constants_for_params = scenarios_loader.set_efficient_feed_grazing_strategy(
        constants_for_params
    )

    constants_for_params = scenarios_loader.include_protein(constants_for_params)

    constants_for_params = scenarios_loader.include_fat(constants_for_params)
    constants_for_params = scenarios_loader.cull_animals(constants_for_params)

    return scenarios_loader, constants_for_params


if __name__ == "__main__":
    run_model_with_resilient_foods()
