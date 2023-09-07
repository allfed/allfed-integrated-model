#


## UnitConversions
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/unit_conversions.py/#L25)
```python 

```


---
This class is used to convert units of nutrients


**Methods:**


### .set_nutrition_requirements
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/unit_conversions.py/#L35)
```python
.set_nutrition_requirements(
   kcals_daily, fat_daily, protein_daily, include_fat, include_protein,
   population
)
```

---
Returns the macronutrients of the food.

This is a bit of a confusing function.

It is normally run from a UnitConversions class in the Food child class

that Food class contains one UnitConversions object which has had its nutrients
assigned.

Then, because this is the parent class, all the functions are inherited.

So, running get_conversions() (the class function to get the conversions object
in the child food class), this will obtain all the conversion data instantiated
through the Food class.

### .get_units_from_list_to_total
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/unit_conversions.py/#L92)
```python
.get_units_from_list_to_total()
```

---
gets the units so that they reflect that of a single month

### .set_units_from_list_to_total
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/unit_conversions.py/#L112)
```python
.set_units_from_list_to_total()
```

---
sets the units so that they reflect that of a single month

### .get_units_from_list_to_element
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/unit_conversions.py/#L129)
```python
.get_units_from_list_to_element()
```

---
gets the units so that they reflect that of a single month

### .set_units_from_list_to_element
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/unit_conversions.py/#L149)
```python
.set_units_from_list_to_element()
```

---
sets the units so that they reflect that of a single month

### .get_units_from_element_to_list
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/unit_conversions.py/#L163)
```python
.get_units_from_element_to_list()
```

---
gets the units so that they reflect that of a list of months

### .set_units_from_element_to_list
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/unit_conversions.py/#L181)
```python
.set_units_from_element_to_list()
```

---
sets the units so that they reflect that of a list of months

### .get_units
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/unit_conversions.py/#L194)
```python
.get_units()
```

---
update and return the unit values as a 3 element array

### .set_units
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/unit_conversions.py/#L202)
```python
.set_units(
   kcals_units, fat_units, protein_units
)
```

---
Sets the units of the food (for example, billion_kcals,thousand_tons, dry
caloric tons, kcals/person/day, or percent of global food supply).
default units are billion kcals, thousand tons fat, thousand tons protein
For convenience and as a memory tool, set the units, and make sure that whenever
an operation on a different food is used, the units are compatible

### .print_units
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/unit_conversions.py/#L220)
```python
.print_units()
```

---
Prints the units of the nutrients

### .is_a_ratio
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/unit_conversions.py/#L230)
```python
.is_a_ratio()
```

---
Returns if units are all "ratio" type

### .is_units_percent
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/unit_conversions.py/#L244)
```python
.is_units_percent()
```

---
Returns if units are all "percent" type

### .in_units_billions_fed
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/unit_conversions.py/#L259)
```python
.in_units_billions_fed()
```

---
If the existing units are understood by this function, it tries to convert the
values and units to billions of people fed.

### .in_units_percent_fed
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/unit_conversions.py/#L346)
```python
.in_units_percent_fed()
```

---
If the existing units are understood by this function, it tries to convert the
values and units to percent of people fed.

### .in_units_bil_kcals_thou_tons_thou_tons_per_month
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/unit_conversions.py/#L433)
```python
.in_units_bil_kcals_thou_tons_thou_tons_per_month()
```

---
If the existing units are understood by this function, it tries to convert the
values and units to percent of people fed.

### .in_units_kcals_equivalent
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/unit_conversions.py/#L493)
```python
.in_units_kcals_equivalent()
```

---
If the existing units are understood by this function, it tries to convert the
values and units to effective kcals per person per day for each nutrient.

### .in_units_kcals_grams_grams_per_person_from_ratio
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/unit_conversions.py/#L585)
```python
.in_units_kcals_grams_grams_per_person_from_ratio(
   kcal_ratio, fat_ratio, protein_ratio
)
```

---
If the existing units are understood by this function, it tries to convert the
values and units to kcals per person per day, grams per pseron per day, kcals
per person per day.
arguments:
kcal ratio (float): kcal  per kg of the food being converted
fat ratio (float): grams per kcal of the food being converted
kcal ratio (float): grams per kcal of the food being converted

### .in_units_kcals_grams_grams_per_person
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/unit_conversions.py/#L655)
```python
.in_units_kcals_grams_grams_per_person()
```

---
If the existing units are understood by this function, it tries to convert the
values and units to kcals per person per day, grams per pseron per day, kcals
per person per day.
