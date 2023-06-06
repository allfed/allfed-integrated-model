#


## Scenarios
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L12)
```python 

```




**Methods:**


### .check_all_set
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L38)
```python
.check_all_set()
```

---
Check that all properties of scenarios have been set.

**Raises**

* **AssertionError**  : If any of the properties have not been set.


### .init_generic_scenario
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L62)
```python
.init_generic_scenario()
```

---
Initializes the constants for the generic scenario.


**Args**

* **self**  : The object instance.


**Returns**

* **dict**  : A dictionary containing the constants for the generic scenario.


### .init_global_food_system_properties
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L100)
```python
.init_global_food_system_properties()
```


### .init_country_food_system_properties
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L332)
```python
.init_country_food_system_properties(
   country_data
)
```

---
Initializes the food system properties for a given country.


**Args**

* **self**  : instance of the class
* **country_data** (dict) : a dictionary containing data for the country


**Returns**

* **dict**  : a dictionary containing constants for the parameters


**Raises**

* **AssertionError**  : if any of the assertions fail


### .set_immediate_shutoff
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L579)
```python
.set_immediate_shutoff(
   constants_for_params
)
```

---
Sets the immediate shutoff of feed and biofuel consumption in the simulation.


**Args**

* **constants_for_params** (dict) : A dictionary containing the simulation parameters.


**Returns**

* **dict**  : The updated dictionary of simulation parameters.


**Raises**

* **AssertionError**  : If the NONHUMAN_CONSUMPTION_SET flag is already set.


### .set_short_delayed_shutoff
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L611)
```python
.set_short_delayed_shutoff(
   constants_for_params
)
```

---
Sets a delayed shutoff for feed and biofuel consumption in the simulation.


**Args**

* **constants_for_params** (dict) : A dictionary containing the simulation parameters.


**Returns**

* **dict**  : The updated dictionary of simulation parameters.


**Raises**

* **AssertionError**  : If NONHUMAN_CONSUMPTION_SET is already True.

---
Scenario Description:
    Adds a description of the scenario to the simulation's scenario_description attribute.

### .set_long_delayed_shutoff
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L645)
```python
.set_long_delayed_shutoff(
   constants_for_params
)
```

---
Sets a long delayed shutoff for feed and biofuel consumption.


**Args**

* **constants_for_params** (dict) : A dictionary of constants for the parameters.


**Returns**

* **dict**  : The updated dictionary of constants for the parameters.


### .reduce_breeding
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L674)
```python
.reduce_breeding(
   constants_for_params
)
```

---
This function reduces breeding/biofuel and sets the delay for feed and biofuel shutoff.

**Args**

* **self**  : instance of the class
* **constants_for_params** (dict) : dictionary containing the parameters for the simulation


**Returns**

* **dict**  : updated dictionary containing the parameters for the simulation


### .set_continued_feed_biofuels
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L713)
```python
.set_continued_feed_biofuels(
   constants_for_params
)
```

---
Sets the parameters for continued feed/biofuel production strategy and updates the scenario description.

**Args**

* **constants_for_params** (dict) : A dictionary containing the parameters for the simulation.


**Returns**

* **dict**  : A dictionary containing the updated parameters for the simulation.


**Raises**

* **AssertionError**  : If there is no food storage, then feed and biofuels when no food is being
* **AssertionError**  : If stored food is not assigned before setting biofuels.
stored would not make any sense, as the total food available could go negative.

### .set_unchanged_proportions_feed_grazing
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L759)
```python
.set_unchanged_proportions_feed_grazing(
   constants_for_params
)
```

---
This function sets the unchanged proportions of feed to grazing for a given scenario.

**Args**

* **self**  : instance of the class
* **constants_for_params** (dict) : dictionary containing the constants for the parameters


**Returns**

* **dict**  : updated dictionary containing the constants for the parameters


