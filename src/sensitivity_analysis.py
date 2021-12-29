# this program runs the optimizer model, and ensures that all the results are 
# reasonable using a couple useful checks to make sure there's nothing wacky 
# going on.

#check that as time increases, more people can be fed

import os
import sys
module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
	sys.path.append(module_path)

import numpy as np
import itertools
import random
from src.optimizer import Optimizer
import matplotlib.pyplot as plt
from scipy import stats
from matplotlib.ticker import MaxNLocator
from datetime import datetime

c = {}
c['inputs'] = {}

c['inputs']['NMONTHS'] = 84
c['inputs']['LIMIT_SEAWEED_AS_PERCENT_KCALS'] = True

c['inputs']['NUTRITION'] = {\
	'FAT_DAILY':47,'KCALS_DAILY':2100,'PROTEIN_DAILY':51}

c['inputs']['MAX_SEAWEED_AS_PERCENT_KCALS'] = 10
c['inputs']['NEW_AREA_PER_DAY'] = 4.153 # 1000 km^2 (seaweed)
c['inputs']['SEAWEED_PRODUCTION_RATE'] = 10 # percent (seaweed)

# "Outputs" https://docs.google.com/spreadsheets/d/19kzHpux690JTCo2IX2UA1faAd7R1QcBK/edit#gid=1815939673 cell G12-G14
c['inputs']['TONS_DRY_CALORIC_EQIVALENT_SF'] = 1360e6
c["inputs"]["OG_USE_BETTER_ROTATION"] = True
c['inputs']['INCLUDE_PROTEIN'] = True
c['inputs']['INCLUDE_FAT'] = True
c['inputs']['WASTE'] = {}
# c['inputs']['WASTE']['CEREALS'] = 19.02 #%
c['inputs']['WASTE']['SUGAR'] = 14.47 #%
c['inputs']['WASTE']['MEAT'] = 15.17 #%
c['inputs']['WASTE']['DAIRY'] = 16.49 #%
c['inputs']['WASTE']['SEAFOOD'] = 14.55 #%
c['inputs']['WASTE']['CROPS'] = 19.33 #%
c['inputs']['WASTE']['SEAWEED'] = 14.37 #%
c["inputs"]["CULL_DURATION"] = 0#analysis.c["CULL_DURATION"]
c['inputs']['RECALCULATE_CULL_DURATION'] = False #thousand tons

c['inputs']['IS_NUCLEAR_WINTER'] = True
excess_per_month = np.array([0]*c['inputs']['NMONTHS'])
c["inputs"]["EXCESS_CALORIES"] = excess_per_month



optimizer = Optimizer()

c['inputs']['ADD_FISH'] = True
c['inputs']['ADD_SEAWEED'] = True
c['inputs']['ADD_CELLULOSIC_SUGAR'] = True
c['inputs']['ADD_METHANE_SCP'] = True
c['inputs']['ADD_GREENHOUSES'] = True
c['inputs']['ADD_DAIRY'] = True
c['inputs']['ADD_STORED_FOOD'] = True
c['inputs']['ADD_MEAT'] = True
c['inputs']['ADD_OUTDOOR_GROWING'] = True
c['inputs']['INITIAL_HARVEST_DURATION'] = 7+1 # months
c['inputs']['STORED_FOOD_SMOOTHING'] = False
c['inputs']['KCAL_SMOOTHING'] = False
c['inputs']['MEAT_SMOOTHING'] = False


# 

