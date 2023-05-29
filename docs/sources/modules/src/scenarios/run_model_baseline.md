#


### run_model_baseline
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/run_model_baseline.py/#L6)
```python
.run_model_baseline(
   plot_figures = True
)
```

---
This function runs the optimizer model for the case of continued trade and baseline climate 2020.
It sets the constants, loads the scenarios, runs the scenario runner, and prints the results.
If plot_figures is True, it also plots the figures.


**Args**

* **plot_figures** (bool) : whether to plot the figures or not.


**Returns**

None

----


### set_common_baseline_properties
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/run_model_baseline.py/#L76)
```python
.set_common_baseline_properties()
```

---
This function sets the common baseline properties for the food system. These properties are true for the baseline
regardless of whether the country or global scenario is being run. The function initializes global food system
properties and sets various parameters to their baseline values.


**Returns**

* **tuple**  : A tuple containing the Scenarios object and the constants_for_params dictionary with the baseline
properties set.
