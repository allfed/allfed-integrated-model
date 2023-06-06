"""
This file contains the code for the creation of figure 1ab.
baseline model by country for with and
without trade scenarios.

Created on Wed Jul 15
@author: morgan
"""
from src.utilities.plotter import Plotter
from src.scenarios.run_scenario import ScenarioRunner
import git

repo_root = git.Repo(".", search_parent_directories=True).working_dir


def call_scenario_runner(this_simulation, title):
    """
    Runs a scenario using the ScenarioRunner class and prints the results.
    Args:
        this_simulation (str): the name of the simulation to run
        title (str): the title to print before the results

    Returns:
        ScenarioResults: the results of the scenario
    """
    # Create a new instance of the ScenarioRunner class
    scenario_runner = ScenarioRunner()

    # Set the constants and scenarios loader based on the simulation option
    constants_for_params, scenarios_loader = scenario_runner.set_depending_on_option(
        [], this_simulation
    )

    # Run the scenario and analyze the results
    results = scenario_runner.run_and_analyze_scenario(
        constants_for_params, scenarios_loader
    )

    # Print the title and the percent of people fed
    print("")
    print(title)
    print("percent_people_fed")
    print(results.percent_people_fed)
    print("")

    # Return the results
    return results

def main():
    """
    This function runs a series of simulations with different parameters and plots the results.
    It then calls a plotting function to create a figure with subplots showing the results of each simulation.

    The function first sets up a dictionary with parameters for the worst-case scenario.
    It then sets up dictionaries with parameters for three additional scenarios with different adaptations.
    For each scenario, it calls a function to run the simulation and store the results.
    Finally, it calls a plotting function to create a figure with subplots showing the results of each simulation.
    """

    # WORST CASE #
    this_simulation = {}
    this_simulation["scale"] = "global"
    this_simulation["crop_disruption"] = "global_nuclear_winter"
    this_simulation["grasses"] = "global_nuclear_winter"
    this_simulation["fish"] = "nuclear_winter"
    this_simulation["nutrition"] = "catastrophe"

    this_simulation["fat"] = "required"
    this_simulation["protein"] = "required"

    this_simulation["scenario"] = "no_resilient_foods"

    this_simulation["buffer"] = "no_stored_between_years"
    this_simulation["seasonality"] = "no_seasonality"

    this_simulation["waste"] = "baseline_globally"
    this_simulation["shutoff"] = "continued"
    this_simulation["meat_strategy"] = "efficient_meat_strategy"

    this_simulation["cull"] = "dont_eat_culled"

    # WORST CASE + SIMPLE_ADAPTATIONS #

    this_simulation["waste"] = "tripled_prices_globally"
    this_simulation["shutoff"] = "long_delayed_shutoff"
    this_simulation["meat_strategy"] = "efficient_meat_strategy"

    title_simple_adaptations = "trade\n+ simple_adaptations"
    results_simple_adaptations = call_scenario_runner(
        this_simulation, title_simple_adaptations
    )

    # WORST CASE + SIMPLE_ADAPTATIONS + CULLING + STORAGE #

    this_simulation["cull"] = "do_eat_culled"
    this_simulation["buffer"] = "zero"
    this_simulation["seasonality"] = "nuclear_winter_globally"
    title_example_scenario = "trade\n+ simple_adaptations\n+ culling\n+ storage"
    results_example_scenario = call_scenario_runner(
        this_simulation, title_example_scenario
    )

    # WORST CASE + SIMPLE_ADAPTATIONS + STORAGE + CULLING + ALL RESILIENT FOODS
    this_simulation["scenario"] = "all_resilient_foods"
    title_resilient_foods = (
        "trade\n+ simple_adaptations\n+ culling\n+ storage\n+ resilient foods"
    )
    results_resilient_foods = call_scenario_runner(
        this_simulation, title_resilient_foods
    )
    results = {}
    results[title_simple_adaptations] = results_simple_adaptations
    results[title_example_scenario] = results_example_scenario
    results[title_resilient_foods] = results_resilient_foods
    Plotter.plot_fig_3abcde_updated(results, 120)


if __name__ == "__main__":
    main()
