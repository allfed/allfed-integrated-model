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
    # now we have a list of all the options we want to test
    this_simulation = {}
    this_simulation["scale"] = "country"
    this_simulation["seasonality"] = "nuclear_winter_in_country"
    this_simulation["fat"] = "required"
    this_simulation["protein"] = "required"
    this_simulation["crop_disruption"] = "zero"
    this_simulation["fish"] = "baseline"

    this_simulation["waste"] = "doubled_prices_in_country"

    this_simulation["nutrition"] = "catastrophe"

    this_simulation["buffer"] = "none"

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

    # this_simulation_combinations["waste"] = [
    #     "baseline_country_in_country",
    #     "doubled_prices_in_country",
    # ]

    # this_simulation_combinations["nutrition"] = ["baseline", "catastrophe"]

    # this_simulation_combinations["buffer"] = ["baseline", "none"]

    # this_simulation_combinations["shutoff"] = ["continued", "short_delayed_shutoff"]

    # this_simulation_combinations["cull"] = ["dont_eat_culled", "do_eat_culled"]

    this_simulation_combinations["waste"] = ["baseline_country_in_country"]

    this_simulation_combinations["nutrition"] = ["baseline"]

    this_simulation_combinations["buffer"] = ["baseline"]

    this_simulation_combinations["shutoff"] = ["continued"]

    this_simulation_combinations["cull"] = ["dont_eat_culled"]

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
    defaults["scale"] = "country"
    defaults["seasonality"] = "baseline_in_country"
    defaults["fat"] = "required"
    defaults["protein"] = "required"
    defaults["crop_disruption"] = "zero"
    defaults["fish"] = "baseline"

    options_including_defaults = []
    for option in options:
        options_including_defaults.append(defaults | option)

    scenario_runner.run_many_options(
        scenario_options=options_including_defaults, title="baseline"
    )


if __name__ == "__main__":
    CREATE_SEVERAL_MAPS_PPTX = True
    scenario_runner = ScenarioRunnerNoTrade()
    if CREATE_SEVERAL_MAPS_PPTX:
        create_several_maps_with_different_assumptions()

    CREATE_PPTX_EACH_COUNTRY = False
    if CREATE_PPTX_EACH_COUNTRY:
        scenario_runner.run_model_no_trade(
            plot_map=True,
            show_figures=False,
            create_pptx_with_all_countries=True,
            scenario_option=[],
        )
