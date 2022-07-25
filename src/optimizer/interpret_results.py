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

from src.food_system.food import Food


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
        self.assign_kcals_effective_from_extractor(extracted_results)

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

        return self

    def assign_percent_fed_from_extractor(self, extracted_results):

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

    def assign_kcals_effective_from_extractor(self, extracted_results):

        self.stored_food_kcals_eff = extracted_results.stored_food.in_units_kcals_eff()

        self.outdoor_crops_kcals_eff = (
            extracted_results.outdoor_crops.in_units_kcals_eff()
        )

        self.seaweed_kcals_eff = extracted_results.seaweed.in_units_kcals_eff()

        self.cell_sugar_kcals_eff = extracted_results.cell_sugar.in_units_kcals_eff()

        self.scp_kcals_eff = extracted_results.scp.in_units_kcals_eff()

        self.greenhouse_kcals_eff = extracted_results.greenhouse.in_units_kcals_eff()

        self.fish_kcals_eff = extracted_results.fish.in_units_kcals_eff()

        self.meat_culled_plus_grazing_cattle_maintained_kcals_eff = (
            extracted_results.meat_culled_plus_grazing_cattle_maintained.in_units_kcals_eff()
        )

        self.grazing_milk_kcals_eff = (
            extracted_results.grazing_milk.in_units_kcals_eff()
        )

        self.grain_fed_meat_kcals_eff = (
            extracted_results.grain_fed_meat.in_units_kcals_eff()
        )

        self.grain_fed_milk_kcals_eff = (
            extracted_results.grain_fed_milk.in_units_kcals_eff()
        )

        self.immediate_outdoor_crops_kcals_eff = (
            extracted_results.immediate_outdoor_crops.in_units_kcals_eff()
        )

        self.new_stored_outdoor_crops_kcals_eff = (
            extracted_results.new_stored_outdoor_crops.in_units_kcals_eff()
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
            self.stored_food_rounded,
            self.outdoor_crops_rounded,
            self.outdoor_crops_plus_stored_food,
            self.nonhuman_consumption_percent,
        )

        # TODO: delete this printout
        print("to_humans_ratio")
        print(to_humans_ratio)

        (
            self.stored_food_fed_to_humans,
            self.outdoor_crops_fed_to_humans,
            self.immediate_outdoor_crops_fed_to_humans,
            self.new_stored_outdoor_crops_fed_to_humans,
        ) = self.get_amount_fed_to_humans(
            self.stored_food,
            self.outdoor_crops,
            self.immediate_outdoor_crops,
            self.new_stored_outdoor_crops,
            to_humans_ratio,
        )

        print("humans_fed_sum")
        print(humans_fed_sum)
        self.kcals_fed = humans_fed_sum.kcals
        self.fat_fed = humans_fed_sum.kcals
        self.protein_fed = humans_fed_sum.kcals

        print("self.get_sum_by_adding_to_humans")
        print(self.get_sum_by_adding_to_humans())

        difference = humans_fed_sum - self.get_sum_by_adding_to_humans()

        # checking that the two ways of adding up food to humans match
        assert difference.get_rounded_to_decimal(decimals=1).all_equals_zero()

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

        return to_humans_fed_sum

    def get_sum_by_subtracting_nonhuman(self, nonhuman_consumption):
        """
        sum the resulting nutrients from the extracted_results, but do this by adding
        all the amounts determined to go to humans

        also rounds result to 1 decimal place in terms of percent fed (within 0.1% of
        it's value)
        """
        print("self.stored_food")
        print(self.stored_food.get_units())
        print("")
        print("self.outdoor_crops")
        print(self.outdoor_crops.get_units())
        print("")
        print("self.seaweed")
        print(self.seaweed.get_units())
        print("")
        print("self.cell_sugar")
        print(self.cell_sugar.get_units())
        print("")
        print("self.scp")
        print(self.scp.get_units())
        print("")
        print("self.greenhouse")
        print(self.greenhouse.get_units())
        print("")
        print("self.fish")
        print(self.fish.get_units())
        print("")
        print("self.meat_culled_plus_grazing_cattle_maintained")
        print(self.meat_culled_plus_grazing_cattle_maintained.get_units())
        print("")
        print("self.grazing_milk")
        print(self.grazing_milk.get_units())
        print("")
        print("self.grain_fed_meat")
        print(self.grain_fed_meat.get_units())
        print("")
        print("self.grain_fed_milk")
        print(self.grain_fed_milk.get_units())
        print("")
        print("nonhuman_consumption")
        print(nonhuman_consumption.get_units())
        print("")

        humans_fed_sum = (
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

        return humans_fed_sum

    def print_kcals_per_capita_per_day(self, interpreted_results):
        """
        This function prints the ratio of needs to actual needs for a given scenario
        result.
        """

        needs_ratio = interpreted_results.percent_people_fed / 100

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

        print("to_humans_ratio")
        print(to_humans_ratio)

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
        remainder_to_humans.ensure_other_list_zero_if_this_is_zero(
            other_list=nonhuman_consumption
        )

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
        get the minimum nutrients required to meet the needs of the population in any month, for kcals, fat, and protein
        """
        fed_as_string = str("result of scenario\n") + str(humans_fed_sum)

        assert humans_fed_sum.is_units_percent()

        (min_nutrient, percent_people_fed) = humans_fed_sum.get_min_nutrient()

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
            difference_consumption_supply.get_rounded_to_decimal(3)
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
