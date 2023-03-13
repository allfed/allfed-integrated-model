"""

Functions and constants relating to cellulosic sugar production

"""

import numpy as np
from src.food_system.food import Food


class CellulosicSugar:
    def __init__(self, constants_for_params):
        # billion kcals a month for 100% population (7.8 billion people).
        self.GLOBAL_MONTHLY_NEEDS = (
            constants_for_params["GLOBAL_POP"] * Food.conversions.kcals_monthly / 1e9
        )

        self.NMONTHS = constants_for_params["NMONTHS"]
        self.INDUSTRIAL_FOODS_SLOPE_MULTIPLIER = constants_for_params[
            "INDUSTRIAL_FOODS_SLOPE_MULTIPLIER"
        ]
        self.MAX_FRACTION_FEED_CONSUMED_AS_CELLULOSIC_SUGAR = 0.3
        self.MAX_FRACTION_BIOFUEL_CONSUMED_AS_CELLULOSIC_SUGAR = (
            1  # All of biofuel can be CS
        )

        self.SUGAR_WASTE = constants_for_params["WASTE"]["SUGAR"]

    # this all comes from one of Juan's recently published industrial foods
    # papers
    def calculate_monthly_cs_production(self, constants_for_params):
        if constants_for_params["ADD_CELLULOSIC_SUGAR"]:
            industrial_delay_months = [0] * constants_for_params["DELAY"][
                "INDUSTRIAL_FOODS_MONTHS"
            ]
            CELL_SUGAR_PERCENT_KCALS = list(
                np.append(
                    industrial_delay_months,
                    np.array([0.0] * 5 + [4.7] * 3 + [9.5] * 253),
                )
                * 1
                / (1 - 0.12)
                * self.INDUSTRIAL_FOODS_SLOPE_MULTIPLIER
            )

            # @li we need to be able to import by-country data here

            production_kcals_CS_per_month_long = []
            for x in CELL_SUGAR_PERCENT_KCALS:
                production_kcals_CS_per_month_long.append(
                    x
                    / 100
                    * self.GLOBAL_MONTHLY_NEEDS
                    * constants_for_params["CS_GLOBAL_PRODUCTION_FRACTION"]
                    * (1 - self.SUGAR_WASTE / 100)
                )
        self.production_kcals_CS_per_month = production_kcals_CS_per_month_long[
            0 : self.NMONTHS
        ]

        self.for_humans = Food()
        # self.for_humans.set_to_zero_after_month(0)
        self.for_humans.kcals = self.production_kcals_CS_per_month

        self.for_humans.set_units(
            kcals_units="billion kcals each month",
            fat_units="thousand tons each month",
            protein_units="thousand tons each month",
        )
