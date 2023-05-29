#


### call_scenario_runner
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/create_figure_2abcde.py/#L19)
```python
.call_scenario_runner(
   this_simulation, title
)
```

---
Runs a simulation using the ScenarioRunnerNoTrade class and returns the results.


**Args**

* **this_simulation** (str) : the name of the simulation to run
* **title** (str) : the title of the simulation


**Returns**

* **list**  : a list containing the world object, total population, fed population, and results dictionary


----


### call_scenario_runner_whole_world_combined
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/create_figure_2abcde.py/#L51)
```python
.call_scenario_runner_whole_world_combined(
   this_simulation, title
)
```

---
Runs a simulation of a nuclear winter catastrophe on the world, with all countries affected.

**Args**

* **this_simulation** (dict) : a dictionary containing simulation parameters
* **title** (str) : a string to be used as a title for the simulation


**Returns**

* **list**  : a list containing the world object, total population, fed population, and global results


----


### call_scenario_runner_with_and_without_fat_protein
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/create_figure_2abcde.py/#L94)
```python
.call_scenario_runner_with_and_without_fat_protein(
   this_simulation, title
)
```

---
Runs a simulation with and without fat and protein, and returns the results.


**Args**

* **this_simulation** (dict) : A dictionary containing simulation parameters.
* **title** (str) : The title of the simulation.


**Returns**

* **list**  : A list containing the simulation results.


**Example**


```python

>>> simulation = (some python dictionary with appropriate options)
>>> results = call_scenario_runner_with_and_without_fat_protein(simulation, "Simulation Title")
```

----


### recalculate_plots
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/create_figure_2abcde.py/#L127)
```python
.recalculate_plots()
```

---
This function recalculates plots for different simulation scenarios and returns a list of results by country.


**Returns**

* **list**  : A list of results by country, including the percent of people fed, country name, simulation results, and scenario name.

