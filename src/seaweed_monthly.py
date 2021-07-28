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



#units: 1000 tons mass, 1000 km^2 area

HARVEST_LOSS=15
INITIAL_SEAWEED=1
INITIAL_AREA=1
NEW_AREA_PER_DAY=4.153
MINIMUM_DENSITY=400
MAXIMUM_DENSITY=4000
MAXIMUM_AREA=1000
PRODUCTION_RATE=10
DAYS_IN_MONTH=30.4

# Protein	Fat total	Saturated fats	Trans fats	Sugars
# g	g	g	g	g	g	g
# 60	2386	2386*0.15

# Per 100 grams dry, laver
# Energy kcal/100g	Protein digestibility	Protein grams	Fat total grams
# 210	0.862	34.9	1.7

NMONTHS=5

# Create the model to optimize
model = LpProblem(name="optimization_nutrition", sense=LpMaximize)


#initialize variables with zero, will be overwritten
built_area_start=
	np.linspace(INITIAL_AREA,
		(NMONTHS-1)*NEW_AREA_PER_DAY*DAYS_IN_MONTH+INITIAL_AREA,
		NMONTHS)
built_area_end=np.linspace(
	INITIAL_AREA+NEW_AREA_PER_DAY*DAYS_IN_MONTH,
	(NMONTHS)*NEW_AREA_PER_DAY*DAYS_IN_MONTH+INITIAL_AREA,
	NMONTHS)
built_area_start[built_area_start>MAXIMUM_AREA]=MAXIMUM_AREA
built_area_end[built_area_end>MAXIMUM_AREA]=MAXIMUM_AREA
seaweed_food_produced=[0]*NMONTHS
seaweed_wet_on_farm_start=[0]*NMONTHS
seaweed_wet_on_farm_end=[0]*NMONTHS
used_area_start=[0]*NMONTHS
used_area_end=[0]*NMONTHS
maximize_constraints=[]

# Initialize the variable to maximize
z = LpVariable(name="least_nutrient_eaten_any_Month", lowBound=0)

allconstraints=[z]

time_days=[]
time_months=[]
for m in range(0,NMONTHS):
	time_days.append(DAYS_IN_MONTH*m)
	time_days.append(DAYS_IN_MONTH*(m+1))
	time_months.append(m)
	time_months.append(m+1)
	print('Month')
	print(m)
	seaweed_wet_on_farm_start[m] = LpVariable("Seaweed_Wet_On_Farm_Start"+str(m)+"_Variable", INITIAL_SEAWEED, MAXIMUM_DENSITY*built_area_start[m])
	seaweed_wet_on_farm_end[m] = LpVariable("Seaweed_Wet_On_Farm_End"+str(m)+"_Variable", INITIAL_SEAWEED, MAXIMUM_DENSITY*built_area_end[m])


	used_area_start[m] = LpVariable("Used_Area_Start_"+str(m)+"_Variable", 
		INITIAL_AREA,
		built_area_start[m])
	used_area_end[m] = LpVariable("Used_Area_End_"+str(m)+"_Variable", 
		INITIAL_AREA,
		built_area_end[m])

	#each month, move all the seaweed over to built area
	if(m==0): #first Month
		model += (seaweed_wet_on_farm_start[0] == INITIAL_SEAWEED,
			"Seaweed_Wet_On_Farm_Start_Month_0_Constraint")
		model += (used_area_start[0] == INITIAL_AREA,
			"Used_Area_Start_Month_0_Constraint")
	else: #later Months
		model += (used_area_start[m]==used_area_end[m-1],
			"Used_Area_Month_"+str(m)+"_Constraint")
		model += (seaweed_wet_on_farm_start[m] == 
			seaweed_wet_on_farm_end[m-1]
			- (used_area_end[m-1]-used_area_start[m-1])
				* MINIMUM_DENSITY
				* HARVEST_LOSS/100,
			"Seaweed_Wet_On_Farm_Loss_Month_"+str(m)+"_Constraint")
		model += (seaweed_wet_on_farm_end[m] <= used_area_end[m]*MAXIMUM_DENSITY,
			"Seaweed_Wet_On_Farm_Min_Month_"+str(m)+"_Constraint")

	model += (seaweed_wet_on_farm_end[m] == 
		seaweed_wet_on_farm_start[m]*(1+PRODUCTION_RATE/100.)**DAYS_IN_MONTH,
		# - seaweed_food_produced[m]
		"Seaweed_Wet_On_Farm_Month_"+str(m)+"_Constraint")


	allconstraints.append(used_area_end[m])
	allconstraints.append(used_area_start[m])
	allconstraints.append(seaweed_wet_on_farm_start[m])
	allconstraints.append(seaweed_wet_on_farm_end[m])


	# maximizes the minimum z value
	# we maximize the minimum humans fed from any Month and either fat, protein, or calories
	if(m==NMONTHS-1):
		maximizer_string="Seaweed_Wet_On_Farm_"+str(m)+"_Objective_Constraint"
		maximize_constraints.append(maximizer_string)
		# model += (z == seaweed_food_produced[m], maximizer_string)
		model += (z == seaweed_wet_on_farm_end[m], maximizer_string)
	allconstraints.append(seaweed_wet_on_farm_end[m])



	
obj_func = z
model += obj_func

status = model.solve(pulp.PULP_CBC_CMD(msg=1))
print(f"objective: {model.objective.value()}")
for var in model.variables():
	print(f"{var.name}: {var.value()}")

print('')

seaweed_wet_on_farm_vals=[]
print('seaweed wet on farm')
for m in range(0,NMONTHS):
	val=seaweed_wet_on_farm_start[m]
	seaweed_wet_on_farm_vals.append(val.varValue)
	val=seaweed_wet_on_farm_end[m]
	seaweed_wet_on_farm_vals.append(val.varValue)
	print(str(val)+str(val.varValue))


print('used area')
used_area_vals=[]
for m in range(0,NMONTHS):
	val=used_area_end[m]
	used_area_vals.append(val.varValue)
	print(str(val)+str(val.varValue))

print('density')
for m in range(0,NMONTHS):
	print(str('density')+str(m)+':'+str(seaweed_wet_on_farm_end[m].varValue/used_area_end[m].varValue))
for m in range(0,NMONTHS):
	val=built_area_end[m]
	print('built'+str(m)+': '+str(val))
print('seaweed food produced')


print([x.varValue for x in seaweed_wet_on_farm_end])
plt.plot(time_days,np.array(seaweed_wet_on_farm_vals)*1000)
plt.yscale('log')
# plt.plot(np.divide(np.array(seaweed_wet_on_farm_vals)*1000,no_loss_spreadsheet))
plt.show()
print('')	
print('')	
print('RESULTS')	
print('')	
print('')	

#double check it worked
SHOW_CONSTRAINT_CHECK=True
# print(model.constraints.items())
print('pulp reports successful optimization')
Validator.checkConstraintsSatisfied(model,status,maximize_constraints,allconstraints,SHOW_CONSTRAINT_CHECK)
# Plotter.plotLine(model)