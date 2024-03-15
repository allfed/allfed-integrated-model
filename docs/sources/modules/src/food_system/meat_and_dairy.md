#


## MeatAndDairy
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/meat_and_dairy.py/#L14)
```python 
MeatAndDairy(
   constants_for_params
)
```




**Methods:**


### .calculate_meat_nutrition
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/meat_and_dairy.py/#L233)
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
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/meat_and_dairy.py/#L293)
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
    - MEDIUM_ANIMAL_KCALS_PER_KG (float): The number of kilocalories per kilogram of meat for a medium
        animal.
    - SMALL_ANIMAL_KCALS_PER_KG (float): The number of kilocalories per kilogram of meat for a small animal.


### .get_milk_produced_postwaste
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/meat_and_dairy.py/#L324)
```python
.get_milk_produced_postwaste(
   milk_produced_prewaste
)
```

---
Calculates the amount of grazing milk produced post-waste, given the amount of grazing milk produced pre-waste.


**Args**

* **milk_produced_prewaste** (list) : A list of the amount of grazing milk produced pre-waste.


**Returns**

* **tuple**  : A tuple containing the amount of grazing milk produced post-waste in billions of kcals, thousands
of tons of fat, and thousands of tons of protein.

### .get_max_slaughter_monthly_after_distribution_waste
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/meat_and_dairy.py/#L372)
```python
.get_max_slaughter_monthly_after_distribution_waste(
   constants_inputs, chickens_culled, pigs_culled,
   small_animals_nonchicken_culled, medium_animals_nonpig_culled,
   large_animals_culled
)
```

---
Get the maximum number of animals that can be culled in a month and return the
resulting array for max total calories slaughtered that month.

### .initialize_this_country_animal_kcals
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/meat_and_dairy.py/#L420)
```python
.initialize_this_country_animal_kcals(
   constants_inputs
)
```


### .calculate_meat_after_distribution_waste
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/meat_and_dairy.py/#L498)
```python
.calculate_meat_after_distribution_waste(
   constants_inputs, init_chickens_culled, init_pigs_culled,
   init_small_animals_nonchicken_culled, init_medium_animals_nonpigs_culled,
   init_large_animals_culled
)
```

