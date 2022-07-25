#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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

from pandas import options
from pandas.core.algorithms import extract_array

module_path = os.path.abspath(os.path.join("../.."))
if module_path not in sys.path:
    sys.path.append(module_path)

# TODO: DELETE ME WITHOUT REMORSE
# strand 2 : optimizer fed sum works?


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

        In no other function is anything assigned to "self" (other than functions)
        """

        # NOTE: this long function is like this because I wanted to be really
        # obvious what was being assigned in this class and to put it right at the top.

        self.stored_food = extracted_results.stored_food.in_units_percent_fed()

        self.outdoor_crops = extracted_results.outdoor_crops.in_units_percent_fed()

        self.seaweed = extracted_results.seaweed.in_units_percent_fed()

        self.cell_sugar = extracted_results.cell_sugar.in_units_percent_fed()

        self.scp = extracted_results.scp.in_units_percent_fed()

        self.greenhouse = extracted_results.greenhouse.in_units_percent_fed()

        self.fish = extracted_results.fish.in_units_percent_fed()

        self.meat_culled_plus_grazing_cattle_maintained = (
            extracted_results.meat_culled_plus_grazing_cattle_maintained.in_units_percent_fed()
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

        nonhuman_consumption = multi_valued_constants[
            "nonhuman_consumption"
        ].in_units_percent_fed()

        optimizer_fed_sum = self.get_sum_by_subtracting_nonhuman(nonhuman_consumption)

        (
            self.percent_people_fed,
            self.constraining_nutrient,
        ) = self.get_percent_people_fed(optimizer_fed_sum)

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
            self.outdoor_crops_plus_stored_food_rounded,
        ) = self.correct_and_validate_rounding_errors(nonhuman_consumption)

        # get the ratio for stored_food_rounded and outdoor_crops (after subtracting
        # feed and biofuels)
        to_humans_ratio = self.get_ratio_for_stored_food_and_outdoor_crops(
            self.stored_food_rounded,
            self.outdoor_crops_rounded,
            self.outdoor_crops_plus_stored_food_rounded,
            nonhuman_consumption,
        )

        # TODO: git diff on the import scripts to be sure nothing WONKY is going on

        # TODO: delete this printout
        print("to_humans_ratio")
        print(to_humans_ratio)

        (
            self.stored_food_fed_to_humans,
            self.outdoor_crops_fed_to_humans,
            self.immediate_outdoor_crops_fed_to_humans,
            self.new_stored_outdoor_crops_fed_to_humans,
        ) = self.get_amount_fed_to_humans(
            self.stored_food_rounded,
            self.outdoor_crops_rounded,
            self.immediate_outdoor_crops_rounded,
            self.new_stored_outdoor_crops_rounded,
            to_humans_ratio,
        )

        assert self.get_sum_by_adding_to_humans() == optimizer_fed_sum

        return self

    def get_amount_fed_to_humans(
        self,
        stored_food_rounded,
        outdoor_crops_rounded,
        immediate_outdoor_crops_rounded,
        new_stored_outdoor_crops_rounded,
        to_humans_ratio,
    ):

        # apply the reduction to stored food and outdoor crops
        stored_food_fed_to_humans = to_humans_ratio * stored_food_rounded
        outdoor_crops_fed_to_humans = to_humans_ratio * outdoor_crops_rounded

        # NOTE: immediate and new used may be slightly different than the outdoor
        #       crops due to rounding errors

        # used for plotting immediate vs food stored in the scenario
        immediate_outdoor_crops_fed_to_humans = (
            to_humans_ratio * immediate_outdoor_crops_rounded
        )

        # used for plotting immediate vs food stored in the scenario
        new_stored_outdoor_crops_fed_to_humans = (
            to_humans_ratio * new_stored_outdoor_crops_rounded
        )

        return (
            stored_food_fed_to_humans,
            outdoor_crops_fed_to_humans,
            immediate_outdoor_crops_fed_to_humans,
            new_stored_outdoor_crops_fed_to_humans,
        )

    def get_sum_by_adding_to_humans(self):
        """
        sum the resulting nutrients from the extracted_results, but subtract nonhuman
        to get the ratio

        also rounds result to 1 decimal place in terms of percent fed (within 0.1% of
        it's value)
        """

        to_humans_fed_sum = (
            self.stored_food_fed_to_humans
            + self.outdoor_crops_fed_to_humans
            + self.seaweed
            + self.cell_sugar
            + self.scp
            + self.greenhouse
            + self.fish
            + self.meat_culled_plus_grazing_cattle_maintained
            + self.grazing_milk
            + self.grain_fed_meat
            + self.grain_fed_milk
        )

        return to_humans_fed_sum.get_rounded_to_decimal(decimals=1)

    def get_sum_by_subtracting_nonhuman(self, nonhuman_consumption):
        """
        sum the resulting nutrients from the extracted_results, but do this by adding
        all the amounts determined to go to humans

        also rounds result to 1 decimal place in terms of percent fed (within 0.1% of
        it's value)
        """

        optimizer_fed_sum = (
            self.stored_food
            + self.outdoor_crops
            + self.seaweed
            + self.cell_sugar
            + self.scp
            + self.greenhouse
            + self.fish
            + self.meat_culled_plus_grazing_cattle_maintained
            + self.grazing_milk
            + self.grain_fed_meat
            + self.grain_fed_milk
            - nonhuman_consumption
        )

        return optimizer_fed_sum.get_rounded_to_decimal(decimals=1)

    def print_kcals_per_capita_per_day(self, interpreted_results):
        """
        This function prints the ratio of needs to actual needs for a given scenario
        result.
        """

        needs_ratio = interpreted_results.percent_people_fed.kcals / 100

        print("No trade expected kcals/capita/day 2020")
        print(needs_ratio * 2100)
        print("")

    def get_ratio_for_stored_food_and_outdoor_crops(
        self,
        stored_food,
        outdoor_crops,
        outdoor_crops_plus_stored_food_rounded,
        nonhuman_consumption,
    ):
        """
        This function returns the ratio of stored food and outdoor crops that would
        be fed to humans, assuming that the rest goes to nonhuman consumption

        NOTE: outdoor_crops_plus_stored_food_rounded may not be exactly the same as
              the sum of stored food and outdoor crops, because the sum has been set
              equal to nonhuman consumption if there were rounding errors making the two
              slightly different.
        """
        remainder_to_humans = (
            outdoor_crops_plus_stored_food_rounded - nonhuman_consumption
        )

        to_humans_ratio = remainder_to_humans / outdoor_crops_plus_stored_food_rounded

        to_humans_ratio.set_units(
            kcals_units="ratio each month",
            fat_units="ratio each month",
            protein_units="ratio each month",
        )

        # make sure if either outdoor_crops_plus_stored_food_rounded or
        # nonhuman_consumption is zero, the other is zero

        outdoor_crops_plus_stored_food_rounded.ensure_other_list_zero_if_this_is_zero(
            other_list=nonhuman_consumption
        )

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
        remainder_to_humans.make_sure_other_list_zero_if_this_is_zero(
            other_list=nonhuman_consumption
        )

        # feed plus human consumption of stored food and outdoor crops adds up to the
        # total outdoor crops
        assert (
            to_humans_ratio * outdoor_crops_plus_stored_food_rounded
            + nonhuman_consumption
            == outdoor_crops_plus_stored_food_rounded
        )

        # cannot have negative stored food and outdoor crops fed to humans
        # also ensures that there are no np.nan's left in the ratio.
        assert to_humans_ratio.all_greater_than_or_equal_to_zero()

        # cannot have more than 100% of stored food and outdoor crops fed to humans
        ratio_one = Food.ratio_one()
        assert to_humans_ratio.all_less_than_or_equal_to(ratio_one)

        return to_humans_ratio

    def get_percent_people_fed(self, optimizer_fed_sum):
        """
        get the minimum nutrients required to meet the needs of the population in any month, for kcals, fat, and protein
        """
        fed_as_string = str("result of scenario\n") + str(optimizer_fed_sum)
        (min_nutrient, percent_people_fed) = optimizer_fed_sum.min_nutrient()

        PRINT_FED = True
        if PRINT_FED:
            print(fed_as_string)

            print("Nutrients with constraining values are: " + str(min_nutrient))
            print("Estimated percent people fed is " + str(percent_people_fed) + "%")
        return [percent_people_fed, min_nutrient]

    def correct_and_validate_rounding_errors(self, nonhuman_consumption):
        """
        any round error we might expect to be very small and easily fixable is corrected
        here. "small" is with respect to percent people fed

        Note: outdoor_crops, stored_food, and seaweed are the only actual outputs of
              the optimizer!
        """
        assert (
            stored_food.NMONTHS
            == outdoor_crops.NMONTHS
            == seaweed.NMONTHS
            == immediate_outdoor_crops.NMONTHS
            == new_stored_outdoor_crops.NMONTHS
        )

        assert self.stored_food.is_units_percent()
        assert self.seaweed.is_units_percent()
        assert self.outdoor_crops.is_units_percent()
        assert self.immediate_outdoor_crops.is_units_percent()
        assert self.new_stored_outdoor_crops.is_units_percent()

        assert nonhuman_consumption.is_units_percent()

        stored_food_rounded = self.stored_food.get_rounded_to_decimal(1)
        seaweed_rounded = self.seaweed.get_rounded_to_decimal(1)
        outdoor_crops_rounded = self.outdoor_crops.get_rounded_to_decimal(1)
        immediate_outdoor_crops_rounded = (
            self.immediate_outdoor_crops.get_rounded_to_decimal(1)
        )
        new_stored_outdoor_crops_rounded = (
            self.new_stored_outdoor_crops.get_rounded_to_decimal(1)
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

        outdoor_crops_plus_stored_food_rounded = (
            outdoor_crops_rounded + stored_food_rounded
        )

        difference_consumption_supply = (
            outdoor_crops_plus_stored_food_rounded - nonhuman_consumption
        )

        difference_consumption_supply_rounded = (
            difference_consumption_supply.get_rounded_to_decimal(1)
        )

        assert difference_consumption_supply_rounded.all_greater_than_or_equal_to_zero()

        # wherever the difference in consumption is zero, that means humand and nonhuman
        # consumption are very close in value and should be assigned to be equal to
        # prevent rounding errors later on down the line when estimating the total
        # food going to humans from all the different food sources

        outdoor_crops_plus_stored_food_rounded = (
            outdoor_crops_plus_stored_food_rounded.replace_if_list_with_zeros_is_zero(
                list_with_zeros=difference_consumption_supply_rounded,
                replacement=nonhuman_consumption,
            )
        )

        return (
            stored_food,
            seaweed,
            outdoor_crops,
            immediate_outdoor_crops,
            new_stored_outdoor_crops,
            outdoor_crops_plus_stored_food_rounded,
        )
