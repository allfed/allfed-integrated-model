# this program runs the optimizer model, and ensures that all the results are 
# reasonable using a couple useful checks to make sure there's nothing wacky 
# going on.

#check that as time increases, more people can be fed

#check that stored food plus meat is always used at the 
#highest rate during the largest food shortage.

import os
import sys
module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
	sys.path.append(module_path)
from src.optimizer import Optimizer
from src.plotter import Plotter
constants = {}
constants['inputs'] = {}

constants['inputs']['NMONTHS'] = 78
constants['inputs']['LIMIT_SEAWEED_AS_PERCENT_KCALS'] = True

constants['inputs']['WASTE'] = {}
# constants['inputs']['WASTE']['CEREALS'] = 19.02+10.5 #%
constants['inputs']['WASTE']['CEREALS'] = 0 #%
# constants['inputs']['WASTE']['SUGAR'] = 14.47+10.5 #%
constants['inputs']['WASTE']['SUGAR'] = 0 #%
# constants['inputs']['WASTE']['MEAT'] = 15.17+10.5 #%
constants['inputs']['WASTE']['MEAT'] = 0 #%
# constants['inputs']['WASTE']['DAIRY'] = 16.49+10.5 #%
constants['inputs']['WASTE']['DAIRY'] = 0 #%
# constants['inputs']['WASTE']['SEAFOOD'] = 14.55+10.5 #%
constants['inputs']['WASTE']['SEAFOOD'] = 0 #%
# constants['inputs']['WASTE']['CROPS'] = 23.87+4.96 #%
constants['inputs']['WASTE']['CROPS'] = 0
# constants['inputs']['WASTE']['SEAWEED'] = 14.37+10.5 #%
constants['inputs']['WASTE']['SEAWEED'] = 0 #%

constants['inputs']['BIOFUEL_SHUTOFF_DELAY'] = 0 # months
constants['inputs']['M1_ADDITIONAL_WASTE'] = 5e9/12#tons dry caloric equivalent
constants['inputs']['NUTRITION']={}
constants['inputs']['NUTRITION']['KCALS_DAILY'] = 2100 #kcals per person per day
constants['inputs']['NUTRITION']['FAT_DAILY'] = 35 #grams per person per day
constants['inputs']['NUTRITION']['PROTEIN_DAILY'] = 51 #grams per person per day

constants['inputs']['INITIAL_MILK_COWS'] = 264e6
constants['inputs']['MAX_SEAWEED_AS_PERCENT_KCALS'] = 10
constants['inputs']['INIT_SMALL_ANIMALS'] = 28.2e9
constants['inputs']['INIT_MEDIUM_ANIMALS'] = 3.2e9
constants['inputs']['INIT_LARGE_ANIMALS'] = 1.9e9
constants['inputs']['HARVEST_LOSS'] = 15 # percent (seaweed)
constants['inputs']['INITIAL_SEAWEED'] = 1 # 1000 tons (seaweed)
constants['inputs']['INITIAL_AREA'] = 1 # 1000 tons (seaweed)
constants['inputs']['NEW_AREA_PER_DAY'] = 4.153 # 1000 km^2 (seaweed)
constants['inputs']['MINIMUM_DENSITY'] = 400 #tons/km^2 (seaweed)
constants['inputs']['MAXIMUM_DENSITY'] = 4000 #tons/km^2 (seaweed)
constants['inputs']['MAXIMUM_AREA'] = 1000 # 1000 km^2 (seaweed)
constants['inputs']['SEAWEED_PRODUCTION_RATE'] = 10 # percent (seaweed)
#trying to 
constants['inputs']['TONS_DRY_CALORIC_EQIVALENT_SF'] = 1602542*1000./10*3
constants['inputs']['INITIAL_SF_PROTEIN'] = 203607 #1000 tons protein per unit mass initial
constants['inputs']['INITIAL_SF_FAT'] = 63948 # 1000 tons fat per unit mass initial

