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
from src.scenarios.scenarios import Scenarios
from src.scenarios.run_scenario import ScenarioRunner
import git

repo_root = git.Repo(".", search_parent_directories=True).working_dir


def call_scenario_runner(this_simulation, title):

    scenario_runner = ScenarioRunner()
    constants_for_params, scenarios_loader = scenario_runner.set_depending_on_option(
        [], this_simulation
    )

    results = scenario_runner.run_and_analyze_scenario(
        constants_for_params, scenarios_loader
    )

    print("")
    print(title)
    print("percent_people_fed")
    print(results.percent_people_fed)
    print("")

    return results


def main(args):
    # WORST CASE #
    this_simulation = {}
    this_simulation["scale"] = "global"
    this_simulation["crop_disruption"] = "global_nuclear_winter"
    this_simulation["grasses"] = "global_nuclear_winter"
    this_simulation["fish"] = "nuclear_winter"
    this_simulation["nutrition"] = "catastrophe"

    this_simulation["fat"] = "required"
    this_simulation["protein"] = "required"

    this_simulation["scenario"] = "no_resilient_foods"

    this_simulation["buffer"] = "no_stored_food"
    this_simulation["seasonality"] = "no_seasonality"

    this_simulation["waste"] = "baseline_globally"
    this_simulation["shutoff"] = "continued"
    this_simulation["meat_strategy"] = "efficient_meat_strategy"

    this_simulation["cull"] = "dont_eat_culled"

    title = "Worst_Case_Considered_with_trade"
    results = call_scenario_runner(this_simulation, title)

    Plotter.plot_fig_1ab(results, 72, title, True, False)

    # WORST CASE + SIMPLE_ADAPTATIONS #

    this_simulation["waste"] = "tripled_prices_globally"
    this_simulation["shutoff"] = "long_delayed_shutoff"
    this_simulation["meat_strategy"] = "efficient_meat_strategy"
    title = "worst case + simple_adaptations"

    results = call_scenario_runner(this_simulation, title)

    Plotter.plot_fig_1ab(results, 72, title, True, False)

    # WORST CASE + SIMPLE_ADAPTATIONS + CULLING #

    this_simulation["cull"] = "do_eat_culled"

    title = "worst_case_+_simple_adaptations_+_culling"
    results = call_scenario_runner(this_simulation, title)
    Plotter.plot_fig_1ab(results, 72, title, True, False)

    # WORST CASE + SIMPLE_ADAPTATIONS + CULLING + STORAGE #

    this_simulation["buffer"] = "zero"
    this_simulation["seasonality"] = "nuclear_winter_globally"
    title = "Example_Scenario:simple_adaptations_+_culling_+_storage"
    results = call_scenario_runner(this_simulation, title)
    Plotter.plot_fig_1ab(results, 72, title, True, False)

    # WORST CASE + SIMPLE_ADAPTATIONS + STORAGE + CULLING + ALL RESILIENT FOODS
    this_simulation["scenario"] = "all_resilient_foods"
    title = "Example_Scenario_+_all_resilient_foods"
    results = call_scenario_runner(this_simulation, title)
    Plotter.plot_fig_1ab(results, 72, title, True, False)


if __name__ == "__main__":
    args = sys.argv[1:]
    main(args)
