"""
This file contains the code for running a set of useful scenarios for Argentina.
In particular, we analyze in some detail how each contribution of availabilities
changes the picture overall for argentina.

Created on Wed Jul 15
@author: morgan
"""
import sys
from src.scenarios.run_model_no_trade import ScenarioRunnerNoTrade


def run_ARG_net_baseline(show_country_figures, show_map_figures):
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

    print("")
    print("")
    print("")
    print("")

    print("Argentina Net Food Production, Baseline Climate")
    print("(Feed and waste subtracted from production)")
    print("")
    # command line argument inputs (optional)
    scenario_runner = ScenarioRunnerNoTrade()
    scenario_runner.run_model_no_trade(
        title="Argentina Net Food Production",
        create_pptx_with_all_countries=False,
        show_country_figures=show_country_figures,
        show_map_figures=show_map_figures,
        add_map_slide_to_pptx=False,
        scenario_option=this_simulation,
        countries_list=["ARG"],  # runs all the countries if empty
        figure_save_postfix="_1a",
        return_results=False,
    )


def run_ARG_gross_baseline(show_country_figures, show_map_figures):
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

    print("")
    print("")
    print("")
    print("")

    print("Argentina Gross Food Production, Baseline Climate")
    print("(Feed and waste NOT subtracted from production)")
    print("")
    # command line argument inputs (optional)
    scenario_runner = ScenarioRunnerNoTrade()
    scenario_runner.run_model_no_trade(
        title="Argentina Net Food Production",
        create_pptx_with_all_countries=False,
        show_country_figures=show_country_figures,
        show_map_figures=show_map_figures,
        add_map_slide_to_pptx=False,
        scenario_option=this_simulation,
        countries_list=["ARG"],  # runs all the countries if empty
        figure_save_postfix="_1b",
        return_results=False,
    )


def run_ARG_net_nuclear_winter(show_country_figures, show_map_figures):
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

    print("")
    print("")
    print("")
    print("")

    print("Argentina Net Food Production, Nuclear Winter")
    print("(Unaltered feed and unaltered waste subtracted from production)")
    print("")

    # command line argument inputs (optional)
    scenario_runner = ScenarioRunnerNoTrade()

    scenario_runner.run_model_no_trade(
        title="Argentina Net Food Production, Nuclear Winter",
        create_pptx_with_all_countries=False,
        show_country_figures=show_country_figures,
        show_map_figures=show_map_figures,
        add_map_slide_to_pptx=False,
        scenario_option=this_simulation,
        countries_list=["ARG"],
        figure_save_postfix="_2a",
        return_results=False,
    )


def run_ARG_net_nuclear_winter_reduced_feed_waste(
    show_country_figures, show_map_figures
):
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
    this_simulation["shutoff"] = "reduce_breeding_USA"
    this_simulation["cull"] = "do_eat_culled"
    this_simulation["meat_strategy"] = "efficient_meat_strategy"

    print("")
    print("")
    print("")
    print("")

    print("Argentina Net Food Production, Nuclear Winter, Reduced waste and feed")
    print("(Reduced feed and reduced waste subtracted from production)")
    print("")

    # command line argument inputs (optional)
    scenario_runner = ScenarioRunnerNoTrade()

    scenario_runner.run_model_no_trade(
        title="Argentina Net Food Production, Nuclear Winter, Reduced Waste",
        create_pptx_with_all_countries=False,
        show_country_figures=show_country_figures,
        show_map_figures=show_map_figures,
        add_map_slide_to_pptx=False,
        scenario_option=this_simulation,
        countries_list=["ARG"],
        figure_save_postfix="_2b",
        return_results=False,
    )


def run_ARG_net_nuclear_winter_reduced_feed_waste_resilient(
    show_country_figures, show_map_figures
):
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
    this_simulation["shutoff"] = "reduce_breeding_USA"
    this_simulation["cull"] = "do_eat_culled"
    this_simulation["meat_strategy"] = "efficient_meat_strategy"

    print("")
    print("")
    print("")
    print("")

    print("Argentina Net Food Production, Nuclear Winter, Resilient Foods")
    print(
        "(Reduced feed and reduced waste subtracted from production, with resilient foods)"
    )
    print("")

    # command line argument inputs (optional)
    scenario_runner = ScenarioRunnerNoTrade()

    scenario_runner.run_model_no_trade(
        title="Argentina Net Food Production, Resilient Foods",
        create_pptx_with_all_countries=False,
        show_country_figures=show_country_figures,
        show_map_figures=show_map_figures,
        add_map_slide_to_pptx=False,
        scenario_option=this_simulation,
        countries_list=["ARG"],
        figure_save_postfix="_2c",
        return_results=False,
    )


def run_ARG_net_nuclear_winter_reduced_feed_waste_resilient_more_area(
    show_country_figures, show_map_figures
):
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
    this_simulation["shutoff"] = "reduce_breeding_USA"
    this_simulation["cull"] = "do_eat_culled"
    this_simulation["meat_strategy"] = "efficient_meat_strategy"

    print("")
    print("")
    print("")
    print("")

    print("Argentina Net Food Production, Nuclear Winter")
    print(
        "(Reduced feed and reduced waste subtracted from production, with increased resilient foods)"
    )
    print("")

    # command line argument inputs (optional)
    scenario_runner = ScenarioRunnerNoTrade()
    scenario_runner.run_model_no_trade(
        title="Argentina Net Food Production, Resilient Foods",
        create_pptx_with_all_countries=False,
        show_country_figures=show_country_figures,
        show_map_figures=show_map_figures,
        add_map_slide_to_pptx=False,
        scenario_option=this_simulation,
        countries_list=["ARG"],
        figure_save_postfix="_2d",
        return_results=False,
    )


def main(args):
    print(
        "USAGE: first arg to True to show country figures, second to show colored map"
    )
    print()
    if not args or len(args) < 2:
        if len(args) == 1:
            args = [args[0], "False"]
        else:
            args = ["True", "False"]
    run_ARG_net_baseline(
        show_country_figures=args[0] == "True", show_map_figures=args[1] == "True"
    )
    run_ARG_gross_baseline(
        show_country_figures=args[0] == "True", show_map_figures=args[1] == "True"
    )
    run_ARG_net_nuclear_winter(
        show_country_figures=args[0] == "True", show_map_figures=args[1] == "True"
    )
    run_ARG_net_nuclear_winter_reduced_feed_waste(
        show_country_figures=args[0] == "True", show_map_figures=args[1] == "True"
    )
    run_ARG_net_nuclear_winter_reduced_feed_waste_resilient(
        show_country_figures=args[0] == "True", show_map_figures=args[1] == "True"
    )
    run_ARG_net_nuclear_winter_reduced_feed_waste_resilient_more_area(
        show_country_figures=args[0] == "True", show_map_figures=args[1] == "True"
    )


if __name__ == "__main__":
    args = sys.argv[1:]
    main(args)
