"""
This file contains the code for the plotting of all figures from the integrated model paper.

It is separate from the .yaml configured custom by-country plots in the scenarios/ folder.

Created on Feb 05 2024
@author: morgan
"""

from src.scenarios.run_model_no_trade import ScenarioRunnerNoTrade
from src.scenarios.run_scenario import ScenarioRunner
from src.utilities.plotter import Plotter
import git
from pathlib import Path
import numpy as np
import copy
import pprint
import sys

repo_root = git.Repo(".", search_parent_directories=True).working_dir


# COMMAND LINE INTERFACE FUNCTIONS #
RUN_FIGURE_1_AND_3_WITH_BASELINE_CLIMATE = False
RUN_FIGURE_1_LEAVING_TYPICAL_BUFFERS = False
RUN_FIGURE_1_NO_STORAGE = False


def print_usage():
    print(
        """
Usage: python3 plot_paper_figures.py [action] [plot_numbers...]

Arguments:
    action          Either 'rerun' to recalculate plots or 'load' to load existing plots.
    plot_numbers    The specific plots to run or load. Allowed values are '1', '2', '3', 's1', or 'all'.
                    Specify multiple plots by listing them after the action argument.
                    Use 'all' to indicate all plots should be processed.

                    Figure 1 refers to "Caloric needs met, no international food trade, all countries"

                    Figure 2 refers to "Caloric needs met over time, top 5 population countries,
                        no food international food trade"

                    Figure 3 refers to "Needs met with continued international food trade"

                    Figure s1 refers to the first plot in the supplemental information, "Production in 2020"

Examples:
    python3 plot_paper_figures.py rerun 1 s1    Recalculate and plot figures 1 and s1.
    python3 plot_paper_figures.py load all      Load and plot all available figures.

Use '--help' to display this message.
"""
    )


def load_results(figure_name):
    loaded_npys = {"worlds": None, "ratios": None, "results": None}
    try:
        if figure_name == "1":
            npy_file_path = (
                Path(repo_root) / "results" / "large_reports" / "worlds_figure1.npy"
            )
            loaded_npys["worlds"] = np.load(npy_file_path, allow_pickle=True).item()

            npy_file_path = (
                Path(repo_root) / "results" / "large_reports" / "ratios_figure1.npy"
            )
            loaded_npys["ratios"] = np.load(npy_file_path, allow_pickle=True).item()
        elif figure_name == "2":
            npy_file_path = (
                Path(repo_root) / "results" / "large_reports" / "results_figure2.npy"
            )
            print("npy_file_path")
            print(npy_file_path)
            loaded_npys["results"] = np.load(npy_file_path, allow_pickle=True)
        return loaded_npys
    except FileNotFoundError:
        print(
            f"Error: The plot for figure {figure_name} could not be loaded because the file {npy_file_path} was "
            " never run. You need to use the 'rerun' argument to calculate figure {figure_name} before loading it."
        )
        sys.exit(1)  # Exit with an error code


def main(args):
    if len(args) == 0 or args[0] in ["--help", "-h"]:
        print_usage()
        return

    # Validate action
    if args[0] not in ["rerun", "load"]:
        print("Invalid action argument. Allowed values are 'rerun' or 'load'.\n")
        print_usage()
        return

    # Validate plots
    valid_plots = {"1", "2", "3", "s1", "all"}
    plots_to_run = set(args[1:])
    if not plots_to_run.issubset(valid_plots):
        print(
            "Invalid plot_numbers argument. Allowed values are '1', '2', '3', 's1', or 'all'.\n"
        )
        print_usage()
        return

    RECALCULATE_PLOTS = args[0] == "rerun"
    plots_to_run = args[1:] if "all" not in args[1:] else ["1", "2", "3", "s1"]
    for plot_to_display in plots_to_run:
        if RECALCULATE_PLOTS:
            if plot_to_display == "1":
                worlds, ratios = recalculate_plot_1()
                np.save(
                    Path(repo_root)
                    / "results"
                    / "large_reports"
                    / "worlds_figure1.npy",
                    worlds,
                )
                np.save(
                    Path(repo_root)
                    / "results"
                    / "large_reports"
                    / "ratios_figure1.npy",
                    ratios,
                )
            elif plot_to_display == "2":
                results = recalculate_plot_2()
                np.save(
                    Path(repo_root)
                    / "results"
                    / "large_reports"
                    / "results_figure2.npy",
                    results,
                )
            elif plot_to_display == "3":
                results = recalculate_plot_3()
            elif plot_to_display == "s1":
                results = recalculate_plot_s1()
        else:
            if plot_to_display == "3":
                print("note: recalculating plot 3 as it's fast")
                results = recalculate_plot_3()
            elif plot_to_display == "s1":
                print("note: recalculating plot s1 as it's fast")
                results = recalculate_plot_s1()

            else:
                loaded_npys = load_results(plot_to_display)
                worlds = loaded_npys["worlds"]
                ratios = loaded_npys["ratios"]
                results = loaded_npys["results"]

        if plot_to_display == "1":
            Plotter.plot_fig_1ab_updated(worlds=worlds, ratios=ratios, xlim=72)
        if plot_to_display == "2":
            Plotter.plot_fig_2abcde_updated(results, xlim=72)
        if plot_to_display == "3":
            Plotter.plot_fig_3abcde_updated(results, xlim=72)


