################################# Validator ###################################
##                                                                            #
##            Checks that the optimizer successfully optimized.               #
##        To do this, it makes sure that the constraints given are            #
##            all satisfied within an acceptable margin of error              #
##                                                                            #
###############################################################################


import os
import sys
import numpy as np

module_path = os.path.abspath(os.path.join("../.."))
if module_path not in sys.path:
    sys.path.append(module_path)


from src.food_system.food import Food


class Validator:
    def __init__(self):
        pass

    def validate_results(self, model, extracted_results, interpreted_results):

        self.ensure_optimizer_returns_same_as_sum_nutrients(model, interpreted_results)

        # TODO: DELETE THIS if not useful
        # self.YES_THIS_ONE_PROBABLY_DOES_SOMETHING_USEFUL_question_mark()

        (
            kcals_total_from_optimizer,
            fat_total_from_optimizer,
            protein_total_from_optimizer,
        ) = extracted_results.get_objective_optimization_results(
            model,
        )

        self.ensure_any_nonzero_kcals_have_nonzero_fat_and_protein(interpreted_results)
        self.ensure_never_nan(interpreted_results)
        self.ensure_all_greater_than_or_equal_to_zero(interpreted_results)

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

    # TODO : DELETE THIS CODE IF IT DOESN'T END UP USEFUL
    # def YES_THIS_ONE_PROBABLY_DOES_SOMETHING_USEFUL_question_mark(
    #     self, stored_food, rotation, no_rotation, excess
    # ):

    #     # OKAY,THIS VALIDATION IS JUST MAKING SURE FEED (with additional excess) AND BIOFUELS ARE ALWAYS LESS THAN STORED FOOD PLUS outdoor_crops, WITH NO WASTE APPLIED ON EITHER SIDE AS WASTE IS THE SAME (BOTH ARE CROPS WASTE)
    #     small_percent_threshold = Food(
    #         -0.01,
    #         -0.01,
    #         -0.01,
    #         "percent people fed per month",
    #         "percent people fed per month",
    #         "percent people fed per month",
    #     )

    #     assert (
    #         (self.sf + self.rotation + self.no_rotation - self.excess)
    #         .in_units_percent()
    #         .all_greater_than(small_percent_threshold)
    #     ), """There are too few calories
    #     available to meet the caloric excess
    #     provided to the simulator. This is probably because the optimizer seems to have
    #      failed to sufficiently meet the constraint to limit total food fed to animals
    #       to the sum of stored food and outdoor growing within a reasonable degree of
    #        precision. Consider reducing precision. Quitting."""

    #     if (
    #         -(
    #             self.sf + self.rotation + self.no_rotation - self.excess
    #         ).in_units_percent()
    #     ).any_greater_than_or_equal_to(small_percent_threshold):
    #         print("")
    #         print(
    #             """WARNING: All of the outdoor growing and stored food is being fed to
    #             animals and none to humans"""
    #         )

    def ensure_optimizer_returns_same_as_sum_nutrients(
        self, model, interpreted_results
    ):
        """
        ensure there was no major error in the optimizer or in analysis which caused
        the sums reported to differ between adding up all the extracted variables and
        just look at the reported result of the objective of the optimizer
        """

        decimals = 1

        percent_people_fed_reported_directly_by_optimizer = model.objective.value()
        percent_people_fed_by_summing_all_foods = interpreted_results.percent_people_fed
        difference = round(
            percent_people_fed_reported_directly_by_optimizer
            - percent_people_fed_by_summing_all_foods,
            decimals,
        )
        # WE MIGHT WANT TO USE THIS INSTEAD, WE SHALL SEE
        # assert (
        #     percent_people_fed_by_summing_all_foods - 0.1
        #     < percent_people_fed_reported_directly_by_optimizer
        #     < percent_people_fed_by_summing_all_foods + 0.1
        # ), "ERROR: The optimizer and the extracted results do not match"
        assert difference == 0, (
            """ERROR: The optimizer and the extracted results do not match.
        optimizer: """
            + str(percent_people_fed_reported_directly_by_optimizer)
            + "\n      summing each food source extracted: "
            + str(percent_people_fed_by_summing_all_foods)
        )

    def ensure_any_nonzero_kcals_have_nonzero_fat_and_protein(
        self, interpreted_results
    ):
        """
        checks that for any month where kcals is zero for any of the foods,
        then fat and protein must also be zero.

        True for every food source and also for feed and biofuels independently.
        """

        interpreted_results.cell_sugar.make_sure_fat_protein_zero_if_kcals_is_zero()

        interpreted_results.scp.make_sure_fat_protein_zero_if_kcals_is_zero()

        interpreted_results.greenhouse.make_sure_fat_protein_zero_if_kcals_is_zero()

        interpreted_results.fish.make_sure_fat_protein_zero_if_kcals_is_zero()

        interpreted_results.meat_culled_plus_grazing_cattle_maintained.make_sure_fat_protein_zero_if_kcals_is_zero()

        interpreted_results.grazing_milk.make_sure_fat_protein_zero_if_kcals_is_zero()

        interpreted_results.grain_fed_meat.make_sure_fat_protein_zero_if_kcals_is_zero()

        interpreted_results.grain_fed_milk.make_sure_fat_protein_zero_if_kcals_is_zero()

        interpreted_results.immediate_outdoor_crops.make_sure_fat_protein_zero_if_kcals_is_zero()

        interpreted_results.new_stored_outdoor_crops.make_sure_fat_protein_zero_if_kcals_is_zero()

        # nonhuman consumption in units percent people fed

        interpreted_results.nonhuman_consumption_percent.make_sure_fat_protein_zero_if_kcals_is_zero()

        interpreted_results.stored_food_rounded.make_sure_fat_protein_zero_if_kcals_is_zero()
        interpreted_results.seaweed_rounded.make_sure_fat_protein_zero_if_kcals_is_zero()
        interpreted_results.outdoor_crops_rounded.make_sure_fat_protein_zero_if_kcals_is_zero()
        interpreted_results.immediate_outdoor_crops_rounded.make_sure_fat_protein_zero_if_kcals_is_zero()
        interpreted_results.new_stored_outdoor_crops_rounded.make_sure_fat_protein_zero_if_kcals_is_zero()
        interpreted_results.stored_food_to_humans.make_sure_fat_protein_zero_if_kcals_is_zero()
        interpreted_results.outdoor_crops_to_humans.make_sure_fat_protein_zero_if_kcals_is_zero()
        interpreted_results.immediate_outdoor_crops_to_humans.make_sure_fat_protein_zero_if_kcals_is_zero()
        interpreted_results.new_stored_outdoor_crops_to_humans.make_sure_fat_protein_zero_if_kcals_is_zero()

    def ensure_never_nan(self, interpreted_results):
        """
        checks that the interpreter results are always defined as a real number
        """

        interpreted_results.stored_food.make_sure_not_nan()

        interpreted_results.outdoor_crops.make_sure_not_nan()

        interpreted_results.seaweed.make_sure_not_nan()

        interpreted_results.cell_sugar.make_sure_not_nan()

        interpreted_results.scp.make_sure_not_nan()

        interpreted_results.greenhouse.make_sure_not_nan()

        interpreted_results.fish.make_sure_not_nan()

        interpreted_results.meat_culled_plus_grazing_cattle_maintained.make_sure_not_nan()

        interpreted_results.grazing_milk.make_sure_not_nan()

        interpreted_results.grain_fed_meat.make_sure_not_nan()

        interpreted_results.grain_fed_milk.make_sure_not_nan()

        interpreted_results.immediate_outdoor_crops.make_sure_not_nan()

        interpreted_results.new_stored_outdoor_crops.make_sure_not_nan()

        # nonhuman consumption in units percent people fed

        interpreted_results.nonhuman_consumption_percent.make_sure_not_nan()

        interpreted_results.stored_food_rounded.make_sure_not_nan()
        interpreted_results.seaweed_rounded.make_sure_not_nan()
        interpreted_results.outdoor_crops_rounded.make_sure_not_nan()
        interpreted_results.immediate_outdoor_crops_rounded.make_sure_not_nan()
        interpreted_results.new_stored_outdoor_crops_rounded.make_sure_not_nan()
        interpreted_results.stored_food_to_humans.make_sure_not_nan()
        interpreted_results.outdoor_crops_to_humans.make_sure_not_nan()
        interpreted_results.immediate_outdoor_crops_to_humans.make_sure_not_nan()
        interpreted_results.new_stored_outdoor_crops_to_humans.make_sure_not_nan()

    def ensure_all_greater_than_or_equal_to_zero(self, interpreted_results):
        """
        checks that all the results variables are greater than or equal to zero
        """

        assert interpreted_results.cell_sugar.all_greater_than_or_equal_to_zero()

        assert interpreted_results.scp.all_greater_than_or_equal_to_zero()

        assert interpreted_results.greenhouse.all_greater_than_or_equal_to_zero()

        assert interpreted_results.fish.all_greater_than_or_equal_to_zero()

        assert (
            interpreted_results.meat_culled_plus_grazing_cattle_maintained.all_greater_than_or_equal_to_zero()
        )

        assert interpreted_results.grazing_milk.all_greater_than_or_equal_to_zero()

        assert interpreted_results.grain_fed_meat.all_greater_than_or_equal_to_zero()

        assert interpreted_results.grain_fed_milk.all_greater_than_or_equal_to_zero()

        assert (
            interpreted_results.immediate_outdoor_crops.all_greater_than_or_equal_to_zero()
        )

        assert (
            interpreted_results.new_stored_outdoor_crops.all_greater_than_or_equal_to_zero()
        )

        # nonhuman consumption in units percent people fed
        assert (
            interpreted_results.nonhuman_consumption_percent.all_greater_than_or_equal_to_zero()
        )

        assert (
            interpreted_results.stored_food_rounded.all_greater_than_or_equal_to_zero()
        )
        assert interpreted_results.seaweed_rounded.all_greater_than_or_equal_to_zero()
        assert (
            interpreted_results.outdoor_crops_rounded.all_greater_than_or_equal_to_zero()
        )
        assert (
            interpreted_results.immediate_outdoor_crops_rounded.all_greater_than_or_equal_to_zero()
        )
        assert (
            interpreted_results.new_stored_outdoor_crops_rounded.all_greater_than_or_equal_to_zero()
        )
        assert (
            interpreted_results.stored_food_to_humans.all_greater_than_or_equal_to_zero()
        )
        assert (
            interpreted_results.outdoor_crops_to_humans.all_greater_than_or_equal_to_zero()
        )
        assert (
            interpreted_results.immediate_outdoor_crops_to_humans.all_greater_than_or_equal_to_zero()
        )
        assert (
            interpreted_results.new_stored_outdoor_crops_to_humans.all_greater_than_or_equal_to_zero()
        )
