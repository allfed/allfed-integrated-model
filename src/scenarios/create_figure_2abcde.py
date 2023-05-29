"""
This file contains the code for the creation of figure 1ab.
baseline model by country for with and
without trade scenarios.

Created on Wed Jul 15
@author: morgan
"""
from src.scenarios.run_model_no_trade import ScenarioRunnerNoTrade
from src.utilities.plotter import Plotter
from src.optimizer.interpret_results import Interpreter
import git
import numpy as np
from pathlib import Path

repo_root = git.Repo(".", search_parent_directories=True).working_dir


def call_scenario_runner(this_simulation, title):
    """
    Runs a simulation using the ScenarioRunnerNoTrade class and returns the results.

    Args:
        this_simulation (str): the name of the simulation to run
        title (str): the title of the simulation

    Returns:
        list: a list containing the world object, total population, fed population, and results dictionary

    """
    # create an instance of the ScenarioRunnerNoTrade class
    scenario_runner = ScenarioRunnerNoTrade()

    # run the model with the specified parameters and store the results
    [world, pop_total, pop_fed, results] = scenario_runner.run_model_no_trade(
        title=title,
        create_pptx_with_all_countries=False,
        show_country_figures=False,
        show_map_figures=False,
        add_map_slide_to_pptx=False,
        scenario_option=this_simulation,
        countries_list=["CHN", "IND", "USA", "IDN", "F5707+GBR"],
        figure_save_postfix="_" + title,
        return_results=True,
    )

    # return the results
    return [world, pop_total, pop_fed, results]


def call_scenario_runner_whole_world_combined(this_simulation, title):
    """
    Runs a simulation of a nuclear winter catastrophe on the world, with all countries affected.
    Args:
        this_simulation (dict): a dictionary containing simulation parameters
        title (str): a string to be used as a title for the simulation

    Returns:
        list: a list containing the world object, total population, fed population, and global results
    """
    # Set simulation parameters for a nuclear winter catastrophe on the world, with all countries affected
    this_simulation["scale"] = "country"
    this_simulation["crop_disruption"] = "country_nuclear_winter"
    this_simulation["grasses"] = "country_nuclear_winter"
    this_simulation["fish"] = "nuclear_winter"
    this_simulation["nutrition"] = "catastrophe"
    this_simulation["fat"] = "not_required"
    this_simulation["protein"] = "not_required"

    # Create a ScenarioRunnerNoTrade object
    scenario_runner = ScenarioRunnerNoTrade()

    # Run the model with the given simulation parameters
    [world, pop_total, pop_fed, results] = scenario_runner.run_model_no_trade(
        title=title,
        create_pptx_with_all_countries=False,
        show_country_figures=False,
        show_map_figures=False,
        add_map_slide_to_pptx=False,
        scenario_option=this_simulation,
        figure_save_postfix="_" + title,
        return_results=True,
    )

    # Sum the results of all countries together
    global_result_no_trade = Interpreter.sum_many_results_together(
        results, cap_at_100_percent=False
    )

    # Return the world object, total population, fed population, and global results
    return [world, pop_total, pop_fed, global_result_no_trade]


def call_scenario_runner_with_and_without_fat_protein(this_simulation, title):
    """
    Runs a simulation with and without fat and protein, and returns the results.

    Args:
        this_simulation (dict): A dictionary containing simulation parameters.
        title (str): The title of the simulation.

    Returns:
        list: A list containing the simulation results.

    Example:
        >>>
        >>> simulation = (some python dictionary with appropriate options)
        >>> results = call_scenario_runner_with_and_without_fat_protein(simulation, "Simulation Title")
    """

    # Set simulation parameters for both scenarios
    this_simulation["scale"] = "country"
    this_simulation["crop_disruption"] = "country_nuclear_winter"
    this_simulation["grasses"] = "country_nuclear_winter"
    this_simulation["fish"] = "nuclear_winter"
    this_simulation["nutrition"] = "catastrophe"

    # Run simulation without fat and protein
    this_simulation["fat"] = "not_required"
    this_simulation["protein"] = "not_required"
    [world, pop_total, pop_fed, results] = call_scenario_runner(this_simulation, title)

    # Return results
    return results


