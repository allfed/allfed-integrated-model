import numpy as np
from src.utilities.plotter import Plotter
from src.scenarios.scenarios import Scenarios
from src.scenarios.run_scenario import ScenarioRunner
from pathlib import Path
import git

repo_root = git.Repo(".", search_parent_directories=True).working_dir


def run_model_with_resilient_foods(plot_figures=True):
    """
    Runs the model in nuclear winter with resilient foods, then calculates a diet
    The diet is 2100 kcals, determined by feeding any excess to animals
    This currently runs for the whole earth, and does not run on a by-country
    basis.

    Args:
        plot_figures (bool): whether to plot the figures or not.

    Returns:
        None
    """

    # Set common properties for resilient foods
    scenarios_loader, constants_for_params = set_common_resilient_properties()

    # Set constants for the model
    constants = {}
    constants["CHECK_CONSTRAINTS"] = False

    # Set immediate shutoff for waste
    constants_for_params = scenarios_loader.set_immediate_shutoff(constants_for_params)

    # Set waste to zero
    constants_for_params = scenarios_loader.set_waste_to_zero(constants_for_params)

    # Set excess to zero
    constants_for_params = scenarios_loader.set_excess_to_zero(constants_for_params)

    # Run the scenario
    scenario_runner = ScenarioRunner()
    results = scenario_runner.run_and_analyze_scenario(
        constants_for_params, scenarios_loader
    )

    # Print the results
    print("")
    print("no waste estimated people fed (percent)")
    print(results.percent_people_fed)
    print("")

    # Save the results
    np.save(
        Path(repo_root) / "data" / "resilient_food_primary_results.npy",
        results,
        allow_pickle=True,
    )

    # Set common properties for resilient foods
    scenarios_loader, constants_for_params = set_common_resilient_properties()

    # Set global waste to doubled prices
    constants_for_params = scenarios_loader.set_global_waste_to_doubled_prices(
        constants_for_params
    )

    # Set short delayed shutoff
    constants_for_params = scenarios_loader.set_short_delayed_shutoff(
        constants_for_params
    )

    # Set excess to zero
    constants_for_params = scenarios_loader.set_excess_to_zero(constants_for_params)

    # Run the scenario
    scenario_runner = ScenarioRunner()
    results = scenario_runner.run_and_analyze_scenario(
        constants_for_params, scenarios_loader
    )

    # Save the results
    results1 = results

    # Print the results
    print(
        """Food available after waste, feed ramp down and biofuel ramp down,
        with resilient foods (percent)"""
    )
    print(results.percent_people_fed / 100 * 2100)
    print("")

    # Run the scenario
    scenario_runner = ScenarioRunner()
    results = scenario_runner.run_and_analyze_scenario(
        constants_for_params, scenarios_loader
    )

    # Set common properties for resilient foods
    scenarios_loader, constants_for_params = set_common_resilient_properties()

    # Set global waste to doubled prices
    constants_for_params = scenarios_loader.set_global_waste_to_doubled_prices(
        constants_for_params
    )

    # Set short delayed shutoff
    constants_for_params = scenarios_loader.set_short_delayed_shutoff(
        constants_for_params
    )

    # Set excess to zero
    constants_for_params = scenarios_loader.set_excess_to_zero(constants_for_params)

    # Get the percent of people fed
    percent_fed = results.percent_people_fed

    # Set feed delay
    feed_delay = constants_for_params["DELAY"]["FEED_SHUTOFF_MONTHS"]

    # No excess calories
    feed_delay = constants_for_params["DELAY"]["FEED_SHUTOFF_MONTHS"]

    # Calculate 2100 calorie diet, excess feed to animals
    n = 0
    print("Calculating 2100 calorie diet, excess feed to animals")
    while True:
        scenario_runner = ScenarioRunner()
        results = scenario_runner.run_and_analyze_scenario(
            constants_for_params, scenarios_loader
        )
        print("percent_fed")
        print(percent_fed)

        # Break if percent fed is between 99.8 and 100.2
        if percent_fed > 99.8 and percent_fed < 100.2:
            break

        # Assert feed delay is greater than or equal to biofuel shutoff months
        assert feed_delay >= constants_for_params["DELAY"]["BIOFUEL_SHUTOFF_MONTHS"]

        # Set common properties for resilient foods
        scenarios_loader, constants_for_params = set_common_resilient_properties()

        # Set global waste to doubled prices
        constants_for_params = scenarios_loader.set_global_waste_to_doubled_prices(
            constants_for_params
        )

        # Set short delayed shutoff
        constants_for_params = scenarios_loader.set_short_delayed_shutoff(
            constants_for_params
        )

        # Get the increased excess to feed
        excess_per_month = results.get_increased_excess_to_feed(feed_delay, percent_fed)

        # Set excess
        constants_for_params = scenarios_loader.set_excess(
            constants_for_params, excess_per_month
        )

        # Get the percent of people fed
        percent_fed = results.percent_people_fed

        n = n + 1

    # Save the results
    results2 = results

    # Plot the figures
    if plot_figures:
        Plotter.plot_fig_2abcd(results1, results2, 48)

    # Print message
    print("Diet computation complete")


def set_common_resilient_properties():
    """
    This function sets the common resilient properties for the food system by calling various functions from the
    Scenarios class.

    Returns:
        tuple: A tuple containing the Scenarios object and the constants_for_params dictionary.
    """
    # Create an instance of the Scenarios class
    scenarios_loader = Scenarios()

    # Initialize the global food system properties
    constants_for_params = scenarios_loader.init_global_food_system_properties()

    # Set the efficient feed grazing strategy
    constants_for_params = scenarios_loader.set_efficient_feed_grazing_strategy(
        constants_for_params
    )

    # Get all resilient foods scenario
    constants_for_params = scenarios_loader.get_all_resilient_foods_scenario(
        constants_for_params
    )

    # Set the catastrophe nutrition profile
    constants_for_params = scenarios_loader.set_catastrophe_nutrition_profile(
        constants_for_params
    )

    # Set the global seasonality nuclear winter
    constants_for_params = scenarios_loader.set_global_seasonality_nuclear_winter(
        constants_for_params
    )

    # Set the global grasses nuclear winter
    constants_for_params = scenarios_loader.set_global_grasses_nuclear_winter(
        constants_for_params
    )

    # Set the stored food buffer to zero
    constants_for_params = scenarios_loader.set_stored_food_buffer_zero(
        constants_for_params
    )

    # Set the fish nuclear winter reduction
    constants_for_params = scenarios_loader.set_fish_nuclear_winter_reduction(
        constants_for_params
    )

    # Set the nuclear winter global disruption to crops
    constants_for_params = (
        scenarios_loader.set_nuclear_winter_global_disruption_to_crops(
            constants_for_params
        )
    )

    # Include protein
    constants_for_params = scenarios_loader.include_protein(constants_for_params)

    # Include fat
    constants_for_params = scenarios_loader.include_fat(constants_for_params)

    # Cull animals
    constants_for_params = scenarios_loader.cull_animals(constants_for_params)

    # Return the Scenarios object and the constants_for_params dictionary
    return scenarios_loader, constants_for_params
