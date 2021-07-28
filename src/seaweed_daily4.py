import os
import sys
module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
	sys.path.append(module_path)

import numpy as np
import matplotlib.pyplot as plt
from src.plotter import Plotter
from src.validate import Validator

import pulp
from pulp import LpMaximize, LpProblem, LpVariable

#all the days are zero indexed, as python is zero indexed. So first Day is Day 0.

# HARVEST_LOSS=15
# INITIAL_SEAWEED=1000./10**4
# INITIAL_AREA=1000./10**4
# NEW_AREA_PER_DAY=4153/10**4
# MINIMUM_DENSITY=400./10**4
# MAXIMUM_DENSITY=4000./10**4
# MAXIMUM_AREA=1000000./10**4/100
# PRODUCTION_RATE=10

#units: 1000 tons mass, 1000 km^2 area

HARVEST_LOSS=15
INITIAL_SEAWEED=1#1000#./10**4
INITIAL_AREA=1#1000./10**4
NEW_AREA_PER_DAY=4.153#4153/10**4
MINIMUM_DENSITY=400
MAXIMUM_DENSITY=4000
MAXIMUM_AREA=1000
PRODUCTION_RATE=10

# INITIAL_SEAWEED=1#1000#./10**4
# INITIAL_AREA=4#1000./10**4
# NEW_AREA_PER_DAY=2#4153/10**4
# MAXIMUM_DENSITY=1
# MAXIMUM_AREA=80
# PRODUCTION_RATE=100

# PERSON_FATS_PER_SEAWEED_FOOD = 1
# PERSON_CALORIES_PER_SEAWEED_FOOD = 0
# PERSON_PROTEINS_PER_SEAWEED_FOOD = .3

spreadsheet=[1000,1100,1210,1331,1464,1611,1772,1949,2144,2358,2594,2853,3138,3452,3797,4177,4595,5054,5560,6116,6727,7400,8140,8954,9850,10835,11918,13110,14421,15863,17449,19194,21114,23225,25548,28102,30913,34004,37404,41145,45259,49785,54764,60240,66264,72890,80180,88197,97017,106719,117391,129130,142043,156247,171872,189059,207965,228762,251638,276801,304482,334930,368423,405265,445792,490371,539408,593349,652683,717952,789747,868722,955594,1051153,1156269,1271895,1399085,1538993,1692893,1862182,2048400,2253240,2478564,2726421,2999063,3298969,3628866,3991753,3792289,4171517,4588669,5047536,5552290,6107519,6718271,7390098,8129107,8942018,9836220,10819842,11901826,13092009,14401210,15841331,17425464,19168010,21084811,23193292,25512621,28063884,30870272,33957299,37353029,35493925,39043318,42947650,47242415,51966656,57163322,62879654,69167619,76084381,83692820,92062102,101268312,111395143,122534657,134788123,148266935,163093629,179402992]
# Human requirements

no_loss_spreadsheet=[1000,1100,1210,1331,1464,1611,1772,1949,2144,2358,2594,2853,3138,3452,3797,4177,4595,5054,5560,6116,6727,7400,8140,8954,9850,10835,11918,13110,14421,15863,17449,19194,21114,23225,25548,28102,30913,34004,37404,41145,45259,49785,54764,60240,66264,72890,80180,88197,97017,106719,117391,129130,142043,156247,171872,189059,207965,228762,251638,276801,304482,334930,368423,405265,445792,490371,539408,593349,652683,717952,789747,868722,955594,1051153,1156269,1271895,1399085,1538993,1692893,1862182,2048400,2253240,2478564,2726421,2999063,3298969,3628866,3991753,4390928,4830021,5313023,5844325,6428757,7071633,7778796,8556676,9412344,10353578,11388936,12527829,13780612,15158674,16674541,18341995,20176195,22193814,24413195,26854515,29539966,32493963,35743359,39317695,43249465,47574411,52331852,57565038,63321541,69653696,76619065,84280972,92709069,101979976,112177973,123395771,135735348,149308882,164239771,180663748,198730123,218603135,240463448]# Protein	Fat total	Saturated fats	Trans fats	Sugars
# g	g	g	g	g	g	g
# 60	2386	2386*0.15

