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
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/unit_conversions.py/#L182)
```python
.set_units_from_element_to_list()
```

---
sets the units so that they reflect that of a list of months

### .get_units
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/unit_conversions.py/#L195)
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

### .in_units_kcals_grams_grams_per_person_from_ratio
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/unit_conversions.py/#L259)
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

### .in_units_billions_fed
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/unit_conversions.py/#L327)
```python
.in_units_billions_fed()
```


### .in_units_percent_fed
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/unit_conversions.py/#L332)
```python
.in_units_percent_fed()
```


### .in_units_kcals_equivalent
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/unit_conversions.py/#L337)
```python
.in_units_kcals_equivalent()
```


### .in_units_kcals_grams_grams_per_person
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/unit_conversions.py/#L344)
```python
.in_units_kcals_grams_grams_per_person()
```


### .in_units_bil_kcals_thou_tons_thou_tons_per_month
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/unit_conversions.py/#L351)
```python
.in_units_bil_kcals_thou_tons_thou_tons_per_month()
```


### .get_kcal_multipliers
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/unit_conversions.py/#L358)
```python
.get_kcal_multipliers()
```

---
This function returns a dictionary, where the value is the multiplier on kcals required to convert from the
units "billion kcals each month" (or equivalently "billion kcals per month") to whatever unit is specified as
the key.

Therefore, multiplying kcals by this dictionary value is applying the unit multiplication: [key units] / [
billion kcals (each,per) month]

### .get_fat_multipliers
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/unit_conversions.py/#L400)
```python
.get_fat_multipliers()
```


### .get_protein_multipliers
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/unit_conversions.py/#L437)
```python
.get_protein_multipliers()
```


### .get_unit_multipliers_from_billion_kcals_thou_tons_thou_tons
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/unit_conversions.py/#L474)
```python
.get_unit_multipliers_from_billion_kcals_thou_tons_thou_tons(
   units
)
```

---
First, check if the unit is a known conversion.

Then, returns the conversion value to get from billion kcals, thousand tons fat, thousand tons protein, to
whatever units are specified in "units" triplet argument. units[0] is kcals units, units[1] is fat units,
units[2] is protein units.

### .get_conversion
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/unit_conversions.py/#L507)
```python
.get_conversion(
   from_units, to_units_kcals, to_units_fat, to_units_protein
)
```

---
To get from any known unit to any other known unit, we first convert the given from_units to the equivalent
billion kcals, thousand tons fat, thousand tons protein, by dividing the given value by the unit_multiplier
dictionary value. We then convert back to the to_units by multiplying by the to_unit dictionary value.

### .in_units
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/unit_conversions.py/#L532)
```python
.in_units(
   to_units_kcals, to_units_fat, to_units_protein
)
```

