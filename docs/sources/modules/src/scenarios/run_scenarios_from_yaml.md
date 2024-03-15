#


### run_scenarios_from_yaml
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/run_scenarios_from_yaml.py/#L43)
```python
.run_scenarios_from_yaml(
   config_data, show_country_figures, show_map_figures, web_interface
)
```

---
Run the scenario in a loop, for each scenario specified, and using all data defined from the scenarios config file

----


### load_config_data
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/run_scenarios_from_yaml.py/#L90)
```python
.load_config_data(
   yaml_filename
)
```

---
Load the configuration data for the scenarios from a YAML file in the "scenarios/" directory.

----


### print_usage_message
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/run_scenarios_from_yaml.py/#L103)
```python
.print_usage_message(
   repo_root
)
```


----


### get_input_args
[source](https://github.com/allfed/allfed-integrated-model/blob/master/src/scenarios/run_scenarios_from_yaml.py/#L117)
```python
.get_input_args(
   args
)
```

---
Get the input arguments from the command line.
Print an error message if usage is incorrect.
