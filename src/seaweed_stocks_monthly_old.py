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

#full months duration of simulation
NMONTHS=9
DAYS_IN_MONTH=30
NDAYS=NMONTHS*DAYS_IN_MONTH
ADD_SEAWEED=False
ADD_STORED_FOOD=True
MAXIMIZE_ONLY_FOOD_AFTER_DAY_150=False

# Create the model to optimize
model = LpProblem(name="optimization_nutrition", sense=LpMaximize)

# Initialize the variable to maximize
z = LpVariable(name="Least_Humans_Fed_Any_Month", lowBound=0)

#### NUTRITION PER MILLION PERSON MONTH####

#https://docs.google.com/spreadsheets/d/1RZqSrHNiIEuPQLtx1ebCd_kUcFvEF6Ea46xyzA5wU0s/edit#gid=1516287804
#we will assume a 2100 calorie diet, and scale the "upper safe" nutrients
#from the spreadsheet down to this "standard" level.

ASSUMED_KCALS_DAILY=2100 #kcals

UPPER_KCALS_DAILY=2755 #kcals
UPPER_PROTEIN_DAILY = 78.75 #grams
UPPER_FAT_DAILY = 70 #grams

STANDARD_TO_UPPER_RATIO=\
	ASSUMED_KCALS_DAILY/UPPER_KCALS_DAILY
STANDARD_KCALS_DAILY=ASSUMED_KCALS_DAILY
STANDARD_PROTEIN_DAILY=UPPER_PROTEIN_DAILY*STANDARD_TO_UPPER_RATIO #grams
STANDARD_FAT_DAILY=UPPER_FAT_DAILY*STANDARD_TO_UPPER_RATIO # grams

# assume need to make up for loss of 13% by mass from waste
WASTE=1/(1-13/100)
KCALS_MONTHLY=STANDARD_KCALS_DAILY*DAYS_IN_MONTH
USED_KCALS_MONTHLY=KCALS_MONTHLY*WASTE*1e6/1e9 #in billions of kcals per million people

#mike's spreadsheet
PROTEIN_MONTHLY=STANDARD_PROTEIN_DAILY*DAYS_IN_MONTH
USED_PROTEIN_MONTHLY=PROTEIN_MONTHLY*WASTE/1e6 # in tons
#mike's spreadsheet
FAT_MONTHLY=STANDARD_FAT_DAILY*DAYS_IN_MONTH
USED_FAT_MONTHLY=FAT_MONTHLY*WASTE/1e6 # in tons


####SEAWEED INITIAL VARIABLES####
food_spreadsheet=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,102562183,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1878422073,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2225588498,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2572754922,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2919921347]
wet_on_farm_spreadsheet=[1000,1100,1210,1331,1464,1611,1772,1949,2144,2358,2594,2853,3138,3452,3797,4177,4595,5054,5560,6116,6727,7400,8140,8954,9850,10835,11918,13110,14421,15863,17449,19194,21114,23225,25548,28102,30913,34004,37404,41145,45259,49785,54764,60240,66264,72890,80180,88197,97017,106719,117391,129130,142043,156247,171872,189059,207965,228762,251638,276801,304482,334930,368423,405265,445792,490371,539408,593349,652683,717952,789747,868722,955594,1051153,1156269,1271895,1399085,1538993,1692893,1862182,2048400,2253240,2478564,2726421,2999063,3298969,3628866,3991753,3792289,4171517,4588669,5047536,5552290,6107519,6718271,7390098,8129107,8942018,9836220,10819842,11901826,13092009,14401210,15841331,17425464,19168010,21084811,23193292,25512621,28063884,30870272,33957299,37353029,35493925,39043318,42947650,47242415,51966656,57163322,62879654,69167619,76084381,83692820,92062102,101268312,111395143,122534657,134788123,148266935,163093629,179402992,197343291,217077620,238785382,262663920,288930312,317823343,349605677,229643215,252607536,277868290,305655119,336220630,369842693,406826963,447509659,492260625,541486687,595635356,655198892,720718781,792790659,872069725,959276697,1055204367,1160724804,1276797284,1404477013,1544924714,1699417185,1869358904,2056294794,2261924274,271172782,298290061,328119067,360930973,397024071,436726478,480399126,528439038,581282942,639411236,703352360,773687596,851056355,936161991,1029778190,1132756009,1246031610,1370634771,1507698248,1658468072,1824314880,2006746368,2207421004,2428163105,2670979415,312702350,343972585,378369844,416206828,457827511,503610262,553971288,609368417,670305259,737335785,811069363,892176299,981393929,1079533322,1187486655,1306235320,1436858852,1580544737,1738599211,1912459132,2103705045,2314075550,2545483105,2800031415,3080034557,354231918,389655110,428620621,471482683,518630951,570494046,627543451,690297796,759327576,835260333,918786367,1010665003,1111731504,1222904654,1345195119,1479714631,1627686094,1790454704,1969500174,2166450192,2383095211,2621404732,2883545205,3171899726,3489089698,395761486]

