from inspect import Attribute
from itertools import product
from random import randint, random
from typing import Any

import pytest

from src.food_system.greenhouses import Greenhouses


@pytest.mark.parametrize(
    ("add_greenhouses", "initial_crop_area_fraction"),
    list(product([True, False], [0, random()])),
)
class TestGreenhouses:
    @pytest.fixture
    def constants_for_params(
        self, add_greenhouses, initial_crop_area_fraction
    ) -> dict[str, Any]:
        _d = {
            "NMONTHS": randint(2, 120),
            "WASTE_DISTRIBUTION": {"CROPS": randint(1, 99)},
            "WASTE_RETAIL": randint(1, 99),
            "ADD_GREENHOUSES": add_greenhouses,
            "INITIAL_GLOBAL_CROP_AREA": (0.5 + random()) * 1e9,
            "INITIAL_CROP_AREA_FRACTION": initial_crop_area_fraction,
            "GREENHOUSE_AREA_MULTIPLIER": random(),
        }
        return (
            _d
            | {"DELAY": {"GREENHOUSE_MONTHS": randint(0, _d["NMONTHS"] - 1)}}
            | {"STARTING_MONTH_NUM": randint(0, _d["NMONTHS"] - 1)}
        )

    def test_init(self, add_greenhouses, constants_for_params):
        gh = Greenhouses(constants_for_params)
        assert isinstance(gh.TOTAL_CROP_AREA, float)
        assert gh.TOTAL_CROP_AREA / constants_for_params[
            "INITIAL_GLOBAL_CROP_AREA"
        ] == pytest.approx(constants_for_params["INITIAL_CROP_AREA_FRACTION"])
        assert isinstance(gh.STARTING_MONTH_NUM, int)
        assert gh.STARTING_MONTH_NUM == constants_for_params["STARTING_MONTH_NUM"]
        assert isinstance(gh.ADD_GREENHOUSES, bool)
        assert gh.ADD_GREENHOUSES == add_greenhouses
        assert isinstance(gh.NMONTHS, int)
        assert gh.NMONTHS == constants_for_params["NMONTHS"]
        if add_greenhouses:
            assert isinstance(gh.greenhouse_delay, int)
            assert (
                gh.greenhouse_delay
                == constants_for_params["DELAY"]["GREENHOUSE_MONTHS"]
            )
            assert isinstance(gh.GREENHOUSE_AREA_MULTIPLIER, float)
            assert gh.GREENHOUSE_AREA_MULTIPLIER == pytest.approx(
                constants_for_params["GREENHOUSE_AREA_MULTIPLIER"]
            )
        else:
            assert gh.GREENHOUSE_AREA_MULTIPLIER == 0
            with pytest.raises(AttributeError):
                assert isinstance(gh.greenhouse_delay, int)
