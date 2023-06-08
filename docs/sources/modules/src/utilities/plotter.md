#


## Plotter
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L49)
```python 

```




**Methods:**


### .plot_fig_1ab
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L61)
```python
.plot_fig_1ab(
   crs, interpreter, xlim, newtitle = '', plot_figure = True,
   add_slide_with_fig = True, description = ''
)
```

---
Plots two figures: one for food availability and one for available food macronutrition.

**Args**

* **crs** (object) : an object of class CRS
* **interpreter** (object) : an object of class Interpreter
* **xlim** (int) : the maximum limit for the x-axis
* **newtitle** (str) : the title of the plot
* **plot_figure** (bool) : whether to plot the figure or not
* **add_slide_with_fig** (bool) : whether to add a slide with the figure or not
* **description** (str) : the description of the slide to be added


**Returns**

None

### .plot_feed
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L342)
```python
.plot_feed(
   crs, interpreter, xlim, newtitle = '', plot_figure = True,
   add_slide_with_fig = True, description = ''
)
```

---
Plots feed and biofuel usage and macronutrition used.


**Args**

* **crs**  : The CRS object
* **interpreter**  : The Interpreter object
* **xlim**  : The limit of the x-axis
* **newtitle**  : The title of the plot
* **plot_figure**  : Whether to plot the figure or not
* **add_slide_with_fig**  : Whether to add slide with figure or not
* **description**  : The description of the plot


**Returns**

None


**Example**


```python

>>> plot_feed(crs, interpreter, 10, "Feed and Biofuel Usage", True, True, "Feed and Biofuel Usage plot")
```

### .plot_fig_1ab_updated
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L571)
```python
.plot_fig_1ab_updated(
   crs, worlds, ratios, xlim
)
```

---
Plots two figures (a and b) side by side, each with 5 subplots, for a total of 10 subplots.
Each subplot shows a choropleth map of a world's caloric needs ratio, with a title indicating
the world's name and the percentage of caloric needs met.

**Args**

* **crs** (str) : Coordinate reference system for the choropleth maps.
* **worlds** (dict) : A dictionary of geopandas.GeoDataFrame objects, each representing a world.
* **ratios** (dict) : A dictionary of the percentage of caloric needs met for each world.
* **xlim** (tuple) : A tuple of the minimum and maximum longitude values to display in the maps.


**Returns**

None

### .helper_for_plotting_fig_3abcde
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L690)
```python
.helper_for_plotting_fig_3abcde(
   interpreter, xlim, gs, row, fig, max_y_percent
)
```

---
This function plots the figure 3abcde for the model output.


**Args**

* **interpreter** (Interpreter) : An instance of the Interpreter class.
* **xlim** (int) : The maximum limit of the x-axis.
* **gs** (GridSpec) : The GridSpec object for the figure.
* **row** (int) : The row number of the subplot.
* **fig** (Figure) : The Figure object for the plot.
* **max_y_percent** (int) : The maximum limit of the y-axis in percentage.


**Returns**

* **GridSpec**  : The GridSpec object for the figure.
* **Figure**  : The Figure object for the plot.


### .helper_for_plotting_fig_2abcde
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L867)
```python
.helper_for_plotting_fig_2abcde(
   ax, interpreter, xlim, title, add_ylabel = True, add_xlabel = True,
   ylim_constraint = 100000
)
```

---
Helper function for plotting figures 2a, 2b, 2c, 2d, and 2e.


**Args**

* **ax** (matplotlib.axes.Axes) : The axes object to plot on.
* **interpreter** (Interpreter) : The interpreter object containing the data to plot.
* **xlim** (int) : The maximum x-axis limit.
* **title** (str) : The title of the plot.
* **add_ylabel** (bool, optional) : Whether to add a y-axis label. Defaults to True.
* **add_xlabel** (bool, optional) : Whether to add an x-axis label. Defaults to True.
* **ylim_constraint** (int, optional) : The maximum y-axis limit. Defaults to 100000.


**Returns**

* **tuple**  : A tuple containing the axes object, the legend, and the color palette.


**Example**

>>> ax, legend, pal = helper_for_plotting_fig_2abcde(ax, interpreter, xlim, title)

