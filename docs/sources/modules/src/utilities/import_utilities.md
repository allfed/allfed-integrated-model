#


## ImportUtilities
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/import_utilities.py/#L5)
```python 
ImportUtilities()
```


---
This class contains methods for importing data from various sources.


**Methods:**


### .stack_on_list
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/import_utilities.py/#L333)
```python
.stack_on_list(
   list, layer
)
```

---
create another layer on an existing stack of layers, or create the first
layer in the stack

example: adding [d,e,f] to a stack

[
[a,b,c]
---
]

gives you

[
    [a,b,c],
    [d,e,f]
]

gets: the original list and the layer
returns: the combined original and layer with the list stacked down below it

### .add_row_to_csv
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/import_utilities.py/#L362)
```python
.add_row_to_csv(
   nw_csv, country, country_name, reductions
)
```


### .weighted_average_percentages
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/import_utilities.py/#L373)
```python
.weighted_average_percentages(
   percentages, weights
)
```

---
create a weighted average of percentages

creates an average for a list of percentage reductions.
Any non-possible number is removed. The remaining are averaged.
If only non-possible numbers are included, then the result is a non-possible number

9.37e36 is returned if things are not valid

### .average_percentages
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/import_utilities.py/#L423)
```python
.average_percentages(
   percentages
)
```

---
set up even weightings for the weighted average

### .average_columns
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/import_utilities.py/#L436)
```python
.average_columns(
   vstack
)
```

---
average all the columns and return the result as a row

gets: vertical stack of columns

returns: a single row with the averages

### .clean_up_eswatini
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/import_utilities.py/#L451)
```python
.clean_up_eswatini(
   nw_csv
)
```

---
change the swaziland country code from the FAOSTAT default to the USDA
standard for compatibility with other datasets

### .import_csv
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/import_utilities.py/#L462)
```python
.import_csv(
   csv_loc, col_names, iso3_col_name
)
```

---
import the csv and load into a dictionary
