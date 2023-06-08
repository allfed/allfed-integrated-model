#


## Optimizer
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/optimizer.py/#L12)
```python 
Optimizer(
   single_valued_constants, time_consts
)
```




**Methods:**


### .optimize_nonhuman_consumption
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/optimizer.py/#L34)
```python
.optimize_nonhuman_consumption(
   single_valued_constants, time_consts
)
```


### .optimize_to_humans
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/optimizer.py/#L74)
```python
.optimize_to_humans(
   single_valued_constants, time_consts
)
```

---
This function optimizes the model to maximize the amount of food produced for humans.

**Args**

* **single_valued_constants** (dict) : A dictionary containing single-valued constants
* **time_consts** (dict) : A dictionary containing time-related constants


**Returns**

* **tuple**  : A tuple containing the following:
    - model (LpProblem): The model to optimize
    - variables (dict): A dictionary containing the variables in the model
    - maximize_constraints (list): A list of constraints to maximize


### .add_variables_and_constraints_to_model
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/optimizer.py/#L145)
```python
.add_variables_and_constraints_to_model(
   model, variables, resource_constants, single_valued_constants
)
```

---
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

### .run_optimizations_to_humans
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/optimizer.py/#L194)
```python
.run_optimizations_to_humans(
   model, variables, single_valued_constants
)
```

---
This function is part of a resource allocation system aiming to model systems which minimize starvation.

The function executes a series of optimization steps. After solving the initial model, it performs several more rounds of optimization, each with added constraints based on the results of the previous round.

Here's a brief overview of the operations it performs:

- It first solves the initial model and asserts that the optimization was successful.
- It then constrains the next optimization to have the same minimum starvation as the previous optimization.
- If the first optimization was successful, it optimizes the best food consumption that goes to humans.
- After that, it constrains the next optimization to have the same total resilient foods in feed as the previous optimization.
- If the first optimization was successful and if food storage between years is allowed, it further optimizes to reduce fluctuations in food distribution.


**Args**

* **self**  : The optimizer object.
* **model**  : A PULP linear programming model object. This model should be already defined and configured.
* **variables**  : A dictionary containing the variables used in the optimization.
* **single_valued_constants**  : A dictionary of constant parameters that are used throughout the optimization process.


### .constrain_next_optimization_to_have_same_total_resilient_foods_in_feed
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/optimizer.py/#L262)
```python
.constrain_next_optimization_to_have_same_total_resilient_foods_in_feed(
   model_max_to_humans, variables
)
```

---
Constrains the next optimization to have the same total resilient foods in feed as the previous optimization.

**Args**

* **model_max_to_humans** (tuple) : A tuple containing the model and the maximizer string.
* **variables** (dict) : A dictionary containing the variables used in the optimization.


**Returns**

* **tuple**  : A tuple containing the updated model and variables.


### .add_conditions_to_model
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/optimizer.py/#L325)
```python
.add_conditions_to_model(
   model, month, conditions
)
```

---
Adds conditions to a given model for a given month.


**Args**

* **model** (Pulp ) : The model to which the conditions will be added.
* **month** (str) : The month for which the conditions will be added.
* **conditions** (dict) : A dictionary containing the conditions to be added to the model.


**Returns**

* **LpProblem**  : The updated model with the added conditions.


**Example**

* 'x > 0', 'condition2': 'y < 10'}

```python

>>> updated_model = add_conditions_to_model(model, 'January', conditions)
```

### .load_variable_names_and_prefixes
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/optimizer.py/#L352)
```python
.load_variable_names_and_prefixes()
```

---
This function initializes a dictionary of variable names and prefixes, and returns it.

**Args**

* **self**  : instance of the Optimizer class


**Returns**

* **variables** (dict) : a dictionary containing variable names and prefixes


### .optimize_best_food_consumption_to_go_to_humans
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/optimizer.py/#L439)
```python
.optimize_best_food_consumption_to_go_to_humans(
   model, variables, ASSERT_SUCCESSFUL_OPTIMIZATION, single_valued_constants
)
```

---
This function optimizes the amount of food to be allocated to humans while ensuring that the minimum demands for feed and biofuel are met.

**Args**

