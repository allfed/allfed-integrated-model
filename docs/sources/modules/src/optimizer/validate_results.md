#


## Validator
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/validate_results.py/#L14)
```python 
Validator()
```




**Methods:**


### .validate_results
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/validate_results.py/#L15)
```python
.validate_results(
   extracted_results, interpreted_results, time_consts, percent_fed_from_model,
   optimization_type, country_code
)
```

---
Validates the results of the model by ensuring that the optimizer returns the same as the sum of nutrients,
that zero kcals have zero fat and protein, that there are no NaN values, and that all values are greater than or
equal to zero.


**Args**

* **model** (Model) : The model to validate the results of.
* **extracted_results** (ExtractedResults) : The extracted results from the model.
* **interpreted_results** (InterpretedResults) : The interpreted results from the model.


**Returns**

None

### .ensure_all_time_constants_units_are_billion_kcals
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/validate_results.py/#L60)
```python
.ensure_all_time_constants_units_are_billion_kcals(
   time_consts
)
```


### .check_constraints_satisfied
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/validate_results.py/#L73)
```python
.check_constraints_satisfied(
   model, maximize_constraints, variables
)
```

---
This function checks if all constraints are satisfied by the final values of the variables.
It takes a really long time to run, so it's run infrequently.


**Args**

* **model** (pulp.LpProblem) : The optimization model
* **maximize_constraints** (list) : A list of constraints to maximize
* **variables** (list) : A list of variables to check constraints against


**Returns**

None


**Raises**

* **AssertionError**  : If a constraint is not satisfied


### .ensure_optimizer_returns_same_as_sum_nutrients
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/validate_results.py/#L160)
```python
.ensure_optimizer_returns_same_as_sum_nutrients(
   percent_fed_from_model, interpreted_results, INCLUDE_FAT, INCLUDE_PROTEIN,
   country_code
)
```

---
ensure there was no major error in the optimizer or in analysis which caused
the sums reported to differ between adding up all the extracted variables and
just look at the reported result of the objective of the optimizer

### .ensure_zero_kcals_have_zero_fat_and_protein
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/validate_results.py/#L223)
```python
.ensure_zero_kcals_have_zero_fat_and_protein(
   interpreted_results
)
```

---
Checks that for any month where kcals is zero for any of the foods,
then fat and protein must also be zero.


**Args**

* **interpreted_results** (InterpretedResults) : An instance of the InterpretedResults class


**Returns**

None

---
Notes:
    This function is called to ensure that the kcals, fat and protein values are consistent
    for each food source, feed and biofuels independently.


**Raises**

* **AssertionError**  : If the kcals value is zero but the fat or protein value is non-zero.


### .ensure_never_nan
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/validate_results.py/#L271)
```python
.ensure_never_nan(
   interpreted_results
)
```

---
This function checks that the interpreter results are always defined as a real number.
It does this by calling the make_sure_not_nan() method on each of the interpreted_results attributes.
If any of the attributes contain NaN values, an exception will be raised.


**Args**

* **interpreted_results** (InterpretedResults) : An instance of the InterpretedResults class.


**Raises**

* **ValueError**  : If any of the interpreted_results attributes contain NaN values.


**Returns**

None

### .ensure_all_greater_than_or_equal_to_zero
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/validate_results.py/#L300)
```python
.ensure_all_greater_than_or_equal_to_zero(
   interpreted_results
)
```

---
Checks that all the results variables are greater than or equal to zero.

**Args**

* **interpreted_results** (InterpretedResults) : An instance of the InterpretedResults class


**Raises**

* **AssertionError**  : If any of the results variables are less than zero


### .assert_population_not_increasing
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/validate_results.py/#L345)
```python
.assert_population_not_increasing(
   meat_dictionary, epsilon = 0.1, round = None
)
```

---
Checks that the animal populations are never increasing with time (currently
the condition is considered satisfied if it is met to within 10%)


**Args**

* **meat_dictionary** (dict) : dictionary containing meat constants
* **epsilon** (float) : threshold for the relative change in population
* **round** (int) : round of optimization (optional, just for printing purposes)


**Returns**

None

### .assert_round2_meat_and_population_greater_than_round1
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/validate_results.py/#L373)
```python
.assert_round2_meat_and_population_greater_than_round1(
   meat_dictionary_first_round, meat_dictionary_second_round, epsilon = 0.01,
   small_number = 100
)
```

---
Asserts that the total meat produced over the simulation timespan and the average animal population
in the second round of optimization are greater than the first round. This test is repeated for each
animal type.


**Args**

* **meat_dictionary_first_round** (dict) : dictionary containing meat constants for the first round
* **meat_dictionary_second_round** (dict) : dictionary containing meat constants for the second round
* **epsilon** (float) : tolerance threshold for comparisons (set to 1% by default, smaller values were
    found to be too strict)
* **small_number** (float) : threshold for the total meat produced or average animal population below which
    the test is not performed (set to 10 by default)


**Returns**

