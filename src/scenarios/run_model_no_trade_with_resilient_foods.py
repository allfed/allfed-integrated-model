"""
This file contains the code for the baseline model by country for with and
without trade scenarios.

Created on Wed Jul 15
@author: morgan
"""
import sys
from src.scenarios.run_model_no_trade import ScenarioRunnerNoTrade


def main(args):
    """
    Runs a simulation with the given arguments.

    Args:
        args (list): List of command line arguments. Optional.

    Returns:
        None
    """
    # Create a dictionary to store simulation parameters
    this_simulation = {}

    # Set the simulation parameters
    this_simulation["scale"] = "country"
    this_simulation["scenario"] = "all_resilient_foods"
    this_simulation["seasonality"] = "country"
    this_simulation["grasses"] = "country_nuclear_winter"
    this_simulation["crop_disruption"] = "country_nuclear_winter"
    this_simulation["fish"] = "nuclear_winter"

    # Create an instance of the ScenarioRunnerNoTrade class
    scenario_runner = ScenarioRunnerNoTrade()

    # Run the desired simulation with the given parameters and command line arguments
    scenario_runner.run_desired_simulation(this_simulation, args)


if __name__ == "__main__":
    # Get command line arguments
    args = sys.argv[1:]

    # Set default command line arguments if none are provided
    args = ["single", "pptx", "plot"]

    # Call the main function with the given arguments
    main(args)
