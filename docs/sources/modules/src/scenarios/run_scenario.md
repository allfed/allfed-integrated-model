#


## ScenarioRunner
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/run_scenario.py/#L48)
```python 

```




**Methods:**


### .display_results_of_optimizer_round
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/run_scenario.py/#L52)
```python
.display_results_of_optimizer_round(
   interpreted_results, country_name, show_country_figures,
   create_pptx_with_all_countries, scenario_loader, figure_save_postfix,
   slaughter_title = '', feed_title = '', to_humans_title = ''
)
```


### .run_round_1
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/run_scenario.py/#L105)
```python
.run_round_1(
   consts_for_optimizer_round1, time_consts_round1, interpreter,
   feed_and_biofuels_round1, meat_dictionary_zero_feed_biofuels,
   title = 'Untitled'
)
```


### .run_round_2
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/run_scenario.py/#L137)
```python
.run_round_2(
   constants_loader, constants_for_params, interpreted_results_round1,
   percent_fed_from_model_round1, consts_for_optimizer_round1,
   time_consts_round1, interpreter, title = 'Untitled'
)
```


### .run_round_3
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/run_scenario.py/#L223)
```python
.run_round_3(
   constants_loader, constants_for_params, consts_for_optimizer_round1,
   consts_for_optimizer_round2, time_consts_round1, time_consts_round2,
   interpreted_results_round2, feed_and_biofuels_round1, feed_demand,
   biofuels_demand, interpreted_results_round1, meat_dictionary_round2,
   each_month_meat_slaughtered, max_consumed_culled_kcals_each_month,
   meat_summed_consumption, feed_meat_object_round1, title = 'Untitled'
)
```


### .get_interpreted_results_for_round3_if_zero_feed
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/run_scenario.py/#L274)
```python
.get_interpreted_results_for_round3_if_zero_feed(
   interpreter, NMONTHS
)
```


### .run_and_analyze_scenario
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/run_scenario.py/#L291)
```python
.run_and_analyze_scenario(
   constants_for_params, time_consts_for_params, scenario_loader,
   create_pptx_with_all_countries, show_country_figures, figure_save_postfix,
   country_data, save_all_results, country_name, country_iso3, title = 'Untitled'
)
```

---
computes params, Runs the optimizer, extracts data from optimizer, interprets
the results, validates the results, and optionally prints an output with people
fed.

arguments: constants from the scenario, scenario loader (to print the aspects
of the scenario and check no scenario parameter has been set twice or left
unset)

returns: the interpreted results

### .interpret_optimizer_results
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/run_scenario.py/#L536)
```python
.interpret_optimizer_results(
   consts_for_optimizer, model, variables, time_consts, interpreter,
   percent_fed_from_model, optimization_type, title = 'Untitled'
)
```


### .run_optimizer
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/run_scenario.py/#L573)
```python
.run_optimizer(
   consts_for_optimizer, time_consts, optimization_type = None,
   min_human_food_consumption = None, title = 'Untitled'
)
```

---
Runs the optimizer and returns the model, variables, and constants

### .alter_scenario_if_known_to_fail
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/run_scenario.py/#L641)
```python
.alter_scenario_if_known_to_fail(
   scenario_option, iso3
)
```

---
These are the scenarios I seem to be unable to determine why optimization is failing.
I belive I have hit diminishing returns trying to figure them out, so I just patch them instead.

### .set_depending_on_option
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/run_scenario.py/#L782)
```python
.set_depending_on_option(
   scenario_option, country_data = None
)
```


### .save_outdoor_crop_production_to_csv
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/run_scenario.py/#L1330)
```python
.save_outdoor_crop_production_to_csv(
   time_consts_round1, title, country_data
)
```

---
Saves the outdoor crop production to a csv file

### .save_feed_and_biofuels_to_csv
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/run_scenario.py/#L1352)
```python
.save_feed_and_biofuels_to_csv(
   feed_demand, biofuels_demand, title, country_data
)
```

---
Saves the feed and biofuels demand to a csv file

----


### are_dicts_approx_same
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/run_scenario.py/#L34)
```python
.are_dicts_approx_same(
   dict1, dict2
)
```

