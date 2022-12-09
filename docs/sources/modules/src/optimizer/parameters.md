#


## Parameters
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/parameters.py/#L25)
```python 

```




**Methods:**


### .computeParameters
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/parameters.py/#L47)
```python
.computeParameters(
   constants_inputs, scenarios_loader
)
```


### .init_scenario
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/parameters.py/#L187)
```python
.init_scenario(
   constants_out, constants_inputs
)
```

---
Initialize the scenario for some constants_out used for the optimizer.

### .set_nutrition_per_month
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/parameters.py/#L220)
```python
.set_nutrition_per_month(
   constants_out, constants_inputs
)
```

---
Set the nutrition per month for the simulation.

### .set_seaweed_params
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/parameters.py/#L264)
```python
.set_seaweed_params(
   constants_out, constants_inputs
)
```

---
Set the seaweed parameters.

### .init_outdoor_crops
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/parameters.py/#L286)
```python
.init_outdoor_crops(
   constants_out, constants_inputs
)
```

---
initialize the outdoor crops parameters

### .init_stored_food
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/parameters.py/#L311)
```python
.init_stored_food(
   constants_out, constants_inputs, outdoor_crops
)
```


### .init_fish_params
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/parameters.py/#L324)
```python
.init_fish_params(
   constants_out, time_consts, constants_inputs
)
```

---
Initialize seafood parameters, not including seaweed

### .init_greenhouse_params
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/parameters.py/#L348)
```python
.init_greenhouse_params(
   time_consts, constants_inputs, outdoor_crops
)
```

---
Initialize the greenhouse parameters.

### .init_cs_params
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/parameters.py/#L381)
```python
.init_cs_params(
   time_consts, constants_inputs
)
```

---
Initialize the parameters for the cellulosic sugar model

### .init_scp_params
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/parameters.py/#L398)
```python
.init_scp_params(
   time_consts, constants_inputs
)
```

---
Initialize the parameters for single cell protein

### .init_feed_and_biofuels
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/parameters.py/#L419)
```python
.init_feed_and_biofuels(
   time_consts, constants_inputs, outdoor_crops, stored_food
)
```

---
Initialize feed and biofuels parameters.

### .init_meat_and_dairy_and_feed_from_breeding
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/parameters.py/#L473)
```python
.init_meat_and_dairy_and_feed_from_breeding(
   constants_out, constants_inputs, time_consts, outdoor_crops, stored_food
)
```

---
In the case of a breeding reduction strategy rather than increased slaughter,
we first calculate the expected amount of livestock if breeding were quickly
reduced and slaughter only increased slightly, then using that we calculate the
feed they would use given the expected input animal populations over time.

### .init_meat_and_dairy_params
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/parameters.py/#L654)
```python
.init_meat_and_dairy_params(
   constants_inputs, constants_out, time_consts, feed_and_biofuels,
   outdoor_crops
)
```

---
Meat and dairy are initialized here.
NOTE: Important convention: anything pre-waste is marked so. Everything else
that could include waste should be assumed to be post-waste if not marked

### .init_grazing_params
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/parameters.py/#L690)
```python
.init_grazing_params(
   constants_inputs, time_consts, meat_and_dairy
)
```


### .init_grain_fed_meat_params
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/parameters.py/#L728)
```python
.init_grain_fed_meat_params(
   time_consts, meat_and_dairy, feed_and_biofuels, constants_inputs,
   outdoor_crops
)
```


### .init_culled_meat_params
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/parameters.py/#L813)
```python
.init_culled_meat_params(
   constants_inputs, constants_out, time_consts, meat_and_dairy
)
```

