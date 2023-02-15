"""
################################# Greenhouses #################################
##                                                                            #
##       Functions and constants relating to greenhouse crop productio        #
##                                                                            #`
###############################################################################
"""

import numpy as np


class Greenhouses:
    def __init__(self, constants_for_params):
        # 500 million hectares in tropics (for outdoor crops 2020)
        # GLOBAL CROP AREA INCLUDING US:
        # (calculated from sum of crop area in between 23 latitude)
        self.TOTAL_CROP_AREA = (
            769176.2e3 * constants_for_params["INITIAL_CROP_AREA_FRACTION"]
        )

        self.STARTING_MONTH_NUM = constants_for_params["STARTING_MONTH_NUM"]

        self.ADD_GREENHOUSES = constants_for_params["ADD_GREENHOUSES"]
        self.NMONTHS = constants_for_params["NMONTHS"]

        if self.ADD_GREENHOUSES:
            # this is in addition to the 5 month delay till harvest
            self.greenhouse_delay = constants_for_params["DELAY"]["GREENHOUSE_MONTHS"]
            self.GREENHOUSE_AREA_MULTIPLIER = constants_for_params[
                "GREENHOUSE_AREA_MULTIPLIER"
            ]
        else:
            self.GREENHOUSE_AREA_MULTIPLIER = 0

    def assign_productivity_reduction_from_climate_impact(
        self, months_cycle, all_months_reductions, exponent, CROP_WASTE
    ):

        MONTHLY_KCALS = np.mean(months_cycle) / self.TOTAL_CROP_AREA

        KCALS_GROWN_PER_HECTARE_BEFORE_WASTE = []
        for i in range(self.NMONTHS):
            baseline_reduction = all_months_reductions[i]
            assert round(baseline_reduction, 8) >= 0  # 8 decimal places rounding

            # if there's some very small negative value here, just round it off to zero
            if baseline_reduction <= 0:
                baseline_reduction = round(baseline_reduction, 8)
            assert baseline_reduction >= 0  # 8 decimal places rounding

            assert (baseline_reduction >= 0).all()

            if baseline_reduction > 1:
                KCALS_GROWN_PER_HECTARE_BEFORE_WASTE.append(
                    MONTHLY_KCALS * baseline_reduction
                )
            else:
                KCALS_GROWN_PER_HECTARE_BEFORE_WASTE.append(
                    MONTHLY_KCALS * baseline_reduction**exponent
                )
        assert (
            KCALS_GROWN_PER_HECTARE_BEFORE_WASTE
            >= MONTHLY_KCALS * all_months_reductions
        ).all(), "ERROR: Relocation has somehow decreased crop production!"

        self.GH_KCALS_GROWN_PER_HECTARE = (1 - CROP_WASTE / 100) * np.array(
            KCALS_GROWN_PER_HECTARE_BEFORE_WASTE
        )

    def get_greenhouse_area(self, constants_for_params, outdoor_crops):

        # greenhouses tab
        # assumption: greenhouse crop production is very similar in nutritional
        # profile to stored food
        # reference:
        # greenhouse paper (scaling of greenhouses in low sunlight scenarios)
        # At constant expansion for 36 months, the cumulative ground coverage
        # will equal 2.5 million km^2 (250 million hectares).
        # Takes 5+36=41 months to reach full output
        # NOTE: the 5 months represents the delay from plant to harvest.

        if self.TOTAL_CROP_AREA == 0:
            self.greenhouse_fraction_area = np.zeros(self.NMONTHS)
            return np.zeros(self.NMONTHS)

        if self.ADD_GREENHOUSES:
            GREENHOUSE_LIMIT_AREA = (
                self.TOTAL_CROP_AREA * self.GREENHOUSE_AREA_MULTIPLIER
            )
            self.greenhouse_area_long = list(
                np.append(
                    np.append(
                        np.append(
                            np.linspace(0, 0, self.greenhouse_delay),
                            np.linspace(0, 0, 5),
                        ),
                        np.linspace(0, GREENHOUSE_LIMIT_AREA, 37),
                    ),
                    np.linspace(
                        GREENHOUSE_LIMIT_AREA,
                        GREENHOUSE_LIMIT_AREA,
                        len(outdoor_crops.KCALS_GROWN) - 42,
                    ),
                )
            )
            greenhouse_area = np.array(self.greenhouse_area_long[0 : self.NMONTHS])

            self.assign_productivity_reduction_from_climate_impact(
                outdoor_crops.months_cycle,
                outdoor_crops.all_months_reductions,
                outdoor_crops.OG_KCAL_EXPONENT,
                constants_for_params["WASTE"]["CROPS"],
            )
        else:
            self.GH_KCALS_GROWN_PER_HECTARE = [0] * self.NMONTHS
            greenhouse_area = np.array([0] * self.NMONTHS)

        self.greenhouse_fraction_area = greenhouse_area / self.TOTAL_CROP_AREA
        return greenhouse_area

    # SUM_CALORIES is an overestimate by some factor, as it is in current
    # day conditions. We improve accuracy by applying the outdoor growing
    # estimate and decreasing the estimated fat and protein by the same
    # factor that kcals are decreased by
    def get_greenhouse_yield_per_ha(self, constants_for_params, outdoor_crops):
        KCAL_RATIO = outdoor_crops.KCAL_RATIO_ROTATION
        FAT_RATIO = outdoor_crops.FAT_RATIO_ROTATION
        PROTEIN_RATIO = outdoor_crops.PROTEIN_RATIO_ROTATION
        if not self.ADD_GREENHOUSES:
            greenhouse_kcals_per_ha = [0] * self.NMONTHS
            greenhouse_fat_per_ha = [0] * self.NMONTHS
            greenhouse_protein_per_ha = [0] * self.NMONTHS
            return (
                greenhouse_kcals_per_ha,
                greenhouse_fat_per_ha,
                greenhouse_protein_per_ha,
            )

        # if constants_for_params["REDUCED_BREEDING_STRATEGY"]:
        # billion_kcals_per_month_gh = [
        #     0,
        #     0,
        #     0,
        #     0,
        #     0,
        #     0,
        #     5827,
        #     5827,
        #     5827,
        #     5827,
        #     5827,
        #     11654,
        #     11654,
        #     11654,
        #     11654,
        #     11654,
        #     17481,
        #     17481,
        #     17481,
        #     17481,
        #     17481,
        #     23308,
        #     23308,
        #     23308,
        #     23308,
        #     23308,
        #     29135,
        #     29135,
        #     29135,
        #     29135,
        #     29135,
        #     34962,
        #     34962,
        #     34962,
        #     34962,
        #     34962,
        #     40789,
        #     40789,
        #     40789,
        #     40789,
        #     40789,
        #     46616,
        #     46616,
        #     46616,
        #     46616,
        #     46616,
        #     52444,
        #     52444,
        #     52444,
        #     52444,
        #     52444,
        #     58271,
        #     58271,
        #     58271,
        #     58271,
        #     58271,
        #     64098,
        #     64098,
        #     64098,
        #     64098,
        #     64098,
        #     69925,
        #     69925,
        #     69925,
        #     69925,
        #     68159,
        #     69925,
        #     69925,
        #     69925,
        #     69925,
        #     68159,
        #     69925,
        #     69925,
        #     69925,
        #     69925,
        #     68159,
        #     69925,
        #     69925,
        #     69925,
        #     69925,
        #     68159,
        #     69925,
        #     69925,
        #     69925,
        #     69925,
        #     68159,
        #     69925,
        #     69925,
        #     69925,
        #     69925,
        #     68159,
        #     69925,
        #     69925,
        #     69925,
        #     69925,
        #     68159,
        #     69925,
        #     69925,
        #     69925,
        #     69925,
        #     68159,
        #     69925,
        #     69925,
        #     69925,
        #     69925,
        #     68159,
        #     69925,
        #     69925,
        #     69925,
        #     69925,
        #     68159,
        #     69925,
        #     69925,
        #     69925,
        #     69925,
        #     68159,
        #     69925,
        #     69925,
        #     69925,
        #     69925,
        # ]
        # GH_KCALS_GROWN_PER_HECTARE = (
        #     1 - constants_for_params["WASTE"]["CROPS"] / 100
        # ) * np.divide(billion_kcals_per_month_gh, self.greenhouse_area_long)
        # # units: billion kcals per hectare
        # return (
        #     GH_KCALS_GROWN_PER_HECTARE,
        #     FAT_RATIO * GH_KCALS_GROWN_PER_HECTARE,
        #     PROTEIN_RATIO * GH_KCALS_GROWN_PER_HECTARE,
        # )

        relocation_kcals_per_ha_long = []
        relocated_fat_per_ha_long = []
        relocation_protein_per_ha_long = []

        for kcals_per_month in self.GH_KCALS_GROWN_PER_HECTARE:
            gh_kcals = (
                kcals_per_month
                * KCAL_RATIO
                * (1 + constants_for_params["GREENHOUSE_GAIN_PCT"] / 100)
            )  # units: billion kcals per month

            relocation_kcals_per_ha_long.append(gh_kcals)

            relocated_fat_per_ha_long.append(FAT_RATIO * gh_kcals)

            relocation_protein_per_ha_long.append(PROTEIN_RATIO * gh_kcals)

        relocation_kcals_per_ha = relocation_kcals_per_ha_long[0 : self.NMONTHS]
        relocation_fat_per_ha = relocated_fat_per_ha_long[0 : self.NMONTHS]
        relocation_protein_per_ha = relocation_protein_per_ha_long[0 : self.NMONTHS]

        return (
            relocation_kcals_per_ha,
            relocation_fat_per_ha,
            relocation_protein_per_ha,
        )
