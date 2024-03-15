#


## Food
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L25)
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
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L110)
```python
.get_Food_class(
   cls
)
```

---
This function returns the class object of the current class.

**Args**

* **cls** (class) : The class object of the current class.


**Returns**

* **class**  : The class object of the current class.


### .get_conversions
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L121)
```python
.get_conversions(
   cls
)
```

---
Returns the class conversions object.
This method is only used by the parent UnitConversions class.


**Args**

* **cls** (class) : The class object.


**Returns**

* **conversions** (object) : The class conversions object.


**Raises**

* **AssertionError**  : If the conversions property has not been assigned before
attempting to convert between food units.

### .get_nutrient_names
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L147)
```python
.get_nutrient_names(
   cls
)
```

---
Returns a list of the macronutrients of the food.


**Args**

* **cls** (class) : The class object representing the Food class.


**Returns**

* **list**  : A list of strings representing the macronutrients of the food.


**Example**

>>> Food.get_nutrient_names()
['kcals', 'fat', 'protein']

### .ratio_one
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L165)
```python
.ratio_one(
   cls
)
```

---
Creates a Food object with kcals, fat, and protein all set to 1, and units set to "ratio".

**Returns**

* **Food**  : a Food object with kcals, fat, and protein all set to 1, and units set to "ratio".


### .ratio_zero
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L183)
```python
.ratio_zero(
   cls
)
```

---
Creates a Food object with all nutrient values set to 0 and units set to "ratio".

**Args**

* **cls**  : the class object


**Returns**

* **Food**  : a Food object with kcals, fat, and protein set to 0 and units set to "ratio".


### .reset_food
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L296)
```python
.reset_food(
   kcals = 0, fat = 0, protein = 0, kcals_units = 'billionkcals',
   fat_units = 'thousandtons', protein_units = 'thousandtons'
)
```

---
Initializes a new food object with the given macronutrients and sets the default units.


**Args**

* **kcals** (float) : The number of kilocalories in the food. Default is 0.
* **fat** (float) : The amount of fat in the food. Default is 0.
* **protein** (float) : The amount of protein in the food. Default is 0.
* **kcals_units** (str) : The units for the kilocalories. Default is "billion kcals".
* **fat_units** (str) : The units for the fat. Default is "thousand tons".
* **protein_units** (str) : The units for the protein. Default is "thousand tons".


**Returns**

None


**Example**


```python

>>> food.reset_food() # sets back to zero and resets units
```

### .total_energy_in_food
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L362)
```python
.total_energy_in_food()
```

---
Calculates the total energy in a given food in billion kcals by converting energy in protein and fat.
Only works if:
kcals_units="billion kcals",
fat_units="thousand tons",
protein_units="thousand tons",
As a thousand tonnes, and a billion kcals are the same (10^9), the maths for conversion is simple.


**Args**

* **self** (Food) : An instance of the Food class.


**Returns**

* **float**  : The total energy in billion kcals.


**Raises**

* **AssertionError**  : If kcals_units, fat_units, or protein_units are not set to the correct values.


**Example**


```python

>>> food.kcals_units = "billion kcals"
>>> food.fat_units = "thousand tons"
>>> food.protein_units = "thousand tons"
>>> food.protein = 1000
>>> food.fat = 2000
>>> food.kcals = 3000
>>> food.total_energy_in_food()
23000.0
```

### .validate_if_list
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L410)
```python
.validate_if_list()
```

---
Checks if the food object is a list type and runs all the necessary checks to ensure
that the list is properly set up.


**Args**

* **self** (Food) : The Food object to be validated.


**Returns**

None


**Example**


```python

>>> food.validate_if_list()
```

### .make_sure_not_a_list
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L454)
```python
.make_sure_not_a_list()
```

---
Check if any of the food nutrients are a list or numpy array and throw an error if so.

**Args**

* **self**  : instance of the Food class


**Returns**

None

### .make_sure_is_a_list
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L473)
```python
.make_sure_is_a_list()
```

---
This function checks if the food nutrients are in the form of a list and throws an error if not.
It then validates the list properties.

