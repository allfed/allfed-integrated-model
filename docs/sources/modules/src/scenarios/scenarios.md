#


## Scenarios
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L12)
```python 

```




**Methods:**


### .check_all_set
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L35)
```python
.check_all_set()
```

---
Ensure all properties of scenarios have been set

### .init_generic_scenario
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L58)
```python
.init_generic_scenario()
```


### .init_global_food_system_properties
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L79)
```python
.init_global_food_system_properties()
```


### .init_country_food_system_properties
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L185)
```python
.init_country_food_system_properties(
   country_data
)
```


### .set_immediate_shutoff
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L367)
```python
.set_immediate_shutoff(
   constants_for_params
)
```


### .set_short_delayed_shutoff
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L377)
```python
.set_short_delayed_shutoff(
   constants_for_params
)
```


### .set_long_delayed_shutoff
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L386)
```python
.set_long_delayed_shutoff(
   constants_for_params
)
```


### .set_continued_feed_biofuels
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L395)
```python
.set_continued_feed_biofuels(
   constants_for_params
)
```


### .set_unchanged_proportions_feed_grazing
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L420)
```python
.set_unchanged_proportions_feed_grazing(
   constants_for_params
)
```


### .set_efficient_feed_grazing_strategy
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L429)
```python
.set_efficient_feed_grazing_strategy(
   constants_for_params
)
```


### .set_excess_to_zero
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L440)
```python
.set_excess_to_zero(
   constants_for_params
)
```


### .set_excess
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L449)
```python
.set_excess(
   constants_for_params, excess
)
```


### .set_waste_to_zero
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L458)
```python
.set_waste_to_zero(
   constants_for_params
)
```


### .get_total_global_waste
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L472)
```python
.get_total_global_waste(
   retail_waste
)
```

---
Calculates the total waste of the global food system by adding retail waste
to distribution loss.

### .set_global_waste_to_tripled_prices
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L499)
```python
.set_global_waste_to_tripled_prices(
   constants_for_params
)
```


### .set_global_waste_to_doubled_prices
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L516)
```python
.set_global_waste_to_doubled_prices(
   constants_for_params
)
```

---
overall waste, on farm + distribution + retail
2x prices (note, currently set to 2019, not 2020)

### .set_global_waste_to_baseline_prices
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L534)
```python
.set_global_waste_to_baseline_prices(
   constants_for_params
)
```

---
overall waste, on farm+distribution+retail
1x prices (note, currently set to 2019, not 2020)

### .get_total_country_waste
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L551)
```python
.get_total_country_waste(
   retail_waste, country_data
)
```

---
Calculates the total waste of the global food system by adding retail waste
to distribution loss.

### .set_country_waste_to_tripled_prices
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L576)
```python
.set_country_waste_to_tripled_prices(
   constants_for_params, country_data
)
```

---
overall waste, on farm + distribution + retail
3x prices (note, currently set to 2019, not 2020)

### .set_country_waste_to_doubled_prices
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L594)
```python
.set_country_waste_to_doubled_prices(
   constants_for_params, country_data
)
```

---
overall waste, on farm + distribution + retail
2x prices (note, currently set to 2019, not 2020)

### .set_country_waste_to_baseline_prices
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L611)
```python
.set_country_waste_to_baseline_prices(
   constants_for_params, country_data
)
```

---
overall waste, on farm+distribution+retail
1x prices (note, currently set to 2019, not 2020)

### .set_baseline_nutrition_profile
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L631)
```python
.set_baseline_nutrition_profile(
   constants_for_params
)
```


### .set_catastrophe_nutrition_profile
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L649)
```python
.set_catastrophe_nutrition_profile(
   constants_for_params
)
```


### .set_no_stored_food
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L669)
```python
.set_no_stored_food(
   constants_for_params
)
```

---
Sets the stored food between years as zero. No food is traded between the
12 month intervals seasons. Makes more sense if seasonality is assumed zero.

However, in reality food in transit and food in grocery stores and
warehouses means there would still likely be some food available at
the end as a buffer.

