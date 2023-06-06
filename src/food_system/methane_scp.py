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
        self.SCP_KCALS_PER_KG = 5350
        self.SCP_FRAC_PROTEIN = 0.650
        self.SCP_FRAC_FAT = 0.09

        # calculate the SCP_KCALS_TO_FAT_CONVERSION and SCP_KCALS_TO_PROTEIN_CONVERSION attributes
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
        """
        Calculates the monthly caloric production of SCP.

        Args:
            constants_for_params (dict): A dictionary containing the constants needed
            for the calculation.

        Attributes:
            production_kcals_scp_per_month_long (list): A list containing the monthly caloric
            production of SCP.

        """
        # check if methane SCP should be added
        if constants_for_params["ADD_METHANE_SCP"]:
            # create a list of industrial delay months
            industrial_delay_months = [0] * constants_for_params["DELAY"][
                "INDUSTRIAL_FOODS_MONTHS"
            ]

            # create a list of methane SCP percentage of kcals
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

            # create a list of monthly caloric production of SCP
            production_kcals_scp_per_month_long = []
            for global_percent_kcals_scp in METHANE_SCP_PERCENT_KCALS:
                production_kcals_scp_per_month_long.append(
                    global_percent_kcals_scp
                    / 100
                    * self.GLOBAL_MONTHLY_NEEDS
                    * constants_for_params["SCP_GLOBAL_PRODUCTION_FRACTION"]
                    * (1 - self.SCP_WASTE / 100)
                )
            # set the production_kcals_scp_per_month_long attribute
            self.production_kcals_scp_per_month_long = (
                production_kcals_scp_per_month_long
            )
        else:
            # if methane SCP should not be added, set the production_kcals_scp_per_month_long
            # attribute to a list of zeros
            self.production_kcals_scp_per_month_long = [0] * self.NMONTHS

    def calculate_scp_fat_and_protein_production(self):
        """
        Calculates the fat and protein production of SCP.

        Attributes:
            production (Food): A Food object containing the production of SCP.
        """
        # create a Food object for production
        self.production = Food()

        # set the kcals attribute of the production Food object
        self.production.kcals = np.array(
            self.production_kcals_scp_per_month_long[0 : self.NMONTHS]
        )

        # calculate the protein attribute of the production Food object
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

        # calculate the fat attribute of the production Food object
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

        # set the units of the production Food object
        self.production.set_units(
            kcals_units="billion kcals each month",
            fat_units="thousand tons each month",
            protein_units="thousand tons each month",
        )

        # self.postwaste = self * (1 - self.SCP_WASTE / 100)
