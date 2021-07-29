'''

A set of utility functions useful for plotting 

'''
import os
import sys
module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
	sys.path.append(module_path)

import matplotlib.pyplot as plt
import numpy as np

class Plotter:
	def __init__(self):
		pass

	def plot_stored_food(time_months,analysis):

		plt.plot(time_months,np.array(analysis.billion_person_years_SF_kcals))
		plt.plot(time_months,np.array(analysis.billion_person_years_SF_fat))
		plt.plot(time_months,np.array(analysis.billion_person_years_SF_protein))
		plt.title('Stored Food')
		plt.xlabel('Months Since May Nuclear Event')
		plt.ylabel('Billion Person-Years')
		plt.legend(['Limit by kcals','Limited by Fat','Limited by protein'])
		plt.show()

	def plot_people_fed(time_months_middle,analysis):
		legend=[]
		if(analysis.constants['ADD_STORED_FOOD']):
			plt.plot(time_months_middle,analysis.billions_fed_SF_kcals)
			plt.plot(time_months_middle,analysis.billions_fed_SF_fat)
			plt.plot(time_months_middle,analysis.billions_fed_SF_protein)
			legend = legend + ['Stored Food, Limit by kcals','Stored Food, Limited by Fat','Stored Food, Limited by protein']
		if(analysis.constants['ADD_SEAWEED']):
			plt.plot(time_months_middle,analysis.billions_fed_seaweed_kcals)
			plt.plot(time_months_middle,analysis.billions_fed_seaweed_fat)
			plt.plot(time_months_middle,analysis.billions_fed_seaweed_protein)
			legend = legend + ['Seaweed, Limit by kcals','Seaweed, Limited by Fat','Seaweed, Limited by protein']
		plt.title('People fed')
		plt.ylabel('billions of people')
		plt.xlabel('Months Since May Nuclear Event')
		plt.legend(legend)
		plt.show()

	#plot comparison between Aron's Data and this model's data
	def plot_seaweed_comparison(time_days_daily,time_days_monthly,analysis):
		#aron's food produced data for each day
		food_spreadsheet=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,102562183,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1878422073,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2225588498,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2572754922,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2919921347]

		#aron's wet on farm data for each day
		wet_on_farm_spreadsheet=[1000,1100,1210,1331,1464,1611,1772,1949,2144,2358,2594,2853,3138,3452,3797,4177,4595,5054,5560,6116,6727,7400,8140,8954,9850,10835,11918,13110,14421,15863,17449,19194,21114,23225,25548,28102,30913,34004,37404,41145,45259,49785,54764,60240,66264,72890,80180,88197,97017,106719,117391,129130,142043,156247,171872,189059,207965,228762,251638,276801,304482,334930,368423,405265,445792,490371,539408,593349,652683,717952,789747,868722,955594,1051153,1156269,1271895,1399085,1538993,1692893,1862182,2048400,2253240,2478564,2726421,2999063,3298969,3628866,3991753,3792289,4171517,4588669,5047536,5552290,6107519,6718271,7390098,8129107,8942018,9836220,10819842,11901826,13092009,14401210,15841331,17425464,19168010,21084811,23193292,25512621,28063884,30870272,33957299,37353029,35493925,39043318,42947650,47242415,51966656,57163322,62879654,69167619,76084381,83692820,92062102,101268312,111395143,122534657,134788123,148266935,163093629,179402992,197343291,217077620,238785382,262663920,288930312,317823343,349605677,229643215,252607536,277868290,305655119,336220630,369842693,406826963,447509659,492260625,541486687,595635356,655198892,720718781,792790659,872069725,959276697,1055204367,1160724804,1276797284,1404477013,1544924714,1699417185,1869358904,2056294794,2261924274,271172782,298290061,328119067,360930973,397024071,436726478,480399126,528439038,581282942,639411236,703352360,773687596,851056355,936161991,1029778190,1132756009,1246031610,1370634771,1507698248,1658468072,1824314880,2006746368,2207421004,2428163105,2670979415,312702350,343972585,378369844,416206828,457827511,503610262,553971288,609368417,670305259,737335785,811069363,892176299,981393929,1079533322,1187486655,1306235320,1436858852,1580544737,1738599211,1912459132,2103705045,2314075550,2545483105,2800031415,3080034557,354231918,389655110,428620621,471482683,518630951,570494046,627543451,690297796,759327576,835260333,918786367,1010665003,1111731504,1222904654,1345195119,1479714631,1627686094,1790454704,1969500174,2166450192,2383095211,2621404732,2883545205,3171899726,3489089698,395761486]


		WORLD_POP=7.9e9#population

		spreadsheet_days=np.linspace(0,len(wet_on_farm_spreadsheet),len(wet_on_farm_spreadsheet))
		
		max_seaweed=np.linspace(analysis.max_seaweed,
			analysis.max_seaweed,
			len(wet_on_farm_spreadsheet))

		plt.plot(spreadsheet_days,max_seaweed)
		plt.plot(time_days_daily,analysis.seaweed_built_area_max_density)
		plt.plot(time_days_daily,analysis.seaweed_used_area_max_density)
		plt.plot(spreadsheet_days,np.array(wet_on_farm_spreadsheet)/1000)
		plt.plot(time_days_daily,analysis.seaweed_wet_on_farm)
		plt.legend([
			'Max Density times Max Area Seaweed',
			'Built Area times Max Density',
			'Used Area times Max Density',
			'Aron\'s Spreadsheet Wet on Farm Estimate',
			'Optimizer Estimate Wet On Farm'
			])
		plt.title('Seaweed Wet, 1000s of tons')
		plt.yscale('log')
		plt.show()
		quit()
		max_line=np.linspace(4e6*SEAWEED_KCALS/KCALS_MONTHLY,4e6*SEAWEED_KCALS/KCALS_MONTHLY,len(wet_on_farm_spreadsheet))

		plt.plot(spreadsheet_days,max_line)
		plt.plot(spreadsheet_days,world_kcals_month/KCALS_MONTHLY)
		plt.plot(spreadsheet_days,np.array(food_spreadsheet).cumsum()/1000*SEAWEED_KCALS/KCALS_MONTHLY)
		plt.plot(time_days_daily,np.array(seaweed_food_produced_vals_daily	).cumsum()*SEAWEED_KCALS/KCALS_MONTHLY)
		legend = [
			'Max Density times Max Area',
			'7.9 billion people monthly kcals requirement',
			'Aron\'s Spreadsheet Food Wet Harvest Estimate',
			'Optimizer Estimate Food Wet Harvest Estimate'
			]
			
		if(ADD_STORED_FOOD):
			legend.append('Stored Food Eaten')
			plt.plot(time_days_middle,np.array(stored_food_eaten_vals).cumsum())
		plt.legend(legend)
		plt.title('Cumulative Eaten food, Billions of people, Monthly')
		plt.yscale('log')
		plt.show()

		# plt.plot(spreadsheet_days,world_kcals_month/KCALS_MONTHLY)
		# plt.plot(time_days_daily,np.array(seaweed_food_produced_monthly)*SEAWEED_KCALS/KCALS_MONTHLY)
		# legend = [
		# 	'7.9 billion people monthly kcals requirement',
		# 	'Seaweed Food'
		# 	]
			
		# if(ADD_STORED_FOOD):
		# 	legend.append('Stored Food Eaten')
		# 	plt.plot(time_days_middle,np.array(stored_food_eaten_vals).cumsum())
		# plt.legend(legend)
		# plt.title('Cumulative Eaten food, Billions of people, Monthly')
		# plt.yscale('log')
		# plt.show()
		

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
			plt.legend(['kcals req satisfied','fat req satisfied','protein req satisfied'])
			plt.title('People Fed (Billions)')
			plt.xlabel('Months Since May Nuclear Event')
			plt.show()
