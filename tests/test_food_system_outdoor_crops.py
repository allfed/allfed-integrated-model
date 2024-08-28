import pickle
from pathlib import Path

import git
import pytest

from src.food_system.outdoor_crops import OutdoorCrops


@pytest.fixture
def constants_for_params() -> OutdoorCrops:
    repo_root = git.Repo(".", search_parent_directories=True).working_dir
    test_data_path = (
        Path(repo_root)
        / "data"
        / "tests_data"
        / "outdoor_crops_constants_for_params_usa_extended_yaml.pickle"
    )
    with open(test_data_path, "rb") as f:
        return pickle.load(f)


def test_assign_increase_from_expanded_planted_area(constants_for_params) -> None:
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
    assert (
        outdoor_crops.KCALS_GROWN >= kcals_grown
    ), "kcals grown decreased with expanded area"
    assert (
        outdoor_crops.NO_RELOCATION_KCALS_GROWN >= no_relocation_kcals_grown
    ), "no relocation kcals grown decreased with expanded area"
