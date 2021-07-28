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

STORED_FOOD_BEFORE_MONTH0=10

FUEL_BEFORE_MONTH0=100
FUEL_ADDED_BEFORE_MONTH2=100
FUEL_ADDED_BEFORE_MONTH3=0

FUEL_USED_PER_LEAF_FOOD=2
FUEL_USED_PER_CROPS_PLANTING=1
FOOD_PRODUCED_PER_CROPS_PLANTED=1

#each month, how many people have their nutrition satisfied for each type of food

PERSON_FATS_PER_STORED_FOOD = .3
PERSON_FATS_PER_LEAF_FOOD = 0
PERSON_FATS_PER_CROPS_FOOD = 1
PERSON_CALORIES_PER_STORED_FOOD = 1
PERSON_CALORIES_PER_LEAF_FOOD = .3
PERSON_CALORIES_PER_CROPS_FOOD = 0
PERSON_PROTEINS_PER_STORED_FOOD = 0
PERSON_PROTEINS_PER_LEAF_FOOD = 1
PERSON_PROTEINS_PER_CROPS_FOOD = .3

NMONTHS=3
# Create the model to optimize
model = LpProblem(name="optimization_nutrition", sense=LpMaximize)


#initialize variables with zero, will be overwritten
fuel=[0]*NMONTHS
fuel_after=[0]*NMONTHS
stored_food=[0]*NMONTHS
stored_food_after=[0]*NMONTHS
leaf_food=[0]*NMONTHS
leaf_food_after=[0]*NMONTHS
crops_food=[0]*NMONTHS
crops_food_after=[0]*NMONTHS
crops_food_produced=[0]*NMONTHS
crops_food_planted=[0]*NMONTHS
leaf_food_produced=[0]*NMONTHS
stored_food_eaten=[0]*NMONTHS
leaf_food_eaten=[0]*NMONTHS
crops_food_eaten=[0]*NMONTHS
humans_fed_fat=[0]*NMONTHS
humans_fed_protein=[0]*NMONTHS
humans_fed_calories=[0]*NMONTHS
maximize_constraints=[]
# Initialize the variable to maximize
z = LpVariable(name="least_food_eaten_any_month", lowBound=0)

for m in range(0,NMONTHS):
	
	print('month')
	print(m)

	#shared resources
	fuel[m] = LpVariable(name="Fuel_Beginning_Month_"+str(m), lowBound=0)
	fuel_after[m] = LpVariable(name="Fuel_After_Month_"+str(m), lowBound=0)

	#foods
	stored_food[m] = LpVariable(name="Stored_Food_Beginning_Month_"+str(m), lowBound=0)
	stored_food_after[m] = LpVariable(name="Stored_Food_After_Month_"+str(m), lowBound=0)
	leaf_food[m] = LpVariable(name="Leaf_Food_Beginning_Month_"+str(m), lowBound=0)
	leaf_food_after[m] = LpVariable(name="Leaf_Food_After_Month_"+str(m), lowBound=0)
	crops_food[m] = LpVariable(name="Crops_Food_Beginning_Month_"+str(m), lowBound=0)
	crops_food_after[m] = LpVariable(name="Crops_Food_After_Month_"+str(m), lowBound=0)

	# food production (using resources)
	leaf_food_produced[m] = LpVariable(name="Leaf_Food_Produced_During_Month_"+str(m), lowBound=0)
	crops_food_produced[m] = LpVariable(name="Crops_Food_Produced_During_Month_"+str(m), lowBound=0)
	crops_food_planted[m] = LpVariable(name="Crops_Food_Planted_During_Month_"+str(m), lowBound=0)

	# food consumption (not all food produced is necessarily consumed)
	stored_food_eaten[m] = LpVariable(name="Stored_Food_Eaten_During_Month_"+str(m), lowBound=0)
	leaf_food_eaten[m] = LpVariable(name="Leaf_Food_Eaten_During_Month_"+str(m), lowBound=0)
	crops_food_eaten[m] = LpVariable(name="Crops_Food_Eaten_During_Month_"+str(m), lowBound=0)

	#total eaten
	humans_fed_fat[m] = LpVariable(name="Humans_Fed_Fat"+str(m),lowBound=0)
	humans_fed_protein[m] = LpVariable(name="Humans_Fed_Protein"+str(m),lowBound=0)
	humans_fed_calories[m] = LpVariable(name="Humans_Fed_Calories"+str(m),lowBound=0)

	#total eaten assignment

	model += (humans_fed_fat[m] <= 
		stored_food_eaten[m]*PERSON_FATS_PER_STORED_FOOD
		+ leaf_food_eaten[m]*PERSON_FATS_PER_LEAF_FOOD
		+ crops_food_eaten[m]*PERSON_FATS_PER_CROPS_FOOD,
		"Fat_Fed_Month_"+str(m)+"_Constraint")
	model += (humans_fed_calories[m] <= 
		stored_food_eaten[m]*PERSON_CALORIES_PER_STORED_FOOD
		+ leaf_food_eaten[m]*PERSON_CALORIES_PER_LEAF_FOOD
		+ crops_food_eaten[m]*PERSON_CALORIES_PER_CROPS_FOOD,
		"Calories_Fed_Month_"+str(m)+"_Constraint")
	model += (humans_fed_protein[m] <= 
		stored_food_eaten[m]*PERSON_PROTEINS_PER_STORED_FOOD
		+leaf_food_eaten[m]*PERSON_PROTEINS_PER_LEAF_FOOD
		+crops_food_eaten[m]*PERSON_PROTEINS_PER_CROPS_FOOD,
		"Protein_Fed_Month_"+str(m)+"_Constraint")

	# maximizes the minimum z value
	# we maximize the minimum humans fed from any month and either fat, protein, or calories
	maximizer_string="Fat_Fed_Month_"+str(m)+"_Objective_Constraint"
	maximize_constraints.append(maximizer_string)
	print(model)
	print(humans_fed_fat[m])
	print(maximizer_string)
	model += (z <= humans_fed_fat[m], maximizer_string)

	maximizer_string="Calories_Fed_Month_"+str(m)+"_Objective_Constraint"
	maximize_constraints.append(maximizer_string)
	model += (z <= humans_fed_protein[m], maximizer_string)

	maximizer_string="Protein_Fed_Month_"+str(m)+"_Objective_Constraint"
	maximize_constraints.append(maximizer_string)
	model += (z <= humans_fed_calories[m], maximizer_string)