# SCENARIO CALLING HELPER FUNCTIONS #


def call_scenario_runner(
    this_simulation,
    title,
    countries_list=[],
    figure_save_postfix="",
    return_results=False,
):
    pprint.pprint("")
    pprint.pprint("")
    pprint.pprint("")
    pprint.pprint("")
    pprint.pprint("")
    pprint.pprint("this_simulation")
    pprint.pprint(this_simulation)
    pprint.pprint("")
    pprint.pprint("")
    pprint.pprint("")
    scenario_runner = ScenarioRunnerNoTrade()
    RUN_LIMITED_SET_OF_COUNTRIES_TO_GENERATE_PPTX = False
    if RUN_LIMITED_SET_OF_COUNTRIES_TO_GENERATE_PPTX:
        [world, pop_total, pop_fed, results] = scenario_runner.run_model_no_trade(
            title=title,
            create_pptx_with_all_countries=True,
            show_country_figures=False,
            show_map_figures=False,
            add_map_slide_to_pptx=True,
            scenario_option=this_simulation,
            countries_list=[
                "IND",
                "BRA",
                "CHN",
                "USA",
                "PAK",
                "ARG",
                "MNG",
                "AUS",
                "CAN",
                "NZL",
                "DJI",
                "IDN",
                "GBR",
                "CHL",
                "RUS",
                "NIG",
                "ZAF",
                "NGA",
                "EGY",
            ],
            figure_save_postfix=figure_save_postfix,
            return_results=return_results,
        )
    else:
        [world, pop_total, pop_fed, results] = scenario_runner.run_model_no_trade(
            title=title,
            create_pptx_with_all_countries=False,
            show_country_figures=False,
            show_map_figures=False,
            add_map_slide_to_pptx=False,
            scenario_option=this_simulation,
            countries_list=countries_list,
            figure_save_postfix=figure_save_postfix,
            return_results=return_results,
        )

    return [world, pop_total, pop_fed, results]


def call_scenario_runner_and_set_options(
    this_simulation,
    title,
    countries_list=[],
    figure_save_postfix="",
    return_results=False,
):
    # make a copy so that properties below are not set for future calls with this_simulation
    this_simulation_copy = copy.deepcopy(this_simulation)

    assert "scale" not in this_simulation_copy, "ERROR: scale overwritten"
    assert "NMONTHS" not in this_simulation_copy, "ERROR: NMONTHS overwritten"
    assert (
        "crop_disruption" not in this_simulation_copy
    ), "ERROR: crop_disruption overwritten"
    assert "grasses" not in this_simulation_copy, "ERROR: grasses overwritten"
    assert "fish" not in this_simulation_copy, "ERROR: fish overwritten"
    assert (
        "intake_constraints" not in this_simulation_copy
    ), "ERROR: intake_constraints overwritten"
    assert "nutrition" not in this_simulation_copy, "ERROR: nutrition overwritten"
    assert "fat" not in this_simulation_copy, "ERROR: fat overwritten"
    assert "protein" not in this_simulation_copy, "ERROR: protein overwritten"
    if RUN_FIGURE_1_AND_3_WITH_BASELINE_CLIMATE:
        this_simulation_copy["crop_disruption"] = "zero"
        this_simulation_copy["grasses"] = "baseline"
        this_simulation_copy["fish"] = "baseline"
    else:
        this_simulation_copy["crop_disruption"] = "country_nuclear_winter"
        this_simulation_copy["grasses"] = "country_nuclear_winter"
        this_simulation_copy["fish"] = "nuclear_winter"

    this_simulation_copy["scale"] = "country"
    this_simulation_copy["NMONTHS"] = 120
    this_simulation_copy["intake_constraints"] = "enabled"
    this_simulation_copy["nutrition"] = "catastrophe"

    this_simulation_copy["fat"] = "not_required"
    this_simulation_copy["protein"] = "not_required"

    [world, pop_total, pop_fed, results] = call_scenario_runner(
        this_simulation_copy,
        title,
        countries_list=countries_list,
        figure_save_postfix=figure_save_postfix,
        return_results=return_results,
    )

    return {
        "world": world,
        "pop_fed_percent": round(100 * pop_fed / pop_total, 0),
        "results": results,
    }


