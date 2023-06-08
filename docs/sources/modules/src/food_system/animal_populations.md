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
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L155)
```python
.set_species_milk_attributes(
   productive_milk_age_start, productive_milk_age_end,
   milk_production_per_month = None
)
```

---
Sets milk-related attributes for a given species of animal.


**Args**

* **productive_milk_age_start** (int) : The age at which an animal starts producing milk.
* **productive_milk_age_end** (int) : The age at which an animal stops producing milk.
* **milk_production_per_month** (float, optional) : The amount of milk produced per month by the animal. Defaults to None.


**Returns**

None


**Example**


```python

>>> cow.set_species_milk_attributes(2, 5, 50.0)
```

### .retiring_milk_head_monthly
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L200)
```python
.retiring_milk_head_monthly()
```

---
Calculates the number of retiring milk animals per month based on the fraction of retiring milk animals
in the population.


**Args**

* **self** (object) : An instance of the class containing the population and fraction of retiring milk animals.


**Returns**

* **float**  : The number of retiring milk animals per month.


**Example**


```python

>>> farm.retiring_milk_head_monthly()
10.0
```

### .set_species_slaughter_attributes
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L220)
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


**Args**

* **gestation** (int) : gestation period in months
* **other_animal_death_rate_annual** (float) : annual death rate of animals
* **animals_per_pregnancy** (int) : number of animals per pregnancy
* **animal_slaughter_hours** (int) : hours per animal spent slaughtering
* **change_in_slaughter_rate** (float) : change in slaughter rate (a static value, given by assumptions of loss of industry etc...)
* **pregnant_animal_slaughter_fraction** (float) : this is the fraction of pregnant animals that are attempted to be slaughtered each month
* **reduction_in_animal_breeding** (float) : this is the reduction in animal breeding (a static value, given by assumptions of loss of industry etc...)
* **target_population_fraction** (float) : this is the target population fraction (a static value, given by assumptions of loss of industry etc...)
* **transfer_births_or_head** (int) : this is head of increased population due to either male offspring of milk animals being added toa meat population or head imported from other countries


**Returns**

None

---
Description:
    This function sets the attributes of the animal species that are related to slaughter. It takes in various parameters and calculates the values of different attributes based on them.

### .exported_births
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L309)
```python
.exported_births()
```

---
Calculates the number of births exported from the animal population.


**Args**

None


**Returns**

* **exported_births** (int) : the number of births exported from the animal population

---
Explanation:
    This function calculates the number of births exported from the animal population
    by multiplying the number of births per month by the birth ratio minus 1.


**Example**

If the animal population has 100 births per month and a birth ratio of 2, then
the number of exported births would be 100 * (2-1) = 100.

### .net_energy_required_per_month
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L333)
```python
.net_energy_required_per_month()
```

---
Calculates the net energy required per month for a given feed and livestock unit (LSU).
The calculation is based on the method described in the article "Livestock unit calculation: a method based on energy requirements to refine the study of livestock farming systems" by NRAE Prod. Anim., 2021, 34 (2), 139e-160e.

**Args**

* **self** (object) : An instance of the class containing the feed and LSU information.


**Returns**

* **float**  : The net energy required per month in billion kcal for the given feed and LSU.


### .feed_required_per_month_individual
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L356)
```python
.feed_required_per_month_individual()
```

---
Calculates the total feed required for this month for the species.
The function uses the net energy required per month function and the digestion efficiency to calculate the total feed.

**Args**

* **self**  : an instance of the Animal class


**Returns**

* **Food**  : an instance of the Food class representing the total feed required for the species for this month.
      The instance contains the following attributes:
      - kcal: billion kcals
      - fat: thousand tons monthly fat (default value of -1)
      - protein: thousand tons monthly protein (default value of -1)


### .feed_required_per_month_species
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L375)
```python
.feed_required_per_month_species()
```

---
Calculates the total feed required for this month for the species.
The function uses the net energy required per month function and the digestion efficiency to calculate the feed.

**Args**

* **self**  : an instance of the Animal class


**Returns**

* **Food**  : an instance of the Food class representing the total feed required for the species for this month.
      The instance contains the following attributes:
      - kcal: billion kcals
      - fat: thousand tons monthly fat
      - protein: thousand tons monthly protein


### .feed_the_species
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L403)
```python
.feed_the_species(
   food_input
)
```

---
Feeds the species with the given food input and updates the feed balance and population fed/starving accordingly.

**Args**

* **food_input** (Food) : The food object containing the amount of kcals, fat, and protein to feed the species.


**Returns**

* **Food**  : The remaining food object after feeding the species.


**Example**


```python

>>> species = Species('lion', 10, Food(500, 25, 10))
>>> remaining_food = species.feed_the_species(food)
```

----


### read_animal_population_data
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L478)
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
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L508)
```python
.read_animal_nutrition_data()
```

---
Reads animal nutrition data from CSV file and returns a pandas dataframe.

Returns
-------
df_animal_nutrition : pandas dataframe
Dataframe containing animal nutrition data

---
Raises
------
FileNotFoundError
    If the CSV file containing animal nutrition data is not found.

