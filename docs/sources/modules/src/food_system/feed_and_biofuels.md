#


## FeedAndBiofuels
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/feed_and_biofuels.py/#L16)
```python 
FeedAndBiofuels(
   constants_for_params
)
```




**Methods:**


### .create_feed_food_from_kcals
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/feed_and_biofuels.py/#L61)
```python
.create_feed_food_from_kcals(
   food_kcals
)
```


### .set_feed_and_biofuels
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/feed_and_biofuels.py/#L76)
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

### .get_biofuels_and_feed_from_delayed_shutoff
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/feed_and_biofuels.py/#L182)
```python
.get_biofuels_and_feed_from_delayed_shutoff(
   constants_for_params
)
```


### .get_feed_usage
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/feed_and_biofuels.py/#L194)
```python
.get_feed_usage(
   feed_duration
)
```

---
This function is used to get the feed usage before the cap is applied.
The total number of months before shutoff is the duration, representing the
number of nonzero feed months for feeds to be used.

### .get_biofuel_usage
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/feed_and_biofuels.py/#L254)
```python
.get_biofuel_usage(
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

* **Food**  : A Food object representing the biofuel usage per month.