**Args**

* **self** (Food) : An instance of the Food class.


**Returns**

None

**Example**


```python

>>> food.make_sure_is_a_list()
```

### .make_sure_fat_protein_zero_if_kcals_is_zero
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L490)
```python
.make_sure_fat_protein_zero_if_kcals_is_zero()
```

---
This function ensures that the values of fat and protein are zero if kcals is zero.

**Args**

* **self** (Food) : an instance of the Food class


**Returns**

None

### .ensure_other_list_zero_if_this_is_zero
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L532)
```python
.ensure_other_list_zero_if_this_is_zero(
   other_list
)
```

---
Get the value of the elements where the passed in list is zero, otherwise
returned elements are zero.

### .make_sure_not_nan
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L596)
```python
.make_sure_not_nan()
```

---
Check if the food's nutritional values are NaN and raise an assertion error if they are.

**Args**

* **self** (Food) : An instance of the Food class.


**Returns**

None

### .get_remaining_food_needed_and_amount_used
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L699)
```python
.get_remaining_food_needed_and_amount_used(
   demand, resource, max_fraction_of__demand_satisfied_by_resource
)
```

---
Calculate the remaining food resource needed to satisfy a given food demand based on a certain resource.


**Args**

* **demand** (Food) : The food demand.
* **resource** (Food) : Available food resources.
* **max_fraction_of__demand_satisfied_by_resource** (float) : Maximum fraction of the demand which
    is allowed to be satisfied by the food resource.


**Returns**

* **Food**  : Remaining food needed to meet the demand.


### .shift
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L725)
```python
.shift(
   months
)
```

---
Shifts the monthly values of kcals, fat, and protein by the given number of months.
The newly introduced values (for months that are shifted into existence) will be set to 0.

### .plot
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L1182)
```python
.plot(
   title = 'genericfoodobjectovertime'
)
```

---
Plots the properties of this food object using the Plotter class.


**Args**

* **title** (str) : The title of the plot. Defaults to "generic food object over time".


**Returns**

* **str**  : The file path of the saved plot.


**Example**


```python

>>> food.plot("My Food Plot")
'/path/to/saved/plot.png'
```

### .is_list_monthly
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L1276)
```python
.is_list_monthly()
```

---
Check if kcals is a list or numpy array.

**Args**

* **self**  : instance of Food class


**Returns**

* **bool**  : True if kcals is a list or numpy array, False otherwise


### .is_never_negative
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L1287)
```python
.is_never_negative()
```

---
Checks whether the food's macronutrients are never negative.


**Returns**

* **bool**  : True if all macronutrients are non-negative, False otherwise.


### .all_greater_than
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L1313)
```python
.all_greater_than(
   other
)
```

---
Determines if the macronutrient values of the current food object are greater than the macronutrient values of

another food object.


**Args**

* **other** (Food) : The other food object to compare against.


**Returns**

* **bool**  : True if the current food object's macronutrient values are greater than the other food object's
macronutrient values.


**Raises**

* **AssertionError**  : If the units of the two food objects are not the same.


**Example**


```python

>>> food2 = Food('banana', 120, 0.4, 0.6, 0.3, 'g')
>>> food1.all_greater_than(food2)
False
```

### .all_less_than
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L1364)
```python
.all_less_than(
   other
)
```

---
Compares the macronutrient values of two food items and returns True if the values of the current food item
are less than the other food item's values.

**Args**

* **other** (Food) : The other food item to compare with.


**Returns**

* **bool**  : True if the current food item's macronutrient values are less than the other food item's values.


**Raises**

* **AssertionError**  : If the units of the two food items are not the same.


**Example**


```python

>>> food2 = Food('banana', 100, 1.0, 0.2, 'g')
>>> food1.all_less_than(food2)
True
```

### .any_greater_than
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L1411)
```python
.any_greater_than(
   other
)
```

---
Determines if the macronutrient values of the current food object are greater than the macronutrient values of
another food object.


**Args**

* **other** (Food) : The other food object to compare against.


**Returns**

* **bool**  : True if the current food object's macronutrient values are greater than the other food object's
macronutrient values.


