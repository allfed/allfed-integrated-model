"""
This file runs the Argentina no-trade scenario many times, each time changing the value of
a single parameter in the yaml file. Tests are run to ensure that the change in the
output is as expected.
"""
import itertools
import pytest

from src.scenarios import run_scenarios_from_yaml
from src.scenarios.run_model_no_trade import ScenarioRunnerNoTrade

test_tolerance = 0.1  # The percent difference between two results that is considered a real difference
test_scenario_key = "argentina_test"
scenario_runner = ScenarioRunnerNoTrade()


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


@pytest.fixture(scope="module")
def run_all_combinations():
    """
    This runs the model for many combinations of parameters, and returns the results

    Yields:
        list: A list of dicts, each containing the parameters and results for a single run
    """
    # List to store the results
    results = []

    # The number of possible combinations of parameters is very large so we cannot test
    # all of them. Similarly, a direct Monte Carlo approach would not be feasible because
    # it would be very rare for all parameters to remain constant except one. Perhaps
    # we could implement a Monte Carlo where only one parameter is varied at a time, which
    # solve this problem, but then the issue becomes that we would not know ahead of time
    # which parameters we are really testing, making the tests more opaque.
    # Instead, we will test all combinations of a few important parameters (the parameters
    # for which we know ahead of time in whuch direction the results should change), and
    # repeat this complete search of the sub-space for a few combinations of the other
    # parameters.
    #
    # The list below gives the sets of parameters that will remain constant for each
    # complete search of the sub-space.
    base_config_data_list = [
        {
            "settings": {"countries": "ARG", "NMONTHS": 120},
            "simulations": {
                test_scenario_key: {
                    "title": "Argentina Net Food Production, Nuclear Winter",
                    "scale": "country",
                    "seasonality": "country",
                    "grasses": "country_nuclear_winter",
                    "fish": "nuclear_winter",
                    "fat": "not_required",
                    "protein": "not_required",
                    "nutrition": "catastrophe",
                    "end_simulation_stocks_ratio": "zero",
                    "shutoff": "continued",
                    "cull": "do_eat_culled",
                    "meat_strategy": "reduce_breeding_USA",
                }
            }
        },
        {
            "settings": {"countries": "ARG", "NMONTHS": 120},
            "simulations": {
                test_scenario_key: {
                    "title": "Argentina Net Food Production, Nuclear Winter",
                    "scale": "country",
                    "seasonality": "country",
                    "grasses": "baseline",
                    "fish": "baseline",
                    "fat": "not_required",
                    "protein": "not_required",
                    "nutrition": "baseline",
                    "end_simulation_stocks_ratio": "zero",
                    "shutoff": "short_delayed_shutoff",
                    "cull": "dont_eat_culled",
                    "meat_strategy": "baseline_breeding",
                }
            }
        }
    ]
    for i_base_config_data, base_config_data in enumerate(base_config_data_list):
        # The parameters to vary. All combinations of these parameters will be tested
        scenario_options = [
            "no_resilient_foods",
            "all_resilient_foods",
            "all_resilient_foods_and_more_area",
            "seaweed",
            "methane_scp",
            "cellulosic_sugar",
            "relocated_crops",
            "greenhouse",
            "industrial_foods",
        ]
        crop_disruption_options = ["country_nuclear_winter", "zero"]
        intake_constraints_options = ["enabled", "disabled_for_humans"]
        stored_food_options = ["zero", "baseline"]
        waste_options = [
            "baseline_in_country",
            "doubled_prices_in_country",
            "tripled_prices_in_country",
        ]

        number_of_runs = (
            len(scenario_options)
            * len(crop_disruption_options)
            * len(intake_constraints_options)
            * len(stored_food_options)
            * len(waste_options)
        )
        print(f"Running {number_of_runs} scenarios")

        # Loop over all combinations of parameters
        for combination in itertools.product(
            scenario_options,
            crop_disruption_options,
            intake_constraints_options,
            stored_food_options,
            waste_options,
        ):
            # Create a new config data for this combination
            config_data = base_config_data.copy()
            config_data["simulations"][test_scenario_key]["scenario"] = combination[0]
            config_data["simulations"][test_scenario_key][
                "crop_disruption"
            ] = combination[1]
            config_data["simulations"][test_scenario_key][
                "intake_constraints"
            ] = combination[2]
            config_data["simulations"][test_scenario_key]["stored_food"] = combination[
                3
            ]
            config_data["simulations"][test_scenario_key]["waste"] = combination[4]
            # Run the model
            percent_people_fed = runner(config_data)
            # Store the results as a dict
            results.append(
                {
                    "scenario": combination[0],
                    "crop_disruption": combination[1],
                    "intake_constraints": combination[2],
                    "stored_food": combination[3],
                    "waste": combination[4],
                    "percent_people_fed": percent_people_fed,
                    "base_config_data": i_base_config_data,
                }
            )
    return results


