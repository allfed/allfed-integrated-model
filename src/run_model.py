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
c = {}
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

c["inputs"]["OG_USE_BETTER_ROTATION"] = True

c['inputs']['INCLUDE_PROTEIN'] = True
c['inputs']['INCLUDE_FAT'] = True

c['inputs']['GREENHOUSE_GAIN_PCT'] = 40

c['inputs']['GREENHOUSE_SLOPE_MULTIPLIER'] = 1 #default values from greenhouse paper
c['inputs']['INDUSTRIAL_FOODS_SLOPE_MULTIPLIER'] = 1 #default values from CS paper

c['inputs']['INITIAL_HARVEST_DURATION'] = 7 # months

c['inputs']['IS_NUCLEAR_WINTER'] = True
c['inputs']['FLUCTUATION_LIMIT'] = 2
c['inputs']['KCAL_SMOOTHING'] = False
c['inputs']['MEAT_SMOOTHING'] = False
c['inputs']['STORED_FOOD_SMOOTHING'] = False

c['inputs']['ADD_CELLULOSIC_SUGAR'] = True
c['inputs']['ADD_DAIRY'] = True
c['inputs']['ADD_FISH'] = True
c['inputs']['ADD_GREENHOUSES'] = True
c['inputs']['ADD_OUTDOOR_GROWING'] = True
c['inputs']['ADD_MEAT'] = True
c['inputs']['ADD_METHANE_SCP'] = True
c['inputs']['ADD_SEAWEED'] = True
c['inputs']['ADD_STORED_FOOD'] = True

c["inputs"]["EXCESS_CALORIES"] = np.array([0]*c['inputs']['NMONTHS'])
c['inputs']['FEED_SHUTOFF_DELAY'] = 0 # months
c['inputs']['BIOFUEL_SHUTOFF_DELAY'] = 0 # months
 
c["inputs"]["CULL_DURATION"] = np.nan # will be recalculated
c['inputs']['RECALCULATE_CULL_DURATION'] = True #thousand tons

c['inputs']['WASTE'] = {}
# c['inputs']['WASTE']['CEREALS'] = 0 #%
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
	'Primary production before waste, + resilient foods')
# nuclear winter 150 tab, cell G30-G38  https://docs.google.com/spreadsheets/d/14t3_PUIky6aNiBvw8q24sj6QYxCN9s_VddLY2-eJuPE/edit#gid=1637082097
#overall waste, on farm+distribution+retail
#3x prices (note, currently set to 2019, not 2020)
c['inputs']['WASTE'] = {}
# c['inputs']['WASTE']['CEREALS'] = 19.02 #%
c['inputs']['WASTE']['SUGAR'] = 14.47 #%
c['inputs']['WASTE']['MEAT'] = 15.17 #%
c['inputs']['WASTE']['DAIRY'] = 16.49 #%
c['inputs']['WASTE']['SEAFOOD'] = 14.55 #%
c['inputs']['WASTE']['CROPS'] = 19.33 #%
c['inputs']['WASTE']['SEAWEED'] = 14.37 #%



excess_per_month = np.array([0]*c['inputs']['NMONTHS'])
c["inputs"]["EXCESS_CALORIES"] = excess_per_month
c['inputs']['FEED_SHUTOFF_DELAY'] = 2 # months
c['inputs']['BIOFUEL_SHUTOFF_DELAY'] = 1 # months
 
c["inputs"]["CULL_DURATION"] = analysis.c["CULL_DURATION"]
c['inputs']['RECALCULATE_CULL_DURATION'] = False #thousand tons

optimizer = Optimizer()
[time_months,time_months_middle,analysis]=optimizer.optimize(c)
Plotter.plot_people_fed_combined(time_months_middle,analysis)
Plotter.plot_people_fed_kcals(time_months_middle,analysis,"Food available after waste, feed ramp down and biofuel ramp down, + resilient foods")

print("")
print("")
print("")
print("")
print("")
print("")
print("==========Running diet balancer=========")
print("")
print("")
print("")

#billions of kcals	
# "Sources/summary" tab cell I14.  https://docs.google.com/spreadsheets/d/1tLFHJpXTStxyfNojP_Wrj0MQowfyKujJUA37ZG1q6pk/edit#gid=0

c['inputs']['INCLUDE_PROTEIN'] = False
c['inputs']['INCLUDE_FAT'] = False


[time_months,time_months_middle,analysis]=optimizer.optimize(c)
Plotter.plot_people_fed_combined(time_months_middle,analysis)