def call_global_scenario_runner(this_simulation, title):
    scenario_runner = ScenarioRunner()
    (
        constants_for_params,
        time_consts_for_params,
        scenario_loader,
    ) = scenario_runner.set_depending_on_option(this_simulation)
    NO_TRADE_CSV = (
        Path(repo_root) / "data" / "no_food_trade" / "computer_readable_combined.csv"
    )
    import pandas as pd

    no_trade_table = pd.read_csv(NO_TRADE_CSV)
    iso3 = "WOR"
    for index, country_data in no_trade_table.iterrows():
        country_code = country_data["iso3"]
        if country_code == iso3:
            break

    interpreted_results = scenario_runner.run_and_analyze_scenario(
        constants_for_params,
        time_consts_for_params,
        scenario_loader,
        create_pptx_with_all_countries=False,
        show_country_figures=False,
        figure_save_postfix="_world",
        country_data=country_data,
        save_all_results=False,
        country_name="world",
        country_iso3="WOR",
        title=title,
    )
    PLOT_FEED = False
    if PLOT_FEED:
        Plotter.plot_feed(
            interpreted_results,
            "earliest_month_zero",
            # (slaughter_title + " " if slaughter_title is not "" else "")
            "world",
            # + figure_save_postfix,
            True,
            False,
            "",
        )

    return interpreted_results


# FIGURE SPECIFIC OPTIONS #


