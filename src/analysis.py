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
		# print("new_stored_eaten_output")
		# print(new_stored_eaten_output)
		# print("immediately_eaten_output")
		# print(immediately_eaten_output)

		# print(np.sum(cf_eaten_output)/sum(cf_produced_output))

		# quit()
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
		# quit()
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

		# print("greenhouse_kcals_per_ha")
		# print(greenhouse_kcals_per_ha)
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
			np.multiply(\
				np.array(greenhouse_area),\
				np.array(greenhouse_kcals_per_ha) \
				* 1/self.constants["KCALS_MONTHLY"]/self.constants["CONVERT_TO_KCALS"]
			)*(1-self.constants["inputs"]["H_E_FRACTION_USED_FOR_FEED"])

		# print("self.billions_fed_GH_kcals")
		# print(self.billions_fed_GH_kcals*self.constants["KCALS_MONTHLY"]*self.constants["CONVERT_TO_KCALS"]/(1-self.constants["inputs"]["H_E_FRACTION_USED_FOR_FEED"]))
		self.billions_fed_GH_fat= \
			np.multiply(
				np.array(greenhouse_area),\
				np.array(greenhouse_fat_per_ha) \
				*1/self.constants["FAT_MONTHLY"]/1e9
			)*(1-self.constants["inputs"]["H_E_FRACTION_USED_FOR_FEED"])

		self.billions_fed_GH_protein = \
			np.multiply(
				np.array(greenhouse_area),\
				np.array(greenhouse_protein_per_ha)
				* 1/self.constants["PROTEIN_MONTHLY"]/1e9
			)*(1-self.constants["inputs"]["H_E_FRACTION_USED_FOR_FEED"])

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
			np.array(production_kcals_fish_per_month) \
			/ self.constants["KCALS_MONTHLY"]/self.constants["CONVERT_TO_KCALS"]\
			*(1-self.constants["inputs"]["H_E_FRACTION_USED_FOR_FEED"])

		self.billions_fed_fish_protein = \
			np.array(production_protein_fish_per_month) \
			/ self.constants["PROTEIN_MONTHLY"]/1e9\
			*(1-self.constants["inputs"]["H_E_FRACTION_USED_FOR_FEED"])

		self.billions_fed_fish_fat = \
			np.array(production_fat_fish_per_month) \
			/ self.constants["FAT_MONTHLY"]/1e9\
			*(1-self.constants["inputs"]["H_E_FRACTION_USED_FOR_FEED"])

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
		# print("crops food eaten")
		# plt.plot(crops_food_eaten)
		# plt.show()

		self.billions_fed_OG_storage = np.multiply(og_rot_frac_kcals,\
			self.makeMidMonthlyVars(
				crops_food_storage,
				1/self.constants["KCALS_MONTHLY"]\
				/self.constants["CONVERT_TO_KCALS"],
				show_output)
			)*(1-self.constants["inputs"]["H_E_FRACTION_USED_FOR_FEED"])
		# import matplotlib.pyplot as plt
		# plt.plot(self.billions_fed_OG_storage)
		# plt.show()
		[self.billions_fed_immediate_OG_kcals_tmp,\
		self.billions_fed_new_stored_OG_kcals_tmp]\
		 = self.makeMidMonthlyOGVars(
			crops_food_eaten,
			crops_food_produced,
			1 / self.constants["KCALS_MONTHLY"]\
				/ self.constants["CONVERT_TO_KCALS"],
			show_output
			)

		self.billions_fed_immediate_OG_kcals = \
			np.multiply(
				og_rot_frac_kcals,
				self.billions_fed_immediate_OG_kcals_tmp
			)*(1-self.constants["inputs"]["H_E_FRACTION_USED_FOR_FEED"])
		self.billions_fed_new_stored_OG_kcals = \
			np.multiply(
				og_rot_frac_kcals,
				self.billions_fed_new_stored_OG_kcals_tmp
			)*(1-self.constants["inputs"]["H_E_FRACTION_USED_FOR_FEED"])

		self.billions_fed_OG_kcals = np.multiply(
			og_rot_frac_kcals,
			np.array(self.makeMidMonthlyVars(
				crops_food_eaten,
				1/self.constants["KCALS_MONTHLY"]\
					/ self.constants["CONVERT_TO_KCALS"],
				show_output))
			)*(1-self.constants["inputs"]["H_E_FRACTION_USED_FOR_FEED"])

		# print("billions_fed_OG_kcals")
		# print(self.billions_fed_OG_kcals)

		self.billions_fed_OG_fat = np.multiply(
			og_rot_frac_fat,
			np.array(self.makeMidMonthlyVars(
				crops_food_eaten,
				1/self.constants["FAT_MONTHLY"]/1e9,
				show_output))\
			)*(1-self.constants["inputs"]["H_E_FRACTION_USED_FOR_FEED"])

		self.billions_fed_OG_protein = np.multiply(
			og_rot_frac_protein,
			np.array(self.makeMidMonthlyVars(
				crops_food_eaten,
				1/self.constants["PROTEIN_MONTHLY"]/1e9,
				show_output))
			)*(1-self.constants["inputs"]["H_E_FRACTION_USED_FOR_FEED"])

		self.billions_fed_OG_produced_kcals = \
			np.multiply(
				np.array(crops_food_produced[0:len(og_rot_frac_kcals)]),\
				og_rot_frac_kcals\
			) * 1 / self.constants["KCALS_MONTHLY"] / self.constants["CONVERT_TO_KCALS"]*(1-self.constants["inputs"]["H_E_FRACTION_USED_FOR_FEED"])

		# print("billions_fed_OG_kcals")
		# print(self.billions_fed_OG_kcals)

		self.billions_fed_OG_produced_fat = \
			np.multiply(
				og_rot_frac_fat,
				np.array(crops_food_produced[0:len(og_rot_frac_fat)])
			) / self.constants["FAT_MONTHLY"] / 1e9*(1-self.constants["inputs"]["H_E_FRACTION_USED_FOR_FEED"])

		self.billions_fed_OG_produced_protein = \
			np.multiply(
				og_rot_frac_protein,
				np.array(crops_food_produced[0:len(og_rot_frac_protein)])\
			) / self.constants["PROTEIN_MONTHLY"]	/ 1e9*(1-self.constants["inputs"]["H_E_FRACTION_USED_FOR_FEED"])

		# print("crops_food_produced")
		# import matplotlib.pyplot as plt
		# plt.plot(crops_food_produced)
		# plt.show()
		# quit()
		# print("billions_fed_OG_produced_kcals")
		# print(self.billions_fed_OG_produced_kcals)

		# self.billion_person_years_OG_kcals = list(np.array(crops_food_produced[0:len(crops_food_eaten)])
			# * og_rot_frac_kcals/(self.constants["KCALS_MONTHLY"]*12))

		# self.billion_person_years_OG_fat = list(np.array(crops_food_produced[0:len(crops_food_eaten)])*
			# self.constants["OG_ROTATION_FRACTION_FAT"]/(self.constants["FAT_MONTHLY"]*12)/1e9)

		# self.billion_person_years_OG_protein = list(np.array(crops_food_produced[0:len(crops_food_eaten)])*
			# self.constants["OG_ROTATION_FRACTION_PROTEIN"]/(self.constants["PROTEIN_MONTHLY"]*12)/1e9)


	#if cellulosic sugar isn't included, these results will be zero
	def analyze_CS_results(
		self,
		production_kcals_cellulosic_sugar_per_month,
		show_output
		):

		self.billions_fed_CS_kcals = \
			np.array(production_kcals_cellulosic_sugar_per_month) \
			/ self.constants["KCALS_MONTHLY"]/self.constants["CONVERT_TO_KCALS"]*(1-self.constants["inputs"]["H_E_FRACTION_USED_FOR_FEED"])


	#if methane scp isn't included, these results will be zero
	def analyze_SCP_results(
		self,
		production_kcals_scp_per_month,
		production_protein_scp_per_month,
		production_fat_scp_per_month,
		show_output
		):

		self.billions_fed_SCP_kcals = \
			np.array(production_kcals_scp_per_month) \
			/ self.constants["KCALS_MONTHLY"]/self.constants["CONVERT_TO_KCALS"]*(1-self.constants["inputs"]["H_E_FRACTION_USED_FOR_FEED"])

		self.billions_fed_SCP_protein = \
			np.array(production_protein_scp_per_month) \
			/ self.constants["PROTEIN_MONTHLY"]/1e9*(1-self.constants["inputs"]["H_E_FRACTION_USED_FOR_FEED"])

		self.billions_fed_SCP_fat = \
			np.array(production_fat_scp_per_month) \
			/ self.constants["FAT_MONTHLY"]/1e9*(1-self.constants["inputs"]["H_E_FRACTION_USED_FOR_FEED"])

	#if stored food isn't included, these results will be zero
	def analyze_nonegg_nondairy_results(
		self,
		nonegg_nondairy_meat_start,
		nonegg_nondairy_meat_end,
		nonegg_nondairy_meat_eaten,
		cattle_maintained_kcals,
		cattle_maintained_fat,
		cattle_maintained_protein,
		show_output
		):

		self.billions_fed_meat_kcals_tmp = np.array(self.makeMidMonthlyVars(
			nonegg_nondairy_meat_eaten,
			self.constants["MEAT_FRACTION_KCALS"]/self.constants["KCALS_MONTHLY"]/self.constants["CONVERT_TO_KCALS"],
			show_output))

		self.billions_fed_meat_kcals = (self.billions_fed_meat_kcals_tmp \
		 + np.array(cattle_maintained_kcals[0:len(self.billions_fed_meat_kcals_tmp)])\
			 / self.constants["KCALS_MONTHLY"]\
			 / self.constants["CONVERT_TO_KCALS"]\
		 )*(1-self.constants["inputs"]["H_E_FRACTION_USED_FOR_FEED"]) #human edible fed
		# self.billion_person_years_meat_kcals = self.makeStartEndMonthlyVars(
		# 	nonegg_nondairy_meat_start,
		# 	nonegg_nondairy_meat_end,
		# 	self.constants["MEAT_FRACTION_KCALS"]/(self.*12),
		# 	show_output)

		# self.billion_person_years_meat_kcals = self.makeStartEndMonthlyVars(
		# 	nonegg_nondairy_meat_start,
		# 	nonegg_nondairy_meat_end,
		# 	self.constants["MEAT_FRACTION_KCALS"]/(self.constants["KCALS_MONTHLY"]*12),
		# 	show_output)

		self.billions_fed_meat_fat_tmp = np.array(self.makeMidMonthlyVars(
			nonegg_nondairy_meat_eaten,
			self.constants["MEAT_FRACTION_FAT"]/self.constants["FAT_MONTHLY"]/1e9,
			show_output))

		self.billions_fed_meat_fat = (self.billions_fed_meat_fat_tmp \
		 + np.array(cattle_maintained_fat) / self.constants["FAT_MONTHLY"]/1e9\
		 )*(1-self.constants["inputs"]["H_E_FRACTION_USED_FOR_FEED"])#human edible fed

		self.billions_fed_h_e_meat_kcals = self.constants["inputs"]["H_E_FED_MEAT_KCALS"]/ self.constants["KCALS_MONTHLY"]\
			 / self.constants["CONVERT_TO_KCALS"]
		# print("self.billions_fed_h_e_meat_kcals*")
		# print(self.billions_fed_h_e_meat_kcals*self.constants["KCALS_MONTHLY"]\
		# 	 * self.constants["CONVERT_TO_KCALS"])

		self.billions_fed_h_e_meat_fat = self.constants["inputs"]["H_E_FED_MEAT_FAT"]/ self.constants["FAT_MONTHLY"]/1e9
		self.billions_fed_h_e_meat_protein = self.constants["inputs"]["H_E_FED_MEAT_PROTEIN"]/ self.constants["PROTEIN_MONTHLY"]/1e9


		# self.billion_person_years_meat_fat = self.makeStartEndMonthlyVars(
		# 	nonegg_nondairy_meat_start,
		# 	nonegg_nondairy_meat_end,
		# 	self.constants["MEAT_FRACTION_FAT"]/(self.constants["FAT_MONTHLY"]*12)/1e9,
		# 	show_output)
	
		self.billions_fed_meat_protein_tmp = np.array(self.makeMidMonthlyVars(
			nonegg_nondairy_meat_eaten,
			self.constants["MEAT_FRACTION_PROTEIN"]/self.constants["PROTEIN_MONTHLY"]/1e9,
			show_output))

		self.billions_fed_meat_protein = (self.billions_fed_meat_protein_tmp\
		 + np.array(cattle_maintained_protein) / self.constants["PROTEIN_MONTHLY"]/1e9\
		 )*(1-self.constants["inputs"]["H_E_FRACTION_USED_FOR_FEED"])#human edible fed


		# self.billion_person_years_meat_protein = self.makeStartEndMonthlyVars(
		# 	nonegg_nondairy_meat_start,
		# 	nonegg_nondairy_meat_end,
		# 	self.constants["MEAT_FRACTION_PROTEIN"]/(self.constants["PROTEIN_MONTHLY"]*12)/1e9,
		# 	show_output)
	
		if(self.constants['ADD_NONEGG_NONDAIRY_MEAT'] and self.constants['VERBOSE']):
			print('Days non egg, non dairy meat global at start, by kcals')
			print(360*self.constants['INITIAL_NONEGG_NONDAIRY_MEAT'] 
				* self.constants['MEAT_FRACTION_KCALS']
				/ (12*self.constants['KCALS_MONTHLY']/self.constants["CONVERT_TO_KCALS"]))

	#if dairy food isn't included, these results will be zero
	def analyze_dairy_results(
		self,
		dairy_milk_kcals,
		dairy_milk_fat,
		dairy_milk_protein,
		show_output
		):


		# self.dairy_animals = self.makeStartEndMonthlyVars(
		# 	dairy_animals_start,
		# 	dairy_animals_end,
		# 	1,
		# 	show_output
		# )

		# self.dairy_animals_start_month = self.makeMidMonthlyVars(
		# 	dairy_animals_start,
		# 	1,
		# 	show_output
		# )

		# self.dairy_animals_end_month = self.makeMidMonthlyVars(
		# 	dairy_animals_end,
		# 	1,
		# 	show_output
		# )
		# dairy_animals_1000s_midmonth = list((np.array( \
		# 	self.dairy_animals_start_month)
		# 	+ np.array(self.dairy_animals_end_month))/2)
		# self.millions_dairy_animals_midmonth = list(np.array(dairy_animals_1000s_midmonth)/1000)

		# print("dairy_milk_kcals")
		# print(dairy_milk_kcals)
		self.billions_fed_milk_kcals = (np.array(dairy_milk_kcals) \
			/ self.constants["KCALS_MONTHLY"]/self.constants["CONVERT_TO_KCALS"])*(1-self.constants["inputs"]["H_E_FRACTION_USED_FOR_FEED"])



		self.billions_fed_milk_fat = (np.array(dairy_milk_fat)\
			/ self.constants["FAT_MONTHLY"] / 1e9)*(1-self.constants["inputs"]["H_E_FRACTION_USED_FOR_FEED"])

		# print("billions_fed_milk_kcals")
		# print("billions_fed_milk_fat")
		# print(self.billions_fed_milk_kcals)
		# print(self.billions_fed_milk_fat)
		# quit()

		self.billions_fed_milk_protein = (np.array(dairy_milk_protein)\
			/ self.constants["PROTEIN_MONTHLY"] / 1e9)*(1-self.constants["inputs"]["H_E_FRACTION_USED_FOR_FEED"])

		# self.billions_fed_dairy_meat_kcals = self.makeMidMonthlyVars(
		# 	dairy_animals_eaten,
		# 	self.constants["KCALS_PER_1000_LARGE_ANIMALS"]
		# 	/ self.constants["KCALS_MONTHLY"]/self.constants["CONVERT_TO_KCALS"],
		# 	show_output)

		# self.billions_fed_dairy_meat_fat = self.makeMidMonthlyVars(
		# 	dairy_animals_eaten,
		# 	self.constants["FAT_PER_1000_LARGE_ANIMALS"]
		# 	/ self.constants["FAT_MONTHLY"]/1e9,
		# 	show_output)
		# self.billions_fed_dairy_meat_protein = self.makeMidMonthlyVars(
		# 	dairy_animals_eaten,
		# 	self.constants["PROTEIN_PER_1000_LARGE_ANIMALS"]
		# 	/self.constants["PROTEIN_MONTHLY"]/1e9,
		# 	show_output)
	

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
			self.constants["SF_FRACTION_KCALS"]/self.constants["KCALS_MONTHLY"]/self.constants["CONVERT_TO_KCALS"]*(1-self.constants["inputs"]["H_E_FRACTION_USED_FOR_FEED"]),
			show_output)


		# self.billion_person_years_SF_kcals = self.makeStartEndMonthlyVars(
		# 	stored_food_start,
		# 	stored_food_end,
		# 	self.constants["SF_FRACTION_KCALS"]/(self.constants["KCALS_MONTHLY"]*12)*(1-self.constants["inputs"]["H_E_FRACTION_USED_FOR_FEED"]),
		# 	show_output)

		self.billions_fed_SF_fat = self.makeMidMonthlyVars(
			stored_food_eaten,
			self.constants["SF_FRACTION_FAT"]/self.constants["FAT_MONTHLY"]/1e9*(1-self.constants["inputs"]["H_E_FRACTION_USED_FOR_FEED"]),
			show_output)

		# self.billion_person_years_SF_fat = self.makeStartEndMonthlyVars(
		# 	stored_food_start,
		# 	stored_food_end,
		# 	self.constants["SF_FRACTION_FAT"]/(self.constants["FAT_MONTHLY"]*12)/1e9*(1-self.constants["inputs"]["H_E_FRACTION_USED_FOR_FEED"]),
		# 	show_output)
	
		self.billions_fed_SF_protein = self.makeMidMonthlyVars(
			stored_food_eaten,
			self.constants["SF_FRACTION_PROTEIN"]/self.constants["PROTEIN_MONTHLY"]/1e9*(1-self.constants["inputs"]["H_E_FRACTION_USED_FOR_FEED"]),
			show_output)

		# self.billion_person_years_SF_protein = self.makeStartEndMonthlyVars(
		# 	stored_food_start,
		# 	stored_food_end,
		# 	self.constants["SF_FRACTION_PROTEIN"]/(self.constants["PROTEIN_MONTHLY"]*12)/1e9*(1-self.constants["inputs"]["H_E_FRACTION_USED_FOR_FEED"],
		# 	show_output)

		if(self.constants['ADD_STORED_FOOD'] and self.constants['VERBOSE']):
			print('Days stored food global at start, by kcals')
			print(360*self.constants['INITIAL_SF'] 
				* self.constants['SF_FRACTION_KCALS']
				/ (12*self.constants["KCALS_MONTHLY"]/self.constants["CONVERT_TO_KCALS"]))
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

		self.billions_fed_seaweed_kcals = self.makeMidMonthlyVars(
			seaweed_food_produced_monthly,
			self.constants["SEAWEED_KCALS"]/self.constants["KCALS_MONTHLY"]/self.constants["CONVERT_TO_KCALS"]*(1-self.constants["inputs"]["H_E_FRACTION_USED_FOR_FEED"]),
			show_output)
		# print("seaweed kcals")
		# print(np.array(self.billions_fed_seaweed_kcals)*self.constants["KCALS_MONTHLY"]*self.constants["CONVERT_TO_KCALS"])

		self.billions_fed_seaweed_fat = self.makeMidMonthlyVars(
			seaweed_food_produced_monthly,
			self.constants["SEAWEED_FAT"]/self.constants["FAT_MONTHLY"]/1e9*(1-self.constants["inputs"]["H_E_FRACTION_USED_FOR_FEED"]),
			show_output)

		self.billions_fed_seaweed_protein = self.makeMidMonthlyVars(
			seaweed_food_produced_monthly,
			self.constants["SEAWEED_PROTEIN"]/self.constants["PROTEIN_MONTHLY"]/1e9*(1-self.constants["inputs"]["H_E_FRACTION_USED_FOR_FEED"]),
			show_output)
		# print("billions_fed_seaweed_kcals")
		# print("billions_fed_seaweed_fat")
		# print(self.billions_fed_seaweed_kcals)
		# print(self.billions_fed_seaweed_fat)


		# self.max_seaweed = self.constants['MAXIMUM_AREA'] * self.constants['MAXIMUM_DENSITY']
		# self.seaweed_used_area_max_density = np.array(self.seaweed_used_area) * self.constants['MAXIMUM_DENSITY']


	def analyze_results(self,model,time_months_middle):
		# np.array(self.billions_fed_GH_kcals[0:len(time_months_middle)]))
		self.kcals_fed = ((np.array(self.billions_fed_SF_kcals)\
			+np.array(self.billions_fed_meat_kcals)\
			+np.array(self.billions_fed_seaweed_kcals)\
			+np.array(self.billions_fed_milk_kcals)\
			+np.array(self.billions_fed_CS_kcals[0:len(time_months_middle)])\
			+np.array(self.billions_fed_SCP_kcals[0:len(time_months_middle)])\
			+np.array(self.billions_fed_GH_kcals[0:len(time_months_middle)])\
			+np.array(self.billions_fed_OG_kcals)\
			+np.array(self.billions_fed_fish_kcals[0:len(time_months_middle)]))\
			*(1-self.constants["inputs"]["H_E_FRACTION_USED_FOR_FEED"])
			+ self.billions_fed_h_e_meat_kcals)* self.constants["CONVERT_TO_KCALS"]
			# +np.array(self.billions_fed_dairy_meat_kcals)\

		# print("SCP")
		# print(greenhouse_fat_per_ha[15])
		# print((self.billions_fed_SCP_kcals[15]*self.constants["CONVERT_TO_KCALS"]))
		# quit()
		# print("added")
		# print((self.billions_fed_GH_fat[15]))
		# print((self.billions_fed_milk_fat[15]+self.billions_fed_meat_fat[15]+self.billions_fed_SCP_fat[15]+self.billions_fed_GH_fat[15]+self.billions_fed_fish_fat[15]))

		self.fat_fed = (np.array(self.billions_fed_SF_fat)\
			+np.array(self.billions_fed_meat_fat)\
			+np.array(self.billions_fed_seaweed_fat)\
			+np.array(self.billions_fed_milk_fat)\
			+np.array(self.billions_fed_SCP_fat[0:len(time_months_middle)])\
			+np.array(self.billions_fed_GH_fat[0:len(time_months_middle)])\
			+np.array(self.billions_fed_OG_fat)\
			+np.array(self.billions_fed_fish_fat[0:len(time_months_middle)]))\
			*(1-self.constants["inputs"]["H_E_FRACTION_USED_FOR_FEED"])\
			+ self.billions_fed_h_e_meat_fat\
			# +np.array(self.billions_fed_dairy_meat_fat)\

		self.protein_fed = (np.array(self.billions_fed_SF_protein)\
			+np.array(self.billions_fed_meat_protein)\
			+np.array(self.billions_fed_seaweed_protein)\
			+np.array(self.billions_fed_milk_protein)\
			+np.array(self.billions_fed_GH_protein[0:len(time_months_middle)])\
			+np.array(self.billions_fed_SCP_protein[0:len(time_months_middle)])\
			+np.array(self.billions_fed_OG_protein)\
			+np.array(self.billions_fed_fish_protein[0:len(time_months_middle)]))\
			*(1-self.constants["inputs"]["H_E_FRACTION_USED_FOR_FEED"])\
			+ self.billions_fed_h_e_meat_protein\
			# +np.array(self.billions_fed_dairy_meat_protein)\
		print("model.objective")
		print(model.objective)

		self.people_fed_billions=model.objective.value()
		# print("self.fat_fed")
		# print(self.kcals_fed)
		# print(self.protein_fed)
		# print(self.kcals_fed)

		fed = {'fat':np.round(np.min(self.fat_fed),2),'kcals':np.round(np.min(self.kcals_fed),2),'protein':np.round(np.min(self.protein_fed),2)}
		mins =  [key for key in fed if 
				all(fed[temp] >= fed[key]
				for temp in fed)]

		# printing result 
		# print(fed)
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

	# https://docs.google.com/document/d/1HlML7ptYmRfNJjko5qMfIJJGyLRUBlnCIiEiBMr41cM/edit#heading=h.7wiajnpimw8t
	def get_meat_from_excess(self,constants,excess):
		# each unit of industrial foods, seaweed, and outdoor crops are fed
		# to pigs and chickens.
		excess_dry_cal_tons = \
		(excess*1e9) * self.constants["KCALS_MONTHLY"] / 4e6

		# constants["inputs"]["H_E_FRACTION_USED_FOR_FEED"] = \
		# 	(self.people_fed_billions*1e9 - constants["WORLD_POP"])\
		# 	/self.people_fed_billions*1e9

		assert(excess_dry_cal_tons>0)

		CHICKEN_AND_PORK_LIMIT = 250e6/12 #tons meat per month

		#dry caloric ton excess/ton meat
		CHICKEN_PORK_CONVERSION = 4.8 

		#dry caloric ton excess/ton meat
		EDIBLE_TO_CATTLE_CONVERSION = 9.8

		#monthly in dry caloric tons inedible feed
		CHICKEN_PORK_LIMIT_FOOD_USAGE = CHICKEN_AND_PORK_LIMIT\
		* CHICKEN_PORK_CONVERSION


		print("excess_dry_cal_tons")
		print(excess_dry_cal_tons)
		max_chicken_pork = excess_dry_cal_tons/CHICKEN_PORK_CONVERSION
		if(max_chicken_pork > CHICKEN_AND_PORK_LIMIT):

			# tons per month meat
			chicken_pork_maintained = CHICKEN_AND_PORK_LIMIT

			for_cattle = excess_dry_cal_tons - CHICKEN_PORK_LIMIT_FOOD_USAGE
			
			# tons per month meat
			cattle_h_e_maintained = for_cattle/EDIBLE_TO_CATTLE_CONVERSION
		else:
			# tons per month meat
			chicken_pork_maintained = max_chicken_pork
			# tons per month meat
			cattle_h_e_maintained = 0
 
		# MEAT_WASTE = constants['inputs']['WASTE']['MEAT']


		present_day_tons_per_month_cattle = 136e6/12 #million tons a month
		present_day_tons_per_month_chicken_pork = 250e6/12 #million tons a month

		ratio_maintained_cattle = cattle_h_e_maintained/present_day_tons_per_month_cattle
		assert(ratio_maintained_cattle <= 1)

		ratio_maintained_chicken_pork = chicken_pork_maintained/present_day_tons_per_month_chicken_pork
		assert(ratio_maintained_chicken_pork <= 1)

		print("ratio_maintained_chicken_pork")
		print(ratio_maintained_chicken_pork)

		#chicken pork assumed to maintain ratio between medium and small animal mass 
		small_to_medium_ratio \
			= 28.2e9*self.constants["KG_PER_SMALL_ANIMAL"] \
			/ (3.2e9*self.constants["KG_PER_MEDIUM_ANIMAL"] + 28.2e9*self.constants["KG_PER_SMALL_ANIMAL"])

		constants['inputs']['INIT_SMALL_ANIMALS']  \
			= 28.2e9*(1-ratio_maintained_chicken_pork)
			 # - (chicken_pork_maintained / KG_PER_SMALL_ANIMAL
				# 	 * small_to_medium_ratio

		constants['inputs']['INIT_MEDIUM_ANIMALS']  \
			= 3.2e9*(1-ratio_maintained_chicken_pork)
				# - (chicken_pork_maintained / KG_PER_MEDIUM_ANIMAL
				# 	* (1-small_to_medium_ratio))

		constants['inputs']['INIT_LARGE_ANIMALS']  \
			= 1.9e9*(1-ratio_maintained_cattle) 
			# - cattle_h_e_maintained/KG_PER_LARGE_ANIMAL

		LARGE_ANIMAL_KCALS_PER_KG = constants["LARGE_ANIMAL_KCALS_PER_KG"]
		LARGE_ANIMAL_FAT_PER_KG = constants["LARGE_ANIMAL_FAT_PER_KG"]
		LARGE_ANIMAL_PROTEIN_PER_KG = constants["LARGE_ANIMAL_PROTEIN_PER_KG"]
		MEDIUM_ANIMAL_KCALS_PER_KG = constants["MEDIUM_ANIMAL_KCALS_PER_KG"]
		MEDIUM_ANIMAL_FAT_PER_KG = constants["MEDIUM_ANIMAL_FAT_PER_KG"]
		MEDIUM_ANIMAL_PROTEIN_PER_KG = constants["MEDIUM_ANIMAL_PROTEIN_PER_KG"]
		SMALL_ANIMAL_KCALS_PER_KG = constants["SMALL_ANIMAL_KCALS_PER_KG"]
		SMALL_ANIMAL_FAT_PER_KG = constants["SMALL_ANIMAL_FAT_PER_KG"]
		SMALL_ANIMAL_PROTEIN_PER_KG = constants["SMALL_ANIMAL_PROTEIN_PER_KG"]
		
		MEAT_WASTE = constants['inputs']['WASTE']['MEAT']

		#billions kcals monthly
		chicken_pork_kcals = chicken_pork_maintained*1e3\
		 * (SMALL_ANIMAL_KCALS_PER_KG*small_to_medium_ratio\
			+ MEDIUM_ANIMAL_KCALS_PER_KG*(1-small_to_medium_ratio))\
		 * (1-MEAT_WASTE/100)\
		 /1e9
		
		#thousands tons monthly
		chicken_pork_fat = chicken_pork_maintained/1e3\
		 * (SMALL_ANIMAL_FAT_PER_KG*small_to_medium_ratio\
			+ MEDIUM_ANIMAL_FAT_PER_KG*(1-small_to_medium_ratio))\
		 * (1-MEAT_WASTE/100)

		#thousands tons monthly
		chicken_pork_protein = chicken_pork_maintained/1e3\
		 * (SMALL_ANIMAL_PROTEIN_PER_KG*small_to_medium_ratio\
			+ MEDIUM_ANIMAL_PROTEIN_PER_KG*(1-small_to_medium_ratio))\
		 * (1-MEAT_WASTE/100)

		#billions kcals monthly
		cattle_h_e_maintained_kcals = cattle_h_e_maintained\
		 * 1000  \
		 * LARGE_ANIMAL_KCALS_PER_KG \
		 / 1e9


		#1000s tons fat
		cattle_h_e_maintained_fat = cattle_h_e_maintained_kcals*1e9 \
		* LARGE_ANIMAL_FAT_PER_KG/LARGE_ANIMAL_KCALS_PER_KG/1e6

		#1000s tons protein
		cattle_h_e_maintained_protein = cattle_h_e_maintained_kcals*1e9 \
		* LARGE_ANIMAL_PROTEIN_PER_KG/LARGE_ANIMAL_KCALS_PER_KG/1e6
		 
		print("cattle_h_e_maintained_kcals + chicken_pork_kcals")
		print(cattle_h_e_maintained_kcals + chicken_pork_kcals)
		print(cattle_h_e_maintained_kcals )
		print(chicken_pork_kcals)

		constants["inputs"]["H_E_FED_MEAT_KCALS"] = \
			cattle_h_e_maintained_kcals + chicken_pork_kcals
		constants["inputs"]["H_E_FED_MEAT_FAT"] = \
			cattle_h_e_maintained_fat + chicken_pork_fat
		constants["inputs"]["H_E_FED_MEAT_PROTEIN"] = \
			cattle_h_e_maintained_protein + chicken_pork_protein

		return constants