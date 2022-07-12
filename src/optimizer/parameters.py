############################### Parameters ####################################
##                                                                            #
##           Calculates all the parameters that feed into the optimizer       #
##                                                                            #
###############################################################################


import os
import sys
import numpy as np

module_path = os.path.abspath(os.path.join("../.."))
if module_path not in sys.path:
    sys.path.append(module_path)

from src.food_system.biofuels import Biofuels
from src.food_system.feed import Feed
from src.food_system.meat_and_dairy import MeatAndDairy
from src.food_system.outdoor_crops import OutdoorCrops
from src.food_system.seafood import Seafood
from src.food_system.stored_food import StoredFood
from src.food_system.cellulosic_sugar import CellulosicSugar
from src.food_system.greenhouses import Greenhouses
from src.food_system.methane_scp import MethaneSCP
from src.food_system.seaweed import Seaweed


class Parameters:
    def __init__(self):

        self.DAYS_IN_MONTH = 30
        self.SIMULATION_STARTING_MONTH = "JUN"
        # Dictionary of the months to set the starting point of the model to
        # the months specified in parameters.py
        months_dict = {
            "JAN": 1,
            "FEB": 2,
            "MAR": 3,
            "APR": 4,
            "MAY": 5,
            "JUN": 6,
            "JUL": 7,
            "AUG": 8,
            "SEP": 9,
            "OCT": 10,
            "NOV": 11,
            "DEC": 12,
        }
        self.SIMULATION_STARTING_MONTH_NUM = months_dict[self.SIMULATION_STARTING_MONTH]

    def computeParameters(self, constants, VERBOSE=False):
        inputs_to_optimizer = constants["inputs"]  # single valued inputs to optimizer
        inputs_to_optimizer["STARTING_MONTH_NUM"] = self.SIMULATION_STARTING_MONTH_NUM

        # population
        self.POP = inputs_to_optimizer["POP"]
        # population in units of millions of people
        self.POP_BILLIONS = inputs_to_optimizer["POP"] / 1e9

        # full months duration of simulation
        NMONTHS = inputs_to_optimizer["NMONTHS"]
        NDAYS = NMONTHS * self.DAYS_IN_MONTH
        ADD_FISH = inputs_to_optimizer["ADD_FISH"]
        ADD_SEAWEED = inputs_to_optimizer["ADD_SEAWEED"]
        ADD_MEAT = inputs_to_optimizer["ADD_MEAT"]
        ADD_DAIRY = inputs_to_optimizer["ADD_DAIRY"]

        ADD_STORED_FOOD = inputs_to_optimizer["ADD_STORED_FOOD"]
        ADD_METHANE_SCP = inputs_to_optimizer["ADD_METHANE_SCP"]
        ADD_CELLULOSIC_SUGAR = inputs_to_optimizer["ADD_CELLULOSIC_SUGAR"]
        ADD_GREENHOUSES = inputs_to_optimizer["ADD_GREENHOUSES"]
        ADD_OUTDOOR_GROWING = inputs_to_optimizer["ADD_OUTDOOR_GROWING"]

        #### NUTRITION PER MONTH ####

        # https://docs.google.com/spreadsheets/d / 1RZqSrHNiIEuPQLtx1ebCd_kUcFvEF6Ea46xyzA5wU0s/edit#gid=1516287804

        # we will assume a 2100 kcals diet, and scale the "upper safe" nutrition
        # from the spreadsheet down to this "standard" level.
        # we also add 20% loss, according to the sorts of loss seen in this spreadsheet
        KCALS_DAILY = inputs_to_optimizer["NUTRITION"]["KCALS_DAILY"]
        PROTEIN_DAILY = inputs_to_optimizer["NUTRITION"]["PROTEIN_DAILY"]
        FAT_DAILY = inputs_to_optimizer["NUTRITION"]["FAT_DAILY"]

        # kcals per person
        self.KCALS_MONTHLY = KCALS_DAILY * self.DAYS_IN_MONTH

        # in thousands of tons (grams per ton == 1e6) per month
        self.FAT_MONTHLY = FAT_DAILY / 1e6 * self.DAYS_IN_MONTH / 1000

        # in thousands of tons (grams per ton == 1e6) per month per person
        self.PROTEIN_MONTHLY = PROTEIN_DAILY / 1e6 * self.DAYS_IN_MONTH / 1000

        # in billions of kcals per month for population
        self.BILLION_KCALS_NEEDED = self.KCALS_MONTHLY * self.POP_BILLIONS
        # in thousands of tons per month for population
        self.THOU_TONS_FAT_NEEDED = self.FAT_MONTHLY * self.POP
        # in thousands of tons per month for population
        self.THOU_TONS_PROTEIN_NEEDED = self.PROTEIN_MONTHLY * self.POP
        print("self.POP_BILLIONS")
        print(self.POP_BILLIONS)

        ####SEAWEED INITIAL VARIABLES####
        seaweed = Seaweed(inputs_to_optimizer)

        # determine area built to enable seaweed to grow there
        built_area = seaweed.get_built_area(inputs_to_optimizer)

        #### FISH ####

        seafood = Seafood(inputs_to_optimizer)

        (
            production_kcals_fish_per_month,
            production_fat_fish_per_month,
            production_protein_fish_per_month,
        ) = seafood.get_seafood_production(inputs_to_optimizer)

        #### BIOFUEL VARIABLES ####
        biofuels = Biofuels(inputs_to_optimizer)
        (biofuels_kcals, biofuels_fat, biofuels_protein) = biofuels.get_biofuel_usage(
            inputs_to_optimizer
        )

        #### FEED VARIABLES ####
        feed = Feed(inputs_to_optimizer)
        (biofuels_kcals, biofuels_fat, biofuels_protein) = feed.get_feed_usage(
            inputs_to_optimizer
        )

        ####LIVESTOCK, EGG, DAIRY INITIAL VARIABLES####

        meat_and_dairy = MeatAndDairy(inputs_to_optimizer)

        meat_and_dairy.calculate_meat_dairy_from_human_inedible_feed(
            inputs_to_optimizer
        )

        meat_and_dairy.calculate_meat_and_dairy_from_excess(feed.kcals_fed_to_animals)

        h_e_fed_dairy_produced = meat_and_dairy.h_e_fed_dairy_produced

        (
            chicken_pork_kcals,
            chicken_pork_fat,
            chicken_pork_protein,
            h_e_meat_kcals,
            h_e_meat_fat,
            h_e_meat_protein,
        ) = meat_and_dairy.get_meat_from_human_edible_feed()

        meat_and_dairy.calculate_animals_culled(inputs_to_optimizer)

        meat_and_dairy.calculate_meat_nutrition()

        meat_culled = meat_and_dairy.get_culled_meat(
            inputs_to_optimizer, feed.feed_shutoff_delay_months
        )
        (
            h_e_milk_kcals,
            h_e_milk_fat,
            h_e_milk_protein,
        ) = meat_and_dairy.get_dairy_from_human_edible_feed(inputs_to_optimizer)

        (
            dairy_milk_kcals,
            dairy_milk_fat,
            dairy_milk_protein,
        ) = meat_and_dairy.get_dairy_produced()

        self.chicken_pork_kcals = meat_and_dairy.chicken_pork_kcals
        self.chicken_pork_fat = meat_and_dairy.chicken_pork_fat
        self.chicken_pork_protein = meat_and_dairy.chicken_pork_protein
        self.cattle_h_e_maintained = meat_and_dairy.cattle_h_e_maintained

        (
            excess_kcals,
            excess_fat_used,
            excess_protein_used,
        ) = meat_and_dairy.get_excess(inputs_to_optimizer, biofuels, feed)

        (
            cattle_maintained_kcals,
            cattle_maintained_fat,
            cattle_maintained_protein,
        ) = meat_and_dairy.get_cattle_maintained()

        h_e_created_kcals = h_e_meat_kcals + h_e_milk_kcals
        h_e_created_fat = h_e_meat_fat + h_e_milk_fat
        h_e_created_protein = h_e_meat_protein + h_e_milk_protein

        # crop waste percentage is applied to excess calories, as these are
        # assumed to be excess crops being feed to animals
        CROP_WASTE = 1 - inputs_to_optimizer["WASTE"]["CROPS"] / 100

        h_e_balance_kcals = -excess_kcals * CROP_WASTE + h_e_created_kcals
        h_e_balance_fat = -excess_fat_used * CROP_WASTE + h_e_created_fat
        h_e_balance_protein = -excess_protein_used * CROP_WASTE + h_e_created_protein

        #### CROP PRODUCTION VARIABLES ####

        outdoor_crops = OutdoorCrops(inputs_to_optimizer)
        outdoor_crops.calculate_rotation_ratios(inputs_to_optimizer)
        outdoor_crops.calculate_monthly_production(inputs_to_optimizer)

        #### STORED FOOD VARIABLES ####

        stored_food = StoredFood(inputs_to_optimizer, outdoor_crops)

        #### CONSTANTS FOR GREENHOUSES ####

        greenhouses = Greenhouses(inputs_to_optimizer)

        greenhouse_area = greenhouses.get_greenhouse_area(
            inputs_to_optimizer, outdoor_crops
        )

        (
            greenhouse_kcals_per_ha,
            greenhouse_fat_per_ha,
            greenhouse_protein_per_ha,
        ) = greenhouses.get_greenhouse_yield_per_ha(inputs_to_optimizer, outdoor_crops)

        crops_food_produced = outdoor_crops.get_crop_production_minus_greenhouse_area(
            inputs_to_optimizer, greenhouses.greenhouse_fraction_area
        )

        #### CONSTANTS FOR METHANE SINGLE CELL PROTEIN ####

        methane_scp = MethaneSCP(inputs_to_optimizer)
        methane_scp.calculate_monthly_scp_production(inputs_to_optimizer)

        (
            production_kcals_scp_per_month,
            production_fat_scp_per_month,
            production_protein_scp_per_month,
        ) = methane_scp.get_scp_production()

        #### CONSTANTS FOR CELLULOSIC SUGAR ####

        cellulosic_sugar = CellulosicSugar(inputs_to_optimizer)
        cellulosic_sugar.calculate_monthly_cs_production(inputs_to_optimizer)

        production_kcals_CS_per_month = cellulosic_sugar.get_monthly_cs_production()

        #### OTHER VARIABLES ####

        CONVERSION_TO_KCALS = self.POP / 1e9 / KCALS_DAILY
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
        time_consts[
            "production_protein_scp_per_month"
        ] = production_protein_scp_per_month
        time_consts["production_fat_scp_per_month"] = production_fat_scp_per_month
        time_consts["production_kcals_fish_per_month"] = production_kcals_fish_per_month
        time_consts[
            "production_protein_fish_per_month"
        ] = production_protein_fish_per_month
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
        constants["VERBOSE"] = VERBOSE
        constants["NMONTHS"] = NMONTHS
        constants["NDAYS"] = NDAYS
        constants["DAYS_IN_MONTH"] = self.DAYS_IN_MONTH
        constants["POP"] = self.POP
        constants["POP_BILLIONS"] = self.POP_BILLIONS

        constants["ADD_STORED_FOOD"] = ADD_STORED_FOOD
        constants["ADD_FISH"] = ADD_FISH
        constants["ADD_SEAWEED"] = ADD_SEAWEED
        constants["ADD_GREENHOUSES"] = ADD_GREENHOUSES
        constants["ADD_MEAT"] = ADD_MEAT
        constants["ADD_DAIRY"] = ADD_DAIRY
        constants["ADD_OUTDOOR_GROWING"] = ADD_OUTDOOR_GROWING
        constants["ADD_CELLULOSIC_SUGAR"] = ADD_CELLULOSIC_SUGAR
        constants["ADD_METHANE_SCP"] = ADD_METHANE_SCP

        constants["CONVERSION_TO_KCALS"] = CONVERSION_TO_KCALS
        constants["CONVERSION_TO_FAT"] = CONVERSION_TO_FAT
        constants["CONVERSION_TO_PROTEIN"] = CONVERSION_TO_PROTEIN

        constants["BILLION_KCALS_NEEDED"] = self.BILLION_KCALS_NEEDED
        constants["THOU_TONS_FAT_NEEDED"] = self.THOU_TONS_FAT_NEEDED
        constants["THOU_TONS_PROTEIN_NEEDED"] = self.THOU_TONS_PROTEIN_NEEDED

        constants["KCALS_DAILY"] = KCALS_DAILY
        constants["FAT_DAILY"] = FAT_DAILY
        constants["PROTEIN_DAILY"] = PROTEIN_DAILY
        constants["KCALS_MONTHLY"] = self.KCALS_MONTHLY
        constants["PROTEIN_MONTHLY"] = self.PROTEIN_MONTHLY
        constants["FAT_MONTHLY"] = self.FAT_MONTHLY

        constants["SF_FRACTION_FAT"] = stored_food.SF_FRACTION_FAT
        constants["SF_FRACTION_PROTEIN"] = stored_food.SF_FRACTION_PROTEIN

        constants["OG_FRACTION_FAT"] = outdoor_crops.OG_FRACTION_FAT
        constants["OG_FRACTION_PROTEIN"] = outdoor_crops.OG_FRACTION_PROTEIN

        constants[
            "OG_ROTATION_FRACTION_KCALS"
        ] = outdoor_crops.OG_ROTATION_FRACTION_KCALS
        constants["OG_ROTATION_FRACTION_FAT"] = outdoor_crops.OG_ROTATION_FRACTION_FAT
        constants[
            "OG_ROTATION_FRACTION_PROTEIN"
        ] = outdoor_crops.OG_ROTATION_FRACTION_PROTEIN

        constants["MEAT_FRACTION_FAT"] = meat_and_dairy.MEAT_FRACTION_FAT
        constants["MEAT_FRACTION_PROTEIN"] = meat_and_dairy.MEAT_FRACTION_PROTEIN

        constants["CULL_DURATION_MONTHS"] = meat_and_dairy.CULL_DURATION_MONTHS

        constants["INITIAL_SEAWEED"] = seaweed.INITIAL_SEAWEED
        constants["SEAWEED_KCALS"] = seaweed.SEAWEED_KCALS
        constants["HARVEST_LOSS"] = seaweed.HARVEST_LOSS
        constants["SEAWEED_FAT"] = seaweed.SEAWEED_FAT
        constants["SEAWEED_PROTEIN"] = seaweed.SEAWEED_PROTEIN

        constants["MINIMUM_DENSITY"] = seaweed.MINIMUM_DENSITY
        constants["MAXIMUM_DENSITY"] = seaweed.MAXIMUM_DENSITY
        constants["MAXIMUM_AREA"] = seaweed.MAXIMUM_AREA
        constants["INITIAL_AREA"] = seaweed.INITIAL_AREA

        constants["INITIAL_SF_KCALS"] = stored_food.INITIAL_SF_KCALS  # no waste
        constants["INITIAL_MEAT"] = meat_and_dairy.INITIAL_MEAT

        constants["FISH_KCALS"] = seafood.FISH_KCALS
        constants["FISH_FAT"] = seafood.FISH_FAT
        constants["FISH_PROTEIN"] = seafood.FISH_PROTEIN

        constants["KG_PER_SMALL_ANIMAL"] = meat_and_dairy.KG_PER_SMALL_ANIMAL
        constants["KG_PER_MEDIUM_ANIMAL"] = meat_and_dairy.KG_PER_MEDIUM_ANIMAL
        constants["KG_PER_LARGE_ANIMAL"] = meat_and_dairy.KG_PER_LARGE_ANIMAL

        constants[
            "LARGE_ANIMAL_KCALS_PER_KG"
        ] = meat_and_dairy.LARGE_ANIMAL_KCALS_PER_KG
        constants["LARGE_ANIMAL_FAT_PER_KG"] = meat_and_dairy.LARGE_ANIMAL_FAT_PER_KG
        constants[
            "LARGE_ANIMAL_PROTEIN_PER_KG"
        ] = meat_and_dairy.LARGE_ANIMAL_PROTEIN_PER_KG

        constants[
            "MEDIUM_ANIMAL_KCALS_PER_KG"
        ] = meat_and_dairy.MEDIUM_ANIMAL_KCALS_PER_KG
        constants["MEDIUM_ANIMAL_FAT_PER_KG"] = meat_and_dairy.MEDIUM_ANIMAL_FAT_PER_KG
        constants[
            "MEDIUM_ANIMAL_PROTEIN_PER_KG"
        ] = meat_and_dairy.MEDIUM_ANIMAL_PROTEIN_PER_KG

        constants[
            "SMALL_ANIMAL_KCALS_PER_KG"
        ] = meat_and_dairy.SMALL_ANIMAL_KCALS_PER_KG
        constants["SMALL_ANIMAL_FAT_PER_KG"] = meat_and_dairy.SMALL_ANIMAL_FAT_PER_KG
        constants[
            "SMALL_ANIMAL_PROTEIN_PER_KG"
        ] = meat_and_dairy.SMALL_ANIMAL_PROTEIN_PER_KG

        constants["inputs"] = inputs_to_optimizer

        PRINT_FIRST_MONTH_CONSTANTS = False
        
        if(PRINT_FIRST_MONTH_CONSTANTS):
            self.print_constants(
                constants,
                time_consts,
                feed,
                stored_food,
                biofuels,
                methane_scp
            )

        return (constants, time_consts)

    def print_constants(
        self,
        constants,
        time_consts,
        feed,
        stored_food,
        biofuels,
        methane_scp):

        # used by world population
        print("")
        print("calories consumed per day")
        print(constants["KCALS_DAILY"])
        print("fat consumed per day grams")
        print(constants["FAT_DAILY"])
        print("protein consumed per day grams")
        print(constants["PROTEIN_DAILY"])
        print("")
        print(
            "INITIAL_HUMANS_KCALS "
            + str(self.POP)
            + " people consumed million tons dry caloric monthly"
        )
        print(-self.POP * self.KCALS_MONTHLY / 4e6 / 1e6)
        print(
            "INITIAL_HUMANS_FAT "
            + str(self.POP)
            + " people consumed million tons monthly"
        )
        print(-self.POP * self.FAT_MONTHLY / 1e3)
        print(
            "INITIAL_HUMANS_PROTEIN "
            + str(self.POP)
            + " people consumed million tons monthly"
        )
        print(-self.POP * self.PROTEIN_MONTHLY / 1e3)
        print("")
        # 1000 tons protein or fat per dry caloric ton
        print("INITIAL_HUMANS_FAT consumed percentage")
        print(
            100
            * self.POP
            * self.FAT_MONTHLY
            / 1e3
            / (self.POP * self.KCALS_MONTHLY / 4e6 / 1e6)
        )
        print("INITIAL_HUMANS_PROTEIN consumed percentage")
        print(
            100
            * self.POP
            * self.PROTEIN_MONTHLY
            / 1e3
            / (self.POP * self.KCALS_MONTHLY / 4e6 / 1e6)
        )

        CFP = time_consts["crops_food_produced"][0]
        OG_RF_KCALS = constants["OG_ROTATION_FRACTION_KCALS"]
        OG_RF_FAT = constants["OG_ROTATION_FRACTION_FAT"]
        OG_RF_PROTEIN = constants["OG_ROTATION_FRACTION_PROTEIN"]

        # 1000 tons protein or fat per dry caloric ton
        print("")
        print("INITIAL_OG_KCALS million tons dry caloric monthly")
        print(CFP * 1e9 / 4e6 / 1e6)
        print("INITIAL_OG_FAT million tons monthly")
        print(CFP * constants["OG_FRACTION_FAT"] / 1e3)
        print("INITIAL_OG_PROTEIN million tons monthly")
        print(CFP * constants["OG_FRACTION_PROTEIN"] / 1e3)
        print("")
        print("INITIAL_OG_FAT percentage")
        print(100 * CFP * constants["OG_FRACTION_FAT"] / 1e3 / (CFP * 1e9 / 4e6 / 1e6))
        print("INITIAL_OG_PROTEIN percentage")
        print(
            100 * CFP * constants["OG_FRACTION_PROTEIN"] / 1e3 / (CFP * 1e9 / 4e6 / 1e6)
        )
        print("")
        print("INITIAL_OG_ROTATION_KCALS million tons dry caloric monthly")
        print(CFP * OG_RF_KCALS * 1e9 / 4e6 / 1e6)
        print("INITIAL_OG_ROTATION_FAT million tons monthly")
        print(CFP * OG_RF_FAT / 1e3)
        print("INITIAL_OG_ROTATION_PROTEIN million tons monthly")
        print(CFP * OG_RF_PROTEIN / 1e3)
        print("")
        print("INITIAL_OG_ROTATION_FAT percentage")
        print(100 * CFP * OG_RF_FAT / 1e3 / (CFP * OG_RF_KCALS * 1e9 / 4e6 / 1e6))
        print("INITIAL_OG_ROTATION_PROTEIN percentage")
        print(
            100
            * CFP
            * OG_RF_PROTEIN
            / 1e3
            / (time_consts["crops_food_produced"][0] * OG_RF_KCALS * 1e9 / 4e6 / 1e6)
        )

        INITIAL_SF_KCALS = constants["INITIAL_SF_KCALS"]
        SF_FRACTION_FAT = constants["SF_FRACTION_FAT"]
        SF_FRACTION_PROTEIN = constants["SF_FRACTION_PROTEIN"]

        print("")
        print("INITIAL_SF_KCALS million tons dry caloric")
        print(INITIAL_SF_KCALS * 1e9 / 4e6 / 1e6)
        print("INITIAL_SF_FAT million tons")
        print(INITIAL_SF_KCALS * SF_FRACTION_FAT / 1e3)
        print("INITIAL_SF_PROTEIN million tons")
        print(INITIAL_SF_KCALS * SF_FRACTION_PROTEIN / 1e3)
        print("")
        print("INITIAL_SF_FAT percentage")
        print(
            100
            * INITIAL_SF_KCALS
            * SF_FRACTION_FAT
            / 1e3
            / (INITIAL_SF_KCALS * 1e9 / 4e6 / 1e6)
        )
        print("INITIAL_SF_PROTEIN percentage")
        print(
            100
            * INITIAL_SF_KCALS
            * SF_FRACTION_PROTEIN
            / 1e3
            / (INITIAL_SF_KCALS * 1e9 / 4e6 / 1e6)
        )
        if feed.FEED_MONTHLY_USAGE_KCALS > 0:
            print("")
            print("INITIAL_FEED_KCALS million tons dry caloric monthly")
            print(-feed.FEED_MONTHLY_USAGE_KCALS * 1e9 / 4e6 / 1e6)
            print("INITIAL_FEED_FAT million tons monthly")
            print(-feed.FEED_MONTHLY_USAGE_FAT / 1e3)
            print("INITIAL_FEED_PROTEIN million tons monthly")
            print(-feed.FEED_MONTHLY_USAGE_PROTEIN / 1e3)
            print("")
            print("INITIAL_FEED_FAT percentage")
            print(
                100
                * feed.FEED_MONTHLY_USAGE_FAT
                / 1e3
                / (feed.FEED_MONTHLY_USAGE_KCALS * 1e9 / 4e6 / 1e6)
            )
            print("INITIAL_FEED_PROTEIN percentage")
            print(
                100
                * feed.FEED_MONTHLY_USAGE_PROTEIN
                / 1e3
                / (feed.FEED_MONTHLY_USAGE_KCALS * 1e9 / 4e6 / 1e6)
            )
            print("")
            CPM = np.array(self.chicken_pork_kcals)[0]
            LARGE_ANIMAL_KCALS_PER_KG = constants["LARGE_ANIMAL_KCALS_PER_KG"]
            LARGE_ANIMAL_FAT_PER_KG = constants["LARGE_ANIMAL_FAT_PER_KG"]
            LARGE_ANIMAL_PROTEIN_PER_KG = constants["LARGE_ANIMAL_PROTEIN_PER_KG"]
            CM = (
                np.array(self.cattle_h_e_maintained)[0]
                * 1000
                * constants["LARGE_ANIMAL_KCALS_PER_KG"]
                / 1e9
            )
            if CPM > 0:
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
                print(
                    100 * self.chicken_pork_protein[0] / 1e3 / (CPM * 1e9 / 4e6 / 1e6)
                )
                print("")
            else:
                print("no chicken pork maintained")
                print("")
            if CM > 0:
                print("INITIAL_CM_KCALS million tons dry caloric monthly")
                print(CM * 1e9 / 4e6 / 1e6)

                print("INITIAL_CM_FAT million tons monthly")
                print(
                    CM
                    * 1e9
                    / LARGE_ANIMAL_KCALS_PER_KG
                    * LARGE_ANIMAL_FAT_PER_KG
                    / 1e6
                    / 1e3
                )
                print("INITIAL_CM_PROTEIN million tons monthly")
                print(
                    CM
                    * 1e9
                    / LARGE_ANIMAL_KCALS_PER_KG
                    * LARGE_ANIMAL_PROTEIN_PER_KG
                    / 1e6
                    / 1e3
                )
                print("")
                print("INITIAL_CM_FAT percentage")
                print(
                    100
                    * CM
                    * 1e9
                    / LARGE_ANIMAL_KCALS_PER_KG
                    * LARGE_ANIMAL_FAT_PER_KG
                    / 1e6
                    / 1e3
                    / (CM * 1e9 / 4e6 / 1e6)
                )
                print("INITIAL_CM_PROTEIN percentage")
                print(
                    100
                    * CM
                    * 1e9
                    / LARGE_ANIMAL_KCALS_PER_KG
                    * LARGE_ANIMAL_PROTEIN_PER_KG
                    / 1e6
                    / 1e3
                    / (CM * 1e9 / 4e6 / 1e6)
                )
                print("")
                print("culled chicken, pork, and cattle per month.")
                print(
                    "reaches minimum after "
                    + str(constants["CULL_DURATION_MONTHS"])
                    + " months"
                )
            else:
                print("no cattle maintained from human edible")
                print("")

            MEAT_WASTE = constants["inputs"]["WASTE"]["MEAT"]

            CM_IN_KCALS = time_consts["cattle_maintained_kcals"][0] / (
                1 - MEAT_WASTE / 100
            )
            CM_IN_FAT = time_consts["cattle_maintained_fat"][0] / (1 - MEAT_WASTE / 100)
            CM_IN_PROTEIN = time_consts["cattle_maintained_protein"][0] / (
                1 - MEAT_WASTE / 100
            )

            if CM_IN_KCALS > 0:
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
            if constants["inputs"]["CULL_ANIMALS"]:
                print("INITIAL_CULLED_KCALS million tons dry caloric monthly")
                print("INITIAL_CULLED_FAT million tons monthly")
                print("INITIAL_CULLED_PROTEIN million tons monthly")
                print("")
                print("INITIAL_CULLED_FAT percentage")
                print("INITIAL_CULLED_PROTEIN percentage")
                print("")
        else:
            print("No Feed Usage")

        if constants["ADD_DAIRY"]:
            dairy_milk_kcals = time_consts["dairy_milk_kcals"][0]
            dairy_milk_fat = time_consts["dairy_milk_fat"][0]
            dairy_milk_protein = time_consts["dairy_milk_protein"][0]
            DAIRY_WASTE = constants["inputs"]["WASTE"]["DAIRY"]
            print("INITIAL_DAIRY_KCALS million tons dry caloric monthly")
            print(dairy_milk_kcals / (1 - DAIRY_WASTE / 100) * 1e9 / 4e6 / 1e6)

            print("INITIAL_DAIRY_FAT million tons monthly")
            print(dairy_milk_fat / (1 - DAIRY_WASTE / 100) / 1e3)
            print("INITIAL_DAIRY_PROTEIN million tons monthly")
            print(dairy_milk_protein / (1 - DAIRY_WASTE / 100) / 1e3)
            print("")
            print("INITIAL_DAIRY_FAT percentage")
            print(
                100
                * dairy_milk_fat
                / (1 - DAIRY_WASTE / 100)
                / 1e3
                / (dairy_milk_kcals / (1 - DAIRY_WASTE / 100) * 1e9 / 4e6 / 1e6)
            )
            print("INITIAL_DAIRY_PROTEIN percentage")
            print(
                100
                * dairy_milk_protein
                / (1 - DAIRY_WASTE / 100)
                / 1e3
                / (dairy_milk_kcals / (1 - DAIRY_WASTE / 100) * 1e9 / 4e6 / 1e6)
            )
            print("")
        if constants["ADD_FISH"]:
            FISH_WASTE = constants["inputs"]["WASTE"]["SEAFOOD"]
            production_kcals_fish_per_month = time_consts[
                "production_kcals_fish_per_month"
            ][0]
            production_fat_fish_per_month = time_consts[
                "production_fat_fish_per_month"
            ][0]
            production_protein_fish_per_month = time_consts[
                "production_protein_fish_per_month"
            ][0]

            print("INITIAL_FISH_KCALS million tons dry caloric monthly")
            print(
                production_kcals_fish_per_month
                / (1 - FISH_WASTE / 100)
                * 1e9
                / 4e6
                / 1e6
            )

            print("INITIAL_FISH_PROTEIN million tons monthly")
            print(production_protein_fish_per_month / (1 - FISH_WASTE / 100) / 1e3)
            print("INITIAL_FISH_FAT million tons monthly")
            print(production_fat_fish_per_month / (1 - FISH_WASTE / 100) / 1e3)
            print("")
            print("INITIAL_FISH_FAT percentage")
            print(
                100
                * production_fat_fish_per_month
                / (1 - FISH_WASTE / 100)
                / 1e3
                / (
                    production_kcals_fish_per_month
                    / (1 - FISH_WASTE / 100)
                    * 1e9
                    / 4e6
                    / 1e6
                )
            )
            print("INITIAL_FISH_PROTEIN percentage")
            print(
                100
                * production_protein_fish_per_month
                / (1 - FISH_WASTE / 100)
                / 1e3
                / (
                    production_kcals_fish_per_month
                    / (1 - FISH_WASTE / 100)
                    * 1e9
                    / 4e6
                    / 1e6
                )
            )
            print("")
            print("")
        if time_consts["biofuels_kcals"][0] > 0:
            # 1000 tons protein/fat per dry caloric ton
            print("INITIAL_BIOFUEL_KCALS million tons dry caloric monthly")
            print(-biofuels.BIOFUEL_MONTHLY_USAGE_KCALS * 1e9 / 4e6 / 1e6)
            print("INITIAL_BIOFUEL_FAT million tons monthly")
            print(-biofuels.BIOFUEL_MONTHLY_USAGE_FAT / 1e3)
            print("INITIAL_BIOFUEL_PROTEIN million tons monthly")
            print(-biofuels.BIOFUEL_MONTHLY_USAGE_PROTEIN / 1e3)
            print("INITIAL_BIOFUEL_FAT percentage")
            print(
                100
                * biofuels.BIOFUEL_MONTHLY_USAGE_FAT
                / 1e3
                / (biofuels.BIOFUEL_MONTHLY_USAGE_KCALS * 1e9 / 4e6 / 1e6)
            )
            print("INITIAL_BIOFUEL_PROTEIN percentage")
            print(
                100
                * biofuels.BIOFUEL_MONTHLY_USAGE_PROTEIN
                / 1e3
                / (biofuels.BIOFUEL_MONTHLY_USAGE_KCALS * 1e9 / 4e6 / 1e6)
            )
        else:
            print("No biofuel usage")
            print("")

        if constants["ADD_METHANE_SCP"]:
            production_kcals_scp_per_month = time_consts[
                "production_kcals_scp_per_month"
            ]
            production_fat_scp_per_month = time_consts["production_fat_scp_per_month"]
            production_protein_scp_per_month = time_consts[
                "production_protein_scp_per_month"
            ]
            print("daily calories SCP")
            print(
                np.array(production_kcals_scp_per_month)
                * 1e9
                / self.DAYS_IN_MONTH
                / self.POP
            )
            print("daily kg SCP")
            print(
                np.array(production_kcals_scp_per_month)
                * 1e9
                / self.DAYS_IN_MONTH
                / self.POP
                / methane_scp.SCP_KCALS_PER_KG
            )
            print("daily grams protein SCP")
            print(
                np.array(production_kcals_scp_per_month)
                * 1e9
                / self.DAYS_IN_MONTH
                / self.POP
                / methane_scp.SCP_KCALS_PER_KG
                * methane_scp.SCP_FRAC_PROTEIN
                * 1000
            )
            print("1000 tons per month protein SCP")
            print(
                np.array(production_kcals_scp_per_month)
                * 1e9
                / methane_scp.SCP_KCALS_PER_KG
                * methane_scp.SCP_FRAC_PROTEIN
                / 1e6
            )
