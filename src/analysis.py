import os
import sys
module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
	sys.path.append(module_path)

import numpy as np

class Analyzer:
	def __init__(self,constants):
		self.constants=constants
		
	#order the variables that occur mid-month into a list of numeric values
	def makeMidMonthlyVars(self,variables,conversion,show_output):
		variable_output=[]
		#if the variable was not modeled
		if(type(variables[0])==type(0)):
			# print(len(variables))
			return [0]*len(variables)  #return initial value

		if(show_output):
			print("Monthly Output for "+str(variables[0]))

		for m in range(0,self.constants['NMONTHS']):
			val=variables[m]
			# if(val==0)
			variable_output.append(val.varValue*conversion)
			if(show_output):
				print("    Month "+str(m)+": "+str(variable_output[m]))
		return variable_output

	#order the variables that occur start and end month into list of numeric values
	def makeStartEndMonthlyVars(
		self,
		variable_start,
		variable_end,
		conversion,
		show_output):

		#if the variable was not modeled
		if(type(variable_start[0])==type(0)):
			#return initial value, all zeros
			return [0]*len(variable_start)*2 

		variable_output=[]
		if(show_output):
			print("Monthly Output for "+str(variable_start[0]))

		for m in range(0,self.constants['NMONTHS']):
			val=variable_start[m]
			variable_output.append(val.varValue*conversion)
			val=variable_end[m]
			variable_output.append(val.varValue*conversion)
			if(show_output):
				print("    End Month "+str(m)+": "+str(variable_output[m]))
		return variable_output

	def makeDailyVars(self,variables,conversion,show_output):
		variable_output=[]
		#if the variable was not modeled
		if(type(variables[0])==type(0)):
			return variables #return initial value

		if(show_output):
			print("Daily Output for "+str(variables[0]))
		for d in range(0,self.constants['NDAYS']):
			val=variables[d]
			# if(val==0)
			variable_output.append(val.varValue*conversion)
			if(show_output):
				print("    Day "+str(d)+": "+str(variable_output[d]))
		return variable_output


	#if cellulosic sugar isn't included, these results will be zero
	def analyze_CS_results(
		self,
		production_calories_cellulosic_sugar_per_month,
		show_output
		):

		self.billions_fed_CS_kcals = \
			np.array(production_calories_cellulosic_sugar_per_month) \
			/ self.constants["KCALS_MONTHLY"]

	#if stored food isn't included, these results will be zero
	def analyze_nonegg_nondairy_results(
		self,
		nonegg_nondairy_meat_start,
		nonegg_nondairy_meat_end,
		nonegg_nondairy_meat_eaten,
		show_output
		):

		self.billions_fed_meat_kcals = self.makeMidMonthlyVars(
			nonegg_nondairy_meat_eaten,
			self.constants["MEAT_FRACTION_KCALS"]/self.constants["KCALS_MONTHLY"],
			show_output)

		self.billion_person_years_meat_kcals = self.makeStartEndMonthlyVars(
			nonegg_nondairy_meat_start,
			nonegg_nondairy_meat_end,
			self.constants["MEAT_FRACTION_KCALS"]/(self.constants["KCALS_MONTHLY"]*12),
			show_output)

		self.billions_fed_meat_fat = self.makeMidMonthlyVars(
			nonegg_nondairy_meat_eaten,
			self.constants["MEAT_FRACTION_FAT"]/self.constants["FAT_MONTHLY"]/1e9,
			show_output)

		self.billion_person_years_meat_fat = self.makeStartEndMonthlyVars(
			nonegg_nondairy_meat_start,
			nonegg_nondairy_meat_end,
			self.constants["MEAT_FRACTION_FAT"]/(self.constants["FAT_MONTHLY"]*12)/1e9,
			show_output)
	
		self.billions_fed_meat_protein = self.makeMidMonthlyVars(
			nonegg_nondairy_meat_eaten,
			self.constants["MEAT_FRACTION_PROTEIN"]/self.constants["PROTEIN_MONTHLY"]/1e9,
			show_output)

		self.billion_person_years_meat_protein = self.makeStartEndMonthlyVars(
			nonegg_nondairy_meat_start,
			nonegg_nondairy_meat_end,
			self.constants["MEAT_FRACTION_PROTEIN"]/(self.constants["PROTEIN_MONTHLY"]*12)/1e9,
			show_output)
	
		if(self.constants['ADD_NONEGG_NONDAIRY_MEAT']):
			print('Days non egg, non dairy meat global at start, by kcals')
			print(360*self.constants['INITIAL_NONEGG_NONDAIRY_MEAT'] 
				* self.constants['MEAT_FRACTION_KCALS']
				/ (12*self.constants['KCALS_MONTHLY']*7.9))

	#if stored food isn't included, these results will be zero
	def analyze_dairy_results(
		self,
		dairy_animals_start,
		dairy_animals_end,
		dairy_animals_eaten,
		show_output
		):


		self.dairy_animals = self.makeStartEndMonthlyVars(
			dairy_animals_start,
			dairy_animals_end,
			1,
			show_output
		)

		self.dairy_animals_start_month = self.makeMidMonthlyVars(
			dairy_animals_start,
			1,
			show_output
		)

		self.dairy_animals_end_month = self.makeMidMonthlyVars(
			dairy_animals_end,
			1,
			show_output
		)
		dairy_animals_1000s_midmonth = (np.array( \
			self.dairy_animals_start_month)
			+ np.array(self.dairy_animals_end_month))/2
		self.millions_dairy_animals_midmonth = dairy_animals_1000s_midmonth/1000

		self.billions_fed_milk_kcals = dairy_animals_1000s_midmonth \
			* self.constants["MILK_KCALS_PER_1000_COWS_PER_MONTH"] \
			/ self.constants["KCALS_MONTHLY"]

		self.billions_fed_milk_fat = dairy_animals_1000s_midmonth \
			* self.constants["MILK_FAT_PER_1000_COWS_PER_MONTH"] \
			/ self.constants["FAT_MONTHLY"]

		self.billions_fed_milk_protein = dairy_animals_1000s_midmonth \
			* self.constants["MILK_PROTEIN_PER_1000_COWS_PER_MONTH"] \
			/ self.constants["PROTEIN_MONTHLY"]

		self.billions_fed_dairy_meat_kcals = self.makeMidMonthlyVars(
			dairy_animals_eaten,
			self.constants["KCALS_PER_1000_LARGE_ANIMALS"]
			# self.constants["MEAT_FRACTION_KCALS"]
			/ self.constants["KCALS_MONTHLY"],
			show_output)

		self.billions_fed_dairy_meat_fat = self.makeMidMonthlyVars(
			dairy_animals_eaten,
			self.constants["FAT_PER_1000_LARGE_ANIMALS"]
			# self.constants["MEAT_FRACTION_FAT"]
			/ self.constants["FAT_MONTHLY"]/1e9,
			True)
		# quit()

		self.billions_fed_dairy_meat_protein = self.makeMidMonthlyVars(
			dairy_animals_eaten,
			self.constants["PROTEIN_PER_1000_LARGE_ANIMALS"]
			# self.constants["MEAT_FRACTION_PROTEIN"]
			/self.constants["PROTEIN_MONTHLY"]/1e9,
			show_output)
	

	#if stored food isn't included, these results will be zero
	def analyze_SF_results(
		self,
		stored_food_eaten,
		stored_food_start,
		stored_food_end,
		show_output
		):

		self.billions_fed_SF_kcals = self.makeMidMonthlyVars(
			stored_food_eaten,
			self.constants["SF_FRACTION_KCALS"]/self.constants["KCALS_MONTHLY"],
			show_output)

		self.billion_person_years_SF_kcals = self.makeStartEndMonthlyVars(
			stored_food_start,
			stored_food_end,
			self.constants["SF_FRACTION_KCALS"]/(self.constants["KCALS_MONTHLY"]*12),
			show_output)

		self.billions_fed_SF_fat = self.makeMidMonthlyVars(
			stored_food_eaten,
			self.constants["SF_FRACTION_FAT"]/self.constants["FAT_MONTHLY"]/1e9,
			show_output)

		self.billion_person_years_SF_fat = self.makeStartEndMonthlyVars(
			stored_food_start,
			stored_food_end,
			self.constants["SF_FRACTION_FAT"]/(self.constants["FAT_MONTHLY"]*12)/1e9,
			show_output)
	
		self.billions_fed_SF_protein = self.makeMidMonthlyVars(
			stored_food_eaten,
			self.constants["SF_FRACTION_PROTEIN"]/self.constants["PROTEIN_MONTHLY"]/1e9,
			show_output)

		self.billion_person_years_SF_protein = self.makeStartEndMonthlyVars(
			stored_food_start,
			stored_food_end,
			self.constants["SF_FRACTION_PROTEIN"]/(self.constants["PROTEIN_MONTHLY"]*12)/1e9,
			show_output)

		if(self.constants['ADD_STORED_FOOD']):
			print('Days stored food global at start, by kcals')
			print(360*self.constants['INITIAL_SF'] 
				* self.constants['SF_FRACTION_KCALS']
				/ (12*self.constants['KCALS_MONTHLY']*7.9))

	def analyze_seaweed_results(
		self,
		seaweed_wet_on_farm,
		used_area,
		built_area,
		seaweed_food_produced,
		seaweed_food_produced_monthly,
		show_output
		):

		self.seaweed_wet_on_farm = self.makeDailyVars(
			seaweed_wet_on_farm,
			1,
			show_output)

		self.seaweed_used_area = self.makeDailyVars(
			used_area,
			1,
			show_output)

		self.seaweed_built_area = built_area
		self.seaweed_built_area_max_density = np.array(built_area)*self.constants['MAXIMUM_DENSITY']

		self.seaweed_loss = np.append([0],
				np.diff(self.seaweed_used_area)
				* self.constants["MINIMUM_DENSITY"]
				* (self.constants["HARVEST_LOSS"]/100))
		self.seaweed_food_produced_daily = self.makeDailyVars(
			seaweed_food_produced,
			1,
			show_output)

		self.seaweed_food_produced_monthly = self.makeMidMonthlyVars(
			seaweed_food_produced_monthly,
			1,
			show_output)

		self.billions_fed_seaweed_kcals = self.makeMidMonthlyVars(
			seaweed_food_produced_monthly,
			self.constants["SEAWEED_KCALS"]/self.constants["KCALS_MONTHLY"],
			show_output)

		self.billions_fed_seaweed_fat = self.makeMidMonthlyVars(
			seaweed_food_produced_monthly,
			self.constants["SEAWEED_FAT"]/self.constants["FAT_MONTHLY"]/1e9,
			show_output)

		self.billions_fed_seaweed_protein = self.makeMidMonthlyVars(
			seaweed_food_produced_monthly,
			self.constants["SEAWEED_PROTEIN"]/self.constants["PROTEIN_MONTHLY"]/1e9,
			show_output)

		self.max_seaweed = self.constants['MAXIMUM_AREA'] * self.constants['MAXIMUM_DENSITY']
		self.seaweed_used_area_max_density = np.array(self.seaweed_used_area) * self.constants['MAXIMUM_DENSITY']