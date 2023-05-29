#


### run_model_no_resilient_foods
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/run_model_no_resilient_foods.py/#L11)
```python
.run_model_no_resilient_foods(
   plot_figures = True
)
```

---
This function runs the optimizer model and ensures that all the results are reasonable using a couple useful checks to make sure there's nothing wacky going on:
1) check that as time increases, more people can be fed
2) check that stored food plus meat is always used at the highest rate during the largest food shortage.


**Args**

* **plot_figures** (bool) : whether to plot the figures or not.


**Returns**

None

----


### set_common_no_resilient_properties
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/run_model_no_resilient_foods.py/#L102)
```python
.set_common_no_resilient_properties()
```

---
This function sets the common properties for the food system in a scenario where there are no resilient foods.
It uses the Scenarios class to load the necessary data and set the properties accordingly.

**Returns**

* **tuple**  : a tuple containing the Scenarios object and the constants for the food system properties

