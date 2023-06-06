#


## UnitConversions
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/unit_conversions.py/#L25)
```python 

```


---
This class is used to convert units of nutrients


**Methods:**


### .set_nutrition_requirements
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/unit_conversions.py/#L44)
```python
.set_nutrition_requirements(
   kcals_daily, fat_daily, protein_daily, include_fat, include_protein,
   population
)
```

---
Calculates the monthly nutritional requirements for a given population based on daily intake.


**Args**

* **kcals_daily** (float) : daily caloric intake per person
* **fat_daily** (float) : daily fat intake per person in grams
* **protein_daily** (float) : daily protein intake per person in grams
* **include_fat** (bool) : whether or not to include fat in the calculations
* **include_protein** (bool) : whether or not to include protein in the calculations
* **population** (int) : number of people to calculate nutritional requirements for


**Returns**

None

---
This function calculates the monthly nutritional requirements for a given population based on daily intake.
It sets several instance variables that can be accessed later.

### .get_units_from_list_to_total
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/unit_conversions.py/#L102)
```python
.get_units_from_list_to_total()
```

---
Gets the units for a single month by removing the " each month" part of the units for kcals, fat, and protein.


**Args**

* **self**  : An instance of the class containing kcals_units, fat_units, and protein_units attributes.


**Returns**

* **list**  : A list of the units for kcals, fat, and protein for a single month.


**Raises**

* **AssertionError**  : If "each month" is not found in kcals_units, fat_units, or protein_units.


### .set_units_from_list_to_total
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/unit_conversions.py/#L131)
```python
.set_units_from_list_to_total()
```

---
Sets the units for a single month.

This function removes the " each month" part of the units for kcals, fat, and protein.
It then sets the units attribute to a list of the units for kcals, fat, and protein for a single month.


**Args**

None


**Returns**

None

### .get_units_from_list_to_element
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/unit_conversions.py/#L160)
```python
.get_units_from_list_to_element()
```

---
Gets the units for a single element.

This function replaces the " each month" part of the units for kcals, fat, and protein with "per month".
It then returns a list of the units for kcals, fat, and protein for a single element.


**Args**

* **self**  : An instance of the class containing kcals_units, fat_units, and protein_units.


**Returns**

* **list**  : A list of the units for kcals, fat, and protein for a single element.


### .set_units_from_list_to_element
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/unit_conversions.py/#L187)
```python
.set_units_from_list_to_element()
```

---
Sets the units for a single element.

This function sets the kcals_units, fat_units, and protein_units attributes to the units for a single element.
It first checks that this only happens for monthly food. Then it sets the units by calling the get_units_from_list_to_element() function.


**Args**

None


**Returns**

None

### .get_units_from_element_to_list
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/unit_conversions.py/#L213)
```python
.get_units_from_element_to_list()
```

---
Gets the units for a list of months.

This function takes the units for kcals, fat, and protein and adds " each month" to signify a food list.
It then returns a list of the units for kcals, fat, and protein for a list of months.


**Returns**

* **list**  : A list of the units for kcals, fat, and protein for a list of months.


### .set_units_from_element_to_list
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/unit_conversions.py/#L237)
```python
.set_units_from_element_to_list()
```

---
Sets the units for a list of months.

This function sets the kcals_units, fat_units, and protein_units attributes to the units for a list of months.
It first checks that this is only happening for a single element. Then, it sets the units for each attribute by
calling the get_units_from_element_to_list() function.


**Args**

None


**Returns**

None

### .get_units
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/unit_conversions.py/#L264)
```python
.get_units()
```

---
Gets the units for kcals, fat, and protein.

Updates the units attribute to the current values of kcals_units, fat_units, and protein_units.


**Returns**

* **list**  : A list of the units for kcals, fat, and protein.


### .set_units
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/unit_conversions.py/#L280)
```python
.set_units(
   kcals_units, fat_units, protein_units
)
```

---
Sets the units for kcals, fat, and protein.

Sets the kcals_units, fat_units, and protein_units attributes to the specified units.


**Args**

* **kcals_units** (str) : The units for kcals.
* **fat_units** (str) : The units for fat.
* **protein_units** (str) : The units for protein.


**Returns**

None

### .print_units
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/unit_conversions.py/#L307)
```python
.print_units()
```

---
Prints the units for kcals, fat, and protein.

This function prints the units for kcals, and optionally for fat and protein if they are included in the conversions.


**Args**

None


**Returns**

None

### .is_a_ratio
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/unit_conversions.py/#L331)
```python
.is_a_ratio()
```

---
Checks if the units for kcals, fat, and protein are all "ratio" type.


**Returns**

* **bool**  : True if the units for kcals, fat, and protein are all "ratio" type, False otherwise.


### .is_units_percent
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/unit_conversions.py/#L351)
```python
.is_units_percent()
```

---
Checks if the units for kcals, fat, and protein are all "percent" type.


**Returns**

* **bool**  : True if the units for kcals, fat, and protein are all "percent" type, False otherwise.


### .in_units_billions_fed
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/unit_conversions.py/#L369)
```python
.in_units_billions_fed()
```

---
Converts the values and units to billions of people fed if the existing units are understood by this function.


**Returns**

* **Food**  : A new Food instance with the converted values and units.


### .in_units_percent_fed
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/unit_conversions.py/#L480)
```python
.in_units_percent_fed()
```

---
Converts the values and units of a Food instance to percent of people fed, if the existing units are understood by this function.

**Args**

* **self** (Food) : The Food instance to be converted.


**Returns**

* **Food**  : A new Food instance with the converted values and units.


### .in_units_bil_kcals_thou_tons_thou_tons_per_month
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/unit_conversions.py/#L571)
```python
.in_units_bil_kcals_thou_tons_thou_tons_per_month()
```

---
Converts values and units to billion kcals and thousand tons per month if the existing units are understood by this function.

**Args**

* **self**  : An instance of the Food class.


**Returns**

* **Food**  : A new Food instance with the converted values and units.


### .in_units_kcals_equivalent
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/unit_conversions.py/#L664)
```python
.in_units_kcals_equivalent()
```

---
Converts the values and units to effective kcals per capita per day for each nutrient
if the existing units are understood by this function.


**Returns**

* **Food**  : A new Food instance with the converted values and units.


### .in_units_kcals_grams_grams_per_capita_from_ratio
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/unit_conversions.py/#L761)
```python
.in_units_kcals_grams_grams_per_capita_from_ratio(
   kcal_ratio, fat_ratio, protein_ratio
)
```

---
Converts values and units to kcals per person per day, grams per person per day, kcals per person per day.
If the existing units are understood by this function, it tries to convert the values and units to kcals per person per day, grams per person per day, kcals per person per day.

**Args**

* **self** (UnitConversions) : instance of the UnitConversions class
* **kcal_ratio** (float) : kcal per kg of the food being converted
* **fat_ratio** (float) : grams per kcal of the food being converted
* **protein_ratio** (float) : grams per kcal of the food being converted


**Returns**

* **Food**  : instance of the Food class with converted units


**Raises**

* **AssertionError**  : if conversion from these units is not known


### .in_units_kcals_grams_grams_per_capita
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/unit_conversions.py/#L832)
```python
.in_units_kcals_grams_grams_per_capita()
```

---
If the existing units are understood by this function, it tries to convert the
values and units to kcals per person per day, grams per pseron per day, kcals
per person per day.
