#


## Parameters
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/parameters.py/#L27)
```python 

```




**Methods:**


### .compute_parameters_first_round
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/parameters.py/#L56)
```python
.compute_parameters_first_round(
   constants_inputs, time_consts_inputs, scenarios_loader
)
```

---
Computes the parameters for the model based on the inputs and scenarios provided.
This is relevant for the first round of optimization, with no feed assumed.



**Args**

* **constants_inputs** (dict) : A dictionary containing the constant inputs for the model.
* **scenarios_loader** (ScenariosLoader) : An instance of the ScenariosLoader class containing the scenario inputs.


**Returns**

* **tuple**  : A tuple containing the computed constants, time constants, and feed and biofuels.


**Raises**

* **AssertionError**  : If maintained meat needs to be added for continued feed usage or if the function is not
run for the first time.

### .get_second_round_kcals_with_redistributed_meat
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/parameters.py/#L165)
```python
.get_second_round_kcals_with_redistributed_meat(
   round_1_meat_kcals, round_2_meat_kcals, milk_kcals_round1, milk_kcals_round2
)
```

---
Gets a new array of kcals where the sum of kcals from meat remains the same, but the places where the meat was
originally larger than round 1 is reduced, and the places where the meat was less than round 1 is increased.

### .fill_negatives_with_positives
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/parameters.py/#L240)
```python
.fill_negatives_with_positives(
   arr
)
```


### .init_meat_and_dairy_and_feed_from_breeding_and_subtract_feed_biofuels_round1
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/parameters.py/#L265)
```python
.init_meat_and_dairy_and_feed_from_breeding_and_subtract_feed_biofuels_round1(
   constants_out, constants_inputs, time_consts
)
```


### .assert_constants_not_nan
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/parameters.py/#L369)
```python
.assert_constants_not_nan(
   consts_for_optimizer, time_consts
)
```

---
This function checks that there are no NaN values in the constants, as the linear optimizer
will fail in a mysterious way if there are. It does this by iterating through the consts_for_optimizer
and time_consts dictionaries and checking each value for NaN.


**Args**

* **consts_for_optimizer** (dict) : A dictionary of single-valued constants
* **time_consts** (dict) : A dictionary of time constants


**Returns**

None

### .assert_dictionary_value_not_nan
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/parameters.py/#L392)
```python
.assert_dictionary_value_not_nan(
   key, value
)
```

---
Asserts if a dictionary value is not NaN. If it is NaN, raises an AssertionError and prints the key.


**Args**

* **key** (str) : The key of the dictionary value being checked.
* **value** (Any) : The value of the dictionary being checked.


**Returns**

None


**Raises**

* **AssertionError**  : If the value is NaN.


### .init_scenario
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/parameters.py/#L424)
```python
.init_scenario(
   constants_out, constants_inputs
)
```

---
Initializes the scenario for some constants_out used for the optimizer.


**Args**

* **constants_out** (dict) : A dictionary containing constants used for the optimizer.
* **constants_inputs** (dict) : A dictionary containing input constants.


**Returns**

* **dict**  : A dictionary containing constants used for the optimizer.


### .set_nutrition_per_month
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/parameters.py/#L463)
```python
.set_nutrition_per_month(
   constants_out, constants_inputs
)
```

---
Set the nutrition per month for the simulation.

This function sets the nutrition per month for the simulation based on the input constants.
It assumes a 2100 kcals diet, and scales the "upper safe" nutrition from the spreadsheet down to this
"standard" level.
It also adds 20% loss, according to the sorts of loss seen in this spreadsheet.


**Args**

* **self**  : instance of the class
* **constants_out** (dict) : dictionary containing the output constants
* **constants_inputs** (dict) : dictionary containing the input constants


**Returns**

* **dict**  : dictionary containing the updated output constants


### .set_seaweed_params
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/parameters.py/#L522)
```python
.set_seaweed_params(
   constants_out, constants_inputs
)
```

