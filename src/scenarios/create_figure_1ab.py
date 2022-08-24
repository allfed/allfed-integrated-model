"""
This file contains the code for the creation of figure 1ab.
baseline model by country for with and
without trade scenarios.

Created on Wed Jul 15
@author: morgan
"""
import sys
from src.scenarios.run_model_no_trade import ScenarioRunnerNoTrade


def call_scenario_runner(this_simulation, title):
    scenario_runner = ScenarioRunnerNoTrade()

    [world, pop_total, pop_fed] = scenario_runner.run_model_no_trade(
        title=title,
        create_pptx_with_all_countries=False,
        show_country_figures=False,
        show_map_figures=True,
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


def main(args):
    # WORST CASE #
    this_simulation = {}
    this_simulation["scenario"] = "no_resilient_foods"

    this_simulation["waste"] = "baseline_in_country"
    this_simulation["shutoff"] = "continued"
    this_simulation["meat_strategy"] = "inefficient_meat_strategy"

    this_simulation["buffer"] = "no_stored_food"
    this_simulation["seasonality"] = "no_seasonality"

    this_simulation["cull"] = "dont_eat_culled"

    # call_scenario_runner_with_and_without_fat_protein(this_simulation, "worst_case")

    # WORST CASE + SIMPLE_ADAPTATIONS #

    this_simulation["waste"] = "tripled_prices_in_country"
    this_simulation["shutoff"] = "long_delayed_shutoff"
    this_simulation["meat_strategy"] = "efficient_meat_strategy"

    call_scenario_runner_with_and_without_fat_protein(
        this_simulation, "worst case + simple_adaptations"
    )

    # WORST CASE + SIMPLE_ADAPTATIONS + CULLING #

    this_simulation["cull"] = "do_eat_culled"

    call_scenario_runner_with_and_without_fat_protein(
        this_simulation, "worst_case_+_simple_adaptations_+_culling"
    )
    # WORST CASE + SIMPLE_ADAPTATIONS + STORAGE + CULLING + ALL RESILIENT FOODS
    this_simulation["scenario"] = "all_resilient_foods"
    call_scenario_runner_with_and_without_fat_protein(
        this_simulation, "Example_Scenario_+_all_resilient_foods"
    )

    # WORST CASE + SIMPLE_ADAPTATIONS + CULLING + STORAGE #

    this_simulation["buffer"] = "zero"
    this_simulation["seasonality"] = "country"
    call_scenario_runner_with_and_without_fat_protein(
        this_simulation, "Example_Scenario"
    )

    # WORST CASE + SIMPLE_ADAPTATIONS + STORAGE + CULLING + EACH RESILIENT FOOD

    this_simulation["scenario"] = "seaweed"
    call_scenario_runner_with_and_without_fat_protein(
        this_simulation, "Example Scenario + seaweed"
    )

    this_simulation["scenario"] = "methane_scp"
    call_scenario_runner_with_and_without_fat_protein(
        this_simulation, "Example Scenario + methane scp"
    )
    this_simulation["scenario"] = "cellulosic_sugar"
    call_scenario_runner_with_and_without_fat_protein(
        this_simulation, "Example Scenario + cellulosic sugar"
    )
    this_simulation["scenario"] = "relocated_crops"
    call_scenario_runner_with_and_without_fat_protein(
        this_simulation, "Example Scenario + relocated crops"
    )
    this_simulation["scenario"] = "greenhouse"
    call_scenario_runner_with_and_without_fat_protein(
        this_simulation, "Example Scenario + greenhouses"
    )


if __name__ == "__main__":
    args = sys.argv[1:]
    main(args)
