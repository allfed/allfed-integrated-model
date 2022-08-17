"""
################################# Seafood #####################################
##                                                                            #
##       Functions and constants relating to seafood, excluding seaweed       #
##                                                                            #
###############################################################################
"""
import numpy as np


class Seafood:
    def __init__(self, constants_for_params):
        self.NMONTHS = constants_for_params["NMONTHS"]
        self.ADD_FISH = constants_for_params["ADD_FISH"]

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
    def get_seafood_production(self, constants_for_params):

        # Based on Xia et al. (2021): Global Famine after Nuclear War

        FISH_PERCENT_EACH_MONTH_LONG = constants_for_params["FISH_PERCENT_MONTHLY"]

        FISH_PERCENT_EACH_MONTH = FISH_PERCENT_EACH_MONTH_LONG[0:self.NMONTHS]

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

        return (
            np.array(production_kcals_fish_per_month),
            np.array(production_fat_fish_per_month),
            np.array(production_protein_fish_per_month),
        )
