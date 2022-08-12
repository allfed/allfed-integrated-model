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


class ScenarioRunnerNoTrade(ScenarioRunner):
    """
    This function runs the model for all countries in the world, no trade.
    """

    def __init__(self):
        super().__init__()

    def run_optimizer_for_country(
        self,
        country_code,
        country_data,
        scenario_option,
        create_pptx_with_all_countries,
        show_figures,
    ):
        country_name = country_data["country"]

        constants_for_params, scenario_loader = self.set_depending_on_option(
            country_data, scenario_option
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

        USE_TRY_CATCH = True
        if USE_TRY_CATCH:
            try:
                scenario_runner = ScenarioRunner()
                interpreted_results = scenario_runner.run_and_analyze_scenario(
                    constants_for_params, scenario_loader
                )
                percent_people_fed = interpreted_results.percent_people_fed
            except Exception as e:
                # print("exception:")
                # print(e)
                percent_people_fed = np.nan
        else:
            scenario_runner = ScenarioRunner()
            interpreted_results = scenario_runner.run_and_analyze_scenario(
                constants_for_params, scenario_loader
            )
            percent_people_fed = interpreted_results.percent_people_fed

        if create_pptx_with_all_countries and not np.isnan(percent_people_fed):
            Plotter.plot_fig_1ab(
                interpreted_results,
                84,
                country_data["country"],
                show_figures,
                scenario_loader.scenario_description,
            )
        return (
            percent_people_fed / 100,
            scenario_loader.scenario_description,
        )

    def fill_data_for_map(self, world, country_code, needs_ratio):
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

    def run_model_no_trade(
        self,
        create_pptx_with_all_countries=True,
        show_figures=True,
        add_map_slide_to_pptx=True,
        scenario_option=[],
    ):
        if len(scenario_option) == 0:
            print("ERROR: a scenario must be specified")
            quit()
        if create_pptx_with_all_countries:
            import os

            if not os.path.exists("../../results/large_reports"):
                os.mkdir("../../results/large_reports")
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

        # iterate over each country from spreadsheet, run the optimizer, plot the result
        net_pop_fed = 0
        net_pop = 0
        scenario_description = ""
        n_errors = 0
        failed_countries = "Failed Countries: \n"
        for index, country_data in no_trade_table.iterrows():

            country_code = country_data["iso3"]
            # if country_code != "USA":
            #     continue

            population = country_data["population"]

            # skip countries with no population
            if np.isnan(population):
                continue

            needs_ratio, scenario_description = self.run_optimizer_for_country(
                country_code,
                country_data,
                scenario_option,
                create_pptx_with_all_countries,
                show_figures,
            )

            if np.isnan(needs_ratio):
                n_errors += 1
                country_name = country_data["country"]
                failed_countries += " " + country_name

                continue

            if country_code == "F5707+GBR":
                for c in UK_27_Plus_GBR_countries:
                    self.fill_data_for_map(world, c, needs_ratio)
            else:
                self.fill_data_for_map(world, country_code, needs_ratio)
            if needs_ratio >= 1:
                capped_ratio = 1
            else:
                capped_ratio = needs_ratio

            net_pop_fed += capped_ratio * population
            net_pop += population
        if net_pop > 0:
            ratio_fed = str(round(float(net_pop_fed) / float(net_pop), 4))
        else:
            ratio_fed = str(np.nan)
        print("Net population considered: " + str(net_pop / 1e9) + " Billion people")
        print("Fraction of this population fed: " + ratio_fed)
        print(scenario_description)
        print("")
        if n_errors > 0:
            print("Errors: " + str(n_errors))
            print(failed_countries)
        print("")
        print("")
        print("")
        if add_map_slide_to_pptx:
            Plotter.plot_map_of_countries_fed(
                world,
                ratio_fed,
                scenario_description,
                show_figures,
                add_map_slide_to_pptx,
            )
        if create_pptx_with_all_countries:
            Plotter.end_pptx(saveloc="../../results/large_reports/no_food_trade.pptx")

    def run_many_options(self, scenario_options, title):
        Plotter.start_pptx("Various Scenario Options " + title)
        print("Number of scenarios:")
        print(len(scenario_options))
        print("")
        print("")
        print("")
        scenario_number = 1
        for scenario_option in scenario_options:
            print("Scenario Number: " + str(scenario_number))
            scenario_number += 1
            self.run_model_no_trade(
                create_pptx_with_all_countries=False,
                show_figures=False,
                add_map_slide_to_pptx=True,
                scenario_option=scenario_option,
            )
        Plotter.end_pptx(
            saveloc="../../results/large_reports/various_scenario_options_"
            + title
            + ".pptx"
        )
