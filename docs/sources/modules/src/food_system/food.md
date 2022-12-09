#


## Food
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L23)
```python 
Food(
   kcals = 0, fat = 0, protein = 0, kcals_units = 'billionkcals',
   fat_units = 'thousandtons', protein_units = 'thousandtons'
)
```


---
A food always has calories, fat, and protein.
Food applies to biofuels and feed properties as well.

A food always has units for each nutrient and these need to match when combining
foods in some way, such as adding up, multiplying, or dividing their nutrients

Best practice is to alter the food's units to be as specific as possible to prevent
errors in the calculation.

Here are some examples of using the food class:

CONVENTIONS:
A nutrient with a list of the value for each month, will need to
have " each month" at the end of the units.
A nutrient that represents the value for every month must have
a " per month" at the end of the units.
A nutrient with a single value all summed up over all time periods must not
contain any " each month" or " per month" in the units.



---
>>> example_food=Food(10,3,1)

(defaults to billion kcals, thousand tons monthly fat, thousand tons monthly
protein)

>>> print(example_food):
    protein: 1  thousand tons


```python

>>>     kcals_units = 'ratio minimum global needs per year',
>>>     fat_units = 'ratio minimum global needs per year',
>>>     protein_units = 'ratio minimum global needs per year',
>>> )
>>> print(example_food):
    protein: 1  ratio minimum global needs per year

```
(in order to get a min nutrient, you need to make sure the units are all the same)
(in reality, you would want to divide the values by the actual global needs above)

>>> print(example_food.get_min_nutrient())
    ('protein', 1)


```python

>>> example_food_monthly.set_units(
>>>     kcals_units = 'ratio minimum global needs per month',
>>>     fat_units = 'ratio minimum global needs per month',
>>>     protein_units = 'ratio minimum global needs per month',
>>> )

```
>>> print(example_food_monthly)
    protein: 0.08333333333333333  ratio minimum global needs per month


```python

>>> example_food_all_months = Food(
>>>     [example_food_monthly.kcals] * NMONTHS,
>>>     [example_food_monthly.fat] * NMONTHS,
>>>     [example_food_monthly.protein] * NMONTHS,
>>> )
>>> example_food_all_months.set_units(
>>>     kcals_units = 'ratio minimum global needs each month',
>>>     fat_units = 'ratio minimum global needs each month',
>>>     protein_units = 'ratio minimum global needs each month',
>>> )
>>> print(example_food_all_months)
    ratio minimum global needs each month
```


**Methods:**


### .get_Food_class
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L108)
```python
.get_Food_class(
   cls
)
```

---
get this class

### .get_conversions
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L115)
```python
.get_conversions(
   cls
)
```

---
return the class conversions object
this is only used by the parent UnitConversions class

### .get_nutrient_names
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L129)
```python
.get_nutrient_names(
   cls
)
```


**Returns**

the macronutrients of the food.

### .ratio_one
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L138)
```python
.ratio_one(
   cls
)
```


**Returns**

a ratio of one.

### .ratio_zero
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L155)
```python
.ratio_zero(
   cls
)
```


**Returns**

a ratio of zero.

### .validate_if_list
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L214)
```python
.validate_if_list()
```

---
Runs all the checks to make sure the list is properly set up

### .make_sure_not_a_list
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L241)
```python
.make_sure_not_a_list()
```

---
throw an error if any of the food nutrients are a list

### .make_sure_is_a_list
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L249)
```python
.make_sure_is_a_list()
```

---
throw an error if any of the food nutrients is not a list, then validate
list properties

### .ensure_other_list_zero_if_this_is_zero
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L258)
```python
.ensure_other_list_zero_if_this_is_zero(
   other_list
)
```

---
Get the value of the elements where the passed in list is zero, otherwise
returned elements are zero.

### .make_sure_fat_protein_zero_if_kcals_is_zero
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L322)
```python
.make_sure_fat_protein_zero_if_kcals_is_zero()
```

---
Get the value of the elements where the passed in list is zero, otherwise
returned elements are zero.

### .make_sure_not_nan
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L357)
```python
.make_sure_not_nan()
```

---
Make sure that the food is not a nan number, or fail the assertion

### .plot
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L713)
```python
.plot(
   title = 'genericfoodobjectovertime'
)
```

---
Use the plotter to plot this food's properties.

### .is_list_monthly
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L765)
```python
.is_list_monthly()
```

---
return whether this is a list

### .is_never_negative
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L771)
```python
.is_never_negative()
```

---
Checks wether the food's macronutrients are never negative.

### .all_greater_than
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L793)
```python
.all_greater_than(
   other
)
```


**Returns**

True if the food's macronutrients are greater than the other food's.

### .all_less_than
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L822)
```python
.all_less_than(
   other
)
```


**Returns**

True if the food's macronutrients are greater than the other food's.

### .any_greater_than
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L852)
```python
.any_greater_than(
   other
)
```


**Returns**

True if the food's macronutrients are greater than the other food's.

### .any_less_than
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L888)
```python
.any_less_than(
   other
)
```


**Returns**

True if the food's macronutrients are less than the other food's.

