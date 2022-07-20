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
        )

        # billions kcals
        self.FEED_MONTHLY_USAGE = Food(
            # thousand tons per month to billion kcals per month
            kcals=self.FEED.kcals / 12 * 4e6 / 1e9,
            fat=self.FEED.fat / 12 / 1e3,
            protein=self.FEED.protein / 12 / 1e3,
        )

        self.BIOFUEL = Food(
            kcals=constants_for_params["BIOFUEL_KCALS"],
            fat=constants_for_params["BIOFUEL_FAT"],
            protein=constants_for_params["BIOFUEL_PROTEIN"],
        )

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


        Example:

        In this example, we have 4 months of biofuel and 5 months of feed before
        shutoff.

        plot: monthly exceedances before accounting for crop+stored food availability
                   |o o o o
            total  |o o o o
            usage  |+ + + + +
                   |+ + + + +
                   |+ + + + +
                   |-------------
                    1 2 3 4 5 6 7
                        month
        Key: o = biofuels (adds up to 8)
        Key: + = feed (adds up to 15)

        Let's say the outdoor growing contributes 13, and the stored food contributes
        5. Then at the end, we would remove the 8 units of biofuels, and 5 units of
        feed usage to end up with a total excess usage feed+biofuels of 10, and the
        only usage ends up being in the form of feed:

        plot: monthly exceedances after accounting for crop+stored food availability

                   |
            total  |
            usage  |
                   |+ + + + +
                   |+ + + + +
                   |-------------
                    1 2 3 4 5 6 7

        Key: o = biofuels (adds up to 0)
        Key: + = feed (adds up to 10)

        In this example we'd return the total biofuel used as zero, and the total feed
        as 10 to ensure the program exactly cancels the available outdoor growing and
        stored food due to the very high biofuel and feed demand in this scenario, but
        does not create the impossible scenario of using more biofuel and feed than
        there is outdoor crops and stored food to use for the purpose.

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

        # billion kcals per month, initialized to zero before calculation
        # this is the total exceedance beyond outdoor growing
        total_exceeding_outdoor_crops = self.calculate_exceedance_past_crops(
            outdoor_crops, nonhuman_consumption_before_cap
        )

        excess_feed_kcals = constants_for_params["EXCESS_FEED_KCALS"]

        self.set_biofuels_and_feed_usage(
            total_exceeding_outdoor_crops,
            stored_food,
            biofuels_before_cap,
            feed_before_cap,
            excess_feed_kcals,
            biofuel_duration,
            feed_duration,
            constants_for_params,
        )

        self.nonhuman_consumption = self.get_nonhuman_consumption_with_cap(
            constants_for_params, self.biofuels, self.feed
        )

    def set_biofuels_and_feed_usage(
        self,
        total_exceeding_outdoor_crops,
        stored_food,
        biofuels_before_cap,
        feed_before_cap,
        excess_feed_kcals,
        biofuel_duration,
        feed_duration,
        constants_for_params,
    ):

        # all macronutrients are zero (none exceed)
        all_zero = (total_exceeding_outdoor_crops.as_list() == 0).all()

        # no macronutrients exceed availability from stored foods
        exceeds_less_than_stored_food = (
            total_exceeding_outdoor_crops.as_list() <= stored_food.as_list()
        ).all()

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
        print("stored_food")
        print(stored_food)
        print("total_exceeding_outdoor_crops")
        print(total_exceeding_outdoor_crops)
        quit()
        # this is the aggregate amount that needs to be reduced from biofuels, and/or
        # feed. It includes kcals, fat, and protein. The most important is getting the
        # amount to reduce down to zero for the nutrient with the highest value.
        to_reduce_nonhuman_consumption = total_exceeding_outdoor_crops - stored_food

        assert to_reduce_nonhuman_consumption > Food(
            kcals=0, fat=0, protein=0
        ), """ERROR: calculating reductions to feed and biofuels, but no reduction is 
              necessary"""

        print("to_reduce_nonhuman_consumption")
        print(to_reduce_nonhuman_consumption)
        quit()
        if biofuel_duration > 0:
            biofuels_reduction_ratio = self.get_reduction_in_biofuels_ratio(
                biofuels_before_cap,
                to_reduce_nonhuman_consumption,
                biofuel_duration,
            )
            print("to_reduce_nonhuman_consumption")
            print(to_reduce_nonhuman_consumption)
            print("biofuels_reduction_ratio * biofuels_before_cap.get_nutrients_sum()")
            print(biofuels_reduction_ratio * biofuels_before_cap.get_nutrients_sum())
            print(biofuels_reduction_ratio)
            print(biofuels_before_cap.get_nutrients_sum())

            to_reduce_nonhuman_consumption = (
                to_reduce_nonhuman_consumption
                - biofuels_reduction_ratio * biofuels_before_cap.get_nutrients_sum()
            )

            self.biofuels = biofuels_before_cap * (1 - biofuels_reduction_ratio)

        if feed_duration > 0:
            feed_reduction_ratio = self.get_reduction_in_feed_ratio(
                feed_before_cap,
                to_reduce_nonhuman_consumption,
                biofuel_duration,
            )

            self.feed = feed_before_cap * (1 - feed_reduction_ratio)

            to_reduce_nonhuman_consumption = (
                to_reduce_nonhuman_consumption
                - feed_reduction_ratio * feed_before_cap.get_nutrients_sum()
            )

        assert (self.feed <= feed_before_cap).all()
        assert (self.biofuels <= biofuels_before_cap).all()

        # it's okay if to_reduce_nonhuman_consumption is negative, because this means
        # that the amount of nonhuman consumption use of some may have been reduced more
        # than strictly be necessary, but this is fine because we expect the minimum is
        # exactly zero.
        assert (
            to_reduce_nonhuman_consumption <= 0
        ).all(), """ERROR: a nutrient is
         above zero that means that there is a nonhuman consumption nutrient that
          cannot be reduced enough by reducing biofuels"""

        assert (
            to_reduce_nonhuman_consumption.get_max_nutrient() >= 0
        ), """ERROR: feed and biofuel
          reductions have added up to more than was required to be produced"""
        assert (
            to_reduce_nonhuman_consumption.get_max_nutrient() <= 0
        ), """ERROR: feed and biofuel reductions were reduced by too little, more needs to be reduced to compensate for low levels of stored food and outdoor growing"""

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

        return biofuels_before_cap

    def get_feed_usage_before_cap(self, feed_duration):
        """
        This function is used to get the feed usage before the cap is applied.
        The total number of months before shutoff is the duration, representing the
        number of nonzero feed months for feeds to be used.
        """
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

        feed_shutoff_before_cap = Food()
        feed_shutoff_before_cap.kcals = feed_shutoff_kcals_before_cap
        feed_shutoff_before_cap.fat = feed_shutoff_fat_before_cap
        feed_shutoff_before_cap.protein = feed_shutoff_protein_before_cap

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

        # totals human edible used for animal feed and biofuels
        # excess is directly supplied separately from the feed_shutoff used.

        nonhuman_consumption = Food()

        nonhuman_consumption.kcals = (
            constants_for_params["EXCESS_FEED_KCALS"]
            + biofuels_before_cap.kcals
            + feed_before_cap.kcals
        )

        nonhuman_consumption.fat = (
            nonshutoff_excess_fat + biofuels_before_cap.fat + feed_before_cap.fat
        )

        nonhuman_consumption.protein = (
            nonshutoff_excess_protein
            + biofuels_before_cap.protein
            + feed_before_cap.protein
        )

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

        nonhuman_consumption = Food()

        nonhuman_consumption.kcals = (
            constants_for_params["EXCESS_FEED_KCALS"] + biofuels.kcals + feed.kcals
        )

        nonhuman_consumption.fat = nonshutoff_excess_fat + biofuels.fat + feed.fat

        nonhuman_consumption.protein = (
            nonshutoff_excess_protein + biofuels.protein + feed.protein
        )

        return nonhuman_consumption

    def calculate_exceedance_past_crops(self, crops, nonhuman_consumption_before_cap):
        """
        Calculate the exceedance of the biofuel and feed usage past the outdoor crops
        production on a monthly basis for each nutrient.
        """
        total_exceeding_outdoor_crops = Food()

        # this is a rather fancy way to calculate the total exceedance in all the months
        # that contain more feed and biofuels nutrient usage than that nutrient usage
        # is available by looping through the nutrient names (kcals, fat, protein)
        for nutrient_name in Food.get_nutrient_names():
            # if nutrient_name == "fat" or nutrient_name == "protein":
            #     # TODO
            #     continue

            exceeding_sum = 0  # initialize to zero

            for i in range(self.NMONTHS):
                nonhuman_consumption_nutrient = getattr(
                    nonhuman_consumption_before_cap, nutrient_name
                )
                crop_nutrient = getattr(crops, nutrient_name)
                if nonhuman_consumption_nutrient[i] > crop_nutrient[i]:
                    exceeding_sum += nonhuman_consumption_nutrient[i] - crop_nutrient[i]

            # set the total_exceeding_outdoor_crops nutrient to the sum of exceedances
            # of that nutrient
            setattr(total_exceeding_outdoor_crops, nutrient_name, exceeding_sum)

        return total_exceeding_outdoor_crops

    def get_reduction_in_biofuels_ratio(
        self,
        biofuels_before_cap,
        to_reduce_nonhuman_consumption,
        biofuel_duration,
    ):
        """
        If there's a limit based on crops+stored food,
        changes the returned ratio of biofuel usage accordingly.

        Assumption: total_exceeding_outdoor_crops > stored_food
        Assumption: biofuel usage is constant for all months it is nonzero

        Arguments:
            total_exceeding_outdoor_crops (float): total exceedance of the nonhuman
                consumption beyond the outdoor crops
            stored_food (float): total amount of stored food

        Returns:
        The ratio biofuels needs to be reduced by. This is the same ratio for all
        nutrients. 1==100% reduction here.
        """
        for month in range(self.NMONTHS):
            assert (
                biofuels_before_cap.kcals[month] == biofuels_before_cap.kcals[0]
                or biofuels_before_cap.kcals[0] == 0
            ), """ERROR: biofuels has to be constant every month it's nonzero. 
                First month with error: """ + str(
                month
            )

        assert biofuels_before_cap.get_first_month() > Food(
            kcals=0, fat=0, protein=0
        ), """ERROR: Biofuels first month must be nonzero if trying to reduce biofuels to match available stored food and outdoor growing"""

        # the amount to try to reduce biofuels by is split into each month biofuels is
        # used
        remainder_per_biofuel_month = to_reduce_nonhuman_consumption / biofuel_duration

        # the  biofuels are consistent every month and the duration is nonzero,
        # so we just look at the first month
        to_reduce_nonhuman_consumption = (
            biofuels_before_cap.get_first_month() - remainder_per_biofuel_month
        )

        # the lowest to_reduce_nonhuman_consumption nutrient will be used to assign total biofuels used
        (
            nutrient_name,
            min_remaining,
        ) = to_reduce_nonhuman_consumption.get_min_nutrient()
        print("min_remaining")
        print(min_remaining)
        quit()

        if min_remaining > 0:
            # in the case that the most used up nutrient is still able to be made up
            # for by a reduction in biofuels
            biofuel_amount_nutrient = getattr(biofuels_before_cap, nutrient_name)

            # the ratio of biofuels to get to the minimum nutrient
            biofuel_ratio = min_remaining / biofuel_amount_nutrient

            assert (
                biofuel_ratio > 0 and biofuel_ratio < 1
            ), """ERROR: biofuel ratio
            reduction must be between zero and one"""

            print("biofuel_amount_nutrient")
            print(biofuel_amount_nutrient)
            # the reduction in biofuels is the original minus the new expected amount
            return 1 - biofuel_ratio
        else:
            # reduction is 100%
            return 1

    def get_reduction_in_feed_ratio(
        self,
        feed_before_cap,
        to_reduce_nonhuman_consumption,
        feed_duration,
    ):
        """
        If there's a limit based on crops+stored food,
        changes the returned ratio of feed usage accordingly.

        Assumption: total_exceeding_outdoor_crops > stored_food
        Assumption: feed usage is constant for all months it is nonzero

        Arguments:
            feed_before_cap,
            to_reduce_nonhuman_consumption,
            feed_duration,

        Returns:
        The ratio feed needs to be reduced by. This is the same ratio for all
        nutrients. 1==100% reduction here.
        """

        assert (
            feed_before_cap.kcals == feed_before_cap.kcals[0]
            or feed_before_cap.kcals == 0
        ).all(), "ERROR: feed has to be constant every month it's nonzero"

        # the amount to try to reduce feed by is split into each month feed is
        # used
        remainder_per_feed_month = to_reduce_nonhuman_consumption / feed_duration

        # the  feed are consistent every month and the duration is nonzero,
        # so we just look at the first month
        to_reduce_nonhuman_consumption = (
            feed_before_cap.get_first_month() - remainder_per_feed_month
        )

        assert (
            feed_before_cap.get_first_month() > 0
        ), """ERROR: Feed first month must be nonzero if trying to reduce feed to match 
            available stored food and outdoor growing"""

        # the lowest to_reduce_nonhuman_consumption nutrient will be used to assign total feed used
        (
            nutrient_name,
            min_remaining,
        ) = to_reduce_nonhuman_consumption.get_min_nutrient()

        if min_remaining > 0:
            # in the case that the most used up nutrient is still able to be made up
            # for by a reduction in feed
            feed_amount_nutrient = getattr(feed_before_cap, nutrient_name)

            # the ratio of feed to get to the minimum nutrient
            feed_ratio = min_remaining / feed_amount_nutrient

            # the reduction in feed is the original minus the new expected amount
            return 1 - feed_ratio
        else:
            # reduction is 100%
            return 1
