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


**Args**

* **extracted_results** (object) : The raw output of the optimizer food categories and
* **time_consts** (dict) : A dictionary containing time constants
total people fed in list form


**Returns**

* **object**  : An instance of the Interpreter class

---
ANYTHING assigned to "self" here is part of a useful result that will either
be printed or plotted as a result

### .assign_percent_fed_from_extractor
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/interpret_results.py/#L145)
```python
.assign_percent_fed_from_extractor(
   extracted_results
)
```

---
Assigns the percentage of food fed to humans from each food source extracted from the results.

**Args**

* **extracted_results** (ExtractedResults) : An instance of the ExtractedResults class containing the results
of the extraction process.

**Returns**

None

### .assign_kcals_equivalent_from_extractor
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/interpret_results.py/#L203)
```python
.assign_kcals_equivalent_from_extractor(
   extracted_results
)
```

---
Assigns the kcals equivalent of various food sources to their respective attributes in the Interpreter object.

**Args**

* **extracted_results** (ExtractedResults) : An object containing the results of the extraction process.


**Returns**

None

### .set_to_humans_properties_kcals_equivalent
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/interpret_results.py/#L269)
```python
.set_to_humans_properties_kcals_equivalent(
   extracted_results
)
```

---
Converts the stored food and outdoor crops to humans properties to their equivalent in kcals.

**Args**

* **extracted_results** (dict) : A dictionary containing the extracted results from the simulation.


**Returns**

None

### .assign_time_months_middle
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/interpret_results.py/#L299)
```python
.assign_time_months_middle(
   NMONTHS
)
```

---
This function assigns the middle of each month to a list of time_months_middle.

**Args**

* **NMONTHS** (int) : The number of months to assign the middle of.


**Returns**

None


**Example**


```python

>>> interpreter.assign_time_months_middle(12)
>>> print(interpreter.time_months_middle)
[0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5, 11.5]
```

### .assign_interpreted_properties
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/interpret_results.py/#L321)
```python
.assign_interpreted_properties(
   extracted_results
)
```

---
Assigns interpreted properties to the Interpreter object based on the extracted results.

**Args**

* **extracted_results** (ExtractedResults) : The extracted results object to interpret.


**Returns**

None


**Example**


```python

>>> interpreter = Interpreter()
>>> interpreter.assign_interpreted_properties(extracted_results)
```

### .get_mean_min_nutrient
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/interpret_results.py/#L352)
```python
.get_mean_min_nutrient()
```

---
Calculates the mean number of people fed in all months by finding the minimum of any nutrient in any month.
This is useful for assessing what would have happened if stored food were not a constraint on the number of people fed.


**Args**

* **self** (Interpreter) : An instance of the Interpreter class.


**Returns**

* **float**  : The mean number of people fed in all months.


**Example**


```python

>>> interpreter.get_mean_min_nutrient()
2.0
```

### .get_sum_by_adding_to_humans
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/interpret_results.py/#L378)
```python
.get_sum_by_adding_to_humans()
```

---
Sums the resulting nutrients from the extracted_results and returns the total.


**Args**

* **self**  : instance of the Interpreter class


**Returns**

* **float**  : the total amount of nutrients that can be fed to humans


**Example**


```python

>>> interpreter.stored_food = 100
>>> interpreter.outdoor_crops = 200
>>> interpreter.seaweed = 50
>>> interpreter.cell_sugar = 75
>>> interpreter.scp = 150
>>> interpreter.greenhouse = 300
>>> interpreter.fish = 100
>>> interpreter.culled_meat_plus_grazing_cattle_maintained = 50
>>> interpreter.grazing_milk = 25
>>> interpreter.grain_fed_meat = 75
>>> interpreter.grain_fed_milk = 50
>>> interpreter.get_sum_by_adding_to_humans()
1025.0
```

### .print_kcals_per_capita_per_day
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/interpret_results.py/#L423)
```python
.print_kcals_per_capita_per_day(
   interpreted_results
)
```

---
This function calculates and prints the expected kcals/capita/day for a given scenario result.

**Args**

* **interpreted_results** (InterpretedResults) : An instance of the InterpretedResults class containing
the interpreted results of a scenario.


**Returns**

None


**Example**


```python

>>> Interpreter.print_kcals_per_capita_per_day(interpreted_results)
```

### .get_percent_people_fed
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/interpret_results.py/#L446)
```python
.get_percent_people_fed(
   humans_fed_sum
)
```

---
Calculates the estimated percentage of people fed based on the minimum nutrients required to meet the needs of the population in any month, for kcals, fat, and protein.


**Args**

* **humans_fed_sum** (HumanFedSum) : An instance of the HumanFedSum class representing the total amount of nutrients available for the population.


**Returns**

* **list**  : A list containing the estimated percentage of people fed and the minimum nutrients required to meet their needs.


**Example**

* 1000, 'fat': 50, 'protein': 20}]

```python

>>> interpreter = Interpreter()
>>> interpreter.get_percent_people_fed(humans_fed_sum)
```

### .correct_and_validate_rounding_errors
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/interpret_results.py/#L480)
```python
.correct_and_validate_rounding_errors()
```

---
This function corrects any rounding errors that might have occurred during the optimization process.
It ensures that the values are rounded to the nearest 3 decimal places and that they are greater than or equal to zero.
The function returns the corrected values for stored_food, outdoor_crops, immediate_outdoor_crops, new_stored_outdoor_crops, and seaweed.


**Args**

None


**Returns**

* **tuple**  : A tuple containing the corrected values for stored_food, outdoor_crops, immediate_outdoor_crops, new_stored_outdoor_crops, and seaweed.


**Example**


```python

>>> stored_food, outdoor_crops, immediate_outdoor_crops, new_stored_outdoor_crops, seaweed = interpreter.correct_and_validate_rounding_errors()
```

### .get_increased_excess_to_feed
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/interpret_results.py/#L539)
```python
.get_increased_excess_to_feed(
   feed_delay, percent_fed
)
```

---
Calculates the excess feed to be added to the diet at a consistent percentage
in the months of interest (months to calculate diet).


**Args**

* **feed_delay** (int) : the number of months before the shutoff
* **percent_fed** (float) : the percentage of the baseline feed to be fed to the population


**Returns**

* **excess_per_month** (numpy.ndarray) : kcals per month, units percent


**Raises**

* **AssertionError**  : if the length of additional_excess_to_add_percent is not equal to after_shutoff_feed


### .correct_and_validate_rounding_errors
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/interpret_results.py/#L480)
```python
.correct_and_validate_rounding_errors()
```

---
This function corrects any rounding errors that might have occurred during the optimization process.
It ensures that the values are rounded to the nearest 3 decimal places and that they are greater than or equal to zero.
The function returns the corrected values for stored_food, outdoor_crops, immediate_outdoor_crops, new_stored_outdoor_crops, and seaweed.


**Args**

None


**Returns**

* **tuple**  : A tuple containing the corrected values for stored_food, outdoor_crops, immediate_outdoor_crops, new_stored_outdoor_crops, and seaweed.


**Example**


```python

>>> stored_food, outdoor_crops, immediate_outdoor_crops, new_stored_outdoor_crops, seaweed = interpreter.correct_and_validate_rounding_errors()
```

### .set_feed_and_biofuels
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/interpret_results.py/#L662)
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
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/interpret_results.py/#L727)
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