def recalculate_plots():
    """
    This function recalculates plots for different simulation scenarios and returns a list of results by country.

    Returns:
        list: A list of results by country, including the percent of people fed, country name, simulation results, and scenario name.
    """

    # Define the worst-case scenario
    this_simulation = {}
    this_simulation["scenario"] = "no_resilient_foods"
    this_simulation["waste"] = "baseline_in_country"
    this_simulation["shutoff"] = "continued"
    this_simulation["meat_strategy"] = "inefficient_meat_strategy"
    this_simulation["buffer"] = "zero"
    this_simulation["seasonality"] = "country"
    this_simulation["cull"] = "do_eat_culled"

    # Run simulation for worst-case scenario
    results_example_scenario = call_scenario_runner_with_and_without_fat_protein(
        this_simulation, "Example_Scenario"
    )

    # Define the worst-case scenario with simple adaptations
    this_simulation["waste"] = "tripled_prices_in_country"
    this_simulation["shutoff"] = "long_delayed_shutoff"
    this_simulation["meat_strategy"] = "efficient_meat_strategy"

    # Run simulation for worst-case scenario with simple adaptations
    results_simple_adaptations = call_scenario_runner_with_and_without_fat_protein(
        this_simulation, "Example_Scenario + Simple Adaptations"
    )

    # Define the worst-case scenario with simple adaptations and culling
    this_simulation["cull"] = "do_eat_culled"

    # Run simulation for worst-case scenario with simple adaptations and culling
    results_culling = call_scenario_runner_with_and_without_fat_protein(
        this_simulation, "Example_Scenario + Simple Adaptations + Culling"
    )

    # Define the worst-case scenario with simple adaptations, culling, storage, and all resilient foods
    this_simulation["scenario"] = "all_resilient_foods"

    # Run simulation for worst-case scenario with simple adaptations, culling, storage, and all resilient foods
    results_resilient_foods = call_scenario_runner_with_and_without_fat_protein(
        this_simulation,
        "Example_Scenario + Simple Adaptations + Culling + All Resilient Foods",
    )

    # Define a dictionary of countries and their names
    countries_dict = {
        "China": "China",
        "India": "India",
        "European Union (27) + UK": "EU 27 + UK",
        "United States of America": "USA",
        "Indonesia": "Indonesia",
    }

    # Create a list of results by country for the worst-case scenario
    list_by_country = []
    for country_id, country in countries_dict.items():
        list_by_country.append(
            [
                results_example_scenario[country_id].percent_people_fed,
                country,
                results_example_scenario[country_id],
                "Example Scenario",
            ]
        )

    # Create a list of results by country for the worst-case scenario with simple adaptations
    for country_id, country in countries_dict.items():
        list_by_country.append(
            [
                results_simple_adaptations[country_id].percent_people_fed,
                country,
                results_simple_adaptations[country_id],
                "Example Scenario + Simple Adaptations",
            ]
        )

    # Create a list of results by country for the worst-case scenario with simple adaptations and culling
    for country_id, country in countries_dict.items():
        list_by_country.append(
            [
                results_culling[country_id].percent_people_fed,
                country,
                results_culling[country_id],
                "Example Scenario + Simple Adaptations + Culling",
            ]
        )

    # Create a list of results by country for the worst-case scenario with simple adaptations, culling, storage, and all resilient foods
    for country_id, country in countries_dict.items():
        list_by_country.append(
            [
                results_resilient_foods[country_id].percent_people_fed,
                country,
                results_resilient_foods[country_id],
                "Example Scenario + Simple Adaptations + Culling + All Resilient Foods",
            ]
        )

    return list_by_country


def main(RECALCULATE_PLOTS=True):
    """
    This function generates and saves plots for figure 2abcde. If RECALCULATE_PLOTS is True,
    the plots are recalculated and saved. Otherwise, the previously saved plots are loaded
    and used. The function then calls Plotter.plot_fig_2abcde_updated to plot the results.

    Args:
        RECALCULATE_PLOTS (bool): If True, the plots are recalculated and saved. Otherwise,
        the previously saved plots are loaded and used.

    Returns:
        None
    """
    if RECALCULATE_PLOTS:
        results = recalculate_plots()
        np.save(Path(repo_root) / "results" / "large_reports" / "results2.npy", results)
    else:
        results = np.load(
            Path(repo_root) / "results" / "large_reports" / "results2.npy",
            allow_pickle=True,
        ).item()
    Plotter.plot_fig_2abcde_updated(results, xlim=120)
