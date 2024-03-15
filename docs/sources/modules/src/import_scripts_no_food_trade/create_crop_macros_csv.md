#


## CropMacros
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/import_scripts_no_food_trade/create_crop_macros_csv.py/#L17)
```python 

```




**Methods:**


### .import_nutrients_and_products
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/import_scripts_no_food_trade/create_crop_macros_csv.py/#L44)
```python
.import_nutrients_and_products()
```

---
This function imports nutrition and production data from Excel and CSV files respectively.
It returns two dataframes: products and nutrition.


**Args**

* **self** (object) : instance of the class


**Returns**

* **tuple**  : a tuple containing two dataframes: products and nutrition


### .get_kcals_matching
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/import_scripts_no_food_trade/create_crop_macros_csv.py/#L82)
```python
.get_kcals_matching(
   match_strings, products
)
```

---
Returns the sum of kcals, fat, and protein for the products that the passed in
name as a substring of the product name string.


**Args**

* **match_strings** (list) : A list of strings to match against the product names
* **products** (pandas.DataFrame) : A pandas DataFrame containing product information


**Returns**

* **float**  : The sum of kcals for the matching products


### .get_nutrients
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/import_scripts_no_food_trade/create_crop_macros_csv.py/#L122)
```python
.get_nutrients(
   products
)
```

---
Returns the sum of kcals, fat, and protein for the products passed in.


**Args**

* **products** (pandas.DataFrame) : A DataFrame containing food products and their values.


**Returns**

* **list**  : A list containing the sum of kcals, fat, and protein for the products passed in.


### .get_macros_csv
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/import_scripts_no_food_trade/create_crop_macros_csv.py/#L178)
```python
.get_macros_csv()
```

---
This function generates a stack of macronutrients that correspond to each country.
It loops through all the countries and their corresponding ISO3 codes, and for each country,
it calculates the total kcals, fat, and protein produced by all crops in that country.
It then adds this information to a numpy array and returns it.


**Returns**

* **ndarray**  : A numpy array containing the following columns:
    - iso3: The ISO3 code of the country
    - country: The name of the country
    - crop_kcals: The total kcals produced by all crops in the country
    - crop_fat: The total fat produced by all crops in the country
    - crop_protein: The total protein produced by all crops in the country