----


### read_animal_options
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L549)
```python
.read_animal_options()
```

---
Read animal nutrition data from CSV file

Returns
-------
df_animal_nutrition : pandas dataframe
Dataframe containing animal nutrition data

----


### create_animal_objects
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L578)
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
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L646)
```python
.update_animal_objects_with_slaughter(
   animal_list, df_animal_attributes, df_animal_options
)
```

---
This function updates the animal objects with the slaughter data


**Args**

* **animal_list** (list) : List of animal objects
* **df_animal_attributes** (pandas dataframe) : Dataframe containing animal attibute data
* **df_animal_options** (pandas dataframe) : Dataframe containing animal options data


**Returns**

* **list**  : List of animal objects

---
This function updates the animal objects with the slaughter data by setting the species slaughter attributes
for each animal in the animal_list.

The function loops through the dict of animal objects and sets the species slaughter attributes for each animal
using the data from the df_animal_attributes and df_animal_options dataframes.


**Args**

* **animal** (Animal) : An animal object from the animal_list


----


### update_animal_objects_with_milk
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L708)
```python
.update_animal_objects_with_milk(
   animal_list, df_animal_attributes
)
```

---
This function updates the animal objects with the milk production data.


**Args**

* **animal_list** (list) : List of animal objects.
* **df_animal_attributes** (pandas dataframe) : Dataframe containing animal attribute data.


**Returns**

* **animal_list** (list) : List of animal objects updated with milk production data.


----


### available_feed
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L742)
```python
.available_feed()
```

---
This function imports feed data from a model and calculates the available feed for animals.
Energy is expressed as digestible (DE), metabolizable (ME), or net energy (NE) by considering the loss of energy during digestion and metabolism from gross energy (GE) in the feed, as follows:

Gross energy (GE): the amount of energy in the feed.
Digestible energy (DE): the amount of energy in the feed minus the amount of energy lost in the feces.
Metabolizable energy (ME): the amount of energy in the feed minus the energy lost in the feces and urine.
Net energy (NE): the amount of energy in the feed minus the energy lost in the feces, urine, and in heat production through digestive and metabolic processes, i.e. heat increment.


**Args**

None


**Returns**

* **Food**  : A Food object representing the available feed for animals.


**Example**

>>> available_feed()
<Food object at 0x7f8d5c6d7c50>

----


### available_grass
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L780)
```python
.available_grass()
```

---
Calculates the amount of available grass as animal feed in kcal.
Energy is expressed as digestible (DE), metabolizable (ME), or net energy (NE) by considering the loss of energy during digestion and metabolism from gross energy (GE) in the feed, as follows:

Gross energy (GE): the amount of energy in the feed.
Digestible energy (DE): the amount of energy in the feed minus the amount of energy lost in the feces.
Metabolizable energy (ME): the amount of energy in the feed minus the energy lost in the feces and urine.
Net energy (NE): the amount of energy in the feed minus the energy lost in the feces, urine, and in heat production through digestive and metabolic processes, i.e. heat increment.

----


### feed_animals
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L802)
```python
.feed_animals(
   animal_list, milk_animals, non_milk_ruminants, non_milk_animals,
   available_feed, available_grass
)
```

---
This function feeds the animals in the farm by allocating the grass first to those animals that can eat it,
and then allocating the remaining feed to the remaining animals. It prioritizes the animals that are most efficient
at converting feed, starting with milk.


**Args**

* **animal_list** (list) : A list of all the animals in the farm
* **milk_animals** (list) : A list of all the milk-producing animals in the farm
* **non_milk_ruminants** (list) : A list of all the non-milk-producing ruminant animals in the farm
* **non_milk_animals** (list) : A list of all the non-milk-producing non-ruminant animals in the farm
* **available_feed** (int) : The amount of feed available to be distributed
* **available_grass** (int) : The amount of grass available to be distributed


**Returns**

* **tuple**  : A tuple containing the remaining available feed and grass after distribution


**Example**


```python

>>> goat = MilkAnimal('goat', 50, 5)
>>> sheep = NonMilkRuminant('sheep', 75, 7)
>>> pig = NonMilkNonRuminant('pig', 80, 8)
>>> animal_list = [cow, goat, sheep, pig]
>>> milk_animals = [cow, goat]
>>> non_milk_ruminants = [sheep]
>>> non_milk_animals = [pig]
>>> available_feed = 1000
>>> available_grass = 500
>>> feed_animals(animal_list, milk_animals, non_milk_ruminants, non_milk_animals, available_feed, available_grass)
(0, 0)
```

----


### calculate_additive_births
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L859)
```python
.calculate_additive_births(
   animal_object, current_month
)
```

---
Calculates the number of new animals born this month given the number of pregnant animals.
If breeding intervention has kicked in, the reduction in breeding is taken into account for new births.

**Args**

* **animal_object** (Animal) : an instance of the Animal class containing information about the animal population
* **current_month** (int) : the current month of the simulation


**Returns**

* **tuple**  : a tuple containing the number of new animals born this month and the number of new export births


----


### calculate_change_in_population
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L883)
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

