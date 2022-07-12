############################## Cellulosic Sugar ################################
##                                                                             #
##      Functions and constants relating to cellulosic sugar production        #
##                                                                             #
################################################################################

import numpy as np


class CellulosicSugar:
    def __init__(self, inputs_to_optimizer):

        # billion kcals a month for 100% population (7.8 billion people).
        self.GLOBAL_MONTHLY_NEEDS = 6793977 / 12

        self.NMONTHS = inputs_to_optimizer["NMONTHS"]
        self.INDUSTRIAL_FOODS_SLOPE_MULTIPLIER = inputs_to_optimizer[
            "INDUSTRIAL_FOODS_SLOPE_MULTIPLIER"
        ]
        self.SUGAR_WASTE = inputs_to_optimizer["WASTE"]["SUGAR"]

    # this all comes from one of Juan's recently published industrial foods
    # papers
    def calculate_monthly_cs_production(self, inputs_to_optimizer):

        if inputs_to_optimizer["ADD_CELLULOSIC_SUGAR"]:

            industrial_delay_months = [0] * inputs_to_optimizer["DELAY"][
                "INDUSTRIAL_FOODS_MONTHS"
            ]

            CELL_SUGAR_PERCENT_KCALS = list(
                np.append(
                    industrial_delay_months,
                    np.array([0.0] * 5 + [9.79] * 3 + [20] * 253),
                )
                * 1
                / (1 - 0.12)
                * self.INDUSTRIAL_FOODS_SLOPE_MULTIPLIER
            )

            production_kcals_CS_per_month_long = []
            for x in CELL_SUGAR_PERCENT_KCALS:
                production_kcals_CS_per_month_long.append(
                    x
                    / 100
                    * self.GLOBAL_MONTHLY_NEEDS
                    * inputs_to_optimizer["CS_GLOBAL_PRODUCTION_FRACTION"]
                    * (1 - self.SUGAR_WASTE / 100)
                )
        else:
            production_kcals_CS_per_month_long = [0] * self.NMONTHS

        self.production_kcals_CS_per_month = production_kcals_CS_per_month_long[
            0 : self.NMONTHS
        ]

    def get_monthly_cs_production(self):
        return self.production_kcals_CS_per_month
