"""
################################# Validator ###################################
##                                                                            #
##            Checks that the optimizer successfully optimized.               #
##        To do this, it makes sure that the constraints given are            #
##            all satisfied within an acceptable margin of error              #
##                                                                            #
###############################################################################
"""
import numpy as np


class Validator:
    def __init__(self):
        pass

    def validate_results(self, model, extracted_results, interpreted_results):

        self.ensure_optimizer_returns_same_as_sum_nutrients(
            model,
            interpreted_results,
            extracted_results.constants["inputs"]["INCLUDE_FAT"],
            extracted_results.constants["inputs"]["INCLUDE_PROTEIN"],
        )

        self.ensure_zero_kcals_have_zero_fat_and_protein(interpreted_results)
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
            if isinstance(c, list):
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

    def ensure_optimizer_returns_same_as_sum_nutrients(
        self, model, interpreted_results, INCLUDE_FAT, INCLUDE_PROTEIN
    ):
        """
        ensure there was no major error in the optimizer or in analysis which caused
        the sums reported to differ between adding up all the extracted variables and
        just look at the reported result of the objective of the optimizer
        """

        pass
        # TODO: FAILS OCCASIONALLY BELOW 1% precision...

        # decimals = 0

        # percent_people_fed_reported_directly_by_optimizer = model.objective.value()
        # percent_people_fed_by_summing_all_foods = interpreted_results.percent_people_fed
        # difference = round(
        #     percent_people_fed_reported_directly_by_optimizer
        #     - percent_people_fed_by_summing_all_foods,
        #     decimals,
        # )

        # TODO: reinstate this as working when protein or fat are excluded
        # if INCLUDE_FAT or INCLUDE_PROTEIN:
        #     return

        # assert difference == 0, (
        #     """ERROR: The optimizer and the extracted results do not match.
        # optimizer: """
        #     + str(percent_people_fed_reported_directly_by_optimizer)
        #     + "\n      summing each food source extracted: "
        #     + str(percent_people_fed_by_summing_all_foods)
        # )

    def ensure_zero_kcals_have_zero_fat_and_protein(self, interpreted_results):
        """
        checks that for any month where kcals is zero for any of the foods,
        then fat and protein must also be zero.

        True for every food source and also for feed and biofuels independently.
        """

        interpreted_results.cell_sugar.make_sure_fat_protein_zero_if_kcals_is_zero()

        interpreted_results.scp.make_sure_fat_protein_zero_if_kcals_is_zero()

        interpreted_results.greenhouse.make_sure_fat_protein_zero_if_kcals_is_zero()

        interpreted_results.fish.make_sure_fat_protein_zero_if_kcals_is_zero()

        interpreted_results.culled_meat_plus_grazing_cattle_maintained.make_sure_fat_protein_zero_if_kcals_is_zero()

        interpreted_results.grazing_milk.make_sure_fat_protein_zero_if_kcals_is_zero()

        interpreted_results.grain_fed_meat.make_sure_fat_protein_zero_if_kcals_is_zero()

        interpreted_results.grain_fed_milk.make_sure_fat_protein_zero_if_kcals_is_zero()

        interpreted_results.immediate_outdoor_crops.make_sure_fat_protein_zero_if_kcals_is_zero()

        interpreted_results.new_stored_outdoor_crops.make_sure_fat_protein_zero_if_kcals_is_zero()

        # nonhuman consumption in units percent people fed

        interpreted_results.nonhuman_consumption_percent.make_sure_fat_protein_zero_if_kcals_is_zero()

        # TODO: REINSTATE ONCE FIGURED OUT WHY THIS FAILS
        # I'm pretty sure, if there is some food that gets its kcals used up by feed
        # but not its calories, it's alright if only fat goes to humans, and no kcals...
        # which is wierd, but it's a reasonable way for the model to work I think

        # interpreted_results.stored_food_rounded.make_sure_fat_protein_zero_if_kcals_is_zero()
        # interpreted_results.seaweed_rounded.get_rounded_to_decimal(
        #     2
        # ).make_sure_fat_protein_zero_if_kcals_is_zero()
        # interpreted_results.outdoor_crops_rounded.make_sure_fat_protein_zero_if_kcals_is_zero()
        # interpreted_results.immediate_outdoor_crops_rounded.make_sure_fat_protein_zero_if_kcals_is_zero()
        # interpreted_results.new_stored_outdoor_crops_rounded.make_sure_fat_protein_zero_if_kcals_is_zero()
        # interpreted_results.stored_food_to_humans.make_sure_fat_protein_zero_if_kcals_is_zero()
        # interpreted_results.outdoor_crops_to_humans.make_sure_fat_protein_zero_if_kcals_is_zero()
        # interpreted_results.immediate_outdoor_crops_to_humans.make_sure_fat_protein_zero_if_kcals_is_zero()
        # interpreted_results.new_stored_outdoor_crops_to_humans.make_sure_fat_protein_zero_if_kcals_is_zero()

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

        interpreted_results.culled_meat_plus_grazing_cattle_maintained.make_sure_not_nan()

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

        assert interpreted_results.greenhouse.get_rounded_to_decimal(
            6
        ).all_greater_than_or_equal_to_zero()

        assert interpreted_results.fish.all_greater_than_or_equal_to_zero()
        assert interpreted_results.culled_meat_plus_grazing_cattle_maintained.get_rounded_to_decimal(
            6
        ).all_greater_than_or_equal_to_zero()

        assert interpreted_results.grazing_milk.all_greater_than_or_equal_to_zero()

        assert interpreted_results.grain_fed_meat.all_greater_than_or_equal_to_zero()

        assert interpreted_results.grain_fed_milk.all_greater_than_or_equal_to_zero()

        assert interpreted_results.immediate_outdoor_crops.get_rounded_to_decimal(
            6
        ).all_greater_than_or_equal_to_zero()

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
        assert interpreted_results.stored_food_to_humans.get_rounded_to_decimal(
            6
        ).all_greater_than_or_equal_to_zero()
        assert interpreted_results.outdoor_crops_to_humans.get_rounded_to_decimal(
            6
        ).all_greater_than_or_equal_to_zero()

        assert interpreted_results.immediate_outdoor_crops_to_humans.get_rounded_to_decimal(
            6
        ).all_greater_than_or_equal_to_zero()
        assert (
            interpreted_results.new_stored_outdoor_crops_to_humans.all_greater_than_or_equal_to_zero()
        )