---
This function sets the seaweed parameters by calling the Seaweed class methods and
assigning the resulting values to the constants_out dictionary. It also calculates
the built_area and growth_rates using the Seaweed class methods and returns them
along with the constants_out dictionary and the Seaweed object.


**Args**

* **constants_out** (dict) : dictionary containing the output constants
* **constants_inputs** (dict) : dictionary containing the input constants


**Returns**

* **tuple**  : a tuple containing the constants_out dictionary, built_area, growth_rates,
and the Seaweed object

### .init_outdoor_crops
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/parameters.py/#L574)
```python
.init_outdoor_crops(
   constants_out, constants_inputs
)
```

---
Initializes the outdoor crops parameters by calculating the rotation ratios and monthly production


**Args**

* **constants_out** (dict) : A dictionary containing the output constants
* **constants_inputs** (dict) : A dictionary containing the input constants


**Returns**

* **tuple**  : A tuple containing the updated constants_out and the outdoor_crops object

---
This function initializes the outdoor crops parameters by calculating the rotation ratios and monthly
production.
It takes in two dictionaries, constants_out and constants_inputs, which contain the output and input constants
respectively.
The function returns a tuple containing the updated constants_out and the outdoor_crops object.

### .init_stored_food
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/parameters.py/#L630)
```python
.init_stored_food(
   constants_out, constants_inputs, outdoor_crops
)
```

---
Initializes the stored food object and calculates the amount of stored food to use
based on the simulation starting month number. If ADD_STORED_FOOD is False, the initial
available stored food is set to zero.


**Args**

* **self**  : the object instance
* **constants_out** (dict) : dictionary containing output constants
* **constants_inputs** (dict) : dictionary containing input constants
* **outdoor_crops** (list) : list of outdoor crop objects


**Returns**

* **tuple**  : a tuple containing the updated constants_out dictionary and the stored_food object


### .init_fish_params
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/parameters.py/#L674)
```python
.init_fish_params(
   time_consts, constants_inputs, time_consts_inputs
)
```

---
Initializes seafood parameters, not including seaweed.


**Args**

* **constants_out** (dict) : A dictionary containing constants for output.
* **time_consts** (dict) : A dictionary containing monthly constants.
* **constants_inputs** (dict) : A dictionary containing constants inputted to parameters.


**Returns**

* **time_consts** (dict) : updated time_consts


### .init_greenhouse_params
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/parameters.py/#L695)
```python
.init_greenhouse_params(
   time_consts, constants_inputs, outdoor_crops
)
```

---
Initializes the greenhouse parameters and calculates the greenhouse yield per hectare.


**Args**

* **time_consts** (dict) : dictionary containing time constants
* **constants_inputs** (dict) : dictionary containing constant inputs
* **outdoor_crops** (OutdoorCrops) : instance of the OutdoorCrops class


**Returns**

* **dict**  : dictionary containing updated time constants


### .init_cs_params
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/parameters.py/#L747)
```python
.init_cs_params(
   constants_out, time_consts, constants_inputs
)
```

---
Initializes the parameters for the cellulosic sugar model.


**Args**

* **time_consts** (dict) : A dictionary containing time constants.
* **constants_inputs** (dict) : A dictionary containing inputs for the constants.


**Returns**

* **tuple**  : A tuple containing the updated time constants dictionary and the
calculated cellulosic sugar object.

---
This function initializes the parameters for the cellulosic sugar model by
creating a CellulosicSugar object and calculating the monthly cellulosic sugar
production using the inputs provided in the constants_inputs dictionary. The
resulting object is then added to the time_consts dictionary.

### .init_scp_params
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/parameters.py/#L778)
```python
.init_scp_params(
   constants_out, time_consts, constants_inputs
)
```

---
Initializes the parameters for single cell protein.


**Args**

* **time_consts** (dict) : A dictionary containing time constants.
* **constants_inputs** (dict) : A dictionary containing constant inputs.


**Returns**

* **tuple**  : A tuple containing the updated time constants dictionary and the methane_scp object.


### .init_meat_and_dairy_and_feed_from_breeding
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/parameters.py/#L813)
```python
.init_meat_and_dairy_and_feed_from_breeding(
   constants_inputs, feed_meat_object, feed_and_biofuels_class, meat_and_dairy,
   constants_out, time_consts
)
```


