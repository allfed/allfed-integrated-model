"""
######################## Methane Single Cell Protein ###########################
##                                                                             #
##            Functions and constants relating to methane SCP                  #
##                                                                             #
################################################################################
"""

import numpy as np
from numpy.typing import ArrayLike

from src.food_system.food import Food


class MethaneSCP:
    def __init__(self, constants_for_params):
        """
        Initializes the MethaneSCP object with the given constants.

        Args:
            constants_for_params (dict): A dictionary containing the constants needed
            for the MethaneSCP object.

        Attributes:
            INDUSTRIAL_FOODS_SLOPE_MULTIPLIER (float): The slope multiplier for industrial
            foods.
            NMONTHS (int): The number of months in the simulation.
            SCP_KCALS_PER_KG (int): The number of kcals per kg of SCP.
            SCP_FRAC_PROTEIN (float): The fraction of SCP that is protein.
            SCP_FRAC_FAT (float): The fraction of SCP that is fat.
            SCP_KCALS_TO_FAT_CONVERSION (float): The conversion factor from SCP kcals to fat.
            SCP_KCALS_TO_PROTEIN_CONVERSION (float): The conversion factor from SCP kcals to protein.
            MAX_FRACTION_HUMAN_FOOD_CONSUMED_AS_SCP (float): The maximum fraction of human food
            that can be consumed as SCP in any month.
            MAX_METHANE_SCP_AS_PERCENT_KCALS_FEED (int): The maximum percentage of kcals in feed
            that can come from methane SCP.
            MAX_METHANE_SCP_AS_PERCENT_KCALS_BIOFUEL (int): The maximum percentage of kcals in
            biofuel that can come from methane SCP.
            COUNTRY_MONTHLY_NEEDS (float): The monthly needs of the country in terms of billion kcals.
            GLOBAL_MONTHLY_NEEDS (float): The monthly needs of the global population in terms of
            billion kcals.
            MAX_METHANE_SCP_HUMANS_CAN_CONSUME_MONTHLY (float): The maximum amount of methane SCP
            that humans can consume monthly in terms of billion kcals.
            SCP_WASTE (float): The amount of waste in SCP due to sugar.

        """
        # set the INDUSTRIAL_FOODS_SLOPE_MULTIPLIER attribute
        self.INDUSTRIAL_FOODS_SLOPE_MULTIPLIER = constants_for_params[
            "INDUSTRIAL_FOODS_SLOPE_MULTIPLIER"
        ]

        # set the NMONTHS attribute
        self.NMONTHS = constants_for_params["NMONTHS"]

        # set the SCP_KCALS_PER_KG, SCP_FRAC_PROTEIN, and SCP_FRAC_FAT attributes
        self.SCP_KCALS_PER_KG = 5350.0  # kcals per kg of scp
        self.SCP_FRAC_PROTEIN = (
            0.650  # fraction protein by mass (1kg is 650 grams protein)
        )
        self.SCP_FRAC_FAT = 0.09  # fraction fat by mass (1kg is 90 grams fat)

        # to arrive at units thousand tons each month of SCP from billion kcals of fat,
        # we multiply the starting number of billion kcals of food by [units]:
        # [billion kcals] * [1e9 kcals / 1 billion kcals] => [kcals of food]
        # [kcals of food] / [kcals / kg] => [kg of food]
        # [kg of food] * [kg fat / kg food] => [kg of fat]
        # [kg of fat] * [1 thousand tons of fat / 1e6 kg fat] => [thousand tons of fat]
        # therefore [billion kcals] * (1e9 / [kcals / kg] * [fraction fat by mass] / 1e6) => [thousand tons of fat]

        self.SCP_KCALS_TO_FAT_CONVERSION = (
            1e9 / self.SCP_KCALS_PER_KG * self.SCP_FRAC_FAT / 1e6
        )
        self.SCP_KCALS_TO_PROTEIN_CONVERSION = (
            1e9 / self.SCP_KCALS_PER_KG * self.SCP_FRAC_PROTEIN / 1e6
        )

        # billion kcals a month for country in question
        self.COUNTRY_MONTHLY_NEEDS = (
            constants_for_params["POP"] * Food.conversions.kcals_monthly / 1e9
        )

        # billion kcals a month for 100% population (7.8 billion people).
        self.GLOBAL_MONTHLY_NEEDS = (
            constants_for_params["GLOBAL_POP"] * Food.conversions.kcals_monthly / 1e9
        )

        # apply sugar waste also to methane scp, for lack of better baseline
        self.SCP_WASTE_DISTRIBUTION = constants_for_params["WASTE_DISTRIBUTION"][
            "SUGAR"
        ]
        self.SCP_WASTE_RETAIL = constants_for_params["WASTE_RETAIL"]

    def calculate_monthly_scp_caloric_production(self, constants_for_params):
        if constants_for_params["ADD_METHANE_SCP"]:
            industrial_delay_months = [0] * constants_for_params["DELAY"][
                "INDUSTRIAL_FOODS_MONTHS"
            ]

            global_values_percent_fed_just_scp = (
                industrial_delay_months
                + [0] * 12
                + [2] * 5
                + [4]
                + [7] * 5
                + [9]
                + [11] * 6
                + [13]
                + [15] * 1000
            )
            METHANE_SCP_PERCENT_KCALS = list(
                np.array(industrial_delay_months + global_values_percent_fed_just_scp)
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
                    * (1 - self.SCP_WASTE_DISTRIBUTION / 100)
                )

            self.production_kcals_scp_per_month = production_kcals_scp_per_month_long[
                0 : self.NMONTHS
            ]
        else:
            self.production_kcals_scp_per_month = [0] * self.NMONTHS

    def create_scp_food_from_kcals(self, kcals: ArrayLike) -> Food:
        """
        Args:
            kcals (np.ArrayLike): array/list of billions of kcals for each month

        Returns:
            Food object.
        """
        kcals = np.squeeze(np.array(kcals))
        assert isinstance(kcals, np.ndarray)
        assert kcals.ndim == 1

        # billions of kcals converted to 1000s of tons fat
        production_fat = kcals * self.SCP_KCALS_TO_FAT_CONVERSION
        # billions of kcals converted to 1000s of tons protein
        production_protein = kcals * self.SCP_KCALS_TO_PROTEIN_CONVERSION

        return Food(
            kcals=kcals,
            fat=production_fat,
            protein=production_protein,
            kcals_units="billion kcals each month",
            fat_units="thousand tons each month",
            protein_units="thousand tons each month",
        )

    def calculate_scp_fat_and_protein_production(self):
        kcals = self.production_kcals_scp_per_month

        self.production = self.create_scp_food_from_kcals(kcals)
