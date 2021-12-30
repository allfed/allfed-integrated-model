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
c['inputs']['NUTRITION']['FAT_DAILY'] = 61.7#47#35 #grams per person per day
c['inputs']['NUTRITION']['PROTEIN_DAILY'] = 59.5#51#46 #grams per person per day

c['inputs']['MAX_SEAWEED_AS_PERCENT_KCALS'] = 0
c['inputs']['NEW_AREA_PER_DAY'] = 0 
c['inputs']['SEAWEED_PRODUCTION_RATE'] = 0 

# "Outputs" https://docs.google.com/spreadsheets/d/19kzHpux690JTCo2IX2UA1faAd7R1QcBK/edit#gid=1815939673 cell G12-G14
c['inputs']['TONS_DRY_CALORIC_EQIVALENT_SF'] = 0.96*351.433*1e6
#these fat and protein values do not produce realistic outputs, so outdoor growing ratios were used instead
# c['inputs']['INITIAL_SF_FAT'] = 166.07e3*351e6/1360e6
# c['inputs']['INITIAL_SF_PROTEIN'] = 69.25e3*351e6/1360e6

c["inputs"]["OG_USE_BETTER_ROTATION"] = False
	
c['inputs']['INCLUDE_PROTEIN'] = True
c['inputs']['INCLUDE_FAT'] = True


c['inputs']['INITIAL_HARVEST_DURATION'] = 7 # (no difference between harvests!)

c['inputs']['FLUCTUATION_LIMIT'] = 1.5 # not used unless smoothing true
c['inputs']['IS_NUCLEAR_WINTER'] = False
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

# c['inputs']['ADD_CELLULOSIC_SUGAR'] = False
# c['inputs']['ADD_DAIRY'] = True
# c['inputs']['ADD_FISH'] = True
# c['inputs']['ADD_GREENHOUSES'] = False
# c['inputs']['ADD_OUTDOOR_GROWING'] = True
# c['inputs']['ADD_MEAT'] = True
# c['inputs']['ADD_METHANE_SCP'] = False
# c['inputs']['ADD_SEAWEED'] = False
# c['inputs']['ADD_STORED_FOOD'] = True


c["inputs"]["EXCESS_CALORIES"] = np.array([0]*c['inputs']['NMONTHS'])
c['inputs']["DELAY"] = {}
c['inputs']["DELAY"]['FEED_SHUTOFF'] = 0 # months
c['inputs']["DELAY"]['BIOFUEL_SHUTOFF'] = 0 # months

c["inputs"]["CULL_DURATION"] = np.nan #not used unless nuclear winter
c['inputs']['RECALCULATE_CULL_DURATION'] = False #thousand tons

c['inputs']['WASTE'] = {}
# c['inputs']['WASTE']['CEREALS'] = 0 #%
c['inputs']['WASTE']['SUGAR'] = 0 #%
c['inputs']['WASTE']['MEAT'] = 0 #%
c['inputs']['WASTE']['DAIRY'] = 0 #%
c['inputs']['WASTE']['SEAFOOD'] = 0 #%
c['inputs']['WASTE']['CROPS'] = 0 #%
c['inputs']['WASTE']['SEAWEED'] = 0 #%

print(c['inputs']['ADD_FISH'])
optimizer = Optimizer()
[time_months,time_months_middle,analysis]=optimizer.optimize(c)

if(c['inputs']['ADD_OUTDOOR_GROWING']):
	Plotter.plot_OG_before_nuclear_event(time_months_middle,analysis)

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
	'Primary production before waste, baseline')
# quit()
	
# nuclear winter 150 tab, cell G30-G38  https://docs.google.com/spreadsheets/d/14t3_PUIky6aNiBvw8q24sj6QYxCN9s_VddLY2-eJuPE/edit#gid=1637082097
#overall waste, on farm+distribution+retail
#1x prices (note, currently set to 2019, not 2020)
c['inputs']['WASTE'] = {}
c['inputs']['WASTE']['CEREALS'] = 28.52 #%
c['inputs']['WASTE']['SUGAR'] = 23.96 #%
c['inputs']['WASTE']['MEAT'] = 24.67 #%
c['inputs']['WASTE']['DAIRY'] = 25.99 #%
c['inputs']['WASTE']['SEAFOOD'] = 24.04 #%
c['inputs']['WASTE']['CROPS'] = 28.83 #%
c['inputs']['WASTE']['SEAWEED'] = 23.87 #%

c["inputs"]["EXCESS_CALORIES"] = np.array([0]*c['inputs']['NMONTHS'])
c['inputs']["DELAY"]['FEED_SHUTOFF'] = c['inputs']['NMONTHS']
c['inputs']["DELAY"]['BIOFUEL_SHUTOFF'] = c['inputs']['NMONTHS']

c["inputs"]["CULL_DURATION"] = 0 # there is no culling
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
	Plotter.plot_OG_before_nuclear_event(time_months_middle,analysis)

Plotter.plot_people_fed_combined(time_months_middle,analysis)
Plotter.plot_people_fed_kcals(time_months_middle,analysis,"Baseline around 2020 average diet")