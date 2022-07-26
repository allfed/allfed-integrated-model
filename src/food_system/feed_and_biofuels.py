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
from pydoc import safeimport
import numpy as np
import collections

from src.food_system.food import Food


class FeedAndBiofuels:
    def __init__(self, constants_for_params):

        self.NMONTHS = constants_for_params["NMONTHS"]

        self.feed_per_year = Food(
            kcals=constants_for_params["FEED_KCALS"],
            fat=constants_for_params["FEED_FAT"],
            protein=constants_for_params["FEED_PROTEIN"],
            kcals_units="thousand dry caloric tons per year",
            fat_units="tons per year",
            protein_units="tons per year",
        )

        self.biofuel_per_year = Food(
            kcals=constants_for_params["BIOFUEL_KCALS"],
            fat=constants_for_params["BIOFUEL_FAT"],
            protein=constants_for_params["BIOFUEL_PROTEIN"],
            kcals_units="thousand dry caloric tons per year",
            fat_units="tons per year",
            protein_units="tons per year",
        )

        # TODO: DELETE THIS IF NO ERRORS
        # self.AMOUNT_TO_REDUCE_RATIO_EACH_ITERATION = 0.05  # 5% reduction
        # self.SAFETY_MARGIN = 0.1
        self.AMOUNT_TO_REDUCE_RATIO_EACH_ITERATION = 0.01  # 1% reduction
        self.SAFETY_MARGIN = 0

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

        However, if there was an excess feed assigned in the EXCESS_FEED variable,
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

        # includes assigned excess feed in nonhuman consumption
        nonhuman_consumption_before_cap = self.get_nonhuman_consumption_before_cap(
            constants_for_params, biofuels_before_cap, feed_before_cap
        )

        # this is the total exceedance beyond outdoor growing
        (
            max_net_demand,
            running_supply_minus_demand,
        ) = self.calculate_max_running_net_demand(
            outdoor_crops, biofuels_before_cap, feed_before_cap
        )

        excess_feed = constants_for_params["EXCESS_FEED"]

        self.set_biofuels_and_feed_usage(
            max_net_demand,
            stored_food,
            outdoor_crops,
            biofuels_before_cap,
            feed_before_cap,
            excess_feed,
        )

        self.nonhuman_consumption = self.get_nonhuman_consumption_with_cap(
            constants_for_params, self.biofuels, self.feed
        )

    def set_biofuels_and_feed_post_waste(self):
        """
        to keep things consistent, we apply the crop waste now to biofuels.
        this is because the total crops that are actually
        TOTAL_SF_OG = Remaining_crops_after_nonhuman_consumption*waste
        TOTAL_SF_OG = (SF_OG - nonhuman_consumption)*waste
        therefore
        TOTAL_SF_OG = SF_OG*waste - nonhuman_consumption*waste

        the only reason to apply waste to feed and biofuels is to represent the amount
        of actual crops and stored food that are used (and that usage is post-waste)

        Every other version of feed and biofuels can be considered pre-waste
        """

    def set_biofuels_and_feed_usage(
        self,
        max_net_demand,
        stored_food,
        outdoor_crops,
        biofuels_before_cap,
        feed_before_cap,
        excess_feed,
    ):

        # all macronutrients are zero (none exceed)
        all_zero = max_net_demand.all_equals_zero()

        # no macronutrients exceed availability from stored foods
        exceeds_less_than_stored_food = max_net_demand.all_less_than_or_equal_to(
            stored_food * (1 - self.SAFETY_MARGIN)
        )

        # the negative amount can be made up for by stored food, so there's no need
        # to change the biofuel or feed usage
        if all_zero or exceeds_less_than_stored_food:

            self.biofuels = biofuels_before_cap
            self.feed = feed_before_cap

            # feed to animals does not have additional waste applied (waste is applied
            # after the meat production, and thus is part of meat waste)
            self.fed_to_animals_prewaste = excess_feed + feed_before_cap

            return

        assert excess_feed.all_equals_zero(), """ERROR: There was an excess feed assigned in the EXCESS_FEED
              variable. This implies that a diet calculation is being run, in
              order to reduce the calories per person per day to 2100.
              This should NEVER be run in the context of feed and biofuels exceeding
              available outdoor growing and stored food, because in that case there
              would not be nearly enough calories to go around to make a full 2100
              kcal diet."""

        ratio = self.iteratively_determine_reduction_in_nonhuman_consumption(
            stored_food, outdoor_crops, biofuels_before_cap, feed_before_cap
        )

        print("Ratio reduction in feed needed to make scenario possible:", ratio)

        self.biofuels = biofuels_before_cap * ratio
        self.feed = feed_before_cap * ratio

        self.fed_to_animals_prewaste = excess_feed + self.feed

        assert self.biofuels.all_less_than_or_equal_to(biofuels_before_cap)
        assert self.feed.all_less_than_or_equal_to(feed_before_cap)

    def iteratively_determine_reduction_in_nonhuman_consumption(
        self, stored_food, outdoor_crops, biofuels_before_cap, feed_before_cap
    ):
        """
        This function iteratively determines the amount of nonhuman consumption by
        reducing the amount of biofuels and feed used.
        """

        demand_more_than_supply = True

        ratio = 1  # initialize to an unchanged amount
        while demand_more_than_supply:
            # if there needs to be more biofuels
            ratio -= self.AMOUNT_TO_REDUCE_RATIO_EACH_ITERATION
            if ratio < 0:
                # if the ratio is negative, then we've already reduced the
                # nonhuman consumption enough
                ratio = 0
                break

            (
                max_net_demand,
                running_supply_minus_demand,
            ) = self.calculate_max_running_net_demand(
                outdoor_crops, biofuels_before_cap * ratio, feed_before_cap * ratio
            )

            demand_more_than_supply = max_net_demand.any_greater_than(stored_food)

        assert 1 >= ratio >= 0

        print("Ratio BEFORE margin reduction:", ratio)
        print("running_supply_minus_demand")

        PLOT_RUNNING_TOTAL = False
        if PLOT_RUNNING_TOTAL:
            running_supply_minus_demand.plot()

        if ratio <= self.SAFETY_MARGIN:
            return 0
        else:
            return ratio - self.SAFETY_MARGIN

    def get_nonhuman_consumption_post_waste(self, CROP_WASTE):
        """
        This function returns amount nonhuman_consumption reduces outdoor crops and stored food
        """
        return self.nonhuman_consumption * CROP_WASTE

    def get_feed_post_waste(self, CROP_WASTE):
        """
        This function returns amount feed reduces outdoor crops and stored food
        """
        return self.feed * CROP_WASTE

    def get_biofuel_usage_before_cap(self, biofuel_duration):
        """
        This function is used to get the biofuel usage before the cap is applied.
        The total number of months before shutoff is the duration, representing the
        number of nonzero biofuel months for biofuels to be used.
        """

        biofuel_monthly_usage_kcals = (
            self.biofuel_per_year.kcals / 12 * 4e6 / 1e9
        )  # billions kcals
        biofuel_monthly_usage_fat = (
            self.biofuel_per_year.fat / 12 / 1e3
        )  # thousand tons
        biofuel_monthly_usage_protein = (
            self.biofuel_per_year.protein / 12 / 1e3
        )  # thousand tons

        self.biofuel_monthly_usage = Food(
            kcals=biofuel_monthly_usage_kcals,
            fat=biofuel_monthly_usage_fat,
            protein=biofuel_monthly_usage_protein,
            kcals_units="billion kcals per month",
            fat_units="thousand tons per month",
            protein_units="thousand tons per month",
        )

        assert self.biofuel_monthly_usage.all_greater_than_or_equal_to_zero()

        biofuels_before_cap_kcals = [
            self.biofuel_monthly_usage.kcals
        ] * biofuel_duration + [0] * (self.NMONTHS - biofuel_duration)

        biofuels_before_cap_fat = [
            self.biofuel_monthly_usage.fat
        ] * biofuel_duration + [0] * (self.NMONTHS - biofuel_duration)

        biofuels_before_cap_protein = [
            self.biofuel_monthly_usage.protein
        ] * biofuel_duration + [0] * (self.NMONTHS - biofuel_duration)

        biofuels_before_cap = Food(
            kcals=biofuels_before_cap_kcals,
            fat=biofuels_before_cap_fat,
            protein=biofuels_before_cap_protein,
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
            kcals=self.feed_per_year.kcals / 12 * 4e6 / 1e9,
            # tons annually to thousand tons per month
            fat=self.feed_per_year.fat / 12 / 1e3,
            # tons annually to thousand tons per month
            protein=self.feed_per_year.protein / 12 / 1e3,
            kcals_units="billion kcals per month",
            fat_units="thousand tons per month",
            protein_units="thousand tons per month",
        )

        assert self.FEED_MONTHLY_USAGE.all_greater_than_or_equal_to_zero()

        baseline_feed_kcals_before_cap = np.array(
            [self.FEED_MONTHLY_USAGE.kcals] * feed_duration
            + [0] * (self.NMONTHS - feed_duration)
        )
        baseline_feed_fat_before_cap = np.array(
            [self.FEED_MONTHLY_USAGE.fat] * feed_duration
            + [0] * (self.NMONTHS - feed_duration)
        )
        baseline_feed_protein_before_cap = np.array(
            [self.FEED_MONTHLY_USAGE.protein] * feed_duration
            + [0] * (self.NMONTHS - feed_duration)
        )

        baseline_feed_before_cap = Food(
            kcals=baseline_feed_kcals_before_cap,
            fat=baseline_feed_fat_before_cap,
            protein=baseline_feed_protein_before_cap,
            kcals_units="billion kcals each month",
            fat_units="thousand tons each month",
            protein_units="thousand tons each month",
        )

        return baseline_feed_before_cap

    def get_nonhuman_consumption_before_cap(
        self, constants_for_params, biofuels_before_cap, feed_before_cap
    ):
        """
        Calculate and set the total usage for consumption of biofuels and feed
        """

        # totals human edible used for animal feed and biofuels
        # excess is directly supplied separately from the feed_shutoff used.

        excess_feed = constants_for_params["EXCESS_FEED"]

        nonhuman_consumption = biofuels_before_cap + feed_before_cap + excess_feed

        return nonhuman_consumption

    def get_nonhuman_consumption_with_cap(self, constants_for_params, biofuels, feed):
        """
        Calculate and set the total usage for consumption of biofuels and feed
        """
        # assume animals need and use human levels of fat and protein per kcal
        # units grams per kcal same as units 1000s tons per billion kcals

        nonshutoff_excess = constants_for_params["EXCESS_FEED"]

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
        assert nonhuman_consumption_before_cap.all_greater_than_or_equal_to_zero()

        supply_minus_demand = outdoor_crops - nonhuman_consumption_before_cap

        running_supply_minus_demand = (
            supply_minus_demand.get_running_total_nutrients_sum()
        )

        max_running_net_demand = -running_supply_minus_demand.get_min_all_months()
        return max_running_net_demand, running_supply_minus_demand