**Raises**

* **AssertionError**  : If the units of the two food objects are not the same.


**Example**


```python

>>> food2 = Food('banana', 105, 0.4, 0.6, 0.1, 'g')
>>> food1.any_greater_than(food2)
False
```

### .any_less_than
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L1468)
```python
.any_less_than(
   other
)
```

---
Determines if the macronutrient values of the current food object are less than the macronutrient values of
another food object.

**Args**

* **other** (Food) : The other food object to compare against.


**Returns**

* **bool**  : True if the current food object's macronutrient values are less than the other food object's
macronutrient values.

### .all_greater_than_or_equal_to
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L1515)
```python
.all_greater_than_or_equal_to(
   other
)
```

---
Compares the macronutrient values of two food items and returns True if the values of the
current food item are greater than or equal to the other food item's values.


**Args**

* **other** (Food) : The other food item to compare with.


**Returns**

* **bool**  : True if the current food item's macronutrient values are greater than or equal to
the other food item's values, False otherwise.

### .all_less_than_or_equal_to
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L1555)
```python
.all_less_than_or_equal_to(
   other
)
```

---
Determines if the macronutrients of this food are less than or equal to the macronutrients of another food.

**Args**

* **other** (Food or List[Food]) : The other food or list of foods to compare to.


**Returns**

* **bool**  : True if the food's macronutrients are less than or equal to the other food's.

---
Cases:
    - This is a single food, other is a single food
    - This is a single food, other is a list of foods
    - This is a list of foods, other is a single food
    - This is a list of foods, other is a list of foods

### .any_greater_than_or_equal_to
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L1602)
```python
.any_greater_than_or_equal_to(
   other
)
```

---
Determines if the macronutrient values of the current food object are greater than or equal to
the macronutrient values of another food object.


**Args**

* **other** (Food) : The other food object to compare against.


**Returns**

* **bool**  : True if the current food object's macronutrient values are greater than or equal to
the other food object's macronutrient values.

### .any_less_than_or_equal_to
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L1644)
```python
.any_less_than_or_equal_to(
   other
)
```

---
Determines if the macronutrients of the current food object are less than or equal to
those of another food object.


**Args**

* **other** (Food) : The other food object to compare against.


**Returns**

* **bool**  : True if the current food's macronutrients are less than or equal to the other food's.


### .all_equals_zero
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L1704)
```python
.all_equals_zero(
   rounding_decimals = 9
)
```

---
Check if all macronutrients of the food are equal to zero.

**Args**

None

**Returns**

* **bool**  : True if the food's macronutrients are equal to zero, False otherwise.


### .any_equals_zero
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L1742)
```python
.any_equals_zero()
```

---
Check if any of the macronutrients of the food are equal to zero.

**Args**

None

**Returns**

* **bool**  : True if any of the macronutrients are equal to zero, False otherwise.


### .all_greater_than_zero
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L1784)
```python
.all_greater_than_zero()
```

---
Check if all macronutrients of the food are greater than zero.

**Args**

None

**Returns**

* **bool**  : True if all macronutrients are greater than zero, False otherwise.


### .any_greater_than_zero
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L1811)
```python
.any_greater_than_zero()
```

---
Returns True if any of the food's macronutrients are greater than zero.

**Args**

* **self** (Food) : an instance of the Food class


**Returns**

* **bool**  : True if any of the food's macronutrients are greater than zero, False otherwise


### .all_greater_than_or_equal_to_zero
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L1855)
```python
.all_greater_than_or_equal_to_zero(
   threshold = 0
)
```

---
Checks if all macronutrients of the food are greater than or equal to zero.

**Args**

* **self** (Food) : An instance of the Food class.


**Returns**

* **bool**  : True if all macronutrients are greater than or equal to zero, False otherwise.


### .as_numpy_array
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L1890)
```python
.as_numpy_array()
```


**Returns**

* **ndarray**  : an ordered numpy array containing the nutrients of the food.


### .get_min_nutrient
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L1898)
```python
.get_min_nutrient()
```

---
Returns the minimum nutrient of the food.

