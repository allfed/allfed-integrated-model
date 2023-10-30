import numpy as np
from src.utilities.plotter import Plotter
from src.scenarios.run_scenario import ScenarioRunner
from src.scenarios.scenarios import Scenarios
import git
from pathlib import Path

repo_root = git.Repo(".", search_parent_directories=True).working_dir


def run_model_no_resilient_foods(plot_figures=True):
    """
    This function runs the optimizer model and ensures that all the results are reasonable using a couple useful checks to make sure there's nothing wacky going on:
    1) check that as time increases, more people can be fed
    2) check that stored food plus meat is always used at the highest rate during the largest food shortage.

    Args:
        plot_figures (bool): whether to plot the figures or not.

    Returns:
        None
    """

    # Set constants dictionary
    constants = {}

    # Set CHECK_CONSTRAINTS to False
    constants["CHECK_CONSTRAINTS"] = False

    # Set common properties for scenarios loader and constants for parameters
    scenarios_loader, constants_for_params = set_common_no_resilient_properties()

    # Set immediate shutoff for constants_for_params
    constants_for_params = scenarios_loader.set_immediate_shutoff(constants_for_params)

    # Set waste to zero for constants_for_params
    constants_for_params = scenarios_loader.set_waste_to_zero(constants_for_params)

    # Create scenario runner object
    scenario_runner = ScenarioRunner()

    # Run and analyze scenario with constants_for_params and scenarios_loader
    results = scenario_runner.run_and_analyze_scenario(
        constants_for_params, scenarios_loader
    )

    # Print estimated percent people fed, no resilient foods, no waste
    print("")
    print("")
    print("Estimated percet people fed, no resilient foods, no waste")
    print(results.percent_people_fed / 100 * 2100)
    print("")

    # Save results to file
    np.save(
        Path(repo_root) / "data" / "no_resilient_food_primary_results.npy",
        results,
        allow_pickle=True,
    )

    # Set common properties for scenarios loader and constants for parameters
    scenarios_loader, constants_for_params = set_common_no_resilient_properties()

    # Set long delayed shutoff for constants_for_params
    constants_for_params = scenarios_loader.set_long_delayed_shutoff(
        constants_for_params
    )

    # Set global waste to tripled prices for constants_for_params
    constants_for_params = scenarios_loader.set_global_waste_to_tripled_prices(
        constants_for_params
    )

    # Create scenario runner object
    scenario_runner = ScenarioRunner()

    # Run and analyze scenario with constants_for_params and scenarios_loader
    results = scenario_runner.run_and_analyze_scenario(
        constants_for_params, scenarios_loader
    )

    # Print estimated percent people fed, no resilient foods, minus waste & delayed halt of nonhuman consumption
    print(
        """Estimated percent people fed, no resilient foods, minus waste & delayed halt
         of nonhuman consumption """
    )

    print(results.percent_people_fed / 100 * 2100)
    print("")

    # Plot figures if plot_figures is True
    if plot_figures:
        Plotter.plot_fig_1ab(
            results,
            77,
            "World",
            True,
            False,
            scenarios_loader.scenario_description,
        )


def set_common_no_resilient_properties():
    """
    This function sets the common properties for the food system in a scenario where there are no resilient foods.
    It uses the Scenarios class to load the necessary data and set the properties accordingly.
    Returns:
        tuple: a tuple containing the Scenarios object and the constants for the food system properties
    """
    # Load the Scenarios object
    scenarios_loader = Scenarios()

    # Initialize the global food system properties
    constants_for_params = scenarios_loader.init_global_food_system_properties()

    # Get the scenario for no resilient food
    constants_for_params = scenarios_loader.get_no_resilient_food_scenario(
        constants_for_params
    )

    # Set excess food to zero
    constants_for_params = scenarios_loader.set_excess_to_zero(constants_for_params)

    # Set the nutrition profile for a catastrophe
    constants_for_params = scenarios_loader.set_catastrophe_nutrition_profile(
        constants_for_params
    )

    # Set the seasonality for a nuclear winter
    constants_for_params = scenarios_loader.set_global_seasonality_nuclear_winter(
        constants_for_params
    )

    # Set the grasses for a nuclear winter
    constants_for_params = scenarios_loader.set_global_grasses_nuclear_winter(
        constants_for_params
    )

    # Set the stored food buffer to zero
    constants_for_params = scenarios_loader.set_stored_food_buffer_zero(
        constants_for_params
    )

    # Set the efficient feed grazing strategy
    constants_for_params = scenarios_loader.set_efficient_feed_grazing_strategy(
        constants_for_params
    )

    # Reduce fish production for a nuclear winter
    constants_for_params = scenarios_loader.set_fish_nuclear_winter_reduction(
        constants_for_params
    )

    # Include protein in the food system
    constants_for_params = scenarios_loader.include_protein(constants_for_params)

    # Include fat in the food system
    constants_for_params = scenarios_loader.include_fat(constants_for_params)

    # Cull animals to match the food supply
    constants_for_params = scenarios_loader.cull_animals(constants_for_params)

    # Set the global disruption to crops for a nuclear winter
    constants_for_params = (
        scenarios_loader.set_nuclear_winter_global_disruption_to_crops(
            constants_for_params
        )
    )

    # Return the Scenarios object and the constants for the food system properties
    return scenarios_loader, constants_for_params
