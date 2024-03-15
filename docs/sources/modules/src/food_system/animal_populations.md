#


## CalculateFeedAndMeat
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L44)
```python 
CalculateFeedAndMeat(
   country_code, available_feed, available_grass, scenario,
   kcals_per_head_meat_dict, constants_inputs = None
)
```




**Methods:**


### .get_meat_produced
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L71)
```python
.get_meat_produced()
```


### .get_total_dairy_cows
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L141)
```python
.get_total_dairy_cows()
```


### .get_total_milk_bearing_animals
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L156)
```python
.get_total_milk_bearing_animals()
```

---
Calculates the total number of milk-bearing animals in the population.


**Returns**

* **ndarray**  : An array containing the total number of milk-bearing animals for each month


----


## CountryData
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L171)
```python 
CountryData(
   country_name
)
```


---
Main functionalities:
CountryData is a class that represents data for a specific country in the food system model. It contains fields
for various data points such as slaughter hours, homekill hours, and meat output. The class has methods
for setting livestock unit factors, calculating homekill hours, and calculating total slaughter hours.

Methods:
- __init__(self, country_name): initializes the CountryData object with the given country name and sets
various fields to empty lists or 0.
---
     LSU conversion factors for the country based on the given dataframes.
- homekill_desperation_parameters(self): sets the homekill fraction and other death homekill rate.
- calculate_homekill_hours(self): calculates the number of hours required to slaughter homekill animals.
    the given list.

Fields:
- country_name: the name of the country.
- slaughter_hours: a list of total slaughter hours for each month.
- homekill_hours_total_month: a list of total homekill hours for each month.
- homekill_hours_budget: a list of budgeted homekill hours for each month.
- meat_output: a list of meat output for each month.
- small_slaughter_hours: the number of small animal slaughter hours for the country.
- medium_slaughter_hours: the number of medium animal hours for the country.
- large_slaughter_hours: the number of large animal hours for the country.
- EK_region: the FAO region for the country.
- LSU_conversion_factors: a dictionary of livestock unit conversion factors for the country.


**Methods:**


### .set_livestock_unit_factors
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L211)
```python
.set_livestock_unit_factors(
   df_country_info, df_regional_conversion_factors
)
```

---
Requires inputs of the country info dataframe, and the regional conversion factors dataframe
df_regional_conversion_factors dataframe contains the conversion factors for the LSU for each animal type, based
on ther region. And the other, df_country_info contains the mapping from the country to the region.

Country Name needs to be the index of the df_country_info dataframe

### .homekill_desperation_parameters
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L258)
```python
.homekill_desperation_parameters()
```


### .calculate_homekill_hours
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L265)
```python
.calculate_homekill_hours()
```

---
Function to calculate the number of hours required to slaughter the homekill animals.

### .calculate_total_slaughter_hours
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L272)
```python
.calculate_total_slaughter_hours(
   all_animals
)
```

---
Probably unneccesary, but could be sueful to ibnterogate the number of salughter hours to compare between
countries.

Not required for the program to work (and not called)

----


## AnimalSpecies
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L299)
```python 
AnimalSpecies(
   animal_type, animal_species
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
feed_balance : int
Amount of feed required this month
nutrition_ratio : object
Object containing the nutrition ratio for the animal type


**Methods:**


### .update_attributes
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L330)
```python
.update_attributes(
   **kwargs
)
```


### .set_animal_attributes
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L334)
```python
.set_animal_attributes(
   population, slaughter, animal_function, livestock_unit, digestion_type,
   animal_size, approximate_feed_conversion, digestion_efficiency_grass = 0.6,
   digestion_efficiency_feed = 0.8, carb_requirement = -1, protein_requirement = -1,
   fat_requirement = -1
)
```


### .set_LSU_attributes
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L420)
```python
.set_LSU_attributes(
   country_object
)
```


### .set_species_milk_attributes
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L426)
```python
.set_species_milk_attributes(
   productive_milk_age_start, productive_milk_age_end,
   insemination_cycle_time_for_milk, milk_production_per_month_per_head = None
)
```


### .retiring_milk_head_monthly
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L461)
```python
.retiring_milk_head_monthly()
```

---
Function to calculate the number of retiring milk animals per month

### .set_species_slaughter_attributes
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L467)
```python
.set_species_slaughter_attributes(
   gestation, other_animal_death_rate_annual, animals_per_pregnancy,
   animal_slaughter_hours, change_in_slaughter_rate,
   pregnant_animal_slaughter_fraction, reduction_in_animal_breeding,
   target_population_fraction, starvation_death_fraction,
   transfer_births_or_head
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
    0.5 = half of animals slaughtered
    animals are attempted to be slaughtered, 0.5 = half of pregnant animals
    1 = no reduction, 0.5 = half of animals are bred
    = target population is equal to the iniitla population, 0 = targetting to kill all animals
    population or head imported from other countries

Returns
-------
None

### .set_milk_birth
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L668)
```python
.set_milk_birth()
```


