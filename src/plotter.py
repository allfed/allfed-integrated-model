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

	def plotLine(model):
		month_start_end_dates=[0,1,1,2,2,3] # line plots x axis

		fuel_varnames=["Fuel_Beginning_Month_0","Fuel_After_Month_0","Fuel_Beginning_Month_1","Fuel_After_Month_1","Fuel_Beginning_Month_2","Fuel_After_Month_2"]
		fuel=[0]*len(fuel_varnames)
		stored_food_varnames=["Stored_Food_Beginning_Month_0","Stored_Food_After_Month_0","Stored_Food_Beginning_Month_1","Stored_Food_After_Month_1","Stored_Food_Beginning_Month_2","Stored_Food_After_Month_2"]
		stored_food=[0]*len(stored_food_varnames)

		month_duration_dates=[0,1,2] # bar graphs x axis
		month_duration_dates_descriptions=['Month 0','Month 1','Month 2']
		leaf_food_produced_varnames=["Leaf_Food_Produced_During_Month_0","Leaf_Food_Produced_During_Month_1","Leaf_Food_Produced_During_Month_2"]
		leaf_food_produced=[0]*len(leaf_food_produced_varnames)
		crops_food_produced_varnames=["Crops_Food_Produced_During_Month_0","Crops_Food_Produced_During_Month_1","Crops_Food_Produced_During_Month_2"]
		crops_food_produced=[0]*len(crops_food_produced_varnames)

		stored_food_eaten_varnames=["Stored_Food_Eaten_During_Month_0","Stored_Food_Eaten_During_Month_1","Stored_Food_Eaten_During_Month_2"]
		stored_food_eaten=[0]*len(stored_food_eaten_varnames)
		leaf_food_eaten_varnames=["Leaf_Food_Eaten_During_Month_0","Leaf_Food_Eaten_During_Month_1","Leaf_Food_Eaten_During_Month_2"]
		leaf_food_eaten=[0]*len(leaf_food_eaten_varnames)
		crops_food_eaten_varnames=["Crops_Food_Eaten_During_Month_0","Crops_Food_Eaten_During_Month_1","Crops_Food_Eaten_During_Month_2"]
		crops_food_eaten=[0]*len(crops_food_eaten_varnames)

		#populate the variable names
		for var in model.variables():
			if(var.name in fuel_varnames):
				fuel_var_index=fuel_varnames.index(var.name)
				fuel[fuel_var_index]=var.value()
			if(var.name in stored_food_varnames):
				stored_food_var_index=stored_food_varnames.index(var.name)
				stored_food[stored_food_var_index]=var.value()
			if(var.name in leaf_food_produced_varnames):
				leaf_food_produced_var_index=leaf_food_produced_varnames.index(var.name)
				leaf_food_produced[leaf_food_produced_var_index]=var.value()
			if(var.name in crops_food_produced_varnames):
				crops_food_produced_var_index=crops_food_produced_varnames.index(var.name)
				crops_food_produced[crops_food_produced_var_index]=var.value()
			if(var.name in stored_food_eaten_varnames):
				stored_food_eaten_var_index=stored_food_eaten_varnames.index(var.name)
				stored_food_eaten[stored_food_eaten_var_index]=var.value()
			if(var.name in leaf_food_eaten_varnames):
				leaf_food_eaten_var_index=leaf_food_eaten_varnames.index(var.name)
				leaf_food_eaten[leaf_food_eaten_var_index]=var.value()
			if(var.name in crops_food_eaten_varnames):
				crops_food_eaten_var_index=crops_food_eaten_varnames.index(var.name)
				crops_food_eaten[crops_food_eaten_var_index]=var.value()
			
		total_food_eaten = stored_food_eaten+ leaf_food_eaten+crops_food_eaten
		total_food_produced = leaf_food_produced+crops_food_produced

		#https://matplotlib.org/stable/gallery/lines_bars_and_markers/barchart.html
		fig, ax = plt.subplots()

		X=np.arange(len(month_duration_dates))
		rects0=ax.bar(X - 0.25, stored_food_eaten, color = 'b', width = 0.25,label='Stored Food')
		rects1=ax.bar(X, leaf_food_eaten, color = 'g', width = 0.25,label='Leaf Food')
		rects2=ax.bar(X + 0.25, crops_food_eaten, color = 'r', width = 0.25,label='Crops')
		ax.set_xticks(X)
		ax.set_xticklabels(month_duration_dates_descriptions)
		ax.legend()

		ax.set_title('Food Eaten Each Month by type')
		plt.show()

		fig = plt.figure()
		plt.plot(month_start_end_dates,fuel)
		plt.plot(month_start_end_dates,stored_food)
		plt.xlabel('Month')
		plt.title('Stored Resources')
		plt.legend(['Fuel','Stored Food'])
		plt.show()

		fig = plt.figure()
		plt.plot(month_start_end_dates,fuel)
		plt.plot(month_start_end_dates,stored_food)
		plt.xlabel('Month')
		plt.title('Stored Resources')
		plt.legend(['Fuel','Stored Food'])
		plt.show()

	def plotSeaweed(model):
		month_start_end_dates=[0,1,1,2,2,3] # line plots x axis

		built_area_varnames=["Built_Area_Beginning_Month_0","Built_Area_After_Month_0","Built_Area_Beginning_Month_1","Built_Area_After_Month_1","Built_Area_Beginning_Month_2","Built_Area_After_Month_2"]
		built_area=[0]*len(built_area_varnames)
		stored_food_varnames=["Stored_Food_Beginning_Month_0","Stored_Food_After_Month_0","Stored_Food_Beginning_Month_1","Stored_Food_After_Month_1","Stored_Food_Beginning_Month_2","Stored_Food_After_Month_2"]
		stored_food=[0]*len(stored_food_varnames)

		month_duration_dates=[0,1,2] # bar graphs x axis
		month_duration_dates_descriptions=['Month 0','Month 1','Month 2']
		seaweed_food_produced_varnames=["Seaweed_Food_Produced_During_Month_0","Seaweed_Food_Produced_During_Month_1","Seaweed_Food_Produced_During_Month_2"]
		seaweed_food_produced=[0]*len(seaweed_food_produced_varnames)

		stored_food_eaten_varnames=["Stored_Food_Eaten_During_Month_0","Stored_Food_Eaten_During_Month_1","Stored_Food_Eaten_During_Month_2"]
		stored_food_eaten=[0]*len(stored_food_eaten_varnames)
		seaweed_food_eaten_varnames=["Seaweed_Food_Eaten_During_Month_0","Seaweed_Food_Eaten_During_Month_1","Seaweed_Food_Eaten_During_Month_2"]
		seaweed_food_eaten=[0]*len(seaweed_food_eaten_varnames)

		#populate the variable names
		for var in model.variables():
			if(var.name in built_area_varnames):
				built_area_var_index=built_area_varnames.index(var.name)
				built_area[built_area_var_index]=var.value()
			if(var.name in stored_food_varnames):
				stored_food_var_index=stored_food_varnames.index(var.name)
				stored_food[stored_food_var_index]=var.value()
			if(var.name in seaweed_food_produced_varnames):
				seaweed_food_produced_var_index=seaweed_food_produced_varnames.index(var.name)
				seaweed_food_produced[seaweed_food_produced_var_index]=var.value()
			if(var.name in stored_food_eaten_varnames):
				stored_food_eaten_var_index=stored_food_eaten_varnames.index(var.name)
				stored_food_eaten[stored_food_eaten_var_index]=var.value()
			if(var.name in seaweed_food_eaten_varnames):
				seaweed_food_eaten_var_index=seaweed_food_eaten_varnames.index(var.name)
				seaweed_food_eaten[seaweed_food_eaten_var_index]=var.value()
			
		total_food_eaten = stored_food_eaten+ seaweed_food_eaten
		total_food_produced = seaweed_food_produced

		#https://matplotlib.org/stable/gallery/lines_bars_and_markers/barchart.html
		fig, ax = plt.subplots()

		X=np.arange(len(month_duration_dates))
		rects0=ax.bar(X - 0.33, stored_food_eaten, color = 'b', width = 0.33,label='Stored Food')
		rects2=ax.bar(X + 0.33, seaweed_food_eaten, color = 'r', width = 0.33,label='Seaweed')
		ax.set_xticks(X)
		ax.set_xticklabels(month_duration_dates_descriptions)
		ax.legend()

		ax.set_title('Food Eaten Each Month by type')
		plt.show()

		fig = plt.figure()
		plt.plot(month_start_end_dates,built_area)
		plt.plot(month_start_end_dates,stored_food)
		plt.xlabel('Month')
		plt.title('Stored Resources')
		plt.legend(['Built_Area','Stored Food'])
		plt.show()

		fig = plt.figure()
		plt.plot(month_start_end_dates,built_area)
		plt.plot(month_start_end_dates,stored_food)
		plt.xlabel('Month')
		plt.title('Stored Resources')
		plt.legend(['Built_Area','Stored Food'])
		plt.show()

