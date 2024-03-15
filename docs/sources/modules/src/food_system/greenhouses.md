#


## Greenhouses
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/greenhouses.py/#L12)
```python 
Greenhouses(
   constants_for_params
)
```




**Methods:**


### .assign_productivity_reduction_from_climate_impact
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/greenhouses.py/#L50)
```python
.assign_productivity_reduction_from_climate_impact(
   months_cycle, all_months_reductions, exponent, CROP_WASTE_COEFFICIENT
)
```

---
Assigns productivity reduction from climate impact to greenhouses.


**Args**

* **months_cycle** (list) : list of monthly cycles
* **all_months_reductions** (list) : list of all months reductions
* **exponent** (float) : exponent value
* **CROP_WASTE_COEFFICIENT** (float) : crop waste value


**Returns**

None


**Example**


```python

>>> greenhouse = Greenhouses()
>>> greenhouse.assign_productivity_reduction_from_climate_impact(
...     [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
...     [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2],
...     2,
...     10
... )
```

### .get_greenhouse_area
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/greenhouses.py/#L124)
```python
.get_greenhouse_area(
   constants_for_params, outdoor_crops
)
```

---
Calculates the area of greenhouses needed to grow crops and returns it as an array.

**Args**

* **self** (Greenhouses) : an instance of the Greenhouses class
* **constants_for_params** (dict) : a dictionary containing constants used in the simulation
* **outdoor_crops** (OutdoorCrops) : an instance of the OutdoorCrops class


**Returns**

* **ndarray**  : an array containing the area of greenhouses needed to grow crops

---
This function calculates the area of greenhouses needed to grow crops. It first checks if there is any crop
area to
grow. If there is no crop area, it returns an array of zeros. If there is crop area, it calculates the area of
greenhouses needed based on the greenhouse area multiplier and the total crop area. If the greenhouse area
multiplier is not specified, it uses the greenhouse fraction from Australia to calculate the greenhouse area. It
then assigns the productivity reduction from climate impact and returns the greenhouse area array.

### .get_greenhouse_yield_per_ha
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/greenhouses.py/#L198)
```python
.get_greenhouse_yield_per_ha(
   constants_for_params, outdoor_crops
)
```

---
Calculates the yield per hectare for greenhouses and returns the results.


**Args**

* **constants_for_params** (dict) : A dictionary containing constants for the parameters.
* **outdoor_crops** (OutdoorCrops) : An instance of the OutdoorCrops class.


**Returns**

* **tuple**  : A tuple containing the greenhouse yield per hectare for kcals, fat, and protein.


**Example**

* 10}

```python

>>> greenhouses = Greenhouses()
>>> greenhouses.ADD_GREENHOUSES = True
>>> greenhouses.NMONTHS = 12
>>> greenhouses.GH_KCALS_GROWN_PER_HECTARE = [100] * 12
>>> greenhouses.get_greenhouse_yield_per_ha(constants_for_params, outdoor_crops)
([110.0, 110.0, 110.0, 110.0, 110.0, 110.0, 110.0, 110.0, 110.0, 110.0, 110.0, 110.0],
[22.0, 22.0, 22.0, 22.0, 22.0, 22.0, 22.0, 22.0, 22.0, 22.0, 22.0, 22.0],
[33.0, 33.0, 33.0, 33.0, 33.0, 33.0, 33.0, 33.0, 33.0, 33.0, 33.0, 33.0])
```
