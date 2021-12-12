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
import numpy as np
c = {} #c = constants
c['CHECK_CONSTRAINTS'] = False

c['inputs'] = {}

c['inputs']['NMONTHS'] = 84
c['inputs']['LIMIT_SEAWEED_AS_PERCENT_KCALS'] = True

c['inputs']['NUTRITION']={}
c['inputs']['NUTRITION']['KCALS_DAILY'] = 2100 #kcals per person per day
c['inputs']['NUTRITION']['FAT_DAILY'] = 47#35 #grams per person per day
c['inputs']['NUTRITION']['PROTEIN_DAILY'] = 51#46 #grams per person per day

c['inputs']['MAX_SEAWEED_AS_PERCENT_KCALS'] = 10
c['inputs']['NEW_AREA_PER_DAY'] = 4.153 # 1000 km^2 (seaweed)
c['inputs']['SEAWEED_PRODUCTION_RATE'] = 10 # percent (seaweed)

# "Outputs" https://docs.google.com/spreadsheets/d/19kzHpux690JTCo2IX2UA1faAd7R1QcBK/edit#gid=1815939673 cell G12-G14
c['inputs']['TONS_DRY_CALORIC_EQIVALENT_SF'] = 1360e6
c['inputs']['INITIAL_SF_PROTEIN'] = 166071 #1000 tons protein per unit mass initial
c['inputs']['INITIAL_SF_FAT'] = 69254 # 1000 tons fat per unit mass 

c["inputs"]["OG_USE_BETTER_ROTATION"] = False

c['inputs']['INCLUDE_PROTEIN'] = True
c['inputs']['INCLUDE_FAT'] = True

c['inputs']['GREENHOUSE_GAIN_PCT'] = 0

c['inputs']['GREENHOUSE_SLOPE_MULTIPLIER'] = 1 #default values from greenhouse paper
c['inputs']['INDUSTRIAL_FOODS_SLOPE_MULTIPLIER'] = 1 #default values from CS paper

c['inputs']['INITIAL_HARVEST_DURATION'] = 7 # months

c['inputs']['IS_NUCLEAR_WINTER'] = True
c['inputs']['FLUCTUATION_LIMIT'] = 1.5
c['inputs']['KCAL_SMOOTHING'] = False
c['inputs']['MEAT_SMOOTHING'] = False
c['inputs']['STORED_FOOD_SMOOTHING'] = False

c['inputs']['ADD_CELLULOSIC_SUGAR'] = False
c['inputs']['ADD_DAIRY'] = True
c['inputs']['ADD_FISH'] = True
c['inputs']['ADD_GREENHOUSES'] = False
c['inputs']['ADD_OUTDOOR_GROWING'] = True
c['inputs']['ADD_MEAT'] = True
c['inputs']['ADD_METHANE_SCP'] = False
c['inputs']['ADD_SEAWEED'] = False
c['inputs']['ADD_STORED_FOOD'] = True

c["inputs"]["EXCESS_CALORIES"] = np.array([0]*c['inputs']['NMONTHS'])
c['inputs']['FEED_SHUTOFF_DELAY'] = 0 # months
c['inputs']['BIOFUEL_SHUTOFF_DELAY'] = 0 # months

c["inputs"]["CULL_DURATION"] = 3
c['inputs']['RECALCULATE_CULL_DURATION'] = False #thousand tons

c['inputs']['WASTE'] = {}
c['inputs']['WASTE']['CEREALS'] = 0 #%
c['inputs']['WASTE']['SUGAR'] = 0 #%
c['inputs']['WASTE']['MEAT'] = 0 #%
c['inputs']['WASTE']['DAIRY'] = 0 #%
c['inputs']['WASTE']['SEAFOOD'] = 0 #%
c['inputs']['WASTE']['CROPS'] = 0 #%
c['inputs']['WASTE']['SEAWEED'] = 0 #%

optimizer = Optimizer()
[time_months,time_months_middle,analysis]=optimizer.optimize(c)

print("")
print("")
print("")
print("")
print("people_fed_billions")
print(analysis.people_fed_billions)
print("")
print("")
print("")
print("")

Plotter.plot_people_fed_combined(time_months_middle,analysis)
Plotter.plot_people_fed_kcals(time_months_middle,analysis,\
	'Primary production before waste, no resilient foods')

