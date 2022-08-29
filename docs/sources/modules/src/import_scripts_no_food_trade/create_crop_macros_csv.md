#


## CropMacros
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/import_scripts_no_food_trade/create_crop_macros_csv.py/#L17)
```python 

```




**Methods:**


### .import_nutrients_and_products
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/import_scripts_no_food_trade/create_crop_macros_csv.py/#L37)
```python
.import_nutrients_and_products()
```


### .get_kcals_matching
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/import_scripts_no_food_trade/create_crop_macros_csv.py/#L62)
```python
.get_kcals_matching(
   match_strings, products
)
```

---
Returns the sum of kcals, fat, and protein for the products that the passed in
name as a substring of the product name string.

### .get_nutrients
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/import_scripts_no_food_trade/create_crop_macros_csv.py/#L83)
```python
.get_nutrients(
   products
)
```

---
Returns the sum of kcals, fat, and protein for the products passed in.

### .get_macros_csv
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/import_scripts_no_food_trade/create_crop_macros_csv.py/#L127)
```python
.get_macros_csv()
```

---
get the stack of macronutrients that correspond to each countryd

### .clean_up_macros_csv
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/import_scripts_no_food_trade/create_crop_macros_csv.py/#L167)
```python
.clean_up_macros_csv(
   macros_csv
)
```