* **self**  : instance of the Optimizer class
* **model**  : the model to be optimized
* **variables**  : dictionary of variables used in the model
* **ASSERT_SUCCESSFUL_OPTIMIZATION**  : assertion to check if optimization was successful
* **single_valued_constants**  : dictionary of constants used in the model


**Returns**

* **tuple**  : a tuple containing the optimized model and the updated variables dictionary


### .reduce_fluctuations_with_a_final_optimization
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/optimizer.py/#L505)
```python
.reduce_fluctuations_with_a_final_optimization(
   model, variables, ASSERT_SUCCESSFUL_OPTIMIZATION, single_valued_constants
)
```

---
Optimize the smoothing objective function to reduce fluctuations in the model.


**Args**

* **model** (pulp.LpProblem) : The model to optimize.
* **variables** (dict) : A dictionary of variables used in the model.
* **ASSERT_SUCCESSFUL_OPTIMIZATION** (bool) : A flag to assert if optimization was successful.
* **single_valued_constants** (dict) : A dictionary of constants used in the model.


**Returns**

* **tuple**  : A tuple containing the optimized model and the updated variables dictionary.


### .constrain_next_optimization_to_have_same_minimum_starvation
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/optimizer.py/#L580)
```python
.constrain_next_optimization_to_have_same_minimum_starvation(
   model, variables
)
```

---
This function constrains the next optimization to have the same minimum starvation
as the previous optimization. It does this by setting the minimum value to the
previous optimization value and ensuring that consumed_kcals meets this value each month.


**Args**

* **self** (Optimizer) : The Optimizer object.
* **model** (pulp.LpProblem) : The optimization model.
* **variables** (dict) : A dictionary of variables used in the optimization.


**Returns**

* **tuple**  : A tuple containing the updated optimization model and variables.


**Example**

>>> model, variables = constrain_next_optimization_to_have_same_minimum_starvation(
...     self, model, variables
... )

### .create_lp_variables
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/optimizer.py/#L645)
```python
.create_lp_variables(
   prefix, month
)
```

---
Create a pulp variable with a given prefix and month.

**Args**

* **prefix** (str) : A string prefix for the variable name.
* **month** (int) : An integer representing the month for the variable name.


**Returns**

* **LpVariable**  : A pulp variable with a given name and lower bound of 0.


### .add_constraints
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/optimizer.py/#L660)
```python
.add_constraints(
   model, month, condition, prefix
)
```

---
Adds a constraint to the given model based on the given condition, month, and prefix.

**Args**

* **model** (Model) : The model to which the constraint will be added.
* **month** (str) : The month to which the constraint applies.
* **condition** (str) : The condition that the constraint enforces.
* **prefix** (str) : The prefix to use in the constraint name.


**Returns**

* **Model**  : The updated model with the added constraint.


### .add_variable_from_prefixes
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/optimizer.py/#L678)
```python
.add_variable_from_prefixes(
   variables, prefixes
)
```

---
Adds variables to the LP problem for each prefix and month.


**Args**

* **variables** (dict) : A dictionary containing the LP variables for each prefix and month.
* **prefixes** (list) : A list of prefixes for which variables need to be added.


**Returns**

* **dict**  : A dictionary containing the updated LP variables for each prefix and month.


**Example**

* [var1, var2, var3], 'prefix2': [var4, var5, var6]}
* [var1, var2, var3], 'prefix2': [var4, var5, var6], 'prefix3': [var7, var8, var9], 'prefix4': [var10, var11, var12]}

```python

>>> add_variable_from_prefixes(variables, prefixes)
```

### .add_seaweed_to_model
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/optimizer.py/#L706)
```python
.add_seaweed_to_model(
   month, variables
)
```

---
Adds seaweed to the model by setting conditions for the seaweed wet on farm, used area, and other variables.

**Args**

* **month** (int) : the current month of the simulation
* **variables** (dict) : a dictionary containing the current values of the variables in the simulation


**Returns**

* **dict**  : a dictionary containing the conditions for the seaweed wet on farm, used area, and other variables


### .add_stored_food_to_model_only_first_year
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/optimizer.py/#L772)
```python
.add_stored_food_to_model_only_first_year(
   month, variables
)
```

