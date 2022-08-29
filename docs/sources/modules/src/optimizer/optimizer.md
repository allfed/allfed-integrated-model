#


## Optimizer
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/optimizer.py/#L10)
```python 

```




**Methods:**


### .optimize
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/optimizer.py/#L14)
```python
.optimize(
   single_valued_constants, multi_valued_constants
)
```


### .add_seaweed_to_model
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/optimizer.py/#L96)
```python
.add_seaweed_to_model(
   model, variables, month
)
```


### .add_stored_food_to_model_only_first_year
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/optimizer.py/#L159)
```python
.add_stored_food_to_model_only_first_year(
   model, variables, month
)
```


### .add_stored_food_to_model
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/optimizer.py/#L216)
```python
.add_stored_food_to_model(
   model, variables, month
)
```


### .add_culled_meat_to_model
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/optimizer.py/#L274)
```python
.add_culled_meat_to_model(
   model, variables, month
)
```

---
incorporate linear constraints for culled meat consumption each month
it's like stored food, but there is a preset limit for how much can be produced

### .add_outdoor_crops_to_model_no_relocation
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/optimizer.py/#L330)
```python
.add_outdoor_crops_to_model_no_relocation(
   model, variables, month
)
```


### .add_outdoor_crops_to_model_no_storage
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/optimizer.py/#L380)
```python
.add_outdoor_crops_to_model_no_storage(
   model, variables, month
)
```


### .add_outdoor_crops_to_model
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/optimizer.py/#L425)
```python
.add_outdoor_crops_to_model(
   model, variables, month
)
```


### .add_objectives_to_model
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/optimizer.py/#L638)
```python
.add_objectives_to_model(
   model, variables, month, maximize_constraints
)
```

