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
    This function sets up a simulation with specific parameters and runs it using the ScenarioRunnerNoTrade class.

    Args:
        args (list): A list of command line arguments (optional)

    Returns:
        None
    """
    # Create a dictionary with simulation parameters
    this_simulation = {}

    # Set the scale, scenario, and seasonality parameters
    this_simulation["scale"] = "country"
    this_simulation["scenario"] = "no_resilient_foods"
    this_simulation["seasonality"] = "country"

    # Set the grasses and crop_disruption parameters to "country_nuclear_winter"
    this_simulation["grasses"] = "country_nuclear_winter"
    this_simulation["crop_disruption"] = "country_nuclear_winter"

    # Set the fish parameter to "nuclear_winter"
    this_simulation["fish"] = "nuclear_winter"

    # Create an instance of the ScenarioRunnerNoTrade class
    scenario_runner = ScenarioRunnerNoTrade()

    # Run the desired simulation using the created dictionary and command line arguments (if provided)
    scenario_runner.run_desired_simulation(this_simulation, args)


if __name__ == "__main__":
    # Get command line arguments
    args = sys.argv[1:]

    # Call the main function with the provided arguments
    main(args)
