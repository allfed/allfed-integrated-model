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
        args (list): optional command line arguments

    Returns:
        None
    """
    # create a dictionary with simulation parameters
    this_simulation = {}

    # set the simulation parameters
    this_simulation["scale"] = "country"
    this_simulation["seasonality"] = "country"
    this_simulation["grasses"] = "baseline"
    this_simulation["crop_disruption"] = "zero"
    this_simulation["scenario"] = "no_resilient_foods"
    this_simulation["fish"] = "baseline"
    this_simulation["waste"] = "baseline_in_country"
    this_simulation["nutrition"] = "baseline"
    this_simulation["buffer"] = "baseline"
    this_simulation["shutoff"] = "continued"
    this_simulation["cull"] = "do_eat_culled"

    # create an instance of the ScenarioRunnerNoTrade class
    scenario_runner = ScenarioRunnerNoTrade()

    # run the simulation with the specified parameters
    scenario_runner.run_desired_simulation(this_simulation, args)


if __name__ == "__main__":
    # get optional command line arguments
    args = sys.argv[1:]

    # call the main function with the arguments
    main(args)