kcals_fed = np.min(analysis.kcals_fed)
print("")
print("")
print("")
print("")
print("billions of people fed from kcals")
print(kcals_fed)
print("")
print("")
print("")
print("")

feed_delay = c['inputs']['FEED_SHUTOFF_DELAY']

#these months are used to estimate the diet before the full scale-up of resilient foods makes there be way too much food to make sense economically
N_MONTHS_TO_CALCULATE_DIET = 48

#don't try to feed more animals in the  months before feed shutoff
excess_per_month[feed_delay:N_MONTHS_TO_CALCULATE_DIET] = \
	excess_per_month[feed_delay:N_MONTHS_TO_CALCULATE_DIET]\
	+ analysis.excess_after_run[feed_delay:N_MONTHS_TO_CALCULATE_DIET]


#=================

n=0
# kcals_fed = 0
while(True):
	import matplotlib.pyplot as plt
	# plt.plot(excess_per_month*1e9/4e6/1e6)
	# plt.show()
	# Plotter.plot_people_fed_combined(time_months_middle,analysis)
	# Plotter.plot_people_fed_kcals(time_months_middle,analysis,"dumb stuff")
	
	# import matplotlib.pyplot as plt
	# # print("excess_per_month")
	# # print(excess_per_month)
	# plt.plot(excess_per_month)
	# plt.show()

	#billions of kcals	
	c['inputs']['FEED_SHUTOFF_DELAY'] = 2 # months
	c['inputs']['BIOFUEL_SHUTOFF_DELAY'] = 1 # months
	# "Sources/summary" tab cell I14.  https://docs.google.com/spreadsheets/d/1tLFHJpXTStxyfNojP_Wrj0MQowfyKujJUA37ZG1q6pk/edit#gid=0

	c["inputs"]["CULL_DURATION"] = analysis.c["CULL_DURATION"]
	c['inputs']['RECALCULATE_CULL_DURATION'] = False #thousand tons

	[time_months,time_months_middle,analysis]=optimizer.optimize(c)
	
	print("")
	print("")
	print("")
	print("")
	print("kcals_fed")
	print(np.min(analysis.kcals_fed))
	print("")
	print("")
	print("")
	print("")

	# the rebalancer is only responsible for balancing calories, and is unable to operate unless the assumption that fat and protein are limiting values is invalid.
	c['inputs']['INCLUDE_PROTEIN'] = False
	c['inputs']['INCLUDE_FAT'] = False

	kcals_fed = np.min(analysis.kcals_fed)
	
	feed_delay = c['inputs']['FEED_SHUTOFF_DELAY']
	
	if(kcals_fed > 7.79 and kcals_fed < 7.81):
		break

	#don't try to feed more animals in the  months before feed shutoff
	excess_per_month[feed_delay:N_MONTHS_TO_CALCULATE_DIET] = \
		excess_per_month[feed_delay:N_MONTHS_TO_CALCULATE_DIET]\
		+ analysis.excess_after_run[feed_delay:N_MONTHS_TO_CALCULATE_DIET]

	# excess_per_month = excess_per_month+ analysis.excess_after_run
	
	# if(n>30):
	# 	break
	n = n + 1

	# if(n==3):
	# 	c['CHECK_CONSTRAINTS'] = True
plt.title("Excess kcals used for feed and biofuel")
plt.ylabel("million dry caloric tons monthly")
plt.xlabel("Months after May nuclear event")
plt.plot(np.array(optimizer.s["excess_kcals"])*1e9/4e6/1e6)
plt.show()
# only on farm + distribution waste
# (on farm waste is implicit in production numbers)
# c['inputs']['DISTRIBUTION_WASTE'] = {} #%
# c['inputs']['DISTRIBUTION_WASTE']['SEAWEED'] = 0 #%
# c['inputs']['DISTRIBUTION_WASTE']['CEREALS'] = 4.65 #%
# c['inputs']['DISTRIBUTION_WASTE']['CROPS'] = 4.96
# c['inputs']['DISTRIBUTION_WASTE']['SUGAR'] = 0.09 #%
# c['inputs']['DISTRIBUTION_WASTE']['MEAT'] = .80 #%
# c['inputs']['DISTRIBUTION_WASTE']['DAIRY'] = 2.120 #%
# c['inputs']['DISTRIBUTION_WASTE']['SEAFOOD'] = 0.17 #%

# calories_fed_to_animals = analysis.get_calories_fed_to_animals(analysis,)