### .plot_fig_2abcde_updated
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L972)
```python
.plot_fig_2abcde_updated(
   crs, lists_of_lists, xlim
)
```

---
Plots a figure with multiple subplots, each containing a map and text.

**Args**

* **crs** (str) : coordinate reference system
* **lists_of_lists** (list) : a list of lists containing data to be plotted
* **xlim** (tuple) : a tuple containing the minimum and maximum x-axis limits


**Returns**

None

### .plot_fig_2abcd
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L1179)
```python
.plot_fig_2abcd(
   interpreter1, interpreter2, xlim
)
```


### .plot_fig_3abcde_updated
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L1335)
```python
.plot_fig_3abcde_updated(
   results, xlim
)
```

---
Plots a figure with 5 subplots, each containing a map and text. The maps show the
distribution of people in a given scenario, and the text shows the percentage of
people fed in that scenario.


**Args**

* **results** (dict) : A dictionary containing the results of the simulation for each
* **xlim** (tuple) : A tuple containing the minimum and maximum x-axis values for the
scenario.
plots.


**Returns**

None


**Example**


```python

>>> plot_fig_3abcde_updated(results, xlim)
```

### .plot_fig_3ab
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L1449)
```python
.plot_fig_3ab(
   monte_carlo_data, food_names, removed, added
)
```


### .plot_fig_s2abcd
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L1546)
```python
.plot_fig_s2abcd(
   interpreter1, interpreter2, xlim1, xlim2
)
```

---
Plots a figure with four subplots, each showing different food availability and macronutrition scenarios.

**Args**

* **interpreter1** (Interpreter) : an instance of the Interpreter class representing the first scenario
* **interpreter2** (Interpreter) : an instance of the Interpreter class representing the second scenario
* **xlim1** (int) : the limit for the x-axis for the first and second subplots
* **xlim2** (int) : the limit for the x-axis for the third and fourth subplots


**Returns**

None

### .plot_fig_s1abcd
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L1755)
```python
.plot_fig_s1abcd(
   crs, interpreter1, interpreter2, xlim, showplot = False
)
```

---
Plots four subplots of food availability and macronutrition before and after ASRS.

**Args**

* **crs** (object) : CRS object
* **interpreter1** (object) : Interpreter object for before ASRS
* **interpreter2** (object) : Interpreter object for after ASRS
* **xlim** (int) : The maximum limit for the x-axis
* **showplot** (bool) : Whether to show the plot or not. Default is False.


**Returns**

None

### .getylim_nutrients
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L1941)
```python
.getylim_nutrients(
   interpreter, xlim
)
```

---
Calculates the minimum and maximum values for the y-axis of a plot of nutrient data.


**Args**

* **interpreter** (Interpreter) : An instance of the Interpreter class containing nutrient data.
* **xlim** (int) : The maximum x-axis value for the plot.


**Returns**

* **list**  : A list containing the minimum and maximum values for the y-axis of the plot.


**Example**


```python

>>> interpreter.include_fat = True
>>> interpreter.include_protein = True
>>> interpreter.kcals_fed = [2000, 2100, 2200, 2300, 2400, 2500, 2600, 2700, 2800, 2900, 3000]
>>> interpreter.fat_fed = [50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
>>> interpreter.protein_fed = [100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200]
>>> getylim_nutrients(interpreter, 5)
[80, 320]
```

### .plot_histogram
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L1985)
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
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L2016)
```python
.plot_histogram_with_boxplot(
   data, xlabel, title
)
```

---
This function plots a histogram with a boxplot on top of it using seaborn library.
It also prints the 95% lower and upper bounds of the data.


**Args**

* **data** (list) : A list of numerical data to be plotted.
* **xlabel** (str) : The label for the x-axis of the histogram.
* **title** (str) : The title of the plot.


**Returns**

None


**Example**


```python

>>> xlabel = "Values"
>>> title = "Histogram with Boxplot"
>>> plot_histogram_with_boxplot(data, xlabel, title)
```

### .get_people_fed_legend
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L2059)
```python
.get_people_fed_legend(
   interpreter, is_nuclear_winter
)
```

---
Returns a list of strings representing the legend for the plot of the amount of people fed

**Args**