# Per 100 grams dry, laver
# Energy kcal/100g	Protein digestibility	Protein grams	Fat total grams
# 210	0.862	34.9	1.7

NDAYS=120

# Create the model to optimize
model = LpProblem(name="optimization_nutrition", sense=LpMaximize)


#initialize variables with zero, will be overwritten
built_area=np.linspace(INITIAL_AREA,(NDAYS-1)*NEW_AREA_PER_DAY+INITIAL_AREA,NDAYS)
built_area[built_area>MAXIMUM_AREA]=MAXIMUM_AREA
seaweed_food_produced=[0]*NDAYS
seaweed_wet_on_farm=[0]*NDAYS
density=[0]*NDAYS
used_area=[0]*NDAYS
is_harvest=[0]*NDAYS
maximize_constraints=[]

print(built_area)
# quit()
# Initialize the variable to maximize
z = LpVariable(name="least_nutrient_eaten_any_day", lowBound=0)

allconstraints=[z]

for d in range(0,NDAYS):
	is_harvest[d] = LpVariable("Is_Harvest_"+str(d)+"_Variable",0,1,cat='Binary')
	print('day')
	print(d)
	print(MAXIMUM_DENSITY*built_area[d])
	# if(d%30=0):
	# 	used_area[d] = built_area[d]
	# 	#incorporate loss from inefficiency
	# 	#amount transferred
	# 	seaweed_wet_on_farm[d] = LpVariable("Seaweed_Wet_On_Farm"+str(d)+"_Variable", INITIAL_SEAWEED, MAXIMUM_DENSITY*built_area[d])
	# 	built_area[d]
	# else:
	seaweed_wet_on_farm[d] = LpVariable("Seaweed_Wet_On_Farm_"+str(d)+"_Variable", INITIAL_SEAWEED, MAXIMUM_DENSITY*built_area[d])
	#foods
	# seaweed_food[d] = LpVariable(name="Seaweed_Food_Beginning_Day_"+str(d), lowBound=0)
	# seaweed_food_after[d] = LpVariable(name="Seaweed_Food_After_Day_"+str(d), lowBound=0)

	# food production (using resources)
	# seaweed_food_produced[d] = LpVariable(name="Seaweed_Food_Produced_During_Day_"+str(d)+"_Variable", lowBound=0)

	# density[d] = LpVariable(name="Density"+str(d), lowBound=0)
	# max_harvest[d] = LpVariable(name="Max_Harvest"+str(d), lowBound=0)

	used_area[d] = LpVariable("Used_Area_"+str(d)+"_Variable", INITIAL_AREA,built_area[d])
	#each month, move all the seaweed over to built area

	#total eaten
	# humans_fed_fat[d] = LpVariable(name="Humans_Fed_Fat"+str(d),lowBound=0)
	# humans_fed_protein[d] = LpVariable(name="Humans_Fed_Protein"+str(d),lowBound=0)
	# humans_fed_calories[d] = LpVariable(name="Humans_Fed_Calories"+str(d),lowBound=0)	

	#resource consumption assignment

	if(d==0): #first Day
		model += (seaweed_wet_on_farm[0] == INITIAL_SEAWEED,
			"Seaweed_Wet_On_Farm_0_Constraint")
		model += (used_area[0] == INITIAL_SEAWEED,
			"Used_Area_0_Constraint")
	else: #later Days
		model += (seaweed_wet_on_farm <= used_area[d]*MAXIMUM_DENSITY,
			"Used_Area_"+str(d)+"_Constraint")
		model += (used_area[d]-used_area[d-1]>=is_harvest[d]*INITIAL_AREA,
			"Is_Harvest_Lower_"+str(d)+"_Constraint")
		model += (used_area[d]-used_area[d-1]<=is_harvest[d]*(MAXIMUM_AREA-INITIAL_AREA),
			"Is_Harvest_Upper_"+str(d)+"_Constraint")
		model += (used_area[d]-used_area[d-1]<=MAXIMUM_AREA-INITIAL_AREA,
			"Is_Harvest_Upper_"+str(d)+"_Constraint")
		loss>=is_harvest

		model += (seaweed_wet_on_farm[d] == 
			seaweed_wet_on_farm[d-1]*(1+PRODUCTION_RATE/100.)
			# - seaweed_food_produced[d]
			- (used_area[d]-used_area[d-1])*MINIMUM_DENSITY*(HARVEST_LOSS/100),
			- (seaweed_wet_on_farm[d-1]-used_area[d-1]*MINIMUM_DENSITY)*(HARVEST_LOSS/100),
			"Seaweed_Wet_On_Farm_"+str(d)+"_Constraint")


	allconstraints.append(is_harvest[d])
	allconstraints.append(used_area[d])
	allconstraints.append(seaweed_wet_on_farm[d])

	# model += (seaweed_wet_on_farm[d]<=MAXIMUM_DENSITY*built_area[d],
	# 	"Seaweed_Density_"+str(d)+"_Constraint")


	# model += (0 <= 
	# 	seaweed_wet_on_farm[d]-built_area[d]*MAXIMUM_DENSITY,
	# 	"Seaweed_Density_"+str(d)+"_Constraint")


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
		maximizer_string="Seaweed_Wet_On_Farm_"+str(d)+"_Objective_Constraint"
		maximize_constraints.append(maximizer_string)
		# model += (z == seaweed_food_produced[d], maximizer_string)
		model += (z == seaweed_wet_on_farm[d], maximizer_string)
	# allconstraints.append(seaweed_wet_on_farm[d])

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

