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
constants = {}
constants['inputs'] = {}

constants['inputs']['NMONTHS'] = 60#84
constants['inputs']['LIMIT_SEAWEED_AS_PERCENT_KCALS'] = True

constants['inputs']['WASTE'] = {}


#overall waste, on farm+distribution+retail
constants['inputs']['WASTE']['CEREALS'] = 19.02 #%
constants['inputs']['WASTE']['SUGAR'] = 14.47 #%
constants['inputs']['WASTE']['MEAT'] = 15.17 #%
constants['inputs']['WASTE']['DAIRY'] = 16.49 #%
constants['inputs']['WASTE']['SEAFOOD'] = 14.55 #%
constants['inputs']['WASTE']['CROPS'] = 19.33 #%
constants['inputs']['WASTE']['SEAWEED'] = 14.37 #%

constants['inputs']['BIOFUEL_SHUTOFF_DELAY'] = 0 # months
constants['inputs']['M1_ADDITIONAL_WASTE'] = 5e9/12#tons dry caloric equivalent
constants['inputs']['NUTRITION']={}
constants['inputs']['NUTRITION']['KCALS_DAILY'] = 2100 #kcals per person per day
constants['inputs']['NUTRITION']['FAT_DAILY'] = 47/2 #grams per person per day
constants['inputs']['NUTRITION']['PROTEIN_DAILY'] = 51/2#grams per person per day

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
constants['inputs']['TONS_DRY_CALORIC_EQIVALENT_SF'] = 1349e6
constants['inputs']['INITIAL_SF_PROTEIN'] = 203607 #1000 tons protein per unit mass initial
constants['inputs']['INITIAL_SF_FAT'] = 63948 # 1000 tons fat per unit mass initial

constants['inputs']['RATIO_KCALS_POSTDISASTER']={}
constants['inputs']['RATIO_KCALS_POSTDISASTER']['Y1'] = 1-.53
constants['inputs']['RATIO_KCALS_POSTDISASTER']['Y2'] = 1-0.82
constants['inputs']['RATIO_KCALS_POSTDISASTER']['Y3'] = 1-.89
constants['inputs']['RATIO_KCALS_POSTDISASTER']['Y4'] = 1-.88
constants['inputs']['RATIO_KCALS_POSTDISASTER']['Y5'] = 1-.84
constants['inputs']['RATIO_KCALS_POSTDISASTER']['Y6'] = 1-.76
constants['inputs']['RATIO_KCALS_POSTDISASTER']['Y7'] = 1-.65
constants['inputs']['RATIO_KCALS_POSTDISASTER']['Y8'] = 1-.5
constants['inputs']['RATIO_KCALS_POSTDISASTER']['Y9'] = 1-.4
constants['inputs']['RATIO_KCALS_POSTDISASTER']['Y10'] = 1-.17
constants['inputs']['RATIO_KCALS_POSTDISASTER']['Y11'] = 1-.08

constants['inputs']['SEASONALITY']=\
	[0.1564,0.0461,0.0650,0.1017,0.0772,0.0785,\
	0.0667,0.0256,0.0163,0.1254,0.1183,0.1228]

MEAT_SUSTAINABLE_YIELD_PER_YEAR = 100.4

MEAT_CURRENT_YIELD_PER_YEAR = 222 #million tons dry caloric

# constants['inputs']['FRACTION_TO_SLAUGHTER'] = 0#\
	# 1-MEAT_SUSTAINABLE_YIELD_PER_YEAR/MEAT_CURRENT_YIELD_PER_YEAR

constants['inputs']['INCLUDE_PROTEIN'] = True
constants['inputs']['INCLUDE_FAT'] = True
constants['inputs']['FLUCTUATION_LIMIT'] = 1.2 
constants['inputs']['GREENHOUSE_GAIN_PCT'] = 40

constants['inputs']['DAIRY_PRODUCTION'] = 1 #multiplies current dairy productivity (based on stress of animals)
constants['inputs']['GREENHOUSE_FAT_MULTIPLIER'] = 1 # we can grow twice as much fat as greenhouses would have
constants['inputs']['GREENHOUSE_SLOPE_MULTIPLIER'] = 1 #default values from greenhouse paper
constants['inputs']['INDUSTRIAL_FOODS_SLOPE_MULTIPLIER'] = 1 #default values from CS paper
constants["inputs"]["OG_USE_BETTER_ROTATION"] = True

constants['inputs']['IS_NUCLEAR_WINTER'] = True
constants['inputs']['STORED_FOOD_SMOOTHING'] = False
constants['inputs']['MEAT_SMOOTHING'] = False
constants['inputs']['OVERALL_SMOOTHING'] = False


constants['inputs']['ADD_FISH'] = True
constants['inputs']['ADD_SEAWEED'] = True
constants['inputs']['ADD_CELLULOSIC_SUGAR'] = True
constants['inputs']['ADD_METHANE_SCP'] = True
constants['inputs']['ADD_GREENHOUSES'] = True
constants['inputs']['ADD_NONEGG_NONDAIRY_MEAT'] = True
constants['inputs']['ADD_DAIRY'] = True
constants['inputs']['ADD_STORED_FOOD'] = True
constants['inputs']['ADD_OUTDOOR_GROWING'] = True