# nuclear winter 150 tab, cell G30-G38  https://docs.google.com/spreadsheets/d/14t3_PUIky6aNiBvw8q24sj6QYxCN9s_VddLY2-eJuPE/edit#gid=1637082097
#overall waste, on farm+distribution+retail
#2x prices (note, currently set to 2019, not 2020)
c['inputs']['WASTE'] = {}
c['inputs']['WASTE']['CEREALS'] = 14.46 #%
c['inputs']['WASTE']['SUGAR'] = 9.91 #%
c['inputs']['WASTE']['MEAT'] = 10.61 #%
c['inputs']['WASTE']['DAIRY'] = 11.93 #%
c['inputs']['WASTE']['SEAFOOD'] = 9.99 #%
c['inputs']['WASTE']['CROPS'] = 14.78 #%
c['inputs']['WASTE']['SEAWEED'] = 9.81 #%

c["inputs"]["EXCESS_CALORIES"] = np.array([0]*c['inputs']['NMONTHS'])
c['inputs']['FEED_SHUTOFF_DELAY'] = 3 # months
c['inputs']['BIOFUEL_SHUTOFF_DELAY'] = 2 # months

c["inputs"]["CULL_DURATION"] = 3
c['inputs']['RECALCULATE_CULL_DURATION'] = False #thousand tons

[time_months,time_months_middle,analysis]=optimizer.optimize(c)

print("")
print("")
print("")
print("")
print("people_fed_billions")
print(analysis.people_fed_billions)
print("")
print("")
print("")
print("")

if(c['inputs']['ADD_OUTDOOR_GROWING']):
	Plotter.plot_OG_no_resilient_foods(time_months_middle,analysis)

Plotter.plot_people_fed_combined(time_months_middle,analysis)
Plotter.plot_people_fed_kcals(time_months_middle,analysis,"Food minus waste & delayed halt of nonhuman consumption, no resilient foods")

# if(c['inputs']['ADD_STORED_FOOD']):
# 	Plotter.plot_stored_food(time_months_middle,analysis)

# if(c['inputs']['ADD_SEAWEED']):
# 	Plotter.plot_seaweed(time_months_middle,analysis)

# if(c['inputs']['ADD_MEAT']):
# 	Plotter.plot_meat(time_months,analysis)

# if(c['inputs']['ADD_DAIRY']):
# 	Plotter.plot_dairy_cows(time_months_middle,analysis)
# 	Plotter.plot_dairy(time_months_middle,analysis)

# # c['inputs']['WASTE']['CEREALS'] = 19.02+10.5 #%
# c['inputs']['WASTE']['CEREALS'] = 4.65 #%
# # c['inputs']['WASTE']['SUGAR'] = 14.47+10.5 #%
# c['inputs']['WASTE']['SUGAR'] = 0.09 #%
# # c['inputs']['WASTE']['MEAT'] = 15.17+10.5 #%
# c['inputs']['WASTE']['MEAT'] = .80 #%
# # c['inputs']['WASTE']['DAIRY'] = 16.49+10.5 #%
# c['inputs']['WASTE']['DAIRY'] = 2.120 #%
# # c['inputs']['WASTE']['SEAFOOD'] = 14.55+10.5 #%
# c['inputs']['WASTE']['SEAFOOD'] = 0.17 #%
# # c['inputs']['WASTE']['CROPS'] = 23.87+4.96 #%
# c['inputs']['WASTE']['CROPS'] = 4.96
# # c['inputs']['WASTE']['SEAWEED'] = 14.37+10.5 #%
# c['inputs']['WASTE']['SEAWEED'] = 0 #%

