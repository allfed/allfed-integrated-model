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

#all the months are zero indexed, as python is zero indexed. So first month is month 0.
#assumes built area scales up with no tradeoffs
#used area 

STORED_FOOD_BEFORE_MONTH0=10
SEAWEED_FOOD_BEFORE_MONTH0=10

BUILT_AREA_BEFORE_MONTH0=100
BUILT_AREA_ADDED_MONTHLY=100

FOOD_PRODUCED_PER_SEAWEED_PLANTED=2

#each month, how many people have their nutrition satisfied for each type of food

PERSON_FATS_PER_STORED_FOOD = .3
PERSON_FATS_PER_SEAWEED_FOOD = 1
PERSON_CALORIES_PER_STORED_FOOD = 1
PERSON_CALORIES_PER_SEAWEED_FOOD = 0
PERSON_PROTEINS_PER_STORED_FOOD = 0
PERSON_PROTEINS_PER_SEAWEED_FOOD = .3

NMONTHS=3
# Create the model to optimize
model = LpProblem(name="optimization_nutrition", sense=LpMaximize)


#initialize variables with zero, will be overwritten
built_area=[0]*NMONTHS
built_area_after=[0]*NMONTHS
stored_food=[0]*NMONTHS
stored_food_after=[0]*NMONTHS
seaweed_food=[0]*NMONTHS
seaweed_food_after=[0]*NMONTHS
seaweed_food_produced=[0]*NMONTHS
seaweed_food_planted=[0]*NMONTHS
stored_food_eaten=[0]*NMONTHS
seaweed_food_eaten=[0]*NMONTHS
humans_fed_fat=[0]*NMONTHS
humans_fed_protein=[0]*NMONTHS
humans_fed_calories=[0]*NMONTHS
maximize_constraints=[]
# Initialize the variable to maximize
z = LpVariable(name="least_nutrient_eaten_any_month", lowBound=0)

for m in range(0,NMONTHS):
	
	print('month')
	print(m)

	#shared resources
	built_area[m] = LpVariable(name="Built_Area_Beginning_Month_"+str(m), lowBound=0)
	built_area_after[m] = LpVariable(name="Built_Area_After_Month_"+str(m), lowBound=0)

	#foods
	stored_food[m] = LpVariable(name="Stored_Food_Beginning_Month_"+str(m), lowBound=0)
	stored_food_after[m] = LpVariable(name="Stored_Food_After_Month_"+str(m), lowBound=0)
	seaweed_food[m] = LpVariable(name="Seaweed_Food_Beginning_Month_"+str(m), lowBound=0)
	seaweed_food_after[m] = LpVariable(name="Seaweed_Food_After_Month_"+str(m), lowBound=0)

	# food production (using resources)
	seaweed_food_produced[m] = LpVariable(name="Seaweed_Food_Produced_During_Month_"+str(m), lowBound=0)
	seaweed_food_planted[m] = LpVariable(name="Seaweed_Food_Planted_During_Month_"+str(m), lowBound=0)

	# food consumption (not all food produced is necessarily consumed)
	stored_food_eaten[m] = LpVariable(name="Stored_Food_Eaten_During_Month_"+str(m), lowBound=0)
	seaweed_food_eaten[m] = LpVariable(name="Seaweed_Food_Eaten_During_Month_"+str(m), lowBound=0)

	#total eaten
	humans_fed_fat[m] = LpVariable(name="Humans_Fed_Fat"+str(m),lowBound=0)
	humans_fed_protein[m] = LpVariable(name="Humans_Fed_Protein"+str(m),lowBound=0)
	humans_fed_calories[m] = LpVariable(name="Humans_Fed_Calories"+str(m),lowBound=0)	

	#resource consumption assignment

	if(m==0): #first month
		model += (built_area[0] <= BUILT_AREA_BEFORE_MONTH0, 
			"Built_Area_Amount_Beginning_Month_0_Constraint")
		model += (stored_food[0] <= STORED_FOOD_BEFORE_MONTH0,
			"Stored_Food_Amount_Beginning_Month_0_Constraint")
		model += (seaweed_food[0] <= SEAWEED_FOOD_BEFORE_MONTH0,
			"Seaweed_Food_Amount_Beginning_Month_0_Constraint")
	else: #later months
		model += (built_area[m] <= built_area_after[m-1]+BUILT_AREA_ADDED_MONTHLY,
			"Built_Area_Amount_Beginning_Month_"+str(m)+"_Constraint")
		model += (stored_food[m] <= stored_food_after[m-1],
			"Stored_Food_Amount_Beginning_Month_"+str(m)+"_Constraint")

	model += (built_area_after[m] <= built_area[m],
		"Built_Area_Amount_After_Month_"+str(m)+"_Constraint")
	model += (stored_food_after[m] <= stored_food[m] - stored_food_eaten[m],
		"Stored_Food_Amount_After_Month_"+str(m)+"_Constraint")
	model += (seaweed_food_after[m] <= 
		seaweed_food[m] 
		- seaweed_food_eaten[m]
		+ seaweed_food_produced[m]
		- seaweed_food_planted[m],
		"Seaweed_Food_Amount_After_Month_"+str(m)+"_Constraint")

	model += (seaweed_food_produced[m] <=seaweed_food_planted[m-1]*FOOD_PRODUCED_PER_SEAWEED_PLANTED, #one month delay
		"Seaweed_Produced_During_Month_"+str(m))


	#total eaten assignment

	model += (humans_fed_fat[m] <= 
		stored_food_eaten[m]*PERSON_FATS_PER_STORED_FOOD
		+ seaweed_food_eaten[m]*PERSON_FATS_PER_SEAWEED_FOOD,
		"Fat_Fed_Month_"+str(m)+"_Constraint")
	model += (humans_fed_calories[m] <= 
		stored_food_eaten[m]*PERSON_CALORIES_PER_STORED_FOOD
		+ seaweed_food_eaten[m]*PERSON_CALORIES_PER_SEAWEED_FOOD,
		"Calories_Fed_Month_"+str(m)+"_Constraint")
	model += (humans_fed_protein[m] <= 
		stored_food_eaten[m]*PERSON_PROTEINS_PER_STORED_FOOD
		+seaweed_food_eaten[m]*PERSON_PROTEINS_PER_SEAWEED_FOOD,
		"Protein_Fed_Month_"+str(m)+"_Constraint")

	# maximizes the minimum z value
	# we maximize the minimum humans fed from any month and either fat, protein, or calories
	maximizer_string="Fat_Fed_Month_"+str(m)+"_Objective_Constraint"
	maximize_constraints.append(maximizer_string)
	model += (z <= humans_fed_fat[m], maximizer_string)

	maximizer_string="Calories_Fed_Month_"+str(m)+"_Objective_Constraint"
	maximize_constraints.append(maximizer_string)
	model += (z <= humans_fed_protein[m], maximizer_string)

	maximizer_string="Protein_Fed_Month_"+str(m)+"_Objective_Constraint"
	maximize_constraints.append(maximizer_string)
	model += (z <= humans_fed_calories[m], maximizer_string)
	
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
Plotter.plotLine(model)