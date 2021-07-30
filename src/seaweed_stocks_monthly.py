import os
import sys
module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
	sys.path.append(module_path)

import numpy as np
from src.analysis import Analyzer
from src.plotter import Plotter
from src.validate import Validator

import pulp
from pulp import LpMaximize, LpProblem, LpVariable

#full months duration of simulation
NMONTHS=9
print("NMONTHS: "+str(NMONTHS))
DAYS_IN_MONTH=30
NDAYS=NMONTHS*DAYS_IN_MONTH
WORLD_POP=7.8e9

ADD_SEAWEED=True
print("ADD_SEAWEED: "+str(ADD_SEAWEED))
ADD_STORED_FOOD=True
print("ADD_STORED_FOOD: "+str(ADD_STORED_FOOD))
ADD_CELLULOSIC_SUGAR = True
print("ADD_CELLULOSIC_SUGAR: "+str(ADD_CELLULOSIC_SUGAR))
MAXIMIZE_ONLY_FOOD_AFTER_DAY_150=False
print("MAXIMIZE_ONLY_FOOD_AFTER_DAY_150: "
	+ str(MAXIMIZE_ONLY_FOOD_AFTER_DAY_150))
LIMIT_SEAWEED_AS_PERCENT_KCALS=False
print("LIMIT_SEAWEED_AS_PERCENT_KCALS: "+str(LIMIT_SEAWEED_AS_PERCENT_KCALS))
VERBOSE = False
print("VERBOSE: "+str(VERBOSE))


# Create the model to optimize
model = LpProblem(name="optimization_nutrition", sense=LpMaximize)

# Initialize the variable to maximize
z = LpVariable(name="Least_Humans_Fed_Any_Month", lowBound=0)

#### NUTRITION PER MONTH ####

#https://docs.google.com/spreadsheets/d/1RZqSrHNiIEuPQLtx1ebCd_kUcFvEF6Ea46xyzA5wU0s/edit#gid=1516287804
#we will assume a 2100 kcals diet, and scale the "upper safe" nutrients
#from the spreadsheet down to this "standard" level.

ASSUMED_KCALS_DAILY=2616 #kcals

UPPER_KCALS_DAILY=2755 #kcals
UPPER_PROTEIN_DAILY = 78.75 #grams
UPPER_FAT_DAILY = 70 #grams

STANDARD_TO_UPPER_RATIO=\
	ASSUMED_KCALS_DAILY/UPPER_KCALS_DAILY
STANDARD_KCALS_DAILY=ASSUMED_KCALS_DAILY
STANDARD_PROTEIN_DAILY=UPPER_PROTEIN_DAILY*STANDARD_TO_UPPER_RATIO #grams
STANDARD_FAT_DAILY=UPPER_FAT_DAILY*STANDARD_TO_UPPER_RATIO # grams

KCALS_MONTHLY=STANDARD_KCALS_DAILY*DAYS_IN_MONTH#in kcals per person
PROTEIN_MONTHLY=STANDARD_PROTEIN_DAILY*DAYS_IN_MONTH/1e9# in thousands of tons
FAT_MONTHLY=STANDARD_FAT_DAILY*DAYS_IN_MONTH/1e9# in thousands of tons

####SEAWEED INITIAL VARIABLES####

#use "laver" variety for now from nutrition calculator
#https://docs.google.com/spreadsheets/d/1RZqSrHNiIEuPQLtx1ebCd_kUcFvEF6Ea46xyzA5wU0s/edit#gid=1516287804
WET_TO_DRY_MASS_CONVERSION=1/6
KCALS_PER_KG=2100. #kcals per kg dry
MASS_FRACTION_PROTEIN_DRY = 0.862*.349# dry fraction mass digestible protein
MASS_FRACTION_FAT_DRY = 0.017# dry fraction mass fat

