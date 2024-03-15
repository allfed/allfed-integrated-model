#!/bin/bash

# Run the python script run_scenarios_from_yaml.py with all arguments passed into the bash script

# The script runs scenario(s) to determine the caloric and/or fat and/or protein supply each month over the 
# duration of the scenario(s) in accordance with settings in the specified yaml config file, and plots the results.

python3 src/scenarios/run_scenarios_from_yaml.py "$@"