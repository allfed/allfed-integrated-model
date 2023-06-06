"""
################################# Seafood #####################################
##                                                                            #
##       Functions and constants relating to seafood, excluding seaweed       #
##                                                                            #
###############################################################################
"""
import numpy as np
from src.food_system.food import Food


class Seafood:
    def __init__(self, constants_for_params):
        """
        Initializes the Seafood object with the given constants for parameters.

        Args:
            constants_for_params (dict): A dictionary containing the constants for parameters.

        Returns:
            None
        """

        # number of months to run the model for
        self.NMONTHS = constants_for_params["NMONTHS"]
        # additional fish to add
        self.ADD_FISH = constants_for_params["ADD_FISH"]

        # percentage of fish waste
        FISH_WASTE = constants_for_params["WASTE"]["SEAFOOD"]

        # fish kcals per month, billions
        self.FISH_KCALS = (
            constants_for_params["FISH_DRY_CALORIC_ANNUAL"]
            * (1 - FISH_WASTE / 100)
            * 4e6
            / 1e9
            / 12
        )
        # units of 1000s tons protein monthly
        # (so, global value is in the hundreds of thousands of tons)
        self.FISH_PROTEIN = (
            constants_for_params["FISH_PROTEIN_TONS_ANNUAL"]
            / 1e3
            / 12
            * (1 - FISH_WASTE / 100)
        )

        # units of 1000s tons fat
        # (so, global value is in the tens of thousands of tons)
        self.FISH_FAT = (
            constants_for_params["FISH_FAT_TONS_ANNUAL"]
            / 1e3
            / 12
            * (1 - FISH_WASTE / 100)
        )

    # includes all seafood (except seaweed), not just fish
    def set_seafood_production(self, constants_for_params):
        """
        Sets the seafood production for the Seafood class based on the given constants for parameters.

        Args:
            constants_for_params (dict): A dictionary containing the constants for parameters.

        Returns:
            None

        """
        # Based on Xia et al. (2021): Global Famine after Nuclear War

        # Get the percentage of fish each month from the given constants.
        FISH_PERCENT_EACH_MONTH_LONG = constants_for_params["FISH_PERCENT_MONTHLY"]
        FISH_PERCENT_EACH_MONTH = FISH_PERCENT_EACH_MONTH_LONG[0 : self.NMONTHS]

        # Calculate the production of fish per month based on the percentage of fish each month.
        if self.ADD_FISH:
            production_kcals_fish_per_month = []
            production_protein_fish_per_month = []
            production_fat_fish_per_month = []
            for x in FISH_PERCENT_EACH_MONTH:
                production_kcals_fish_per_month.append(x / 100 * self.FISH_KCALS)
                production_protein_fish_per_month.append(x / 100 * self.FISH_PROTEIN)
                production_fat_fish_per_month.append(x / 100 * self.FISH_FAT)
        else:
            production_kcals_fish_per_month = [0] * len(FISH_PERCENT_EACH_MONTH)
            production_protein_fish_per_month = [0] * len(FISH_PERCENT_EACH_MONTH)
            production_fat_fish_per_month = [0] * len(FISH_PERCENT_EACH_MONTH)

        # Set the seafood production to the calculated fish production.
        self.to_humans = Food(
            kcals=np.array(production_kcals_fish_per_month),
            fat=np.array(production_fat_fish_per_month),
            protein=np.array(production_protein_fish_per_month),
            kcals_units="billion kcals each month",
            fat_units="thousand tons each month",
            protein_units="thousand tons each month",
        )
