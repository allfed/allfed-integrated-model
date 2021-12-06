import numpy as np
class Constants:
	def __init__(self):
		pass

	def computeConstants(self,c):
		#full months duration of simulation
		NMONTHS=c['inputs']['NMONTHS']
		DAYS_IN_MONTH=30
		NDAYS=NMONTHS*DAYS_IN_MONTH
		ADD_FISH = c['inputs']['ADD_FISH']
		ADD_SEAWEED=c['inputs']['ADD_SEAWEED']
		ADD_NONEGG_NONDAIRY_MEAT=c['inputs']['ADD_NONEGG_NONDAIRY_MEAT']
		ADD_DAIRY=c['inputs']['ADD_DAIRY']

		# eggs are lower priority than milk, so we're waiting till later to fill in data
		ADD_EGGS=False 

		ADD_STORED_FOOD=c['inputs']['ADD_STORED_FOOD']
		ADD_METHANE_SCP = c['inputs']['ADD_METHANE_SCP']
		ADD_CELLULOSIC_SUGAR = c['inputs']['ADD_CELLULOSIC_SUGAR']
		ADD_GREENHOUSES = c['inputs']['ADD_GREENHOUSES']
		ADD_OUTDOOR_GROWING = c['inputs']['ADD_OUTDOOR_GROWING']
		MAXIMIZE_ONLY_FOOD_AFTER_DAY_150=False
			# + str(MAXIMIZE_ONLY_FOOD_AFTER_DAY_150))
		LIMIT_SEAWEED_AS_PERCENT_KCALS=c['inputs']['LIMIT_SEAWEED_AS_PERCENT_KCALS']
		MAX_SEAWEED_AS_PERCENT_KCALS=c['inputs']['MAX_SEAWEED_AS_PERCENT_KCALS']#max percent of kcals from seaweed  per person

		VERBOSE = False


		#### NUTRITION PER MONTH ####

		#https://docs.google.com/spreadsheets/d/1RZqSrHNiIEuPQLtx1ebCd_kUcFvEF6Ea46xyzA5wU0s/edit#gid=1516287804

		#we will assume a 2100 kcals diet, and scale the "upper safe" nutrients
		#from the spreadsheet down to this "standard" level.
		#we also add 20% loss, according to the sorts of loss seen in this spreadsheet
		KCALS_DAILY = c['inputs']['NUTRITION']['KCALS_DAILY']
		PROTEIN_DAILY = c['inputs']['NUTRITION']['PROTEIN_DAILY']
		FAT_DAILY = c['inputs']['NUTRITION']['FAT_DAILY']

		# INTAKES={}
		# INTAKES['lower_severe']={}
		# INTAKES['lower_severe']['fat'] = 20 #grams per day
		# INTAKES['lower_severe']['protein'] = 46 #grams per day
		# INTAKES['lower_severe']['kcals'] = 1039 #per day
		# INTAKES['lower_moderate']={}
		# INTAKES['lower_moderate']['fat'] = 35 #grams per day
		# INTAKES['lower_moderate']['protein'] = 51 #grams per day
		# INTAKES['lower_moderate']['kcals'] = 1039 #per day
		WORLD_POP=7.8e9
		KCALS_MONTHLY=KCALS_DAILY*DAYS_IN_MONTH#in kcals per person
		PROTEIN_MONTHLY=PROTEIN_DAILY*DAYS_IN_MONTH/1e9# in thousands of tons
		FAT_MONTHLY=FAT_DAILY*DAYS_IN_MONTH/1e9# in thousands of tons

		KG_TO_1000_TONS=1/(1e6)

		# MILK_INIT_TONS_ANNUAL=c['inputs']['MILK_INIT_TONS_ANNUAL']
		# MILK_INIT_TONS_DRY_CALORIC_EQIVALENT=MILK_INIT_TONS_ANNUAL*1e6/12 #first month
		KCALS_PER_DRY_CALORIC_TONS=4e6



		####SEAWEED INITIAL VARIABLES####

		#use "laver" variety for now from nutrition calculator
		#https://docs.google.com/spreadsheets/d/1RZqSrHNiIEuPQLtx1ebCd_kUcFvEF6Ea46xyzA5wU0s/edit#gid=1516287804
		WET_TO_DRY_MASS_CONVERSION=1/6

		#in order, in equal parts by mass:
		# Emi-tsunomata dry
		# Irish Moss dry
		# Kelp dry
		# Laver dry
		# Wakame dry
		# Fucus vesiculosus dry
		# Fucus spiralis dry

		#kcals per kg dry
		KCALS_PER_KG = \
			(2590
			+2940
			+2580
			+2100
			+2700
			+2520
			+3100)/7

		# dry fraction mass fat		
		MASS_FRACTION_FAT_DRY = \
			(.014
			+.010
			+.034
			+.017
			+.038
			+.031
			+.020)/7

		# dry fraction mass digestible protein		
		MASS_FRACTION_PROTEIN_DRY = (\
			0.770 * 0.153
			+ 0.770 * 0.091
			+ 0.768 * 0.101
			+ 0.862 * 0.349
			+ 0.700 * 0.182
			+ 0.147 * 0.060
			+ 0.147 * 0.100)/7

		SEAWEED_WASTE = c['inputs']['WASTE']['SEAWEED']

		## seaweed billion kcals per 1000 tons wet
		# convert 1000 tons to kg 
		# convert kg to kcals
		# convert kcals to billions of kcals
		# convert wet mass seaweed to dry mass seaweed
		SEAWEED_KCALS = 1e6 * KCALS_PER_KG / 1e9 \
			* WET_TO_DRY_MASS_CONVERSION \
			* (1-SEAWEED_WASTE/100)

		## seaweed fraction digestible protein per 1000 ton wet
		SEAWEED_PROTEIN = MASS_FRACTION_PROTEIN_DRY \
			* WET_TO_DRY_MASS_CONVERSION \
			* (1-SEAWEED_WASTE/100)


		## seaweed fraction fat per 1000 tons wet
		SEAWEED_FAT = MASS_FRACTION_FAT_DRY \
			* WET_TO_DRY_MASS_CONVERSION \
			* (1-SEAWEED_WASTE/100)

		HARVEST_LOSS=c['inputs']['HARVEST_LOSS']
		INITIAL_SEAWEED=c['inputs']['INITIAL_SEAWEED']
		INITIAL_AREA=c['inputs']['INITIAL_AREA']
		NEW_AREA_PER_DAY=c['inputs']['NEW_AREA_PER_DAY']
		MAXIMUM_AREA=c['inputs']['MAXIMUM_AREA']
		SEAWEED_PRODUCTION_RATE=c['inputs']['SEAWEED_PRODUCTION_RATE']


		built_area=np.linspace(INITIAL_AREA,(NDAYS-1)*NEW_AREA_PER_DAY+INITIAL_AREA,NDAYS)
		built_area[built_area>MAXIMUM_AREA]=MAXIMUM_AREA


		#### STORED FOOD VARIABLES ####

		# (nuclear event in mid-may)
		#mike's spreadsheet: https://docs.google.com/spreadsheets/d/19kzHpux690JTCo2IX2UA1faAd7R1QcBK/edit#gid=806987252

		TONS_DRY_CALORIC_EQIVALENT_SF=c['inputs']['TONS_DRY_CALORIC_EQIVALENT_SF']
		INITIAL_SF_KCALS = KCALS_PER_DRY_CALORIC_TONS*TONS_DRY_CALORIC_EQIVALENT_SF/1e9 # billion kcals per unit mass initial

		INITIAL_SF_PROTEIN = c['inputs']['INITIAL_SF_PROTEIN'] 
		INITIAL_SF_FAT = c['inputs']['INITIAL_SF_FAT'] 



		#we need kcals from a unit of mass of stored food.
		#if the unit is mass, we know initial_sf_kcals/initial_sf_kcals is unitless 1

		SF_FRACTION_KCALS =	INITIAL_SF_KCALS \
			/ (INITIAL_SF_KCALS
				+ INITIAL_SF_PROTEIN
				+ INITIAL_SF_FAT)
		SF_FRACTION_FAT =	INITIAL_SF_FAT \
			/ (INITIAL_SF_KCALS
				+ INITIAL_SF_PROTEIN
				+ INITIAL_SF_FAT)
		SF_FRACTION_PROTEIN = INITIAL_SF_PROTEIN \
			/ (INITIAL_SF_KCALS
				+ INITIAL_SF_PROTEIN
				+ INITIAL_SF_FAT)


		SF_WASTE = c['inputs']['WASTE']['CEREALS']
		#mass initial, units don't matter, we only need to ensure we use the correct 
		#fraction of kcals, fat, and protein per unit initial stored food.
		INITIAL_SF=INITIAL_SF_KCALS/SF_FRACTION_KCALS * (1-SF_WASTE/100)


		# INITIAL_SF = 350e6*4e6/1e9

		# so INITIAL_SF = INITIAL_SF_KCALS+ INITIAL_SF_PROTEIN+ INITIAL_SF_FAT
		# and we find:  INITIAL_SF*SF_FRACTION_FAT =INITIAL_SF_FAT
		# 


		#### FISH ####


		FISH_TONS_WET_2018 = 168936.71*1e3
		FISH_KCALS_PER_TON = 1310*1e3
		FISH_PROTEIN_PER_KG = 0.0204
		FISH_FAT_PER_KG = 0.0048

		FISH_WASTE = c['inputs']['WASTE']['SEAFOOD']
		FISH_ESTIMATE = FISH_TONS_WET_2018 * (1-FISH_WASTE/100)
		#billions of kcals per month
		FISH_KCALS = FISH_ESTIMATE/12*FISH_KCALS_PER_TON/1e9
		FISH_KG_MONTHLY=FISH_ESTIMATE/12*1e3

		FISH_PROTEIN = FISH_KG_MONTHLY * FISH_PROTEIN_PER_KG / 1e6 #units of 1000s tons protein (so, value is in the hundreds of thousands of tons)
		FISH_FAT = FISH_KG_MONTHLY * FISH_FAT_PER_KG / 1e6 #units of 1000s tons fat (so, value is in the tens of thousands of tons)

		#https://assets.researchsquare.com/files/rs-830419/v1_covered.pdf?c=1631878417

		FISH_PERCENT_EACH_MONTH_LONG = list(np.array(\
			[  0.        ,  -0.90909091,  -1.81818182,  -2.72727273,
			  -3.63636364,  -4.54545455,  -5.45454545,  -6.36363636,
			  -7.27272727,  -8.18181818,  -9.09090909, -10         ,
			  \
			  -10., -12., -14., -16.,
			  -18., -20., -22., -24.,
			  -26., -28., -30., -32.,
			  \
			  -32.        , -32.27272727, -32.54545455, -32.81818182,
			  -33.09090909, -33.36363636, -33.63636364, -33.90909091,
			  -34.18181818, -34.45454545, -34.72727273, -35.        ,
			  \
			  -35.        , -34.90909091, -34.81818182, -34.72727273,
			  -34.63636364, -34.54545455, -34.45454545, -34.36363636,
			  -34.27272727, -34.18181818, -34.09090909, -34.        ,
			  \
			  -34.        , -33.90909091, -33.81818182, -33.72727273,
			  -33.63636364, -33.54545455, -33.45454545, -33.36363636,
			  -33.27272727, -33.18181818, -33.09090909, -33.        ,
			  \
			  -33.        , -32.81818182, -32.63636364, -32.45454545,
			  -32.27272727, -32.09090909, -31.90909091, -31.72727273,
			  -31.54545455, -31.36363636, -31.18181818, -31.        ,
			  \
			  -31.        , -30.90909091, -30.81818182, -30.72727273,
			  -30.63636364, -30.54545455, -30.45454545, -30.36363636,
			  -30.27272727, -30.18181818, -30.09090909, -30.        
			]) + 100)
		FISH_PERCENT_EACH_MONTH = FISH_PERCENT_EACH_MONTH_LONG[0:NMONTHS]
		if(ADD_FISH):
			production_kcals_fish_per_m = []
			production_protein_fish_per_m = []
			production_fat_fish_per_m = []
			for x in FISH_PERCENT_EACH_MONTH:
				if(c['inputs']['IS_NUCLEAR_WINTER']):				
					production_kcals_fish_per_m.append(x / 100 * FISH_KCALS)
					production_protein_fish_per_m.append(x / 100 * FISH_PROTEIN)
					production_fat_fish_per_m.append(x / 100 * FISH_FAT)
				else:
					production_kcals_fish_per_m.append(FISH_KCALS)
					production_protein_fish_per_m.append(FISH_PROTEIN)
					production_fat_fish_per_m.append(FISH_FAT)					
		else:
			production_kcals_fish_per_m=[0]*len(FISH_PERCENT_EACH_MONTH)
			production_protein_fish_per_m =[0]*len(FISH_PERCENT_EACH_MONTH)
			production_fat_fish_per_m =[0]*len(FISH_PERCENT_EACH_MONTH)



		####LIVESTOCK, EGG, DAIRY INITIAL VARIABLES####



		#time from slaughter livestock to it turning into food
		#not functional yet
		# MEAT_DELAY = 1 #months

		#we use this spreadsheeet https://docs.google.com/spreadsheets/d/1ZyDrGI84TwhXj_QNicwjj9EPWLJ-r3xnAYMzKSAfWc0/edit#gid=824870019

		#edible meat, organs, and fat added
		MEAT_WASTE = c['inputs']['WASTE']['MEAT']

		KG_PER_SMALL_ANIMAL=2.36
		KG_PER_MEDIUM_ANIMAL=24.6
		KG_PER_LARGE_ANIMAL=269.7


		LARGE_ANIMAL_KCALS_PER_KG = 2750
		LARGE_ANIMAL_FAT_PER_KG = .182
		LARGE_ANIMAL_PROTEIN_PER_KG = .257

		SMALL_ANIMAL_KCALS_PER_KG = 1525
		SMALL_ANIMAL_FAT_PER_KG = 0.076
		SMALL_ANIMAL_PROTEIN_PER_KG = .196

		# https://docs.google.com/spreadsheets/d/1tLFHJpXTStxyfNojP_Wrj0MQowfyKujJUA37ZG1q6pk/edit#gid=300573673
		#this one uses pigs from FAOstat, unlike the other two
		#roww 264, "Nutrition Data From FAOstat" tab
		MEDIUM_ANIMAL_KCALS_PER_KG = 3590
		MEDIUM_ANIMAL_FAT_PER_KG = .34
		MEDIUM_ANIMAL_PROTEIN_PER_KG = .11

		# DAIRY_PRODUCTION = c['inputs']['DAIRY_PRODUCTION']
		# DAIRY_WASTE = c['inputs']['WASTE']['DAIRY']
		#billions of kcals
		# MILK_KCALS_PER_1000_COWS_PER_MONTH = ANNUAL_LITERS_PER_COW \
		# 	* KCALS_PER_LITER \
		# 	/ 12 \
		# 	/ 1e9 \
		# 	* 1000 \
		# 	* DAIRY_PRODUCTION \
		# 	* (1-DAIRY_WASTE/100)

		# MILK_KCALS_PER_1000_COWS_PER_MONTH = 0.0369/(1/1000*1e9/4e6)* (1-DAIRY_WASTE/100)
		#https://docs.google.com/spreadsheets/d/1-upBP5-iPtBzyjm5zbeGlfuE4FwqLUyR/edit#gid=2007828143
		#per kg, whole milk, per nutrition calculator
		MILK_KCALS = 610 # kcals per kg
		MILK_FAT = .032 #kg per kg
		MILK_PROTEIN = .033 #kg per kg

		#1000 tons to billions of kcals = grams/kcals
		# MILK_FAT_TO_KCAL_RATIO = MILK_FAT/MILK_KCALS
		# MILK_PROTEIN_TO_KCAL_RATIO = MILK_PROTEIN/MILK_KCALS

		# "FAOSTAT Food Balances", cell z 148
		#https://docs.google.com/spreadsheets/d/1-upBP5-iPtBzyjm5zbeGlfuE4FwqLUyR/edit#gid=102948593 

		# !!!assume all dairy from large animals!!!

		#!!!THESE NUMBERS ARE PRELIMINARY, NEED FUTURE ADJUSTMENT!!! (I googled these numbers)

		#1000s of Tons
		# MILK_FAT_PER_1000_COWS_PER_MONTH= MILK_FAT/MILK_KCALS \
		# 	* (MILK_KCALS_PER_1000_COWS_PER_MONTH / 1000) \
		# 	* KG_TO_1000_TONS \
		# 	* 1000

		# #1000s of Tons
		# MILK_PROTEIN_PER_1000_COWS_PER_MONTH=MILK_PROTEIN/MILK_KCALS \
		# 	* (MILK_KCALS_PER_1000_COWS_PER_MONTH / 1000) \
		# 	* KG_TO_1000_TONS \
		# 	* 1000

		#mike's spreadsheet "area and scaling by month"
		#https://docs.google.com/spreadsheets/d/1-upBP5-iPtBzyjm5zbeGlfuE4FwqLUyR/edit#gid=642022040


		# dairy_animals_1000s_start=[0]*NMONTHS
		# dairy_animals_1000s_end=[0]*NMONTHS
		# dairy_animals_1000s_eaten=[0]*NMONTHS

		######## Human Inedible Produced Primary Dairy and Cattle Meat #########

		# monthly dry caloric tons, globally
		human_inedible_feed = np.array([\
		2728,2728,2728,2728,2728,2728,2728,2728,
		972,972,972,972,972,972,972,972,972,972,972,972,
		594,594,594,594,594,594,594,594,594,594,594,594,
		531,531,531,531,531,531,531,531,531,531,531,531,
		552,552,552,552,552,552,552,552,552,552,552,552,
		789,789,789,789,789,789,789,789,789,789,789,789,
		1026,1026,1026,1026,1026,1026,1026,1026,1026,1026,1026,1026,
		1026,1026,1026,1026,1026,1026,1026,1026,1026,1026,1026,1026#NEEDS FIXING
		])\
		 * 1e6/12

		#dry caloric ton feed/ton milk
		INEDIBLE_TO_DAIRY_CONVERSION = 1.44

		#dry caloric ton feed/ton chicken or pork
		INEDIBLE_TO_CHICKEN_PORK_CONVERSION = 4.8

		#dry caloric ton feed/ton cattle
		INEDIBLE_TO_CATTLE_CONVERSION = 103.0

		# monthly in tons milk (present day value)
		DAIRY_LIMIT = 879e6/12
		# CHICKEN_PORK_LIMIT = 250e6/12

		#monthly in dry caloric tons inedible feed
		DAIRY_LIMIT_FEED_USAGE = DAIRY_LIMIT*INEDIBLE_TO_DAIRY_CONVERSION


		dairy_milk_produced = [] # tons
		cattle_maintained = [] # tons
		for m in range(0,NMONTHS):
			if(ADD_DAIRY):
				max_dairy = human_inedible_feed[m]/INEDIBLE_TO_DAIRY_CONVERSION
				if(max_dairy <= DAIRY_LIMIT):
					dairy_milk_produced.append(max_dairy)
					cattle_maintained.append(0)
					continue
				dairy_milk_produced.append(DAIRY_LIMIT)
				inedible_for_cattle = human_inedible_feed[m] \
				 - DAIRY_LIMIT_FEED_USAGE 
			else:
				dairy_milk_produced.append(0)
				inedible_for_cattle = human_inedible_feed[m]

			if(ADD_NONEGG_NONDAIRY_MEAT):
				cattle_maintained.append(\
					inedible_for_cattle/INEDIBLE_TO_CATTLE_CONVERSION)
			else:
				cattle_maintained.append(0)

		h_e_fed_dairy_limit = DAIRY_LIMIT - np.array(dairy_milk_produced)

		if(ADD_NONEGG_NONDAIRY_MEAT):

			#billions kcals
			cattle_maintained_kcals = np.array(cattle_maintained)\
			 * 1000  \
			 * LARGE_ANIMAL_KCALS_PER_KG \
			 / 1e9


			#1000s tons fat
			cattle_maintained_fat = cattle_maintained_kcals*1e9 \
			 * LARGE_ANIMAL_FAT_PER_KG/LARGE_ANIMAL_KCALS_PER_KG/1e6

			#1000s tons protein
			cattle_maintained_protein = cattle_maintained_kcals*1e9 \
			 * LARGE_ANIMAL_PROTEIN_PER_KG/LARGE_ANIMAL_KCALS_PER_KG/1e6

		else:
			cattle_maintained_kcals =[0]*len(cattle_maintained)
			cattle_maintained_fat =[0]*len(cattle_maintained)
			cattle_maintained_protein =[0]*len(cattle_maintained)

		###### Human Edible Produced "Secondary" Dairy and Cattle Meat #######

		# https://docs.google.com/document/d/1HlML7ptYmRfNJjko5qMfIJJGyLRUBlnCIiEiBMr41cM/edit#heading=h.7wiajnpimw8t
		def get_meat_milk_from_excess(excess_calories,h_e_fed_dairy_limit):

			# each unit of excess calories (with associated fat and protein)
			#are fed first to dairy, then to pigs and chickens, then to cattle

			excess_dry_cal_tons = excess_calories*1e9/4e6

			assert(np.array(excess_dry_cal_tons>=0).all())

			#dry caloric ton excess/ton milk
			EDIBLE_TO_DAIRY_CONVERSION = 0.7

			h_e_fed_dairy_limit_food_usage = h_e_fed_dairy_limit\
			 * EDIBLE_TO_DAIRY_CONVERSION

			CHICKEN_AND_PORK_LIMIT = 250e6/12 #tons meat per month

			#dry caloric ton excess/ton meat
			CHICKEN_PORK_CONVERSION = 4.8 

			#monthly in dry caloric tons inedible feed
			CHICKEN_PORK_LIMIT_FOOD_USAGE = CHICKEN_AND_PORK_LIMIT\
			 * CHICKEN_PORK_CONVERSION

			#dry caloric ton excess/ton meat
			EDIBLE_TO_CATTLE_CONVERSION = 9.8
			dairy_h_e = []
			chicken_pork_maintained = []
			cattle_h_e_maintained = []
			for m in range(0,NMONTHS):

				max_dairy = excess_dry_cal_tons[m]/EDIBLE_TO_DAIRY_CONVERSION

				if(ADD_DAIRY):

					if(max_dairy <= h_e_fed_dairy_limit[m]):
						# tons per month dairy
						dairy_h_e.append(max_dairy)
						# tons per month meat
						chicken_pork_maintained.append(0)
						cattle_h_e_maintained.append(0)
						continue

					dairy_h_e.append(h_e_fed_dairy_limit[m])


					limit_dairy = h_e_fed_dairy_limit_food_usage[m]
				else:
					limit_dairy = 0			
					dairy_h_e.append(0)

				for_chicken_pork_cattle = excess_dry_cal_tons[m] - limit_dairy

				assert(for_chicken_pork_cattle>=0)

				max_chicken_pork = for_chicken_pork_cattle/CHICKEN_PORK_CONVERSION

				if(max_chicken_pork <= CHICKEN_AND_PORK_LIMIT):
					# tons per month meat
					chicken_pork_maintained.append(max_chicken_pork)
					# tons per month meat
					cattle_h_e_maintained.append(0)

					continue				

				# tons per month meat
				chicken_pork_maintained.append(CHICKEN_AND_PORK_LIMIT)

				for_cattle = for_chicken_pork_cattle - CHICKEN_PORK_LIMIT_FOOD_USAGE
				
				# tons per month meat
				cattle_h_e_maintained.append(for_cattle/EDIBLE_TO_CATTLE_CONVERSION)
				

			present_day_tons_per_m_cattle = 136e6/12 #tons a month meat
			present_day_tons_per_m_chicken_pork = 250e6/12 #tons a month

			ratio_maintained_cattle = (np.array(cattle_maintained)+np.array(cattle_h_e_maintained))/present_day_tons_per_m_cattle
			print(ratio_maintained_cattle)
			assert((ratio_maintained_cattle <= 1)[0:47].all())

			ratio_maintained_chicken_pork = np.array(chicken_pork_maintained)/present_day_tons_per_m_chicken_pork
			assert((ratio_maintained_chicken_pork <= 1).all())
			assert((np.array(dairy_h_e)>=0).all())


			#chicken pork assumed to maintain ratio between medium and small animal mass 
			small_to_medium_ratio \
				= 28.2e9*KG_PER_SMALL_ANIMAL \
				/ (3.2e9*KG_PER_MEDIUM_ANIMAL + 28.2e9*KG_PER_SMALL_ANIMAL)

			INIT_SMALL_ANIMALS  \
				= 28.2e9*(1-np.min(ratio_maintained_chicken_pork))

			INIT_MEDIUM_ANIMALS  \
				= 3.2e9*(1-np.min(ratio_maintained_chicken_pork))

			print("culled chicken pork fraction")
			print(1-np.min(ratio_maintained_chicken_pork))

			INIT_LARGE_ANIMALS  \
				= 1.9e9*(1-np.min(ratio_maintained_cattle)) 

			print("culled cattle fraction")
			print(1-np.min(ratio_maintained_cattle))

			#billions kcals monthly
			chicken_pork_kcals = np.array(chicken_pork_maintained)*1e3\
			 * (SMALL_ANIMAL_KCALS_PER_KG*small_to_medium_ratio\
				+ MEDIUM_ANIMAL_KCALS_PER_KG*(1-small_to_medium_ratio))\
			 * (1-MEAT_WASTE/100)\
			 /1e9
			
			#thousands tons monthly
			chicken_pork_fat = np.array(chicken_pork_maintained)*1e3\
			 * (SMALL_ANIMAL_FAT_PER_KG*small_to_medium_ratio\
				+ MEDIUM_ANIMAL_FAT_PER_KG*(1-small_to_medium_ratio))\
			 * (1-MEAT_WASTE/100)\
			 /1e6

			#thousands tons monthly
			chicken_pork_protein = np.array(chicken_pork_maintained)*1e3\
			 * (SMALL_ANIMAL_PROTEIN_PER_KG*small_to_medium_ratio\
				+ MEDIUM_ANIMAL_PROTEIN_PER_KG*(1-small_to_medium_ratio))\
			 * (1-MEAT_WASTE/100)\
			 /1e6

			#billions kcals monthly
			cattle_h_e_maintained_kcals = np.array(cattle_h_e_maintained)\
			 * 1000  \
			 * LARGE_ANIMAL_KCALS_PER_KG \
			 / 1e9

			#1000s tons fat
			cattle_h_e_maintained_fat = cattle_h_e_maintained_kcals*1e9 \
			 / LARGE_ANIMAL_KCALS_PER_KG * LARGE_ANIMAL_FAT_PER_KG/1e6

			#1000s tons protein
			cattle_h_e_maintained_protein = cattle_h_e_maintained_kcals*1e9 \
			 / LARGE_ANIMAL_KCALS_PER_KG * LARGE_ANIMAL_PROTEIN_PER_KG/1e6
			 

			h_e_meat_kcals = \
				cattle_h_e_maintained_kcals + chicken_pork_kcals
			h_e_meat_fat = \
				cattle_h_e_maintained_fat + chicken_pork_fat
			h_e_meat_protein = \
				cattle_h_e_maintained_protein + chicken_pork_protein
			
			return (INIT_SMALL_ANIMALS,
				INIT_MEDIUM_ANIMALS,
				INIT_LARGE_ANIMALS,
				h_e_meat_kcals,
				h_e_meat_fat,
				h_e_meat_protein,
				np.array(dairy_h_e))

		#assume animals need and use human levels of fat and protein per kcal
		#units grams per kcal same as units 1000s tons per billion kcals
		fat_used_ls = c['inputs']['NUTRITION']['FAT_DAILY']/c['inputs']['NUTRITION']['KCALS_DAILY']
		protein_used_ls = c['inputs']['NUTRITION']['PROTEIN_DAILY']/c['inputs']['NUTRITION']['KCALS_DAILY']

		excess_calories = c["inputs"]["EXCESS_CALORIES"] 
		excess_fat_used = fat_used_ls*excess_calories

		excess_protein_used = protein_used_ls*excess_calories

		(INIT_SMALL_ANIMALS,
		INIT_MEDIUM_ANIMALS,
		INIT_LARGE_ANIMALS,
		h_e_meat_kcals,
		h_e_meat_fat,
		h_e_meat_protein, 
		h_e_fed_dairy_produced) = get_meat_milk_from_excess(excess_calories,h_e_fed_dairy_limit)

		if(not ADD_NONEGG_NONDAIRY_MEAT):
			h_e_meat_kcals = np.array([0]*NMONTHS)
			h_e_meat_fat = np.array([0]*NMONTHS)
			h_e_meat_protein = np.array([0]*NMONTHS)

		if(not ADD_DAIRY):
			h_e_fed_dairy_produced = np.array([0]*NMONTHS)


		DAIRY_WASTE = c['inputs']['WASTE']['DAIRY']
		if(ADD_DAIRY):
			
			#billions kcals
			dairy_milk_kcals = np.array(dairy_milk_produced)*1e3\
				* MILK_KCALS/1e9*(1-DAIRY_WASTE/100)

			h_e_milk_kcals = h_e_fed_dairy_produced*1e3\
				* MILK_KCALS/1e9*(1-DAIRY_WASTE/100)
			
			#thousands tons
			dairy_milk_fat = np.array(dairy_milk_produced)/1e3\
				* MILK_FAT*(1-DAIRY_WASTE/100)

			h_e_milk_fat = h_e_fed_dairy_produced/1e3\
				* MILK_FAT*(1-DAIRY_WASTE/100)
			
			#thousands tons
			dairy_milk_protein = np.array(dairy_milk_produced)/1e3\
				* MILK_PROTEIN*(1-DAIRY_WASTE/100)

			h_e_milk_protein = h_e_fed_dairy_produced/1e3\
				* MILK_PROTEIN*(1-DAIRY_WASTE/100)


		else:
			dairy_milk_kcals = np.array([0]*NMONTHS)
			dairy_milk_fat = np.array([0]*NMONTHS)
			dairy_milk_protein = np.array([0]*NMONTHS)


		h_e_balance_kcals = -excess_calories + h_e_meat_kcals + h_e_milk_kcals
		h_e_balance_fat = -excess_fat_used + h_e_meat_fat + h_e_milk_fat
		h_e_balance_protein = -excess_protein_used + h_e_meat_protein + h_e_milk_protein

		#### NON EGG NONDAIRY MEAT ####

		#https://www.ciwf.org.uk/media/5235182/Statistics-Dairy-cows.pdf
		ANNUAL_LITERS_PER_COW = 2200
		KCALS_PER_LITER=609 #kcals for 1 liter whole milk, googled it

		# billion kcals per unit mass initial (first month)
		INITIAL_MILK_COWS = c['inputs']['INITIAL_MILK_COWS']
		INITIAL_MILK_COWS_THOUSANDS = INITIAL_MILK_COWS/1000

		# INIT_SMALL_ANIMALS=c['inputs']['INIT_SMALL_ANIMALS']
		INIT_SMALL_NONEGG_ANIMALS=INIT_SMALL_ANIMALS
		# INIT_MEDIUM_ANIMALS=c['inputs']['INIT_MEDIUM_ANIMALS']
		# INIT_LARGE_ANIMALS = c['inputs']['INIT_LARGE_ANIMALS']

		INIT_LARGE_NONDAIRY_ANIMALS=INIT_LARGE_ANIMALS-INITIAL_MILK_COWS_THOUSANDS*1e3

		# see comparison between row https://docs.google.com/spreadsheets/d/1RZqSrHNiIEuPQLtx1ebCd_kUcFvEF6Ea46xyzA5wU0s/edit#gid=1516287804
		#kcal ratio:
		# compared to livestock meat stats here: https://docs.google.com/spreadsheets/d/1-upBP5-iPtBzyjm5zbeGlfuE4FwqLUyR/edit#gid=1495649381

		#this helps with fat vs other meat https://extension.tennessee.edu/publications/documents/pb1822.pdf
		#that's how we get 237 kg meat but not separable fat, and 91kg separable fat+bone
		#then, we use this spreadsheeet https://docs.google.com/spreadsheets/d/1ZyDrGI84TwhXj_QNicwjj9EPWLJ-r3xnAYMzKSAfWc0/edit#gid=824870019
		# to estimate 13% organ to meat ratio.


		#billions of kcals, 1000s of tons fat, 1000s of tons protein
		#includes organs, fat, and meat


		KCALS_PER_SMALL_ANIMAL=SMALL_ANIMAL_KCALS_PER_KG*KG_PER_SMALL_ANIMAL/1e9
		FAT_PER_SMALL_ANIMAL=SMALL_ANIMAL_FAT_PER_KG*KG_PER_SMALL_ANIMAL*KG_TO_1000_TONS
		PROTEIN_PER_SMALL_ANIMAL=SMALL_ANIMAL_PROTEIN_PER_KG*KG_PER_SMALL_ANIMAL*KG_TO_1000_TONS

		KCALS_PER_MEDIUM_ANIMAL=MEDIUM_ANIMAL_KCALS_PER_KG*KG_PER_MEDIUM_ANIMAL/1e9
		FAT_PER_MEDIUM_ANIMAL=MEDIUM_ANIMAL_FAT_PER_KG*KG_PER_MEDIUM_ANIMAL*KG_TO_1000_TONS
		PROTEIN_PER_MEDIUM_ANIMAL=MEDIUM_ANIMAL_PROTEIN_PER_KG*KG_PER_MEDIUM_ANIMAL*KG_TO_1000_TONS

		KCALS_PER_LARGE_ANIMAL=LARGE_ANIMAL_KCALS_PER_KG*KG_PER_LARGE_ANIMAL/1e9
		FAT_PER_LARGE_ANIMAL=LARGE_ANIMAL_FAT_PER_KG*KG_PER_LARGE_ANIMAL*KG_TO_1000_TONS
		PROTEIN_PER_LARGE_ANIMAL=LARGE_ANIMAL_PROTEIN_PER_KG*KG_PER_LARGE_ANIMAL*KG_TO_1000_TONS

		KCALS_PER_1000_LARGE_ANIMALS=KCALS_PER_LARGE_ANIMAL * 1000
		FAT_PER_1000_LARGE_ANIMALS=FAT_PER_LARGE_ANIMAL * 1000
		PROTEIN_PER_1000_LARGE_ANIMALS=PROTEIN_PER_LARGE_ANIMAL * 1000

		INIT_NONEGG_NONDAIRY_MEAT_KCALS = \
			INIT_SMALL_NONEGG_ANIMALS*KCALS_PER_SMALL_ANIMAL \
			+ INIT_MEDIUM_ANIMALS*KCALS_PER_MEDIUM_ANIMAL \
			+ INIT_LARGE_NONDAIRY_ANIMALS*KCALS_PER_LARGE_ANIMAL 
		INIT_NONEGG_NONDAIRY_MEAT_FAT = \
			INIT_SMALL_NONEGG_ANIMALS*FAT_PER_SMALL_ANIMAL \
			+ INIT_MEDIUM_ANIMALS*FAT_PER_MEDIUM_ANIMAL \
			+ INIT_LARGE_NONDAIRY_ANIMALS*FAT_PER_LARGE_ANIMAL
		INIT_NONEGG_NONDAIRY_MEAT_PROTEIN = \
			INIT_SMALL_NONEGG_ANIMALS*PROTEIN_PER_SMALL_ANIMAL \
			+ INIT_MEDIUM_ANIMALS*PROTEIN_PER_MEDIUM_ANIMAL \
			+ INIT_LARGE_NONDAIRY_ANIMALS*PROTEIN_PER_LARGE_ANIMAL


		MEAT_FRACTION_KCALS = INIT_NONEGG_NONDAIRY_MEAT_KCALS \
			/ (INIT_NONEGG_NONDAIRY_MEAT_KCALS
				+ INIT_NONEGG_NONDAIRY_MEAT_PROTEIN
				+ INIT_NONEGG_NONDAIRY_MEAT_FAT)
		MEAT_FRACTION_FAT =	INIT_NONEGG_NONDAIRY_MEAT_FAT \
			/ (INIT_NONEGG_NONDAIRY_MEAT_KCALS
				+ INIT_NONEGG_NONDAIRY_MEAT_PROTEIN
				+ INIT_NONEGG_NONDAIRY_MEAT_FAT)
		MEAT_FRACTION_PROTEIN = INIT_NONEGG_NONDAIRY_MEAT_PROTEIN \
			/ (INIT_NONEGG_NONDAIRY_MEAT_KCALS
				+ INIT_NONEGG_NONDAIRY_MEAT_PROTEIN
				+ INIT_NONEGG_NONDAIRY_MEAT_FAT)



		# if we assume the rich serve the remaining food to animals and 
		# eating the animals

		#billions kcals
		# MEAT_CURRENT_YIELD_PER_YEAR = 222 #million tons dry caloric
		# MEAT_SUSTAINABLE_YIELD_PER_YEAR = c['inputs']["MEAT_SUSTAINABLE_YIELD_PER_YEAR"] #million tons dry caloric

		# FRACTION_TO_SLAUGHTER = 1-MEAT_SUSTAINABLE_YIELD_PER_YEAR/MEAT_CURRENT_YIELD_PER_YEAR

		# FRACTION_TO_SLAUGHTER = c["inputs"]["FRACTION_TO_SLAUGHTER"]


		# MEAT_SUSTAINABLE_YIELD_PER_MONTH = \
		# 	MEAT_SUSTAINABLE_YIELD_PER_YEAR/12*4e12/1e9

		# SUSTAINED_MEAT_MONTHLY = MEAT_SUSTAINABLE_YIELD_PER_YEAR



		INITIAL_NONEGG_NONDAIRY_MEAT=INIT_NONEGG_NONDAIRY_MEAT_KCALS \
			/ MEAT_FRACTION_KCALS \
			* (1-MEAT_WASTE/100) \
			# * FRACTION_TO_SLAUGHTER


		#### CROP PRODUCTION VARIABLES ####
		#assumption: outdoor crop production is very similar in nutritional
		# profile to stored food
		#reference: row 11, 'outputs' tab  https://docs.google.com/spreadsheets/d/19kzHpux690JTCo2IX2UA1faAd7R1QcBK/edit#gid=1815939673


		ANNUAL_YIELD = 4372e6 #tonnes dry carb equivalent
		JAN_FRACTION = c['inputs']['SEASONALITY'][0]
		FEB_FRACTION = c['inputs']['SEASONALITY'][1]
		MAR_FRACTION = c['inputs']['SEASONALITY'][2]
		APR_FRACTION = c['inputs']['SEASONALITY'][3]
		MAY_FRACTION = c['inputs']['SEASONALITY'][4]
		JUN_FRACTION = c['inputs']['SEASONALITY'][5]
		JUL_FRACTION = c['inputs']['SEASONALITY'][6]
		AUG_FRACTION = c['inputs']['SEASONALITY'][7]
		SEP_FRACTION = c['inputs']['SEASONALITY'][8]
		OCT_FRACTION = c['inputs']['SEASONALITY'][9]
		NOV_FRACTION = c['inputs']['SEASONALITY'][10]
		DEC_FRACTION = c['inputs']['SEASONALITY'][11]

		JAN_YIELD = JAN_FRACTION*ANNUAL_YIELD #tonnes dry carb equivalent
		FEB_YIELD = FEB_FRACTION*ANNUAL_YIELD #tonnes dry carb equivalent
		MAR_YIELD = MAR_FRACTION*ANNUAL_YIELD #tonnes dry carb equivalent
		APR_YIELD = APR_FRACTION*ANNUAL_YIELD #tonnes dry carb equivalent
		MAY_YIELD = MAY_FRACTION*ANNUAL_YIELD #tonnes dry carb equivalent
		JUN_YIELD = JUN_FRACTION*ANNUAL_YIELD #tonnes dry carb equivalent
		JUL_YIELD = JUL_FRACTION*ANNUAL_YIELD #tonnes dry carb equivalent
		AUG_YIELD = AUG_FRACTION*ANNUAL_YIELD #tonnes dry carb equivalent
		SEP_YIELD = SEP_FRACTION*ANNUAL_YIELD #tonnes dry carb equivalent
		OCT_YIELD = OCT_FRACTION*ANNUAL_YIELD #tonnes dry carb equivalent
		NOV_YIELD = NOV_FRACTION*ANNUAL_YIELD #tonnes dry carb equivalent
		DEC_YIELD = DEC_FRACTION*ANNUAL_YIELD #tonnes dry carb equivalent


		#billions of kcals
		JAN_KCALS_OG=JAN_YIELD*KCALS_PER_DRY_CALORIC_TONS / 1e9
		FEB_KCALS_OG=FEB_YIELD*KCALS_PER_DRY_CALORIC_TONS / 1e9
		MAR_KCALS_OG=MAR_YIELD*KCALS_PER_DRY_CALORIC_TONS / 1e9
		APR_KCALS_OG=APR_YIELD*KCALS_PER_DRY_CALORIC_TONS / 1e9
		MAY_KCALS_OG=MAY_YIELD*KCALS_PER_DRY_CALORIC_TONS / 1e9
		JUN_KCALS_OG=JUN_YIELD*KCALS_PER_DRY_CALORIC_TONS / 1e9
		JUL_KCALS_OG=JUL_YIELD*KCALS_PER_DRY_CALORIC_TONS / 1e9
		AUG_KCALS_OG=AUG_YIELD*KCALS_PER_DRY_CALORIC_TONS / 1e9
		SEP_KCALS_OG=SEP_YIELD*KCALS_PER_DRY_CALORIC_TONS / 1e9
		OCT_KCALS_OG=OCT_YIELD*KCALS_PER_DRY_CALORIC_TONS / 1e9
		NOV_KCALS_OG=NOV_YIELD*KCALS_PER_DRY_CALORIC_TONS / 1e9
		DEC_KCALS_OG=DEC_YIELD*KCALS_PER_DRY_CALORIC_TONS / 1e9

		KCALS_PREDISASTER_BEFORE_MAY = JAN_KCALS_OG+FEB_KCALS_OG+MAR_KCALS_OG+APR_KCALS_OG+MAY_KCALS_OG
		KCALS_PREDISASTER_AFTER_MAY = JUN_KCALS_OG+JUL_KCALS_OG+AUG_KCALS_OG+SEP_KCALS_OG+OCT_KCALS_OG+NOV_KCALS_OG+DEC_KCALS_OG

		KCALS_PREDISASTER_ANNUAL=JAN_KCALS_OG+FEB_KCALS_OG+MAR_KCALS_OG+APR_KCALS_OG+MAY_KCALS_OG+JUN_KCALS_OG+JUL_KCALS_OG+AUG_KCALS_OG+SEP_KCALS_OG+OCT_KCALS_OG+NOV_KCALS_OG+DEC_KCALS_OG


		# RATIO_KCALS_POSTDISASTER_Y1 = c['inputs']['RATIO_KCALS_POSTDISASTER']['Y1']

		# RATIO_KCALS_POSTDISASTER_AFTER_MAY_Y1 = (RATIO_KCALS_POSTDISASTER_Y1
		# 	* KCALS_PREDISASTER_ANNUAL
		# 	- KCALS_PREDISASTER_BEFORE_MAY) \
		# 	/ KCALS_PREDISASTER_AFTER_MAY

		# year 2: 20% of normal year
		RATIO_KCALS_POSTDISASTER_Y1 = c['inputs']['RATIO_KCALS_POSTDISASTER']['Y1']
		RATIO_KCALS_POSTDISASTER_Y2 = c['inputs']['RATIO_KCALS_POSTDISASTER']['Y2']
		RATIO_KCALS_POSTDISASTER_Y3 = c['inputs']['RATIO_KCALS_POSTDISASTER']['Y3']
		RATIO_KCALS_POSTDISASTER_Y4 = c['inputs']['RATIO_KCALS_POSTDISASTER']['Y4']
		RATIO_KCALS_POSTDISASTER_Y5 = c['inputs']['RATIO_KCALS_POSTDISASTER']['Y5']
		RATIO_KCALS_POSTDISASTER_Y6 = c['inputs']['RATIO_KCALS_POSTDISASTER']['Y6']
		RATIO_KCALS_POSTDISASTER_Y7 = c['inputs']['RATIO_KCALS_POSTDISASTER']['Y7']
		RATIO_KCALS_POSTDISASTER_Y8 = c['inputs']['RATIO_KCALS_POSTDISASTER']['Y8']
		RATIO_KCALS_POSTDISASTER_Y9 = c['inputs']['RATIO_KCALS_POSTDISASTER']['Y9']
		RATIO_KCALS_POSTDISASTER_Y10 = c['inputs']['RATIO_KCALS_POSTDISASTER']['Y10']
		RATIO_KCALS_POSTDISASTER_Y11 = c['inputs']['RATIO_KCALS_POSTDISASTER']['Y11']

		#billions of kcals
		KCALS_GROWN=[\
			MAY_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y1,
			JUN_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y1,
			JUL_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y1,
			AUG_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y1,
			SEP_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y1,
			OCT_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y1,
			NOV_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y1,
			DEC_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y1,
			JAN_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y2,
			FEB_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y2,
			MAR_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y2,
			APR_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y2,
			MAY_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y2,
			JUN_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y2,
			JUL_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y2,
			AUG_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y2,
			SEP_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y2,
			OCT_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y2,
			NOV_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y2,
			DEC_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y2,
			JAN_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y3,
			FEB_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y3,
			MAR_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y3,
			APR_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y3,
			MAY_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y3,
			JUN_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y3,
			JUL_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y3,
			AUG_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y3,
			SEP_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y3,
			OCT_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y3,
			NOV_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y3,
			DEC_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y3,
			JAN_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y4,
			FEB_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y4,
			MAR_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y4,
			APR_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y4,
			MAY_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y4,
			JUN_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y4,
			JUL_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y4,
			AUG_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y4,
			SEP_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y4,
			OCT_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y4,
			NOV_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y4,
			DEC_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y4,
			JAN_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y5,
			FEB_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y5,
			MAR_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y5,
			APR_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y5,
			MAY_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y5,
			JUN_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y5,
			JUL_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y5,
			AUG_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y5,
			SEP_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y5,
			OCT_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y5,
			NOV_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y5,
			DEC_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y5,
			JAN_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y6,
			FEB_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y6,
			MAR_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y6,
			APR_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y6,
			MAY_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y6,
			JUN_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y6,
			JUL_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y6,
			AUG_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y6,
			SEP_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y6,
			OCT_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y6,
			NOV_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y6,
			DEC_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y6,
			JAN_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y7,
			FEB_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y7,
			MAR_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y7,
			APR_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y7,
			MAY_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y7,
			JUN_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y7,
			JUL_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y7,
			AUG_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y7,
			SEP_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y7,
			OCT_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y7,
			NOV_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y7,
			DEC_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y7,
			JAN_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y8,
			FEB_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y8,
			MAR_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y8,
			APR_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y8,
			MAY_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y8,
			JUN_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y8,
			JUL_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y8,
			AUG_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y8,
			SEP_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y8,
			OCT_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y8,
			NOV_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y8,
			DEC_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y8,
			JAN_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y9,
			FEB_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y9,
			MAR_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y9,
			APR_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y9,
			MAY_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y9,
			JUN_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y9,
			JUL_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y9,
			AUG_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y9,
			SEP_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y9,
			OCT_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y9,
			NOV_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y9,
			DEC_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y9,
			JAN_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y10,
			FEB_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y10,
			MAR_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y10,
			APR_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y10,
			MAY_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y10,
			JUN_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y10,
			JUL_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y10,
			AUG_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y10,
			SEP_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y10,
			OCT_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y10,
			NOV_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y10,
			DEC_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y10,
			JAN_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y11,
			FEB_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y11,
			MAR_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y11,
			APR_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y11,
			MAY_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y11,
			JUN_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y11,
			JUL_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y11,
			AUG_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y11,
			SEP_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y11,
			OCT_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y11,
			NOV_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y11,
			DEC_KCALS_OG * RATIO_KCALS_POSTDISASTER_Y11
			]

		CROP_WASTE = c['inputs']['WASTE']['CROPS']

		TOTAL_CROP_AREA = 500e6 #500 million hectares in tropics

		# we know:
		# 	units_sf_mass*SF_FRACTION_KCALS=sf_kcals
		# and
		# 	units_sf_mass*SF_FRACTION_PROTEIN=sf_protein
		# so
		# 	units_sf_mass = sf_kcals/SF_FRACTION_KCALS
		# => assumption listed previously =>
		# 	units_og_mass = og_kcals/SF_FRACTION_KCALS
		# 	units_og_mass = og_protein/SF_FRACTION_PROTEIN
		# therefore
		# 	og_protein = og_kcals*SF_FRACTION_PROTEIN/SF_FRACTION_KCALS


		#see z152 on 'FAOSTAT food balance' tab https://docs.google.com/spreadsheets/d/1-upBP5-iPtBzyjm5zbeGlfuE4FwqLUyR/edit#gid=102948593
		OG_PROTEIN_PER_KCALS = 0.00946373696 #1000 tons protein per billion kcals
		OG_FAT_PER_KCALS = 0.01361071549 #1000 tons fat per billion kcals


		#### CONSTANTS FOR GREENHOUSES ####
		#greenhouses tab
		#assumption: greenhouse crop production is very similar in nutritional
		# profile to stored food
		# reference: see https://docs.google.com/spreadsheets/d/1f9eVD14Y2d9vmLFP3OsJPFA5d2JXBU-63MTz8MlB1rY/edit#gid=756212200
		GREENHOUSE_SLOPE_MULTIPLIER = c['inputs']['GREENHOUSE_SLOPE_MULTIPLIER']

		#greenhouse paper (scaling of greenhouses in low sunlight scenarios)
		# At constant expansion for 36 months, the cumulative ground coverage 
		# will equal 2.5 million km^2 (250 million hectares). 
		# Takes 5+36=41 months to reach full output
		# NOTE: the 5 months represents the delay from plant to harvest.
		greenhouse_area_long = \
			list(\
				np.append(\
					np.append(\
						np.linspace(0,0,5),\
						np.linspace(0,0.25e9,37)
					),\
					np.linspace(0.25e9,0.25e9,len(KCALS_GROWN)-42)\
				)*GREENHOUSE_SLOPE_MULTIPLIER
			)\

		greenhouse_area = greenhouse_area_long[0:NMONTHS]

		if(ADD_GREENHOUSES):
			MONTHLY_KCALS = np.mean([JAN_KCALS_OG,FEB_KCALS_OG,MAR_KCALS_OG,APR_KCALS_OG,MAY_KCALS_OG,JUN_KCALS_OG,JUL_KCALS_OG,AUG_KCALS_OG,SEP_KCALS_OG,OCT_KCALS_OG,NOV_KCALS_OG,DEC_KCALS_OG])/TOTAL_CROP_AREA


			KCALS_GROWN_PER_HECTARE_BEFORE_WASTE=[\
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y1,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y1,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y1,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y1,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y1,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y1,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y1,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y1,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y2,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y2,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y2,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y2,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y2,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y2,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y2,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y2,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y2,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y2,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y2,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y2,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y3,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y3,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y3,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y3,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y3,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y3,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y3,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y3,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y3,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y3,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y3,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y3,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y4,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y4,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y4,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y4,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y4,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y4,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y4,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y4,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y4,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y4,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y4,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y4,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y5,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y5,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y5,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y5,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y5,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y5,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y5,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y5,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y5,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y5,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y5,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y5,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y6,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y6,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y6,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y6,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y6,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y6,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y6,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y6,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y6,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y6,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y6,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y6,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y7,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y7,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y7,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y7,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y7,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y7,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y7,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y7,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y7,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y7,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y7,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y7,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y8,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y8,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y8,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y8,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y8,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y8,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y8,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y8,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y8,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y8,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y8,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y8,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y9,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y9,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y9,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y9,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y9,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y9,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y9,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y9,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y9,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y9,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y9,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y9,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y10,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y10,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y10,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y10,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y10,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y10,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y10,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y10,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y10,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y10,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y10,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y10,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y11,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y11,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y11,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y11,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y11,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y11,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y11,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y11,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y11,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y11,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y11,
				MONTHLY_KCALS * RATIO_KCALS_POSTDISASTER_Y11
				]
			# plt.title(" dry caloric tons per hectare if 500 million hectares, no waste")
			# plt.plot(np.array(KCALS_GROWN_PER_HECTARE_BEFORE_WASTE)*1e9/4e6)
			# plt.show()
			# SUM_CALORIES_PER_HECTARE = 0.0237337
			KCALS_GROWN_PER_HECTARE = (1-CROP_WASTE/100) \
				* np.array(KCALS_GROWN_PER_HECTARE_BEFORE_WASTE)
			# for x in greenhouse_area:
			# 	kcals_per_hectare.append(x * )
		else:
			KCALS_GROWN_PER_HECTARE = [0]*NMONTHS
			greenhouse_area = [0]*NMONTHS

		KCALS_GROWN_MINUS_GREENHOUSE = []

		for i in range(0,NMONTHS):
			#billions of kcals
			KCALS_GROWN_MINUS_GREENHOUSE.append(\
				KCALS_GROWN[i]*(1-greenhouse_area[i]/TOTAL_CROP_AREA)\
			)
		# plt.plot(KCALS_GROWN_MINUS_GREENHOUSE)
		# plt.show()
		# GH_DRY_TONS_PER_HECTARE_PER_YEAR*4e6/1e9



		if(ADD_OUTDOOR_GROWING):
			production_kcals_outdoor_growing_per_m = \
				list(np.array(KCALS_GROWN_MINUS_GREENHOUSE) \
					* (1 - CROP_WASTE/100) )
		else:
			production_kcals_outdoor_growing_per_m=[0]*NMONTHS
		# we know:
		# 	units_sf_mass*SF_FRACTION_KCALS=sf_kcals
		# and
		# 	units_sf_mass*SF_FRACTION_PROTEIN=sf_protein
		# so
		# 	units_sf_mass = sf_kcals/SF_FRACTION_KCALS
		# => assumption listed previously =>
		# 	units_gh_mass = gh_kcals/SF_FRACTION_KCALS
		# 	units_gh_mass = gh_protein/SF_FRACTION_PROTEIN
		# therefore
		# 	gh_protein = gh_kcals*SF_FRACTION_PROTEIN/SF_FRACTION_KCALS
		#mass initial, units don't matter, we only need to ensure we use the correct 
		#fraction of kcals, fat, and protein per unit initial stored food.

		#for the conversions and numbers, go here 
		# https://docs.google.com/document/d/1HlML7ptYmRfNJjko5qMfIJJGyLRUBlnCIiEiBMr41cM/edit#
		# and here
		# https://docs.google.com/spreadsheets/d/1rYcxSe-Z7ztvW-QwTBXT8GABaRmVdDuQ05HXmTHbQ8I/edit#gid=1141282747

		greenhouse_start=[0]*NMONTHS
		greenhouse_end=[0]*NMONTHS
		greenhouse_eaten=[0]*NMONTHS

		production_protein_outdoor_growing_per_m = \
			list(np.array(production_kcals_outdoor_growing_per_m) \
			* OG_PROTEIN_PER_KCALS  )

		production_fat_outdoor_growing_per_m = \
			list(np.array(production_kcals_outdoor_growing_per_m) \
			* OG_FAT_PER_KCALS)

		INITIAL_OG_KCALS = production_kcals_outdoor_growing_per_m[0]
		INITIAL_OG_FAT = production_fat_outdoor_growing_per_m[0]
		INITIAL_OG_PROTEIN = production_protein_outdoor_growing_per_m[0] 

		if(INITIAL_OG_KCALS==0):
			OG_FRACTION_FAT = 0
			OG_FRACTION_PROTEIN = 0			
		else:

			OG_FRACTION_FAT = INITIAL_OG_FAT / INITIAL_OG_KCALS
			OG_FRACTION_PROTEIN = INITIAL_OG_PROTEIN / INITIAL_OG_KCALS

		# crops_food_start=[0]*NMONTHS
		# crops_food_end=[0]*NMONTHS
		crops_food_produced=list(\
			np.array(production_kcals_outdoor_growing_per_m)
			)
		# plt.plot(crops_food_produced)
		# plt.plot(production_kcals_outdoor_growing_per_m)
		# plt.show()
		crops_food_eaten=[0]*NMONTHS
		crops_food_storage=[0]*NMONTHS

		def getImprovementsFromRotation(
			spring_wheat_fraction_of_rotation,\
			spring_barley_fraction_of_rotation,\
			potato_fraction_of_rotation,\
			rapeseed_fraction_of_rotation):

			#see https://docs.google.com/spreadsheets/d/1-upBP5-iPtBzyjm5zbeGlfuE4FwqLUyR/edit#gid=352242036 greenhouse_NW tab

			# assert(spring_wheat_fraction_of_rotation
			# + spring_barley_fraction_of_rotation
			# + potato_fraction_of_rotation
			# + rapeseed_fraction_of_rotation == 1)

			#billion kcals per hectare per year
			# SPRING_WHEAT_CALORIES = 21056*1e3/1e9 * spring_wheat_fraction_of_rotation
			# SPRING_BARLEY_CALORIES = 22528*1e3/1e9 * spring_barley_fraction_of_rotation
			# POTATO_CALORIES = 37410*1e3/1e9 * potato_fraction_of_rotation
			# RAPESEED_CALORIES = 10670*1e3/1e9 * rapeseed_fraction_of_rotation

			#annual
			# SPRING_WHEAT_CALORIES = 2.91195539 # dry caloric tons per ha
			# SPRING_BARLEY_CALORIES =  2.91195539# dry caloric tons per ha
			# POTATO_CALORIES = 3.749669935 # dry caloric tons per ha
			# RAPESEED_CALORIES = 2.558870452 # dry caloric tons per ha

			SPRING_WHEAT_CALORIES = 2.6 # dry caloric tons per ha
			SPRING_BARLEY_CALORIES =  2.6# dry caloric tons per ha
			POTATO_CALORIES = 9.3525 # dry caloric tons per ha
			RAPESEED_CALORIES = 2.559 # dry caloric tons per ha

			#due to NW
			SPRING_WHEAT_REDUCED =  -.65 + 1
			SPRING_BARLEY_REDUCED = -.65 + 1
			POTATO_REDUCED = -.166 + 1
			RAPESEED_REDUCED = -.679 + 1


			# annual estimated calorie contribution per hectare for each crop 
			#weighted by the fraction of rotation
			SPRING_WHEAT_CONTRIBUTION = spring_wheat_fraction_of_rotation \
				* SPRING_WHEAT_CALORIES*SPRING_WHEAT_REDUCED*4e6/1e9
			SPRING_BARLEY_CONTRIBUTION = spring_barley_fraction_of_rotation\
				* SPRING_BARLEY_CALORIES*SPRING_BARLEY_REDUCED*4e6/1e9
			POTATO_CONTRIBUTION = potato_fraction_of_rotation \
				* POTATO_CALORIES*POTATO_REDUCED*4e6/1e9
			RAPESEED_CONTRIBUTION = rapeseed_fraction_of_rotation \
				* RAPESEED_CALORIES*RAPESEED_REDUCED*4e6/1e9
			# min 1 in 6 years, max 1 in 3.
			# rotation_options = [0.17,0.2,0.25,0.3,0.33]

			SUM_CALORIES_PER_HA_PER_MONTH = (SPRING_WHEAT_CONTRIBUTION \
				+ SPRING_BARLEY_CONTRIBUTION \
				+ POTATO_CONTRIBUTION \
				+ RAPESEED_CONTRIBUTION)/12


			SUM_CALORIES = SUM_CALORIES_PER_HA_PER_MONTH * TOTAL_CROP_AREA

			#estimate for "do nothing" nuclear yields, cell h41
			DO_NOTHING_SUM_PER_HECTARE_PER_MONTH=0.0004798542381 # bill kcals
			SUM_CALORIES_DO_NOTHING = DO_NOTHING_SUM_PER_HECTARE_PER_MONTH*TOTAL_CROP_AREA # billions kcals per month
			# let's assume greenhouses average the annual from outdoor growing plus
			# a 40% increase.

			#thousand tons protein per hectare per year
			# ADJUSTED_POTATO_PROTEIN = 0.804/1e3 *(3.7496/9.3525)*  potato_fraction_of_rotation*POTATO_REDUCED
			ADJUSTED_POTATO_PROTEIN = 0.804/1e3 *  potato_fraction_of_rotation*POTATO_REDUCED

			#thousand tons protein per hectare per year8
			# ADJUSTED_SPRING_BARLEY_PROTEIN = 0.634/1e3 *(2.9/2.6)  \
			ADJUSTED_SPRING_BARLEY_PROTEIN = 0.634/1e3  \
				* spring_barley_fraction_of_rotation*SPRING_BARLEY_REDUCED

			#thousand tons protein per hectare per year
			# ADJUSTED_SPRING_WHEAT_PROTEIN = 0.634/1e3*(2.9/2.6) \
			ADJUSTED_SPRING_WHEAT_PROTEIN = 0.634/1e3 \
				* spring_wheat_fraction_of_rotation*SPRING_WHEAT_REDUCED

			#thousand tons protein per hectare per year
			ADJUSTED_RAPESEED_PROTEIN = 0/1e3 *  rapeseed_fraction_of_rotation*RAPESEED_REDUCED

			#thousand tons fat per hectare per year
			# ADJUSTED_POTATO_FAT = 0.043/1e3 *(3.7496/9.3525)*  potato_fraction_of_rotation*POTATO_REDUCED
			ADJUSTED_POTATO_FAT = 0.043/1e3 *  potato_fraction_of_rotation*POTATO_REDUCED

			#thousand tons fat per hectare per year
			# ADJUSTED_SPRING_WHEAT_FAT = 0.074/1e3  *(2.9/2.6) \
			ADJUSTED_SPRING_WHEAT_FAT = 0.074/1e3  \
				* spring_wheat_fraction_of_rotation*SPRING_WHEAT_REDUCED


			#thousand tons fat per hectare per year
			# ADJUSTED_SPRING_BARLEY_FAT = 0.074/1e3 *(2.9/2.6)\
			ADJUSTED_SPRING_BARLEY_FAT = 0.074/1e3 \
				* spring_barley_fraction_of_rotation*SPRING_BARLEY_REDUCED

			#thousand tons fat per hectare per year
			# ADJUSTED_RAPESEED_FAT = 2.66745/2.559*1.195/1e3 *  rapeseed_fraction_of_rotation*RAPESEED_REDUCED
			ADJUSTED_RAPESEED_FAT = 1.195/1e3 *  rapeseed_fraction_of_rotation*RAPESEED_REDUCED

			ROTATION_PROTEIN = (ADJUSTED_POTATO_PROTEIN \
				+ ADJUSTED_SPRING_BARLEY_PROTEIN\
				+ ADJUSTED_SPRING_WHEAT_PROTEIN\
				+ ADJUSTED_RAPESEED_PROTEIN) \
				/12

			ROTATION_FAT = (ADJUSTED_POTATO_FAT \
				+ ADJUSTED_SPRING_WHEAT_FAT \
				+ ADJUSTED_SPRING_BARLEY_FAT \
				+ ADJUSTED_RAPESEED_FAT) \
				/12

			KCAL_RATIO = SUM_CALORIES_PER_HA_PER_MONTH / DO_NOTHING_SUM_PER_HECTARE_PER_MONTH
			FAT_RATIO = ROTATION_FAT/SUM_CALORIES_PER_HA_PER_MONTH
			PROTEIN_RATIO = ROTATION_PROTEIN/SUM_CALORIES_PER_HA_PER_MONTH

			return (KCAL_RATIO,FAT_RATIO,PROTEIN_RATIO)



		# SUM_CALORIES is an overestimate by some factor, as it is in current
		# day conditions. We improve accuracy by applying the outdoor growing 
		# estimate and decreasing the estimated fat and protein by the same 
		# factor that calories are decreased by
		def get_greenhouse_yield_per_ha(KCAL_RATIO,FAT_RATIO,PROTEIN_RATIO):
			rotation_fat_per_ha_long = []
			rotation_protein_per_ha_long = []
			rotation_kcals_per_ha_long = []
			for yearly_mean_kcals in KCALS_GROWN_PER_HECTARE:
				gh_kcals = yearly_mean_kcals*KCAL_RATIO \
				* (1+c['inputs']["GREENHOUSE_GAIN_PCT"]/100)
				
				rotation_kcals_per_ha_long.append(gh_kcals)

				rotation_fat_per_ha_long.append(FAT_RATIO * gh_kcals)


				rotation_protein_per_ha_long.append(PROTEIN_RATIO * gh_kcals)
				# if(yearly_mean_kcals>0):

				rotation_kcals_per_ha = rotation_kcals_per_ha_long[0:NMONTHS]
				rotation_fat_per_ha = rotation_fat_per_ha_long[0:NMONTHS]
				rotation_protein_per_ha = rotation_protein_per_ha_long[0:NMONTHS]

			return (rotation_kcals_per_ha,\
				rotation_fat_per_ha,\
				rotation_protein_per_ha)


		spring_wheat_pct_of_rotation = 17
		spring_barley_pct_of_rotation = 17
		potato_pct_of_rotation = 33
		rapeseed_pct_of_rotation = 33
		assert(spring_wheat_pct_of_rotation
					+ spring_barley_pct_of_rotation
					+ potato_pct_of_rotation
					+ rapeseed_pct_of_rotation == 100)

		(KCAL_RATIO,FAT_RATIO,PROTEIN_RATIO) = getImprovementsFromRotation(spring_wheat_pct_of_rotation/100,\
			spring_barley_pct_of_rotation/100,\
			potato_pct_of_rotation/100,\
			rapeseed_pct_of_rotation/100)

		og_rot_frac_kcals = []
		og_rot_frac_fat = []
		og_rot_frac_protein = []

		for m in range(0,NMONTHS):
			
			if(np.isnan(OG_FRACTION_PROTEIN)):
				OG_FRACTION_PROTEIN = 0
			if(np.isnan(OG_FRACTION_FAT)):
				OG_FRACTION_FAT = 0

			#need to use the multiplier on units of kcals to get fat and protein
			if(c["inputs"]["OG_USE_BETTER_ROTATION"] and m>8):
				OG_ROTATION_FRACTION_KCALS = KCAL_RATIO
				#need to multiply the amount of actual calories, 
				#then multiply by 1000s tons fat and protein per billion calories
				OG_ROTATION_FRACTION_FAT = KCAL_RATIO * FAT_RATIO
				OG_ROTATION_FRACTION_PROTEIN = KCAL_RATIO * PROTEIN_RATIO

				

			else:
				OG_ROTATION_FRACTION_KCALS = 1
				OG_ROTATION_FRACTION_FAT = OG_FRACTION_FAT
				OG_ROTATION_FRACTION_PROTEIN = OG_FRACTION_PROTEIN

			og_rot_frac_kcals.append(OG_ROTATION_FRACTION_KCALS) 
			og_rot_frac_fat.append(OG_ROTATION_FRACTION_FAT) 
			og_rot_frac_protein.append(OG_ROTATION_FRACTION_PROTEIN) 

		(greenhouse_kcals_per_ha,greenhouse_fat_per_ha,greenhouse_protein_per_ha) \
			= get_greenhouse_yield_per_ha(KCAL_RATIO, FAT_RATIO, PROTEIN_RATIO)


		if(VERBOSE):
			print("production_kcals_outdoor_growing_per_m0")
			print(production_kcals_outdoor_growing_per_m[0])
			print("production_protein_outdoor_growing_per_m[0]")
			print(production_protein_outdoor_growing_per_m[0])
			print("production_fat_outdoor_growing_per_m[0]")
			print(production_fat_outdoor_growing_per_m[0])

			print("production_protein_outdoor_growing_per_m per b kcals[0]")
			print(production_protein_outdoor_growing_per_m[0]/production_kcals_outdoor_growing_per_m[0])
			print("production_fat_outdoor_growing_per_mper b kcals[0]")
			print(production_fat_outdoor_growing_per_m[0]/production_kcals_outdoor_growing_per_m[0])
			
			print("production_protein_sf_per_m per b kcals[0]")
			print(INITIAL_SF_PROTEIN/INITIAL_SF_KCALS)
			print("production_fat_stored_food_per_mper b kcals[0]")
			print(INITIAL_SF_FAT/INITIAL_SF_KCALS)


		#### CONSTANTS FOR METHANE SINGLE CELL PROTEIN ####
		SUGAR_WASTE = c['inputs']['WASTE']['SUGAR']

		#apply sugar waste also to methane scp, for lack of better baseline

		#in billions of calories
		INDUSTRIAL_FOODS_SLOPE_MULTIPLIER = \
			c['inputs']['INDUSTRIAL_FOODS_SLOPE_MULTIPLIER']
		#billion calories a month for 100% population.
		INDUSTRIAL_FOODS_MONTHLY_KCAL_MULTIPLIER = 6793977/12 
		METHANE_SCP_PERCENT_KCALS = list(np.array([0,0,0,0,0,0,0,0,0,0,0,0,2,2,\
			2,2,2,4,7,7,7,7,7,9,11,11,11,11,11,11,13,15,15,15,15,\
			15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15])/(1-0.12)*INDUSTRIAL_FOODS_SLOPE_MULTIPLIER)

			# 15,17,20,20,\
			# 20,20,20,22,22,24,24,24,24,24,26,28,28,28,28,28,30,30,33,33,33,33,
			# 33,35,37,37,37,37,37,39,39,41,41,\
			# 41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,\
			# 41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,\
			# 41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,\
			# 41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,\
			# 41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,\
			# 41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,\
			# 41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,\
			# 41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41])/(1-0.12)*INDUSTRIAL_FOODS_SLOPE_MULTIPLIER)

		if(ADD_METHANE_SCP):
			production_kcals_scp_per_m_long = []
			for x in METHANE_SCP_PERCENT_KCALS:
				production_kcals_scp_per_m_long.append(x / 100 * INDUSTRIAL_FOODS_MONTHLY_KCAL_MULTIPLIER*(1-SUGAR_WASTE/100))
		else:
			production_kcals_scp_per_m_long=[0]*len(METHANE_SCP_PERCENT_KCALS)

		production_kcals_scp_per_m = production_kcals_scp_per_m_long[0:NMONTHS]

		SCP_KCALS_PER_KG = 5350
		SCP_FRAC_PROTEIN=0.650
		SCP_FRAC_FAT=0.09

		production_protein_scp_per_m = \
			list(np.array(production_kcals_scp_per_m) \
			* SCP_FRAC_PROTEIN / SCP_KCALS_PER_KG )

		production_fat_scp_per_m = \
			list(np.array(production_kcals_scp_per_m) \
			* SCP_FRAC_FAT / SCP_KCALS_PER_KG )



		#### CONSTANTS FOR CELLULOSIC SUGAR ####

		#in billions of calories
		# CELL_SUGAR_PERCENT_KCALS = list(np.array([0.00, 0.00, 0.00, 0.00, 0.00, 9.79, 9.79, 9.79, 19.57, 23.48, 24.58, 28.49, 28.49,29.59,31.64, 31.64, 31.64, 31.64, 33.69, 35.74, 35.74, 35.74, 35.74, 37.78, 38.70, 39.61,40.53,41.44, 42.35, 43.27, 44.18, 45.10, 46.01, 46.93, 47.84, 48.76, 49.67, 50.58, 51.50,52.41,53.33, 54.24, 55.16, 56.07, 56.99, 57.90, 58.81, 59.73, 60.64, 61.56, 62.47, 63.39,64.30,65.21, 66.13, 67.04, 67.96, 68.87, 69.79, 70.70, 71.62, 72.53, 73.44, 74.36, 75.27,76.19,77.10, 78.02, 78.93, 79.85, 80.76, 81.67]) * CELLULOSIC_SUGAR_SLOPE_MULTIPLIER*(1-12/100))
		CELL_SUGAR_PERCENT_KCALS = list(np.array([0.00, 0.00, 0.00, 0.00, 0.00, 9.79, 9.79, 9.79, 20, 20, 20, 20, 20, 20,20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20,20,20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20,20,20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20,20,20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20,20,20, 20, 20, 20, 20, 20,20, 20, 20, 20, 20,20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20,20,20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20,20,20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20,20,20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20,20,20, 20, 20, 20, 20, 20,20, 20, 20, 20, 20,20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20,20,20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20,20,20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20,20,20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20,20,20, 20, 20, 20, 20, 20,20, 20, 20, 20, 20,20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20,20,20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20,20,20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20,20,20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20,20,20, 20, 20, 20, 20, 20]) *1/(1-0.12)* INDUSTRIAL_FOODS_SLOPE_MULTIPLIER)

		# years = np.linspace(0,len(CELL_SUGAR_PERCENT_KCALS)-1,len(CELL_SUGAR_PERCENT_KCALS))/12
		# plt.plot(years,np.array(CELL_SUGAR_PERCENT_KCALS)+np.array(METHANE_SCP_PERCENT_KCALS))
		# plt.xlabel('years from may event')
		# plt.ylabel('percent human kcal requirement')
		# plt.show()
		if(ADD_CELLULOSIC_SUGAR):
			production_kcals_CS_per_m_long = []
			for x in CELL_SUGAR_PERCENT_KCALS:
				production_kcals_CS_per_m_long.append(x / 100 * INDUSTRIAL_FOODS_MONTHLY_KCAL_MULTIPLIER*(1-SUGAR_WASTE/100))
		else:
			production_kcals_CS_per_m_long = \
				[0]*len(CELL_SUGAR_PERCENT_KCALS)

		production_kcals_CS_per_m = production_kcals_CS_per_m_long[0:NMONTHS]

		if(VERBOSE):
			print("INITIAL_MILK_COWS_THOUSANDS, billions")
			print(INITIAL_MILK_COWS_THOUSANDS/1e9)
			print("Number of large animals, billions")
			print((INIT_LARGE_NONDAIRY_ANIMALS+INITIAL_MILK_COWS_THOUSANDS)/1e9)
			print("Percent Dairy Animals of large animals")
			print(INITIAL_MILK_COWS_THOUSANDS/(INIT_LARGE_NONDAIRY_ANIMALS+INITIAL_MILK_COWS_THOUSANDS)*100)

			print('millions of people fed for a year from eating milk cows')
			print(INITIAL_MILK_COWS_THOUSANDS*1000*FAT_PER_LARGE_ANIMAL/(12*FAT_MONTHLY)/1e6)

			print("billions of people fed for a year from eating all livestock minus dairy cows and egg laying hens")
			print(INIT_NONEGG_NONDAIRY_MEAT_FAT/(12*FAT_MONTHLY)/1e9)


		#### BIOFUELS ####
		#see 'biofuels' tab https://docs.google.com/spreadsheets/d/1-upBP5-iPtBzyjm5zbeGlfuE4FwqLUyR/edit#gid=2030318378
		BIOFUEL_KCALS_PER_YEAR = 8.3e5 #billions of kcals
		BIOFUEL_KCALS_PER_MONTH = BIOFUEL_KCALS_PER_YEAR/12
		BIOFUEL_PROTEIN_PER_YEAR = 1.45e4 #1000s of tons
		BIOFUEL_PROTEIN_PER_MONTH = BIOFUEL_PROTEIN_PER_YEAR/12
		BIOFUEL_FAT_PER_YEAR = 0.522e4 #1000s of tons
		BIOFUEL_FAT_PER_MONTH = BIOFUEL_FAT_PER_YEAR/12#1000s of tons

		biofuel_delay = c['inputs']['BIOFUEL_SHUTOFF_DELAY']
		biofuels_kcals = [BIOFUEL_KCALS_PER_MONTH]*biofuel_delay + [0]*(NMONTHS-biofuel_delay)
		biofuels_fat = [BIOFUEL_FAT_PER_MONTH]*biofuel_delay + [0]*(NMONTHS-biofuel_delay)
		biofuels_protein = [BIOFUEL_PROTEIN_PER_MONTH]*biofuel_delay + [0]*(NMONTHS-biofuel_delay)



		#### OTHER VARIABLES ####

		CONVERT_TO_KCALS = WORLD_POP/1e9/KCALS_DAILY
		CONVERT_TO_FAT = 1/WORLD_POP * FAT_DAILY / 1e9
		CONVERT_TO_PROTEIN = 1/WORLD_POP * PROTEIN_DAILY / 1e9

		s = {}

		s["built_area"] = built_area
		s["biofuels_fat"] = biofuels_fat
		s["biofuels_protein"] = biofuels_protein
		s["biofuels_kcals"] = biofuels_kcals
		s["crops_food_produced"] = crops_food_produced
		s["og_rot_frac_kcals"] = og_rot_frac_kcals
		s["og_rot_frac_fat"] = og_rot_frac_fat
		s["og_rot_frac_protein"] = og_rot_frac_protein
		s["greenhouse_kcals_per_ha"] = greenhouse_kcals_per_ha
		s["greenhouse_fat_per_ha"] = greenhouse_fat_per_ha
		s["greenhouse_protein_per_ha"] = greenhouse_protein_per_ha
		s["production_kcals_scp_per_m"] = production_kcals_scp_per_m
		s["production_protein_scp_per_m"] = production_protein_scp_per_m
		s["production_fat_scp_per_m"] = production_fat_scp_per_m
		s["production_kcals_fish_per_m"] = production_kcals_fish_per_m
		s["production_protein_fish_per_m"] = production_protein_fish_per_m
		s["production_fat_fish_per_m"] = production_fat_fish_per_m
		s["production_kcals_CS_per_m"] = production_kcals_CS_per_m
		s["dairy_milk_kcals"] = dairy_milk_kcals
		s["h_e_milk_kcals"] = h_e_milk_kcals
		s["dairy_milk_fat"] = dairy_milk_fat
		s["h_e_milk_fat"] = h_e_milk_fat
		s["dairy_milk_protein"] = dairy_milk_protein
		s["h_e_milk_protein"] = h_e_milk_protein
		s["h_e_balance_kcals"] = h_e_balance_kcals
		s["h_e_balance_fat"] = h_e_balance_fat
		s["h_e_balance_protein"] = h_e_balance_protein
		s["cattle_maintained_kcals"] = cattle_maintained_kcals
		s["cattle_maintained_fat"] = cattle_maintained_fat
		s["cattle_maintained_protein"] = cattle_maintained_protein
		s["greenhouse_area"] = greenhouse_area
		s["og_rot_frac_fat"] = og_rot_frac_fat
		s["og_rot_frac_protein"] = og_rot_frac_protein
		s["h_e_meat_kcals"] = h_e_meat_kcals
		s["h_e_meat_fat"] = h_e_meat_fat
		s["h_e_meat_protein"] = h_e_meat_protein
		s["h_e_fed_dairy_produced"] = h_e_fed_dairy_produced
		s["excess_calories"] = excess_calories
		s["excess_fat_used"] = excess_fat_used
		s["excess_protein_used"] = excess_protein_used
		#store variables useful for analysis
		# c={}
		c['NMONTHS']=NMONTHS
		c['NDAYS']=NDAYS
		c['KCALS_DAILY']=KCALS_DAILY
		c['FAT_DAILY']=FAT_DAILY
		c['PROTEIN_DAILY']=PROTEIN_DAILY
		c['ADD_STORED_FOOD']=ADD_STORED_FOOD
		c['ADD_FISH']=ADD_FISH
		c['ADD_SEAWEED']=ADD_SEAWEED
		c['ADD_GREENHOUSES']=ADD_GREENHOUSES
		c['ADD_NONEGG_NONDAIRY_MEAT']=ADD_NONEGG_NONDAIRY_MEAT
		c['ADD_DAIRY']=ADD_DAIRY
		c['ADD_OUTDOOR_GROWING']=ADD_OUTDOOR_GROWING
		c['MAXIMIZE_ONLY_FOOD_AFTER_DAY_150']= \
			MAXIMIZE_ONLY_FOOD_AFTER_DAY_150
		c['LIMIT_SEAWEED_AS_PERCENT_KCALS']=\
			LIMIT_SEAWEED_AS_PERCENT_KCALS
		c['VERBOSE']=VERBOSE
		c['KCALS_MONTHLY']=KCALS_MONTHLY
		c['PROTEIN_MONTHLY']=PROTEIN_MONTHLY
		c['FAT_MONTHLY']=FAT_MONTHLY
		c['HARVEST_LOSS']=HARVEST_LOSS
		c['SF_FRACTION_KCALS']=SF_FRACTION_KCALS
		c['SF_FRACTION_FAT']=SF_FRACTION_FAT
		c['SF_FRACTION_PROTEIN']=SF_FRACTION_PROTEIN
		# c['OG_ROTATION_FRACTION_KCALS']=OG_ROTATION_FRACTION_KCALS
		# c['OG_ROTATION_FRACTION_FAT']=OG_ROTATION_FRACTION_FAT
		# c['OG_ROTATION_FRACTION_PROTEIN']=OG_ROTATION_FRACTION_PROTEIN
		c['MEAT_FRACTION_KCALS']=MEAT_FRACTION_KCALS
		c['MEAT_FRACTION_FAT']=MEAT_FRACTION_FAT
		c['MEAT_FRACTION_PROTEIN']=MEAT_FRACTION_PROTEIN
		# c['MILK_KCALS_PER_1000_COWS_PER_MONTH']=MILK_KCALS_PER_1000_COWS_PER_MONTH
		# c['MILK_FAT_PER_1000_COWS_PER_MONTH']=MILK_FAT_PER_1000_COWS_PER_MONTH
		# c['MILK_PROTEIN_PER_1000_COWS_PER_MONTH']=MILK_PROTEIN_PER_1000_COWS_PER_MONTH
		c['KCALS_PER_1000_LARGE_ANIMALS']=KCALS_PER_1000_LARGE_ANIMALS
		c['FAT_PER_1000_LARGE_ANIMALS']=FAT_PER_1000_LARGE_ANIMALS
		c['PROTEIN_PER_1000_LARGE_ANIMALS']=PROTEIN_PER_1000_LARGE_ANIMALS
		c['SEAWEED_KCALS']=SEAWEED_KCALS
		c['SEAWEED_FAT']=SEAWEED_FAT
		c['SEAWEED_PROTEIN']=SEAWEED_PROTEIN
		c['INITIAL_SF']=INITIAL_SF
		c['INITIAL_NONEGG_NONDAIRY_MEAT']=INITIAL_NONEGG_NONDAIRY_MEAT
		c['WORLD_POP'] = WORLD_POP
		c['ADD_CELLULOSIC_SUGAR'] = ADD_CELLULOSIC_SUGAR
		c['ADD_METHANE_SCP'] = ADD_METHANE_SCP
		c['FISH_FAT'] = FISH_FAT
		c['FISH_PROTEIN'] = FISH_PROTEIN
		c['FISH_KCALS'] = FISH_KCALS
		c['CONVERT_TO_KCALS'] = CONVERT_TO_KCALS

		c["KG_PER_SMALL_ANIMAL"] = KG_PER_SMALL_ANIMAL
		c["KG_PER_MEDIUM_ANIMAL"] = KG_PER_MEDIUM_ANIMAL
		c["KG_PER_LARGE_ANIMAL"] = KG_PER_LARGE_ANIMAL

		c["LARGE_ANIMAL_KCALS_PER_KG"] = LARGE_ANIMAL_KCALS_PER_KG
		c["LARGE_ANIMAL_FAT_PER_KG"] = LARGE_ANIMAL_FAT_PER_KG
		c["LARGE_ANIMAL_PROTEIN_PER_KG"] = LARGE_ANIMAL_PROTEIN_PER_KG

		c["MEDIUM_ANIMAL_KCALS_PER_KG"] = MEDIUM_ANIMAL_KCALS_PER_KG
		c["MEDIUM_ANIMAL_FAT_PER_KG"] = MEDIUM_ANIMAL_FAT_PER_KG
		c["MEDIUM_ANIMAL_PROTEIN_PER_KG"] = MEDIUM_ANIMAL_PROTEIN_PER_KG

		c["SMALL_ANIMAL_KCALS_PER_KG"] = SMALL_ANIMAL_KCALS_PER_KG
		c["SMALL_ANIMAL_FAT_PER_KG"] = SMALL_ANIMAL_FAT_PER_KG
		c["SMALL_ANIMAL_PROTEIN_PER_KG"] = SMALL_ANIMAL_PROTEIN_PER_KG
		c["DAYS_IN_MONTH"] = DAYS_IN_MONTH

		return (c,s)