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
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/import_utilities.py/#L369)
```python
.stack_on_list(
   list, layer
)
```

---
This function creates another layer on an existing stack of layers, or creates the first
layer in the stack. It takes in the original list and the layer to be added, and returns
the combined original and layer with the list stacked down below it.


**Example**

If we have an existing list [a,b,c] and we want to add [d,e,f] to it, we can call the
function like this:
stack_on_list([a,b,c], [d,e,f])

This will give us:
[
    [a,b,c],
    [d,e,f]
]


**Args**

* **list** (numpy.ndarray) : The original list to which the layer is to be added
* **layer** (numpy.ndarray) : The layer to be added to the original list


**Returns**

* **ndarray**  : The combined list with the layer stacked down below it


### .add_row_to_csv
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/import_utilities.py/#L402)
```python
.add_row_to_csv(
   nw_csv, country, country_name, reductions
)
```

---
Adds a row to a CSV file.


**Args**

* **nw_csv** (List[List[str]]) : The CSV file to add a row to.
* **country** (str) : The country to add to the row.
* **country_name** (str) : The name of the country to add to the row.
* **reductions** (List[float]) : A list of reduction values to add to the row.


**Returns**

* The updated CSV file with the new row added.


### .weighted_average_percentages
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/import_utilities.py/#L426)
```python
.weighted_average_percentages(
   percentages, weights
)
```

---
Calculates the weighted average of a list of percentage reductions.


**Args**

* **percentages** (list) : A list of percentage reductions.
* **weights** (list) : A list of weights corresponding to the percentages.


**Returns**

* **float**  : The weighted average of the percentages.


**Raises**

* **AssertionError**  : If the length of the percentages and weights lists are not equal.
* **AssertionError**  : If the sum of the weights is not between 0.99999 and 1.00001.

---
The function calculates the weighted average of a list of percentage reductions.
Any non-possible number is removed. The remaining are averaged.
If only non-possible numbers are included, then the result is a non-possible number.

A percentage reduction is considered non-possible if it is greater than 1e5 or less than -100.

If there are no valid percentages, the function returns 9.37e36.

### .average_percentages
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/import_utilities.py/#L499)
```python
.average_percentages(
   percentages
)
```

---
This function calculates the weighted average of a list of percentages.
The weightings are set up to be even across all percentages.


**Args**

* **percentages** (list) : A list of percentages to be averaged.


**Returns**

* **float**  : The weighted average of the percentages.


### .average_columns
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/import_utilities.py/#L525)
```python
.average_columns(
   vstack
)
```

---
This function takes a vertical stack of columns and returns a single row with the averages of each column.


**Args**

* **vstack** (numpy.ndarray) : A vertical stack of columns.


**Returns**

* **list**  : A single row with the averages of each column.


**Example**


```python

>>> vstack = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
>>> average_columns(vstack)
[4.0, 5.0, 6.0]
```

### .clean_up_eswatini
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/import_utilities.py/#L548)
```python
.clean_up_eswatini(
   nw_csv
)
```

---
This function changes the country code for Swaziland from the FAOSTAT default to the USDA
standard for compatibility with other datasets. It does this by finding the index of the
Swaziland country code in the input numpy array and changing it to the new country code
for Eswatini.


**Args**

* **nw_csv** (numpy.ndarray) : A numpy array containing country codes and other data


**Returns**

* **ndarray**  : The input numpy array with the Swaziland country code changed to Eswatini


### .import_csv
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/import_utilities.py/#L571)
```python
.import_csv(
   csv_loc, col_names, iso3_col_name
)
```

---
This function imports a CSV file into a pandas dataframe and calls the import_csv_from_df function.


**Args**

* **csv_loc** (str) : The file path of the CSV file to be imported.
* **col_names** (list) : A list of column names to be included in the dataframe.
* **iso3_col_name** (str) : The name of the column containing the ISO3 country codes.


**Returns**

* **DataFrame**  : A dataframe containing the specified columns from the CSV file.


**Example**

>>> import_csv('data.csv', ['col1', 'col2', 'col3'], 'iso3_code')

### .import_csv_from_df
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/utilities/import_utilities.py/#L593)
```python
.import_csv_from_df(
   df, iso3_col_name
)
```

---
This function takes a pandas dataframe and a column name as input and returns a dictionary
containing each table for each unique value in the specified column.


**Args**

* **df** (pandas.DataFrame) : The input dataframe
* **iso3_col_name** (str) : The name of the column containing the unique values


**Returns**

* **dict**  : A dictionary containing each table for each unique value in the specified column