#resource consumption assignment
model += (fuel[0] <= 100, "Stored_Fuel_Amount_Beginning_Month_0")
model += (fuel_after[0] <= fuel[0]-leaf_food_produced[0]*FUEL_USED_PER_LEAF_FOOD,
	"Stored_Fuel_Amount_After_Month_0")
model += (fuel[1] <= fuel_after[0]+FUEL_ADDED_BEFORE_MONTH2,
	"Stored_Fuel_Amount_Beginning_Month_1")
model += (fuel_after[1] <= fuel[1]
	-leaf_food_produced[1]*FUEL_USED_PER_LEAF_FOOD
	-crops_food_planted[0]*FUEL_USED_PER_CROPS_PLANTING,
	"Stored_Fuel_Amount_After_Month_1")
model += (fuel[2] <= fuel_after[1]+FUEL_ADDED_BEFORE_MONTH3,
	"Stored_Fuel_Amount_Beginning_Month_2")
model += (fuel_after[2] <= fuel[2]-
	leaf_food_produced[2]*FUEL_USED_PER_LEAF_FOOD
	-crops_food_planted[1]*FUEL_USED_PER_CROPS_PLANTING,
	"Stored_Fuel_Amount_After_Month_2")


# assignment of food over time equations
model += (leaf_food[0] <= 0, "Leaf_Food_Amount_Beginning_Month_0_Constraint")
model += (leaf_food_after[0] <= leaf_food[0] - leaf_food_eaten[0]+leaf_food_produced[0], "Leaf_Food_Amount_After_Month_0_Constraint")
model += (leaf_food[1] <= leaf_food_after[0],
 "Leaf_Food_Amount_Beginning_Month_1_Constraint")
model += (leaf_food_after[1] <= leaf_food[1] - leaf_food_eaten[1]+leaf_food_produced[1],
 "Leaf_Food_Amount_After_Month_1_Constraint")
model += (leaf_food[2] <= leaf_food_after[1], "Leaf_Food_Amount_Beginning_Month_2_Constraint")
model += (leaf_food_after[2] <= leaf_food[2] - leaf_food_eaten[2]+leaf_food_produced[2], "Leaf_Food_Amount_After_Month_2_Constraint")

model += (crops_food[0] <= 0, "Crops_Food_Amount_Beginning_Month_0_Constraint")
model += (crops_food_after[0] <= crops_food[0] - crops_food_eaten[0]+crops_food_produced[0], "Crops_Food_Amount_After_Month_0_Constraint")
model += (crops_food[1] <= crops_food_after[0],
 "Crops_Food_Amount_Beginning_Month_1_Constraint")
model += (crops_food_after[1] <= crops_food[1] - crops_food_eaten[1]+crops_food_produced[1],
 "Crops_Food_Amount_After_Month_1_Constraint")
model += (crops_food[2] <= crops_food_after[1], "Crops_Food_Amount_Beginning_Month_2_Constraint")
model += (crops_food_after[2] <= crops_food[2] - crops_food_eaten[2]+crops_food_produced[2], "Crops_Food_Amount_After_Month_2_Constraint")
model += (crops_food_produced[0] <= 0,
	"Crops_Produced_During_Month_0")
model += (crops_food_produced[1] <=crops_food_planted[0]*FOOD_PRODUCED_PER_CROPS_PLANTED, #one month delay
	"Crops_Produced_During_Month_1")
model += (crops_food_produced[2] <=crops_food_planted[1]*FOOD_PRODUCED_PER_CROPS_PLANTED, #one month delay
	"Crops_Produced_During_Month_2")

#stored food assignment
model += (stored_food[0] <= STORED_FOOD_BEFORE_MONTH0, "Stored_Food_Amount_Beginning_Month_0_Constraint")
model += (stored_food_after[0] <= stored_food[0] - stored_food_eaten[0], "Stored_Food_Amount_After_Month_0_Constraint")
model += (stored_food[1] <= stored_food_after[0],
 "Stored_Food_Amount_Beginning_Month_1_Constraint")
model += (stored_food_after[1] <= stored_food[1] - stored_food_eaten[1],
 "Stored_Food_Amount_After_Month_1_Constraint")
model += (stored_food[2] <= stored_food_after[1], "Stored_Food_Amount_Beginning_Month_2_Constraint")
model += (stored_food_after[2] <= stored_food[2] - stored_food_eaten[2], "Stored_Food_Amount_After_Month_2_Constraint")

obj_func = z
model += obj_func

status = model.solve()
print(f"objective: {model.objective.value()}")
for var in model.variables():
	print(f"{var.name}: {var.value()}")


#double check it worked
SHOW_CONSTRAINT_CHECK=False
# print(model.constraints.items())
print('pulp reports successful optimization')
Validator.checkConstraintsSatisfied(model,status,maximize_constraints,SHOW_CONSTRAINT_CHECK)
Plotter.plotLine(model)