#use "laver" variety for now from nutrition calculator
#https://docs.google.com/spreadsheets/d/1RZqSrHNiIEuPQLtx1ebCd_kUcFvEF6Ea46xyzA5wU0s/edit#gid=1516287804
WET_TO_DRY_MASS_CONVERSION=1/6
KCALS_PER_KG=2100 #kcals per kg dry
MASS_FRACTION_PROTEIN_DRY = 0.862*.349# dry fraction mass digestible protein
MASS_FRACTION_FAT_DRY = 0.017# dry fraction mass fat

## seaweed billion kcals per 1000 tons wet
# convert 1000 tons to kg 
# convert kg to kcals
# convert kcals to billions of kcals
SEAWEED_KCALS = 1e6 * KCALS_PER_KG / 1e9 * WET_TO_DRY_MASS_CONVERSION

## seaweed tons digestible protein per 1000 ton wet
# convert 1000 tons to tons
SEAWEED_PROTEIN = MASS_FRACTION_PROTEIN_DRY	* 1000 * WET_TO_DRY_MASS_CONVERSION

## seaweed tons fat per 1000 ton wet
# convert 1000 tons to tons
SEAWEED_FATS = MASS_FRACTION_FAT_DRY * 1000 * WET_TO_DRY_MASS_CONVERSION 

HARVEST_LOSS=15 # percent
INITIAL_SEAWEED=1 # 1000 tons
INITIAL_AREA=1 # 1000 tons
NEW_AREA_PER_DAY=4.153 # 1000 km^2
MINIMUM_DENSITY=400 #tons/km^2
MAXIMUM_DENSITY=4000 #tons/km^2
MAXIMUM_AREA=1000 # 1000 km^2
PRODUCTION_RATE=10 # percent
built_area=np.linspace(INITIAL_AREA,(NDAYS-1)*NEW_AREA_PER_DAY+INITIAL_AREA,NDAYS)
built_area[built_area>MAXIMUM_AREA]=MAXIMUM_AREA
seaweed_food_produced=[0]*NDAYS
seaweed_food_produced_monthly=[0]*NMONTHS
seaweed_wet_on_farm=[0]*NDAYS
density=[0]*NDAYS
used_area=[0]*NDAYS

#### STORED FOOD VARIABLES ####

# (nuclear event in mid-may)
#mike's spreadsheet: https://docs.google.com/spreadsheets/d/19kzHpux690JTCo2IX2UA1faAd7R1QcBK/edit#gid=806987252
# MTONS_TO_KG=1e6#1000 kg in tonne
INITIAL_SF_KCALS = 1602542.0 # billion kcals per unit mass
INITIAL_SF_PROTEIN = 203.607 # million grams = tons per unit mass
INITIAL_SF_FATS = 63.948 # million grams = tons per unit mass

SF_FRACTION_KCALS =	INITIAL_SF_KCALS \
	/ (INITIAL_SF_KCALS
		+ INITIAL_SF_PROTEIN
		+ INITIAL_SF_FATS)
SF_FRACTION_FATS =	INITIAL_SF_FATS \
	/ (INITIAL_SF_KCALS
		+ INITIAL_SF_PROTEIN
		+ INITIAL_SF_FATS)
SF_FRACTION_PROTEIN = INITIAL_SF_PROTEIN \
	/ (INITIAL_SF_KCALS
		+ INITIAL_SF_PROTEIN
		+ INITIAL_SF_FATS)

#mass initial, units don't matter, we only need to ensure we use the correct 
#fraction of kcals, fat, and protein per unit initial stored food.
INITIAL_SF=INITIAL_SF_KCALS/SF_FRACTION_KCALS
print(INITIAL_SF)
# quit()
stored_food_start=[0]*NMONTHS
stored_food_end=[0]*NMONTHS
stored_food_eaten=[0]*NMONTHS # if stored food isn't modeled, this stays zero

