"""
# ############################### Seaweed #####################################
#                                                                            #
#             Functions and constants relating to edible seaweed             #
#                                                                            #
# ##############################################################################
"""

import numpy as np


class Seaweed:
    def __init__(self, constants_for_params):
        self.NMONTHS = constants_for_params["NMONTHS"]
        # Cutting back based on this paper
        # https://www.sciencedirect.com/science/article/abs/pii/0044848678900303
        self.MINIMUM_DENSITY = 1200  # tons/km^2 (seaweed)
        self.MAXIMUM_DENSITY = 3600  # tons/km^2 (seaweed)

        # units: 1000 km^2 global (trading blocs multiply this by some fraction)
        self.SEAWEED_NEW_AREA_PER_MONTH_GLOBAL = 2.0765 * 30

        # 1000 km^2 (seaweed) times the fraction
        MAXIMUM_SEAWEED_AREA_GLOBAL = 1000
        self.MAXIMUM_SEAWEED_AREA = (
            MAXIMUM_SEAWEED_AREA_GLOBAL
            * constants_for_params["SEAWEED_MAX_AREA_FRACTION"]
        )

        # 1000s of tons wet global (trading blocs multiply this by some fraction)
        INITIAL_SEAWEED_GLOBAL = 1

        # 1000s of km^2 global  (trading blocs multiply this by some fraction)
        INITIAL_BUILT_SEAWEED_AREA_GLOBAL = 0.1

        # Montgomery, W. L., & Gerking, S. D. (1980). Marine macroalgae as foods for
        # fishes: an evaluation of potential food quality. Environmental Biology of
        # Fishes, 5(2), 143–153. doi:10.1007/bf02391621

        # Use the mean red algae protein fraction (Gracilaria Tikvahiae is a red agae)
        self.WET_TO_DRY_MASS_CONVERSION = 1 / 6

        # in order, in equal parts by mass:
        # Laver dry

        # kcals per kg dry
        self.KCALS_PER_KG = 2490

        # dry fraction mass fat
        self.MASS_FRACTION_FAT_DRY = 0.0205
        # dry fraction mass protein times average protein digestibility of seaweed
        self.MASS_FRACTION_PROTEIN_DRY = 0.077 * 0.79

        self.HARVEST_LOSS = 15  # percent (seaweed)

        # 1000 tons (seaweed)

        # landlocked country
        if constants_for_params["SEAWEED_MAX_AREA_FRACTION"] == 0:
            self.INITIAL_SEAWEED = 0
        else:
            self.INITIAL_SEAWEED = (
                INITIAL_SEAWEED_GLOBAL
                * constants_for_params["INITIAL_SEAWEED_FRACTION"]
            )
        self.INITIAL_BUILT_SEAWEED_AREA = (
            INITIAL_BUILT_SEAWEED_AREA_GLOBAL
            * constants_for_params["SEAWEED_NEW_AREA_FRACTION"]
        )

        self.SEAWEED_WASTE = constants_for_params["WASTE"]["SEAWEED"]

        # seaweed billion kcals per 1000 tons wet
        # convert 1000 tons to kg
        # convert kg to kcals
        # convert kcals to billions of kcals
        # convert wet mass seaweed to dry mass seaweed
        self.SEAWEED_KCALS = (
            1e6
            * self.KCALS_PER_KG
            / 1e9
            * self.WET_TO_DRY_MASS_CONVERSION
            * (1 - self.SEAWEED_WASTE / 100)
        )
        # seaweed fraction digestible protein per 1000 ton wet
        self.SEAWEED_PROTEIN = (
            self.MASS_FRACTION_PROTEIN_DRY
            * self.WET_TO_DRY_MASS_CONVERSION
            * (1 - self.SEAWEED_WASTE / 100)
        )

        # seaweed fraction fat per 1000 tons wet
        self.SEAWEED_FAT = (
            self.MASS_FRACTION_FAT_DRY
            * self.WET_TO_DRY_MASS_CONVERSION
            * (1 - self.SEAWEED_WASTE / 100)
        )

    def get_built_area(self, constants_for_params):

        SEAWEED_NEW_AREA_PER_MONTH = (
            self.SEAWEED_NEW_AREA_PER_MONTH_GLOBAL
            * constants_for_params["SEAWEED_NEW_AREA_FRACTION"]
        )
        PRINT_DIFFERENCE_IN_SEAWEED_AREA = False
        if PRINT_DIFFERENCE_IN_SEAWEED_AREA:
            print("MAX SEAWEED AREA Was: ")
            print(self.MAXIMUM_SEAWEED_AREA / (200 / 30.4))
            print("now is")
            print(SEAWEED_NEW_AREA_PER_MONTH)

        if constants_for_params["ADD_SEAWEED"]:
            sd = [self.INITIAL_BUILT_SEAWEED_AREA] * constants_for_params["DELAY"][
                "SEAWEED_MONTHS"
            ]
        else:
            # arbitrarily long list of months all at constant area
            sd = [self.INITIAL_BUILT_SEAWEED_AREA] * 1000

        built_area_long = np.append(
            np.array(sd),
            np.linspace(
                self.INITIAL_BUILT_SEAWEED_AREA,
                (self.NMONTHS - 1) * SEAWEED_NEW_AREA_PER_MONTH
                + self.INITIAL_BUILT_SEAWEED_AREA,
                self.NMONTHS,
            ),
        )
        built_area_long[
            built_area_long > self.MAXIMUM_SEAWEED_AREA
        ] = self.MAXIMUM_SEAWEED_AREA

        # reduce list to length of months of simulation
        built_area = built_area_long[: self.NMONTHS]
        # print("built_area")
        # print(built_area)
        return built_area
