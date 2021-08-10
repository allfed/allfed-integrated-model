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

####### TO DO ###
##  Crops
##		nonrelocated: we're closer to an answer here. Open phil: 
##			total production year 1, war happens month 5: 40%
##			already 20% harvested, remaining 20% after month 5 (7 months).
##			year 2: 10% of normal
##			
##		relocated: 60% reduction plucked out of thin air (for later)
##		crop relocation within countries (for later)
##		
##  Assume food availability increases, increasing human food to chickens (for later)
## 	Assume different times till standard agriculture supplants resilient foods (12 months baseline). Not having resilient foods would extend.
## 	For small animals, should be able to slaughter them in less than a month (1 month baseline)
##  Cattle currently take a year to slaughter normally
##		Rate limit: all cattle in 3 months. (baseline)
##  Assume biofuel takes a month (baseline)
##		find biofuel values for total production, tons dry food, ask mike
##		roughly currently 60% sugarcane, 40% maize
## 	Assume waste drops
##		assume global average is waste from household from poor countries in one month (baseline)
##		waste from distribution doesn't change (baseline)
##		seaweed as 30% (baseline)

constants = {}
constants['inputs'] = {}

constants['inputs']['NMONTHS'] = 12
constants['inputs']['NUTRITION'] = 'lower_moderate'
constants['inputs']['ADD_SEAWEED'] = True
constants['inputs']['ADD_NONEGG_NONDAIRY_MEAT'] = True
constants['inputs']['ADD_DAIRY'] = True
constants['inputs']['ADD_STORED_FOOD'] = True
constants['inputs']['ADD_CELLULOSIC_SUGAR'] = True
constants['inputs']['ADD_GREENHOUSES'] = True
constants['inputs']['LIMIT_SEAWEED_AS_PERCENT_KCALS'] = True
constants['inputs']['ASSUMED_WASTE_PERCENT'] = 35
constants['inputs']['ASSUMED_KCALS_EATEN'] = 2100
constants['inputs']['MILK_INIT_TONS_ANNUAL'] = 145
constants['inputs']['INITIAL_MILK_COWS'] = 264e6
constants['inputs']['MAX_SEAWEED_AS_PERCENT_KCALS'] = 10
constants['inputs']['INIT_SMALL_ANIMALS'] = 28.2e9
constants['inputs']['INIT_MEDIUM_ANIMALS'] = 3.2e9
constants['inputs']['INIT_LARGE_ANIMALS'] = 1.9e9
constants['inputs']['HARVEST_LOSS'] = 15 # percent
constants['inputs']['INITIAL_SEAWEED'] = 1 # 1000 tons
constants['inputs']['INITIAL_AREA'] = 1 # 1000 tons
constants['inputs']['NEW_AREA_PER_DAY'] = 4.153 # 1000 km^2
constants['inputs']['MINIMUM_DENSITY'] = 400 #tons/km^2
constants['inputs']['MAXIMUM_DENSITY'] = 4000 #tons/km^2
constants['inputs']['MAXIMUM_AREA'] = 1000 # 1000 km^2
constants['inputs']['PRODUCTION_RATE'] = 10 # percent
constants['inputs']['TONS_DRY_CALORIC_EQIVALENT'] = = 1602542*1000.
constants['inputs']['INITIAL_SF_PROTEIN'] = 203607 #1000 tons protein per unit mass initial
constants['inputs']['INITIAL_SF_FAT'] = 63948 # 1000 tons fat per unit mass initial
#full months duration of simulation
NMONTHS=constants['inputs']['NMONTHS']
print("NMONTHS: "+str(NMONTHS))
DAYS_IN_MONTH=30
NDAYS=NMONTHS*DAYS_IN_MONTH

#Lower (severe risk)": it is dangerous to be under
#"Lower (moderate risk)": it is tolerable to be under and adequate to be above
NUTRITION = 'lower_severe'
# NUTRITION = 'lower_moderate'

ADD_SEAWEED=constants['inputs']['ADD_SEAWEED']
print("ADD_SEAWEED: "+str(ADD_SEAWEED))
ADD_NONEGG_NONDAIRY_MEAT=constants['inputs']['ADD_NONEGG_NONDAIRY_MEAT']
print("ADD_NONEGG_NONDAIRY_MEAT: "+str(ADD_NONEGG_NONDAIRY_MEAT))
ADD_DAIRY=constants['inputs']['ADD_DAIRY']
print("ADD_DAIRY: "+str(ADD_DAIRY))

# eggs are lower priority than milk, so we're waiting till later to fill in data
ADD_EGGS=False 
print("ADD_EGGS: "+str(ADD_EGGS))

