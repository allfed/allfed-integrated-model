#


## Parameters
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/parameters.py/#L24)
```python 

```




**Methods:**


### .computeParameters
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/parameters.py/#L46)
```python
.computeParameters(
   constants, scenarios_loader
)
```


### .init_scenario
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/parameters.py/#L161)
```python
.init_scenario(
   constants, constants_for_params
)
```

---
Initialize the scenario for some constants used for the optimizer.

### .set_nutrition_per_month
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/parameters.py/#L194)
```python
.set_nutrition_per_month(
   constants, constants_for_params
)
```

---
Set the nutrition per month for the simulation.

### .set_seaweed_params
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/parameters.py/#L238)
```python
.set_seaweed_params(
   constants, constants_for_params
)
```

---
Set the seaweed parameters.

### .init_outdoor_crops
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/parameters.py/#L260)
```python
.init_outdoor_crops(
   constants, constants_for_params
)
```

---
initialize the outdoor crops parameters

### .init_stored_food
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/parameters.py/#L283)
```python
.init_stored_food(
   constants, constants_for_params, outdoor_crops
)
```


### .init_fish_params
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/parameters.py/#L296)
```python
.init_fish_params(
   constants, time_consts, constants_for_params
)
```

---
Initialize seafood parameters, not including seaweed

### .init_greenhouse_params
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/parameters.py/#L320)
```python
.init_greenhouse_params(
   time_consts, constants_for_params, outdoor_crops
)
```

---
Initialize the greenhouse parameters.

### .init_cs_params
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/parameters.py/#L357)
```python
.init_cs_params(
   time_consts, constants_for_params
)
```

---
Initialize the parameters for the cellulosic sugar model

### .init_scp_params
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/parameters.py/#L374)
```python
.init_scp_params(
   time_consts, constants_for_params
)
```

---
Initialize the parameters for single cell protein

### .init_feed_and_biofuels
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/parameters.py/#L395)
```python
.init_feed_and_biofuels(
   time_consts, constants_for_params, outdoor_crops, stored_food
)
```

---
Initialize feed and biofuels parameters.

### .init_meat_and_dairy_params
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/parameters.py/#L422)
```python
.init_meat_and_dairy_params(
   constants, time_consts, constants_for_params, feed_and_biofuels,
   outdoor_crops
)
```

---
Meat and dairy are initialized here.
NOTE: Important convention: anything pre-waste is marked so. Everything else
that could include waste should be assumed to be post-waste if not marked

### .init_grazing_params
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/parameters.py/#L458)
```python
.init_grazing_params(
   constants_for_params, time_consts, meat_and_dairy
)
```


### .init_grain_fed_meat_params
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/parameters.py/#L493)
```python
.init_grain_fed_meat_params(
   time_consts, meat_and_dairy, feed_and_biofuels, constants_for_params,
   outdoor_crops
)
```


### .init_culled_meat_params
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/parameters.py/#L574)
```python
.init_culled_meat_params(
   constants_for_params, constants, time_consts, meat_and_dairy
)
```