* **interpreter** (Interpreter) : an instance of the Interpreter class
* **is_nuclear_winter** (bool) : a boolean indicating whether the simulation includes a nuclear winter


**Returns**

* **list**  : a list of strings representing the legend for the plot of the amount of people fed


### .get_feed_biofuels_legend
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L2150)
```python
.get_feed_biofuels_legend(
   interpreter
)
```

---
Returns a list of strings representing the legend for the feed and biofuels in the simulation.


**Args**

* **interpreter** (Interpreter) : An instance of the Interpreter class.


**Returns**

* **list**  : A list of strings representing the legend for the feed and biofuels in the simulation.


**Example**


```python

>>> get_feed_biofuels_legend(interpreter)
['Cellulosic Sugar Feed', '', 'Seaweed Feed', 'Outdoor Crops consumed Feed', 'Stored food, either from before or after catastrophe Feed', 'Cellulosic Sugar Feed', 'Methane SCP Biofuels', 'Seaweed Biofuels', 'Outdoor Crops consumed Biofuels', 'Stored food, either from before or after catastrophe Biofuels']
```

### .plot_monthly_reductions_seasonally
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L2234)
```python
.plot_monthly_reductions_seasonally(
   ratios
)
```

---
Plots the fraction of crop production per month, including seasonality.


**Args**

* **ratios** (list) : A list of ratios to baseline production.


**Returns**

None


**Example**


```python

>>> plot_monthly_reductions_seasonally(ratios)
```

### .plot_monthly_reductions_no_seasonality
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L2269)
```python
.plot_monthly_reductions_no_seasonality(
   all_months_reductions
)
```

---
Plot the reduction each month, showing the seasonal variability.


**Args**

* **all_months_reductions** (list) : A list of floats representing the reduction in crop production for each month.


**Returns**

None


**Example**


```python

>>> plot_monthly_reductions_no_seasonality(all_months_reductions)
```

### .plot_food
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L2299)
```python
.plot_food(
   food, title
)
```

---
Plot the food generically with the 3 macronutrients.


**Args**

* **food** (Food) : An instance of the Food class containing the macronutrient data to be plotted.
* **title** (str) : The title of the plot.


**Returns**

* **Path**  : The path to the saved plot.


**Example**


```python

>>> plot_food(food, "Monthly Macronutrient Intake")
```

### .plot_food_alternative
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L2372)
```python
.plot_food_alternative(
   food, title
)
```

---
Plot the food generically with the 3 macronutrients (alternative layout).

**Args**

* **food** (Food) : An instance of the Food class containing the macronutrient data to be plotted.
* **title** (str) : The title of the plot.


**Returns**

* **Path**  : The path to the saved plot.


### .plot_map_of_countries_fed
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L2444)
```python
.plot_map_of_countries_fed(
   crs, world, ratio_fed, description, plot_map, create_slide
)
```

---
Plots a map of countries fed with a given ratio of minimum macronutritional needs with no trade.
Saves the plot as a png file and displays it if plot_map is True.
If create_slide is True, inserts a slide with the plot in a presentation.


**Args**

* **crs** (object) : an object with a method to insert a slide in a presentation
* **world** (GeoDataFrame) : a GeoDataFrame containing the world map
* **ratio_fed** (float) : the ratio of minimum macronutritional needs with no trade
* **description** (str) : the description of the slide to be inserted
* **plot_map** (bool) : whether to display the plot or not
* **create_slide** (bool) : whether to insert a slide or not


**Returns**

None


**Example**


```python

>>> plot_map_of_countries_fed(crs, world, 0.5, "Slide description", True, True)
```

### .start_pptx
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L2517)
```python
.start_pptx(
   crs, title
)
```

---
Initializes a PowerPoint presentation with a title slide.


**Args**

* **crs** (Course) : An instance of the Course class.
* **title** (str) : The title of the presentation.


**Returns**

None.


**Example**


```python

>>> start_pptx(crs, "My Presentation")
```

### .end_pptx
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/plotter.py/#L2542)
```python
.end_pptx(
   crs, saveloc
)
```

---
Saves a PowerPoint file and creates a directory for it if it doesn't exist.

**Args**

* **crs** (class) : an instance of the Plotter class
* **saveloc** (str) : the path to save the PowerPoint file to


**Returns**

None
