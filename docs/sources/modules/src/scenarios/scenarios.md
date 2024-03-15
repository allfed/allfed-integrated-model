#


## Scenarios
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L14)
```python 

```




**Methods:**


### .check_all_set
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L38)
```python
.check_all_set()
```

---
Ensure all properties of scenarios have been set

### .init_generic_scenario
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L62)
```python
.init_generic_scenario()
```


### .init_global_food_system_properties
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L80)
```python
.init_global_food_system_properties()
```


### .init_country_food_system_properties
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L321)
```python
.init_country_food_system_properties(
   country_data
)
```


### .set_immediate_shutoff
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L538)
```python
.set_immediate_shutoff(
   constants_for_params
)
```


### .set_one_month_delayed_shutoff
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L549)
```python
.set_one_month_delayed_shutoff(
   constants_for_params
)
```


### .set_short_delayed_shutoff
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L562)
```python
.set_short_delayed_shutoff(
   constants_for_params
)
```


### .set_long_delayed_shutoff
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L574)
```python
.set_long_delayed_shutoff(
   constants_for_params
)
```


### .set_continued_feed_biofuels
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L587)
```python
.set_continued_feed_biofuels(
   constants_for_params
)
```


### .set_continued_after_10_percent_fed
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L609)
```python
.set_continued_after_10_percent_fed(
   constants_for_params
)
```


### .set_long_delayed_shutoff_after_10_percent_fed
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L631)
```python
.set_long_delayed_shutoff_after_10_percent_fed(
   constants_for_params
)
```


### .set_breeding_to_greatly_reduced
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L651)
```python
.set_breeding_to_greatly_reduced(
   constants_for_params
)
```


### .set_to_baseline_breeding
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L660)
```python
.set_to_baseline_breeding(
   constants_for_params
)
```


### .set_to_feed_only_ruminants
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L669)
```python
.set_to_feed_only_ruminants(
   constants_for_params
)
```


### .set_waste_to_zero
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L680)
```python
.set_waste_to_zero(
   constants_for_params
)
```


### .get_global_distribution_waste
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L695)
```python
.get_global_distribution_waste()
```

---
Calculates the distribution waste of the global food system.

### .set_global_waste_to_tripled_prices
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L712)
```python
.set_global_waste_to_tripled_prices(
   constants_for_params
)
```


### .set_global_waste_to_doubled_prices
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L730)
```python
.set_global_waste_to_doubled_prices(
   constants_for_params
)
```

---
overall waste, on farm + distribution + retail
2x prices (note, currently set to 2019, not 2020)

### .set_global_waste_to_baseline_prices
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L748)
```python
.set_global_waste_to_baseline_prices(
   constants_for_params
)
```

---
overall waste, on farm+distribution+retail
1x prices (note, currently set to 2019, not 2020)

### .get_distribution_waste
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L767)
```python
.get_distribution_waste(
   country_data
)
```

---
Calculates the distribution waste of the global food system.

### .set_country_waste_to_tripled_prices
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L783)
```python
.set_country_waste_to_tripled_prices(
   constants_for_params, country_data
)
```

---
overall waste, on farm + distribution + retail
3x prices (note, currently set to 2019, not 2020)

### .set_country_waste_to_doubled_prices
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L802)
```python
.set_country_waste_to_doubled_prices(
   constants_for_params, country_data
)
```

---
overall waste, on farm + distribution + retail
2x prices (note, currently set to 2019, not 2020)

### .set_country_waste_to_baseline_prices
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L820)
```python
.set_country_waste_to_baseline_prices(
   constants_for_params, country_data
)
```

---
overall waste, on farm+distribution+retail
1x prices (note, currently set to 2019, not 2020)

### .set_baseline_nutrition_profile
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L839)
```python
.set_baseline_nutrition_profile(
   constants_for_params
)
```


### .set_catastrophe_nutrition_profile
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L857)
```python
.set_catastrophe_nutrition_profile(
   constants_for_params
)
```


### .set_intake_constraints_to_enabled
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L877)
```python
.set_intake_constraints_to_enabled(
   constants_for_params
)
```


### .set_intake_constraints_to_disabled_for_humans
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L895)
```python
.set_intake_constraints_to_disabled_for_humans(
   constants_for_params
)
```


### .set_no_stored_food
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L915)
```python
.set_no_stored_food(
   constants_for_params
)
```

---
Sets the stored food at start of simulation to zero.

### .set_baseline_stored_food
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L928)
```python
.set_baseline_stored_food(
   constants_for_params
)
```

---
Sets the stored food at start of simulation to the expected amount in the start month.

### .set_stored_food_buffer_zero
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L943)
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

### .set_no_stored_food_between_years
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L961)
```python
.set_no_stored_food_between_years(
   constants_for_params
)
```

---
Sets the stored food between years as zero. No food is traded between the
12 month intervals seasons. Makes more sense if seasonality is assumed zero.
All expected stored food at start is however available.

However, in reality food in transit and food in grocery stores and
warehouses means there would still likely be some food available at
the end as a buffer.

