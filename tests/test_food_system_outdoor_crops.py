import pickle
from pathlib import Path

import git
import numpy as np
import pytest

from src.food_system.outdoor_crops import OutdoorCrops


@pytest.fixture
def constants_for_params() -> dict:
    """
    The file used here is a snapshot from a simulation run of
    the USA_extended.yaml scenario.
    The snapshot is of the ```constants_for_params``` dict,
    captured immediately before the instantiation of the OutdoorCrops class.
    """
    repo_root = git.Repo(".", search_parent_directories=True).working_dir
    test_data_path = (
        Path(repo_root)
        / "data"
        / "tests_data"
        / "outdoor_crops_constants_for_params_usa_extended_yaml.pickle"
    )
    with open(test_data_path, "rb") as f:
        return pickle.load(f)


def _get_fake_constants_for_params(expanded_area_scenario: str) -> dict:
    return {
        "NMONTHS": np.random.randint(13, 120 + 1),
        "STARTING_MONTH_NUM": np.random.randint(1, 12 + 1),
        "BASELINE_CROP_KCALS": np.random.random() * 1e9,
        "BASELINE_CROP_FAT": np.nan,
        "BASELINE_CROP_PROTEIN": np.nan,
        "ADD_OUTDOOR_GROWING": True,
        "WASTE_DISTRIBUTION": {"CROPS": np.nan},
        "WASTE_RETAIL": np.nan,
        "EXPANDED_AREA": expanded_area_scenario,
        "SEASONALITY": np.random.random(12),
    } | {
        f"expanded_area_{expanded_area_scenario}_kcals_year{year}": np.random.random()
        * 1e8
        for year in range(1, 11)
    }


def test_assign_increase_from_expanded_planted_area_usa_special(
    constants_for_params,
) -> None:
    outdoor_crops = OutdoorCrops(constants_for_params)
    outdoor_crops.calculate_rotation_ratios(constants_for_params)
    expanded_area = constants_for_params["EXPANDED_AREA"]
    assert (
        expanded_area != "none"
    ), "expanded area must be other than `none` to test its effects"
    # disable expanded area
    constants_for_params["EXPANDED_AREA"] = "none"
    outdoor_crops.calculate_monthly_production(constants_for_params)
    kcals_grown = outdoor_crops.KCALS_GROWN
    no_relocation_kcals_grown = outdoor_crops.NO_RELOCATION_KCALS_GROWN
    # re-enable expanded area
    constants_for_params["EXPANDED_AREA"] = expanded_area
    outdoor_crops.assign_increase_from_expanded_planted_area(constants_for_params)
    # compare before and after
    assert all(
        np.array(outdoor_crops.KCALS_GROWN) >= np.array(kcals_grown)
    ), "kcals grown decreased with expanded area"
    assert all(
        np.array(outdoor_crops.NO_RELOCATION_KCALS_GROWN)
        >= np.array(no_relocation_kcals_grown)
    ), "no relocation kcals grown decreased with expanded area"


@pytest.mark.parametrize("expanded_area_scenario", ["none", "no_trade", "export_pool"])
def test_assign_increase_from_expanded_planted_area_fake_constants_for_params(
    expanded_area_scenario,
) -> None:
    constants_for_params = _get_fake_constants_for_params(expanded_area_scenario)
    outdoor_crops = OutdoorCrops(constants_for_params)
    kcals_grown = list(np.random.random(outdoor_crops.NMONTHS) * 1e9)
    no_relocation_kcals_grown = list(np.random.random(outdoor_crops.NMONTHS) * 1e9)
    outdoor_crops.KCALS_GROWN = kcals_grown
    outdoor_crops.NO_RELOCATION_KCALS_GROWN = no_relocation_kcals_grown
    if expanded_area_scenario == "none":
        # this is expected to fail
        with pytest.raises(AssertionError):
            outdoor_crops.assign_increase_from_expanded_planted_area(
                constants_for_params
            )
    else:
        outdoor_crops.assign_increase_from_expanded_planted_area(constants_for_params)
        # compare before and after
        assert all(
            np.array(outdoor_crops.KCALS_GROWN) >= np.array(kcals_grown)
        ), "kcals grown decreased with expanded area"
        assert all(
            np.array(outdoor_crops.NO_RELOCATION_KCALS_GROWN)
            >= np.array(no_relocation_kcals_grown)
        ), "no relocation kcals grown decreased with expanded area"
