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
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/extract_results.py/#L16)
```python
.extract_results(
   model, variables, time_consts
)
```


### .to_monthly_list
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/extract_results.py/#L128)
```python
.to_monthly_list(
   variables, conversion
)
```


### .to_monthly_list_outdoor_crops_kcals
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/extract_results.py/#L153)
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
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/extract_results.py/#L197)
```python
.get_greenhouse_results(
   greenhouse_kcals_per_ha, greenhouse_fat_per_ha, greenhouse_protein_per_ha,
   greenhouse_area
)
```


### .create_food_object_from_fat_protein_variables
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/extract_results.py/#L219)
```python
.create_food_object_from_fat_protein_variables(
   production_kcals, production_fat, production_protein
)
```


### .extract_generic_results
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/extract_results.py/#L248)
```python
.extract_generic_results(
   production_kcals, ratio_kcals, ratio_fat, ratio_protein, constants
)
```


### .extract_outdoor_crops_results
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/extract_results.py/#L278)
```python
.extract_outdoor_crops_results(
   crops_food_to_humans, crops_food_to_humans_fat, crops_food_to_humans_protein,
   crops_food_biofuel, crops_food_biofuel_fat, crops_food_biofuel_protein,
   crops_food_feed, crops_food_feed_fat, crops_food_feed_protein,
   outdoor_crops_production
)
```


### .calculate_outdoor_crops_kcals
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/extract_results.py/#L352)
```python
.calculate_outdoor_crops_kcals(
   crops_food_to_humans, to_humans_outdoor_crop_production
)
```


### .validate_sources_add_up
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/extract_results.py/#L361)
```python
.validate_sources_add_up(
   billions_fed_immediate_outdoor_crops_kcals,
   billions_fed_new_stored_outdoor_crops_kcals
)
```


### .set_new_stored_outdoor_crops_values
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/extract_results.py/#L376)
```python
.set_new_stored_outdoor_crops_values(
   billions_fed_new_stored_outdoor_crops_kcals
)
```


### .set_immediate_outdoor_crops_values
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/extract_results.py/#L388)
```python
.set_immediate_outdoor_crops_values(
   billions_fed_immediate_outdoor_crops_kcals
)
```


### .validate_outdoor_growing_production
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/extract_results.py/#L400)
```python
.validate_outdoor_growing_production()
```


### .extract_meat_milk_results
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/extract_results.py/#L407)
```python
.extract_meat_milk_results(
   culled_meat_eaten, grazing_milk_kcals, grazing_milk_fat,
   grazing_milk_protein, cattle_grazing_maintained_kcals,
   cattle_grazing_maintained_fat, cattle_grazing_maintained_protein,
   grain_fed_meat_kcals, grain_fed_meat_fat, grain_fed_meat_protein,
   grain_fed_milk_kcals, grain_fed_milk_fat, grain_fed_milk_protein
)
```


### .extract_to_humans_feed_and_biofuel
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/extract_results.py/#L535)
```python
.extract_to_humans_feed_and_biofuel(
   to_humans, feed, biofuel, kcals_ratio, fat_ratio, protein_ratio, constants
)
```


### .get_objective_optimization_results
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/extract_results.py/#L581)
```python
.get_objective_optimization_results(
   model
)
```