ADD_STORED_FOOD=constants['inputs']['ADD_STORED_FOOD']
print("ADD_STORED_FOOD: "+str(ADD_STORED_FOOD))
ADD_CELLULOSIC_SUGAR = constants['inputs']['ADD_CELLULOSIC_SUGAR']
print("ADD_CELLULOSIC_SUGAR: "+str(ADD_CELLULOSIC_SUGAR))
ADD_GREENHOUSES = constants['inputs']['ADD_GREENHOUSES']
print("ADD_GREENHOUSES: "+str(ADD_GREENHOUSES))
MAXIMIZE_ONLY_FOOD_AFTER_DAY_150=False
print("MAXIMIZE_ONLY_FOOD_AFTER_DAY_150: "
	+ str(MAXIMIZE_ONLY_FOOD_AFTER_DAY_150))
LIMIT_SEAWEED_AS_PERCENT_KCALS=constants['inputs']['LIMIT_SEAWEED_AS_PERCENT_KCALS']
print("LIMIT_SEAWEED_AS_PERCENT_KCALS: "+str(LIMIT_SEAWEED_AS_PERCENT_KCALS))
MAX_SEAWEED_AS_PERCENT_KCALS=constants['inputs']['MAX_SEAWEED_AS_PERCENT_KCALS']#max percent of kcals from seaweed  per person

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
#we also add 20% loss, according to the sorts of loss seen in this spreadsheet
ASSUMED_WASTE_PERCENT = constants['inputs']['ASSUMED_WASTE_PERCENT']
ASSUMED_KCALS_EATEN = constants['inputs']['ASSUMED_KCALS_EATEN']
ASSUMED_KCALS_DAILY=ASSUMED_KCALS_EATEN/(1-ASSUMED_WASTE_PERCENT/100) #kcals

# INTAKES={}
# INTAKES['lower_severe']={}
# INTAKES['lower_severe']['fat'] = 20 #grams per day
# INTAKES['lower_severe']['protein'] = 46 #grams per day
# INTAKES['lower_severe']['kcals'] = 1039 #per day
# INTAKES['lower_moderate']={}
# INTAKES['lower_moderate']['fat'] = 35 #grams per day
# INTAKES['lower_moderate']['protein'] = 51 #grams per day
# INTAKES['lower_moderate']['kcals'] = 1039 #per day

UPPER_KCALS_DAILY=2755 #kcals
UPPER_PROTEIN_DAILY = 78.75 #grams
UPPER_FAT_DAILY = 35 #grams


STANDARD_TO_UPPER_RATIO=\
	ASSUMED_KCALS_DAILY/UPPER_KCALS_DAILY
STANDARD_KCALS_DAILY=ASSUMED_KCALS_DAILY
STANDARD_PROTEIN_DAILY=UPPER_PROTEIN_DAILY*STANDARD_TO_UPPER_RATIO #grams
STANDARD_FAT_DAILY=UPPER_FAT_DAILY*STANDARD_TO_UPPER_RATIO # grams

KCALS_MONTHLY=STANDARD_KCALS_DAILY*DAYS_IN_MONTH#in kcals per person
PROTEIN_MONTHLY=STANDARD_PROTEIN_DAILY*DAYS_IN_MONTH/1e9# in thousands of tons
FAT_MONTHLY=STANDARD_FAT_DAILY*DAYS_IN_MONTH/1e9# in thousands of tons

WORLD_POP=7.8e9
KCAL_REQ_PER_MONTH = WORLD_POP * KCALS_MONTHLY/1e9

KG_TO_1000_TONS=1/(1e6)

MILK_INIT_TONS_ANNUAL=constants['inputs']['MILK_INIT_TONS_ANNUAL']
# MILK_INIT_TONS_DRY_CALORIC_EQIVALENT=MILK_INIT_TONS_ANNUAL*1e6/12 #first month
KCALS_PER_DRY_CALORIC_TONS=4e6

#https://www.ciwf.org.uk/media/5235182/Statistics-Dairy-cows.pdf
ANNUAL_LITERS_PER_COW=2200
KCALS_PER_LITER=609 #kcals for 1 liter whole milk, googled it

#billions of kcals
MILK_KCALS_PER_1000_COWS_PER_MONTH = ANNUAL_LITERS_PER_COW \
	* KCALS_PER_LITER \
	/ 12 \
	/ 1e9 \
	* 1000 

# billion kcals per unit mass initial (first month)
INITIAL_MILK_COWS = constants['inputs']['INITIAL_MILK_COWS']
INITIAL_MILK_COWS_THOUSANDS = INITIAL_MILK_COWS/1000

INIT_SMALL_ANIMALS=constants['inputs']['INIT_SMALL_ANIMALS']
INIT_SMALL_NONEGG_ANIMALS=INIT_SMALL_ANIMALS
INIT_MEDIUM_ANIMALS=constants['inputs']['INIT_MEDIUM_ANIMALS']
INIT_LARGE_ANIMALS = constants['inputs']['INIT_LARGE_ANIMALS']

