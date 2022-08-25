"""
This file contains the code for the creation of figure 1ab.
baseline model by country for with and
without trade scenarios.

Created on Wed Jul 15
@author: morgan
"""
import sys
from src.scenarios.run_model_no_trade import ScenarioRunnerNoTrade
from src.utilities.plotter import Plotter
import git
import numpy as np

repo_root = git.Repo(".", search_parent_directories=True).working_dir


def call_scenario_runner(this_simulation, title):
    scenario_runner = ScenarioRunnerNoTrade()

    [world, pop_total, pop_fed, results] = scenario_runner.run_model_no_trade(
        title=title,
        create_pptx_with_all_countries=False,
        show_country_figures=False,
        show_map_figures=False,
        add_map_slide_to_pptx=False,
        scenario_option=this_simulation,
        countries_list=["CHN", "IND", "USA", "IDN", "PAK"],
        figure_save_postfix="_" + title,
        return_results=True,
    )

    return [world, pop_total, pop_fed, results]


def call_scenario_runner_with_and_without_fat_protein(this_simulation, title):
    this_simulation["scale"] = "country"
    this_simulation["crop_disruption"] = "country_nuclear_winter"
    this_simulation["grasses"] = "country_nuclear_winter"
    this_simulation["fish"] = "nuclear_winter"
    this_simulation["nutrition"] = "catastrophe"

    this_simulation["fat"] = "not_required"
    this_simulation["protein"] = "not_required"

    print("title")
    print(title)
    # print("percent fed")
    # print(pop_fed / pop_total)
    [world, pop_total, pop_fed, results] = call_scenario_runner(this_simulation, title)
    print("return_results")
    print(results)

    return results
    # this_simulation["fat"] = "not_required"
    # this_simulation["protein"] = "not_required"

    # [world, pop_total, pop_fed] = call_scenario_runner(
    #     this_simulation, title + " require fat+protein"
    # )
    # print(pop_fed / pop_total)


def recalculate_plots():
    # WORST CASE #
    this_simulation = {}
    this_simulation["scenario"] = "no_resilient_foods"

    this_simulation["waste"] = "baseline_in_country"
    this_simulation["shutoff"] = "continued"
    this_simulation["meat_strategy"] = "inefficient_meat_strategy"

    this_simulation["buffer"] = "zero"
    this_simulation["seasonality"] = "country"
    this_simulation["cull"] = "do_eat_culled"

    # WORST CASE + SIMPLE_ADAPTATIONS #

    this_simulation["waste"] = "tripled_prices_in_country"
    this_simulation["shutoff"] = "long_delayed_shutoff"
    this_simulation["meat_strategy"] = "efficient_meat_strategy"

    # WORST CASE + SIMPLE_ADAPTATIONS + CULLING #

    this_simulation["cull"] = "do_eat_culled"

    results_example_scenario = call_scenario_runner_with_and_without_fat_protein(
        this_simulation, "Example_Scenario"
    )
    # WORST CASE + SIMPLE_ADAPTATIONS + STORAGE + CULLING + ALL RESILIENT FOODS
    this_simulation["scenario"] = "all_resilient_foods"
    results_resilient_foods = call_scenario_runner_with_and_without_fat_protein(
        this_simulation, "Example_Scenario_+_all_resilient_foods"
    )

    results = {}
    results["Example Scenario"] = results_example_scenario
    results["Example Scenario, Resilient Foods"] = results_resilient_foods

    return results


def main(args):

    RECALCULATE_PLOTS = True
    if RECALCULATE_PLOTS:
        results = recalculate_plots()
        np.save(repo_root + "/results/large_reports/results2.npy", results)
    else:
        results = np.load(
            repo_root + "/results/large_reports/results2.npy", allow_pickle=True
        ).item()

    Plotter.plot_fig_2abcde_updated(results=results, xlim=72)


if __name__ == "__main__":
    args = sys.argv[1:]
    main(args)