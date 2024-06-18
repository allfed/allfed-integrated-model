"""
-------------------------------------------------------------------------------
Scenario Analysis for Food Production System
-------------------------------------------------------------------------------

This script evaluates the impact of various scenarios on a country's food
production system, focusing on the effects of factors such as climate change,
waste reduction, and adoption of resilient foods. Each scenario is a combination
of several parameters, including scale, seasonality, grasses, crop disruption,
fishing conditions, waste, nutrition, buffer, shutoff, culling, fat, protein, and
meat strategy.

Instead of hardcoding the scenario parameters, this version of the script reads
them from a YAML configuration file, providing flexibility and scalability.
This makes it easier to update or add new scenarios without modifying the core
script.

- Created on: Tue Oct 17
- Author: morgan

Usage:
To run the script, two optional command line arguments can be provided:
1. To show country-specific figures (True/False)
2. To display colored maps (True/False)
3. To run the scenarios in the web interface (True/False)
If not provided, the default values are True for the first argument and False
for the second.

YAML Configuration:
The scenarios and their respective parameters are defined in a YAML file. Each
scenario is a named dictionary with parameter-value pairs. This makes it easy
to visualize, edit, and manage various scenarios.

"""

import sys
import os
import yaml
import git
from pathlib import Path

from src.scenarios.run_model_no_trade import ScenarioRunnerNoTrade


def run_scenarios_from_yaml(
    config_data, show_country_figures, show_map_figures, web_interface
):
    """
    Run the scenario in a loop, for each scenario specified, and using all data defined from the scenarios config file
    """
    if "countries" in config_data["settings"]:
        countries = config_data["settings"]["countries"]
    else:
        countries = []  # runs all countries!
    nmonths = config_data["settings"]["NMONTHS"]

    if isinstance(countries, str):  # In case only one country is provided
        countries = [countries]

    simulations = config_data["simulations"]

    for scenario_name, this_simulation in simulations.items():
        print("\n" * 4)
        print(this_simulation["title"])  # Using the title from the YAML file
        print("")

        this_simulation["NMONTHS"] = nmonths

        if web_interface:
            return_results = True
            save_all_results = True
        else:
            return_results = False
            save_all_results = False

        # Command line argument inputs (optional)
        scenario_runner = ScenarioRunnerNoTrade()
        scenario_runner.run_model_no_trade(
            title=this_simulation["title"],
            create_pptx_with_all_countries=False,
            show_country_figures=show_country_figures,
            show_map_figures=show_map_figures,
            add_map_slide_to_pptx=False,
            scenario_option=this_simulation,
            countries_list=countries,
            figure_save_postfix=f"_{scenario_name}",
            return_results=return_results,
            save_all_results=save_all_results,
        )


def load_config_data(yaml_filename):
    """
    Load the configuration data for the scenarios from a YAML file in the "scenarios/" directory.
    """
    repo_root = git.Repo(".", search_parent_directories=True).working_dir

    full_config_file_path = Path(repo_root) / "scenarios" / yaml_filename
    with open(full_config_file_path, "r") as file:
        config_data = yaml.load(file, Loader=yaml.FullLoader)

    return config_data


def print_usage_message(repo_root):
    print(
        "Usage: python3 run_scenarios_from_yaml.py",
        "<show_country_figures: True/False> <color_map: True/False> <web_interface: True/False> <yaml_filename>",
    )
    print("Example: python3 run_scenarios_from_yaml.py True False False scenarios.yaml")
    print("Note: all yaml files must be in the scenarios/ directory")

    print("\nAvailable scenarios:")
    files = os.listdir(Path(repo_root) / "scenarios")
    for file in files:
        print(file)


def get_input_args(args):
    """
    Get the input arguments from the command line.
    Print an error message if usage is incorrect.
    """
    repo_root = git.Repo(".", search_parent_directories=True).working_dir
    if len(args) < 4:
        print_usage_message(repo_root)
        print("\nError: fewer than 4 arguments supplied.")
        sys.exit(1)

    if len(args) > 4:
        print_usage_message(repo_root)
        print("\nError: more than 4 arguments supplied.")
        sys.exit(1)

    # there are 3 arguments
    if not os.path.exists(Path(repo_root) / "scenarios" / args[-1]):
        print_usage_message(repo_root)
        print("\nError: the scenario you entered doesn't exist.")
        print("You entered:")
        print(args[-1])
        sys.exit(1)

    try:
        show_country_figures = args[0].lower() == "true"
        show_map_figures = args[1].lower() == "true"
        web_interface = args[2].lower() == "true"
    except ValueError:
        print_usage_message(repo_root)
        print(
            "\nInvalid plotting arguments provided. Use True or False for the first 3 arguments."
        )
        sys.exit(1)

    yaml_filename = args[-1]

    return show_country_figures, show_map_figures, web_interface, yaml_filename


def main(args):
    """
    Main function to run the script.
    Uses input args to determine whether to show country-specific figures and
    color map of by-country fractional starvation.

    """
    (
        show_country_figures,
        show_map_figures,
        web_interface,
        yaml_filename,
    ) = get_input_args(args)

    config_data = load_config_data(yaml_filename)
    run_scenarios_from_yaml(
        config_data, show_country_figures, show_map_figures, web_interface
    )


if __name__ == "__main__":
    args = sys.argv[1:]
    main(args)
