# this program runs the optimizer model, and ensures that all the results are 
# reasonable using a couple useful checks to make sure there's nothing wacky 
# going on.

#check that as time increases, more people can be fed

import os
import sys
module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
	sys.path.append(module_path)

import itertools
import random
from src.optimizer import Optimizer
import matplotlib.pyplot as plt

constants = {}
constants['inputs'] = {}

constants['inputs']['NMONTHS'] = 84
constants['inputs']['LIMIT_SEAWEED_AS_PERCENT_KCALS'] = True

constants['inputs']['NUTRITION'] = {\
	'FAT_DAILY':47,'KCALS_DAILY':2100,'PROTEIN_DAILY':51}

constants['inputs']['MAX_SEAWEED_AS_PERCENT_KCALS'] = 30
constants['inputs']['NEW_AREA_PER_DAY'] = 4.153 # 1000 km^2 (seaweed)
constants['inputs']['SEAWEED_PRODUCTION_RATE'] = 10 # percent (seaweed)

# "Outputs" https://docs.google.com/spreadsheets/d/19kzHpux690JTCo2IX2UA1faAd7R1QcBK/edit#gid=1815939673 cell G12-G14
constants['inputs']['TONS_DRY_CALORIC_EQIVALENT_SF'] = 1360e6
constants['inputs']['INITIAL_SF_PROTEIN'] = 166071 #1000 tons protein per unit mass initial
constants['inputs']['INITIAL_SF_FAT'] = 69254 # 1000 tons fat per unit mass 

constants["inputs"]["OG_USE_BETTER_ROTATION"] = False


optimizer = Optimizer()


constants['inputs']['ADD_FISH'] = True
constants['inputs']['ADD_SEAWEED'] = True
constants['inputs']['ADD_CELLULOSIC_SUGAR'] = True
constants['inputs']['ADD_GREENHOUSES'] = True
constants['inputs']['ADD_NONEGG_NONDAIRY_MEAT'] = True
constants['inputs']['ADD_DAIRY'] = True
constants['inputs']['ADD_STORED_FOOD'] = True
constants['inputs']['ADD_OUTDOOR_GROWING'] = True
constants['inputs']['GREENHOUSE_FAT_MULTIPLIER'] = 1.5
# 

constants['CHECK_CONSTRAINTS'] = False
def monte_carlo():

	variables = {}

	variables['NMONTHS'] = [12,24,36]
	variables['ASSUMED_WASTE'] = [40,35,25,15]

	variables['NUTRITION'] = [{'FAT_DAILY':35,'KCALS_DAILY':2100,'PROTEIN_DAILY':51}]

	variables['RATIO_KCALS_POSTDISASTER_Y1'] = [{'Y1':0.4,'Y2':0.2,'Y3':0.2,'Y4':0.2},
		{'Y1':0.35,'Y2':0.1,'Y3':0.1,'Y4':0.1},
		{'Y1':0.45,'Y2':0.3,'Y3':0.3,'Y4':0.3}]

	variables['GREENHOUSE_FAT_MULTIPLIER'] = [1,1.5,2,3]
	variables['DAIRY_PRODUCTION'] = [0.5,1]
	variables['MAX_SEAWEED_AS_PERCENT_KCALS'] = [5,10,20,30]
	variables['SEAWEED_PRODUCTION_RATE'] = [5,10,15,20]
	variables['SEAWEED_NEW_AREA'] = [1,4.153,6]
	variables['GREENHOUSE_SLOPE_MULTIPLIER'] = [0.1,0.5,1,2,3]
	variables['CELLULOSIC_SUGAR_SLOPE_MULTIPLIER'] = [0.1,0.5,1,2,3]
	variables['OUTDOOR_GROWING_FAT_MULTIPLIER'] = [1,1.5,2,3]


	# variables['NMONTHS'] = [12]
	# variables['ASSUMED_WASTE'] = [15]

	# variables['NUTRITION'] = [{'FAT_DAILY':35,'KCALS_DAILY':2100,'PROTEIN_DAILY':51}]

	# variables['RATIO_KCALS_POSTDISASTER_Y1'] = [{'Y1':0.4,'Y2':0.2,'Y3':0.2,'Y4':0.2}]

	# variables['GREENHOUSE_FAT_MULTIPLIER'] = [3]
	# variables['DAIRY_PRODUCTION'] = [1]
	# variables['MAX_SEAWEED_AS_PERCENT_KCALS'] = [30]
	# variables['SEAWEED_PRODUCTION_RATE'] = [20]
	# variables['SEAWEED_NEW_AREA'] = [6]
	# variables['GREENHOUSE_SLOPE_MULTIPLIER'] = [3]
	# variables['CELLULOSIC_SUGAR_SLOPE_MULTIPLIER'] = [3]
	# variables['OUTDOOR_GROWING_FAT_MULTIPLIER'] = [3]


	nsamples=1000
	
	all_vars = list(variables.values())
	all_keys = [list(variables.keys())]*nsamples
	all_combos=list(itertools.product(*all_vars))

	random_sample=random.sample(all_combos,nsamples)
	# print(random_sample[0])
	# print(all_keys[0])
	# quit()
	sample_constants = constants

	all_fed = []
	for i in range(0,len(random_sample)):

		# print(constants)
		s = random_sample[i]
		# print(s)
		# print(all_keys)
		# quit()
		keylist=all_keys[i]
		for j in range(0,len(keylist)):
			# print(len(s))
			# print(len(all_keys[j]))
			# quit()
			key = keylist[j]
			value=s[j]
			
			sample_constants['inputs'][key] = value

		# print(sample_constants)
		[time_months,time_months_middle,analysis]=optimizer.optimize(sample_constants)
		all_fed.append(analysis.people_fed_billions)
		
		# quit()
	print(all_fed)
	plt.scatter(all_fed,all_fed)
	plt.show()
monte_carlo()