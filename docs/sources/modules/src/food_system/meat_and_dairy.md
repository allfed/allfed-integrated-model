#


## MeatAndDairy
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/meat_and_dairy.py/#L12)
```python 
MeatAndDairy(
   constants_for_params
)
```




**Methods:**


### .calculate_meat_nutrition
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/meat_and_dairy.py/#L113)
```python
.calculate_meat_nutrition()
```


### .calculate_meat_limits
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/meat_and_dairy.py/#L158)
```python
.calculate_meat_limits(
   MAX_RATIO_CULLED_SLAUGHTER_TO_BASELINE, culled_meat_initial
)
```

---
calculate the baseline levels of meat production, indicating slaughter capacity

There's no limit on the actual amount eaten, but the amount produced and
then preserved after culling is assumed to be some multiple of current slaughter
capacity

This just means that the limit each month on the amount that could be eaten is
the sum of the max estimated slaughter capacity each month

### .calculate_continued_ratios_meat_dairy_grazing
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/meat_and_dairy.py/#L190)
```python
.calculate_continued_ratios_meat_dairy_grazing(
   constants_for_params
)
```


### .calculate_continued_ratios_meat_dairy_grain
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/meat_and_dairy.py/#L242)
```python
.calculate_continued_ratios_meat_dairy_grain(
   fed_to_animals_prewaste, outdoor_crops
)
```


### .calculate_meat_and_dairy_from_grain
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/meat_and_dairy.py/#L309)
```python
.calculate_meat_and_dairy_from_grain(
   fed_to_animals_prewaste
)
```


### .calculate_meat_milk_from_human_inedible_feed
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/meat_and_dairy.py/#L402)
```python
.calculate_meat_milk_from_human_inedible_feed(
   constants_for_params
)
```


### .get_milk_from_human_edible_feed
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/meat_and_dairy.py/#L434)
```python
.get_milk_from_human_edible_feed(
   constants_for_params
)
```


### .get_meat_from_human_edible_feed
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/meat_and_dairy.py/#L468)
```python
.get_meat_from_human_edible_feed()
```


### .get_grazing_milk_produced_postwaste
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/meat_and_dairy.py/#L634)
```python
.get_grazing_milk_produced_postwaste()
```


### .get_cattle_grazing_maintained
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/meat_and_dairy.py/#L662)
```python
.get_cattle_grazing_maintained()
```


### .calculated_culled_meat
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/meat_and_dairy.py/#L712)
```python
.calculated_culled_meat()
```


### .get_culled_meat_post_waste
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/meat_and_dairy.py/#L779)
```python
.get_culled_meat_post_waste(
   constants_for_params
)
```


### .calculate_animals_culled
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/meat_and_dairy.py/#L788)
```python
.calculate_animals_culled(
   constants_for_params
)
```

