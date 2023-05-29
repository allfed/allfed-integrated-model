#


### get_crop_ratios_this_country
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/import_scripts_no_food_trade/create_nuclear_winter_csv.py/#L22)
```python
.get_crop_ratios_this_country(
   country_id, crop_macros
)
```

---
This function calculates the kcal ratios production for wheat, rice, soy, and spring wheat for each country.
We assume some similar crops will count towards these ratios, in order to get a better approximation of how the reduction will affect the country.


**Args**

* **country_id** (str) : The country ID for which the crop ratios are to be calculated.
* **crop_macros** (CropMacros) : An instance of the CropMacros class.


**Returns**

* **dict**  : A dictionary containing the crop ratios for the given country.


**Raises**

* **AssertionError**  : If the sum of relevant kcals is not between 0 and kcals_check.


----


### get_overall_reduction
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/import_scripts_no_food_trade/create_nuclear_winter_csv.py/#L93)
```python
.get_overall_reduction(
   country_data, country_id, crop_macros
)
```

---
This function determines the total reduction in production using the relative reduction
in corn, rice, soy, and spring wheat. It also separately assigns the grass reduction appropriately.


**Args**

* **country_data** (pandas.DataFrame) : A pandas dataframe containing the data for the country
* **country_id** (str) : The id of the country
* **crop_macros** (pandas.DataFrame) : A pandas dataframe containing the crop macros data


**Returns**

* **dict**  : A dictionary containing the average yearly reduction for crop production


----


### calculate_reductions
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/import_scripts_no_food_trade/create_nuclear_winter_csv.py/#L143)
```python
.calculate_reductions(
   country_data, country_id, crop_macros
)
```

---
Calculate the crop reduction percentage for each year and aggregate as array.


**Args**

* **country_data** (dict) : A dictionary containing data for a specific country.
* **country_id** (str) : A string representing the ID of the country.
* **crop_macros** (dict) : A dictionary containing crop macro data.


**Returns**

* **list**  : A list of crop and grass reduction percentages for each year.


**Example**

* {'year1': 100, 'year2': 90, 'year3': 80, 'year4': 70, 'year5': 60,
* 50, 'year7': 40, 'year8': 30, 'year9': 20, 'year10': 10},
* {'year1': 100, 'year2': 90, 'year3': 80, 'year4': 70, 'year5': 60,
* 50, 'year7': 40, 'year8': 30, 'year9': 20, 'year10': 10}}
* 0.5, 'crop_reduction_year2': 0.6, 'crop_reduction_year3': 0.7,
* 0.8, 'crop_reduction_year5': 0.9, 'crop_reduction_year6': 1.0,
* 1.1, 'crop_reduction_year8': 1.2, 'crop_reduction_year9': 1.3,
* 1.4, 'grasses_reduction_year1': 0.5, 'grasses_reduction_year2': 0.6,
* 0.7, 'grasses_reduction_year4': 0.8, 'grasses_reduction_year5': 0.9,
* 1.0, 'grasses_reduction_year7': 1.1, 'grasses_reduction_year8': 1.2,
* 1.3, 'grasses_reduction_year10': 1.4}

```python

>>> calculate_reductions(country_data, country_id, crop_macros)
[0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4]
```

----


### clean_up_nw_csv
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/import_scripts_no_food_trade/create_nuclear_winter_csv.py/#L201)
```python
.clean_up_nw_csv(
   nw_csv, nw_csv_cols
)
```

---
This function takes in a nuclear winter csv file and its columns, cleans up the data, and returns a pandas dataframe.


**Args**

* **nw_csv** (pandas.DataFrame) : The nuclear winter csv file to be cleaned up.
* **nw_csv_cols** (list) : The columns of the nuclear winter csv file.


**Returns**

* **DataFrame**  : The cleaned up nuclear winter csv file.


----


### get_all_crops_correct_countries
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/import_scripts_no_food_trade/create_nuclear_winter_csv.py/#L252)
```python
.get_all_crops_correct_countries(
   input_table
)
```

---
This function takes in a table of crop data for different countries and returns the columns with all the reductions for every crop, with the
countries properly aggregated (eu27+uk combined) and Taiwan reductions equal to China's (Rutgers dataset doesn't include Taiwan as a distinct entity)


**Args**

* **input_table** (dict) : A dictionary containing crop data for different countries


**Returns**

* **tuple**  : A tuple containing two lists. The first list contains tuples of country IDs and names. The second list contains the reductions for all crops for each country.


**Raises**

* **ValueError**  : If there is missing data for a country

