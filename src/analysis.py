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


	#order the variables that occur mid-month into a list of numeric values
	def makeMidMonthlyOGVars(self,crops_food_eaten,crops_food_produced,conversion,show_output):
		immediately_eaten_output=[]
		new_stored_eaten_output=[]

		#if the variable was not modeled
		if(type(crops_food_eaten[0])==type(0)):
			return [[0]*len(variables),[0]*len(variables)]  #return initial value

		if(show_output):
			print("Monthly Output for "+str(variables[0]))

		for m in range(0,self.constants['NMONTHS']):
			cf_produced = crops_food_produced[m]
			cf_eaten = crops_food_eaten[m].varValue
			if(cf_produced <= cf_eaten):
				immediately_eaten = cf_produced
				new_stored_crops_eaten = cf_eaten - cf_produced
			else: #crops_food_eaten < crops_food_produced
				immediately_eaten = cf_eaten
				new_stored_crops_eaten = 0

			immediately_eaten_output.append(immediately_eaten*conversion)
			new_stored_eaten_output.append(new_stored_crops_eaten*conversion)
			if(show_output):
				print("    Month "+str(m)+": imm eaten: "
					+ str(immediately_eaten_output[m])
					+' new stored eaten: '
					+str(new_stored_eaten_output[m]))
		print(immediately_eaten_output)
		print(new_stored_eaten_output)
		return [immediately_eaten_output,new_stored_eaten_output]

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


	#if greenhouses aren't included, these results will be zero
	def analyze_GH_results(
		self,
		greenhouse_area,
		show_output
		):

		self.billions_fed_GH_kcals = \
			np.array(greenhouse_area)*self.constants['GREENHOUSE_CALORIES'] \
			/ self.constants["KCALS_MONTHLY"]
		self.billions_fed_GH_fat= \
			np.array(greenhouse_area)*self.constants['GREENHOUSE_FAT'] \
			/ self.constants["FAT_MONTHLY"]/1e9
		self.billions_fed_GH_protein = \
			np.array(greenhouse_area)*self.constants['GREENHOUSE_PROTEIN'] \
			/ self.constants["PROTEIN_MONTHLY"]/1e9

	# #if greenhouses aren't included, these results will be zero
	# def analyze_GH_results(
	# 	self,
	# 	production_kcals_greenhouses_per_month,
	# 	production_fat_greenhouses_per_month,
	# 	production_protein_greenhouses_per_month,
	# 	show_output
	# 	):

	# 	self.billions_fed_GH_kcals = \
	# 		np.array(production_kcals_greenhouses_per_month) \
	# 		/ self.constants["KCALS_MONTHLY"]
	# 	self.billions_fed_GH_fat= \
	# 		np.array(production_fat_greenhouses_per_month) \
	# 		/ self.constants["FAT_MONTHLY"]/1e9
	# 	self.billions_fed_GH_protein = \
	# 		np.array(production_protein_greenhouses_per_month) \
	# 		/ self.constants["PROTEIN_MONTHLY"]/1e9


	#if fish aren't included, these results will be zero
	def analyze_fish_results(
		self,
		production_kcals_fish_per_month,
		production_protein_fish_per_month,
		production_fat_fish_per_month,
		show_output
		):

		self.billions_fed_fish_kcals = \
			list(np.array(production_kcals_fish_per_month) \
			/ self.constants["KCALS_MONTHLY"])

		self.billions_fed_fish_protein = \
			list(np.array(production_protein_fish_per_month) \
			/ self.constants["PROTEIN_MONTHLY"]/1e9)

		self.billions_fed_fish_fat = \
			list(np.array(production_fat_fish_per_month) \
			/ self.constants["FAT_MONTHLY"]/1e9)

	#if outdoor growing isn't included, these results will be zero
	def analyze_OG_results(
		self,
		crops_food_eaten,
		crops_food_start,
		crops_food_end,
		crops_food_produced,
		show_output
		):

		[self.billions_fed_immediate_OG_kcals,\
		self.billions_fed_new_stored_OG_kcals]\
		 = self.makeMidMonthlyOGVars(
			crops_food_eaten,
			crops_food_produced,
			self.constants["OG_FRACTION_KCALS"]/self.constants["KCALS_MONTHLY"],
			show_output
			)


		self.billions_fed_OG_kcals = self.makeMidMonthlyVars(
			crops_food_eaten,
			self.constants["OG_FRACTION_KCALS"]/self.constants["KCALS_MONTHLY"],
			show_output)

		self.billions_fed_OG_fat = self.makeMidMonthlyVars(
			crops_food_eaten,
			self.constants["OG_FRACTION_FAT"]/self.constants["FAT_MONTHLY"]/1e9,
			show_output)

		self.billions_fed_OG_protein = self.makeMidMonthlyVars(
			crops_food_eaten,
			self.constants["OG_FRACTION_PROTEIN"]/self.constants["PROTEIN_MONTHLY"]/1e9,
			show_output)

		self.billion_person_years_OG_kcals = list(np.array(crops_food_produced[0:len(crops_food_eaten)])
			* self.constants["OG_FRACTION_KCALS"]/(self.constants["KCALS_MONTHLY"]*12))

		self.billion_person_years_OG_fat = list(np.array(crops_food_produced[0:len(crops_food_eaten)])*
			self.constants["OG_FRACTION_FAT"]/(self.constants["FAT_MONTHLY"]*12)/1e9)

		self.billion_person_years_OG_protein = list(np.array(crops_food_produced[0:len(crops_food_eaten)])*
			self.constants["OG_FRACTION_PROTEIN"]/(self.constants["PROTEIN_MONTHLY"]*12)/1e9)


	#if cellulosic sugar isn't included, these results will be zero
	def analyze_CS_results(
		self,
		production_kcals_cellulosic_sugar_per_month,
		show_output
		):

		self.billions_fed_CS_kcals = \
			list(np.array(production_kcals_cellulosic_sugar_per_month) \
			/ self.constants["KCALS_MONTHLY"])


	#if methane scp isn't included, these results will be zero
	def analyze_SCP_results(
		self,
		production_kcals_scp_per_month,
		production_protein_scp_per_month,
		production_fat_scp_per_month,
		show_output
		):

		self.billions_fed_SCP_kcals = \
			list(np.array(production_kcals_scp_per_month) \
			/ self.constants["KCALS_MONTHLY"])

		self.billions_fed_SCP_protein = \
			list(np.array(production_protein_scp_per_month) \
			/ self.constants["PROTEIN_MONTHLY"]/1e9)

		self.billions_fed_SCP_fat = \
			list(np.array(production_fat_scp_per_month) \
			/ self.constants["FAT_MONTHLY"]/1e9)

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
	
		if(self.constants['ADD_NONEGG_NONDAIRY_MEAT'] and self.constants['VERBOSE']):
			print('Days non egg, non dairy meat global at start, by kcals')
			print(360*self.constants['INITIAL_NONEGG_NONDAIRY_MEAT'] 
				* self.constants['MEAT_FRACTION_KCALS']
				/ (12*self.constants['KCALS_MONTHLY']*7.9))

	#if dairy food isn't included, these results will be zero
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
		dairy_animals_1000s_midmonth = list((np.array( \
			self.dairy_animals_start_month)
			+ np.array(self.dairy_animals_end_month))/2)
		self.millions_dairy_animals_midmonth = list(np.array(dairy_animals_1000s_midmonth)/1000)

		self.billions_fed_milk_kcals = list(np.array(dairy_animals_1000s_midmonth) \
			* self.constants["MILK_KCALS_PER_1000_COWS_PER_MONTH"] \
			/ self.constants["KCALS_MONTHLY"])

		self.billions_fed_milk_fat = list(np.array(dairy_animals_1000s_midmonth)\
			* self.constants["MILK_FAT_PER_1000_COWS_PER_MONTH"] \
			/ self.constants["FAT_MONTHLY"])

		self.billions_fed_milk_protein = list(np.array(dairy_animals_1000s_midmonth) \
			* self.constants["MILK_PROTEIN_PER_1000_COWS_PER_MONTH"] \
			/ self.constants["PROTEIN_MONTHLY"])

		self.billions_fed_dairy_meat_kcals = self.makeMidMonthlyVars(
			dairy_animals_eaten,
			self.constants["KCALS_PER_1000_LARGE_ANIMALS"]
			/ self.constants["KCALS_MONTHLY"],
			show_output)

		self.billions_fed_dairy_meat_fat = self.makeMidMonthlyVars(
			dairy_animals_eaten,
			self.constants["FAT_PER_1000_LARGE_ANIMALS"]
			/ self.constants["FAT_MONTHLY"]/1e9,
			show_output)
		# quit()
		self.billions_fed_dairy_meat_protein = self.makeMidMonthlyVars(
			dairy_animals_eaten,
			self.constants["PROTEIN_PER_1000_LARGE_ANIMALS"]
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

		if(self.constants['ADD_STORED_FOOD'] and self.constants['VERBOSE']):
			print('Days stored food global at start, by kcals')
			print(360*self.constants['INITIAL_SF'] 
				* self.constants['SF_FRACTION_KCALS']
				/ (12*self.constants['KCALS_MONTHLY']*7.9))
			print('Days stored food global at start, by fat')
			print(360*self.constants['INITIAL_SF'] 
				* self.constants['SF_FRACTION_FAT']
				/ (12*self.constants['FAT_MONTHLY']*7.9e9))
			print('Days stored food global at start, by protein')
			print(360*self.constants['INITIAL_SF'] 
				* self.constants['SF_FRACTION_PROTEIN']
				/ (12*self.constants['PROTEIN_MONTHLY']*7.9e9))

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


	def analyze_results(self,model,time_months_middle):
		# np.array(self.billions_fed_GH_kcals[0:len(time_months_middle)]))
		# quit
		self.kcals_fed = np.array(self.billions_fed_SF_kcals)\
			+np.array(self.billions_fed_meat_kcals)\
			+np.array(self.billions_fed_seaweed_kcals)\
			+np.array(self.billions_fed_dairy_meat_kcals)\
			+np.array(self.billions_fed_milk_kcals)\
			+np.array(self.billions_fed_CS_kcals[0:len(time_months_middle)])\
			+np.array(self.billions_fed_SCP_kcals[0:len(time_months_middle)])\
			+np.array(self.billions_fed_GH_kcals[0:len(time_months_middle)])\
			+np.array(self.billions_fed_OG_kcals)\
			+np.array(self.billions_fed_fish_kcals[0:len(time_months_middle)])

		self.fat_fed = np.array(self.billions_fed_SF_fat)\
			+np.array(self.billions_fed_meat_fat)\
			+np.array(self.billions_fed_seaweed_fat)\
			+np.array(self.billions_fed_dairy_meat_fat)\
			+np.array(self.billions_fed_milk_fat)\
			+np.array(self.billions_fed_SCP_fat[0:len(time_months_middle)])\
			+np.array(self.billions_fed_GH_fat[0:len(time_months_middle)])\
			+np.array(self.billions_fed_OG_fat)\
			+np.array(self.billions_fed_fish_fat[0:len(time_months_middle)])\

		self.protein_fed = np.array(self.billions_fed_SF_protein)\
			+np.array(self.billions_fed_meat_protein)\
			+np.array(self.billions_fed_seaweed_protein)\
			+np.array(self.billions_fed_dairy_meat_protein)\
			+np.array(self.billions_fed_milk_protein)\
			+np.array(self.billions_fed_GH_protein[0:len(time_months_middle)])\
			+np.array(self.billions_fed_SCP_protein[0:len(time_months_middle)])\
			+np.array(self.billions_fed_OG_protein)\
			+np.array(self.billions_fed_fish_protein[0:len(time_months_middle)])\

		self.people_fed_billions=model.objective.value()
		fed = {'fat':np.round(np.min(self.fat_fed),2),'kcals':np.round(np.min(self.kcals_fed),2),'protein':np.round(np.min(self.protein_fed),2)}
		mins =  [key for key in fed if 
				all(fed[temp] >= fed[key]
				for temp in fed)]

		# printing result 
		print("Nutrients with constraining values are: " + str(mins))
		print('Estimated people fed is '+ str(self.people_fed_billions)+' billion')
		return [self.people_fed_billions,mins]
		

	#billions of kcals
	def countProduction(self,months):
		
		kcals = self.kcals_fed*self.constants['KCALS_MONTHLY']

		kcals_sum = 0
		for m in months:
			kcals_sum = kcals_sum + kcals[m-1]

		return kcals_sum

