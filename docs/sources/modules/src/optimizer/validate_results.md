#


## Validator
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/validate_results.py/#L13)
```python 

```




**Methods:**


### .validate_results
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/validate_results.py/#L17)
```python
.validate_results(
   model, extracted_results, interpreted_results
)
```


### .check_constraints_satisfied
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/validate_results.py/#L30)
```python
.check_constraints_satisfied(
   model, maximize_constraints, variables
)
```

---
passing in the variables explicitly to the constraint checker here
ensures that the final values that are used in reports are explicitly
validated against all the constraints.

NOTE: THIS FUNCTION TAKES A REALLY, REALLY LONG TIME SO IT'S RUN INFREQUENTLY

### .ensure_optimizer_returns_same_as_sum_nutrients
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/validate_results.py/#L109)
```python
.ensure_optimizer_returns_same_as_sum_nutrients(
   model, interpreted_results, INCLUDE_FAT, INCLUDE_PROTEIN
)
```

---
ensure there was no major error in the optimizer or in analysis which caused
the sums reported to differ between adding up all the extracted variables and
just look at the reported result of the objective of the optimizer

### .ensure_zero_kcals_have_zero_fat_and_protein
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/validate_results.py/#L143)
```python
.ensure_zero_kcals_have_zero_fat_and_protein(
   interpreted_results
)
```

---
checks that for any month where kcals is zero for any of the foods,
then fat and protein must also be zero.

True for every food source and also for feed and biofuels independently.

### .ensure_never_nan
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/validate_results.py/#L192)
```python
.ensure_never_nan(
   interpreted_results
)
```

---
checks that the interpreter results are always defined as a real number

### .ensure_all_greater_than_or_equal_to_zero
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/validate_results.py/#L237)
```python
.ensure_all_greater_than_or_equal_to_zero(
   interpreted_results
)
```

---
checks that all the results variables are greater than or equal to zero