INIT_LARGE_NONDAIRY_ANIMALS=INIT_LARGE_ANIMALS-INITIAL_MILK_COWS_THOUSANDS*1e3




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
SEAWEED_FAT = MASS_FRACTION_FAT_DRY * WET_TO_DRY_MASS_CONVERSION 

HARVEST_LOSS=constants['inputs']['HARVEST_LOSS']
INITIAL_SEAWEED=constants['inputs']['INITIAL_SEAWEED']
INITIAL_AREA=constants['inputs']['INITIAL_AREA']
NEW_AREA_PER_DAY=constants['inputs']['NEW_AREA_PER_DAY']
MINIMUM_DENSITY=constants['inputs']['MINIMUM_DENSITY']
MAXIMUM_DENSITY=constants['inputs']['MAXIMUM_DENSITY']
MAXIMUM_AREA=constants['inputs']['MAXIMUM_AREA']
PRODUCTION_RATE=constants['inputs']['PRODUCTION_RATE']


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

TONS_DRY_CALORIC_EQIVALENT=constants['inputs']['TONS_DRY_CALORIC_EQIVALENT']
INITIAL_SF_KCALS = KCALS_PER_DRY_CALORIC_TONS*TONS_DRY_CALORIC_EQIVALENT/1e9 # billion kcals per unit mass initial
INITIAL_SF_PROTEIN = constants['inputs']['INITIAL_SF_PROTEIN'] 
INITIAL_SF_FAT = constants['inputs']['INITIAL_SF_FAT'] 

SF_FRACTION_KCALS =	INITIAL_SF_KCALS \
	/ (INITIAL_SF_KCALS
		+ INITIAL_SF_PROTEIN
		+ INITIAL_SF_FAT)
SF_FRACTION_FAT =	INITIAL_SF_FAT \
	/ (INITIAL_SF_KCALS
		+ INITIAL_SF_PROTEIN
		+ INITIAL_SF_FAT)
SF_FRACTION_PROTEIN = INITIAL_SF_PROTEIN \
	/ (INITIAL_SF_KCALS
		+ INITIAL_SF_PROTEIN
		+ INITIAL_SF_FAT)

#mass initial, units don't matter, we only need to ensure we use the correct 
#fraction of kcals, fat, and protein per unit initial stored food.
INITIAL_SF=INITIAL_SF_KCALS/SF_FRACTION_KCALS
stored_food_start=[0]*NMONTHS
stored_food_end=[0]*NMONTHS
stored_food_eaten=[0]*NMONTHS # if stored food isn't modeled, this stays zero

#### NON EGG NONDAIRY MEAT ####

#time from slaughter livestock to it turning into food
#not functional yet
# MEAT_DELAY = 1 #months

#mike's spreadsheet "livestock meat stats"
#https://docs.google.com/spreadsheets/d/1-upBP5-iPtBzyjm5zbeGlfuE4FwqLUyR/edit#gid=642022040

KG_PER_SMALL_ANIMAL=1.6
KG_PER_MEDIUM_ANIMAL=17
KG_PER_LARGE_ANIMAL=211

#billions of kcals, 1000s of tons fat, 1000s of tons protein

KCALS_PER_SMALL_ANIMAL=1480*KG_PER_SMALL_ANIMAL/1e9
FAT_PER_SMALL_ANIMAL=.135*KG_PER_SMALL_ANIMAL*KG_TO_1000_TONS
PROTEIN_PER_SMALL_ANIMAL=.273*KG_PER_SMALL_ANIMAL*KG_TO_1000_TONS

KCALS_PER_MEDIUM_ANIMAL=2080*KG_PER_MEDIUM_ANIMAL/1e9
FAT_PER_MEDIUM_ANIMAL=.205*KG_PER_MEDIUM_ANIMAL*KG_TO_1000_TONS
PROTEIN_PER_MEDIUM_ANIMAL=.215*KG_PER_MEDIUM_ANIMAL*KG_TO_1000_TONS

KCALS_PER_LARGE_ANIMAL=2090*KG_PER_LARGE_ANIMAL/1e9
FAT_PER_LARGE_ANIMAL=.147*KG_PER_LARGE_ANIMAL*KG_TO_1000_TONS
PROTEIN_PER_LARGE_ANIMAL=.204*KG_PER_LARGE_ANIMAL*KG_TO_1000_TONS

KCALS_PER_1000_LARGE_ANIMALS=KCALS_PER_LARGE_ANIMAL * 1000
FAT_PER_1000_LARGE_ANIMALS=FAT_PER_LARGE_ANIMAL * 1000
PROTEIN_PER_1000_LARGE_ANIMALS=PROTEIN_PER_LARGE_ANIMAL * 1000