### .set_stored_food_buffer_as_baseline
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L979)
```python
.set_stored_food_buffer_as_baseline(
   constants_for_params
)
```

---
Sets the stored food buffer as 100% -- the typical stored food buffer
in ~2020 left at the end of the simulation.

### .set_no_seasonality
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L995)
```python
.set_no_seasonality(
   constants_for_params
)
```


### .set_global_seasonality_baseline
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L1006)
```python
.set_global_seasonality_baseline(
   constants_for_params
)
```


### .set_global_seasonality_nuclear_winter
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L1029)
```python
.set_global_seasonality_nuclear_winter(
   constants_for_params
)
```


### .set_country_seasonality
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L1054)
```python
.set_country_seasonality(
   constants_for_params, country_data
)
```


### .set_grasses_baseline
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L1081)
```python
.set_grasses_baseline(
   constants_for_params
)
```


### .set_global_grasses_nuclear_winter
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L1090)
```python
.set_global_grasses_nuclear_winter(
   constants_for_params
)
```


### .set_country_grasses_nuclear_winter
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L1110)
```python
.set_country_grasses_nuclear_winter(
   constants_for_params, country_data
)
```


### .set_country_grasses_to_zero
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L1123)
```python
.set_country_grasses_to_zero(
   constants_for_params
)
```


### .set_fish_zero
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L1136)
```python
.set_fish_zero(
   constants_for_params, time_consts
)
```


### .set_fish_nuclear_winter_reduction
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L1147)
```python
.set_fish_nuclear_winter_reduction(
   time_consts
)
```

---
Set the fish percentages in every country (or globally) from baseline
although this is a global number, we don't have the regional number, so
we use the global instead.

### .set_fish_baseline
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L1317)
```python
.set_fish_baseline(
   constants_for_params, time_consts
)
```


### .set_disruption_to_crops_to_zero
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L1330)
```python
.set_disruption_to_crops_to_zero(
   constants_for_params
)
```


### .set_nuclear_winter_global_disruption_to_crops
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L1341)
```python
.set_nuclear_winter_global_disruption_to_crops(
   constants_for_params
)
```


### .set_nuclear_winter_country_disruption_to_crops
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L1362)
```python
.set_nuclear_winter_country_disruption_to_crops(
   constants_for_params, country_data
)
```


### .set_zero_crops
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L1408)
```python
.set_zero_crops(
   constants_for_params
)
```


### .include_protein
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L1433)
```python
.include_protein(
   constants_for_params
)
```


### .dont_include_protein
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L1440)
```python
.dont_include_protein(
   constants_for_params
)
```


### .include_fat
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L1449)
```python
.include_fat(
   constants_for_params
)
```


### .dont_include_fat
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L1457)
```python
.dont_include_fat(
   constants_for_params
)
```


### .no_resilient_foods
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L1466)
```python
.no_resilient_foods(
   constants_for_params
)
```


### .seaweed
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L1480)
```python
.seaweed(
   constants_for_params
)
```


### .greenhouse
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L1486)
```python
.greenhouse(
   constants_for_params
)
```


### .relocated_outdoor_crops
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L1495)
```python
.relocated_outdoor_crops(
   constants_for_params
)
```


### .expanded_area_and_relocated_outdoor_crops
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L1508)
```python
.expanded_area_and_relocated_outdoor_crops(
   constants_for_params
)
```


### .methane_scp
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L1522)
```python
.methane_scp(
   constants_for_params
)
```


### .cellulosic_sugar
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L1532)
```python
.cellulosic_sugar(
   constants_for_params
)
```


### .get_all_resilient_foods_scenario
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L1542)
```python
.get_all_resilient_foods_scenario(
   constants_for_params
)
```


### .get_all_resilient_foods_and_more_area_scenario
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L1554)
```python
.get_all_resilient_foods_and_more_area_scenario(
   constants_for_params
)
```


### .get_seaweed_scenario
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L1577)
```python
.get_seaweed_scenario(
   constants_for_params
)
```


### .get_methane_scp_scenario
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L1597)
```python
.get_methane_scp_scenario(
   constants_for_params
)
```


### .get_cellulosic_sugar_scenario
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L1615)
```python
.get_cellulosic_sugar_scenario(
   constants_for_params
)
```


### .get_industrial_foods_scenario
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L1633)
```python
.get_industrial_foods_scenario(
   constants_for_params
)
```


### .get_relocated_crops_scenario
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L1651)
```python
.get_relocated_crops_scenario(
   constants_for_params
)
```


### .get_greenhouse_scenario
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L1667)
```python
.get_greenhouse_scenario(
   constants_for_params
)
```


### .get_no_resilient_food_scenario
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L1687)
```python
.get_no_resilient_food_scenario(
   constants_for_params
)
```


### .cull_animals
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L1698)
```python
.cull_animals(
   constants_for_params
)
```


### .dont_cull_animals
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/scenarios.py/#L1707)
```python
.dont_cull_animals(
   constants_for_params
)
```