#### OTHER VARIABLES ####
humans_fed_fat = [0]*NMONTHS
humans_fed_protein = [0]*NMONTHS
humans_fed_kcals = [0]*NMONTHS
maximize_constraints=[] #useful only for validation
allconstraints=[z] #useful only for validation

#### FUNCTIONS FOR EACH FOOD TYPE ####


def add_seaweed_to_model(model, m):
	sum_food_this_month=[]
	for d in np.arange(m*DAYS_IN_MONTH,(m+1)*DAYS_IN_MONTH):
		time_days_daily.append(d)
		seaweed_wet_on_farm[d] = LpVariable("Seaweed_Wet_On_Farm_"+str(d)+"_Variable", INITIAL_SEAWEED, MAXIMUM_DENSITY*built_area[d])
		# food production (using resources)
		seaweed_food_produced[d] = LpVariable(name="Seaweed_Food_Produced_During_Day_"+str(d)+"_Variable", lowBound=0)

		used_area[d] = LpVariable("Used_Area_"+str(d)+"_Variable", INITIAL_AREA,built_area[d])

		if(d==0): #first Day
			model += (seaweed_wet_on_farm[0] == INITIAL_SEAWEED,
				"Seaweed_Wet_On_Farm_0_Constraint")
			model += (used_area[0] == INITIAL_AREA,
				"Used_Area_Day_0_Constraint")
			model += (seaweed_food_produced[0] == 0,
				"Seaweed_Food_Produced_Day_0_Constraint")

		else: #later Days
			model += (seaweed_wet_on_farm[d] <= used_area[d]*MAXIMUM_DENSITY)

			model += (seaweed_wet_on_farm[d] == 
				seaweed_wet_on_farm[d-1]*(1+PRODUCTION_RATE/100.)
				- seaweed_food_produced[d]
				- (used_area[d]-used_area[d-1])*MINIMUM_DENSITY*(HARVEST_LOSS/100),
				"Seaweed_Wet_On_Farm_"+str(d)+"_Constraint")
			# else:
			# 	model += (seaweed_wet_on_farm[d] == 
			# 		seaweed_wet_on_farm[d-1]*(1+PRODUCTION_RATE/100.)
			# 		# - seaweed_food_produced[d]
			# 		- (used_area[d]-used_area[d-1])*MINIMUM_DENSITY*50/100,
			# 		"Seaweed_Wet_On_Farm_"+str(d)+"_Constraint")

		allconstraints.append(used_area[d])
		allconstraints.append(seaweed_wet_on_farm[d])

		allconstraints.append(seaweed_food_produced[d])
		sum_food_this_month.append(seaweed_food_produced[d])

	seaweed_food_produced_monthly[m] = LpVariable(name="Seaweed_Food_Produced_Monthly_"+str(m)+"_Variable", lowBound=0)
	
	model += (seaweed_food_produced_monthly[m] == np.sum(sum_food_this_month),
		"Seaweed_Food_Produced_Monthly_"+str(m)+"_Constraint")

	allconstraints.append(seaweed_food_produced_monthly[m])

	return model

# print(INITIAL_SF)
# quit()

#incorporate linear constraints for stored food consumption each month
def add_stored_food_to_model(model, m):
	stored_food_start[m] = LpVariable("Stored_Food_Start_Month_"+str(m)+"_Variable", 0,INITIAL_SF)
	stored_food_end[m] = LpVariable("Stored_Food_End_Month_"+str(m)+"_Variable", 0,INITIAL_SF)
	stored_food_eaten[m] = LpVariable("Stored_Food_Eaten_During_Month_"+str(m)+"_Variable",0,INITIAL_SF)
	
	if(m==0): #first Month
		model += (stored_food_start[0] <= INITIAL_SF, "Stored_Food_Amount_Start_Month_0_Constraint")
	else:
		model += (stored_food_start[m] <= stored_food_end[m-1], "Stored_Food_Amount_Start_Month_"+str(m)+"_Constraint")

	model += (stored_food_end[m] <= stored_food_start[m] - stored_food_eaten[m], "Stored_Food_Amount_End_Month_"+str(m)+"_Constraint")

	allconstraints.append(stored_food_start[m])
	allconstraints.append(stored_food_end[m])
	allconstraints.append(stored_food_eaten[m])

	return model

