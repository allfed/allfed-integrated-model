#


## FeedAndBiofuels
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/feed_and_biofuels.py/#L19)
```python 
FeedAndBiofuels(
   constants_for_params
)
```




**Methods:**


### .set_nonhuman_consumption_with_cap
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/feed_and_biofuels.py/#L45)
```python
.set_nonhuman_consumption_with_cap(
   constants_for_params, outdoor_crops, stored_food,
   biofuels_before_cap_prewaste, feed_before_cap_prewaste, excess_feed_prewaste
)
```

---
#NOTE: This function depends on get_excess being run first!

Cap biofuel usage to the amount of food available (stored food
plus outdoor crops)

This takes all the outdoor growing in each month in which feed and biofuel would
be used. First, the amount of food from the outdoor crops is subtracted from the
net feed plus biofuel previously assigned to be used.

If kcals, fat, and
protein used by biofuels plus feed is always less than outdoor growing, then
nothing is changed and the program returns.

If kcals, fat, and
protein used by biofuels plus feed is greater in any of the months than outdoor
growing, then the sum of all of these exceedances from what is grown is summed.
If the sum of exceedances is greater than any of the macronutrients summed from
stored food, then the amount of biofuels is reduced such that the sum of
exceedances uses exactly as much stored food is available.

However, if there was an excess feed assigned in the EXCESS_FEED variable,
then this implies that a diet calculation is being run, in order to reduce the
calories per person per day to 2100. This should NEVER be run in the context of
feed and biofuels exceeding available outdoor growing and stored food, because
in that case there would not be nearly enough calories to go around. Therefore,
the program will raise an error if this occurs.

If the biofuels are reduced to zero, then the remaining exceedance is subtracted
from the feed usage until exceedances use exactly as much stored food is
available.

In the case that the stored food is zero, this means that biofuels plus feed
will be capped to the outdoor production of any macronutrient in any month.

### .get_biofuels_and_feed_before_waste_from_delayed_shutoff
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/feed_and_biofuels.py/#L115)
```python
.get_biofuels_and_feed_before_waste_from_delayed_shutoff(
   constants_for_params
)
```


### .get_biofuels_and_feed_before_waste_from_animal_pops
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/feed_and_biofuels.py/#L141)
```python
.get_biofuels_and_feed_before_waste_from_animal_pops(
   constants_for_params, feed_over_time
)
```


### .set_biofuels_and_feed_usage_postwaste
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/feed_and_biofuels.py/#L186)
```python
.set_biofuels_and_feed_usage_postwaste(
   max_net_demand, stored_food, outdoor_crops, biofuels_before_cap,
   feed_before_cap, excess_feed_prewaste
)
```


### .iteratively_determine_reduction_in_nonhuman_consumption_postwaste
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/feed_and_biofuels.py/#L249)
```python
.iteratively_determine_reduction_in_nonhuman_consumption_postwaste(
   stored_food, outdoor_crops, biofuels_before_cap, feed_before_cap
)
```

---
This function iteratively determines the amount of nonhuman consumption by
reducing the amount of biofuels and feed used.

### .get_biofuel_usage_before_cap_prewaste
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/feed_and_biofuels.py/#L299)
```python
.get_biofuel_usage_before_cap_prewaste(
   biofuel_duration
)
```

---
This function is used to get the biofuel usage before the cap is applied.
The total number of months before shutoff is the duration, representing the
number of nonzero biofuel months for biofuels to be used.

pre waste: this is the actual amount used of stored food and crops before waste
is applied to crops and stored food

### .get_feed_usage_before_cap_prewaste
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/feed_and_biofuels.py/#L353)
```python
.get_feed_usage_before_cap_prewaste(
   feed_duration, excess_feed_prewaste
)
```

---
This function is used to get the feed usage before the cap is applied.
The total number of months before shutoff is the duration, representing the
number of nonzero feed months for feeds to be used.

### .get_nonhuman_consumption_before_cap_prewaste
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/feed_and_biofuels.py/#L401)
```python
.get_nonhuman_consumption_before_cap_prewaste(
   biofuels_before_cap_prewaste, feed_before_cap_prewaste
)
```

---
Calculate and set the total usage for consumption of biofuels and feed

### .get_nonhuman_consumption_with_cap_postwaste
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/feed_and_biofuels.py/#L419)
```python
.get_nonhuman_consumption_with_cap_postwaste(
   constants_for_params, biofuels, feed
)
```

---
Calculate and set the total usage for consumption of biofuels and feed

assume animals need and use human levels of fat and protein per kcal

### .calculate_max_running_net_demand_postwaste
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/feed_and_biofuels.py/#L431)
```python
.calculate_max_running_net_demand_postwaste(
   outdoor_crops, biofuels_before_cap, feed_before_cap
)
```

---
Calculate the exceedance of the biofuel and feed usage past the outdoor
outdoor_crops
production on a monthly basis for each nutrient.

NOTE:
UPDATE
I realized that the max amount of stored food or OG used each month by
kcals, fat or protein needs to be summed, rather than the max of each
individual nutrient


**Example**

* **kcals**  :   10, 20, 10, 10
    fat:     10, 30, 20, 20
    protein: 10, 30, 20, 20
    month:    1   2   3   4
* **kcals**  :    5, 20, 10, 15
    fat:      5, 15, 25, 20
    protein: 25, 15, 20, 20
    month:    1   2   3   4
* **kcals**  :    5,  0,  0, -5
    fat:      5, 15, -5,  0
    protein:-15, 15,  0,  0
    month:    1   2   3   4
* **kcals**  :    5,  5,  5,  0
    fat:      5, 20, 15, 15
    protein:-15,  0,  0,  0
    month:    1   2   3   4
* **kcals**  :    0
    fat:      5
    protein:-15
    month: allmonths
* **kcals**  :    0
    fat:      -5
    protein: 15
    month: allmonths
outdoor crops:

nonhuman_consumption:

supply_minus_demand:

running_net_supply:

min_running_net_supply:

max_running_net_demand:


For all month combined, how much original stored food is needed to make up
for each macronutrient?

---
Answer:
    We sum up all the discrepancies between supply and demand.
    The stored food will need to make up for the minimum total shortage added
    up.

### .get_excess_food_usage_from_percents
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/feed_and_biofuels.py/#L535)
```python
.get_excess_food_usage_from_percents(
   excess_feed_percent
)
```