### .set_efficient_feed_grazing_strategy
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L783)
```python
.set_efficient_feed_grazing_strategy(
   constants_for_params
)
```

---
This function sets the efficient feed grazing strategy for dairy cows by updating the constants_for_params dictionary.
It also updates the scenario_description attribute of the object to reflect the change in strategy.


**Args**

* **self**  : the object instance
* **constants_for_params** (dict) : a dictionary containing the parameters for the simulation


**Returns**

* **dict**  : the updated constants_for_params dictionary


**Raises**

* **AssertionError**  : if the meat strategy has already been set


### .set_feed_based_on_livestock_levels
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L814)
```python
.set_feed_based_on_livestock_levels(
   constants_for_params
)
```

---
Sets the feed based on breeding patterns. This function is not really necessary, but it keeps the pattern I guess.

**Args**

* **self**  : instance of the class
* **constants_for_params** (dict) : dictionary containing the constants for the parameters


**Returns**

* **dict**  : dictionary containing the updated constants for the parameters


### .set_excess_to_zero
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L839)
```python
.set_excess_to_zero(
   constants_for_params
)
```

---
Sets the excess feed percentage to zero for all months in the constants_for_params dictionary.
This function should only be called once, as indicated by the EXCESS_SET attribute.


**Args**

* **constants_for_params** (dict) : A dictionary containing the parameters for the simulation.


**Returns**

* **dict**  : The modified constants_for_params dictionary with the excess feed percentage set to zero.


**Raises**

* **AssertionError**  : If the EXCESS_SET attribute is already True, indicating that this function has already been called.


### .set_excess
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L867)
```python
.set_excess(
   constants_for_params, excess
)
```


### .set_waste_to_zero
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L876)
```python
.set_waste_to_zero(
   constants_for_params
)
```

---
Sets the waste percentage for all food types to zero.


**Args**

* **constants_for_params** (dict) : A dictionary containing the constants for the simulation.


**Returns**

* **dict**  : The updated dictionary of constants for the simulation.


**Raises**

* **AssertionError**  : If the waste has already been set.


### .get_total_global_waste
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L911)
```python
.get_total_global_waste(
   retail_waste
)
```

---
Calculates the total waste of the global food system by adding retail waste
to distribution loss.


**Args**

* **retail_waste** (float) : The amount of waste generated at the retail level.


**Returns**

* **dict**  : A dictionary containing the total waste for each food category.


**Raises**

* **AssertionError**  : If the analysis is not global.


### .set_global_waste_to_tripled_prices
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L949)
```python
.set_global_waste_to_tripled_prices(
   constants_for_params
)
```

---
Sets the global waste to tripled prices and updates the constants_for_params dictionary.


**Args**

* **self**  : the instance of the class
* **constants_for_params** (dict) : a dictionary containing the constants for the simulation


**Returns**

* **dict**  : the updated constants_for_params dictionary


**Raises**

* **AssertionError**  : if IS_GLOBAL_ANALYSIS is False or WASTE_SET is True


### .set_global_waste_to_doubled_prices
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L989)
```python
.set_global_waste_to_doubled_prices(
   constants_for_params
)
```

---
Sets the global waste to double the prices of 2019. This includes overall waste, on farm, distribution, and retail.

**Args**

* **self**  : instance of the class
* **constants_for_params** (dict) : dictionary containing the constants for the parameters


**Returns**

* **dict**  : updated dictionary containing the constants for the parameters


**Raises**

* **AssertionError**  : if WASTE_SET is True or IS_GLOBAL_ANALYSIS is False


### .set_global_waste_to_baseline_prices
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L1022)
```python
.set_global_waste_to_baseline_prices(
   constants_for_params
)
```

---
Sets the global waste to baseline prices for on farm, distribution, and retail.

**Args**

* **self**  : instance of the class
* **constants_for_params** (dict) : dictionary containing the constants for the parameters


**Returns**

* **dict**  : updated dictionary containing the constants for the parameters


