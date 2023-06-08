#


## Seaweed
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/seaweed.py/#L13)
```python 
Seaweed(
   constants_for_params
)
```




**Methods:**


### .get_growth_rates
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/seaweed.py/#L136)
```python
.get_growth_rates(
   constants_for_params
)
```

---
Calculates the monthly growth rates of seaweed based on the daily growth percentages provided in the constants.


**Args**

* **constants_for_params** (dict) : A dictionary containing the constants for the seaweed growth model.


**Returns**

* **ndarray**  : An array of monthly growth rates for the seaweed.


### .get_built_area
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/seaweed.py/#L169)
```python
.get_built_area(
   constants_for_params
)
```

---
Calculates the built area of seaweed based on the provided constants.


**Args**

* **constants_for_params** (dict) : A dictionary containing the constants for the seaweed growth model.


**Returns**

* **ndarray**  : An array of the built area of seaweed over time.


### .estimate_seaweed_growth_for_estimating_feed_availability
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/seaweed.py/#L230)
```python
.estimate_seaweed_growth_for_estimating_feed_availability()
```

---
Estimates the growth of seaweed for the purpose of estimating feed availability.

We have to see whether predicted feed needs are more than available feed, in which case the feed needs to be reduced.
We have to do that before we run the optimization which more accurately determines seaweed growth.
So, this function makes the simplifying assumptions which no longer require linear optimization:
1. seaweed is not harvested until production would reach the human consumption percentage calories limit
2. once it reaches this limit, it stays at that rate of production for the rest of the simulation


**Returns**

None
