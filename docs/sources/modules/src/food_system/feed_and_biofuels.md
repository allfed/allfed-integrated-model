#


## FeedAndBiofuels
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/feed_and_biofuels.py/#L19)
```python 
FeedAndBiofuels(
   constants_for_params
)
```




**Methods:**


### .set_feed_and_biofuels
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/feed_and_biofuels.py/#L35)
```python
.set_feed_and_biofuels(
   outdoor_crops_used_for_biofuel, methane_scp_used_for_biofuel,
   cellulosic_sugar_used_for_biofuel, remaining_biofuel_needed_from_stored_food,
   outdoor_crops_used_for_feed, methane_scp_used_for_feed,
   cellulosic_sugar_used_for_feed, remaining_feed_needed_from_stored_food
)
```

---
This function sets the feed and biofuel usage for each month. It takes the
outdoor crops, methane, and cellulosic sugar that are used for feed and
biofuels, and the remaining feed and biofuel needed from stored food.

### .get_biofuels_and_feed_before_waste_from_animal_pops
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/feed_and_biofuels.py/#L112)
```python
.get_biofuels_and_feed_before_waste_from_animal_pops(
   constants_for_params, feed_over_time
)
```

---
Mostly, this function converts from feed_over_time in dry caloric tons to
the appropriate fat and protein values, as well as getting biofules from the
expected shutoff duration, then creates a Food object for the feed usage.
This function has "animal pops" in there because it's used only in the case that
feed is calculated in the context of breeding.

### .get_biofuel_usage_prewaste
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/feed_and_biofuels.py/#L139)
```python
.get_biofuel_usage_prewaste(
   biofuel_duration
)
```

---
This function is used to get the biofuel usage before the cap is applied.
The total number of months before shutoff is the duration, representing the
number of nonzero biofuel months for biofuels to be used.

pre waste: this is the actual amount used of stored food and crops before waste
is applied to crops and stored food

### .get_excess_food_usage_from_percents
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/feed_and_biofuels.py/#L193)
```python
.get_excess_food_usage_from_percents(
   excess_feed_percent
)
```


### .convert_kcal_to_tons
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/feed_and_biofuels.py/#L210)
```python
.convert_kcal_to_tons(
   kcals
)
```