#the objective optimization is performed here, using human nutritional 
#requirements. Any foods which are not modeled will be default zero.
def add_seaweed_objectives_to_model(model, m, maximize_constraints):
	maximizer_string="Seaweed_Food_Produced_"+str(m)+"_Objective_Constraint"
	maximize_constraints.append(maximizer_string)
	model += (z == seaweed_food_produced_monthly[m], maximizer_string)
	# allconstraints.append(seaweed_food_produced_monthly[m])
	return [model, maximize_constraints]

def add_objectives_to_model(model, m, maximize_constraints):
	#total eaten
	humans_fed_fat[m] = \
		LpVariable(name="Humans_Fed_Fat_"+str(m)+"_Variable",lowBound=0)
	humans_fed_protein[m] = \
		LpVariable(name="Humans_Fed_Protein_"+str(m)+"_Variable",lowBound=0)
	humans_fed_kcals[m] = \
		LpVariable(name="Humans_Fed_Calories_"+str(m)+"_Variable",lowBound=0)

	allconstraints.append(humans_fed_fat[m])
	allconstraints.append(humans_fed_protein[m])
	allconstraints.append(humans_fed_kcals[m])

	#finds millions of people fed per nutrient

	#used kcals is in billions kcals per millions of people monthly
	#stored food eaten*fraction_kcals is in units billions kcals monthly
	#seaweed_food_produced_monthly*seaweed_kcals is in units billions kcals

	# print(SEAWEED_KCALS)
	# print(SF_FRACTION_KCALS)
	# quit()
	model += (humans_fed_kcals[m] == 
		(stored_food_eaten[m]*SF_FRACTION_KCALS
		+ seaweed_food_produced_monthly[m]*SEAWEED_KCALS)/USED_KCALS_MONTHLY,
		"Calories_Fed_Month_"+str(m)+"_Constraint")
	model += (humans_fed_fat[m] == 
		(stored_food_eaten[m]*SF_FRACTION_FATS 
		+ seaweed_food_produced_monthly[m]*SEAWEED_FATS)/(USED_FAT_MONTHLY*1000),
		"Fat_Fed_Month_"+str(m)+"_Constraint")
	model += (humans_fed_protein[m] == 
		(stored_food_eaten[m]*SF_FRACTION_PROTEIN
		+ seaweed_food_produced_monthly[m]*SEAWEED_PROTEIN)/(USED_PROTEIN_MONTHLY*1000),
		"Protein_Fed_Month_"+str(m)+"_Constraint")

	# maximizes the minimum z value
	# We maximize the minimum humans fed from any month 
	# We therefore maximize the minimum ratio of fat per human requirement, 
	# protein per human requirement, or kcals per human requirement
	# for all months
	maximizer_string="Fat_Fed_Month_"+str(m)+"_Objective_Constraint"
	maximize_constraints.append(maximizer_string)
	model += (z <= humans_fed_fat[m], maximizer_string)

	maximizer_string="Calories_Fed_Month_"+str(m)+"_Objective_Constraint"
	maximize_constraints.append(maximizer_string)
	model += (z <= humans_fed_protein[m], maximizer_string)

	maximizer_string="Protein_Fed_Month_"+str(m)+"_Objective_Constraint"
	maximize_constraints.append(maximizer_string)
	model += (z <= humans_fed_kcals[m], maximizer_string)

	return [model, maximize_constraints]

time_days_monthly=[]
time_days_daily=[]
time_months=[]
time_days_middle=[]
time_months_middle=[]
for m in range(0,NMONTHS):
	time_days_middle.append(DAYS_IN_MONTH*(m+0.5))
	time_days_monthly.append(DAYS_IN_MONTH*m)
	time_days_monthly.append(DAYS_IN_MONTH*(m+1))
	time_months.append(m)
	time_months.append(m+1)
	time_months_middle.append(m+0.5)

	if(ADD_SEAWEED):
		model = add_seaweed_to_model(model,m)

	if(ADD_STORED_FOOD):
		model = add_stored_food_to_model(model,m)
	if(
		(not MAXIMIZE_ONLY_FOOD_AFTER_DAY_150)
		or 
		(MAXIMIZE_ONLY_FOOD_AFTER_DAY_150 and (m >= 5))
	):
		[model,maximize_constraints] = \
			add_objectives_to_model(model, m,maximize_constraints)

	

	# maximizes the minimum z value
	# we maximize the minimum humans fed from any Month and either fat, protein, or kcals
	# if(m==NMONTHS-1):
	# maximizer_string="Seaweed_Wet_On_Farm_"+str(m)+"_Objective_Constraint"
	# maximize_constraints.append(maximizer_string)
	# model += (z == seaweed_food_produced[m], maximizer_string)
	# model += (z == seaweed_wet_on_farm_end[m], maximizer_string)
	
