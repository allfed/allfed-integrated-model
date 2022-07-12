######################## Methane Single Cell Protein ###########################
##                                                                             #
##            Functions and constants relating to methane SCP                  #
##                                                                             #
################################################################################


import numpy as np


class MethaneSCP:
    def __init__(self, inputs_to_optimizer):
        self.INDUSTRIAL_FOODS_SLOPE_MULTIPLIER = inputs_to_optimizer[
            "INDUSTRIAL_FOODS_SLOPE_MULTIPLIER"
        ]

        self.NMONTHS = inputs_to_optimizer["NMONTHS"]

        self.SCP_KCALS_PER_KG = 5350
        self.SCP_FRAC_PROTEIN = 0.650
        self.SCP_FRAC_FAT = 0.09

        # billion kcals a month for 100% population (7.8 billion people).
        self.GLOBAL_MONTHLY_NEEDS = 6793977 / 12

        # apply sugar waste also to methane scp, for lack of better baseline
        self.SCP_WASTE = inputs_to_optimizer["WASTE"]["SUGAR"]

    def calculate_monthly_scp_production(self, inputs_to_optimizer):
        if inputs_to_optimizer["ADD_METHANE_SCP"]:

            industrial_delay_months = [0] * inputs_to_optimizer["DELAY"][
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
            for x in METHANE_SCP_PERCENT_KCALS:
                production_kcals_scp_per_month_long.append(
                    x
                    / 100
                    * self.GLOBAL_MONTHLY_NEEDS
                    * inputs_to_optimizer["SCP_GLOBAL_PRODUCTION_FRACTION"]
                    * (1 - self.SCP_WASTE / 100)
                )
        else:
            production_kcals_scp_per_month_long = [0] * self.NMONTHS

        self.production_kcals_scp_per_month = production_kcals_scp_per_month_long[
            0 : self.NMONTHS
        ]

    def get_scp_production(self):

        # billions of kcals converted to 1000s of tons protein
        production_protein_scp_per_month = list(
            np.array(self.production_kcals_scp_per_month)
            * 1e9
            * self.SCP_FRAC_PROTEIN
            / self.SCP_KCALS_PER_KG
            / 1e6
        )

        # billions of kcals converted to 1000s of tons fat
        production_fat_scp_per_month = list(
            np.array(self.production_kcals_scp_per_month)
            * 1e9
            * self.SCP_FRAC_FAT
            / self.SCP_KCALS_PER_KG
            / 1e6
        )

        return (
            self.production_kcals_scp_per_month,
            production_fat_scp_per_month,
            production_protein_scp_per_month,
        )