def recalculate_plot_1():
    # WORST CASE #
    this_simulation = {}
    this_simulation["scenario"] = "no_resilient_foods"

    this_simulation["waste"] = "baseline_in_country"
    this_simulation["shutoff"] = "continued_after_10_percent_fed"
    this_simulation["meat_strategy"] = "baseline_breeding"

    this_simulation["stored_food"] = "baseline"

    if RUN_FIGURE_1_LEAVING_TYPICAL_BUFFERS:
        this_simulation[
            "end_simulation_stocks_ratio"
        ] = "baseline_no_stored_between_years"
        suffix_storage = ""
    else:
        this_simulation["end_simulation_stocks_ratio"] = "no_stored_between_years"

    this_simulation["seasonality"] = "country"

    this_simulation["cull"] = "do_eat_culled"

    worst_case_title = "No Adaptations"
    worst_case = call_scenario_runner_and_set_options(
        this_simulation,
        worst_case_title,
        # countries_list=[
        #     "IND",
        #     "BRA",
        #     "CHN",
        #     "USA",
        #     "PAK",
        #     "ARG",
        #     "MNG",
        #     "AUS",
        #     "CAN",
        #     "NZL",
        #     "DJI",
        #     "IDN",
        #     "GBR",
        #     "CHL",
        #     "RUS",
        #     "NIG",
        #     "ZAF",
        #     "NGA",
        #     "EGY",
        # ],
    )
    # WORST CASE + EAT AND STORE MEAT #

    this_simulation["waste"] = "tripled_prices_in_country"
    this_simulation["shutoff"] = "long_delayed_shutoff_after_10_percent_fed"
    simple_adaptations_title = (
        "Simple Adaptations \n(waste reduced,\n feed + biofuel delayed shutoff)"
    )
    simple_adaptations = call_scenario_runner_and_set_options(
        this_simulation,
        simple_adaptations_title,
        # countries_list=["IND", "BRA", "CHN", "USA", "PAK"],
    )

    # WORST CASE + EAT AND STORE MEAT + SHUT OFF BREEDING + REDUCE  #
    if RUN_FIGURE_1_LEAVING_TYPICAL_BUFFERS:
        assert (
            not RUN_FIGURE_1_NO_STORAGE
        ), "ERROR: You can't run typical buffers if there's no storage..."
        this_simulation["end_simulation_stocks_ratio"] = "baseline"
        suffix_storage = " (Reduced)"
    else:
        this_simulation["end_simulation_stocks_ratio"] = "zero"
        suffix_storage = ""

    if RUN_FIGURE_1_NO_STORAGE:
        this_simulation["end_simulation_stocks_ratio"] = "no_stored_between_years"
        include_storage_resilient_foods_tag = ", No Rationing"
        suffix_storage = " Removed"
    else:
        include_storage_resilient_foods_tag = ""

    simple_adaptations_culling_title = (
        f"Simple Adaptations,\n Rationing{suffix_storage}"
    )

    simple_adaptations_culling = call_scenario_runner_and_set_options(
        this_simulation, simple_adaptations_culling_title  # , countries_list=["CHN"]
    )

    # WORST CASE + SIMPLE_ADAPTATIONS + CULLING + STORAGE #
    this_simulation["meat_strategy"] = "feed_only_ruminants"
    this_simulation["shutoff"] = "long_delayed_shutoff"
    example_scenario_title = f"Example Scenario:\nSimple Adaptations\n+ Rationing{suffix_storage}\n+Humans Prioritized "
    example_scenario = call_scenario_runner_and_set_options(
        this_simulation, example_scenario_title  # , countries_list=["CHN"]
    )

    this_simulation["scenario"] = "all_resilient_foods"
    all_resilient_foods_title = (
        f"Example Scenario\n + Resilient Foods{include_storage_resilient_foods_tag}"
    )
    example_scenario_resilient_foods = call_scenario_runner_and_set_options(
        this_simulation, all_resilient_foods_title  # , countries_list=["CHN"]
    )

    # WORST CASE + SIMPLE_ADAPTATIONS + STORAGE + CULLING + ALL RESILIENT FOODS
    seaweed_title = f"Example Scenario\n + Seaweed{include_storage_resilient_foods_tag}"
    this_simulation["scenario"] = "seaweed"
    seaweed = call_scenario_runner_and_set_options(
        this_simulation, seaweed_title  # , countries_list=["CHN"]
    )

    this_simulation["scenario"] = "methane_scp"
    methane_scp_title = (
        f"Example Scenario\n + Methane SCP{include_storage_resilient_foods_tag}"
    )
    methane_scp = call_scenario_runner_and_set_options(
        this_simulation, methane_scp_title  # , countries_list=["CHN"]
    )

    this_simulation["scenario"] = "cellulosic_sugar"
    cs_title = (
        f"Example Scenario\n+ Cellulosic Sugar{include_storage_resilient_foods_tag}"
    )
    cellulosic_sugar = call_scenario_runner_and_set_options(
        this_simulation, cs_title  # , countries_list=["CHN"]
    )

    this_simulation["scenario"] = "relocated_crops"
    cold_crops_title = (
        f"Example Scenario\n+ Cold Tolerant Crops{include_storage_resilient_foods_tag}"
    )
    cold_crops = call_scenario_runner_and_set_options(
        this_simulation, cold_crops_title  # , countries_list=["CHN"]
    )

    this_simulation["scenario"] = "greenhouse"
    greenhouse_title = (
        f"Example Scenario\n+ Greenhouse Crops{include_storage_resilient_foods_tag}"
    )
    greenhouses = call_scenario_runner_and_set_options(
        this_simulation, greenhouse_title  # , countries_list=["CHN"]
    )

    worlds = {}
    worlds[worst_case_title] = worst_case["world"]
    worlds[simple_adaptations_title] = simple_adaptations["world"]
    worlds[simple_adaptations_culling_title] = simple_adaptations_culling["world"]
    worlds[example_scenario_title] = example_scenario["world"]
    worlds[all_resilient_foods_title] = example_scenario_resilient_foods["world"]
    worlds[seaweed_title] = seaweed["world"]
    worlds[methane_scp_title] = methane_scp["world"]
    worlds[cs_title] = cellulosic_sugar["world"]
    worlds[cold_crops_title] = cold_crops["world"]
    worlds[greenhouse_title] = greenhouses["world"]

    ratios = {}
    ratios[worst_case_title] = worst_case["pop_fed_percent"]
    ratios[simple_adaptations_title] = simple_adaptations["pop_fed_percent"]
    ratios[simple_adaptations_culling_title] = simple_adaptations_culling[
        "pop_fed_percent"
    ]
    ratios[example_scenario_title] = example_scenario["pop_fed_percent"]
    ratios[all_resilient_foods_title] = example_scenario_resilient_foods[
        "pop_fed_percent"
    ]
    ratios[seaweed_title] = seaweed["pop_fed_percent"]
    ratios[methane_scp_title] = methane_scp["pop_fed_percent"]
    ratios[cs_title] = cellulosic_sugar["pop_fed_percent"]
    ratios[cold_crops_title] = cold_crops["pop_fed_percent"]
    ratios[greenhouse_title] = greenhouses["pop_fed_percent"]
    if RUN_FIGURE_1_LEAVING_TYPICAL_BUFFERS:
        print("\nTypical buffers remain in place in figure 1\n")

    if RUN_FIGURE_1_AND_3_WITH_BASELINE_CLIMATE:
        print("\nBaseline climate run for figure 1\n")

    if RUN_FIGURE_1_NO_STORAGE:
        print("\nRationing removed all scenarios figure 1\n")

    return worlds, ratios