obj_func = z
model += obj_func

status = model.solve(pulp.PULP_CBC_CMD(fracGap=0.01))
print(f"objective: {model.objective.value()}")
for var in model.variables():
	print(f"{var.name}: {var.value()}")

print('')

stored_food_vals=[]
print('stored food not eaten')
print('billions of calories stored at first')
print(INITIAL_SF*SF_FRACTION_KCALS)
print('million people per month eat this many billion kcals')
print(USED_KCALS_MONTHLY)
print('billions of person-years, stored food')
print(INITIAL_SF*SF_FRACTION_KCALS/USED_KCALS_MONTHLY/1000/12)
for m in range(0,NMONTHS):
	val=stored_food_start[m]
	stored_food_vals.append(val.varValue*SF_FRACTION_KCALS/USED_KCALS_MONTHLY/1000/12)
	print(str(val)+str(val.varValue*SF_FRACTION_KCALS/USED_KCALS_MONTHLY/1000/12))
	val=stored_food_end[m]
	stored_food_vals.append(val.varValue)

stored_food_eaten_vals=[]
print('stored food eaten')
for m in range(0,NMONTHS):
	val=stored_food_eaten[m]
	stored_food_eaten_vals.append(val.varValue*SF_FRACTION_KCALS/USED_KCALS_MONTHLY/1000)
	print(str(val)+str(val.varValue*SF_FRACTION_KCALS/USED_KCALS_MONTHLY/1000))

plt.plot(time_months_middle,np.array(stored_food_eaten_vals))
plt.title('Stored food eaten, billion people')
plt.show()
# quit()
if(ADD_SEAWEED):
	seaweed_wet_on_farm_vals=[]
	# print('seaweed wet on farm')
	for d in range(0,NDAYS):
		val=seaweed_wet_on_farm[d]
		seaweed_wet_on_farm_vals.append(val.varValue)
		# print(str(val)+str(val.varValue))

	seaweed_food_produced_vals_daily=[]
	# print('seaweed produced')
	for d in range(0,NDAYS):
		val=seaweed_food_produced[d]
		seaweed_food_produced_vals_daily.append(val.varValue)
		# print(str(val)+str(val.varValue))

	seaweed_food_produced_vals=[]
	print('seaweed produced monthly')
	for m in range(0,NMONTHS):
		val=seaweed_food_produced_monthly[m]
		seaweed_food_produced_vals.append(val.varValue*SEAWEED_KCALS/USED_KCALS_MONTHLY)
		print(str(val)+str(val.varValue))

	print('used area')
	used_area_vals=[]
	for d in range(0,NDAYS):
		val=used_area[d]
		used_area_vals.append(val.varValue)
		print(str(val)+str(val.varValue))

	print('density')
	for d in range(0,NDAYS):
		print(str('density')+str(d)+':'+str(seaweed_wet_on_farm[d].varValue/used_area[d].varValue))
	print('built area')
	# for d in range(0,NDAYS):
	# 	val=built_area[d]
	# 	print('built'+str(d)+': '+str(val))

	WORLD_POP=7.9e3#millions of people
	spreadsheet_days=np.linspace(0,len(wet_on_farm_spreadsheet),len(wet_on_farm_spreadsheet))
	max_line=np.linspace(4e6,4e6,len(wet_on_farm_spreadsheet))

	max_world_calories_month=WORLD_POP*USED_KCALS_MONTHLY
	max_world_calories_wet_tonnage_month=max_world_calories_month/SEAWEED_KCALS
	world_calories_line=np.linspace(max_world_calories_wet_tonnage_month,max_world_calories_wet_tonnage_month,len(wet_on_farm_spreadsheet))

	plt.plot(spreadsheet_days,max_line)
	plt.plot(spreadsheet_days,world_calories_line)
	plt.plot(np.array(built_area)*MAXIMUM_DENSITY)
	plt.plot(np.array(used_area_vals)*MAXIMUM_DENSITY)
	plt.plot(spreadsheet_days,np.array(wet_on_farm_spreadsheet)/1000)
	plt.plot(np.array(seaweed_wet_on_farm_vals))
	# plt.plot(time_days_monthly,np.array(stored_food_vals))
	# plt.plot(time_days_middle,np.array(stored_food_eaten_vals))
	plt.legend([
		'Max Density times Max Area',
		'7.9 billion people monthly calorie requirement',
		'Built Area times Max Density',
		'Used Area times Max Density',
		'Aron\'s Spreadsheet Wet on Farm Estimate',
		'Optimizer Estimate Wet On Farm',
		# 'stored_food_eaten'
		])
	# plt.plot(np.divide(np.array(seaweed_wet_on_farm_vals)*1000,no_loss_spreadsheet))
	plt.title('Seaweed Wet, 1000s of tons, Optimize Food after day 150, Daily')
	plt.yscale('log')
	plt.show()

	plt.plot(spreadsheet_days,max_line)
	plt.plot(spreadsheet_days,world_calories_line)
	# plt.plot(np.array(built_area)*MAXIMUM_DENSITY)
	# plt.plot(np.array(used_area_vals)*MAXIMUM_DENSITY)
	plt.plot(spreadsheet_days,np.array(food_spreadsheet).cumsum()/1000)
	plt.plot(time_days_daily,np.array(seaweed_food_produced_vals_daily).cumsum()*SEAWEED_KCALS/USED_KCALS_MONTHLY)
	# plt.plot(time_days_monthly,np.array(stored_food_vals*12))
	plt.plot(time_days_middle,np.array(stored_food_eaten_vals).cumsum())
	plt.legend([
		'Max Density times Max Area',
		'7.9 billion people monthly calorie requirement',
		# 'Built Area times Max Density',
		# 'Used Area times Max Density',
		'Aron\'s Spreadsheet Food Wet Harvest Estimate',
		'Optimizer Estimate Food Wet Harvest Estimate',
		'Stored Food Eaten'
		])
	# plt.plot(np.divide(np.array(seaweed_wet_on_farm_vals)*1000,no_loss_spreadsheet))
	plt.title('Eaten food, Billions of people, Monthly')
	plt.yscale('log')
	plt.show()


