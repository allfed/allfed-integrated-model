#


## Validator
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/validate_results.py/#L13)
```python 
Validator()
```




**Methods:**


### .validate_results
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/validate_results.py/#L14)
```python
.validate_results(
   results
)
```

---
Validates the results of a simulation by checking if the output is within a certain range.

**Args**

* **results** (list) : A list of floats representing the output of a simulation.


**Returns**

* **bool**  : True if the output is within the range, False otherwise.


### .validate_results
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/validate_results.py/#L14)
```python
.validate_results(
   results
)
```

---
Validates the results of a simulation by checking if the output is within a certain range.

**Args**

* **results** (list) : A list of floats representing the output of a simulation.


**Returns**

* **bool**  : True if the output is within the range, False otherwise.


### .check_constraints_satisfied
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/validate_results.py/#L67)
```python
.check_constraints_satisfied(
   model, maximize_constraints, variables
)
```

---
This function checks if all constraints are satisfied by the final values of the variables.
It takes a really long time to run, so it's run infrequently.


**Args**

* **model** (pulp.LpProblem) : The optimization model
* **maximize_constraints** (list) : A list of constraints to maximize
* **variables** (list) : A list of variables to check constraints against


**Returns**

None


**Raises**

* **AssertionError**  : If a constraint is not satisfied


### .ensure_optimizer_returns_same_as_sum_nutrients
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/validate_results.py/#L154)
```python
.ensure_optimizer_returns_same_as_sum_nutrients(
   model, interpreted_results, INCLUDE_FAT, INCLUDE_PROTEIN
)
```

---
Ensure that there was no major error in the optimizer or in analysis which caused
the sums reported to differ between adding up all the extracted variables and
just looking at the reported result of the objective of the optimizer.


**Args**

* **model**  : The optimization model
* **interpreted_results**  : The interpreted results of the optimization model
* **INCLUDE_FAT**  : A boolean indicating whether to include fat in the results
* **INCLUDE_PROTEIN**  : A boolean indicating whether to include protein in the results


**Returns**

None


**Raises**

* **AssertionError**  : If the optimizer and the extracted results do not match


### .ensure_zero_kcals_have_zero_fat_and_protein
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/validate_results.py/#L200)
```python
.ensure_zero_kcals_have_zero_fat_and_protein(
   interpreted_results
)
```

---
Checks that for any month where kcals is zero for any of the foods,
then fat and protein must also be zero.


**Args**

* **interpreted_results** (InterpretedResults) : An instance of the InterpretedResults class


**Returns**

None

---
Notes:
    This function is called to ensure that the kcals, fat and protein values are consistent
    for each food source, feed and biofuels independently.


**Raises**

* **AssertionError**  : If the kcals value is zero but the fat or protein value is non-zero.


### .ensure_never_nan
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/validate_results.py/#L250)
```python
.ensure_never_nan(
   interpreted_results
)
```

---
This function checks that the interpreter results are always defined as a real number.
It does this by calling the make_sure_not_nan() method on each of the interpreted_results attributes.
If any of the attributes contain NaN values, an exception will be raised.


**Args**

* **interpreted_results** (InterpretedResults) : An instance of the InterpretedResults class.


**Raises**

* **ValueError**  : If any of the interpreted_results attributes contain NaN values.


**Returns**

None

### .ensure_all_greater_than_or_equal_to_zero
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/optimizer/validate_results.py/#L281)
```python
.ensure_all_greater_than_or_equal_to_zero(
   interpreted_results
)
```

---
Checks that all the results variables are greater than or equal to zero.

**Args**

* **interpreted_results** (InterpretedResults) : An instance of the InterpretedResults class


**Raises**

* **AssertionError**  : If any of the results variables are less than zero

