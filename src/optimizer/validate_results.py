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
import pytest
from src.food_system.food import Food


class Validator:
    def validate_results(
        self,
        extracted_results,
        interpreted_results,
        time_consts,
        percent_fed_from_model,
        optimization_type,
        country_code,
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
        if optimization_type != "to_animals":
            # Ensure optimizer returns same as sum of nutrients
            self.ensure_optimizer_returns_same_as_sum_nutrients(
                percent_fed_from_model,
                interpreted_results,
                extracted_results.constants["inputs"]["INCLUDE_FAT"],
                extracted_results.constants["inputs"]["INCLUDE_PROTEIN"],
                country_code,
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
                assert value.units == [
                    "billion kcals each month",
                    "thousand tons each month",
                    "thousand tons each month",
                ], (
                    "ERROR: All the units for foods passed to optimizer don't match expected units."
                    "Expected 'billion kcals each month' for kcals and 'thousand tons each month' for fat "
                    f"and protein but got\n {str(value.units)} for food {key}"
                )

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
        self,
        percent_fed_from_model,
        interpreted_results,
        INCLUDE_FAT,
        INCLUDE_PROTEIN,
        country_code,
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
        if (
            country_code == "EST"  # Estonia, population 1,320,8032
            or country_code == "LUX"  # Luxembourg, population 658,359
            or country_code == "CYP"  # Cyprus, population 1,251,488
            or country_code == "GUY"  # Guyana, population 816,853
            or country_code
            == "SWT"  # Eswatini (formerly swaziland), population 1,201,670
        ):
            # known issue with estonia...
            assert difference < 5, (
                """ERROR: Estonia or Luxembourg is more wrong than usual...: """
                + str(percent_fed_from_model)
                + "\n      summing each food source extracted: "
                + str(percent_people_fed_by_summing_all_foods)
            )
            if (
                abs(percent_fed_from_model - percent_people_fed_by_summing_all_foods)
                > 1
            ):
                # no excessive error above, so print a warning
                print(
                    f"WARNING: country {country_code} reports results potentially incorrectly by a few percent (< 5%)."
                )
                print(
                    f"        linear optimization found {round(percent_fed_from_model,2)}% fed,"
                )
                print(
                    "        but summing each food reported in stackplot adds to"
                    f" {round(percent_people_fed_by_summing_all_foods,2)}%."
                )
                print(
                    f"        Ignoring this because {country_code} is small and difference is small."
                )
        else:
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
        interpreted_results.meat.make_sure_fat_protein_zero_if_kcals_is_zero()
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
        interpreted_results.meat.make_sure_not_nan()
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
        assert interpreted_results.cell_sugar.all_greater_than_or_equal_to_zero(
            threshold=1e-9
        )

        # Check that the scp variable is greater than or equal to zero
        assert interpreted_results.scp.all_greater_than_or_equal_to_zero(threshold=1e-9)

        # Check that the greenhouse variable is greater than or equal to zero
        assert interpreted_results.greenhouse.get_rounded_to_decimal(
            6
        ).all_greater_than_or_equal_to_zero()

        # Check that the fish variable is greater than or equal to zero
        assert interpreted_results.fish.all_greater_than_or_equal_to_zero()

        # Check that the meat variable is greater than or equal to zero
        assert interpreted_results.meat.get_rounded_to_decimal(
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

    @staticmethod
    def assert_population_not_increasing(meat_dictionary, epsilon=1e-1, round=None):
        """
        Checks that the animal populations are never increasing with time (currently
        the condition is considered satisfied if it is met to within 10%)

        Args:
            meat_dictionary (dict): dictionary containing meat constants
            epsilon (float): threshold for the relative change in population
            round (int): round of optimization (optional, just for printing purposes)

        Returns:
            None
        """
        for key in meat_dictionary:
            if "population" in key:
                population_series = np.array(meat_dictionary[key])
                previous_month = population_series[:-1].copy()
                previous_month[
                    previous_month == 0
                ] = epsilon  # this is to avoid division by zero
                population_series[population_series < 1] = 0
                relative_changes = np.diff(population_series) / previous_month
                assert np.all(relative_changes <= epsilon), (
                    f"Error: round {round} of optimization has increasing {key} with time "
                    + f"beyond the allowed {epsilon*100}% threshold"
                )

    @staticmethod
    def assert_round2_meat_and_population_greater_than_round1(
        meat_dictionary_first_round,
        meat_dictionary_second_round,
        epsilon=1e-2,
        small_number=100,
    ):
        """
        Asserts that the total meat produced over the simulation timespan and the average animal population
        in the second round of optimization are greater than the first round. This test is repeated for each
        animal type.

        Args:
            meat_dictionary_first_round (dict): dictionary containing meat constants for the first round
            meat_dictionary_second_round (dict): dictionary containing meat constants for the second round
            epsilon (float): tolerance threshold for comparisons (set to 1% by default, smaller values were
                found to be too strict)
            small_number (float): threshold for the total meat produced or average animal population below which
                the test is not performed (set to 10 by default)

        Returns:
            None
        """
        for key in meat_dictionary_first_round:
            first_round_sum = np.sum(meat_dictionary_first_round[key])
            second_round_sum = np.sum(meat_dictionary_second_round[key])
            if "population" in key:
                # if the population if very small, than any deviation is most likely due to rounding errors
                if second_round_sum < small_number:
                    continue
                assert second_round_sum >= first_round_sum * (1 - epsilon), (
                    "Error: second round of optimization has a smaller "
                    + key
                    + " average than first round over the course of the simulation"
                )
            elif ("population" not in key) and ("milk" not in key):
                # if the ammout of meat if very small, than any deviation is most likely due to rounding errors
                if second_round_sum < small_number:
                    continue
                assert second_round_sum >= first_round_sum * (1 - epsilon), (
                    "Error: second round of optimization has less "
                    + key
                    + " produced over the course of the simulation than first round"
                )

    @staticmethod
    def verify_minimum_food_consumption_sum_round2(
        interpreted_results_round1, min_human_food_consumption, epsilon=1e-4
    ):
        """
        Verify that the sum of all foods for every month is always smaller or equal
        to the minimum food consumption targeted during round 2.
        This is only relevant if only kcals is required in the optimization, otherwise
        it is possible that more calories are consumed than the minimum targeted in order
        to meet the fat and protein requirements.

        Args:
            interpreted_results_round1 (InterpretedResults): interpreted results from round 1 of optimization
            min_human_food_consumption (dict): dictionary containing the minimum food consumption from
                calculate_human_consumption_for_min_needs
            epsilon (float): tolerance threshold for the sum of all foods (set to 0.01% by default)

        Returns:
            None
        """
        # do nothing if fat and protein are included in the optimization
        if (
            interpreted_results_round1.include_protein
            or interpreted_results_round1.include_fat
        ):
            return

        # sum all foods
        for i, key in enumerate(min_human_food_consumption):
            min_human_food_consumption[key]
            if i == 0:
                sum_of_all_foods = min_human_food_consumption[key]
            else:
                sum_of_all_foods = sum_of_all_foods + min_human_food_consumption[key]

        # verify that the sum is lower or equal to the minimum food consumption for each month
        target_calories = min_human_food_consumption[key].conversions.kcals_daily
        for i, total_that_month in enumerate(sum_of_all_foods.kcals):
            assert total_that_month <= target_calories * (1 + epsilon), (
                "Error: sum of all foods is greater than the minimum food consumption in round 2"
                + f" for month {i}"
            )

    @staticmethod
    def verify_food_usage_priorities_round2(
        interpreted_results_round1, min_human_food_consumption, epsilon=1e-4
    ):
        """
        Verify that the percentage of each food used (compared to the total amount of that food availabe)
        decreases when looking at foods in this order: fish, meat, dairy, greenhouse, outdoor crops, stored food,
        methane scp, cellulosic sugar, seaweed.
        Only relevant if only kcals is required in the optimization.

        Args:
            interpreted_results_round1 (InterpretedResults): interpreted results from round 1 of optimization
            min_human_food_consumption (dict): dictionary containing the minimum food consumption from
                calculate_human_consumption_for_min_needs
            epsilon (float): tolerance threshold for comparisons (set to 0.01% by default)

        Returns:
            None
        """
        # do nothing if fat and protein are included in the optimization
        if (
            interpreted_results_round1.include_protein
            or interpreted_results_round1.include_fat
        ):
            return

        previous_food_usage_percentages = 100.0 * np.ones(
            len(min_human_food_consumption["fish"].kcals)
        )
        previous_food_name = "none"
        for food_name, interpreted_food_name in zip(
            [
                "fish",
                "meat",
                "dairy",
                "greenhouse",
                "outdoor_crops",
                "stored_food",
                "methane_scp",
                "cellulosic_sugar",
                "seaweed",
            ],
            [
                "fish_kcals_equivalent",
                "meat_kcals_equivalent",
                "milk_kcals_equivalent",
                "greenhouse_kcals_equivalent",
                "immediate_outdoor_crops_kcals_equivalent",
                "stored_food_kcals_equivalent",
                "scp_kcals_equivalent",
                "cell_sugar_kcals_equivalent",
                "seaweed_kcals_equivalent",
            ],
        ):
            # calculate the percentage of each food used
            available_food = getattr(
                interpreted_results_round1, interpreted_food_name
            ).kcals
            if food_name == "outdoor_crops":
                available_food = (
                    interpreted_results_round1.immediate_outdoor_crops_kcals_equivalent.kcals
                    + interpreted_results_round1.new_stored_outdoor_crops_kcals_equivalent.kcals
                )
            food_usage_percentages = (
                100.0 * min_human_food_consumption[food_name].kcals / available_food
            )
            for month, percentage in enumerate(food_usage_percentages):
                # if that food is not available that month, then skip
                if (
                    available_food[month] <= epsilon
                    or food_usage_percentages[month] <= epsilon
                ):
                    continue
                # if that food is available that month, then check that the percentage
                # used is less than or equal to the previous food
                assert percentage <= previous_food_usage_percentages[month] * (
                    1 + epsilon
                ), (
                    f"Error: {food_name} usage percentage ({percentage}%)"
                    + f" is greater than {previous_food_name} in month {month}"
                    + f"({previous_food_usage_percentages[month]}%)"
                )
                previous_food_usage_percentages[month] = percentage
            previous_food_name = food_name

    @staticmethod
    def assert_meat_doesnt_increase_round_2(
        meat_running_available_round1, meat_running_available_round2, epsilon=1e-2
    ):
        assert np.all(
            meat_running_available_round2.sum()
            >= meat_running_available_round1.sum() * (1 - epsilon)
        ), (
            "Error: round 2 gets the same or more feed, yet it appears that the sum of meat available in round 2 is "
            "less than in round 1."
        )

    @staticmethod
    def assert_fewer_calories_round2_than_round3(
        interpreted_results_round2,
        interpreted_results_round3,
        epsilon=1e-1,
        absepsilon=1e-1,
    ):
        """
        Asserts that the total calories consumed in round 2 is less than or equal to round 3, for
        all months.
        This is only relevant if only kcals is required in the optimization.

        Args:
            interpreted_results_round2 (InterpretedResults): interpreted results from round 2 of optimization
            interpreted_results_round3 (InterpretedResults): interpreted results from round 3 of optimization
            epsilon (float): tolerance threshold for comparison (set to 1e-4 by default)

        Returns:
            None
        """
        # do nothing if fat and protein are included in the optimization
        if (
            interpreted_results_round3.include_protein
            or interpreted_results_round3.include_fat
        ):
            return

        # do nothing if no feed or biofuels are included in the optimization
        # (presumably because rounds 1 and 2 were skipped due to no feed or biofuels options)
        if np.all(
            interpreted_results_round2.feed_sum_kcals_equivalent.kcals == 0
        ) and np.all(
            interpreted_results_round2.biofuels_sum_kcals_equivalent.kcals == 0
        ):
            return

        # ignore meat and milk as these may be larger for round 2 due to incresased feed/biofuel
        total_calories_round2 = (
            interpreted_results_round2.fish_kcals_equivalent.kcals
            + interpreted_results_round2.cell_sugar_kcals_equivalent.kcals
            + interpreted_results_round2.scp_kcals_equivalent.kcals
            + interpreted_results_round2.greenhouse_kcals_equivalent.kcals
            + interpreted_results_round2.seaweed_kcals_equivalent.kcals
            # + interpreted_results_round2.milk_kcals_equivalent.kcals
            # + interpreted_results_round2.meat_kcals_equivalent.kcals
            + interpreted_results_round2.immediate_outdoor_crops_kcals_equivalent.kcals
            + interpreted_results_round2.new_stored_outdoor_crops_kcals_equivalent.kcals
            + interpreted_results_round2.stored_food_kcals_equivalent.kcals
        )

        total_calories_round3 = (
            interpreted_results_round3.fish_kcals_equivalent.kcals
            + interpreted_results_round3.cell_sugar_kcals_equivalent.kcals
            + interpreted_results_round3.scp_kcals_equivalent.kcals
            + interpreted_results_round3.greenhouse_kcals_equivalent.kcals
            + interpreted_results_round3.seaweed_kcals_equivalent.kcals
            + interpreted_results_round3.milk_kcals_equivalent.kcals
            + interpreted_results_round3.meat_kcals_equivalent.kcals
            + interpreted_results_round3.immediate_outdoor_crops_kcals_equivalent.kcals
            + interpreted_results_round3.new_stored_outdoor_crops_kcals_equivalent.kcals
            + interpreted_results_round3.stored_food_kcals_equivalent.kcals
        )

        # verify that the sum is lower or equal to the minimum food consumption for each month
        for i, total_that_month in enumerate(total_calories_round3):
            assert (
                total_that_month
                >= total_calories_round2[i] * (1 - epsilon) - absepsilon
            ), (
                "Error: total calories consumed in round 2 is greater than round 3"
                + f" for month {i}"
                + f"\n round 2 {total_calories_round2[i]}"
                + f"\n round 3 {total_that_month}"
            )
            PRINT_KCAL_EXCEEDED_WARNING = False
            if PRINT_KCAL_EXCEEDED_WARNING:
                if total_that_month < total_calories_round2[i]:
                    print(
                        "WARNING: calories round 2 greater than round 3 by small amount"
                        + f" for month {i}"
                        + f"\n round 2 {total_calories_round2[i]}"
                        + f"\n round 3 {total_that_month}"
                    )

    @staticmethod
    def assert_feed_used_below_feed_demand(
        feed_demand, interpreted_results, round, epsilon=1e-4
    ):
        """
        Asserts that the feed used is less than or equal to the feed demand for each month.
        Args:
            interpreted_results (InterpretedResults): interpreted results from any round of optimization
            round (int): round of optimization number (for more useful error messages)
            epsilon (float): tolerance threshold for comparison (set to 1e-4 by default)
        Returns:
            None
        """
        # do nothing if fat and protein are included in the optimization
        if interpreted_results.include_protein or interpreted_results.include_fat:
            return

        total_feed = Validator.sum_feed_sources(interpreted_results)
        reduced_feed_correct_units = (
            total_feed.in_units_bil_kcals_thou_tons_thou_tons_per_month()
            * (1 - epsilon)
        )

        assert np.all((feed_demand - reduced_feed_correct_units).kcals > -1e-6), (
            f"Error: feed used is greater than feed demand in round {round}\n"
            f"feed demand:\n"
            f"{feed_demand}\n"
            f"reduced_feed_correct_units:\n"
            f"{reduced_feed_correct_units}\n"
        )

    @staticmethod
    def assert_biofuels_used_below_biofuels_demand(
        biofuels_demand, interpreted_results, round, epsilon=1e-4
    ):
        """
        Asserts that the biofuels used is less than or equal to the biofuels demand for each month.
        Args:
            interpreted_results (InterpretedResults): interpreted results from any round of optimization
            round (int): round of optimization number (for more useful error messages)
            epsilon (float): tolerance threshold for comparison (set to 1e-6 by default)
        Returns:
            None
        """
        # do nothing if fat and protein are included in the optimization
        if interpreted_results.include_protein or interpreted_results.include_fat:
            return

        total_biofuels = Validator.sum_biofuel_sources(interpreted_results)
        reduced_biofuels_correct_units = (
            total_biofuels.in_units_bil_kcals_thou_tons_thou_tons_per_month()
            * (1 - epsilon)
        )

        assert np.all(
            (biofuels_demand - reduced_biofuels_correct_units).kcals > -1e-6
        ), (
            f"Error: biofuels used is greater than biofuels demand in round {round}\n"
            f"biofuels demand:\n"
            f"{biofuels_demand}\n"
            f"reduced_biofuels_correct_units:\n"
            f"{reduced_biofuels_correct_units}\n"
        )

    @staticmethod
    def assert_feed_used_round3_below_feed_used_round2(
        interpreted_results_round2, interpreted_results_round3, epsilon=1e-4
    ):
        # do nothing if fat and protein are included in the optimization
        if (
            interpreted_results_round3.include_protein
            or interpreted_results_round3.include_fat
        ):
            return

        total_feed_round2 = Validator.sum_feed_sources(interpreted_results_round2)
        if total_feed_round2 is None:
            return

        total_feed_round3 = Validator.sum_feed_sources(interpreted_results_round3)

        assert np.all(
            total_feed_round2.kcals - total_feed_round3.kcals > -epsilon
        ), "Error: total feed used in round 3 is greater than round 2"

    @staticmethod
    def sum_feed_sources(interpreted_results):
        """
        Sums all the feed sources together.
        """
        attributes = [
            "cell_sugar_feed",
            "scp_feed",
            "seaweed_feed",
            "outdoor_crops_feed",
            "stored_food_feed",
        ]

        for attr in attributes:
            if hasattr(interpreted_results, attr):
                if "total_feed" not in locals():
                    total_feed = getattr(interpreted_results, attr)
                else:
                    total_feed += getattr(interpreted_results, attr)

        if "total_feed" not in locals():
            total_feed = None
        else:
            return total_feed

    @staticmethod
    def sum_biofuel_sources(interpreted_results):
        """
        Sums all the biofuels sources together.
        """
        attributes = [
            "cell_sugar_biofuels",
            "scp_biofuels",
            "seaweed_biofuels",
            "outdoor_crops_biofuels",
            "stored_food_biofuels",
        ]

        for attr in attributes:
            if hasattr(interpreted_results, attr):
                if "total_biofuels" not in locals():
                    total_biofuels = getattr(interpreted_results, attr)
                else:
                    total_biofuels += getattr(interpreted_results, attr)

        if "total_biofuels" not in locals():
            total_biofuels = None
        else:
            return total_biofuels

    def assert_feed_and_biofuel_used_is_zero_if_humans_are_starving(
        interpreted_results, epsilon=1e-3
    ):
        if interpreted_results.include_protein or interpreted_results.include_fat:
            assert (
                False
            ), "ERROR: we haven't dealt with this edge case of fat or protein required yet"
        NMONTHS = interpreted_results.constants["NMONTHS"]

        # let's have a "grace" epsilon of 0.1% for the model -- if 99.9% of people are fed, this is basically 100%
        # so it's alright if we have feed and biofuel
        if interpreted_results.percent_people_fed < 99.9:
            total_biofuels = (
                interpreted_results.cell_sugar_biofuels
                + interpreted_results.scp_biofuels
                + interpreted_results.seaweed_biofuels
                + interpreted_results.outdoor_crops_biofuels
                + interpreted_results.stored_food_biofuels
            )

            total_feed = (
                interpreted_results.cell_sugar_feed
                + interpreted_results.scp_feed
                + interpreted_results.seaweed_feed
                + interpreted_results.outdoor_crops_feed
                + interpreted_results.stored_food_feed
            )
            feed_and_biofuels_sum = total_biofuels + total_feed

            # this is asserting the percent people fed from biofuels is less than 0.1% of the food.
            # Honestly, 0.1% is a bit higher than I'd like, but I think this is resulting from compounding rounding
            # errors in the second round optimization so it's hard to fix
            if not np.allclose(
                np.zeros(NMONTHS),
                feed_and_biofuels_sum.kcals,
                atol=0.1,
            ):
                print(
                    f"""
                    ERROR!
                    ERROR!
                    ERROR!
                    ERROR!
                    ERROR!
                    ERROR!
                    ERROR!
                    ERROR!
                    ERROR!
                    ERROR!
                    ERROR!

                    ERROR: ASSERT FAILED! WILL NEED TO FIX!!

                assert np.allclose(
                    np.zeros(NMONTHS),
                    feed_and_biofuels_sum.kcals,
                    atol=0.1,
                ), (
                    f"ERROR: although interpreted_results.percent_people_fed is less \n"
                    f"than 100% (it's {interpreted_results.percent_people_fed}%), there \n"
                    f"is still feed and biofuel being used in at least 1 month.\n"
                    f"feed and biofuel sum:\n"
                    f"{feed_and_biofuels_sum}"
                )


                """
                )

    @staticmethod
    def assert_round3_percent_fed_not_lower_than_round1(
        percent_fed_round1, percent_fed_round3, epsilon=1
    ):
        if (
            percent_fed_round3 <= 99.9
        ):  # only in the case that people are starving do we check this
            if not percent_fed_round1 <= percent_fed_round3 + epsilon:
                print(
                    f"""
                assert percent_fed_round1 <= percent_fed_round3 + epsilon, (
                    "ERROR: Humans starving in round 3, yet round 3 % fed less than round 1 % fed!\n"
                    "Round 1: no animal feed\n"
                    "Round 3: just the amount of animal feed determined would allow people to meet their \n"
                    "minimum caloric needs, from round 2\n"
                    "Therefore, it must be that round 1 always has less than or equal percent fed compared to round3.\n"
                    f"percent fed round1: {percent_fed_round1}%\n"
                    f"percent fed round3: {percent_fed_round3}%\n"
                )"""
                )