def select_runs(results, independent_parameter):
    """
    Takes the results list created by run_all_combinations, and returns a dictionary
    of lists, where each list contains the results for a single combination of parameters,
    excluding the independent_parameter

    For example, if the independent_parameter is "scenario", then all items in a given
    list will have the same values for "crop_disruption", "nutrition", and "waste", etc.
    but different values for "scenario"
    """
    grouped_elements = {}

    # Iterate through each dictionary in the list
    for item in results:
        # Create a key based on the values excluding 'scenario' and 'percent_people_fed'
        key = tuple(
            item[k]
            for k in item
            if k not in [independent_parameter, "percent_people_fed"]
        )

        # Group the dictionaries by this key
        if key not in grouped_elements:
            grouped_elements[key] = [item]
        else:
            grouped_elements[key].append(item)

    # Select and return the groups with more than one element
    return grouped_elements


def test_resilient_foods(run_all_combinations):
    """
    This test compares results assuming different resilient foods are available. The test passes if more
    resilient foods result in more people fed. More specifically, we verify that:
        "no_resilient_foods"
        <= ("seaweed","methane_scp","cellulosic_sugar","relocated_crops","greenhouse","industrial_foods")
        <= "all_resilient_foods"
        <= "all_resilient_foods_and_more_area"
        and that
        "methane_scp" <= "industrial_foods"
        "cellulosic_sugar" <= "industrial_foods"
    This is repeated for all available combinations of the other parameters
    """
    select_runs_results = select_runs(run_all_combinations, "scenario")
    print(select_runs_results)
    for key, runs in select_runs_results.items():
        no_resilient_food_result = None
        seaweed_only_result = None
        methane_scp_only_result = None
        cellulosic_sugar_only_result = None
        relocated_crops_only_result = None
        greenhouse_only_result = None
        industrial_foods_only_result = None
        all_resilient_food_result = None
        all_resilient_food_and_more_area_result = None
        for run in runs:
            if run["scenario"] == "no_resilient_foods":
                no_resilient_food_result = run["percent_people_fed"]
            elif run["scenario"] == "seaweed":
                seaweed_only_result = run["percent_people_fed"]
            elif run["scenario"] == "methane_scp":
                methane_scp_only_result = run["percent_people_fed"]
            elif run["scenario"] == "cellulosic_sugar":
                cellulosic_sugar_only_result = run["percent_people_fed"]
            elif run["scenario"] == "relocated_crops":
                relocated_crops_only_result = run["percent_people_fed"]
            elif run["scenario"] == "greenhouse":
                greenhouse_only_result = run["percent_people_fed"]
            elif run["scenario"] == "industrial_foods":
                industrial_foods_only_result = run["percent_people_fed"]
            elif run["scenario"] == "all_resilient_foods":
                all_resilient_food_result = run["percent_people_fed"]
            elif run["scenario"] == "all_resilient_foods_and_more_area":
                all_resilient_food_and_more_area_result = run["percent_people_fed"]
            else:
                raise ValueError("Unexpected scenario")
        # Now we check if all conditions are met
        assert (
            no_resilient_food_result <= seaweed_only_result + test_tolerance
        ), "Including seaweed cannot decrease the number of people fed"
        assert (
            no_resilient_food_result <= methane_scp_only_result + test_tolerance
        ), "Including methane SCP cannot decrease the number of people fed"
        assert (
            no_resilient_food_result <= cellulosic_sugar_only_result + test_tolerance
        ), "Including cellulosic sugar cannot decrease the number of people fed"
        assert (
            no_resilient_food_result <= relocated_crops_only_result + test_tolerance
        ), "Including relocated crops cannot decrease the number of people fed"
        assert (
            no_resilient_food_result <= greenhouse_only_result + test_tolerance
        ), "Including greenhouse cannot decrease the number of people fed"
        assert (
            no_resilient_food_result <= industrial_foods_only_result + test_tolerance
        ), "Including industrial foods cannot decrease the number of people fed"
        assert (
            methane_scp_only_result <= industrial_foods_only_result + test_tolerance
        ), "Adding cellulosic sugar cannot decrease the number of people fed compared to having just methane SCP"
        assert (
            cellulosic_sugar_only_result
            <= industrial_foods_only_result + test_tolerance
        ), "Adding methane SCP cannot decrease the number of people fed compared to having just cellulosic sugar"
        assert (
            seaweed_only_result <= all_resilient_food_result + test_tolerance
        ), "Adding all resilient foods cannot decrease the number of people fed compared to having just seaweed"
        assert (
            methane_scp_only_result <= all_resilient_food_result + test_tolerance
        ), "Adding all resilient foods cannot decrease the number of people fed compared to having just methane SCP"
        assert (
            cellulosic_sugar_only_result <= all_resilient_food_result + test_tolerance
        ), "Adding all resilient foods cannot decrease the number of people fed compared to having just cellulosic sugar"
        assert (
            relocated_crops_only_result <= all_resilient_food_result + test_tolerance
        ), "Adding all resilient foods cannot decrease the number of people fed compared to having just relocated crops"
        # test disabled due to all_resilient_foods assuming low_area_greenhouse
        # assert (
        #    greenhouse_only_result <= all_resilient_food_result + test_tolerance
        # ), "Adding all resilient foods cannot decrease the number of people fed compared to having just greenhouse"
        assert (
            industrial_foods_only_result <= all_resilient_food_result + test_tolerance
        ), "Adding all resilient foods cannot decrease the number of people fed compared to having just industrial foods"
        assert (
            all_resilient_food_result
            <= all_resilient_food_and_more_area_result + test_tolerance
        ), "Adding more area cannot decrease the number of people fed compared to having just resilient foods"


