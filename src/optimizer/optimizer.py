"""
Optimizer Model
In this model, we estimate the macronutrient production allocated optimally
over time including models for traditional and resilient foods.
"""
import sys
import pulp
import json
from pulp import LpMaximize, LpMinimize, LpProblem, LpVariable


class Optimizer:
    def __init__(self, consts_for_optimizer, time_consts):
        """
        Initializes an instance of the Optimizer class with the given constants.

        Args:
            consts_for_optimizer (dict): A dictionary containing single-valued constants.
            time_consts (dict): A dictionary containing time constants.

        Returns:
            None
        """
        # Set the single-valued constants and time constants as instance variables
        self.consts_for_optimizer = consts_for_optimizer
        self.time_consts = time_consts

        # Set the number of months as an instance variable
        self.NMONTHS = consts_for_optimizer["NMONTHS"]

        # Load the variable names and prefixes as instance variables
        self.initial_variables = self.load_variable_names_and_prefixes()

        # Define the resource constants
        self.resource_constants = {
            "ADD_SEAWEED": {
                "food_name": "seaweed",
                "prefixes": self.seaweed_prefixes,
                "function": self.add_seaweed_to_model,
            },
            "ADD_OUTDOOR_GROWING": {
                "food_name": "outdoor_crops",
                "prefixes": self.crops_food_prefixes,
                "function": self.add_outdoor_crops_to_model,
            },
            "ADD_STORED_FOOD": {
                "food_name": "stored_food",
                "prefixes": self.stored_food_prefixes,
                "function": self.add_stored_food_to_model,
            },
            "ADD_MEAT": {
                "food_name": "meat",
                "prefixes": self.meat_prefixes,
                "function": self.add_meat_to_model,
            },
            "ADD_METHANE_SCP": {
                "food_name": "methane_scp",
                "prefixes": self.methane_scp_prefixes,
                "function": self.add_methane_scp_to_model,
            },
            "ADD_CELLULOSIC_SUGAR": {
                "food_name": "cellulosic_sugar",
                "prefixes": self.cell_sugar_prefixes,
                "function": self.add_cellulosic_sugar_to_model,
            },
        }

    def optimize_to_humans(self, consts_for_optimizer, time_consts):
        """
        This function optimizes the model to maximize the amount of food produced for humans.
        Args:
            consts_for_optimizer (dict): A dictionary containing single-valued constants
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

        # Add variables and constraints to the model
        (
            model,
            variables,
            maximize_constraints,
        ) = self.add_variables_and_constraints_to_model(
            model,
            variables,
            consts_for_optimizer,
            optimization_type="to_humans",
        )

        # Run optimizations to maximize food production for humans
        percent_fed_from_model = self.run_optimizations_on_constraints(
            model, variables, consts_for_optimizer, optimization_type="to_humans"
        )

        # Return the model, variables, maximize_constraints, consts_for_optimizer, and time_consts
        return (
            model,
            variables,
            maximize_constraints,
            percent_fed_from_model,
        )

    def optimize_feed_to_animals(
        self, consts_for_optimizer, time_consts, min_human_food_consumption
    ):
        """
        This function optimizes the model to maximize the amount of food produced for feed and biofuel.
        Args:
            consts_for_optimizer (dict): A dictionary containing single-valued constants
            time_consts (dict): A dictionary containing time-related constants
            min_human_food_consumption (dict): A dictionary of foods mandated to be fed to humans in the optimization
                in order of preference
        Returns:
            tuple: A tuple containing the following:
                - model (LpProblem): The model to optimize
                - variables (dict): A dictionary containing the variables in the model
                - maximize_constraints (list): A list of constraints to maximize

        """

        self.time_consts["min_human_food_consumption"] = min_human_food_consumption

        # Create the model to optimize
        model = LpProblem(name="optimization_feed", sense=LpMaximize)

        # Create a copy of the initial variables
        variables = self.initial_variables.copy()

        # Add all variables and constraints to the model
        (
            model,
            variables,
            maximize_constraints,
        ) = self.add_variables_and_constraints_to_model(
            model,
            variables,
            consts_for_optimizer,
            optimization_type="to_animals",
        )

        # Run optimizations to maximize food production for animals after human food is fixed.
        percent_fed_from_model = self.run_optimizations_on_constraints(
            model, variables, consts_for_optimizer, optimization_type="to_animals"
        )

        # Return the model, variables, maximize_constraints, consts_for_optimizer, and time_consts
        return (
            model,
            variables,
            maximize_constraints,
            percent_fed_from_model,
        )

    def assign_predetermined_human_consumption_of_foods(
        self, model, month, variables, min_human_food_consumption, food_type
    ):
        condition = {}
        # Calculate 99.999% of the min_human_food_consumption for this food and month
        min_consumption = (
            min_human_food_consumption[food_type]
            .in_units_bil_kcals_thou_tons_thou_tons_per_month()[month]
            .kcals
        )
        if self.consts_for_optimizer["POP"] < 1e7:
            # I loosened these by 1 order of magnitude and it fixed an optimization failure for djibouti...
            # Loosened by 2 and fixed lesotho
            lower_bound = 0.9999 * min_consumption
            upper_bound = 1.0001 * min_consumption
        else:
            lower_bound = 0.99999 * min_consumption
            upper_bound = 1.00001 * min_consumption

        # Define the relaxed conditions for the to_human variables
        if food_type == "outdoor_crops":
            condition["Outdoor_crops_Min_Requirement"] = (
                variables["crops_food_to_humans"][month] >= lower_bound
            )
            condition["Outdoor_crops_Max_Requirement"] = (
                variables["crops_food_to_humans"][month] <= upper_bound
            )
        elif food_type == "stored_food":
            condition["Stored_food_Min_Requirement"] = (
                variables["stored_food_to_humans"][month] >= lower_bound
            )
            condition["Stored_food_Max_Requirement"] = (
                variables["stored_food_to_humans"][month] <= upper_bound
            )
        elif food_type == "meat":
            condition["Meat_Min_Requirement"] = (
                variables["meat_eaten"][month] >= lower_bound
            )
            condition["Meat_Max_Requirement"] = (
                variables["meat_eaten"][month] <= upper_bound
            )
        elif food_type == "methane_scp":
            condition["Methane_SCP_Min_Requirement"] = (
                variables["methane_scp_to_humans"][month] >= lower_bound
            )
            condition["Methane_SCP_Max_Requirement"] = (
                variables["methane_scp_to_humans"][month] <= upper_bound
            )
        elif food_type == "cellulosic_sugar":
            condition["Cellulosic_Sugar_Min_Requirement"] = (
                variables["cellulosic_sugar_to_humans"][month] >= lower_bound
            )
            condition["Cellulosic_Sugar_Max_Requirement"] = (
                variables["cellulosic_sugar_to_humans"][month] <= upper_bound
            )
        elif food_type == "seaweed":
            seaweed_kcals = self.consts_for_optimizer["SEAWEED_KCALS"]
            condition["Seaweed_Min_Requirement"] = (
                variables["seaweed_to_humans"][month] * seaweed_kcals >= lower_bound
            )
            condition["Seaweed_Max_Requirement"] = (
                variables["seaweed_to_humans"][month] * seaweed_kcals <= upper_bound
            )
        else:
            print("ERROR: added a condition for a food type that wasn't defined")
            sys.exit(1)
        return condition

    def add_variables_and_constraints_to_model(
        self,
        model,
        variables,
        consts_for_optimizer,
        optimization_type,
    ):
        """
        This function is utilized for adding variables and constraints to a given optimization model. It operates on
        resource constants and single valued constants.

        ### Parameters:

        - `model`: A PULP linear programming model object. This model should be already defined but may be in need of
         decision variables, objective function, and constraints.
        - `variables`: A dictionary object storing decision variables of the model.
        - `resource_constants`: A dictionary object, where each item includes information about a resource, including
         the prefixes and function for variable and constraint generation.
        - `consts_for_optimizer`: A dictionary object consisting of constant parameters used throughout the
        optimization process.

        ### Behavior:

        The function operates in two major steps:

        - First, it loops through each resource in `resource_constants`. If the corresponding key
            in `consts_for_optimizer` is set to True, it generates and adds new variables based on
            the resource prefixes. It then generates and adds constraints to the model for each month
             in the time horizon (from 0 to NMONTHS), using the function provided with each resource.
        - After adding all resource-based variables and constraints, the function adds objectives to
           the model for each month in the time horizon. These objectives are added to the
           `maximize_constraints` list, which is only used for validation.

        The function concludes by adding the objective function (stored under the "objective_function" key in the
        `variables` dictionary) to the model.

        ### Returns:

        This function returns three outputs:

        - `model`: The updated PULP model after adding the variables, constraints, and the objective function.
        - `variables`: The updated dictionary of variables after the function has added new variables.
        - `maximize_constraints`: A list of the objective functions added to the model, used for validation purposes.
        """
        self.optimization_type = optimization_type  # stored food isn't forced to be entirely consumed in to_animals
        for key, resource in self.resource_constants.items():
            if consts_for_optimizer[key]:  # if ADD_[resource name] is true...
                prefixes = resource["prefixes"]
                func = resource["function"]
                food_name = resource["food_name"]

                variables = self.add_variable_from_prefixes(variables, prefixes)

                for month in range(0, self.NMONTHS):
                    self.add_resource_specific_conditions_to_model(
                        model, variables, month, optimization_type, func, food_name
                    )

        maximize_constraints = []  # used only for validation
        for month in range(0, self.NMONTHS):
            # Add feed biofuel to the model
            model = self.add_feed_biofuel_to_model(
                model, variables, month, optimization_type
            )
            if optimization_type == "to_humans":
                (model, variables,) = self.add_total_human_consumption_to_model(
                    model, variables, month, optimization_type
                )

            # Add percentage intake constraints to the model (HAS TO HAPPEN AFTER ADDING TOTAL HUMAN CONSUMPTION)
            model = self.add_percentage_intake_constraints(
                model, variables, month, optimization_type
            )

        if optimization_type == "to_humans":
            for month in range(0, self.NMONTHS):
                (
                    model,
                    variables,
                    maximize_constraints,
                ) = self.add_maximize_min_month_objective_to_model(
                    model, variables, month, maximize_constraints
                )
        elif optimization_type == "to_animals":
            (
                model,
                variables,
                maximize_constraints,
            ) = self.add_maximize_sum_total_feed_used_by_animals(
                model, variables, self.NMONTHS
            )
        else:
            print("error!! only to humans or to animals allowed to optimize")
            sys.exit()
        model += variables["objective_function"]

        return model, variables, maximize_constraints

    def add_resource_specific_conditions_to_model(
        self, model, variables, month, optimization_type, func, food_name
    ):
        # Add the conditions returned from the functions defined in "resource_constants"
        conditions = func(month, variables)
        model = self.add_conditions_to_model(model, month, conditions)

        if optimization_type == "to_animals":
            condition = self.assign_predetermined_human_consumption_of_foods(
                model,
                month,
                variables,
                self.time_consts["min_human_food_consumption"],
                food_name,
            )
            model = self.add_conditions_to_model(model, month, condition)

    def run_optimizations_on_constraints(
        self, model, variables, consts_for_optimizer, optimization_type
    ):
        """
        This function is part of a resource allocation system aiming to model systems which
            1. minimizes human starvation
            2. maximizes feed going to animals, and secondarily biofuel, assuming minimal nutrition for humans are met
            3. reduces unnecessary fluctuations in the predicted food consumption.

        This function specifically takes the series of constraints which either involve a maximization of the minimum
        to_human food, OR a maximization of the number of months where to_animals feed demand is fully met, starting at
        the first month of the simulation.

        The function executes a series of optimization steps. After solving the initial model, it performs several more
        rounds of optimization, each with added constraints based on the results of the previous round.

        Here's a brief overview of the operations it performs:

        - It first solves the initial model and asserts that the optimization was successful.
        - It then constrains the next optimization to have the same minimum starvation as the previous optimization.
        - If the first optimization was successful, it optimizes the best food consumption that goes to humans.
        - After that, it constrains the next optimization to have the same total resilient foods in feed as the
            previous optimization.
        - If the first optimization was successful and if food storage between years is allowed, it further optimizes
            to reduce fluctuations in food distribution.

        Args:
            self : The optimizer object.
            model : A PULP linear programming model object. This model should be already defined and configured.
            variables : A dictionary containing the variables used in the optimization.
            consts_for_optimizer: A dictionary of constant parameters that are used throughout the optimization
            process.

        """

        # Set this to True to print PULP messages
        PRINT_PULP_MESSAGES_FLAG = False
        if PRINT_PULP_MESSAGES_FLAG:
            print("")
            print(
                "This is the set of linear constraints for the model, containing all constraints and"
                " variable definitions."
            )
            print(model)
        # Solve the initial model
        status = model.solve(
            pulp.PULP_CBC_CMD(gapRel=0.00001, msg=PRINT_PULP_MESSAGES_FLAG)
        )

        # Assert that the optimization was successful
        ASSERT_SUCCESSFUL_OPTIMIZATION_FLAG = True
        if ASSERT_SUCCESSFUL_OPTIMIZATION_FLAG:
            if status != 1:
                data = model.to_dict()
                print("")
                print("")
                with open("model.json", "w") as f:
                    json.dump(data, f, indent=4)
                print(
                    f'model failed when running country {consts_for_optimizer["inputs"]["COUNTRY_CODE"]}! '
                    "Saving the json as model.json in root dir. run the run_saved_model.py in "
                    "scripts/ to reproduce the error"
                )
            assert (
                status == 1
            ), f'ERROR: OPTIMIZATION FAILED FOR {consts_for_optimizer["inputs"]["COUNTRY_CODE"]}!'

        percent_fed_from_first_optimization = model.objective.value()
        # To determine the allocation of
        # both biofuels and feed, the optimizer first does an optimization ignoring
        # feed and biofuel usage entirely. This optimization does not at all subtract
        # feed or biofuel usage.  The result is a maximum on the number of people that
        # could be fed before considering feed or biofuel.  Note however that this
        # also is using the meat production which required usage of the feed that was
        # ignored.  This is the point in the code we're at on this very line: we've
        # allocated all food to humans,
        # but have not yet considered how feed and biofuels will be satisfied.
        # So, passed to the optimizer to allocate to humans (ignoring waste).
        # At this stage, we have made an optimization for
        # minimizing human starvation that completely ignores feed and biofuels.

        if optimization_type == "to_humans":
            # Constrain the next optimization to have the same minimum starvation as the previous optimization
            # the previous optimization is just allocating all the food to humans, and using this to determine the
            # month with the minimum starvation
            # the next optimization is arranging the scenario so that the outdoor crops, greenhouse, and stored food
            # preferentially go to humans rather than to animals
            (
                model,
                variables,
            ) = self.constrain_next_optimization_to_have_same_minimum_starvation(
                model, variables
            )
        else:
            # Constrain the next optimization to have the same allocation of feed and biofuel as the previous
            # optimization
            (
                model,
                variables,
            ) = self.constrain_next_optimization_to_have_same_feed_biofuel(
                model, variables
            )

        # If the first optimization was successful, optimize the best food consumption that goes to humans
        # best foods are hardcoded in the model as outdoor crops, greenhouse, and stored food.
        if status == 1:
            model, variables = self.optimize_best_food_consumption_to_go_to_humans(
                model,
                variables,
                ASSERT_SUCCESSFUL_OPTIMIZATION_FLAG,
                consts_for_optimizer,
            )

        # Constrain the next optimization to have the same total resilient foods in feed as the previous optimization
        (
            model,
            variables,
        ) = self.constrain_next_optimization_to_have_same_total_resilient_foods_in_feed(
            model, variables
        )

        # If the first optimization was successful, further optimize to reduce fluctuations in food
        # distribution
        if status == 1:
            model, variables = self.reduce_fluctuations_with_a_final_optimization(
                model,
                variables,
                ASSERT_SUCCESSFUL_OPTIMIZATION_FLAG,
                consts_for_optimizer,
                optimization_type,
            )
        return percent_fed_from_first_optimization

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
            ) / self.NMONTHS * 0.99995  # TODO: can this just be equal to 1? # NOTE: seems to fail if I set it to 1...

        # Add the constraint to the model
        # TODO: can this just be set to "equals?"
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
            >>> updated_model = add_conditions_to_model(model, '1', conditions)
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
            name="Objective_To_Optimize", lowBound=0
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
        self.meat_prefixes = [
            "Meat_Start",
            "Meat_End",
            "Meat_Eaten",
        ]
        self.crops_food_prefixes = [
            "Crops_Food_Storage",
            "Crops_Food_Consumed",
            "Crops_Food_Consumed_Fat",
            "Crops_Food_Consumed_Protein",
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
            self.meat_prefixes,
            self.crops_food_prefixes,
            self.seaweed_prefixes,
        ]

        # Flatten the nested list
        flattened_list = [item for sublist in nested_list for item in sublist]

        # Add all variable names to the dictionary with initial values of 0 for each month
        for camel_case_variable_name in flattened_list:
            # these will be overwritten if the variable is used
            variables[camel_case_variable_name.lower()] = [0] * self.NMONTHS

        # Add consumed_kcals, consumed_fat, and consumed_protein variables to the
        # dictionary with initial values of 0 for each month
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
        consts_for_optimizer,
    ):
        """
        This function optimizes the amount of food to be allocated to humans while ensuring that the minimum
        demands for feed and biofuel are met.
        Args:
            self: instance of the Optimizer class
            model: the model to be optimized
            variables: dictionary of variables used in the model
            ASSERT_SUCCESSFUL_OPTIMIZATION: assertion to check if optimization was successful
            consts_for_optimizer: dictionary of constants used in the model
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
        # NOTE: this does not include stored food or outdoor growing! Therefore stored food and outdoor growing
        # will be going to humans instead where possible.
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
        # This means that the optimizer is trying to maximize the feed and biofuel coming from resilient foods.
        # That is because the model is constrained to still feed the most humans possible, and all food resources
        # are used by the optimizer in the first optimization run.
        model_max_to_humans += (
            variables["objective_function_best_to_humans"]
            <= total_feed_biofuel_variable,
            maximizer_string,
        )

        # Set the objective of the model to the objective function variable
        model_max_to_humans.setObjective(variables["objective_function_best_to_humans"])

        # Solve the model using the PULP_CBC_CMD solver
        status = model_max_to_humans.solve(pulp.PULP_CBC_CMD(gapRel=0.0001, msg=False))
        if ASSERT_SUCCESSFUL_OPTIMIZATION:
            # Check if optimization was successful
            assert (
                status == 1
            ), f'ERROR: OPTIMIZATION FAILED FOR {consts_for_optimizer["inputs"]["COUNTRY_CODE"]}!'

        # Return the optimized model and updated variables dictionary
        return model_max_to_humans, variables

    def reduce_fluctuations_with_a_final_optimization(
        self,
        model,
        variables,
        ASSERT_SUCCESSFUL_OPTIMIZATION,
        consts_for_optimizer,
        optimization_type,
    ):
        """
        Optimize the smoothing objective function to reduce fluctuations in the model.

        Args:
            model (pulp.LpProblem): The model to optimize.
            variables (dict): A dictionary of variables used in the model.
            ASSERT_SUCCESSFUL_OPTIMIZATION (bool): A flag to assert if optimization was successful.
            consts_for_optimizer (dict): A dictionary of constants used in the model.

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

        PENALTY_COST = 100  # Adjust as needed, this is the weight of the penalty
        for month in range(1, self.NMONTHS):
            # Variables to capture the absolute difference
            meat_change = LpVariable(f"Meat_Change_{month}", lowBound=0)
            stored_food_change = LpVariable(f"Stored_Food_Change_{month}", lowBound=0)
            outdoor_crops_change = LpVariable(
                f"Outdoor_Crops_Change_{month}", lowBound=0
            )
            seaweed_change = LpVariable(f"Seaweed_Change_{month}", lowBound=0)
            cellulosic_sugar_change = LpVariable(
                f"Cellulosic_Sugar_Change_{month}", lowBound=0
            )
            methane_scp_change = LpVariable(f"Methane_Scp_Change_{month}", lowBound=0)
            outdoor_crops_change_feed = LpVariable(
                f"Outdoor_Crops_Feed_Change_{month}", lowBound=0
            )
            outdoor_crops_change_biofuel = LpVariable(
                f"Outdoor_Crops_Biofuel_Change_{month}", lowBound=0
            )
            stored_food_change_feed = LpVariable(
                f"Stored_Food_Feed_Change_{month}", lowBound=0
            )
            stored_food_change_biofuel = LpVariable(
                f"Stored_Food_Biofuel_Change_{month}", lowBound=0
            )
            methane_scp_change_feed = LpVariable(
                f"Methane_Scp_Feed_Change_{month}", lowBound=0
            )
            methane_scp_change_biofuel = LpVariable(
                f"Methane_Scp_Biofuel_Change_{month}", lowBound=0
            )
            cellulosic_sugar_change_feed = LpVariable(
                f"Cellulosic_Sugar_Feed_Change_{month}", lowBound=0
            )
            cellulosic_sugar_change_biofuel = LpVariable(
                f"Cellulosic_Sugar_Biofuel_Change_{month}", lowBound=0
            )

            if consts_for_optimizer["ADD_MEAT"]:
                model_smoothing += (
                    meat_change
                    >= -(
                        variables["meat_eaten"][month]
                        - variables["meat_eaten"][month - 1]
                    ),
                    f"Meat_Decrease_{month}",
                )

            if consts_for_optimizer["ADD_STORED_FOOD"]:
                model_smoothing += (
                    stored_food_change
                    >= -(
                        variables["stored_food_to_humans"][month]
                        - variables["stored_food_to_humans"][month - 1]
                    ),
                    f"Stored_Food_Decrease_{month}",
                )
            if consts_for_optimizer["ADD_OUTDOOR_GROWING"]:
                model_smoothing += (
                    outdoor_crops_change
                    >= -(
                        variables["crops_food_to_humans"][month]
                        - variables["crops_food_to_humans"][month - 1]
                    ),
                    f"Crops_Food_Decrease_{month}",
                )
            if consts_for_optimizer["ADD_SEAWEED"]:
                model_smoothing += (
                    seaweed_change
                    >= -(
                        variables["seaweed_to_humans"][month]
                        - variables["seaweed_to_humans"][month - 1]
                    ),
                    f"Seaweed_Decrease_{month}",
                )
            if consts_for_optimizer["ADD_METHANE_SCP"]:
                model_smoothing += (
                    methane_scp_change
                    >= -(
                        variables["methane_scp_to_humans"][month]
                        - variables["methane_scp_to_humans"][month - 1]
                    ),
                    f"Methane_Scp_Decrease_{month}",
                )
            if consts_for_optimizer["ADD_CELLULOSIC_SUGAR"]:
                model_smoothing += (
                    cellulosic_sugar_change
                    >= -(
                        variables["cellulosic_sugar_to_humans"][month]
                        - variables["cellulosic_sugar_to_humans"][month - 1]
                    ),
                    f"Cell_Sugar_Decrease_{month}",
                )

            if optimization_type == "to_animals":
                # in this case, we want to smooth out the feed and biofuel usage if possible
                model_smoothing += (
                    outdoor_crops_change_feed
                    >= -(
                        variables["crops_food_feed"][month]
                        - variables["crops_food_feed"][month - 1]
                    ),
                    f"Crops_Food_Feed_Decrease_{month}",
                )
                model_smoothing += (
                    outdoor_crops_change_biofuel
                    >= -(
                        variables["crops_food_biofuel"][month]
                        - variables["crops_food_biofuel"][month - 1]
                    ),
                    f"Crops_Food_Biofuel_Decrease_{month}",
                )
                model_smoothing += (
                    stored_food_change_feed
                    >= -(
                        variables["stored_food_feed"][month]
                        - variables["stored_food_feed"][month - 1]
                    ),
                    f"Stored_Food_Feed_Decrease_{month}",
                )
                model_smoothing += (
                    stored_food_change_biofuel
                    >= -(
                        variables["stored_food_biofuel"][month]
                        - variables["stored_food_biofuel"][month - 1]
                    ),
                    f"Stored_Food_Biofuel_Decrease_{month}",
                )
                if consts_for_optimizer["ADD_METHANE_SCP"]:
                    model_smoothing += (
                        methane_scp_change_feed
                        >= -(
                            variables["methane_scp_feed"][month]
                            - variables["methane_scp_feed"][month - 1]
                        ),
                        f"Methane_Scp_Feed_Decrease_{month}",
                    )
                    model_smoothing += (
                        methane_scp_change_biofuel
                        >= -(
                            variables["methane_scp_biofuel"][month]
                            - variables["methane_scp_biofuel"][month - 1]
                        ),
                        f"Methane_Scp_Biofuel_Decrease_{month}",
                    )

                if consts_for_optimizer["ADD_CELLULOSIC_SUGAR"]:
                    model_smoothing += (
                        cellulosic_sugar_change_feed
                        >= -(
                            variables["cellulosic_sugar_feed"][month]
                            - variables["cellulosic_sugar_feed"][month - 1]
                        ),
                        f"Cell_Sugar_Feed_Decrease_{month}",
                    )
                    model_smoothing += (
                        cellulosic_sugar_change_feed
                        >= -(
                            variables["cellulosic_sugar_biofuel"][month]
                            - variables["cellulosic_sugar_biofuel"][month - 1]
                        ),
                        f"Cell_Sugar_Biofuel_Decrease_{month}",
                    )

            # Add the absolute differences to the objective function
            smoothing_obj += PENALTY_COST * (
                meat_change
                + stored_food_change
                + outdoor_crops_change
                + outdoor_crops_change_feed
                + methane_scp_change_feed
                + cellulosic_sugar_change_feed
                + outdoor_crops_change_biofuel
                + methane_scp_change_biofuel
                + cellulosic_sugar_change_biofuel
                + stored_food_change_feed
                + stored_food_change_biofuel
                + seaweed_change
                + methane_scp_change
                + cellulosic_sugar_change
            )

        # Set the objective of the model to the smoothing objective function
        model_smoothing.setObjective(smoothing_obj)

        # Solve the model using the PULP_CBC_CMD solver
        status = model_smoothing.solve(pulp.PULP_CBC_CMD(gapRel=0.0001, msg=False))

        # Assert if optimization was successful
        if ASSERT_SUCCESSFUL_OPTIMIZATION:
            assert (
                status == 1
            ), f'ERROR: OPTIMIZATION FAILED FOR {consts_for_optimizer["inputs"]["COUNTRY_CODE"]}!'

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
            model.objective.value() * 0.99995
        )  # reach almost the same as objective, but allow for small rounding error if needed

        # Add the constraint for consumed_kcals each month
        for month in range(0, self.NMONTHS):
            maximizer_string = (
                "Old_Objective_Month_" + str(month) + "_Objective_Constraint"
            )

            # This means the optimizer is trying to maximize the calories consumed in the month (or months)
            # with the least number of calories, within the bounds of the previous constraints enforced.
            # (the right hand side is what is attempted to be maximized)
            # (the left hand side is the minimum calories any month must have, meaning that this more constrained
            # optimization must at least allow for satisfying the previous optimization's objectives)
            model += (
                min_value <= variables["consumed_kcals"][month],
                maximizer_string,
            )

            # Add the constraint for consumed_fat each month if INCLUDE_FAT is True
            if self.consts_for_optimizer["inputs"]["INCLUDE_FAT"]:
                maximizer_string = (
                    "Old_Fat_Objective_Month_" + str(month) + "_Objective_Constraint"
                )

                model += (
                    variables["objective_function"] <= variables["consumed_fat"][month],
                    maximizer_string,
                )

            # Add the constraint for consumed_protein each month if INCLUDE_PROTEIN is True
            if self.consts_for_optimizer["inputs"]["INCLUDE_PROTEIN"]:
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

    def constrain_next_optimization_to_have_same_feed_biofuel(self, model, variables):
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
        # (previous optimization value is the minimum humans fed in any month).
        # Set min_value to the previous optimization value and make sure consumed_kcals meets this value each month
        min_value = (
            model.objective.value() * 0.99995
        )  # reach almost the same as objective, but allow for small rounding error if needed

        # Add the constraint for consumed_kcals each month
        feed_sum, biofuel_sum = self.get_nonhuman_consumption_sum(
            self.NMONTHS, variables
        )
        maximizer_string = "Old_Objective_Constraint"

        # This means the optimizer is trying to maximize the sum calories consumed in the scenario
        # within the bounds of the previous constraints enforced (previous constraint is the minimum humans fed in
        # any month).
        # (the right hand side is what is attempted to be maximized)
        # (the left hand side is the minimum calories any month must have, meaning that this more constrained
        # optimization must at least allow for satisfying the previous optimization's objectives)
        model += (
            min_value <= 2 / 3 * feed_sum + biofuel_sum / 3,
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

    def add_percentage_intake_constraints(
        self, model, variables, month, optimization_type
    ):
        """
        Adds constraints to the optimization model based on the percentage intake of the nonhuman and human diets.



        Args:
            model (object): The optimization model object
            variables (dict): A dictionary of variables used in the optimization model
            month (int): The month for which the constraints are being added

        Returns:
            object: The optimization model object with added constraints
        """

        # Dictionary containing nutrient ratios for different resources
        resilient_food_ratios = {
            "Seaweed": self.consts_for_optimizer["SEAWEED_KCALS"],
            "Methane_SCP": 1,
            "Cellulosic_Sugar": 1,
        }

        initial_population_minimum_needs = (
            self.consts_for_optimizer["POP"]
            * self.consts_for_optimizer["KCALS_MONTHLY"]
            / 1e9
        )  # Billion kcals

        # Loop through each nutrient and add constraints based on its usage
        for food_name, kcal_to_nutrient_ratio in resilient_food_ratios.items():
            if self.consts_for_optimizer["ADD_" + food_name.upper()]:
                constraints_data = [
                    (
                        "HUMANS",
                        "MAX_" + food_name.upper() + "_AS_PERCENT_KCALS_HUMANS",
                        "to_humans",
                    ),
                    (
                        "FEED",
                        "MAX_" + food_name.upper() + "_AS_PERCENT_KCALS_FEED",
                        "feed",
                    ),
                    (
                        "BIOFUEL",
                        "MAX_" + food_name.upper() + "_AS_PERCENT_KCALS_BIOFUEL",
                        "biofuel",
                    ),
                ]
                for constraint_type, limit_key, variable_tag in constraints_data:
                    food_consumption_to_limit = variables[
                        food_name.lower() + "_" + variable_tag
                    ][month]
                    max_fraction_of_consumption = (
                        self.consts_for_optimizer["inputs"][limit_key] / 100
                    )
                    if constraint_type == "HUMANS":
                        if optimization_type != "to_humans":
                            continue  # the below constraints only apply to human consumption of calories.

                        # This condition is just saying that even if variables["consumed_kcals"] is greater than the
                        # minimum needs of the initialpopulation in a given month, don't allow consumption above the
                        # original population's max_fraction_of_consumption for this food.
                        condition = (
                            max_fraction_of_consumption
                            * initial_population_minimum_needs
                            >= food_consumption_to_limit * kcal_to_nutrient_ratio
                        )
                        # Add the constraint to the model
                        model = self.add_constraints(
                            model,
                            month,
                            condition,
                            food_name + "_Limit_" + constraint_type,
                        )

                        # This multiplies the fractional intake limit by the actual to_human consumption in the
                        # given month. We limit this food based on the reduced population level rather
                        # than the initial population (it's assumed the reduced population is determined by the percent
                        # people fed in the month).
                        # convert from % fed (consumed_kcals units) to billion_kcals_fed (all the different food's
                        # units)
                        condition = (
                            food_consumption_to_limit * kcal_to_nutrient_ratio
                            <= (
                                max_fraction_of_consumption
                                * (
                                    variables["consumed_kcals"][month]
                                    * self.consts_for_optimizer["BILLION_KCALS_NEEDED"]
                                    / 100
                                )
                            )
                        )
                        # Add the constraint to the model
                        model = self.add_constraints(
                            model,
                            month,
                            condition,
                            food_name + "_Limit_Reduced_Population_" + constraint_type,
                        )
                    elif constraint_type in ("FEED", "BIOFUEL"):
                        # limit the feed or biofuel
                        kcals_feed_or_biofuel_used = self.time_consts[
                            variable_tag.lower()
                        ].kcals[month]

                        condition = (
                            food_consumption_to_limit * kcal_to_nutrient_ratio
                            <= (
                                max_fraction_of_consumption * kcals_feed_or_biofuel_used
                            )
                        )

                        # Add the constraint to the model
                        model = self.add_constraints(
                            model,
                            month,
                            condition,
                            food_name + "_Limit_" + constraint_type,
                        )
                    else:
                        print(
                            "ERROR: can only constrain feed, biofuel, or human usage in optimizer"
                        )
                        sys.exit()

        return model

    def get_feed_sum(self, variables, month):
        return (
            variables["stored_food_feed"][month]
            + variables["crops_food_feed"][month]
            + variables["seaweed_feed"][month]
            * self.consts_for_optimizer["SEAWEED_KCALS"]
            + variables["cellulosic_sugar_feed"][month]
            + variables["methane_scp_feed"][month]
        )

    def get_biofuel_sum(self, variables, month):
        return (
            variables["stored_food_biofuel"][month]
            + variables["crops_food_biofuel"][month]
            + variables["seaweed_biofuel"][month]
            * self.consts_for_optimizer["SEAWEED_KCALS"]
            + variables["cellulosic_sugar_biofuel"][month]
            + variables["methane_scp_biofuel"][month]
        )

    def add_feed_biofuel_to_model(self, model, variables, month, optimization_type):
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
        feed_sum = self.get_feed_sum(variables, month)

        # Calculate the sum of all biofuel variables for the given month
        biofuel_sum = self.get_biofuel_sum(variables, month)

        add_feed_constraints = True
        add_biofuel_constraints = True
        if isinstance(feed_sum, float) and feed_sum == 0:
            add_feed_constraints = False
        if isinstance(biofuel_sum, float) and biofuel_sum == 0:
            add_biofuel_constraints = False

        conditions = {}
        if optimization_type == "to_humans":
            # Define the conditions for the feed and biofuel variables
            if add_feed_constraints:
                conditions["Feed_Used"] = (
                    feed_sum == self.time_consts["feed"].kcals[month]
                )
            if add_biofuel_constraints:
                conditions["Biofuel_Used"] = (
                    biofuel_sum == self.time_consts["biofuel"].kcals[month]
                )

            model = self.add_conditions_to_model(model, month, conditions)
        elif optimization_type == "to_animals":
            if add_feed_constraints:
                conditions["Feed_Used"] = (
                    feed_sum
                    <= self.time_consts["max_feed_that_could_be_used"].kcals[month]
                )
            if add_biofuel_constraints:
                conditions["Biofuel_Used"] = (
                    biofuel_sum
                    <= self.time_consts["max_biofuel_that_could_be_used"].kcals[month]
                )

            if month > 0 and add_feed_constraints:
                feed_sum_previous_month = self.get_feed_sum(variables, month - 1)
                biofuel_sum_previous_month = self.get_biofuel_sum(variables, month - 1)
                conditions["Feed_Decreases"] = feed_sum_previous_month >= feed_sum
                conditions["Biofuel_Decreases"] = (
                    biofuel_sum_previous_month >= biofuel_sum
                )
            model = self.add_conditions_to_model(model, month, conditions)

        else:
            print(
                'ERROR: incorrect optimization type. Only "to_humans" or "to_animals" defined'
            )
            sys.exit()

        return model

    def add_total_human_consumption_to_model(
        self, model, variables, month, optimization_type
    ):
        """
        Adds conditions that are not specific to a specific food (not defined in a function for that food)
        to the optimization model.

        Args:
            model (pulp.LpProblem): The optimization model to which objectives are added.
            variables (dict): A dictionary of variables used in the optimization model.
            month (int): The month for which objectives are added.
            maximize_constraints (list): A list of constraints to be maximized.

        Returns:
            list: A list containing the updated model, variables, and maximize_constraints.

        """

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
                * self.consts_for_optimizer["SEAWEED_KCALS"]
                + self.time_consts["milk_kcals"][month]
                + variables["meat_eaten"][month]
                + variables["cellulosic_sugar_to_humans"][month]
                + variables["methane_scp_to_humans"][month]
                + self.time_consts["greenhouse_crops"][month].kcals
                + self.time_consts["fish"].to_humans.kcals[month]
            )
            / self.consts_for_optimizer["BILLION_KCALS_NEEDED"]
            * 100,
            "Kcals_Fed_Month_" + str(month) + "_Constraint",
        )

        # Add constraints for consumed fat and protein
        # TODO: PUT BACK IN!
        # if self.consts_for_optimizer["inputs"]["INCLUDE_FAT"]:
        #     # fat monthly is in units thousand tons
        #     model += (
        #         variables["consumed_fat"][month]
        #         == (
        #             variables["stored_food_eaten"][month]
        #             * self.consts_for_optimizer["SF_FRACTION_FAT"]
        #             + variables["crops_food_consumed_fat"][month]
        #             + variables["seaweed_to_humans"][month]
        #             * self.consts_for_optimizer["SEAWEED_FAT"]
        #             + variables["seaweed_feed"][month]
        #             * self.consts_for_optimizer["SEAWEED_FAT"]
        #             + self.time_consts["milk_fat"][month]
        #             + self.time_consts["cattle_grazing_maintained_fat"][month]
        #             + variables["meat_eaten"][month]
        #             * self.consts_for_optimizer["MEAT_FRACTION_FAT"]
        #             + variables["methane_scp_to_humans"][month]
        #             * self.consts_for_optimizer["SCP_KCALS_TO_FAT_CONVERSION"]
        #             + variables["methane_scp_feed"][month]
        #             * self.consts_for_optimizer["SCP_KCALS_TO_FAT_CONVERSION"]
        #             + self.time_consts["greenhouse_area"][month]
        #             * self.time_consts["greenhouse_fat_per_ha"][month]
        #             + self.time_consts["fish"].to_humans.fat[month]
        #             - self.time_consts["nonhuman_consumption"].fat[month]
        #         )
        #         / self.consts_for_optimizer["THOU_TONS_FAT_NEEDED"]
        #         * 100,
        #         "Fat_Fed_Month_" + str(month) + "_Constraint",
        #     )

        # if self.consts_for_optimizer["inputs"]["INCLUDE_PROTEIN"]:
        #     model += (
        #         variables["consumed_protein"][month]
        #         == (
        #             variables["stored_food_eaten"][month]
        #             * self.consts_for_optimizer["SF_FRACTION_PROTEIN"]
        #             + variables["crops_food_consumed_protein"][month]
        #             + variables["seaweed_to_humans"][month]
        #             * self.consts_for_optimizer["SEAWEED_PROTEIN"]
        #             + variables["seaweed_feed"][month]
        #             * self.consts_for_optimizer["SEAWEED_PROTEIN"]
        #             + self.time_consts["milk_protein"][month]
        #             + self.time_consts["cattle_grazing_maintained_protein"][month]
        #             + variables["methane_scp_to_humans"][month]
        #             * self.consts_for_optimizer["SCP_KCALS_TO_PROTEIN_CONVERSION"]
        #             + variables["methane_scp_feed"][month]
        #             * self.consts_for_optimizer["SCP_KCALS_TO_PROTEIN_CONVERSION"]
        #             + variables["meat_eaten"][month]
        #             * self.consts_for_optimizer["MEAT_FRACTION_PROTEIN"]
        #             + self.time_consts["greenhouse_area"][month]
        #             * self.time_consts["greenhouse_protein_per_ha"][month]
        #             + self.time_consts["fish"].to_humans.kcals[month]
        #             - self.time_consts["nonhuman_consumption"].protein[month]
        #         )
        #         / self.consts_for_optimizer["THOU_TONS_PROTEIN_NEEDED"]
        #         * 100,
        #         "Protein_Fed_Month_" + str(month) + "_Constraint",
        #     )

        # Add constraint for no feeding human edible maintained meat or milk to animals or biofuels

        return model, variables

    def add_maximize_min_month_objective_to_model(
        self, model, variables, month, maximize_constraints
    ):
        # Maximize the minimum objective_function value
        # We maximize the minimum humans fed from any month
        # We therefore maximize the minimum ratio of fat per human requirement,
        # protein per human requirement, or kcals per human requirement
        # for all months
        maximizer_string = "Kcals_Fed_Month_" + str(month) + "_Objective_Constraint"
        maximize_constraints.append(maximizer_string)

        # this tells the model to maximize the minimum month of consumed_kcals
        model += (
            variables["objective_function"] <= variables["consumed_kcals"][month],
            maximizer_string,
        )

        if self.consts_for_optimizer["inputs"]["INCLUDE_FAT"]:
            maximizer_string = "Fat_Fed_Month_" + str(month) + "_Objective_Constraint"
            maximize_constraints.append(maximizer_string)
            model += (
                variables["objective_function"] <= variables["consumed_fat"][month],
                maximizer_string,
            )

        if self.consts_for_optimizer["inputs"]["INCLUDE_PROTEIN"]:
            maximizer_string = (
                "Protein_Fed_Month_" + str(month) + "_Objective_Constraint"
            )
            maximize_constraints.append(maximizer_string)
            model += (
                variables["objective_function"] <= variables["consumed_protein"][month],
                maximizer_string,
            )
        return model, variables, maximize_constraints

    def get_nonhuman_consumption_sum(self, nmonths, variables):
        feed_sum = 0
        biofuel_sum = 0
        for month in range(nmonths):
            feed_sum += self.get_feed_sum(variables, month)
            biofuel_sum += self.get_biofuel_sum(variables, month)
        return feed_sum, biofuel_sum

    def add_maximize_sum_total_feed_used_by_animals(self, model, variables, nmonths):
        # to satisfy animal feed demand:
        #   - each month must be less than or equal to the last.
        #   - maximize minimum month
        feed_sum, biofuel_sum = self.get_nonhuman_consumption_sum(nmonths, variables)

        maximizer_string = "Nonhuman_Consumption_All_Months_Objective_Constraint"
        maximize_constraints = [maximizer_string]

        # this tells the model to maximize the total feed_sum over all months
        # AND it tries to also maximize biofuels... but it weights biofuel with only 1/3
        # the "importance" of animal feed
        model += (
            variables["objective_function"] <= 2 / 3 * feed_sum + biofuel_sum / 3,
            maximizer_string,
        )
        # TODO: ADD FAT AND PROTEIN

        return model, variables, maximize_constraints

    # RESOURCE CONSTANTS FUNCTIONS BELOW

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
        initial_seaweed = self.consts_for_optimizer["INITIAL_SEAWEED"]
        max_density = self.consts_for_optimizer["MAXIMUM_DENSITY"]
        built_area = self.time_consts["built_area"][month]
        initial_built_area = self.consts_for_optimizer["INITIAL_BUILT_SEAWEED_AREA"]

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
            harvest_loss = self.consts_for_optimizer["HARVEST_LOSS"] / 100.0
            min_density = self.consts_for_optimizer["MINIMUM_DENSITY"]

            # Set the condition for the seaweed wet on farm
            conditions["Seaweed_Wet_On_Farm"] = (
                variables["seaweed_wet_on_farm"][month]
                == prev_seaweed * (1 + growth_rate)
                - humans_consumed
                * 1
                / (
                    1 - self.consts_for_optimizer["SEAWEED_WASTE_RETAIL"] / 100
                )  # humans use more seaweed if there's more retail waste
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
        max_kcals = self.consts_for_optimizer["stored_food"].initial_available.kcals

        # If it's the first month of the simulation
        if month == 0:
            # Add the condition that the stored food at the start of the simulation is
            # equal to the maximum kcals available
            conditions["Stored_Food_Start"] = (
                variables["stored_food_start"][0] == max_kcals
            )
            # Add the condition that the stored food eaten in the first month is equal
            # to the difference between the stored food at the start of the month and
            # the food used for humans, feed, and biofuel
            conditions["Stored_Food_Eaten"] = (
                variables["stored_food_end"][0]
                == variables["stored_food_start"][0]
                - variables["stored_food_to_humans"][0]
                * 1
                / (
                    1 - self.consts_for_optimizer["STORED_FOOD_WASTE_RETAIL"] / 100
                )  # increase calories, fat, and protein humans consumed by retail waste coefficient
                - variables["stored_food_feed"][0]
                - variables["stored_food_biofuel"][0]
            )
        # If it's after the first year of the simulation
        elif month > 12:
            # conditions["Stored_Food_End"] = variables["stored_food_end"][month] == 0
            # if self.optimization_type != "to_animals":
            # Add the condition that all stored food prefixes after the second one are equal to 0
            for prefix in [
                "Stored_Food_To_Humans",
                "Stored_Food_Feed",
                "Stored_Food_Biofuel",
            ]:
                conditions[prefix] = variables[prefix.lower()][month] == 0
            conditions["Stored_Food_Start"] = (
                variables["stored_food_start"][month]
                == variables["stored_food_end"][month - 1]
            )

        # If it's within the first year of the simulation
        else:
            # Add the condition that the stored food eaten in the current month is
            # equal to the difference between the stored food at the start of the
            # month and the food used for humans, feed, and biofuel
            conditions["Stored_Food_Eaten"] = (
                variables["stored_food_end"][month]
                == variables["stored_food_start"][month]
                - variables["stored_food_to_humans"][month]
                * 1
                / (
                    1 - self.consts_for_optimizer["STORED_FOOD_WASTE_RETAIL"] / 100
                )  # increase calories, fat, and protein humans consumed by retail waste coefficient
                - variables["stored_food_feed"][month]
                - variables["stored_food_biofuel"][month]
            )
            conditions["Stored_Food_Start"] = (
                variables["stored_food_start"][month]
                == variables["stored_food_end"][month - 1]
            )

        # Return the dictionary containing the conditions
        return conditions

    def add_stored_food_to_model(self, month, variables):
        if not self.consts_for_optimizer["STORE_FOOD_BETWEEN_YEARS"]:
            return self.add_stored_food_to_model_only_first_year(month, variables)

        conditions = {}

        if month == 0:  # first Month
            conditions["Stored_Food_Start"] = (
                variables["stored_food_start"][0]
                == self.consts_for_optimizer["stored_food"].initial_available.kcals
            )

        elif month == self.NMONTHS - 1:  # last month
            # be sure to eat all the stored food by the end, unless you are optimizing to animals
            if self.optimization_type != "to_animals":
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
            * 1
            / (
                1 - self.consts_for_optimizer["STORED_FOOD_WASTE_RETAIL"] / 100
            )  # increase calories, fat, and protein humans consumed by retail waste coefficient
            - variables["stored_food_feed"][month]
            - variables["stored_food_biofuel"][month]
        )

        return conditions

    def add_meat_to_model(self, month, variables):
        """
        This function adds meat to the model based on the month and variables passed in.

        It just makes sure the sum total meat consumed never exceeds the sum total allowed consumption.
        The maximum per month constraint is responsible for making sure meat eaten each month does not
        exceed the amount in that month and the months prior.

        Args:
            month (int): The month for which the meat is being added
            variables (dict): A dictionary containing variables related to meat

        Returns:
            dict: A dictionary containing conditions related to meat

        """
        if not self.consts_for_optimizer["STORE_FOOD_BETWEEN_YEARS"]:
            return self.add_meat_to_model_no_storage(month, variables)

        conditions = {}

        if month == 0:  # first Month
            # Check if the meat start value is equal to the constant value
            conditions["Meat_Start"] = (
                variables["meat_start"][0]
                == self.consts_for_optimizer["meat_summed_consumption"]
            )
        else:
            # Check if the meat start value is equal to the meat end value of the previous month
            conditions["Meat_Start"] = (
                variables["meat_start"][month] == variables["meat_end"][month - 1]
            )

        # Calculate the amount of meat eaten in the month
        conditions["Meat_Eaten"] = variables["meat_end"][month] == variables[
            "meat_start"
        ][month] - variables["meat_eaten"][month] * 1 / (
            1 - self.consts_for_optimizer["MEAT_WASTE_RETAIL"] / 100
        )

        # Add in the constraint that meat eaten is less than the maximum consumed that month.
        conditions["Meat_Eaten_Maximum"] = (
            variables["meat_eaten"][month]
            * 1
            / (1 - self.consts_for_optimizer["MEAT_WASTE_RETAIL"] / 100)
            <= self.time_consts["max_consumed_culled_kcals_each_month"][month]
        )

        return conditions

    def add_meat_to_model_no_storage(self, month, variables):
        """
        This function adds meat to the model based on the month and variables passed in.

        It simply sets the meat eaten to the amount of meat slaughtered -- no storage at all.

        Args:
            month (int): The month for which the meat is being added
            variables (dict): A dictionary containing variables related to meat

        Returns:
            dict: A dictionary containing conditions related to meat

        """

        conditions = {}

        # Add in the constraint that meat eaten is less than the maximum consumed that month.
        conditions["Meat_Eaten"] = (
            variables["meat_eaten"][month]
            * 1
            / (1 - self.consts_for_optimizer["MEAT_WASTE_RETAIL"] / 100)
            <= self.time_consts["each_month_meat_slaughtered"][month].kcals
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
        conditions = {}
        # TODO: add fat and protein variables
        conditions.update(
            self.create_linear_constraints_for_fat_and_protein_crops_food(
                month, variables, None, None
            )
        )

        # Create a dictionary containing the condition to be added to the model
        conditions["Crops_Food_Storage_Zero"] = (
            variables["crops_food_storage"][month] == 0
        )
        conditions["Crops_Food_Storage"] = (
            0
            == self.time_consts["outdoor_crops"].production.kcals[month]
            - variables["crops_food_consumed"][month]
        )

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
                - variables["crops_food_consumed"][month]
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
            "Crops_Food_Storage": (
                variables["crops_food_storage"][month]
                == self.time_consts["outdoor_crops"].production.kcals[month]
                + variables["crops_food_storage"][month - 1]
                - variables["crops_food_consumed"][month]
            ),
        }

        # if we're not optimizing to maximize animal feed, then make sure all stored crop food is used
        if self.optimization_type != "to_animals":
            conditions["Crops_Food_None_Left"] = (
                variables["crops_food_storage"][month] == 0
            )

        return conditions

    def handle_other_months(self, variables, month, use_relocated_crops):
        """
        This function handles months that are not January or July. It calculates the conditions for the month based on
        the variables passed in and returns them.

        Args:
            variables (dict): A dictionary containing variables for the simulation
            month (int): The current month of the simulation
            use_relocated_crops (bool): A boolean indicating whether or not to use relocated crops

        Returns:
            dict: A dictionary containing the conditions for the month

        Example:
            >>> variables = {
            ...     "crops_food_storage": [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200],
            ...     "crops_food_consumed": [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120]
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
                - variables["crops_food_consumed"][month]
            )
        }
        # Return the conditions
        return conditions

    def add_crops_food_consumed_with_nutrient_name(
        self, variables, month, nutrient, lowercase_nutrient
    ):
        conditions = {
            "Crops_Food_Consumed"
            + nutrient: (
                variables["crops_food_consumed" + lowercase_nutrient][month]
                == variables["crops_food_to_humans" + lowercase_nutrient][month]
                * 1
                / (1 - self.consts_for_optimizer["CROP_WASTE_RETAIL"] / 100)
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
            self.add_crops_food_consumed_with_nutrient_name(variables, month, "", "")
        )

        # Create a dictionary to store the nutrient multipliers
        nutrient_multiplier_dictionary = {}
        if self.consts_for_optimizer["inputs"]["INCLUDE_PROTEIN"]:
            nutrient_multiplier_dictionary[protein_multiplier] = "_Protein"

        if self.consts_for_optimizer["inputs"]["INCLUDE_FAT"]:
            nutrient_multiplier_dictionary[fat_multiplier] = "_Fat"
        if len(nutrient_multiplier_dictionary) > 0:
            # Loop through the nutrient multiplier dictionary
            for multiplier, nutrient in nutrient_multiplier_dictionary.items():
                # Convert the nutrient name to lowercase
                lowercase_nutrient = nutrient.lower()

                # Add constraints for crops food eaten with a specified nutrient name
                conditions.update(
                    self.add_crops_food_consumed_with_nutrient_name(
                        variables, month, nutrient, lowercase_nutrient
                    )
                )

                # Loop through the usage types
                for usage_type in ["_Feed", "_Biofuel"]:
                    # Convert the usage type to lowercase
                    lowercase_usage_type = usage_type.lower()

                    # Add a constraint for the crops food eaten conversion
                    conditions[
                        "Crops_Food_Eaten_Conversion" + usage_type + nutrient
                    ] = (
                        variables[
                            "crops_food" + lowercase_usage_type + lowercase_nutrient
                        ][month]
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
            self.consts_for_optimizer["INITIAL_HARVEST_DURATION_IN_MONTHS"]
            + self.consts_for_optimizer["DELAY"]["ROTATION_CHANGE_IN_MONTHS"]
        )

        # Check if relocated crops are being used and if the month is greater than or equal
        # to the initial harvest duration
        if use_relocated_crops and month >= initial_harvest_duration:
            # If so, use the rotation fraction constants for fat and protein
            fat_multiplier = self.consts_for_optimizer["OG_ROTATION_FRACTION_FAT"]
            protein_multiplier = self.consts_for_optimizer[
                "OG_ROTATION_FRACTION_PROTEIN"
            ]
        else:
            # Otherwise, use the original fraction constants for fat and protein
            fat_multiplier = self.consts_for_optimizer["OG_FRACTION_FAT"]
            protein_multiplier = self.consts_for_optimizer["OG_FRACTION_PROTEIN"]

        # Return the calculated constants as a tuple
        return (initial_harvest_duration, fat_multiplier, protein_multiplier)

    def add_outdoor_crops_to_model(self, month, variables):
        conditions = {}

        # if not self.consts_for_optimizer["STORE_FOOD_BETWEEN_YEARS"]:
        #     return self.add_outdoor_crops_to_model_no_storage(month, variables)

        use_relocated_crops = self.consts_for_optimizer["inputs"][
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
            * 1
            / (1 - self.consts_for_optimizer["SCP_RETAIL_WASTE"] / 100)
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
            * 1
            / (1 - self.consts_for_optimizer["CELL_SUGAR_RETAIL_WASTE"] / 100)
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
