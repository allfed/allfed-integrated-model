"""
######################## Methane Single Cell Protein ###########################
##                                                                             #
##            Functions and constants relating to methane SCP                  #
##                                                                             #
################################################################################
"""

import numpy as np
from src.food_system.food import Food


class MethaneSCP:
    def __init__(self, constants_for_params):
        self.INDUSTRIAL_FOODS_SLOPE_MULTIPLIER = constants_for_params[
            "INDUSTRIAL_FOODS_SLOPE_MULTIPLIER"
        ]

        self.NMONTHS = constants_for_params["NMONTHS"]

        self.SCP_KCALS_PER_KG = 5350
        self.SCP_FRAC_PROTEIN = 0.650
        self.SCP_FRAC_FAT = 0.09

        self.SCP_KCALS_TO_FAT_CONVERSION = (
            1e9 * self.SCP_FRAC_FAT / self.SCP_KCALS_PER_KG / 1e6
        )
        self.SCP_KCALS_TO_PROTEIN_CONVERSION = (
            1e9 * self.SCP_FRAC_PROTEIN / self.SCP_KCALS_PER_KG / 1e6
        )

        # feed can't be more than this fraction in terms of calories in any month
        self.MAX_FRACTION_HUMAN_FOOD_CONSUMED_AS_SCP = 0.3

        self.MAX_METHANE_SCP_AS_PERCENT_KCALS_FEED = 30
        self.MAX_METHANE_SCP_AS_PERCENT_KCALS_BIOFUEL = 100

        # billion kcals a month for country in question
        self.COUNTRY_MONTHLY_NEEDS = (
            constants_for_params["POP"] * Food.conversions.kcals_monthly / 1e9
        )

        # billion kcals a month for 100% population (7.8 billion people).
        self.GLOBAL_MONTHLY_NEEDS = (
            constants_for_params["GLOBAL_POP"] * Food.conversions.kcals_monthly / 1e9
        )

        self.MAX_METHANE_SCP_HUMANS_CAN_CONSUME_MONTHLY = (
            self.MAX_FRACTION_HUMAN_FOOD_CONSUMED_AS_SCP * self.COUNTRY_MONTHLY_NEEDS
        )

        # apply sugar waste also to methane scp, for lack of better baseline
        self.SCP_WASTE = constants_for_params["WASTE"]["SUGAR"]

    def calculate_monthly_scp_caloric_production(self, constants_for_params):
        if constants_for_params["ADD_METHANE_SCP"]:
            industrial_delay_months = [0] * constants_for_params["DELAY"][
                "INDUSTRIAL_FOODS_MONTHS"
            ]

            METHANE_SCP_PERCENT_KCALS = list(
                np.array(
                    industrial_delay_months
                    + [0] * 12
                    + [2] * 5
                    + [4]
                    + [7] * 5
                    + [9]
                    + [11] * 6
                    + [13]
                    + [15] * 210
                )
                / (1 - 0.12)
                * self.INDUSTRIAL_FOODS_SLOPE_MULTIPLIER
            )

            production_kcals_scp_per_month_long = []
            for global_percent_kcals_scp in METHANE_SCP_PERCENT_KCALS:
                production_kcals_scp_per_month_long.append(
                    global_percent_kcals_scp
                    / 100
                    * self.GLOBAL_MONTHLY_NEEDS
                    * constants_for_params["SCP_GLOBAL_PRODUCTION_FRACTION"]
                    * (1 - self.SCP_WASTE / 100)
                )
            self.production_kcals_scp_per_month_long = (
                production_kcals_scp_per_month_long
            )
        else:
            self.production_kcals_scp_per_month_long = [0] * self.NMONTHS

    def calculate_scp_fat_and_protein_production(self):
        self.production = Food()
        self.production.kcals = np.array(
            self.production_kcals_scp_per_month_long[0 : self.NMONTHS]
        )
        # billions of kcals converted to 1000s of tons protein
        self.production.protein = np.array(
            list(
                np.array(self.production.kcals)
                * 1e9
                * self.SCP_FRAC_PROTEIN
                / self.SCP_KCALS_PER_KG
                / 1e6
            )
        )

        # billions of kcals converted to 1000s of tons fat
        self.production.fat = np.array(
            list(
                np.array(self.production.kcals)
                * 1e9
                * self.SCP_FRAC_FAT
                / self.SCP_KCALS_PER_KG
                / 1e6
            )
        )

        self.production.set_units(
            kcals_units="billion kcals each month",
            fat_units="thousand tons each month",
            protein_units="thousand tons each month",
        )

        # self.postwaste = self * (1 - self.SCP_WASTE / 100)
