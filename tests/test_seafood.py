from random import randint
from typing import Any

import numpy as np
import pytest

from src.food_system.food import Food
from src.food_system.seafood import Seafood


@pytest.fixture
def constants_for_params() -> dict[str, Any]:
    return {
        "NMONTHS": randint(1, 120),
        "ADD_FISH": True,
        "WASTE_DISTRIBUTION": {"SEAFOOD": randint(1, 99)},
        "WASTE_RETAIL": randint(1, 99),
        "FISH_DRY_CALORIC_ANNUAL": randint(int(1e9), int(2e9)),
        "FISH_PROTEIN_TONS_ANNUAL": randint(int(1e3), int(2e3)),
        "FISH_FAT_TONS_ANNUAL": randint(int(1e3), int(2e3)),
    }


def test_init(constants_for_params):
    sf = Seafood(constants_for_params)
    assert isinstance(sf.NMONTHS, int)
    assert sf.NMONTHS >= 1
    assert isinstance(sf.ADD_FISH, bool)
    assert isinstance(sf.FISH_KCALS, float)
    assert sf.FISH_KCALS > 0
    assert isinstance(sf.FISH_PROTEIN, float)
    assert sf.FISH_PROTEIN > 0
    assert isinstance(sf.FISH_FAT, float)
    assert sf.FISH_FAT > 0


@pytest.mark.parametrize("add_fish", [True, False])
def test_set_seafood_production(constants_for_params, add_fish):
    time_consts_for_params = {
        "FISH_PERCENT_MONTHLY": [
            randint(1, 200) for _ in range(constants_for_params["NMONTHS"])
        ]
    }
    constants_for_params["ADD_FISH"] = add_fish
    sf = Seafood(constants_for_params)
    sf.set_seafood_production(time_consts_for_params)
    assert isinstance(sf.to_humans, Food)
    assert isinstance(sf.to_humans.kcals, np.ndarray)
    assert sf.to_humans.kcals.dtype == float
    assert isinstance(sf.to_humans.protein, np.ndarray)
    assert sf.to_humans.protein.dtype == float
    assert isinstance(sf.to_humans.fat, np.ndarray)
    assert sf.to_humans.fat.dtype == float
    assert sf.to_humans.kcals_units == "billion kcals each month"
    assert sf.to_humans.protein_units == "thousand tons each month"
    assert sf.to_humans.fat_units == "thousand tons each month"
    assert sf.to_humans.kcals.shape == (constants_for_params["NMONTHS"],)
    assert sf.to_humans.protein.shape == (constants_for_params["NMONTHS"],)
    assert sf.to_humans.fat.shape == (constants_for_params["NMONTHS"],)
    if add_fish:
        assert np.all(sf.to_humans.kcals)
        assert np.all(sf.to_humans.protein)
        assert np.all(sf.to_humans.fat)
    else:
        assert not np.any(sf.to_humans.kcals)
        assert not np.any(sf.to_humans.protein)
        assert not np.any(sf.to_humans.fat)