### .set_stored_food_buffer_zero
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L686)
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

### .set_stored_food_buffer_as_baseline
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L704)
```python
.set_stored_food_buffer_as_baseline(
   constants_for_params
)
```

---
Sets the stored food buffer as 100% -- the typical stored food buffer
in ~2020 left at the end of the simulation.

### .set_no_seasonality
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L720)
```python
.set_no_seasonality(
   constants_for_params
)
```


### .set_global_seasonality_baseline
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L731)
```python
.set_global_seasonality_baseline(
   constants_for_params
)
```


### .set_global_seasonality_nuclear_winter
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L754)
```python
.set_global_seasonality_nuclear_winter(
   constants_for_params
)
```


### .set_country_seasonality
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L779)
```python
.set_country_seasonality(
   constants_for_params, country_data
)
```


### .set_grasses_baseline
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L793)
```python
.set_grasses_baseline(
   constants_for_params
)
```


### .set_global_grasses_nuclear_winter
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L802)
```python
.set_global_grasses_nuclear_winter(
   constants_for_params
)
```


### .set_country_grasses_nuclear_winter
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L820)
```python
.set_country_grasses_nuclear_winter(
   constants_for_params, country_data
)
```


### .set_fish_nuclear_winter_reduction
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L845)
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
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L948)
```python
.set_fish_baseline(
   constants_for_params
)
```


### .set_disruption_to_crops_to_zero
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L961)
```python
.set_disruption_to_crops_to_zero(
   constants_for_params
)
```


### .set_nuclear_winter_global_disruption_to_crops
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L971)
```python
.set_nuclear_winter_global_disruption_to_crops(
   constants_for_params
)
```


### .set_nuclear_winter_country_disruption_to_crops
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L991)
```python
.set_nuclear_winter_country_disruption_to_crops(
   constants_for_params, country_data
)
```


### .include_protein
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L1038)
```python
.include_protein(
   constants_for_params
)
```


### .dont_include_protein
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L1045)
```python
.dont_include_protein(
   constants_for_params
)
```


### .include_fat
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L1054)
```python
.include_fat(
   constants_for_params
)
```


### .dont_include_fat
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L1062)
```python
.dont_include_fat(
   constants_for_params
)
```


### .no_resilient_foods
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L1071)
```python
.no_resilient_foods(
   constants_for_params
)
```


### .seaweed
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L1084)
```python
.seaweed(
   constants_for_params
)
```


### .greenhouse
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L1095)
```python
.greenhouse(
   constants_for_params
)
```


### .relocated_outdoor_crops
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L1104)
```python
.relocated_outdoor_crops(
   constants_for_params
)
```


### .methane_scp
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L1119)
```python
.methane_scp(
   constants_for_params
)
```


### .cellulosic_sugar
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L1128)
```python
.cellulosic_sugar(
   constants_for_params
)
```


### .get_all_resilient_foods_scenario
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L1137)
```python
.get_all_resilient_foods_scenario(
   constants_for_params
)
```


### .get_seaweed_scenario
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L1150)
```python
.get_seaweed_scenario(
   constants_for_params
)
```


### .get_methane_scp_scenario
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L1168)
```python
.get_methane_scp_scenario(
   constants_for_params
)
```


### .get_cellulosic_sugar_scenario
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L1186)
```python
.get_cellulosic_sugar_scenario(
   constants_for_params
)
```


### .get_relocated_crops_scenario
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L1204)
```python
.get_relocated_crops_scenario(
   constants_for_params
)
```


### .get_greenhouse_scenario
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L1222)
```python
.get_greenhouse_scenario(
   constants_for_params
)
```


### .get_no_resilient_food_scenario
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L1242)
```python
.get_no_resilient_food_scenario(
   constants_for_params
)
```


### .cull_animals
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L1253)
```python
.cull_animals(
   constants_for_params
)
```


### .dont_cull_animals
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L1261)
```python
.dont_cull_animals(
   constants_for_params
)
```