c['CHECK_CONSTRAINTS'] = False
nsamples = 100
# all_fed = stats.norm.rvs(size=nsamples)
def monte_carlo():

	variables = {}

	variables['MAX_SEAWEED_AS_PERCENT_KCALS'] = [5,10,30]
	variables['SEAWEED_PRODUCTION_RATE'] = [5,10,15]
	variables['SEAWEED_NEW_AREA'] = [4.153/2,4.153,4.153*2]
	variables['GREENHOUSE_GAIN_PCT'] = [40/2,40,40*2]
	variables['GREENHOUSE_AREA_MULTIPLIER'] = [1/4,1/2,1]
	variables['INDUSTRIAL_FOODS_SLOPE_MULTIPLIER'] = [0.6,1,1.4]
	variables["DELAY"] = [\
		{\
			"SEAWEED" : 2,
			'INDUSTRIAL_FOODS' : 6,
			'GREENHOUSE' : 4,
			'FEED_SHUTOFF' : 4,
			'BIOFUEL_SHUTOFF' : 2,
			'ROTATION_CHANGE' : 4
		},
		{\
			"SEAWEED" : 1,
			'INDUSTRIAL_FOODS' : 3,
			'GREENHOUSE' : 2,
			'FEED_SHUTOFF' : 2,
			'BIOFUEL_SHUTOFF' : 1,
			'ROTATION_CHANGE' : 2
		},
		{\
			"SEAWEED" : 0,
			'INDUSTRIAL_FOODS' : 1,
			'GREENHOUSE' : 1,
			'FEED_SHUTOFF' : 1,
			'BIOFUEL_SHUTOFF' : 0,
			'ROTATION_CHANGE' : 1
		}
	]

	variables["ROTATION_IMPROVEMENTS"] = \
	[\
		{
			"KCALS_REDUCTION" : .822,
			"FAT_RATIO" : 1.746,
			"PROTEIN_RATIO" : 1.063
		},
		{
			"KCALS_REDUCTION" : .808,
			"FAT_RATIO" : 1.861,
			"PROTEIN_RATIO" : 1.062
		},
		{
			"KCALS_REDUCTION" : .799,
			"FAT_RATIO" : 1.928,
			"PROTEIN_RATIO" : 1.067
		}
	]
	nsamples=1000
	
	#worst plausibly likely variables all in one case
	sample_c = c
	# print(sample_c)
	# print(sample_c["inputs"])
	for i in variables.items():
		sample_c["inputs"][i[0]] = i[1][0]
	print("")
	print("worst case: ")
	tstart = datetime.now()
	[time_months,time_months_middle,analysis]=optimizer.optimize(sample_c)
	tend = datetime.now()
	diff = tend-tstart
	print("seconds worst case")
	print(diff.seconds)
	print("microseconds worst case")
	print(diff.microseconds)

	#best plausibly likely variables all in one case
	for i in variables.items():
		sample_c["inputs"][i[0]] = i[1][-1]
	print("")
	print("best case: ")
	tstart = datetime.now()
	[time_months,time_months_middle,analysis]=optimizer.optimize(sample_c)
	tend = datetime.now()
	diff = tend-tstart
	print("seconds best case")
	print(diff.seconds)
	print("microseconds best case")
	print(diff.microseconds)

	input("Press enter to continue")
	all_vars = list(variables.values())
	all_keys = [list(variables.keys())]*nsamples
	all_combos=list(itertools.product(*all_vars))
	random_sample=random.sample(all_combos,nsamples)
	# print(random_sample[0])
	# print(all_keys[0])
	# quit()
	sample_c = c

	all_fed = []
	for i in range(0,len(random_sample)):

		# print(c)
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
			
			sample_c['inputs'][key] = value

		[time_months,time_months_middle,analysis]=optimizer.optimize(sample_c)
		all_fed.append(analysis.people_fed_billions)

	# https://stackoverflow.com/questions/61940618/how-do-i-draw-a-histogram-for-a-normal-distribution-using-python-matplotlib
	# plt.scatter(all_fed,all_fed)
	# https://stackoverflow.com/questions/12050393/how-to-force-the-y-axis-to-only-use-integers-in-matplotlib	

	num_bins = int(nsamples/5)
	plt.hist(all_fed, bins=num_bins, facecolor='blue', alpha=0.5)
	# y = np.linspace(-4, 4, nsamples)
	bin_width = (max(all_fed) - min(all_fed)) / num_bins
	# plt.plot(y, stats.norm.pdf(y) * nsamples * bin_width)
	plt.title("Food Available After Delayed Shutoff and Waste ")
	plt.xlabel("Maximum people fed, billions")
	plt.ylabel("Number of Scenarios")
	ax = plt.gca()
	ax.yaxis.set_major_locator(MaxNLocator(integer=True))
	plt.show()
		# quit()

monte_carlo()

