'''

A set of utility functions useful for plotting 

'''
import os
import sys
module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
	sys.path.append(module_path)

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from cycler import cycler
class Plotter:
	def __init__(self):
		pass

	def plot_stored_food(time_months,analysis):
		ls_cycler = cycler('linestyle',
							[\
							 (0,()), # solid 
							 (0, (1, 1)), # densely dotted
							 (0, (1, 5)) # dotted
							 ]
						  )

		color_cycler = cycler('color', [plt.get_cmap('viridis')(i/3) for i in np.arange(3)] )

		new_cycler = color_cycler + ls_cycler
		plt.rc('axes',prop_cycle=new_cycler)
		
		plt.plot(time_months,np.array(analysis.billion_person_years_SF_kcals))
		plt.plot(time_months,np.array(analysis.billion_person_years_SF_fat))
		plt.plot(time_months,np.array(analysis.billion_person_years_SF_protein))
		plt.title('Stored Food')
		plt.xlabel('Months Since May Sunlight Reduction Event')
		plt.ylabel('Billion Person-Years')
		plt.legend(['kcals available','fat available','protein available'])
		plt.show()

	def plot_CS(time_months_middle,analysis):
		ls_cycler = cycler('linestyle',
							[\
							 (0,()) # solid 
							 # (0, (1, 1)), # densely dotted
							 # (0, (1, 5)) # dotted
							 ]
						  )

		color_cycler = cycler('color', [plt.get_cmap('viridis')(i) for i in np.arange(len(ls_cycler))] )

		new_cycler = color_cycler + ls_cycler
		plt.rc('axes',prop_cycle=new_cycler)
		
		plt.plot(time_months_middle,np.array(analysis.billions_fed_CS_kcals),marker='o',markersize=3)
		plt.title('Industrial Foods')
		plt.xlabel('Months Since May Sunlight Reduction Event')
		plt.ylabel('Billions fed from CS')
		plt.show()

	def plot_fish(time_months_middle,analysis):
		ls_cycler = cycler('linestyle',
							[\
							 (0,()), # solid 
							 (0, (1, 1)), # densely dotted
							 (0, (1, 5)) # dotted
							 ]
						  )

		color_cycler = cycler('color', [plt.get_cmap('viridis')(i) for i in np.arange(len(ls_cycler))] )

		new_cycler = color_cycler + ls_cycler
		plt.rc('axes',prop_cycle=new_cycler)
		
		plt.plot(time_months_middle,analysis.billions_fed_fish_kcals,marker='o',markersize=3)
		plt.plot(time_months_middle,analysis.billions_fed_fish_fat,marker='o',markersize=3)
		plt.plot(time_months_middle,analysis.billions_fed_fish_protein,marker='o',markersize=3)
		plt.legend(['kcals available','fat available','protein available'])

		plt.title('Fish')
		plt.xlabel('Months Since May Sunlight Reduction Event')
		plt.ylabel('Billions fed from fish')
		plt.show()

	def plot_GH(time_months_middle,analysis):
		ls_cycler = cycler('linestyle',
							[\
							 (0,()), # solid 
							 (0, (1, 1)), # densely dotted
							 (0, (1, 5)) # dotted
							 ]
						  )

		color_cycler = cycler('color', [plt.get_cmap('viridis')(i) for i in np.arange(len(ls_cycler))] )

		new_cycler = color_cycler + ls_cycler
		plt.rc('axes',prop_cycle=new_cycler)
		
		plt.plot(time_months_middle,np.array(analysis.billions_fed_GH_kcals),marker='o',markersize=3)
		plt.plot(time_months_middle,np.array(analysis.billions_fed_GH_fat),marker='o',markersize=3)
		plt.plot(time_months_middle,np.array(analysis.billions_fed_GH_protein),marker='o',markersize=3)
		plt.title('Greenhouses')
		plt.xlabel('Months Since May Sunlight Reduction Event')
		plt.ylabel('Billions Fed from Greenhouses')
		plt.legend(['kcals available','fat available','protein available'])
		plt.show()

	def plot_OG_with_resilient_foods(time_months_middle,analysis):
		# ls_cycler = cycler('linestyle',
		# 					[\
		# 					 (0,()), # solid 
		# 					 (0, (1, 1)), # densely dotted
		# 					 (0, (1, 5)) # dotted
		# 					 ]
		# 				  )

		# color_cycler = cycler('color', [plt.get_cmap('viridis')(i) for i in np.arange(len(ls_cycler))] )

		# new_cycler = color_cycler + ls_cycler
		# plt.rc('axes',prop_cycle=new_cycler)
		plt.title('Outdoor Growing, Resilient Foods Deployment')
		plt.xlabel('Months Since May Sunlight Reduction Event')
		
		ax = plt.gca()
		ax2 = ax.twinx()
		
		ax.plot(time_months_middle,np.array(analysis.\
			billions_fed_OG_produced_kcals),marker='o',markersize=3,color='green', linestyle='solid')
		ax.set_ylabel('Calories per Capita per Day')
		ax.legend(['kcals available'],loc=2)
		# ax2.set_x(['kcals available'])

		ax2.plot(time_months_middle,np.array(analysis.\
			billions_fed_OG_produced_fat),marker='o',markersize=3,color='red', linestyle='dashed')
		ax2.plot(time_months_middle,np.array(analysis.\
			billions_fed_OG_produced_protein),marker='o',markersize=3,color='blue', linestyle='dotted')
		ax2.set_ylabel('Grams per Capita per Day')
		ax2.set_ylim([0,50])
		ax2.legend(['fat available','protein available'],loc=1)
		
		plt.show()

	def plot_OG_before_nuclear_event(time_months_middle,analysis):
		plt.title('Outdoor Growing, Present-Day')
		plt.xlabel('Months Since May')
		
		ax = plt.gca()
		ax2 = ax.twinx()
		
		ax.plot(time_months_middle,np.array(analysis.\
			billions_fed_OG_produced_kcals),marker='o',markersize=3,color='green', linestyle='solid')
		ax.set_ylabel('Calories per Capita per Day')
		ax.legend(['kcals available'],loc=2)
		# ax2.set_x(['kcals available'])

		ax2.plot(time_months_middle,np.array(analysis.\
			billions_fed_OG_produced_fat),marker='o',markersize=3,color='red', linestyle='dashed')
		ax2.plot(time_months_middle,np.array(analysis.\
			billions_fed_OG_produced_protein),marker='o',markersize=3,color='blue', linestyle='dotted')
		ax2.set_ylabel('Grams per Capita per Day')
		ax2.set_ylim([0,50])
		ax2.legend(['fat available','protein available'],loc=1)
		
		plt.show()



	def plot_OG_no_resilient_foods(time_months_middle,analysis):
		plt.title('Outdoor Growing, No Resilient Foods Deployment')
		plt.xlabel('Months Since May')
		
		ax = plt.gca()
		ax2 = ax.twinx()
		
		ax.plot(time_months_middle,np.array(analysis.\
			billions_fed_OG_produced_kcals),marker='o',markersize=3,color='green', linestyle='solid')
		ax.set_ylabel('Calories per Capita per Day')
		ax.legend(['kcals available'],loc=2)
		# ax2.set_x(['kcals available'])

		ax2.plot(time_months_middle,np.array(analysis.\
			billions_fed_OG_produced_fat),marker='o',markersize=3,color='red', linestyle='dashed')
		ax2.plot(time_months_middle,np.array(analysis.\
			billions_fed_OG_produced_protein),marker='o',markersize=3,color='blue', linestyle='dotted')
		ax2.set_ylabel('Grams per Capita per Day')
		ax2.set_ylim([0,50])
		ax2.legend(['fat available','protein available'],loc=1)
		
		plt.show()




	def plot_nonegg_nondairy_meat(time_months_middle,analysis):

		plt.plot(time_months_middle,np.array(analysis.billions_fed_meat_kcals))
		plt.plot(time_months_middle,np.array(analysis.billions_fed_meat_fat))
		plt.plot(time_months_middle,np.array(analysis.billions_fed_meat_protein))
		plt.title('Meat')
		plt.xlabel('Months Since May Sunlight Reduction Event')
		plt.ylabel('Billion Person-Years')
		plt.legend(['kcals available','fat available','protein available'])
		plt.show()

	def plot_dairy_cows(time_months_middle,analysis):
		plt.plot(time_months_middle,np.array(analysis.millions_dairy_animals_midmonth),marker='o',markersize=3)
		plt.title('Millions of Dairy Animals')
		plt.xlabel('Months Since May Sunlight Reduction Event')
		plt.ylabel('Livestock Population, Millions')
		plt.show()


	def plot_dairy(time_months,analysis):
		ls_cycler = cycler('linestyle',
							[\
							 (0,()), # solid 
							 (0,()), # solid 
							 (0,()), # solid 
							 (0, (1, 1)), # densely dotted
							 (0, (1, 1)), # densely dotted
							 (0, (1, 1)) # densely dotted
							 ]
						  )

		color_cycler = cycler('color', [plt.get_cmap('viridis')(np.floor(i%3)/3) for i in np.arange(len(ls_cycler))])

		new_cycler = color_cycler + ls_cycler
		plt.rc('axes',prop_cycle=new_cycler)
		
		plt.plot(time_months,np.array(analysis.billions_fed_milk_kcals))
		plt.plot(time_months,np.array(analysis.billions_fed_milk_fat))
		plt.plot(time_months,np.array(analysis.billions_fed_milk_protein))
		# plt.plot(time_months,np.array(analysis.billions_fed_dairy_meat_kcals))
		# plt.plot(time_months,np.array(analysis.billions_fed_dairy_meat_fat))
		# plt.plot(time_months,np.array(analysis.billions_fed_dairy_meat_protein))
		plt.title('Billions Fed from Milk and Eating Dairy Animals')
		plt.xlabel('Months Since May Sunlight Reduction Event')
		plt.ylabel('Billion Person-Years')
		plt.legend([\
			'kcals available, milk',
			'fat available, milk',
			'protein available, milk',
			'kcals available, dairy cow meat',
			'fat available, dairy cow meat',
			'protein available, dairy cow meat'])
		plt.show()

	def plot_people_fed(time_months_middle,analysis):
		linestyles=[]
		if(analysis.constants['ADD_STORED_FOOD']):
			linestyles = linestyles + ([\
				(0,()), # solid 
				(0,()), # solid 
				(0,()) # solid 
				])
		if(analysis.constants['ADD_NONEGG_NONDAIRY_MEAT']):
			linestyles = linestyles + ([\
				(0,(1, 1)), # densely dotted 
				(0,(1, 1)), # densely dotted 
				(0,(1, 1)) # densely dotted 
				])
		if(analysis.constants['ADD_DAIRY']):
			linestyles = linestyles + ([\
				(0,(1, 5)), # dotted 
				(0,(1, 5)), # dotted 
				(0,(1, 5)) # dotted 
				])
		if(analysis.constants['ADD_SEAWEED']):
			linestyles = linestyles + ([\
				(0, (3, 5, 1, 5)), # dashdotted
				(0, (3, 5, 1, 5)), # dashdotted
				(0, (3, 5, 1, 5)) # dashdotted
				])
		if(analysis.constants['ADD_GREENHOUSES']):
			linestyles = linestyles + ([\
				(0, (5, 1)), # densely dashed 
				(0, (5, 1)), # densely dashed 
				(0, (5, 1)), # densely dashed 
				])

		# if(analysis.constants['ADD_FISH']):
		# 	linestyles = linestyles + ([\
		# 		(0, (5, 1)), # densely dashed 
		# 		(0, (5, 1)), # densely dashed 
		# 		(0, (5, 1)), # densely dashed 
		# 		])

		if(analysis.constants['ADD_OUTDOOR_GROWING']):
			linestyles = linestyles + ([\
				(0, (3, 10, 1, 10, 1, 10)), # loosely dash dotted 
				(0, (3, 10, 1, 10, 1, 10)), # loosely dash dotted 
				(0, (3, 10, 1, 10, 1, 10)), # loosely dash dotted 
				])

		if(analysis.constants['ADD_CELLULOSIC_SUGAR']):
			linestyles = linestyles + ([(0, (3, 1, 1, 1, 1, 1))]) # densely dashdotdotted

		ls_cycler = cycler('linestyle',linestyles)

		color_cycler = cycler('color', [plt.get_cmap('viridis')(np.floor(i%3)/3) for i in np.arange(len(linestyles))])

		new_cycler = color_cycler + ls_cycler
		plt.rc('axes',prop_cycle=new_cycler)
		fig = plt.figure()
		ax=plt.subplot(111)
		legend=[]
		if(analysis.constants['ADD_STORED_FOOD']):
			ax.plot(time_months_middle,analysis.billions_fed_SF_kcals,marker='o',markersize=3)
			ax.plot(time_months_middle,analysis.billions_fed_SF_fat,marker='o',markersize=3)
			ax.plot(time_months_middle,analysis.billions_fed_SF_protein,marker='o',markersize=3)
			legend = legend + ['Stored Food, Limited by kcals',
			'Stored Food, Limited by Fat',
			'Stored Food, Limited by protein']
		if(analysis.constants['ADD_NONEGG_NONDAIRY_MEAT']):
			ax.plot(time_months_middle,np.array(analysis.billions_fed_meat_kcals)\
				# +np.array(analysis.billions_fed_dairy_meat_kcals)\
				,marker='o',markersize=3)
			ax.plot(time_months_middle,np.array(analysis.billions_fed_meat_fat)\
				+np.array(analysis.billions_fed_dairy_meat_fat),marker='o',markersize=3)
			ax.plot(time_months_middle,np.array(analysis.billions_fed_meat_protein)\
				+np.array(analysis.billions_fed_dairy_meat_protein),marker='o',markersize=3)
			legend = legend + ['Meat, Limited by kcals',
			'Meat, Limited by Fat',
			'Meat, Limited by protein']
		if(analysis.constants['ADD_DAIRY']):
			ax.plot(time_months_middle,analysis.billions_fed_milk_kcals,marker='o',markersize=3)
			ax.plot(time_months_middle,analysis.billions_fed_milk_fat,marker='o',markersize=3)
			ax.plot(time_months_middle,analysis.billions_fed_milk_protein,marker='o',markersize=3)
			legend = legend + ['Milk, Limited by kcals',
			'Milk, Limited by Fat',
			'Milk, Limited by protein']

		if(analysis.constants['ADD_SEAWEED']):
			ax.plot(time_months_middle,analysis.billions_fed_seaweed_kcals,marker='o',markersize=3)
			ax.plot(time_months_middle,analysis.billions_fed_seaweed_fat,marker='o',markersize=3)
			ax.plot(time_months_middle,analysis.billions_fed_seaweed_protein,marker='o',markersize=3)
			legend = legend + ['Seaweed, Limited by kcals',
				'Seaweed, Limited by Fat',
				'Seaweed, Limited by protein']
		if(analysis.constants['ADD_GREENHOUSES']):
			ax.plot(time_months_middle,analysis.billions_fed_GH_kcals,marker='o',markersize=3)
			ax.plot(time_months_middle,analysis.billions_fed_GH_fat,marker='o',markersize=3)
			ax.plot(time_months_middle,analysis.billions_fed_GH_protein,marker='o',markersize=3)
			legend = legend + ['Greenhouse Food, Limited by kcals',
			'Greenhouse Food, Limited by Fat',
			'Greenhouse Food, Limited by protein']
		if(analysis.constants['ADD_OUTDOOR_GROWING']):
			ax.plot(time_months_middle,analysis.billions_fed_OG_kcals,marker='o',markersize=3)
			ax.plot(time_months_middle,analysis.billions_fed_OG_fat,marker='o',markersize=3)
			ax.plot(time_months_middle,analysis.billions_fed_OG_protein,marker='o',markersize=3)
			legend = legend + ['Outdoor Growing Food, Limited by kcals',
			'Outdoor Growing Food, Limited by Fat',
			'Outdoor Growing Food, Limited by protein']
		if(analysis.constants['ADD_CELLULOSIC_SUGAR']):
			ax.plot(time_months_middle,analysis.billions_fed_CS_kcals,marker='o',markersize=3)
			legend = legend + ['Industrial Foods, Limited by kcals']

		# if(analysis.constants['ADD_FISH']
		# 	ax.plot(time_months_middle,analysis.billions_fed_CS_kcals,marker='o',markersize=3)
		# 	legend = legend + ['Cellulosic Sugar, Limited by kcals']

		box = ax.get_position()
		ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
		ax.legend(legend,loc='center left', bbox_to_anchor=(1, 0.5))
		plt.title('People fed, by type')
		plt.ylabel('billions of people')
		plt.xlabel('Months Since May Sunlight Reduction Event')
		# plt.legend(legend,loc='upper center', bbox_to_anchor=(0.5, 1.05),
		  # ncol=3, fancybox=True, shadow=True)
		ax.set_ylim([0,analysis.billions_fed_immediate_OG_kcals[-1]
			+analysis.billions_fed_new_stored_OG_kcals[-1]
			+analysis.billions_fed_SF_kcals[-1]
			+analysis.billions_fed_fish_kcals[-1]
			+analysis.billions_fed_milk_kcals[-1]
			+analysis.billions_fed_meat_kcals[-1]
			+analysis.billions_fed_GH_kcals[-1]
			+analysis.billions_fed_seaweed_kcals[-1]
			+analysis.billions_fed_CS_kcals[-1]
			+analysis.billions_fed_SCP_kcals[-1]]
			+analysis.billions_fed_h_e_milk_kcals[-1]
			+analysis.billions_fed_h_e_meat_kcals[-1])

		plt.show()

	def plot_people_fed_fat(time_months_middle,analysis):
		linestyles=[]
		if(analysis.constants['ADD_STORED_FOOD']):
			linestyles = linestyles + ([\
				(0,()) # solid 
				])
		if(analysis.constants['ADD_NONEGG_NONDAIRY_MEAT']):
			linestyles = linestyles + ([\
				(0,(1, 1)) # densely dotted 
				])
		if(analysis.constants['ADD_DAIRY']):
			linestyles = linestyles + ([\
				(0,(1, 5)) # dotted 
				])
		if(analysis.constants['ADD_SEAWEED']):
			linestyles = linestyles + ([\
				(0, (3, 5, 1, 5)), # dashdotted
				])
		if(analysis.constants['ADD_GREENHOUSES']):
			linestyles = linestyles + ([\
				(0, (5, 1)), # densely dashed 
				])
		if(analysis.constants['ADD_OUTDOOR_GROWING']):
			linestyles = linestyles + ([\
				(0, (3, 10, 1, 10, 1, 10)) # loosely dash dotted 
				])

		ls_cycler = cycler('linestyle',linestyles)

		color_cycler = cycler('color', [plt.get_cmap('viridis')(i/len(linestyles)) for i in np.arange(len(linestyles))])

		new_cycler = color_cycler + ls_cycler
		plt.rc('axes',prop_cycle=new_cycler)
		fig = plt.figure()
		ax=plt.subplot(111)
		legend=[]
		if(analysis.constants['ADD_STORED_FOOD']):
			ax.plot(time_months_middle,analysis.billions_fed_SF_fat,marker='o',markersize=3)
			legend = legend + ['Stored Food']
		if(analysis.constants['ADD_NONEGG_NONDAIRY_MEAT']):
			ax.plot(time_months_middle,np.array(analysis.billions_fed_meat_fat)\
				+np.array(analysis.billions_fed_dairy_meat_fat),marker='o',markersize=3)
			legend = legend + ['Meat']
		if(analysis.constants['ADD_DAIRY']):
			ax.plot(time_months_middle,analysis.billions_fed_milk_fat,marker='o',markersize=3)
			legend = legend + ['Milk']

		if(analysis.constants['ADD_SEAWEED']):
			ax.plot(time_months_middle,analysis.billions_fed_seaweed_fat,marker='o',markersize=3)
			legend = legend + ['Seaweed']
		if(analysis.constants['ADD_GREENHOUSES']):
			ax.plot(time_months_middle,analysis.billions_fed_GH_fat,marker='o',markersize=3)
			legend = legend + ['Greenhouse Food']
		if(analysis.constants['ADD_OUTDOOR_GROWING']):
			ax.plot(time_months_middle,analysis.billions_fed_OG_fat,marker='o',markersize=3)
			legend = legend + ['Outdoor Growing']
		box = ax.get_position()
		ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
		ax.legend(legend,loc='center left', bbox_to_anchor=(1, 0.5))
		plt.title('People fed, in terms of fat')
		plt.ylabel('billions of people')
		plt.xlabel('Months Since May Sunlight Reduction Event')
		# plt.legend(legend,loc='upper center', bbox_to_anchor=(0.5, 1.05),
		  # ncol=3, fancybox=True, shadow=True)

		plt.show()

	def plot_people_fed_protein(time_months_middle,analysis):
		linestyles=[]
		if(analysis.constants['ADD_STORED_FOOD']):
			linestyles = linestyles + ([\
				(0,()) # solid 
				])
		if(analysis.constants['ADD_NONEGG_NONDAIRY_MEAT']):
			linestyles = linestyles + ([\
				(0,(1, 1)) # densely dotted 
				])
		if(analysis.constants['ADD_DAIRY']):
			linestyles = linestyles + ([\
				(0,(1, 5)) # dotted 
				])
		if(analysis.constants['ADD_SEAWEED']):
			linestyles = linestyles + ([\
				(0, (3, 5, 1, 5)), # dashdotted
				])
		if(analysis.constants['ADD_GREENHOUSES']):
			linestyles = linestyles + ([\
				(0, (5, 1)), # densely dashed 
				])
		if(analysis.constants['ADD_OUTDOOR_GROWING']):
			linestyles = linestyles + ([\
				(0, (3, 10, 1, 10, 1, 10)) # loosely dash dotted 
				])

		ls_cycler = cycler('linestyle',linestyles)

		color_cycler = cycler('color', [plt.get_cmap('viridis')(i/len(linestyles)) for i in np.arange(len(linestyles))])

		new_cycler = color_cycler + ls_cycler
		plt.rc('axes',prop_cycle=new_cycler)
		fig = plt.figure()
		ax=plt.subplot(111)
		legend=[]
		if(analysis.constants['ADD_STORED_FOOD']):
			ax.plot(time_months_middle,analysis.billions_fed_SF_protein,marker='o',markersize=3)
			legend = legend + ['Stored Food']
		if(analysis.constants['ADD_NONEGG_NONDAIRY_MEAT']):
			ax.plot(time_months_middle,np.array(analysis.billions_fed_meat_protein)\
				+np.array(analysis.billions_fed_dairy_meat_protein),marker='o',markersize=3)
			legend = legend + ['Meat']
		if(analysis.constants['ADD_DAIRY']):
			ax.plot(time_months_middle,analysis.billions_fed_milk_protein,marker='o',markersize=3)
			legend = legend + ['Milk']

		if(analysis.constants['ADD_SEAWEED']):
			ax.plot(time_months_middle,analysis.billions_fed_seaweed_protein,marker='o',markersize=3)
			legend = legend + ['Seaweed']
		if(analysis.constants['ADD_GREENHOUSES']):
			ax.plot(time_months_middle,analysis.billions_fed_GH_protein,marker='o',markersize=3)
			legend = legend + ['Greenhouse Food']
		if(analysis.constants['ADD_OUTDOOR_GROWING']):
			ax.plot(time_months_middle,analysis.billions_fed_OG_protein,marker='o',markersize=3)
			legend = legend + ['Outdoor Growing']
		box = ax.get_position()
		ax.set_position([box.x0, box.y0, box.width * 0.695, box.height])
		ax.legend(legend,loc='center left', bbox_to_anchor=(1, 0.5))
		plt.title('People fed, in terms of protein')
		plt.ylabel('billions of people')
		plt.xlabel('Months Since May Sunlight Reduction Event')
		# plt.legend(legend,loc='upper center', bbox_to_anchor=(0.5, 1.05),
		  # ncol=3, fancybox=True, shadow=True)
		ax.set_ylim([0,analysis.billions_fed_immediate_OG_kcals[-1]
			+analysis.billions_fed_new_stored_OG_kcals[-1]
			+analysis.billions_fed_SF_kcals[-1]
			+analysis.billions_fed_fish_kcals[-1]
			+analysis.billions_fed_milk_kcals[-1]
			+analysis.billions_fed_meat_kcals[-1]
			+analysis.billions_fed_GH_kcals[-1]
			+analysis.billions_fed_seaweed_kcals[-1]
			+analysis.billions_fed_CS_kcals[-1]
			+analysis.billions_fed_SCP_kcals[-1]]
			+analysis.billions_fed_h_e_milk_kcals[-1]
			+analysis.billions_fed_h_e_meat_kcals[-1])

		plt.show()



	def plot_people_fed_kcals(time_months_middle,analysis):

		font = {'family' : 'normal',
				'weight' : 'bold',
				'size'   : 16}

		matplotlib.rc('font', **font)
		fig = plt.figure()
		ax=plt.subplot(111)
		# legend=[]
		# if(analysis.constants['ADD_STORED_FOOD']):
		# 	legend = legend + ['Stored Food']
		# if(analysis.constants['ADD_NONEGG_NONDAIRY_MEAT']):
		# 	legend = legend + ['Meat']
		# if(analysis.constants['ADD_DAIRY']):
		# 	legend = legend + ['Milk']
		# if(analysis.constants['ADD_DAIRY']):
		# 	legend = legend + ['Fish']
		# if(analysis.constants['ADD_SEAWEED']):
		# 	legend = legend + ['Seaweed']
		# if(analysis.constants['ADD_GREENHOUSES']):
		# 	legend = legend + ['Greenhouse Food']
		# if(analysis.constants['ADD_OUTDOOR_GROWING']):
		# 	legend = legend + ['Outdoor Growing']
		# if(analysis.constants['ADD_CELLULOSIC_SUGAR']):
		# 	legend = legend + ['Cellulosic Sugar']
		# https://jacksonlab.agronomy.wisc.edu/2016/05/23/15-level-colorblind-friendly-palette/
		# 	"#000000","#004949","#009292","#ff6db6","#ffb6db",
		# "#490092","#006ddb","#b66dff","#6db6ff","#b6dbff",
		# "#920000","#924900","#db6d00","#24ff24","#ffff6d"
		# patterns = [ "/" , "\\" , "|" , "-" , "+" , "x", "o", "O", ".", "*" ]
		patterns = [ "/" , "\\" , "|" , "-" , "+" , "x", "o", "O"]
		pal=["#006ddb","#b66dff","6db6ff","#b6dbff",\
		 "#920000","#924900","#db6d00","#24ff24","#ffff6d"]
		# print('analysis.billions_fed_immediate_OG_kcals')
		# print(analysis.billions_fed_immediate_OG_kcals)
		# print('analysis.billions_fed_new_stored_OG_kcals')
		# print(analysis.billions_fed_new_stored_OG_kcals)


		stacks = ax.stackplot(time_months_middle,\
			analysis.billions_fed_fish_kcals/analysis.constants["CONVERT_TO_KCALS"],\
			(np.array(analysis.billions_fed_CS_kcals)+np.array(analysis.billions_fed_SCP_kcals))/ analysis.constants["CONVERT_TO_KCALS"],\
			analysis.billions_fed_GH_kcals/ analysis.constants["CONVERT_TO_KCALS"],\
			analysis.billions_fed_seaweed_kcals/ analysis.constants["CONVERT_TO_KCALS"],\
			(analysis.billions_fed_milk_kcals+analysis.billions_fed_h_e_milk_kcals)/ analysis.constants["CONVERT_TO_KCALS"],\
			(analysis.billions_fed_meat_kcals+analysis.billions_fed_h_e_meat_kcals)/analysis.constants["CONVERT_TO_KCALS"],\
			analysis.billions_fed_SF_kcals/analysis.constants["CONVERT_TO_KCALS"],\
			analysis.billions_fed_immediate_OG_kcals/analysis.constants["CONVERT_TO_KCALS"],\
			analysis.billions_fed_new_stored_OG_kcals/analysis.constants["CONVERT_TO_KCALS"],\
			 labels=[\
			 'Marine Fish',\
			 'Industrial Foods',\
			 'Greenhouses',\
			 'Seaweed',\
			 'Dairy Milk',\
			 'Culled Livestock and Meat \nfrom Human Inedible Feed ',\
			 'Crops consumed that month \n that were stored \n before sunlight reduction',\
			 'Outdoor Crops consumed \n immediately',
			 'Crops consumed that month \n that were stored \n after sunlight reduction'
			 # ], colors=pal)
			 ], colors=pal)
		for stack, hatch in zip(stacks, patterns):
			stack.set_hatch(hatch)
		box = ax.get_position()
		ax.set_position([box.x0, box.y0, box.width * 0.695, box.height])
		handles, labels = ax.get_legend_handles_labels()   #get the handles
		ax.legend()
		ax.legend(loc='center left', bbox_to_anchor=(1, 0.5),handles=reversed(handles),labels=reversed(labels))
		# plt.title('Caloric Availability, Nuclear Winter, No Resilient Foods')
		plt.title('Primary Caloric Monthly Sources, With Deployment')
		plt.ylabel('Calories per Capita per Day')
		plt.xlabel('Months Since May Sunlight Reduction Event')
		# plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05),
		#   ncol=3, fancybox=True, shadow=True)
		ax.set_ylim([0,(analysis.billions_fed_immediate_OG_kcals[-1]
			+analysis.billions_fed_new_stored_OG_kcals[-1]
			+analysis.billions_fed_SF_kcals[-1]
			+analysis.billions_fed_fish_kcals[-1]
			+analysis.billions_fed_milk_kcals[-1]
			+analysis.billions_fed_meat_kcals[-1]
			+analysis.billions_fed_h_e_milk_kcals[-1]
			+analysis.billions_fed_h_e_meat_kcals[-1]
			+analysis.billions_fed_GH_kcals[-1]
			+analysis.billions_fed_seaweed_kcals[-1]
			+analysis.billions_fed_CS_kcals[-1]
			+analysis.billions_fed_SCP_kcals[-1])/analysis.constants["CONVERT_TO_KCALS"]])
		# ax.set_ylim([0,48])
		ax.set_xlim([0,48])
		plt.show()


	def plot_people_fed_kcals_before_nuclear_event(time_months_middle,analysis):

		font = {'family' : 'normal',
				'weight' : 'bold',
				'size'   : 16}

		matplotlib.rc('font', **font)
		fig = plt.figure()
		ax=plt.subplot(111)
		# legend=[]
		# if(analysis.constants['ADD_STORED_FOOD']):
		# 	legend = legend + ['Stored Food']
		# if(analysis.constants['ADD_NONEGG_NONDAIRY_MEAT']):
		# 	legend = legend + ['Meat']
		# if(analysis.constants['ADD_DAIRY']):
		# 	legend = legend + ['Milk']
		# if(analysis.constants['ADD_DAIRY']):
		# 	legend = legend + ['Fish']
		# if(analysis.constants['ADD_SEAWEED']):
		# 	legend = legend + ['Seaweed']
		# if(analysis.constants['ADD_GREENHOUSES']):
		# 	legend = legend + ['Greenhouse Food']
		# if(analysis.constants['ADD_OUTDOOR_GROWING']):
		# 	legend = legend + ['Outdoor Growing']
		# if(analysis.constants['ADD_CELLULOSIC_SUGAR']):
		# 	legend = legend + ['Cellulosic Sugar']
		# https://jacksonlab.agronomy.wisc.edu/2016/05/23/15-level-colorblind-friendly-palette/
		# 	"#000000","#004949","#009292","#ff6db6","#ffb6db",
		# "#490092","#006ddb","#b66dff","#6db6ff","#b6dbff",
		# "#920000","#924900","#db6d00","#24ff24","#ffff6d"
		# patterns = [ "/" , "\\" , "|" , "-" , "+" , "x", "o", "O", ".", "*" ]
		patterns = [ "/" , "\\" , "|" , "-" , "+" , "x", "o", "O"]
		pal=["#006ddb","#b66dff","6db6ff","#b6dbff",\
		 "#920000","#924900","#db6d00","#24ff24","#ffff6d"]

		stacks = ax.stackplot(time_months_middle,\
			analysis.billions_fed_fish_kcals/analysis.constants["CONVERT_TO_KCALS"],\
			analysis.billions_fed_immediate_OG_kcals/analysis.constants["CONVERT_TO_KCALS"],\
			analysis.billions_fed_new_stored_OG_kcals/analysis.constants["CONVERT_TO_KCALS"],\
			analysis.billions_fed_SF_kcals/analysis.constants["CONVERT_TO_KCALS"],\
			(analysis.billions_fed_milk_kcals\
				+analysis.billions_fed_h_e_milk_kcals)/analysis.constants["CONVERT_TO_KCALS"],\
			(np.array(analysis.billions_fed_meat_kcals)\
				+analysis.billions_fed_h_e_meat_kcals)/analysis.constants["CONVERT_TO_KCALS"],\
			 analysis.billions_fed_GH_kcals/analysis.constants["CONVERT_TO_KCALS"],\
			 analysis.billions_fed_seaweed_kcals/analysis.constants["CONVERT_TO_KCALS"],\
			(np.array(analysis.billions_fed_CS_kcals)+np.array(analysis.billions_fed_SCP_kcals))/analysis.constants["CONVERT_TO_KCALS"],\
			 labels=[\
			 'Marine Fish',\
			 'Crops consumed \n immediately',
			 'Crops consumed that month \n that were stored \n after simulation',\
			 'Crops consumed that month \n that were stored \n before simulation',
			 'Dairy Milk',\
			 # 'All livestock',\
			 ], colors=pal)
			 # 'Greenhouses',\
			 # 'Seaweed',\
			 # 'Industrial Foods'\
			 # ], colors=pal)
		for stack, hatch in zip(stacks, patterns):
			stack.set_hatch(hatch)
		box = ax.get_position()
		ax.set_position([box.x0, box.y0, box.width * 0.695, box.height])
		handles, labels = ax.get_legend_handles_labels()   #get the handles
		ax.legend()
		ax.legend(loc='center left', bbox_to_anchor=(1, 0.5),handles=reversed(handles),labels=reversed(labels))
		plt.title('Primary Caloric Monthly Sources, Present-Day')
		plt.ylabel('Calories per Capita per Day')
		plt.xlabel('Months Since May Sunlight Reduction Event')
		# plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05),
		#   ncol=3, fancybox=True, shadow=True)
		ax.set_xlim([0,48])
		ax.set_ylim([0,(analysis.billions_fed_immediate_OG_kcals[-1]
			+analysis.billions_fed_new_stored_OG_kcals[-1]
			+analysis.billions_fed_SF_kcals[-1]
			+analysis.billions_fed_fish_kcals[-1]
			+analysis.billions_fed_milk_kcals[-1]
			+analysis.billions_fed_meat_kcals[-1]
			+analysis.billions_fed_h_e_milk_kcals[-1]
			+analysis.billions_fed_h_e_meat_kcals[-1]
			+analysis.billions_fed_GH_kcals[-1]
			+analysis.billions_fed_seaweed_kcals[-1]
			+analysis.billions_fed_CS_kcals[-1]
			+analysis.billions_fed_SCP_kcals[-1])/self.constants["CONVERT_TO_KCALS"]])
		plt.show()


	def plot_people_fed_kcals_no_resilient(time_months_middle,analysis):

		font = {'family' : 'normal',
				'weight' : 'bold',
				'size'   : 16}

		matplotlib.rc('font', **font)
		fig = plt.figure()
		ax=plt.subplot(111)
		# legend=[]
		# if(analysis.constants['ADD_STORED_FOOD']):
		# 	legend = legend + ['Stored Food']
		# if(analysis.constants['ADD_NONEGG_NONDAIRY_MEAT']):
		# 	legend = legend + ['Meat']
		# if(analysis.constants['ADD_DAIRY']):
		# 	legend = legend + ['Milk']
		# if(analysis.constants['ADD_DAIRY']):
		# 	legend = legend + ['Fish']
		# if(analysis.constants['ADD_SEAWEED']):
		# 	legend = legend + ['Seaweed']
		# if(analysis.constants['ADD_GREENHOUSES']):
		# 	legend = legend + ['Greenhouse Food']
		# if(analysis.constants['ADD_OUTDOOR_GROWING']):
		# 	legend = legend + ['Outdoor Growing']
		# if(analysis.constants['ADD_CELLULOSIC_SUGAR']):
		# 	legend = legend + ['Cellulosic Sugar']
		# https://jacksonlab.agronomy.wisc.edu/2016/05/23/15-level-colorblind-friendly-palette/
		# 	"#000000","#004949","#009292","#ff6db6","#ffb6db",
		# "#490092","#006ddb","#b66dff","#6db6ff","#b6dbff",
		# "#920000","#924900","#db6d00","#24ff24","#ffff6d"
		# patterns = [ "/" , "\\" , "|" , "-" , "+" , "x", "o", "O", ".", "*" ]
		patterns = [ "/" , "\\" , "|" , "-" , "+" , "x", "o", "O"]
		pal=["#006ddb","#b66dff","6db6ff","#b6dbff",\
		 "#920000","#924900","#db6d00","#24ff24","#ffff6d"]
		# print('analysis.billions_fed_immediate_OG_kcals')
		# print(analysis.billions_fed_immediate_OG_kcals)
		# print('analysis.billions_fed_new_stored_OG_kcals')
		# print(analysis.billions_fed_new_stored_OG_kcals)

		stacks = ax.stackplot(time_months_middle,\
			analysis.billions_fed_fish_kcals/analysis.constants["CONVERT_TO_KCALS"],\
			analysis.billions_fed_immediate_OG_kcals/analysis.constants["CONVERT_TO_KCALS"],\
			analysis.billions_fed_new_stored_OG_kcals/analysis.constants["CONVERT_TO_KCALS"],\
			analysis.billions_fed_SF_kcals/analysis.constants["CONVERT_TO_KCALS"],\
			# (analysis.billions_fed_milk_kcals\
			# 	+analysis.billions_fed_h_e_milk_kcals)/analysis.constants["CONVERT_TO_KCALS"],\
			(np.array(analysis.billions_fed_meat_kcals)\
				+analysis.billions_fed_h_e_meat_kcals)/analysis.constants["CONVERT_TO_KCALS"],\
			 analysis.billions_fed_GH_kcals/analysis.constants["CONVERT_TO_KCALS"],\
			 analysis.billions_fed_seaweed_kcals/analysis.constants["CONVERT_TO_KCALS"],\
			(np.array(analysis.billions_fed_CS_kcals)+np.array(analysis.billions_fed_SCP_kcals))/analysis.constants["CONVERT_TO_KCALS"],\
			 labels=[\
			 'Marine Fish',\
			 'Outdoor Crops consumed \n immediately',
			 'Crops consumed that month \n that were stored \n after sunlight reduction',
			 'Crops consumed that month \n that were stored \n before sunlight reduction',\
			 # 'Dairy Milk',\
			 'All Livestock Culled',\
			 ], colors=pal)
			 # 'Greenhouses',\
			 # 'Seaweed',\
			 # 'Industrial Foods'\
			 # ], colors=pal)
		for stack, hatch in zip(stacks, patterns):
			stack.set_hatch(hatch)
		box = ax.get_position()
		ax.set_position([box.x0, box.y0, box.width * 0.695, box.height])
		handles, labels = ax.get_legend_handles_labels()   #get the handles
		ax.legend()
		ax.legend(loc='center left', bbox_to_anchor=(1, 0.5),handles=reversed(handles),labels=reversed(labels))
		plt.title('Primary Caloric Monthly Sources, No Deployment')
		plt.ylabel('Calories per Capita per Day')
		plt.xlabel('Months Since May Sunlight Reduction Event')
		# plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05),
		#   ncol=3, fancybox=True, shadow=True)
		ax.set_ylim([0,(analysis.billions_fed_immediate_OG_kcals[-1]
			+analysis.billions_fed_new_stored_OG_kcals[-1]
			+analysis.billions_fed_SF_kcals[-1]
			+analysis.billions_fed_fish_kcals[-1]
			+analysis.billions_fed_milk_kcals[-1]
			+analysis.billions_fed_h_e_milk_kcals[-1]
			+analysis.billions_fed_meat_kcals[-1]
			+analysis.billions_fed_h_e_meat_kcals[-1]
			+analysis.billions_fed_GH_kcals[-1]
			+analysis.billions_fed_seaweed_kcals[-1]
			+analysis.billions_fed_CS_kcals[-1]
			+analysis.billions_fed_SCP_kcals[-1])/self.constants["CONVERT_TO_KCALS"]])
		ax.set_xlim([0,48])

		plt.show()


		# linestyles=[]
		# if(analysis.constants['ADD_STORED_FOOD']):
		# 	linestyles = linestyles + ([\
		# 		(0,()) # solid 
		# 		])
		# if(analysis.constants['ADD_NONEGG_NONDAIRY_MEAT']):
		# 	linestyles = linestyles + ([\
		# 		(0,(1, 1)) # densely dotted 
		# 		])
		# if(analysis.constants['ADD_DAIRY']):
		# 	linestyles = linestyles + ([\
		# 		(0,(1, 5)) # dotted 
		# 		])
		# if(analysis.constants['ADD_SEAWEED']):
		# 	linestyles = linestyles + ([\
		# 		(0, (3, 5, 1, 5)), # dashdotted
		# 		])
		# if(analysis.constants['ADD_GREENHOUSES']):
		# 	linestyles = linestyles + ([\
		# 		(0, (5, 1)), # densely dashed 
		# 		])
		# if(analysis.constants['ADD_OUTDOOR_GROWING']):
		# 	linestyles = linestyles + ([\
		# 		(0, (3, 10, 1, 10, 1, 10)) # loosely dash dotted 
		# 		])

		# if(analysis.constants['ADD_CELLULOSIC_SUGAR']):
		# 	linestyles = linestyles + ([(0, (3, 1, 1, 1, 1, 1))]) # densely dashdotdotted

		# ls_cycler = cycler('linestyle',linestyles)

		# color_cycler = cycler('color', [plt.get_cmap('viridis')(i/len(linestyles)) for i in np.arange(len(linestyles))])

		# new_cycler = color_cycler + ls_cycler
		# plt.rc('axes',prop_cycle=new_cycler)
		# fig = plt.figure()
		# ax=plt.subplot(111)
		# legend=[]
		# if(analysis.constants['ADD_STORED_FOOD']):
		# 	ax.plot(time_months_middle,analysis.billions_fed_SF_kcals,marker='o',markersize=3)
		# 	legend = legend + ['Stored Food']
		# if(analysis.constants['ADD_NONEGG_NONDAIRY_MEAT']):
		# 	ax.plot(time_months_middle,np.array(analysis.billions_fed_meat_kcals)\
		# 		+np.array(analysis.billions_fed_dairy_meat_kcals),marker='o',markersize=3)
		# 	legend = legend + ['Meat']
		# if(analysis.constants['ADD_DAIRY']):
		# 	ax.plot(time_months_middle,analysis.billions_fed_milk_kcals,marker='o',markersize=3)
		# 	legend = legend + ['Milk']

		# if(analysis.constants['ADD_SEAWEED']):
		# 	ax.plot(time_months_middle,analysis.billions_fed_seaweed_kcals,marker='o',markersize=3)
		# 	legend = legend + ['Seaweed']
		# if(analysis.constants['ADD_GREENHOUSES']):
		# 	ax.plot(time_months_middle,analysis.billions_fed_GH_kcals,marker='o',markersize=3)
		# 	legend = legend + ['Greenhouse Food']
		# if(analysis.constants['ADD_OUTDOOR_GROWING']):
		# 	ax.plot(time_months_middle,analysis.billions_fed_OG_kcals,marker='o',markersize=3)
		# 	legend = legend + ['Outdoor Growing']
		# if(analysis.constants['ADD_CELLULOSIC_SUGAR']):
		# 	ax.plot(time_months_middle,analysis.billions_fed_CS_kcals,marker='o',markersize=3)
		# 	legend = legend + ['Cellulosic Sugar']
		# box = ax.get_position()
		# ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
		# ax.legend(legend,loc='center left', bbox_to_anchor=(1, 0.5))
		# plt.title('People fed, in terms of calorie requirement')
		# plt.ylabel('billions of people')
		# plt.xlabel('Months Since May Sunlight Reduction Event')
		# # plt.legend(legend,loc='upper center', bbox_to_anchor=(0.5, 1.05),
		#   # ncol=3, fancybox=True, shadow=True)

		# plt.show()




	def plot_people_fed_combined(time_months_middle,analysis):

		
		fig = plt.figure()
		ax=plt.subplot(111)
		title=''
		if(analysis.constants['ADD_SEAWEED']):
			title = title + "Seaweed, "
		if(analysis.constants['ADD_STORED_FOOD']):
			title = title + "Stored Food, "
		if(analysis.constants['ADD_NONEGG_NONDAIRY_MEAT']):
			title = title + "Meat, "
		if(analysis.constants['ADD_CELLULOSIC_SUGAR']):
			title = title + "Cell. Sugar, "
		if(analysis.constants['ADD_DAIRY']):
			title = title + "Dairy, "
		if(analysis.constants['ADD_GREENHOUSES']):
			title = title + "Greenhouses, "
		if(analysis.constants['ADD_OUTDOOR_GROWING']):
			title = title + "Outdoor Growing, "
		if(analysis.constants['ADD_FISH']):
			title = title + "Fish, "
		title = title + "Population Fed"
		plt.title(title)
		plt.xlabel('Months Since May Sunlight Reduction Event')
		
		ax = plt.gca()
		# ax2 = ax.twinx()
		# print("analysis.billions_fed_meat_kcals")
		# print(analysis.billions_fed_OG_kcals[0])
		ax.plot(time_months_middle,
			np.array(analysis.billions_fed_SF_kcals)
			+np.array(analysis.billions_fed_meat_kcals)
			+np.array(analysis.billions_fed_seaweed_kcals)
			+np.array(analysis.billions_fed_milk_kcals)
			+np.array(analysis.billions_fed_CS_kcals)
			+np.array(analysis.billions_fed_SCP_kcals)
			+np.array(analysis.billions_fed_GH_kcals)
			+np.array(analysis.billions_fed_OG_kcals)
			+np.array(analysis.billions_fed_fish_kcals)
			+ analysis.billions_fed_h_e_meat_kcals\
			+ analysis.billions_fed_h_e_milk_kcals,marker='o',markersize=3,color='blue', linestyle='solid')
		ax.set_ylabel('Calories per Capita per Day')
		# ax.legend(['kcals available'],loc=2)
		# ax2.set_x(['kcals available'])

		ax.plot(time_months_middle,
			np.array(analysis.billions_fed_SF_protein)
			+np.array(analysis.billions_fed_meat_protein)
			+np.array(analysis.billions_fed_seaweed_protein)
			+np.array(analysis.billions_fed_milk_protein)
			+np.array(analysis.billions_fed_SCP_protein)
			+np.array(analysis.billions_fed_GH_protein[0:len(time_months_middle)
				])
			+np.array(analysis.billions_fed_OG_protein)
			+np.array(analysis.billions_fed_fish_protein)
			+ analysis.billions_fed_h_e_meat_protein\
			+ analysis.billions_fed_h_e_milk_protein,marker='o',markersize=3,color='red', linestyle='dotted')

		ax.plot(time_months_middle,
			np.array(analysis.billions_fed_SF_fat)
			+np.array(analysis.billions_fed_meat_fat)
			+np.array(analysis.billions_fed_seaweed_fat)
			+np.array(analysis.billions_fed_milk_fat)
			+np.array(analysis.billions_fed_SCP_fat)
			+np.array(analysis.billions_fed_GH_fat)
			+np.array(analysis.billions_fed_OG_fat)
			+np.array(analysis.billions_fed_fish_fat)
			+ analysis.billions_fed_h_e_meat_fat\
			+ analysis.billions_fed_h_e_milk_fat, marker='o',markersize=3,color='green', linestyle='dashed')
		# ax2.set_ylabel('Grams per Capita per Day')
		# ax2.set_ylim([0,50])
		ax.legend(['kcals_available','protein available','fat available'],loc=1)
		
		plt.show()

	def plot_people_fed_comparison(time_months_middle,analysis):

		ls_cycler = cycler('linestyle',
							[\
							 (0,()), # solid 
							 (0,()), # solid 
							 (0,()), # solid 
							 (0, (1, 1)), # densely dotted
							 (0, (1, 1)), # densely dotted
							 (0, (1, 1)) # densely dotted
							 ]
						  )

		color_cycler = cycler('color', [plt.get_cmap('viridis')(np.floor(i%3)/3) for i in np.arange(len(ls_cycler))])

		new_cycler = color_cycler + ls_cycler
		plt.rc('axes',prop_cycle=new_cycler)
		title = "Population Fed Existing vs New Resilient Foods"
		plt.title(title)
		plt.plot(time_months_middle,
			np.array(analysis.billions_fed_SF_kcals)
			+np.array(analysis.billions_fed_meat_kcals)
			+np.array(analysis.billions_fed_milk_kcals)
			# +np.array(analysis.billions_fed_dairy_meat_kcals)
			+np.array(analysis.billions_fed_OG_kcals),marker='o',markersize=3)
		plt.plot(time_months_middle,
			np.array(analysis.billions_fed_SF_fat)
			+np.array(analysis.billions_fed_meat_fat)
			+np.array(analysis.billions_fed_milk_fat)
			# +np.array(analysis.billions_fed_dairy_meat_kcals)
			+np.array(analysis.billions_fed_OG_fat),marker='o',markersize=3)
		plt.plot(time_months_middle,
			np.array(analysis.billions_fed_SF_protein)
			+np.array(analysis.billions_fed_meat_protein)
			+np.array(analysis.billions_fed_milk_protein)
			# +np.array(analysis.billions_fed_dairy_meat_kcals)
			+np.array(analysis.billions_fed_OG_fat),marker='o',markersize=3)
		plt.plot(time_months_middle,
			+np.array(analysis.billions_fed_seaweed_kcals)
			+np.array(analysis.billions_fed_CS_kcals)
			+np.array(analysis.billions_fed_GH_kcals),marker='o',markersize=3)
		plt.plot(time_months_middle,
			+np.array(analysis.billions_fed_seaweed_fat)
			+np.array(analysis.billions_fed_GH_fat),marker='o',markersize=3)
		plt.plot(time_months_middle,
			+np.array(analysis.billions_fed_seaweed_protein)
			+np.array(analysis.billions_fed_GH_protein),marker='o',markersize=3)

		legend = [\
			'if added, Dairy+Meat+SF+OG, kcals',
			'if added, Dairy+Meat+SF+OG, fat',
			'if added, Dairy+Meat+SF+OG, protein',
			'if added, Seaweed+CS+GH, kcals',
			'if added, Seaweed+CS+GH, fat',
			'if added, Seaweed+CS+GH, protein'
			]
		plt.ylabel('billions of people')
		plt.xlabel('Months Since May Sunlight Reduction Event')
		plt.legend(legend)
		plt.show()


	def plot_seaweed(time_months_middle,analysis):
		ls_cycler = cycler('linestyle',
							[\
							 (0,()), # solid 
							 (0, (1, 1)), # densely dotted
							 (0, (1, 5)) # dotted
							 ]
						  )

		color_cycler = cycler('color', [plt.get_cmap('viridis')(i/3) for i in np.arange(3)] )

		new_cycler = color_cycler + ls_cycler
		plt.rc('axes',prop_cycle=new_cycler)

		plt.plot(time_months_middle,np.array(analysis.billions_fed_seaweed_kcals),marker='o',markersize=3)
		plt.plot(time_months_middle,np.array(analysis.billions_fed_seaweed_fat),marker='o',markersize=3)
		plt.plot(time_months_middle,np.array(analysis.billions_fed_seaweed_protein),marker='o',markersize=3)
		plt.title('Seaweed People Fed')
		plt.xlabel('Months Since May Sunlight Reduction Event')
		plt.ylabel('Billion People Fed by macronutrient')
		plt.legend(['kcals available','fat available','protein available'])
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
		plt.xlabel('Days since May Sunlight Reduction Event')
		plt.yscale('log')
		plt.show()

		plt.plot(spreadsheet_days,np.array(food_spreadsheet).cumsum()/1000*analysis.constants["SEAWEED_KCALS"]/analysis.constants["KCALS_MONTHLY"])
		plt.plot(time_days_daily,np.array(analysis.seaweed_food_produced_daily).cumsum()*analysis.constants["SEAWEED_KCALS"]/analysis.constants["KCALS_MONTHLY"])
		legend = [
			'Aron\'s Spreadsheet Food Wet Harvest Estimate',
			'Optimizer Estimate Food Wet Harvest Estimate'
			]
			
		plt.legend(legend)
		plt.xlabel('Days since May Sunlight Reduction Event')
		plt.title('Cumulative Seaweed Harvest, 1000s Tons Wet')
		# plt.yscale('log')
		plt.show()
