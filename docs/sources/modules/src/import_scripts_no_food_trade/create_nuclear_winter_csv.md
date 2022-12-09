#


### get_crop_ratios_this_country
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/import_scripts_no_food_trade/create_nuclear_winter_csv.py/#L22)
```python
.get_crop_ratios_this_country(
   country_id, crop_macros
)
```

---
get the kcal ratios production for wheat, rice, soy, spring wheat each country
We assume some similar crops will count towards these ratios, in order to get
a better approximation of how the reduction will affect the country.

----


### get_overall_reduction
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/import_scripts_no_food_trade/create_nuclear_winter_csv.py/#L71)
```python
.get_overall_reduction(
   country_data, country_id, crop_macros
)
```

---
determine the total reduction in production using the relative reduction
in corn, rice, soy, and spring wheat

also separately assigns the grass reduction appropriately

----


### calculate_reductions
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/import_scripts_no_food_trade/create_nuclear_winter_csv.py/#L104)
```python
.calculate_reductions(
   country_data, country_id, crop_macros
)
```

---
calculate the crop reduction percentage for each year and aggregate as array

----


### clean_up_nw_csv
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/import_scripts_no_food_trade/create_nuclear_winter_csv.py/#L135)
```python
.clean_up_nw_csv(
   nw_csv, nw_csv_cols
)
```


----


### get_all_crops_correct_countries
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/import_scripts_no_food_trade/create_nuclear_winter_csv.py/#L170)
```python
.get_all_crops_correct_countries(
   input_table
)
```

---
get the columns with all the reductions for every crop, with the
countries properly aggregated (eu27+uk combined) and Taiwan reductions
equal to China's (Rutgers dataset doesn't include Taiwan as a distinct entity)