INIT_NONEGG_NONDAIRY_MEAT_KCALS = \
	INIT_SMALL_NONEGG_ANIMALS*KCALS_PER_SMALL_ANIMAL \
	+ INIT_MEDIUM_ANIMALS*KCALS_PER_MEDIUM_ANIMAL \
	+ INIT_LARGE_NONDAIRY_ANIMALS*KCALS_PER_LARGE_ANIMAL 
INIT_NONEGG_NONDAIRY_MEAT_FAT = \
	INIT_SMALL_NONEGG_ANIMALS*FAT_PER_SMALL_ANIMAL \
	+ INIT_MEDIUM_ANIMALS*FAT_PER_MEDIUM_ANIMAL \
	+ INIT_LARGE_NONDAIRY_ANIMALS*FAT_PER_LARGE_ANIMAL
INIT_NONEGG_NONDAIRY_MEAT_PROTEIN = \
	INIT_SMALL_NONEGG_ANIMALS*PROTEIN_PER_SMALL_ANIMAL \
	+ INIT_MEDIUM_ANIMALS*PROTEIN_PER_MEDIUM_ANIMAL \
	+ INIT_LARGE_NONDAIRY_ANIMALS*PROTEIN_PER_LARGE_ANIMAL


MEAT_FRACTION_KCALS = INIT_NONEGG_NONDAIRY_MEAT_KCALS \
	/ (INIT_NONEGG_NONDAIRY_MEAT_KCALS
		+ INIT_NONEGG_NONDAIRY_MEAT_PROTEIN
		+ INIT_NONEGG_NONDAIRY_MEAT_FAT)
MEAT_FRACTION_FAT =	INIT_NONEGG_NONDAIRY_MEAT_FAT \
	/ (INIT_NONEGG_NONDAIRY_MEAT_KCALS
		+ INIT_NONEGG_NONDAIRY_MEAT_PROTEIN
		+ INIT_NONEGG_NONDAIRY_MEAT_FAT)
MEAT_FRACTION_PROTEIN = INIT_NONEGG_NONDAIRY_MEAT_PROTEIN \
	/ (INIT_NONEGG_NONDAIRY_MEAT_KCALS
		+ INIT_NONEGG_NONDAIRY_MEAT_PROTEIN
		+ INIT_NONEGG_NONDAIRY_MEAT_FAT)

#arbitrary mass units
INITIAL_NONEGG_NONDAIRY_MEAT=INIT_NONEGG_NONDAIRY_MEAT_KCALS/MEAT_FRACTION_KCALS


nonegg_nondairy_meat_start=[0]*NMONTHS
nonegg_nondairy_meat_end=[0]*NMONTHS
nonegg_nondairy_meat_eaten=[0]*NMONTHS

#### CONSTANTS FOR GREENHOUSES ####
#greenhouses tab
#assumption: greenhouse crop production is very similar in nutritional
# profile to stored food
# reference: see https://docs.google.com/spreadsheets/d/1f9eVD14Y2d9vmLFP3OsJPFA5d2JXBU-63MTz8MlB1rY/edit#gid=756212200
GREENHOUSE_PERCENT_KCALS=[0,0,0,0,0,11.60,11.60,11.60,23.21,23.21,23.21,34.81,34.81,34.81,46.41,46.41,46.41,58.01,58.01,58.01,69.62,69.62,69.62,81.22,81.22,81.22,92.82,92.82,92.82,104.43,104.43,104.43,116.03,116.03,116.03,127.63,127.63,127.63,139.24,139.24,139.24,139.24,139.24,139.24,139.24,139.24,139.24,139.24,139.24,139.24,139.24,139.24,139.24,139.24,139.24,139.24,139.24,139.24,139.24,139.24,139.24,139.24,139.24,139.24,139.24,139.24,139.24,139.24,139.24,139.24,139.24]

if(ADD_GREENHOUSES):
	production_kcals_greenhouses_per_month = []
	for x in GREENHOUSE_PERCENT_KCALS:
		production_kcals_greenhouses_per_month.append(x / 100 * KCAL_REQ_PER_MONTH)
else:
	production_kcals_greenhouses_per_month=[0]*len(GREENHOUSE_PERCENT_KCALS)

# we know:
# 	units_sf_mass*SF_FRACTION_KCALS=sf_kcals
# and
# 	units_sf_mass*SF_FRACTION_PROTEIN=sf_protein
# so
# 	units_sf_mass = sf_kcals/SF_FRACTION_KCALS
# => assumption listed previously =>
# 	units_gh_mass = gh_kcals/SF_FRACTION_KCALS
# 	units_gh_mass = gh_protein/SF_FRACTION_PROTEIN
# therefore
# 	gh_protein = gh_kcals*SF_FRACTION_PROTEIN/SF_FRACTION_KCALS

