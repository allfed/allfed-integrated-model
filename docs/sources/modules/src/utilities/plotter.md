#


## Plotter
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L38)
```python 

```




**Methods:**


### .plot_to_humans_stackplot
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L43)
```python
.plot_to_humans_stackplot(
   crs, interpreter, xlim, newtitle = '', plot_figure = True,
   add_slide_with_fig = True, description = ''
)
```


### .plot_feed
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L278)
```python
.plot_feed(
   crs, interpreter, xlim, newtitle = '', plot_figure = True,
   add_slide_with_fig = True, description = ''
)
```


### .plot_slaughter
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L491)
```python
.plot_slaughter(
   crs, interpreter, xlim, newtitle = '', plot_figure = True,
   add_slide_with_fig = True, description = ''
)
```


### .plot_fig_1ab_updated
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L654)
```python
.plot_fig_1ab_updated(
   crs, worlds, ratios, xlim
)
```


### .helper_for_plotting_fig_3abcde
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L754)
```python
.helper_for_plotting_fig_3abcde(
   interpreter, xlim, gs, row, fig, max_y_percent, ADD_SECOND_COLUMN
)
```


### .helper_for_plotting_fig_2abcde
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L895)
```python
.helper_for_plotting_fig_2abcde(
   ax, interpreter, xlim, title, add_ylabel = True, add_xlabel = True,
   ylim_constraint = 100000
)
```


### .plot_fig_2abcde_updated
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L989)
```python
.plot_fig_2abcde_updated(
   crs, lists_of_lists, xlim
)
```


### .plot_fig_2abcd
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L1185)
```python
.plot_fig_2abcd(
   interpreter1, interpreter2, xlim
)
```


### .plot_fig_3abcde_updated
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L1337)
```python
.plot_fig_3abcde_updated(
   results, xlim, ADD_SECOND_COLUMN = False
)
```


### .plot_fig_3ab
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L1421)
```python
.plot_fig_3ab(
   monte_carlo_data, food_names, removed, added
)
```


### .plot_fig_s2abcd
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L1518)
```python
.plot_fig_s2abcd(
   interpreter1, interpreter2, xlim1, xlim2
)
```


### .plot_fig_s1abcd
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L1679)
```python
.plot_fig_s1abcd(
   crs, interpreter1, interpreter2, xlim, showplot = False
)
```


### .getylim_nutrients
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L1838)
```python
.getylim_nutrients(
   interpreter, xlim
)
```


### .plot_histogram
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L1861)
```python
.plot_histogram(
   ax, data, N, xlabel, ylabel, title
)
```

---
Plots a histogram of the given data on the given axis with the given labels and title.


**Args**

* **ax** (matplotlib.axes.Axes) : The axis to plot the histogram on.
* **data** (list) : The data to plot.
* **N** (int) : The number of data points.
* **xlabel** (str) : The label for the x-axis.
* **ylabel** (str) : The label for the y-axis.
* **title** (str) : The title for the plot.


**Returns**

None


**Example**


```python

>>> data = [1, 2, 3, 4, 5]
>>> N = 5
>>> xlabel = "X Label"
>>> ylabel = "Y Label"
>>> title = "Title"
>>> plot_histogram(ax, data, N, xlabel, ylabel, title)
```

### .plot_histogram_with_boxplot
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L1891)
```python
.plot_histogram_with_boxplot(
   data, xlabel, title
)
```


### .get_people_fed_legend
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L1916)
```python
.get_people_fed_legend(
   interpreter, is_nuclear_winter
)
```


### .get_feed_biofuels_legend
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L1983)
```python
.get_feed_biofuels_legend(
   interpreter
)
```


### .plot_monthly_reductions_seasonally
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L2039)
```python
.plot_monthly_reductions_seasonally(
   ratios
)
```


### .plot_monthly_reductions_no_seasonality
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L2051)
```python
.plot_monthly_reductions_no_seasonality(
   all_months_reductions
)
```

---
Plot the reduction each month, showing the seasonal variability.

### .plot_food
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L2066)
```python
.plot_food(
   food, title
)
```

---
Plot the food generically with the 3 macronutrients.

### .plot_food_alternative
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L2130)
```python
.plot_food_alternative(
   food, title
)
```

---
Plot the food generically with the 3 macronutrients (alternative layout).

### .plot_map_of_countries_fed
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L2196)
```python
.plot_map_of_countries_fed(
   crs, world, ratio_fed, description, plot_map, create_slide
)
```


### .start_pptx
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L2240)
```python
.start_pptx(
   crs, title
)
```


### .end_pptx
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L2247)
```python
.end_pptx(
   crs, saveloc
)
```

