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
import geopandas as gpd
from itertools import product

module_path = os.path.abspath(os.path.join("../.."))
if module_path not in sys.path:
    sys.path.append(module_path)

# import some python files from this integrated model repository
from src.utilities.plotter import Plotter
from src.scenarios.scenarios import Scenarios
from src.scenarios.run_scenario import ScenarioRunner
from src.food_system.food import Food

import warnings
import logging

logging.basicConfig(level=logging.ERROR)
warnings.filterwarnings("ignore")


def run_baseline_by_country_no_trade(
    plot_map=True,
    show_figures=True,
    create_pptx_with_all_countries=True,
    scenario_option=[],
):
    if create_pptx_with_all_countries:
        Plotter.start_pptx("Baseline no trade")
    """
    Runs the baseline model by country and without trade

    Arguments:

    Returns:
        None
    """
    # country codes for UK + EU 27 countries (used for plotting map)
    UK_27_Plus_GBR_countries = [
        "GBR",
        "AUT",
        "BEL",
        "BGR",
        "HRV",
        "CYP",
        "CZE",
        "DNK",
        "EST",
        "FIN",
        "FRA",
        "DEU",
        "GRC",
        "HUN",
        "IRL",
        "ITA",
        "LVA",
        "LTU",
        "LUX",
        "MLT",
        "NLD",
        "POL",
        "PRT",
        "ROU",
        "SVK",
        "SVN",
        "ESP",
        "SWE",
    ]

    NO_TRADE_CSV = "../../data/no_food_trade/computer_readable_combined.csv"

    no_trade_table = pd.read_csv(NO_TRADE_CSV)

    # import the visual map
    world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))

    # oddly, some of these were -99
    world.loc[world.name == "France", "iso_a3"] = "FRA"
    world.loc[world.name == "Norway", "iso_a3"] = "NOR"
    world.loc[world.name == "Kosovo", "iso_a3"] = "KOS"

    def run_optimizer_for_country(country_code, country_data, scenario_option):
        if len(scenario_option) == 0:  # default
            scenario_loader = Scenarios()

            # initialize country specific food system properties
            constants_for_params = scenario_loader.init_country_food_system_properties(
                country_data
            )

            constants_for_params = scenario_loader.set_country_seasonality_baseline(
                constants_for_params, country_data
            )

            constants_for_params = scenario_loader.set_country_waste_to_doubled_prices(
                constants_for_params, country_data
            )

            # set params that are true for baseline climate,
            # regardless of whether country or global scenario

            constants_for_params = scenario_loader.get_baseline_climate_scenario(
                constants_for_params
            )

            constants_for_params = scenario_loader.set_catastrophe_nutrition_profile(
                constants_for_params
            )

            constants_for_params = scenario_loader.set_stored_food_buffer_zero(
                constants_for_params
            )

            constants_for_params = scenario_loader.set_excess_to_zero(
                constants_for_params
            )
            
            constants_for_params = scenario_loader.set_fish_baseline(
                constants_for_params
            )

            constants_for_params = scenario_loader.set_short_delayed_shutoff(
                constants_for_params
            )

            constants_for_params = scenario_loader.set_disruption_to_crops_to_zero(
                constants_for_params
            )
            constants_for_params = scenario_loader.include_protein(constants_for_params)

            constants_for_params = scenario_loader.include_fat(constants_for_params)

            constants_for_params = scenario_loader.dont_cull_animals(
                constants_for_params
            )

        else:
            constants_for_params, scenario_loader = set_depending_on_option(
                country_data, scenario_option
            )

        PRINT_COUNTRY = True
        if PRINT_COUNTRY:

            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print(country_name)
            print("")
            print("")
            print("")

        try:
            scenario_runner = ScenarioRunner()
            interpreted_results = scenario_runner.run_and_analyze_scenario(
                constants_for_params, scenario_loader
            )
            PLOT_EACH_FIGURE = create_pptx_with_all_countries or show_figures
            if PLOT_EACH_FIGURE:
                Plotter.plot_fig_1ab(
                    interpreted_results,
                    84,
                    country_data["country"],
                    show_figures,
                    "Mean fed:"+self.mean_fed+"\n"+scenario_loader.scenario_description,
                )
            percent_people_fed = interpreted_results.percent_people_fed
        except Exception as e:
            print("TERRIBLE FAILURE!")
            print(country_name)
            print("exception:")
            print(e)
            percent_people_fed = np.nan
            print("")
            print(scenario_loader.scenario_description)
            print("")
            print("")
        return (
            percent_people_fed / 100,
            scenario_loader.scenario_description,
        )

    def fill_data_for_map(country_code, needs_ratio):
        if country_code == "SWT":
            country_code_map = "SWZ"
        else:
            country_code_map = country_code

        country_map = world[world["iso_a3"].apply(lambda x: x == country_code_map)]

        if len(country_map) == 0:
            PRINT_NO_MATCH = False
            if PRINT_NO_MATCH:
                print("no match")
                print(country_code_map)

        if len(country_map) == 1:

            # cap at 100% fed, surplus is not traded away in this scenario
            kcals_ratio_capped = 1 if needs_ratio >= 1 else needs_ratio
            world_index = country_map.index
            world.loc[world_index, "needs_ratio"] = kcals_ratio_capped

    # iterate over each country from spreadsheet, run the optimizer, plot the result
    net_pop_fed = 0
    net_pop = 0
    scenario_description = ""
    for index, country_data in no_trade_table.iterrows():

        country_code = country_data["iso3"]
        # if country_code != "USA":
        #     continue
        country_name = country_data["country"]

        population = country_data["population"]

        # skip countries with no population
        if np.isnan(population):
            continue

        needs_ratio, scenario_description = run_optimizer_for_country(
            country_code, country_data, scenario_option
        )

        if np.isnan(needs_ratio):
            continue

        if country_code == "F5707+GBR":
            for c in UK_27_Plus_GBR_countries:
                fill_data_for_map(c, needs_ratio)
        else:
            fill_data_for_map(country_code, needs_ratio)
        if needs_ratio >= 1:
            capped_ratio = 1
        else:
            capped_ratio = needs_ratio

        net_pop_fed += capped_ratio * population
        net_pop += population
    ratio_fed = str(round(float(net_pop_fed) / float(net_pop), 4))

    print("Net population considered: " + str(net_pop / 1e9) + " Billion people")
    print("Fraction of this population fed: " + ratio_fed)
    print(scenario_description)
    print("")
    if plot_map:
        Plotter.plot_map_of_countries_fed(
            world,
            ratio_fed,
            scenario_description,
            show_figures,
            create_pptx_with_all_countries,
        )
    if create_pptx_with_all_countries:
        Plotter.end_pptx(saveloc="../../results/large_reports/no_food_trade.pptx")