print('')	
print('')	
print('RESULTS')	
print('')	
print('')
	
if(ADD_STORED_FOOD):
	print('stored food')
	stored_food_vals=[]
	for m in range(0,NMONTHS):
		val=stored_food_start[m]
		stored_food_vals.append(val.varValue*SF_FRACTION_KCALS/USED_KCALS_MONTHLY/12/1000)
		val=stored_food_end[m]
		stored_food_vals.append(val.varValue*SF_FRACTION_KCALS/USED_KCALS_MONTHLY/12/1000)
		print(str(val)+str(val.varValue))

	plt.plot(time_months,np.array(stored_food_vals))
	plt.title('Stored Food in Billion Person-Years, by Calories')
	plt.xlabel('Months Since May Nuclear Event')
	plt.show()

if(not MAXIMIZE_ONLY_FOOD_AFTER_DAY_150):
	humans_fed_fat_vals=[]
	humans_fed_protein_vals=[]
	humans_fed_kcals_vals=[]
	for m in range(0,NMONTHS):
		val=humans_fed_kcals[m]
		humans_fed_kcals_vals.append(val.varValue)
		val=humans_fed_fat[m]
		humans_fed_fat_vals.append(val.varValue)
		val=humans_fed_protein[m]
		humans_fed_protein_vals.append(val.varValue)
		print(str(val)+str(val.varValue))

	plt.plot(time_months_middle,np.array(humans_fed_kcals_vals))
	plt.plot(time_months_middle,np.array(humans_fed_fat_vals))
	plt.plot(time_months_middle,np.array(humans_fed_protein_vals))
	plt.legend(['calorie req satisfied','fat req satisfied','protein req satisfied'])
	plt.title('People Fed (Millions)')
	plt.xlabel('Months Since May Nuclear Event')
	plt.show()

#double check it worked
SHOW_CONSTRAINT_CHECK=True
# print(model.constraints.items())
print('pulp reports successful optimization')
Validator.checkConstraintsSatisfied(model,status,maximize_constraints,allconstraints,SHOW_CONSTRAINT_CHECK)
# Plotter.plot(model)

#add all the constraints and variables to the model