None

### .verify_minimum_food_consumption_sum_round2
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/validate_results.py/#L418)
```python
.verify_minimum_food_consumption_sum_round2(
   interpreted_results_round1, min_human_food_consumption, epsilon = 0.0001
)
```

---
Verify that the sum of all foods for every month is always smaller or equal
to the minimum food consumption targeted during round 2.
This is only relevant if only kcals is required in the optimization, otherwise
it is possible that more calories are consumed than the minimum targeted in order
to meet the fat and protein requirements.


**Args**

* **interpreted_results_round1** (InterpretedResults) : interpreted results from round 1 of optimization
* **min_human_food_consumption** (dict) : dictionary containing the minimum food consumption from
    calculate_human_consumption_for_min_needs
* **epsilon** (float) : tolerance threshold for the sum of all foods (set to 0.01% by default)


**Returns**

None

### .verify_food_usage_priorities_round2
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/validate_results.py/#L461)
```python
.verify_food_usage_priorities_round2(
   interpreted_results_round1, min_human_food_consumption, epsilon = 0.0001
)
```

---
Verify that the percentage of each food used (compared to the total amount of that food availabe)
decreases when looking at foods in this order: fish, meat, dairy, greenhouse, outdoor crops, stored food,
methane scp, cellulosic sugar, seaweed.
Only relevant if only kcals is required in the optimization.


**Args**

* **interpreted_results_round1** (InterpretedResults) : interpreted results from round 1 of optimization
* **min_human_food_consumption** (dict) : dictionary containing the minimum food consumption from
    calculate_human_consumption_for_min_needs
* **epsilon** (float) : tolerance threshold for comparisons (set to 0.01% by default)


**Returns**

None

### .assert_meat_dairy_doesnt_decrease_round_2
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/validate_results.py/#L546)
```python
.assert_meat_dairy_doesnt_decrease_round_2(
   meat_running_available_round1, meat_running_available_round2,
   milk_kcals_round1, milk_kcals_round2, epsilon = 0.01
)
```


### .assert_fewer_calories_round2_than_round3
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/validate_results.py/#L563)
```python
.assert_fewer_calories_round2_than_round3(
   interpreted_results_round2, interpreted_results_round3, epsilon = 0.1,
   absepsilon = 0.1
)
```

---
Asserts that the total calories consumed in round 2 is less than or equal to round 3, for
all months.
This is only relevant if only kcals is required in the optimization.


**Args**

* **interpreted_results_round2** (InterpretedResults) : interpreted results from round 2 of optimization
* **interpreted_results_round3** (InterpretedResults) : interpreted results from round 3 of optimization
* **epsilon** (float) : tolerance threshold for comparison (set to 1e-4 by default)


**Returns**

None

### .assert_feed_used_below_feed_demand
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/validate_results.py/#L647)
```python
.assert_feed_used_below_feed_demand(
   feed_demand, interpreted_results, round, epsilon = 0.0001
)
```

---
Asserts that the feed used is less than or equal to the feed demand for each month.

**Args**

* **interpreted_results** (InterpretedResults) : interpreted results from any round of optimization
* **round** (int) : round of optimization number (for more useful error messages)
* **epsilon** (float) : tolerance threshold for comparison (set to 1e-4 by default)


**Returns**

None

### .assert_biofuels_used_below_biofuels_demand
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/validate_results.py/#L677)
```python
.assert_biofuels_used_below_biofuels_demand(
   biofuels_demand, interpreted_results, round, epsilon = 0.0001
)
```

---
Asserts that the biofuels used is less than or equal to the biofuels demand for each month.

**Args**

* **interpreted_results** (InterpretedResults) : interpreted results from any round of optimization
* **round** (int) : round of optimization number (for more useful error messages)
* **epsilon** (float) : tolerance threshold for comparison (set to 1e-6 by default)


**Returns**

None

### .assert_feed_used_round3_below_feed_used_round2
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/validate_results.py/#L710)
```python
.assert_feed_used_round3_below_feed_used_round2(
   interpreted_results_round2, interpreted_results_round3, epsilon = 0.0001
)
```


### .sum_feed_sources
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/validate_results.py/#L731)
```python
.sum_feed_sources(
   interpreted_results
)
```

---
Sums all the feed sources together.

### .sum_biofuel_sources
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/validate_results.py/#L756)
```python
.sum_biofuel_sources(
   interpreted_results
)
```

---
Sums all the biofuels sources together.

### .assert_feed_and_biofuel_used_is_zero_if_humans_are_starving
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/validate_results.py/#L780)
```python
.assert_feed_and_biofuel_used_is_zero_if_humans_are_starving(
   interpreted_results, epsilon = 0.001
)
```


### .assert_round3_percent_fed_not_lower_than_round1
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/validate_results.py/#L850)
```python
.assert_round3_percent_fed_not_lower_than_round1(
   minimum_people_percent_fed, percent_fed_round1, percent_fed_round3,
   epsilon = 1
)
```