## seaweed billion kcals per 1000 tons wet
# convert 1000 tons to kg 
# convert kg to kcals
# convert kcals to billions of kcals
# convert wet mass seaweed to dry mass seaweed
SEAWEED_KCALS = 1e6 * KCALS_PER_KG / 1e9 * WET_TO_DRY_MASS_CONVERSION

## seaweed fraction digestible protein per 1000 ton wet
SEAWEED_PROTEIN = MASS_FRACTION_PROTEIN_DRY * WET_TO_DRY_MASS_CONVERSION

## seaweed fraction fat per ton wet
SEAWEED_FATS = MASS_FRACTION_FAT_DRY * WET_TO_DRY_MASS_CONVERSION 

HARVEST_LOSS=15 # percent
INITIAL_SEAWEED=1 # 1000 tons
INITIAL_AREA=1 # 1000 tons
NEW_AREA_PER_DAY=4.153 # 1000 km^2
MINIMUM_DENSITY=400 #tons/km^2
MAXIMUM_DENSITY=4000 #tons/km^2
MAXIMUM_AREA=1000 # 1000 km^2
PRODUCTION_RATE=10 # percent

MAX_SEAWEED_AS_PERCENT_KCALS=20#max percent of kcals from seaweed  per person

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
TONS_DRY_CALORIC_EQIVALENT=1602542*1000.
KCALS_PER_DRY_CALORIC_TONS=4e6
INITIAL_SF_KCALS = KCALS_PER_DRY_CALORIC_TONS*TONS_DRY_CALORIC_EQIVALENT/1e9 # billion kcals per unit mass initial
INITIAL_SF_PROTEIN = 203607 #1000 tons protein per unit mass initial
INITIAL_SF_FATS = 63948 # 1000 tons fat per unit mass initial

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
stored_food_start=[0]*NMONTHS
stored_food_end=[0]*NMONTHS
stored_food_eaten=[0]*NMONTHS # if stored food isn't modeled, this stays zero



#### CONSTANTS FOR CELLULOSIC SUGAR ####

#in billions of calories
caloric_requirement_per_month = WORLD_POP * KCALS_MONTHLY/1e9

ramp_up_cellulosic_sugar_monthly = [0.00, 0.00, 0.00, 0.00, 0.00, 9.79, 9.79, 9.79, 19.57, 23.48, 24.58, 28.49, 28.49,
									29.59,
									31.64, 31.64, 31.64, 31.64, 33.69, 35.74, 35.74, 35.74, 35.74, 37.78, 38.70, 39.61,
									40.53,
									41.44, 42.35, 43.27, 44.18, 45.10, 46.01, 46.93, 47.84, 48.76, 49.67, 50.58, 51.50,
									52.41,
									53.33, 54.24, 55.16, 56.07, 56.99, 57.90, 58.81, 59.73, 60.64, 61.56, 62.47, 63.39,
									64.30,
									65.21, 66.13, 67.04, 67.96, 68.87, 69.79, 70.70, 71.62, 72.53, 73.44, 74.36, 75.27,
									76.19,
									77.10, 78.02, 78.93, 79.85, 80.76, 81.67]
if(ADD_CELLULOSIC_SUGAR):
	production_calories_cellulosic_sugar_per_month = []
	for x in ramp_up_cellulosic_sugar_monthly:
		production_calories_cellulosic_sugar_per_month.append(x / 100 * caloric_requirement_per_month)
else:
	production_calories_cellulosic_sugar_per_month=[0]*len(ramp_up_cellulosic_sugar_monthly)

# print(production_calories_cellulosic_sugar_per_month)
# quit()

#### OTHER VARIABLES ####

humans_fed_fat = [0]*NMONTHS
humans_fed_protein = [0]*NMONTHS
humans_fed_kcals = [0]*NMONTHS
maximize_constraints=[] #useful only for validation
allconstraints=[z] #useful only for validation

