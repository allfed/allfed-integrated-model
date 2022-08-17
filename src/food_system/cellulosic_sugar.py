############################## Cellulosic Sugar ################################
##                                                                             #
##      Functions and constants relating to cellulosic sugar production        #
##                                                                             #
################################################################################

import numpy as np


class CellulosicSugar:
    def __init__(self, constants_for_params):

        # billion kcals a month for 100% population (7.8 billion people).
        self.GLOBAL_MONTHLY_NEEDS = 6793977 / 12

        self.NMONTHS = constants_for_params["NMONTHS"]
        self.INDUSTRIAL_FOODS_SLOPE_MULTIPLIER = constants_for_params[
            "INDUSTRIAL_FOODS_SLOPE_MULTIPLIER"
        ]
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
                    np.array([0.0] * 5 + [9.79] * 3 + [20] * 253),
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
            # @li nothing should need to be done here, but good to check that it works

        else:
            production_kcals_CS_per_month_long = [0] * self.NMONTHS

        self.production_kcals_CS_per_month = production_kcals_CS_per_month_long[
            0 : self.NMONTHS
        ]

    def get_monthly_cs_production(self):
        return self.production_kcals_CS_per_month
