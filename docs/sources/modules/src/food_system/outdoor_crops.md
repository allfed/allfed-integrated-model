#


## OutdoorCrops
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/outdoor_crops.py/#L14)
```python 
OutdoorCrops(
   constants_for_params
)
```




**Methods:**


### .calculate_rotation_ratios
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/outdoor_crops.py/#L75)
```python
.calculate_rotation_ratios(
   constants_for_params
)
```

---
Calculates the rotation ratios for fat and protein based on the constants provided.
If OG_USE_BETTER_ROTATION is True, the function uses the ROTATION_IMPROVEMENTS
constants to calculate the ratios. Otherwise, the original ratios are used.

**Args**

* **constants_for_params** (dict) : A dictionary containing the constants needed for
the calculation.

### .calculate_monthly_production
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/outdoor_crops.py/#L126)
```python
.calculate_monthly_production(
   constants_for_params
)
```

---
Calculates the monthly production of outdoor crops based on various parameters.


**Args**

* **self**  : instance of the class
* **constants_for_params** (dict) : dictionary containing various constants used in the calculation


**Returns**

None


**Raises**

* **AssertionError**  : if the sum of seasonality values is not within a certain range


### .assign_increase_from_increased_cultivated_area
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/outdoor_crops.py/#L323)
```python
.assign_increase_from_increased_cultivated_area(
   constants_for_params
)
```

---
This function calculates the increase in crop yield due to an increase in cultivated area.
It updates the KCALS_GROWN array with the new values.


**Args**

* **self** (object) : The instance of the class
* **constants_for_params** (dict) : A dictionary containing the constants used in the calculation


**Returns**

None

### .assign_reduction_from_climate_impact
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/outdoor_crops.py/#L364)
```python
.assign_reduction_from_climate_impact(
   constants_for_params
)
```

---
Assigns the reduction in crop production due to climate impact for each month of the year.

**Args**

* **self**  : instance of the class
* **constants_for_params**  : dictionary containing constants used in the function


### .set_crop_production_minus_greenhouse_area
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/outdoor_crops.py/#L404)
```python
.set_crop_production_minus_greenhouse_area(
   constants_for_params, greenhouse_fraction_area
)
```

---
Calculates the crop production minus greenhouse area and sets the production attribute of the class instance.

**Args**

* **self**  : instance of the class
* **constants_for_params** (dict) : dictionary containing constants for parameters
* **greenhouse_fraction_area** (numpy.ndarray) : array containing the fraction of greenhouse area for each month


**Returns**

None
