#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""     
This file contains the code for the baseline model by country for with and 
without trade scenarios.

Created on Wed Jul 15
@author: morgan
"""
import pandas as pd
import numpy as np
import os
import sys
import matplotlib.pyplot as plt
import itertools
from itertools import product

module_path = os.path.abspath(os.path.join("../.."))
if module_path not in sys.path:
    sys.path.append(module_path)

# import some python files from this integrated model repository
from src.scenarios.run_model_no_trade import ScenarioRunnerNoTrade


def run_baseline_by_country_no_trade(
    plot_map=True,
    show_figures=True,
    create_pptx_with_all_countries=True,
    scenario_option=[],
):
    # Scenario properties:
    #
    # country_food_system
    # country_seasonality_baseline
    # disruption_to_crops_to_zero
    # include fat
    # include protein
    # fish_baseline
    # country_waste_to_baseline_prices
    # baseline_nutrition_profile
    # stored_food_buffer_as_baseline
    # continued_feed_biofuels
    # don't include culled animals

    # now we have a list of all the options we want to test
    this_simulation = {}
    this_simulation["scale"] = "country"
    this_simulation["seasonality"] = "baseline_in_country"
    this_simulation["crop_disruption"] = "zero"
    this_simulation["scenario"] = "baseline_climate"
    this_simulation["fish"] = "baseline"

    this_simulation["waste"] = "doubled_prices_in_country"
    this_simulation["fat"] = "not_required"
    this_simulation["protein"] = "not_required"
    this_simulation["nutrition"] = "catastrophe"
    this_simulation["buffer"] = "zero"
    this_simulation["shutoff"] = "short_delayed_shutoff"
    this_simulation["cull"] = "do_eat_culled"

    scenario_runner = ScenarioRunnerNoTrade()

    scenario_runner.run_model_no_trade(
        create_pptx_with_all_countries=create_pptx_with_all_countries,
        show_figures=show_figures,
        add_map_slide_to_pptx=plot_map,
        scenario_option=this_simulation,
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

    # # one example set of assumptions
    # this_simulation_combinations["nutrition"] = ["baseline"]
    # this_simulation_combinations["buffer"] = ["baseline"]
    # this_simulation_combinations["shutoff"] = ["continued"]
    # this_simulation_combinations["cull"] = ["dont_eat_culled"]

    # I don't really know why this works, but it certainly does.
    # I'm just combining things a lot like this example:
    #
    # >>> kwargs = {'a': [1, 2, 3], 'b': [1, 2, 3]}
    # >>> flat = [[(k, v) for v in vs] for k, vs in kwargs.items()]
    # >>> flat
    # [[('b', 1), ('b', 2), ('b', 3)], [('a', 1), ('a', 2), ('a', 3)]]
    #
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
    defaults["seasonality"] = "baseline_in_country"
    defaults["crop_disruption"] = "zero"
    defaults["fish"] = "baseline"
    defaults["scenario"] = "baseline_climate"
    defaults["cull"] = "do_eat_culled"

    options_including_defaults = []
    for option in options:
        options_including_defaults.append(defaults | option)

    scenario_runner = ScenarioRunnerNoTrade()
    scenario_runner.run_many_options(
        scenario_options=options_including_defaults, title="baseline"
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
        run_baseline_by_country_no_trade(
            plot_map=(create_pptx == "pptx"),
            show_figures=(plot_figs == "plot"),
            create_pptx_with_all_countries=(create_pptx == "pptx"),
        )