### .get_total_country_waste
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L1053)
```python
.get_total_country_waste(
   retail_waste, country_data
)
```

---
Calculates the total waste of the global food system by adding retail waste
to distribution loss.


**Args**

* **retail_waste** (float) : The amount of waste generated at the retail level
* **country_data** (dict) : A dictionary containing the distribution loss data for
different food categories


**Returns**

* **dict**  : A dictionary containing the total waste for different food categories


**Raises**

* **AssertionError**  : If the analysis is global


### .set_country_waste_to_tripled_prices
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L1093)
```python
.set_country_waste_to_tripled_prices(
   constants_for_params, country_data
)
```

---
Sets the overall waste, on farm + distribution + retail, to 3x prices (note, currently set to 2019, not 2020).

**Args**

* **self**  : instance of the class
* **constants_for_params** (dict) : dictionary containing the constants for the parameters
* **country_data** (dict) : dictionary containing the data for the country


**Returns**

* **dict**  : updated dictionary containing the constants for the parameters


### .set_country_waste_to_doubled_prices
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L1127)
```python
.set_country_waste_to_doubled_prices(
   constants_for_params, country_data
)
```

---
Sets the country's waste to double the retail price and updates the constants_for_params dictionary accordingly.

**Args**

* **self**  : instance of the class
* **constants_for_params** (dict) : dictionary containing the constants for the model
* **country_data** (dict) : dictionary containing the data for the country


**Returns**

* **dict**  : updated constants_for_params dictionary


### .set_country_waste_to_baseline_prices
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L1159)
```python
.set_country_waste_to_baseline_prices(
   constants_for_params, country_data
)
```

---
Sets the waste for a country to baseline prices for on-farm, distribution, and retail.

**Args**

* **self**  : instance of the class
* **constants_for_params** (dict) : dictionary of constants for the model
* **country_data** (dict) : dictionary of data for the country


**Returns**

* **dict**  : updated dictionary of constants for the model


### .set_baseline_nutrition_profile
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L1191)
```python
.set_baseline_nutrition_profile(
   constants_for_params
)
```

---
Sets the baseline nutrition profile for the scenario.


**Args**

* **constants_for_params** (dict) : A dictionary containing the constants for the scenario.


**Returns**

* **dict**  : The updated dictionary of constants for the scenario.


**Raises**

* **AssertionError**  : If the nutrition profile has already been set.


### .set_catastrophe_nutrition_profile
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L1229)
```python
.set_catastrophe_nutrition_profile(
   constants_for_params
)
```

---
Sets the minimum sufficient nutrition profile for a catastrophe scenario.


**Args**

* **constants_for_params** (dict) : A dictionary containing the constants for the scenario.


**Returns**

* **dict**  : The updated dictionary of constants for the scenario.


**Raises**

* **AssertionError**  : If the nutrition profile has already been set.


### .set_no_stored_food
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L1267)
```python
.set_no_stored_food(
   constants_for_params
)
```

---
This function sets the stored food between years as zero. It assumes that no food is traded between the
12 month intervals seasons. This makes more sense if seasonality is assumed zero.

However, in reality food in transit and food in grocery stores and
warehouses means there would still likely be some food available at
the end as a buffer.


**Args**

* **self**  : instance of the class
* **constants_for_params** (dict) : dictionary containing the parameters for the simulation


**Returns**

* **dict**  : updated dictionary containing the parameters for the simulation


### .set_stored_food_buffer_zero
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L1299)
```python
.set_stored_food_buffer_zero(
   constants_for_params
)
```

---
Sets the stored food buffer as zero -- no stored food left at
the end of the simulation.

However, in reality food in transit and food in grocery stores and
warehouses means there would still likely be some food available at
the end as a buffer.


**Args**

* **constants_for_params** (dict) : A dictionary containing the constants for the simulation.


**Returns**

* **dict**  : A dictionary containing the updated constants for the simulation.