status = model.solve(pulp.PULP_CBC_CMD(msg=1))
print(f"objective: {model.objective.value()}")
for var in model.variables():
	print(f"{var.name}: {var.value()}")

print('')

seaweed_wet_on_farm_vals=[]
print('seaweed wet on farm')
for d in range(0,NDAYS):
	val=seaweed_wet_on_farm[d]
	seaweed_wet_on_farm_vals.append(val.varValue)
	print(str(val)+str(val.varValue))

print('used area')
used_area_vals=[]
for d in range(0,NDAYS):
	val=used_area[d]
	used_area_vals.append(val.varValue)
	print(str(val)+str(val.varValue))

print('built area')
for d in range(0,NDAYS):
	val=built_area[d]
	print('built'+str(d)+': '+str(val))
print('density')
for d in range(0,NDAYS):
	print(str('density')+str(d)+':'+str(seaweed_wet_on_farm[d].varValue/used_area[d].varValue))

print('seaweed food produced')
# for d in range(0,NDAYS):
# 	val=seaweed_food_produced[d]
# 	# seaweed_food_produced_vals.append(val.varValue)
# 	print(str(val)+str(val.varValue))


# plt.fig()
# print('')
# print('')
# print('')
# print('')
# print('')
# print('')
# print('')
# print('')
# print('')
# print('')
# print(spreadsheet[0:10])
# print('')
# print(np.array(seaweed_wet_on_farm_vals[0:10])*1000)
# quit()
plt.plot(spreadsheet)
# plt.plot(no_loss_spreadsheet)
# plt.plot(np.array(built_area)*MAXIMUM_DENSITY*1000)
plt.plot(np.array(seaweed_wet_on_farm_vals)*1000)
# plt.plot(np.divide(np.array(seaweed_wet_on_farm_vals)*1000,no_loss_spreadsheet))
plt.show()
print('')	
print('')	
print('RESULTS')	
print('')	
print('')	
# for d in range(0,NDAYS):
# 	print('Day '+str(d))
# 	print('seaweed_wet_on_farm')
# 	print(seaweed_wet_on_farm[d].name)
# 	print(seaweed_wet_on_farm[d].varValue)
# 	print('seaweed_food_produced')
# 	print(seaweed_food_produced[d].name)
# 	print(seaweed_food_produced[d].varValue)

#double check it worked
SHOW_CONSTRAINT_CHECK=False
# print(model.constraints.items())
print('pulp reports successful optimization')
Validator.checkConstraintsSatisfied(model,status,maximize_constraints,allconstraints,SHOW_CONSTRAINT_CHECK)
# Plotter.plotLine(model)
# Plotter.plotLine(model)