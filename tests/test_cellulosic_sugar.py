from random import randint
from typing import Any

import numpy as np
import pytest

from src.food_system.cellulosic_sugar import CellulosicSugar
from src.food_system.food import Food


@pytest.fixture
def constants_for_params() -> dict[str, Any]:
    _dict = {
        "NMONTHS": randint(2, 120),
        "ADD_CELLULOSIC_SUGAR": True,
        "WASTE_DISTRIBUTION": {"SUGAR": randint(1, 99)},
        "WASTE_RETAIL": randint(1, 99),
        "INDUSTRIAL_FOODS_SLOPE_MULTIPLIER": np.random.random() * 3,
        "POP": np.random.random() * 8e9,
        "CS_GLOBAL_PRODUCTION_FRACTION": np.random.random(),
    }
    _dict |= {"DELAY": {"INDUSTRIAL_FOODS_MONTHS": randint(1, _dict["NMONTHS"] - 1)}}
    _dict |= {"GLOBAL_POP": _dict["POP"] * 10}
    return _dict


def test_init(constants_for_params):
    assert Food.conversions
    Food.conversions.kcals_monthly = 2100 * 30
    cs = CellulosicSugar(constants_for_params)
    assert isinstance(cs.NMONTHS, int)
    assert cs.NMONTHS >= 1
    assert isinstance(cs.GLOBAL_MONTHLY_NEEDS, float)
    assert cs.GLOBAL_MONTHLY_NEEDS > 0
    assert (
        cs.INDUSTRIAL_FOODS_SLOPE_MULTIPLIER
        == constants_for_params["INDUSTRIAL_FOODS_SLOPE_MULTIPLIER"]
    )
    assert (
        cs.SUGAR_WASTE_DISTRIBUTION
        == constants_for_params["WASTE_DISTRIBUTION"]["SUGAR"]
    )
    assert cs.SUGAR_WASTE_RETAIL == constants_for_params["WASTE_RETAIL"]


@pytest.mark.parametrize("add_sugar", [True, False])
def test_calculate_monthly_cs_production(constants_for_params, add_sugar):
    constants_for_params["ADD_CELLULOSIC_SUGAR"] = add_sugar
    assert Food.conversions
    Food.conversions.kcals_monthly = 2100 * 30
    cs = CellulosicSugar(constants_for_params)
    cs.calculate_monthly_cs_production(constants_for_params)
    assert isinstance(cs.production_kcals_CS_per_month, np.ndarray)
    assert cs.production_kcals_CS_per_month.shape == (constants_for_params["NMONTHS"],)
    assert isinstance(cs.production, Food)
    assert isinstance(cs.production.kcals, np.ndarray)
    assert cs.production.kcals.dtype == float
    assert isinstance(cs.production.protein, np.ndarray)
    assert cs.production.protein.dtype == float
    assert isinstance(cs.production.fat, np.ndarray)
    assert cs.production.fat.dtype == float
    assert cs.production.kcals_units == "billion kcals each month"
    assert cs.production.protein_units == "thousand tons each month"
    assert cs.production.fat_units == "thousand tons each month"
    assert cs.production.kcals.shape == (constants_for_params["NMONTHS"],)
    assert cs.production.protein.shape == (constants_for_params["NMONTHS"],)
    assert cs.production.fat.shape == (constants_for_params["NMONTHS"],)
    assert np.all(cs.production.kcals == cs.production_kcals_CS_per_month)
    assert not np.any(
        cs.production.kcals[
            : constants_for_params["DELAY"]["INDUSTRIAL_FOODS_MONTHS"] + 5
        ]
    )
    if add_sugar:
        assert np.all(
            cs.production.kcals[
                constants_for_params["DELAY"]["INDUSTRIAL_FOODS_MONTHS"] + 5 :
            ]
        )
        assert not np.any(cs.production.protein)
        assert not np.any(cs.production.fat)
    else:
        assert not np.any(cs.production.kcals)
        assert not np.any(cs.production.protein)
        assert not np.any(cs.production.fat)
