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
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/optimizer.py/#L22)
```python
.optimize_nonhuman_consumption(
   single_valued_constants, time_consts
)
```


### .optimize_to_humans
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/optimizer.py/#L62)
```python
.optimize_to_humans(
   single_valued_constants, time_consts
)
```


### .add_variables_and_constraints_to_model
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/optimizer.py/#L115)
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
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/optimizer.py/#L164)
```python
.run_optimizations_to_humans(
   model, variables, single_valued_constants
)
```

---
This function is part of a resource allocation system aiming to optimize food distribution.

### Parameters:

- `model`: A PULP linear programming model object. This model should be already defined and configured.
- `single_valued_constants`: A dictionary of constant parameters that are used throughout the optimization process.

### Behavior:

The function executes a series of optimization steps. After solving the initial model, it performs several more rounds of optimization, each with added constraints based on the results of the previous round.

Here's a brief overview of the operations it performs:

- It first solves the initial model and asserts that the optimization was successful.
- It then constrains the next optimization to have the same minimum starvation as the previous optimization.
- If the first optimization was successful, it optimizes the best food consumption that goes to humans.
- After that, it constrains the next optimization to have the same total resilient foods in feed as the previous optimization.
- If the first optimization was successful and if food storage between years is allowed, it further optimizes to reduce fluctuations in food distribution.

### .constrain_next_optimization_to_have_same_total_resilient_foods_in_feed
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/optimizer.py/#L226)
```python
.constrain_next_optimization_to_have_same_total_resilient_foods_in_feed(
   model_max_to_humans, variables
)
```

---
here we're constraining the previous optimization to the previously determined optimal value

### .add_conditions_to_model
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/optimizer.py/#L276)
```python
.add_conditions_to_model(
   model, month, conditions
)
```


### .load_variable_names_and_prefixes
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/optimizer.py/#L283)
```python
.load_variable_names_and_prefixes()
```


### .optimize_best_food_consumption_to_go_to_humans
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/optimizer.py/#L357)
```python
.optimize_best_food_consumption_to_go_to_humans(
   model, variables, ASSERT_SUCCESSFUL_OPTIMIZATION, single_valued_constants
)
```

---
in this case we are trying to maximize the amount to humans, as long as feed and biofuel
minimum demands are satisfied
this allows the "best" food (stored food and outdoor growing) to go to humans if possible

### .reduce_fluctuations_with_a_final_optimization
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/optimizer.py/#L405)
```python
.reduce_fluctuations_with_a_final_optimization(
   model, variables, ASSERT_SUCCESSFUL_OPTIMIZATION, single_valued_constants
)
```

---
Optimize the smoothing objective function.

### .constrain_next_optimization_to_have_same_minimum_starvation
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/optimizer.py/#L455)
```python
.constrain_next_optimization_to_have_same_minimum_starvation(
   model, variables
)
```

---
we set min_value to the previous optimization value and make
sure consumed_kcals meets this value each month

### .create_lp_variables
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/optimizer.py/#L503)
```python
.create_lp_variables(
   prefix, month
)
```

---
create a pulp variable, always positive

### .add_constraints
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/optimizer.py/#L511)
```python
.add_constraints(
   model, month, condition, prefix
)
```


### .add_variable_from_prefixes
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/optimizer.py/#L516)
```python
.add_variable_from_prefixes(
   variables, prefixes
)
```


### .add_seaweed_to_model
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/optimizer.py/#L523)
```python
.add_seaweed_to_model(
   month, variables
)
```


### .add_stored_food_to_model_only_first_year
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/optimizer.py/#L575)
```python
.add_stored_food_to_model_only_first_year(
   month, variables
)
```


### .add_stored_food_to_model
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/optimizer.py/#L607)
```python
.add_stored_food_to_model(
   month, variables
)
```


### .add_culled_meat_to_model
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/optimizer.py/#L642)
```python
.add_culled_meat_to_model(
   month, variables
)
```


### .add_outdoor_crops_to_model_no_storage
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/optimizer.py/#L664)
```python
.add_outdoor_crops_to_model_no_storage(
   month, variables
)
```


### .handle_first_month
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/optimizer.py/#L670)
```python
.handle_first_month(
   variables, month
)
```


### .handle_last_month
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/optimizer.py/#L680)
```python
.handle_last_month(
   variables, month, use_relocated_crops, initial_harvest_duration
)
```


### .handle_other_months
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/optimizer.py/#L702)
```python
.handle_other_months(
   variables, month, use_relocated_crops
)
```


### .add_crops_food_eaten_with_nutrient_name
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/optimizer.py/#L713)
```python
.add_crops_food_eaten_with_nutrient_name(
   variables, month, nutrient, lowercase_nutrient
)
```


### .create_linear_constraints_for_fat_and_protein_crops_food
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/optimizer.py/#L727)
```python
.create_linear_constraints_for_fat_and_protein_crops_food(
   month, variables, fat_multiplier, protein_multiplier
)
```


### .get_outdoor_crops_month_constants
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/optimizer.py/#L761)
```python
.get_outdoor_crops_month_constants(
   use_relocated_crops, month
)
```


### .add_outdoor_crops_to_model
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/optimizer.py/#L777)
```python
.add_outdoor_crops_to_model(
   month, variables
)
```


### .add_methane_scp_to_model
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/optimizer.py/#L810)
```python
.add_methane_scp_to_model(
   month, variables
)
```


### .add_cellulosic_sugar_to_model
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/optimizer.py/#L822)
```python
.add_cellulosic_sugar_to_model(
   month, variables
)
```


### .add_percentage_intake_constraints
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/optimizer.py/#L834)
```python
.add_percentage_intake_constraints(
   model, variables, month
)
```

---
Percentage intake of the nonhuman and human diets, and the ratio of these resources used as biofuel

### .add_feed_biofuel_to_model
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/optimizer.py/#L883)
```python
.add_feed_biofuel_to_model(
   model, variables, month
)
```


### .add_objectives_to_model
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/optimizer.py/#L910)
```python
.add_objectives_to_model(
   model, variables, month, maximize_constraints
)
```

