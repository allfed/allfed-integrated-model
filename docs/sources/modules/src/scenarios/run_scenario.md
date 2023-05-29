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
This function runs a scenario by computing the necessary parameters, running the optimizer,
extracting data from the optimizer, interpreting the results, validating the results, and
optionally printing an output with people fed.


**Args**

* **constants_for_params** (dict) : A dictionary containing constants for the scenario.
* **scenarios_loader** (ScenarioLoader) : An instance of the ScenarioLoader class.


**Returns**

* **dict**  : A dictionary containing the interpreted results.


### .compute_parameters
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/run_scenario.py/#L76)
```python
.compute_parameters(
   constants_for_params, scenarios_loader
)
```

---
This function computes the parameters based on the constants and scenarios provided.
It returns the resulting constants.


**Args**

* **constants_for_params** (dict) : A dictionary containing the constants for the parameters.
* **scenarios_loader** (ScenariosLoader) : An instance of the ScenariosLoader class.


**Returns**

* **tuple**  : A tuple containing the single_valued_constants, time_consts, and feed_and_biofuels.


### .run_optimizer
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/run_scenario.py/#L103)
```python
.run_optimizer(
   single_valued_constants, time_consts
)
```

---
Runs the optimizer and returns the model, variables, and constants


**Args**

* **single_valued_constants** (dict) : A dictionary of single-valued constants
* **time_consts** (dict) : A dictionary of time constants


**Returns**

* **tuple**  : A tuple containing the model, variables, single_valued_constants, and time_consts


### .set_depending_on_option
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/run_scenario.py/#L150)
```python
.set_depending_on_option(
   country_data, scenario_option
)
```