If the food is a list, it can return the minimum of any month of any nutrient.
If the food is not a list, it returns the minimum of any nutrient.

Only works when the units are identical for the different nutrients.


**Args**

* **self**  : an instance of the Food class


**Returns**

* **tuple**  : a tuple containing the name and value of the minimum nutrient


**Example**


```python

>>> food.get_min_nutrient()
('kcals', 0)

```

**Raises**

* **AssertionError**  : if the units for kcals, fat, and protein are not identical
* **AssertionError**  : if the minimum nutrient value is greater than the kcals value
* **AssertionError**  : if the minimum nutrient value is greater than the fat value and
                the fat nutrient is not excluded
* **AssertionError**  : if the minimum nutrient value is greater than the protein value and
                the protein nutrient is not excluded


### .get_max_nutrient
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L1961)
```python
.get_max_nutrient()
```

---
Returns the maximum nutrient of the food.

NOTE:
This function only works on single valued instances of nutrients, not arrays.


**Args**

None


**Returns**

* **tuple**  : A tuple containing the name and value of the maximum nutrient.


**Example**


```python

>>> food.kcals = 100
>>> food.fat = 20
>>> food.protein = 30
>>> food.conversions.include_fat = True
>>> food.conversions.include_protein = True
>>> food.kcals_units = "kcal"
>>> food.fat_units = "g"
>>> food.protein_units = "g"
>>> food.get_max_nutrient()
('fat', 20)
```

### .get_nutrients_sum
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L2024)
```python
.get_nutrients_sum()
```

---
Sums up the nutrients in all the months, then alters the units to remove "each month".

**Args**

* **self**  : instance of the Food class


**Returns**

* **Food**  : instance of the Food class with summed up nutrient values and altered units


**Raises**

* **AssertionError**  : if the list is not monthly


### .get_abs_values
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L2056)
```python
.get_abs_values()
```

---
Returns a new Food object with the absolute values of all nutrients.

### .get_running_total_nutrients_sum
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L2069)
```python
.get_running_total_nutrients_sum()
```

---
Calculates the running sum of the nutrients in all the months, without altering the units.

**Args**

* **self**  : instance of the Food class


**Returns**

* **Food**  : a new instance of the Food class with the running sum of the nutrients


### .get_amount_used_other_food
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L2123)
```python
.get_amount_used_other_food(
   other_fat_ratio, other_protein_ratio
)
```

---
Running sum of the amount used of the other food each month.

This function calculates the amount of stored food or outdoor growing that is
used by biofuels and feed. It determines the amount of the other food used by
taking the max amount used of the three nutrients, which is satisfied by a
certain number of units of the other food. Surplus of the nutrients used is
not used at all in the calculation.


**Args**

* **other_fat_ratio** (float) : The ratio of fat in the other food
* **other_protein_ratio** (float) : The ratio of protein in the other food


**Returns**

* **Food**  : A Food object containing the amount of kcals, fat, and protein consumed
each month


**Example**


```python

>>> other_fat_ratio = 0.2
>>> other_protein_ratio = 0.3
>>> amount_consumed_list = food.get_amount_used_other_food(other_fat_ratio, other_protein_ratio)
```

### .min_elementwise
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L2187)
```python
.min_elementwise(
   food1, food2
)
```

---
Returns a new Food object where each nutrient value
is the minimum between the corresponding values of food1 and food2.


**Args**

* **food1** (Food) : First Food object.
* **food2** (Food) : Second Food object.


**Returns**

* **Food**  : New Food object with minimum nutrient values for each month.


**Raises**

* **ValueError**  : If either of the Food objects is not in monthly list format.


### .get_consumed_amount
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L2237)
```python
.get_consumed_amount(
   demand_to_be_met, used_nutrient_ratio
)
```

---
Returns the amount used of the demand_to_be_met a food with a given used_nutrient_ratio.
The maximum nutrient used is used to determine the amount of the consumed
food will be used.


**Args**

* **demand_to_be_met** (Food) : A Food object representing the nutrient demand to be met
* **used_nutrient_ratio** (Food) : A Food object representing the nutrient ratio of the food being consumed


