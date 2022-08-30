#


## ScenarioRunnerNoTrade
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/run_model_no_trade.py/#L31)
```python 

```


---
This function runs the model for all countries in the world, no trade.


**Methods:**


### .run_model_defaults_no_trade
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/run_model_no_trade.py/#L39)
```python
.run_model_defaults_no_trade(
   this_simulation, show_map_figures = False, show_country_figures = False,
   create_pptx_with_all_countries = False, scenario_option = []
)
```

---
Set a few options to set on top of the specific options for the given simulation
These could easily change if another scenario was of more interest.

### .run_optimizer_for_country
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/run_model_no_trade.py/#L68)
```python
.run_optimizer_for_country(
   country_code, country_data, scenario_option, create_pptx_with_all_countries,
   show_country_figures, figure_save_postfix = ''
)
```


### .fill_data_for_map
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/run_model_no_trade.py/#L142)
```python
.fill_data_for_map(
   world, country_code, needs_ratio
)
```


### .run_model_no_trade
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/run_model_no_trade.py/#L162)
```python
.run_model_no_trade(
   title = 'untitled', create_pptx_with_all_countries = True,
   show_country_figures = False, show_map_figures = False,
   add_map_slide_to_pptx = True, scenario_option = [], countries_list = [],
   figure_save_postfix = '', return_results = False
)
```

---
This function runs the model for all countries in the world, no trade.
countries_list is a list of country codes to run the model for, but if
there's an "!" in the list, you skip that one.
If you leave it blank, it runs all the countries

You can generate a powerpoint as an option here too

### .get_countries_to_run_and_skip
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/run_model_no_trade.py/#L329)
```python
.get_countries_to_run_and_skip(
   countries_list
)
```

---
if there's any country code with a "!", skip that one
For example, if !USA is one of the country codes, that one will be skipped
If !USA and !CHN are country codes, then both will skip
if there's no ! in any of the codes, then only the ones listed will be
run.

### .run_many_options
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/run_model_no_trade.py/#L357)
```python
.run_many_options(
   scenario_options, title, add_map_slide_to_pptx = True, show_map_figures = False,
   countries_list = [], return_results = False
)
```


### .create_several_maps_with_different_assumptions
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/run_model_no_trade.py/#L417)
```python
.create_several_maps_with_different_assumptions(
   this_simulation, show_map_figures = False
)
```


### .run_desired_simulation
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/run_model_no_trade.py/#L486)
```python
.run_desired_simulation(
   this_simulation, args
)
```