#store variables useful for analysis
constants={}
constants['NMONTHS']=NMONTHS
constants['NDAYS']=NDAYS
constants['ADD_STORED_FOOD']=ADD_STORED_FOOD
constants['ADD_SEAWEED']=ADD_SEAWEED
constants['MAXIMIZE_ONLY_FOOD_AFTER_DAY_150']=MAXIMIZE_ONLY_FOOD_AFTER_DAY_150
constants['LIMIT_SEAWEED_AS_PERCENT_KCALS']=LIMIT_SEAWEED_AS_PERCENT_KCALS
constants['VERBOSE']=VERBOSE
constants['KCALS_MONTHLY']=KCALS_MONTHLY
constants['PROTEIN_MONTHLY']=PROTEIN_MONTHLY
constants['FAT_MONTHLY']=FAT_MONTHLY
constants['MINIMUM_DENSITY']=MINIMUM_DENSITY
constants['HARVEST_LOSS']=HARVEST_LOSS
constants['MAXIMUM_AREA']=MAXIMUM_AREA
constants['MAXIMUM_DENSITY']=MAXIMUM_DENSITY
constants['SF_FRACTION_KCALS']=SF_FRACTION_KCALS
constants['SF_FRACTION_FATS']=SF_FRACTION_FATS
constants['SF_FRACTION_PROTEIN']=SF_FRACTION_PROTEIN
constants['SEAWEED_KCALS']=SEAWEED_KCALS
constants['SEAWEED_FATS']=SEAWEED_FATS
constants['SEAWEED_PROTEIN']=SEAWEED_PROTEIN
constants['INITIAL_SF']=INITIAL_SF
constants['STANDARD_KCALS_DAILY']=STANDARD_KCALS_DAILY
constants['WORLD_POP'] = WORLD_POP
constants['ADD_CELLULOSIC_SUGAR'] = ADD_CELLULOSIC_SUGAR
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

		allconstraints.append(used_area[d])
		allconstraints.append(seaweed_wet_on_farm[d])

		allconstraints.append(seaweed_food_produced[d])
		sum_food_this_month.append(seaweed_food_produced[d])

	seaweed_food_produced_monthly[m] = LpVariable(name="Seaweed_Food_Produced_Monthly_"+str(m)+"_Variable", lowBound=0)
	
	model += (seaweed_food_produced_monthly[m] == np.sum(sum_food_this_month),
		"Seaweed_Food_Produced_Monthly_"+str(m)+"_Constraint")

	allconstraints.append(seaweed_food_produced_monthly[m])

	return model


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


#### OBJECTIVE FUNCTIONS ####


