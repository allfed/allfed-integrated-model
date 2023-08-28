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
        """
        Initializes a new instance of the Model class.
        """
        super().__init__()
        self.data = None
        self.model = None
        self.predictions = None
        self.metrics = None
        self.trained = False

    ...

    def run_model_defaults_no_trade(
        self,
        this_simulation,
        show_map_figures=False,
        show_country_figures=False,
        create_pptx_with_all_countries=False,
        scenario_option=[],
    ):
        """
        Runs the model with default options for a given simulation, and generates figures and a PowerPoint presentation.
        Args:
            this_simulation (dict): a dictionary containing specific options for the given simulation
            show_map_figures (bool): whether to show map figures or not
            show_country_figures (bool): whether to show country figures or not
            create_pptx_with_all_countries (bool): whether to create a PowerPoint presentation with all countries or not
            scenario_option (list): a list of scenario options
        """
        # Set a few options to set on top of the specific options for the given simulation
        # These could easily change if another scenario was of more interest.
        this_simulation["fat"] = "not_required"
        this_simulation["protein"] = "not_required"
        this_simulation["meat_strategy"] = "efficient_meat_strategy"

        # Call the run_model_no_trade function with the given options
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
        """
        Runs the optimizer for a given country and scenario option, and returns the percentage of people fed,
        the scenario description, and the interpreted results.

        Args:
            self: instance of the Optimizer class
            country_data (dict): dictionary containing data for the country
            scenario_option (str): scenario option to use for the optimization
            create_pptx_with_all_countries (bool): whether to create a PowerPoint file with all countries' figures
            show_country_figures (bool): whether to show the figures for the country
            figure_save_postfix (str): postfix to add to the figure file names

        Returns:
            tuple: a tuple containing the percentage of people fed, the scenario description, and the interpreted results
        """

        # Extract the country name from the country data
        country_name = country_data["country"]

        # Set the constants and scenario loader based on the scenario option
        constants_for_params, scenario_loader = self.set_depending_on_option(
            country_data, scenario_option
        )

        # Set the excess feed to 0
        constants_for_params["EXCESS_FEED"] = Food(
            kcals=[0] * constants_for_params["NMONTHS"],
            fat=[0] * constants_for_params["NMONTHS"],
            protein=[0] * constants_for_params["NMONTHS"],
            kcals_units="billion kcals each month",
            fat_units="thousand tons each month",
            protein_units="thousand tons each month",
        )

        # Print the country name
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

        # Run the scenario and analyze the results
        USE_TRY_CATCH = False
        if USE_TRY_CATCH:
            try:
                print("running scenario")
                scenario_runner = ScenarioRunner()
                interpreted_results = scenario_runner.run_and_analyze_scenario(
                    constants_for_params, scenario_loader
                )
                percent_people_fed = interpreted_results.percent_people_fed
            except Exception as e:
                print("exception:")
                print(e)
                percent_people_fed = np.nan
        else:
            scenario_runner = ScenarioRunner()
            interpreted_results = scenario_runner.run_and_analyze_scenario(
                constants_for_params, scenario_loader
            )
            percent_people_fed = interpreted_results.percent_people_fed

        # Print the percentage of people fed
        print("percent_people_fed")
        print(percent_people_fed)

        # If the percentage of people fed is not NaN, plot the feed and figure 1ab
        if not np.isnan(percent_people_fed):
            Plotter.plot_feed(
                interpreted_results,
                84,  # constants_for_params["NMONTHS"],
                country_data["country"] + figure_save_postfix,
                show_country_figures,
                create_pptx_with_all_countries,
                scenario_loader.scenario_description,
            )
            Plotter.plot_fig_1ab(
                interpreted_results,
                84,
                # constants_for_params["NMONTHS"],
                country_data["country"] + figure_save_postfix,
                show_country_figures,
                create_pptx_with_all_countries,
                scenario_loader.scenario_description,
            )

        # Return the percentage of people fed, the scenario description, and the interpreted results
        return (
            percent_people_fed / 100,
            scenario_loader.scenario_description,
            interpreted_results,
        )

    def fill_data_for_map(self, world, country_code, needs_ratio):
        """
        This function fills the needs_ratio column of the world dataframe with the kcals_ratio_capped value for a given
        country_code. If the country_code is not found in the world dataframe, a message is printed.

        Args:
            world (pandas.DataFrame): the dataframe containing the data for all countries
            country_code (str): the ISO3 code of the country for which the needs_ratio is to be filled
            needs_ratio (float): the kcals_ratio value for the country

        Returns:
            None
        """

        # Map the country_code to the corresponding ISO3 code in the world dataframe
        if country_code == "SWT":
            country_code_map = "SWZ"
        else:
            country_code_map = country_code

        # Get the row(s) corresponding to the country_code_map in the world dataframe
        country_map = world[world["iso_a3"].apply(lambda x: x == country_code_map)]

        # If no match is found, print a message
        if len(country_map) == 0:
            PRINT_NO_MATCH = False
            if PRINT_NO_MATCH:
                print("no match")
                print(country_code_map)

        # If exactly one match is found, fill the needs_ratio column with kcals_ratio_capped
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

        Args:
            title (str): title of the powerpoint presentation
            create_pptx_with_all_countries (bool): whether to create a powerpoint presentation
            show_country_figures (bool): whether to show figures for each country
            show_map_figures (bool): whether to show the map figure
            add_map_slide_to_pptx (bool): whether to add the map slide to the powerpoint presentation
            scenario_option (list): list of scenarios to run the model for
            countries_list (list): list of country codes to run the model for
            figure_save_postfix (str): postfix to add to the figure save name
            return_results (bool): whether to return the results

        Returns:
            list: a list containing the world, net population, net population fed, and results
        """
        assert len(scenario_option) > 0, "ERROR: a scenario must be specified"

        if create_pptx_with_all_countries:
            if not os.path.exists(Path(repo_root) / "results" / "large_reports"):
                os.mkdir(Path(repo_root) / "results" / "large_reports")
            Plotter.start_pptx("No trade by country")

        # read the no trade csv file
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

        # get the countries to run and skip
        (
            exclusive_countries_to_run,
            countries_to_skip,
        ) = self.get_countries_to_run_and_skip(countries_list)

        results = {}
        net_pop_fed = 0
        net_pop = 0
        scenario_description = ""
        n_errors = 0
        failed_countries = "Failed Countries: \n"

        # iterate over each country from spreadsheet, run the optimizer, plot the result
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

            print("about to run optimizer for country")

            # run the optimizer for the country
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

            # fill data for map
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

        # plot the map of countries fed
        if show_map_figures or add_map_slide_to_pptx:
            Plotter.plot_map_of_countries_fed(
                world,
                ratio_fed,
                scenario_description,
                show_map_figures,
                add_map_slide_to_pptx,
            )

        # save the powerpoint presentation
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

        # return a dataframe with each country and the world needs ratio
        return [world, net_pop, net_pop_fed, results]

    def get_countries_to_run_and_skip(self, countries_list):
        """
        This function takes a list of country codes and returns two lists: one with the
        country codes that should be run exclusively, and another with the country codes
        that should be skipped. If a country code has a "!" in front of it, it should be
        skipped. If there are no "!" in any of the codes, then only the ones listed will
        be run.

        Args:
            countries_list (list): A list of country codes.

        Returns:
            tuple: A tuple containing two lists: the first list contains the country codes
            that should be run exclusively, and the second list contains the country codes
            that should be skipped.
        """

        countries_to_skip = []
        exclusive_countries_to_run = []

        # If the countries_list is empty, return two empty lists
        if countries_list == []:
            return [[], []]

        # If all the country codes have a "!" in front of them, skip all of them except
        # the ones without the "!".
        if np.array([("!" in c) for c in countries_list]).all():
            for c in countries_list:
                if "!" in c:
                    countries_to_skip.append(c.replace("!", ""))
        else:
            # If there is at least one country code without a "!", add it to the list of
            # countries to run exclusively.
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
        """
        Runs multiple scenarios and generates a PowerPoint presentation with the results.
        Args:
            self: instance of the class
            scenario_options (list): list of dictionaries, each containing the parameters for a scenario
            title (str): title of the PowerPoint presentation
            add_map_slide_to_pptx (bool): whether to add a map slide to the PowerPoint presentation
            show_map_figures (bool): whether to show map figures
            countries_list (list): list of countries to include in the analysis
            return_results (bool): whether to return the results of the scenarios
        """
        # Print the number of scenarios
        print("Number of scenarios:")
        print(len(scenario_options))
        print("")
        print("")
        print("")

        # If add_map_slide_to_pptx is True, start a PowerPoint presentation
        if add_map_slide_to_pptx:
            Plotter.start_pptx("Various Scenario Options " + title)

        # Loop through each scenario and run the model
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

        # If add_map_slide_to_pptx is True, end the PowerPoint presentation and save it
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
        """
        This function creates several maps with different assumptions by combining different options
        for waste, buffer, shutoff, fat, and protein. It then runs many options using the
        run_many_options function.

        Args:
            self: instance of the class
            this_simulation (dict): dictionary containing the simulation parameters
            show_map_figures (bool): whether to show the map figures or not

        Returns:
            None
        """

        # initializing lists
        this_simulation_combinations = {}

        # creating different options for waste, buffer, shutoff, fat, and protein
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

        # combining the different options using itertools.product
        flat = [[(k, v) for v in vs] for k, vs in this_simulation_combinations.items()]
        options = [dict(items) for items in product(*flat)]

        # adding default options to the list of options
        defaults = this_simulation
        defaults["nutrition"] = "catastrophe"
        defaults["cull"] = "do_eat_culled"
        defaults["meat_strategy"] = "efficient_meat_strategy"
        options_including_defaults = []
        for option in options:
            options_including_defaults.append(defaults | option)

        # running the simulation for each option
        self.run_many_options(
            scenario_options=options_including_defaults,
            title=this_simulation["scenario"],
            show_map_figures=show_map_figures,
            add_map_slide_to_pptx=True,
        )

    def run_desired_simulation(self, this_simulation, args):
        """
        Runs the desired simulation based on the given arguments and generates a report if specified.

        Args:
            this_simulation (Simulation): The simulation object to run.
            args (list): A list of optional arguments to specify the type of simulation to run and report generation.

        Optional Args:
            first: [single|multi] (single set of assumptions or multiple)
            second: [pptx|no_pptx] (save a pptx report or not)
            third: [no_plot|plot] (plots figures)

        Returns:
            None

        Example:
            >>>
            >>> run_desired_simulation(simulation_object, ['single', 'pptx', 'plot'])

        """
        # Print optional argument descriptions
        print("arguments, all optional:")
        print("first: [single|multi] (single set of assumptions or multiple)")
        print("second: [pptx|no_pptx] (save a pptx report or not)")
        print("third: [no_plot|plot] (plots figures)")
        print("")
        print("")
        print("")

        # Determine which optional arguments were provided
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

        # Determine if multiple maps need to be created
        CREATE_SEVERAL_MAPS_PPTX = single_or_various == "multi"
        if CREATE_SEVERAL_MAPS_PPTX:
            self.create_several_maps_with_different_assumptions(
                this_simulation, show_map_figures=(plot_figs == "plot")
            )

        # Determine if a report needs to be generated for each country
        CREATE_PPTX_EACH_COUNTRY = single_or_various == "single"
        if CREATE_PPTX_EACH_COUNTRY:
            self.run_model_defaults_no_trade(
                this_simulation=this_simulation,
                show_map_figures=(plot_figs == "plot"),
                show_country_figures=(plot_figs == "plot"),
                create_pptx_with_all_countries=(create_pptx == "pptx"),
            )
