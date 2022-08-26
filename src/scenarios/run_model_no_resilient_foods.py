import numpy as np
from src.utilities.plotter import Plotter
from src.scenarios.run_scenario import ScenarioRunner
from src.scenarios.scenarios import Scenarios
import git
from pathlib import Path

repo_root = git.Repo(".", search_parent_directories=True).working_dir


def run_model_no_resilient_foods(plot_figures=True):
    """
    this program runs the optimizer model, and ensures that all the results are
    reasonable using a couple useful checks to make sure there's nothing wacky
    going on:
    1) check that as time increases, more people can be fed
    2) check that stored food plus meat is always used at the
    highest rate during the largest food shortage.
    Arguments:
        plot_figures (bool): whether to plot the figures or not.
    Returns:
        None
    """

    constants = {}

    constants["CHECK_CONSTRAINTS"] = False

    scenarios_loader, constants_for_params = set_common_no_resilient_properties()

    constants_for_params = scenarios_loader.set_immediate_shutoff(constants_for_params)

    constants_for_params = scenarios_loader.set_waste_to_zero(constants_for_params)

    scenario_runner = ScenarioRunner()
    results = scenario_runner.run_and_analyze_scenario(
        constants_for_params, scenarios_loader
    )

    print("")
    print("")
    print("Estimated percet people fed, no resilient foods, no waste")
    print(results.percent_people_fed / 100 * 2100)
    print("")

    np.save(
        Path(repo_root) / "data" / "no_resilient_food_primary_results.npy",
        results,
        allow_pickle=True,
    )

    scenarios_loader, constants_for_params = set_common_no_resilient_properties()

    constants_for_params = scenarios_loader.set_long_delayed_shutoff(
        constants_for_params
    )

    constants_for_params = scenarios_loader.set_global_waste_to_tripled_prices(
        constants_for_params
    )

    scenario_runner = ScenarioRunner()
    results = scenario_runner.run_and_analyze_scenario(
        constants_for_params, scenarios_loader
    )

    print(
        """Estimated percent people fed, no resilient foods, minus waste & delayed halt
         of nonhuman consumption """
    )

    print(results.percent_people_fed / 100 * 2100)
    print("")

    if plot_figures:
        Plotter.plot_fig_1ab(
            results,
            77,
            "World",
            True,
            False,
            scenarios_loader.scenario_description,
        )


def set_common_no_resilient_properties():
    scenarios_loader = Scenarios()

    constants_for_params = scenarios_loader.init_global_food_system_properties()

    constants_for_params = scenarios_loader.get_no_resilient_food_scenario(
        constants_for_params
    )

    constants_for_params = scenarios_loader.set_excess_to_zero(constants_for_params)

    constants_for_params = scenarios_loader.set_catastrophe_nutrition_profile(
        constants_for_params
    )

    constants_for_params = scenarios_loader.set_global_seasonality_nuclear_winter(
        constants_for_params
    )
    constants_for_params = scenarios_loader.set_global_grasses_nuclear_winter(
        constants_for_params
    )
    constants_for_params = scenarios_loader.set_stored_food_buffer_zero(
        constants_for_params
    )
    constants_for_params = scenarios_loader.set_efficient_feed_grazing_strategy(
        constants_for_params
    )

    constants_for_params = scenarios_loader.set_fish_nuclear_winter_reduction(
        constants_for_params
    )
    constants_for_params = scenarios_loader.include_protein(constants_for_params)

    constants_for_params = scenarios_loader.include_fat(constants_for_params)
    constants_for_params = scenarios_loader.cull_animals(constants_for_params)

    constants_for_params = (
        scenarios_loader.set_nuclear_winter_global_disruption_to_crops(
            constants_for_params
        )
    )

    return scenarios_loader, constants_for_params


if __name__ == "__main__":
    run_model_no_resilient_foods()
