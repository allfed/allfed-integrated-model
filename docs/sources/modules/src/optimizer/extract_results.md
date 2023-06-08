#


## Extractor
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/extract_results.py/#L12)
```python 
Extractor(
   constants
)
```




**Methods:**


### .extract_results
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/extract_results.py/#L24)
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
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/extract_results.py/#L151)
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
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/extract_results.py/#L186)
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
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/extract_results.py/#L230)
```python
.get_greenhouse_results(
   greenhouse_kcals_per_ha, greenhouse_fat_per_ha, greenhouse_protein_per_ha,
   greenhouse_area
)
```


### .create_food_object_from_fat_protein_variables
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/extract_results.py/#L252)
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
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/extract_results.py/#L290)
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
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/extract_results.py/#L331)
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


**Args**

* **crops_food_to_humans** (float) : amount of outdoor crops produced for human consumption
* **crops_food_to_humans_fat** (float) : amount of fat in outdoor crops produced for human consumption
* **crops_food_to_humans_protein** (float) : amount of protein in outdoor crops produced for human consumption
* **crops_food_biofuel** (float) : amount of outdoor crops produced for biofuel
* **crops_food_biofuel_fat** (float) : amount of fat in outdoor crops produced for biofuel
* **crops_food_biofuel_protein** (float) : amount of protein in outdoor crops produced for biofuel
* **crops_food_feed** (float) : amount of outdoor crops produced for animal feed
* **crops_food_feed_fat** (float) : amount of fat in outdoor crops produced for animal feed
* **crops_food_feed_protein** (float) : amount of protein in outdoor crops produced for animal feed
* **outdoor_crops_production** (Food) : food object representing the total outdoor crop production


**Returns**

None


**Example**


```python

>>> extractor.extract_outdoor_crops_results(
...     100, 10, 20, 50, 5, 10, 30, 30, 3, 6, Food(1000, 200, 100, 50)
... )
```

### .calculate_outdoor_crops_kcals
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/extract_results.py/#L432)
```python
.calculate_outdoor_crops_kcals(
   crops_food_to_humans, to_humans_outdoor_crop_production
)
```


### .validate_sources_add_up
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/extract_results.py/#L441)
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
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/extract_results.py/#L478)
```python
.set_new_stored_outdoor_crops_values(
   billions_fed_new_stored_outdoor_crops_kcals
)
```

---
Sets the values of new_stored_outdoor_crops attribute of the Extractor class with the given billions_fed_new_stored_outdoor_crops_kcals.

**Args**

* **self** (Extractor) : An instance of the Extractor class.
* **billions_fed_new_stored_outdoor_crops_kcals** (list) : A list of kcals in billions fed to new stored outdoor crops each month.


**Returns**

None

### .set_immediate_outdoor_crops_values
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/extract_results.py/#L498)
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
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/extract_results.py/#L519)
```python
.validate_outdoor_growing_production()
```

---
Validates the outdoor growing production by checking if the difference between the outdoor crops to humans and the
sum of immediate outdoor crops and new stored outdoor crops is equal to zero.

**Args**

* **self** (Extractor) : An instance of the Extractor class.


**Returns**

None

### .extract_meat_milk_results
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/extract_results.py/#L535)
```python
.extract_meat_milk_results(
   culled_meat_eaten, grazing_milk_kcals, grazing_milk_fat,
   grazing_milk_protein, cattle_grazing_maintained_kcals,
   cattle_grazing_maintained_fat, cattle_grazing_maintained_protein,
   grain_fed_meat_kcals, grain_fed_meat_fat, grain_fed_meat_protein,
   grain_fed_milk_kcals, grain_fed_milk_fat, grain_fed_milk_protein
)
```

---
Extracts the results of meat and milk production from various sources and calculates the amount of food
produced in billions of people fed each month.


**Args**

* **culled_meat_eaten** (list) : List of the amount of culled meat eaten in kg per year
* **grazing_milk_kcals** (list) : List of the amount of grazing milk produced in kcal per year
* **grazing_milk_fat** (list) : List of the amount of grazing milk produced in fat per year
* **grazing_milk_protein** (list) : List of the amount of grazing milk produced in protein per year
* **cattle_grazing_maintained_kcals** (list) : List of the amount of cattle grazing maintained in kcal per year
* **cattle_grazing_maintained_fat** (list) : List of the amount of cattle grazing maintained in fat per year
* **cattle_grazing_maintained_protein** (list) : List of the amount of cattle grazing maintained in protein per year
* **grain_fed_meat_kcals** (float) : Amount of grain-fed meat produced in kcal per year
* **grain_fed_meat_fat** (float) : Amount of grain-fed meat produced in fat per year
* **grain_fed_meat_protein** (float) : Amount of grain-fed meat produced in protein per year
* **grain_fed_milk_kcals** (float) : Amount of grain-fed milk produced in kcal per year
* **grain_fed_milk_fat** (float) : Amount of grain-fed milk produced in fat per year
* **grain_fed_milk_protein** (float) : Amount of grain-fed milk produced in protein per year


**Returns**

None


**Example**


```python

>>> extractor = Extractor()
>>> extractor.extract_meat_milk_results(
>>>     culled_meat_eaten=[1000, 2000, 3000],
>>>     grazing_milk_kcals=[1000, 2000, 3000],
>>>     grazing_milk_fat=[100, 200, 300],
>>>     grazing_milk_protein=[50, 100, 150],
>>>     cattle_grazing_maintained_kcals=[1000, 2000, 3000],
>>>     cattle_grazing_maintained_fat=[100, 200, 300],
>>>     cattle_grazing_maintained_protein=[50, 100, 150],
>>>     grain_fed_meat_kcals=1000,
>>>     grain_fed_meat_fat=100,
>>>     grain_fed_meat_protein=50,
>>>     grain_fed_milk_kcals=1000,
>>>     grain_fed_milk_fat=100,
>>>     grain_fed_milk_protein=50,
>>> )
```

### .extract_to_humans_feed_and_biofuel
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/extract_results.py/#L725)
```python
.extract_to_humans_feed_and_biofuel(
   to_humans, feed, biofuel, kcals_ratio, fat_ratio, protein_ratio, constants
)
```


### .get_objective_optimization_results
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/extract_results.py/#L771)
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