def set_depending_on_option(country_data, scenario_option):
    scenario_loader = Scenarios()

    # initialize country specific food system properties
    constants_for_params = scenario_loader.init_country_food_system_properties(
        country_data
    )

    constants_for_params = scenario_loader.set_country_seasonality_baseline(
        constants_for_params, country_data
    )

    constants_for_params = scenario_loader.get_baseline_climate_scenario(
        constants_for_params
    )

    constants_for_params = scenario_loader.set_disruption_to_crops_to_zero(
        constants_for_params
    )

    constants_for_params = scenarios_loader.set_excess_to_zero(
        constants_for_params
    )

    constants_for_params = scenario_loader.include_fat(constants_for_params)
    constants_for_params = scenario_loader.include_protein(constants_for_params)

    constants_for_params = scenario_loader.set_fish_baseline(constants_for_params)
    if scenario_option["prices"] == "catastrophe_expected":
        constants_for_params = scenario_loader.set_country_waste_to_doubled_prices(
            constants_for_params, country_data
        )
    elif scenario_option["prices"] == "more_like_baseline":
        constants_for_params = scenario_loader.set_country_waste_to_baseline_prices(
            constants_for_params, country_data
        )

    if scenario_option["nutrition"] == "catastrophe_expected":
        constants_for_params = scenario_loader.set_catastrophe_nutrition_profile(
            constants_for_params
        )
    elif scenario_option["nutrition"] == "more_like_baseline":
        constants_for_params = scenario_loader.set_baseline_nutrition_profile(
            constants_for_params
        )

    if scenario_option["buffer"] == "catastrophe_expected":
        constants_for_params = scenario_loader.set_stored_food_buffer_zero(
            constants_for_params
        )
    elif scenario_option["buffer"] == "more_like_baseline":
        constants_for_params = scenario_loader.set_stored_food_buffer_as_baseline(
            constants_for_params
        )

    if scenario_option["shutoff"] == "catastrophe_expected":
        constants_for_params = scenario_loader.set_short_delayed_shutoff(
            constants_for_params
        )
    elif scenario_option["shutoff"] == "more_like_baseline":
        constants_for_params = scenario_loader.set_continued_feed_biofuels(
            constants_for_params
        )

    if scenario_option["cull"] == "catastrophe_expected":
        constants_for_params = scenario_loader.cull_animals(constants_for_params)
    elif scenario_option["cull"] == "more_like_baseline":
        constants_for_params = scenario_loader.dont_cull_animals(constants_for_params)

    return constants_for_params, scenario_loader


def create_several_maps_with_different_assumptions():
    # initializing lists
    properties = ["prices", "nutrition", "buffer", "shutoff", "cull"]
    outcomes = ["catastrophe_expected", "more_like_baseline"]

    temp = product(outcomes, repeat=len(properties))
    options = [{key: val for (key, val) in zip(properties, ele)} for ele in temp]

    Plotter.start_pptx("Various Scenario Options")
    for option in options:

        run_baseline_by_country_no_trade(
            plot_map=True,
            show_figures=False,
            create_pptx_with_all_countries=False,
            scenario_option=option,
        )
        # break
    Plotter.end_pptx(
        saveloc="../../results/large_reports/various_scenario_options.pptx"
    )


if __name__ == "__main__":
    CREATE_SEVERAL_MAPS_PPTX = False

    if CREATE_SEVERAL_MAPS_PPTX:
        create_several_maps_with_different_assumptions()

    CREATE_PPTX_EACH_COUNTRY = True
    if CREATE_PPTX_EACH_COUNTRY:
        run_baseline_by_country_no_trade(
            plot_map=True,
            show_figures=False,
            create_pptx_with_all_countries=True,
            scenario_option=[],
        )
