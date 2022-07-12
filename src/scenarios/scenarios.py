################################ Scenarios ####################################
##                                                                            #
##                  Provides numbers and methods to set the                   #
##                    specific scenario to be optimized                       #
##                                                                            #
###############################################################################

import numpy as np


class Scenarios:
    def set_immediate_shutoff(self, inputs_to_optimizer):
        inputs_to_optimizer["DELAY"]["FEED_SHUTOFF_MONTHS"] = 0
        inputs_to_optimizer["DELAY"]["BIOFUEL_SHUTOFF_MONTHS"] = 0

        return inputs_to_optimizer

    def set_short_delayed_shutoff(self, inputs_to_optimizer):
        inputs_to_optimizer["DELAY"]["FEED_SHUTOFF_MONTHS"] = 2
        inputs_to_optimizer["DELAY"]["BIOFUEL_SHUTOFF_MONTHS"] = 1

        return inputs_to_optimizer

    def set_long_delayed_shutoff(self, inputs_to_optimizer):
        inputs_to_optimizer["DELAY"]["FEED_SHUTOFF_MONTHS"] = 3
        inputs_to_optimizer["DELAY"]["BIOFUEL_SHUTOFF_MONTHS"] = 2

        return inputs_to_optimizer

    def set_continued_feed_biofuels(self, inputs_to_optimizer):
        inputs_to_optimizer["DELAY"]["FEED_SHUTOFF_MONTHS"] = inputs_to_optimizer[
            "NMONTHS"
        ]
        inputs_to_optimizer["DELAY"]["BIOFUEL_SHUTOFF_MONTHS"] = inputs_to_optimizer[
            "NMONTHS"
        ]

        return inputs_to_optimizer

    def set_waste_to_zero(self, inputs_to_optimizer):
        inputs_to_optimizer["WASTE"] = {}
        inputs_to_optimizer["WASTE"]["SUGAR"] = 0  # %
        inputs_to_optimizer["WASTE"]["MEAT"] = 0  # %
        inputs_to_optimizer["WASTE"]["DAIRY"] = 0  # %
        inputs_to_optimizer["WASTE"]["SEAFOOD"] = 0  # %
        inputs_to_optimizer["WASTE"]["CROPS"] = 0  # %
        inputs_to_optimizer["WASTE"]["SEAWEED"] = 0  # %

        return inputs_to_optimizer

    def set_waste_to_tripled_prices(self, inputs_to_optimizer):
        # nuclear winter 150 tab, cell G30-G38  https://docs.google.com/spreadsheets/d/14t3_PUIky6aNiBvw8q24sj6QYxCN9s_VddLY2-eJuPE/edit#gid=1637082097
        # overall waste, on farm + distribution + retail
        # 3x prices (note, currently set to 2019, not 2020)
        inputs_to_optimizer["WASTE"] = {}
        # inputs_to_optimizer['WASTE']['CEREALS'] = 14.46  # %
        inputs_to_optimizer["WASTE"]["SUGAR"] = 9.91  # %
        inputs_to_optimizer["WASTE"]["MEAT"] = 10.61  # %
        inputs_to_optimizer["WASTE"]["DAIRY"] = 11.93  # %
        inputs_to_optimizer["WASTE"]["SEAFOOD"] = 9.99  # %
        inputs_to_optimizer["WASTE"]["CROPS"] = 14.78  # %
        inputs_to_optimizer["WASTE"]["SEAWEED"] = 9.81  # %

        return inputs_to_optimizer

    def set_waste_to_doubled_prices(self, inputs_to_optimizer):
        # nuclear winter 150 tab, cell G30-G38  https://docs.google.com/spreadsheets/d/14t3_PUIky6aNiBvw8q24sj6QYxCN9s_VddLY2-eJuPE/edit#gid=1637082097
        # overall waste, on farm + distribution + retail
        # 2x prices (note, currently set to 2019, not 2020)
        inputs_to_optimizer["WASTE"] = {}
        # inputs_to_optimizer['WASTE']['CEREALS'] = 19.02 #%
        inputs_to_optimizer["WASTE"]["SUGAR"] = 14.47  # %
        inputs_to_optimizer["WASTE"]["MEAT"] = 15.17  # %
        inputs_to_optimizer["WASTE"]["DAIRY"] = 16.49  # %
        inputs_to_optimizer["WASTE"]["SEAFOOD"] = 14.55  # %
        inputs_to_optimizer["WASTE"]["CROPS"] = 19.33  # %
        inputs_to_optimizer["WASTE"]["SEAWEED"] = 14.37  # %

        return inputs_to_optimizer

    def set_waste_to_baseline_prices(self, inputs_to_optimizer):
        # nuclear winter 150 tab, cell G30-G38  https://docs.google.com/spreadsheets/d/14t3_PUIky6aNiBvw8q24sj6QYxCN9s_VddLY2-eJuPE/edit#gid=1637082097
        # overall waste, on farm+distribution+retail
        # 1x prices (note, currently set to 2019, not 2020)
        inputs_to_optimizer["WASTE"] = {}
        inputs_to_optimizer["WASTE"]["CEREALS"] = 28.52  # %
        inputs_to_optimizer["WASTE"]["SUGAR"] = 23.96  # %
        inputs_to_optimizer["WASTE"]["MEAT"] = 24.67  # %
        inputs_to_optimizer["WASTE"]["DAIRY"] = 25.99  # %
        inputs_to_optimizer["WASTE"]["SEAFOOD"] = 24.04  # %
        inputs_to_optimizer["WASTE"]["CROPS"] = 28.83  # %
        inputs_to_optimizer["WASTE"]["SEAWEED"] = 23.87  # %

        return inputs_to_optimizer

    def set_baseline_nutrition_profile(self, inputs_to_optimizer):

        inputs_to_optimizer["NUTRITION"] = {}

        # kcals per person per day
        inputs_to_optimizer["NUTRITION"]["KCALS_DAILY"] = 2100

        # grams per person per day
        inputs_to_optimizer["NUTRITION"]["FAT_DAILY"] = 61.7

        # grams per person per day
        inputs_to_optimizer["NUTRITION"]["PROTEIN_DAILY"] = 59.5

        return inputs_to_optimizer

    def set_catastrophe_nutrition_profile(self, inputs_to_optimizer):

        inputs_to_optimizer["NUTRITION"] = {}

        # kcals per person per day
        inputs_to_optimizer["NUTRITION"]["KCALS_DAILY"] = 2100

        # grams per person per day
        inputs_to_optimizer["NUTRITION"]["FAT_DAILY"] = 47

        # grams per person per day
        inputs_to_optimizer["NUTRITION"]["PROTEIN_DAILY"] = 51

        return inputs_to_optimizer

    def set_stored_food_all_used(self, inputs_to_optimizer):
        # "Outputs" https://docs.google.com/spreadsheets/d/19kzHpux690JTCo2IX2UA1faAd7R1QcBK/edit#gid=1815939673 cell G12-G14
        inputs_to_optimizer["TONS_DRY_CALORIC_EQIVALENT_SF"] = inputs_to_optimizer[
            "TONS_DRY_CALORIC_EQIVALENT_SF_AVAILABLE"
        ]
        return inputs_to_optimizer

    def set_stored_food_usage_as_may_till_minimum(self, inputs_to_optimizer):
        # "Outputs" https://docs.google.com/spreadsheets/d/19kzHpux690JTCo2IX2UA1faAd7R1QcBK/edit#gid=1815939673 cell G12-G14
        inputs_to_optimizer["TONS_DRY_CALORIC_EQIVALENT_SF"] = (
            inputs_to_optimizer["TONS_DRY_CALORIC_EQIVALENT_SF_AVAILABLE"] * 0.26
        )
        return inputs_to_optimizer

    def set_stored_food_usage_as_80_percent_used(self, inputs_to_optimizer):
        # "Outputs" https://docs.google.com/spreadsheets/d/19kzHpux690JTCo2IX2UA1faAd7R1QcBK/edit#gid=1815939673 cell G12-G14
        inputs_to_optimizer["TONS_DRY_CALORIC_EQIVALENT_SF"] = (
            inputs_to_optimizer["TONS_DRY_CALORIC_EQIVALENT_SF_AVAILABLE"] * 0.80
        )
        return inputs_to_optimizer

    def set_country_seasonality_baseline(self, inputs_to_optimizer, country_data):

        # fractional production per month
        inputs_to_optimizer["SEASONALITY"] = [
            country_data["seasonality_m" + str(i)] for i in range(1, 13)
        ]

        # tons dry caloric monthly
        inputs_to_optimizer["HUMAN_INEDIBLE_FEED"] = (
            np.array(
                [country_data["grasses_baseline"]] * inputs_to_optimizer["NMONTHS"]
            )
            / 12
        )

        return inputs_to_optimizer

    def set_country_seasonality_nuclear_winter(self, inputs_to_optimizer, country_data):

        # fractional production per month
        inputs_to_optimizer["SEASONALITY"] = [
            country_data["seasonality_m" + str(i)] for i in range(1, 13)
        ]

        inputs_to_optimizer["HUMAN_INEDIBLE_FEED"] = np.array(
            list(
                np.array([country_data["grasses_year1"]] * 8),
                np.array([country_data["grasses_year2"]] * 12),
                np.array([country_data["grasses_year3"]] * 12),
                np.array([country_data["grasses_year4"]] * 12),
                np.array([country_data["grasses_year5"]] * 12),
                np.array([country_data["grasses_year6"]] * 12),
                np.array([country_data["grasses_year7"]] * 12),
                np.array([country_data["grasses_year8"]] * 12),
                np.array([country_data["grasses_year9"]] * 12),
                np.array([country_data["grasses_year10"]] * 12),
            )
        )
        return inputs_to_optimizer

    def set_global_seasonality_baseline(self, inputs_to_optimizer):

        # fractional production per month
        inputs_to_optimizer["SEASONALITY"] = [
            0.1121,
            0.0178,
            0.0241,
            0.0344,
            0.0338,
            0.0411,
            0.0882,
            0.0791,
            0.1042,
            0.1911,
            0.1377,
            0.1365,
        ]

        # tons dry caloric monthly
        inputs_to_optimizer["HUMAN_INEDIBLE_FEED"] = (
            np.array([4206] * inputs_to_optimizer["NMONTHS"]) * 1e6 / 12
        )

        return inputs_to_optimizer

    def set_global_seasonality_nuclear_winter(self, inputs_to_optimizer):

        # most food grown in tropics, so set seasonality to typical in tropics
        # fractional production per month
        inputs_to_optimizer["SEASONALITY"] = [
            0.1564,
            0.0461,
            0.0650,
            0.1017,
            0.0772,
            0.0785,
            0.0667,
            0.0256,
            0.0163,
            0.1254,
            0.1183,
            0.1228,
        ]

        # tons dry caloric monthly
        inputs_to_optimizer["HUMAN_INEDIBLE_FEED"] = (
            np.array(
                [2728] * 8
                + [972] * 12
                + [594] * 12
                + [531] * 12
                + [552] * 12
                + [789] * 12
                + [1026] * 12
                + [1394] * 12
            )
            * 1e6
            / 12
        )

        return inputs_to_optimizer

    def init_global_food_system_properties(self):

        inputs_to_optimizer = {}

        ##########!!!!!!MOOOOOVEEEE MMEEEEEE!!!!!!######

        # the following are used for all scenarios
        inputs_to_optimizer["NMONTHS"] = 84

        # global stocks

        # not used unless smoothing true
        # useful for ensuring output variables don't fluctuate wildly
        inputs_to_optimizer["FLUCTUATION_LIMIT"] = 1.5

        inputs_to_optimizer["DELAY"] = {}
        inputs_to_optimizer["CULL_DURATION_MONTHS"] = 60

        ################################################

        # global human population (2020)
        inputs_to_optimizer["POP"] = 7.8e9

        # annual tons dry carb equivalent
        inputs_to_optimizer["BASELINE_CROP_KCALS"] = 3898e6

        # annual tons fat
        inputs_to_optimizer["BASELINE_CROP_FAT"] = 322e6

        # annual tons protein
        inputs_to_optimizer["BASELINE_CROP_PROTEIN"] = 350e6

        # annual tons dry carb equivalent
        inputs_to_optimizer["BIOFUEL_KCALS"] = 623e6

        # annual tons fat
        inputs_to_optimizer["BIOFUEL_FAT"] = 124e6

        # annual tons protein
        inputs_to_optimizer["BIOFUEL_PROTEIN"] = 32e6

        # annual tons dry carb equivalent
        inputs_to_optimizer["FEED_KCALS"] = 1385e6

        # annual tons fat
        inputs_to_optimizer["FEED_FAT"] = 60e6

        # annual tons protein
        inputs_to_optimizer["FEED_PROTEIN"] = 147e6

        # total head count of milk cattle
        inputs_to_optimizer["INITIAL_MILK_CATTLE"] = 264e6

        # total head count of small sized animals
        inputs_to_optimizer["INIT_SMALL_ANIMALS"] = 28.2e9

        # total head count of medium sized animals
        inputs_to_optimizer["INIT_MEDIUM_ANIMALS"] = 3.2e9

        # total head count of large sized animals minus milk cows
        inputs_to_optimizer["INIT_LARGE_ANIMALS_WITH_MILK_COWS"] = 1.9e9

        FISH_KCALS_PER_TON = 1310 * 1e3
        FISH_FAT_RATIO = 0.0048  # units: ton fat per ton wet
        FISH_PROTEIN_RATIO = 0.0204  # units: ton protein per ton wet

        # annual tons fish
        FISH_TONS_WET_2018 = 168936.71 * 1e3

        # converting from kcals to dry caloric tons:
        # 4e6 kcals = 1 dry caloric ton
        inputs_to_optimizer["FISH_DRY_CALORIC_ANNUAL"] = (
            FISH_TONS_WET_2018 * FISH_KCALS_PER_TON / 4e6
        )
        inputs_to_optimizer["FISH_FAT_TONS_ANNUAL"] = (
            FISH_TONS_WET_2018 * FISH_FAT_RATIO
        )
        inputs_to_optimizer["FISH_PROTEIN_TONS_ANNUAL"] = (
            FISH_TONS_WET_2018 * FISH_PROTEIN_RATIO
        )
        # annual tons milk production
        inputs_to_optimizer["TONS_DAIRY_ANNUAL"] = 879e6

        # annual tons chicken and pork production
        inputs_to_optimizer["TONS_CHICKEN_AND_PORK_ANNUAL"] = 250e6

        # annual tons cattle beef production
        inputs_to_optimizer["TONS_BEEF_ANNUAL"] = 74.2e6

        # total stored food available in the month of May in tons dry caloric,
        # if all of it were used for the whole earth, including private stocks
        inputs_to_optimizer["TONS_DRY_CALORIC_EQIVALENT_SF_AVAILABLE"] = 1360e6 * 0.96

        # Single cell protein fraction of global production
        inputs_to_optimizer["SCP_GLOBAL_PRODUCTION_FRACTION"] = 1

        # Cellulosic sugar fraction of global production
        inputs_to_optimizer["CS_GLOBAL_PRODUCTION_FRACTION"] = 1

        # 1000s of tons wet
        inputs_to_optimizer["INITIAL_SEAWEED"] = 1

        # 1000s of hectares
        inputs_to_optimizer["INITIAL_AREA"] = 1

        return inputs_to_optimizer

    def init_country_food_system_properties(self, country_data):

        inputs_to_optimizer = {}

        ##########!!!!!!MOOOOOVEEEE MMEEEEEE!!!!!!######

        # the following are used for all scenarios
        inputs_to_optimizer["NMONTHS"] = 84

        # not used unless smoothing true
        # useful for ensuring output variables don't fluctuate wildly
        inputs_to_optimizer["FLUCTUATION_LIMIT"] = 1.5

        inputs_to_optimizer["DELAY"] = {}
        inputs_to_optimizer["CULL_DURATION_MONTHS"] = 60

        ################################################

        # global human population (2020)
        inputs_to_optimizer["POP"] = country_data["population"]

        # annual tons dry carb equivalent
        inputs_to_optimizer["BASELINE_CROP_KCALS"] = country_data["crop_kcals"]

        # annual tons fat
        inputs_to_optimizer["BASELINE_CROP_FAT"] = country_data["crop_fat"]

        # annual tons protein
        inputs_to_optimizer["BASELINE_CROP_PROTEIN"] = country_data["crop_protein"]

        # annual tons dry carb equivalent
        inputs_to_optimizer["BIOFUEL_KCALS"] = country_data["biofuel_kcals"]

        # annual tons fat
        inputs_to_optimizer["BIOFUEL_FAT"] = country_data["biofuel_fat"]

        # annual tons protein
        inputs_to_optimizer["BIOFUEL_PROTEIN"] = country_data["biofuel_protein"]

        # annual tons dry carb equivalent
        inputs_to_optimizer["FEED_KCALS"] = country_data["feed_kcals"]

        # annual tons fat
        inputs_to_optimizer["FEED_FAT"] = country_data["feed_fat"]

        # annual tons protein
        inputs_to_optimizer["FEED_PROTEIN"] = country_data["feed_protein"]

        # total head count of milk cattle
        inputs_to_optimizer["INITIAL_MILK_CATTLE"] = country_data["dairy_cows"]

        # total head count of small sized animals
        inputs_to_optimizer["INIT_SMALL_ANIMALS"] = country_data["small_animals"]

        # total head count of medium sized animals
        inputs_to_optimizer["INIT_MEDIUM_ANIMALS"] = country_data["medium_animals"]

        # total head count of large sized animals minus milk cows
        inputs_to_optimizer["INIT_LARGE_ANIMALS_WITH_MILK_COWS"] = country_data[
            "large_animals"
        ]

        # fish kcals per month, billions
        inputs_to_optimizer["FISH_DRY_CALORIC_ANNUAL"] = country_data["aq_kcals"]

        # units of 1000s tons fat
        # (so, global value is in the tens of thousands of tons)
        inputs_to_optimizer["FISH_FAT_TONS_ANNUAL"] = country_data["aq_fat"]

        # units of 1000s tons protein monthly
        # (so, global value is in the hundreds of thousands of tons)
        inputs_to_optimizer["FISH_PROTEIN_TONS_ANNUAL"] = country_data["aq_protein"]

        # annual tons milk production
        inputs_to_optimizer["TONS_DAIRY_ANNUAL"] = country_data["dairy"]

        # annual tons chicken and pork production
        inputs_to_optimizer["TONS_CHICKEN_AND_PORK_ANNUAL"] = (
            country_data["chicken"] + country_data["pork"]
        )

        # annual tons cattle beef production
        inputs_to_optimizer["TONS_BEEF_ANNUAL"] = country_data["beef"]

        # total stored food available in the month of May in tons dry caloric,
        # if all of it were used for the whole earth, including private stocks.
        # The 0.96 comes from adjustment for whole world to match up
        # residuals in baseline scenario
        inputs_to_optimizer["TONS_DRY_CALORIC_EQIVALENT_SF_AVAILABLE"] = (
            country_data["stocks_kcals"] * 0.96
        )

        # TODO: ALTER THESE TO CORRECT CLOBAL FRACTIONS

        # Single cell protein fraction of global production
        inputs_to_optimizer["SCP_GLOBAL_PRODUCTION_FRACTION"] = 1

        # Cellulosic sugar fraction of global production
        inputs_to_optimizer["CS_GLOBAL_PRODUCTION_FRACTION"] = 1

        # 1000s of tons wet
        inputs_to_optimizer["INITIAL_SEAWEED"] = 1

        # 1000s of hectares
        inputs_to_optimizer["INITIAL_AREA"] = 1

        return inputs_to_optimizer

    def set_fish_nuclear_winter_reduction(self, inputs_to_optimizer):
        inputs_to_optimizer["FISH_PERCENT_MONTHLY"] = list(
            np.array(
                [
                    0.0,
                    -0.90909091,
                    -1.81818182,
                    -2.72727273,
                    -3.63636364,
                    -4.54545455,
                    -5.45454545,
                    -6.36363636,
                    -7.27272727,
                    -8.18181818,
                    -9.09090909,
                    -10,
                    -10.0,
                    -12.0,
                    -14.0,
                    -16.0,
                    -18.0,
                    -20.0,
                    -22.0,
                    -24.0,
                    -26.0,
                    -28.0,
                    -30.0,
                    -32.0,
                    -32.0,
                    -32.27272727,
                    -32.54545455,
                    -32.81818182,
                    -33.09090909,
                    -33.36363636,
                    -33.63636364,
                    -33.90909091,
                    -34.18181818,
                    -34.45454545,
                    -34.72727273,
                    -35.0,
                    -35.0,
                    -34.90909091,
                    -34.81818182,
                    -34.72727273,
                    -34.63636364,
                    -34.54545455,
                    -34.45454545,
                    -34.36363636,
                    -34.27272727,
                    -34.18181818,
                    -34.09090909,
                    -34.0,
                    -34.0,
                    -33.90909091,
                    -33.81818182,
                    -33.72727273,
                    -33.63636364,
                    -33.54545455,
                    -33.45454545,
                    -33.36363636,
                    -33.27272727,
                    -33.18181818,
                    -33.09090909,
                    -33.0,
                    -33.0,
                    -32.81818182,
                    -32.63636364,
                    -32.45454545,
                    -32.27272727,
                    -32.09090909,
                    -31.90909091,
                    -31.72727273,
                    -31.54545455,
                    -31.36363636,
                    -31.18181818,
                    -31.0,
                    -31.0,
                    -30.90909091,
                    -30.81818182,
                    -30.72727273,
                    -30.63636364,
                    -30.54545455,
                    -30.45454545,
                    -30.36363636,
                    -30.27272727,
                    -30.18181818,
                    -30.09090909,
                    -30.0,
                ]
            )
            + 100
        )

        return inputs_to_optimizer

    def set_fish_baseline(self, inputs_to_optimizer):
        # 100% of fishing remains in baseline
        inputs_to_optimizer["FISH_PERCENT_MONTHLY"] = np.array(
            [100] * inputs_to_optimizer["NMONTHS"]
        )

        return inputs_to_optimizer

    def set_disruption_to_crops_to_zero(self, inputs_to_optimizer):
        inputs_to_optimizer["DISRUPTION_CROPS_YEAR1"] = 0
        inputs_to_optimizer["DISRUPTION_CROPS_YEAR2"] = 0
        inputs_to_optimizer["DISRUPTION_CROPS_YEAR3"] = 0
        inputs_to_optimizer["DISRUPTION_CROPS_YEAR4"] = 0
        inputs_to_optimizer["DISRUPTION_CROPS_YEAR5"] = 0
        inputs_to_optimizer["DISRUPTION_CROPS_YEAR6"] = 0
        inputs_to_optimizer["DISRUPTION_CROPS_YEAR7"] = 0
        inputs_to_optimizer["DISRUPTION_CROPS_YEAR8"] = 0
        inputs_to_optimizer["DISRUPTION_CROPS_YEAR9"] = 0
        inputs_to_optimizer["DISRUPTION_CROPS_YEAR10"] = 0
        inputs_to_optimizer["DISRUPTION_CROPS_YEAR11"] = 0

        return inputs_to_optimizer

    def set_nuclear_winter_global_disruption_to_crops(self, inputs_to_optimizer):
        inputs_to_optimizer["DISRUPTION_CROPS_YEAR1"] = 0.53
        inputs_to_optimizer["DISRUPTION_CROPS_YEAR2"] = 0.82
        inputs_to_optimizer["DISRUPTION_CROPS_YEAR3"] = 0.89
        inputs_to_optimizer["DISRUPTION_CROPS_YEAR4"] = 0.88
        inputs_to_optimizer["DISRUPTION_CROPS_YEAR5"] = 0.84
        inputs_to_optimizer["DISRUPTION_CROPS_YEAR6"] = 0.76
        inputs_to_optimizer["DISRUPTION_CROPS_YEAR7"] = 0.65
        inputs_to_optimizer["DISRUPTION_CROPS_YEAR8"] = 0.5
        inputs_to_optimizer["DISRUPTION_CROPS_YEAR9"] = 0.33
        inputs_to_optimizer["DISRUPTION_CROPS_YEAR10"] = 0.17
        inputs_to_optimizer["DISRUPTION_CROPS_YEAR11"] = 0.08

        return inputs_to_optimizer

    def get_baseline_scenario(self, inputs_to_optimizer):

        inputs_to_optimizer["MAX_SEAWEED_AS_PERCENT_KCALS"] = 0
        inputs_to_optimizer["SEAWEED_NEW_AREA_PER_MONTH"] = 0
        inputs_to_optimizer["SEAWEED_PRODUCTION_RATE"] = 0
        inputs_to_optimizer["INDUSTRIAL_FOODS_SLOPE_MULTIPLIER"] = 0

        # these fat and protein values do not produce realistic outputs, so outdoor growing ratios were used instead
        # inputs_to_optimizer['INITIAL_SF_FAT'] = 166.07e3 * 351e6/1360e6
        # inputs_to_optimizer['INITIAL_SF_PROTEIN'] = 69.25e3 * 351e6/1360e6

        inputs_to_optimizer["OG_USE_BETTER_ROTATION"] = False

        inputs_to_optimizer["INCLUDE_PROTEIN"] = True
        inputs_to_optimizer["INCLUDE_FAT"] = True

        # (no difference between harvests in the different countries!)
        inputs_to_optimizer["INITIAL_HARVEST_DURATION_IN_MONTHS"] = 7

        inputs_to_optimizer["CULL_ANIMALS"] = False
        inputs_to_optimizer["KCAL_SMOOTHING"] = False
        inputs_to_optimizer["MEAT_SMOOTHING"] = False
        inputs_to_optimizer["STORED_FOOD_SMOOTHING"] = False

        inputs_to_optimizer["ADD_CELLULOSIC_SUGAR"] = False
        inputs_to_optimizer["ADD_DAIRY"] = True
        inputs_to_optimizer["ADD_FISH"] = True
        inputs_to_optimizer["ADD_GREENHOUSES"] = False
        inputs_to_optimizer["ADD_OUTDOOR_GROWING"] = True
        inputs_to_optimizer["ADD_MEAT"] = True
        inputs_to_optimizer["ADD_METHANE_SCP"] = False
        inputs_to_optimizer["ADD_SEAWEED"] = False
        inputs_to_optimizer["ADD_STORED_FOOD"] = True

        inputs_to_optimizer["GREENHOUSE_AREA_MULTIPLIER"] = 1 / 4

        return inputs_to_optimizer

    def get_resilient_food_scenario(self, inputs_to_optimizer):

        # maximize minimum of fat or protein or kcals
        inputs_to_optimizer["INCLUDE_PROTEIN"] = True
        inputs_to_optimizer["INCLUDE_FAT"] = True

        inputs_to_optimizer["MAX_SEAWEED_AS_PERCENT_KCALS"] = 10

        # units: 1000 km^2
        inputs_to_optimizer["SEAWEED_NEW_AREA_PER_MONTH"] = 2.0765 * 30

        # percent (seaweed)
        # represents 10% daily growth
        inputs_to_optimizer["SEAWEED_PRODUCTION_RATE"] = 100 * (1.1 ** 30 - 1)

        inputs_to_optimizer["OG_USE_BETTER_ROTATION"] = True
        inputs_to_optimizer["ROTATION_IMPROVEMENTS"] = {}
        inputs_to_optimizer["ROTATION_IMPROVEMENTS"]["KCALS_REDUCTION"] = 0.93
        inputs_to_optimizer["ROTATION_IMPROVEMENTS"]["FAT_RATIO"] = 1.487
        inputs_to_optimizer["ROTATION_IMPROVEMENTS"]["PROTEIN_RATIO"] = 1.108

        inputs_to_optimizer["GREENHOUSE_GAIN_PCT"] = 50

        # half values from greenhouse paper due to higher cost
        inputs_to_optimizer["GREENHOUSE_AREA_MULTIPLIER"] = 1 / 4
        inputs_to_optimizer[
            "INDUSTRIAL_FOODS_SLOPE_MULTIPLIER"
        ] = 1  # default values from CS and SCP papers

        inputs_to_optimizer["INITIAL_HARVEST_DURATION_IN_MONTHS"] = 7 + 1
        inputs_to_optimizer["DELAY"]["ROTATION_CHANGE_IN_MONTHS"] = 2
        inputs_to_optimizer["DELAY"]["INDUSTRIAL_FOODS_MONTHS"] = 3
        inputs_to_optimizer["DELAY"]["GREENHOUSE_MONTHS"] = 2
        inputs_to_optimizer["DELAY"]["SEAWEED_MONTHS"] = 1

        inputs_to_optimizer["CULL_ANIMALS"] = True
        inputs_to_optimizer["KCAL_SMOOTHING"] = True
        inputs_to_optimizer["MEAT_SMOOTHING"] = True
        inputs_to_optimizer["STORED_FOOD_SMOOTHING"] = True

        inputs_to_optimizer["ADD_CELLULOSIC_SUGAR"] = True
        inputs_to_optimizer["ADD_DAIRY"] = True
        inputs_to_optimizer["ADD_FISH"] = True
        inputs_to_optimizer["ADD_GREENHOUSES"] = True
        inputs_to_optimizer["ADD_OUTDOOR_GROWING"] = True
        inputs_to_optimizer["ADD_MEAT"] = True
        inputs_to_optimizer["ADD_METHANE_SCP"] = True
        inputs_to_optimizer["ADD_SEAWEED"] = True
        inputs_to_optimizer["ADD_STORED_FOOD"] = True

        ##### ERROR CHECKING, TO BE REMOVED WHEN SUFFICIENT BY-COUNTRY
        ##### RESILIENT FOOD DATA ARE AVAILABLE
        if inputs_to_optimizer["POP"] < 7e9:
            print("ERROR: CANNOT RUN RESILIENT FOOD SCENARIO WITH BY-COUNTRY")

            # this is just random stuff to cause a compile time error
            dsbginoempwrinrqjomeiwgnu

        return inputs_to_optimizer

    def get_no_resilient_food_scenario(self, inputs_to_optimizer):

        inputs_to_optimizer["MAX_SEAWEED_AS_PERCENT_KCALS"] = 0
        inputs_to_optimizer["SEAWEED_NEW_AREA_PER_MONTH"] = 0  # 1000 km^2 (seaweed)
        inputs_to_optimizer["SEAWEED_PRODUCTION_RATE"] = 0  # percent (seaweed)

        inputs_to_optimizer["OG_USE_BETTER_ROTATION"] = False

        inputs_to_optimizer["INCLUDE_PROTEIN"] = True
        inputs_to_optimizer["INCLUDE_FAT"] = True

        inputs_to_optimizer["GREENHOUSE_GAIN_PCT"] = 0

        inputs_to_optimizer[
            "GREENHOUSE_SLOPE_MULTIPLIER"
        ] = 1  # default values from greenhouse paper
        inputs_to_optimizer[
            "INDUSTRIAL_FOODS_SLOPE_MULTIPLIER"
        ] = 1  # default values from CS paper

        inputs_to_optimizer["INITIAL_HARVEST_DURATION_IN_MONTHS"] = 7

        inputs_to_optimizer["CULL_ANIMALS"] = True
        inputs_to_optimizer["KCAL_SMOOTHING"] = False
        inputs_to_optimizer["MEAT_SMOOTHING"] = True
        inputs_to_optimizer["STORED_FOOD_SMOOTHING"] = True

        inputs_to_optimizer["ADD_CELLULOSIC_SUGAR"] = False
        inputs_to_optimizer["ADD_DAIRY"] = False
        inputs_to_optimizer["ADD_FISH"] = True
        inputs_to_optimizer["ADD_GREENHOUSES"] = False
        inputs_to_optimizer["ADD_OUTDOOR_GROWING"] = True
        inputs_to_optimizer["ADD_MEAT"] = False
        inputs_to_optimizer["ADD_METHANE_SCP"] = False
        inputs_to_optimizer["ADD_SEAWEED"] = False
        inputs_to_optimizer["ADD_STORED_FOOD"] = True

        inputs_to_optimizer["SEASONALITY"] = [
            0.1564,
            0.0461,
            0.0650,
            0.1017,
            0.0772,
            0.0785,
            0.0667,
            0.0256,
            0.0163,
            0.1254,
            0.1183,
            0.1228,
        ]

        ##### ERROR CHECKING, TO BE REMOVED WHEN SUFFICIENT BY-COUNTRY
        ##### RESILIENT FOOD DATA ARE AVAILABLE
        if inputs_to_optimizer["POP"] < 7e9:
            print("ERROR: CANNOT RUN RESILIENT FOOD SCENARIO WITH BY-COUNTRY")
            print("THIS IS BECAUSE WE HAVE NOT YET IMPORTED BY-COUNTRY CROP")
            print("PRODUCTION IN A NUCLEAR WINTER")

            # this is just random stuff to cause a compile time error
            dsbginoempwrinrqjomeiwgnu

        return inputs_to_optimizer
