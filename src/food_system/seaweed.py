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
        self.MINIMUM_DENSITY = 400  # tons/km^2 (seaweed)
        self.MAXIMUM_DENSITY = 800  # tons/km^2 (seaweed)
        self.MAXIMUM_SEAWEED_AREA = 1000  # 1000 km^2 (seaweed)

        # use "laver" variety for now from nutrition calculator
        # @Morgan: Link broken
        self.WET_TO_DRY_MASS_CONVERSION = 1 / 6

        # in order, in equal parts by mass:
        # Laver dry

        # kcals per kg dry
        self.KCALS_PER_KG = 2100

        # dry fraction mass fat
        self.MASS_FRACTION_FAT_DRY = 0.017

        # dry fraction mass digestible protein
        self.MASS_FRACTION_PROTEIN_DRY = 0.862 * 0.349

        self.HARVEST_LOSS = 15  # percent (seaweed)

        # 1000 tons (seaweed)
        self.INITIAL_SEAWEED = constants_for_params["INITIAL_SEAWEED"]
        # @li multiply by fraction
        # 1000 tons (seaweed)
        self.INITIAL_BUILT_SEAWEED_AREA = constants_for_params[
            "INITIAL_BUILT_SEAWEED_AREA"
        ]
        # @li multiply by fraction

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
            constants_for_params["SEAWEED_NEW_AREA_PER_MONTH"]
            * constants_for_params["SEAWEED_NEW_AREA_FRACTION"]
        )

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
        built_area = built_area_long[0 : self.NMONTHS]

        return built_area