production_protein_greenhouses_per_month = \
	np.array(production_kcals_greenhouses_per_month) \
	* SF_FRACTION_PROTEIN / SF_FRACTION_KCALS  / 1e9

production_fat_greenhouses_per_month = \
	np.array(production_kcals_greenhouses_per_month) \
	* SF_FRACTION_FAT / SF_FRACTION_KCALS   / 1e9

# #mass initial, units don't matter, we only need to ensure we use the correct 
# #fraction of kcals, fat, and protein per unit greenhouse grown food.
# #we use stored food fractions here per assumption mentioned above.
# production_kcals_greenhouses_per_month = \
# 	np.array(production_kcals_greenhouses_per_month) * SF_FRACTION_PROTEIN

####LIVESTOCK, EGG, DAIRY INITIAL VARIABLES####

#https://docs.google.com/spreadsheets/d/1-upBP5-iPtBzyjm5zbeGlfuE4FwqLUyR/edit#gid=2007828143
#per kg, whole milk, per nutrition calculator
MILK_KCALS = 610
MILK_FAT = .032 #kg
MILK_PROTEIN = .033 #kg

#1000 tons to billions of kcals = grams/kcals
MILK_FAT_TO_KCAL_RATIO = MILK_FAT/MILK_KCALS
MILK_PROTEIN_TO_KCAL_RATIO = MILK_PROTEIN/MILK_KCALS

# "FAOSTAT Food Balances", cell z 148
#https://docs.google.com/spreadsheets/d/1-upBP5-iPtBzyjm5zbeGlfuE4FwqLUyR/edit#gid=102948593 
# !!!assume all dairy from large animals!!!
# at start, from all large animals, milk contribution over a month

#gallons per cow times calories per cow gives total milk cows
#!!!THESE NUMBERS ARE PRELIMINARY, NEED FUTURE ADJUSTMENT!!! (I googled these numbers)

#1000s of Tons
MILK_FAT_PER_1000_COWS_PER_MONTH= MILK_FAT/MILK_KCALS \
	* (MILK_KCALS_PER_1000_COWS_PER_MONTH / 1000) \
	* KG_TO_1000_TONS \
	* 1000

#1000s of Tons
MILK_PROTEIN_PER_1000_COWS_PER_MONTH=MILK_PROTEIN/MILK_KCALS \
	* (MILK_KCALS_PER_1000_COWS_PER_MONTH / 1000) \
	* KG_TO_1000_TONS \
	* 1000

#mike's spreadsheet "area and scaling by month"
#https://docs.google.com/spreadsheets/d/1-upBP5-iPtBzyjm5zbeGlfuE4FwqLUyR/edit#gid=642022040


dairy_animals_1000s_start=[0]*NMONTHS
dairy_animals_1000s_end=[0]*NMONTHS
dairy_animals_1000s_eaten=[0]*NMONTHS



#### CONSTANTS FOR CELLULOSIC SUGAR ####

#in billions of calories