### .set_initial_milk_transfer
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L681)
```python
.set_initial_milk_transfer()
```


### .total_homekill
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L690)
```python
.total_homekill()
```

---
Function to calculate the total homekill per month.

Parameters
----------
None

Returns
-------
total_homekill : int
the total homekill per month

### .exported_births
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L714)
```python
.exported_births()
```

---
Function to calculate the number of births exported from the animal population.

Parameters
----------
None

Returns
-------
exported_births : int
the number of births exported from the animal population

### .one_LSU_monthly_billion_kcal
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L731)
```python
.one_LSU_monthly_billion_kcal()
```


### .net_energy_required_per_month
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L748)
```python
.net_energy_required_per_month()
```

---
Function to calculate the total net energy required per month for the species

### .net_energy_required_per_species
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L757)
```python
.net_energy_required_per_species()
```

---
Function to calculate the total net energy required per month for the species

### .reset_NE_balance
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L764)
```python
.reset_NE_balance()
```

---
This function resets the feed balance to the feed required per month for the species
Needs to be run before feeding the animals each month.

### .feed_the_species
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L774)
```python
.feed_the_species(
   grass_input, feed_input, is_ruminant = False
)
```


### .append_month_zero
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L818)
```python
.append_month_zero()
```

---
Objective:
- The objective of the 'append_month_zero' method is to append the baseline values of various attributes
of the animal species to their respective lists. These values will be used as a reference point for future
calculations.

---
Inputs:
- The method takes no external inputs. It uses the instance variables of the class 'AnimalSpecies' to
calculate and append the baseline values.

----


## AnimalPopulation
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L962)
```python 
AnimalPopulation()
```




**Methods:**


### .calculate_additive_births
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L963)
```python
.calculate_additive_births(
   animal, current_month
)
```


### .calculate_change_in_population
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L980)
```python
.calculate_change_in_population(
   animal, country_object, new_additive_animals_month,
   remaining_hours_this_size
)
```

---
This function will calculate the change in animal population for a given animal type
It will do so by calculating the number of new births, the number of deaths, and the number of animals
slaughtered
It will then update the animal object with the new population

It will also update the animal object with the number of animals that are pregnant, and the number of animals
that are lactating

Some parameters are calulctaed before the 'slaughter event' where the populations change, some are calculated
after
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

### .calculate_pregnant_animals_birthing
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L1093)
```python
.calculate_pregnant_animals_birthing(
   animal, new_pregnant_animals_total
)
```

---
This function will calculate the number of pregnant animals birthing this month, based on the number of
pregnant animals remaining
Uses a simple calculation of the number of pregnant animals divided by the gestation period
This is not a perfect calculation, as it assumes that an even distribution of animals will birth each month
However, it is a good approximation for the purposes of this model

Parameters
----------
animal : AnimalSpecies
The animal object for the animal type that you want to calculate the change in population for
---
    The number of pregnant animals remaining this month

Returns
-------
    The number of pregnant animals birthing this month

### .calculate_pregnant_slaughter
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L1119)
```python
.calculate_pregnant_slaughter(
   animal, new_slaughter_rate
)
```

---
This function will determine how many of the animals who died this month were pregnant
Check if the number of pregnant animals set for slaughter is less than the number of animals slaughtered this
month
If so, proceed to calculate the number of pregnant animals slaughtered
Otherwise, set the number of pregnant animals slaughtered to the number of animals slaughtered this month

### .calculate_animal_population
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L1195)
```python
.calculate_animal_population(
   animal, country_object, new_additive_animals_month, new_other_animal_death,
   new_slaughter_rate
)
```


### .calculate_births
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L1245)
```python
.calculate_births(
   animal
)
```

---
This function calculates the number of new births this month

Parameters
----------
animal : object
The animal object that is being calculated

---
Returns
-------
    from milk animals, not total births (meat and milk))
    to meat births from milk animals, not total births (meat and milk))

### .calculate_breeding_changes
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L1276)
```python
.calculate_breeding_changes(
   animal
)
```

