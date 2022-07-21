#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

This class is used for calculating feed and biofuel usage. They are combined into
a monthly total "excess usage" for the purposes of the optimizer, and are treated 
similarly in the model.

Created on Wed Jul 17

@author: morgan
"""

from operator import mod
import numpy as np
import collections

from src.food_system.food import Food


class FeedAndBiofuels:
    def __init__(self, constants_for_params):

        self.NMONTHS = constants_for_params["NMONTHS"]

        self.FEED = Food(
            kcals=constants_for_params["FEED_KCALS"],
            fat=constants_for_params["FEED_FAT"],
            protein=constants_for_params["FEED_PROTEIN"],
            kcals_units="thousand dry caloric tons per year",
            fat_units="tons per year",
            protein_units="tons per year",
        )

        self.BIOFUEL = Food(
            kcals=constants_for_params["BIOFUEL_KCALS"],
            fat=constants_for_params["BIOFUEL_FAT"],
            protein=constants_for_params["BIOFUEL_PROTEIN"],
            kcals_units="thousand dry caloric tons per year",
            fat_units="tons per year",
            protein_units="tons per year",
        )
        self.AMOUNT_TO_REDUCE_RATIO_EACH_ITERATION = 0.01  # 10% reduction

    def set_nonhuman_consumption_with_cap(
        self, constants_for_params, outdoor_crops, stored_food
    ):
        """
        #NOTE: This function depends on get_excess being run first!

        Cap biofuel usage to the amount of food available (stored food
        plus outdoor crops)

        This takes all the outdoor growing in each month in which feed and biofuel would
        be used. First, the amount of food from the outdoor crops is subtracted from the
        net feed plus biofuel previously assigned to be used.

        If kcals, fat, and
        protein used by biofuels plus feed is always less than outdoor growing, then
        nothing is changed and the program returns.

        If kcals, fat, and
        protein used by biofuels plus feed is greater in any of the months than outdoor
        growing, then the sum of all of these exceedances from what is grown is summed.
        If the sum of exceedances is greater than any of the macronutrients summed from
        stored food, then the amount of biofuels is reduced such that the sum of
        exceedances uses exactly as much stored food is available.

        However, if there was an excess feed assigned in the EXCESS_FEED_KCALS variable,
        then this implies that a diet calculation is being run, in order to reduce the
        calories per person per day to 2100. This should NEVER be run in the context of
        feed and biofuels exceeding available outdoor growing and stored food, because
        in that case there would not be nearly enough calories to go around. Therefore,
        the program will raise an error if this occurs.

        If the biofuels are reduced to zero, then the remaining exceedance is subtracted
        from the feed usage until exceedances use exactly as much stored food is
        available.

        In the case that the stored food is zero, this means that biofuels plus feed
        will be capped to the outdoor production of any macronutrient in any month.

        """
        # billion kcals per month

        biofuel_duration = constants_for_params["DELAY"]["BIOFUEL_SHUTOFF_MONTHS"]
        biofuels_before_cap = self.get_biofuel_usage_before_cap(biofuel_duration)

        feed_duration = constants_for_params["DELAY"]["FEED_SHUTOFF_MONTHS"]
        feed_before_cap = self.get_feed_usage_before_cap(feed_duration)

        self.kcals_fed_to_animals = (
            constants_for_params["EXCESS_FEED_KCALS"] + feed_before_cap.kcals
        )

        # includes assigned excess feed in nonhuman consumption
        nonhuman_consumption_before_cap = self.get_nonhuman_consumption_before_cap(
            constants_for_params, biofuels_before_cap, feed_before_cap
        )

        # this is the total exceedance beyond outdoor growing
        max_net_demand = self.calculate_max_running_net_demand(
            outdoor_crops, biofuels_before_cap, feed_before_cap
        )

        excess_feed_kcals = constants_for_params["EXCESS_FEED_KCALS"]

        self.set_biofuels_and_feed_usage(
            max_net_demand,
            stored_food,
            outdoor_crops,
            biofuels_before_cap,
            feed_before_cap,
            excess_feed_kcals,
        )

        self.nonhuman_consumption = self.get_nonhuman_consumption_with_cap(
            constants_for_params, self.biofuels, self.feed
        )

    def set_biofuels_and_feed_usage(
        self,
        max_net_demand,
        stored_food,
        outdoor_crops,
        biofuels_before_cap,
        feed_before_cap,
        excess_feed_kcals,
    ):

        # all macronutrients are zero (none exceed)
        all_zero = max_net_demand.equals_zero()

        # no macronutrients exceed availability from stored foods
        exceeds_less_than_stored_food = max_net_demand.all_less_than_or_equal(
            stored_food
        )

        # the negative amount can be made up for by stored food, so there's no need
        # to change the biofuel or feed usage
        if all_zero or exceeds_less_than_stored_food:
            self.biofuels = biofuels_before_cap
            self.feed = feed_before_cap
            return

        assert (
            (excess_feed_kcals == 0).all()
        ).all(), """ERROR: There was an excess feed assigned in the EXCESS_FEED_KCALS
              variable. This implies that a diet calculation is being run, in
              order to reduce the calories per person per day to 2100.
              This should NEVER be run in the context of feed and biofuels exceeding
              available outdoor growing and stored food, because in that case there
              would not be nearly enough calories to go around to make a full 2100
              kcal diet."""

        ratio = self.iteratively_determine_reduction_in_nonhuman_consumption(
            stored_food, outdoor_crops, biofuels_before_cap, feed_before_cap
        )

        self.biofuels = biofuels_before_cap * ratio
        self.feed = feed_before_cap * ratio

        assert self.biofuels.all_less_than_or_equal(biofuels_before_cap)
        assert self.feed.all_less_than_or_equal(feed_before_cap)

    def iteratively_determine_reduction_in_nonhuman_consumption(
        self, stored_food, outdoor_crops, biofuels_before_cap, feed_before_cap
    ):

        demand_more_than_supply = True

        ratio = 1
        while demand_more_than_supply:
            # if there needs to be more biofuels
            ratio -= self.AMOUNT_TO_REDUCE_RATIO_EACH_ITERATION
            if ratio < 0:
                # if the ratio is negative, then we've already reduced the
                # nonhuman consumption enough
                ratio = 0
                break

            max_net_demand = self.calculate_max_running_net_demand(
                outdoor_crops, biofuels_before_cap * ratio, feed_before_cap * ratio
            )

            demand_more_than_supply = max_net_demand.any_greater_than(stored_food)

        assert 1 >= ratio >= 0

        print("Final ratio for feed and biofuels:" + str(ratio))
        return ratio

    def get_biofuel_usage_before_cap(self, biofuel_duration):
        """
        This function is used to get the biofuel usage before the cap is applied.
        The total number of months before shutoff is the duration, representing the
        number of nonzero biofuel months for biofuels to be used.
        """

        self.BIOFUEL_MONTHLY_USAGE = Food()

        self.BIOFUEL_MONTHLY_USAGE.kcals = (
            self.BIOFUEL.kcals / 12 * 4e6 / 1e9
        )  # billions kcals
        self.BIOFUEL_MONTHLY_USAGE.fat = self.BIOFUEL.fat / 12 / 1e3  # thousand tons
        self.BIOFUEL_MONTHLY_USAGE.protein = (
            self.BIOFUEL.protein / 12 / 1e3
        )  # thousand tons

        assert self.BIOFUEL_MONTHLY_USAGE.all_greater_than_or_equal_zero()

        self.BIOFUEL_MONTHLY_USAGE.set_units(
            kcals_units="billion kcals per month",
            fat_units="thousand tons per month",
            protein_units="thousand tons per month",
        )

        biofuels_before_cap = Food()

        biofuels_before_cap.kcals = [
            self.BIOFUEL_MONTHLY_USAGE.kcals
        ] * biofuel_duration + [0] * (self.NMONTHS - biofuel_duration)

        biofuels_before_cap.fat = [
            self.BIOFUEL_MONTHLY_USAGE.fat
        ] * biofuel_duration + [0] * (self.NMONTHS - biofuel_duration)

        biofuels_before_cap.protein = [
            self.BIOFUEL_MONTHLY_USAGE.protein
        ] * biofuel_duration + [0] * (self.NMONTHS - biofuel_duration)

        biofuels_before_cap.set_units(
            kcals_units="billion kcals each month",
            fat_units="thousand tons each month",
            protein_units="thousand tons each month",
        )

        return biofuels_before_cap

    def get_feed_usage_before_cap(self, feed_duration):
        """
        This function is used to get the feed usage before the cap is applied.
        The total number of months before shutoff is the duration, representing the
        number of nonzero feed months for feeds to be used.
        """

        self.FEED_MONTHLY_USAGE = Food(
            # thousand tons annually to billion kcals per month
            kcals=self.FEED.kcals / 12 * 4e6 / 1e9,
            # tons annually to thousand tons per month
            fat=self.FEED.fat / 12 / 1e3,
            # tons annually to thousand tons per month
            protein=self.FEED.protein / 12 / 1e3,
            kcals_units="billion kcals per month",
            fat_units="thousand tons per month",
            protein_units="thousand tons per month",
        )

        assert self.FEED_MONTHLY_USAGE.all_greater_than_or_equal_zero()

        feed_shutoff_kcals_before_cap = np.array(
            [self.FEED_MONTHLY_USAGE.kcals] * feed_duration
            + [0] * (self.NMONTHS - feed_duration)
        )
        feed_shutoff_fat_before_cap = np.array(
            [self.FEED_MONTHLY_USAGE.fat] * feed_duration
            + [0] * (self.NMONTHS - feed_duration)
        )
        feed_shutoff_protein_before_cap = np.array(
            [self.FEED_MONTHLY_USAGE.protein] * feed_duration
            + [0] * (self.NMONTHS - feed_duration)
        )

        feed_shutoff_before_cap = Food(
            kcals=feed_shutoff_kcals_before_cap,
            fat=feed_shutoff_fat_before_cap,
            protein=feed_shutoff_protein_before_cap,
            kcals_units="billion kcals each month",
            fat_units="thousand tons each month",
            protein_units="thousand tons each month",
        )

        return feed_shutoff_before_cap

    def get_nonhuman_consumption_before_cap(
        self, constants_for_params, biofuels_before_cap, feed_before_cap
    ):
        """
        Calculate and set the total usage for consumption of biofuels and feed
        """
        # assume animals need and use human levels of fat and protein per kcal
        # units grams per kcal same as units 1000s tons per billion kcals
        fat_used_livestock = (
            constants_for_params["NUTRITION"]["FAT_DAILY"]
            / constants_for_params["NUTRITION"]["KCALS_DAILY"]
        )

        protein_used_livestock = (
            constants_for_params["NUTRITION"]["PROTEIN_DAILY"]
            / constants_for_params["NUTRITION"]["KCALS_DAILY"]
        )

        nonshutoff_excess_fat = (
            fat_used_livestock * constants_for_params["EXCESS_FEED_KCALS"]
        )

        nonshutoff_excess_protein = (
            protein_used_livestock * constants_for_params["EXCESS_FEED_KCALS"]
        )

        nonshutoff_excess = Food(
            kcals=constants_for_params["EXCESS_FEED_KCALS"],
            fat=nonshutoff_excess_fat,
            protein=nonshutoff_excess_protein,
            kcals_units="billion kcals each month",
            fat_units="thousand tons each month",
            protein_units="thousand tons each month",
        )

        # totals human edible used for animal feed and biofuels
        # excess is directly supplied separately from the feed_shutoff used.

        nonhuman_consumption = biofuels_before_cap + feed_before_cap + nonshutoff_excess

        return nonhuman_consumption

    def get_nonhuman_consumption_with_cap(self, constants_for_params, biofuels, feed):
        """
        Calculate and set the total usage for consumption of biofuels and feed
        """
        # assume animals need and use human levels of fat and protein per kcal
        # units grams per kcal same as units 1000s tons per billion kcals
        fat_used_livestock = (
            constants_for_params["NUTRITION"]["FAT_DAILY"]
            / constants_for_params["NUTRITION"]["KCALS_DAILY"]
        )

        protein_used_livestock = (
            constants_for_params["NUTRITION"]["PROTEIN_DAILY"]
            / constants_for_params["NUTRITION"]["KCALS_DAILY"]
        )

        nonshutoff_excess_fat = (
            fat_used_livestock * constants_for_params["EXCESS_FEED_KCALS"]
        )

        nonshutoff_excess_protein = (
            protein_used_livestock * constants_for_params["EXCESS_FEED_KCALS"]
        )

        # totals human edible used for animal feed and biofuels
        # excess is directly supplied separately from the feed_shutoff used.
        nonshutoff_excess = Food(
            kcals=constants_for_params["EXCESS_FEED_KCALS"],
            fat=nonshutoff_excess_fat,
            protein=nonshutoff_excess_protein,
            kcals_units="billion kcals each month",
            fat_units="thousand tons each month",
            protein_units="thousand tons each month",
        )

        nonhuman_consumption = biofuels + feed + nonshutoff_excess

        return nonhuman_consumption

    def calculate_max_running_net_demand(
        self, outdoor_crops, biofuels_before_cap, feed_before_cap
    ):
        """
        Calculate the exceedance of the biofuel and feed usage past the outdoor outdoor_crops
        production on a monthly basis for each nutrient.

        Example:

        outdoor crops:
            kcals:   10, 20, 10, 10
            fat:     10, 30, 20, 20
            protein: 10, 30, 20, 20
            month:    1   2   3   4

        nonhuman_consumption:
            kcals:    5, 20, 10, 15
            fat:      5, 15, 25, 20
            protein: 25, 15, 20, 20
            month:    1   2   3   4

        supply_minus_demand:
            kcals:    5,  0,  0, -5
            fat:      5, 15, -5,  0
            protein:-15, 15,  0,  0
            month:    1   2   3   4

        running_net_supply:
            kcals:    5,  5,  5,  0
            fat:      5, 20, 15, 15
            protein:-15,  0,  0,  0
            month:    1   2   3   4

        min_running_net_supply:
            kcals:    0
            fat:      5
            protein:-15
            month: allmonths

        max_running_net_demand:
            kcals:    0
            fat:      -5
            protein: 15
            month: allmonths


        For all month combined, how much original stored food is needed to make up for
        each macronutrient?

        Answer:
            We sum up all the discrepancies between supply and demand.
            The stored food will need to make up for the minimum total shortage added
            up.

        """

        nonhuman_consumption_before_cap = biofuels_before_cap + feed_before_cap
        assert nonhuman_consumption_before_cap.all_greater_than_or_equal_zero()

        supply_minus_demand = outdoor_crops - nonhuman_consumption_before_cap

        running_supply_minus_demand = (
            supply_minus_demand.get_running_total_nutrients_sum()
        )

        PLOT_RUNNING_TOTAL = False
        if PLOT_RUNNING_TOTAL:
            running_supply_minus_demand.plot("running total")

        max_running_net_demand = -running_supply_minus_demand.get_min_all_months()

        return max_running_net_demand
