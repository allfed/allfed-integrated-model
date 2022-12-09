#


## CalculateAnimalOutputs
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/calculate_animals_and_feed_over_time.py/#L22)
```python 

```




**Methods:**


### .calculate_feed_and_animals_using_baseline_feed_usage
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/calculate_animals_and_feed_over_time.py/#L26)
```python
.calculate_feed_and_animals_using_baseline_feed_usage(
   reduction_in_beef_calves, reduction_in_dairy_calves, increase_in_slaughter,
   reduction_in_pig_breeding, reduction_in_poultry_breeding, months,
   discount_rate, mother_slaughter, use_grass_and_residues_for_dairy,
   baseline_kcals_per_month_feed
)
```

---
the way this function works, is it first calculates the expected feed tons in
 baseline conditions, and compares it to known feed calories in baseline, and
uses this information to determine the caloric density of feed

then it calculates the feed usage for the actual scenario.

### .calculate_feed_and_animals
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/calculate_animals_and_feed_over_time.py/#L67)
```python
.calculate_feed_and_animals(
   reduction_in_beef_calves, reduction_in_dairy_calves, increase_in_slaughter,
   reduction_in_pig_breeding, reduction_in_poultry_breeding, months,
   discount_rate, mother_slaughter, use_grass_and_residues_for_dairy,
   tons_to_kcals
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

tons_to_kcals: calories per ton of feed

----


## ModelAnimalInputs
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/calculate_animals_and_feed_over_time.py/#L491)
```python 
ModelAnimalInputs(
   dataframe
)
```