# only on farm + distribution waste

constants['inputs']['DISTRIBUTION_WASTE'] = {} #%
constants['inputs']['DISTRIBUTION_WASTE']['SEAWEED'] = 0 #%
constants['inputs']['DISTRIBUTION_WASTE']['CEREALS'] = 4.65 #%
constants['inputs']['DISTRIBUTION_WASTE']['CROPS'] = 4.96
constants['inputs']['DISTRIBUTION_WASTE']['SUGAR'] = 0.09 #%
constants['inputs']['DISTRIBUTION_WASTE']['MEAT'] = .80 #%
constants['inputs']['DISTRIBUTION_WASTE']['DAIRY'] = 2.120 #%
constants['inputs']['DISTRIBUTION_WASTE']['SEAFOOD'] = 0.17 #%

 
constants["inputs"]["H_E_FED_MEAT_KCALS"] = 0
constants["inputs"]["H_E_FED_MEAT_FAT"] = 0
constants["inputs"]["H_E_FED_MEAT_PROTEIN"] = 0

# constants["inputs"]["FEED_SOURCES"] = ["SEAWEED","CELLULOSIC_SUGAR","METHANE_SCP","OUTDOOR_GROWING","STORED_FOOD"]


constants['CHECK_CONSTRAINTS'] = False
optimizer = Optimizer()

# [time_months,time_months_middle,analysis]=optimizer.optimize(constants)
# Plotter.plot_people_fed_combined(time_months_middle,analysis)
# Plotter.plot_people_fed_kcals(time_months_middle,analysis)

# we take total food produced given the excess, calculate calories from animals fed maintained, and subtract the human edible and add the resulting meat to the simulation. If the minimum is below, we take the discepancy, use it as an added value to maintained, and run optimizer again. Stop when within 0.1% of the minimum being at 7.8 billion.

# previous_fed = analysis.people_fed_billions
# excess = analysis.people_fed_billions - 7.8
# fraction_to_feed_to_animals = initial_excess/analysis.people_fed_billions
n=0
excess = 0
people_fed_billions = 0

people_fed_arr = []
excess_to_animals_arr = []
# for excess in range(0,6):#billions human edible people excess calories
while(people_fed_billions > 7.81 \
	or people_fed_billions < 7.79):
	excess_to_animals_arr.append(excess)


	excess_per_month = 2100 * 30*7.8e9/1e9/50
	# print("excess_per_month")
	# print(excess_per_month)
	#implies a certain amount of protein actually eaten by the animals as well
	#units of billions of calories monthly
	constants["inputs"]["EXCESS_CALORIES"] = np.array([excess_per_month]*constants['inputs']['NMONTHS'])

	[time_months,time_months_middle,analysis]=optimizer.optimize(constants)
	people_fed_billions = analysis.people_fed_billions
	people_fed_arr.append(people_fed_billions)
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
	Plotter.plot_people_fed_kcals(time_months_middle,analysis)
	quit()
	# if(analysis.people_fed_billions < 7.75):
	# 	excess = excess*.99
	# 	previous_fed = analysis.people_fed_billions*1/.9
	# 	continue
	# 	#went too fast
	# 	print("went too fast")


	# if(analysis.people_fed_billions < 7.79):
	# 	print("less than population, stopping")
		# break
	#below could break if we are short on fat or protein
	# assert(analysis.people_fed_billions <= previous_fed)


	# previous_fed = analysis.people_fed_billions
	# new_excess = analysis.people_fed_billions - 7.8
	# print('new_excess')
	# print(new_excess)
	# excess = new_excess + excess
	# print("excess")
	# print(excess)
	# constants = analysis.get_meat_from_excess(constants,excess) #, human_edible_excess)

	# constants['inputs']['FRACTION_TO_SLAUGHTER']
	print("Human Edible meat as fraction of population")
	# h_e_frac = constants["inputs"]["H_E_FED_MEAT_KCALS"]*1e9/constants["KCALS_MONTHLY"]/analysis.people_fed_billions/1e9
	h_e_meat_people_fed = constants["inputs"]["H_E_FED_MEAT_KCALS"]*1e9/constants["KCALS_MONTHLY"]/1e9

	print("h_e_meat_people_fed/excess")
	# print(h_e_meat_people_fed/excess)
	print("h_e_meat_people_fed")
	print(h_e_meat_people_fed)

	# fraction_to_feed_to_animals = excess/analysis.people_fed_billions
	fraction_to_feed_to_animals = excess/7.8
	
	constants["inputs"]["gshrjdtrm"] = fraction_to_feed_to_animals
	print("fraction_to_feed_to_animals")
	print(fraction_to_feed_to_animals)
	# print("conversion_ratio")
	# print(h_e_frac/fraction_to_feed_to_animals)

	if(n==3):
		quit()
	n = n + 1

	# print("excess")
	# print(excess)


	# constants['inputs']['FRACTION_TO_SLAUGHTER']
	# [time_months,time_months_middle,analysis]=optimizer.optimize(constants)



