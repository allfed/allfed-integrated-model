import os
import sys
module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
	sys.path.append(module_path)

import numpy as np
import matplotlib.pyplot as plt
from src.plotter import Plotter
from src.validate import Validator

from pulp import LpMaximize, LpProblem, LpVariable

#all the days are zero indexed, as python is zero indexed. So first Day is Day 0.

HARVEST_LOSS=15
INITIAL_SEAWEED=1000./10**4
INITIAL_AREA=1000./10**4
NEW_AREA_PER_DAY=4153/10**4
MINIMUM_DENSITY=400./10**4
MAXIMUM_DENSITY=4000./10**4
MAXIMUM_AREA=1000000./10**4/100
PRODUCTION_RATE=10

# PERSON_FATS_PER_SEAWEED_FOOD = 1
# PERSON_CALORIES_PER_SEAWEED_FOOD = 0
# PERSON_PROTEINS_PER_SEAWEED_FOOD = .3


# Human requirements

# Protein	Fat total	Saturated fats	Trans fats	Sugars
# g	g	g	g	g	g	g
# 60	2386	2386*0.15

# Per 100 grams dry, laver
# Energy kcal/100g	Protein digestibility	Protein grams	Fat total grams
# 210	0.862	34.9	1.7

NDAYS=5
# Create the model to optimize
model = LpProblem(name="optimization_nutrition", sense=LpMaximize)


#initialize variables with zero, will be overwritten
built_area=np.linspace(INITIAL_AREA,NDAYS*NEW_AREA_PER_DAY+INITIAL_AREA,NDAYS)
built_area[built_area>MAXIMUM_AREA]=MAXIMUM_AREA
seaweed_food=[0]*NDAYS
seaweed_food_after=[0]*NDAYS
seaweed_food_produced=[0]*NDAYS
seaweed_wet_on_farm=[0]*NDAYS
humans_fed_fat=[0]*NDAYS
humans_fed_protein=[0]*NDAYS
humans_fed_calories=[0]*NDAYS
density=[0]*NDAYS
max_harvest=[0]*NDAYS
maximize_constraints=[]

print(built_area)
# quit()
# Initialize the variable to maximize
z = LpVariable(name="least_nutrient_eaten_any_day", lowBound=0)

for d in range(0,NDAYS):
	
	print('day')
	print(d)

	seaweed_wet_on_farm[d] = LpVariable(name="Seaweed_Wet_On_Farm"+str(d), lowBound=0)

	# #foods
	# seaweed_food[d] = LpVariable(name="Seaweed_Food_Beginning_Day_"+str(d), lowBound=0)
	# seaweed_food_after[d] = LpVariable(name="Seaweed_Food_After_Day_"+str(d), lowBound=0)

	# # food production (using resources)
	seaweed_food_produced[d] = LpVariable(name="Seaweed_Food_Produced_During_Day_"+str(d), lowBound=0)

	# density[d] = LpVariable(name="Density"+str(d), lowBound=0)
	# max_harvest[d] = LpVariable(name="Max_Harvest"+str(d), lowBound=0)



	#total eaten
	# humans_fed_fat[d] = LpVariable(name="Humans_Fed_Fat"+str(d),lowBound=0)
	# humans_fed_protein[d] = LpVariable(name="Humans_Fed_Protein"+str(d),lowBound=0)
	# humans_fed_calories[d] = LpVariable(name="Humans_Fed_Calories"+str(d),lowBound=0)	

	#resource consumption assignment

	if(d==0): #first Day
		model += (seaweed_wet_on_farm[0] == INITIAL_SEAWEED,
			"Seaweed_Food_Amount_Beginning_Day_0_Constraint")
	else: #later Days
		model += (seaweed_wet_on_farm[d] == 
			seaweed_wet_on_farm[d-1]*(1+PRODUCTION_RATE/100.)
			- seaweed_food_produced[d],
			"Seaweed_Wet_On_Farm_"+str(d)+"_Constraint")

	# print('MAXIMUM_DENSITY/built_area')
	# print(MAXIMUM_DENSITY/built_area[d])
	model += (seaweed_wet_on_farm[d]<=MAXIMUM_DENSITY*built_area[d],
		"Seaweed_Density_"+str(d)+"_Constraint")
	# model += (max_harvest[d] <= 
	# 	seaweed_wet_on_farm[d]-seaweed_food_produced[d],
	# 	"Seaweed_Max_Harvest_"+str(d)+"_Constraint")


	#total eaten assignment

	# model += (humans_fed_fat[d] <= 
	# 	seaweed_food_eaten[d]*PERSON_FATS_PER_SEAWEED_FOOD,
	# 	"Fat_Fed_Day_"+str(d)+"_Constraint")
	# model += (humans_fed_calories[d] <= 
	# 	seaweed_food_eaten[d]*PERSON_CALORIES_PER_SEAWEED_FOOD,
	# 	"Calories_Fed_Day_"+str(d)+"_Constraint")
	# model += (humans_fed_protein[d] <= 
	# 	seaweed_food_eaten[d]*PERSON_PROTEINS_PER_SEAWEED_FOOD,
	# 	"Protein_Fed_Day_"+str(d)+"_Constraint")

	# maximizes the minimum z value
	# we maximize the minimum humans fed from any Day and either fat, protein, or calories
	if(d==NDAYS-1):
		maximizer_string="Seaweed_Produced_Day_"+str(d)+"_Objective_Constraint"
		maximize_constraints.append(maximizer_string)
		model += (z <= seaweed_food_produced[d], maximizer_string)

	# maximizer_string="Fat_Fed_Day_"+str(d)+"_Objective_Constraint"
	# maximize_constraints.append(maximizer_string)
	# model += (z <= humans_fed_fat[d], maximizer_string)

	# maximizer_string="Calories_Fed_Day_"+str(d)+"_Objective_Constraint"
	# maximize_constraints.append(maximizer_string)
	# model += (z <= humans_fed_protein[d], maximizer_string)

	# maximizer_string="Protein_Fed_Day_"+str(d)+"_Objective_Constraint"
	# maximize_constraints.append(maximizer_string)
	# model += (z <= humans_fed_calories[d], maximizer_string)
	
obj_func = z
model += obj_func

status = model.solve()
print(f"objective: {model.objective.value()}")
for var in model.variables():
	print(f"{var.name}: {var.value()}")


#double check it worked
SHOW_CONSTRAINT_CHECK=True
# print(model.constraints.items())
print('pulp reports successful optimization')
Validator.checkConstraintsSatisfied(model,status,maximize_constraints,SHOW_CONSTRAINT_CHECK)
# Plotter.plotLine(model)