constants['inputs']['RATIO_KCALS_POSTDISASTER']={}
constants['inputs']['RATIO_KCALS_POSTDISASTER']['Y1'] = 1
constants['inputs']['RATIO_KCALS_POSTDISASTER']['Y2'] = 1
constants['inputs']['RATIO_KCALS_POSTDISASTER']['Y3'] = 1
constants['inputs']['RATIO_KCALS_POSTDISASTER']['Y4'] = 1
constants['inputs']['RATIO_KCALS_POSTDISASTER']['Y5'] = 1
constants['inputs']['RATIO_KCALS_POSTDISASTER']['Y6'] = 1
constants['inputs']['RATIO_KCALS_POSTDISASTER']['Y7'] = 1
constants['inputs']['RATIO_KCALS_POSTDISASTER']['Y8'] = 1
constants['inputs']['RATIO_KCALS_POSTDISASTER']['Y9'] = 1
constants['inputs']['RATIO_KCALS_POSTDISASTER']['Y10'] = 1
constants['inputs']['RATIO_KCALS_POSTDISASTER']['Y11'] = 1
constants['inputs']['DAIRY_PRODUCTION'] = 1 #multiplies current dairy productivity (based on stress of animals)
constants['inputs']['GREENHOUSE_FAT_MULTIPLIER'] = 1 # we can grow twice as much fat as greenhouses would have
constants['inputs']['GREENHOUSE_SLOPE_MULTIPLIER'] = 1 #default values from greenhouse paper
constants['inputs']['INDUSTRIAL_FOODS_SLOPE_MULTIPLIER'] = 1 #default values from CS paper

constants['inputs']['NO_RESILIENT_FOODS'] = True

constants['inputs']['INCLUDE_PROTEIN'] = False
constants['inputs']['INCLUDE_FAT'] = False
constants['inputs']['MEAT_SUSTAINABLE_YIELD_PER_YEAR'] = 222
constants['inputs']['IS_NUCLEAR_WINTER'] = False

constants['inputs']['ADD_FISH'] = False
constants['inputs']['ADD_SEAWEED'] = False
constants['inputs']['ADD_CELLULOSIC_SUGAR'] = False
constants['inputs']['ADD_METHANE_SCP'] = False
constants['inputs']['ADD_GREENHOUSES'] = False
constants['inputs']['ADD_NONEGG_NONDAIRY_MEAT'] = True
constants['inputs']['ADD_DAIRY'] = False
constants['inputs']['ADD_STORED_FOOD'] = True
constants['inputs']['ADD_OUTDOOR_GROWING'] = True

constants['inputs']['INCLUDE_ECONOMICS'] = True
constants['CHECK_CONSTRAINTS'] = False
optimizer = Optimizer()

[time_months,time_months_middle,analysis]=optimizer.optimize(constants)

# if(constants['inputs']['ADD_CELLULOSIC_SUGAR']):
# 	Plotter.plot_CS(time_months_middle,analysis)

# if(constants['inputs']['ADD_FISH']):
# 	Plotter.plot_fish(time_months_middle,analysis)

if(constants['inputs']['ADD_GREENHOUSES']):
	Plotter.plot_GH(time_months_middle,analysis)

if(constants['inputs']['ADD_OUTDOOR_GROWING']):
	Plotter.plot_OG_before_nuclear_event(time_months_middle,analysis)

if(constants['inputs']['ADD_STORED_FOOD']):
	Plotter.plot_stored_food(time_months,analysis)

# if(constants['inputs']['ADD_SEAWEED']):
# 	Plotter.plot_seaweed(time_months_middle,analysis)

# if(constants['inputs']['ADD_NONEGG_NONDAIRY_MEAT']):
# 	Plotter.plot_nonegg_nondairy_meat(time_months,analysis)

# if(constants['inputs']['ADD_DAIRY']):
# 	Plotter.plot_dairy_cows(time_months_middle,analysis)
# 	Plotter.plot_dairy(time_months_middle,analysis)

# Plotter.plot_people_fed(time_months_middle,analysis)
Plotter.plot_people_fed_combined(time_months_middle,analysis)
Plotter.plot_people_fed_kcals_before_nuclear_event(time_months_middle,analysis)
# Plotter.plot_people_fed_fat(time_months_middle,analysis)
# Plotter.plot_people_fed_protein(time_months_middle,analysis)
# Plotter.plot_people_fed_comparison(time_months_middle,analysis)
# constants['inputs']['ADD_SEAWEED'] = False
# constants['inputs']['ADD_CELLULOSIC_SUGAR'] = True
# constants['inputs']['ADD_GREENHOUSES'] = True
# constants['inputs']['ADD_NONEGG_NONDAIRY_MEAT'] = True
# constants['inputs']['ADD_DAIRY'] = True
# constants['inputs']['ADD_STORED_FOOD'] = True
# constants['inputs']['ADD_OUTDOOR_GROWING'] = True

