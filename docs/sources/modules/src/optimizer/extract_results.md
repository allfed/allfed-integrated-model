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
   model, variables, single_valued_constants, multi_valued_constants
)
```


### .to_monthly_list
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/extract_results.py/#L97)
```python
.to_monthly_list(
   variables, conversion
)
```


### .to_monthly_list_outdoor_crops_kcals
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/extract_results.py/#L119)
```python
.to_monthly_list_outdoor_crops_kcals(
   crops_food_eaten_no_relocation, crops_food_eaten_relocated,
   crops_kcals_produced, conversion
)
```

---
This function is actually guessing at the internal operations of the optimizer
when it creates an optimized plot.

It takes the total outdoor crop production and limits it by the actual amount
eaten by people reported by the optimizer.

If more is eaten than produced, this difference is attributed to the eating
of stored up crops.

We know it can't be stored food from before the simulation because the variable
only considers the outdoor_crops variable, not the stored_food variable

The amount of expected crops produced that month that were eaten is assigned to
the "immediate" list.
The amount eaten beyond the production that month is assigned to the
new stored list.

NOTE: the validator will check that the sum of immediate and new stored is the
same as the total amount eaten.

### .extract_greenhouse_results
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/extract_results.py/#L201)
```python
.extract_greenhouse_results(
   greenhouse_kcals_per_ha, greenhouse_fat_per_ha, greenhouse_protein_per_ha,
   greenhouse_area
)
```


### .extract_fish_results
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/extract_results.py/#L238)
```python
.extract_fish_results(
   production_kcals_fish_per_month, production_fat_fish_per_month,
   production_protein_fish_per_month
)
```


### .extract_outdoor_crops_results
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/extract_results.py/#L270)
```python
.extract_outdoor_crops_results(
   crops_food_eaten_no_relocation, crops_food_eaten_relocated, outdoor_crops
)
```


### .set_crop_produced_monthly
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/extract_results.py/#L462)
```python
.set_crop_produced_monthly(
   outdoor_crops
)
```

---
get the crop produced monthly, rather than the amount eaten
incorporates relocations

### .extract_cell_sugar_results
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/extract_results.py/#L545)
```python
.extract_cell_sugar_results(
   production_kcals_cell_sugar_per_month
)
```


### .extract_SCP_results
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/extract_results.py/#L566)
```python
.extract_SCP_results(
   production_kcals_scp_per_month, production_fat_scp_per_month,
   production_protein_scp_per_month
)
```


### .extract_meat_milk_results
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/extract_results.py/#L597)
```python
.extract_meat_milk_results(
   culled_meat_eaten, grazing_milk_kcals, grazing_milk_fat,
   grazing_milk_protein, cattle_grazing_maintained_kcals,
   cattle_grazing_maintained_fat, cattle_grazing_maintained_protein,
   grain_fed_meat_kcals, grain_fed_meat_fat, grain_fed_meat_protein,
   grain_fed_milk_kcals, grain_fed_milk_fat, grain_fed_milk_protein
)
```


### .extract_stored_food_results
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/extract_results.py/#L751)
```python
.extract_stored_food_results(
   stored_food_eaten
)
```

---
Extracts results from stored food eaten.

### .extract_seaweed_results
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/extract_results.py/#L782)
```python
.extract_seaweed_results(
   seaweed_wet_on_farm, used_area, built_area, seaweed_food_produced
)
```


### .get_objective_optimization_results
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/extract_results.py/#L831)
```python
.get_objective_optimization_results(
   model
)
```

