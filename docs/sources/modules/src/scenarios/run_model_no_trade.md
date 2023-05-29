#


## ScenarioRunnerNoTrade
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/run_model_no_trade.py/#L31)
```python 

```


---
This function runs the model for all countries in the world, no trade.


**Methods:**


### .run_model_defaults_no_trade
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/run_model_no_trade.py/#L49)
```python
.run_model_defaults_no_trade(
   this_simulation, show_map_figures = False, show_country_figures = False,
   create_pptx_with_all_countries = False, scenario_option = []
)
```

---
Runs the model with default options for a given simulation, and generates figures and a PowerPoint presentation.

**Args**

* **this_simulation** (dict) : a dictionary containing specific options for the given simulation
* **show_map_figures** (bool) : whether to show map figures or not
* **show_country_figures** (bool) : whether to show country figures or not
* **create_pptx_with_all_countries** (bool) : whether to create a PowerPoint presentation with all countries or not
* **scenario_option** (list) : a list of scenario options


### .run_optimizer_for_country
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/run_model_no_trade.py/#L113)
```python
.run_optimizer_for_country(
   country_data, scenario_option, create_pptx_with_all_countries,
   show_country_figures, figure_save_postfix = ''
)
```

---
Runs the optimizer for a given country and scenario option, and returns the percentage of people fed,
the scenario description, and the interpreted results.


**Args**

* **self**  : instance of the Optimizer class
* **country_data** (dict) : dictionary containing data for the country
* **scenario_option** (str) : scenario option to use for the optimization
* **create_pptx_with_all_countries** (bool) : whether to create a PowerPoint file with all countries' figures
* **show_country_figures** (bool) : whether to show the figures for the country
* **figure_save_postfix** (str) : postfix to add to the figure file names


**Returns**

* **tuple**  : a tuple containing the percentage of people fed, the scenario description, and the interpreted results


### .fill_data_for_map
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/run_model_no_trade.py/#L221)
```python
.fill_data_for_map(
   world, country_code, needs_ratio
)
```

---
This function fills the needs_ratio column of the world dataframe with the kcals_ratio_capped value for a given
country_code. If the country_code is not found in the world dataframe, a message is printed.


**Args**

* **world** (pandas.DataFrame) : the dataframe containing the data for all countries
* **country_code** (str) : the ISO3 code of the country for which the needs_ratio is to be filled
* **needs_ratio** (float) : the kcals_ratio value for the country


**Returns**

None

### .run_model_no_trade
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/run_model_no_trade.py/#L258)
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


**Args**

* **title** (str) : title of the powerpoint presentation
* **create_pptx_with_all_countries** (bool) : whether to create a powerpoint presentation
* **show_country_figures** (bool) : whether to show figures for each country
* **show_map_figures** (bool) : whether to show the map figure
* **add_map_slide_to_pptx** (bool) : whether to add the map slide to the powerpoint presentation
* **scenario_option** (list) : list of scenarios to run the model for
* **countries_list** (list) : list of country codes to run the model for
* **figure_save_postfix** (str) : postfix to add to the figure save name
* **return_results** (bool) : whether to return the results


**Returns**

* **list**  : a list containing the world, net population, net population fed, and results


### .get_countries_to_run_and_skip
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/run_model_no_trade.py/#L434)
```python
.get_countries_to_run_and_skip(
   countries_list
)
```

---
This function takes a list of country codes and returns two lists: one with the
country codes that should be run exclusively, and another with the country codes
that should be skipped. If a country code has a "!" in front of it, it should be
skipped. If there are no "!" in any of the codes, then only the ones listed will
be run.


**Args**

* **countries_list** (list) : A list of country codes.


**Returns**

* **tuple**  : A tuple containing two lists: the first list contains the country codes
that should be run exclusively, and the second list contains the country codes
that should be skipped.

### .run_many_options
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/run_model_no_trade.py/#L473)
```python
.run_many_options(
   scenario_options, title, add_map_slide_to_pptx = True, show_map_figures = False,
   countries_list = [], return_results = False
)
```

---
Runs multiple scenarios and generates a PowerPoint presentation with the results.

**Args**

* **self**  : instance of the class
* **scenario_options** (list) : list of dictionaries, each containing the parameters for a scenario
* **title** (str) : title of the PowerPoint presentation
* **add_map_slide_to_pptx** (bool) : whether to add a map slide to the PowerPoint presentation
* **show_map_figures** (bool) : whether to show map figures
* **countries_list** (list) : list of countries to include in the analysis
* **return_results** (bool) : whether to return the results of the scenarios


### .create_several_maps_with_different_assumptions
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/run_model_no_trade.py/#L549)
```python
.create_several_maps_with_different_assumptions(
   this_simulation, show_map_figures = False
)
```

---
This function creates several maps with different assumptions by combining different options
for waste, buffer, shutoff, fat, and protein. It then runs many options using the
run_many_options function.


**Args**

* **self**  : instance of the class
* **this_simulation** (dict) : dictionary containing the simulation parameters
* **show_map_figures** (bool) : whether to show the map figures or not


**Returns**

None

### .run_desired_simulation
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/run_model_no_trade.py/#L603)
```python
.run_desired_simulation(
   this_simulation, args
)
```

---
Runs the desired simulation based on the given arguments and generates a report if specified.


**Args**

* **this_simulation** (Simulation) : The simulation object to run.
* **args** (list) : A list of optional arguments to specify the type of simulation to run and report generation.

---
Optional Args:
    third: [no_plot|plot] (plots figures)


**Returns**

None


**Example**


```python

>>> run_desired_simulation(simulation_object, ['single', 'pptx', 'plot'])
```
