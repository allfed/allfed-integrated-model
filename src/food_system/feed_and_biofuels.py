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

    def set_nonhuman_consumption_with_cap(
        self,
        constants_for_params,
        net_feed_available_without_stored_food,
        stored_food,
        biofuels_before_cap,  # TODO: CHANGE THIS TO PREWASTE
        feed_before_cap,  # TODO: CHANGE THIS TO PREWASTE
        excess_feed_prewaste,
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

        # this is the total exceedance beyond outdoor growing max of any month
        # cumulative
        (
            max_net_demand,
            running_supply_minus_demand,
        ) = self.calculate_max_running_net_demand_postwaste(
            constants_for_params["INCLUDE_FAT"]
            or constants_for_params["INCLUDE_PROTEIN"],
            net_feed_available_without_stored_food,
            biofuels_before_cap,
            feed_before_cap,
        )

        ratio = self.set_biofuels_and_feed_usage_postwaste(
            constants_for_params["INCLUDE_FAT"]
            or constants_for_params["INCLUDE_PROTEIN"],
            max_net_demand,
            stored_food,
            net_feed_available_without_stored_food,
            biofuels_before_cap,
            feed_before_cap,
            excess_feed_prewaste,
        )

        return ratio
        # self.nonhuman_consumption.set_to_zero_after_month(12)

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
        biofuels_before_cap_prewaste = self.get_biofuel_usage_before_cap_prewaste(
            biofuel_duration
        )

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
        return (biofuels_before_cap_prewaste, total_feed_usage, excess_feed_prewaste)

    def set_biofuels_and_feed_usage_postwaste(
        self,
        include_fat_or_protein,
        max_net_demand,
        stored_food,
        net_feed_available_without_stored_food,
        biofuels_before_cap,
        feed_before_cap,
        excess_feed_prewaste,
    ):
        # whether all macronutrients are zero (none exceed)
        all_zero = max_net_demand.all_equals_zero()

        """
        TODO

        If humans cannot be fed minimum requirement from the available food, don't feed any to animals.
        Subtract the human requirement.
        """
        # # calculate the amount of food expected to be eaten by humans
        # humans_need_estimated_without_meat =

        # # calculate the amount of food remaining from what's available for feed
        # remaining_available_for_feed =

        # if remaining_available_for_feed > 0:

        # whether macronutrients exceed availability from stored foods + og
        exceeds_less_than_stored_food = max_net_demand.all_less_than_or_equal_to(
            stored_food * (1 - self.SAFETY_MARGIN)
        )

        # the negative amount can be made up for by stored food, so there's no need
        # to change the biofuel or feed usage
        if all_zero or exceeds_less_than_stored_food:
            self.biofuels = biofuels_before_cap
            self.feed = feed_before_cap

            return 1

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
            include_fat_or_protein,
            stored_food,
            net_feed_available_without_stored_food,
            biofuels_before_cap,
            feed_before_cap,
        )
        self.biofuels = biofuels_before_cap * ratio
        self.feed = feed_before_cap * ratio

        PRINT_OVER_FEED_BIOFUEL_WARNING = True
        if PRINT_OVER_FEED_BIOFUEL_WARNING:
            print("WARNING: feed and biofuel is estimated at an impossibly high level")
            print(
                "this run has reduced biofuels and feed to a fraction of "
                + str(round(ratio, 2))
                + " of the original total estimate over all months!"
            )

        assert self.biofuels.all_less_than_or_equal_to(biofuels_before_cap)
        assert self.feed.all_less_than_or_equal_to(feed_before_cap)

        return ratio

    def iteratively_determine_reduction_in_nonhuman_consumption_postwaste(
        self,
        include_fat_or_protein,
        stored_food,
        net_feed_available_without_stored_food,
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

        if include_fat_or_protein:
            # necessary for the way we've computed this cap to work out correctly
            # TODO: account for that the ratios are different now (methane, cell_sugar)
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
                include_fat_or_protein,
                net_feed_available_without_stored_food,
                biofuels_before_cap * ratio,
                feed_before_cap * ratio,
            )
            demand_more_than_supply = max_net_demand.any_greater_than(stored_food)
        assert 1 >= ratio >= 0

        PLOT_RUNNING_TOTAL = True
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

    def calculate_max_running_net_demand_postwaste(
        self,
        account_for_fat_and_protein,
        net_feed_available_without_stored_food,
        biofuels_before_cap,
        feed_before_cap,
    ):
        """
        Calculate the exceedance of the biofuel and feed usage past the outdoor
        outdoor_crops
        production on a monthly basis for each nutrient.

        NOTE:
            UPDATE
            I realized that the max amount of stored food or OG used each month by
            kcals, fat or protein needs to be summed, rather than the max of each
            individual nutrient

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


            For all month combined, how much original stored food is needed to make up
            for each macronutrient?

        Answer:
            We sum up all the discrepancies between supply and demand.
            The stored food will need to make up for the minimum total shortage added
            up.

        """

        nonhuman_consumption_before_cap = biofuels_before_cap + feed_before_cap

        assert nonhuman_consumption_before_cap.all_greater_than_or_equal_to_zero()

        # TODO: account for fat and protein appropriately here
        if account_for_fat_and_protein:
            amount_stored_food_and_outdoor_crops_used = (
                nonhuman_consumption_before_cap.get_amount_used_other_food(
                    outdoor_crops.OG_FRACTION_FAT, outdoor_crops.OG_FRACTION_PROTEIN
                )
            )
            assert False, """ERROR: we haven't properly accounted for the fraction fat and 
            protein used when estimating feed usage"""
        else:
            amount_stored_food_and_outdoor_crops_used = nonhuman_consumption_before_cap

        # amount_stored_food_and_outdoor_crops_used is post waste (as well as
        # nonhuman_consumption_before_cap)
        demand_minus_supply = (
            amount_stored_food_and_outdoor_crops_used
            - net_feed_available_without_stored_food
        )

        running_demand_minus_supply = (
            demand_minus_supply.get_running_total_nutrients_sum()
        )

        max_running_net_demand = running_demand_minus_supply.get_max_all_months()

        return max_running_net_demand, running_demand_minus_supply

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