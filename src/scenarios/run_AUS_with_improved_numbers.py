"""
This file contains the code for the baseline model by country for with and
without trade scenarios.

Created on Wed Jul 15
@author: morgan
"""
import sys
from src.scenarios.run_model_no_trade import ScenarioRunnerNoTrade


def run_AUS_with_and_without_resilient():
    """
    This function runs a simulation for AUS with and without resilient foods. It sets up a dictionary of simulation
    parameters and passes it to the ScenarioRunnerNoTrade object to run the simulation. It also takes optional command
    line arguments.

    Args:
        None

    Returns:
        None
    """

    # Set up dictionary of simulation parameters
    this_simulation = {}

    this_simulation["scale"] = "country"
    this_simulation["scenario"] = "all_resilient_foods"
    this_simulation["seasonality"] = "country"
    this_simulation["grasses"] = "country_nuclear_winter"
    this_simulation["crop_disruption"] = "country_nuclear_winter"
    this_simulation["fish"] = "nuclear_winter"

    this_simulation["waste"] = "doubled_prices_in_country"
    this_simulation["fat"] = "not_required"
    this_simulation["protein"] = "not_required"
    this_simulation["nutrition"] = "catastrophe"
    this_simulation["buffer"] = "zero"
    this_simulation["shutoff"] = "reduce_breeding"
    this_simulation["cull"] = "do_eat_culled"
    this_simulation["meat_strategy"] = "reduce_breeding"

    # Set up ScenarioRunnerNoTrade object and run simulation
    scenario_runner = ScenarioRunnerNoTrade()

    scenario_runner.run_model_no_trade(
        title="Resilient foods for US only",
        create_pptx_with_all_countries=False,
        show_country_figures=True,
        show_map_figures=True,
        add_map_slide_to_pptx=False,
        scenario_option=this_simulation,
        countries_list=["USA"],
    )


def main(args):
    """
    This function is the entry point of the program. It takes in command line arguments and runs the AUS simulation
    with and without resilient features.

    Args:
        args (list): A list of command line arguments.

    Returns:
        None
    """
    run_AUS_with_and_without_resilient()


if __name__ == "__main__":
    # Get command line arguments
    args = sys.argv[1:]
    # Call main function with arguments
    main(args)