CELL_SUGAR_PERCENT_KCALS = [0.00, 0.00, 0.00, 0.00, 0.00, 9.79, 9.79, 9.79, 19.57, 23.48, 24.58, 28.49, 28.49,
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
	production_kcals_cell_sugar_per_month = []
	for x in CELL_SUGAR_PERCENT_KCALS:
		production_kcals_cell_sugar_per_month.append(x / 100 * KCAL_REQ_PER_MONTH)
else:
	production_kcals_cell_sugar_per_month=[0]*len(CELL_SUGAR_PERCENT_KCALS)

if(VERBOSE):
	print("INITIAL_MILK_COWS_THOUSANDS, billions")
	print(INITIAL_MILK_COWS_THOUSANDS/1e9)
	print("Number of large animals, billions")
	print((INIT_LARGE_NONDAIRY_ANIMALS+INITIAL_MILK_COWS_THOUSANDS)/1e9)
	print("Percent Dairy Animals of large animals")
	print(INITIAL_MILK_COWS_THOUSANDS/(INIT_LARGE_NONDAIRY_ANIMALS+INITIAL_MILK_COWS_THOUSANDS)*100)

	print('millions of people fed for a year from eating milk cows')
	print(INITIAL_MILK_COWS_THOUSANDS*1000*FAT_PER_LARGE_ANIMAL/(12*FAT_MONTHLY)/1e6)

	print("billions of people fed for a year from eating all livestock minus dairy cows and egg laying hens")
	print(INIT_NONEGG_NONDAIRY_MEAT_FAT/(12*FAT_MONTHLY)/1e9)

#### OTHER VARIABLES ####

humans_fed_fat = [0]*NMONTHS
humans_fed_protein = [0]*NMONTHS
humans_fed_kcals = [0]*NMONTHS
maximize_constraints=[] #used only for validation
allvariables=[z] #used only for validation

#store variables useful for analysis
constants={}
constants['NMONTHS']=NMONTHS
constants['NDAYS']=NDAYS
constants['ADD_STORED_FOOD']=ADD_STORED_FOOD
constants['ADD_SEAWEED']=ADD_SEAWEED
constants['ADD_GREENHOUSES']=ADD_GREENHOUSES
constants['ADD_NONEGG_NONDAIRY_MEAT']=ADD_NONEGG_NONDAIRY_MEAT
constants['ADD_DAIRY']=ADD_DAIRY
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
constants['SF_FRACTION_FAT']=SF_FRACTION_FAT
constants['SF_FRACTION_PROTEIN']=SF_FRACTION_PROTEIN
constants['MEAT_FRACTION_KCALS']=MEAT_FRACTION_KCALS
constants['MEAT_FRACTION_FAT']=MEAT_FRACTION_FAT
constants['MEAT_FRACTION_PROTEIN']=MEAT_FRACTION_PROTEIN
constants['MILK_KCALS_PER_1000_COWS_PER_MONTH']=MILK_KCALS_PER_1000_COWS_PER_MONTH
constants['MILK_FAT_PER_1000_COWS_PER_MONTH']=MILK_FAT_PER_1000_COWS_PER_MONTH
constants['MILK_PROTEIN_PER_1000_COWS_PER_MONTH']=MILK_PROTEIN_PER_1000_COWS_PER_MONTH
constants['KCALS_PER_1000_LARGE_ANIMALS']=KCALS_PER_1000_LARGE_ANIMALS
constants['FAT_PER_1000_LARGE_ANIMALS']=FAT_PER_1000_LARGE_ANIMALS
constants['PROTEIN_PER_1000_LARGE_ANIMALS']=PROTEIN_PER_1000_LARGE_ANIMALS
constants['SEAWEED_KCALS']=SEAWEED_KCALS
constants['SEAWEED_FAT']=SEAWEED_FAT
constants['SEAWEED_PROTEIN']=SEAWEED_PROTEIN
constants['INITIAL_SF']=INITIAL_SF
constants['INITIAL_NONEGG_NONDAIRY_MEAT']=INITIAL_NONEGG_NONDAIRY_MEAT
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

		allvariables.append(used_area[d])
		allvariables.append(seaweed_wet_on_farm[d])

		allvariables.append(seaweed_food_produced[d])
		sum_food_this_month.append(seaweed_food_produced[d])

	seaweed_food_produced_monthly[m] = LpVariable(name="Seaweed_Food_Produced_Monthly_"+str(m)+"_Variable", lowBound=0)
	

	model += (seaweed_food_produced_monthly[m] == np.sum(sum_food_this_month),
		"Seaweed_Food_Produced_Monthly_"+str(m)+"_Constraint")


	allvariables.append(seaweed_food_produced_monthly[m])

	return model


#incorporate linear constraints for stored food consumption each month
def add_stored_food_to_model(model, m):
	stored_food_start[m] = LpVariable("Stored_Food_Start_Month_"+str(m)+"_Variable", 0,INITIAL_SF)
	stored_food_end[m] = LpVariable("Stored_Food_End_Month_"+str(m)+"_Variable", 0,INITIAL_SF)
	stored_food_eaten[m] = LpVariable("Stored_Food_Eaten_During_Month_"+str(m)+"_Variable",0,INITIAL_SF)
	
	if(m==0): #first Month
		model += (stored_food_start[0] <= INITIAL_SF, "Stored_Food_Start_Month_0_Constraint")
	else:
		model += (stored_food_start[m] <= stored_food_end[m-1], "Stored_Food_Start_Month_"+str(m)+"_Constraint")

	model += (stored_food_end[m] <= stored_food_start[m] - stored_food_eaten[m], "Stored_Food_End_Month_"+str(m)+"_Constraint")

	allvariables.append(stored_food_start[m])
	allvariables.append(stored_food_end[m])
	allvariables.append(stored_food_eaten[m])

	return model

#### LIVESTOCK: NONDAIRY MEAT, NON EGGS ####

#assumes all meat is fed using grasslands
#no difference in waste between carcass meat and other food sources yet
#dairy cows and egg-laying chickens are modeled separately
#this can be treated essentially as stored food
#assume there's no population growth of cows

#incorporate linear constraints for nonegg_nondairy meat consumption each month
def add_nonegg_nondairy_meat_to_model(model, m):
	nonegg_nondairy_meat_start[m] = LpVariable("Non_Egg_Nondairy_Meat_Start_"+str(m)+"_Variable", 0,INITIAL_NONEGG_NONDAIRY_MEAT)
	nonegg_nondairy_meat_end[m] = LpVariable("Non_Egg_Nondairy_Meat_End_"+str(m)+"_Variable", 0,INITIAL_NONEGG_NONDAIRY_MEAT)
	nonegg_nondairy_meat_eaten[m] = LpVariable("Non_Egg_Nondairy_Meat_Eaten_During_Month_"+str(m)+"_Variable",0,INITIAL_NONEGG_NONDAIRY_MEAT)
	
	if(m==0): #first Month
		model += (nonegg_nondairy_meat_start[0] <= INITIAL_NONEGG_NONDAIRY_MEAT, "Non_Egg_Nondairy_Meat_Start_Month_0_Constraint")
	else:
		model += (nonegg_nondairy_meat_start[m] <= nonegg_nondairy_meat_end[m-1], "Non_Egg_Nondairy_Meat_Start_Month_"+str(m)+"_Constraint")

	model += (nonegg_nondairy_meat_end[m] <= nonegg_nondairy_meat_start[m] - nonegg_nondairy_meat_eaten[m], "Non_Egg_Nondairy_Meat_End_Month_"+str(m)+"_Constraint")

	allvariables.append(nonegg_nondairy_meat_start[m])
	allvariables.append(nonegg_nondairy_meat_end[m])
	allvariables.append(nonegg_nondairy_meat_eaten[m])

	return model

#### LIVESTOCK: MILK, EGGS ####
#no resources currently are used by dairy cows or chickens
#the only trade-off is between eating their meat vs eating their milk or eggs  

def add_eggs_to_model(model, m):
	pass
	#small_nonegg_animals_start

#dairy animals are all assumed to be large animals
def add_dairy_to_model(model, m):
	# print(INITIAL_MILK_COWS_THOUSANDS)
	dairy_animals_1000s_start[m] = LpVariable("Dairy_Animals_Start_"+str(m)+"_Variable", 0,INITIAL_MILK_COWS_THOUSANDS)
	dairy_animals_1000s_end[m] = LpVariable("Dairy_Animals_End_"+str(m)+"_Variable", 0,INITIAL_MILK_COWS_THOUSANDS)
	dairy_animals_1000s_eaten[m] = LpVariable("Dairy_Animals_Eaten_During_Month_"+str(m)+"_Variable",0,INITIAL_MILK_COWS_THOUSANDS)
	
	if(m==0): #first Month
		model += (dairy_animals_1000s_start[0] <= INITIAL_MILK_COWS_THOUSANDS, "Dairy_Animals_Start_Month_0_Constraint")
	else:
		model += (dairy_animals_1000s_start[m] <= dairy_animals_1000s_end[m-1], 
			"Dairy_Animals_Start_Month_"+str(m)+"_Constraint")

	model += (dairy_animals_1000s_end[m] <= dairy_animals_1000s_start[m] \
		- dairy_animals_1000s_eaten[m],
		"Dairy_Animals_Eaten_Month_"+str(m)+"_Constraint")

	allvariables.append(dairy_animals_1000s_start[m])
	allvariables.append(dairy_animals_1000s_end[m])
	allvariables.append(dairy_animals_1000s_eaten[m])

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

	allvariables.append(humans_fed_fat[m])
	allvariables.append(humans_fed_protein[m])
	allvariables.append(humans_fed_kcals[m])


	if(ADD_SEAWEED and LIMIT_SEAWEED_AS_PERCENT_KCALS):
		model += (seaweed_food_produced_monthly[m]*SEAWEED_KCALS <= 
			(MAX_SEAWEED_AS_PERCENT_KCALS/100)*(humans_fed_kcals[m]*KCALS_MONTHLY),
			"Seaweed_Limit_Kcals_"+str(m)+"_Constraint")

		# allvariables.append(humans_fed_fat[m])

	#finds billions of people fed that month per nutrient

	#stored food eaten*sf_fraction_kcals is in units billions kcals monthly
	#seaweed_food_produced_monthly*seaweed_kcals is in units billions kcals
	#kcals monthly is in units kcals
	model += (humans_fed_kcals[m] == 
		(stored_food_eaten[m]*SF_FRACTION_KCALS
		+ seaweed_food_produced_monthly[m]*SEAWEED_KCALS
		+ dairy_animals_1000s_eaten[m]*KCALS_PER_1000_LARGE_ANIMALS
		+ (dairy_animals_1000s_start[m]+dairy_animals_1000s_end[m])/2 \
			* MILK_KCALS_PER_1000_COWS_PER_MONTH
		+ nonegg_nondairy_meat_eaten[m]*MEAT_FRACTION_KCALS
		+ production_kcals_cell_sugar_per_month[m]
		+ production_kcals_greenhouses_per_month[m])/KCALS_MONTHLY,
		"Kcals_Fed_Month_"+str(m)+"_Constraint")

	#stored_food_eaten*sf_fraction_fat is in units thousand tons monthly
	#seaweed_food_produced_monthly*seaweed_fat is in units thousand tons monthly
	#fat monthly is in units thousand tons
	# print("MEAT_FRACTION_FAT")
	# print(MEAT_FRACTION_FAT)
	# print("FAT_PER_LARGE_ANIMAL")
	# print(FAT_PER_LARGE_ANIMAL)
	# quit()
	model += (humans_fed_fat[m] == 
		(stored_food_eaten[m]*SF_FRACTION_FAT 
		+ seaweed_food_produced_monthly[m]*SEAWEED_FAT
		+ dairy_animals_1000s_eaten[m]*FAT_PER_1000_LARGE_ANIMALS
		+ (dairy_animals_1000s_start[m]+dairy_animals_1000s_end[m])/2 \
			* MILK_FAT_PER_1000_COWS_PER_MONTH
		+ production_fat_greenhouses_per_month[m]
		+ nonegg_nondairy_meat_eaten[m]*MEAT_FRACTION_FAT)/FAT_MONTHLY/1e9,
		"Fat_Fed_Month_"+str(m)+"_Constraint")
	
	#stored_food_eaten*sf_fraction_protein is in units thousand tons monthly
	#seaweed_food_produced_monthly*seaweed_protein is in units thousand tons monthly
	#fat monthly is in units thousand tons
	model += (humans_fed_protein[m] == 
		(stored_food_eaten[m]*SF_FRACTION_PROTEIN
		+ seaweed_food_produced_monthly[m]*SEAWEED_PROTEIN
		+ dairy_animals_1000s_eaten[m]*PROTEIN_PER_1000_LARGE_ANIMALS
		+ (dairy_animals_1000s_start[m]+dairy_animals_1000s_end[m])/2 \
			* MILK_PROTEIN_PER_1000_COWS_PER_MONTH
		+ production_protein_greenhouses_per_month[m]
		+ nonegg_nondairy_meat_eaten[m]*MEAT_FRACTION_PROTEIN)/PROTEIN_MONTHLY/1e9,
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

	if(ADD_NONEGG_NONDAIRY_MEAT):
		model = add_nonegg_nondairy_meat_to_model(model,m)

	if(ADD_DAIRY):
		model = add_dairy_to_model(model,m)

	if(ADD_EGGS):
		model = add_eggs_to_model(model,m)

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
	allvariables,
	VERBOSE)

print('')	
print('')	
print('RESULTS')	
print('')	
print('')

print(f"objective: {model.objective.value()}")

if(VERBOSE):
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
	seaweed_food_produced,#daily
	seaweed_food_produced_monthly,
	show_output
)