**Raises**

* **AssertionError**  : If the stored food buffer has already been set.


### .set_stored_food_buffer_as_baseline
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L1334)
```python
.set_stored_food_buffer_as_baseline(
   constants_for_params
)
```

---
Sets the stored food buffer as 100% -- the typical stored food buffer
in ~2020 left at the end of the simulation.


**Args**

* **self**  : instance of the class
* **constants_for_params** (dict) : dictionary containing the parameters for the simulation


**Returns**

* **dict**  : updated dictionary containing the parameters for the simulation


**Raises**

* **AssertionError**  : if the stored food buffer has already been set


### .set_no_seasonality
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L1366)
```python
.set_no_seasonality(
   constants_for_params
)
```

---
Sets the seasonality of the scenario to be constant throughout the year.

**Args**

* **constants_for_params** (dict) : A dictionary containing the constants for the scenario.


**Returns**

* **dict**  : A dictionary containing the updated constants for the scenario.


### .set_global_seasonality_baseline
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L1391)
```python
.set_global_seasonality_baseline(
   constants_for_params
)
```

---
Sets the global seasonality baseline for the crop production model.


**Args**

* **constants_for_params** (dict) : A dictionary containing the constants for the crop production model.


**Returns**

* **dict**  : A dictionary containing the updated constants for the crop production model.


**Raises**

* **AssertionError**  : If the global analysis flag is not set or if seasonality has already been set.


### .set_global_seasonality_nuclear_winter
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L1436)
```python
.set_global_seasonality_nuclear_winter(
   constants_for_params
)
```

---
Sets the seasonality for a global analysis in the event of a nuclear winter.
The seasonality is set to typical in the tropics, where most food is grown.

**Args**

* **self**  : instance of the class
* **constants_for_params** (dict) : dictionary containing the constants for the parameters


**Returns**

* **dict**  : dictionary containing the updated constants for the parameters


### .set_country_seasonality
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L1475)
```python
.set_country_seasonality(
   constants_for_params, country_data
)
```

---
Sets the seasonal crop production for a given country based on the data provided.
This function sets the seasonal crop production for a given country based on the data provided.
It sets the fractional production per month and updates the scenario description.

**Args**

* **constants_for_params** (dict) : A dictionary containing the constants for the model.
* **country_data** (dict) : A dictionary containing the data for the country.


**Returns**

* **dict**  : A dictionary containing the updated constants for the model.


### .set_grasses_baseline
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L1501)
```python
.set_grasses_baseline(
   constants_for_params
)
```

---
Sets the baseline grazing for the simulation by setting the ratio of grasses to 1 for each year in the simulation.

**Args**

* **self**  : the instance of the class
* **constants_for_params** (dict) : a dictionary containing the constants for the simulation


**Returns**

* **dict**  : the updated dictionary of constants for the simulation


### .set_global_grasses_nuclear_winter
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L1527)
```python
.set_global_grasses_nuclear_winter(
   constants_for_params
)
```

---
Sets the ratio of grasses for each year in the case of a nuclear winter scenario.

**Args**

* **constants_for_params** (dict) : dictionary containing the constants for the model


**Returns**

* **dict**  : updated dictionary containing the constants for the model


### .set_country_grasses_nuclear_winter
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L1561)
```python
.set_country_grasses_nuclear_winter(
   constants_for_params, country_data
)
```

---
This function sets the ratio of grasses production for each month of the year
based on the country's grasses reduction data. It also updates the scenario description
and sets the GRASSES_SET flag to True.

**Args**

* **self**  : instance of the class
* **constants_for_params** (dict) : dictionary containing the constants for the model
* **country_data** (dict) : dictionary containing the country-specific data


**Returns**

* **dict**  : updated constants_for_params dictionary


### .set_fish_nuclear_winter_reduction
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L1594)
```python
.set_fish_nuclear_winter_reduction(
   constants_for_params
)
```

