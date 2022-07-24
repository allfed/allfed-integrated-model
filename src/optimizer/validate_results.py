################################# Validator ###################################
##                                                                            #
##            Checks that the optimizer successfully optimized.               #
##        To do this, it makes sure that the constraints given are            #
##            all satisfied within an acceptable margin of error              #
##                                                                            #
###############################################################################


import os
import sys

module_path = os.path.abspath(os.path.join("../.."))
if module_path not in sys.path:
    sys.path.append(module_path)

import matplotlib.pyplot as plt
import numpy as np


class Validator:
    def __init__(self):
        pass

    def validate_optimization(self, model):
        """
        validate things directly from the optimizer, including
        """
        self.ensure_food_to_humans_plus_food_to_other_equals_total_food(interpreter)

    def validate_interpretation(self, model, interpreter):

        self.ensure_optimizer_returns_same_as_sum_nutrients(model, interpreter)

        new_stored = interpreter.new_stored_outdoor_crops
        immediate = interpreter.immediate_outdoor_crops
        outdoor_crops = interpreter.outdoor_crops_outdoor_crops
        stored_food = interpreter.stored_food_outdoor_crops

        self.ensure_consumption_zero_if_stored_food_plus_outdoor_crops_zero(
            stored_food_plus_outdoor_crops, nonhuman_consumption
        )

        self.YES_THIS_ONE_PROBABLY_DOES_SOMETHING_USEFUL_question_mark()

        (
            kcals_total_from_optimizer,
            fat_total_from_optimizer,
            protein_total_from_optimizer,
        ) = interpreter.get_objective_optimization_results(
            model,
        )

        self.not_REALLY_sure_AT_ALL_what_THIS_one_DOES_lol(
            kcals_total_from_optimizer,
            fat_total_from_optimizer,
            protein_total_from_optimizer,
        )

        self.ensure_immediate_and_new_stored_add_correctly_to_sources(
            immediate, new_stored, outdoor_crops, stored_food
        )

    def check_constraints_satisfied(self, model, maximize_constraints, variables):
        """
        passing in the variables explicitly to the constraint checker here
        ensures that the final values that are used in reports are explicitly
        validated against all the constraints.

        NOTE: THIS FUNCTION TAKES A REALLY, REALLY LONG TIME SO IT'S RUN INFREQUENTLY
        """
        SHOW_CONSTRAINT_CHECK = False
        constraints_dict = {}
        for c in variables:
            if SHOW_CONSTRAINT_CHECK:
                print(c)
            if type(c) == type([]):
                print("list")
                continue
            if c.name in maximize_constraints:
                continue
            constraints_dict[c.name] = c.varValue
        differences = []
        constraintlist = list(model.constraints.items())
        for constraint in constraintlist:

            if constraint[0] in maximize_constraints:
                differences.append(0)
                continue
            compare_type = 0

            splitted = str(constraint[1]).split(" = ")
            if len(splitted) < 2:
                compare_type = 1
                splitted = str(constraint[1]).split(" <= ")
                if len(splitted) < 2:
                    compare_type = 2
                    splitted = str(constraint[1]).split(" >= ")
                    if len(splitted) < 2:
                        print("Error! Assignment is not ==, <=, or >=")
                        quit()
                # splitted=str(constraint[1]).split(' >= ')
            variable_string = splitted[0]
            equation_string = splitted[1]

            for var in model.variables():
                equation_string = equation_string.replace(
                    var.name, str(constraints_dict[var.name])
                )
                variable_string = variable_string.replace(
                    var.name, str(constraints_dict[var.name])
                )
            eq_val = eval(equation_string)
            var_val = eval(variable_string)

            if SHOW_CONSTRAINT_CHECK:
                print(
                    "checking constraint "
                    + str(constraint[0])
                    + " has "
                    + str(constraint[1])
                )
            if compare_type == 0:
                if SHOW_CONSTRAINT_CHECK:
                    print("difference" + str(abs(eq_val - var_val)))

                assert abs(eq_val - var_val) < 1
                differences.append(abs(eq_val - var_val))
            if compare_type == 1:
                assert var_val - eq_val <= 1
                differences.append(var_val - eq_val)
            if compare_type == 2:
                assert eq_val - var_val <= 1
                differences.append(eq_val - var_val)

        print("all constraints satisfied")
        m = max(differences)
        print("biggest difference:" + str(m))
        max_index = np.where(np.array(differences) == m)[0][0]
        print("for constraint:")
        print(constraintlist[max_index])

    def not_REALLY_sure_AT_ALL_what_THIS_one_DOES_lol(self):

        population_billions = self.constants["inputs"]["POP"] / 1e9

        # convert from billions fed to percentage fed to reduce rounding errors
        kcals_fed_percent = 100 * (self.kcals_fed / population_billions)
        humans_fed_kcals_optimizer_percent = 100 * (
            np.array(self.humans_fed_kcals_optimizer) / population_billions
        )

        assert (
            abs(
                np.divide(
                    kcals_fed_percent - np.array(humans_fed_kcals_optimizer_percent),
                    kcals_fed_percent,
                )
            )
            < 1e-6
        ).all()
        if self.constants["inputs"]["INCLUDE_FAT"]:
            # convert from billions fed to percentage fed to reduce rounding errors
            fat_fed_percent = 100 * (self.fat_fed / population_billions)
            humans_fed_fat_optimizer_percent = 100 * (
                np.array(self.humans_fed_fat_optimizer) / population_billions
            )

            assert (
                abs(
                    np.divide(
                        fat_fed_percent - np.array(humans_fed_fat_optimizer_percent),
                        fat_fed_percent,
                    )
                )
                < 1e-6
            ).all()

        if self.constants["inputs"]["INCLUDE_PROTEIN"]:
            # convert from billions fed to percentage fed to reduce rounding errors
            protein_fed_percent = 100 * (self.protein_fed / population_billions)
            humans_fed_protein_optimizer_percent = 100 * (
                np.array(self.humans_fed_protein_optimizer) / population_billions
            )

            assert (
                abs(
                    np.divide(
                        protein_fed_percent
                        - np.array(humans_fed_protein_optimizer_percent),
                        protein_fed_percent,
                    )
                )
                < 1e-6
            ).all()

        stored_food_outdoor_crops_kcals = np.array(
            self.billions_fed_stored_food_kcals
        ) + np.array(self.billions_fed_outdoor_crops_kcals)
        stored_food_outdoor_crops_fat = np.array(
            self.billions_fed_stored_food_fat
        ) + np.array(self.billions_fed_outdoor_crops_fat)
        stored_food_outdoor_crops_protein = np.array(
            self.billions_fed_stored_food_protein
        ) + np.array(self.billions_fed_outdoor_crops_protein)

        # if it takes all the available ag production to produce minimum for biofuel and animal feed demands
        division = []

        for zipped_lists in zip(
            stored_food_outdoor_crops_kcals,
            self.outdoor_crops_stored_food_fraction_kcals_to_humans,
            self.excess,
        ):

            if zipped_lists[1] <= 0:
                assert zipped_lists[0] >= -1e-5
                division.append(zipped_lists[2] / self.constants["KCALS_MONTHLY"])
            else:
                division.append(zipped_lists[0] / zipped_lists[1])

        # stored_food_outdoor_crops_kcals =

        # a-b==a*c
        # if a==b,c == 0
        # if b>a, we don't have enough stored food and outdoor_crops to produced food, and should quit.
        # This may happen even if there is plenty of food to go around, because the stored food needs to
        # If we optimize such that stored food is used in one part while culled meat is used in another, and that generates excess calories above world demand

        denominator = (
            stored_food_outdoor_crops_kcals
            + self.billions_fed_h_e_meat_kcals
            + self.billions_fed_h_e_milk_kcals
        )

        fractional_difference = np.divide(
            (
                stored_food_outdoor_crops_kcals
                + self.billions_fed_h_e_meat_kcals
                + self.billions_fed_h_e_milk_kcals
            )
            - (np.array(division) + self.billions_fed_h_e_balance.kcals),
            denominator,
        )

        # stored_food_outdoor_crops_kcals + MEAT_MILK_H_E
        # ==
        # THING + MEAT_MILK_H_E - BIOFUELS_KCALS - FEED_KCALS
        #
        # simplify by subrtaction of input parameter:
        #
        # stored_food_outdoor_crops_kcals
        # ==
        # THING - BIOFUELS_KCALS - FEED_KCALS
        #
        # where THING = depends:
        #          outdoor_crops_stored_food_fraction_kcals_to_humans <= 0:
        #               THING = BIOFUELS_KCALS + FEED_KCALS
        #          outdoor_crops_stored_food_fraction_kcals_to_humans > 0:
        #               THING = stored_food_outdoor_crops_kcals / outdoor_crops_stored_food_fraction_kcals_to_humans
        #               where
        #               outdoor_crops_stored_food_fraction_kcals_to_humans
        #                   = 1 - (BIOFUELS_KCALS + FEED_KCALS) / stored_food_outdoor_crops_kcals
        #               so
        #               THING
        #                   = stored_food_outdoor_crops_kcals
        #                     /
        #                     (1 - (BIOFUELS_KCALS + FEED_KCALS) / stored_food_outdoor_crops_kcals)
        # In case outdoor_crops_stored_food_fraction_kcals_to_humans <= 0: (all og and sf going to nonhuman consumption):
        #
        # stored_food_outdoor_crops_kcals
        # ==
        # 0
        #
        # OK! that makes sense. Any situtation with all to nonhuman would be wierd and
        # rare low og and sf so this bug wouldn't matter
        #
        #
        # In case outdoor_crops_stored_food_fraction_kcals_to_humans > 0: (all og and sf going to nonhuman consumption):
        #
        # stored_food_outdoor_crops_kcals
        # ==
        # stored_food_outdoor_crops_kcals / (1 - (BIOFUELS_KCALS + FEED_KCALS) / stored_food_outdoor_crops_kcals)
        # - BIOFUELS_KCALS - FEED_KCALS
        #
        # 1 + (BIOFUELS_KCALS + FEED_KCALS)/stored_food_outdoor_crops_KCALS
        # ==
        # 1 / (1 - (BIOFUELS_KCALS + FEED_KCALS) / stored_food_outdoor_crops_kcals)
        #
        # if we let x= (BIOFUELS_KCALS + FEED_KCALS) / stored_food_outdoor_crops_kcals)
        #
        # we see as x is small:
        #
        #   1+x == 1/(1-x) ~= 1+x
        #

        fractional_difference = np.where(
            np.abs(denominator) <= 1e-6, 0, fractional_difference
        )

        assert (abs(fractional_difference) < 1e-6).all()

        if self.constants["inputs"]["INCLUDE_FAT"]:
            division = []
            print("stored_food_outdoor_crops_fat")
            print(stored_food_outdoor_crops_fat)
            index = 0
            print("self.outdoor_crops_stored_food_fraction_fat_to_humans")
            print(self.outdoor_crops_stored_food_fraction_fat_to_humans)
            for zipped_lists in zip(
                stored_food_outdoor_crops_fat,
                self.outdoor_crops_stored_food_fraction_fat_to_humans,
            ):
                if zipped_lists[1] < 0:
                    assert zipped_lists[0] >= -1e-5
                    if index == 0:
                        print("IN WIERD CONDITION FIRST")
                    division.append(0)
                else:
                    if index == 0:
                        print("NOT IN WIERD CONDITION FIRST")
                    if index == 4:
                        print("NOT IN WIERD CONDITION LATER")
                    division.append(zipped_lists[0] / zipped_lists[1])
                index += 1
            numerator = (
                stored_food_outdoor_crops_fat
                + self.billions_fed_h_e_meat_fat
                + self.billions_fed_h_e_milk_fat
            ) - (np.array(division) + self.billions_fed_h_e_balance.fat)

            # stored_food_outdoor_crops_fat + MEAT_MILK_H_E ==
            # (stored_food_outdoor_crops_fat/outdoor_crops_SF_FRACTION_FAT_TO_HUMANS + BALANCE_FAT)
            #
            # BALANCE_FAT = MEAT_MILK_H_E - FEED_FAT - BIOFUEL_FAT
            #
            # stored_food_outdoor_crops_fat == THING - FEED_FAT - BIOFUEL_FAT
            #
            # THING = stored_food_outdoor_crops_fat * (1-(FEED_FAT-BIOFUEL_FAT)/stored_food_outdoor_crops_fat)
            #
            # how it's being modified:
            #
            # stored_food_outdoor_crops_fat * (1-(FEED_FAT+BIOFUEL_FAT)/stored_food_outdoor_crops_fat)
            # ==
            # stored_food_outdoor_crops_fat - (FEED_FAT+BIOFUEL_FAT) * (1-(FEED_FAT+BIOFUEL_FAT)/stored_food_outdoor_crops_fat)
            #
            # stored_food_outdoor_crops_fat - (FEED_FAT+BIOFUEL_FAT)
            # ==
            # stored_food_outdoor_crops_fat - (FEED_FAT+BIOFUEL_FAT) -(FEED_FAT+BIOFUEL_FAT)/stored_food_outdoor_crops_fat)
            #
            # THING must be greater than stored_food_outdoor_crops_FAT. It's everything!
            # It's taking the result, and scaling it up by dividing the fraction of "everything" to animals -> if you scale stored_food_outdoor_crops_fat up before subtracting feed and biofuels, so you get stored_food_outdoor_crops_fat.
            #
            # THING = SCALED_UP_stored_food_outdoor_crops_fat = stored_food_outdoor_crops_fat/self.outdoor_crops_stored_food_fraction_fat_to_humans
            #
            # outdoor_crops_stored_food_fraction_fat_to_feed  = excess_fat_used / stored_food_outdoor_crops_fat
            # THING = 1 - excess_fat_used / stored_food_outdoor_crops_fat
            #

            #
            #
            # balance fat is just the result of feed and biofuels on the overall balance
            #
            #
            # I *think* this is checking total fat is equal to nonhuman fat plus human fat
            #
            # The only reason to do this is to check the optimizer.
            #
            # stored_food_outdoor_crops_fat + MEAT_MILK_HE ==
            # (stored_food_outdoor_crops_fat/outdoor_crops_SF_FRACTION_FAT_TO_HUMANS - EXCESS_NONHUMAN)
            #
            #
            #
            #

            #
            # (all the sources except using human edible fed food) + (-excess provided)
            # (all the sources except using human edible fed food)*(fraction fed to humans)
            #
            #
            #
            # FRACTION_TO_FEED
            #      = nonhuman_consumption.fat / (np.array(outdoor_crops_fat) + np.array(stored_food_fat))
            #
            # MEAT_MILK ==
            # (outdoor_crops_SF_FRACTION_FAT_TO_HUMANS*(MEAT_MILK-WASTE*(feed_fat+biofuels_fat)))
            #
            # outdoor_crops_stored_food_fat * FRACTION_TO_NONHUMAN = FEED_USAGE
            #
            #
            #
            #
            # MEAT_MILK * FRACTION_TO_FEED = MEAT_MILK - FEED_USAGE
            #
            # MEAT_MILK * FEED_USAGE/TOTAL = MEAT_MILK - FEED_USAGE

            # stored_food_outdoor_crops_fat + MEAT_MILK ==
            # (stored_food_outdoor_crops_fat/outdoor_crops_SF_FRACTION_FAT_TO_HUMANS+ BALANCE_FAT)
            #
            # MEAT_MILK: sent in from parameters
            #
            #   So really we have the following check:
            #
            # stored_food_outdoor_crops_fat = stored_food_outdoor_crops_fat*FRAC_TO_HUMANS - FAT_USED_FOR_FEED
            #
            # SOURCES:
            #           stored_food_outdoor_crops_fat: optimized
            #           FRAC_TO_HUMAN=stored_food_outdoor_crops_fat/outdoor_crops_SF_FRACTION_FAT_TO_HUMANS:
            #                   outdoor_crops_SF_FRACTION_FAT_TO_HUMANS: derived from ratio
            #                       nonhuman_consumption.fat
            #                       / (np.array(outdoor_crops_fat) + np.array(stored_food_fat))
            #
            #                       nonhuman_consumption.fat: sent in from parameters
            #                      stored_food_fat and outdoor_crops_fat: optimized
            #               FAT_USED_FOR_FEED: nonhuman_consumption.fat from parameters
            #
            # Which leaves us with sources of error from stored_food_fat, outdoor_crops_fat, and stored_food_outdoor_crops_fat
            #
            # stored_food_fat = self.to_monthly_list(
            #     stored_food_eaten,
            #     self.constants["SF_FRACTION_FAT"] / self.constants["FAT_MONTHLY"] / 1e9,
            #     False,
            # )
            # self.billions_fed_stored_food_fat = np.multiply(
            #     self.to_monthly_list(
            #         stored_food_eaten,
            #
            #         * self.constants["SF_FRACTION_FAT"]
            #         / self.constants["FAT_MONTHLY"]
            #         / 1e9,
            #                     #     ),
            #     self.outdoor_crops_stored_food_fraction_fat_to_humans,
            # )
            print(
                "why billions_fed h e meat and billions fed he milk fat not equal to the balance?"
            )
            print(
                "stored_food_outdoor_crops EQUALS ZERO:"
                + str(
                    100 * stored_food_outdoor_crops_fat[0] / population_billions < 0.1
                )
            )
            print(
                "DIV EQUALS ZERO:" + str(100 * division[0] / population_billions < 0.1)
            )
            # DELETEME

            print(
                "stored_food_outdoor_crops_fat+ self.billions_fed_h_e_meat_fat+ self.billions_fed_h_e_milk_fat"
            )
            print(
                (
                    stored_food_outdoor_crops_fat
                    + self.billions_fed_h_e_meat_fat
                    + self.billions_fed_h_e_milk_fat
                )
                / population_billions
                * 100
            )

            print("np.array(division)")
            print(100 * (np.array(division) / population_billions))
            print("np.array(division) + self.billions_fed_h_e_balance.fat")
            print(
                (np.array(division) + self.billions_fed_h_e_balance.fat)
                / population_billions
                * 100
            )
            denominator = (
                stored_food_outdoor_crops_fat
                + self.billions_fed_h_e_meat_fat
                + self.billions_fed_h_e_milk_fat
            )

            numerator_percent = 100 * (numerator / population_billions)
            denominator_percent = 100 * (np.array(denominator) / population_billions)

            fractional_difference = np.divide(numerator_percent, denominator_percent)

            # THe fractional difference is enforcing the condition that the optimizer
            # has taken all the fat remaining after enforced feed, and used it for humans
            fractional_difference = np.where(
                np.abs(denominator_percent) <= 0.1, 0, fractional_difference
            )

            print("numerator_percent")
            print(numerator_percent)
            print("denominator_percent")
            print(denominator_percent)
            print("fractional_difference")
            print(fractional_difference)

            assert (abs(fractional_difference) < 1e-4).all()

        if self.constants["inputs"]["INCLUDE_PROTEIN"]:

            division = []
            for zipped_lists in zip(
                stored_food_outdoor_crops_protein,
                self.outdoor_crops_stored_food_fraction_protein_to_humans,
            ):

                if zipped_lists[1] <= 0:
                    assert zipped_lists[0] >= -1e-5
                    division.append(0)
                else:
                    division.append(zipped_lists[0] / zipped_lists[1])

            # a separate problem is if we have a primary restriction on protein or fat rather than calories, the rebalancer will try to get the calories the same for each month, but then even if there are enough calories, this will force protein used to be more than is available from outdoor growing and stored food.

            numerator = (
                stored_food_outdoor_crops_protein
                + self.billions_fed_h_e_meat_protein
                + self.billions_fed_h_e_milk_protein
            ) - (np.array(division) + self.billions_fed_h_e_balance.protein)

            denominator = (
                stored_food_outdoor_crops_protein
                + self.billions_fed_h_e_meat_protein
                + self.billions_fed_h_e_milk_protein
            )

            fractional_difference = np.divide(
                numerator,
                denominator,
            )
            numerator_percent = 100 * (numerator / population_billions)
            denominator_percent = 100 * (np.array(denominator) / population_billions)

            fractional_difference = np.divide(numerator_percent, denominator_percent)

            fractional_difference = np.where(
                np.abs(denominator) <= 0.1, 0, fractional_difference
            )
            assert (abs(fractional_difference) < 1e-6).all()

    def YES_THIS_ONE_PROBABLY_DOES_SOMETHING_USEFUL_question_mark(
        self, stored_food, rotation, no_rotation, excess
    ):

        # OKAY,THIS VALIDATION IS JUST MAKING SURE FEED (with additional excess) AND BIOFUELS ARE ALWAYS LESS THAN STORED FOOD PLUS outdoor_crops, WITH NO WASTE APPLIED ON EITHER SIDE AS WASTE IS THE SAME (BOTH ARE CROPS WASTE)
        small_percent_threshold = Food(
            -0.01,
            -0.01,
            -0.01,
            "percent people fed per month",
            "percent people fed per month",
            "percent people fed per month",
        )

        assert (
            (self.sf + self.rot + self.no_rot - self.excess)
            .in_units_percent()
            .all_greater_than(small_percent_threshold)
        ), """There are too few calories 
        available to meet the caloric excess 
        provided to the simulator. This is probably because the optimizer seems to have
         failed to sufficiently meet the constraint to limit total food fed to animals
          to the sum of stored food and outdoor growing within a reasonable degree of
           precision. Consider reducing precision. Quitting."""

        if (
            -(self.sf + self.rot + self.no_rot - self.excess).in_units_percent()
        ).any_greater_than_or_equal_to(small_percent_threshold):
            print("")
            print(
                """WARNING: All of the outdoor growing and stored food is being fed to 
                animals and none to humans"""
            )

    def ensure_optimizer_returns_same_as_sum_nutrients(self, model, interpeter):
        """
        ensure there was no major error in the optimizer or in analysis which caused
        the sums reported to differ between adding up all the extracted variables and
        just look at the reported result of the objective of the optimizer
        """

        percent_people_fed_reported_directly_by_optimizer = model.objective.value()
        percent_people_fed_by_summing_all_foods = interpeter.percent_people_fed

        # WE MIGHT WANT TO USE THIS INSTEAD, WE SHALL SEE
        # assert (
        #     percent_people_fed_by_summing_all_foods - 0.1
        #     < percent_people_fed_reported_directly_by_optimizer
        #     < percent_people_fed_by_summing_all_foods + 0.1
        # ), "ERROR: The optimizer and the extracted results do not match"
        assert (
            percent_people_fed_by_summing_all_foods
            < percent_people_fed_reported_directly_by_optimizer
            < percent_people_fed_by_summing_all_foods
        ), "ERROR: The optimizer and the extracted results do not match"

    def ensure_interpreted_food_to_humans_same_as_food_from_optimizer(self, results):
        """
        ensure that the total food to humans plus food to other equals the total food

        Does this by summing the food results directly from the extractor,
        and comparing to the food results from the intepreter

        """

        total_food_to_humans = results.x + results.x + results.x
        total_food_to_other = results.x + results.x + results.x
        total_food = total_food_to_humans + total_food_to_other

        assert (
            total_food - 0.1 < results.total_food - total_food < total_food + 0.1
        ), "ERROR: The total food to humans plus food to other does not equal the total food"

    def ensure_consumption_zero_if_stored_food_plus_outdoor_crops_zero(
        self, stored_food_plus_outdoor_crops, nonhuman_consumption
    ):
        """
        ensure that the consumption of nonhuman food is zero where the stored food plus
        outdoor crops is zero
        """

        nonhuman_consumption_where_stored_food_plus_outdoor_crops_zero = np.where(
            stored_food_plus_outdoor_crops <= 0, nonhuman_consumption, 0
        )

        assert (
            nonhuman_consumption_where_stored_food_plus_outdoor_crops_zero == 0
        ).all()

    def ensure_immediate_and_new_stored_add_correctly_to_sources(
        self, immediate, new_stored, outdoor_crops, stored_food
    ):

        difference = (immediate + new_stored) - (outdoor_crops + new_stored)
        difference_rounded = difference.get_rounded_to_decimal(1)

        assert difference_rounded.is_units_percent()

        assert (
            difference_rounded.kcals == 0
        ).all(), """ERROR: Immediate 
            and new stored sources do not add up to the sources of outdoor crops 
            and stored food"""
