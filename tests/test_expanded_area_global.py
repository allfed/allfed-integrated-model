import pytest

from src.scenarios.run_scenario import ScenarioRunner


@pytest.fixture
def global_result():
    results = {}
    for expanded_area_scenario in ["none", "no_trade", "export_pool"]:
        simulation_parameters = {
            "NMONTHS": 120,
            "crop_disruption": "global_nuclear_winter",
            "grasses": "global_nuclear_winter",
            "fish": "nuclear_winter",
            "seasonality": "nuclear_winter_globally",
            "scale": "global",
            "stored_food": "baseline",
            "nutrition": "catastrophe",
            "fat": "not_required",
            "protein": "not_required",
            "intake_constraints": "enabled",
            "scenario": "no_resilient_foods",
            "end_simulation_stocks_ratio": "no_stored_between_years",
            "cull": "do_eat_culled",
            "meat_strategy": "baseline_breeding",
            "waste": "baseline_globally",
            "shutoff": "continued_after_10_percent_fed",
            "expanded_area": expanded_area_scenario,
        }
        scenario_runner = ScenarioRunner()
        (
            constants_for_params,
            time_consts_for_params,
            scenario_loader,
        ) = scenario_runner.set_depending_on_option(simulation_parameters)
        interpreted_results = scenario_runner.run_and_analyze_scenario(
            constants_for_params,
            time_consts_for_params,
            scenario_loader,
            create_pptx_with_all_countries=False,
            show_country_figures=False,
            figure_save_postfix="_world",
            country_data=None,
            save_all_results=False,
            country_name="world",
            country_iso3="WOR",
            title="",
        )
        results[expanded_area_scenario] = interpreted_results
    return results


def test_expanded_area_is_better(global_result):
    for expanded_area_scenario in ["none", "no_trade", "export_pool"]:
        assert global_result[expanded_area_scenario] is not None
        assert len(global_result[expanded_area_scenario].outdoor_crops.kcals) == 120
    assert all(
        global_result["no_trade"].outdoor_crops.kcals
        >= global_result["none"].outdoor_crops.kcals
    )
    assert all(
        global_result["export_pool"].outdoor_crops.kcals
        >= global_result["no_trade"].outdoor_crops.kcals
    )