def recalculate_plot_2():
    # WORST CASE + SIMPLE_ADAPTATIONS + CULLING + STORAGE #

    this_simulation = {}
    this_simulation["scenario"] = "no_resilient_foods"

    this_simulation["stored_food"] = "baseline"
    this_simulation["end_simulation_stocks_ratio"] = "zero"  # use all the stocks up

    this_simulation["buffer"] = "zero"
    this_simulation["seasonality"] = "country"

    this_simulation["waste"] = "tripled_prices_in_country"
    this_simulation["shutoff"] = "long_delayed_shutoff"
    this_simulation["meat_strategy"] = "feed_only_ruminants"

    this_simulation["cull"] = "do_eat_culled"

    countries_list = ["CHN", "IND", "USA", "BRA", "NGA"]

    example_scenario = call_scenario_runner_and_set_options(
        this_simulation,
        "Example_Scenario",
        countries_list=countries_list,
        figure_save_postfix="_Example_Scenario",
        return_results=True,
    )

    # WORST CASE + SIMPLE_ADAPTATIONS + STORAGE + CULLING + ALL RESILIENT FOODS

    this_simulation["scenario"] = "all_resilient_foods"
    resilient_foods = call_scenario_runner_and_set_options(
        this_simulation,
        "Example_Scenario_+_all_resilient_foods",
        countries_list=countries_list,
        figure_save_postfix="_Example_Scenario_+_all_resilient_foods",
        return_results=True,
    )

    countries_dict = {
        "China": "China",
        "India": "India",
        "United States of America": "USA",
        "Brazil": "Brazil",
        "Nigeria": "Nigeria",
    }
    list_by_country = []

    for country_id, country in countries_dict.items():
        list_by_country.append(
            [
                example_scenario["results"][country_id].percent_people_fed,
                country,
                example_scenario["results"][country_id],
                "Example Scenario",
            ]
        )

    for country_id, country in countries_dict.items():
        list_by_country.append(
            [
                resilient_foods["results"][country_id].percent_people_fed,
                country,
                resilient_foods["results"][country_id],
                "Example Scenario + Resilient Foods",
            ]
        )

    return list_by_country


