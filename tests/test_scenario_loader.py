from operator import itemgetter
from pathlib import Path
from random import random

import git
import pandas as pd
import pytest
from pulp import constants

from src.scenarios.scenarios import Scenarios


@pytest.fixture
def country_data() -> pd.Series:
    repo_root = git.Repo(".", search_parent_directories=True).working_dir
    no_trade_table = pd.read_csv(
        Path(repo_root) / "data" / "no_food_trade" / "computer_readable_combined.csv"
    )
    country_data = no_trade_table.sample(1).squeeze()
    assert isinstance(country_data, pd.Series), "country data format is incorrect"
    return country_data


@pytest.mark.parametrize("expanded_area_scenario", ["none", "export_pool", "no_trade"])
def test_set_expanded_area(country_data, expanded_area_scenario) -> None:
    scenario_loader = Scenarios()
    scenario_loader.IS_GLOBAL_ANALYSIS = False
    scenario_loader.scenario_description += "nuclear winter crops"
    scenario_description = scenario_loader.scenario_description
    constants_for_params = {"NMONTHS": 120}
    scenario_loader.set_expanded_area(
        constants_for_params,
        expanded_area_scenario,
        country_data,
    )
    assert (
        scenario_loader.scenario_description != scenario_description
    ), "scenario description remains unchanged"
    assert constants_for_params["EXPANDED_AREA"] in [
        "none",
        "no_trade",
        "export_pool",
    ], "expanded area scenario is set incorrectly"
    if expanded_area_scenario != "none":
        # TODO: this assumes "NMONTHS" = 120, as for the forseable future
        # this is what we want, however, we might need to update this
        # should we plan to vary the time span
        expanded_area_years_in_data = [
            c
            for c in country_data.index
            if expanded_area_scenario in c
            and "kcals" in c  # TODO: include protein and fat
        ]
        expanded_area_years_in_constants = [
            k for k in constants_for_params if expanded_area_scenario in k
        ]
        assert len(expanded_area_years_in_data) == len(
            expanded_area_years_in_constants
        ), "number of expanded area years does not match between country data and set constants"
        assert all(
            [
                isinstance(v, float)
                for v in itemgetter(*expanded_area_years_in_constants)(
                    constants_for_params
                )
            ]
        ), "expanded area yiels are not all floating point numbers"