Some parameters are calculated before the 'slaughter event' where the populations change, some are calculated after
Those that are calculated before are:
- the new births this month (based on the number of animals that are pregnant)
- other deaths this month
- the slaughter rate this month
- spare slaughter hours this month
---
Those that are calculated after are:
    - the number of animals that are lactating
    - the new population this month
    - the population of animals that are pregnant for next month


**Args**

* **animal_object** (Animal) : an instance of the Animal class
* **spare_slaughter_hours** (float) : the number of slaughter hours left over from the previous month
* **new_additive_animals_month** (int) : the number of new animals added to the population this month


**Returns**

* **float**  : the number of slaughter hours left over after the calculations have been made


**Example**


```python

>>> spare_slaughter_hours = 10.0
>>> new_additive_animals_month = 5
>>> calculate_change_in_population(animal_object, spare_slaughter_hours, new_additive_animals_month)
0.0
```

----


### calculate_pregnant_animals_birthing
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L993)
```python
.calculate_pregnant_animals_birthing(
   animal_object, new_pregnant_animals_total
)
```

---
Calculates the number of pregnant animals birthing this month, based on the number of pregnant animals remaining.
Uses a simple calculation of the number of pregnant animals divided by the gestation period.
This is not a perfect calculation, as it assumes that an even distribution of animals will birth each month.
However, it is a good approximation for the purposes of this model.


**Args**

* **animal_object** (AnimalSpecies) : The animal object for the animal type that you want to calculate the change in population for.
* **new_pregnant_animals_total** (int) : The number of pregnant animals remaining this month.


**Returns**

* **int**  : The number of pregnant animals birthing this month.


----


### calculate_pregnant_slaughter
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L1017)
```python
.calculate_pregnant_slaughter(
   animal_object, new_slaughter_rate
)
```

---
This function calculates the number of pregnant animals that were slaughtered in a given month.


**Args**

* **animal_object** (object) : An object containing information about the animal population.
* **new_slaughter_rate** (float) : The number of animals slaughtered in the current month.


**Returns**

* **tuple**  : A tuple containing the new total number of pregnant animals and the number of pregnant animals slaughtered.


----


### calculate_animal_population
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L1061)
```python
.calculate_animal_population(
   animal_object, new_births_animals_month, new_other_animal_death,
   new_slaughter_rate
)
```

---
Calculates the new animal population based on the previous population, new births, deaths, and slaughter rate.

**Args**

* **animal_object** (Animal) : an object representing the animal population
* **new_births_animals_month** (int) : the number of new births in a month
* **new_other_animal_death** (int) : the number of deaths from other causes in a month
* **new_slaughter_rate** (int) : the number of animals slaughtered in a month


**Returns**

* **int**  : the new animal population after accounting for births, deaths, and slaughter rate


----


### calculate_retiring_milk_animals
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L1095)
```python
.calculate_retiring_milk_animals(
   animal_object
)
```

---
This function calculates the number of animals retiring from milk production this month


**Args**

* **animal_object** (object) : The animal object that is being calculated


**Returns**

* **int**  : The number of animals retiring from milk production this month


----


### calculate_births
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L1116)
```python
.calculate_births(
   animal_object
)
```

---
This function calculates the number of new births this month


**Args**

* **animal_object** (object) : The animal object that is being calculated


**Returns**

* **tuple**  : A tuple containing two integers:
    - new_births_animals_month: The number of new births this month
    - new_export_births_animals_month: The number of new export births this month (optional)


**Raises**

None


**Example**


```python

>>> calculate_births(cow)
(10, 0)
```

----


### calculate_breeding_changes
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L1154)
```python
.calculate_breeding_changes(
   animal_object
)
```

---
Calculates changes in animal breeding based on the reduction in animal breeding rate.

**Args**

* **animal_object** (Animal) : An instance of the Animal class containing information about the animal population.


**Returns**

None


**Example**


```python

>>> calculate_breeding_changes(animal)
```

----


### calculate_other_deaths
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L1185)
```python
.calculate_other_deaths(
   animal_object
)
```

---
Calculates the number of deaths of animals due to factors other than predation or birth.

**Args**

* **animal_object** (Animal) : An instance of the Animal class containing the population and other_animal_death_rate_monthly attributes.


**Returns**

* **float**  : The number of deaths due to other factors.


----


### calculate_slaughter_rate
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/animal_populations.py/#L1202)
```python
.calculate_slaughter_rate(
   animal_object, spare_slaughter_hours, target_animal_population,
   new_births_animals_month, new_other_animal_death
)
```

---
This function calculates the new slaughter rate based on the spare slaughter hours and the target animal population


**Args**

* **animal_object** (object) : The animal object that is being calculated
* **spare_slaughter_hours** (int) : The number of spare slaughter hours generated
* **target_animal_population** (int) : The target animal population
* **new_births_animals_month** (int) : The number of new births of animals per month
* **new_other_animal_death** (int) : The number of deaths of other animals per month


**Returns**

* **new_slaughter_rate** (int) : The new slaughter rate
* **spare_slaughter_hours** (int) : The number of spare slaughter hours remaining after the new slaughter rate is calculated

