"""
Optimizer Model
In this model, we estimate the macronutrient production allocated optimally
over time including models for traditional and resilient foods.
"""
from datetime import time
import pulp
import numpy as np
from pulp import LpMaximize, LpMinimize, LpProblem, LpVariable, LpConstraint


class Optimizer:
    def __init__(self, single_valued_constants, time_consts):
        """
        Initializes an instance of the Optimizer class with the given constants.

        Args:
            single_valued_constants (dict): A dictionary containing single-valued constants.
            time_consts (dict): A dictionary containing time constants.

        Returns:
            None
        """
        # Set the single-valued constants and time constants as instance variables
        self.single_valued_constants = single_valued_constants
        self.time_consts = time_consts

        # Set the number of months as an instance variable
        self.NMONTHS = single_valued_constants["NMONTHS"]

        # Load the variable names and prefixes as instance variables
        self.initial_variables = self.load_variable_names_and_prefixes()

    def optimize_nonhuman_consumption(self, single_valued_constants, time_consts):
        variables = self.initial_variables.copy()
        # Create the model to optimize
        model = LpProblem(name="optimization_animals", sense=LpMaximize)

        resource_constants = {
            "ADD_SEAWEED": {
                "prefixes": self.seaweed_prefixes,
                "function": self.add_seaweed_to_model,
            },
            "ADD_OUTDOOR_GROWING": {
                "prefixes": self.crops_food_prefixes,
                "function": self.add_outdoor_crops_to_model,
            },
            "ADD_STORED_FOOD": {
                "prefixes": self.stored_food_prefixes,
                "function": self.add_stored_food_to_model,
            },
            "ADD_CULLED_MEAT": {
                "prefixes": self.culled_meat_prefixes,
                "function": self.add_culled_meat_to_model,
            },
            "ADD_METHANE_SCP": {
                "prefixes": self.methane_scp_prefixes,
                "function": self.add_methane_scp_to_model,
            },
            "ADD_CELLULOSIC_SUGAR": {
                "prefixes": self.cell_sugar_prefixes,
                "function": self.add_cellulosic_sugar_to_model,
            },
        }

        (
            model,
            variables,
            maximize_constraints,
        ) = self.add_variables_and_constraints_to_model(
            model, variables, resource_constants, single_valued_constants
        )

    def optimize_to_humans(self, single_valued_constants, time_consts):
        """
        This function optimizes the model to maximize the amount of food produced for humans.
        Args:
            single_valued_constants (dict): A dictionary containing single-valued constants
            time_consts (dict): A dictionary containing time-related constants

        Returns:
            tuple: A tuple containing the following:
                - model (LpProblem): The model to optimize
                - variables (dict): A dictionary containing the variables in the model
                - maximize_constraints (list): A list of constraints to maximize

        """

        # Create the model to optimize
        model = LpProblem(name="optimization_nutrition", sense=LpMaximize)

        # Create a copy of the initial variables
        variables = self.initial_variables.copy()

        # Define the resource constants
        resource_constants = {
            "ADD_SEAWEED": {
                "prefixes": self.seaweed_prefixes,
                "function": self.add_seaweed_to_model,
            },
            "ADD_OUTDOOR_GROWING": {
                "prefixes": self.crops_food_prefixes,
                "function": self.add_outdoor_crops_to_model,
            },
            "ADD_STORED_FOOD": {
                "prefixes": self.stored_food_prefixes,
                "function": self.add_stored_food_to_model,
            },
            "ADD_CULLED_MEAT": {
                "prefixes": self.culled_meat_prefixes,
                "function": self.add_culled_meat_to_model,
            },
            "ADD_METHANE_SCP": {
                "prefixes": self.methane_scp_prefixes,
                "function": self.add_methane_scp_to_model,
            },
            "ADD_CELLULOSIC_SUGAR": {
                "prefixes": self.cell_sugar_prefixes,
                "function": self.add_cellulosic_sugar_to_model,
            },
        }

        # Add variables and constraints to the model
        NMONTHS = single_valued_constants["NMONTHS"]
        (
            model,
            variables,
            maximize_constraints,
        ) = self.add_variables_and_constraints_to_model(
            model, variables, resource_constants, single_valued_constants
        )

        # Run optimizations to maximize food production for humans
        self.run_optimizations_to_humans(model, variables, single_valued_constants)

        # Return the model, variables, maximize_constraints, single_valued_constants, and time_consts
        return (
            model,
            variables,
            maximize_constraints,
            single_valued_constants,
            time_consts,
        )

    def add_variables_and_constraints_to_model(
        self, model, variables, resource_constants, single_valued_constants
    ):
        """
        This function is utilized for adding variables and constraints to a given optimization model. It operates on resource constants and single valued constants.

        ### Parameters:

        - `model`: A PULP linear programming model object. This model should be already defined but may be in need of decision variables, objective function, and constraints.
        - `variables`: A dictionary object storing decision variables of the model.
        - `resource_constants`: A dictionary object, where each item includes information about a resource, including the prefixes and function for variable and constraint generation.
        - `single_valued_constants`: A dictionary object consisting of constant parameters used throughout the optimization process.

        ### Behavior:

        The function operates in two major steps:

        - First, it loops through each resource in `resource_constants`. If the corresponding key in `single_valued_constants` is set to True, it generates and adds new variables based on the resource prefixes. It then generates and adds constraints to the model for each month in the time horizon (from 0 to NMONTHS), using the function provided with each resource.
        - After adding all resource-based variables and constraints, the function adds objectives to the model for each month in the time horizon. These objectives are added to the `maximize_constraints` list, which is only used for validation.

        The function concludes by adding the objective function (stored under the "objective_function" key in the `variables` dictionary) to the model.

        ### Returns:

        This function returns three outputs:

        - `model`: The updated PULP model after adding the variables, constraints, and the objective function.
        - `variables`: The updated dictionary of variables after the function has added new variables.
        - `maximize_constraints`: A list of the objective functions added to the model, used for validation purposes.
        """

        for key, resource in resource_constants.items():
            if single_valued_constants[key]:
                prefixes = resource["prefixes"]
                func = resource["function"]
                variables = self.add_variable_from_prefixes(variables, prefixes)
                for month in range(0, self.NMONTHS):
                    conditions = func(month, variables)
                    model = self.add_conditions_to_model(model, month, conditions)

        maximize_constraints = []  # used only for validation
        for month in range(0, self.NMONTHS):
            [model, variables, maximize_constraints] = self.add_objectives_to_model(
                model, variables, month, maximize_constraints
            )
        model += variables["objective_function"]

        return model, variables, maximize_constraints

    def run_optimizations_to_humans(self, model, variables, single_valued_constants):
        """
        This function is part of a resource allocation system aiming to model systems which minimize starvation.

        The function executes a series of optimization steps. After solving the initial model, it performs several more rounds of optimization, each with added constraints based on the results of the previous round.

        Here's a brief overview of the operations it performs:

        - It first solves the initial model and asserts that the optimization was successful.
        - It then constrains the next optimization to have the same minimum starvation as the previous optimization.
        - If the first optimization was successful, it optimizes the best food consumption that goes to humans.
        - After that, it constrains the next optimization to have the same total resilient foods in feed as the previous optimization.
        - If the first optimization was successful and if food storage between years is allowed, it further optimizes to reduce fluctuations in food distribution.

        Args:
            self : The optimizer object.
            model : A PULP linear programming model object. This model should be already defined and configured.
            variables : A dictionary containing the variables used in the optimization.
            single_valued_constants: A dictionary of constant parameters that are used throughout the optimization process.

        """
        # Set this to True to print PULP messages
        PRINT_PULP_MESSAGES = False

        # Solve the initial model
        status = model.solve(
            pulp.PULP_CBC_CMD(gapRel=0.0001, msg=PRINT_PULP_MESSAGES, fracGap=0.001)
        )

        # Assert that the optimization was successful
        ASSERT_SUCCESSFUL_OPTIMIZATION = True
        if ASSERT_SUCCESSFUL_OPTIMIZATION:
            assert status == 1, "ERROR: OPTIMIZATION FAILED!"

        # Constrain the next optimization to have the same minimum starvation as the previous optimization
        (
            model,
            variables,
        ) = self.constrain_next_optimization_to_have_same_minimum_starvation(
            model, variables
        )

        # If the first optimization was successful, optimize the best food consumption that goes to humans
        if status == 1:
            model, variables = self.optimize_best_food_consumption_to_go_to_humans(
                model,
                variables,
                ASSERT_SUCCESSFUL_OPTIMIZATION,
                single_valued_constants,
            )

        # Constrain the next optimization to have the same total resilient foods in feed as the previous optimization
        (
            model,
            variables,
        ) = self.constrain_next_optimization_to_have_same_total_resilient_foods_in_feed(
            model, variables
        )

        # If the first optimization was successful and if food storage between years is allowed, further optimize to reduce fluctuations in food distribution
        if status == 1 and self.single_valued_constants["STORE_FOOD_BETWEEN_YEARS"]:
            model, variables = self.reduce_fluctuations_with_a_final_optimization(
                model,
                variables,
                ASSERT_SUCCESSFUL_OPTIMIZATION,
                single_valued_constants,
            )

    def constrain_next_optimization_to_have_same_total_resilient_foods_in_feed(
        self, model_max_to_humans, variables
    ):
        """
        Constrains the next optimization to have the same total resilient foods in feed as the previous optimization.
        Args:
            model_max_to_humans (tuple): A tuple containing the model and the maximizer string.
            variables (dict): A dictionary containing the variables used in the optimization.

        Returns:
            tuple: A tuple containing the updated model and variables.
        """
        # Initialize variables
        scp_sum = 0
        cell_sugar_sum = 0
        seaweed_sum = 0
        total_feed_biofuel_variable_for_constraint = 0
        maximizer_string = "Crops_And_Stored_Food_Optimization_Averaged_Objective"

        # Loop through each month
        for month in range(0, self.NMONTHS):
            # Calculate the sum of methane_scp_feed and methane_scp_biofuel
            scp_sum = (
                variables["methane_scp_feed"][month].varValue
                + variables["methane_scp_biofuel"][month].varValue
                if hasattr(variables["methane_scp_feed"][month], "varValue")
                else 0
            )
            # Calculate the sum of cellulosic_sugar_feed and cellulosic_sugar_biofuel
            cell_sugar_sum = (
                variables["cellulosic_sugar_feed"][month].varValue
                + variables["cellulosic_sugar_biofuel"][month].varValue
                if hasattr(variables["cellulosic_sugar_feed"][month], "varValue")
                else 0
            )
            # Calculate the sum of seaweed_feed and seaweed_biofuel
            seaweed_sum = (
                variables["seaweed_feed"][month].varValue
                + variables["seaweed_biofuel"][month].varValue
                if hasattr(variables["seaweed_feed"][month], "varValue")
                else 0
            )
            # Calculate the total feed biofuel variable for constraint
            total_feed_biofuel_variable_for_constraint += (
                variables["methane_scp_feed"][month]
                + variables["methane_scp_biofuel"][month]
                + variables["cellulosic_sugar_feed"][month]
                + variables["cellulosic_sugar_biofuel"][month]
                + variables["seaweed_feed"][month]
                + variables["seaweed_biofuel"][month]
            ) / self.NMONTHS >= (
                scp_sum + cell_sugar_sum + seaweed_sum
            ) / self.NMONTHS * 0.9999

        # Add the constraint to the model
        model_max_to_humans += (
            variables["objective_function_best_to_humans"]
            <= total_feed_biofuel_variable_for_constraint,
            maximizer_string,
        )

        return model_max_to_humans, variables

    def add_conditions_to_model(self, model, month, conditions):
        """
        Adds conditions to a given model for a given month.

        Args:
            model (Pulp ): The model to which the conditions will be added.
            month (str): The month for which the conditions will be added.
            conditions (dict): A dictionary containing the conditions to be added to the model.

        Returns:
            LpProblem: The updated model with the added conditions.

        Example:
            >>> model = LpProblem(name="optimization_animals", sense=LpMaximize)
            >>> conditions = {'condition1': 'x > 0', 'condition2': 'y < 10'}
            >>> updated_model = add_conditions_to_model(model, 'January', conditions)
        """
        # Iterate over the conditions and add them to the model
        for prefix, condition in conditions.items():
            # Create a constraint with the given condition and a name based on the prefix and month
            constraint = (condition, f"{prefix}_{month}_Constraint")
            # Add the constraint to the model
            model += constraint

        # Return the updated model
        return model

    def load_variable_names_and_prefixes(self):
        """
        This function initializes a dictionary of variable names and prefixes, and returns it.
        Args:
            self: instance of the Optimizer class
        Returns:
            variables (dict): a dictionary containing variable names and prefixes
        """
        variables = {}

        # Add objective function variable to the dictionary
        variables["objective_function"] = LpVariable(
            name="Least_Humans_Fed_Any_Month", lowBound=0
        )

        # Initialize prefixes for different types of variables
        self.stored_food_prefixes = [
            "Stored_Food_Start",
            "Stored_Food_End",
            "Stored_Food_To_Humans",
            "Stored_Food_Feed",
            "Stored_Food_Biofuel",
        ]
        self.methane_scp_prefixes = [
            "Methane_SCP_To_Humans",
            "Methane_SCP_Feed",
            "Methane_SCP_Biofuel",
        ]
        self.cell_sugar_prefixes = [
            "Cellulosic_Sugar_To_Humans",
            "Cellulosic_Sugar_Feed",
            "Cellulosic_Sugar_Biofuel",
        ]
        self.culled_meat_prefixes = [
            "Culled_Meat_Start",
            "Culled_Meat_End",
            "Culled_Meat_Eaten",
        ]
        self.crops_food_prefixes = [
            "Crops_Food_Storage",
            "Crops_Food_Eaten",
            "Crops_Food_Eaten_Fat",
            "Crops_Food_Eaten_Protein",
            "Crops_Food_To_Humans",
            "Crops_Food_Feed",
            "Crops_Food_Biofuel",
            "Crops_Food_To_Humans_Fat",
            "Crops_Food_Feed_Fat",
            "Crops_Food_Biofuel_Fat",
            "Crops_Food_To_Humans_Protein",
            "Crops_Food_Feed_Protein",
            "Crops_Food_Biofuel_Protein",
        ]
        self.seaweed_prefixes = [
            "Seaweed_Wet_On_Farm",
            "Seaweed_To_Humans",
            "Seaweed_Feed",
            "Seaweed_Biofuel",
            "Used_Area",
        ]

        # Combine all prefixes into a nested list
        nested_list = [
            self.stored_food_prefixes,
            self.methane_scp_prefixes,
            self.cell_sugar_prefixes,
            self.culled_meat_prefixes,
            self.crops_food_prefixes,
            self.seaweed_prefixes,
        ]

        # Flatten the nested list
        flattened_list = [item for sublist in nested_list for item in sublist]

        # Add all variable names to the dictionary with initial values of 0 for each month
        for camel_case_variable_name in flattened_list:
            # these will be overwritten if the variable is used
            variables[camel_case_variable_name.lower()] = [0] * self.NMONTHS

        # Add consumed_kcals, consumed_fat, and consumed_protein variables to the dictionary with initial values of 0 for each month
        variables["consumed_kcals"] = [0] * self.NMONTHS
        variables["consumed_fat"] = [0] * self.NMONTHS
        variables["consumed_protein"] = [0] * self.NMONTHS

        # Return the dictionary of variable names and prefixes
        return variables

    def optimize_best_food_consumption_to_go_to_humans(
        self,
        model,
        variables,
        ASSERT_SUCCESSFUL_OPTIMIZATION,
        single_valued_constants,
    ):
        """
        This function optimizes the amount of food to be allocated to humans while ensuring that the minimum demands for feed and biofuel are met.
        Args:
            self: instance of the Optimizer class
            model: the model to be optimized
            variables: dictionary of variables used in the model
            ASSERT_SUCCESSFUL_OPTIMIZATION: assertion to check if optimization was successful
            single_valued_constants: dictionary of constants used in the model
        Returns:
            tuple: a tuple containing the optimized model and the updated variables dictionary
        """

        # Create a copy of the model to optimize
        model_max_to_humans = model

        # Set the optimization sense to maximize
        model_max_to_humans.sense = LpMaximize

        # Create a variable to represent the objective function
        variables["objective_function_best_to_humans"] = LpVariable(
            name="TO_HUMANS_OBJECTIVE", lowBound=0
        )

        # Create a string to represent the maximizer
        maximizer_string = "Crops_And_Stored_Food_Optimization_Averaged"

        # Calculate the total feed and biofuel variable
        total_feed_biofuel_variable = 0
        for month in range(0, self.NMONTHS):
            total_feed_biofuel_variable += (
                variables["methane_scp_feed"][month]
                + variables["methane_scp_biofuel"][month]
                + variables["cellulosic_sugar_feed"][month]
                + variables["cellulosic_sugar_biofuel"][month]
                + variables["seaweed_feed"][month]
                + variables["seaweed_biofuel"][month]
            ) / self.NMONTHS

        # Add the objective function to the model
        model_max_to_humans += (
            variables["objective_function_best_to_humans"]
            <= total_feed_biofuel_variable,
            maximizer_string,
        )

        # Set the objective of the model to the objective function variable
        model_max_to_humans.setObjective(variables["objective_function_best_to_humans"])

        # Solve the model using the PULP_CBC_CMD solver
        status = model_max_to_humans.solve(
            pulp.PULP_CBC_CMD(gapRel=0.0001, msg=True, fracGap=0.001)
        )

        # Check if optimization was successful
        assert status == 1, "ERROR: OPTIMIZATION FAILED!"

        # Return the optimized model and updated variables dictionary
        return model_max_to_humans, variables

    def reduce_fluctuations_with_a_final_optimization(
        self,
        model,
        variables,
        ASSERT_SUCCESSFUL_OPTIMIZATION,
        single_valued_constants,
    ):
        """
        Optimize the smoothing objective function to reduce fluctuations in the model.

        Args:
            model (pulp.LpProblem): The model to optimize.
            variables (dict): A dictionary of variables used in the model.
            ASSERT_SUCCESSFUL_OPTIMIZATION (bool): A flag to assert if optimization was successful.
            single_valued_constants (dict): A dictionary of constants used in the model.

        Returns:
            tuple: A tuple containing the optimized model and the updated variables dictionary.
        """

        # Create a copy of the model to optimize
        model_smoothing = model.copy()

        # Set the sense of the model to minimize
        model_smoothing.sense = LpMinimize

        # Create a variable for the smoothing objective function
        smoothing_obj = LpVariable(name="SMOOTHING_OBJECTIVE", lowBound=0)

        # Add the smoothing objective function to the variables dictionary
        variables["objective_function_smoothing"] = smoothing_obj

        # Add constraints for culled meat eaten
        for month in range(self.NMONTHS):
            if single_valued_constants["ADD_CULLED_MEAT"]:
                constraint_name = f"Smoothing_Culled_{month}_Objective_Constraint"

                # Add positive constraint for culled meat eaten
                model_smoothing += (
                    smoothing_obj >= variables["culled_meat_eaten"][month] * 0.9999,
                    constraint_name + "_Pos",
                )

                # Add negative constraint for culled meat eaten
                model_smoothing += (
                    smoothing_obj >= -variables["culled_meat_eaten"][month] * 0.9999,
                    constraint_name + "_Neg",
                )

        # Add constraints for stored food to humans
        for month in range(3, self.NMONTHS):
            if single_valued_constants["ADD_STORED_FOOD"]:
                constraint_name = f"Smoothing_Stored_{month}_Objective_Constraint"

                # Add positive constraint for stored food to humans
                model_smoothing += (
                    smoothing_obj >= variables["stored_food_to_humans"][month] * 0.9999,
                    constraint_name + "_Pos",
                )

        # Set the objective of the model to the smoothing objective function
        model_smoothing.setObjective(smoothing_obj)

        # Solve the model using the PULP_CBC_CMD solver
        status = model_smoothing.solve(
            pulp.PULP_CBC_CMD(gapRel=0.0001, msg=False, fracGap=0.001)
        )

        # Assert if optimization was successful
        if ASSERT_SUCCESSFUL_OPTIMIZATION:
            assert status == 1, "ERROR: OPTIMIZATION FAILED!"

        # Return the optimized model and the updated variables dictionary
        return model_smoothing, variables

    def constrain_next_optimization_to_have_same_minimum_starvation(
        self, model, variables
    ):
        """
        This function constrains the next optimization to have the same minimum starvation
        as the previous optimization. It does this by setting the minimum value to the
        previous optimization value and ensuring that consumed_kcals meets this value each month.

        Args:
            self (Optimizer): The Optimizer object.
            model (pulp.LpProblem): The optimization model.
            variables (dict): A dictionary of variables used in the optimization.

        Returns:
            tuple: A tuple containing the updated optimization model and variables.

        Example:
            >>> model, variables = constrain_next_optimization_to_have_same_minimum_starvation(
            ...     self, model, variables
            ... )
        """

        # Set min_value to the previous optimization value and make sure consumed_kcals meets this value each month
        min_value = (
            model.objective.value() * 0.9999
        )  # reach almost the same as objective, but allow for small rounding error if needed

        # Add the constraint for consumed_kcals each month
        for month in range(0, self.NMONTHS):
            maximizer_string = (
                "Old_Objective_Month_" + str(month) + "_Objective_Constraint"
            )

            model += (
                min_value <= variables["consumed_kcals"][month],
                maximizer_string,
            )

            # Add the constraint for consumed_fat each month if INCLUDE_FAT is True
            if self.single_valued_constants["inputs"]["INCLUDE_FAT"]:
                maximizer_string = (
                    "Old_Fat_Objective_Month_" + str(month) + "_Objective_Constraint"
                )

                model += (
                    variables["objective_function"] <= variables["consumed_fat"][month],
                    maximizer_string,
                )

            # Add the constraint for consumed_protein each month if INCLUDE_PROTEIN is True
            if self.single_valued_constants["inputs"]["INCLUDE_PROTEIN"]:
                maximizer_string = (
                    "Old_Protein_Objective_Month_"
                    + str(month)
                    + "_Objective_Constraint"
                )

                model += (
                    variables["objective_function"]
                    <= variables["consumed_protein"][month],
                    maximizer_string,
                )

        return model, variables

    def create_lp_variables(self, prefix, month):
        """
        Create a pulp variable with a given prefix and month.
        Args:
            prefix (str): A string prefix for the variable name.
            month (int): An integer representing the month for the variable name.
        Returns:
            pulp.LpVariable: A pulp variable with a given name and lower bound of 0.
        """
        # Create a variable name based on the prefix and month.
        variable_name = f"{prefix}_Month_{month}_Variable"

        # Create a pulp variable with the given name and lower bound of 0.
        return LpVariable(variable_name, lowBound=0)

    def add_constraints(self, model, month, condition, prefix):
        """
        Adds a constraint to the given model based on the given condition, month, and prefix.
        Args:
            model (Model): The model to which the constraint will be added.
            month (str): The month to which the constraint applies.
            condition (str): The condition that the constraint enforces.
            prefix (str): The prefix to use in the constraint name.
        Returns:
            Model: The updated model with the added constraint.
        """
        # Create the constraint using the given condition and prefix
        constraint = (condition, f"{prefix}_{month}_Constraint")
        # Add the constraint to the model
        model += constraint
        # Return the updated model
        return model

    def add_variable_from_prefixes(self, variables, prefixes):
        """
        Adds variables to the LP problem for each prefix and month.

        Args:
            variables (dict): A dictionary containing the LP variables for each prefix and month.
            prefixes (list): A list of prefixes for which variables need to be added.

        Returns:
            dict: A dictionary containing the updated LP variables for each prefix and month.

        Example:
            >>> variables = {'prefix1': [var1, var2, var3], 'prefix2': [var4, var5, var6]}
            >>> prefixes = ['prefix3', 'prefix4']
            >>> add_variable_from_prefixes(variables, prefixes)
            {'prefix1': [var1, var2, var3], 'prefix2': [var4, var5, var6], 'prefix3': [var7, var8, var9], 'prefix4': [var10, var11, var12]}
        """
        # Loop through each month
        for month in range(0, self.NMONTHS):
            # Loop through each prefix
            for prefix in prefixes:
                # Create a new LP variable for the prefix and month
                variable = self.create_lp_variables(prefix, month)
                # Add the variable to the dictionary of LP variables
                variables[prefix.lower()][month] = variable
        # Return the updated dictionary of LP variables
        return variables

    def add_seaweed_to_model(self, month, variables):
        """
        Adds seaweed to the model by setting conditions for the seaweed wet on farm, used area, and other variables.
        Args:
            month (int): the current month of the simulation
            variables (dict): a dictionary containing the current values of the variables in the simulation
        Returns:
            dict: a dictionary containing the conditions for the seaweed wet on farm, used area, and other variables
        """

        # Initialize the conditions dictionary
        conditions = {}

        # Get the initial seaweed, maximum density, built area, and initial built seaweed area
        initial_seaweed = self.single_valued_constants["INITIAL_SEAWEED"]
        max_density = self.single_valued_constants["MAXIMUM_DENSITY"]
        built_area = self.time_consts["built_area"][month]
        initial_built_area = self.single_valued_constants["INITIAL_BUILT_SEAWEED_AREA"]

        # Set the conditions for the seaweed wet on farm, used area, and other variables
        conditions["Seaweed_Wet_On_Farm_Lowerbound"] = (
            initial_seaweed <= variables["seaweed_wet_on_farm"][month]
        )
        conditions["Seaweed_Wet_On_Farm_Upperbound"] = (
            variables["seaweed_wet_on_farm"][month] <= max_density * built_area
        )
        conditions["Used_Area_Lowerbound"] = (
            variables["used_area"][month] >= initial_built_area
        )
        conditions["Used_Area_Upperbound"] = variables["used_area"][month] <= built_area

        # Additional conditions for the first month and later months
        if month == 0:
            conditions["Seaweed_Wet_On_Farm"] = (
                variables["seaweed_wet_on_farm"][0] == initial_seaweed
            )
            conditions["Used_Area"] = variables["used_area"][0] == initial_built_area
            conditions["Seaweed_To_Humans"] = variables["seaweed_to_humans"][0] == 0
            conditions["Seaweed_Feed"] = variables["seaweed_feed"][0] == 0
            conditions["Seaweed_Biofuel"] = variables["seaweed_biofuel"][0] == 0

        else:
            # Calculate intermediate values to simplify the condition
            prev_seaweed = variables["seaweed_wet_on_farm"][month - 1]
            growth_rate = self.time_consts["growth_rates_monthly"][month] / 100.0
            humans_consumed = variables["seaweed_to_humans"][month]
            feed_consumed = variables["seaweed_feed"][month]
            biofuel_consumed = variables["seaweed_biofuel"][month]
            prev_used_area = variables["used_area"][month - 1]
            curr_used_area = variables["used_area"][month]
            harvest_loss = self.single_valued_constants["HARVEST_LOSS"] / 100.0
            min_density = self.single_valued_constants["MINIMUM_DENSITY"]

            # Set the condition for the seaweed wet on farm
            conditions["Seaweed_Wet_On_Farm"] = (
                variables["seaweed_wet_on_farm"][month]
                == prev_seaweed * (1 + growth_rate)
                - humans_consumed
                - feed_consumed
                - biofuel_consumed
                - (curr_used_area - prev_used_area) * min_density * harvest_loss
            )

        # Return the conditions dictionary
        return conditions

    def add_stored_food_to_model_only_first_year(self, month, variables):
        """
        Adds stored food to the model for the first year only.
        Args:
            month (int): the current month of the simulation
            variables (dict): a dictionary containing the variables of the simulation
        Returns:
            dict: a dictionary containing the conditions for the simulation
        """
        # Initialize an empty dictionary to store the conditions
        conditions = {}

        # Get the maximum number of kcals of stored food available
        max_kcals = self.single_valued_constants["stored_food"].initial_available.kcals

        # If it's the first month of the simulation
        if month == 0:
            # Add the condition that the stored food at the start of the simulation is equal to the maximum kcals available
            conditions["Stored_Food_Start"] = (
                variables["stored_food_start"][0] == max_kcals
            )
            # Add the condition that the stored food eaten in the first month is equal to the difference between the stored food at the start of the month and the food used for humans, feed, and biofuel
            conditions["Stored_Food_Eaten"] = (
                variables["stored_food_end"][0]
                == variables["stored_food_start"][0]
                - variables["stored_food_to_humans"][0]
                - variables["stored_food_feed"][0]
                - variables["stored_food_biofuel"][0]
            )

        # If it's after the first year of the simulation
        elif month > 12:
            # Add the condition that all stored food prefixes after the second one are equal to 0
            for prefix in self.stored_food_prefixes[2:]:
                conditions[prefix] = variables[prefix][month] == 0

        # If it's within the first year of the simulation
        else:
            # Add the condition that the stored food eaten in the current month is equal to the difference between the stored food at the start of the month and the food used for humans, feed, and biofuel
            conditions["Stored_Food_Eaten"] = (
                variables["stored_food_end"][month]
                == variables["stored_food_start"][month]
                - variables["stored_food_to_humans"][month]
                - variables["stored_food_feed"][month]
                - variables["stored_food_biofuel"][month]
            )

        # Return the dictionary containing the conditions
        return conditions

    def add_stored_food_to_model(self, month, variables):
        if not self.single_valued_constants["STORE_FOOD_BETWEEN_YEARS"]:
            return self.add_stored_food_to_model_only_first_year(month, variables)

        conditions = {}

        if month == 0:  # first Month
            conditions["Stored_Food_Start"] = (
                variables["stored_food_start"][0]
                == self.single_valued_constants["stored_food"].initial_available.kcals
            )

        elif month == self.NMONTHS - 1:  # last month
            conditions["Stored_Food_End"] = variables["stored_food_end"][month] == 0
            conditions["Stored_Food_Start"] = (
                variables["stored_food_start"][month]
                == variables["stored_food_end"][month - 1]
            )

        else:
            conditions["Stored_Food_Start"] = (
                variables["stored_food_start"][month]
                == variables["stored_food_end"][month - 1]
            )

        conditions["Stored_Food_Eaten"] = (
            variables["stored_food_end"][month]
            == variables["stored_food_start"][month]
            - variables["stored_food_to_humans"][month]
            - variables["stored_food_feed"][month]
            - variables["stored_food_biofuel"][month]
        )

        return conditions

    def add_culled_meat_to_model(self, month, variables):
        """
        This function adds culled meat to the model based on the month and variables passed in.
        Args:
            month (int): The month for which the culled meat is being added
            variables (dict): A dictionary containing variables related to culled meat

        Returns:
            dict: A dictionary containing conditions related to culled meat

        Example:
            >>> optimizer = Optimizer()
            >>> variables = {
            ...     "culled_meat_start": [10, 20, 30],
            ...     "culled_meat_end": [20, 30, 40],
            ...     "culled_meat_eaten": [5, 10, 15]
            ... }
            >>> optimizer.add_culled_meat_to_model(1, variables)
            {'Culled_Meat_Start': True, 'Culled_Meat_Eaten': 10}
        """
        conditions = {}

        if month == 0:  # first Month
            # Check if the culled meat start value is equal to the constant value
            conditions["Culled_Meat_Start"] = (
                variables["culled_meat_start"][0]
                == self.single_valued_constants["culled_meat"]
            )
        else:
            # Check if the culled meat start value is equal to the culled meat end value of the previous month
            conditions["Culled_Meat_Start"] = (
                variables["culled_meat_start"][month]
                == variables["culled_meat_end"][month - 1]
            )

        # Calculate the amount of culled meat eaten in the month
        conditions["Culled_Meat_Eaten"] = (
            variables["culled_meat_end"][month]
            == variables["culled_meat_start"][month]
            - variables["culled_meat_eaten"][month]
        )

        return conditions

    def add_outdoor_crops_to_model_no_storage(self, month, variables):
        """
        Adds a condition to the model that checks if the crops food storage is zero for a given month.
        Args:
            month (int): The month to check the crops food storage for.
            variables (dict): A dictionary containing the variables used in the model.

        Returns:
            dict: A dictionary containing the condition to be added to the model.

        Example:
            >>> variables = {"crops_food_storage": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}
            >>> add_outdoor_crops_to_model_no_storage(3, variables)
            {'Crops_Food_Storage_Zero': True}
        """
        # Create a dictionary containing the condition to be added to the model
        conditions = {
            "Crops_Food_Storage_Zero": variables["crops_food_storage"][month] == 0
        }
        # Return the dictionary containing the condition
        return conditions

    def handle_first_month(self, variables, month):
        """
        This function handles the first month of the simulation. It checks if the crops food storage is equal to the
        outdoor crops production minus the crops food eaten. If this condition is met, it returns a dictionary with the
        condition as a key and True as a value.
        Args:
            self (Optimizer): the instance of the Optimizer class
            variables (dict): a dictionary containing the variables used in the simulation
            month (int): the current month of the simulation
        Returns:
            dict: a dictionary containing the condition as a key and True as a value if the condition is met
        """
        # Define the condition to check
        conditions = {
            "Crops_Food_Storage": (
                variables["crops_food_storage"][month]
                == self.time_consts["outdoor_crops"].production.kcals[month]
                - variables["crops_food_eaten"][month]
            )
        }
        # Return the dictionary with the condition and its value
        return conditions

    def handle_last_month(
        self, variables, month, use_relocated_crops, initial_harvest_duration
    ):
        if use_relocated_crops:
            assert (
                month > initial_harvest_duration
            ), """ERROR: In relocated case, you need to have a scenario at least 1 harvest duration long,
                right now it is this many months for harvest duration:""" + str(
                initial_harvest_duration
            )

        conditions = {
            "Crops_Food_None_Left": variables["crops_food_storage"][month] == 0,
            "Crops_Food_Storage": (
                variables["crops_food_storage"][month]
                == self.time_consts["outdoor_crops"].production.kcals[month]
                + variables["crops_food_storage"][month - 1]
                - variables["crops_food_eaten"][month]
            ),
        }
        return conditions

    def handle_other_months(self, variables, month, use_relocated_crops):
        """
        This function handles months that are not January or July. It calculates the conditions for the month based on the
        variables passed in and returns them.

        Args:
            variables (dict): A dictionary containing variables for the simulation
            month (int): The current month of the simulation
            use_relocated_crops (bool): A boolean indicating whether or not to use relocated crops

        Returns:
            dict: A dictionary containing the conditions for the month

        Example:
            >>> variables = {
            ...     "crops_food_storage": [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200],
            ...     "crops_food_eaten": [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120]
            ... }
            >>> month = 2
            >>> use_relocated_crops = False
            >>> optimizer = Optimizer()
            >>> optimizer.handle_other_months(variables, month, use_relocated_crops)
            {'Crops_Food_Storage': True}
        """
        # Calculate the conditions for the month
        conditions = {
            "Crops_Food_Storage": (
                variables["crops_food_storage"][month]
                == self.time_consts["outdoor_crops"].production.kcals[month]
                + variables["crops_food_storage"][month - 1]
                - variables["crops_food_eaten"][month]
            )
        }
        # Return the conditions
        return conditions

    def add_crops_food_eaten_with_nutrient_name(
        self, variables, month, nutrient, lowercase_nutrient
    ):
        conditions = {
            "Crops_Food_Eaten"
            + nutrient: (
                variables["crops_food_eaten" + lowercase_nutrient][month]
                == variables["crops_food_to_humans" + lowercase_nutrient][month]
                + variables["crops_food_biofuel" + lowercase_nutrient][month]
                + variables["crops_food_feed" + lowercase_nutrient][month]
            )
        }
        return conditions

    def create_linear_constraints_for_fat_and_protein_crops_food(
        self, month, variables, fat_multiplier, protein_multiplier
    ):
        """
        This function creates linear constraints for fat and protein crops food.
        Args:
            month (int): The month for which the constraints are being created
            variables (dict): A dictionary containing variables used in the constraints
            fat_multiplier (float): The multiplier for fat
            protein_multiplier (float): The multiplier for protein
        Returns:
            dict: A dictionary containing the created constraints
        """
        # Create an empty dictionary to store the conditions
        conditions = {}

        # Add constraints for crops food eaten without specifying a nutrient name
        conditions.update(
            self.add_crops_food_eaten_with_nutrient_name(variables, month, "", "")
        )

        # Create a dictionary to store the nutrient multipliers
        nutrient_multiplier_dictionary = {
            fat_multiplier: "_Fat",
            protein_multiplier: "_Protein",
        }

        # Loop through the nutrient multiplier dictionary
        for multiplier, nutrient in nutrient_multiplier_dictionary.items():
            # Convert the nutrient name to lowercase
            lowercase_nutrient = nutrient.lower()

            # Add constraints for crops food eaten with a specified nutrient name
            conditions.update(
                self.add_crops_food_eaten_with_nutrient_name(
                    variables, month, nutrient, lowercase_nutrient
                )
            )

            # Loop through the usage types
            for usage_type in ["_Feed", "_Biofuel"]:
                # Convert the usage type to lowercase
                lowercase_usage_type = usage_type.lower()

                # Add a constraint for the crops food eaten conversion
                conditions["Crops_Food_Eaten_Conversion" + usage_type + nutrient] = (
                    variables["crops_food" + lowercase_usage_type + lowercase_nutrient][
                        month
                    ]
                    == variables["crops_food" + lowercase_usage_type][month]
                    * multiplier
                )

        # Return the created conditions
        return conditions

    def get_outdoor_crops_month_constants(self, use_relocated_crops, month):
        """
        Calculates the constants for outdoor crops based on the month and whether or not
        relocated crops are being used. Returns a tuple of the initial harvest duration,
        fat multiplier, and protein multiplier.

        Args:
            use_relocated_crops (bool): Whether or not relocated crops are being used.
            month (int): The current month.

        Returns:
            tuple: A tuple containing the initial harvest duration, fat multiplier, and
            protein multiplier.

        Example:
            >>> get_outdoor_crops_month_constants(True, 5)
            (7, 0.4, 0.3)
        """
        # Calculate the initial harvest duration based on constants
        initial_harvest_duration = (
            self.single_valued_constants["INITIAL_HARVEST_DURATION_IN_MONTHS"]
            + self.single_valued_constants["DELAY"]["ROTATION_CHANGE_IN_MONTHS"]
        )

        # Check if relocated crops are being used and if the month is greater than or equal
        # to the initial harvest duration
        if use_relocated_crops and month >= initial_harvest_duration:
            # If so, use the rotation fraction constants for fat and protein
            fat_multiplier = self.single_valued_constants["OG_ROTATION_FRACTION_FAT"]
            protein_multiplier = self.single_valued_constants[
                "OG_ROTATION_FRACTION_PROTEIN"
            ]
        else:
            # Otherwise, use the original fraction constants for fat and protein
            fat_multiplier = self.single_valued_constants["OG_FRACTION_FAT"]
            protein_multiplier = self.single_valued_constants["OG_FRACTION_PROTEIN"]

        # Return the calculated constants as a tuple
        return (initial_harvest_duration, fat_multiplier, protein_multiplier)

    def add_outdoor_crops_to_model(self, month, variables):
        conditions = {}

        use_relocated_crops = self.single_valued_constants["inputs"][
            "OG_USE_BETTER_ROTATION"
        ]
        (
            initial_harvest_duration,
            fat_multiplier,
            protein_multiplier,
        ) = self.get_outdoor_crops_month_constants(use_relocated_crops, month)

        conditions.update(
            self.create_linear_constraints_for_fat_and_protein_crops_food(
                month, variables, fat_multiplier, protein_multiplier
            )
        )

        if month == 0:
            conditions.update(self.handle_first_month(variables, month))
        elif month == self.NMONTHS - 1:
            conditions.update(
                self.handle_last_month(
                    variables, month, use_relocated_crops, initial_harvest_duration
                )
            )
        else:
            conditions.update(
                self.handle_other_months(variables, month, initial_harvest_duration)
            )

        return conditions

    def add_methane_scp_to_model(self, month, variables):
        """
        Adds the methane SCP (Substrate Coefficient of Production) constraint to the model for a given month.
        The constraint ensures that the total amount of methane SCP from all sources is less than or equal to the
        maximum amount of methane SCP allowed for that month.

        Args:
            month (int): The month for which the constraint is being added.
            variables (dict): A dictionary containing the variables used in the constraint.

        Returns:
            dict: A dictionary containing the methane SCP constraint.

        Example:
            >>> variables = {
            ...     "methane_scp_to_humans": [10, 20, 30],
            ...     "methane_scp_feed": [5, 10, 15],
            ...     "methane_scp_biofuel": [2, 4, 6]
            ... }
            >>> optimizer = Optimizer()
            >>> constraint = optimizer.add_methane_scp_to_model(1, variables)
            >>> print(constraint)
            {'Methane_SCP': True}
        """
        # Calculate the total amount of methane SCP from all sources for the given month
        total_methane_scp = (
            variables["methane_scp_to_humans"][month]
            + variables["methane_scp_feed"][month]
            + variables["methane_scp_biofuel"][month]
        )

        # Create a dictionary containing the methane SCP constraint
        conditions = {
            "Methane_SCP": (
                total_methane_scp <= self.time_consts["methane_scp"].kcals[month]
            )
        }

        return conditions

    def add_cellulosic_sugar_to_model(self, month, variables):
        """
        Adds the amount of cellulosic sugar available in a given month to the model and checks if it is within the
        limit of available kcals for that month.

        Args:
            month (int): The month for which the cellulosic sugar is being added to the model.
            variables (dict): A dictionary containing the variables for the model.

        Returns:
            dict: A dictionary containing the conditions for the model.

        Example:
            >>> variables = {
            ...     "cellulosic_sugar_to_humans": [100, 200, 300],
            ...     "cellulosic_sugar_feed": [50, 100, 150],
            ...     "cellulosic_sugar_biofuel": [25, 50, 75]
            ... }
            >>> optimizer = Optimizer()
            >>> optimizer.add_cellulosic_sugar_to_model(1, variables)
            {'Cellulosic_Sugar': True}
        """
        # Calculate the total amount of cellulosic sugar available in the given month
        total_cellulosic_sugar = (
            variables["cellulosic_sugar_to_humans"][month]
            + variables["cellulosic_sugar_feed"][month]
            + variables["cellulosic_sugar_biofuel"][month]
        )

        # Check if the total amount of cellulosic sugar is within the limit of available kcals for that month
        conditions = {
            "Cellulosic_Sugar": (
                total_cellulosic_sugar
                <= self.time_consts["cellulosic_sugar"].kcals[month]
            )
        }

        return conditions

    def add_percentage_intake_constraints(self, model, variables, month):
        """
        Adds constraints to the optimization model based on the percentage intake of the nonhuman and human diets,
        and the ratio of these resources used as biofuel.

        Args:
            model (object): The optimization model object
            variables (dict): A dictionary of variables used in the optimization model
            month (int): The month for which the constraints are being added

        Returns:
            object: The optimization model object with added constraints
        """

        # Dictionary containing nutrient ratios for different resources
        nutrient_ratios = {
            "Seaweed": self.single_valued_constants["SEAWEED_KCALS"],
            "Methane_SCP": 1,
            "Cellulosic_Sugar": 1,
        }

        # Loop through each nutrient and add constraints based on its usage
        for nutrient, nutrient_kcal_ratio in nutrient_ratios.items():
            if self.single_valued_constants["ADD_" + nutrient.upper()]:
                constraints_data = [
                    (
                        "HUMANS",
                        "MAX_" + nutrient.upper() + "_HUMANS_CAN_CONSUME_MONTHLY",
                        "to_humans",
                    ),
                    (
                        "FEED",
                        "MAX_" + nutrient.upper() + "_AS_PERCENT_KCALS_FEED",
                        "feed",
                    ),
                    (
                        "BIOFUEL",
                        "MAX_" + nutrient.upper() + "_AS_PERCENT_KCALS_BIOFUEL",
                        "biofuel",
                    ),
                ]
                for constraint_type, limit_key, usage in constraints_data:
                    # Calculate the condition for the constraint
                    condition = variables[nutrient.lower() + "_" + usage][
                        month
                    ] * nutrient_kcal_ratio <= (
                        self.single_valued_constants[limit_key]
                        if constraint_type == "HUMANS"
                        else self.single_valued_constants[limit_key]
                        / 100
                        * self.time_consts[usage.lower()].kcals[month]
                    )

                    # Add the constraint to the model
                    model = self.add_constraints(
                        model,
                        month,
                        condition,
                        nutrient + "_Limit_" + constraint_type,
                    )

        return model

    def add_feed_biofuel_to_model(self, model, variables, month):
        """
        Adds feed and biofuel variables to the model for a given month.

        Args:
            model (LpProblem): The LpProblem model to add the variables to.
            variables (dict): A dictionary containing the variables to add to the model.
            month (int): The month for which to add the variables.

        Returns:
            LpProblem: The Pulp model with the added variables.

        Example:
            >>> model = LpProblem()
            >>> variables = {
            ...     "stored_food_feed": [1, 2, 3],
            ...     "crops_food_feed": [4, 5, 6],
            ...     "seaweed_feed": [7, 8, 9],
            ...     "cellulosic_sugar_feed": [10, 11, 12],
            ...     "methane_scp_feed": [13, 14, 15],
            ...     "stored_food_biofuel": [16, 17, 18],
            ...     "crops_food_biofuel": [19, 20, 21],
            ...     "seaweed_biofuel": [22, 23, 24],
            ...     "cellulosic_sugar_biofuel": [25, 26, 27],
            ...     "methane_scp_biofuel": [28, 29, 30],
            ... }
            >>> optimizer = Optimizer()
            >>> optimizer.add_feed_biofuel_to_model(model, variables, 0)
        """
        # Calculate the sum of all feed variables for the given month
        feed_sum = (
            variables["stored_food_feed"][month]
            + variables["crops_food_feed"][month]
            + variables["seaweed_feed"][month]
            * self.single_valued_constants["SEAWEED_KCALS"]
            + variables["cellulosic_sugar_feed"][month]
            + variables["methane_scp_feed"][month]
        )

        # Calculate the sum of all biofuel variables for the given month
        biofuel_sum = (
            variables["stored_food_biofuel"][month]
            + variables["crops_food_biofuel"][month]
            + variables["seaweed_biofuel"][month]
            * self.single_valued_constants["SEAWEED_KCALS"]
            + variables["cellulosic_sugar_biofuel"][month]
            + variables["methane_scp_biofuel"][month]
        )

        # Define the conditions for the feed and biofuel variables
        conditions = {
            "Feed_Used": (feed_sum == self.time_consts["feed"].kcals[month]),
            "Biofuel_Used": (biofuel_sum == self.time_consts["biofuel"].kcals[month]),
        }

        # Add the conditions to the model for the given month
        model = self.add_conditions_to_model(model, month, conditions)

        return model

    # OBJECTIVE FUNCTIONS  #

    def add_objectives_to_model(self, model, variables, month, maximize_constraints):
        """
        Adds objectives to the optimization model.

        Args:
            model (pulp.LpProblem): The optimization model to which objectives are added.
            variables (dict): A dictionary of variables used in the optimization model.
            month (int): The month for which objectives are added.
            maximize_constraints (list): A list of constraints to be maximized.

        Returns:
            list: A list containing the updated model, variables, and maximize_constraints.

        """
        # Add percentage intake constraints to the model
        model = self.add_percentage_intake_constraints(model, variables, month)
        # Add feed biofuel to the model
        model = self.add_feed_biofuel_to_model(model, variables, month)

        # Add variables for consumed kcals, fat, and protein
        variables["consumed_kcals"][month] = LpVariable(
            name="Humans_Fed_Kcals_" + str(month) + "_Variable", lowBound=0
        )
        variables["consumed_fat"][month] = LpVariable(
            name="Humans_Fed_Fat_" + str(month) + "_Variable", lowBound=0
        )
        variables["consumed_protein"][month] = LpVariable(
            name="Humans_Fed_Protein_" + str(month) + "_Variable", lowBound=0
        )

        # Add constraint for consumed kcals
        model += (
            variables["consumed_kcals"][month]
            == (
                variables["stored_food_to_humans"][month]
                + variables["crops_food_to_humans"][month]
                + variables["seaweed_to_humans"][month]
                * self.single_valued_constants["SEAWEED_KCALS"]
                + self.time_consts["grazing_milk_kcals"][month]
                + self.time_consts["cattle_grazing_maintained_kcals"][month]
                + variables["culled_meat_eaten"][month]
                + variables["cellulosic_sugar_to_humans"][month]
                + variables["methane_scp_to_humans"][month]
                + self.time_consts["greenhouse_area"][month]
                * self.time_consts["greenhouse_kcals_per_ha"][month]
                + self.time_consts["fish"].to_humans.kcals[month]
                + self.time_consts["grain_fed_created_kcals"][month]
            )
            / self.single_valued_constants["BILLION_KCALS_NEEDED"]
            * 100,
            "Kcals_Fed_Month_" + str(month) + "_Constraint",
        )

        # Add constraints for consumed fat and protein
        # TODO: PUT BACK IN!
        # if self.single_valued_constants["inputs"]["INCLUDE_FAT"]:
        #     # fat monthly is in units thousand tons
        #     model += (
        #         variables["consumed_fat"][month]
        #         == (
        #             variables["stored_food_eaten"][month]
        #             * self.single_valued_constants["SF_FRACTION_FAT"]
        #             + variables["crops_food_eaten_fat"][month]
        #             + variables["seaweed_to_humans"][month]
        #             * self.single_valued_constants["SEAWEED_FAT"]
        #             + variables["seaweed_feed"][month]
        #             * self.single_valued_constants["SEAWEED_FAT"]
        #             + self.time_consts["grazing_milk_fat"][month]
        #             + self.time_consts["cattle_grazing_maintained_fat"][month]
        #             + variables["culled_meat_eaten"][month]
        #             * self.single_valued_constants["CULLED_MEAT_FRACTION_FAT"]
        #             + variables["methane_scp_to_humans"][month]
        #             * self.single_valued_constants["SCP_KCALS_TO_FAT_CONVERSION"]
        #             + variables["methane_scp_feed"][month]
        #             * self.single_valued_constants["SCP_KCALS_TO_FAT_CONVERSION"]
        #             + self.time_consts["greenhouse_area"][month]
        #             * self.time_consts["greenhouse_fat_per_ha"][month]
        #             + self.time_consts["fish"].to_humans.fat[month]
        #             + self.time_consts["grain_fed_created_fat"][month]
        #             - self.time_consts["nonhuman_consumption"].fat[month]
        #         )
        #         / self.single_valued_constants["THOU_TONS_FAT_NEEDED"]
        #         * 100,
        #         "Fat_Fed_Month_" + str(month) + "_Constraint",
        #     )

        # if self.single_valued_constants["inputs"]["INCLUDE_PROTEIN"]:
        #     model += (
        #         variables["consumed_protein"][month]
        #         == (
        #             variables["stored_food_eaten"][month]
        #             * self.single_valued_constants["SF_FRACTION_PROTEIN"]
        #             + variables["crops_food_eaten_protein"][month]
        #             + variables["seaweed_to_humans"][month]
        #             * self.single_valued_constants["SEAWEED_PROTEIN"]
        #             + variables["seaweed_feed"][month]
        #             * self.single_valued_constants["SEAWEED_PROTEIN"]
        #             + self.time_consts["grazing_milk_protein"][month]
        #             + self.time_consts["cattle_grazing_maintained_protein"][month]
        #             + variables["methane_scp_to_humans"][month]
        #             * self.single_valued_constants["SCP_KCALS_TO_PROTEIN_CONVERSION"]
        #             + variables["methane_scp_feed"][month]
        #             * self.single_valued_constants["SCP_KCALS_TO_PROTEIN_CONVERSION"]
        #             + variables["culled_meat_eaten"][month]
        #             * self.single_valued_constants["CULLED_MEAT_FRACTION_PROTEIN"]
        #             + self.time_consts["greenhouse_area"][month]
        #             * self.time_consts["greenhouse_protein_per_ha"][month]
        #             + self.time_consts["fish"].to_humans.kcals[month]
        #             + self.time_consts["grain_fed_created_protein"][month]
        #             - self.time_consts["nonhuman_consumption"].protein[month]
        #         )
        #         / self.single_valued_constants["THOU_TONS_PROTEIN_NEEDED"]
        #         * 100,
        #         "Protein_Fed_Month_" + str(month) + "_Constraint",
        #     )

        # Add constraint for no feeding human edible maintained meat or milk to animals or biofuels

        # Maximize the minimum objective_function value
        # We maximize the minimum humans fed from any month
        # We therefore maximize the minimum ratio of fat per human requirement,
        # protein per human requirement, or kcals per human requirement
        # for all months

        maximizer_string = "Kcals_Fed_Month_" + str(month) + "_Objective_Constraint"
        maximize_constraints.append(maximizer_string)
        model += (
            variables["objective_function"] <= variables["consumed_kcals"][month],
            maximizer_string,
        )

        if self.single_valued_constants["inputs"]["INCLUDE_FAT"]:
            maximizer_string = "Fat_Fed_Month_" + str(month) + "_Objective_Constraint"
            maximize_constraints.append(maximizer_string)
            model += (
                variables["objective_function"] <= variables["consumed_fat"][month],
                maximizer_string,
            )

        if self.single_valued_constants["inputs"]["INCLUDE_PROTEIN"]:
            maximizer_string = (
                "Protein_Fed_Month_" + str(month) + "_Objective_Constraint"
            )
            maximize_constraints.append(maximizer_string)
            model += (
                variables["objective_function"] <= variables["consumed_protein"][month],
                maximizer_string,
            )

        return [model, variables, maximize_constraints]
