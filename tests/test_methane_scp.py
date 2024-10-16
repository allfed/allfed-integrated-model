from random import randint, random
from typing import Any

import pytest

from src.food_system.food import Food
from src.food_system.methane_scp import MethaneSCP


@pytest.fixture
def constants_for_params() -> dict[str, Any]:
    _dict = {
        "INDUSTRIAL_FOODS_SLOPE_MULTIPLIER": random() * 3,
        "NMONTHS": randint(1, 120),
        "POP": random() * 8e9,
        "WASTE_DISTRIBUTION": {"SUGAR": randint(1, 99)},
        "WASTE_RETAIL": randint(1, 99),
        "CS_GLOBAL_PRODUCTION_FRACTION": random(),
    }
    _dict |= {"DELAY": {"INDUSTRIAL_FOODS_MONTHS": randint(1, _dict["NMONTHS"] - 1)}}
    _dict |= {"GLOBAL_POP": _dict["POP"] * 10}
    return _dict


def test_init(constants_for_params):
    assert Food.conversions
    Food.conversions.kcals_monthly = 2100 * 30
    mscp = MethaneSCP(constants_for_params)
    assert isinstance(mscp.NMONTHS, int)
    assert mscp.NMONTHS >= 1
    assert mscp.NMONTHS == constants_for_params["NMONTHS"]
    assert isinstance(mscp.SCP_KCALS_PER_KG, float)
    assert isinstance(mscp.SCP_FRAC_PROTEIN, float)
    assert 0 <= mscp.SCP_FRAC_PROTEIN <= 1
    assert isinstance(mscp.SCP_FRAC_FAT, float)
    assert 0 <= mscp.SCP_FRAC_FAT <= 1
    assert isinstance(mscp.SCP_KCALS_TO_PROTEIN_CONVERSION, float)
    assert isinstance(mscp.SCP_KCALS_TO_FAT_CONVERSION, float)
    assert isinstance(mscp.COUNTRY_MONTHLY_NEEDS, float)
    assert isinstance(mscp.GLOBAL_MONTHLY_NEEDS, float)
    assert mscp.GLOBAL_MONTHLY_NEEDS > mscp.COUNTRY_MONTHLY_NEEDS
    assert isinstance(mscp.SCP_WASTE_RETAIL, int)
    assert mscp.SCP_WASTE_RETAIL == constants_for_params["WASTE_RETAIL"]
    assert isinstance(mscp.SCP_WASTE_DISTRIBUTION, int)
    assert (
        mscp.SCP_WASTE_DISTRIBUTION
        == constants_for_params["WASTE_DISTRIBUTION"]["SUGAR"]
    )
