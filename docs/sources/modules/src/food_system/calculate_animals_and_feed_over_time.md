#


## CalculateAnimalOutputs
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/calculate_animals_and_feed_over_time.py/#L50)
```python 

```


---
import relevant data as dataframes and assign as properties of this class


**Methods:**


### .calculate_country_specific_per_species_feed_consumption
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/calculate_animals_and_feed_over_time.py/#L60)
```python
.calculate_country_specific_per_species_feed_consumption(
   country_code, feed_ratio
)
```

---
This function is used to calculate the total feed usage for a country

feed_ratio is a fraction from 0 to 1 which scales the default input feed per
month to a lower value. This is used to account for scenarios where the feed
is more than could possibly be supplied in the scenario.

### .calculate_feed_and_animals
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/calculate_animals_and_feed_over_time.py/#L174)
```python
.calculate_feed_and_animals(
   data
)
```

---
This function calculates the feed and animal populations for a given country
Parameters
----------
data : dict
Dictionary containing the country code and the animal populations
---
Returns
-------
    species

### .calculate_animal_populations
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/calculate_animals_and_feed_over_time.py/#L244)
```python
.calculate_animal_populations(
   data
)
```

---
Inputs:
reduction_in_beef_calves: Reduction in Beef Birth Rate
reduction_in_dairy_calves: Reduction in Dairy Birth Rate
increase_in_slaughter: So 20% indicates an 80% drop in baseline sluaghter rates
in slaughterhouses
reduction_in_pig_breeding: Reduction Pig Breeding
100(=100% reduction) means that all insemination and breeding stops on day 0 (
with the corresponding drop in birth rate happening 9 months later for cows, 1
 month for chickens, 4 months pigs (as per gestation variables))
reduction_in_poultry_breeding: Reduction Poultry Breeding
months: Months to simulate
discount_rate: discount_rate: Discount Rate for Labour/Technology Transfer
between species
mother_slaughter: Proportion of Slaughter which is mothers
(In a normal slaughtering regime pregnant animals are not killed.
mother_slaughter is a percentage of how much of the slaughtering capacity
will be used on pregnant animals.)
use_grass_and_residues_for_dairy: Whether to Use Residues for Dairy