---
Set the fish percentages in every country (or globally) from baseline
although this is a global number, we don't have the regional number, so
we use the global instead.

### .set_fish_baseline
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L1764)
```python
.set_fish_baseline(
   constants_for_params
)
```

---
Sets the baseline for fish by updating the constants_for_params dictionary with
the necessary values. Also updates the scenario_description attribute of the object.

**Args**

* **constants_for_params** (dict) : dictionary containing the constants for the simulation


**Returns**

* **dict**  : updated dictionary with the baseline fish values


### .set_disruption_to_crops_to_zero
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L1790)
```python
.set_disruption_to_crops_to_zero(
   constants_for_params
)
```

---
Sets the disruption to crops to zero for the given constants_for_params.

**Args**

* **self**  : instance of the class
* **constants_for_params** (dict) : dictionary containing the constants for the parameters


**Returns**

* **dict**  : updated dictionary containing the constants for the parameters


**Raises**

* **AssertionError**  : if the disruption has already been set


### .set_nuclear_winter_global_disruption_to_crops
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L1817)
```python
.set_nuclear_winter_global_disruption_to_crops(
   constants_for_params
)
```

---
This function sets the ratio of crops for each year after a nuclear winter event.

**Args**

* **self**  : instance of the class
* **constants_for_params** (dict) : dictionary containing the constants for the parameters


**Returns**

* **constants_for_params** (dict) : updated dictionary containing the constants for the parameters


### .set_nuclear_winter_country_disruption_to_crops
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L1851)
```python
.set_nuclear_winter_country_disruption_to_crops(
   constants_for_params, country_data
)
```

---
This function sets the crop reduction ratios for a country in the event of a nuclear winter.

**Args**

* **self**  : instance of the class
* **constants_for_params** (dict) : dictionary containing the constants for the model
* **country_data** (dict) : dictionary containing the crop reduction ratios for a country


**Returns**

* **dict**  : dictionary containing the updated constants for the model


### .include_protein
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L1913)
```python
.include_protein(
   constants_for_params
)
```

---
This function sets the INCLUDE_PROTEIN parameter to True in the constants_for_params dictionary
and updates the scenario_description attribute of the object to include the string "include protein".

**Args**

* **self**  : the object instance
* **constants_for_params** (dict) : a dictionary containing the constants and their values


**Returns**

* **dict**  : the updated constants_for_params dictionary


### .dont_include_protein
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L1939)
```python
.dont_include_protein(
   constants_for_params
)
```

---
This function sets the INCLUDE_PROTEIN parameter to False, indicating that protein should not be included in the simulation.

**Args**

* **constants_for_params** (dict) : a dictionary containing the simulation parameters


**Returns**

* **dict**  : a dictionary containing the updated simulation parameters


### .include_fat
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L1963)
```python
.include_fat(
   constants_for_params
)
```

---
This function includes the 'fat' parameter in the scenario description and sets the 'INCLUDE_FAT' constant to True.

**Args**

* **self**  : the instance of the class
* **constants_for_params** (dict) : a dictionary containing the constants for the parameters


**Returns**

* **dict**  : the updated dictionary containing the constants for the parameters


### .dont_include_fat
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L1988)
```python
.dont_include_fat(
   constants_for_params
)
```

---
This function sets the INCLUDE_FAT parameter to False in the constants_for_params dictionary
and updates the scenario_description attribute of the object to indicate that fat should not be included.

**Args**

* **self**  : the object instance
* **constants_for_params** (dict) : a dictionary containing the constants for the parameters


**Returns**

* **dict**  : the updated constants_for_params dictionary


### .no_resilient_foods
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L2014)
```python
.no_resilient_foods(
   constants_for_params
)
```

---
This function sets the constants for a scenario where there are no resilient foods.
Resilient foods are foods that can withstand the effects of abrupt sunlight reduction due to volcano, nuclear winter, or asteroid impact.
This scenario sets the constants such that there are no resilient foods, which can lead to food insecurity and other issues.


