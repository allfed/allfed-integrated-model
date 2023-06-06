#


### run_model_with_resilient_foods
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/run_model_with_resilient_foods.py/#L11)
```python
.run_model_with_resilient_foods(
   plot_figures = True
)
```

---
Runs the model in nuclear winter with resilient foods, then calculates a diet
The diet is 2100 kcals, determined by feeding any excess to animals
This currently runs for the whole earth, and does not run on a by-country
basis.


**Args**

* **plot_figures** (bool) : whether to plot the figures or not.


**Returns**

None

----


### set_common_resilient_properties
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/run_model_with_resilient_foods.py/#L178)
```python
.set_common_resilient_properties()
```

---
This function sets the common resilient properties for the food system by calling various functions from the
Scenarios class.


**Returns**

* **tuple**  : A tuple containing the Scenarios object and the constants_for_params dictionary.

