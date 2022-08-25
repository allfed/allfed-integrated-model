#


## ScenarioRunner
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/run_scenario.py/#L19)
```python 

```




**Methods:**


### .run_and_analyze_scenario
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/run_scenario.py/#L23)
```python
.run_and_analyze_scenario(
   constants_for_params, scenarios_loader
)
```

---
computes params, Runs the optimizer, extracts data from optimizer, interprets
the results, validates the results, and optionally prints an output with people
fed.

arguments:
constants from the scenario, scenario loader (to print the aspects
---
of the scenario and check no scenario parameter has been set twice or left
unset)

returns:
    the interpreted results

### .compute_parameters
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/run_scenario.py/#L81)
```python
.compute_parameters(
   constants_for_params, scenarios_loader
)
```

---
computes the parameters
returns:
the resulting constants

### .run_optimizer
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/run_scenario.py/#L99)
```python
.run_optimizer(
   single_valued_constants, multi_valued_constants
)
```

---
Runs the optimizer and returns the model, variables, and constants

### .set_depending_on_option
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/run_scenario.py/#L130)
```python
.set_depending_on_option(
   country_data, scenario_option
)
```