def test_intake_constraints(run_all_combinations):
    """
    Verifies that using intake_constraints enabled results in more people fed than using
    disabled_for_humans
    """
    select_runs_results = select_runs(run_all_combinations, "intake_constraints")
    for key, runs in select_runs_results.items():
        enabled_result = None
        disabled_result = None
        for run in runs:
            if run["intake_constraints"] == "enabled":
                enabled_result = run["percent_people_fed"]
            elif run["intake_constraints"] == "disabled_for_humans":
                disabled_result = run["percent_people_fed"]
            else:
                raise ValueError("Unexpected intake_constraints")
        assert (
            enabled_result >= disabled_result - test_tolerance
        ), "Using intake_constraints enabled must result in more people fed than using disabled_for_humans"


def test_stored_food(run_all_combinations):
    """
    Verifies that storing no food results in fewer people fed than storing food
    """
    select_runs_results = select_runs(run_all_combinations, "stored_food")
    for key, runs in select_runs_results.items():
        zero_result = None
        baseline_result = None
        for run in runs:
            if run["stored_food"] == "zero":
                zero_result = run["percent_people_fed"]
            elif run["stored_food"] == "baseline":
                baseline_result = run["percent_people_fed"]
            else:
                raise ValueError("Unexpected stored_food")
        assert (
            zero_result <= baseline_result + test_tolerance
        ), "Storing no food must result in fewer people fed than storing food"


def test_waste(run_all_combinations):
    """
    Verifies that wasting more food results in fewer people fed
    """
    select_runs_results = select_runs(run_all_combinations, "waste")
    for key, runs in select_runs_results.items():
        baseline_result = None
        doubled_prices_result = None
        tripled_prices_result = None
        for run in runs:
            if run["waste"] == "baseline_in_country":
                baseline_result = run["percent_people_fed"]
            elif run["waste"] == "doubled_prices_in_country":
                doubled_prices_result = run["percent_people_fed"]
            elif run["waste"] == "tripled_prices_in_country":
                tripled_prices_result = run["percent_people_fed"]
            else:
                raise ValueError("Unexpected waste")
        assert (
            baseline_result <= doubled_prices_result + test_tolerance
        ), "Wasting more food must result in fewer people fed"
        assert (
            doubled_prices_result <= tripled_prices_result + test_tolerance
        ), "Wasting more food must result in fewer people fed"


def test_nuclear_crop_reduction(run_all_combinations):
    """
    Verifies that reducing crop production due to nuclear winter results in fewer people fed
    Note that this test assumes that nuclear winter reduces crop production, which is not
    necessarily the case for all countries (but it is true for Argentina)
    """
    select_runs_results = select_runs(run_all_combinations, "crop_disruption")
    for key, runs in select_runs_results.items():
        nuclear_winter_result = None
        zero_result = None
        for run in runs:
            if run["crop_disruption"] == "country_nuclear_winter":
                nuclear_winter_result = run["percent_people_fed"]
            elif run["crop_disruption"] == "zero":
                zero_result = run["percent_people_fed"]
            else:
                raise ValueError("Unexpected crop_disruption")
        assert (
            nuclear_winter_result <= zero_result + test_tolerance
        ), "Reducing crop production due to nuclear winter must result in fewer people fed"
