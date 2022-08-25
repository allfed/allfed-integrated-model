#


## CropMacros
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/import_scripts_no_food_trade/create_crop_macros_csv.py/#L16)
```python 

```




**Methods:**


### .import_nutrients_and_products
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/import_scripts_no_food_trade/create_crop_macros_csv.py/#L32)
```python
.import_nutrients_and_products()
```


### .get_kcals_matching
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/import_scripts_no_food_trade/create_crop_macros_csv.py/#L57)
```python
.get_kcals_matching(
   match_strings, products
)
```

---
Returns the sum of kcals, fat, and protein for the products that the passed in
name as a substring of the product name string.

### .get_nutrients
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/import_scripts_no_food_trade/create_crop_macros_csv.py/#L78)
```python
.get_nutrients(
   products
)
```

---
Returns the sum of kcals, fat, and protein for the products passed in.

### .get_macros_csv
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/import_scripts_no_food_trade/create_crop_macros_csv.py/#L122)
```python
.get_macros_csv()
```

---
get the stack of macronutrients that correspond to each countryd

### .clean_up_macros_csv
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/import_scripts_no_food_trade/create_crop_macros_csv.py/#L162)
```python
.clean_up_macros_csv(
   macros_csv
)
```

