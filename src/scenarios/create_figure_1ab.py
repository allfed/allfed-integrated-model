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

    [world, pop_total, pop_fed, return_results] = scenario_runner.run_model_no_trade(
        title=title,
        create_pptx_with_all_countries=False,
        show_country_figures=False,
        show_map_figures=False,
        add_map_slide_to_pptx=False,
        scenario_option=this_simulation,
        countries_list=[],
    )

    return [world, pop_total, pop_fed]


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
    [world, pop_total, pop_fed] = call_scenario_runner(this_simulation, title)

    # this_simulation["fat"] = "not_required"
    # this_simulation["protein"] = "not_required"

    # [world, pop_total, pop_fed] = call_scenario_runner(
    #     this_simulation, title + " require fat+protein"
    # )
    # print(pop_fed / pop_total)

    return world, round(100 * pop_fed / pop_total, 0)


def recalculate_plots():
    # WORST CASE #
    this_simulation = {}
    this_simulation["scenario"] = "no_resilient_foods"

    this_simulation["waste"] = "baseline_in_country"
    this_simulation["shutoff"] = "continued"
    this_simulation["meat_strategy"] = "inefficient_meat_strategy"

    this_simulation["buffer"] = "no_stored_food"
    this_simulation["seasonality"] = "no_seasonality"

    this_simulation["cull"] = "dont_eat_culled"

    [
        world_worst_case,
        fraction_needs_worst_case,
    ] = call_scenario_runner_with_and_without_fat_protein(this_simulation, "Worst Case")

    # WORST CASE + SIMPLE_ADAPTATIONS #

    this_simulation["waste"] = "tripled_prices_in_country"
    this_simulation["shutoff"] = "long_delayed_shutoff"
    this_simulation["meat_strategy"] = "efficient_meat_strategy"

    [
        world_simple_adaptations,
        fraction_needs_simple_adaptations,
    ] = call_scenario_runner_with_and_without_fat_protein(
        this_simulation, "simple_adaptations"
    )

    # WORST CASE + SIMPLE_ADAPTATIONS + CULLING #

    this_simulation["cull"] = "do_eat_culled"

    [
        world_simple_adaptations_culling,
        fraction_needs_simple_adaptations_culling,
    ] = call_scenario_runner_with_and_without_fat_protein(
        this_simulation, "simple_adaptations,\nculling"
    )

    # WORST CASE + SIMPLE_ADAPTATIONS + CULLING + STORAGE #
    this_simulation["buffer"] = "zero"
    this_simulation["seasonality"] = "country"
    [
        world_simple_adaptations_culling_storage,
        fraction_needs_simple_adaptations_culling_storage,
    ] = call_scenario_runner_with_and_without_fat_protein(
        this_simulation, "simple_adaptations,\nculling,\nstorage"
    )

    this_simulation["scenario"] = "all_resilient_foods"
    [
        world_example_scenario_resilient_foods,
        fraction_needs_example_scenario_resilient_foods,
    ] = call_scenario_runner_with_and_without_fat_protein(
        this_simulation,
        "Example Scenario:\nsimple_adaptations,\nculling,\nstorage,\nresilient foods",
    )

    # WORST CASE + SIMPLE_ADAPTATIONS + STORAGE + CULLING + ALL RESILIENT FOODS
    this_simulation["scenario"] = "seaweed"
    [
        world_seaweed,
        fraction_needs_seaweed,
    ] = call_scenario_runner_with_and_without_fat_protein(
        this_simulation, "Example Scenario + seaweed"
    )

    this_simulation["scenario"] = "methane_scp"
    [
        world_methane_scp,
        fraction_needs_methane_scp,
    ] = call_scenario_runner_with_and_without_fat_protein(
        this_simulation, "Example Scenario + methane_scp"
    )
    this_simulation["scenario"] = "cellulosic_sugar"
    [
        world_cellulosic_sugar,
        fraction_needs_cellulosic_sugar,
    ] = call_scenario_runner_with_and_without_fat_protein(
        this_simulation, "Example Scenario + cellulosic_sugar"
    )
    this_simulation["scenario"] = "relocated_crops"
    [
        world_cold_crops,
        fraction_needs_cold_crops,
    ] = call_scenario_runner_with_and_without_fat_protein(
        this_simulation, "Example Scenario + cold_crops"
    )
    this_simulation["scenario"] = "greenhouse"
    [
        world_greenhouses,
        fraction_needs_greenhouses,
    ] = call_scenario_runner_with_and_without_fat_protein(
        this_simulation, "Example Scenario + greenhouses"
    )

    worlds = {}
    worlds["Worst Case"] = world_worst_case
    worlds["simple_adaptations"] = world_simple_adaptations
    worlds["simple_adaptations,\nculling"] = world_simple_adaptations_culling
    worlds[
        "simple_adaptations,\nculling,\nstorage"
    ] = world_example_scenario_resilient_foods
    worlds["Example Scenario + seaweed"] = world_seaweed
    worlds["Example Scenario + methane_scp"] = world_methane_scp
    worlds["Example Scenario + cellulosic_sugar"] = world_cellulosic_sugar
    worlds["Example Scenario + cold_crops"] = world_cold_crops
    worlds["Example Scenario + greenhouses"] = world_greenhouses

    ratios = {}
    ratios["Worst Case"] = fraction_needs_worst_case
    ratios["simple_adaptations"] = fraction_needs_simple_adaptations
    ratios["simple_adaptations,\nculling"] = fraction_needs_simple_adaptations_culling
    ratios[
        "simple_adaptations,\nculling,\nstorage"
    ] = fraction_needs_example_scenario_resilient_foods
    ratios["Example Scenario + seaweed"] = fraction_needs_seaweed
    ratios["Example Scenario + methane_scp"] = fraction_needs_methane_scp
    ratios["Example Scenario + cellulosic_sugar"] = fraction_needs_cellulosic_sugar
    ratios["Example Scenario + cold_crops"] = fraction_needs_cold_crops
    ratios["Example Scenario + greenhouses"] = fraction_needs_greenhouses

    return worlds, ratios


def main(args):
    RECALCULATE_PLOTS = True
    if RECALCULATE_PLOTS:
        worlds, ratios = recalculate_plots()
        np.save(repo_root + "/results/large_reports/worlds1.npy", worlds)
        np.save(repo_root + "/results/large_reports/ratios1.npy", ratios)
    else:
        worlds = np.load(
            repo_root + "/results/large_reports/worlds1.npy", allow_pickle=True
        ).item()
        ratios = np.load(
            repo_root + "/results/large_reports/ratios1.npy", allow_pickle=True
        ).item()

    Plotter.plot_fig_1ab_updated(worlds=worlds, ratios=ratios, xlim=72)


if __name__ == "__main__":
    args = sys.argv[1:]
    main(args)
