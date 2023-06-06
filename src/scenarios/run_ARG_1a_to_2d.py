"""
This file contains the code for running a set of useful scenarios for Argentina.
In particular, we analyze in some detail how each contribution of availabilities
changes the picture overall for argentina.

Created on Wed Jul 15
@author: morgan
"""
import sys
from src.scenarios.run_model_no_trade import ScenarioRunnerNoTrade


def run_ARG_net_baseline():
    """
    Runs a simulation for Argentina's net food production under baseline climate conditions.
    The function sets up the simulation parameters, prints some information about the simulation,
    and then runs the simulation using the ScenarioRunnerNoTrade class.

    Args:
        None

    Returns:
        None
    """

    # Set up simulation parameters
    this_simulation = {}
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
    this_simulation["fat"] = "not_required"
    this_simulation["protein"] = "not_required"
    this_simulation["meat_strategy"] = "efficient_meat_strategy"

    # Print some information about the simulation
    print("")
    print("")
    print("")
    print("")
    print("Argentina Net Food Production, Baseline Climate")
    print("(Feed and waste subtracted from production)")
    print("")

    # Run the simulation using the ScenarioRunnerNoTrade class
    scenario_runner = ScenarioRunnerNoTrade()
    scenario_runner.run_model_no_trade(
        title="Argentina Net Food Production",
        create_pptx_with_all_countries=False,
        show_country_figures=True,
        show_map_figures=False,
        add_map_slide_to_pptx=False,
        scenario_option=this_simulation,
        countries_list=["ARG"],  # runs all the countries if empty
        figure_save_postfix="_1a",
        return_results=False,
    )


def run_ARG_gross_baseline():
    """
    Runs a simulation for Argentina's gross food production with baseline climate.
    Feed and waste are NOT subtracted from production.
    """
    # Define simulation parameters
    this_simulation = {}
    this_simulation["scale"] = "country"
    this_simulation["seasonality"] = "country"
    this_simulation["grasses"] = "baseline"
    this_simulation["crop_disruption"] = "zero"
    this_simulation["scenario"] = "no_resilient_foods"
    this_simulation["fish"] = "baseline"
    this_simulation["waste"] = "zero"
    this_simulation["nutrition"] = "baseline"
    this_simulation["buffer"] = "baseline"
    this_simulation["shutoff"] = "immediate"
    this_simulation["cull"] = "dont_eat_culled"
    this_simulation["fat"] = "not_required"
    this_simulation["protein"] = "not_required"
    this_simulation["meat_strategy"] = "efficient_meat_strategy"

    # Print empty lines for formatting
    print("")
    print("")
    print("")
    print("")

    # Print simulation information
    print("Argentina Gross Food Production, Baseline Climate")
    print("(Feed and waste NOT subtracted from production)")
    print("")

    # Run simulation
    # command line argument inputs (optional)
    scenario_runner = ScenarioRunnerNoTrade()
    scenario_runner.run_model_no_trade(
        title="Argentina Net Food Production",
        create_pptx_with_all_countries=False,
        show_country_figures=True,
        show_map_figures=False,
        add_map_slide_to_pptx=False,
        scenario_option=this_simulation,
        countries_list=["ARG"],  # runs all the countries if empty
        figure_save_postfix="_1b",
        return_results=False,
    )


def run_ARG_net_nuclear_winter():
    """
    Runs a simulation for Argentina's net food production during a nuclear winter catastrophe.
    The function sets up a dictionary of simulation parameters, prints a header, and then runs
    the simulation using the ScenarioRunnerNoTrade class.

    Args:
        None

    Returns:
        None
    """
    # Set up simulation parameters
    this_simulation = {}
    this_simulation["scale"] = "country"
    this_simulation["scenario"] = "no_resilient_foods"
    this_simulation["seasonality"] = "country"
    this_simulation["grasses"] = "country_nuclear_winter"
    this_simulation["crop_disruption"] = "country_nuclear_winter"
    this_simulation["fish"] = "nuclear_winter"
    this_simulation["waste"] = "baseline_in_country"
    this_simulation["fat"] = "not_required"
    this_simulation["protein"] = "not_required"
    this_simulation["nutrition"] = "catastrophe"
    this_simulation["buffer"] = "zero"
    this_simulation["shutoff"] = "continued"
    this_simulation["cull"] = "do_eat_culled"
    this_simulation["meat_strategy"] = "efficient_meat_strategy"

    # Print header
    print("")
    print("")
    print("")
    print("")
    print("Argentina Net Food Production, Nuclear Winter")
    print("(Unaltered feed and unaltered waste subtracted from production)")
    print("")

    # Run simulation using ScenarioRunnerNoTrade class
    # command line argument inputs (optional)
    scenario_runner = ScenarioRunnerNoTrade()

    scenario_runner.run_model_no_trade(
        title="Argentina Net Food Production, Nuclear Winter",
        create_pptx_with_all_countries=False,
        show_country_figures=True,
        show_map_figures=True,
        add_map_slide_to_pptx=False,
        scenario_option=this_simulation,
        countries_list=["ARG"],
        figure_save_postfix="_2a",
        return_results=False,
    )


