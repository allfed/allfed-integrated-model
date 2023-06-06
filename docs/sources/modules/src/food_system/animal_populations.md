#


## AnimalSpecies
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L41)
```python 
AnimalSpecies(
   animal_type, animal_species, population, slaughter, animal_function,
   feed_LSU, digestion_type, approximate_feed_conversion,
   digestion_efficiency = 0.5, carb_requirement = -1, protein_requirement = -1,
   fat_requirement = -1
)
```


---
Class to store animal population data in. Needs to store the following: animal type, population, and slaughter.

Parameters
----------
animal_type : str
Type of animal (beef, pork, chicken etc...)
population : int
Number of animals (total)
slaughter : int
Number of animals slaughtered this month
pregnant : int
Number of animals pregnant this month
starving : int
Number of animals starving this month
feed_required : int
Amount of feed required this month
nutrition_ratio : object
Object containing the nutrition ratio for the animal type


**Methods:**


### .set_species_milk_attributes
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L105)
```python
.set_species_milk_attributes(
   productive_milk_age_start, productive_milk_age_end,
   milk_production_per_month = None
)
```


### .retiring_milk_head_monthly
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L116)
```python
.retiring_milk_head_monthly()
```

---
Function to calculate the number of retiring milk animals per month

### .set_species_slaughter_attributes
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L122)
```python
.set_species_slaughter_attributes(
   gestation, other_animal_death_rate_annual, animals_per_pregnancy,
   animal_slaughter_hours, change_in_slaughter_rate,
   pregnant_animal_slaughter_fraction, reduction_in_animal_breeding,
   target_population_fraction, transfer_births_or_head = 0
)
```

---
Function to set the attributes of the animal species that are related to slaughter

Parameters
----------
gestation : int
gestation period in months
---
    annual death rate of animals
    number of animals per pregnancy
    hours per animal spent slaughtering
    change in slaughter rate (a static value, given by assumptions of loss of industry etc...)
    this is the fraction of pregnant animals that are attempted to be slaughtered each month
    this is the reduction in animal breeding (a static value, given by assumptions of loss of industry etc...)
    this is the target population fraction (a static value, given by assumptions of loss of industry etc...)
    this is head of increased population due to either male offspring of milk animals being added toa meat population or head imported from other countries

Returns
-------
None

### .exported_births
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L185)
```python
.exported_births()
```

---
Function to calculate the number of births exported from the animal population

Parameters
----------
None

Returns
-------
exported_births : int
the number of births exported from the animal population

### .net_energy_required_per_month
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L204)
```python
.net_energy_required_per_month()
```


### .feed_required_per_month_individual
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L222)
```python
.feed_required_per_month_individual()
```


### .feed_required_per_month_species
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L229)
```python
.feed_required_per_month_species()
```


### .feed_the_species
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L236)
```python
.feed_the_species(
   food_input
)
```


----


### read_animal_population_data
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L290)
```python
.read_animal_population_data()
```

---
Read animal population data from CSV file

Returns
-------
df_animal_stock_info : pandas dataframe
Dataframe containing animal population data

----


### read_animal_nutrition_data
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L316)
```python
.read_animal_nutrition_data()
```

---
"
Read animal nutrition data from CSV file

Returns
-------
df_animal_nutrition : pandas dataframe
Dataframe containing animal nutrition data

----


### read_animal_options
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L338)
```python
.read_animal_options()
```

---
"
Read animal nutrition data from CSV file

Returns
-------
df_animal_nutrition : pandas dataframe
Dataframe containing animal nutrition data

----


### create_animal_objects
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L360)
```python
.create_animal_objects(
   df_animal_stock_info, df_animal_attributes
)
```

---
Create animal objects from dataframes

Parameters
----------
df_animal_stock_info : pandas dataframe
Single dimension Dataframe containing animal population data for each country 
---
    Dataframe containing animal nutrition data

Returns
-------
    List of animal objects

----


### update_animal_objects_with_slaughter
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L431)
```python
.update_animal_objects_with_slaughter(
   animal_list, df_animal_attributes, df_animal_options
)
```

---
This function updates the animal objects with the slaughter data

Parameters
----------
animal_list : list
List of animal objects
---
    Dataframe containing animal attibute data
    Dataframe containing animal options data

Returns
-------
    List of animal objects

----


### update_animal_objects_with_milk
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L478)
```python
.update_animal_objects_with_milk(
   animal_list, df_animal_attributes
)
```

---
This function updates the animal objects with the slaughter data

Parameters
----------
animal_list : list
List of animal objects
---
    Dataframe containing animal attibute data
    Dataframe containing animal options data

Returns
-------
    List of animal objects

----


### food_conversion
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L515)
```python
.food_conversion()
```


----


### available_feed
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L520)
```python
.available_feed()
```

---
Energy is expressed as digestible (DE), metabolizable (ME), or net energy (NE) by considering the loss of energy during digestion and metabolism from gross energy (GE) in the feed, as follows:

Gross energy (GE): the amount of energy in the feed.
Digestible energy (DE): the amount of energy in the feed minus the amount of energy lost in the feces.
Metabolizable energy (ME): the amount of energy in the feed minus the energy lost in the feces and urine.
Net energy (NE): the amount of energy in the feed minus the energy lost in the feces, urine, and in heat production through digestive and metabolic processes, i.e. heat increment.

----


### available_grass
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L545)
```python
.available_grass()
```

---
Energy is expressed as digestible (DE), metabolizable (ME), or net energy (NE) by considering the loss of energy during digestion and metabolism from gross energy (GE) in the feed, as follows:

Gross energy (GE): the amount of energy in the feed.
Digestible energy (DE): the amount of energy in the feed minus the amount of energy lost in the feces.
Metabolizable energy (ME): the amount of energy in the feed minus the energy lost in the feces and urine.
Net energy (NE): the amount of energy in the feed minus the energy lost in the feces, urine, and in heat production through digestive and metabolic processes, i.e. heat increment.

----


### feed_animals
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L569)
```python
.feed_animals(
   animal_list, milk_animals, non_milk_ruminants, non_milk_animals,
   available_feed, available_grass
)
```

---
This function will feed the animals
It will do so by allocating the grass first to those animals that can eat it,
and then allocating the remaining feed to the remaining animals

It will also priotiise the animals that are most efficient at converting feed,
This means starting with milk.

List needs to be sorted in the oprder you want the animals to be prioritised for feed

----


### calculate_additive_births
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L602)
```python
.calculate_additive_births(
   animal_object, current_month
)
```


----


### calculate_change_in_population
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L616)
```python
.calculate_change_in_population(
   animal_object, spare_slaughter_hours, new_additive_animals_month
)
```

---
This function will calculate the change in animal population for a given animal type
It will do so by calculating the number of new births, the number of deaths, and the number of animals slaughtered
It will then update the animal object with the new population

It will also update the animal object with the number of animals that are pregnant, and the number of animals that are lactating

Some parameters are calulctaed before the 'slaughter event' where the populations change, some are calculated after
Those that are calulcated before are:
- the new births this month (based on the number of animals that are pregnant)
- other deaths this month
- the slauhter rate this month  
- spare slaughter hours this month
---
Those that are calculated after are:
    - the number of animals that are lactating
    - the new population this month
    - the population of animals that are pregnant for next month

----


### calculate_pregnant_animals_birthing
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L695)
```python
.calculate_pregnant_animals_birthing(
   animal_object, new_pregnant_animals_total
)
```

---
This function will calculate the number of pregnant animals birthing this month, based on the number of pregnant animals remaining
Uses a simple calculation of the number of pregnant animals divided by the gestation period
This is not a perfect calculation, as it assumes that an even distribution of animals will birth each month
However, it is a good approximation for the purposes of this model

Parameters
----------
animal_object : AnimalSpecies
The animal object for the animal type that you want to calculate the change in population for
---
    The number of pregnant animals remaining this month

Returns
-------
    The number of pregnant animals birthing this month

----


### calculate_pregnant_slaughter
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L719)
```python
.calculate_pregnant_slaughter(
   animal_object, new_slaughter_rate
)
```

---
This function will determine how many of the animals who died this month were pregnant
Check if the number of pregnant animals set for slaughter is less than the number of animals slaughtered this month
If so, proceed to calculate the number of pregnant animals slaughtered
Otherwise, set the number of pregnant animals slaughtered to the number of animals slaughtered this month

----


### calculate_animal_population
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L740)
```python
.calculate_animal_population(
   animal_object, new_births_animals_month, new_other_animal_death,
   new_slaughter_rate
)
```


----


### calculate_retiring_milk_animals
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L750)
```python
.calculate_retiring_milk_animals(
   animal_object
)
```

---
This function calculates the number of animals retiring from milk production this month

Parameters
----------
animal_object : object
The animal object that is being calculated

---
Returns
-------
    The number of animals retiring from milk production this month        

----


### calculate_births
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L769)
```python
.calculate_births(
   animal_object
)
```

---
This function calculates the number of new births this month

Parameters
----------
animal_object : object
The animal object that is being calculated

---
Returns
-------
    The number of new births this month        

----


### calculate_breeding_changes
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L789)
```python
.calculate_breeding_changes(
   animal_object
)
```


----


### calculate_other_deaths
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L795)
```python
.calculate_other_deaths(
   animal_object
)
```


----


### calculate_slaughter_rate
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L800)
```python
.calculate_slaughter_rate(
   animal_object, spare_slaughter_hours, target_animal_population,
   new_births_animals_month, new_other_animal_death
)
```

---
This function calculates the new slaughter rate based on the spare slaughter hours and the target animal population

Parameters
----------
animal_object : object
The animal object that is being calculated
---
    The number of spare slaughter hours generated
    The target animal population

Returns
-------
    The new slaughter rate
    The number of spare slaughter hours remaining after the new slaughter rate is calculated
