################################ Constants ####################################
##                                                                            #
##           Calculates all the constants (class soon to be edited)           #
##                                                                            #
###############################################################################

import numpy as np


class Constants:

    def __init__(self):
        self.TOTAL_CROP_AREA = 500e6  # 500 million hectares in tropics

        # billion kcals a month for 100% population (7.8 billion people).
        self.GLOBAL_MONTHLY_NEEDS = 6793977 / 12

        self.KG_TO_1000_TONS = 1 / (1e6)

        self.DAYS_IN_MONTH = 30

        # FAO ALL SUPPLY UTILIZATION SHEET
        # units are millions tons (dry caloric, fat, protein)
        #         year    Kcals    Fat    Protein
        #         2014    3550    225    468
        #         2015    3583    228    478
        #         2016    3682    234    493
        #         2017    3774    246    511
        #         2018    3725    245    498
        #         2019    7087    449    937

        # TREND    2020    3879.2    257    525
        # percent OG redirected to non-eaten seeds
        self.SEED_PERCENT = 100 * (92 / 3898)


    def computeConstants(self, constants):
        VERBOSE = False

        inputs_to_optimizer = constants['inputs']  # single valued inputs to optimizer

        # full months duration of simulation
        self.POP = inputs_to_optimizer['POP']
        NMONTHS = inputs_to_optimizer['NMONTHS']
        NDAYS = NMONTHS * self.DAYS_IN_MONTH
        ADD_FISH = inputs_to_optimizer['ADD_FISH']
        ADD_SEAWEED = inputs_to_optimizer['ADD_SEAWEED']
        ADD_MEAT = inputs_to_optimizer['ADD_MEAT']
        ADD_DAIRY = inputs_to_optimizer['ADD_DAIRY']

        BASELINE_CROP_KCALS = inputs_to_optimizer['BASELINE_CROP_KCALS']
        BASELINE_CROP_FAT = inputs_to_optimizer['BASELINE_CROP_FAT']
        BASELINE_CROP_PROTEIN = inputs_to_optimizer['BASELINE_CROP_PROTEIN']

        FEED_KCALS = inputs_to_optimizer['FEED_KCALS']
        FEED_FAT = inputs_to_optimizer['FEED_FAT']
        FEED_PROTEIN = inputs_to_optimizer['FEED_PROTEIN']

        BIOFUEL_KCALS = inputs_to_optimizer['BIOFUEL_KCALS']
        BIOFUEL_FAT = inputs_to_optimizer['BIOFUEL_FAT']
        BIOFUEL_PROTEIN = inputs_to_optimizer['BIOFUEL_PROTEIN']

        # tonnes dry carb equivalent
        ANNUAL_YIELD = 0.96 * BASELINE_CROP_KCALS \
                            * (1 - self.SEED_PERCENT / 100)

        # 1000 tons fat per billion kcals
        OG_FRACTION_FAT = 1.02 * (BASELINE_CROP_FAT / 1e3) \
                               / (ANNUAL_YIELD * 4e6 / 1e9)

        # 1000 tons protein per billion kcals
        OG_FRACTION_PROTEIN = 0.93 * (BASELINE_CROP_PROTEIN / 1e3) \
                                   / (ANNUAL_YIELD * 4e6 / 1e9)

        ADD_STORED_FOOD = inputs_to_optimizer['ADD_STORED_FOOD']
        ADD_METHANE_SCP = inputs_to_optimizer['ADD_METHANE_SCP']
        ADD_CELLULOSIC_SUGAR = inputs_to_optimizer['ADD_CELLULOSIC_SUGAR']
        ADD_GREENHOUSES = inputs_to_optimizer['ADD_GREENHOUSES']
        ADD_OUTDOOR_GROWING = inputs_to_optimizer['ADD_OUTDOOR_GROWING']

        # or, should this be 1543e6?? cell L8 https://docs.google.com/spreadsheets/d / 1rYcxSe-Z7ztvW-QwTBXT8GABaRmVdDuQ05HXmTHbQ8I/edit#gid=1141282747
        self.FEED_MONTHLY_USAGE_KCALS = FEED_KCALS / 12 * 4e6 / 1e9  # billions kcals
        self.FEED_MONTHLY_USAGE_FAT = FEED_FAT / 12 / 1e3  # thousand tons
        self.FEED_MONTHLY_USAGE_PROTEIN = FEED_PROTEIN / 12 / 1e3  # thousand tons

        self.BIOFUEL_MONTHLY_USAGE_KCALS = BIOFUEL_KCALS / 12 * 4e6 / 1e9  # billions kcals
        self.BIOFUEL_MONTHLY_USAGE_FAT = BIOFUEL_FAT / 12 / 1e3  # thousand tons
        self.BIOFUEL_MONTHLY_USAGE_PROTEIN = BIOFUEL_PROTEIN / 12 / 1e3  # thousand tons


        #### NUTRITION PER MONTH ####

        # https://docs.google.com/spreadsheets/d / 1RZqSrHNiIEuPQLtx1ebCd_kUcFvEF6Ea46xyzA5wU0s/edit#gid=1516287804

        # we will assume a 2100 kcals diet, and scale the "upper safe" nutrition
        # from the spreadsheet down to this "standard" level.
        # we also add 20% loss, according to the sorts of loss seen in this spreadsheet
        KCALS_DAILY = inputs_to_optimizer['NUTRITION']['KCALS_DAILY']
        PROTEIN_DAILY = inputs_to_optimizer['NUTRITION']['PROTEIN_DAILY']
        FAT_DAILY = inputs_to_optimizer['NUTRITION']['FAT_DAILY']

        self.KCALS_MONTHLY = KCALS_DAILY * self.DAYS_IN_MONTH  # in kcals per person
        self.PROTEIN_MONTHLY = PROTEIN_DAILY * self.DAYS_IN_MONTH / 1e9  # in thousands of tons
        self.FAT_MONTHLY = FAT_DAILY * self.DAYS_IN_MONTH / 1e9  # in thousands of tons

        ####SEAWEED INITIAL VARIABLES####

        # use "laver" variety for now from nutrition calculator
        # https://docs.google.com/spreadsheets/d / 1RZqSrHNiIEuPQLtx1ebCd_kUcFvEF6Ea46xyzA5wU0s/edit#gid=1516287804
        WET_TO_DRY_MASS_CONVERSION = 1 / 6

        # in order, in equal parts by mass:
        # Laver dry

        # kcals per kg dry
        KCALS_PER_KG = 2100

        # dry fraction mass fat
        MASS_FRACTION_FAT_DRY = .017

        # dry fraction mass digestible protein
        MASS_FRACTION_PROTEIN_DRY = 0.862 * 0.349


        INITIAL_MILK_CATTLE = inputs_to_optimizer["INITIAL_MILK_CATTLE"]
        INIT_SMALL_ANIMALS = inputs_to_optimizer["INIT_SMALL_ANIMALS"]
        INIT_MEDIUM_ANIMALS = inputs_to_optimizer["INIT_MEDIUM_ANIMALS"]

        INIT_LARGE_ANIMALS = inputs_to_optimizer["INIT_LARGE_ANIMALS_WITH_MILK_COWS"] - INITIAL_MILK_CATTLE


        HARVEST_LOSS = 15  # percent (seaweed)

        # 1000 tons (seaweed)
        INITIAL_SEAWEED = inputs_to_optimizer['INITIAL_SEAWEED']

        # 1000 tons (seaweed)
        INITIAL_AREA = inputs_to_optimizer['INITIAL_AREA']
        
        MINIMUM_DENSITY = 400  # tons/km^2 (seaweed)
        MAXIMUM_DENSITY = 800  # tons/km^2 (seaweed)
        MAXIMUM_AREA = 1000  # 1000 km^2 (seaweed)

        SEAWEED_WASTE = inputs_to_optimizer['WASTE']['SEAWEED']

        # seaweed billion kcals per 1000 tons wet
        # convert 1000 tons to kg
        # convert kg to kcals
        # convert kcals to billions of kcals
        # convert wet mass seaweed to dry mass seaweed
        SEAWEED_KCALS = 1e6 * KCALS_PER_KG / 1e9 \
            * WET_TO_DRY_MASS_CONVERSION \
            * (1 - SEAWEED_WASTE / 100)

        # seaweed fraction digestible protein per 1000 ton wet
        SEAWEED_PROTEIN = MASS_FRACTION_PROTEIN_DRY \
            * WET_TO_DRY_MASS_CONVERSION \
            * (1 - SEAWEED_WASTE / 100)

        # seaweed fraction fat per 1000 tons wet
        SEAWEED_FAT = MASS_FRACTION_FAT_DRY \
            * WET_TO_DRY_MASS_CONVERSION \
            * (1 - SEAWEED_WASTE / 100)

        SEAWEED_NEW_AREA_PER_DAY = inputs_to_optimizer['SEAWEED_NEW_AREA_PER_DAY']
        SEAWEED_PRODUCTION_RATE = inputs_to_optimizer['SEAWEED_PRODUCTION_RATE']

        if(inputs_to_optimizer["ADD_SEAWEED"]):
            sd = [INITIAL_AREA] * inputs_to_optimizer["DELAY"]["SEAWEED_MONTHS"] * self.DAYS_IN_MONTH
        else:
            sd = [INITIAL_AREA] * 100000

        built_area_long = np.append(
            np.array(sd),
            np.linspace(
                INITIAL_AREA,
                (NDAYS - 1) * SEAWEED_NEW_AREA_PER_DAY + INITIAL_AREA,
                NDAYS
            )
        )
        built_area_long[built_area_long > MAXIMUM_AREA] = MAXIMUM_AREA
        built_area = built_area_long[0:NDAYS]

        #### STORED FOOD VARIABLES ####

        # (nuclear event in mid-may)
        # Mike's spreadsheet: https://docs.google.com/spreadsheets/d / 19kzHpux690JTCo2IX2UA1faAd7R1QcBK/edit#gid=806987252

        TONS_DRY_CALORIC_EQIVALENT_SF = \
            inputs_to_optimizer['TONS_DRY_CALORIC_EQIVALENT_SF']

        # billion kcals per unit mass initial
        INITIAL_SF_KCALS = TONS_DRY_CALORIC_EQIVALENT_SF * \
            4e6 / 1e9  

        SF_FRACTION_FAT = OG_FRACTION_FAT
        SF_FRACTION_PROTEIN = OG_FRACTION_PROTEIN


        #### FISH ####

        FISH_WASTE = inputs_to_optimizer['WASTE']['SEAFOOD']

        # fish kcals per month, billions
        FISH_KCALS = inputs_to_optimizer["FISH_DRY_CALORIC_ANNUAL"] \
                     * (1 - FISH_WASTE / 100) * 4e6 / 1e9 / 12 

        # units of 1000s tons protein monthly 
        # (so, global value is in the hundreds of thousands of tons)
        FISH_PROTEIN = inputs_to_optimizer["FISH_PROTEIN_TONS_ANNUAL"] \
                       / 1e3 / 12

        # units of 1000s tons fat
        # (so, global value is in the tens of thousands of tons)
        FISH_FAT = inputs_to_optimizer["FISH_FAT_TONS_ANNUAL"] \
                       / 1e3 / 12

        # https://assets.researchsquare.com/files/rs-830419/v1_covered.pdf?c=1631878417

        FISH_PERCENT_EACH_MONTH_LONG = \
            inputs_to_optimizer["FISH_PERCENT_MONTHLY"]

        FISH_PERCENT_EACH_MONTH = FISH_PERCENT_EACH_MONTH_LONG[0:NMONTHS]

        if(ADD_FISH):
            production_kcals_fish_per_month = []
            production_protein_fish_per_month = []
            production_fat_fish_per_month = []
            for x in FISH_PERCENT_EACH_MONTH:
                production_kcals_fish_per_month.append(x / 100 * FISH_KCALS)
                production_protein_fish_per_month.append(
                    x / 100 * FISH_PROTEIN)
                production_fat_fish_per_month.append(x / 100 * FISH_FAT)
        else:
            production_kcals_fish_per_month = \
                [0] * len(FISH_PERCENT_EACH_MONTH)
            production_protein_fish_per_month = \
                [0] * len(FISH_PERCENT_EACH_MONTH)
            production_fat_fish_per_month = \
                [0] * len(FISH_PERCENT_EACH_MONTH)

        ####LIVESTOCK, EGG, DAIRY INITIAL VARIABLES####

        # time from slaughter livestock to it turning into food
        # not functional yet

        # we use this spreadsheeet https://docs.google.com/spreadsheets/d / 1ZyDrGI84TwhXj_QNicwjj9EPWLJ-r3xnAYMzKSAfWc0/edit#gid=824870019

        # edible meat, organs, and fat added
        MEAT_WASTE = inputs_to_optimizer['WASTE']['MEAT']

        KG_PER_SMALL_ANIMAL = 2.36
        KG_PER_MEDIUM_ANIMAL = 24.6
        KG_PER_LARGE_ANIMAL = 269.7

        LARGE_ANIMAL_KCALS_PER_KG = 2750
        LARGE_ANIMAL_FAT_PER_KG = .182
        LARGE_ANIMAL_PROTEIN_PER_KG = .257

        SMALL_ANIMAL_KCALS_PER_KG = 1525
        SMALL_ANIMAL_FAT_PER_KG = 0.076
        SMALL_ANIMAL_PROTEIN_PER_KG = .196

        # https://docs.google.com/spreadsheets/d / 1tLFHJpXTStxyfNojP_Wrj0MQowfyKujJUA37ZG1q6pk/edit#gid=300573673
        # this one uses pigs from FAOstat, unlike the other two
        # roww 264, "Nutrition Data From FAOstat" tab
        MEDIUM_ANIMAL_KCALS_PER_KG = 3590
        MEDIUM_ANIMAL_FAT_PER_KG = .34
        MEDIUM_ANIMAL_PROTEIN_PER_KG = .11

        # DAIRY_PRODUCTION = inputs_to_optimizer['DAIRY_PRODUCTION']
        # DAIRY_WASTE = inputs_to_optimizer['WASTE']['DAIRY']
        # billions of kcals
        # MILK_KCALS_PER_1000_CATTLE_PER_MONTH = ANNUAL_LITERS_PER_COW \
        #     * KCALS_PER_LITER \
        #     / 12 \
        #     / 1e9 \
        #     * 1000 \
        #     * DAIRY_PRODUCTION \
        #     * (1 - DAIRY_WASTE / 100)

        # MILK_KCALS_PER_1000_CATTLE_PER_MONTH = 0.0369 / (1 / 1000 * 1e9 / 4e6) *  (1 - DAIRY_WASTE / 100)
        # https://docs.google.com/spreadsheets/d / 1 - upBP5-iPtBzyjm5zbeGlfuE4FwqLUyR/edit#gid=2007828143
        # per kg, whole milk, per nutrition calculator
        MILK_KCALS = 610  # kcals per kg
        MILK_FAT = .032  # kg per kg
        MILK_PROTEIN = .033  # kg per kg

        ######## Human Inedible Produced Primary Dairy and Cattle Meat #########
        # 'integrated model 150 tg' tab https://docs.google.com/spreadsheets/d / 1rYcxSe-Z7ztvW-QwTBXT8GABaRmVdDuQ05HXmTHbQ8I/edit#gid=1141282747
        human_inedible_feed = inputs_to_optimizer['HUMAN_INEDIBLE_FEED']

        # dry caloric ton feed/ton milk
        INEDIBLE_TO_DAIRY_CONVERSION = 1.44

        # dry caloric ton feed/ton cattle
        # INEDIBLE_TO_CATTLE_CONVERSION = 103.0
        INEDIBLE_TO_CATTLE_CONVERSION = 92.6

        # monthly in tons milk (present day value)
        DAIRY_LIMIT = inputs_to_optimizer['TONS_DAIRY_ANNUAL'] / 12
        # CHICKEN_PORK_LIMIT = 250e6 / 12

        # monthly in dry caloric tons inedible feed
        DAIRY_LIMIT_FEED_USAGE = DAIRY_LIMIT * INEDIBLE_TO_DAIRY_CONVERSION

        dairy_milk_produced = []  # tons
        cattle_maintained = []  # tons
        for m in range(0, NMONTHS):
            if(ADD_DAIRY):
                max_dairy = human_inedible_feed[m] \
                    / INEDIBLE_TO_DAIRY_CONVERSION
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

            if(ADD_MEAT):
                cattle_maintained.append(
                    inedible_for_cattle / INEDIBLE_TO_CATTLE_CONVERSION)
            else:
                cattle_maintained.append(0)

        h_e_fed_dairy_limit = DAIRY_LIMIT - np.array(dairy_milk_produced)

        if(ADD_MEAT):

            # billions kcals
            cattle_maintained_kcals = np.array(cattle_maintained)\
                * 1000  \
                * LARGE_ANIMAL_KCALS_PER_KG \
                / 1e9\
                * (1 - MEAT_WASTE / 100)

            # 1000s tons fat
            cattle_maintained_fat = cattle_maintained_kcals * 1e9 \
                * LARGE_ANIMAL_FAT_PER_KG / LARGE_ANIMAL_KCALS_PER_KG / 1e6

            # 1000s tons protein
            cattle_maintained_protein = cattle_maintained_kcals * 1e9 \
                * LARGE_ANIMAL_PROTEIN_PER_KG / LARGE_ANIMAL_KCALS_PER_KG / 1e6

        else:
            cattle_maintained_kcals = [0] * len(cattle_maintained)
            cattle_maintained_fat = [0] * len(cattle_maintained)
            cattle_maintained_protein = [0] * len(cattle_maintained)

        #### Delayed shutoff BIOFUELS and FEED ####
        # "Monthly flows" tab https://docs.google.com/spreadsheets/d / 1tLFHJpXTStxyfNojP_Wrj0MQowfyKujJUA37ZG1q6pk/edit#gid=1714403726

        biofuel_delay = inputs_to_optimizer["DELAY"]["BIOFUEL_SHUTOFF_MONTHS"]
        biofuels_kcals = [self.BIOFUEL_MONTHLY_USAGE_KCALS] * \
            biofuel_delay + [0] * (NMONTHS-biofuel_delay)
        biofuels_fat = [self.BIOFUEL_MONTHLY_USAGE_FAT] * \
            biofuel_delay + [0] * (NMONTHS-biofuel_delay)
        biofuels_protein = [self.BIOFUEL_MONTHLY_USAGE_PROTEIN] * \
            biofuel_delay + [0] * (NMONTHS-biofuel_delay)

        feed_shutoff_delay_months = inputs_to_optimizer["DELAY"]["FEED_SHUTOFF_MONTHS"]
        self.feed_shutoff_kcals = np.array(
            [self.FEED_MONTHLY_USAGE_KCALS] * feed_shutoff_delay_months + [0] * (NMONTHS-feed_shutoff_delay_months))
        feed_shutoff_fat = np.array(
            [self.FEED_MONTHLY_USAGE_FAT] * feed_shutoff_delay_months + [0] * (NMONTHS-feed_shutoff_delay_months))
        feed_shutoff_protein = np.array(
            [self.FEED_MONTHLY_USAGE_PROTEIN] * feed_shutoff_delay_months + [0] * (NMONTHS-feed_shutoff_delay_months))

        KG_TO_1000_TONS = self.KG_TO_1000_TONS

        KCALS_PER_SMALL_ANIMAL = SMALL_ANIMAL_KCALS_PER_KG * KG_PER_SMALL_ANIMAL / 1e9
        FAT_PER_SMALL_ANIMAL = SMALL_ANIMAL_FAT_PER_KG * \
            KG_PER_SMALL_ANIMAL * KG_TO_1000_TONS
        PROTEIN_PER_SMALL_ANIMAL = SMALL_ANIMAL_PROTEIN_PER_KG * \
            KG_PER_SMALL_ANIMAL * KG_TO_1000_TONS

        KCALS_PER_MEDIUM_ANIMAL = MEDIUM_ANIMAL_KCALS_PER_KG * KG_PER_MEDIUM_ANIMAL / 1e9
        FAT_PER_MEDIUM_ANIMAL = MEDIUM_ANIMAL_FAT_PER_KG * \
            KG_PER_MEDIUM_ANIMAL * KG_TO_1000_TONS
        PROTEIN_MEDIUM_ANIMAL = MEDIUM_ANIMAL_PROTEIN_PER_KG * \
            KG_PER_MEDIUM_ANIMAL * KG_TO_1000_TONS

        KCALS_PER_LARGE_ANIMAL = LARGE_ANIMAL_KCALS_PER_KG * KG_PER_LARGE_ANIMAL / 1e9
        FAT_PER_LARGE_ANIMAL = LARGE_ANIMAL_FAT_PER_KG * \
            KG_PER_LARGE_ANIMAL * KG_TO_1000_TONS
        PROTEIN_PER_LARGE_ANIMAL = LARGE_ANIMAL_PROTEIN_PER_KG * \
            KG_PER_LARGE_ANIMAL * KG_TO_1000_TONS

        ###### Human Edible Produced "Secondary" Dairy and Cattle Meat #######
        CHICKEN_AND_PORK_LIMIT = inputs_to_optimizer['TONS_CHICKEN_AND_PORK_ANNUAL'] / 12  # tons meat per month

        # https://docs.google.com/document/d / 1HlML7ptYmRfNJjko5qMfIJJGyLRUBlnCIiEiBMr41cM/edit#heading=h.7wiajnpimw8t
        def get_meat_milk_from_excess(excess_kcals, h_e_fed_dairy_limit):

            # each unit of excess kcals (with associated fat and protein)
            # are fed first to dairy, then to pigs and chickens, then to cattle

            excess_dry_cal_tons = excess_kcals * 1e9 / 4e6
            if(np.array(excess_dry_cal_tons < 0).any()):
                print("excess_dry_cal_tons per month")
                print(excess_dry_cal_tons)
                print("It appears assigning excess calories to feed or biofuels was attempted, but there were not enough calories to use for the feed and biofuel (because of this, excess was calculated as being negative). \nTry to rerun where the population fed after waste incorporating delayed shutoff to feed in biofuels is above the assigned global population. \nQuitting.")
                quit()
            assert(np.array(excess_dry_cal_tons >= 0).all())

            # dry caloric ton excess/ton milk
            EDIBLE_TO_DAIRY_CONVERSION = 0.7

            h_e_fed_dairy_limit_food_usage = h_e_fed_dairy_limit\
                * EDIBLE_TO_DAIRY_CONVERSION

            # dry caloric ton excess/ton meat
            CHICKEN_PORK_CONVERSION = 4.8

            # monthly in dry caloric tons inedible feed
            CHICKEN_PORK_LIMIT_FOOD_USAGE = CHICKEN_AND_PORK_LIMIT\
                * CHICKEN_PORK_CONVERSION

            # dry caloric ton excess/ton meat
            EDIBLE_TO_CATTLE_CONVERSION = 9.8
            dairy_h_e = []
            chicken_pork_maintained = []
            cattle_h_e_maintained = []
            for m in range(0, NMONTHS):

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

                assert(for_chicken_pork_cattle >= 0)

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
                cattle_h_e_maintained.append(
                    for_cattle/EDIBLE_TO_CATTLE_CONVERSION)
                # cattle_h_e_maintained.append(0)

            present_day_tons_per_month_cattle = inputs_to_optimizer['TONS_BEEF_ANNUAL'] / 12  # tons a month meat
            present_day_tons_per_month_chicken_pork = \
                CHICKEN_AND_PORK_LIMIT  # tons a month

            # does not consider waste
            ratio_maintained_cattle = (np.array(
                cattle_maintained) + np.array(cattle_h_e_maintained)) / present_day_tons_per_month_cattle
            ratio_not_maintained_cattle = 1 - ratio_maintained_cattle

            # make sure for the months we really care about we're not exceeding present-day cattle meat maintained production
            # assert((ratio_maintained_cattle <= 1)[0:47].all())
            if((ratio_maintained_cattle[0:47] >= 1).any()):
                print("")
                print(
                    "WARNING: cattle maintained is exceeding 2020 baseline levels in months:")
                print(np.where(ratio_maintained_cattle[0:47] >= 1))
                print(
                    "Consider whether the predicted amount of human edible feed fed to animals is reasonable.")
                print("")

            ratio_not_maintained_cattle[ratio_not_maintained_cattle < 0] = 0

            # does not consider waste
            ratio_maintained_chicken_pork = np.array(
                chicken_pork_maintained) / present_day_tons_per_month_chicken_pork
            if(not (ratio_maintained_chicken_pork <= 1).all()):
                print("DIRE, DIRE WARNING!!")

            # assert((ratio_maintained_chicken_pork <= 1).all())
            assert((np.array(dairy_h_e) >= 0).all())

            # limit the rate of livestock culling by how long it takes to reduce the maintained livestock to its minimum.

            # chicken pork assumed to maintain ratio between medium and small animal mass
            small_to_medium_ratio \
                = INIT_SMALL_ANIMALS * KG_PER_SMALL_ANIMAL \
                / (INIT_MEDIUM_ANIMALS * KG_PER_MEDIUM_ANIMAL + INIT_SMALL_ANIMALS * KG_PER_SMALL_ANIMAL)

            # billions kcals monthly
            chicken_pork_kcals = np.array(chicken_pork_maintained) * 1e3\
                * (SMALL_ANIMAL_KCALS_PER_KG * small_to_medium_ratio
                   + MEDIUM_ANIMAL_KCALS_PER_KG * (1 - small_to_medium_ratio))\
                / 1e9

            # thousands tons monthly
            chicken_pork_fat = np.array(chicken_pork_maintained) * 1e3\
                * (SMALL_ANIMAL_FAT_PER_KG * small_to_medium_ratio
                   + MEDIUM_ANIMAL_FAT_PER_KG * (1 - small_to_medium_ratio))\
                / 1e6

            # thousands tons monthly
            chicken_pork_protein = np.array(chicken_pork_maintained) * 1e3\
                * (SMALL_ANIMAL_PROTEIN_PER_KG * small_to_medium_ratio
                + MEDIUM_ANIMAL_PROTEIN_PER_KG * (1 - small_to_medium_ratio))\
                / 1e6

            # billions kcals monthly
            cattle_h_e_maintained_kcals = np.array(cattle_h_e_maintained)\
                * 1000  \
                * LARGE_ANIMAL_KCALS_PER_KG \
                / 1e9

            # 1000s tons fat
            cattle_h_e_maintained_fat = cattle_h_e_maintained_kcals * 1e9 \
                / LARGE_ANIMAL_KCALS_PER_KG * LARGE_ANIMAL_FAT_PER_KG / 1e6

            # 1000s tons protein
            cattle_h_e_maintained_protein = cattle_h_e_maintained_kcals * 1e9 \
                / LARGE_ANIMAL_KCALS_PER_KG * LARGE_ANIMAL_PROTEIN_PER_KG / 1e6

            h_e_meat_kcals = \
                np.array(cattle_h_e_maintained_kcals + chicken_pork_kcals) \
                * (1 - MEAT_WASTE / 100)
            h_e_meat_fat = \
                np.array(cattle_h_e_maintained_fat + chicken_pork_fat) \
                * (1 - MEAT_WASTE / 100)
            h_e_meat_protein = \
                np.array(cattle_h_e_maintained_protein + chicken_pork_protein)\
                * (1 - MEAT_WASTE / 100)

            if(inputs_to_optimizer["CULL_ANIMALS"]):
                INIT_SMALL_ANIMALS_CULLED  \
                    = INIT_SMALL_ANIMALS \
                    * (1 - np.min(ratio_maintained_chicken_pork))
                INIT_MEDIUM_ANIMALS_CULLED  \
                    = INIT_MEDIUM_ANIMALS \
                    * (1 - np.min(ratio_maintained_chicken_pork))
                INIT_LARGE_ANIMALS_CULLED  \
                    = INIT_LARGE_ANIMALS \
                    * np.max(ratio_not_maintained_cattle)
            else:
                INIT_SMALL_ANIMALS_CULLED = 0
                INIT_MEDIUM_ANIMALS_CULLED = 0
                INIT_LARGE_ANIMALS_CULLED = 0

            return (small_to_medium_ratio,
                    INIT_SMALL_ANIMALS_CULLED,
                    INIT_MEDIUM_ANIMALS_CULLED,
                    INIT_LARGE_ANIMALS_CULLED,
                    chicken_pork_kcals,
                    chicken_pork_fat,
                    chicken_pork_protein,
                    h_e_meat_kcals,
                    h_e_meat_fat,
                    h_e_meat_protein,
                    np.array(dairy_h_e),
                    ratio_maintained_chicken_pork,
                    ratio_maintained_cattle,
                    ratio_not_maintained_cattle,
                    cattle_h_e_maintained)

        # assume animals need and use human levels of fat and protein per kcal
        # units grams per kcal same as units 1000s tons per billion kcals
        fat_used_ls = inputs_to_optimizer['NUTRITION']['FAT_DAILY'] / \
            inputs_to_optimizer['NUTRITION']['KCALS_DAILY']

        protein_used_ls = inputs_to_optimizer['NUTRITION']['PROTEIN_DAILY'] / \
            inputs_to_optimizer['NUTRITION']['KCALS_DAILY']

        nonshutoff_excess_fat_used = fat_used_ls * \
            inputs_to_optimizer["EXCESS_CALORIES"]

        nonshutoff_excess_protein_used = protein_used_ls * \
            inputs_to_optimizer["EXCESS_CALORIES"]

        # totals human edible used for animal feed and biofuels
        # excess is directly supplied separately from the feed_shutoff used.

        excess_kcals = inputs_to_optimizer["EXCESS_CALORIES"] \
            + biofuels_kcals \
            + self.feed_shutoff_kcals

        excess_fat_used = nonshutoff_excess_fat_used\
            + biofuels_fat \
            + feed_shutoff_fat

        excess_protein_used = nonshutoff_excess_protein_used\
            + biofuels_protein \
            + feed_shutoff_protein

        kcals_fed_to_animals = inputs_to_optimizer["EXCESS_CALORIES"]\
            + self.feed_shutoff_kcals

        (small_to_medium_ratio,
         INIT_SMALL_ANIMALS_CULLED,
         INIT_MEDIUM_ANIMALS_CULLED,
         INIT_LARGE_ANIMALS_CULLED,
         self.chicken_pork_kcals,
         self.chicken_pork_fat,
         self.chicken_pork_protein,
         h_e_meat_kcals,
         h_e_meat_fat,
         h_e_meat_protein,
         h_e_fed_dairy_produced,
         ratio_maintained_chicken_pork,
         ratio_maintained_cattle,
         ratio_not_maintained_cattle,
         self.cattle_h_e_maintained) = get_meat_milk_from_excess(kcals_fed_to_animals, h_e_fed_dairy_limit)


        INIT_MEAT_KCALS = \
            INIT_SMALL_ANIMALS_CULLED * KCALS_PER_SMALL_ANIMAL \
            + INIT_MEDIUM_ANIMALS_CULLED * KCALS_PER_MEDIUM_ANIMAL \
            + INIT_LARGE_ANIMALS_CULLED * KCALS_PER_LARGE_ANIMAL
        INIT_MEAT_FAT = \
            INIT_SMALL_ANIMALS_CULLED * FAT_PER_SMALL_ANIMAL \
            + INIT_MEDIUM_ANIMALS_CULLED * FAT_PER_MEDIUM_ANIMAL \
            + INIT_LARGE_ANIMALS_CULLED * FAT_PER_LARGE_ANIMAL
        INIT_MEAT_PROTEIN = \
            INIT_SMALL_ANIMALS_CULLED * PROTEIN_PER_SMALL_ANIMAL \
            + INIT_MEDIUM_ANIMALS_CULLED * PROTEIN_MEDIUM_ANIMAL \
            + INIT_LARGE_ANIMALS_CULLED * PROTEIN_PER_LARGE_ANIMAL

        INITIAL_MEAT = INIT_MEAT_KCALS \
            * (1 - MEAT_WASTE / 100)

        if(INITIAL_MEAT > 0):
            MEAT_FRACTION_FAT = INIT_MEAT_FAT \
                / INIT_MEAT_KCALS
            MEAT_FRACTION_PROTEIN = INIT_MEAT_PROTEIN \
                / INIT_MEAT_KCALS
        else:
            MEAT_FRACTION_FAT = 0
            MEAT_FRACTION_PROTEIN = 0

        if(inputs_to_optimizer['CULL_ANIMALS']):
            CULL_DURATION_MONTHS = inputs_to_optimizer["CULL_DURATION_MONTHS"]
            if(CULL_DURATION_MONTHS != 0):
                meat_culled =\
                    [0] * feed_shutoff_delay_months\
                    + [INITIAL_MEAT / CULL_DURATION_MONTHS] * CULL_DURATION_MONTHS\
                    + [0] * (NMONTHS - CULL_DURATION_MONTHS - feed_shutoff_delay_months)

            else:
                meat_culled = [0] * NMONTHS
        else:
            CULL_DURATION_MONTHS = 0
            meat_culled = [0] * NMONTHS

        if(not inputs_to_optimizer["CULL_ANIMALS"]):
            assert(max(meat_culled)==0)

        if(VERBOSE):
            print("CULL_DURATION_MONTHS")
            print(CULL_DURATION_MONTHS)

        if(not ADD_MEAT):
            h_e_meat_kcals = np.array([0] * NMONTHS)
            h_e_meat_fat = np.array([0] * NMONTHS)
            h_e_meat_protein = np.array([0] * NMONTHS)
            CULL_DURATION_MONTHS = 0
            meat_culled = [0] * NMONTHS

            
        if(not ADD_DAIRY):
            h_e_fed_dairy_produced = np.array([0] * NMONTHS)

        DAIRY_WASTE = inputs_to_optimizer['WASTE']['DAIRY']
        if(ADD_DAIRY):

            # billions kcals
            dairy_milk_kcals = np.array(dairy_milk_produced) * 1e3\
                * MILK_KCALS / 1e9 * (1 - DAIRY_WASTE / 100)

            h_e_milk_kcals = h_e_fed_dairy_produced * 1e3\
                * MILK_KCALS / 1e9 * (1 - DAIRY_WASTE / 100)

            # thousands tons
            dairy_milk_fat = np.array(dairy_milk_produced) / 1e3\
                * MILK_FAT * (1 - DAIRY_WASTE / 100)

            h_e_milk_fat = h_e_fed_dairy_produced / 1e3\
                * MILK_FAT * (1 - DAIRY_WASTE / 100)

            # thousands tons
            dairy_milk_protein = np.array(dairy_milk_produced) / 1e3\
                * MILK_PROTEIN * (1 - DAIRY_WASTE / 100)

            h_e_milk_protein = h_e_fed_dairy_produced / 1e3\
                * MILK_PROTEIN * (1 - DAIRY_WASTE / 100)

        else:
            dairy_milk_kcals = np.array([0] * NMONTHS)
            dairy_milk_fat = np.array([0] * NMONTHS)
            dairy_milk_protein = np.array([0] * NMONTHS)

            h_e_milk_kcals = np.array([0] * NMONTHS)
            h_e_milk_fat = np.array([0] * NMONTHS)
            h_e_milk_protein = np.array([0] * NMONTHS)

        h_e_created_kcals = h_e_meat_kcals + h_e_milk_kcals
        h_e_created_fat = h_e_meat_fat + h_e_milk_fat
        h_e_created_protein = h_e_meat_protein + h_e_milk_protein

        CROP_WASTE = 1 - inputs_to_optimizer["WASTE"]["CROPS"] / 100

        h_e_balance_kcals = -excess_kcals * CROP_WASTE \
            + h_e_created_kcals
        h_e_balance_fat = -excess_fat_used * CROP_WASTE \
            + h_e_created_fat
        h_e_balance_protein = -excess_protein_used * CROP_WASTE \
            + h_e_created_protein

        #### CROP PRODUCTION VARIABLES ####
        # assumption: outdoor crop production is very similar in nutritional
        # profile to stored food
        # reference: row 11, 'outputs' tab  https://docs.google.com/spreadsheets/d / 19kzHpux690JTCo2IX2UA1faAd7R1QcBK/edit#gid=1815939673

        JAN_FRACTION = inputs_to_optimizer['SEASONALITY'][0]
        FEB_FRACTION = inputs_to_optimizer['SEASONALITY'][1]
        MAR_FRACTION = inputs_to_optimizer['SEASONALITY'][2]
        APR_FRACTION = inputs_to_optimizer['SEASONALITY'][3]
        MAY_FRACTION = inputs_to_optimizer['SEASONALITY'][4]
        JUN_FRACTION = inputs_to_optimizer['SEASONALITY'][5]
        JUL_FRACTION = inputs_to_optimizer['SEASONALITY'][6]
        AUG_FRACTION = inputs_to_optimizer['SEASONALITY'][7]
        SEP_FRACTION = inputs_to_optimizer['SEASONALITY'][8]
        OCT_FRACTION = inputs_to_optimizer['SEASONALITY'][9]
        NOV_FRACTION = inputs_to_optimizer['SEASONALITY'][10]
        DEC_FRACTION = inputs_to_optimizer['SEASONALITY'][11]

        JAN_YIELD = JAN_FRACTION * ANNUAL_YIELD  # tonnes dry carb equivalent
        FEB_YIELD = FEB_FRACTION * ANNUAL_YIELD  # tonnes dry carb equivalent
        MAR_YIELD = MAR_FRACTION * ANNUAL_YIELD  # tonnes dry carb equivalent
        APR_YIELD = APR_FRACTION * ANNUAL_YIELD  # tonnes dry carb equivalent
        MAY_YIELD = MAY_FRACTION * ANNUAL_YIELD  # tonnes dry carb equivalent
        JUN_YIELD = JUN_FRACTION * ANNUAL_YIELD  # tonnes dry carb equivalent
        JUL_YIELD = JUL_FRACTION * ANNUAL_YIELD  # tonnes dry carb equivalent
        AUG_YIELD = AUG_FRACTION * ANNUAL_YIELD  # tonnes dry carb equivalent
        SEP_YIELD = SEP_FRACTION * ANNUAL_YIELD  # tonnes dry carb equivalent
        OCT_YIELD = OCT_FRACTION * ANNUAL_YIELD  # tonnes dry carb equivalent
        NOV_YIELD = NOV_FRACTION * ANNUAL_YIELD  # tonnes dry carb equivalent
        DEC_YIELD = DEC_FRACTION * ANNUAL_YIELD  # tonnes dry carb equivalent

        # billions of kcals
        JAN_KCALS_OG = JAN_YIELD * 4e6 / 1e9
        FEB_KCALS_OG = FEB_YIELD * 4e6 / 1e9
        MAR_KCALS_OG = MAR_YIELD * 4e6 / 1e9
        APR_KCALS_OG = APR_YIELD * 4e6 / 1e9
        MAY_KCALS_OG = MAY_YIELD * 4e6 / 1e9
        JUN_KCALS_OG = JUN_YIELD * 4e6 / 1e9
        JUL_KCALS_OG = JUL_YIELD * 4e6 / 1e9
        AUG_KCALS_OG = AUG_YIELD * 4e6 / 1e9
        SEP_KCALS_OG = SEP_YIELD * 4e6 / 1e9
        OCT_KCALS_OG = OCT_YIELD * 4e6 / 1e9
        NOV_KCALS_OG = NOV_YIELD * 4e6 / 1e9
        DEC_KCALS_OG = DEC_YIELD * 4e6 / 1e9

        KCALS_PREDISASTER_BEFORE_MAY = JAN_KCALS_OG + \
            FEB_KCALS_OG+MAR_KCALS_OG+APR_KCALS_OG+MAY_KCALS_OG
        KCALS_PREDISASTER_AFTER_MAY = JUN_KCALS_OG+JUL_KCALS_OG + \
            AUG_KCALS_OG+SEP_KCALS_OG+OCT_KCALS_OG+NOV_KCALS_OG+DEC_KCALS_OG

        KCALS_PREDISASTER_ANNUAL = JAN_KCALS_OG+FEB_KCALS_OG+MAR_KCALS_OG+APR_KCALS_OG+MAY_KCALS_OG + \
            JUN_KCALS_OG+JUL_KCALS_OG+AUG_KCALS_OG+SEP_KCALS_OG + \
            OCT_KCALS_OG+NOV_KCALS_OG+DEC_KCALS_OG

        RATIO_KCALS_POSTDISASTER_1Y = \
            1 - inputs_to_optimizer["DISRUPTION_CROPS_YEAR1"]
        RATIO_KCALS_POSTDISASTER_2Y = \
            1 - inputs_to_optimizer["DISRUPTION_CROPS_YEAR2"]
        RATIO_KCALS_POSTDISASTER_3Y = \
            1 - inputs_to_optimizer["DISRUPTION_CROPS_YEAR3"]
        RATIO_KCALS_POSTDISASTER_4Y = \
            1 - inputs_to_optimizer["DISRUPTION_CROPS_YEAR4"]
        RATIO_KCALS_POSTDISASTER_5Y = \
            1 - inputs_to_optimizer["DISRUPTION_CROPS_YEAR5"]
        RATIO_KCALS_POSTDISASTER_6Y = \
            1 - inputs_to_optimizer["DISRUPTION_CROPS_YEAR6"]
        RATIO_KCALS_POSTDISASTER_7Y = \
            1 - inputs_to_optimizer["DISRUPTION_CROPS_YEAR7"]
        RATIO_KCALS_POSTDISASTER_8Y = \
            1 - inputs_to_optimizer["DISRUPTION_CROPS_YEAR8"]
        RATIO_KCALS_POSTDISASTER_9Y = \
            1 - inputs_to_optimizer["DISRUPTION_CROPS_YEAR9"]
        RATIO_KCALS_POSTDISASTER_10Y = \
            1 - inputs_to_optimizer["DISRUPTION_CROPS_YEAR10"]
        RATIO_KCALS_POSTDISASTER_11Y = \
            1 - inputs_to_optimizer["DISRUPTION_CROPS_YEAR11"]

        first_year_jan_to_may = [1, 1, 1, 1, 1]
        jun_y1_to_may_y2 = np.linspace(1, RATIO_KCALS_POSTDISASTER_1Y, 13)[1:]
        jun_y2_to_may_y3 = np.linspace(
            RATIO_KCALS_POSTDISASTER_1Y, RATIO_KCALS_POSTDISASTER_2Y, 13)[1:]
        jun_y3_to_may_y4 = np.linspace(
            RATIO_KCALS_POSTDISASTER_2Y, RATIO_KCALS_POSTDISASTER_3Y, 13)[1:]
        jun_y4_to_may_y5 = np.linspace(
            RATIO_KCALS_POSTDISASTER_3Y, RATIO_KCALS_POSTDISASTER_4Y, 13)[1:]
        jun_y5_to_may_y6 = np.linspace(
            RATIO_KCALS_POSTDISASTER_4Y, RATIO_KCALS_POSTDISASTER_5Y, 13)[1:]
        jun_y6_to_may_y7 = np.linspace(
            RATIO_KCALS_POSTDISASTER_5Y, RATIO_KCALS_POSTDISASTER_6Y, 13)[1:]
        jun_y7_to_may_y8 = np.linspace(
            RATIO_KCALS_POSTDISASTER_6Y, RATIO_KCALS_POSTDISASTER_7Y, 13)[1:]
        jun_y8_to_may_y9 = np.linspace(
            RATIO_KCALS_POSTDISASTER_7Y, RATIO_KCALS_POSTDISASTER_8Y, 13)[1:]
        jun_y9_to_may_y10 = np.linspace(
            RATIO_KCALS_POSTDISASTER_8Y, RATIO_KCALS_POSTDISASTER_9Y, 13)[1:]
        jun_y10_to_may_y11 = np.linspace(
            RATIO_KCALS_POSTDISASTER_9Y, RATIO_KCALS_POSTDISASTER_10Y, 13)[1:]
        jun_y11_to_dec_y11 = np.linspace(
            RATIO_KCALS_POSTDISASTER_10Y, RATIO_KCALS_POSTDISASTER_11Y, 13)[1:8]

        all_months_reductions = np.array(first_year_jan_to_may
                                         + list(jun_y1_to_may_y2)
                                         + list(jun_y2_to_may_y3)
                                         + list(jun_y3_to_may_y4)
                                         + list(jun_y4_to_may_y5)
                                         + list(jun_y5_to_may_y6)
                                         + list(jun_y6_to_may_y7)
                                         + list(jun_y7_to_may_y8)
                                         + list(jun_y8_to_may_y9)
                                         + list(jun_y9_to_may_y10)
                                         + list(jun_y10_to_may_y11)
                                         + list(jun_y11_to_dec_y11))\

        assert(len(all_months_reductions) == 12 * 11)


        months_cycle = [MAY_KCALS_OG, JUN_KCALS_OG, JUL_KCALS_OG, AUG_KCALS_OG, SEP_KCALS_OG,
                        OCT_KCALS_OG, NOV_KCALS_OG, DEC_KCALS_OG, JAN_KCALS_OG, FEB_KCALS_OG, MAR_KCALS_OG, APR_KCALS_OG]

        # need to use the multiplier on units of kcals to get fat and protein
        if(inputs_to_optimizer["OG_USE_BETTER_ROTATION"]):

            # deals with the issue of caloric improvement being more than present-day production during the beginning months of the simulation.
            OG_KCAL_REDUCED = inputs_to_optimizer["ROTATION_IMPROVEMENTS"]["KCALS_REDUCTION"]

            OG_ROTATION_FRACTION_KCALS = 1

            KCAL_RATIO_ROT = 1
            FAT_ROTATION_RATIO = inputs_to_optimizer["ROTATION_IMPROVEMENTS"]["FAT_RATIO"]
            PROTEIN_ROTATION_RATIO = inputs_to_optimizer["ROTATION_IMPROVEMENTS"]["PROTEIN_RATIO"]

            OG_ROTATION_FRACTION_FAT = OG_FRACTION_FAT * FAT_ROTATION_RATIO
            OG_ROTATION_FRACTION_PROTEIN = OG_FRACTION_PROTEIN * PROTEIN_ROTATION_RATIO

            FAT_RATIO_ROT = OG_ROTATION_FRACTION_FAT
            PROTEIN_RATIO_ROT = OG_ROTATION_FRACTION_PROTEIN

        else:
            OG_KCAL_REDUCED = 1
            OG_ROTATION_FRACTION_KCALS = 1
            OG_ROTATION_FRACTION_FAT = OG_FRACTION_FAT
            OG_ROTATION_FRACTION_PROTEIN = OG_FRACTION_PROTEIN

            KCAL_RATIO_ROT = 1
            FAT_RATIO_ROT = OG_FRACTION_FAT
            PROTEIN_RATIO_ROT = OG_FRACTION_PROTEIN

        KCALS_GROWN = []
        NO_ROT_KCALS_GROWN = []
        print(OG_KCAL_REDUCED)

        for i in range(0, NMONTHS):
            cycle_index = i % 12
            month_kcals = months_cycle[cycle_index]
            print("months_kcals")
            print(month_kcals)
            print("all_months_reductions")
            # return months_cycle[0]
            # print(months_cycle)
            KCALS_GROWN.append(
                month_kcals * (1 - (
                    OG_KCAL_REDUCED
                    * (1 - all_months_reductions[i+4])
                ))
            )
            NO_ROT_KCALS_GROWN.append(
                month_kcals * (1 - (
                    (1 - all_months_reductions[i+4])
                ))
            )

        CROP_WASTE = inputs_to_optimizer['WASTE']['CROPS']

        # we know:
        #     units_sf_mass * SF_FRACTION_KCALS=sf_kcals
        # and
        #     units_sf_mass * SF_FRACTION_PROTEIN=sf_protein
        # so
        #     units_sf_mass = sf_kcals/SF_FRACTION_KCALS
        # => assumption listed previously =>
        #     units_og_mass = og_kcals/SF_FRACTION_KCALS
        #     units_og_mass = og_protein/SF_FRACTION_PROTEIN
        # therefore
        #     og_protein = og_kcals * SF_FRACTION_PROTEIN/SF_FRACTION_KCALS

        #### CONSTANTS FOR GREENHOUSES ####
        # greenhouses tab
        # assumption: greenhouse crop production is very similar in nutritional
        # profile to stored food
        # reference: see https://docs.google.com/spreadsheets/d / 1f9eVD14Y2d9vmLFP3OsJPFA5d2JXBU-63MTz8MlB1rY/edit#gid=756212200
        # greenhouse paper (scaling of greenhouses in low sunlight scenarios)
        # At constant expansion for 36 months, the cumulative ground coverage
        # will equal 2.5 million km^2 (250 million hectares).
        # Takes 5+36=41 months to reach full output
        # NOTE: the 5 months represents the delay from plant to harvest.

        if(ADD_GREENHOUSES):
            GREENHOUSE_AREA_MULTIPLIER = inputs_to_optimizer['GREENHOUSE_AREA_MULTIPLIER']
            GREENHOUSE_LIMIT_AREA = self.TOTAL_CROP_AREA * GREENHOUSE_AREA_MULTIPLIER
            # past the 5 month delay till harvest
            greenhouse_delay = inputs_to_optimizer["DELAY"]["GREENHOUSE_MONTHS"]

            greenhouse_area_long = \
                list(
                    np.append(
                        np.append(
                            np.append(np.linspace(0, 0, greenhouse_delay),
                                      np.linspace(0, 0, 5)),
                            np.linspace(0, GREENHOUSE_LIMIT_AREA, 37)
                        ),
                        np.linspace(GREENHOUSE_LIMIT_AREA,
                                    GREENHOUSE_LIMIT_AREA, len(KCALS_GROWN) - 42)
                    )
                )\

            greenhouse_area = np.array(greenhouse_area_long[0:NMONTHS])
            print("CANT DEAL TOTAL CROPS SAD")
            quit()

            MONTHLY_KCALS = np.mean(months_cycle) / self.TOTAL_CROP_AREA

            KCALS_GROWN_PER_HECTARE_BEFORE_WASTE = \
                MONTHLY_KCALS * (1 - (
                    (1 - all_months_reductions[4:])
                    * OG_KCAL_REDUCED
                ))

            KCALS_GROWN_PER_HECTARE = (1 - CROP_WASTE / 100) \
                * np.array(KCALS_GROWN_PER_HECTARE_BEFORE_WASTE)
        else:
            KCALS_GROWN_PER_HECTARE = [0] * NMONTHS
            greenhouse_area = np.array([0] * NMONTHS)

        if(ADD_OUTDOOR_GROWING):
            if(inputs_to_optimizer["OG_USE_BETTER_ROTATION"]):
                crops_food_produced = np.array([0] * NMONTHS)
                # print(crops_food_produced[0] * 1e9 / 4e6 / 1e6)
                # quit()
                hd = inputs_to_optimizer["INITIAL_HARVEST_DURATION_IN_MONTHS"] + \
                    inputs_to_optimizer["DELAY"]["ROTATION_CHANGE_IN_MONTHS"]

                crops_food_produced[hd:] = \
                    np.multiply(np.array(KCALS_GROWN[hd:]),
                                (1 - greenhouse_area[hd:]/self.TOTAL_CROP_AREA))

                crops_food_produced[:hd] = \
                    np.multiply(np.array(NO_ROT_KCALS_GROWN[:hd]),
                                (1 - greenhouse_area[:hd]/self.TOTAL_CROP_AREA))

                print("CANT DEAL TOTAL CROPS SAD")
                quit()

            else:
                crops_food_produced = \
                    np.array(NO_ROT_KCALS_GROWN)

        else:
            crops_food_produced = np.array([0] * NMONTHS)

        # we know:
        #     units_sf_mass * SF_FRACTION_KCALS=sf_kcals
        # and
        #     units_sf_mass * SF_FRACTION_PROTEIN=sf_protein
        # so
        #     units_sf_mass = sf_kcals/SF_FRACTION_KCALS
        # => assumption listed previously =>
        #     units_gh_mass = gh_kcals/SF_FRACTION_KCALS
        #     units_gh_mass = gh_protein/SF_FRACTION_PROTEIN
        # therefore
        #     gh_protein = gh_kcals * SF_FRACTION_PROTEIN/SF_FRACTION_KCALS
        # mass initial, units don't matter, we only need to ensure we use the correct
        # fraction of kcals, fat, and protein per unit initial stored food.

        # for the conversions and numbers, go here
        # https://docs.google.com/document/d / 1HlML7ptYmRfNJjko5qMfIJJGyLRUBlnCIiEiBMr41cM/edit#
        # and here
        # https://docs.google.com/spreadsheets/d / 1rYcxSe-Z7ztvW-QwTBXT8GABaRmVdDuQ05HXmTHbQ8I/edit#gid=1141282747

        # SUM_CALORIES is an overestimate by some factor, as it is in current
        # day conditions. We improve accuracy by applying the outdoor growing
        # estimate and decreasing the estimated fat and protein by the same
        # factor that kcals are decreased by
        def get_greenhouse_yield_per_ha(KCAL_RATIO, FAT_RATIO, PROTEIN_RATIO):

            rotation_fat_per_ha_long = []
            rotation_protein_per_ha_long = []
            rotation_kcals_per_ha_long = []
            for kcals_per_month in KCALS_GROWN_PER_HECTARE:
                gh_kcals = kcals_per_month * KCAL_RATIO \
                    * (1+inputs_to_optimizer["GREENHOUSE_GAIN_PCT"] / 100)

                rotation_kcals_per_ha_long.append(gh_kcals)

                rotation_fat_per_ha_long.append(FAT_RATIO * gh_kcals)

                rotation_protein_per_ha_long.append(PROTEIN_RATIO * gh_kcals)

            rotation_kcals_per_ha = rotation_kcals_per_ha_long[0:NMONTHS]
            rotation_fat_per_ha = rotation_fat_per_ha_long[0:NMONTHS]
            rotation_protein_per_ha = rotation_protein_per_ha_long[0:NMONTHS]

            return (rotation_kcals_per_ha,
                    rotation_fat_per_ha,
                    rotation_protein_per_ha)

        if(ADD_GREENHOUSES):

            (greenhouse_kcals_per_ha,
             greenhouse_fat_per_ha,
             greenhouse_protein_per_ha) \
                = get_greenhouse_yield_per_ha(KCAL_RATIO_ROT,
                                              FAT_RATIO_ROT,
                                              PROTEIN_RATIO_ROT)
        else:
            greenhouse_kcals_per_ha = [0] * NMONTHS
            greenhouse_fat_per_ha = [0] * NMONTHS
            greenhouse_protein_per_ha = [0] * NMONTHS

        #### CONSTANTS FOR METHANE SINGLE CELL PROTEIN ####

        # apply sugar waste also to methane scp, for lack of better baseline

        INDUSTRIAL_FOODS_SLOPE_MULTIPLIER = \
            inputs_to_optimizer['INDUSTRIAL_FOODS_SLOPE_MULTIPLIER']
        if(inputs_to_optimizer['ADD_METHANE_SCP']):
            SCP_WASTE = inputs_to_optimizer['WASTE']['SUGAR']
            industrial_delay_months = [0] * inputs_to_optimizer['DELAY']['INDUSTRIAL_FOODS_MONTHS']

            METHANE_SCP_PERCENT_KCALS = list(np.array(industrial_delay_months
            + [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2,
            2, 2, 2, 4, 7, 7, 7, 7, 7, 9, 11, 11, 11, 11, 11, 11, 13, 15, 15, 15, 15,
            15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15]) / (1 - 0.12) * INDUSTRIAL_FOODS_SLOPE_MULTIPLIER)

            production_kcals_scp_per_month_long = []
            for x in METHANE_SCP_PERCENT_KCALS:
                production_kcals_scp_per_month_long.append(
                    x / 100 \
                    * self.GLOBAL_MONTHLY_NEEDS \
                    * inputs_to_optimizer['SCP_GLOBAL_PRODUCTION_FRACTION']
                    * (1 - SCP_WASTE / 100))
        else:
            production_kcals_scp_per_month_long = [0] * NMONTHS

        production_kcals_scp_per_month = production_kcals_scp_per_month_long[0:NMONTHS]

        self.SCP_KCALS_PER_KG = 5350
        self.SCP_FRAC_PROTEIN = 0.650
        self.SCP_FRAC_FAT = 0.09

        #billions of kcals converted to 1000s of tons protein
        production_protein_scp_per_month = \
            list(np.array(production_kcals_scp_per_month)
                 * 1e9
                 * self.SCP_FRAC_PROTEIN
                 / self.SCP_KCALS_PER_KG
                 / 1e6)

        #billions of kcals converted to 1000s of tons fat
        production_fat_scp_per_month = \
            list(np.array(production_kcals_scp_per_month)
                 * 1e9
                 * self.SCP_FRAC_FAT
                 / self.SCP_KCALS_PER_KG
                 / 1e6)

        #### CONSTANTS FOR CELLULOSIC SUGAR ####

        if(inputs_to_optimizer["ADD_CELLULOSIC_SUGAR"]):
            SUGAR_WASTE = inputs_to_optimizer['WASTE']['SUGAR']

            industrial_delay_months = [0] * inputs_to_optimizer["DELAY"]['INDUSTRIAL_FOODS_MONTHS']


            CELL_SUGAR_PERCENT_KCALS = list(np.append(industrial_delay_months, np.array([0.00, 0.00, 0.00, 0.00, 0.00, 9.79, 9.79, 9.79, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20,
                20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20])) * 1 / (1 - 0.12) * INDUSTRIAL_FOODS_SLOPE_MULTIPLIER)

            production_kcals_CS_per_month_long = []
            for x in CELL_SUGAR_PERCENT_KCALS:
                production_kcals_CS_per_month_long.append(
                    x / 100 \
                    * self.GLOBAL_MONTHLY_NEEDS \
                    * inputs_to_optimizer['CS_GLOBAL_PRODUCTION_FRACTION'] \
                    * (1 - SUGAR_WASTE / 100))
        else:
            production_kcals_CS_per_month_long = \
                [0] * NMONTHS

        production_kcals_CS_per_month = production_kcals_CS_per_month_long[0:NMONTHS]

        #### OTHER VARIABLES ####

        CONVERSION_TO_KCALS = self.POP / 1e9/ KCALS_DAILY
        CONVERSION_TO_FAT = self.POP / 1e9 / FAT_DAILY
        CONVERSION_TO_PROTEIN = self.POP / 1e9 / PROTEIN_DAILY

        time_consts = {}  # time dependent constants as inputs to the optimizer

        time_consts["built_area"] = built_area
        time_consts["biofuels_fat"] = biofuels_fat
        time_consts["biofuels_protein"] = biofuels_protein
        time_consts["biofuels_kcals"] = biofuels_kcals
        time_consts["crops_food_produced"] = crops_food_produced  # no waste
        time_consts["greenhouse_kcals_per_ha"] = greenhouse_kcals_per_ha
        time_consts["greenhouse_fat_per_ha"] = greenhouse_fat_per_ha
        time_consts["greenhouse_protein_per_ha"] = greenhouse_protein_per_ha
        time_consts["production_kcals_scp_per_month"] = production_kcals_scp_per_month
        time_consts["production_protein_scp_per_month"] = \
        production_protein_scp_per_month
        time_consts["production_fat_scp_per_month"] = production_fat_scp_per_month
        time_consts["production_kcals_fish_per_month"] = production_kcals_fish_per_month
        time_consts["production_protein_fish_per_month"] = \
        production_protein_fish_per_month
        time_consts["production_fat_fish_per_month"] = production_fat_fish_per_month
        time_consts["production_kcals_CS_per_month"] = production_kcals_CS_per_month
        time_consts["dairy_milk_kcals"] = dairy_milk_kcals
        time_consts["dairy_milk_fat"] = dairy_milk_fat
        time_consts["dairy_milk_protein"] = dairy_milk_protein
        time_consts["h_e_milk_kcals"] = h_e_milk_kcals
        time_consts["h_e_milk_fat"] = h_e_milk_fat
        time_consts["h_e_milk_protein"] = h_e_milk_protein
        time_consts["h_e_created_kcals"] = h_e_created_kcals
        time_consts["h_e_created_fat"] = h_e_created_fat
        time_consts["h_e_created_protein"] = h_e_created_protein
        time_consts["h_e_balance_kcals"] = h_e_balance_kcals
        time_consts["h_e_balance_fat"] = h_e_balance_fat
        time_consts["h_e_balance_protein"] = h_e_balance_protein
        time_consts["cattle_maintained_kcals"] = cattle_maintained_kcals
        time_consts["cattle_maintained_fat"] = cattle_maintained_fat
        time_consts["cattle_maintained_protein"] = cattle_maintained_protein
        time_consts["greenhouse_area"] = greenhouse_area
        time_consts["meat_eaten"] = meat_culled
        time_consts["h_e_meat_kcals"] = h_e_meat_kcals
        time_consts["h_e_meat_fat"] = h_e_meat_fat
        time_consts["h_e_meat_protein"] = h_e_meat_protein
        time_consts["h_e_fed_dairy_produced"] = h_e_fed_dairy_produced
        time_consts["excess_kcals"] = excess_kcals
        time_consts["excess_fat_used"] = excess_fat_used
        time_consts["excess_protein_used"] = excess_protein_used

        # store variables useful for analysis

        constants = {}
        constants['VERBOSE'] = VERBOSE
        constants['NMONTHS'] = NMONTHS
        constants['NDAYS'] = NDAYS
        constants["DAYS_IN_MONTH"] = self.DAYS_IN_MONTH
        constants['POP'] = self.POP
        constants['ADD_STORED_FOOD'] = ADD_STORED_FOOD
        constants['ADD_FISH'] = ADD_FISH
        constants['ADD_SEAWEED'] = ADD_SEAWEED
        constants['ADD_GREENHOUSES'] = ADD_GREENHOUSES
        constants['ADD_MEAT'] = ADD_MEAT
        constants['ADD_DAIRY'] = ADD_DAIRY
        constants['ADD_OUTDOOR_GROWING'] = ADD_OUTDOOR_GROWING
        constants['ADD_CELLULOSIC_SUGAR'] = ADD_CELLULOSIC_SUGAR
        constants['ADD_METHANE_SCP'] = ADD_METHANE_SCP

        constants['KCALS_DAILY'] = KCALS_DAILY
        constants['FAT_DAILY'] = FAT_DAILY
        constants['PROTEIN_DAILY'] = PROTEIN_DAILY
        constants['CONVERSION_TO_KCALS'] = CONVERSION_TO_KCALS
        constants['CONVERSION_TO_FAT'] = CONVERSION_TO_FAT
        constants['CONVERSION_TO_PROTEIN'] = CONVERSION_TO_PROTEIN

        constants['KCALS_MONTHLY'] = self.KCALS_MONTHLY
        constants['PROTEIN_MONTHLY'] = self.PROTEIN_MONTHLY
        constants['FAT_MONTHLY'] = self.FAT_MONTHLY

        constants['SF_FRACTION_FAT'] = SF_FRACTION_FAT
        constants['SF_FRACTION_PROTEIN'] = SF_FRACTION_PROTEIN

        constants['OG_FRACTION_FAT'] = OG_FRACTION_FAT
        constants['OG_FRACTION_PROTEIN'] = OG_FRACTION_PROTEIN

        constants['OG_ROTATION_FRACTION_KCALS'] = OG_ROTATION_FRACTION_KCALS
        constants['OG_ROTATION_FRACTION_FAT'] = OG_ROTATION_FRACTION_FAT
        constants['OG_ROTATION_FRACTION_PROTEIN'] = OG_ROTATION_FRACTION_PROTEIN

        constants['MEAT_FRACTION_FAT'] = MEAT_FRACTION_FAT
        constants['MEAT_FRACTION_PROTEIN'] = MEAT_FRACTION_PROTEIN

        constants['CULL_DURATION_MONTHS'] = CULL_DURATION_MONTHS

        constants['INITIAL_SEAWEED'] = INITIAL_SEAWEED
        constants['SEAWEED_KCALS'] = SEAWEED_KCALS
        constants['HARVEST_LOSS'] = HARVEST_LOSS
        constants['SEAWEED_FAT'] = SEAWEED_FAT
        constants['SEAWEED_PROTEIN'] = SEAWEED_PROTEIN

        constants["MINIMUM_DENSITY"] = MINIMUM_DENSITY
        constants["MAXIMUM_DENSITY"] = MAXIMUM_DENSITY
        constants["MAXIMUM_AREA"] = MAXIMUM_AREA
        constants["INITIAL_AREA"] = INITIAL_AREA

        constants['INITIAL_SF_KCALS'] = INITIAL_SF_KCALS  # no waste
        constants['INITIAL_MEAT'] = INITIAL_MEAT

        constants['FISH_FAT'] = FISH_FAT
        constants['FISH_PROTEIN'] = FISH_PROTEIN
        constants['FISH_KCALS'] = FISH_KCALS

        constants["KG_PER_SMALL_ANIMAL"] = KG_PER_SMALL_ANIMAL
        constants["KG_PER_MEDIUM_ANIMAL"] = KG_PER_MEDIUM_ANIMAL
        constants["KG_PER_LARGE_ANIMAL"] = KG_PER_LARGE_ANIMAL

        constants["LARGE_ANIMAL_KCALS_PER_KG"] = LARGE_ANIMAL_KCALS_PER_KG
        constants["LARGE_ANIMAL_FAT_PER_KG"] = LARGE_ANIMAL_FAT_PER_KG
        constants["LARGE_ANIMAL_PROTEIN_PER_KG"] = LARGE_ANIMAL_PROTEIN_PER_KG

        constants["MEDIUM_ANIMAL_KCALS_PER_KG"] = MEDIUM_ANIMAL_KCALS_PER_KG
        constants["MEDIUM_ANIMAL_FAT_PER_KG"] = MEDIUM_ANIMAL_FAT_PER_KG
        constants["MEDIUM_ANIMAL_PROTEIN_PER_KG"] = MEDIUM_ANIMAL_PROTEIN_PER_KG

        constants["SMALL_ANIMAL_KCALS_PER_KG"] = SMALL_ANIMAL_KCALS_PER_KG
        constants["SMALL_ANIMAL_FAT_PER_KG"] = SMALL_ANIMAL_FAT_PER_KG
        constants["SMALL_ANIMAL_PROTEIN_PER_KG"] = SMALL_ANIMAL_PROTEIN_PER_KG

        constants['inputs'] = inputs_to_optimizer

        self.print_constants(constants,time_consts)

        return (constants, time_consts)

    def print_constants(self,constants,time_consts):
        # used by world population
        print("")
        print("calories consumed per day")
        print(constants['KCALS_DAILY'])
        print("fat consumed per day grams")
        print(constants['FAT_DAILY'])
        print("protein consumed per day grams")
        print(constants['PROTEIN_DAILY'])
        print("")
        print(
            "INITIAL_HUMANS_KCALS "+str(self.POP)+" people consumed million tons dry caloric monthly")
        print(-self.POP * self.KCALS_MONTHLY / 4e6 / 1e6)
        print("INITIAL_HUMANS_FAT "+str(self.POP)+" people consumed million tons monthly")
        print(-self.POP * self.FAT_MONTHLY / 1e3)
        print("INITIAL_HUMANS_PROTEIN "+str(self.POP)+" people consumed million tons monthly")
        print(-self.POP * self.PROTEIN_MONTHLY / 1e3)
        print("")
        # 1000 tons protein or fat per dry caloric ton
        print("INITIAL_HUMANS_FAT consumed percentage")
        print(100 * self.POP * self.FAT_MONTHLY / 1e3 /
              (self.POP * self.KCALS_MONTHLY / 4e6 / 1e6))
        print("INITIAL_HUMANS_PROTEIN consumed percentage")
        print(100 * self.POP * self.PROTEIN_MONTHLY / 1e3 /
              (self.POP * self.KCALS_MONTHLY / 4e6 / 1e6))
        
        CFP = time_consts['crops_food_produced'][0]
        OG_RF_KCALS = constants['OG_ROTATION_FRACTION_KCALS']
        OG_RF_FAT = constants['OG_ROTATION_FRACTION_FAT']
        OG_RF_PROTEIN = constants['OG_ROTATION_FRACTION_PROTEIN']

        # 1000 tons protein/fat per dry caloric ton
        print("")
        print("INITIAL_OG_KCALS million tons dry caloric monthly")
        print(CFP * 1e9 / 4e6 / 1e6)
        print("INITIAL_OG_FAT million tons monthly")
        print(CFP * constants['OG_FRACTION_FAT'] / 1e3)
        print("INITIAL_OG_PROTEIN million tons monthly")
        print(CFP * constants['OG_FRACTION_PROTEIN'] / 1e3)
        print("")
        print("INITIAL_OG_FAT percentage")
        print(100 * CFP * constants['OG_FRACTION_FAT'] /
              1e3 / (CFP * 1e9 / 4e6 / 1e6))
        print("INITIAL_OG_PROTEIN percentage")
        print(100 * CFP * constants['OG_FRACTION_PROTEIN'] /
              1e3 / (CFP * 1e9 / 4e6 / 1e6))
        print("")
        print("INITIAL_OG_ROTATION_KCALS million tons dry caloric monthly")
        print(CFP  * 
              OG_RF_KCALS * 1e9 / 4e6 / 1e6)
        print("INITIAL_OG_ROTATION_FAT million tons monthly")
        print(CFP * OG_RF_FAT / 1e3)
        print("INITIAL_OG_ROTATION_PROTEIN million tons monthly")
        print(CFP * OG_RF_PROTEIN / 1e3)
        print("")
        print("INITIAL_OG_ROTATION_FAT percentage")
        print(100 * CFP * OG_RF_FAT / 1e3 / (
            CFP * OG_RF_KCALS * 1e9 / 4e6 / 1e6))
        print("INITIAL_OG_ROTATION_PROTEIN percentage")
        print(100 * CFP * OG_RF_PROTEIN / 1e3 / (time_consts['crops_food_produced'][0]
           * OG_RF_KCALS * 1e9 / 4e6 / 1e6))  # 1000 tons protein/fat per dry caloric ton

        INITIAL_SF_KCALS = constants['INITIAL_SF_KCALS']
        SF_FRACTION_FAT = constants['SF_FRACTION_FAT']
        SF_FRACTION_PROTEIN = constants['SF_FRACTION_PROTEIN']

        print("")
        print("INITIAL_SF_KCALS million tons dry caloric")
        print(INITIAL_SF_KCALS * 1e9 / 4e6 / 1e6)
        print("INITIAL_SF_FAT million tons")
        print(INITIAL_SF_KCALS * SF_FRACTION_FAT / 1e3)
        print("INITIAL_SF_PROTEIN million tons")
        print(INITIAL_SF_KCALS * SF_FRACTION_PROTEIN / 1e3)
        print("")
        print("INITIAL_SF_FAT percentage")
        print(100 * INITIAL_SF_KCALS * SF_FRACTION_FAT /
              1e3 / (INITIAL_SF_KCALS * 1e9 / 4e6 / 1e6))
        print("INITIAL_SF_PROTEIN percentage")
        print(100 * INITIAL_SF_KCALS * SF_FRACTION_PROTEIN /
              1e3 / (INITIAL_SF_KCALS * 1e9 / 4e6 / 1e6))
        if(self.feed_shutoff_kcals[0] > 0):
            print("")
            print("INITIAL_FEED_KCALS million tons dry caloric monthly")
            print(-self.FEED_MONTHLY_USAGE_KCALS * 1e9 / 4e6 / 1e6)
            print("INITIAL_FEED_FAT million tons monthly")
            print(-self.FEED_MONTHLY_USAGE_FAT / 1e3)
            print("INITIAL_FEED_PROTEIN million tons monthly")
            print(-self.FEED_MONTHLY_USAGE_PROTEIN / 1e3)
            print("")
            print("INITIAL_FEED_FAT percentage")
            print(100 * self.FEED_MONTHLY_USAGE_FAT / 1e3 /
                  (self.FEED_MONTHLY_USAGE_KCALS * 1e9 / 4e6 / 1e6))
            print("INITIAL_FEED_PROTEIN percentage")
            print(100 * self.FEED_MONTHLY_USAGE_PROTEIN / 1e3 /
                  (self.FEED_MONTHLY_USAGE_KCALS * 1e9 / 4e6 / 1e6))
            print("")
            CPM = np.array(self.chicken_pork_kcals)[0]
            LARGE_ANIMAL_KCALS_PER_KG = constants['LARGE_ANIMAL_KCALS_PER_KG']
            LARGE_ANIMAL_FAT_PER_KG = constants['LARGE_ANIMAL_FAT_PER_KG']
            LARGE_ANIMAL_PROTEIN_PER_KG = constants['LARGE_ANIMAL_PROTEIN_PER_KG']
            CM = np.array(self.cattle_h_e_maintained)[0]\
                * 1000  \
                * constants['LARGE_ANIMAL_KCALS_PER_KG'] \
                / 1e9
            if(CPM > 0):
                print("INITIAL_CH_PK_KCALS million tons dry caloric monthly")
                print(CPM * 1e9 / 4e6 / 1e6)
                print("INITIAL_CH_PK_FAT million tons monthly")
                print(self.chicken_pork_fat[0] / 1e3)
                print("INITIAL_CH_PK_PROTEIN million tons monthly")
                print(self.chicken_pork_protein[0] / 1e3)
                print("")
                print("INITIAL_CH_PK_FAT percentage")
                print(100 * self.chicken_pork_fat[0] / 1e3 / (CPM * 1e9 / 4e6 / 1e6))
                print("INITIAL_CH_PK_PROTEIN percentage")
                print(100 * self.chicken_pork_protein[0] / 1e3 / (CPM * 1e9 / 4e6 / 1e6))
                print("")
            else:
                print("no chicken pork maintained")
                print("")
            if(CM > 0):
                print("INITIAL_CM_KCALS million tons dry caloric monthly")
                print(CM * 1e9 / 4e6 / 1e6)

                print("INITIAL_CM_FAT million tons monthly")
                print(CM * 1e9 / LARGE_ANIMAL_KCALS_PER_KG  * 
                      LARGE_ANIMAL_FAT_PER_KG / 1e6 / 1e3)
                print("INITIAL_CM_PROTEIN million tons monthly")
                print(CM * 1e9 / LARGE_ANIMAL_KCALS_PER_KG  * 
                      LARGE_ANIMAL_PROTEIN_PER_KG / 1e6 / 1e3)
                print("")
                print("INITIAL_CM_FAT percentage")
                print(100 * CM * 1e9 / LARGE_ANIMAL_KCALS_PER_KG  * 
                      LARGE_ANIMAL_FAT_PER_KG / 1e6 / 1e3 / (CM * 1e9 / 4e6 / 1e6))
                print("INITIAL_CM_PROTEIN percentage")
                print(100 * CM * 1e9 / LARGE_ANIMAL_KCALS_PER_KG  * 
                      LARGE_ANIMAL_PROTEIN_PER_KG / 1e6 / 1e3 / (CM * 1e9 / 4e6 / 1e6))
                print("")
                print("culled chicken, pork, and cattle per month.")
                print("reaches minimum after " +
                      str(constants['CULL_DURATION_MONTHS'])+" months")
            else:
                print("no cattle maintained from human edible")
                print("")

            MEAT_WASTE = constants['inputs']['WASTE']['MEAT']

            CM_IN_KCALS = time_consts['cattle_maintained_kcals'][0]\
                          / (1 - MEAT_WASTE / 100)
            CM_IN_FAT = time_consts['cattle_maintained_fat'][0]\
                          / (1 - MEAT_WASTE / 100)
            CM_IN_PROTEIN = time_consts['cattle_maintained_protein'][0]\
                          / (1 - MEAT_WASTE / 100)

            if(CM_IN_KCALS > 0):
                print("INITIAL_CM_IN_KCALS million tons dry caloric monthly")
                print(CM_IN_KCALS * 1e9 / 4e6 / 1e6)

                print("INITIAL_CM_IN_FAT million tons monthly")
                print(CM_IN_FAT / 1e3)
                print("INITIAL_CM_IN_PROTEIN million tons monthly")
                print(CM_IN_PROTEIN / 1e3)
                print("")
                print("INITIAL_CM_IN_FAT percentage")
                print(100 * CM_IN_FAT / 1e3 / (CM_IN_KCALS * 1e9 / 4e6 / 1e6))
                print("INITIAL_CM_IN_PROTEIN percentage")
                print(100 * CM_IN_PROTEIN / 1e3 / (CM_IN_KCALS * 1e9 / 4e6 / 1e6))
                print("")
            else:
                print("No meat (would be cattle) from inedible sources")
                print("")

            print("")
            if(constants['inputs']["CULL_ANIMALS"]):
                print("INITIAL_CULLED_KCALS million tons dry caloric monthly")
                print("INITIAL_CULLED_FAT million tons monthly")
                print("INITIAL_CULLED_PROTEIN million tons monthly")
                print("")
                print("INITIAL_CULLED_FAT percentage")
                print("INITIAL_CULLED_PROTEIN percentage")
                print("")
        else:
            print("No Feed Usage")

        if(constants['ADD_DAIRY']):
            dairy_milk_kcals = time_consts['dairy_milk_kcals'][0]
            dairy_milk_fat = time_consts['dairy_milk_fat'][0]
            dairy_milk_protein = time_consts['dairy_milk_protein'][0]
            DAIRY_WASTE = constants['inputs']['WASTE']['DAIRY']
            print("INITIAL_DAIRY_KCALS million tons dry caloric monthly")
            print(dairy_milk_kcals / (1 - DAIRY_WASTE / 100) * 1e9 / 4e6 / 1e6)

            print("INITIAL_DAIRY_FAT million tons monthly")
            print(dairy_milk_fat / (1 - DAIRY_WASTE / 100) / 1e3)
            print("INITIAL_DAIRY_PROTEIN million tons monthly")
            print(dairy_milk_protein / (1 - DAIRY_WASTE / 100) / 1e3)
            print("")
            print("INITIAL_DAIRY_FAT percentage")
            print(100 * dairy_milk_fat / (1 - DAIRY_WASTE / 100) / 1e3 /
                  (dairy_milk_kcals / (1 - DAIRY_WASTE / 100) * 1e9 / 4e6 / 1e6))
            print("INITIAL_DAIRY_PROTEIN percentage")
            print(100 * dairy_milk_protein / (1 - DAIRY_WASTE / 100) / 1e3 /
                  (dairy_milk_kcals / (1 - DAIRY_WASTE / 100) * 1e9 / 4e6 / 1e6))
            print("")
        if(constants['ADD_FISH']):
            FISH_WASTE = constants['inputs']['WASTE']['SEAFOOD']
            production_kcals_fish_per_month = time_consts['production_kcals_fish_per_month'][0]
            production_fat_fish_per_month = time_consts['production_fat_fish_per_month'][0]
            production_protein_fish_per_month = time_consts['production_protein_fish_per_month'][0]

            print("INITIAL_FISH_KCALS million tons dry caloric monthly")
            print(
                production_kcals_fish_per_month / (1 - FISH_WASTE / 100) * 1e9 / 4e6 / 1e6)

            print("INITIAL_FISH_PROTEIN million tons monthly")
            print(production_protein_fish_per_month / (1 - FISH_WASTE / 100) / 1e3)
            print("INITIAL_FISH_FAT million tons monthly")
            print(production_fat_fish_per_month / (1 - FISH_WASTE / 100) / 1e3)
            print("")
            print("INITIAL_FISH_FAT percentage")
            print(100 * production_fat_fish_per_month / (1 - FISH_WASTE / 100) / 1e3 / (
                production_kcals_fish_per_month / (1 - FISH_WASTE / 100) * 1e9 / 4e6 / 1e6))
            print("INITIAL_FISH_PROTEIN percentage")
            print(100 * production_protein_fish_per_month / (1 - FISH_WASTE / 100) / 1e3 / (
                production_kcals_fish_per_month / (1 - FISH_WASTE / 100) * 1e9 / 4e6 / 1e6))
            print("")
            print("")
        if(time_consts['biofuels_kcals'][0] > 0):
            # 1000 tons protein/fat per dry caloric ton
            print("INITIAL_BIOFUEL_KCALS million tons dry caloric monthly")
            print(-self.BIOFUEL_MONTHLY_USAGE_KCALS * 1e9 / 4e6 / 1e6)
            print("INITIAL_BIOFUEL_FAT million tons monthly")
            print(-self.BIOFUEL_MONTHLY_USAGE_FAT / 1e3)
            print("INITIAL_BIOFUEL_PROTEIN million tons monthly")
            print(-self.BIOFUEL_MONTHLY_USAGE_PROTEIN / 1e3)
            print("INITIAL_BIOFUEL_FAT percentage")
            print(100 * self.BIOFUEL_MONTHLY_USAGE_FAT / 1e3 /
                  (self.BIOFUEL_MONTHLY_USAGE_KCALS * 1e9 / 4e6 / 1e6))
            print("INITIAL_BIOFUEL_PROTEIN percentage")
            print(100 * self.BIOFUEL_MONTHLY_USAGE_PROTEIN / 1e3 /
                  (self.BIOFUEL_MONTHLY_USAGE_KCALS * 1e9 / 4e6 / 1e6))
        else:
            print("No biofuel usage")
            print("")

        if(constants['ADD_METHANE_SCP']):
            production_kcals_scp_per_month = time_consts['production_kcals_scp_per_month']
            production_fat_scp_per_month = time_consts['production_fat_scp_per_month']
            production_protein_scp_per_month = time_consts['production_protein_scp_per_month']
            print("daily calories SCP")
            print(np.array(production_kcals_scp_per_month)\
                * 1e9 \
                / self.DAYS_IN_MONTH \
                / self.POP)
            print("daily kg SCP")
            print(np.array(production_kcals_scp_per_month)*1e9 \
                / self.DAYS_IN_MONTH \
                / self.POP \
                / self.SCP_KCALS_PER_KG)
            print("daily grams protein SCP")
            print(np.array(production_kcals_scp_per_month)*1e9 \
                / self.DAYS_IN_MONTH \
                / self.POP \
                / self.SCP_KCALS_PER_KG * self.SCP_FRAC_PROTEIN*1000)
            print("1000 tons per month protein SCP")
            print(np.array(production_kcals_scp_per_month)\
                * 1e9 \
                / self.SCP_KCALS_PER_KG \
                * self.SCP_FRAC_PROTEIN \
                / 1e6)