---
This function calculates the changes in breeding for the animal type
This is *only* called after the gestation period is over
It will update the animal object with the new number of pregnant animals
Based on the reduction in breeding

Pregnant slaughter is halted, as breeding changes have taken place from the breeding intervention

Parameters
----------
animal : object
The animal object that is being calculated

---
Returns
-------
None

### .calculate_other_deaths
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L1306)
```python
.calculate_other_deaths(
   animal
)
```


### .calculate_slaughter_rate
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L1312)
```python
.calculate_slaughter_rate(
   animal, country_object, new_births_animals_month, new_other_animal_death,
   remaining_hours_this_size
)
```

---
This function calculates the new slaughter rate based on the spare slaughter hours and the target animal
population

Parameters
----------
animal : object
The animal object that is being calculated
---
    The number of spare slaughter hours generated
    The target animal population

Returns
-------
    The new slaughter rate
    The number of spare slaughter hours remaining after the new slaughter rate is calculated

### .calculate_other_death_homekill_head
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L1379)
```python
.calculate_other_death_homekill_head(
   animal, country_object
)
```


### .calculate_healthy_homekill_head
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L1402)
```python
.calculate_healthy_homekill_head(
   animal, country_object
)
```


### .calculate_starving_pop_post_slaughter_healthy_homekill
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L1428)
```python
.calculate_starving_pop_post_slaughter_healthy_homekill(
   animal
)
```


### .calculate_starving_homekill_head
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L1443)
```python
.calculate_starving_homekill_head(
   animal, country_object,
   population_starving_post_slaughter_and_healthy_homekill
)
```


### .calculate_starving_pop_post_all_slaughter_homekill
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L1481)
```python
.calculate_starving_pop_post_all_slaughter_homekill(
   animal, population_starving_post_slaughter_and_healthy_homekill
)
```


### .other_death_pregnant_adjustment
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L1492)
```python
.other_death_pregnant_adjustment(
   animal
)
```


### .calculate_starving_other_death_head
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L1532)
```python
.calculate_starving_other_death_head(
   animal, population_starving_post_slaughter_and_all_homekill
)
```

---
This function calculates the number of animals that die from starvation in a month.

It takes the population of animals that are starving after slaughter and homekill, and calculates the number
of animals that die from starvation.
In terms of physical relevance - the animals that don't die from starvation are the ones that are able to find
enough other food to survive or have fat stores etc.
These animals ARE NOT turned in to meat.
Those that are turned in to meat are captured in the homekill functions.


Parameters
----------
animal : Animal
The animal object that is being calculated for.
---
    The number of animals that are starving after slaughter and homekill.

Returns
-------
float
    The number of animals that die from starvation in a month.

### .calculate_final_population
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L1565)
```python
.calculate_final_population(
   animal
)
```

---
This function calculates the final population of the animal after all the slaughter and homekill has been done.

Parameters
----------
animal : Animal
The animal object that is being calculated for.

---
Returns
-------
float
    The final population of the animal.

### .feed_animals
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L1595)
```python
.feed_animals(
   animal_list, ruminants, available_feed, available_grass
)
```

---
This function will feed the animals
It will do so by allocating the grass first to those animals that can eat it,
and then allocating the remaining feed to the remaining animals

It will also priotiise the animals that are most efficient at converting feed,
This means starting with milk.

List needs to be sorted in the oprder you want the animals to be prioritised for feed

### .calculate_starving_animals_after_feed
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L1620)
```python
.calculate_starving_animals_after_feed(
   animal_list
)
```

---
This function will calculate the number of animals that are starving after feeding
It iterates through the animal list and calculates the number of animals that are starving
result is appended to the animal object

### .set_current_populations
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L1631)
```python
.set_current_populations(
   animal_objects
)
```

---
Sets the current population of each animal object
This simply sets the current population to the value at the end of the previous month.
This value is then updated during the month loop.
Runs at the start opf the month before any changes to population are made.

### .appened_current_populations
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L1653)
```python
.appened_current_populations(
   animal_objects
)
```

---
Appends the current population of each animal object to its population list.
Runs at the end of the month loop once currrent population has been updated


**Args**

* **animal_objects** (_type_) : _description_


----


## AnimalDataReader
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L1666)
```python 
AnimalDataReader()
```




**Methods:**


### .read_animal_population_data
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L1667)
```python
.read_animal_population_data(
   filename
)
```

---
Read animal population data from CSV file

Returns
-------
df_animal_stock_info : pandas dataframe
Dataframe containing animal population data