**Returns**

* **Food**  : A Food object representing the amount of food consumed to meet the nutrient demand


**Raises**

* **AssertionError**  : If demand_to_be_met is a monthly list
* **AssertionError**  : If used_nutrient_ratio fat or protein is less than or equal to 0


### .get_first_month
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L2280)
```python
.get_first_month()
```

---
Returns the nutrient values for the first month and converts the units from "each" to "per".

**Args**

* **self**  : instance of the Food class


**Returns**

* **dict**  : dictionary containing the nutrient values for the first month


**Raises**

* **AssertionError**  : if the nutrient values are not in a list format


### .get_month
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L2296)
```python
.get_month(
   index
)
```

---
Get the i month's nutrient values, and convert the units from "each" to "per".

**Args**

* **index** (int) : The index of the month to retrieve nutrient values for.


**Returns**

* **Food**  : A Food object containing the nutrient values for the specified month.


### .get_min_all_months
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L2326)
```python
.get_min_all_months()
```

---
Creates a new Food object with the minimum nutrient values for each month.

**Args**

* **self**  : The Food object to operate on.


**Returns**

A new Food object with the minimum nutrient values for each month.

### .get_max_all_months
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L2353)
```python
.get_max_all_months()
```

---
Returns a new Food object with the maximum nutrient values for each month.

**Args**

* **self** (Food) : The Food object to find the maximum nutrient values for.


**Returns**

* **Food**  : A new Food object with the maximum nutrient values for each month.


### .negative_values_to_zero
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L2380)
```python
.negative_values_to_zero()
```

---
Replaces negative values with zero for each month for all nutrients.
If the food object is monthly, it replaces negative values for each month.
If the food object is not monthly, it replaces negative values for the entire year.
Also tests that the function worked by asserting that all values are greater than or equal to zero.


**Args**

None


**Returns**

* **Food**  : the relevant food object with negative values replaced


### .get_rounded_to_decimal
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L2423)
```python
.get_rounded_to_decimal(
   decimals
)
```

---
Round the nutritional values of a food item to the nearest decimal place.


**Args**

* **decimals** (int) : The number of decimal places to round to.


**Returns**

* **Food**  : A new Food object with rounded nutritional values.


**Example**


```python

>>> rounded_food = food.get_rounded_to_decimal(1)
>>> rounded_food.kcals
100.1
>>> rounded_food.fat
5.7
>>> rounded_food.protein
11.0

```
---
NOTE: This function is only implemented for lists at the moment.

### .replace_if_list_with_zeros_is_zero
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L2462)
```python
.replace_if_list_with_zeros_is_zero(
   list_with_zeros, replacement
)
```

---
Replaces elements in a list with zeros with a specified replacement.


**Args**

* **list_with_zeros** (Food list) : A list that has zeros in it.
* **replacement** (Food list, Food, or number) : Thing used to replace the elements.


**Returns**

* **Food**  : A copy of the original list with places where list_with_zeros is zero replaced with replacement.


**Raises**

* **AssertionError**  : If the length of list_with_zeros is not equal to the length of the original list.
* **AssertionError**  : If the units of replacement are not the same as the units of the original list.


**Example**

* **kcals**  : [101 693   0   3 786], fat: [1 20 0 4 40], protein: [10 20 0 40 20]

```python

>>> list_with_zeros = Food(kcals=[0, 1, 3, 0, 5], fat=[0, 1, 3, 0, 5], protein=[0, 1, 3, 0, 5])
>>> replacement = Food(kcals=[101, 62, 23, 3, 0], fat=[1, 2, 3, 4, 5], protein=[10, 20, 30, 40, 50])
>>> processed_list = original_list.replace_if_list_with_zeros_is_zero(list_with_zeros, replacement)
>>> print(processed_list)
```

### .set_to_zero_after_month
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/food.py/#L2554)
```python
.set_to_zero_after_month(
   month
)
```

---
Set all values after the given month to zero.

**Args**

* **month** (int) : The month after which all values should be set to zero.


**Returns**

None