# [time_months,time_months_middle,analysis]=optimizer.estimate_food_ratios(c)

# if(c['inputs']['ADD_CELLULOSIC_SUGAR']):
# 	Plotter.plot_CS(time_months_middle,analysis)

# if(c['inputs']['ADD_FISH']):
# 	Plotter.plot_fish(time_months_middle,analysis)

# if(c['inputs']['ADD_GREENHOUSES']):
# 	Plotter.plot_GH(time_months_middle,analysis)

# if(c['inputs']['ADD_OUTDOOR_GROWING']):
# 	Plotter.plot_OG_with_resilient_foods(time_months_middle,analysis)

# if(c['inputs']['ADD_STORED_FOOD']):
# 	Plotter.plot_stored_food(time_months,analysis)

# if(c['inputs']['ADD_SEAWEED']):
# 	Plotter.plot_seaweed(time_months_middle,analysis)

if(c['inputs']['ADD_MEAT']):
	Plotter.plot_meat(time_months_middle,analysis)

if(c['inputs']['ADD_DAIRY']):
	# Plotter.plot_dairy_cows(time_months_middle,analysis)
	Plotter.plot_dairy(time_months_middle,analysis)

# plt.plot(excess_per_month/2100/30)
# plt.show()
# Plotter.plot_people_fed(time_months_middle,analysis)
Plotter.plot_people_fed_combined(time_months_middle,analysis)
Plotter.plot_people_fed_kcals(time_months_middle,analysis,"Average diet, excess production used for feed, + resilient foods")
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


# c['inputs']['ADD_SEAWEED'] = True
# c['inputs']['ADD_CELLULOSIC_SUGAR'] = False
# c['inputs']['ADD_GREENHOUSES'] = True
# c['inputs']['ADD_MEAT'] = True
# c['inputs']['ADD_DAIRY'] = True
# c['inputs']['ADD_STORED_FOOD'] = True
# c['inputs']['ADD_OUTDOOR_GROWING'] = True
# cell_sugar_omitted=optimizer.optimize(c)


# c['inputs']['ADD_SEAWEED'] = True
# c['inputs']['ADD_CELLULOSIC_SUGAR'] = True
# c['inputs']['ADD_GREENHOUSES'] = False
# c['inputs']['ADD_MEAT'] = True
# c['inputs']['ADD_DAIRY'] = True
# c['inputs']['ADD_STORED_FOOD'] = True
# c['inputs']['ADD_OUTDOOR_GROWING'] = True
# greenhouses_omitted=optimizer.optimize(c)


# c['inputs']['ADD_SEAWEED'] = False
# c['inputs']['ADD_CELLULOSIC_SUGAR'] = False
# c['inputs']['ADD_GREENHOUSES'] = False
# c['inputs']['ADD_MEAT'] = True
# c['inputs']['ADD_DAIRY'] = True
# c['inputs']['ADD_STORED_FOOD'] = True
# c['inputs']['ADD_OUTDOOR_GROWING'] = True
# no_intervention=optimizer.optimize(c)


# c['inputs']['ADD_SEAWEED'] = True
# c['inputs']['ADD_CELLULOSIC_SUGAR'] = False
# c['inputs']['ADD_GREENHOUSES'] = False
# c['inputs']['ADD_MEAT'] = True
# c['inputs']['ADD_DAIRY'] = True
# c['inputs']['ADD_STORED_FOOD'] = True
# c['inputs']['ADD_OUTDOOR_GROWING'] = True
# just_seaweed=optimizer.optimize(c)


# c['inputs']['ADD_SEAWEED'] = False
# c['inputs']['ADD_CELLULOSIC_SUGAR'] = True
# c['inputs']['ADD_GREENHOUSES'] = False
# c['inputs']['ADD_MEAT'] = True
# c['inputs']['ADD_DAIRY'] = True
# c['inputs']['ADD_STORED_FOOD'] = True
# c['inputs']['ADD_OUTDOOR_GROWING'] = True
# just_cell_sugar=optimizer.optimize(c)



# c['inputs']['ADD_SEAWEED'] = False
# c['inputs']['ADD_CELLULOSIC_SUGAR'] = False
# c['inputs']['ADD_GREENHOUSES'] = True
# c['inputs']['ADD_MEAT'] = True
# c['inputs']['ADD_DAIRY'] = True
# c['inputs']['ADD_STORED_FOOD'] = True
# c['inputs']['ADD_OUTDOOR_GROWING'] = True
# just_greenhouses=optimizer.optimize(c)
