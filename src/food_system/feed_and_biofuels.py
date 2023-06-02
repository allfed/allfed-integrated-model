"""
This class is used for calculating feed and biofuel usage. They are combined into
a monthly total "excess usage" for the purposes of the optimizer, and are treated
similarly in the model.

NOTE: Anything that could have waste applied, and is not being wasted, has the pre-waste
      marker

Created on Wed Jul 17

@author: morgan
"""

import numpy as np

from src.food_system.food import Food


class FeedAndBiofuels:
    def __init__(self, constants_for_params):
        """
        Initializes the FeedAndBiofuels class with the given constants for parameters.

        Args:
            constants_for_params (dict): A dictionary containing the constants for parameters.

        Returns:
            None

        Example:
            >>> constants = {
            ...     "NMONTHS": 12,
            ...     "BIOFUEL_KCALS": 1000,
            ...     "BIOFUEL_FAT": 200,
            ...     "BIOFUEL_PROTEIN": 100,
            ... }
            >>> feed_and_biofuels = FeedAndBiofuels(constants)
        """
        # Set the number of months
        self.NMONTHS = constants_for_params["NMONTHS"]

        # Create a Food object for biofuel per year pre-waste
        self.biofuel_per_year_prewaste = Food(
            kcals=constants_for_params["BIOFUEL_KCALS"],
            fat=constants_for_params["BIOFUEL_FAT"],
            protein=constants_for_params["BIOFUEL_PROTEIN"],
            kcals_units="thousand dry caloric tons per year",
            fat_units="tons per year",
            protein_units="tons per year",
        )

        # Set the amount to reduce ratio each iteration and the safety margin
        self.AMOUNT_TO_REDUCE_RATIO_EACH_ITERATION = 0.01  # 1% reduction
        self.SAFETY_MARGIN = 0.01

    def set_feed_and_biofuels(
        self,
        outdoor_crops_used_for_biofuel,
        methane_scp_used_for_biofuel,
        cellulosic_sugar_used_for_biofuel,
        remaining_biofuel_needed_from_stored_food,
        outdoor_crops_used_for_feed,
        methane_scp_used_for_feed,
        cellulosic_sugar_used_for_feed,
        remaining_feed_needed_from_stored_food,
    ):
        """
        This function sets the feed and biofuel usage for each month. It takes the
        outdoor crops, methane, and cellulosic sugar that are used for feed and
        biofuels, and the remaining feed and biofuel needed from stored food.

        Args:
            outdoor_crops_used_for_biofuel (list): A list of outdoor crops used for biofuel
            methane_scp_used_for_biofuel (list): A list of methane SCP used for biofuel
            cellulosic_sugar_used_for_biofuel (list): A list of cellulosic sugar used for biofuel
            remaining_biofuel_needed_from_stored_food (Food): The remaining biofuel needed from stored food
            outdoor_crops_used_for_feed (list): A list of outdoor crops used for feed
            methane_scp_used_for_feed (list): A list of methane SCP used for feed
            cellulosic_sugar_used_for_feed (list): A list of cellulosic sugar used for feed
            remaining_feed_needed_from_stored_food (Food): The remaining feed needed from stored food

        Returns:
            None

        Example:
            >>> feed_and_biofuels = FeedAndBiofuels()
            >>> feed_and_biofuels.set_feed_and_biofuels(
            ...     [10, 20, 30],
            ...     [40, 50, 60],
            ...     [70, 80, 90],
            ...     Food(100),
            ...     [10, 20, 30],
            ...     [40, 50, 60],
            ...     [70, 80, 90],
            ...     Food(100),
            ... )
        """

        # Set the biofuel and feed usage for each source
        self.cell_sugar_biofuels = Food(
            cellulosic_sugar_used_for_biofuel
        ).in_units_percent_fed()
        self.cell_sugar_feed = Food(
            cellulosic_sugar_used_for_feed
        ).in_units_percent_fed()
        self.scp_biofuels = Food(methane_scp_used_for_biofuel).in_units_percent_fed()
        self.scp_feed = Food(methane_scp_used_for_feed).in_units_percent_fed()

        # TODO: add seaweed as a feed source
        self.seaweed_biofuels = Food(
            np.zeros(len(outdoor_crops_used_for_biofuel))
        ).in_units_percent_fed()
        # TODO: add seaweed as a feed source
        self.seaweed_feed = Food(
            np.zeros(len(outdoor_crops_used_for_biofuel))
        ).in_units_percent_fed()

        self.outdoor_crops_biofuels = Food(
            outdoor_crops_used_for_biofuel
        ).in_units_percent_fed()
        self.outdoor_crops_feed = Food(
            outdoor_crops_used_for_feed
        ).in_units_percent_fed()
        self.stored_food_biofuels = (
            remaining_biofuel_needed_from_stored_food.in_units_percent_fed()
        )

        self.stored_food_feed = (
            remaining_feed_needed_from_stored_food.in_units_percent_fed()
        )

        # Convert the feed and biofuel usage to kcal equivalents
        self.cell_sugar_biofuels_kcals_equivalent = (
            self.cell_sugar_biofuels.in_units_kcals_equivalent()
        )
        self.cell_sugar_feed_kcals_equivalent = (
            self.cell_sugar_feed.in_units_kcals_equivalent()
        )
        self.scp_biofuels_kcals_equivalent = (
            self.scp_biofuels.in_units_kcals_equivalent()
        )
        self.scp_feed_kcals_equivalent = self.scp_feed.in_units_kcals_equivalent()
        self.seaweed_biofuels_kcals_equivalent = (
            self.seaweed_biofuels.in_units_kcals_equivalent()
        )
        self.seaweed_feed_kcals_equivalent = (
            self.seaweed_feed.in_units_kcals_equivalent()
        )
        self.outdoor_crops_biofuels_kcals_equivalent = (
            self.outdoor_crops_biofuels.in_units_kcals_equivalent()
        )
        self.outdoor_crops_feed_kcals_equivalent = (
            self.outdoor_crops_feed.in_units_kcals_equivalent()
        )
        self.stored_food_biofuels_kcals_equivalent = (
            self.stored_food_biofuels.in_units_kcals_equivalent()
        )
        self.stored_food_feed_kcals_equivalent = (
            self.stored_food_feed.in_units_kcals_equivalent()
        )

    def get_biofuels_and_feed_before_waste_from_animal_pops(
        self, constants_for_params, feed_over_time
    ):
        """
        Mostly, this function converts from feed_over_time in dry caloric tons to
        the appropriate fat and protein values, as well as getting biofules from the
        expected shutoff duration, then creates a Food object for the feed usage.
        This function has "animal pops" in there because it's used only in the case that
        feed is calculated in the context of breeding.
        """
        biofuel_duration = constants_for_params["DELAY"]["BIOFUEL_SHUTOFF_MONTHS"]
        biofuels_prewaste = self.get_biofuel_usage_prewaste(biofuel_duration)

        # excess feed is just using human levels of fat and protein. May need to be
        # altered to reflect more accurate usage.
        # The purpose of EXCESS_FEED_PERCENT is to be able to use even more feed until
        # all the food production is accounted for. This helps us estimate human diets.
        excess_feed_prewaste = self.get_excess_food_usage_from_percents(
            constants_for_params["EXCESS_FEED_PERCENT"]
        )

        total_feed_usage = (
            feed_over_time.in_units_bil_kcals_thou_tons_thou_tons_per_month()
            + excess_feed_prewaste.in_units_bil_kcals_thou_tons_thou_tons_per_month()
        )
        return (biofuels_prewaste, total_feed_usage, excess_feed_prewaste)

    def get_biofuel_usage_prewaste(self, biofuel_duration):
        """
        This function calculates the biofuel usage before the cap is applied.
        The total number of months before shutoff is the duration, representing the
        number of nonzero biofuel months for biofuels to be used.

        Args:
            biofuel_duration (int): The number of months before the biofuel shutoff.

        Returns:
            Food: A Food object representing the biofuel usage before waste is applied.

        Example:
            >>> feed = FeedAndBiofuels()
            >>> feed.get_biofuel_usage_prewaste(6)
            Food(kcals=[1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 0, 0, 0, 0, 0, 0],
                 fat=[0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0, 0, 0, 0, 0, 0],
                 protein=[0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0, 0, 0, 0, 0, 0],
                 kcals_units='billion kcals each month',
                 fat_units='thousand tons each month',
                 protein_units='thousand tons each month')
        """

        # Calculate the monthly biofuel usage before waste is applied
        biofuel_monthly_usage_kcals_prewaste = (
            self.biofuel_per_year_prewaste.kcals / 12 * 4e6 / 1e9
        )  # billions kcals
        biofuel_monthly_usage_fat_prewaste = (
            self.biofuel_per_year_prewaste.fat / 12 / 1e3
        )  # thousand tons
        biofuel_monthly_usage_protein_prewaste = (
            self.biofuel_per_year_prewaste.protein / 12 / 1e3
        )  # thousand tons

        # Create a Food object representing the monthly biofuel usage before waste is applied
        self.biofuel_monthly_usage_prewaste = Food(
            kcals=biofuel_monthly_usage_kcals_prewaste,
            fat=biofuel_monthly_usage_fat_prewaste,
            protein=biofuel_monthly_usage_protein_prewaste,
            kcals_units="billion kcals per month",
            fat_units="thousand tons per month",
            protein_units="thousand tons per month",
        )

        # Ensure that all values in the Food object are greater than or equal to zero
        assert self.biofuel_monthly_usage_prewaste.all_greater_than_or_equal_to_zero()

        # Create lists representing the monthly biofuel usage before waste is applied
        biofuels_kcals_prewaste = [
            self.biofuel_monthly_usage_prewaste.kcals
        ] * biofuel_duration + [0] * (self.NMONTHS - biofuel_duration)

        biofuels_fat_prewaste = [
            self.biofuel_monthly_usage_prewaste.fat
        ] * biofuel_duration + [0] * (self.NMONTHS - biofuel_duration)

        biofuels_protein_prewaste = [
            self.biofuel_monthly_usage_prewaste.protein
        ] * biofuel_duration + [0] * (self.NMONTHS - biofuel_duration)

        # Create a Food object representing the total biofuel usage before waste is applied
        biofuels_prewaste = Food(
            kcals=biofuels_kcals_prewaste,
            fat=biofuels_fat_prewaste,
            protein=biofuels_protein_prewaste,
            kcals_units="billion kcals each month",
            fat_units="thousand tons each month",
            protein_units="thousand tons each month",
        )

        return biofuels_prewaste

    def get_excess_food_usage_from_percents(self, excess_feed_percent):
        """
        Calculates the excess food usage based on the percentage of excess feed.
        Args:
            excess_feed_percent (float): The percentage of excess feed.

        Returns:
            Food: A Food object representing the excess food usage.
        """
        # TODO: ALTER BASED ON THE EXPECTED FEED FAT AND PROTEIN RATIOS
        # (CURRENTLY IS JUST USING HUMAN NEEDS)

        # This function is no longer used in the paper, but it may be useful for future work.
        # For now, it simply returns a Food object with the same percentage values for kcals, fat, and protein.

        # No excess calories
        return Food(
            kcals=excess_feed_percent,
            fat=excess_feed_percent,
            protein=excess_feed_percent,
            kcals_units="percent people fed each month",
            fat_units="percent people fed each month",
            protein_units="percent people fed each month",
        )

    def convert_kcal_to_tons(self, kcals):
        """
        Converts a given number of kcals to tons of feed or biofuel.
        Args:
            kcals (float): number of kcals to convert to tons
        Returns:
            float: number of tons equivalent to the given number of kcals
        """
        tons = kcals / self.KCAL_PER_TON  # calculate the number of tons
        return tons
