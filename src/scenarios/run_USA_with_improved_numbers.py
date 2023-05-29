"""
This file contains the code for the baseline model by country for with and
without trade scenarios.

Created on Wed Jul 15
@author: morgan
"""
import sys
from src.scenarios.run_model_no_trade import ScenarioRunnerNoTrade


def run_USA_with_and_without_resilient():
    """
    This function runs two simulations for the USA, one with resilient foods and one without.
    It sets the simulation parameters for each run and calls the ScenarioRunnerNoTrade class to run the simulation.
    """
    # Set simulation parameters for the first run with resilient foods
    this_simulation = {}
    this_simulation["scale"] = "country"
    this_simulation["scenario"] = "all_resilient_foods"
    this_simulation["seasonality"] = "no_seasonality"
    this_simulation["grasses"] = "country_nuclear_winter"
    this_simulation["crop_disruption"] = "country_nuclear_winter"
    this_simulation["fish"] = "nuclear_winter"
    this_simulation["waste"] = "zero"
    this_simulation["fat"] = "not_required"
    this_simulation["protein"] = "not_required"
    this_simulation["nutrition"] = "catastrophe"
    this_simulation["buffer"] = "zero"
    this_simulation["shutoff"] = "reduce_breeding"
    this_simulation["cull"] = "do_eat_culled"
    this_simulation["meat_strategy"] = "reduce_breeding"

    # Call the ScenarioRunnerNoTrade class to run the simulation with the above parameters
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

    # Set simulation parameters for the second run without resilient foods
    this_simulation["waste"] = "zero"
    this_simulation["scenario"] = "no_resilient_foods"

    # Call the ScenarioRunnerNoTrade class to run the simulation with the above parameters
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
    This function is the entry point of the program. It calls the function run_USA_with_and_without_resilient() to
    run the simulation with and without resilient measures.

    Args:
        args (list): A list of command line arguments.

    Returns:
        None
    """
    run_USA_with_and_without_resilient()


if __name__ == "__main__":
    args = sys.argv[1:]
    main(args)
