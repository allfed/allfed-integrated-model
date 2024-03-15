#


## Extractor
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/extract_results.py/#L13)
```python 
Extractor(
   constants
)
```




**Methods:**


### .extract_results
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/extract_results.py/#L26)
```python
.extract_results(
   model, variables, time_consts
)
```

---
Extracts the results from the model and stores them in the Extractor object.

**Args**

* **model** (pysd.PySD) : the PySD model object
* **variables** (dict) : a dictionary of model variables
* **time_consts** (dict) : a dictionary of time constants


**Returns**

* **Extractor**  : the Extractor object with the extracted results stored in its attributes


### .to_monthly_list
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/extract_results.py/#L138)
```python
.to_monthly_list(
   variables, conversion
)
```

---
Converts a list of variables to a monthly list of values.

**Args**

* **variables** (list) : A list of variables to be converted.
* **conversion** (float) : A conversion factor to be applied to each variable.


**Returns**

* **array**  : A numpy array of the converted monthly values.


### .to_monthly_list_outdoor_crops_kcals
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/extract_results.py/#L174)
```python
.to_monthly_list_outdoor_crops_kcals(
   crops_food_eaten, crops_kcals_produced, conversion
)
```

---
This function calculates the amount of outdoor crop production that is immediately eaten and the
amount that is stored for later consumption. If more is eaten than produced, the difference is
attributed to the eating of stored up crops.


**Args**

* **crops_food_eaten**  : list of the amount of crops eaten each month
* **crops_kcals_produced**  : list of the amount of crop production (kcals) each month
* **conversion**  : conversion factor from kcals to another unit of measurement


**Returns**

- A list of two lists:
    - The first list contains the amount of outdoor crop production (converted to the specified
    unit of measurement) that is immediately eaten each month.
    - The second list contains the amount of outdoor crop production (converted to the specified
    unit of measurement) that is stored for later consumption each month.

### .get_greenhouse_results
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/extract_results.py/#L233)
```python
.get_greenhouse_results(
   greenhouse_crops
)
```


### .create_food_object_from_fat_protein_variables
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/extract_results.py/#L241)
```python
.create_food_object_from_fat_protein_variables(
   production_kcals, production_fat, production_protein
)
```

---
This function creates a Food object from the given production_kcals, production_fat, and production_protein.

**Args**

* **production_kcals** (float) : the amount of kcals produced
* **production_fat** (float) : the amount of fat produced
* **production_protein** (float) : the amount of protein produced


**Returns**

* **Food**  : a Food object with kcals, fat, and protein attributes


### .extract_generic_results
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/extract_results.py/#L285)
```python
.extract_generic_results(
   production_kcals, ratio_kcals, ratio_fat, ratio_protein, constants
)
```

---
Extracts generic results from production_kcals, ratio_kcals, ratio_fat, ratio_protein, and constants.

**Args**

* **production_kcals** (float) : total production kcals
* **ratio_kcals** (float) : ratio of kcals to production kcals
* **ratio_fat** (float) : ratio of fat to production kcals
* **ratio_protein** (float) : ratio of protein to production kcals
* **constants** (dict) : dictionary of constants used in the calculations


**Returns**

* **Food**  : a Food object containing the extracted results


### .extract_outdoor_crops_results
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/extract_results.py/#L328)
```python
.extract_outdoor_crops_results(
   crops_food_to_humans, crops_food_to_humans_fat, crops_food_to_humans_protein,
   crops_food_biofuel, crops_food_biofuel_fat, crops_food_biofuel_protein,
   crops_food_feed, crops_food_feed_fat, crops_food_feed_protein,
   outdoor_crops_production
)
```

---
Extracts results for outdoor crops and assigns them to the corresponding food objects.
Calculates outdoor crop production for humans and assigns the values to the corresponding food object.
Validates if immediate and new stored sources add up correctly.
Calculates and assigns new stored outdoor crops values.
Calculates and assigns immediate outdoor crops values.
Validates if the total outdoor growing production has not changed.


**Returns**

None

### .calculate_outdoor_crops_kcals
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/extract_results.py/#L451)
```python
.calculate_outdoor_crops_kcals(
   crops_food_to_humans, to_humans_outdoor_crop_production
)
```


