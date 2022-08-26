from src.utilities.plotter import Plotter
from src.scenarios.scenarios import Scenarios
from src.scenarios.run_scenario import ScenarioRunner


def run_model_baseline(plot_figures=True):
    """
    this program runs the optimizer model, in the case of continued trade and baseline
    climate 2020

    Arguments:
        plot_figures (bool): whether to plot the figures or not.
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

    scenario_runner = ScenarioRunner()
    results = scenario_runner.run_and_analyze_scenario(
        constants_for_params, scenarios_loader
    )

    print("Maximum usable kcals/capita/day 2020, after waste and feed")
    print(results.percent_people_fed / 100 * 2100)
    results2 = results

    if plot_figures:
        Plotter.plot_fig_s1abcd(results1, results2, 72, True)


def set_common_baseline_properties():
    scenarios_loader = Scenarios()
    # initialize global food system properties
    constants_for_params = scenarios_loader.init_global_food_system_properties()

    # set params that are true for baseline regardless of whether country or global

    constants_for_params = scenarios_loader.get_no_resilient_food_scenario(
        constants_for_params
    )

    constants_for_params = scenarios_loader.set_excess_to_zero(constants_for_params)

    constants_for_params = scenarios_loader.set_baseline_nutrition_profile(
        constants_for_params
    )

    constants_for_params = scenarios_loader.set_unchanged_proportions_feed_grazing(
        constants_for_params
    )

    constants_for_params = scenarios_loader.set_stored_food_buffer_as_baseline(
        constants_for_params
    )

    constants_for_params = scenarios_loader.set_global_seasonality_baseline(
        constants_for_params
    )

    constants_for_params = scenarios_loader.set_grasses_baseline(constants_for_params)

    constants_for_params = scenarios_loader.set_fish_baseline(constants_for_params)

    constants_for_params = scenarios_loader.set_disruption_to_crops_to_zero(
        constants_for_params
    )

    constants_for_params = scenarios_loader.include_protein(constants_for_params)

    constants_for_params = scenarios_loader.include_fat(constants_for_params)
    constants_for_params = scenarios_loader.dont_cull_animals(constants_for_params)

    return scenarios_loader, constants_for_params


if __name__ == "__main__":
    run_model_baseline(True)