### .read_animal_nutrition_data
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L1693)
```python
.read_animal_nutrition_data(
   filename
)
```

---
"
Read animal nutrition data from CSV file

Returns
-------
df_animal_nutrition : pandas dataframe
Dataframe containing animal nutrition data

### .read_animal_options
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L1718)
```python
.read_animal_options(
   filename
)
```

---
"
Read animal nutrition data from CSV file

Returns
-------
df_animal_nutrition : pandas dataframe
Dataframe containing animal nutrition data

### .read_animal_regional_factors
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L1739)
```python
.read_animal_regional_factors(
   filename
)
```

---
"
Read animal nutrition data from CSV file

Returns
-------
df_animal_nutrition : pandas dataframe
Dataframe containing animal nutrition data

### .read_country_data
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L1760)
```python
.read_country_data(
   filename
)
```

---
"
Read animal nutrition data from CSV file

Returns
-------
df_animal_nutrition : pandas dataframe
Dataframe containing animal nutrition data

----


## AnimalModelBuilder
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L1782)
```python 
AnimalModelBuilder()
```




**Methods:**


### .create_animal_objects
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L1783)
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

### .get_optimal_next_animal_to_feed
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L1869)
```python
.get_optimal_next_animal_to_feed(
   animal_dict, kcals_per_head_meat_dict, df_animal_attributes
)
```


### .update_animal_objects_with_slaughter
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L2071)
```python
.update_animal_objects_with_slaughter(
   animal_list, df_animal_attributes, df_animal_options, scenario,
   kcals_per_head_meat_dict
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

### .update_animal_objects_with_milk
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L2176)
```python
.update_animal_objects_with_milk(
   animal_list, df_animal_attributes
)
```

---
This function updates the animal objects with the slaughter data.

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

### .update_animal_objects_LSU_factor
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L2220)
```python
.update_animal_objects_LSU_factor(
   animal_list, country_object
)
```

---
This function updates the animal objects with the LSU factors

Parameters
----------
animal_list : list
List of animal objects
---
    Object containing country data

Returns
-------
    List of animal objects

### .remove_first_month
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L2242)
```python
.remove_first_month(
   animal
)
```


----


## Debugging
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L2250)
```python 
Debugging()
```




**Methods:**


### .print_list_lengths
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L2251)
```python
.print_list_lengths(
   obj
)
```


### .save_single_animal_data_to_csv
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L2259)
```python
.save_single_animal_data_to_csv(
   animal, output_path = 'animal_single_data_to_csv.csv'
)
```


### .print_list_any
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L2306)
```python
.print_list_any(
   animal_list
)
```


### .available_feed_function
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L2370)
```python
.available_feed_function(
   billion_kcals, months_to_run = 120
)
```

---
Energy is expressed as digestible (DE), metabolizable (ME), or net energy (NE) by considering the loss of
energy during digestion and metabolism from gross energy (GE) in the feed, as follows:

Gross energy (GE): the amount of energy in the feed.
Digestible energy (DE): the amount of energy in the feed minus the amount of energy lost in the feces.
Metabolizable energy (ME): the amount of energy in the feed minus the energy lost in the feces and urine.
Net energy (NE): the amount of energy in the feed minus the energy lost in the feces, urine, and in heat
production through digestive and metabolic processes, i.e. heat increment.

### .available_grass_function
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L2402)
```python
.available_grass_function(
   billion_kcals, months_to_run = 120
)
```

---
### CHECK IS BILLION KCALS

Energy is expressed as digestible (DE), metabolizable (ME), or net energy (NE) by considering the loss of energy
during digestion and metabolism from gross energy (GE) in the feed, as follows:

Gross energy (GE): the amount of energy in the feed. Digestible energy (DE): the amount of energy in the feed
minus the amount of energy lost in the feces. Metabolizable energy (ME): the amount of energy in the feed minus
the energy lost in the feces and urine. Net energy (NE): the amount of energy in the feed minus the energy lost
in the feces, urine, and in heat production through digestive and metabolic processes, i.e. heat increment.

----


### calculate_net_slaughter_hours_by_size
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L2438)
```python
.calculate_net_slaughter_hours_by_size(
   animals
)
```

---
@author: DMR
This function gets the total hours in the relevant size (small, medium, or large) which can be used to slaughter
animals of that size

----


### world_test
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L2814)
```python
.world_test()
```

---
Test the animal population model for the case with full-trade by including worldwide aggregated
feed and grass supply.
