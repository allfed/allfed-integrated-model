from itertools import product
from random import randint, random
from types import SimpleNamespace
from typing import Any

import numpy as np
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

    @pytest.fixture
    def outdoor_crops(self):
        months_cycle = np.random.random(12) * 1e3
        exponent = random()
        reductions = np.random.random(200)
        kcals_grown = np.random.random(200) * 1e3
        return SimpleNamespace(
            months_cycle=months_cycle,
            all_months_reductions=reductions,
            OG_KCAL_EXPONENT=exponent,
            KCALS_GROWN=kcals_grown,
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

    def test_assign_producivity_from_climate_impact(self, constants_for_params):
        gh = Greenhouses(constants_for_params)
        months_cycle = np.random.random(12) * 1e3
        if gh.TOTAL_CROP_AREA == 0:
            with pytest.raises(AssertionError, match="total crop area cannot be zero"):
                gh.assign_productivity_reduction_from_climate_impact(
                    [1], np.random.random(gh.NMONTHS - 1), 0.5, 0.5
                )
            return
        else:
            with pytest.raises(AssertionError, match="not enough reduction values"):
                gh.assign_productivity_reduction_from_climate_impact(
                    [1], np.random.random(gh.NMONTHS - 1), 0.5, 0.5
                )

        with pytest.raises(AssertionError):
            # reductions must be numpy array
            gh.assign_productivity_reduction_from_climate_impact(
                months_cycle, [-1e-9] * gh.NMONTHS, 0.5, 0.5
            )

        crop_waste_coeff = random()
        exponent = random()
        reductions = np.random.random(gh.NMONTHS + 1)
        # all_months_reduction cases
        # case 1
        # all > 1
        gh.assign_productivity_reduction_from_climate_impact(
            months_cycle, reductions + 1, exponent, crop_waste_coeff
        )
        assert all([isinstance(x, float) for x in gh.GH_KCALS_GROWN_PER_HECTARE])
        assert (gh.GH_KCALS_GROWN_PER_HECTARE > 0).all()
        assert gh.GH_KCALS_GROWN_PER_HECTARE == pytest.approx(
            np.mean(months_cycle)
            * (reductions[: gh.NMONTHS] + 1)
            * crop_waste_coeff
            / gh.TOTAL_CROP_AREA
        )
        # case 2
        # all < 1 but > 0
        gh.assign_productivity_reduction_from_climate_impact(
            months_cycle, reductions, exponent, crop_waste_coeff
        )
        assert all([isinstance(x, float) for x in gh.GH_KCALS_GROWN_PER_HECTARE])
        assert (gh.GH_KCALS_GROWN_PER_HECTARE > 0).all()
        assert gh.GH_KCALS_GROWN_PER_HECTARE == pytest.approx(
            np.mean(months_cycle)
            * reductions[: gh.NMONTHS] ** exponent
            * crop_waste_coeff
            / gh.TOTAL_CROP_AREA
        )
        # case 3
        # < 0 --> assertion error
        with pytest.raises(AssertionError):
            gh.assign_productivity_reduction_from_climate_impact(
                months_cycle, reductions - 1, exponent, crop_waste_coeff
            )
        # case 4
        # < 0 but only slighlty (1e-9) --> all get set to 0
        gh.assign_productivity_reduction_from_climate_impact(
            months_cycle, np.array([-1e-9] * gh.NMONTHS), exponent, crop_waste_coeff
        )
        assert not any(gh.GH_KCALS_GROWN_PER_HECTARE)
        # exponent cases:
        # < 1 --> correct (already checked above)
        # > 1 --> should break
        with pytest.raises(
            AssertionError, match="Relocation has somehow decreased crop production!"
        ):
            gh.assign_productivity_reduction_from_climate_impact(
                months_cycle, reductions, exponent + 1, crop_waste_coeff
            )

    def test_get_greenhouse_area(
        self, add_greenhouses, constants_for_params, outdoor_crops
    ):
        gh = Greenhouses(constants_for_params)
        gh_area = gh.get_greenhouse_area(constants_for_params, outdoor_crops)
        assert isinstance(gh_area, np.ndarray)
        assert len(gh_area) == constants_for_params["NMONTHS"]
        if gh.TOTAL_CROP_AREA == 0:
            assert not any(gh_area)
        else:
            if add_greenhouses:
                assert not any(
                    gh_area[: 5 + constants_for_params["DELAY"]["GREENHOUSE_MONTHS"]]
                )
                assert all(
                    gh_area[
                        5 + constants_for_params["DELAY"]["GREENHOUSE_MONTHS"] + 1 :
                    ]
                    > 0
                )
                assert gh_area[
                    5 + constants_for_params["DELAY"]["GREENHOUSE_MONTHS"] + 36 :
                ] == pytest.approx(gh.TOTAL_CROP_AREA * gh.GREENHOUSE_AREA_MULTIPLIER)
            else:
                assert isinstance(gh.GH_KCALS_GROWN_PER_HECTARE, list)
                assert len(gh.GH_KCALS_GROWN_PER_HECTARE) == gh.NMONTHS
                assert not any(gh.GH_KCALS_GROWN_PER_HECTARE)
                assert not any(gh_area)
                assert isinstance(gh.greenhouse_fraction_area, np.ndarray)
                assert not any(gh.greenhouse_fraction_area)
