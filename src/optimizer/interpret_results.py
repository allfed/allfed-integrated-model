"""
This function takes the raw output of the optimizer food categories and total people fed
and breaks this down into what the amount of each expected food category would be in
order to produce these results.

The evaluation creates more useful values for plotting and scenario evaluation than
exactly what is being optimized in the optimizer.

Created on Tue Jul 19

@author: morgan
"""
import os
import sys

module_path = os.path.abspath(os.path.join("../.."))
if module_path not in sys.path:
    sys.path.append(module_path)

from src.food_system.food import Food
import numpy as np


class Interpreter:
    """
    This class is used to convert between optimization results data and other useful
    ways of interpreting the results, as a diet, or as a total food supply.
    """

    def __init__(self):
        pass

    def interpret_results(self, extracted_results, multi_valued_constants):
        """
        This function takes the raw output of the optimizer food categories and total
        people fed in list form, and converts the naive people fed which includes
        negative feed, into a purely list of values, where the negative feed has been
        subtracted from the sum of outdoor growing and stored food.

        ANYTHING assigned to "self" here is part of a useful result that will either
        be printed or plotted as a result

        """

        self.assign_percent_fed_from_extractor(extracted_results)
        self.assign_kcals_equivalent_from_extractor(extracted_results)

        # now the same, but in units effective kcals per day
        # all these are just used for plotting only

        # TODO: only used for plotting, should remove eventually
        self.constants = extracted_results.constants
        self.assign_time_months_middle(self.constants["NMONTHS"])

        # nonhuman consumption in units percent people fed

        nonhuman_consumption_billions_fed = multi_valued_constants[
            "nonhuman_consumption"
        ]

        self.nonhuman_consumption_percent = (
            nonhuman_consumption_billions_fed.in_units_percent_fed()
        )

        self.assign_interpreted_properties(extracted_results)

        self.include_fat = Food.conversions.include_fat
        self.include_protein = Food.conversions.include_protein

        return self

    def assign_percent_fed_from_extractor(self, extracted_results):

        self.stored_food = extracted_results.stored_food.in_units_percent_fed()

        self.outdoor_crops = extracted_results.outdoor_crops.in_units_percent_fed()

        self.seaweed = extracted_results.seaweed.in_units_percent_fed()

        self.cell_sugar = extracted_results.cell_sugar.in_units_percent_fed()

        self.scp = extracted_results.scp.in_units_percent_fed()

        self.greenhouse = extracted_results.greenhouse.in_units_percent_fed()

        self.fish = extracted_results.fish.in_units_percent_fed()

        self.culled_meat_plus_grazing_cattle_maintained = (
            extracted_results.culled_meat_plus_grazing_cattle_maintained.in_units_percent_fed()
        )

        self.grazing_milk = extracted_results.grazing_milk.in_units_percent_fed()

        self.grain_fed_meat = extracted_results.grain_fed_meat.in_units_percent_fed()

        self.grain_fed_milk = extracted_results.grain_fed_milk.in_units_percent_fed()

        self.immediate_outdoor_crops = (
            extracted_results.immediate_outdoor_crops.in_units_percent_fed()
        )

        self.new_stored_outdoor_crops = (
            extracted_results.new_stored_outdoor_crops.in_units_percent_fed()
        )

    def assign_kcals_equivalent_from_extractor(self, extracted_results):

        self.stored_food_kcals_equivalent = (
            extracted_results.stored_food.in_units_kcals_equivalent()
        )

        self.outdoor_crops_kcals_equivalent = (
            extracted_results.outdoor_crops.in_units_kcals_equivalent()
        )

        self.seaweed_kcals_equivalent = (
            extracted_results.seaweed.in_units_kcals_equivalent()
        )

        self.cell_sugar_kcals_equivalent = (
            extracted_results.cell_sugar.in_units_kcals_equivalent()
        )

        self.scp_kcals_equivalent = extracted_results.scp.in_units_kcals_equivalent()

        self.greenhouse_kcals_equivalent = (
            extracted_results.greenhouse.in_units_kcals_equivalent()
        )

        self.fish_kcals_equivalent = extracted_results.fish.in_units_kcals_equivalent()

        self.culled_meat_plus_grazing_cattle_maintained_kcals_equivalent = (
            extracted_results.culled_meat_plus_grazing_cattle_maintained.in_units_kcals_equivalent()
        )

        self.grazing_milk_kcals_equivalent = (
            extracted_results.grazing_milk.in_units_kcals_equivalent()
        )

        self.grain_fed_meat_kcals_equivalent = (
            extracted_results.grain_fed_meat.in_units_kcals_equivalent()
        )

        self.grain_fed_milk_kcals_equivalent = (
            extracted_results.grain_fed_milk.in_units_kcals_equivalent()
        )

        self.immediate_outdoor_crops_kcals_equivalent = (
            extracted_results.immediate_outdoor_crops.in_units_kcals_equivalent()
        )

        self.new_stored_outdoor_crops_kcals_equivalent = (
            extracted_results.new_stored_outdoor_crops.in_units_kcals_equivalent()
        )

    def set_to_humans_properties_kcals_equivalent(self, extracted_results):

        self.stored_food_to_humans_kcals_equivalent = (
            self.stored_food_to_humans.in_units_kcals_equivalent()
        )

        self.outdoor_crops_to_humans_kcals_equivalent = (
            self.outdoor_crops_to_humans.in_units_kcals_equivalent()
        )

        self.immediate_outdoor_crops_to_humans_kcals_equivalent = (
            self.immediate_outdoor_crops_to_humans.in_units_kcals_equivalent()
        )

        self.new_stored_outdoor_crops_to_humans_kcals_equivalent = (
            self.new_stored_outdoor_crops_to_humans.in_units_kcals_equivalent()
        )

    def assign_time_months_middle(self, NMONTHS):
        self.time_months_middle = []
        for month in range(0, NMONTHS):
            self.time_months_middle.append(month + 0.5)

    def assign_interpreted_properties(self, extracted_results):

        humans_fed_sum = self.get_sum_by_subtracting_nonhuman(
            self.nonhuman_consumption_percent
        )

        (
            self.percent_people_fed,
            self.constraining_nutrient,
        ) = self.get_percent_people_fed(humans_fed_sum)
        # rounding errors can be introduced by the optimizer. We correct them here.
        # ... at least the ones that we can identify.
        # We also round everything to within 0.1% of its value,
        # in terms of % people fed.
        (
            self.stored_food_rounded,
            self.seaweed_rounded,
            self.outdoor_crops_rounded,
            self.immediate_outdoor_crops_rounded,
            self.new_stored_outdoor_crops_rounded,
            self.outdoor_crops_plus_stored_food,
        ) = self.correct_and_validate_rounding_errors(self.nonhuman_consumption_percent)

        # get the ratio for stored_food_rounded and outdoor_crops (after subtracting
        # feed and biofuels)
        to_humans_ratio = self.get_ratio_for_stored_food_and_outdoor_crops(
            self.outdoor_crops_plus_stored_food,
            self.nonhuman_consumption_percent,
        )

        (
            self.stored_food_to_humans,
            self.outdoor_crops_to_humans,
            self.immediate_outdoor_crops_to_humans,
            self.new_stored_outdoor_crops_to_humans,
        ) = self.get_amount_fed_to_humans(
            self.stored_food,
            self.outdoor_crops,
            self.immediate_outdoor_crops,
            self.new_stored_outdoor_crops,
            to_humans_ratio,
        )

        self.excess_feed = extracted_results.excess_feed

        self.set_to_humans_properties_kcals_equivalent(extracted_results)

        self.kcals_fed = humans_fed_sum.kcals
        self.fat_fed = humans_fed_sum.fat
        self.protein_fed = humans_fed_sum.protein

        difference = humans_fed_sum - self.get_sum_by_adding_to_humans()

        # checking that the two ways of adding up food to humans match
        assert difference.get_rounded_to_decimal(decimals=1).all_equals_zero()

    def get_mean_min_nutrient(self):
        """
        for finding the minimum of any nutrient in any month
        and then getting the mean people fed in all the months
        This is useful for assessing what would have happened if stored food were not
        a constraint on number of people fed

        returns: the mean people fed in all months
        """
        # this is what the command below does
        # >>> a = np.array([3,2,1])
        # >>> b = np.array([2,2,6])
        # >>> c = np.array([100,100,0])
        # >>> np.min([a,b,c],axis=0)
        # array([2, 2, 0])
        # TODO @ Morgan: this variable does not exist? What's the plan here?
        assert humans_fed_sum.is_units_percent()
        min_fed = np.min([self.kcals_fed, self.fat_fed, self.protein_fed], axis=0)

        mean_fed = np.mean(min_fed)
        return mean_fed

    def get_amount_fed_to_humans(
        self,
        stored_food,
        outdoor_crops,
        immediate_outdoor_crops,
        new_stored_outdoor_crops,
        to_humans_ratio,
    ):

        # apply the reduction to stored food and outdoor crops
        stored_food_to_humans = to_humans_ratio * stored_food
        outdoor_crops_to_humans = to_humans_ratio * outdoor_crops

        # NOTE: immediate and new used may be slightly different than the outdoor
        #       crops due to rounding errors

        immediate_outdoor_crops_to_humans = to_humans_ratio * immediate_outdoor_crops

        # used for plotting immediate vs food stored in the scenario
        new_stored_outdoor_crops_to_humans = to_humans_ratio * new_stored_outdoor_crops

        return (
            stored_food_to_humans,
            outdoor_crops_to_humans,
            immediate_outdoor_crops_to_humans,
            new_stored_outdoor_crops_to_humans,
        )

    def get_sum_by_adding_to_humans(self):
        """
        sum the resulting nutrients from the extracted_results, but subtract nonhuman
        to get the ratio

        also rounds result to 1 decimal place in terms of percent fed (within 0.1% of
        it's value)
        """

        to_humans_fed_sum = (
            self.stored_food_to_humans
            + self.outdoor_crops_to_humans
            + self.seaweed
            + self.cell_sugar
            + self.scp
            + self.greenhouse
            + self.fish
            + self.culled_meat_plus_grazing_cattle_maintained
            + self.grazing_milk
            + self.grain_fed_meat
            + self.grain_fed_milk
        )

        return to_humans_fed_sum

    def get_sum_by_subtracting_nonhuman(self, nonhuman_consumption):
        """
        sum the resulting nutrients from the extracted_results, but do this by adding
        all the amounts determined to go to humans

        also rounds result to 1 decimal place in terms of percent fed (within 0.1% of
        it's value)
        """

        humans_fed_sum = (
            self.stored_food
            + self.outdoor_crops
            + self.seaweed
            + self.cell_sugar
            + self.scp
            + self.greenhouse
            + self.fish
            + self.culled_meat_plus_grazing_cattle_maintained
            + self.grazing_milk
            + self.grain_fed_meat
            + self.grain_fed_milk
            - nonhuman_consumption
        )

        return humans_fed_sum

    def print_kcals_per_capita_per_day(self, interpreted_results):
        """
        This function prints the ratio of needs to actual needs for a given scenario
        result.
        """

        needs_ratio = interpreted_results.percent_people_fed / 100

        print("Expected kcals/capita/day")
        print(needs_ratio * 2100)
        print("")

    def get_ratio_for_stored_food_and_outdoor_crops(
        self,
        outdoor_crops_plus_stored_food_rounded,
        nonhuman_consumption,
    ):
        """
        This function returns the ratio of stored food and outdoor crops that would
        be fed to humans, assuming that the rest goes to nonhuman consumption.

        It doesn't put any limit on the calories eaten by humans, technically the model
        just keeps metabolic waste at a similiar rate of waste based on the food price
        assigned, and then just continues feeding humans at their minimum macronutrient
        as high as it can.

        NOTE: outdoor_crops_plus_stored_food_rounded may not be exactly the same as
              the sum of stored food and outdoor crops, because the sum has been set
              equal to nonhuman consumption if there were rounding errors making the two
              slightly different.
        """

        remainder_to_humans = (
            outdoor_crops_plus_stored_food_rounded - nonhuman_consumption
        )

        to_humans_ratio = remainder_to_humans / outdoor_crops_plus_stored_food_rounded
        # make sure if either outdoor_crops_plus_stored_food_rounded or
        # nonhuman_consumption is zero, the other is zero

        # TODO: Reinstate?
        # outdoor_crops_plus_stored_food_rounded.ensure_other_list_zero_if_this_is_zero(
        #     other_list=nonhuman_consumption
        # )

        # remove all the places we would have had 0/0 => np.nan with 0/0 => 0
        # That's because if there's no food, nothing goes to humans, even if there's
        # no nonhuman consumption.
        to_humans_ratio = to_humans_ratio.replace_if_list_with_zeros_is_zero(
            list_with_zeros=outdoor_crops_plus_stored_food_rounded,
            replacement=0,
        )

        # We don't expect any situation where some animals are fed but no humans are!
        # check that any time outdoor_crops_plus_stored_food_rounded is zero,
        # outdoor_crops_plus_stored_food_rounded - nonhuman_consumption is also zero

        # if stored food is greater than zero, and there is some usage by animals which
        # generates fat and protein, it would make sense that ... DELETE ME

        # TODO: Reinstate?
        # remainder_to_humans.ensure_other_list_zero_if_this_is_zero(
        #     other_list=nonhuman_consumption
        # )

        difference = (
            to_humans_ratio * outdoor_crops_plus_stored_food_rounded
            + nonhuman_consumption
            - outdoor_crops_plus_stored_food_rounded
        )

        decimals = 1
        assert difference.get_rounded_to_decimal(
            decimals
        ).all_equals_zero(), """feed plus human consumption of stored food
             and outdoor crops must add up to the total outdoor crops"""

        # cannot have negative stored food and outdoor crops fed to humans
        # also ensures that there are no np.nan's left in the ratio.
        assert to_humans_ratio.all_greater_than_or_equal_to_zero()

        # cannot have more than 100% of stored food and outdoor crops fed to humans
        ratio_one = Food.ratio_one()
        assert to_humans_ratio.all_less_than_or_equal_to(ratio_one)

        return to_humans_ratio

    def get_percent_people_fed(self, humans_fed_sum):
        """
        get the minimum nutrients required to meet the needs of the population
         in any month, for kcals, fat, and protein
        """
        assert humans_fed_sum.is_units_percent()
        (min_nutrient, percent_people_fed) = humans_fed_sum.get_min_nutrient()

        PRINT_FED = True
        if PRINT_FED:

            print("Nutrients with constraining values are: " + str(min_nutrient))
            print(
                "Estimated percent people fed is "
                + str(round(percent_people_fed, 1))
                + "%"
            )
        return [percent_people_fed, min_nutrient]

    def correct_and_validate_rounding_errors(self, nonhuman_consumption):
        """
        any round error we might expect to be very small and easily fixable is corrected
        here. "small" is with respect to percent people fed

        Note: outdoor_crops, stored_food, and seaweed are the only actual outputs of
              the optimizer!
        """
        assert (
            self.stored_food.NMONTHS
            == self.outdoor_crops.NMONTHS
            == self.seaweed.NMONTHS
            == self.immediate_outdoor_crops.NMONTHS
            == self.new_stored_outdoor_crops.NMONTHS
        )

        assert self.stored_food.is_units_percent()
        assert self.seaweed.is_units_percent()
        assert self.outdoor_crops.is_units_percent()
        assert self.immediate_outdoor_crops.is_units_percent()
        assert self.new_stored_outdoor_crops.is_units_percent()

        assert nonhuman_consumption.is_units_percent()

        stored_food_rounded = self.stored_food.get_rounded_to_decimal(3)
        seaweed_rounded = self.seaweed.get_rounded_to_decimal(3)
        outdoor_crops_rounded = self.outdoor_crops.get_rounded_to_decimal(3)

        immediate_outdoor_crops_rounded = (
            self.immediate_outdoor_crops.get_rounded_to_decimal(3)
        )
        new_stored_outdoor_crops_rounded = (
            self.new_stored_outdoor_crops.get_rounded_to_decimal(3)
        )

        # if the value was a little less than zero, when rounded it would no longer be
        # less than zero.

        assert stored_food_rounded.all_greater_than_or_equal_to_zero()
        assert seaweed_rounded.all_greater_than_or_equal_to_zero()
        assert outdoor_crops_rounded.all_greater_than_or_equal_to_zero()
        assert immediate_outdoor_crops_rounded.all_greater_than_or_equal_to_zero()
        assert new_stored_outdoor_crops_rounded.all_greater_than_or_equal_to_zero()

        assert nonhuman_consumption.all_greater_than_or_equal_to_zero()

        # because all nonhuman consumption is created from stored_food and
        # outdoor_crops, we make sure nonhuman consumption is less than or equal to
        # the sum within a reasonable percent error

        outdoor_crops_plus_stored_food = self.outdoor_crops + self.stored_food

        difference_consumption_supply = (
            outdoor_crops_plus_stored_food - nonhuman_consumption
        )
        difference_consumption_supply_rounded = (
            difference_consumption_supply.get_rounded_to_decimal(1)
        )
        assert difference_consumption_supply_rounded.all_greater_than_or_equal_to_zero()

        # wherever the difference in consumption is zero, that means humand and nonhuman
        # consumption are very close in value and should be assigned to be equal to
        # prevent rounding errors later on down the line when estimating the total
        # food going to humans from all the different food sources

        outdoor_crops_plus_stored_food = (
            outdoor_crops_plus_stored_food.replace_if_list_with_zeros_is_zero(
                list_with_zeros=difference_consumption_supply_rounded,
                replacement=nonhuman_consumption,
            )
        )
        return (
            stored_food_rounded,
            seaweed_rounded,
            outdoor_crops_rounded,
            immediate_outdoor_crops_rounded,
            new_stored_outdoor_crops_rounded,
            outdoor_crops_plus_stored_food,
        )

    def get_increased_excess_to_feed(
        self,
        feed_delay,
        percent_fed,
    ):
        """
        when calculating the excess calories, the amount of human edible feed
        used can't be more than the excess calories. Because the baseline feed
        usage is higher than in nuclear winter, we don't want to increase
        feed usage before the shutoff.

        this function adds an additional amount of excess at a consistent percentage
        in the months of interest (months to calculate diet)
        """

        # these months are used to estimate the diet before the full scale-up of
        # resilient foods makes there be way too much food to make sense economically
        N_MONTHS_TO_CALCULATE_DIET = 49

        # rapidly feed more to people until it's close to 2100 kcals, then
        # slowly feed more to people
        SMALL_INCREASE_IN_EXCESS = 0.1
        LARGE_INCREASE_IN_EXCESS = 1.0

        excess_per_month_percent = self.excess_feed.kcals

        baseline_feed = excess_per_month_percent[:feed_delay]

        part_at_end_to_leave_unchanged = excess_per_month_percent[
            N_MONTHS_TO_CALCULATE_DIET:
        ]

        after_shutoff_feed = excess_per_month_percent[
            feed_delay:N_MONTHS_TO_CALCULATE_DIET
        ]

        if percent_fed < 106 and percent_fed > 100:

            additional_excess_to_add_percent = np.linspace(
                SMALL_INCREASE_IN_EXCESS,
                SMALL_INCREASE_IN_EXCESS,
                N_MONTHS_TO_CALCULATE_DIET - feed_delay,
            )
        else:
            additional_excess_to_add_percent = np.linspace(
                LARGE_INCREASE_IN_EXCESS,
                LARGE_INCREASE_IN_EXCESS,
                N_MONTHS_TO_CALCULATE_DIET - feed_delay,
            )

        assert len(additional_excess_to_add_percent) == len(after_shutoff_feed)

        # don't add any additional feed before the shutoff, that's already at
        # baseline feed levels
        new_excess_kcals = after_shutoff_feed + additional_excess_to_add_percent

        excess_per_month = np.append(
            np.append(baseline_feed, new_excess_kcals),
            part_at_end_to_leave_unchanged,
        )

        # kcals per month, units percent
        return excess_per_month
