################################# Seaweed #####################################
##                                                                            #
##             Functions and constants relating to edible seaweed             #
##                                                                            #
###############################################################################

import numpy as np

class Seaweed:

    def __init__(self,inputs_to_optimizer):
        self.NMONTHS = inputs_to_optimizer['NMONTHS']
        self.MINIMUM_DENSITY = 400  # tons/km^2 (seaweed)
        self.MAXIMUM_DENSITY = 800  # tons/km^2 (seaweed)
        self.MAXIMUM_AREA = 1000  # 1000 km^2 (seaweed)

        # use "laver" variety for now from nutrition calculator
        # https://docs.google.com/spreadsheets/d / 1RZqSrHNiIEuPQLtx1ebCd_kUcFvEF6Ea46xyzA5wU0s/edit#gid=1516287804
        self.WET_TO_DRY_MASS_CONVERSION = 1 / 6

        # in order, in equal parts by mass:
        # Laver dry

        # kcals per kg dry
        self.KCALS_PER_KG = 2100

        # dry fraction mass fat
        self.MASS_FRACTION_FAT_DRY = .017

        # dry fraction mass digestible protein
        self.MASS_FRACTION_PROTEIN_DRY = 0.862 * 0.349

        self.HARVEST_LOSS = 15  # percent (seaweed)

        # 1000 tons (seaweed)
        self.INITIAL_SEAWEED = inputs_to_optimizer['INITIAL_SEAWEED']

        # 1000 tons (seaweed)
        self.INITIAL_AREA = inputs_to_optimizer['INITIAL_AREA']
        

        self.SEAWEED_WASTE = inputs_to_optimizer['WASTE']['SEAWEED']

        # seaweed billion kcals per 1000 tons wet
        # convert 1000 tons to kg
        # convert kg to kcals
        # convert kcals to billions of kcals
        # convert wet mass seaweed to dry mass seaweed
        self.SEAWEED_KCALS = 1e6 * self.KCALS_PER_KG / 1e9 \
            * self.WET_TO_DRY_MASS_CONVERSION \
            * (1 - self.SEAWEED_WASTE / 100)

        # seaweed fraction digestible protein per 1000 ton wet
        self.SEAWEED_PROTEIN = self.MASS_FRACTION_PROTEIN_DRY \
            * self.WET_TO_DRY_MASS_CONVERSION \
            * (1 - self.SEAWEED_WASTE / 100)

        # seaweed fraction fat per 1000 tons wet
        self.SEAWEED_FAT = self.MASS_FRACTION_FAT_DRY \
            * self.WET_TO_DRY_MASS_CONVERSION \
            * (1 - self.SEAWEED_WASTE / 100)

    def get_built_area(self, inputs_to_optimizer):


        SEAWEED_NEW_AREA_PER_DAY = inputs_to_optimizer['SEAWEED_NEW_AREA_PER_DAY']
        SEAWEED_PRODUCTION_RATE = inputs_to_optimizer['SEAWEED_PRODUCTION_RATE']

        if(inputs_to_optimizer["ADD_SEAWEED"]):
            sd = [self.INITIAL_AREA] * inputs_to_optimizer["DELAY"]["SEAWEED_MONTHS"] * self.DAYS_IN_MONTH
        else:
            sd = [self.INITIAL_AREA] * 100000

        built_area_long = np.append(
            np.array(sd),
            np.linspace(
                self.INITIAL_AREA,
                (self.NMONTHS*30 - 1) * SEAWEED_NEW_AREA_PER_DAY + self.INITIAL_AREA,
                self.NMONTHS*30
            )
        )
        built_area_long[built_area_long > self.MAXIMUM_AREA] = self.MAXIMUM_AREA
        built_area = built_area_long[0:self.NMONTHS*30]

        return built_area