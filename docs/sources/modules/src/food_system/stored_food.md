#


## StoredFood
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/stored_food.py/#L11)
```python 
StoredFood(
   constants_for_params, outdoor_crops
)
```




**Methods:**


### .calculate_stored_food_to_use
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/stored_food.py/#L49)
```python
.calculate_stored_food_to_use(
   starting_month
)
```

---
Calculates and returns total stored food available to use at start of
simulation. While a baseline scenario will simply use the typical amount
of stocks to keep the buffer at a typical usage, other more extreme
scenarios should be expected to use a higher percentage of all stored food,
eating into the typical buffer.

**Arguments**

* **starting_month** (int) : the month the simulation starts on.
1=JAN, 2=FEB, ...,  12=DEC.
(NOT TO BE CONFUSED WITH THE INDEX)


**Returns**

* **float**  : the total stored food in millions of tons dry caloric

---
Assumptions:

end_simulation_ratio (float): the percent of the typical stored food
to keep at the end of the simulation.

The stocks listed are tabulated at the end of the month.

The minimum of any beginning month is a reasonable proxy for the very
lowest levels stocks reach.

**Note**

the optimizer will run through the stocks for the duration of
each month. So, even starting at August (the minimum month), you would
want to use the difference in stocks at the end of the previous month
until the end of August to determine the stocks.