**Args**

* **constants_for_params** (dict) : A dictionary containing the constants for the simulation.


**Returns**

* **dict**  : A dictionary containing the updated constants for the simulation.


### .seaweed
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L2043)
```python
.seaweed(
   constants_for_params
)
```

---
This function adds seaweed to the simulation by modifying the constants_for_params dictionary.

**Args**

* **constants_for_params** (dict) : A dictionary containing the simulation parameters.


**Returns**

* **dict**  : The modified dictionary with seaweed parameters added.


### .low_area_greenhouse
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L2068)
```python
.low_area_greenhouse(
   constants_for_params
)
```

---
This function sets the constants for a low area greenhouse scenario.


**Args**

* **constants_for_params** (dict) : A dictionary containing the constants for the simulation.


**Returns**

* **dict**  : A dictionary containing the updated constants for the simulation.


### .greenhouse
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L2095)
```python
.greenhouse(
   constants_for_params
)
```

---
This function sets the constants for the greenhouse scenario.


**Args**

* **constants_for_params** (dict) : A dictionary containing the constants for the scenario.


**Returns**

* **dict**  : A dictionary containing the updated constants for the scenario.


### .relocated_outdoor_crops
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L2121)
```python
.relocated_outdoor_crops(
   constants_for_params
)
```

---
This function modifies the constants_for_params dictionary to improve the rotation of outdoor crops.
It sets the OG_USE_BETTER_ROTATION flag to True, and adjusts the FAT_RATIO, PROTEIN_RATIO, INITIAL_HARVEST_DURATION_IN_MONTHS,
DELAY_ROTATION_CHANGE_IN_MONTHS, and RATIO_INCREASED_CROP_AREA parameters to improve the rotation of outdoor crops.


**Args**

* **constants_for_params** (dict) : A dictionary containing the parameters for the simulation.


**Returns**

* **dict**  : The modified dictionary of parameters.


### .expanded_area_and_relocated_outdoor_crops
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L2151)
```python
.expanded_area_and_relocated_outdoor_crops(
   constants_for_params
)
```

---
This function expands the area of outdoor crops and relocates them to a better location.
It modifies the constants_for_params dictionary to include the necessary parameters for this process.


**Args**

* **constants_for_params** (dict) : A dictionary containing the necessary parameters for the simulation.


**Returns**

* **dict**  : The modified constants_for_params dictionary.


### .methane_scp
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L2187)
```python
.methane_scp(
   constants_for_params
)
```

---
This function modifies the input dictionary of constants to include a new key-value pair
that enables the addition of methane SCP to the model. It also modifies two existing keys
in the dictionary to set default values from CS and SCP papers.


**Args**

* **constants_for_params** (dict) : A dictionary of constants used in the model


**Returns**

* **dict**  : The modified dictionary of constants with the new key-value pair added


### .cellulosic_sugar
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L2208)
```python
.cellulosic_sugar(
   constants_for_params
)
```

---
This function modifies the constants_for_params dictionary to include a delay of 3 months for
industrial foods and a slope multiplier of 1 for industrial foods. It also sets the ADD_CELLULOSIC_SUGAR
flag to True.

**Args**

* **constants_for_params** (dict) : A dictionary containing constants for the model parameters


**Returns**

* **dict**  : The modified constants_for_params dictionary


### .get_all_resilient_foods_scenario
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L2230)
```python
.get_all_resilient_foods_scenario(
   constants_for_params
)
```

---
This function sets the scenario for all resilient foods by calling several other functions
that modify the constants_for_params argument. It then sets the SCENARIO_SET flag to True
and returns the modified constants_for_params.


**Args**

* **constants_for_params** (dict) : a dictionary of constants used in the simulation


**Returns**

* **dict**  : the modified constants_for_params with the scenario for all resilient foods set


**Raises**

