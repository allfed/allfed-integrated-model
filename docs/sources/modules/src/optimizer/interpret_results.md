#


## Interpreter
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/interpret_results.py/#L26)
```python 

```


---
This class is used to convert between optimization results data and other useful
ways of interpreting the results, as a diet, or as a total food supply.


**Methods:**


### .interpret_results
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/interpret_results.py/#L35)
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
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/interpret_results.py/#L130)
```python
.assign_percent_fed_from_extractor(
   extracted_results
)
```


### .assign_kcals_equivalent_from_extractor
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/interpret_results.py/#L167)
```python
.assign_kcals_equivalent_from_extractor(
   extracted_results
)
```


### .set_to_humans_properties_kcals_equivalent
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/interpret_results.py/#L214)
```python
.set_to_humans_properties_kcals_equivalent(
   extracted_results
)
```


### .assign_time_months_middle
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/interpret_results.py/#L231)
```python
.assign_time_months_middle(
   NMONTHS
)
```


### .assign_interpreted_properties
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/interpret_results.py/#L236)
```python
.assign_interpreted_properties(
   extracted_results
)
```


### .get_mean_min_nutrient
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/interpret_results.py/#L254)
```python
.get_mean_min_nutrient()
```

---
for finding the minimum of any nutrient in any month
and then getting the mean people fed in all the months
This is useful for assessing what would have happened if stored food were not
a constraint on number of people fed

returns: the mean people fed in all months

### .get_sum_by_adding_to_humans
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/interpret_results.py/#L274)
```python
.get_sum_by_adding_to_humans()
```

---
sum the resulting nutrients from the extracted_results

### .print_kcals_per_capita_per_day
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/interpret_results.py/#L295)
```python
.print_kcals_per_capita_per_day(
   interpreted_results
)
```

---
This function prints the ratio of needs to actual needs for a given scenario
result.

### .get_percent_people_fed
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/interpret_results.py/#L307)
```python
.get_percent_people_fed(
   humans_fed_sum
)
```

---
get the minimum nutrients required to meet the needs of the population
 in any month, for kcals, fat, and protein

### .correct_and_validate_rounding_errors
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/interpret_results.py/#L325)
```python
.correct_and_validate_rounding_errors()
```

---
any round error we might expect to be very small and easily fixable is corrected
here. "small" is with respect to percent people fed


**Note**

the optimizer!

### .get_increased_excess_to_feed
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/interpret_results.py/#L375)
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

### .correct_and_validate_rounding_errors
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/interpret_results.py/#L325)
```python
.correct_and_validate_rounding_errors()
```

---
any round error we might expect to be very small and easily fixable is corrected
here. "small" is with respect to percent people fed


**Note**

the optimizer!

### .set_feed_and_biofuels
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/interpret_results.py/#L488)
```python
.set_feed_and_biofuels(
   seaweed_used_for_biofuel, methane_scp_used_for_biofuel,
   cellulosic_sugar_used_for_biofuel, stored_food_used_for_biofuel,
   outdoor_crops_used_for_biofuel, seaweed_used_for_feed,
   methane_scp_used_for_feed, cellulosic_sugar_used_for_feed,
   stored_food_used_for_feed, outdoor_crops_used_for_feed
)
```

---
This function sets the feed and biofuel usage for each month. It takes the
outdoor crops, methane, and cellulosic sugar that are used for feed and
biofuels, and the remaining feed and biofuel needed from stored food.

### .sum_many_results_together
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/interpret_results.py/#L553)
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
