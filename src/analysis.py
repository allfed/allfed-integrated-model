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
			return np.array([0]*len(variables))  #return initial value

		if(show_output):
			print("Monthly Output for "+str(variables[0]))

		for m in range(0,self.constants['NMONTHS']):
			val=variables[m]
			# if(val==0)
			variable_output.append(val.varValue*conversion)
			if(show_output):
				print("    Month "+str(m)+": "+str(variable_output[m]))
		return np.array(variable_output)


	#order the variables that occur mid-month into a list of numeric values
	def makeMidMonthlyOGVars(self,crops_food_eaten,crops_food_produced,conversion,show_output):
		
		immediately_eaten_output=[]
		new_stored_eaten_output=[]
		cf_eaten_output = []
		cf_produced_output = []

		#if the variable was not modeled
		if(type(crops_food_eaten[0])==type(0)):
			return [[0]*len(crops_food_eaten),[0]*len(crops_food_eaten)]  #return initial value

		if(show_output):
			print("Monthly Output for "+str(variables[0]))

		for m in range(0,self.constants['NMONTHS']):
			cf_produced = crops_food_produced[m]
			cf_produced_output.append(cf_produced)
			
			cf_eaten = crops_food_eaten[m].varValue
			cf_eaten_output.append(cf_eaten)

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
		import matplotlib.pyplot as plt


		# plt.plot(cf_produced_output)
		# plt.title("cfpo")
		# plt.show()

		# plt.plot(cf_eaten_output)
		# plt.title("cfeo")
		# plt.show()
		# plt.plot(new_stored_eaten_output)
		# plt.title("nseo")
		# plt.show()
		# plt.plot(immediately_eaten_output)
		# plt.title("ieo")
		# plt.show()
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
		greenhouse_kcals_per_ha,
		greenhouse_protein_per_ha,
		greenhouse_fat_per_ha,
		greenhouse_area,
		show_output
		):

		# self.greenhouse_kcals_per_ha = self.makeMidMonthlyVars(
		# 	greenhouse_kcals_per_ha,
		# 	1,
		# 	show_output)
		# self.greenhouse_fat_per_ha = self.makeMidMonthlyVars(
		# 	greenhouse_fat_per_ha,
		# 	1,
		# 	show_output)
		# self.greenhouse_protein_per_ha = self.makeMidMonthlyVars(
		# 	greenhouse_protein_per_ha,
		# 	1,
		# 	show_output)
		self.billions_fed_GH_kcals = \
			np.multiply(np.multiply(\
				np.array(greenhouse_area),\
				np.array(greenhouse_kcals_per_ha) \
				* 1/self.constants["KCALS_MONTHLY"]
			),self.h_e_fraction_kcals_fed_to_humans)

		self.billions_fed_GH_fat= \
			np.multiply(np.multiply(
				np.array(greenhouse_area),\
				np.array(greenhouse_fat_per_ha) \
				*1/self.constants["FAT_MONTHLY"]/1e9
			),self.h_e_fraction_fat_fed_to_humans)

		self.billions_fed_GH_protein = \
			np.multiply(np.multiply(
				np.array(greenhouse_area),\
				np.array(greenhouse_protein_per_ha)
				* 1/self.constants["PROTEIN_MONTHLY"]/1e9
			),self.h_e_fraction_protein_fed_to_humans)

	# #if greenhouses aren't included, these results will be zero
	# def analyze_GH_results(
	# 	self,
	# 	production_kcals_greenhouses_per_m,
	# 	production_fat_greenhouses_per_m,
	# 	production_protein_greenhouses_per_m,
	# 	show_output
	# 	):

	# 	self.billions_fed_GH_kcals = \
	# 		np.array(production_kcals_greenhouses_per_m) \
	# 		/ self.constants["KCALS_MONTHLY"]
	# 	self.billions_fed_GH_fat= \
	# 		np.array(production_fat_greenhouses_per_m) \
	# 		/ self.constants["FAT_MONTHLY"]/1e9
	# 	self.billions_fed_GH_protein = \
	# 		np.array(production_protein_greenhouses_per_m) \
	# 		/ self.constants["PROTEIN_MONTHLY"]/1e9


	#if fish aren't included, these results will be zero
	def analyze_fish_results(
		self,
		production_kcals_fish_per_m,
		production_fat_fish_per_m,
		production_protein_fish_per_m,
		show_output
		):

		self.billions_fed_fish_kcals = \
			np.multiply(np.array(production_kcals_fish_per_m) \
			/ self.constants["KCALS_MONTHLY"]\
			,self.h_e_fraction_kcals_fed_to_humans)

		self.billions_fed_fish_protein = \
			np.multiply(np.array(production_protein_fish_per_m) \
			/ self.constants["PROTEIN_MONTHLY"]/1e9\
			,self.h_e_fraction_protein_fed_to_humans)

		self.billions_fed_fish_fat = \
			np.multiply(np.array(production_fat_fish_per_m) \
			/ self.constants["FAT_MONTHLY"]/1e9\
			,self.h_e_fraction_fat_fed_to_humans)
		
	#if outdoor growing isn't included, these results will be zero
	def analyze_OG_results(
		self,
		crops_food_eaten,
#		crops_food_start,
#		crops_food_end,
		crops_food_storage,
		crops_food_produced,
		og_rot_frac_kcals,
		og_rot_frac_fat,
		og_rot_frac_protein,
		show_output
		):
		# import matplotlib.pyplot as plt
		# plt.plot(crops_food_eaten)
		# plt.show()

		self.billions_fed_OG_storage = np.multiply(np.multiply(og_rot_frac_kcals,\
			self.makeMidMonthlyVars(
				crops_food_storage,
				1/self.constants["KCALS_MONTHLY"]\
				,
				show_output)
			),self.h_e_fraction_kcals_fed_to_humans)
		# import matplotlib.pyplot as plt
		# plt.plot(self.billions_fed_OG_storage)
		# plt.show()
		[self.billions_fed_immediate_OG_kcals_tmp,\
		self.billions_fed_new_stored_OG_kcals_tmp]\
		 = self.makeMidMonthlyOGVars(
			crops_food_eaten,
			crops_food_produced,
			1 / self.constants["KCALS_MONTHLY"],
			show_output
			)

		self.billions_fed_immediate_OG_kcals = \
			np.multiply(np.multiply(
				og_rot_frac_kcals,
				self.billions_fed_immediate_OG_kcals_tmp
			),self.h_e_fraction_kcals_fed_to_humans)
		self.billions_fed_new_stored_OG_kcals = \
			np.multiply(np.multiply(
				og_rot_frac_kcals,
				self.billions_fed_new_stored_OG_kcals_tmp
			),self.h_e_fraction_kcals_fed_to_humans)

		self.billions_fed_OG_kcals = np.multiply(np.multiply(
			og_rot_frac_kcals,
			np.array(self.makeMidMonthlyVars(
				crops_food_eaten,
				1/self.constants["KCALS_MONTHLY"],
				show_output))
			),self.h_e_fraction_kcals_fed_to_humans)


		self.billions_fed_OG_fat = np.multiply(np.multiply(
			og_rot_frac_fat,
			np.array(self.makeMidMonthlyVars(
				crops_food_eaten,
				1/self.constants["FAT_MONTHLY"]/1e9,
				show_output))\
			),self.h_e_fraction_fat_fed_to_humans)

		self.billions_fed_OG_protein = np.multiply(np.multiply(
			og_rot_frac_protein,
			np.array(self.makeMidMonthlyVars(
				crops_food_eaten,
				1/self.constants["PROTEIN_MONTHLY"]/1e9,
				show_output))
			),self.h_e_fraction_protein_fed_to_humans)

		self.billions_fed_OG_produced_kcals = \
			np.multiply(np.multiply(
				np.array(crops_food_produced[0:len(og_rot_frac_kcals)]),\
				og_rot_frac_kcals\
			) * 1 / self.constants["KCALS_MONTHLY"],self.h_e_fraction_kcals_fed_to_humans)


		self.billions_fed_OG_produced_fat = \
			np.multiply(np.multiply(
				og_rot_frac_fat,
				np.array(crops_food_produced[0:len(og_rot_frac_fat)])
			) / self.constants["FAT_MONTHLY"] / 1e9,self.h_e_fraction_fat_fed_to_humans)

		self.billions_fed_OG_produced_protein = \
			np.multiply(np.multiply(
				og_rot_frac_protein,
				np.array(crops_food_produced[0:len(og_rot_frac_protein)])\
			) / self.constants["PROTEIN_MONTHLY"]	/ 1e9,self.h_e_fraction_protein_fed_to_humans)

		# import matplotlib.pyplot as plt
		# plt.plot(crops_food_produced)
		# plt.show()

		# self.billion_person_years_OG_kcals = list(np.array(crops_food_produced[0:len(crops_food_eaten)])
			# * og_rot_frac_kcals/(self.constants["KCALS_MONTHLY"]*12))

		# self.billion_person_years_OG_fat = list(np.array(crops_food_produced[0:len(crops_food_eaten)])*
			# self.constants["OG_ROTATION_FRACTION_FAT"]/(self.constants["FAT_MONTHLY"]*12)/1e9)

		# self.billion_person_years_OG_protein = list(np.array(crops_food_produced[0:len(crops_food_eaten)])*
			# self.constants["OG_ROTATION_FRACTION_PROTEIN"]/(self.constants["PROTEIN_MONTHLY"]*12)/1e9)


	#if cellulosic sugar isn't included, these results will be zero
	def analyze_CS_results(
		self,
		production_kcals_CS_per_m,
		show_output
		):

		self.billions_fed_CS_kcals = \
			np.multiply(np.array(production_kcals_CS_per_m) \
			/ self.constants["KCALS_MONTHLY"],self.h_e_fraction_kcals_fed_to_humans)


	#if methane scp isn't included, these results will be zero
	def analyze_SCP_results(
		self,
		production_kcals_scp_per_m,
		production_protein_scp_per_m,
		production_fat_scp_per_m,
		show_output
		):

		self.billions_fed_SCP_kcals = \
			np.multiply(np.array(production_kcals_scp_per_m) \
			/ self.constants["KCALS_MONTHLY"],self.h_e_fraction_kcals_fed_to_humans)

		self.billions_fed_SCP_fat = \
			np.multiply(np.array(production_fat_scp_per_m) \
			/ self.constants["FAT_MONTHLY"]/1e9,self.h_e_fraction_fat_fed_to_humans)

		self.billions_fed_SCP_protein = \
			np.multiply(np.array(production_protein_scp_per_m) \
			/ self.constants["PROTEIN_MONTHLY"]/1e9,self.h_e_fraction_protein_fed_to_humans)

	#if stored food isn't included, these results will be zero
	def analyze_meat_dairy_results(
		self,
		nonegg_nondairy_meat_start,
		nonegg_nondairy_meat_end,
		nonegg_nondairy_meat_eaten,
		dairy_milk_kcals,
		dairy_milk_fat,
		dairy_milk_protein,
		cattle_maintained_kcals,
		cattle_maintained_fat,
		cattle_maintained_protein,
		h_e_meat_kcals,
		h_e_meat_fat,
		h_e_meat_protein,
		h_e_milk_kcals,
		h_e_milk_fat,
		h_e_milk_protein,
		h_e_balance_kcals,
		h_e_balance_fat,
		h_e_balance_protein,
		show_output
		):

		self.billions_fed_meat_kcals_tmp = np.array(self.makeMidMonthlyVars(
			nonegg_nondairy_meat_eaten,
			self.constants["MEAT_FRACTION_KCALS"]/self.constants["KCALS_MONTHLY"],
			show_output))

		self.billions_fed_meat_kcals = np.multiply(\
			self.billions_fed_meat_kcals_tmp \
		 + np.array(cattle_maintained_kcals)\
			 / self.constants["KCALS_MONTHLY"],\
		 self.h_e_fraction_kcals_fed_to_humans) #human edible fed


		self.billions_fed_meat_fat_tmp = np.array(self.makeMidMonthlyVars(
			nonegg_nondairy_meat_eaten,
			self.constants["MEAT_FRACTION_FAT"]/self.constants["FAT_MONTHLY"]/1e9,
			show_output))

		self.billions_fed_meat_fat = np.multiply(self.billions_fed_meat_fat_tmp\
		 + np.array(cattle_maintained_fat) / self.constants["FAT_MONTHLY"]/1e9,\
		 self.h_e_fraction_fat_fed_to_humans)#human edible fed

		self.billions_fed_meat_protein_tmp = np.array(self.makeMidMonthlyVars(
			nonegg_nondairy_meat_eaten,
			self.constants["MEAT_FRACTION_PROTEIN"]\
			/self.constants["PROTEIN_MONTHLY"]/1e9,
			show_output))

		self.billions_fed_meat_protein = np.multiply(self.billions_fed_meat_protein_tmp\
		 + np.array(cattle_maintained_protein) / self.constants["PROTEIN_MONTHLY"]/1e9,\
		 self.h_e_fraction_protein_fed_to_humans)#human edible fed


		self.billions_fed_milk_kcals = np.multiply(np.array(dairy_milk_kcals) \
			/ self.constants["KCALS_MONTHLY"],self.h_e_fraction_kcals_fed_to_humans)

		self.billions_fed_milk_fat = np.multiply(np.array(dairy_milk_fat)\
			/ self.constants["FAT_MONTHLY"] / 1e9,self.h_e_fraction_fat_fed_to_humans)

		self.billions_fed_milk_protein = np.multiply(np.array(dairy_milk_protein)\
			/ self.constants["PROTEIN_MONTHLY"] / 1e9,self.h_e_fraction_protein_fed_to_humans)


		self.billions_fed_h_e_meat_kcals = \
			h_e_meat_kcals / self.constants["KCALS_MONTHLY"]

		self.billions_fed_h_e_meat_fat = \
			h_e_meat_fat / self.constants["FAT_MONTHLY"]/1e9

		self.billions_fed_h_e_meat_protein = \
			h_e_meat_protein / self.constants["PROTEIN_MONTHLY"]/1e9


		self.billions_fed_h_e_milk_kcals = \
			h_e_milk_kcals / self.constants["KCALS_MONTHLY"]

		self.billions_fed_h_e_milk_fat = \
			h_e_milk_fat / self.constants["FAT_MONTHLY"]/1e9

		self.billions_fed_h_e_milk_protein = \
			h_e_milk_protein / self.constants["PROTEIN_MONTHLY"]/1e9


		self.billions_fed_h_e_balance_kcals = \
			h_e_balance_kcals / self.constants["KCALS_MONTHLY"]

		self.billions_fed_h_e_balance_fat = \
			h_e_balance_fat / self.constants["FAT_MONTHLY"]/1e9

		self.billions_fed_h_e_balance_protein = \
			h_e_balance_protein / self.constants["PROTEIN_MONTHLY"]/1e9

		if(self.constants['ADD_NONEGG_NONDAIRY_MEAT'] and self.constants['VERBOSE']):
			print('Days non egg, non dairy meat global at start, by kcals')
			print(360*self.constants['INITIAL_NONEGG_NONDAIRY_MEAT'] 
				* self.constants['MEAT_FRACTION_KCALS']
				/ (12*self.constants['KCALS_MONTHLY']))

	#if stored food isn't included, these results will be zero
	def analyze_SF_results(
		self,
		stored_food_eaten,
		stored_food_start,
		stored_food_end,
		show_output
		):



		self.billions_fed_SF_kcals = np.multiply(self.makeMidMonthlyVars(
			stored_food_eaten,
			self.constants["SF_FRACTION_KCALS"]/self.constants["KCALS_MONTHLY"],
			show_output),self.h_e_fraction_kcals_fed_to_humans)


		# self.billion_person_years_SF_kcals = self.makeStartEndMonthlyVars(
		# 	stored_food_start,
		# 	stored_food_end,
		# 	self.constants["SF_FRACTION_KCALS"]/(self.constants["KCALS_MONTHLY"]*12)*(1-self.constants["inputs"]["H_E_FRACTION_USED_FOR_FEED"]),
		# 	show_output)

		self.billions_fed_SF_fat = np.multiply(self.makeMidMonthlyVars(
			stored_food_eaten,
			self.constants["SF_FRACTION_FAT"]/self.constants["FAT_MONTHLY"]/1e9,
			show_output),self.h_e_fraction_fat_fed_to_humans)

		# self.billion_person_years_SF_fat = self.makeStartEndMonthlyVars(
		# 	stored_food_start,
		# 	stored_food_end,
		# 	self.constants["SF_FRACTION_FAT"]/(self.constants["FAT_MONTHLY"]*12)/1e9*(1-self.constants["inputs"]["H_E_FRACTION_USED_FOR_FEED"]),
		# 	show_output)
	
		self.billions_fed_SF_protein = np.multiply(self.makeMidMonthlyVars(
			stored_food_eaten,
			self.constants["SF_FRACTION_PROTEIN"]/self.constants["PROTEIN_MONTHLY"]/1e9,
			show_output),self.h_e_fraction_protein_fed_to_humans)

		# self.billion_person_years_SF_protein = self.makeStartEndMonthlyVars(
		# 	stored_food_start,
		# 	stored_food_end,
		# 	self.constants["SF_FRACTION_PROTEIN"]/(self.constants["PROTEIN_MONTHLY"]*12)/1e9*(1-self.constants["inputs"]["H_E_FRACTION_USED_FOR_FEED"],
		# 	show_output)

		if(self.constants['ADD_STORED_FOOD'] and self.constants['VERBOSE']):
			print('Days stored food global at start, by kcals')
			print(360*self.constants['INITIAL_SF'] 
				* self.constants['SF_FRACTION_KCALS']
				/ (12*self.constants["KCALS_MONTHLY"]))
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

		# self.seaweed_wet_on_farm = self.makeDailyVars(
		# 	seaweed_wet_on_farm,
		# 	1,
		# 	show_output)

		# self.seaweed_used_area = self.makeDailyVars(
		# 	used_area,
		# 	1,
		# 	show_output)

		self.seaweed_built_area = built_area
		self.seaweed_built_area_max_density = np.array(built_area)*self.constants['MAXIMUM_DENSITY']

		# self.seaweed_loss = np.append([0],
		# 		np.diff(self.seaweed_used_area)
		# 		* self.constants["MINIMUM_DENSITY"]
		# 		* (self.constants["HARVEST_LOSS"]/100))
		# self.seaweed_food_produced_daily = self.makeDailyVars(
		# 	seaweed_food_produced,
		# 	1,
		# 	show_output)

		self.seaweed_food_produced_monthly = self.makeMidMonthlyVars(
			seaweed_food_produced_monthly,
			1,
			show_output)

		self.billions_fed_seaweed_kcals = np.multiply(self.makeMidMonthlyVars(
			seaweed_food_produced_monthly,
			self.constants["SEAWEED_KCALS"]/self.constants["KCALS_MONTHLY"],
			show_output),self.h_e_fraction_kcals_fed_to_humans)

		self.billions_fed_seaweed_fat = np.multiply(self.makeMidMonthlyVars(
			seaweed_food_produced_monthly,
			self.constants["SEAWEED_FAT"]/self.constants["FAT_MONTHLY"]/1e9,
			show_output),self.h_e_fraction_fat_fed_to_humans)

		self.billions_fed_seaweed_protein = np.multiply(self.makeMidMonthlyVars(
			seaweed_food_produced_monthly,
			self.constants["SEAWEED_PROTEIN"]/self.constants["PROTEIN_MONTHLY"]/1e9,
			show_output),self.h_e_fraction_protein_fed_to_humans)


		# self.max_seaweed = self.constants['MAXIMUM_AREA'] * self.constants['MAXIMUM_DENSITY']
		# self.seaweed_used_area_max_density = np.array(self.seaweed_used_area) * self.constants['MAXIMUM_DENSITY']


	def calc_fraction_h_e_used_for_feed(
		self,
		model,
		h_e_meat_kcals,
		h_e_meat_fat,
		h_e_meat_protein,
		h_e_milk_kcals,
		h_e_milk_fat,
		h_e_milk_protein,
		excess_calories,
		excess_fat_used,
		excess_protein_used
		):

		# I spent like five hours trying to figure out why the answer was wrong 
		# until I finally found an issue with string ordering, fixed it below

		humans_fed_kcals = []
		humans_fed_fat = []
		humans_fed_protein = []
		order_kcals = []
		order_fat = []
		order_protein = []
		for var in model.variables():
			if("Humans_Fed_Kcals_" in var.name):
				humans_fed_kcals.append(var.value())
				order_kcals.append(\
					int(var.name[len("Humans_Fed_Kcals_"):].split("_")[0])\
				)
			if("Humans_Fed_Fat_" in var.name):
				order_fat.append(\
					int(var.name[len("Humans_Fed_Fat_"):].split("_")[0])\
				)
				humans_fed_fat.append(var.value())
			if("Humans_Fed_Protein_" in var.name):
				order_protein.append(\
					int(var.name[len("Humans_Fed_Protein_"):].split("_")[0])\
				)
				humans_fed_protein.append(var.value())

		zipped_lists = zip(order_kcals, humans_fed_kcals)
		sorted_zipped_lists = sorted(zipped_lists)
		humans_fed_kcals = [element for _, element in sorted_zipped_lists]

		print("humans_fed_kcals[0]")
		print(humans_fed_kcals[0])
		zipped_lists = zip(order_fat, humans_fed_fat)
		sorted_zipped_lists = sorted(zipped_lists)
		humans_fed_fat = [element for _, element in sorted_zipped_lists]
		
		zipped_lists = zip(order_protein, humans_fed_protein)
		sorted_zipped_lists = sorted(zipped_lists)
		humans_fed_protein = [element for _, element in sorted_zipped_lists]
		
		assert(len(humans_fed_kcals) == len(excess_calories))
		assert(len(humans_fed_fat) == len(h_e_meat_fat))
		assert(len(humans_fed_protein) == len(h_e_meat_protein))

		"""

		each month:
			(all the sources except using human edible fed food) + (-excess provided) + (meat and dairy from human edible sources)
			=
			(all the sources except using human edible fed food)*(fraction fed to humans) + (meat and dairy from human edible sources) 
		because each month:
			1 + (-excess provided)/(all the sources except using human edible fed food)
			=
			(fraction fed to humans)
		
		so then we let

		(all the sources except using human edible fed food)*(fraction fed to humans)
		==
		(all the sources except using human edible fed food) + (-excess provided)

		it's also true

		let:
		a = all the sources except using human edible fed food
		b = excess
		c = fraction fed to humans
		d = meat and dairy from human edible sources
		e = humans actually fed from everything together

		Perhaps this (inscrutible?) algebra will be helpful to you

		a-b = a*c => c = (a-b)/a = 1-b/a

		and if:
		a+d-b=e
		a=b-d+e

		then we have

		c = 1 - b/(b-d+e)
		
		"""

		h_e_fraction_kcals_used_for_feed\
			= np.divide(\
				excess_calories,\
				excess_calories\
				 - h_e_meat_kcals\
				 - h_e_milk_kcals\
				 + np.array(humans_fed_kcals) * self.constants["KCALS_MONTHLY"]\
				)


		h_e_fraction_kcals_fed_to_humans = 1 - h_e_fraction_kcals_used_for_feed

		h_e_fraction_fat_used_for_feed\
			= np.divide(\
				excess_fat_used,\
				excess_fat_used\
				 - h_e_meat_fat\
				 - h_e_milk_fat\
				 + np.array(humans_fed_fat)\
					 * self.constants["FAT_MONTHLY"]\
					 * 1e9\
				)

		h_e_fraction_fat_fed_to_humans = 1 - h_e_fraction_fat_used_for_feed
			
		h_e_fraction_protein_used_for_feed\
			= np.divide(\
				excess_protein_used,\
				excess_protein_used\
				 - h_e_meat_protein\
				 - h_e_milk_protein\
				 + np.array(humans_fed_protein)\
					 * self.constants["PROTEIN_MONTHLY"]\
					 * 1e9\
				)

		h_e_fraction_protein_fed_to_humans = 1 - h_e_fraction_protein_used_for_feed

		assert((h_e_fraction_kcals_used_for_feed < 1).all())
		assert((h_e_fraction_kcals_used_for_feed >= 0).all())
		assert((h_e_fraction_fat_used_for_feed < 1).all())
		assert((h_e_fraction_fat_used_for_feed >= 0).all())
		assert((h_e_fraction_protein_used_for_feed < 1).all())
		assert((h_e_fraction_protein_used_for_feed >= 0).all())

		self.h_e_fraction_kcals_fed_to_humans = h_e_fraction_kcals_fed_to_humans
		self.h_e_fraction_fat_fed_to_humans = h_e_fraction_fat_fed_to_humans
		self.h_e_fraction_protein_fed_to_humans = h_e_fraction_protein_fed_to_humans

	def analyze_results(self,model,time_months_middle):
		self.kcals_fed = (np.array(self.billions_fed_SF_kcals)\
			+np.array(self.billions_fed_meat_kcals)\
			+np.array(self.billions_fed_seaweed_kcals)\
			+np.array(self.billions_fed_milk_kcals)\
			+np.array(self.billions_fed_CS_kcals)\
			+np.array(self.billions_fed_SCP_kcals)\
			+np.array(self.billions_fed_GH_kcals)\
			+np.array(self.billions_fed_OG_kcals)\
			+np.array(self.billions_fed_fish_kcals)\
			+ self.billions_fed_h_e_meat_kcals\
			+ self.billions_fed_h_e_milk_kcals)

		self.fat_fed = np.array(self.billions_fed_SF_fat)\
			+np.array(self.billions_fed_meat_fat)\
			+np.array(self.billions_fed_seaweed_fat)\
			+np.array(self.billions_fed_milk_fat)\
			+np.array(self.billions_fed_SCP_fat)\
			+np.array(self.billions_fed_GH_fat)\
			+np.array(self.billions_fed_OG_fat)\
			+np.array(self.billions_fed_fish_fat)\
			+ self.billions_fed_h_e_meat_fat\
			+ self.billions_fed_h_e_milk_fat

		self.protein_fed = (np.array(self.billions_fed_SF_protein)\
			+np.array(self.billions_fed_meat_protein)\
			+np.array(self.billions_fed_seaweed_protein)\
			+np.array(self.billions_fed_milk_protein)\
			+np.array(self.billions_fed_GH_protein)\
			+np.array(self.billions_fed_SCP_protein)\
			+np.array(self.billions_fed_OG_protein)\
			+np.array(self.billions_fed_fish_protein))\
			+ self.billions_fed_h_e_meat_protein\
			+ self.billions_fed_h_e_milk_protein

		sum_sources_minus_excess_minus_h_e_fed_kcals = (np.array(self.billions_fed_SF_kcals)\
			+np.array(self.billions_fed_meat_kcals)\
			+np.array(self.billions_fed_seaweed_kcals)\
			+np.array(self.billions_fed_milk_kcals)\
			+np.array(self.billions_fed_CS_kcals)\
			+np.array(self.billions_fed_SCP_kcals)\
			+np.array(self.billions_fed_GH_kcals)\
			+np.array(self.billions_fed_OG_kcals)\
			+np.array(self.billions_fed_fish_kcals)\
			)
		sum_sources_minus_excess_minus_h_e_fed_fat = (np.array(self.billions_fed_SF_fat)\
			+np.array(self.billions_fed_meat_fat)\
			+np.array(self.billions_fed_seaweed_fat)\
			+np.array(self.billions_fed_milk_fat)\
			+np.array(self.billions_fed_SCP_fat)\
			+np.array(self.billions_fed_GH_fat)\
			+np.array(self.billions_fed_OG_fat)\
			+np.array(self.billions_fed_fish_fat)\
			)
		sum_sources_minus_excess_minus_h_e_fed_protein = (np.array(self.billions_fed_SF_protein)\
			+np.array(self.billions_fed_meat_protein)\
			+np.array(self.billions_fed_seaweed_protein)\
			+np.array(self.billions_fed_milk_protein)\
			+np.array(self.billions_fed_SCP_protein)\
			+np.array(self.billions_fed_GH_protein)\
			+np.array(self.billions_fed_OG_protein)\
			+np.array(self.billions_fed_fish_protein)\
			)
		
		fractional_difference = \
			np.divide(\
				(\
					sum_sources_minus_excess_minus_h_e_fed_kcals \
					+ self.billions_fed_h_e_meat_kcals\
					+ self.billions_fed_h_e_milk_kcals\
				)\
				-\
				(\
					np.divide(\
						sum_sources_minus_excess_minus_h_e_fed_kcals,\
						self.h_e_fraction_kcals_fed_to_humans\
					)\
					+self.billions_fed_h_e_balance_kcals\
				),\
				sum_sources_minus_excess_minus_h_e_fed_kcals \
				+ self.billions_fed_h_e_meat_kcals\
				+ self.billions_fed_h_e_milk_kcals\
			)

		assert((abs(fractional_difference)<1e-6).all())
		
		fractional_difference = \
			np.divide(\
				(\
					sum_sources_minus_excess_minus_h_e_fed_fat \
					+ self.billions_fed_h_e_meat_fat\
					+ self.billions_fed_h_e_milk_fat\
				)\
				-\
				(\
					np.divide(\
						sum_sources_minus_excess_minus_h_e_fed_fat,\
						self.h_e_fraction_fat_fed_to_humans\
					)\
					+self.billions_fed_h_e_balance_fat\
				),\
				sum_sources_minus_excess_minus_h_e_fed_fat \
				+ self.billions_fed_h_e_meat_fat\
				+ self.billions_fed_h_e_milk_fat\
			)

		print(fractional_difference)
		assert((abs(fractional_difference)<1e-6).all())
		

		
		fractional_difference = \
			np.divide(\
				(\
					sum_sources_minus_excess_minus_h_e_fed_protein \
					+ self.billions_fed_h_e_meat_protein\
					+ self.billions_fed_h_e_milk_protein\
				)\
				-\
				(\
					np.divide(\
						sum_sources_minus_excess_minus_h_e_fed_protein,\
						self.h_e_fraction_protein_fed_to_humans\
					)\
					+self.billions_fed_h_e_balance_protein\
				),\
				sum_sources_minus_excess_minus_h_e_fed_protein \
				+ self.billions_fed_h_e_meat_protein\
				+ self.billions_fed_h_e_milk_protein\
			)

		assert((abs(fractional_difference)<1e-6).all())
		


		self.people_fed_billions=model.objective.value()

		fed = {'fat':np.round(np.min(self.fat_fed),2),'kcals':np.round(np.min(self.kcals_fed),2),'protein':np.round(np.min(self.protein_fed),2)}
		mins =  [key for key in fed if 
				all(fed[temp] >= fed[key]
				for temp in fed)]
		print(fed)

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