"""
################################# Outdoor Crops ###############################
##                                                                            #
##       Functions and constants relating to outdoor crop production          #
##                                                                            #
###############################################################################
"""

import numpy as np
from src.food_system.food import Food


class OutdoorCrops:
    def __init__(self, constants_for_params):
        super().__init__()

        self.NMONTHS = constants_for_params["NMONTHS"]

        self.ADD_OUTDOOR_GROWING = constants_for_params["ADD_OUTDOOR_GROWING"]

        self.CROP_WASTE_DISTRIBUTION = constants_for_params["WASTE_DISTRIBUTION"][
            "CROPS"
        ]
        self.CROP_WASTE_RETAIL = constants_for_params["WASTE_RETAIL"]

        self.OG_FRACTION_FAT = constants_for_params["OG_FRACTION_FAT"]
        self.OG_FRACTION_PROTEIN = constants_for_params["OG_FRACTION_PROTEIN"]

    def calculate_rotation_ratios(self, constants_for_params):
        # need to use the multiplier on units of kcals to get fat and protein
        if constants_for_params["OG_USE_BETTER_ROTATION"]:
            self.OG_KCAL_EXPONENT = constants_for_params["ROTATION_IMPROVEMENTS"][
                "POWER_LAW_IMPROVEMENT"
            ]

            self.OG_ROTATION_FRACTION_KCALS = 1

            self.KCAL_RATIO_ROTATION = 1
            self.FAT_ROTATION_RATIO = constants_for_params["ROTATION_IMPROVEMENTS"][
                "FAT_RATIO"
            ]
            self.PROTEIN_ROTATION_RATIO = constants_for_params["ROTATION_IMPROVEMENTS"][
                "PROTEIN_RATIO"
            ]

            self.OG_ROTATION_FRACTION_FAT = (
                constants_for_params["OG_FRACTION_FAT"] * self.FAT_ROTATION_RATIO
            )
            self.OG_ROTATION_FRACTION_PROTEIN = (
                constants_for_params["OG_FRACTION_PROTEIN"]
                * self.PROTEIN_ROTATION_RATIO
            )

            self.FAT_RATIO_ROTATION = self.OG_ROTATION_FRACTION_FAT
            self.PROTEIN_RATIO_ROTATION = self.OG_ROTATION_FRACTION_PROTEIN
        else:
            self.OG_KCAL_EXPONENT = 1
            self.OG_ROTATION_FRACTION_KCALS = 1
            self.OG_ROTATION_FRACTION_FAT = constants_for_params["OG_FRACTION_FAT"]
            self.OG_ROTATION_FRACTION_PROTEIN = constants_for_params[
                "OG_FRACTION_PROTEIN"
            ]

            self.KCAL_RATIO_ROTATION = 1
            self.FAT_RATIO_ROTATION = constants_for_params["OG_FRACTION_FAT"]
            self.PROTEIN_RATIO_ROTATION = constants_for_params["OG_FRACTION_PROTEIN"]

    def assign_increase_from_relocated_crops(self, constants_for_params, time_consts):
        baseline_reduction = time_consts["baseline_reduction"]
        production_no_relocation = time_consts["KCALS_GROWN_NO_RELOCATION"]
        new_kcals_grown = []
        self.DOMESTIC_SUPPLY_AFTER_RELOCATION = []
        for i in range(self.NMONTHS):
            # if there's some very small negative value here, just round it off to zero
            if baseline_reduction[i] <= 0:
                baseline_reduction[i] = round(baseline_reduction[i], 8)

            assert baseline_reduction[i] >= 0  # 8 decimal places rounding

            if baseline_reduction[i] == 0 or baseline_reduction[i] > 1:
                new_kcals_grown.append(
                    production_no_relocation[i]
                )  # month_kcals * baseline_reduction)
            else:
                # currently is this:
                # production_no_relocation=baseline_yield * baseline_reduction
                # needs to be this:
                # new_kcals_grown = baseline_yield * baseline_reduction**OG_KCAL_EXPONENT
                # so multiply as:
                # production_no_relocation
                #   = production_no_relocation * (baseline_reduction**OG_KCAL_EXPONENT/baseline_reduction)

                new_kcals_grown.append(
                    production_no_relocation[i]
                    * (
                        baseline_reduction[i]
                        ** constants_for_params["ROTATION_IMPROVEMENTS"][
                            "POWER_LAW_IMPROVEMENT"
                        ]
                    )
                    / baseline_reduction[i]
                )

            assert (
                new_kcals_grown[-1] >= production_no_relocation[i]
            ), "ERROR: Relocation has somehow decreased crop production!"

            # need to add the increase computed here to the domestic supply
            self.DOMESTIC_SUPPLY_AFTER_RELOCATION.append(
                time_consts["domestic_supply"][i]
                + (new_kcals_grown[i] - production_no_relocation[i])
            )

        self.KCALS_GROWN_AFTER_RELOCATION = new_kcals_grown

    def assign_increase_from_increased_cultivated_area(self, constants_for_params):
        assert (
            constants_for_params["RATIO_INCREASED_CROP_AREA"] >= 1
        ), "ERROR: cannot decrease crop area as an adaptation.."
        if constants_for_params["RATIO_INCREASED_CROP_AREA"] == 1:
            self.DOMESTIC_SUPPLY_AFTER_MORE_AREA = self.DOMESTIC_SUPPLY_AFTER_RELOCATION
            self.KCALS_GROWN_AFTER_MORE_AREA = self.KCALS_GROWN_AFTER_RELOCATION
            return
        # Constants

        N = constants_for_params["INITIAL_HARVEST_DURATION_IN_MONTHS"]
        max_value = constants_for_params["RATIO_INCREASED_CROP_AREA"]
        total_months = (
            constants_for_params["NUMBER_YEARS_TAKES_TO_REACH_INCREASED_AREA"] * 12
        )

        # Create the linspace
        linspace = np.ones(self.NMONTHS)

        # Calculate the increment per month after the delay
        increment = (max_value - 1) / (total_months - N)

        # Update the linspace values
        for i in range(N, total_months):
            linspace[i] = 1 + (i - N) * increment

        # Maintain the value after the specified number of years
        linspace[total_months:] = max_value

        self.KCALS_GROWN_AFTER_MORE_AREA = np.multiply(
            self.KCALS_GROWN_AFTER_RELOCATION, (1 - linspace)
        )

        # increase the kcals grown using the increased ratio due to increased area
        # linspace is the ratio of new crop area, so 1 - linspace is the fractional increase in crop area.
        # we assume cold toleran crops can't be exported, so domestic production increase all goes towards the
        # domestic supply
        self.DOMESTIC_SUPPLY_AFTER_MORE_AREA = []
        self.KCALS_GROWN_AFTER_MORE_AREA = []
        for i in range(self.NMONTHS):
            increase_from_more_area = self.KCALS_GROWN_AFTER_RELOCATION[i] * (
                1 - linspace[i]
            )
            self.DOMESTIC_SUPPLY_AFTER_MORE_AREA.append(
                self.DOMESTIC_SUPPLY_AFTER_RELOCATION[i] + increase_from_more_area
            )
            self.KCALS_GROWN_AFTER_MORE_AREA.append(
                self.KCALS_GROWN_AFTER_RELOCATION[i] + increase_from_more_area
            )

    def set_crop_production_minus_greenhouse_area(
        self, constants_for_params, time_consts_inputs, greenhouse_fraction_area
    ):
        if self.ADD_OUTDOOR_GROWING:
            if constants_for_params["OG_USE_BETTER_ROTATION"]:
                crops_produced = np.array([0] * self.NMONTHS)

                hd = (
                    constants_for_params["INITIAL_HARVEST_DURATION_IN_MONTHS"]
                    + constants_for_params["DELAY"]["ROTATION_CHANGE_IN_MONTHS"]
                )

                crops_produced[:hd] = np.multiply(
                    np.array(time_consts_inputs["KCALS_GROWN_NO_RELOCATION"][:hd]),
                    (1 - greenhouse_fraction_area[:hd]),
                )

                crops_produced[hd:] = np.multiply(
                    np.array(self.KCALS_GROWN_AFTER_RELOCATION[hd:]),
                    (1 - greenhouse_fraction_area[hd:]),
                )

            else:
                crops_produced = np.array(
                    time_consts_inputs["KCALS_GROWN_NO_RELOCATION"]
                )

        else:
            crops_produced = np.array([0] * self.NMONTHS)

        self.production = Food(
            kcals=np.array(crops_produced) * (1 - self.CROP_WASTE_DISTRIBUTION / 100),
            fat=np.array(constants_for_params["OG_FRACTION_FAT"] * crops_produced)
            * (1 - self.CROP_WASTE_DISTRIBUTION / 100),
            protein=np.array(
                constants_for_params["OG_FRACTION_PROTEIN"] * crops_produced
            )
            * (1 - self.CROP_WASTE_DISTRIBUTION / 100),
            kcals_units="billion kcals each month",
            fat_units="thousand tons each month",
            protein_units="thousand tons each month",
        )

        assert not np.isnan(
            self.production.kcals
        ).any(), """Error: the outdoor crop production expected is
            unknown, cannot compute optimization"""
