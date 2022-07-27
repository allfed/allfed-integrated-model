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
import geoplot as gplt

module_path = os.path.abspath(os.path.join("../.."))
if module_path not in sys.path:
    sys.path.append(module_path)

# import some python files from this integrated model repository
from src.utilities.plotter import Plotter
from src.scenarios.scenarios import Scenarios
from src.scenarios.run_scenario import ScenarioRunner
from src.food_system.food import Food


def run_baseline_by_country_no_trade(plot_figures=True):
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

    def run_optimizer_for_country(country_code, country_data):

        if country_code == "BRB":
            return np.nan
        #     country_code == "USA"
        #     or country_code == "CHN"
        #     or country_code == "AUS"
        #     or country_code == "IND"
        #     or country_code == "PAK"
        #     or country_code == "BRA"
        #     or country_code == "F5707+GBR"
        # ):
        #     return np.nan
        scenarios_loader = Scenarios()

        # initialize country specific food system properties
        constants_for_params = scenarios_loader.init_country_food_system_properties(
            country_data
        )

        constants_for_params = scenarios_loader.set_country_seasonality_baseline(
            constants_for_params, country_data
        )

        constants_for_params = scenarios_loader.set_country_waste_to_doubled_prices(
            constants_for_params, country_data
        )

        # set params that are true for baseline climate,
        # regardless of whether country or global scenario

        constants_for_params = scenarios_loader.get_baseline_climate_scenario(
            constants_for_params
        )

        constants_for_params = scenarios_loader.set_catastrophe_nutrition_profile(
            constants_for_params
        )

        constants_for_params = scenarios_loader.set_stored_food_buffer_zero(
            constants_for_params
        )

        constants_for_params = scenarios_loader.set_fish_baseline(constants_for_params)

        constants_for_params = scenarios_loader.set_short_delayed_shutoff(
            constants_for_params
        )

        constants_for_params = scenarios_loader.set_disruption_to_crops_to_zero(
            constants_for_params
        )

        # No excess calories

        # No excess calories
        constants_for_params["EXCESS_FEED"] = Food(
            kcals=[0] * constants_for_params["NMONTHS"],
            fat=[0] * constants_for_params["NMONTHS"],
            protein=[0] * constants_for_params["NMONTHS"],
            kcals_units="billion kcals each month",
            fat_units="thousand tons each month",
            protein_units="thousand tons each month",
        )

        print(country_name)

        scenario_runner = ScenarioRunner()
        interpreted_results = scenario_runner.run_and_analyze_scenario(
            constants_for_params, scenarios_loader
        )

        if plot_figures:
            PLOT_EACH_FIGURE = False
            if PLOT_EACH_FIGURE:
                Plotter.plot_fig_s1abcd(interpreted_results, interpreted_results, 84)
        print("")
        print("")
        print("")
        return interpreted_results.percent_people_fed / 100

    def fill_data_for_map(country_code, needs_ratio):
        if country_code == "SWT":
            country_code_map = "SWZ"
        else:
            country_code_map = country_code

        country_map = world[world["iso_a3"].apply(lambda x: x == country_code_map)]

        if len(country_map) == 0:
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
    for index, country_data in no_trade_table.iterrows():

        country_code = country_data["iso3"]
        country_name = country_data["country"]

        population = country_data["population"]

        # skip countries with no population
        if np.isnan(population):
            continue

        needs_ratio = run_optimizer_for_country(country_code, country_data)

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
    print("")
    if plot_figures:
        Plotter.plot_map_of_countries_fed()


if __name__ == "__main__":
    run_baseline_by_country_no_trade()
