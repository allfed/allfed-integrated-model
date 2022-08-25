#


## Plotter
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L32)
```python 

```




**Methods:**


### .plot_fig_2abcd
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L225)
```python
.plot_fig_2abcd(
   interpreter1, interpreter2, xlim
)
```


### .plot_fig_3ab
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L385)
```python
.plot_fig_3ab(
   monte_carlo_data, food_names, removed, added
)
```


### .plot_fig_s1
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L482)
```python
.plot_fig_s1(
   variables, N
)
```


### .plot_fig_s2abcd
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L560)
```python
.plot_fig_s2abcd(
   interpreter1, interpreter2, xlim1, xlim2
)
```


### .getylim_nutrients
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L1126)
```python
.getylim_nutrients(
   interpreter, xlim
)
```


### .plot_histogram
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L1149)
```python
.plot_histogram(
   ax, data, N, xlabel, ylabel, title
)
```


### .plot_histogram_with_boxplot
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L1158)
```python
.plot_histogram_with_boxplot(
   data, xlabel, title
)
```


### .get_people_fed_legend
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L1183)
```python
.get_people_fed_legend(
   interpreter, is_nuclear_winter
)
```


### .plot_monthly_reductions_seasonally
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L1253)
```python
.plot_monthly_reductions_seasonally(
   ratios
)
```


### .plot_monthly_reductions_no_seasonality
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L1266)
```python
.plot_monthly_reductions_no_seasonality(
   all_months_reductions
)
```

---
Plot the reduction each month, showing the seasonal variability.

### .plot_food
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L1281)
```python
.plot_food(
   food, title
)
```

---
Plot the food generically with the 3 macronutrients.

### .plot_food_alternative
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L1339)
```python
.plot_food_alternative(
   food, title
)
```

---
Plot the food generically with the 3 macronutrients (alternative layout).
