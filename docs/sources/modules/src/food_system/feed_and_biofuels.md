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
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/feed_and_biofuels.py/#L56)
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


**Args**

* **outdoor_crops_used_for_biofuel** (list) : A list of outdoor crops used for biofuel
* **methane_scp_used_for_biofuel** (list) : A list of methane SCP used for biofuel
* **cellulosic_sugar_used_for_biofuel** (list) : A list of cellulosic sugar used for biofuel
* **remaining_biofuel_needed_from_stored_food** (Food) : The remaining biofuel needed from stored food
* **outdoor_crops_used_for_feed** (list) : A list of outdoor crops used for feed
* **methane_scp_used_for_feed** (list) : A list of methane SCP used for feed
* **cellulosic_sugar_used_for_feed** (list) : A list of cellulosic sugar used for feed
* **remaining_feed_needed_from_stored_food** (Food) : The remaining feed needed from stored food


**Returns**

None


**Example**


```python

>>> feed_and_biofuels.set_feed_and_biofuels(
...     [10, 20, 30],
...     [40, 50, 60],
...     [70, 80, 90],
...     Food(100),
...     [10, 20, 30],
...     [40, 50, 60],
...     [70, 80, 90],
...     Food(100),
... )
```

### .get_biofuels_and_feed_before_waste_from_animal_pops
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/feed_and_biofuels.py/#L162)
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
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/feed_and_biofuels.py/#L189)
```python
.get_biofuel_usage_prewaste(
   biofuel_duration
)
```

---
This function calculates the biofuel usage before the cap is applied.
The total number of months before shutoff is the duration, representing the
number of nonzero biofuel months for biofuels to be used.


**Args**

* **biofuel_duration** (int) : The number of months before the biofuel shutoff.


**Returns**

* **Food**  : A Food object representing the biofuel usage before waste is applied.


**Example**


```python

>>> feed.get_biofuel_usage_prewaste(6)
Food(kcals=[1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 0, 0, 0, 0, 0, 0],
     fat=[0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0, 0, 0, 0, 0, 0],
     protein=[0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0, 0, 0, 0, 0, 0],
     kcals_units='billion kcals each month',
     fat_units='thousand tons each month',
     protein_units='thousand tons each month')
```

### .get_excess_food_usage_from_percents
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/feed_and_biofuels.py/#L261)
```python
.get_excess_food_usage_from_percents(
   excess_feed_percent
)
```

---
Calculates the excess food usage based on the percentage of excess feed.

**Args**

* **excess_feed_percent** (float) : The percentage of excess feed.


**Returns**

* **Food**  : A Food object representing the excess food usage.


### .convert_kcal_to_tons
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/feed_and_biofuels.py/#L286)
```python
.convert_kcal_to_tons(
   kcals
)
```

---
Converts a given number of kcals to tons of feed or biofuel.

**Args**

* **kcals** (float) : number of kcals to convert to tons


**Returns**

* **float**  : number of tons equivalent to the given number of kcals