### .get_animal_meat_dictionary
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/parameters.py/#L860)
```python
.get_animal_meat_dictionary(
   constants_inputs, feed_meat_object, meat_and_dairy
)
```


### .calculate_meat_from_feed_results
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/parameters.py/#L939)
```python
.calculate_meat_from_feed_results(
   constants_inputs, constants_out, time_consts, meat_and_dairy,
   feed_meat_object
)
```

---
Calculates the amount of culled meat from feed results and updates the constants_out and time_consts
dictionaries.


**Args**

* **constants_inputs** (dict) : dictionary containing input constants
* **constants_out** (dict) : dictionary containing constants to be updated
* **time_consts** (dict) : dictionary containing time constants to be updated
* **meat_and_dairy** (MeatAndDairy) : instance of MeatAndDairy class
* **feed_dairy_meat_results** (dict) : dictionary containing feed, dairy, and meat results


**Returns**

* **tuple**  : tuple containing updated constants_out and time_consts dictionaries


### .calculate_non_meat_and_dairy_from_feed_results
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/parameters.py/#L1016)
```python
.calculate_non_meat_and_dairy_from_feed_results(
   constants_inputs, constants_out, time_consts, dairy_pop, meat_and_dairy
)
```

---
Calculates the non-culled meat and dairy from feed results.

**Args**

* **self**  : instance of the Parameters class
* **constants_inputs** (dict) : dictionary of input constants
* **constants_out** (dict) : dictionary of output constants
* **time_consts** (dict) : dictionary of time constants
* **dairy_pop** (float) : number of dairy cows
* **meat_and_dairy** (MeatAndDairy) : instance of the MeatAndDairy class


**Returns**

* **tuple**  : tuple containing constants_out and time_consts


### .compute_parameters_second_round
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/parameters.py/#L1085)
```python
.compute_parameters_second_round(
   constants_inputs, constants_out_round1, time_consts_round1,
   interpreted_results_round1
)
```

---
Compute the parameters for the second round of optimizations, where we now know the amount of feed
available for animals after humans have used all they need for their minimum nutritional needs.

### .calculate_human_consumption_for_min_needs
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/parameters.py/#L1248)
```python
.calculate_human_consumption_for_min_needs(
   constants_inputs, interpreted_results_round1, extra_meat_round2
)
```

---
We run through each month and determine the amount consumed each month of all foods.
However, any human consumption which exceeds the starvation percentage is ignored.
To determine when to start ignoring human consumption, we loop through the different foods
in the following order of priority for humans to consume:
  First fish, then meat, then dairy, then greenhouse crops, then outdoor crops, then stored food,
  then scp, then cs, then seaweed.

NOTE: We only use variables set here in the optimizer that are NOT  greenhouses or dairy or fish, because
greenhouses and dairy and fish are not actually added as variables in the model (they are added as monthly
constants to sum of human consumption) and they cannot be optimized.
Furthermore, these foods always go to humans anyway.
We only add these variables for the purposes of validation in the case
that they sum up to human caloric minimum needs.

### .assert_consumption_within_limits
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/parameters.py/#L1478)
```python
.assert_consumption_within_limits(
   human_food_consumption, kcals_daily_maximum
)
```

---
Asserts that each Food object in the human_food_consumption dictionary is less than
or equal to kcals_daily_maximum for all months.

### .increase_biofuels_then_feed
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/parameters.py/#L1504)
```python
.increase_biofuels_then_feed(
   biofuel, feed, increase, max_biofuel, max_feed, total_crops_available
)
```


### .compute_parameters_third_round
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/parameters.py/#L1544)
```python
.compute_parameters_third_round(
   constants_inputs, constants_out_round1, constants_out_round2,
   time_consts_round1, time_consts_round2, interpreted_results_round1,
   interpreted_results_round2, feed_and_biofuels_class, feed_demand,
   biofuels_demand, feed_meat_object_round1
)
```

