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
        """
        analysis.calc_fraction_outdoor_crops_stored_food_to_humans(
            model,
            variables["crops_food_eaten_no_rotation"],
            variables["crops_food_eaten_with_rotation"],
            variables["stored_food_eaten"],
        )

        [
            optimizer_fed_sum,
            stored_food,
            seaweed,
            outdoor_crops,
            immediate_outdoor_crops,
            new_stored_outdoor_crops,
        ] = self.get_sum_and_stored_food_and_outdoor_crops_percents(extracted_results)

        nonhuman_consumption = multi_valued_constants[
            "nonhuman_consumption"
        ].in_units_percent_fed()

        # rounding errors can be introduced by the optimizer. We correct them here.
        (
            stored_food,
            seaweed,
            outdoor_crops,
            immediate_outdoor_crops,
            new_stored_outdoor_crops,
            outdoor_crops_plus_stored_food_rounded,
        ) = self.correct_and_validate_rounding_errors(
            stored_food,
            seaweed,
            outdoor_crops,
            immediate_outdoor_crops,
            new_stored_outdoor_crops,
            nonhuman_consumption,
        )

        (
            self.percent_people_fed,
            self.constraining_nutrient,
        ) = self.get_percent_people_fed(optimizer_fed_sum)

        # get the ratio for stored_food and outdoor_crops (after subtracting feed and
        # biofuels)
        to_humans_ratio = self.get_ratio_for_stored_food_and_outdoor_crops(
            stored_food,
            outdoor_crops,
            nonhuman_consumption,
            outdoor_crops_plus_stored_food_rounded,
        )

        # apply the reduction to stored food and outdoor crops
        self.stored_food_fed_to_humans = to_humans_ratio * extracted_results.stored_food
        self.outdoor_crops_fed_to_humans = (
            to_humans_ratio * extracted_results.outdoor_crops
        )

        # NOTE: immediate and new used may be slightly different than the outdoor
        #       crops due to rounding errors

        # used for plotting immediate vs food stored in the scenario
        self.immediate_outdoor_crops_fed_to_humans = (
            to_humans_ratio * extracted_results.immediate_outdoor_crops
        )

        # used for plotting immediate vs food stored in the scenario
        self.new_stored_outdoor_crops_fed_to_humans = (
            to_humans_ratio * extracted_results.new_stored_outdoor_crops
        )

        return self

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

    def get_sum_and_stored_food_and_outdoor_crops_percents(self, extracted_results):
        """
        sum the resulting nutrients from the extracted_results
        """

        optimizer_fed_sum = (
            extracted_results.stored_food
            + extracted_results.outdoor_crops
            + extracted_results.meat
            + extracted_results.seaweed
            + extracted_results.milk
            + extracted_results.cell_sugar
            + extracted_results.scp
            + extracted_results.greenhouse
            + extracted_results.fish
            + extracted_results.h_e_meat
            + extracted_results.h_e_milk
        )

        stored_food = extracted_results.stored_food.in_units_percent_fed()
        outdoor_crops = extracted_results.outdoor_crops.in_units_percent_fed()
        meat = extracted_results.meat.in_units_percent_fed()
        seaweed = extracted_results.seaweed.in_units_percent_fed()
        milk = extracted_results.milk.in_units_percent_fed()
        cell_sugar = extracted_results.cell_sugar.in_units_percent_fed()
        scp = extracted_results.scp.in_units_percent_fed()
        greenhouse = extracted_results.greenhouse.in_units_percent_fed()
        fish = extracted_results.fish.in_units_percent_fed()
        h_e_meat = extracted_results.h_e_meat.in_units_percent_fed()
        h_e_milk = extracted_results.h_e_milk.in_units_percent_fed()

        immediate_outdoor_crops = (
            extracted_results.immediate_outdoor_crops.in_units_percent_fed()
        )
        new_stored_outdoor_crops = (
            extracted_results.new_stored_outdoor_crops.in_units_percent_fed()
        )

        optimizer_fed_sum = (
            stored_food
            + outdoor_crops
            + meat
            + seaweed
            + milk
            + cell_sugar
            + scp
            + greenhouse
            + fish
            + h_e_meat
            + h_e_milk
        )

        return [
            optimizer_fed_sum,
            stored_food,
            seaweed,
            outdoor_crops,
            immediate_outdoor_crops,
            new_stored_outdoor_crops,
        ]

    def calc_fraction_outdoor_crops_stored_food_to_humans(
        self,
        model,
        crops_food_eaten_no_rotation,
        crops_food_eaten_with_rotation,
        stored_food_eaten,
        excess_calories,
        excess_fat_used,
        excess_protein_used,
    ):

        # it seems impossible for there to be more fat used for feed than actually produced from all the sources, if the optimizer spits out a positive number of people fed in terms of fat.
        # The estimate for amount used for feed divides the excess by all the sources (except human edible feed). If the excess is greater than the sources, we have a problem.
        # The sources actually added to get humans_fed_fat, does however include the excess as a negative number. The excess is added to humans_fat_fed to cancel this. Also, humans_fed_fat includes meat and milk from human edible.
        # So the only reason it doesnt actually go negative is because the optimizer takes an optimization including the human edible fat which pushes it to some positive balance of people fed in terms of fat.
        # So its not impossible, it just means that the part of the excess which required more fat had to come from the animal outputs themselves.
        # By adding a requirement that the fat, calories and protein need to be satisfied before human edible produce meat is taken into account we will have 100% of resources spent on meeting these requirements and 0% going to humans. The optimizer will still
        print("excess_fat_used")
        print(excess_fat_used)
        print(
            "(np.array(outdoor_crops_fat) + np.array(stored_food_fat)) * self.constants[FAT_MONTHLY] * 1e9"
        )
        print(
            (np.array(outdoor_crops_fat) + np.array(stored_food_fat))
            * self.constants["FAT_MONTHLY"]
            * 1e9
        )
        outdoor_crops_stored_food_fraction_fat_to_feed = np.divide(
            excess_fat_used,
            (np.array(outdoor_crops_fat) + np.array(stored_food_fat))
            * self.constants["FAT_MONTHLY"]
            * 1e9,
        )

        outdoor_crops_stored_food_fraction_fat_to_feed = np.where(
            total_production == 0, 0, outdoor_crops_stored_food_fraction_fat_to_feed
        )

        outdoor_crops_stored_food_fraction_fat_to_humans = (
            1 - outdoor_crops_stored_food_fraction_fat_to_feed
        )

        if (outdoor_crops_stored_food_fraction_fat_to_humans < 0).any():
            assert (outdoor_crops_stored_food_fraction_fat_to_humans > -1e-6).all()
            outdoor_crops_stored_food_fraction_fat_to_humans = np.where(
                np.array(outdoor_crops_stored_food_fraction_fat_to_humans) < 0,
                0,
                np.array(outdoor_crops_stored_food_fraction_fat_to_humans),
            )
        print("outdoor_crops_stored_food_fraction_fat_to_humans")
        print(outdoor_crops_stored_food_fraction_fat_to_humans)
        outdoor_crops_stored_food_fraction_protein_to_feed = np.divide(
            excess_protein_used,
            (np.array(outdoor_crops_protein) + np.array(stored_food_protein))
            * self.constants["PROTEIN_MONTHLY"]
            * 1e9,
        )
        outdoor_crops_stored_food_fraction_protein_to_feed = np.where(
            total_production == 0, 0, outdoor_crops_stored_food_fraction_protein_to_feed
        )

        outdoor_crops_stored_food_fraction_protein_to_humans = (
            1 - outdoor_crops_stored_food_fraction_protein_to_feed
        )

        FEED_NAN = np.isnan(outdoor_crops_stored_food_fraction_kcals_to_feed).any()

        MORE_THAN_AVAILABLE_USED_FOR_FEED = not (
            outdoor_crops_stored_food_fraction_kcals_to_feed <= 1 + 1e-5
        ).all()

        NEGATIVE_FRACTION_FEED = not (
            outdoor_crops_stored_food_fraction_kcals_to_feed >= 0
        ).all()

        if FEED_NAN:
            print("ERROR: Feed not a number")
            quit()

        if MORE_THAN_AVAILABLE_USED_FOR_FEED:
            print("")
            print(
                "ERROR: Attempted to feed more food to animals than exists available outdoor growing fat, calories, or protein. Scenario is impossible."
            )
            quit()

        if NEGATIVE_FRACTION_FEED:
            print("ERROR: fraction feed to humans is negative")
            quit()

        assert (outdoor_crops_stored_food_fraction_kcals_to_feed <= 1 + 1e-5).all()

        if (outdoor_crops_stored_food_fraction_kcals_to_feed >= 1).any():
            outdoor_crops_stored_food_fraction_kcals_to_humans[
                outdoor_crops_stored_food_fraction_kcals_to_feed >= 1
            ] = 0

        assert (outdoor_crops_stored_food_fraction_kcals_to_feed >= 0).all()
        if self.constants["inputs"]["INCLUDE_FAT"]:
            assert (outdoor_crops_stored_food_fraction_fat_to_feed <= 1 + 1e-5).all()
            assert (outdoor_crops_stored_food_fraction_fat_to_feed >= 0).all()
        if self.constants["inputs"]["INCLUDE_PROTEIN"]:
            assert (
                outdoor_crops_stored_food_fraction_protein_to_feed <= 1 + 1e-5
            ).all()
            assert (outdoor_crops_stored_food_fraction_protein_to_feed >= 0).all()

    def get_crop_produced_monthly(self):
        """
        get the crop produced monthly, rather than the amount eaten
        incorporates rotations
        """
        og_produced_kcals = np.concatenate(
            [
                np.array(
                    crops_food_produced[
                        0 : self.constants["inputs"][
                            "INITIAL`HARVEST_DURATION_IN_MONTHS"
                        ]
                    ]
                ),
                np.array(
                    crops_food_produced[
                        self.constants["inputs"]["INITIAL_HARVEST_DURATION_IN_MONTHS"] :
                    ]
                )
                * self.constants["OG_ROTATION_FRACTION_KCALS"],
            ]
        )

        self.billions_fed_outdoor_crops_produced_fat = (
            np.concatenate(
                [
                    np.array(
                        crops_food_produced[
                            0 : self.constants["inputs"][
                                "INITIAL_HARVEST_DURATION_IN_MONTHS"
                            ]
                        ]
                    )
                    * self.constants["OG_FRACTION_FAT"],
                    np.array(
                        crops_food_produced[
                            self.constants["inputs"][
                                "INITIAL_HARVEST_DURATION_IN_MONTHS"
                            ] :
                        ]
                    )
                    * self.constants["OG_ROTATION_FRACTION_FAT"],
                ]
            )
            / self.constants["FAT_MONTHLY"]
            / 1e9
        )

        self.billions_fed_outdoor_crops_produced_protein = (
            np.concatenate(
                [
                    np.array(
                        crops_food_produced[
                            0 : self.constants["inputs"][
                                "INITIAL_HARVEST_DURATION_IN_MONTHS"
                            ]
                        ]
                    )
                    * self.constants["OG_FRACTION_PROTEIN"],
                    np.array(
                        crops_food_produced[
                            self.constants["inputs"][
                                "INITIAL_HARVEST_DURATION_IN_MONTHS"
                            ] :
                        ]
                    )
                    * self.constants["OG_ROTATION_FRACTION_PROTEIN"],
                ]
            )
            / self.constants["PROTEIN_MONTHLY"]
            / 1e9
        )

        self.outdoor_crops_produced = Food(
            kcals=self.billions_fed_outdoor_crops_produced_kcals,
            fat=self.billions_fed_outdoor_crops_produced_fat,
            protein=self.billions_fed_outdoor_crops_produced_protein,
            kcals_units="billion people fed each month",
            fat_units="billion people fed each month",
            protein_units="billion people fed each month",
        )

        self.billions_fed_outdoor_crops_produced_kcals = np.multiply(
            og_produced_kcals / self.constants["KCALS_MONTHLY"],
            self.outdoor_crops_stored_food_fraction_kcals_to_humans,
        )
        self.billions_fed_outdoor_crops_produced_fat = np.multiply(
            self.billions_fed_outdoor_crops_produced_fat,
            self.outdoor_crops_stored_food_fraction_fat_to_humans,
        )

        self.billions_fed_outdoor_crops_produced_protein = np.multiply(
            self.billions_fed_outdoor_crops_produced_protein,
            self.outdoor_crops_stored_food_fraction_protein_to_humans,
        )

    def correct_and_validate_rounding_errors(
        self,
        stored_food,
        seaweed,
        outdoor_crops,
        immediate_outdoor_crops,
        new_stored_outdoor_crops,
        nonhuman_consumption,
    ):
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

        assert stored_food.is_units_percent()
        assert seaweed.is_units_percent()
        assert outdoor_crops.is_units_percent()
        assert immediate_outdoor_crops.is_units_percent()
        assert new_stored_outdoor_crops.is_units_percent()

        assert nonhuman_consumption.is_units_percent()

        stored_food_rounded = stored_food.get_rounded_to_decimal(1)
        seaweed_rounded = seaweed.get_rounded_to_decimal(1)
        outdoor_crops_rounded = outdoor_crops.get_rounded_to_decimal(1)
        immediate_outdoor_crops_rounded = (
            immediate_outdoor_crops.get_rounded_to_decimal(1)
        )
        new_stored_outdoor_crops_rounded = (
            new_stored_outdoor_crops.get_rounded_to_decimal(1)
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
