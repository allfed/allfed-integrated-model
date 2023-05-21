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
        self.NMONTHS = constants_for_params["NMONTHS"]

        self.biofuel_per_year_prewaste = Food(
            kcals=constants_for_params["BIOFUEL_KCALS"],
            fat=constants_for_params["BIOFUEL_FAT"],
            protein=constants_for_params["BIOFUEL_PROTEIN"],
            kcals_units="thousand dry caloric tons per year",
            fat_units="tons per year",
            protein_units="tons per year",
        )

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
        """
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
        This function is used to get the biofuel usage before the cap is applied.
        The total number of months before shutoff is the duration, representing the
        number of nonzero biofuel months for biofuels to be used.

        pre waste: this is the actual amount used of stored food and crops before waste
                   is applied to crops and stored food
        """

        biofuel_monthly_usage_kcals_prewaste = (
            self.biofuel_per_year_prewaste.kcals / 12 * 4e6 / 1e9
        )  # billions kcals
        biofuel_monthly_usage_fat_prewaste = (
            self.biofuel_per_year_prewaste.fat / 12 / 1e3
        )  # thousand tons
        biofuel_monthly_usage_protein_prewaste = (
            self.biofuel_per_year_prewaste.protein / 12 / 1e3
        )  # thousand tons

        self.biofuel_monthly_usage_prewaste = Food(
            kcals=biofuel_monthly_usage_kcals_prewaste,
            fat=biofuel_monthly_usage_fat_prewaste,
            protein=biofuel_monthly_usage_protein_prewaste,
            kcals_units="billion kcals per month",
            fat_units="thousand tons per month",
            protein_units="thousand tons per month",
        )

        assert self.biofuel_monthly_usage_prewaste.all_greater_than_or_equal_to_zero()

        biofuels_kcals_prewaste = [
            self.biofuel_monthly_usage_prewaste.kcals
        ] * biofuel_duration + [0] * (self.NMONTHS - biofuel_duration)

        biofuels_fat_prewaste = [
            self.biofuel_monthly_usage_prewaste.fat
        ] * biofuel_duration + [0] * (self.NMONTHS - biofuel_duration)

        biofuels_protein_prewaste = [
            self.biofuel_monthly_usage_prewaste.protein
        ] * biofuel_duration + [0] * (self.NMONTHS - biofuel_duration)

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
        # TODO: ALTER BASED ON THE EXPECTED FEED FAT AND PROTEIN RATIOS
        # (CURRENTLY IS JUST USING HUMAN NEEDS)

        # this only applies to diet calculations which we are no longer reporting in
        # the paper

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
        return kcals / self.KCAL_PER_TON
        # what is KCAL_PER_TON?