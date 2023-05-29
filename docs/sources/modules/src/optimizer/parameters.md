#


## Parameters
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/parameters.py/#L26)
```python 

```




**Methods:**


### .compute_parameters
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/parameters.py/#L55)
```python
.compute_parameters(
   constants_inputs, scenarios_loader
)
```

---
Computes the parameters for the model based on the inputs and scenarios provided.


**Args**

* **constants_inputs** (dict) : A dictionary containing the constant inputs for the model.
* **scenarios_loader** (ScenariosLoader) : An instance of the ScenariosLoader class containing the scenario inputs.


**Returns**

* **tuple**  : A tuple containing the computed constants, time constants, and feed and biofuels.


**Raises**

* **AssertionError**  : If maintained meat needs to be added for continued feed usage or if the function is not run for the first time.


### .init_meat_and_dairy_and_feed_from_breeding_and_subtract_feed_biofuels
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/parameters.py/#L158)
```python
.init_meat_and_dairy_and_feed_from_breeding_and_subtract_feed_biofuels(
   constants_out, constants_inputs, time_consts, outdoor_crops, methane_scp,
   cellulosic_sugar, seaweed, stored_food
)
```

---
Calculates the expected amount of livestock if breeding were quickly reduced and slaughter only increased slightly,
then using that we calculate the feed they would use given the expected input animal populations over time.

**Args**

* **self**  : instance of the class
* **constants_out** (dict) : dictionary containing output constants
* **constants_inputs** (dict) : dictionary containing input constants
* **time_consts** (dict) : dictionary containing time constants
* **outdoor_crops** (dict) : dictionary containing outdoor crop constants
* **methane_scp** (dict) : dictionary containing methane SCP constants
* **cellulosic_sugar** (dict) : dictionary containing cellulosic sugar constants
* **seaweed** (dict) : dictionary containing seaweed constants
* **stored_food** (dict) : dictionary containing stored food constants


**Returns**

* **tuple**  : tuple containing constants_out, time_consts, and feed_and_biofuels


### .assert_constants_not_nan
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/parameters.py/#L245)
```python
.assert_constants_not_nan(
   single_valued_constants, time_consts
)
```

---
This function checks that there are no NaN values in the constants, as the linear optimizer
will fail in a mysterious way if there are. It does this by iterating through the single_valued_constants
and time_consts dictionaries and checking each value for NaN.


**Args**

* **single_valued_constants** (dict) : A dictionary of single-valued constants
* **time_consts** (dict) : A dictionary of time constants


**Returns**

None

### .assert_dictionary_value_not_nan
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/parameters.py/#L268)
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
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/parameters.py/#L300)
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
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/parameters.py/#L340)
```python
.set_nutrition_per_month(
   constants_out, constants_inputs
)
```

---
Set the nutrition per month for the simulation.

This function sets the nutrition per month for the simulation based on the input constants.
It assumes a 2100 kcals diet, and scales the "upper safe" nutrition from the spreadsheet down to this "standard" level.
It also adds 20% loss, according to the sorts of loss seen in this spreadsheet.


**Args**

* **self**  : instance of the class
* **constants_out** (dict) : dictionary containing the output constants
* **constants_inputs** (dict) : dictionary containing the input constants


**Returns**

* **dict**  : dictionary containing the updated output constants


### .set_seaweed_params
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/parameters.py/#L398)
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
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/parameters.py/#L449)
```python
.init_outdoor_crops(
   constants_out, constants_inputs
)
```

---
Initializes the outdoor crops parameters by calculating the rotation ratios and monthly production

**Args**

* **constants_out** (dict) : dictionary containing the output constants
* **constants_inputs** (dict) : dictionary containing the input constants


**Returns**

* **tuple**  : tuple containing the updated constants_out and the outdoor_crops object