---
Adds stored food to the model for the first year only.

**Args**

* **month** (int) : the current month of the simulation
* **variables** (dict) : a dictionary containing the variables of the simulation


**Returns**

* **dict**  : a dictionary containing the conditions for the simulation


### .add_stored_food_to_model
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/optimizer.py/#L822)
```python
.add_stored_food_to_model(
   month, variables
)
```


### .add_culled_meat_to_model
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/optimizer.py/#L857)
```python
.add_culled_meat_to_model(
   month, variables
)
```

---
This function adds culled meat to the model based on the month and variables passed in.

**Args**

* **month** (int) : The month for which the culled meat is being added
* **variables** (dict) : A dictionary containing variables related to culled meat


**Returns**

* **dict**  : A dictionary containing conditions related to culled meat


**Example**

* [10, 20, 30],
* [20, 30, 40],
* [5, 10, 15]
* True, 'Culled_Meat_Eaten': 10}

```python

>>> variables = {
... }
>>> optimizer.add_culled_meat_to_model(1, variables)
```

### .add_outdoor_crops_to_model_no_storage
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/optimizer.py/#L901)
```python
.add_outdoor_crops_to_model_no_storage(
   month, variables
)
```

---
Adds a condition to the model that checks if the crops food storage is zero for a given month.

**Args**

* **month** (int) : The month to check the crops food storage for.
* **variables** (dict) : A dictionary containing the variables used in the model.


**Returns**

* **dict**  : A dictionary containing the condition to be added to the model.


**Example**

* [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}
* True}
>>> add_outdoor_crops_to_model_no_storage(3, variables)

### .handle_first_month
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/optimizer.py/#L923)
```python
.handle_first_month(
   variables, month
)
```

---
This function handles the first month of the simulation. It checks if the crops food storage is equal to the
outdoor crops production minus the crops food eaten. If this condition is met, it returns a dictionary with the
condition as a key and True as a value.

**Args**

* **self** (Optimizer) : the instance of the Optimizer class
* **variables** (dict) : a dictionary containing the variables used in the simulation
* **month** (int) : the current month of the simulation


**Returns**

* **dict**  : a dictionary containing the condition as a key and True as a value if the condition is met


### .handle_last_month
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/optimizer.py/#L946)
```python
.handle_last_month(
   variables, month, use_relocated_crops, initial_harvest_duration
)
```


### .handle_other_months
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/optimizer.py/#L968)
```python
.handle_other_months(
   variables, month, use_relocated_crops
)
```

---
This function handles months that are not January or July. It calculates the conditions for the month based on the
variables passed in and returns them.


**Args**

* **variables** (dict) : A dictionary containing variables for the simulation
* **month** (int) : The current month of the simulation
* **use_relocated_crops** (bool) : A boolean indicating whether or not to use relocated crops


**Returns**

* **dict**  : A dictionary containing the conditions for the month


**Example**

* [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200],
* [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120]
* True}

```python

>>> month = 2
>>> use_relocated_crops = False
>>> optimizer = Optimizer()
>>> optimizer.handle_other_months(variables, month, use_relocated_crops)
```

### .add_crops_food_eaten_with_nutrient_name
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/optimizer.py/#L1004)
```python
.add_crops_food_eaten_with_nutrient_name(
   variables, month, nutrient, lowercase_nutrient
)
```


### .create_linear_constraints_for_fat_and_protein_crops_food
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/optimizer.py/#L1018)
```python
.create_linear_constraints_for_fat_and_protein_crops_food(
   month, variables, fat_multiplier, protein_multiplier
)
```

---
This function creates linear constraints for fat and protein crops food.

**Args**

* **month** (int) : The month for which the constraints are being created
* **variables** (dict) : A dictionary containing variables used in the constraints
* **fat_multiplier** (float) : The multiplier for fat
* **protein_multiplier** (float) : The multiplier for protein


**Returns**

* **dict**  : A dictionary containing the created constraints


### .get_outdoor_crops_month_constants
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/optimizer.py/#L1074)
```python
.get_outdoor_crops_month_constants(
   use_relocated_crops, month
)
```

