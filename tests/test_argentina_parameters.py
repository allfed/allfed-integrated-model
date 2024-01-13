"""
This file runs the Argentina scenario many times, each time changing the value of
a single parameter in the yaml file. Tests are run to ensure that the change in the
output is as expected.
"""
from src.scenarios import run_scenarios_from_yaml
from src.scenarios.run_model_no_trade import ScenarioRunnerNoTrade

# The name of the scenario to test
test_scenario_key = "argentina_test"

# The scenario runner
scenario_runner = ScenarioRunnerNoTrade()

# The base configuration data
# These are the base parameters for the scenario, which we will change one at a time
base_config_data = {
    "settings": {"countries": "ARG", "NMONTHS": 120},
    "simulations": {
        test_scenario_key: {
            "title": "Argentina Net Food Production, Nuclear Winter",
            "scale": "country",
            "scenario": "no_resilient_foods",
            "seasonality": "country",
            "grasses": "country_nuclear_winter",
            "crop_disruption": "country_nuclear_winter",
            "fish": "nuclear_winter",
            "waste": "baseline_in_country",
            "fat": "not_required",
            "protein": "not_required",
            "nutrition": "catastrophe",
            "intake_constraints": "enabled",
            "stored_food": "baseline",
            "end_simulation_stocks_ratio": "zero",
            "shutoff": "continued",
            "cull": "do_eat_culled",
            "meat_strategy": "reduce_breeding_USA",
        }
    },
}


def runner(config_data):
    """
    Runs a single-country no-trade scenario, and returns the percent of people fed

    Args:
        config_data (dict): The configuration data for the scenario

    Returns:
        float: The percent of people fed
    """
    if "countries" in config_data["settings"]:
        countries = config_data["settings"]["countries"]
    else:
        raise ValueError("No country specified for the tests")
    if isinstance(countries, str):
        countries = [countries]
    else:
        raise ValueError("Only one country supported for the tests")
    nmonths = config_data["settings"]["NMONTHS"]
    config_data["simulations"][test_scenario_key]["NMONTHS"] = nmonths
    _, _, _, interpreted_results = scenario_runner.run_model_no_trade(
        title=config_data["simulations"][test_scenario_key]["title"],
        create_pptx_with_all_countries=False,
        show_country_figures=False,
        show_map_figures=False,
        add_map_slide_to_pptx=False,
        scenario_option=config_data["simulations"][test_scenario_key],
        countries_list=countries,
        figure_save_postfix=f"_{test_scenario_key}",
        return_results=True,
    )
    percent_people_fed = interpreted_results[
        list(interpreted_results.keys())[0]
    ].percent_people_fed
    return percent_people_fed