### .init_stored_food
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/parameters.py/#L491)
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
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/parameters.py/#L533)
```python
.init_fish_params(
   time_consts, constants_inputs
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
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/parameters.py/#L554)
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
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/parameters.py/#L601)
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
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/parameters.py/#L643)
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
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/parameters.py/#L687)
```python
.init_meat_and_dairy_and_feed_from_breeding(
   constants_inputs, reduction_in_dairy_calves,
   use_grass_and_residues_for_dairy, cao, feed_and_biofuels, meat_and_dairy,
   feed_ratio, constants_out, time_consts
)
```


### .calculate_culled_meat_from_feed_results
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/parameters.py/#L887)
```python
.calculate_culled_meat_from_feed_results(
   constants_out, time_consts, meat_and_dairy, feed_dairy_meat_results
)
```


### .calculate_non_culled_meat_and_dairy_from_feed_results
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/parameters.py/#L908)
```python
.calculate_non_culled_meat_and_dairy_from_feed_results(
   constants_inputs, constants_out, time_consts, dairy_pop, meat_and_dairy
)
```


### .init_meat_and_dairy_params
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/parameters.py/#L974)
```python
.init_meat_and_dairy_params(
   constants_inputs, constants_out, time_consts, feed_and_biofuels,
   outdoor_crops
)
```

---
Initializes meat and dairy parameters.


**Args**

* **constants_inputs** (dict) : dictionary of input constants
* **constants_out** (dict) : dictionary of output constants
* **time_consts** (dict) : dictionary of time constants
* **feed_and_biofuels** (dict) : dictionary of feed and biofuel constants
* **outdoor_crops** (dict) : dictionary of outdoor crop constants


**Returns**

* **tuple**  : tuple containing meat and dairy object, constants_out dictionary, and time_consts dictionary


### .init_grazing_params
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/parameters.py/#L1026)
```python
.init_grazing_params(
   constants_inputs, time_consts, meat_and_dairy
)
```

---
Initializes grazing parameters for the simulation.


**Args**

* **constants_inputs** (dict) : A dictionary containing constant inputs for the simulation.
* **time_consts** (dict) : A dictionary containing time constants for the simulation.
* **meat_and_dairy** (MeatAndDairy) : An instance of the MeatAndDairy class.


**Returns**

* **tuple**  : A tuple containing the updated time constants and the updated meat_and_dairy instance.


### .init_grain_fed_meat_params
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/parameters.py/#L1081)
```python
.init_grain_fed_meat_params(
   time_consts, meat_and_dairy, feed_and_biofuels, constants_inputs,
   outdoor_crops
)
```

---
Initializes grain-fed meat parameters by calculating the amount of grain-fed meat and milk
produced from human-edible feed, and updating the time constants dictionary with the results.


**Args**

* **self**  : instance of the class
* **time_consts** (dict) : dictionary containing time constants
* **meat_and_dairy** (MeatAndDairy) : instance of MeatAndDairy class
* **feed_and_biofuels** (FeedAndBiofuels) : instance of FeedAndBiofuels class
* **constants_inputs** (dict) : dictionary containing constant inputs
* **outdoor_crops** (OutdoorCrops) : instance of OutdoorCrops class


**Returns**

* **tuple**  : updated time constants dictionary and instance of MeatAndDairy class


### .init_culled_meat_params
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/parameters.py/#L1174)
```python
.init_culled_meat_params(
   constants_inputs, constants_out, time_consts, meat_and_dairy
)
```

---
Initializes the parameters for culled meat, which is based on the amount that wouldn't be maintained
(excluding maintained cattle as well as maintained chicken and pork). This calculation is pre-waste for
the meat maintained of course (no waste applied to livestock maintained counts from which we determined
the amount of meat which can be culled). The actual culled meat returned is post waste.


**Args**

* **constants_inputs** (dict) : dictionary of input constants
* **constants_out** (dict) : dictionary of output constants
* **time_consts** (dict) : dictionary of time constants
* **meat_and_dairy** (MeatAndDairy) : instance of MeatAndDairy class


**Returns**

* **tuple**  : tuple containing updated constants_out, time_consts, and meat_and_dairy

