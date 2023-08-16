"""
# ############################### Seaweed #####################################
#                                                                            #
#             Functions and constants relating to edible seaweed             #
#                                                                            #
# ##############################################################################
"""

import numpy as np
from src.food_system.food import Food


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

        self.MAX_SEAWEED_AS_PERCENT_KCALS_HUMANS = constants_for_params[
            "MAX_SEAWEED_AS_PERCENT_KCALS_HUMANS"
        ]

        self.MAX_SEAWEED_HUMANS_CAN_CONSUME_MONTHLY = (
            self.MAX_SEAWEED_AS_PERCENT_KCALS_HUMANS
            / 100
            * (constants_for_params["POP"] * Food.conversions.kcals_monthly / 1e9)
        )

        self.MAX_SEAWEED_AS_PERCENT_KCALS_FEED = constants_for_params[
            "MAX_SEAWEED_AS_PERCENT_KCALS_FEED"
        ]

        # 1000s of tons wet global (trading blocs multiply this by some fraction)
        INITIAL_SEAWEED_GLOBAL = 1

        # 1000s of km^2 global  (trading blocs multiply this by some fraction)
        INITIAL_BUILT_SEAWEED_AREA_GLOBAL = 0.1

        # Gracilaria Tikvahiae wet to dry mass conversion
        # https://www.degruyter.com/document/doi/10.1515/botm.1987.30.6.525/html
        self.WET_TO_DRY_MASS_CONVERSION = 0.11

        # kcals per kg dry
        # http://pubs.sciepub.com/jfnr/8/8/7/index.html
        self.KCALS_PER_KG = 2620

        # dry fraction mass fat
        self.MASS_FRACTION_FAT_DRY = 0.0205
        # dry fraction mass protein times average protein digestibility of seaweed
        self.MASS_FRACTION_PROTEIN_DRY = 0.077 * 0.79

        # Percent loss of seaweed
        # https://krishi.icar.gov.in/jspui/handle/123456789/51103
        self.HARVEST_LOSS = 20  # percent (seaweed)

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

    def get_growth_rates(self, constants_for_params):
        # Convert keys to integers and sort them
        sorted_columns = sorted(
            [int(key) for key in constants_for_params["SEAWEED_GROWTH_PER_DAY"].keys()]
        )

        # Create a list of values in the proper order
        sorted_daily_percents = np.array(
            [
                constants_for_params["SEAWEED_GROWTH_PER_DAY"][str(key)]
                for key in sorted_columns
            ]
        )

        # percentage gain per month
        sorted_monthly_percents = 100 * (((sorted_daily_percents / 100) + 1) ** 30)
        self.growth_rates_monthly = sorted_monthly_percents

        return sorted_monthly_percents

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
        self.built_area = built_area

        return built_area