### .validate_sources_add_up
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/extract_results.py/#L460)
```python
.validate_sources_add_up(
   billions_fed_immediate_outdoor_crops_kcals,
   billions_fed_new_stored_outdoor_crops_kcals
)
```

---
Validates that the sum of immediate and new stored sources of outdoor crops for humans
matches the input of outdoor crop for humans.


**Args**

* **billions_fed_immediate_outdoor_crops_kcals** (list) : A list of billions of kcals fed
    from immediate outdoor crops to humans.
* **billions_fed_new_stored_outdoor_crops_kcals** (list) : A list of billions of kcals fed
    from new stored outdoor crops to humans.


**Returns**

None


**Example**


```python

>>> extractor.outdoor_crops_to_humans.kcals = [1, 2, 3]
>>> extractor.validate_sources_add_up([0.5, 1, 1.5], [0.5, 1, 1.5])
None

```

**Raises**

* **AssertionError**  : If the sum of immediate and new stored sources of outdoor crops for
    humans does not match the input of outdoor crop for humans.


### .set_new_stored_outdoor_crops_values
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/extract_results.py/#L498)
```python
.set_new_stored_outdoor_crops_values(
   billions_fed_new_stored_outdoor_crops_kcals
)
```

---
Sets the values of new_stored_outdoor_crops attribute of the Extractor class with the given
billions_fed_new_stored_outdoor_crops_kcals.

**Args**

* **self** (Extractor) : An instance of the Extractor class.
* **billions_fed_new_stored_outdoor_crops_kcals** (list) : A list of kcals in billions fed to new stored outdoor
crops each month.

**Returns**

None

### .set_immediate_outdoor_crops_values
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/extract_results.py/#L521)
```python
.set_immediate_outdoor_crops_values(
   billions_fed_immediate_outdoor_crops_kcals
)
```

---
Sets the values of immediate outdoor crops in the Extractor object.

**Args**

* **self** (Extractor) : The Extractor object.
* **billions_fed_immediate_outdoor_crops_kcals** (list) : A list of kcals fed to billions of people each month.


**Returns**

None

### .validate_outdoor_growing_production
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/extract_results.py/#L543)
```python
.validate_outdoor_growing_production()
```

---
Validates the outdoor growing production by checking if the difference between the outdoor crops to humans and
the
sum of immediate outdoor crops and new stored outdoor crops is equal to zero.

**Args**

* **self** (Extractor) : An instance of the Extractor class.


**Returns**

None

### .extract_meat_milk_results
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/extract_results.py/#L562)
```python
.extract_meat_milk_results(
   meat_eaten, milk_kcals, milk_fat, milk_protein
)
```

---
Extracts the results of meat and milk production from various sources and calculates the amount of food
produced in billions of people fed each month.


**Args**

* **meat_eaten** (list) : List of the amount of culled meat eaten in kg per year
* **milk_kcals** (list) : List of the amount of grazing milk produced in kcal per year
* **milk_fat** (list) : List of the amount of grazing milk produced in fat per year
* **milk_protein** (list) : List of the amount of grazing milk produced in protein per year


**Returns**

None


**Example**


```python

>>> extractor = Extractor()
>>> extractor.extract_meat_milk_results(
>>>     meat_eaten=[1000, 2000, 3000],
>>>     milk_kcals=[1000, 2000, 3000],
>>>     milk_fat=[100, 200, 300],
>>>     milk_protein=[50, 100, 150],
>>> )
```

### .extract_to_humans_feed_and_biofuel
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/extract_results.py/#L644)
```python
.extract_to_humans_feed_and_biofuel(
   to_humans, feed, biofuel, kcals_ratio, fat_ratio, protein_ratio, constants
)
```


### .get_objective_optimization_results
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/extract_results.py/#L690)
```python
.get_objective_optimization_results(
   model
)
```

---
This function extracts the optimization results for the objective function of the model.

**Args**

* **self**  : instance of the Extractor class
* **model**  : the optimization model to extract results from


**Returns**

* **tuple**  : a tuple containing the optimization results for consumed_kcals, consumed_fat, and consumed_protein

