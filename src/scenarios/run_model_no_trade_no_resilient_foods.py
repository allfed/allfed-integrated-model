"""
This file contains the code for the baseline model by country for with and
without trade scenarios.

Created on Wed Jul 15
@author: morgan
"""
import sys
from itertools import product
from src.scenarios.run_model_no_trade import ScenarioRunnerNoTrade


def run_nuclear_winter_by_country_no_trade(
    plot_map=True,
    show_figures=True,
    create_pptx_with_all_countries=True,
    scenario_option=[],
):

    # country_food_system
    #
    # excess zero
    # short_delayed_shutoff
    # global_waste_to_baseline_prices
    # baseline_nutrition_profile
    # stored_food_buffer_as_baseline
    # set_country_seasonality_nuclear_winter
    # fish_baseline
    # nuclear_winter_country_disruption_to_crops
    # include protein
    # include fat
    # don't include culled animals
    # get_no_resilient_food_scenario

    # now we have a list of all the options we want to test
    this_simulation = {}
    this_simulation["scale"] = "country"
    this_simulation["scenario"] = "no_resilient_food_nuclear_winter"
    this_simulation["seasonality"] = "nuclear_winter_in_country"
    this_simulation["crop_disruption"] = "country_nuclear_winter"
    this_simulation["fish"] = "nuclear_winter"

    this_simulation["fat"] = "not_required"
    this_simulation["protein"] = "not_required"
    this_simulation["waste"] = "baseline_in_country"
    this_simulation["nutrition"] = "catastrophe"
    this_simulation["buffer"] = "zero"
    this_simulation["shutoff"] = "short_delayed_shutoff"
    this_simulation["cull"] = "dont_eat_culled"

    scenario_runner = ScenarioRunnerNoTrade()

    scenario_runner.run_model_no_trade(
        create_pptx_with_all_countries=create_pptx_with_all_countries,
        show_figures=show_figures,
        add_map_slide_to_pptx=plot_map,
        scenario_option=this_simulation,
        countries_to_skip=["TWN"],  # taiwan doesn't have crop results
    )


def create_several_maps_with_different_assumptions():
    # initializing lists

    this_simulation_combinations = {}

    this_simulation_combinations["waste"] = [
        "baseline_in_country",
        "doubled_prices_in_country",
    ]

    this_simulation_combinations["buffer"] = ["baseline", "zero"]
    this_simulation_combinations["shutoff"] = [
        "continued",
        "long_delayed_shutoff",
    ]
    this_simulation_combinations["fat"] = ["required", "not_required"]
    this_simulation_combinations["protein"] = ["required", "not_required"]

    # this_simulation_combinations["waste"] = ["tripled_prices_in_country"]
    # this_simulation_combinations["nutrition"] = ["baseline"]
    # this_simulation_combinations["buffer"] = ["baseline"]
    # this_simulation_combinations["shutoff"] = ["continued"]
    # this_simulation_combinations["cull"] = ["dont_eat_culled"]

    # I don't really know why this works, but it certainly does.
    # I'm just combining things a lot like this example:

    # >>> kwargs = {'a': [1, 2, 3], 'b': [1, 2, 3]}
    # >>> flat = [[(k, v) for v in vs] for k, vs in kwargs.items()]
    # >>> flat
    # [[('b', 1), ('b', 2), ('b', 3)], [('a', 1), ('a', 2), ('a', 3)]]

    # >>> from itertools import product
    # >>> [dict(items) for items in product(*flat)]
    # [{'a': 1, 'b': 1},
    #  {'a': 2, 'b': 1},
    #  {'a': 3, 'b': 1},
    #  {'a': 1, 'b': 2},
    #  {'a': 2, 'b': 2},
    #  {'a': 3, 'b': 2},
    #  {'a': 1, 'b': 3},
    #  {'a': 2, 'b': 3},
    #  {'a': 3, 'b': 3}]

    # thanks to thefourtheye on stackoverflow
    # https://stackoverflow.com/questions/41254205/explode-a-dict-get-all-combinations-of-the-values-in-a-dictionary

    flat = [[(k, v) for v in vs] for k, vs in this_simulation_combinations.items()]

    options = [dict(items) for items in product(*flat)]

    # now we have a list of all the options we want to test
    defaults = {}
    defaults["nutrition"] = "catastrophe"
    defaults["scale"] = "country"
    defaults["seasonality"] = "nuclear_winter_in_country"
    defaults["crop_disruption"] = "country_nuclear_winter"
    defaults["fish"] = "baseline"
    defaults["scenario"] = "no_resilient_food_nuclear_winter"
    defaults["cull"] = "do_eat_culled"

    options_including_defaults = []
    for option in options:
        options_including_defaults.append(defaults | option)

    scenario_runner = ScenarioRunnerNoTrade()
    scenario_runner.run_many_options(
        scenario_options=options_including_defaults,
        title="nuclear winter no response",
        countries_to_skip=["TWN"],
    )


if __name__ == "__main__":

    print("arguments, all optional:")
    print("first: [single|multi] (single set of assumptions or multiple)")
    print("second: [pptx|no_pptx] (save a pptx report or not)")
    print("third: [no_plot|plot] (plots figures)")
    print("fourth: country_code (which country to run, if desired)")

    args = sys.argv[1:]
    if len(args) == 1:
        single_or_various = args[0]
        plot_figs = "no_plot"
        create_pptx = "pptx"
        country = "world"
    elif len(args) == 2:
        single_or_various = args[0]
        create_pptx = args[1]
        plot_figs = "no_plot"
        country = "world"
    elif len(args) == 3:
        single_or_various = args[0]
        create_pptx = args[1]
        plot_figs = args[2]
        country = "world"
    elif len(args) == 4:
        single_or_various = args[0]
        create_pptx = args[1]
        plot_figs = args[2]
        country = args[3]
    else:
        single_or_various = "single"
        create_pptx = "pptx"
        plot_figs = "no_plot"
        country = "world"

    CREATE_SEVERAL_MAPS_PPTX = single_or_various == "multi"
    if CREATE_SEVERAL_MAPS_PPTX:
        create_several_maps_with_different_assumptions()

    CREATE_PPTX_EACH_COUNTRY = single_or_various == "single"
    if CREATE_PPTX_EACH_COUNTRY:
        run_nuclear_winter_by_country_no_trade(
            plot_map=(create_pptx == "pptx"),
            show_figures=(plot_figs == "plot"),
            create_pptx_with_all_countries=(create_pptx == "pptx"),
        )
