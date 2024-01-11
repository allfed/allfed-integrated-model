"""
This class is used for calculating feed and biofuel usage. They are combined into
a monthly total "excess usage" for the purposes of the optimizer, and are treated
similarly in the model.

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

        # Create a Food object for biofuel per year
        self.biofuel_per_year = Food(
            kcals=constants_for_params["BIOFUEL_KCALS"],
            fat=constants_for_params["BIOFUEL_FAT"],
            protein=constants_for_params["BIOFUEL_PROTEIN"],
            kcals_units="thousand dry caloric tons per year",
            fat_units="tons per year",
            protein_units="tons per year",
        )

        self.feed_per_year = Food(
            kcals=constants_for_params["FEED_KCALS"],
            fat=constants_for_params["FEED_FAT"],
            protein=constants_for_params["FEED_PROTEIN"],
            kcals_units="thousand dry caloric tons per year",
            fat_units="tons per year",
            protein_units="tons per year",
        )
        # Set the amount to reduce ratio each iteration and the safety margin
        self.AMOUNT_TO_REDUCE_RATIO_EACH_ITERATION = 0.01  # 1% reduction
        self.SAFETY_MARGIN = 0.01

    def create_feed_food_from_kcals(self, food_kcals):
        production_fat = np.array(food_kcals.kcals) * self.fat_to_kcal_ratio_feed
        production_protein = (
            np.array(food_kcals.kcals) * self.protein_to_kcal_ratio_feed
        )

        return Food(
            kcals=food_kcals.kcals,
            fat=production_fat,
            protein=production_protein,
            kcals_units=food_kcals.kcals_units,
            fat_units=food_kcals.fat_units,
            protein_units=food_kcals.protein_units,
        )

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

    def get_biofuels_and_feed_from_delayed_shutoff(self, constants_for_params):
        biofuel_duration = constants_for_params["DELAY"]["BIOFUEL_SHUTOFF_MONTHS"]
        biofuels = self.get_biofuel_usage(biofuel_duration)
        # excess feed is just using human levels of fat and protein. May need to be
        # altered to reflect more accurate usage.
        feed_duration = constants_for_params["DELAY"]["FEED_SHUTOFF_MONTHS"]
        feed = self.get_feed_usage(feed_duration)
        return (
            biofuels,
            feed,
        )

    def get_feed_usage(self, feed_duration):
        """
        This function is used to get the feed usage before the cap is applied.
        The total number of months before shutoff is the duration, representing the
        number of nonzero feed months for feeds to be used.
        """
        self.feed_monthly_usage = Food(
            # thousand tons annually to billion kcals per month
            kcals=self.feed_per_year.kcals / 12 * 4e6 / 1e9,
            # tons annually to thousand tons per month
            fat=self.feed_per_year.fat / 12 / 1e3,
            # tons annually to thousand tons per month
            protein=self.feed_per_year.protein / 12 / 1e3,
            kcals_units="billion kcals per month",
            fat_units="thousand tons per month",
            protein_units="thousand tons per month",
        )

        # Calculate fat-to-kcal and protein-to-kcal ratios for the first month
        # if zero kcals at any month, then set the ratio to zero as well that month
        if self.feed_monthly_usage.kcals == 0:
            self.fat_to_kcal_ratio_feed = 0
        else:
            self.fat_to_kcal_ratio_feed = (
                self.feed_monthly_usage.fat / self.feed_monthly_usage.kcals
            )

        if self.feed_monthly_usage.kcals == 0:
            self.protein_to_kcal_ratio_feed = 0
        else:
            self.protein_to_kcal_ratio_feed = (
                self.feed_monthly_usage.protein / self.feed_monthly_usage.kcals
            )

        assert self.feed_monthly_usage.all_greater_than_or_equal_to_zero()

        baseline_feed_kcals = np.array(
            [self.feed_monthly_usage.kcals] * feed_duration
            + [0] * (self.NMONTHS - feed_duration)
        )
        baseline_feed_fat = np.array(
            [self.feed_monthly_usage.fat] * feed_duration
            + [0] * (self.NMONTHS - feed_duration)
        )
        baseline_feed_protein = np.array(
            [self.feed_monthly_usage.protein] * feed_duration
            + [0] * (self.NMONTHS - feed_duration)
        )

        baseline_feed = Food(
            kcals=baseline_feed_kcals,
            fat=baseline_feed_fat,
            protein=baseline_feed_protein,
            kcals_units="billion kcals each month",
            fat_units="thousand tons each month",
            protein_units="thousand tons each month",
        )
        return baseline_feed

    def get_biofuel_usage(self, biofuel_duration):
        """
        This function calculates the biofuel usage before the cap is applied.
        The total number of months before shutoff is the duration, representing the
        number of nonzero biofuel months for biofuels to be used.

        Args:
            biofuel_duration (int): The number of months before the biofuel shutoff.

        Returns:
            Food: A Food object representing the biofuel usage per month.
        """

        # Calculate the monthly biofuel usage
        biofuel_monthly_usage_kcals = (
            self.biofuel_per_year.kcals / 12 * 4e6 / 1e9
        )  # billions kcals
        biofuel_monthly_usage_fat = (
            self.biofuel_per_year.fat / 12 / 1e3
        )  # thousand tons
        biofuel_monthly_usage_protein = (
            self.biofuel_per_year.protein / 12 / 1e3
        )  # thousand tons

        # Create a Food object representing the monthly biofuel usage
        self.biofuel_monthly_usage = Food(
            kcals=biofuel_monthly_usage_kcals,
            fat=biofuel_monthly_usage_fat,
            protein=biofuel_monthly_usage_protein,
            kcals_units="billion kcals per month",
            fat_units="thousand tons per month",
            protein_units="thousand tons per month",
        )

        # Ensure that all values in the Food object are greater than or equal to zero
        assert self.biofuel_monthly_usage.all_greater_than_or_equal_to_zero()

        # Create lists representing the monthly biofuel usage
        biofuels_kcals = [self.biofuel_monthly_usage.kcals] * biofuel_duration + [0] * (
            self.NMONTHS - biofuel_duration
        )

        biofuels_fat = [self.biofuel_monthly_usage.fat] * biofuel_duration + [0] * (
            self.NMONTHS - biofuel_duration
        )

        biofuels_protein = [self.biofuel_monthly_usage.protein] * biofuel_duration + [
            0
        ] * (self.NMONTHS - biofuel_duration)

        # Create a Food object representing the total biofuel usage
        biofuels = Food(
            kcals=biofuels_kcals,
            fat=biofuels_fat,
            protein=biofuels_protein,
            kcals_units="billion kcals each month",
            fat_units="thousand tons each month",
            protein_units="thousand tons each month",
        )

        return biofuels
