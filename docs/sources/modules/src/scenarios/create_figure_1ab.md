#


### call_scenario_runner
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/create_figure_1ab.py/#L19)
```python
.call_scenario_runner(
   this_simulation, title
)
```

---
Runs a simulation using the ScenarioRunnerNoTrade class and returns the resulting world, total population, and fed population.


**Args**

* **this_simulation** (str) : the name of the simulation to run
* **title** (str) : the title of the simulation


**Returns**

* **list**  : a list containing the resulting world, total population, and fed population


----


### call_scenario_runner_with_and_without_fat_protein
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/create_figure_1ab.py/#L48)
```python
.call_scenario_runner_with_and_without_fat_protein(
   this_simulation, title
)
```

---
Runs a simulation with and without fat and protein, and returns the world object and the percentage of population fed.


**Args**

* **this_simulation** (dict) : A dictionary containing simulation parameters.
* **title** (str) : A string containing the title of the simulation.


**Returns**

* **tuple**  : A tuple containing the world object and the percentage of population fed.


----


### recalculate_plots
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/create_figure_1ab.py/#L75)
```python
.recalculate_plots()
```

---
This function recalculates plots for different scenarios and returns the results.


**Returns**

* **tuple**  : A tuple containing two dictionaries. The first dictionary contains the
results for each scenario, and the second dictionary contains the fraction of
needs met for each scenario.
