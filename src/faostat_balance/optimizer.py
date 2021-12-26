 ################################Optimizer Model################################
 ##                                                                            #
 ##	In this model, we estimate the macronutrient production allocated optimally#
 ##  over time including models for traditional and resilient foods.           #
 ##	                                                                           #
 ###############################################################################

import os
import sys
module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
	sys.path.append(module_path)

import numpy as np
from src.constants import Constants
from src.analysis import Analyzer
from src.plotter import Plotter
from src.validate import Validator

import pulp
from pulp import LpMaximize, LpProblem, LpVariable, LpInteger

####### TO DO ###
## 	For small animals, should be able to slaughter them in less than a month (1 month baseline)
##  Cattle currently take a year to slaughter normally
##		Rate limit: all cattle in 3 months. (baseline)

class Optimizer:

	def __init__(self):
		pass

	def optimize(self,constants):

		maximize_constraints=[] #used only for validation

		constant_loader = Constants()
		# print(constants['inputs']['ADD_FISH'])
		#single valued constants = c, multi valued constants = s
		(c,s) = constant_loader.computeConstants(constants)
		# Create the model to optimize
		model = LpProblem(name="optimization_nutrition", sense=LpMaximize)

		# Initialize the variable to maximize
		z = LpVariable(name="Least_Humans_Fed_Any_Month", lowBound=0)

		# v = all variables
		v = {}
		v["z"] = z #used only for validation

		self.c = c
		self.s = s

		#### MODEL GENERATION LOOP ####
		self.time_days_monthly=[]
		self.time_days_daily=[]
		self.time_months=[]
		self.time_days_middle=[]
		self.time_months_middle=[]

		NDAYS = c["NDAYS"]
		NMONTHS = c["NMONTHS"]

		humans_fed_kcals = [0]*NMONTHS
		humans_fed_fat = [0]*NMONTHS
		humans_fed_protein = [0]*NMONTHS
		
		# spring_wheat_fraction_of_rotation= LpVariable(\
		# 	"Spring_Wheat_Fraction_Of_Rotation",\
		# 	17,33)

		# spring_barley_fraction_of_rotation= LpVariable(\
		# 	"Spring_Barley_Fraction_Of_Rotation",\
		# 	17,33)

		# potato_fraction_of_rotation= LpVariable(\
		# 	"Potato_Fraction_Of_Rotation",\
		# 	17,33)

		# rapeseed_fraction_of_rotation= LpVariable(\
		# 	"Rapeseed_Fraction_Of_Rotation",\
		# 	17,33)

		# model += (spring_wheat_fraction_of_rotation
		# 	+ spring_barley_fraction_of_rotation
		# 	+ potato_fraction_of_rotation
		# 	+ rapeseed_fraction_of_rotation == 100, \
		# 	"Crop_Rotation_Upper_Constraint")		
		v["stored_food_start"]=[0]*NMONTHS
		v["stored_food_end"]=[0]*NMONTHS
		v["stored_food_eaten"]=[0]*NMONTHS # if stored food isn't modeled, this stays zero

		v["seaweed_wet_on_farm"]=[0]*NDAYS
		v["seaweed_food_produced"]=[0]*NDAYS
		v["used_area"]=[0]*NDAYS
		v["seaweed_food_produced_monthly"]=[0]*NMONTHS

		v["crops_food_storage_no_rot"]=[0]*NMONTHS
		v["crops_food_storage_rot"]=[0]*NMONTHS
		v["crops_food_eaten_rot"]=[0]*NMONTHS
		v["crops_food_eaten_no_rot"]=[0]*NMONTHS

		v["meat_start"]=[0]*NMONTHS
		v["meat_end"]=[0]*NMONTHS
		v["meat_eaten"]=[0]*NMONTHS

		v["humans_fed_kcals"]=[0]*NMONTHS
		v["humans_fed_fat"]=[0]*NMONTHS
		v["humans_fed_protein"]=[0]*NMONTHS

		for m in range(0,self.c["NMONTHS"]):
			# if(m>0):
			# 	continue
			self.time_days_middle.append(c["DAYS_IN_MONTH"]*(m+0.5))
			self.time_days_monthly.append(c["DAYS_IN_MONTH"]*m)
			self.time_days_monthly.append(c["DAYS_IN_MONTH"]*(m+1))
			self.time_months.append(m)
			self.time_months.append(m+1)
			self.time_months_middle.append(m+0.5)

			if(c["ADD_SEAWEED"]):
				(model,v) = self.add_seaweed_to_model(model,v,m)

			if(c["ADD_OUTDOOR_GROWING"]):
				(model,v) = self.add_outdoor_crops_to_model(model,v,m)

			if(c["ADD_STORED_FOOD"]):
				(model,v) = self.add_stored_food_to_model(model,v,m)

			if(c["ADD_MEAT"]):
				(model,v) = self.add_meat_to_model(model,v,m)

			if(
				(not c["MAXIMIZE_ONLY_FOOD_AFTER_DAY_150"])
				or 
				(c["MAXIMIZE_ONLY_FOOD_AFTER_DAY_150"] and (m >= 5))#start month 5 is day 150
			):

				[model,v,maximize_constraints] = \
					self.add_objectives_to_model(model,v,m, maximize_constraints)

		obj_func = z
		# print("obj_func")
		# print(obj_func)
		model += obj_func
		# print(model)
		# print(model.variables())

		status = model.solve(pulp.PULP_CBC_CMD(fracGap=0.0001,msg=c["VERBOSE"]))
		assert(status==1)

		# print("h_e_created_fat")
		# print(h_e_created_fat)
		# print("production_fat_fish_per_m")
		# print(production_fat_fish_per_m)

		# var_values = [x for x in v.values()]
		print('pulp reports successful optimization')
		if(c['CHECK_CONSTRAINTS']):
			print('')	
			print('VALIDATION')	
			print('')	
			print('')
			Validator.checkConstraintsSatisfied(
				model,
				status,
				maximize_constraints,
				model.variables(),
				c["VERBOSE"])

		# for var in model.variables():
		# 	if("Crops_Food_Eaten_No_Rotation_During_Month_39" in var.name):
		# 		print(f"{var.name}: {var.value()*1e9/4e6/1e6}")
		# 	if("Crops_Food_Eaten_Rotation_During_Month_39" in var.name):
		# 		vv = float(var.value())*self.c["OG_ROTATION_FRACTION_KCALS"]*1e9/4e6/1e6
		# 		print(f"{var.name}: {vv}")
		# 	if("Stored_Food_Eaten_During_Month_39" in var.name):
		# 		vv = var.value()*1e9/4e6/1e6
		# 		print(f"{var.name}: {vv}")
		# variable_output=[]
		# for m in range(0,self.c['NMONTHS']):
		# 	val=v["crops_food_eaten_rot"][m]

		# 	#if something went wrong and the variable was not added for a certain month
		# 	assert(type(val) != type(0))
		# 	# if(type(val)==type(0)):
		# 	# 	variable_output.append(val*conversion)
		# 	# else:
		# 	variable_output.append(val.varValue)
		# print("variable output")
		# print(np.array(variable_output)*1e9/4e6/1e6* self.c["OG_ROTATION_FRACTION_KCALS"])
		# print(variable_output[39]*1e9/4e6/1e6* self.c["OG_ROTATION_FRACTION_KCALS"])
		

		print("excess_kcals")
		print(self.s["excess_kcals"][39]*1e9/4e6/1e6)

		# quit()
		analysis = Analyzer(c)

		show_output=False

		analysis.compute_excess_after_run(model)

		analysis.calc_fraction_OG_SF_to_humans(\
			model,
			v["crops_food_eaten_no_rot"],
			v["crops_food_eaten_rot"],
			v["stored_food_eaten"],
			s["excess_kcals"],
			s["excess_fat_used"],
			s["excess_protein_used"]
		)


		# if no stored food, will be zero
		analysis.analyze_SF_results(
			v["stored_food_eaten"],
			v["stored_food_start"],
			v["stored_food_end"],
			show_output
		)
		#extract numeric seaweed results in terms of people fed and raw tons wet
		#if seaweed not added to model, will be zero
		analysis.analyze_seaweed_results(
			v["seaweed_wet_on_farm"],
			v["used_area"],
			s["built_area"],
			v["seaweed_food_produced"],#daily
			v["seaweed_food_produced_monthly"],
			show_output
		)

		# if no cellulosic sugar, will be zero
		analysis.analyze_CS_results(
			s["production_kcals_CS_per_m"],
			show_output
		)

		# if no scp, will be zero
		analysis.analyze_SCP_results(
			s["production_kcals_scp_per_m"],
			s["production_fat_scp_per_m"],
			s["production_protein_scp_per_m"],
			show_output
		)

		# if no fish, will be zero
		analysis.analyze_fish_results(
			s["production_kcals_fish_per_m"],
			s["production_fat_fish_per_m"],
			s["production_protein_fish_per_m"],
			show_output
		)
		
		# if no greenhouses, will be zero
		analysis.analyze_GH_results(
			s["greenhouse_kcals_per_ha"],
			s["greenhouse_fat_per_ha"],
			s["greenhouse_protein_per_ha"],
			s["greenhouse_area"],
			show_output
		)

		# if no outdoor food, will be zero
		analysis.analyze_OG_results(
			v["crops_food_eaten_no_rot"],
			v["crops_food_eaten_rot"],
			v["crops_food_storage_no_rot"],
			v["crops_food_storage_rot"],
			s["crops_food_produced"],
			show_output
		)

		#if nonegg nondairy meat isn't included, these results will be zero
		analysis.analyze_meat_dairy_results(
			v["meat_start"],
			v["meat_end"],
			v["meat_eaten"],
			s["dairy_milk_kcals"],
			s["dairy_milk_fat"],
			s["dairy_milk_protein"],
			s["cattle_maintained_kcals"],
			s["cattle_maintained_fat"],
			s["cattle_maintained_protein"],
			s["h_e_meat_kcals"],
			s["h_e_meat_fat"],
			s["h_e_meat_protein"],
			s["h_e_milk_kcals"],
			s["h_e_milk_fat"],
			s["h_e_milk_protein"],
			s["h_e_balance_kcals"],
			s["h_e_balance_fat"],
			s["h_e_balance_protein"],
			show_output
		)

		analysis.analyze_results(model,self.time_months_middle)

		return [self.time_months,self.time_months_middle,analysis]



	def add_seaweed_to_model(self,model,v,m):
		sum_food_this_month=[]
		if(m > 15):
			v["seaweed_food_produced_monthly"][m] = LpVariable(name="Seaweed_Food_Produced_Monthly_"+str(m)+"_Variable", lowBound=0)
			return (model,v)

		else:
			for d in np.arange(m*self.c["DAYS_IN_MONTH"],(m+1)*self.c["DAYS_IN_MONTH"]):
				self.time_days_daily.append(d)
				v["seaweed_wet_on_farm"][d] = LpVariable("Seaweed_Wet_On_Farm_"+str(d)+"_Variable", self.c["INITIAL_SEAWEED"], self.c["MAXIMUM_DENSITY"]*self.s["built_area"][d])
				# food production (using resources)
				v["seaweed_food_produced"][d] = LpVariable(name="Seaweed_Food_Produced_During_Day_"+str(d)+"_Variable", lowBound=0)

				v["used_area"][d] = LpVariable("Used_Area_"+str(d)+"_Variable", self.c["INITIAL_AREA"],self.s["built_area"][d])

				if(d==0): #first Day
					model += (v["seaweed_wet_on_farm"][0] == self.c["INITIAL_SEAWEED"],
						"Seaweed_Wet_On_Farm_0_Constraint")
					model += (v["used_area"][0] == self.c["INITIAL_AREA"],
						"Used_Area_Day_0_Constraint")
					model += (v["seaweed_food_produced"][0] == 0,
						"Seaweed_Food_Produced_Day_0_Constraint")

				else: #later Days
					model += (v["seaweed_wet_on_farm"][d] <= v["used_area"][d]*self.c["MAXIMUM_DENSITY"])

					model += (v["seaweed_wet_on_farm"][d] == 
						v["seaweed_wet_on_farm"][d-1]*(1+self.c["inputs"]["SEAWEED_PRODUCTION_RATE"]/100.)
						- v["seaweed_food_produced"][d]
						- (v["used_area"][d]-v["used_area"][d-1])*self.c["MINIMUM_DENSITY"]*(self.c["HARVEST_LOSS"]/100),
						"Seaweed_Wet_On_Farm_"+str(d)+"_Constraint")

				sum_food_this_month.append(v["seaweed_food_produced"][d])

			v["seaweed_food_produced_monthly"][m] = LpVariable(name="Seaweed_Food_Produced_Monthly_"+str(m)+"_Variable", lowBound=0)
			

			model += (v["seaweed_food_produced_monthly"][m] == np.sum(sum_food_this_month),
				"Seaweed_Food_Produced_Monthly_"+str(m)+"_Constraint")


			return (model,v)


	#incorporate linear constraints for stored food consumption each month
	def add_stored_food_to_model(self,model,v,m):
		v["stored_food_start"][m] = LpVariable("Stored_Food_Start_Month_"+str(m)+"_Variable", 0,self.c["INITIAL_SF_KCALS"])
		v["stored_food_end"][m] = LpVariable("Stored_Food_End_Month_"+str(m)+"_Variable", 0,self.c["INITIAL_SF_KCALS"])
		v["stored_food_eaten"][m] = LpVariable("Stored_Food_Eaten_During_Month_"+str(m)+"_Variable",0,self.c["INITIAL_SF_KCALS"])
		
		if(m==0): #first Month
			model += (v["stored_food_start"][0] == self.c["INITIAL_SF_KCALS"], "Stored_Food_Start_Month_0_Constraint")
		else:
			model += (v["stored_food_start"][m] == v["stored_food_end"][m-1], "Stored_Food_Start_Month_"+str(m)+"_Constraint")

			#####helps reduce wild fluctutions in stored food #######
			if(m>0 and self.c['inputs']["STORED_FOOD_SMOOTHING"]):
				model += (v["stored_food_eaten"][m] <= v["stored_food_eaten"][m-1]*self.c["inputs"]["FLUCTUATION_LIMIT"], "Small_Change_Plus_SF_Eaten_Month_"+str(m)+"_Constraint")

				model += (v["stored_food_eaten"][m] >= v["stored_food_eaten"][m-1]*(1/self.c["inputs"]["FLUCTUATION_LIMIT"]), "Small_Change_Minus_SF_Eaten_Month_"+str(m)+"_Constraint")
				pass

		model += (v["stored_food_end"][m] == v["stored_food_start"][m] - v["stored_food_eaten"][m], "Stored_Food_End_Month_"+str(m)+"_Constraint")

		return (model,v)

	#incorporate linear constraints for stored food consumption each month
	def add_outdoor_crops_to_model(self,model,v,m):
		# crops_food_stored[m] = LpVariable("Crops_Food_Start_Month_"+str(m)+"_Variable", lowBound=0)
		# crops_food_end[m] = LpVariable("Crops_Food_End_Month_"+str(m)+"_Variable", lowBound=0)
		
		v["crops_food_storage_rot"][m] = \
			LpVariable(\
				"Crops_Food_Storage_Rotation_Month_"+str(m)+"_Variable", \
				lowBound=0)
		v["crops_food_storage_no_rot"][m] = \
			LpVariable(\
				"Crops_Food_Storage_No_Rotation_Month_"+str(m)+"_Variable",\
				lowBound=0)

		v["crops_food_eaten_rot"][m] = \
			LpVariable(\
				"Crops_Food_Eaten_Rotation_During_Month_"+str(m)+"_Variable",\
				lowBound=0\
			)
		v["crops_food_eaten_no_rot"][m] = \
			LpVariable(\
				"Crops_Food_Eaten_No_Rotation_During_Month_"+str(m)+"_Variable",\
				lowBound=0)

		if(m==0):
			
			model += (\
				v["crops_food_storage_no_rot"][m] == \
				self.s["crops_food_produced"][m]\
				 - v["crops_food_eaten_no_rot"][m],\
				"Crops_Food_Storage_No_Rotation_"+str(m)+"_Constraint"\
			)

			model += (\
				v["crops_food_storage_rot"][m] == 0,\
				"Crops_Food_Storage_Rotation_"+str(m)+"_Constraint"\
			)

			model += (\
				v["crops_food_eaten_rot"][m] == 0,\
				"Crops_Food_Eaten_Rotation_"+str(m)+"_Constraint"\
			)

		elif(m==self.c["NMONTHS"]-1):
			#haven't dealt with the case of nmonths being less than initial harvest
			assert(m>self.c["inputs"]["INITIAL_HARVEST_DURATION"])
			
			model += (\
				v["crops_food_storage_no_rot"][m] == 0,\
				"Crops_Food_No_Rotation_None_Left_"+str(m)+"_Constraint"\
			)
			
			model += (\
				v["crops_food_storage_rot"][m] == 0,\
				"Crops_Food_Rotation_None_Left_"+str(m)+"_Constraint"\
			)
			
			model += (\
				v["crops_food_storage_rot"][m] \
				== self.s["crops_food_produced"][m]\
				 - v["crops_food_eaten_rot"][m]\
				 + v["crops_food_storage_rot"][m-1],\
				"Crops_Food_Rotation_Storage_"+str(m)+"_Constraint"\
			)
			
			model += (\
				v["crops_food_storage_no_rot"][m] \
				== v["crops_food_storage_no_rot"][m-1]\
				 - v["crops_food_eaten_no_rot"][m], \
				"Crops_Food_No_Rotation_Storage_"+str(m)+"_Constraint")

		elif(m<self.c["inputs"]["INITIAL_HARVEST_DURATION"]):

			model += (\
				v["crops_food_storage_rot"][m] == 0,\
				"Crops_Food_Storage_Rotation"+str(m)+"_Constraint"\
			)

			model += (\
				v["crops_food_eaten_rot"][m] == 0,\
				"Crops_Food_Eaten_Rotation"+str(m)+"_Constraint"\
			)

			model += (\
				v["crops_food_storage_no_rot"][m] \
				== self.s["crops_food_produced"][m]\
				 - v["crops_food_eaten_no_rot"][m]\
				 + v["crops_food_storage_no_rot"][m-1],\
				"Crops_Food_Storage_No_Rotation_"+str(m)+"_Constraint"
			)

		else: # now producing rotation, but can still eat "no rotation" storage

			model += (\
				v["crops_food_storage_rot"][m] \
				== self.s["crops_food_produced"][m]\
				 - v["crops_food_eaten_rot"][m]\
				 + v["crops_food_storage_rot"][m-1],\
				"Crops_Food_Storage_Rotation_"+str(m)+"_Constraint"\
			)

			model += (\
				v["crops_food_storage_no_rot"][m] \
				== v["crops_food_storage_no_rot"][m-1]\
				 - v["crops_food_eaten_no_rot"][m],\
				"Crops_Food_Storage_No_Rotation_"+str(m)+"_Constraint")

		#the commented out block below seems pretty much equivalent, but 
		#seems to cause problems

		# if(m==0):
		# 	model += (crops_food_storage[m] == 0, "Crops_Food_Storage_"+str(m)+"_Constraint")
		# elif(m==NMONTHS-1):
		# 	model += (crops_food_storage[m] == 0, "Crops_Food_None_Left_"+str(m)+"_Constraint")
		# 	model += (crops_food_storage[m] + crops_food_produced[m] - crops_food_eaten[m] == 0, "Crops_Food_Storage_"+str(m)+"_Constraint")

		# else:
		# 	model += (crops_food_storage[m] == crops_food_produced[m-1]\
		# 		- crops_food_eaten[m-1]\
		# 		+ crops_food_storage[m-1],\
		# 		 "Crops_Food_Storage_"+str(m)+"_Constraint")


		return (model,v)

	# #incorporate greenhouse planted food tradeoff to address calories and
	# #protein requirements
	# #we already have the area for growing total food, and the productivity
	# # in terms of calories, fat, and protein per hectare
	# def add_greenhouses_to_model(self,model,v,m):
		
	# 	#Spring wheat
	# 	#Spring barley
	# 	#Potato
	# 	#Rapeseed (oil only)
	# 	# greenhouse_area

	# 	if(m==0): #first Month
	# 		model += (area_spring_wheat[m] <= 0, \
	# 			"Area_Spring_Wheat_Month_0_Constraint")
	# 		model += (area_spring_barley[m] <= 0, \
	# 			"Area_Spring_Barley_Month_0_Constraint")
	# 		model += (area_potato[m] <= 0, \
	# 			"Area_Potato_Month_0_Constraint")
	# 		model += (area_rapeseed[m] <= 0, \
	# 			"Area_Rapeseed_Month_0_Constraint")
			
	# 	else:
	# 		model += (greenhouse_food_start[m] <= greenhouse_food_end[m-1],
	# 			"Crops_Food_Start_Month_"+str(m)+"_Constraint")
	# 		model += (greenhouse_area[m] == \
	# 			area_spring_barley[m] + \
	# 			area_rapeseed[m] + \
	# 			area_potato[m] + \
	# 			area_spring_wheat[m],\
	# 			"Area_Spring_Wheat_Month_"+str(m)+"_Constraint")
	# 		model += (area_spring_barley[m] <= 0, \
	# 			"Area_Spring_Barley_Month_"+str(m)+"_Constraint")
	# 		model += (area_potato[m] <= 0, \
	# 			"Area_Potato_Month_"+str(m)+"_Constraint")
	# 		model += (area_rapeseed[m] <= 0, \
	# 			"Area_Rapeseed_Month_"+str(m)+"_Constraint")

	# 	return (model,v)

	#### LIVESTOCK: NONDAIRY MEAT, NON EGGS ####

	#assumes all meat is fed using grasslands
	#no difference in waste between carcass meat and other food sources yet
	#dairy cows and egg-laying chickens are modeled separately
	#this can be treated essentially as stored food
	#assume there's no population growth of cows

	#incorporate linear constraints for nonegg_nondairy meat consumption each month
	def add_meat_to_model(self,model,v,m):
		v["meat_start"][m] = LpVariable("Meat_Start_"+str(m)+"_Variable", 0,self.c["INITIAL_MEAT"])
		v["meat_end"][m] = LpVariable("Meat_End_"+str(m)+"_Variable", 0,self.c["INITIAL_MEAT"])
		v["meat_eaten"][m] = LpVariable("Meat_Eaten_During_Month_"+str(m)+"_Variable",0,self.c["INITIAL_MEAT"])
		
		if(m==0): #first Month
			model += (v["meat_start"][0] == self.c["INITIAL_MEAT"], "Meat_Start_Month_0_Constraint")
		else:
			model += (v["meat_start"][m] == v["meat_end"][m-1], "Meat_Start_Month_"+str(m)+"_Constraint")

			#####helps reduce wild fluctutions in meat #######
			if(m>0 and self.c['inputs']["MEAT_SMOOTHING"]):
				self.c["FLUCTUATION_LIMIT"] = self.c['inputs']["FLUCTUATION_LIMIT"]

				model += (v["meat_eaten"][m] <= v["meat_eaten"][m-1]*self.c["FLUCTUATION_LIMIT"], "Small_Change_Plus_Eaten_Month_"+str(m)+"_Constraint")
				model += (v["meat_eaten"][m] >= v["meat_eaten"][m-1]*(1/self.c["FLUCTUATION_LIMIT"]), "Small_Change_Minus_Eaten_Month_"+str(m)+"_Constraint")

		model += (v["meat_end"][m] == v["meat_start"][m] - v["meat_eaten"][m], "Meat_End_Month_"+str(m)+"_Constraint")

		if(self.c["inputs"]["IS_NUCLEAR_WINTER"]):
			model += (v["meat_eaten"][m] <= self.c["LIMIT_PER_MONTH_CULLED"], "Meat_Limit_Culled_"+str(m)+"_Constraint")

		return (model,v)

	#### LIVESTOCK: MILK, EGGS ####
	#no resources currently are used by dairy cows or chickens
	#the only trade-off is between eating their meat vs eating their milk or eggs  

	#dairy animals are all assumed to be large animals
	# def add_dairy_to_model(self,model,v,m):
	# 	dairy_animals_1000s_start[m] = LpVariable("Dairy_Animals_Start_"+str(m)+"_Variable", 0,INITIAL_MILK_COWS_THOUSANDS)
	# 	dairy_animals_1000s_end[m] = LpVariable("Dairy_Animals_End_"+str(m)+"_Variable", 0,INITIAL_MILK_COWS_THOUSANDS)
	# 	# dairy_animals_1000s_eaten[m] = LpVariable("Dairy_Animals_Eaten_During_Month_"+str(m)+"_Variable",0,INITIAL_MILK_COWS_THOUSANDS)
		
	# 	if(m==0): #first Month
	# 		model += (dairy_animals_1000s_start[0] == INITIAL_MILK_COWS_THOUSANDS, "Dairy_Animals_Start_Month_0_Constraint")
	# 	else:
	# 		model += (dairy_animals_1000s_start[m] == dairy_animals_1000s_end[m-1], 
	# 			"Dairy_Animals_Start_Month_"+str(m)+"_Constraint")


	# 	model += (dairy_animals_1000s_end[m] == dairy_animals_1000s_start[m],
	# 		# - dairy_animals_1000s_eaten[m], #(uncomment to eat dairy animals)
	# 		"Dairy_Animals_Eaten_Month_"+str(m)+"_Constraint")

	# 	v["dairy_animals_1000s_start"][m] = dairy_animals_1000s_start[m]
	# 	v["dairy_animals_1000s_end"][m] = dairy_animals_1000s_end[m]
	# 	# v["dairy_animals_1000s_eaten"][m] = dairy_animals_1000s_eatenm])

	# 	return (model,v)

	#### OBJECTIVE FUNCTIONS ####


	def add_objectives_to_model(self,model,v,m, maximize_constraints):
		#total eaten

		v["humans_fed_kcals"][m] = \
			LpVariable(name="Humans_Fed_Kcals_"+str(m)+"_Variable",lowBound=0)
		v["humans_fed_fat"][m] = \
			LpVariable(name="Humans_Fed_Fat_"+str(m)+"_Variable",lowBound=0)
		v["humans_fed_protein"][m] = \
			LpVariable(name="Humans_Fed_Protein_"+str(m)+"_Variable",lowBound=0)


		if(self.c["ADD_SEAWEED"] and self.c["LIMIT_SEAWEED_AS_PERCENT_KCALS"]):
			# after month 8, enforce maximum seaweed production to prevent 
			# a rounding error from producing full quantity of seaweed
			if(m>10): 
				model += (v["seaweed_food_produced_monthly"][m]*self.c["SEAWEED_KCALS"] == 
					(self.c["inputs"]["MAX_SEAWEED_AS_PERCENT_KCALS"]/100) \
					* (self.c["WORLD_POP"]/1e9*self.c["KCALS_MONTHLY"]),
					"Seaweed_Limit_Kcals_"+str(m)+"_Constraint")
			else:
				model += (v["seaweed_food_produced_monthly"][m]*self.c["SEAWEED_KCALS"] <= 
					(self.c["inputs"]["MAX_SEAWEED_AS_PERCENT_KCALS"]/100) \
					* (self.c["WORLD_POP"]/1e9*self.c["KCALS_MONTHLY"]),
					"Seaweed_Limit_Kcals_"+str(m)+"_Constraint")
		# line was * (v["humans_fed_kcals"][m]*self.c["KCALS_MONTHLY"]),

		

		# if(m>24):
		# 	model += (stored_food_eaten[m] == 0,
		# 		"Food_Storage_Limit_"+str(m)+"_Constraint")
		# 	# v["humans_fed_fat"][m] = humans_fed_fat[m]

		#finds billions of people fed that month per nutrient

		#stored food eaten*sf_fraction_kcals is in units billions kcals monthly
		#seaweed_food_produced_monthly*seaweed_kcals is in units billions kcals
		# kcals monthly is in units kcals
		CROPS_WASTE = 1-self.c["inputs"]["WASTE"]["CROPS"]/100
		
		model += (v["humans_fed_kcals"][m] == \
			(v["stored_food_eaten"][m]* CROPS_WASTE\
			+ v["crops_food_eaten_no_rot"][m]* CROPS_WASTE\
			+ v["crops_food_eaten_rot"][m] * self.c["OG_ROTATION_FRACTION_KCALS"]* CROPS_WASTE\
			- self.s["excess_kcals"][m]* CROPS_WASTE\
			+ v["seaweed_food_produced_monthly"][m]*self.c["SEAWEED_KCALS"]
			+ self.s["dairy_milk_kcals"][m]
			+ self.s["cattle_maintained_kcals"][m]
			+ v["meat_eaten"][m]
			+ self.s["production_kcals_CS_per_m"][m]
			+ self.s["production_kcals_scp_per_m"][m]
			+ self.s["greenhouse_area"][m]*self.s["greenhouse_kcals_per_ha"][m]
			+ self.s["production_kcals_fish_per_m"][m]
			+ self.s["h_e_created_kcals"][m]
			)/self.c["KCALS_MONTHLY"],
			"Kcals_Fed_Month_"+str(m)+"_Constraint")

		#v["stored_food_eaten"][rsraction_fat is in units thousand tons monthly
		#seaweed_food_produced_monthly*seaweed_fat is in units thousand tons monthly
		# print('excess_fat_used')
		# print(self.s['excess_fat_used'])
		if(self.c['inputs']['INCLUDE_FAT']):
			# fat monthly is in units thousand tons
			model += (v["humans_fed_fat"][m] == 
				(v["stored_food_eaten"][m]*self.c["SF_FRACTION_FAT"] \
					* CROPS_WASTE
				+ v["crops_food_eaten_no_rot"][m]\
					* self.c["OG_FRACTION_FAT"]*CROPS_WASTE\
				+ v["crops_food_eaten_rot"][m]\
					* self.c["OG_ROTATION_FRACTION_FAT"]\
					*CROPS_WASTE\
				- self.s["excess_fat_used"][m] * CROPS_WASTE\
				+ v["seaweed_food_produced_monthly"][m]*self.c["SEAWEED_FAT"]
				+ self.s["dairy_milk_fat"][m]
				+ self.s["cattle_maintained_fat"][m]
				+ v["meat_eaten"][m]*self.c["MEAT_FRACTION_FAT"]
				+ self.s["production_fat_scp_per_m"][m]
				+ self.s["greenhouse_area"][m]*self.s["greenhouse_fat_per_ha"][m]
				+ self.s["production_fat_fish_per_m"][m] \
				+ self.s["h_e_created_fat"][m])\
				/self.c["FAT_MONTHLY"]/1e9,\
				"Fat_Fed_Month_"+str(m)+"_Constraint")

		if(self.c['inputs']['INCLUDE_PROTEIN']):

			model += (v["humans_fed_protein"][m] == 
				(v["stored_food_eaten"][m]*self.c["SF_FRACTION_PROTEIN"]\
					* CROPS_WASTE
				+ v["crops_food_eaten_no_rot"][m]\
					* self.c["OG_FRACTION_PROTEIN"] * CROPS_WASTE\
				+ v["crops_food_eaten_rot"][m]\
					* self.c["OG_ROTATION_FRACTION_PROTEIN"]*CROPS_WASTE\
				- self.s["excess_protein_used"][m] * CROPS_WASTE
				+ v["seaweed_food_produced_monthly"][m]*self.c["SEAWEED_PROTEIN"]
				+ self.s["dairy_milk_protein"][m]
				+ self.s["cattle_maintained_protein"][m]
				+ self.s["production_protein_scp_per_m"][m]
				+ v["meat_eaten"][m]*self.c["MEAT_FRACTION_PROTEIN"]
				+ self.s["greenhouse_area"][m]*self.s["greenhouse_protein_per_ha"][m]
				+ self.s["production_protein_fish_per_m"][m]
				+ self.s["h_e_created_protein"][m])\
				/self.c["PROTEIN_MONTHLY"]/1e9,
				"Protein_Fed_Month_"+str(m)+"_Constraint")

		# no feeding human edible maintained meat or dairy to animals or biofuels

		model += (v["stored_food_eaten"][m]\
			+v["crops_food_eaten_no_rot"][m]\
			+v["crops_food_eaten_rot"][m]\
				* self.c["OG_ROTATION_FRACTION_KCALS"]\
			>= self.s["excess_kcals"][m],
			"Excess_Kcals_Less_Than_SF_And_OG_"+str(m)+"_Constraint")

		if(self.c['inputs']['INCLUDE_FAT']):
			model += (v["stored_food_eaten"][m]*self.c["SF_FRACTION_FAT"] \
				+v["crops_food_eaten_no_rot"][m]*self.c["OG_FRACTION_FAT"]\
				+v["crops_food_eaten_rot"][m]\
					* self.c["OG_ROTATION_FRACTION_FAT"]\
				>= self.s["excess_fat_used"][m],
				"Excess_Fat_Less_Than_SF_And_OG_"+str(m)+"_Constraint")

		if(self.c['inputs']['INCLUDE_PROTEIN']):
			model += (v["stored_food_eaten"][m]*self.c["SF_FRACTION_PROTEIN"] \
				+v["crops_food_eaten_no_rot"][m]*self.c["OG_FRACTION_PROTEIN"]\
				+v["crops_food_eaten_rot"][m]\
					* self.c["OG_ROTATION_FRACTION_PROTEIN"]\
				>= self.s["excess_protein_used"][m],
				"Excess_Protein_Less_Than_SF_And_OG_"+str(m)+"_Constraint")
		
		#####helps reduce wild fluctutions in people fed #######
		# if(m>0 and self.c['inputs']['KCAL_SMOOTHING']):
		if(m>0 and self.c['inputs']['KCAL_SMOOTHING']):
			model += (v["humans_fed_kcals"][m-1] >= v["humans_fed_kcals"][m]*(1/1.05), "Small_Change_Minus_Humans_Fed_Month_"+str(m)+"_Constraint")
			# model += (v["humans_fed_kcals"][m] >= v["humans_fed_kcals"][m]*(1/self.c["inputs"]["FLUCTUATION_LIMIT"]), "Small_Change_Minus_Humans_Fed_Month_"+str(m)+"_Constraint")
			# model += (v["humans_fed_kcals"][m] <= v["humans_fed_kcals"][m]*(self.c["inputs"]["FLUCTUATION_LIMIT"]), "Small_Change_Plus_Humans_Fed_Month_"+str(m)+"_Constraint")
			model += (v["humans_fed_kcals"][m-1] <= v["humans_fed_kcals"][m]*(1.05), "Small_Change_Plus_Humans_Fed_Month_"+str(m)+"_Constraint")

		# couldn't get this to work?
		# if(m>0 and self.c['inputs']['PROTEIN_SMOOTHING'] and m < 74):
		# 	model += (v["humans_fed_protein"][m] >= v["humans_fed_protein"][m]*(1/self.c["inputs"]["FLUCTUATION_LIMIT"]), "Small_Change_Minus_Humans_Protein_Month_"+str(m)+"_Constraint")
		# 	model += (v["humans_fed_protein"][m] <= v["humans_fed_protein"][m]*(self.c["inputs"]["FLUCTUATION_LIMIT"]), "Small_Change_Plus_Humans_Protein_Month_"+str(m)+"_Constraint")


		# maximizes the minimum z value
		# We maximize the minimum humans fed from any month 
		# We therefore maximize the minimum ratio of fat per human requirement, 
		# protein per human requirement, or kcals per human requirement
		# for all months



		maximizer_string="Kcals_Fed_Month_"+str(m)+"_Objective_Constraint"
		maximize_constraints.append(maximizer_string)
		model += (v["z"] <= v["humans_fed_kcals"][m], maximizer_string)


		if(self.c['inputs']['INCLUDE_FAT']):

			maximizer_string="Fat_Fed_Month_"+str(m)+"_Objective_Constraint"
			maximize_constraints.append(maximizer_string)
			model += (v["z"] <= v["humans_fed_fat"][m], maximizer_string)

		if(self.c['inputs']['INCLUDE_PROTEIN']):
			maximizer_string="Protein_Fed_Month_"+str(m)+"_Objective_Constraint"
			maximize_constraints.append(maximizer_string)
			model += (v["z"] <= v["humans_fed_protein"][m], maximizer_string)

		return [model,v,maximize_constraints]