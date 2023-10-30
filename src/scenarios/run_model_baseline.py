from src.utilities.plotter import Plotter
from src.scenarios.scenarios import Scenarios
from src.scenarios.run_scenario import ScenarioRunner


def run_model_baseline(plot_figures=True):
    """
    This function runs the optimizer model for the case of continued trade and baseline climate 2020.
    It sets the constants, loads the scenarios, runs the scenario runner, and prints the results.
    If plot_figures is True, it also plots the figures.

    Args:
        plot_figures (bool): whether to plot the figures or not.

    Returns:
        None
    """

    # Set the constants
    constants = {}
    constants["CHECK_CONSTRAINTS"] = False

    # Load the scenarios and set the common baseline properties
    scenarios_loader, constants_for_params = set_common_baseline_properties()

    # Set the global waste to baseline prices and immediate shutoff
    constants_for_params = scenarios_loader.set_global_waste_to_baseline_prices(
        constants_for_params
    )
    constants_for_params = scenarios_loader.set_immediate_shutoff(constants_for_params)

    # Run and analyze the scenario
    scenario_runner = ScenarioRunner()
    results = scenario_runner.run_and_analyze_scenario(
        constants_for_params, scenarios_loader
    )

    # Print the results
    print("")
    print("")
    print("")

    print("")
    print("Maximum usable kcals/capita/day 2020, no waste, primary production")
    print(results.percent_people_fed / 100 * 2100)
    print("")

    results1 = results

    # Load the scenarios and set the common baseline properties
    scenarios_loader, constants_for_params = set_common_baseline_properties()

    # Set the continued feed biofuels and global waste to baseline prices
    constants_for_params = scenarios_loader.set_continued_feed_biofuels(
        constants_for_params
    )
    constants_for_params = scenarios_loader.set_global_waste_to_baseline_prices(
        constants_for_params
    )

    # Run and analyze the scenario
    scenario_runner = ScenarioRunner()
    results = scenario_runner.run_and_analyze_scenario(
        constants_for_params, scenarios_loader
    )

    # Print the results
    print("Maximum usable kcals/capita/day 2020, after waste and feed")
    print(results.percent_people_fed / 100 * 2100)
    results2 = results

    # Plot the figures if plot_figures is True
    if plot_figures:
        Plotter.plot_fig_s1abcd(results1, results2, 72, True)


def set_common_baseline_properties():
    """
    This function sets the common baseline properties for the food system. These properties are true for the baseline
    regardless of whether the country or global scenario is being run. The function initializes global food system
    properties and sets various parameters to their baseline values.

    Returns:
        tuple: A tuple containing the Scenarios object and the constants_for_params dictionary with the baseline
        properties set.
    """

    # Initialize Scenarios object
    scenarios_loader = Scenarios()

    # Initialize global food system properties
    constants_for_params = scenarios_loader.init_global_food_system_properties()

    # Set params that are true for baseline regardless of whether country or global
    # Set no resilient food scenario
    constants_for_params = scenarios_loader.get_no_resilient_food_scenario(
        constants_for_params
    )

    # Set excess to zero
    constants_for_params = scenarios_loader.set_excess_to_zero(constants_for_params)

    # Set baseline nutrition profile
    constants_for_params = scenarios_loader.set_baseline_nutrition_profile(
        constants_for_params
    )

    # Set unchanged proportions feed grazing
    constants_for_params = scenarios_loader.set_unchanged_proportions_feed_grazing(
        constants_for_params
    )

    # Set stored food buffer as baseline
    constants_for_params = scenarios_loader.set_stored_food_buffer_as_baseline(
        constants_for_params
    )

    # Set global seasonality baseline
    constants_for_params = scenarios_loader.set_global_seasonality_baseline(
        constants_for_params
    )

    # Set grasses baseline
    constants_for_params = scenarios_loader.set_grasses_baseline(constants_for_params)

    # Set fish baseline
    constants_for_params = scenarios_loader.set_fish_baseline(constants_for_params)

    # Set disruption to crops to zero
    constants_for_params = scenarios_loader.set_disruption_to_crops_to_zero(
        constants_for_params
    )

    # Include protein
    constants_for_params = scenarios_loader.include_protein(constants_for_params)

    # Include fat
    constants_for_params = scenarios_loader.include_fat(constants_for_params)

    # Don't cull animals
    constants_for_params = scenarios_loader.dont_cull_animals(constants_for_params)

    # Return Scenarios object and constants_for_params dictionary with baseline properties set
    return scenarios_loader, constants_for_params