# if no cellulosic sugar, will be zero
analysis.analyze_CS_results(
	production_kcals_cell_sugar_per_month,
	show_output
)

# if no greenhouses, will be zero
analysis.analyze_GH_results(
	production_kcals_greenhouses_per_month,
	production_fat_greenhouses_per_month,
	production_protein_greenhouses_per_month,
	show_output
)

#if nonegg nondairy meat isn't included, these results will be zero
analysis.analyze_nonegg_nondairy_results(
	nonegg_nondairy_meat_start,
	nonegg_nondairy_meat_end,
	nonegg_nondairy_meat_eaten,
	show_output
)

#if dairy isn't included, these results will be zero
analysis.analyze_dairy_results(
	dairy_animals_1000s_start,
	dairy_animals_1000s_end,
	dairy_animals_1000s_eaten,
	show_output
)

if(ADD_CELLULOSIC_SUGAR):
	Plotter.plot_CS(time_months_middle,analysis)

if(ADD_STORED_FOOD):
	Plotter.plot_stored_food(time_months,analysis)
if(ADD_SEAWEED):
	Plotter.plot_seaweed(time_months_middle,analysis)

if(ADD_NONEGG_NONDAIRY_MEAT):
	Plotter.plot_nonegg_nondairy_meat(time_months,analysis)

if(ADD_DAIRY):
	Plotter.plot_dairy_cows(time_months_middle,analysis)
	Plotter.plot_dairy(time_months_middle,analysis)

Plotter.plot_people_fed(time_months_middle,analysis)

#if we don't have stored food, and we are optimizing last 150 days,
# we can compare to Aron's data.
if(ADD_SEAWEED and (not ADD_STORED_FOOD) and MAXIMIZE_ONLY_FOOD_AFTER_DAY_150):
	Plotter.plot_seaweed_comparison(time_days_daily,time_days_monthly,analysis)