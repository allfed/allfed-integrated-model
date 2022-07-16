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
from src.optimizer.optimizer import Optimizer
from src.utilities.plotter import Plotter
from src.optimizer.parameters import Parameters
from src.scenarios.scenarios import Scenarios


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

    constants_loader = Parameters()
    scenarios_loader = Scenarios()

    def run_optimizer_for_country(country_code, country_data):

        # initialize country specific food system properties
        inputs_to_optimizer = scenarios_loader.init_country_food_system_properties(
            country_data
        )

        inputs_to_optimizer = scenarios_loader.set_country_seasonality_baseline(
            inputs_to_optimizer, country_data
        )

        # set params that are true for baseline climate,
        # regardless of whether country or global scenario

        inputs_to_optimizer = scenarios_loader.get_baseline_scenario(
            inputs_to_optimizer
        )

        inputs_to_optimizer = scenarios_loader.set_baseline_nutrition_profile(
            inputs_to_optimizer
        )

        inputs_to_optimizer = scenarios_loader.set_stored_food_buffer_zero(
            inputs_to_optimizer
        )

        inputs_to_optimizer = scenarios_loader.set_fish_baseline(inputs_to_optimizer)

        inputs_to_optimizer = scenarios_loader.set_waste_to_zero(inputs_to_optimizer)

        inputs_to_optimizer = scenarios_loader.set_immediate_shutoff(
            inputs_to_optimizer
        )

        inputs_to_optimizer = scenarios_loader.set_disruption_to_crops_to_zero(
            inputs_to_optimizer
        )

        # No excess calories
        inputs_to_optimizer["EXCESS_CALORIES"] = np.array(
            [0] * inputs_to_optimizer["NMONTHS"]
        )

        constants = {}
        constants["inputs"] = inputs_to_optimizer

        print(country_name)

        (
            single_valued_constants,
            multi_valued_constants,
        ) = constants_loader.computeParameters(constants)
        single_valued_constants["CHECK_CONSTRAINTS"] = False
        optimizer = Optimizer()
        [time_months, time_months_middle, analysis] = optimizer.optimize(
            single_valued_constants, multi_valued_constants
        )

        needs_ratio = analysis.percent_people_fed / 100

        print("No trade expected kcals/capita/day 2020")
        print(needs_ratio * 2100)
        print("")

        if plot_figures:
            PLOT_EACH_FIGURE = False
            if PLOT_EACH_FIGURE:
                Plotter.plot_fig_s1abcd(analysis, analysis, 84)

        return needs_ratio

    def fill_data_for_map(country_code, needs_ratio):
        if country_code == "SWT":
            country_code_map = "SWZ"
        else:
            country_code_map = country_code

        country_map = world[world["iso_a3"].apply(
            lambda x: x == country_code_map
        )]

        if len(country_map) == 0:
            print("no match")
            print(country_code_map)

        if len(country_map) == 1:

            # cap at 100% fed, surplus is not traded away in this scenario
            kcals_ratio_capped = 1 if needs_ratio >= 1 else needs_ratio
            world_index = country_map.index
            world.loc[world_index, "needs_ratio"] = kcals_ratio_capped

    # iterate over each country from spreadsheet, run the optimizer, plot the result
    og_sum = 0
    for index, country_data in no_trade_table.iterrows():
        country_code = country_data["iso3"]
        country_name = country_data["country"]

        population = country_data["population"]
        
        # skip countries with no population
        if(np.isnan(population)):
            continue

        needs_ratio = run_optimizer_for_country(country_code, country_data)

        if country_code == "F5707+GBR":
            for c in UK_27_Plus_GBR_countries:
                fill_data_for_map(c, needs_ratio)
        else:
            fill_data_for_map(country_code, needs_ratio)

    plt.close()
    mn = 0
    mx = 1
    ax = world.plot(
        column="needs_ratio",
        legend=True,
        cmap="viridis",
        legend_kwds={"label": "Fraction Fed", "orientation": "horizontal"},
    )
    if plot_figures:
        pp = gplt.polyplot(world, ax=ax, zorder=1, linewidth=0.1)
        plt.title("Fraction of minimum macronutritional needs with no trade")
        plt.show()
        plt.close()


if __name__ == "__main__":
    run_baseline_by_country_no_trade()