def run_ARG_net_nuclear_winter_reduced_feed_waste():
    """
    Runs a simulation for Argentina's net food production during a nuclear winter with reduced feed and waste.
    Prints the simulation title and command line argument inputs.
    """
    # Define simulation parameters
    this_simulation = {}
    this_simulation["scale"] = "country"
    this_simulation["scenario"] = "no_resilient_foods"
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
    this_simulation["meat_strategy"] = "efficient_meat_strategy"

    # Print empty lines for spacing
    print("")
    print("")
    print("")
    print("")

    # Print simulation title
    print("Argentina Net Food Production, Nuclear Winter, Reduced waste and feed")
    print("(Reduced feed and reduced waste subtracted from production)")
    print("")

    # Run simulation with command line argument inputs (optional)
    scenario_runner = ScenarioRunnerNoTrade()
    scenario_runner.run_model_no_trade(
        title="Argentina Net Food Production, Nuclear Winter, Reduced Waste",
        create_pptx_with_all_countries=False,
        show_country_figures=True,
        show_map_figures=True,
        add_map_slide_to_pptx=False,
        scenario_option=this_simulation,
        countries_list=["ARG"],
        figure_save_postfix="_2b",
        return_results=False,
    )


def run_ARG_net_nuclear_winter_reduced_feed_waste_resilient():
    """
    Runs a simulation for Argentina's net food production during a nuclear winter, with reduced feed and waste, and
    resilient foods. Prints the simulation inputs and outputs.

    Args:
        None

    Returns:
        None
    """

    # Define the simulation inputs
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
    this_simulation["meat_strategy"] = "efficient_meat_strategy"

    # Print blank lines for readability
    print("")
    print("")
    print("")
    print("")

    # Print the simulation title and description
    print("Argentina Net Food Production, Nuclear Winter, Resilient Foods")
    print(
        "(Reduced feed and reduced waste subtracted from production, with resilient foods)"
    )
    print("")

    # Run the simulation using the ScenarioRunnerNoTrade class
    scenario_runner = ScenarioRunnerNoTrade()
    scenario_runner.run_model_no_trade(
        title="Argentina Net Food Production, Resilient Foods",
        create_pptx_with_all_countries=False,
        show_country_figures=True,
        show_map_figures=True,
        add_map_slide_to_pptx=False,
        scenario_option=this_simulation,
        countries_list=["ARG"],
        figure_save_postfix="_2c",
        return_results=False,
    )


def run_ARG_net_nuclear_winter_reduced_feed_waste_resilient_more_area():
    """
    This function sets up a simulation for Argentina's net food production during a nuclear winter.
    It reduces feed and waste, increases resilient foods, and sets other parameters for the simulation.
    It then runs the simulation using the ScenarioRunnerNoTrade class.

    Args:
        None

    Returns:
        None
    """

    # Set up simulation parameters
    this_simulation = {}

    this_simulation["scale"] = "country"
    this_simulation["scenario"] = "all_resilient_foods_and_more_area"
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
    this_simulation["meat_strategy"] = "efficient_meat_strategy"

    # Print simulation information
    print("")
    print("")
    print("")
    print("")

    print("Argentina Net Food Production, Nuclear Winter")
    print(
        "(Reduced feed and reduced waste subtracted from production, with increased resilient foods)"
    )
    print("")

    # Run simulation
    # command line argument inputs (optional)
    scenario_runner = ScenarioRunnerNoTrade()

    scenario_runner.run_model_no_trade(
        title="Argentina Net Food Production, Resilient Foods",
        create_pptx_with_all_countries=False,
        show_country_figures=True,
        show_map_figures=True,
        add_map_slide_to_pptx=False,
        scenario_option=this_simulation,
        countries_list=["ARG"],
        figure_save_postfix="_2d",
        return_results=False,
    )


def main(args):
    """
    This function runs the different scenarios for the ARG model. It is called with a list of arguments.
    The different scenarios are commented out, and only the last one is currently being run.
    """
    run_ARG_net_baseline()  # Run the baseline scenario for net food production
    run_ARG_gross_baseline()  # Run the baseline scenario for gross food production
    # run_ARG_net_nuclear_winter()  # Run the scenario for net food production during a nuclear winter
    run_ARG_net_nuclear_winter_reduced_feed_waste()  # Run the scenario for net food production during a nuclear winter with reduced feed and waste
    run_ARG_net_nuclear_winter_reduced_feed_waste_resilient()  # Run the scenario for net food production during a nuclear winter with reduced feed and waste and increased resilience
    run_ARG_net_nuclear_winter_reduced_feed_waste_resilient_more_area()  # Run the scenario for net food production during a nuclear winter with reduced feed and waste, increased resilience, and more area


if __name__ == "__main__":
    args = sys.argv[1:]
    main(args)
