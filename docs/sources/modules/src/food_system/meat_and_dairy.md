#


## MeatAndDairy
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/meat_and_dairy.py/#L12)
```python 
MeatAndDairy(
   constants_for_params
)
```




**Methods:**


### .calculate_meat_nutrition
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/meat_and_dairy.py/#L125)
```python
.calculate_meat_nutrition()
```

---
Calculates the nutritional values of meat products based on animal ratios and
nutritional ratios of small, medium, and large animals.


**Args**

* **self**  : instance of the class


**Returns**

None

### .get_meat_nutrition
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/meat_and_dairy.py/#L185)
```python
.get_meat_nutrition()
```

---
Returns a tuple containing nutritional information for different sizes of animals.


**Returns**

* **tuple**  : A tuple containing the following nutritional information:
    - KG_PER_SMALL_ANIMAL (float): The weight of meat in kilograms for a small animal.
    - KG_PER_MEDIUM_ANIMAL (float): The weight of meat in kilograms for a medium animal.
    - KG_PER_LARGE_ANIMAL (float): The weight of meat in kilograms for a large animal.
    - LARGE_ANIMAL_KCALS_PER_KG (float): The number of kilocalories per kilogram of meat for a large animal.
    - LARGE_ANIMAL_FAT_RATIO (float): The ratio of fat to meat for a large animal.
    - LARGE_ANIMAL_PROTEIN_RATIO (float): The ratio of protein to meat for a large animal.
    - MEDIUM_ANIMAL_KCALS_PER_KG (float): The number of kilocalories per kilogram of meat for a medium animal.
    - SMALL_ANIMAL_KCALS_PER_KG (float): The number of kilocalories per kilogram of meat for a small animal.


### .calculate_meat_limits
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/meat_and_dairy.py/#L211)
```python
.calculate_meat_limits(
   MAX_RATIO_CULLED_SLAUGHTER_TO_BASELINE, culled_meat_initial
)
```

---
Calculate the baseline levels of meat production, indicating slaughter capacity.

There's no limit on the actual amount eaten, but the amount produced and
then preserved after culling is assumed to be some multiple of current slaughter
capacity. This just means that the limit each month on the amount that could be eaten is
the sum of the max estimated slaughter capacity each month.


**Args**

* **MAX_RATIO_CULLED_SLAUGHTER_TO_BASELINE** (float) : The maximum ratio of culled meat to baseline meat.
* **culled_meat_initial** (float) : The initial amount of culled meat.


**Returns**

* **ndarray**  : An array of cumulative meat limits for each month.


### .calculate_continued_ratios_meat_dairy_grazing
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/meat_and_dairy.py/#L250)
```python
.calculate_continued_ratios_meat_dairy_grazing(
   constants_for_params
)
```

---
Calculates the ratios of grazing meat and milk produced pre-waste based on the
number of dairy cows and total heads of cattle precatastrophe.


**Args**

* **constants_for_params** (dict) : dictionary of constants used in the simulation


**Returns**

None


**Raises**

* **AssertionError**  : if the calculated ratios are not between 0 and 1


### .calculate_continued_ratios_meat_dairy_grain
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/meat_and_dairy.py/#L321)
```python
.calculate_continued_ratios_meat_dairy_grain(
   fed_to_animals_prewaste, outdoor_crops
)
```

---
Calculates the ratios of grain-fed meat, grain-fed milk, and grain-fed chicken/pork
maintained pre-waste. The ratios are calculated based on the amount of feed used for
meat cattle and chicken/pork precatastrophe, and the amount of human-edible feed used
for dairy. The function also calculates the amount of grain-fed milk produced pre-waste,
the amount of cattle grain-fed maintained pre-waste, and the amount of chicken/pork
maintained pre-waste.


**Args**

* **fed_to_animals_prewaste** (class) : an instance of the FedToAnimalsPrewaste class
* **outdoor_crops** (class) : an instance of the OutdoorCrops class


**Returns**

None

### .calculate_meat_and_dairy_from_grain
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/meat_and_dairy.py/#L412)
```python
.calculate_meat_and_dairy_from_grain(
   fed_to_animals_prewaste
)
```

---
Calculates the amount of meat and dairy that can be produced from excess grain fed to animals.
The excess grain is first used to produce milk, then to feed pigs and chickens, and finally to feed cattle.


**Args**

* **fed_to_animals_prewaste** (np.ndarray) : array of kcals fed to animals before waste


**Returns**

None


**Raises**

* **AssertionError**  : if any of the calculated values are negative


### .calculate_meat_milk_from_human_inedible_feed
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/meat_and_dairy.py/#L532)
```python
.calculate_meat_milk_from_human_inedible_feed(
   constants_for_params
)
```

---
Calculates the amount of milk and meat that can be produced from human inedible feed.

**Args**

