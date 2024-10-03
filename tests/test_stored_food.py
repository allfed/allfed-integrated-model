import re
from types import SimpleNamespace
from typing import Any

import numpy as np
import pytest

from src.food_system.food import Food
from src.food_system.stored_food import StoredFood


@pytest.fixture
def constants_for_params() -> dict[str, Any]:
    months = [
        "JAN",
        "FEB",
        "MAR",
        "APR",
        "MAY",
        "JUN",
        "JUL",
        "AUG",
        "SEP",
        "OCT",
        "NOV",
        "DEC",
    ]
    _dict = {
        "END_OF_MONTH_STOCKS": dict(zip(months, np.random.random(12) * 1e9)),
        "RATIO_STOCKS_UNTOUCHED": np.random.random(),
        "WASTE_DISTRIBUTION": {"CROPS": np.random.random() * 100},
    }
    _dict |= {
        "PERCENT_STORED_FOOD_TO_USE": (_dict["RATIO_STOCKS_UNTOUCHED"] + 0.1) * 100
    }
    return _dict


@pytest.fixture
def outdoor_crops() -> SimpleNamespace:
    obj = SimpleNamespace()
    obj.OG_FRACTION_FAT = np.random.random()
    obj.OG_FRACTION_PROTEIN = np.random.random()
    return obj


def test_init(constants_for_params, outdoor_crops):
    sf = StoredFood(constants_for_params, outdoor_crops)
    assert isinstance(sf.end_of_month_stocks, list)
    assert len(sf.end_of_month_stocks) == 12
    assert all([isinstance(el, float) for el in sf.end_of_month_stocks])
    for v1, v2 in zip(
        sf.end_of_month_stocks, constants_for_params["END_OF_MONTH_STOCKS"].values()
    ):
        # this should work because we insert months in order in the fixture
        assert v1 == v2
    assert isinstance(sf.ratio_lowest_stocks_untouched, float)
    assert (
        sf.ratio_lowest_stocks_untouched
        == constants_for_params["RATIO_STOCKS_UNTOUCHED"]
    )
    assert isinstance(sf.percent_stored_food_to_use, float)
    assert (
        sf.percent_stored_food_to_use
        == constants_for_params["PERCENT_STORED_FOOD_TO_USE"]
    )
    assert isinstance(sf.CROP_WASTE_DISTRIBUTION, float)
    assert (
        sf.CROP_WASTE_DISTRIBUTION
        == constants_for_params["WASTE_DISTRIBUTION"]["CROPS"]
    )
    assert isinstance(sf.SF_FRACTION_FAT, float)
    assert sf.SF_FRACTION_FAT == outdoor_crops.OG_FRACTION_FAT
    assert isinstance(sf.SF_FRACTION_PROTEIN, float)
    assert sf.SF_FRACTION_PROTEIN == outdoor_crops.OG_FRACTION_PROTEIN


@pytest.mark.parametrize("starting_month", list(range(1, 13)))
def test_calculate_stored_food_to_use(
    constants_for_params, outdoor_crops, starting_month
):
    sf = StoredFood(constants_for_params, outdoor_crops)
    sf.calculate_stored_food_to_use(starting_month)
    assert isinstance(sf.initial_available, Food)
    assert isinstance(sf.initial_available.kcals, float)
    assert sf.initial_available.kcals >= 0
    assert isinstance(sf.initial_available.fat, float)
    assert sf.initial_available.fat >= 0
    assert isinstance(sf.initial_available.protein, float)
    assert sf.initial_available.protein >= 0
    assert sf.initial_available.kcals_units == "billion kcals"
    assert sf.initial_available.fat_units == "thousand tons"
    assert sf.initial_available.protein_units == "thousand tons"


@pytest.mark.parametrize("starting_month", [-1, 0, 13, 14])
def test_calculate_stored_food_to_use_starting_month_error(
    constants_for_params, outdoor_crops, starting_month
):
    sf = StoredFood(constants_for_params, outdoor_crops)
    with pytest.raises(
        AssertionError,
        match=re.escape("ERROR: starting month must be within [1,12]"),
    ):
        sf.calculate_stored_food_to_use(starting_month)


@pytest.mark.parametrize("starting_month", list(range(1, 13)))
def test_calculate_stored_food_to_use_ratio_error(
    constants_for_params, outdoor_crops, starting_month
):
    constants_for_params["PERCENT_STORED_FOOD_TO_USE"] = (
        constants_for_params["RATIO_STOCKS_UNTOUCHED"] - 0.1
    ) * 100
    sf = StoredFood(constants_for_params, outdoor_crops)
    with pytest.raises(
        AssertionError,
        match=re.escape(
            "ERROR: fraction_stored_food_to_use must be greater or equal to the ratio_lowest_stocks_untouched"
        ),
    ):
        sf.calculate_stored_food_to_use(starting_month)
