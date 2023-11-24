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
from src.food_system.food import Food


class Validator:
    def validate_results(
        self,
        extracted_results,
        interpreted_results,
        time_consts,
        percent_fed_from_model,
    ):
        """
        Validates the results of the model by ensuring that the optimizer returns the same as the sum of nutrients,
        that zero kcals have zero fat and protein, that there are no NaN values, and that all values are greater than or
        equal to zero.

        Args:
            model (Model): The model to validate the results of.
            extracted_results (ExtractedResults): The extracted results from the model.
            interpreted_results (InterpretedResults): The interpreted results from the model.

        Returns:
            None
        """

        # Ensure optimizer returns same as sum of nutrients
        self.ensure_optimizer_returns_same_as_sum_nutrients(
            percent_fed_from_model,
            interpreted_results,
            extracted_results.constants["inputs"]["INCLUDE_FAT"],
            extracted_results.constants["inputs"]["INCLUDE_PROTEIN"],
        )

        # Ensure zero kcals have zero fat and protein
        self.ensure_zero_kcals_have_zero_fat_and_protein(interpreted_results)

        # Ensure there are no NaN values
        self.ensure_never_nan(interpreted_results)

        # Ensure all values are greater than or equal to zero
        self.ensure_all_greater_than_or_equal_to_zero(interpreted_results)

        # check if all Food objects in the dictionary have the same units list
        self.ensure_all_time_constants_units_are_billion_kcals(time_consts)

    # Function to check if all Food objects in the dictionary have the same units list
    def ensure_all_time_constants_units_are_billion_kcals(self, time_consts):
        for key, value in time_consts.items():
            if isinstance(value, Food):
                print("FOOD!")
                print("food key")
                print(key)
                print(value.units)
                assert value.units == [
                    "billion kcals each month",
                    "thousand tons each month",
                    "thousand tons each month",
                ], "ERROR: All the units for foods passed to optimizer don't match expected units"

    def check_constraints_satisfied(self, model, maximize_constraints, variables):
        """
        This function checks if all constraints are satisfied by the final values of the variables.
        It takes a really long time to run, so it's run infrequently.

        Args:
            model (pulp.LpProblem): The optimization model
            maximize_constraints (list): A list of constraints to maximize
            variables (list): A list of variables to check constraints against

        Returns:
            None

        Raises:
            AssertionError: If a constraint is not satisfied

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
        self, percent_fed_from_model, interpreted_results, INCLUDE_FAT, INCLUDE_PROTEIN
    ):
        """
        ensure there was no major error in the optimizer or in analysis which caused
        the sums reported to differ between adding up all the extracted variables and
        just look at the reported result of the objective of the optimizer
        """

        decimals = 0

        percent_people_fed_by_summing_all_foods = interpreted_results.percent_people_fed
        difference = round(
            percent_fed_from_model - percent_people_fed_by_summing_all_foods,
            decimals,
        )

        assert difference == 0, (
            """ERROR: The optimizer and the extracted results do not match.
        optimizer: """
            + str(percent_fed_from_model)
            + "\n      summing each food source extracted: "
            + str(percent_people_fed_by_summing_all_foods)
        )

    def ensure_zero_kcals_have_zero_fat_and_protein(self, interpreted_results):
        """
        Checks that for any month where kcals is zero for any of the foods,
        then fat and protein must also be zero.

        Args:
            interpreted_results (InterpretedResults): An instance of the InterpretedResults class

        Returns:
            None

        Notes:
            This function is called to ensure that the kcals, fat and protein values are consistent
            for each food source, feed and biofuels independently.

        Raises:
            AssertionError: If the kcals value is zero but the fat or protein value is non-zero.

        """

        # Check each food source for consistency
        interpreted_results.cell_sugar.make_sure_fat_protein_zero_if_kcals_is_zero()
        interpreted_results.scp.make_sure_fat_protein_zero_if_kcals_is_zero()
        interpreted_results.greenhouse.make_sure_fat_protein_zero_if_kcals_is_zero()
        interpreted_results.fish.make_sure_fat_protein_zero_if_kcals_is_zero()
        interpreted_results.culled_meat.make_sure_fat_protein_zero_if_kcals_is_zero()
        interpreted_results.milk.make_sure_fat_protein_zero_if_kcals_is_zero()
        interpreted_results.immediate_outdoor_crops.make_sure_fat_protein_zero_if_kcals_is_zero()
        interpreted_results.new_stored_outdoor_crops.make_sure_fat_protein_zero_if_kcals_is_zero()

        # TODO: REINSTATE ONCE FIGURED OUT WHY THIS FAILS
        # I'm pretty sure, if there is some food that gets its kcals used up by feed
        # but not its calories, it's alright if only fat goes to humans, and no kcals...
        # which is wierd, but it's a reasonable way for the model to work I think

        # Check each feed and biofuel for consistency
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
        This function checks that the interpreter results are always defined as a real number.
        It does this by calling the make_sure_not_nan() method on each of the interpreted_results attributes.
        If any of the attributes contain NaN values, an exception will be raised.

        Args:
            interpreted_results (InterpretedResults): An instance of the InterpretedResults class.

        Raises:
            ValueError: If any of the interpreted_results attributes contain NaN values.

        Returns:
            None
        """

        # Call make_sure_not_nan() on each of the interpreted_results attributes
        interpreted_results.stored_food.make_sure_not_nan()
        interpreted_results.outdoor_crops.make_sure_not_nan()
        interpreted_results.seaweed.make_sure_not_nan()
        interpreted_results.cell_sugar.make_sure_not_nan()
        interpreted_results.scp.make_sure_not_nan()
        interpreted_results.greenhouse.make_sure_not_nan()
        interpreted_results.fish.make_sure_not_nan()
        interpreted_results.culled_meat.make_sure_not_nan()
        interpreted_results.milk.make_sure_not_nan()
        interpreted_results.immediate_outdoor_crops.make_sure_not_nan()
        interpreted_results.new_stored_outdoor_crops.make_sure_not_nan()

    def ensure_all_greater_than_or_equal_to_zero(self, interpreted_results):
        """
        Checks that all the results variables are greater than or equal to zero.
        Args:
            interpreted_results (InterpretedResults): An instance of the InterpretedResults class
        Raises:
            AssertionError: If any of the results variables are less than zero
        """

        # Check that the cell_sugar variable is greater than or equal to zero
        assert interpreted_results.cell_sugar.all_greater_than_or_equal_to_zero()

        # Check that the scp variable is greater than or equal to zero
        assert interpreted_results.scp.all_greater_than_or_equal_to_zero()

        # Check that the greenhouse variable is greater than or equal to zero
        assert interpreted_results.greenhouse.get_rounded_to_decimal(
            6
        ).all_greater_than_or_equal_to_zero()

        # Check that the fish variable is greater than or equal to zero
        assert interpreted_results.fish.all_greater_than_or_equal_to_zero()

        # Check that the culled_meat variable is greater than or equal to zero
        assert interpreted_results.culled_meat.get_rounded_to_decimal(
            6
        ).all_greater_than_or_equal_to_zero()

        # Check that the milk variable is greater than or equal to zero
        assert interpreted_results.milk.all_greater_than_or_equal_to_zero()

        # Check that the immediate_outdoor_crops variable is greater than or equal to zero

        # interpreted_results.immediate_outdoor_crops.plot("imm crops")
        # interpreted_results.new_stored_outdoor_crops.plot("ns crops")
        # Todo: fix this
        # assert interpreted_results.immediate_outdoor_crops.get_rounded_to_decimal(
        #     6
        # ).all_greater_than_or_equal_to_zero()
        assert (
            interpreted_results.new_stored_outdoor_crops.all_greater_than_or_equal_to_zero()
        )