def add_objectives_to_model(model, m, maximize_constraints):
	#total eaten
	humans_fed_fat[m] = \
		LpVariable(name="Humans_Fed_Fat_"+str(m)+"_Variable",lowBound=0)
	humans_fed_protein[m] = \
		LpVariable(name="Humans_Fed_Protein_"+str(m)+"_Variable",lowBound=0)
	humans_fed_kcals[m] = \
		LpVariable(name="Humans_Fed_Kcals_"+str(m)+"_Variable",lowBound=0)

	allconstraints.append(humans_fed_fat[m])
	allconstraints.append(humans_fed_protein[m])
	allconstraints.append(humans_fed_kcals[m])

	#finds billions of people fed that month per nutrient

	#stored food eaten*sf_fraction_kcals is in units billions kcals monthly
	#seaweed_food_produced_monthly*seaweed_kcals is in units billions kcals
	#kcals monthly is in units kcals
	model += (humans_fed_kcals[m] == 
		(stored_food_eaten[m]*SF_FRACTION_KCALS
		+ seaweed_food_produced_monthly[m]*SEAWEED_KCALS
		+ production_calories_cellulosic_sugar_per_month[m])/KCALS_MONTHLY,
		"Kcals_Fed_Month_"+str(m)+"_Constraint")
	#stored_food_eaten*sf_fraction_fat is in units thousand tons monthly
	#seaweed_food_produced_monthly*seaweed_fats is in units thousand tons monthly
	#fat monthly is in units thousand tons
	model += (humans_fed_fat[m] == 
		(stored_food_eaten[m]*SF_FRACTION_FATS 
		+ seaweed_food_produced_monthly[m]*SEAWEED_FATS)/FAT_MONTHLY/1e9,
		"Fat_Fed_Month_"+str(m)+"_Constraint")
	#stored_food_eaten*sf_fraction_protein is in units thousand tons monthly
	#seaweed_food_produced_monthly*seaweed_protein is in units thousand tons monthly
	#fat monthly is in units thousand tons
	model += (humans_fed_protein[m] == 
		(stored_food_eaten[m]*SF_FRACTION_PROTEIN
		+ seaweed_food_produced_monthly[m]*SEAWEED_PROTEIN)/PROTEIN_MONTHLY/1e9,
		"Protein_Fed_Month_"+str(m)+"_Constraint")

	# maximizes the minimum z value
	# We maximize the minimum humans fed from any month 
	# We therefore maximize the minimum ratio of fat per human requirement, 
	# protein per human requirement, or kcals per human requirement
	# for all months
	maximizer_string="Kcals_Fed_Month_"+str(m)+"_Objective_Constraint"
	maximize_constraints.append(maximizer_string)
	model += (z <= humans_fed_kcals[m], maximizer_string)

	maximizer_string="Fat_Fed_Month_"+str(m)+"_Objective_Constraint"
	maximize_constraints.append(maximizer_string)
	model += (z <= humans_fed_fat[m], maximizer_string)

	maximizer_string="Protein_Fed_Month_"+str(m)+"_Objective_Constraint"
	maximize_constraints.append(maximizer_string)
	model += (z <= humans_fed_protein[m], maximizer_string)

	return [model, maximize_constraints]


#### MODEL GENERATION LOOP ####


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
		(MAXIMIZE_ONLY_FOOD_AFTER_DAY_150 and (m >= 5))#start month 5 is day 150
	):
		[model,maximize_constraints] = \
			add_objectives_to_model(model, m,maximize_constraints)
	
obj_func = z
model += obj_func

status = model.solve(pulp.PULP_CBC_CMD(fracGap=0.0001,msg=VERBOSE))

print('')	
print('')	
print('VALIDATION')	
print('')	
print('')


#double check it worked

print('pulp reports successful optimization')
Validator.checkConstraintsSatisfied(
	model,
	status,
	maximize_constraints,
	allconstraints,
	VERBOSE)

print('')	
print('')	
print('RESULTS')	
print('')	
print('')

if(VERBOSE):
	print(f"objective: {model.objective.value()}")
	for var in model.variables():
		print(f"{var.name}: {var.value()}")

print('')

analysis = Analyzer(constants)

show_output=False

# if no stored food, will be zero
analysis.analyze_SF_results(
	stored_food_eaten,
	stored_food_start,
	stored_food_end,
	show_output
)

#extract numeric seaweed results in terms of people fed and raw tons wet
#if seaweed not added to model, will be zero
analysis.analyze_seaweed_results(
	seaweed_wet_on_farm,
	used_area,
	built_area,
	seaweed_food_produced_monthly,
	show_output
)

# if no stored food, will be zero
analysis.analyze_CS_results(
	production_calories_cellulosic_sugar_per_month,
	show_output
)


if(ADD_STORED_FOOD):
	Plotter.plot_stored_food(time_months,analysis)

Plotter.plot_people_fed(time_months_middle,analysis)

#if we don't have stored food, and we are optimizing last 150 days, we can compare to Aron's data.
if(ADD_SEAWEED and (not ADD_STORED_FOOD) and MAXIMIZE_ONLY_FOOD_AFTER_DAY_150):
	Plotter.plot_seaweed_comparison(time_days_daily,time_days_monthly,analysis)