* **AssertionError**  : if the SCENARIO_SET flag is already True


### .get_all_resilient_foods_and_more_area_scenario
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L2265)
```python
.get_all_resilient_foods_and_more_area_scenario(
   constants_for_params
)
```

---
This function sets a scenario for all resilient foods and more area. It expands the area and relocates outdoor crops,
applies methane SCP, cellulosic sugar, greenhouse, and seaweed. It then sets the scenario and returns the constants
for parameters.


**Args**

* **self**  : instance of the class
* **constants_for_params** (dict) : dictionary of constants for parameters


**Returns**

* **dict**  : dictionary of constants for parameters with the scenario set


**Raises**

* **AssertionError**  : if the scenario set is already True


### .get_seaweed_scenario
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L2311)
```python
.get_seaweed_scenario(
   constants_for_params
)
```

---
This function sets the constants for a seaweed scenario and returns them.
It also updates the scenario description and sets the SCENARIO_SET flag to True.


**Args**

* **constants_for_params** (dict) : a dictionary of constants for the scenario


**Returns**

* **dict**  : a dictionary of updated constants for the seaweed scenario


### .get_methane_scp_scenario
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L2343)
```python
.get_methane_scp_scenario(
   constants_for_params
)
```

---
This function sets up the parameters for a scaled up methane SCP scenario.
It modifies the constants_for_params dictionary to reflect the new scenario.


**Args**

* **constants_for_params** (dict) : A dictionary containing the parameters for the scenario.


**Returns**

* **dict**  : A dictionary containing the modified parameters for the scenario.


### .get_cellulosic_sugar_scenario
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L2378)
```python
.get_cellulosic_sugar_scenario(
   constants_for_params
)
```

---
This function sets the parameters for a scenario where cellulosic sugar is scaled up.

**Args**

* **constants_for_params** (dict) : a dictionary of parameters for the model


**Returns**

* **dict**  : a dictionary of updated parameters for the model


### .get_relocated_crops_scenario
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L2416)
```python
.get_relocated_crops_scenario(
   constants_for_params
)
```

---
This function sets up a scenario where cold crops are scaled up and other crops are scaled down.
It also sets some constants to zero and some to False.

**Args**

* **constants_for_params** (dict) : a dictionary of constants used in the model


**Returns**

* **dict**  : a dictionary of constants used in the model with some constants set to zero and some to False


### .get_greenhouse_scenario
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L2453)
```python
.get_greenhouse_scenario(
   constants_for_params
)
```

---
This function sets up a scenario for scaled up greenhouses by modifying the constants_for_params dictionary.
It also updates the scenario_description attribute of the class instance.

**Args**

* **constants_for_params** (dict) : A dictionary containing the model parameters and their values.


**Returns**

* **dict**  : A dictionary containing the modified model parameters and their values.


### .get_no_resilient_food_scenario
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L2488)
```python
.get_no_resilient_food_scenario(
   constants_for_params
)
```

---
This function sets the scenario to have no resilient foods and returns the updated constants_for_params.

**Args**

* **constants_for_params** (dict) : a dictionary of constants used in the simulation


**Returns**

* **dict**  : the updated constants_for_params with no resilient foods


**Raises**

* **AssertionError**  : if the scenario has already been set


### .cull_animals
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L2518)
```python
.cull_animals(
   constants_for_params
)
```

---
This function sets a flag to cull animals and adds a description to the scenario.

**Args**

* **constants_for_params** (dict) : a dictionary of constants for the simulation


**Returns**

* **dict**  : the updated dictionary of constants for the simulation


### .dont_cull_animals
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L2542)
```python
.dont_cull_animals(
   constants_for_params
)
```

---
This function sets a parameter to prevent the culling of animals and updates the scenario description.

**Args**

* **self**  : instance of the class
* **constants_for_params** (dict) : dictionary of parameters to be used in the simulation


**Returns**

* **dict**  : updated dictionary of parameters