def recalculate_plot_3():
    # WORST CASE #
    this_simulation = {}
    this_simulation["NMONTHS"] = 120

    if RUN_FIGURE_1_AND_3_WITH_BASELINE_CLIMATE:
        this_simulation["crop_disruption"] = "zero"
        this_simulation["grasses"] = "baseline"
        this_simulation["fish"] = "baseline"
        this_simulation["seasonality"] = "baseline_globally"
    else:
        this_simulation["crop_disruption"] = "global_nuclear_winter"
        this_simulation["grasses"] = "global_nuclear_winter"
        this_simulation["fish"] = "nuclear_winter"
        this_simulation["seasonality"] = "nuclear_winter_globally"

    this_simulation["scale"] = "global"
    this_simulation["stored_food"] = "baseline"

    this_simulation["nutrition"] = "catastrophe"
    this_simulation["fat"] = "not_required"
    this_simulation["protein"] = "not_required"
    this_simulation["intake_constraints"] = "enabled"

    this_simulation["scenario"] = "no_resilient_foods"

    this_simulation["end_simulation_stocks_ratio"] = "no_stored_between_years"

    this_simulation["cull"] = "do_eat_culled"

    # WORST CASE #
    this_simulation["meat_strategy"] = "baseline_breeding"
    this_simulation["waste"] = "baseline_globally"
    this_simulation["shutoff"] = "continued_after_10_percent_fed"

    this_simulation["meat_strategy"] = "baseline_breeding"
    title_no_adaptations = "Trade, no adaptations"
    results_no_adaptations = call_global_scenario_runner(
        this_simulation, title_no_adaptations
    )

    # WORST CASE + SIMPLE_ADAPTATIONS #
    this_simulation["waste"] = "tripled_prices_globally"
    this_simulation["shutoff"] = "long_delayed_shutoff_after_10_percent_fed"

    title_simple_adaptations = "Trade\n+ Simple Adaptations"
    results_simple_adaptations = call_global_scenario_runner(
        this_simulation, title_simple_adaptations
    )

    # WORST CASE + SIMPLE_ADAPTATIONS + CULLING + STORAGE #
    this_simulation["end_simulation_stocks_ratio"] = "zero"
    this_simulation["meat_strategy"] = "feed_only_ruminants"
    this_simulation["shutoff"] = "long_delayed_shutoff"

    title_example_scenario = (
        "Trade\n+ Simple Adaptations\n+ Rationing\n+ Humans Prioritized"
    )
    results_example_scenario = call_global_scenario_runner(
        this_simulation, title_example_scenario
    )

    # WORST CASE + SIMPLE_ADAPTATIONS + STORAGE + CULLING + ALL RESILIENT FOODS
    this_simulation["scenario"] = "all_resilient_foods"
    title_resilient_foods = "Trade\n+ Simple Adaptations\n+ Rationing\n+ Humans Prioritized\n+ Resilient Foods"
    results_resilient_foods = call_global_scenario_runner(
        this_simulation, title_resilient_foods
    )

    results = {}
    results[title_no_adaptations] = results_no_adaptations
    results[title_simple_adaptations] = results_simple_adaptations
    results[title_example_scenario] = results_example_scenario
    results[title_resilient_foods] = results_resilient_foods

    return results


def recalculate_plot_s1():
    # WORST CASE #
    this_simulation = {}
    this_simulation["NMONTHS"] = 120
    this_simulation["scale"] = "global"
    this_simulation["crop_disruption"] = "zero"
    this_simulation["grasses"] = "baseline"
    this_simulation["fish"] = "baseline"
    this_simulation["stored_food"] = "baseline"

    this_simulation["nutrition"] = "baseline"
    this_simulation["fat"] = "not_required"
    this_simulation["protein"] = "not_required"
    this_simulation["intake_constraints"] = "enabled"

    this_simulation["scenario"] = "no_resilient_foods"

    this_simulation["end_simulation_stocks_ratio"] = "baseline"
    this_simulation["seasonality"] = "baseline_globally"

    this_simulation["cull"] = "do_eat_culled"

    # WORST CASE + SIMPLE_ADAPTATIONS #
    this_simulation["meat_strategy"] = "baseline_breeding"
    this_simulation["waste"] = "baseline_globally"
    this_simulation["shutoff"] = "continued"

    title = "baseline"
    scenario_runner = ScenarioRunner()
    (
        constants_for_params,
        time_consts_for_params,
        scenario_loader,
    ) = scenario_runner.set_depending_on_option(this_simulation)

    NO_TRADE_CSV = (
        Path(repo_root) / "data" / "no_food_trade" / "computer_readable_combined.csv"
    )
    import pandas as pd

    no_trade_table = pd.read_csv(NO_TRADE_CSV)
    iso3 = "WOR"
    for index, country_data in no_trade_table.iterrows():
        country_code = country_data["iso3"]
        if country_code == iso3:
            break
    interpreted_results = scenario_runner.run_and_analyze_scenario(
        constants_for_params,
        time_consts_for_params,
        scenario_loader,
        create_pptx_with_all_countries=False,
        show_country_figures=False,
        figure_save_postfix="_world",
        country_data=country_data,
        save_all_results=False,
        country_name="world",
        country_iso3="WOR",
        title=title,
    )
    PLOT_SLAUGHTER = False
    if PLOT_SLAUGHTER:
        Plotter.plot_slaughter(
            interpreted_results,
            "earliest_month_zero",
            # (slaughter_title + " " if slaughter_title is not "" else "")
            "world",
            # + figure_save_postfix,
            True,
            False,
            scenario_loader.scenario_description,
        )

    Plotter.plot_to_humans_stackplot(
        interpreted_results,
        72,
        "Global Baseline",
        plot_figure=True,
        add_slide_with_fig=False,
        description=scenario_loader.scenario_description,
    )

    results = {}
    results["baseline_global"] = interpreted_results

    return results


if __name__ == "__main__":
    main(sys.argv[1:])
