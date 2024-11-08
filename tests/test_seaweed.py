from random import randint, random
from typing import Any

import pytest

from src.food_system.seaweed import Seaweed


@pytest.fixture
def constants_for_params() -> dict[str, Any]:
    return {
        "NMONTHS": randint(1, 120),
        "INITIAL_SEAWEED_FRACTION": random(),
        "SEAWEED_NEW_AREA_FRACTION": random(),
        "MAX_SEAWEED_AS_PERCENT_KCALS_HUMANS": randint(1, 99),
        "MAX_SEAWEED_AS_PERCENT_KCALS_FEED": randint(1, 99),
        "MAX_SEAWEED_AS_PERCENT_KCALS_BIOFUEL": randint(1, 99),
        "WASTE_DISTRIBUTION": {"SEAWEED": randint(1, 99)},
        "WASTE_RETAIL": randint(1, 99),
        "SEAWEED_GROWTH_PER_DAY": {str(ii - 3): random() * 10 for ii in range(120)},
    }


@pytest.mark.parametrize("add_seaweed", [True, False])
@pytest.mark.parametrize("seaweed_max_area_fraction", [0, random()])
def test_init(add_seaweed, seaweed_max_area_fraction, constants_for_params):
    constants_for_params["ADD_SEAWEED"] = add_seaweed
    constants_for_params["SEAWEED_MAX_AREA_FRACTION"] = seaweed_max_area_fraction
    sw = Seaweed(constants_for_params)
    assert isinstance(sw.NMONTHS, int)
    assert sw.NMONTHS == constants_for_params["NMONTHS"]
    assert isinstance(sw.MAX_SEAWEED_AS_PERCENT_KCALS_HUMANS, int)
    assert isinstance(sw.MAX_SEAWEED_AS_PERCENT_KCALS_FEED, int)
    assert isinstance(sw.MAX_SEAWEED_AS_PERCENT_KCALS_BIOFUEL, int)
    if add_seaweed:
        assert (
            sw.MAX_SEAWEED_AS_PERCENT_KCALS_HUMANS
            == constants_for_params["MAX_SEAWEED_AS_PERCENT_KCALS_HUMANS"]
        )
        assert (
            sw.MAX_SEAWEED_AS_PERCENT_KCALS_FEED
            == constants_for_params["MAX_SEAWEED_AS_PERCENT_KCALS_FEED"]
        )
        assert (
            sw.MAX_SEAWEED_AS_PERCENT_KCALS_BIOFUEL
            == constants_for_params["MAX_SEAWEED_AS_PERCENT_KCALS_BIOFUEL"]
        )
    else:
        assert sw.MAX_SEAWEED_AS_PERCENT_KCALS_HUMANS == 0
        assert sw.MAX_SEAWEED_AS_PERCENT_KCALS_FEED == 0
        assert sw.MAX_SEAWEED_AS_PERCENT_KCALS_BIOFUEL == 0
    assert sw.MAXIMUM_SEAWEED_AREA == pytest.approx(
        constants_for_params["SEAWEED_MAX_AREA_FRACTION"] * 1853
    )
    if seaweed_max_area_fraction == 0:
        assert sw.INITIAL_SEAWEED == 0
    else:
        assert isinstance(sw.INITIAL_SEAWEED, float)
        assert sw.INITIAL_SEAWEED == pytest.approx(
            constants_for_params["INITIAL_SEAWEED_FRACTION"] * 1
        )
    assert isinstance(sw.INITIAL_BUILT_SEAWEED_AREA, float)
    assert sw.INITIAL_BUILT_SEAWEED_AREA == pytest.approx(
        constants_for_params["SEAWEED_NEW_AREA_FRACTION"] * 0.1
    )
    assert isinstance(sw.SEAWEED_WASTE_RETAIL, int)
    assert sw.SEAWEED_WASTE_RETAIL == constants_for_params["WASTE_RETAIL"]
    assert isinstance(sw.SEAWEED_WASTE_DISTRIBUTION, int)
    assert (
        sw.SEAWEED_WASTE_DISTRIBUTION
        == constants_for_params["WASTE_DISTRIBUTION"]["SEAWEED"]
    )
    assert isinstance(sw.SEAWEED_KCALS, float)
    assert sw.SEAWEED_KCALS > 0
    assert isinstance(sw.SEAWEED_PROTEIN, float)
    assert sw.SEAWEED_PROTEIN > 0
    assert isinstance(sw.SEAWEED_PROTEIN, float)
    assert sw.SEAWEED_PROTEIN > 0


@pytest.mark.parametrize("add_seaweed", [True, False])
@pytest.mark.parametrize("seaweed_max_area_fraction", [0, random()])
def test_get_growth_rates(add_seaweed, seaweed_max_area_fraction, constants_for_params):
    constants_for_params["ADD_SEAWEED"] = add_seaweed
    constants_for_params["SEAWEED_MAX_AREA_FRACTION"] = seaweed_max_area_fraction
    sw = Seaweed(constants_for_params)
    gr = sw.get_growth_rates(constants_for_params)
    assert all(sw.growth_rates_monthly == gr)
    assert all([isinstance(x, float) for x in gr])
    assert all(gr >= 0)
    sorted_gr = dict(
        sorted(
            constants_for_params["SEAWEED_GROWTH_PER_DAY"].items(),
            key=lambda kv: int(kv[0]),
        )
    )
    for v1, v2 in zip(gr, sorted_gr.values()):
        assert v1 == pytest.approx(100 * (v2 / 100 + 1) ** 30)
