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
        self.MAX_SEAWEED_AS_PERCENT_KCALS_BIOFUEL = constants_for_params[
            "MAX_SEAWEED_AS_PERCENT_KCALS_BIOFUEL"
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
        """
        Calculates the monthly growth rates of seaweed based on the daily growth percentages provided in the constants.

        Args:
            constants_for_params (dict): A dictionary containing the constants for the seaweed growth model.

        Returns:
            numpy.ndarray: An array of monthly growth rates for the seaweed.

        """
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

        # Calculate the monthly growth rates based on the daily growth percentages
        sorted_monthly_percents = 100 * (((sorted_daily_percents / 100) + 1) ** 30)

        # Store the monthly growth rates in the object's growth_rates_monthly attribute
        self.growth_rates_monthly = sorted_monthly_percents

        # Return the monthly growth rates
        return sorted_monthly_percents

    def get_built_area(self, constants_for_params):
        """
        Calculates the built area of seaweed based on the provided constants.

        Args:
            constants_for_params (dict): A dictionary containing the constants for the seaweed growth model.

        Returns:
            numpy.ndarray: An array of the built area of seaweed over time.

        """
        # Calculate the new area of seaweed per month based on the global value and the fraction provided in the constants
        SEAWEED_NEW_AREA_PER_MONTH = (
            self.SEAWEED_NEW_AREA_PER_MONTH_GLOBAL
            * constants_for_params["SEAWEED_NEW_AREA_FRACTION"]
        )

        # Set a flag to print the difference in seaweed area if desired
        PRINT_DIFFERENCE_IN_SEAWEED_AREA = False

        # Print the difference in seaweed area if desired
        if PRINT_DIFFERENCE_IN_SEAWEED_AREA:
            print("MAX SEAWEED AREA Was: ")
            print(self.MAXIMUM_SEAWEED_AREA / (200 / 30.4))
            print("now is")
            print(SEAWEED_NEW_AREA_PER_MONTH)

        # If seaweed is being added, create a list of built seaweed areas for the delay period
        if constants_for_params["ADD_SEAWEED"]:
            sd = [self.INITIAL_BUILT_SEAWEED_AREA] * constants_for_params["DELAY"][
                "SEAWEED_MONTHS"
            ]
        else:
            # Create an arbitrarily long list of months all at the constant initial area
            sd = [self.INITIAL_BUILT_SEAWEED_AREA] * 1000

        # Create a long list of the built seaweed area over time, starting with the delay period and then increasing linearly
        built_area_long = np.append(
            np.array(sd),
            np.linspace(
                self.INITIAL_BUILT_SEAWEED_AREA,
                (self.NMONTHS - 1) * SEAWEED_NEW_AREA_PER_MONTH
                + self.INITIAL_BUILT_SEAWEED_AREA,
                self.NMONTHS,
            ),
        )

        # Cap the built seaweed area at the maximum allowed area
        built_area_long[
            built_area_long > self.MAXIMUM_SEAWEED_AREA
        ] = self.MAXIMUM_SEAWEED_AREA

        # Reduce the list to the length of the simulation
        built_area = built_area_long[: self.NMONTHS]

        # Store the built seaweed area in the object's built_area attribute
        self.built_area = built_area

        # Return the built seaweed area
        return built_area

    def estimate_seaweed_growth_for_estimating_feed_availability(self):
        """
        Estimates the growth of seaweed for the purpose of estimating feed availability.

        We have to see whether predicted feed needs are more than available feed, in which case the feed needs to be reduced.
        We have to do that before we run the optimization which more accurately determines seaweed growth.
        So, this function makes the simplifying assumptions which no longer require linear optimization:
        1. seaweed is not harvested until production would reach the human consumption percentage calories limit
        2. once it reaches this limit, it stays at that rate of production for the rest of the simulation

        Returns:
            None

        """
        # If there is no growth, set the estimated seaweed to an empty Food object and return
        if (np.array(self.growth_rates_monthly) == 0).all():
            self.estimated_seaweed = Food()
            return

        # Initialize variables for estimating seaweed consumption
        estimated_seaweed_consumed_after_waste_wet = np.zeros(self.NMONTHS)
        seaweed_wet_on_farm = self.INITIAL_SEAWEED

        # Set the smallest harvest for minimum sufficient consumption
        smallest_harvest_for_min_sufficient_consumption = max_seaweed_harvested / (
            1 - 1 / (1 + growth_rate / 100.0)
        )

        used_area = self.INITIAL_BUILT_SEAWEED_AREA

        # Loop through each month of the simulation
        for month in range(0, self.NMONTHS):
            # Calculate the maximum seaweed that could be consumed by humans in a given month
            max_seaweed_eaten = self.MAX_SEAWEED_HUMANS_CAN_CONSUME_MONTHLY
            max_seaweed_harvested = max_seaweed_eaten / (self.HARVEST_LOSS / 100)

            # Calculate the growth rate and the amount of seaweed wet on the farm
            growth_rate = self.growth_rates_monthly[month]
            seaweed_wet_on_farm_without_considering_max_seaweed = (
                seaweed_wet_on_farm * (1 + growth_rate / 100.0)
            )
            seaweed_wet_on_farm = min(
                seaweed_wet_on_farm_without_considering_max_seaweed,
                self.built_area[month] * self.MAXIMUM_DENSITY,
            )

            # Estimate the used area as the initial built seaweed area or the minimum density times the used area
            used_area_without_considering_whats_built = max(
                seaweed_wet_on_farm / self.MAXIMUM_DENSITY,
                self.INITIAL_BUILT_SEAWEED_AREA,
            )
            used_area = min(
                used_area_without_considering_whats_built, self.built_area[month]
            )

            # Calculate the amount of seaweed that can be harvested
            amount_can_harvest = seaweed_wet_on_farm - self.MINIMUM_DENSITY * used_area

            if amount_can_harvest >= smallest_harvest_for_min_sufficient_consumption:
                # If we can actually harvest all the seaweed to meet minimum needs, start doing it
                seaweed_wet_on_farm = seaweed_wet_on_farm - max_seaweed_harvested
                estimated_seaweed_consumed_after_waste_wet[
                    month
                ] = self.MAX_SEAWEED_HUMANS_CAN_CONSUME_MONTHLY
            else:
                estimated_seaweed_consumed_after_waste_wet[month] = 0

        # Set the estimated seaweed consumed after waste
        self.estimated_seaweed_consumed_after_waste = Food(
            kcals=estimated_seaweed_consumed_after_waste_wet * self.SEAWEED_KCALS,
            fat=estimated_seaweed_consumed_after_waste_wet * self.SEAWEED_FAT,
            protein=estimated_seaweed_consumed_after_waste_wet * self.SEAWEED_PROTEIN,
            kcals_units="billion kcals each month",
            fat_units="thousand tons each month",
            protein_units="thousand tons each month",
        )

        # Plot the estimated seaweed
        convenient_units = (
            self.estimated_seaweed_consumed_after_waste.in_units_percent_fed()
        )
        convenient_units.plot("Seaweed estimate")
