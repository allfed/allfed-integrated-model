#


## MethaneSCP
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/methane_scp.py/#L13)
```python 
MethaneSCP(
   constants_for_params
)
```




**Methods:**


### .calculate_monthly_scp_caloric_production
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/methane_scp.py/#L89)
```python
.calculate_monthly_scp_caloric_production(
   constants_for_params
)
```

---
Calculates the monthly caloric production of SCP.


**Args**

* **constants_for_params** (dict) : A dictionary containing the constants needed
for the calculation.


**Attributes**

* **production_kcals_scp_per_month_long** (list) : A list containing the monthly caloric
production of SCP.

### .calculate_scp_fat_and_protein_production
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/food_system/methane_scp.py/#L145)
```python
.calculate_scp_fat_and_protein_production()
```

---
Calculates the fat and protein production of SCP.


**Attributes**

* **production** (Food) : A Food object containing the production of SCP.