* **self**  : instance of the class
* **constants_for_params**  : dictionary containing constants used in the calculations


**Returns**

None

### .get_milk_from_human_edible_feed
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/meat_and_dairy.py/#L583)
```python
.get_milk_from_human_edible_feed(
   constants_for_params
)
```

---
Calculates the amount of milk produced from human-edible feed, taking into account
the amount of waste produced during the process.


**Args**

* **self** (object) : The object instance
* **constants_for_params** (dict) : A dictionary containing the constants used in the
calculations


**Returns**

* **tuple**  : A tuple containing the amount of kcals, fat, and protein produced from
grain-fed milk

### .get_meat_from_human_edible_feed
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/meat_and_dairy.py/#L632)
```python
.get_meat_from_human_edible_feed()
```

---
Calculates the amount of meat that can be obtained from human-edible feed.

**Args**

* **self**  : instance of the class containing the necessary data for calculations


**Returns**

* **tuple**  : a tuple containing the amount of kcals, fat, and protein that can be obtained from the meat


### .get_grazing_milk_produced_postwaste
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/meat_and_dairy.py/#L771)
```python
.get_grazing_milk_produced_postwaste(
   grazing_milk_produced_prewaste
)
```

---
Calculates the amount of grazing milk produced post-waste, given the amount of grazing milk produced pre-waste.


**Args**

* **grazing_milk_produced_prewaste** (list) : A list of the amount of grazing milk produced pre-waste.


**Returns**

* **tuple**  : A tuple containing the amount of grazing milk produced post-waste in billions of kcals, thousands of tons of fat, and thousands of tons of protein.


### .get_cattle_grazing_maintained
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/meat_and_dairy.py/#L810)
```python
.get_cattle_grazing_maintained()
```

---
Calculates the kcals, fat, and protein from cattle grazing that is maintained for meat production.
If ADD_MAINTAINED_MEAT is True, the function calculates the kcals, fat, and protein from cattle grazing that is maintained for meat production.
If ADD_MAINTAINED_MEAT is False, the function returns 0 for kcals, fat, and protein.

**Args**

* **self**  : instance of the class


**Returns**

* **tuple**  : a tuple containing the kcals, fat, and protein from cattle grazing that is maintained for meat production.


### .get_max_slaughter_monthly
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/meat_and_dairy.py/#L866)
```python
.get_max_slaughter_monthly(
   small_animals_culled, medium_animals_culled, large_animals_culled
)
```

---
Get the maximum number of animals that can be culled in a month and return the
resulting array for max total calories slaughtered that month.


**Args**

* **self** (object) : instance of the class
* **small_animals_culled** (list) : list of integers representing the number of small animals culled each month
* **medium_animals_culled** (list) : list of integers representing the number of medium animals culled each month
* **large_animals_culled** (list) : list of integers representing the number of large animals culled each month


**Returns**

* **list**  : list of integers representing the maximum total calories that can be slaughtered each month


**Raises**

None

### .calculate_culled_meat
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/meat_and_dairy.py/#L901)
```python
.calculate_culled_meat(
   init_small_animals_culled, init_medium_animals_culled,
   init_large_animals_culled
)
```

---
Calculates the amount of culled meat in billion kcals, thousand tons of fat, and thousand tons of protein
based on the number of small, medium, and large animals culled.


**Args**

* **self** (object) : instance of the class
* **init_small_animals_culled** (int) : number of small animals culled
* **init_medium_animals_culled** (int) : number of medium animals culled
* **init_large_animals_culled** (int) : number of large animals culled


**Returns**

* **tuple**  : a tuple containing the initial culled meat pre-waste in billion kcals,
the fraction of culled meat that is fat, and the fraction of culled meat that is protein

### .get_culled_meat_post_waste
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/meat_and_dairy.py/#L999)
```python
.get_culled_meat_post_waste(
   constants_for_params
)
```

---
Calculates the amount of culled meat post-waste based on the initial amount of culled meat pre-waste and the
percentage of meat waste.


**Args**

* **self**  : instance of the class containing the function
* **constants_for_params**  : dictionary containing the constants used in the calculation


**Returns**

* **float**  : the amount of culled meat post-waste


### .calculate_animals_culled
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/meat_and_dairy.py/#L1023)
```python
.calculate_animals_culled(
   constants_for_params
)
```

---
Calculates the number of animals culled based on the given constants and parameters.


**Args**

* **self**  : instance of the class
* **constants_for_params**  : dictionary containing the constants and parameters


**Returns**

None

---
The function calculates the number of animals culled based on the given constants and parameters.
If ADD_CULLED_MEAT is True, the function calculates the number of small, medium, and large animals culled
based on the ratio of maintained chicken and pork and the ratio of not maintained cattle.
If ADD_CULLED_MEAT is False, the function sets the number of culled animals to 0.