def test_resilient_foods():
    """
    This test compares results assuming different resilient foods are available.
    The test passes if more resilient foods result in more people fed.
    More specifically, we verify that:
        "no_resilient_foods"
        <= ("seaweed","methane_scp","cellulosic_sugar","relocated_crops","greenhouse","industrial_foods")
        <= "all_resilient_foods"
        <= "all_resilient_foods_and_more_area"
        and that
        "methane_scp" <= "industrial_foods"
        "cellulosic_sugar" <= "industrial_foods"
    """
    # (1) No resilient foods
    no_resilient_food_config_data = base_config_data.copy()
    assert (
        no_resilient_food_config_data["simulations"][test_scenario_key]["scenario"]
        == "no_resilient_foods"
    )
    no_resilient_food_result = runner(no_resilient_food_config_data)

    # (2) All resilient foods
    all_resilient_food_config_data = base_config_data.copy()
    all_resilient_food_config_data["simulations"][test_scenario_key][
        "scenario"
    ] = "all_resilient_foods"
    all_resilient_food_result = runner(all_resilient_food_config_data)

    # (3) All resilient foods and more area
    all_resilient_food_and_more_area_config_data = base_config_data.copy()
    all_resilient_food_and_more_area_config_data["simulations"][test_scenario_key][
        "scenario"
    ] = "all_resilient_foods_and_more_area"
    all_resilient_food_and_more_area_result = runner(
        all_resilient_food_and_more_area_config_data
    )

    # (4) Seaweed only
    seaweed_only_config_data = base_config_data.copy()
    seaweed_only_config_data["simulations"][test_scenario_key]["scenario"] = "seaweed"
    seaweed_only_result = runner(seaweed_only_config_data)

    # (5) Methane SCP only
    methane_scp_only_config_data = base_config_data.copy()
    methane_scp_only_config_data["simulations"][test_scenario_key][
        "scenario"
    ] = "methane_scp"
    methane_scp_only_result = runner(methane_scp_only_config_data)

    # (6) Cellulosic sugar only
    cellulosic_sugar_only_config_data = base_config_data.copy()
    cellulosic_sugar_only_config_data["simulations"][test_scenario_key][
        "scenario"
    ] = "cellulosic_sugar"
    cellulosic_sugar_only_result = runner(cellulosic_sugar_only_config_data)

    # (7) Relocated crops only
    relocated_crops_only_config_data = base_config_data.copy()
    relocated_crops_only_config_data["simulations"][test_scenario_key][
        "scenario"
    ] = "relocated_crops"
    relocated_crops_only_result = runner(relocated_crops_only_config_data)

    # (8) Greenhouse only
    greenhouse_only_config_data = base_config_data.copy()
    greenhouse_only_config_data["simulations"][test_scenario_key][
        "scenario"
    ] = "greenhouse"
    greenhouse_only_result = runner(greenhouse_only_config_data)

    # (9) Industrial foods only
    industrial_foods_only_config_data = base_config_data.copy()
    industrial_foods_only_config_data["simulations"][test_scenario_key][
        "scenario"
    ] = "industrial_foods"
    industrial_foods_only_result = runner(industrial_foods_only_config_data)

    # Now we check if all conditions are met
    assert (
        no_resilient_food_result <= seaweed_only_result
    ), "Including seaweed cannot decrease the number of people fed"
    assert (
        no_resilient_food_result <= methane_scp_only_result
    ), "Including methane SCP cannot decrease the number of people fed"
    assert (
        no_resilient_food_result <= cellulosic_sugar_only_result
    ), "Including cellulosic sugar cannot decrease the number of people fed"
    assert (
        no_resilient_food_result <= relocated_crops_only_result
    ), "Inclding relocated crops cannot decrease the number of people fed"
    assert (
        no_resilient_food_result <= greenhouse_only_result
    ), "Including greenhouse cannot decrease the number of people fed"
    assert (
        no_resilient_food_result <= industrial_foods_only_result
    ), "Including industrial foods cannot decrease the number of people fed"
    assert (
        methane_scp_only_result <= industrial_foods_only_result
    ), "Adding cellulosic sugar cannot decrease the number of people fed compared to having just methane SCP"
    assert (
        cellulosic_sugar_only_result <= industrial_foods_only_result
    ), "Adding methane SCP cannot decrease the number of people fed compared to having just cellulosic sugar"
    assert (
        seaweed_only_result <= all_resilient_food_result
    ), "Adding all resilient foods cannot decrease the number of people fed compared to having just seaweed"
    assert (
        methane_scp_only_result <= all_resilient_food_result
    ), "Adding all resilient foods cannot decrease the number of people fed compared to having just methane SCP"
    assert (
        cellulosic_sugar_only_result <= all_resilient_food_result
    ), "Adding all resilient foods cannot decrease the number of people fed compared to having just cellulosic sugar"
    assert (
        relocated_crops_only_result <= all_resilient_food_result
    ), "Adding all resilient foods cannot decrease the number of people fed compared to having just relocated crops"
    assert (
        greenhouse_only_result <= all_resilient_food_result
    ), "Adding all resilient foods cannot decrease the number of people fed compared to having just greenhouse"
    assert (
        industrial_foods_only_result <= all_resilient_food_result
    ), "Adding all resilient foods cannot decrease the number of people fed compared to having just industrial foods"
    assert (
        all_resilient_food_result <= all_resilient_food_and_more_area_result
    ), "Adding more area cannot decrease the number of people fed compared to having just resilient foods"