### .all_greater_than_or_equal_to
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L924)
```python
.all_greater_than_or_equal_to(
   other
)
```


**Returns**

True if the food's macronutrients are greater than or equal to
the other food's.

### .all_less_than_or_equal_to
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L954)
```python
.all_less_than_or_equal_to(
   other
)
```

---
Returns
:True if the food's macronutrients are less than or equal to
the other food's.

---
cases:
    this is food, other is food
    this is food, other is food list
    this is food list, other is food
    this is food list, other is food list

### .any_greater_than_or_equal_to
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L998)
```python
.any_greater_than_or_equal_to(
   other
)
```


**Returns**

True if the food's macronutrients are greater than or equal to
the other food's.

### .any_less_than_or_equal_to
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L1028)
```python
.any_less_than_or_equal_to(
   other
)
```


**Returns**

True if the food's macronutrients are less than or equal to
the other food's.

### .all_equals_zero
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L1069)
```python
.all_equals_zero()
```


**Returns**

True if the food's macronutrients are equal to zero.

### .any_equals_zero
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L1093)
```python
.any_equals_zero()
```


**Returns**

True if the food's macronutrients are equal to zero.

### .all_greater_than_zero
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L1126)
```python
.all_greater_than_zero()
```


**Returns**

True if the food's macronutrients are greater than zero.

### .any_greater_than_zero
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L1147)
```python
.any_greater_than_zero()
```

---
Returns True if any of the food's macronutrients are greater than zero.

### .all_greater_than_or_equal_to_zero
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L1179)
```python
.all_greater_than_or_equal_to_zero()
```


**Returns**

True if the food's macronutrients are greater than or equal to zero.

### .as_numpy_array
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L1205)
```python
.as_numpy_array()
```


**Returns**

the nutrients as an ordered numpy_array.

### .get_min_nutrient
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L1212)
```python
.get_min_nutrient()
```

---
Returns the minimum nutrient of the food.

Can return the minimum of any month of any nutrient if a food list, or just
`the minimum of any nutrient if a food

Only works when the units is identical for the different nutrients


**Returns**

(minimum nutrient name, minimum nutrient value)

### .get_max_nutrient
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L1259)
```python
.get_max_nutrient()
```

---
Returns the maximum nutrient of the food.

NOTE:
only works on single valued instances of nutrients, not arrays.


**Returns**

(maximum nutrient name, maximum nutrient value)

### .get_nutrients_sum
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L1296)
```python
.get_nutrients_sum()
```

---
Sum up the nutrients in all the months, then alter the units to remove
 "each month"

### .get_running_total_nutrients_sum
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L1318)
```python
.get_running_total_nutrients_sum()
```

---
Running sum of the nutrients in all the months, don't alter units

### .get_amount_used_other_food
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L1355)
```python
.get_amount_used_other_food(
   other_fat_ratio, other_protein_ratio
)
```

---
Running sum of the amount used of the other food each month.

Function used to determine the amount of stored food or outdoor growing that is
used by biofuels and feed

this is determined by taking the max amount used of the three nutrients,
which is satisfied by a certain number of units of the other food. Surplus
of the nutrients used is not used at all in the calculation.

### .get_consumed_amount
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L1400)
```python
.get_consumed_amount(
   demand_to_be_met, used_nutrient_ratio
)
```

---
returns the amount used of the demand_to_be_met a food with a given used_nutrient_ratio.
The maximum nutrient used is used to determine the amount of the consumed
food will be used.

### .get_first_month
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L1426)
```python
.get_first_month()
```

---
Just get the first month's nutrient values and convert the units from "each" to
"per"

### .get_month
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L1434)
```python
.get_month(
   index
)
```

---
Get the i month's nutrient values, and convert the units from "each" to
"per"

### .get_min_all_months
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L1455)
```python
.get_min_all_months()
```

---
create a food with the minimum of every month as a total nutrient

### .get_max_all_months
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L1473)
```python
.get_max_all_months()
```

---
create a food with the maximum of every month as a total nutrient

### .negative_values_to_zero
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L1491)
```python
.negative_values_to_zero()
```

---
Replace negative values with zero for each month for all nutrients.
Also tests that the function worked.


**Returns**

the relevant food object with negative values replaced

### .get_rounded_to_decimal
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L1524)
```python
.get_rounded_to_decimal(
   decimals
)
```

---
Round to the nearest decimal place

to give you an idea how this works:
>>> np.round([1,-1,.1,-.1,0.01,-0.01],decimals=1)
array([ 1. , -1. ,  0.1, -0.1,  0. , -0. ])

---
NOTE: only implemented for lists at the moment

### .replace_if_list_with_zeros_is_zero
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L1548)
```python
.replace_if_list_with_zeros_is_zero(
   list_with_zeros, replacement
)
```

---
replace with the replacement if list_with_zeros is zero


arguments: list with zeros ( food list ): a list that has zeros in it
                                            the elements

---
returns:
    itself, but with places list_with_zeros zero replaced with replacement

### .set_to_zero_after_month
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L1645)
```python
.set_to_zero_after_month(
   month
)
```

---
set all values after the month to zero