---
Calculates the constants for outdoor crops based on the month and whether or not
relocated crops are being used. Returns a tuple of the initial harvest duration,
fat multiplier, and protein multiplier.


**Args**

* **use_relocated_crops** (bool) : Whether or not relocated crops are being used.
* **month** (int) : The current month.


**Returns**

* **tuple**  : A tuple containing the initial harvest duration, fat multiplier, and
protein multiplier.


**Example**

>>> get_outdoor_crops_month_constants(True, 5)
(7, 0.4, 0.3)

### .add_outdoor_crops_to_model
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/optimizer.py/#L1114)
```python
.add_outdoor_crops_to_model(
   month, variables
)
```


### .add_methane_scp_to_model
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/optimizer.py/#L1147)
```python
.add_methane_scp_to_model(
   month, variables
)
```

---
Adds the methane SCP (Substrate Coefficient of Production) constraint to the model for a given month.
The constraint ensures that the total amount of methane SCP from all sources is less than or equal to the
maximum amount of methane SCP allowed for that month.


**Args**

* **month** (int) : The month for which the constraint is being added.
* **variables** (dict) : A dictionary containing the variables used in the constraint.


**Returns**

* **dict**  : A dictionary containing the methane SCP constraint.


**Example**

* [10, 20, 30],
* [5, 10, 15],
* [2, 4, 6]
* True}

```python

>>> optimizer = Optimizer()
>>> constraint = optimizer.add_methane_scp_to_model(1, variables)
>>> print(constraint)
```

### .add_cellulosic_sugar_to_model
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/optimizer.py/#L1187)
```python
.add_cellulosic_sugar_to_model(
   month, variables
)
```

---
Adds the amount of cellulosic sugar available in a given month to the model and checks if it is within the
limit of available kcals for that month.


**Args**

* **month** (int) : The month for which the cellulosic sugar is being added to the model.
* **variables** (dict) : A dictionary containing the variables for the model.


**Returns**

* **dict**  : A dictionary containing the conditions for the model.


**Example**

* [100, 200, 300],
* [50, 100, 150],
* [25, 50, 75]
* True}

```python

>>> optimizer = Optimizer()
>>> optimizer.add_cellulosic_sugar_to_model(1, variables)
```

### .add_percentage_intake_constraints
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/optimizer.py/#L1226)
```python
.add_percentage_intake_constraints(
   model, variables, month
)
```

---
Adds constraints to the optimization model based on the percentage intake of the nonhuman and human diets,
and the ratio of these resources used as biofuel.


**Args**

* **model** (object) : The optimization model object
* **variables** (dict) : A dictionary of variables used in the optimization model
* **month** (int) : The month for which the constraints are being added


**Returns**

* **object**  : The optimization model object with added constraints


### .add_feed_biofuel_to_model
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/optimizer.py/#L1289)
```python
.add_feed_biofuel_to_model(
   model, variables, month
)
```

---
Adds feed and biofuel variables to the model for a given month.


**Args**

* **model** (LpProblem) : The LpProblem model to add the variables to.
* **variables** (dict) : A dictionary containing the variables to add to the model.
* **month** (int) : The month for which to add the variables.


**Returns**

* **LpProblem**  : The Pulp model with the added variables.


**Example**

* [1, 2, 3],
* [4, 5, 6],
* [7, 8, 9],
* [10, 11, 12],
* [13, 14, 15],
* [16, 17, 18],
* [19, 20, 21],
* [22, 23, 24],
* [25, 26, 27],
* [28, 29, 30],

```python

>>> variables = {
... }
>>> optimizer = Optimizer()
>>> optimizer.add_feed_biofuel_to_model(model, variables, 0)
```

### .add_objectives_to_model
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/optimizer.py/#L1351)
```python
.add_objectives_to_model(
   model, variables, month, maximize_constraints
)
```

---
Adds objectives to the optimization model.


**Args**

* **model** (pulp.LpProblem) : The optimization model to which objectives are added.
* **variables** (dict) : A dictionary of variables used in the optimization model.
* **month** (int) : The month for which objectives are added.
* **maximize_constraints** (list) : A list of constraints to be maximized.


**Returns**

* **list**  : A list containing the updated model, variables, and maximize_constraints.