# calories_fed_to_animals = analysis.get_calories_fed_to_animals(analysis,)

# [time_months,time_months_middle,analysis]=optimizer.estimate_food_ratios(constants)

# if(constants['inputs']['ADD_CELLULOSIC_SUGAR']):
# 	Plotter.plot_CS(time_months_middle,analysis)

# if(constants['inputs']['ADD_FISH']):
# 	Plotter.plot_fish(time_months_middle,analysis)

# if(constants['inputs']['ADD_GREENHOUSES']):
# 	Plotter.plot_GH(time_months_middle,analysis)

# if(constants['inputs']['ADD_OUTDOOR_GROWING']):
# 	Plotter.plot_OG_with_resilient_foods(time_months_middle,analysis)

# if(constants['inputs']['ADD_STORED_FOOD']):
# 	Plotter.plot_stored_food(time_months,analysis)

# if(constants['inputs']['ADD_SEAWEED']):
# 	Plotter.plot_seaweed(time_months_middle,analysis)

if(constants['inputs']['ADD_NONEGG_NONDAIRY_MEAT']):
	Plotter.plot_nonegg_nondairy_meat(time_months_middle,analysis)

if(constants['inputs']['ADD_DAIRY']):
	# Plotter.plot_dairy_cows(time_months_middle,analysis)
	Plotter.plot_dairy(time_months_middle,analysis)

# Plotter.plot_people_fed(time_months_middle,analysis)
Plotter.plot_people_fed_combined(time_months_middle,analysis)
Plotter.plot_people_fed_kcals(time_months_middle,analysis)
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


# constants['inputs']['ADD_SEAWEED'] = True
# constants['inputs']['ADD_CELLULOSIC_SUGAR'] = False
# constants['inputs']['ADD_GREENHOUSES'] = True
# constants['inputs']['ADD_NONEGG_NONDAIRY_MEAT'] = True
# constants['inputs']['ADD_DAIRY'] = True
# constants['inputs']['ADD_STORED_FOOD'] = True
# constants['inputs']['ADD_OUTDOOR_GROWING'] = True
# cell_sugar_omitted=optimizer.optimize(constants)


# constants['inputs']['ADD_SEAWEED'] = True
# constants['inputs']['ADD_CELLULOSIC_SUGAR'] = True
# constants['inputs']['ADD_GREENHOUSES'] = False
# constants['inputs']['ADD_NONEGG_NONDAIRY_MEAT'] = True
# constants['inputs']['ADD_DAIRY'] = True
# constants['inputs']['ADD_STORED_FOOD'] = True
# constants['inputs']['ADD_OUTDOOR_GROWING'] = True
# greenhouses_omitted=optimizer.optimize(constants)


# constants['inputs']['ADD_SEAWEED'] = False
# constants['inputs']['ADD_CELLULOSIC_SUGAR'] = False
# constants['inputs']['ADD_GREENHOUSES'] = False
# constants['inputs']['ADD_NONEGG_NONDAIRY_MEAT'] = True
# constants['inputs']['ADD_DAIRY'] = True
# constants['inputs']['ADD_STORED_FOOD'] = True
# constants['inputs']['ADD_OUTDOOR_GROWING'] = True
# no_intervention=optimizer.optimize(constants)


# constants['inputs']['ADD_SEAWEED'] = True
# constants['inputs']['ADD_CELLULOSIC_SUGAR'] = False
# constants['inputs']['ADD_GREENHOUSES'] = False
# constants['inputs']['ADD_NONEGG_NONDAIRY_MEAT'] = True
# constants['inputs']['ADD_DAIRY'] = True
# constants['inputs']['ADD_STORED_FOOD'] = True
# constants['inputs']['ADD_OUTDOOR_GROWING'] = True
# just_seaweed=optimizer.optimize(constants)


# constants['inputs']['ADD_SEAWEED'] = False
# constants['inputs']['ADD_CELLULOSIC_SUGAR'] = True
# constants['inputs']['ADD_GREENHOUSES'] = False
# constants['inputs']['ADD_NONEGG_NONDAIRY_MEAT'] = True
# constants['inputs']['ADD_DAIRY'] = True
# constants['inputs']['ADD_STORED_FOOD'] = True
# constants['inputs']['ADD_OUTDOOR_GROWING'] = True
# just_cell_sugar=optimizer.optimize(constants)



# constants['inputs']['ADD_SEAWEED'] = False
# constants['inputs']['ADD_CELLULOSIC_SUGAR'] = False
# constants['inputs']['ADD_GREENHOUSES'] = True
# constants['inputs']['ADD_NONEGG_NONDAIRY_MEAT'] = True
# constants['inputs']['ADD_DAIRY'] = True
# constants['inputs']['ADD_STORED_FOOD'] = True
# constants['inputs']['ADD_OUTDOOR_GROWING'] = True
# just_greenhouses=optimizer.optimize(constants)