# c['inputs']['WASTE']['CEREALS'] = 19.02 #%
# c['inputs']['WASTE']['SUGAR'] = 14.47 #%
# c['inputs']['WASTE']['MEAT'] = 15.17 #%
# c['inputs']['WASTE']['DAIRY'] = 16.49 #%
# c['inputs']['WASTE']['SEAFOOD'] = 14.55 #%
# c['inputs']['WASTE']['CROPS'] = 19.33 #%
# c['inputs']['WASTE']['SEAWEED'] = 14.37 #%
# Plotter.plot_people_fed_fat(time_months_middle,analysis)
# Plotter.plot_people_fed_protein(time_months_middle,analysis)
# Plotter.plot_people_fed_comparison(time_months_middle,analysis)
# c['inputs']['ADD_SEAWEED'] = False
# c['inputs']['ADD_CELLULOSIC_SUGAR'] = True
# c['inputs']['ADD_GREENHOUSES'] = True
# c['inputs']['ADD_MEAT'] = True
# c['inputs']['ADD_DAIRY'] = True
# c['inputs']['ADD_STORED_FOOD'] = True
# c['inputs']['ADD_OUTDOOR_GROWING'] = True

# seaweed_omitted=optimizer.optimize(c)
# print('seaweed omitted')
# print(seaweed_omitted-max_fed)


# c['inputs']['ADD_SEAWEED'] = True
# c['inputs']['ADD_CELLULOSIC_SUGAR'] = False
# c['inputs']['ADD_GREENHOUSES'] = True
# c['inputs']['ADD_MEAT'] = True
# c['inputs']['ADD_DAIRY'] = True
# c['inputs']['ADD_STORED_FOOD'] = True
# c['inputs']['ADD_OUTDOOR_GROWING'] = True
# cell_sugar_omitted=optimizer.optimize(c)
# print('cellulosic sugar omitted')
# print(cell_sugar_omitted-max_fed)


# c['inputs']['ADD_SEAWEED'] = True
# c['inputs']['ADD_CELLULOSIC_SUGAR'] = True
# c['inputs']['ADD_GREENHOUSES'] = False
# c['inputs']['ADD_MEAT'] = True
# c['inputs']['ADD_DAIRY'] = True
# c['inputs']['ADD_STORED_FOOD'] = True
# c['inputs']['ADD_OUTDOOR_GROWING'] = True
# greenhouses_omitted=optimizer.optimize(c)
# print('greenhouses omitted')
# print(greenhouses_omitted-max_fed)


# c['inputs']['ADD_SEAWEED'] = False
# c['inputs']['ADD_CELLULOSIC_SUGAR'] = False
# c['inputs']['ADD_GREENHOUSES'] = False
# c['inputs']['ADD_MEAT'] = True
# c['inputs']['ADD_DAIRY'] = True
# c['inputs']['ADD_STORED_FOOD'] = True
# c['inputs']['ADD_OUTDOOR_GROWING'] = True
# no_intervention=optimizer.optimize(c)
# print('no intervention')
# print(no_intervention)


# c['inputs']['ADD_SEAWEED'] = True
# c['inputs']['ADD_CELLULOSIC_SUGAR'] = False
# c['inputs']['ADD_GREENHOUSES'] = False
# c['inputs']['ADD_MEAT'] = True
# c['inputs']['ADD_DAIRY'] = True
# c['inputs']['ADD_STORED_FOOD'] = True
# c['inputs']['ADD_OUTDOOR_GROWING'] = True
# just_seaweed=optimizer.optimize(c)
# print('just seaweed')
# print(just_seaweed-no_intervention)


# c['inputs']['ADD_SEAWEED'] = False
# c['inputs']['ADD_CELLULOSIC_SUGAR'] = True
# c['inputs']['ADD_GREENHOUSES'] = False
# c['inputs']['ADD_MEAT'] = True
# c['inputs']['ADD_DAIRY'] = True
# c['inputs']['ADD_STORED_FOOD'] = True
# c['inputs']['ADD_OUTDOOR_GROWING'] = True
# just_cell_sugar=optimizer.optimize(c)
# print('just CS')
# print(just_cell_sugar-no_intervention)



# c['inputs']['ADD_SEAWEED'] = False
# c['inputs']['ADD_CELLULOSIC_SUGAR'] = False
# c['inputs']['ADD_GREENHOUSES'] = True
# c['inputs']['ADD_MEAT'] = True
# c['inputs']['ADD_DAIRY'] = True
# c['inputs']['ADD_STORED_FOOD'] = True
# c['inputs']['ADD_OUTDOOR_GROWING'] = True
# just_greenhouses=optimizer.optimize(c)
# print('just Greenhouses')
# print(just_greenhouses-no_intervention)
