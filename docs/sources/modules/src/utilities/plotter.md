#


## Plotter
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L49)
```python 

```




**Methods:**


### .plot_fig_1ab
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L54)
```python
.plot_fig_1ab(
   crs, interpreter, xlim, newtitle = '', plot_figure = True,
   add_slide_with_fig = True, description = ''
)
```


### .plot_feed
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L269)
```python
.plot_feed(
   crs, interpreter, xlim, newtitle = '', plot_figure = True,
   add_slide_with_fig = True, description = ''
)
```


### .plot_fig_1ab_updated
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L478)
```python
.plot_fig_1ab_updated(
   crs, worlds, ratios, xlim
)
```


### .helper_for_plotting_fig_3abcde
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L578)
```python
.helper_for_plotting_fig_3abcde(
   interpreter, xlim, gs, row, fig, max_y_percent
)
```


### .helper_for_plotting_fig_2abcde
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L723)
```python
.helper_for_plotting_fig_2abcde(
   ax, interpreter, xlim, title, add_ylabel = True, add_xlabel = True,
   ylim_constraint = 100000
)
```


### .plot_fig_2abcde_updated
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L828)
```python
.plot_fig_2abcde_updated(
   crs, lists_of_lists, xlim
)
```


### .plot_fig_2abcd
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L1018)
```python
.plot_fig_2abcd(
   interpreter1, interpreter2, xlim
)
```


### .plot_fig_3abcde_updated
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L1174)
```python
.plot_fig_3abcde_updated(
   results, xlim
)
```


### .plot_fig_3ab
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L1261)
```python
.plot_fig_3ab(
   monte_carlo_data, food_names, removed, added
)
```


### .plot_fig_s2abcd
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L1358)
```python
.plot_fig_s2abcd(
   interpreter1, interpreter2, xlim1, xlim2
)
```


### .plot_fig_s1abcd
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L1523)
```python
.plot_fig_s1abcd(
   crs, interpreter1, interpreter2, xlim, showplot = False
)
```


### .getylim_nutrients
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L1685)
```python
.getylim_nutrients(
   interpreter, xlim
)
```


### .plot_histogram
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L1708)
```python
.plot_histogram(
   ax, data, N, xlabel, ylabel, title
)
```


### .plot_histogram_with_boxplot
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L1717)
```python
.plot_histogram_with_boxplot(
   data, xlabel, title
)
```


### .get_people_fed_legend
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L1742)
```python
.get_people_fed_legend(
   interpreter, is_nuclear_winter
)
```


### .get_feed_biofuels_legend
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L1812)
```python
.get_feed_biofuels_legend(
   interpreter
)
```


### .plot_monthly_reductions_seasonally
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L1868)
```python
.plot_monthly_reductions_seasonally(
   ratios
)
```


### .plot_monthly_reductions_no_seasonality
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L1880)
```python
.plot_monthly_reductions_no_seasonality(
   all_months_reductions
)
```

---
Plot the reduction each month, showing the seasonal variability.

### .plot_food
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L1895)
```python
.plot_food(
   food, title
)
```

---
Plot the food generically with the 3 macronutrients.

### .plot_food_alternative
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L1953)
```python
.plot_food_alternative(
   food, title
)
```

---
Plot the food generically with the 3 macronutrients (alternative layout).

### .plot_map_of_countries_fed
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L2013)
```python
.plot_map_of_countries_fed(
   crs, world, ratio_fed, description, plot_map, create_slide
)
```


### .start_pptx
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L2057)
```python
.start_pptx(
   crs, title
)
```


### .end_pptx
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L2064)
```python
.end_pptx(
   crs, saveloc
)
```

