#


## Interpreter
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/interpret_results.py/#L18)
```python 

```


---
This class is used to convert between optimization results data and other useful
ways of interpreting the results, as a diet, or as a total food supply.


**Methods:**


### .interpret_results
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/interpret_results.py/#L27)
```python
.interpret_results(
   extracted_results, time_consts
)
```

---
This function takes the raw output of the optimizer food categories and total
people fed in list form, and converts the naive people fed which includes
negative feed, into a purely list of values, where the negative feed has been
subtracted from the sum of outdoor growing and stored food.

ANYTHING assigned to "self" here is part of a useful result that will either
be printed or plotted as a result

### .assign_percent_fed_from_extractor
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/interpret_results.py/#L96)
```python
.assign_percent_fed_from_extractor(
   extracted_results
)
```


### .assign_kcals_equivalent_from_extractor
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/interpret_results.py/#L130)
```python
.assign_kcals_equivalent_from_extractor(
   extracted_results
)
```


### .set_to_humans_properties_kcals_equivalent
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/interpret_results.py/#L180)
```python
.set_to_humans_properties_kcals_equivalent(
   extracted_results
)
```


### .assign_time_months_middle
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/interpret_results.py/#L198)
```python
.assign_time_months_middle(
   NMONTHS
)
```


### .assign_interpreted_properties
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/interpret_results.py/#L203)
```python
.assign_interpreted_properties(
   extracted_results
)
```


### .get_mean_min_nutrient
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/interpret_results.py/#L259)
```python
.get_mean_min_nutrient()
```

---
for finding the minimum of any nutrient in any month
and then getting the mean people fed in all the months
This is useful for assessing what would have happened if stored food were not
a constraint on number of people fed

returns: the mean people fed in all months

### .get_amount_fed_to_humans
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/interpret_results.py/#L279)
```python
.get_amount_fed_to_humans(
   stored_food, outdoor_crops, immediate_outdoor_crops,
   new_stored_outdoor_crops, to_humans_ratio
)
```


### .get_sum_by_adding_to_humans
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/interpret_results.py/#L307)
```python
.get_sum_by_adding_to_humans()
```

---
sum the resulting nutrients from the extracted_results, but subtract nonhuman
to get the ratio

also rounds result to 1 decimal place in terms of percent fed (within 0.1% of
it's value)

### .get_sum_by_subtracting_nonhuman
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/interpret_results.py/#L332)
```python
.get_sum_by_subtracting_nonhuman(
   nonhuman_consumption
)
```

---
sum the resulting nutrients from the extracted_results, but do this by adding
all the amounts determined to go to humans

### .print_kcals_per_capita_per_day
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/interpret_results.py/#L356)
```python
.print_kcals_per_capita_per_day(
   interpreted_results
)
```

---
This function prints the ratio of needs to actual needs for a given scenario
result.

### .get_ratio_for_stored_food_and_outdoor_crops
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/interpret_results.py/#L368)
```python
.get_ratio_for_stored_food_and_outdoor_crops(
   outdoor_crops_plus_stored_food_rounded, nonhuman_consumption
)
```

---
This function returns the ratio of stored food and outdoor crops that would
be fed to humans, assuming that the rest goes to nonhuman consumption.

It doesn't put any limit on the calories eaten by humans, technically the model
just keeps metabolic waste at a similiar rate of waste based on the food price
assigned, and then just continues feeding humans at their minimum macronutrient
as high as it can.

NOTE: outdoor_crops_plus_stored_food_rounded may not be exactly the same as
the sum of stored food and outdoor crops, because the sum has been set
equal to nonhuman consumption if there were rounding errors making the two
slightly different.

### .get_percent_people_fed
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/interpret_results.py/#L435)
```python
.get_percent_people_fed(
   humans_fed_sum
)
```

---
get the minimum nutrients required to meet the needs of the population
 in any month, for kcals, fat, and protein

### .correct_and_validate_rounding_errors
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/interpret_results.py/#L454)
```python
.correct_and_validate_rounding_errors(
   nonhuman_consumption
)
```

---
any round error we might expect to be very small and easily fixable is corrected
here. "small" is with respect to percent people fed


**Note**

the optimizer!

### .get_increased_excess_to_feed
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/interpret_results.py/#L534)
```python
.get_increased_excess_to_feed(
   feed_delay, percent_fed
)
```

---
when calculating the excess calories, the amount of human edible feed
used can't be more than the excess calories. Because the baseline feed
usage is higher than in nuclear winter, we don't want to increase
feed usage before the shutoff.

this function adds an additional amount of excess at a consistent percentage
in the months of interest (months to calculate diet)

### .sum_many_results_together
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/interpret_results.py/#L598)
```python
.sum_many_results_together(
   many_results, cap_at_100_percent
)
```

---
sum together the results from many different runs of the model
create a new object summing the results

returns: the interpreter object with the summed results divided by the
population in question
