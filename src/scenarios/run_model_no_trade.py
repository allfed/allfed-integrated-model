"""
This file contains the code for the baseline model by country for with and
without trade scenarios.

Created on Wed Jul 15
@author: morgan
"""
import pandas as pd
import os
import numpy as np
import geopandas as gpd
import warnings
import logging
import datetime
from datetime import date
from src.utilities.plotter import Plotter
from src.scenarios.run_scenario import ScenarioRunner
from src.food_system.food import Food
from itertools import product
import git
from pathlib import Path

repo_root = git.Repo(".", search_parent_directories=True).working_dir


logging.basicConfig(level=logging.ERROR)
warnings.filterwarnings("ignore")


class ScenarioRunnerNoTrade(ScenarioRunner):
    """
    This function runs the model for all countries in the world, no trade.
    """

    def __init__(self):
        super().__init__()

    def run_model_defaults_no_trade(
        self,
        this_simulation,
        show_map_figures=False,
        show_country_figures=False,
        create_pptx_with_all_countries=False,
        scenario_option=[],
    ):
        """
        Set a few options to set on top of the specific options for the given simulation
        These could easily change if another scenario was of more interest.
        """
        if "fat" not in this_simulation.keys():
            this_simulation["fat"] = "not_required"
        if "protein" not in this_simulation.keys():
            this_simulation["fat"] = "not_required"

        if "waste" not in this_simulation.keys():
            this_simulation["waste"] = "zero"
        if "nutrition" not in this_simulation.keys():
            this_simulation["nutrition"] = "baseline"
        if "buffer" not in this_simulation.keys():
            this_simulation["buffer"] = "baseline"
        if "shutoff" not in this_simulation.keys():
            this_simulation[
                "shutoff"
            ] = "continued"  # this_simulation["shutoff"] = "immediate"
        if "cull" not in this_simulation.keys():
            this_simulation["cull"] = "do_eat_culled"

        self.run_model_no_trade(
            title=this_simulation["scenario"] + "_" + this_simulation["fish"],
            create_pptx_with_all_countries=create_pptx_with_all_countries,
            show_country_figures=show_country_figures,
            show_map_figures=show_map_figures,
            add_map_slide_to_pptx=show_map_figures and create_pptx_with_all_countries,
            scenario_option=this_simulation,
            countries_list=[
                "!SWT",
                "!GBR",
                "!AUT",
                "!BEL",
                "!BGR",
                "!HRV",
                "!CYP",
                "!CZE",
                "!DNK",
                "!EST",
                "!FIN",
                "!FRA",
                "!DEU",
                "!GRC",
                "!HUN",
                "!IRL",
                "!ITA",
                "!LVA",
                "!LTU",
                "!LUX",
                "!MLT",
                "!NLD",
                "!POL",
                "!PRT",
                "!ROU",
                "!SVK",
                "!SVN",
                "!ESP",
                "!SWE",
            ],
        )

    def run_optimizer_for_country(
        self,
        country_data,
        scenario_option,
        create_pptx_with_all_countries,
        show_country_figures,
        figure_save_postfix="",
    ):
        country_name = country_data["country"]
        constants_for_params, scenario_loader = self.set_depending_on_option(
            country_data, scenario_option
        )

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

        USE_TRY_CATCH = False
        if USE_TRY_CATCH:
            try:
                print("running scenario")
                scenario_runner = ScenarioRunner()
                interpreted_results = scenario_runner.run_and_analyze_scenario(
                    constants_for_params,
                    scenario_loader,
                    create_pptx_with_all_countries,
                    show_country_figures,
                    figure_save_postfix,
                    country_data,
                )
                percent_people_fed = interpreted_results.percent_people_fed
            except Exception as e:
                print("exception:")
                print(e)
                percent_people_fed = np.nan
        else:
            scenario_runner = ScenarioRunner()
            interpreted_results = scenario_runner.run_and_analyze_scenario(
                constants_for_params,
                scenario_loader,
                create_pptx_with_all_countries,
                show_country_figures,
                figure_save_postfix,
                country_data,
            )
            percent_people_fed = interpreted_results.percent_people_fed
        return (
            percent_people_fed / 100,
            scenario_loader.scenario_description,
            interpreted_results,
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
        title="untitled",
        create_pptx_with_all_countries=True,
        show_country_figures=False,
        show_map_figures=False,
        add_map_slide_to_pptx=True,
        scenario_option=[],
        countries_list=[],  # runs all the countries if empty
        figure_save_postfix="",
        return_results=False,
    ):
        """
        This function runs the model for all countries in the world, no trade.
        countries_list is a list of country codes to run the model for, but if
        there's an "!" in the list, you skip that one.
        If you leave it blank, it runs all the countries

        You can generate a powerpoint as an option here too

        """
        assert len(scenario_option) > 0, "ERROR: a scenario must be specified"

        if create_pptx_with_all_countries:
            if not os.path.exists(Path(repo_root) / "results" / "large_reports"):
                os.mkdir(Path(repo_root) / "results" / "large_reports")
            Plotter.start_pptx("No trade by country")
        """
        Runs the baseline model by country and without trade

        Arguments:

        Returns:
            None
        """
        # country codes for UK + EU 27 countries (used for plotting map)

        NO_TRADE_CSV = (
            Path(repo_root)
            / "data"
            / "no_food_trade"
            / "computer_readable_combined.csv"
        )

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

        print(countries_list)

        (
            exclusive_countries_to_run,
            countries_to_skip,
        ) = self.get_countries_to_run_and_skip(countries_list)

        results = {}

        for index, country_data in no_trade_table.iterrows():
            country_code = country_data["iso3"]

            if len(exclusive_countries_to_run) > 0:
                if country_code not in exclusive_countries_to_run:
                    continue

            if country_code in countries_to_skip:
                continue

            population = country_data["population"]

            # skip countries with no population
            if np.isnan(population):
                continue

            (
                needs_ratio,
                scenario_description,
                interpreted_results,
            ) = self.run_optimizer_for_country(
                country_data,
                scenario_option,
                create_pptx_with_all_countries,
                show_country_figures,
                figure_save_postfix,
            )
            country_name = country_data["country"]
            if np.isnan(needs_ratio):
                n_errors += 1
                failed_countries += " " + country_name
                continue

            self.fill_data_for_map(world, country_code, needs_ratio)

            # we say all are fed if ratio of macronutrient needs met is greater than 1
            if needs_ratio >= 1:
                capped_ratio = 1
            else:
                capped_ratio = needs_ratio

            net_pop_fed += capped_ratio * population
            net_pop += population

            if return_results:
                results[country_name] = interpreted_results

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
        if show_map_figures or add_map_slide_to_pptx:
            Plotter.plot_map_of_countries_fed(
                world,
                ratio_fed,
                scenario_description,
                show_map_figures,
                add_map_slide_to_pptx,
            )
        year = str(date.today().year)
        month = str(date.today().month)
        day = str(date.today().day)
        hour = str(datetime.datetime.now().hour)
        minute = str(datetime.datetime.now().minute)
        if create_pptx_with_all_countries:
            file_root = Path(repo_root) / "results" / "large_reports" / "no_food_trade_"
            Plotter.end_pptx(
                saveloc=str(file_root)
                + title
                + "."
                + year
                + "."
                + month
                + "."
                + day
                + "."
                + hour
                + "."
                + minute
                + ".pptx"
            )
        # @li return a dataframe with each country and the world needs ratio
        return [world, net_pop, net_pop_fed, results]

    def get_countries_to_run_and_skip(self, countries_list):
        """
        if there's any country code with a "!", skip that one
        For example, if !USA is one of the country codes, that one will be skipped
        If !USA and !CHN are country codes, then both will skip
        if there's no ! in any of the codes, then only the ones listed will be
        run.
        """

        countries_to_skip = []
        exclusive_countries_to_run = []
        if countries_list == []:
            return [[], []]

        if np.array([("!" in c) for c in countries_list]).all():
            # all the countries listed are ones to skip, all the others should be run
            for c in countries_list:
                if "!" in c:
                    countries_to_skip.append(c.replace("!", ""))
        else:
            # there's at least one country that is supposed to in the exclusive list
            # to run
            for c in countries_list:
                if "!" not in c:
                    exclusive_countries_to_run.append(c)

        return exclusive_countries_to_run, countries_to_skip

    def run_many_options(
        self,
        scenario_options,
        title,
        add_map_slide_to_pptx=True,
        show_map_figures=False,
        countries_list=[],
        return_results=False,
    ):
        print("Number of scenarios:")
        print(len(scenario_options))
        print("")
        print("")
        print("")
        if add_map_slide_to_pptx:
            Plotter.start_pptx("Various Scenario Options " + title)

        scenario_number = 1
        for scenario_option in scenario_options:
            print("Scenario Number: " + str(scenario_number))
            scenario_number += 1
            self.run_model_no_trade(
                title=title,
                create_pptx_with_all_countries=False,
                show_country_figures=False,
                show_map_figures=show_map_figures,
                add_map_slide_to_pptx=add_map_slide_to_pptx,
                scenario_option=scenario_option,
                countries_list=countries_list,
                return_results=False,
            )

        if add_map_slide_to_pptx:
            year = str(date.today().year)
            month = str(date.today().month)
            day = str(date.today().day)
            hour = str(datetime.datetime.now().hour)
            minute = str(datetime.datetime.now().minute)
            path_string = str(
                Path(repo_root)
                / "results"
                / "large_reports"
                / "various_scenario_options_"
            )
            Plotter.end_pptx(
                saveloc=path_string
                + title
                + "."
                + year
                + "."
                + month
                + "."
                + day
                + "."
                + hour
                + "."
                + minute
                + ".pptx"
            )

    def create_several_maps_with_different_assumptions(
        self, this_simulation, show_map_figures=False
    ):
        # initializing lists
        this_simulation_combinations = {}

        this_simulation_combinations["waste"] = [
            "baseline_in_country",
            "tripled_prices_in_country",
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
        defaults = this_simulation
        defaults["nutrition"] = "catastrophe"
        defaults["cull"] = "do_eat_culled"
        defaults["meat_strategy"] = "efficient_meat_strategy"
        assert "waste" not in this_simulation.keys()
        assert "nutrition" not in this_simulation.keys()
        assert "buffer" not in this_simulation.keys()
        assert "shutoff" not in this_simulation.keys()
        assert "cull" not in this_simulation.keys()
        defaults["waste"] = "zero"
        defaults["nutrition"] = "baseline"
        defaults["buffer"] = "baseline"
        defaults["shutoff"] = "reduce_breeding_USA"
        defaults["cull"] = "do_eat_culled"

        options_including_defaults = []
        for option in options:
            options_including_defaults.append(defaults | option)

        self.run_many_options(
            scenario_options=options_including_defaults,
            title=this_simulation["scenario"],
            show_map_figures=show_map_figures,
            add_map_slide_to_pptx=True,
        )

    def run_desired_simulation(self, this_simulation, args):
        print("arguments, all optional:")
        print("first: [single|multi] (single set of assumptions or multiple)")
        print("second: [pptx|no_pptx] (save a pptx report or not)")
        print("third: [no_plot|plot] (plots figures)")
        print("")
        print("")
        print("")

        if len(args) == 1:
            single_or_various = args[0]
            create_pptx = "pptx"
            plot_figs = "no_plot"
        elif len(args) == 2:
            single_or_various = args[0]
            create_pptx = args[1]
            plot_figs = "no_plot"
        elif len(args) == 3:
            single_or_various = args[0]
            create_pptx = args[1]
            plot_figs = args[2]
        elif len(args) == 4:
            single_or_various = args[0]
            create_pptx = args[1]
            plot_figs = args[2]
        else:
            single_or_various = "single"
            create_pptx = "pptx"
            plot_figs = "no_plot"

        CREATE_SEVERAL_MAPS_PPTX = single_or_various == "multi"
        if CREATE_SEVERAL_MAPS_PPTX:
            self.create_several_maps_with_different_assumptions(
                this_simulation, show_map_figures=(plot_figs == "plot")
            )

        CREATE_PPTX_EACH_COUNTRY = single_or_various == "single"
        if CREATE_PPTX_EACH_COUNTRY:
            self.run_model_defaults_no_trade(
                this_simulation=this_simulation,
                show_map_figures=(plot_figs == "plot"),
                show_country_figures=(plot_figs == "plot"),
                create_pptx_with_all_countries=(create_pptx == "pptx"),
            )