# seaweed_omitted=optimizer.optimize(constants)
# print('seaweed omitted')
# print(seaweed_omitted-max_fed)


# constants['inputs']['ADD_SEAWEED'] = True
# constants['inputs']['ADD_CELLULOSIC_SUGAR'] = False
# constants['inputs']['ADD_GREENHOUSES'] = True
# constants['inputs']['ADD_NONEGG_NONDAIRY_MEAT'] = True
# constants['inputs']['ADD_DAIRY'] = True
# constants['inputs']['ADD_STORED_FOOD'] = True
# constants['inputs']['ADD_OUTDOOR_GROWING'] = True
# cell_sugar_omitted=optimizer.optimize(constants)
# print('cellulosic sugar omitted')
# print(cell_sugar_omitted-max_fed)


# constants['inputs']['ADD_SEAWEED'] = True
# constants['inputs']['ADD_CELLULOSIC_SUGAR'] = True
# constants['inputs']['ADD_GREENHOUSES'] = False
# constants['inputs']['ADD_NONEGG_NONDAIRY_MEAT'] = True
# constants['inputs']['ADD_DAIRY'] = True
# constants['inputs']['ADD_STORED_FOOD'] = True
# constants['inputs']['ADD_OUTDOOR_GROWING'] = True
# greenhouses_omitted=optimizer.optimize(constants)
# print('greenhouses omitted')
# print(greenhouses_omitted-max_fed)


# constants['inputs']['ADD_SEAWEED'] = False
# constants['inputs']['ADD_CELLULOSIC_SUGAR'] = False
# constants['inputs']['ADD_GREENHOUSES'] = False
# constants['inputs']['ADD_NONEGG_NONDAIRY_MEAT'] = True
# constants['inputs']['ADD_DAIRY'] = True
# constants['inputs']['ADD_STORED_FOOD'] = True
# constants['inputs']['ADD_OUTDOOR_GROWING'] = True
# no_intervention=optimizer.optimize(constants)
# print('no intervention')
# print(no_intervention)


# constants['inputs']['ADD_SEAWEED'] = True
# constants['inputs']['ADD_CELLULOSIC_SUGAR'] = False
# constants['inputs']['ADD_GREENHOUSES'] = False
# constants['inputs']['ADD_NONEGG_NONDAIRY_MEAT'] = True
# constants['inputs']['ADD_DAIRY'] = True
# constants['inputs']['ADD_STORED_FOOD'] = True
# constants['inputs']['ADD_OUTDOOR_GROWING'] = True
# just_seaweed=optimizer.optimize(constants)
# print('just seaweed')
# print(just_seaweed-no_intervention)


# constants['inputs']['ADD_SEAWEED'] = False
# constants['inputs']['ADD_CELLULOSIC_SUGAR'] = True
# constants['inputs']['ADD_GREENHOUSES'] = False
# constants['inputs']['ADD_NONEGG_NONDAIRY_MEAT'] = True
# constants['inputs']['ADD_DAIRY'] = True
# constants['inputs']['ADD_STORED_FOOD'] = True
# constants['inputs']['ADD_OUTDOOR_GROWING'] = True
# just_cell_sugar=optimizer.optimize(constants)
# print('just CS')
# print(just_cell_sugar-no_intervention)



# constants['inputs']['ADD_SEAWEED'] = False
# constants['inputs']['ADD_CELLULOSIC_SUGAR'] = False
# constants['inputs']['ADD_GREENHOUSES'] = True
# constants['inputs']['ADD_NONEGG_NONDAIRY_MEAT'] = True
# constants['inputs']['ADD_DAIRY'] = True
# constants['inputs']['ADD_STORED_FOOD'] = True
# constants['inputs']['ADD_OUTDOOR_GROWING'] = True
# just_greenhouses=optimizer.optimize(constants)
# print('just Greenhouses')
# print(just_greenhouses-no_intervention)
