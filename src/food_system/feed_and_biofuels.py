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

        self.feed_per_year_prewaste = Food(
            kcals=constants_for_params["FEED_KCALS"],
            fat=constants_for_params["FEED_FAT"],
            protein=constants_for_params["FEED_PROTEIN"],
            kcals_units="thousand dry caloric tons per year",
            fat_units="tons per year",
            protein_units="tons per year",
        )

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
        biofuels_before_cap_prewaste = self.get_biofuel_usage_before_cap_prewaste(
            biofuel_duration
        )

        # excess feed is just using human levels of fat and protein. May need to be
        # altered to reflect more accurate usage.
        excess_feed_prewaste = self.get_excess_food_usage_from_percents(
            constants_for_params["EXCESS_FEED_PERCENT"]
        )

        feed_duration = constants_for_params["DELAY"]["FEED_SHUTOFF_MONTHS"]
        feed_before_cap_prewaste = self.get_feed_usage_before_cap_prewaste(
            feed_duration, excess_feed_prewaste
        )

        waste_adjustment = 1 - outdoor_crops.CROP_WASTE / 100
        biofuels_before_cap = biofuels_before_cap_prewaste * waste_adjustment
        feed_before_cap = feed_before_cap_prewaste * waste_adjustment
        # this is the total exceedance beyond outdoor growing max of any month
        # cumulative
        (
            max_net_demand,
            running_supply_minus_demand,
        ) = self.calculate_max_running_net_demand_postwaste(
            outdoor_crops, biofuels_before_cap, feed_before_cap
        )

        self.set_biofuels_and_feed_usage_postwaste(
            max_net_demand,
            stored_food,
            outdoor_crops,
            biofuels_before_cap,
            feed_before_cap,
            excess_feed_prewaste,
        )

        self.nonhuman_consumption = self.get_nonhuman_consumption_with_cap_postwaste(
            constants_for_params, self.biofuels, self.feed
        )

        # self.nonhuman_consumption.set_to_zero_after_month(12)

    def set_biofuels_and_feed_usage_postwaste(
        self,
        max_net_demand,
        stored_food,
        outdoor_crops,
        biofuels_before_cap,
        feed_before_cap,
        excess_feed_prewaste,
    ):

        # whether all macronutrients are zero (none exceed)
        all_zero = max_net_demand.all_equals_zero()

        # whether macronutrients exceed availability from stored foods + og
        exceeds_less_than_stored_food = max_net_demand.all_less_than_or_equal_to(
            stored_food * (1 - self.SAFETY_MARGIN)
        )

        # in order to get the pre-waste amount, we need to take the amount that we
        # calculated feed to be after cap and waste, and divide back out the waste
        # to get back to the original
        assert (
            outdoor_crops.CROP_WASTE < 100
        ), """100 percent crop waste will cause divide by zero errors"""

        waste_adjustment = 1 - outdoor_crops.CROP_WASTE / 100
        # the negative amount can be made up for by stored food, so there's no need
        # to change the biofuel or feed usage
        if all_zero or exceeds_less_than_stored_food:

            self.biofuels = biofuels_before_cap
            self.feed = feed_before_cap
            # feed to animals does not have additional waste applied (waste is applied
            # after the meat production, and thus is part of meat waste)
            self.fed_to_animals_prewaste = feed_before_cap / waste_adjustment

            return

        if not excess_feed_prewaste.all_equals_zero():
            PRINT_WARNING = False
            if PRINT_WARNING:
                print(
                    """WARNING: There was an excess feed assigned in the EXCESS_FEED
                  variable. This implies that a diet calculation is being run, in
                  order to reduce the calories per person per day to 2100.
                  However, feed and biofuels are exceeding
                  available outdoor growing and stored food!
                  Make sure this makes sense."""
                )

        ratio = self.iteratively_determine_reduction_in_nonhuman_consumption_postwaste(
            stored_food,
            outdoor_crops,
            biofuels_before_cap,
            feed_before_cap,
        )
        self.biofuels = biofuels_before_cap * ratio
        self.feed = feed_before_cap * ratio
        self.fed_to_animals_prewaste = self.feed / waste_adjustment

        assert self.biofuels.all_less_than_or_equal_to(biofuels_before_cap)
        assert self.feed.all_less_than_or_equal_to(feed_before_cap)

    def iteratively_determine_reduction_in_nonhuman_consumption_postwaste(
        self,
        stored_food,
        outdoor_crops,
        biofuels_before_cap,
        feed_before_cap,
    ):
        """
        This function iteratively determines the amount of nonhuman consumption by
        reducing the amount of biofuels and feed used.
        """

        demand_more_than_supply = True

        # initialized to zero but will be overwritten probably
        running_supply_minus_demand = Food()

        # necessary for the way we've computed this cap to work out correctly
        assert stored_food.SF_FRACTION_FAT == outdoor_crops.OG_FRACTION_FAT
        assert stored_food.SF_FRACTION_PROTEIN == outdoor_crops.OG_FRACTION_PROTEIN

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
            ) = self.calculate_max_running_net_demand_postwaste(
                outdoor_crops,
                biofuels_before_cap * ratio,
                feed_before_cap * ratio,
            )
            demand_more_than_supply = max_net_demand.any_greater_than(stored_food)
        assert 1 >= ratio >= 0

        PLOT_RUNNING_TOTAL = False
        if PLOT_RUNNING_TOTAL:
            running_supply_minus_demand.plot("running_net_supply minus demand")
        if ratio <= self.SAFETY_MARGIN:
            return 0
        else:
            return ratio - self.SAFETY_MARGIN

    def get_biofuel_usage_before_cap_prewaste(self, biofuel_duration):
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

        biofuels_before_cap_kcals_prewaste = [
            self.biofuel_monthly_usage_prewaste.kcals
        ] * biofuel_duration + [0] * (self.NMONTHS - biofuel_duration)

        biofuels_before_cap_fat_prewaste = [
            self.biofuel_monthly_usage_prewaste.fat
        ] * biofuel_duration + [0] * (self.NMONTHS - biofuel_duration)

        biofuels_before_cap_protein_prewaste = [
            self.biofuel_monthly_usage_prewaste.protein
        ] * biofuel_duration + [0] * (self.NMONTHS - biofuel_duration)

        biofuels_before_cap_prewaste = Food(
            kcals=biofuels_before_cap_kcals_prewaste,
            fat=biofuels_before_cap_fat_prewaste,
            protein=biofuels_before_cap_protein_prewaste,
            kcals_units="billion kcals each month",
            fat_units="thousand tons each month",
            protein_units="thousand tons each month",
        )

        return biofuels_before_cap_prewaste

    def get_feed_usage_before_cap_prewaste(self, feed_duration, excess_feed_prewaste):
        """
        This function is used to get the feed usage before the cap is applied.
        The total number of months before shutoff is the duration, representing the
        number of nonzero feed months for feeds to be used.
        """

        self.feed_monthly_usage_prewaste = Food(
            # thousand tons annually to billion kcals per month
            kcals=self.feed_per_year_prewaste.kcals / 12 * 4e6 / 1e9,
            # tons annually to thousand tons per month
            fat=self.feed_per_year_prewaste.fat / 12 / 1e3,
            # tons annually to thousand tons per month
            protein=self.feed_per_year_prewaste.protein / 12 / 1e3,
            kcals_units="billion kcals per month",
            fat_units="thousand tons per month",
            protein_units="thousand tons per month",
        )

        assert self.feed_monthly_usage_prewaste.all_greater_than_or_equal_to_zero()

        baseline_feed_before_cap_prewaste_kcals = np.array(
            [self.feed_monthly_usage_prewaste.kcals] * feed_duration
            + [0] * (self.NMONTHS - feed_duration)
        )
        baseline_feed_before_cap_prewaste_fat = np.array(
            [self.feed_monthly_usage_prewaste.fat] * feed_duration
            + [0] * (self.NMONTHS - feed_duration)
        )
        baseline_feed_before_cap_prewaste_protein = np.array(
            [self.feed_monthly_usage_prewaste.protein] * feed_duration
            + [0] * (self.NMONTHS - feed_duration)
        )

        baseline_feed_before_cap_prewaste = Food(
            kcals=baseline_feed_before_cap_prewaste_kcals,
            fat=baseline_feed_before_cap_prewaste_fat,
            protein=baseline_feed_before_cap_prewaste_protein,
            kcals_units="billion kcals each month",
            fat_units="thousand tons each month",
            protein_units="thousand tons each month",
        )

        return (
            baseline_feed_before_cap_prewaste
            + excess_feed_prewaste.in_units_bil_kcals_thou_tons_thou_tons_per_month()
        )

    def get_nonhuman_consumption_before_cap_prewaste(
        self,
        biofuels_before_cap_prewaste,
        feed_before_cap_prewaste,
    ):
        """
        Calculate and set the total usage for consumption of biofuels and feed
        """

        # totals human edible used for animal feed and biofuels
        # excess is directly supplied separately from the feed_shutoff used.

        nonhuman_consumption_prewaste = (
            biofuels_before_cap_prewaste + feed_before_cap_prewaste
        )

        return nonhuman_consumption_prewaste

    def get_nonhuman_consumption_with_cap_postwaste(
        self, constants_for_params, biofuels, feed
    ):
        """
        Calculate and set the total usage for consumption of biofuels and feed

        assume animals need and use human levels of fat and protein per kcal
        """
        nonhuman_consumption = biofuels + feed

        return nonhuman_consumption

    def calculate_max_running_net_demand_postwaste(
        self, outdoor_crops, biofuels_before_cap, feed_before_cap
    ):
        """
        Calculate the exceedance of the biofuel and feed usage past the outdoor outdoor_crops
        production on a monthly basis for each nutrient.

        NOTE: 
            UPDATE
            I realized that the max amount of stored food or OG used each month by kcals,
            fat or protein needs to be summed, rather than the max of each individual nutrient

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

        amount_stored_food_and_outdoor_crops_used = (
            nonhuman_consumption_before_cap.get_amount_used_other_food(
                outdoor_crops.OG_FRACTION_FAT, outdoor_crops.OG_FRACTION_PROTEIN
            )
        )
        diff = (
            amount_stored_food_and_outdoor_crops_used.fat
            / amount_stored_food_and_outdoor_crops_used.kcals
            - outdoor_crops.OG_FRACTION_FAT
        )

        no_nans_diff = np.where(
            amount_stored_food_and_outdoor_crops_used.kcals == 0, 0, diff
        )
        assert (np.round(no_nans_diff, 4) == 0).all()

        diff = (
            amount_stored_food_and_outdoor_crops_used.protein
            / amount_stored_food_and_outdoor_crops_used.kcals
            - outdoor_crops.OG_FRACTION_PROTEIN
        )

        no_nans_diff = np.where(
            amount_stored_food_and_outdoor_crops_used.kcals == 0, 0, diff
        )
        assert (np.round(no_nans_diff, 4) == 0).all()

        # outdoor crops is post waste (as well as nonhuman_consumption_before_cap)
        demand_minus_supply = amount_stored_food_and_outdoor_crops_used - outdoor_crops

        running_demand_minus_supply = (
            demand_minus_supply.get_running_total_nutrients_sum()
        )

        max_running_net_demand = running_demand_minus_supply.get_max_all_months()

        return max_running_net_demand, running_demand_minus_supply

    def get_excess_food_usage_from_percents(self, excess_feed_percent):

        # TODO: ALTER BASED ON THE EXPECTED FEED FAT AND PROTEIN RATIOS
        # (CURRENTLY IS JUST USING HUMAN NEEDS)

        # No excess calories
        return Food(
            kcals=excess_feed_percent,
            fat=excess_feed_percent,
            protein=excess_feed_percent,
            kcals_units="percent people fed each month",
            fat_units="percent people fed each month",
            protein_units="percent people fed each month",
        )
