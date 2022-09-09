#


## Plotter
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L37)
```python 

```




**Methods:**


### .helper_for_plotting_fig_3abcde
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L326)
```python
.helper_for_plotting_fig_3abcde(
   interpreter, xlim, gs, row, fig, max_y_percent
)
```


### .helper_for_plotting_fig_2abcde
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L479)
```python
.helper_for_plotting_fig_2abcde(
   ax, interpreter, xlim, title, add_ylabel = True, add_xlabel = True,
   ylim_constraint = 100000
)
```


### .plot_fig_2abcd
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L779)
```python
.plot_fig_2abcd(
   interpreter1, interpreter2, xlim
)
```


### .plot_fig_3abcde_updated
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L936)
```python
.plot_fig_3abcde_updated(
   results, xlim
)
```


### .plot_fig_3ab
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L1024)
```python
.plot_fig_3ab(
   monte_carlo_data, food_names, removed, added
)
```


### .plot_fig_s2abcd
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L1121)
```python
.plot_fig_s2abcd(
   interpreter1, interpreter2, xlim1, xlim2
)
```


### .getylim_nutrients
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L1457)
```python
.getylim_nutrients(
   interpreter, xlim
)
```


### .plot_histogram
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L1480)
```python
.plot_histogram(
   ax, data, N, xlabel, ylabel, title
)
```


### .plot_histogram_with_boxplot
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L1489)
```python
.plot_histogram_with_boxplot(
   data, xlabel, title
)
```


### .get_people_fed_legend
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L1514)
```python
.get_people_fed_legend(
   interpreter, is_nuclear_winter
)
```


### .plot_monthly_reductions_seasonally
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L1584)
```python
.plot_monthly_reductions_seasonally(
   ratios
)
```


### .plot_monthly_reductions_no_seasonality
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L1597)
```python
.plot_monthly_reductions_no_seasonality(
   all_months_reductions
)
```

---
Plot the reduction each month, showing the seasonal variability.

### .plot_food
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L1612)
```python
.plot_food(
   food, title
)
```

---
Plot the food generically with the 3 macronutrients.

### .plot_food_alternative
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L1670)
```python
.plot_food_alternative(
   food, title
)
```

---
Plot the food generically with the 3 macronutrients (alternative layout).
