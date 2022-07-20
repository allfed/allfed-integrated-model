################################ Scenarios ####################################
##                                                                            #
##                  Provides numbers and methods to set the                   #
##                    specific scenario to be optimized                       #
##                                                                            #
###############################################################################

import numpy as np


class Scenarios:

    # FEED AND BIOFUELS

    def set_immediate_shutoff(self, constants_for_params):
        constants_for_params["DELAY"]["FEED_SHUTOFF_MONTHS"] = 0
        constants_for_params["DELAY"]["BIOFUEL_SHUTOFF_MONTHS"] = 0

        return constants_for_params

    def set_short_delayed_shutoff(self, constants_for_params):
        constants_for_params["DELAY"]["FEED_SHUTOFF_MONTHS"] = 2
        constants_for_params["DELAY"]["BIOFUEL_SHUTOFF_MONTHS"] = 1

        return constants_for_params

    def set_long_delayed_shutoff(self, constants_for_params):
        constants_for_params["DELAY"]["FEED_SHUTOFF_MONTHS"] = 3
        constants_for_params["DELAY"]["BIOFUEL_SHUTOFF_MONTHS"] = 2

        return constants_for_params

    def set_continued_feed_biofuels(self, constants_for_params):
        constants_for_params["DELAY"]["FEED_SHUTOFF_MONTHS"] = constants_for_params[
            "NMONTHS"
        ]
        constants_for_params["DELAY"]["BIOFUEL_SHUTOFF_MONTHS"] = constants_for_params[
            "NMONTHS"
        ]

        return constants_for_params

    # WASTE

    def set_waste_to_zero(self, constants_for_params):
        constants_for_params["WASTE"] = {}
        constants_for_params["WASTE"]["SUGAR"] = 0  # %
        constants_for_params["WASTE"]["MEAT"] = 0  # %
        constants_for_params["WASTE"]["DAIRY"] = 0  # %
        constants_for_params["WASTE"]["SEAFOOD"] = 0  # %
        constants_for_params["WASTE"]["CROPS"] = 0  # %
        constants_for_params["WASTE"]["SEAWEED"] = 0  # %

        return constants_for_params

    def get_total_global_waste(self, retail_waste):
        """
        Calculates the total waste of the global food system by adding retail waste
        to distribution loss.
        """

        distribution_loss = {}

        distribution_loss["SUGAR"] = 0.09
        distribution_loss["CROPS"] = 4.96
        distribution_loss["MEAT"] = 0.80
        distribution_loss["DAIRY"] = 2.12
        distribution_loss["SEAFOOD"] = 0.17
        distribution_loss["SEAWEED"] = distribution_loss["SEAFOOD"]

        total_waste = {}

        total_waste["SUGAR"] = distribution_loss["SUGAR"] + retail_waste
        total_waste["CROPS"] = distribution_loss["CROPS"] + retail_waste
        total_waste["MEAT"] = distribution_loss["MEAT"] + retail_waste
        total_waste["DAIRY"] = distribution_loss["DAIRY"] + retail_waste
        total_waste["SEAFOOD"] = distribution_loss["SEAFOOD"] + retail_waste
        total_waste["SEAWEED"] = distribution_loss["SEAWEED"] + retail_waste

        return total_waste

    def set_global_waste_to_tripled_prices(self, constants_for_params):
        """
        overall waste, on farm + distribution + retail
        3x prices (note, currently set to 2019, not 2020)
        """
        RETAIL_WASTE = 5.75

        total_waste = self.get_total_global_waste(RETAIL_WASTE)

        constants_for_params["WASTE"] = total_waste

        return constants_for_params

    def set_global_waste_to_doubled_prices(self, constants_for_params):
        """
        overall waste, on farm + distribution + retail
        2x prices (note, currently set to 2019, not 2020)
        """

        RETAIL_WASTE = 10.04

        total_waste = self.get_total_global_waste(RETAIL_WASTE)

        constants_for_params["WASTE"] = total_waste

        return constants_for_params

    def set_global_waste_to_baseline_prices(self, constants_for_params):
        """
        overall waste, on farm+distribution+retail
        1x prices (note, currently set to 2019, not 2020)
        """
        RETAIL_WASTE = 23.87

        total_waste = self.get_total_global_waste(RETAIL_WASTE)

        constants_for_params["WASTE"] = total_waste

        return constants_for_params

    def get_total_country_waste(self, retail_waste, country_data):
        """
        Calculates the total waste of the global food system by adding retail waste
        to distribution loss.
        """

        distribution_loss = {}

        distribution_loss["SUGAR"] = country_data["distribution_loss_sugar"]
        distribution_loss["CROPS"] = country_data["distribution_loss_crops"]
        distribution_loss["MEAT"] = country_data["distribution_loss_meat"]
        distribution_loss["DAIRY"] = country_data["distribution_loss_dairy"]
        distribution_loss["SEAFOOD"] = country_data["distribution_loss_seafood"]
        distribution_loss["SEAWEED"] = distribution_loss["SEAFOOD"]

        total_waste = {}

        total_waste["SUGAR"] = distribution_loss["SUGAR"] + retail_waste
        total_waste["CROPS"] = distribution_loss["CROPS"] + retail_waste
        total_waste["MEAT"] = distribution_loss["MEAT"] + retail_waste
        total_waste["DAIRY"] = distribution_loss["DAIRY"] + retail_waste
        total_waste["SEAFOOD"] = distribution_loss["SEAFOOD"] + retail_waste
        total_waste["SEAWEED"] = distribution_loss["SEAWEED"] + retail_waste

        return total_waste

    def set_country_waste_to_tripled_prices(self, constants_for_params, country_data):
        """
        overall waste, on farm + distribution + retail
        3x prices (note, currently set to 2019, not 2020)
        """

        RETAIL_WASTE = country_data["retail_waste_price_tripled"]

        total_waste = self.get_total_country_waste(RETAIL_WASTE)

        constants_for_params["WASTE"] = total_waste

        return constants_for_params

    def set_country_waste_to_doubled_prices(self, constants_for_params, country_data):
        """
        overall waste, on farm + distribution + retail
        2x prices (note, currently set to 2019, not 2020)
        """

        RETAIL_WASTE = country_data["retail_waste_price_doubled"]

        total_waste = self.get_total_country_waste(RETAIL_WASTE)

        constants_for_params["WASTE"] = total_waste

        return constants_for_params

    def set_country_waste_to_baseline_prices(self, constants_for_params, country_data):
        """
        overall waste, on farm+distribution+retail
        1x prices (note, currently set to 2019, not 2020)
        """
        RETAIL_WASTE = country_data["retail_waste_baseline"]

        total_waste = self.get_total_country_waste(RETAIL_WASTE)

        constants_for_params["WASTE"] = total_waste

        return constants_for_params

    # NUTRITION

    def set_baseline_nutrition_profile(self, constants_for_params):

        constants_for_params["NUTRITION"] = {}

        # kcals per person per day
        constants_for_params["NUTRITION"]["KCALS_DAILY"] = 2100

        # grams per person per day
        constants_for_params["NUTRITION"]["FAT_DAILY"] = 61.7

        # grams per person per day
        constants_for_params["NUTRITION"]["PROTEIN_DAILY"] = 59.5

        return constants_for_params

    def set_catastrophe_nutrition_profile(self, constants_for_params):

        constants_for_params["NUTRITION"] = {}

        # kcals per person per day
        constants_for_params["NUTRITION"]["KCALS_DAILY"] = 2100

        # grams per person per day
        constants_for_params["NUTRITION"]["FAT_DAILY"] = 47

        # grams per person per day
        constants_for_params["NUTRITION"]["PROTEIN_DAILY"] = 51

        return constants_for_params

    # STORED FOOD

    def set_stored_food_buffer_zero(self, constants_for_params):
        """
        Sets the stored food buffer as zero -- no stored food left at
        the end of the simulation.

        However, in reality food in transit and food in grocery stores and
        warehouses means there would still likely be some food available at
        the end as a buffer.

        """
        constants_for_params["BUFFER_RATIO"] = 0

        return constants_for_params

    def set_stored_food_buffer_as_baseline(self, constants_for_params):
        """
        Sets the stored food buffer as 100% -- the typical stored food buffer
        in ~2020 left at the end of the simulation.

        """
        constants_for_params["BUFFER_RATIO"] = 1

        return constants_for_params

    # SEASONALITY

    def set_country_seasonality_baseline(self, constants_for_params, country_data):

        # fractional production per month
        constants_for_params["SEASONALITY"] = [
            country_data["seasonality_m" + str(i)] for i in range(1, 13)
        ]

        # tons dry caloric monthly
        constants_for_params["HUMAN_INEDIBLE_FEED"] = (
            np.array(
                [country_data["grasses_baseline"]] * constants_for_params["NMONTHS"]
            )
            / 12
        )

        return constants_for_params

    def set_country_seasonality_nuclear_winter(
        self, constants_for_params, country_data
    ):

        # fractional production per month
        constants_for_params["SEASONALITY"] = [
            country_data["seasonality_m" + str(i)] for i in range(1, 13)
        ]

        constants_for_params["HUMAN_INEDIBLE_FEED"] = np.array(
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

        return constants_for_params

    def set_global_seasonality_baseline(self, constants_for_params):

        # fractional production per month
        constants_for_params["SEASONALITY"] = [
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
        constants_for_params["HUMAN_INEDIBLE_FEED"] = (
            np.array([4206] * constants_for_params["NMONTHS"]) * 1e6 / 12
        )

        return constants_for_params

    def set_global_seasonality_nuclear_winter(self, constants_for_params):

        # most food grown in tropics, so set seasonality to typical in tropics
        # fractional production per month
        constants_for_params["SEASONALITY"] = [
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
        constants_for_params["HUMAN_INEDIBLE_FEED"] = (
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

        return constants_for_params

    # INITIALIZATION

    def init_generic_scenario(self):
        constants_for_params = {}

        # the following are used for all scenarios
        constants_for_params["NMONTHS"] = 84

        # not used unless smoothing true
        # useful for ensuring output variables don't fluctuate wildly
        constants_for_params["FLUCTUATION_LIMIT"] = 1.5

        constants_for_params["DELAY"] = {}
        constants_for_params["CULL_DURATION_MONTHS"] = 60

        return constants_for_params

    def init_global_food_system_properties(self):

        constants_for_params = self.init_generic_scenario()

        # global human population (2020)
        constants_for_params["POP"] = 7.8e9

        # annual tons dry carb equivalent
        constants_for_params["BASELINE_CROP_KCALS"] = 3898e6

        # annual tons fat
        constants_for_params["BASELINE_CROP_FAT"] = 322e6

        # annual tons protein
        constants_for_params["BASELINE_CROP_PROTEIN"] = 350e6

        # annual tons dry carb equivalent
        constants_for_params["BIOFUEL_KCALS"] = 623e6

        # annual tons fat
        constants_for_params["BIOFUEL_FAT"] = 124e6

        # annual tons protein
        constants_for_params["BIOFUEL_PROTEIN"] = 32e6

        # annual tons dry carb equivalent
        constants_for_params["FEED_KCALS"] = 1385e6

        # annual tons fat
        constants_for_params["FEED_FAT"] = 60e6

        # annual tons protein
        constants_for_params["FEED_PROTEIN"] = 147e6

        # total stocks at the end of the month in dry caloric tons
        # this is total stored food available
        # if all of it were used for the whole earth, including private stocks
        # but not including a 2 month in-transit or the estimated 2 weeks to 1
        # month of stocks in people's homes, grocery stores, and food
        # warehouses
        constants_for_params["END_OF_MONTH_STOCKS"] = {}
        constants_for_params["END_OF_MONTH_STOCKS"]["JAN"] = 1960.922e6
        constants_for_params["END_OF_MONTH_STOCKS"]["FEB"] = 1784.277e6
        constants_for_params["END_OF_MONTH_STOCKS"]["MAR"] = 1624.673e6
        constants_for_params["END_OF_MONTH_STOCKS"]["APR"] = 1492.822e6
        constants_for_params["END_OF_MONTH_STOCKS"]["MAY"] = 1359.236e6
        constants_for_params["END_OF_MONTH_STOCKS"]["JUN"] = 1245.351e6
        constants_for_params["END_OF_MONTH_STOCKS"]["JUL"] = 1246.485e6
        constants_for_params["END_OF_MONTH_STOCKS"]["AUG"] = 1140.824e6
        constants_for_params["END_OF_MONTH_STOCKS"]["SEP"] = 1196.499e6
        constants_for_params["END_OF_MONTH_STOCKS"]["OCT"] = 1487.030e6
        constants_for_params["END_OF_MONTH_STOCKS"]["NOV"] = 1642.406e6
        constants_for_params["END_OF_MONTH_STOCKS"]["DEC"] = 1813.862e6

        # total head count of milk cattle
        constants_for_params["INITIAL_MILK_CATTLE"] = 264e6

        # total head count of small sized animals
        constants_for_params["INIT_SMALL_ANIMALS"] = 28.2e9

        # total head count of medium sized animals
        constants_for_params["INIT_MEDIUM_ANIMALS"] = 3.2e9

        # total head count of large sized animals minus milk cows
        constants_for_params["INIT_LARGE_ANIMALS_WITH_MILK_COWS"] = 1.9e9

        FISH_KCALS_PER_TON = 1310 * 1e3
        FISH_FAT_RATIO = 0.0048  # units: ton fat per ton wet
        FISH_PROTEIN_RATIO = 0.0204  # units: ton protein per ton wet

        # annual tons fish
        FISH_TONS_WET_2018 = 168936.71 * 1e3

        # converting from kcals to dry caloric tons:
        # 4e6 kcals = 1 dry caloric ton
        constants_for_params["FISH_DRY_CALORIC_ANNUAL"] = (
            FISH_TONS_WET_2018 * FISH_KCALS_PER_TON / 4e6
        )
        constants_for_params["FISH_FAT_TONS_ANNUAL"] = (
            FISH_TONS_WET_2018 * FISH_FAT_RATIO
        )
        constants_for_params["FISH_PROTEIN_TONS_ANNUAL"] = (
            FISH_TONS_WET_2018 * FISH_PROTEIN_RATIO
        )
        # annual tons milk production
        constants_for_params["TONS_DAIRY_ANNUAL"] = 879e6

        # annual tons chicken and pork production
        constants_for_params["TONS_CHICKEN_AND_PORK_ANNUAL"] = 250e6

        # annual tons cattle beef production
        constants_for_params["TONS_BEEF_ANNUAL"] = 74.2e6

        # Single cell protein fraction of global production
        constants_for_params["SCP_GLOBAL_PRODUCTION_FRACTION"] = 1

        # Cellulosic sugar fraction of global production
        constants_for_params["CS_GLOBAL_PRODUCTION_FRACTION"] = 1

        # 1000s of tons wet
        constants_for_params["INITIAL_SEAWEED"] = 1

        # 1000s of hectares
        constants_for_params["INITIAL_AREA"] = 1

        return constants_for_params

    def init_country_food_system_properties(self, country_data):

        constants_for_params = self.init_generic_scenario()

        # global human population (2020)
        constants_for_params["POP"] = country_data["population"]

        # annual tons dry carb equivalent
        constants_for_params["BASELINE_CROP_KCALS"] = country_data["crop_kcals"]

        # annual tons fat
        constants_for_params["BASELINE_CROP_FAT"] = country_data["crop_fat"]

        # annual tons protein
        constants_for_params["BASELINE_CROP_PROTEIN"] = country_data["crop_protein"]

        # annual tons dry carb equivalent
        constants_for_params["BIOFUEL_KCALS"] = country_data["biofuel_kcals"]

        # annual tons fat
        constants_for_params["BIOFUEL_FAT"] = country_data["biofuel_fat"]

        # annual tons protein
        constants_for_params["BIOFUEL_PROTEIN"] = country_data["biofuel_protein"]

        # annual tons dry carb equivalent
        constants_for_params["FEED_KCALS"] = country_data["feed_kcals"]

        # annual tons fat
        constants_for_params["FEED_FAT"] = country_data["feed_fat"]

        # annual tons protein
        constants_for_params["FEED_PROTEIN"] = country_data["feed_protein"]

        # total head count of milk cattle
        constants_for_params["INITIAL_MILK_CATTLE"] = country_data["dairy_cows"]

        # total head count of small sized animals
        constants_for_params["INIT_SMALL_ANIMALS"] = country_data["small_animals"]

        # total head count of medium sized animals
        constants_for_params["INIT_MEDIUM_ANIMALS"] = country_data["medium_animals"]

        # total head count of large sized animals minus milk cows
        constants_for_params["INIT_LARGE_ANIMALS_WITH_MILK_COWS"] = country_data[
            "large_animals"
        ]

        # fish kcals per month, billions
        constants_for_params["FISH_DRY_CALORIC_ANNUAL"] = country_data["aq_kcals"]

        # units of 1000s tons fat
        # (so, global value is in the tens of thousands of tons)
        constants_for_params["FISH_FAT_TONS_ANNUAL"] = country_data["aq_fat"]

        # units of 1000s tons protein monthly
        # (so, global value is in the hundreds of thousands of tons)
        constants_for_params["FISH_PROTEIN_TONS_ANNUAL"] = country_data["aq_protein"]

        # annual tons milk production
        constants_for_params["TONS_DAIRY_ANNUAL"] = country_data["dairy"]

        # annual tons chicken and pork production
        constants_for_params["TONS_CHICKEN_AND_PORK_ANNUAL"] = (
            country_data["chicken"] + country_data["pork"]
        )

        # annual tons cattle beef production
        constants_for_params["TONS_BEEF_ANNUAL"] = country_data["beef"]

        constants_for_params["END_OF_MONTH_STOCKS"] = {}
        constants_for_params["END_OF_MONTH_STOCKS"]["JAN"] = country_data[
            "stocks_kcals_jan"
        ]
        constants_for_params["END_OF_MONTH_STOCKS"]["FEB"] = country_data[
            "stocks_kcals_feb"
        ]
        constants_for_params["END_OF_MONTH_STOCKS"]["MAR"] = country_data[
            "stocks_kcals_mar"
        ]
        constants_for_params["END_OF_MONTH_STOCKS"]["APR"] = country_data[
            "stocks_kcals_apr"
        ]
        constants_for_params["END_OF_MONTH_STOCKS"]["MAY"] = country_data[
            "stocks_kcals_may"
        ]
        constants_for_params["END_OF_MONTH_STOCKS"]["JUN"] = country_data[
            "stocks_kcals_jun"
        ]
        constants_for_params["END_OF_MONTH_STOCKS"]["JUL"] = country_data[
            "stocks_kcals_jul"
        ]
        constants_for_params["END_OF_MONTH_STOCKS"]["AUG"] = country_data[
            "stocks_kcals_aug"
        ]
        constants_for_params["END_OF_MONTH_STOCKS"]["SEP"] = country_data[
            "stocks_kcals_sep"
        ]
        constants_for_params["END_OF_MONTH_STOCKS"]["OCT"] = country_data[
            "stocks_kcals_oct"
        ]
        constants_for_params["END_OF_MONTH_STOCKS"]["NOV"] = country_data[
            "stocks_kcals_nov"
        ]
        constants_for_params["END_OF_MONTH_STOCKS"]["DEC"] = country_data[
            "stocks_kcals_dec"
        ]

        # TODO: ALTER THESE TO CORRECT CLOBAL FRACTIONS

        # Single cell protein fraction of global production
        constants_for_params["SCP_GLOBAL_PRODUCTION_FRACTION"] = 1

        # Cellulosic sugar fraction of global production
        constants_for_params["CS_GLOBAL_PRODUCTION_FRACTION"] = 1

        # 1000s of tons wet
        constants_for_params["INITIAL_SEAWEED"] = 1

        # 1000s of hectares
        constants_for_params["INITIAL_AREA"] = 1

        return constants_for_params

    # FISH

    def set_fish_nuclear_winter_reduction(self, constants_for_params):
        constants_for_params["FISH_PERCENT_MONTHLY"] = list(
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

        return constants_for_params

    def set_fish_baseline(self, constants_for_params):
        # 100% of fishing remains in baseline
        constants_for_params["FISH_PERCENT_MONTHLY"] = np.array(
            [100] * constants_for_params["NMONTHS"]
        )

        return constants_for_params

    # CROP DISRUPTION

    def set_disruption_to_crops_to_zero(self, constants_for_params):
        constants_for_params["DISRUPTION_CROPS_YEAR1"] = 0
        constants_for_params["DISRUPTION_CROPS_YEAR2"] = 0
        constants_for_params["DISRUPTION_CROPS_YEAR3"] = 0
        constants_for_params["DISRUPTION_CROPS_YEAR4"] = 0
        constants_for_params["DISRUPTION_CROPS_YEAR5"] = 0
        constants_for_params["DISRUPTION_CROPS_YEAR6"] = 0
        constants_for_params["DISRUPTION_CROPS_YEAR7"] = 0
        constants_for_params["DISRUPTION_CROPS_YEAR8"] = 0
        constants_for_params["DISRUPTION_CROPS_YEAR9"] = 0
        constants_for_params["DISRUPTION_CROPS_YEAR10"] = 0
        constants_for_params["DISRUPTION_CROPS_YEAR11"] = 0

        return constants_for_params

    def set_nuclear_winter_global_disruption_to_crops(self, constants_for_params):
        constants_for_params["DISRUPTION_CROPS_YEAR1"] = 0.53
        constants_for_params["DISRUPTION_CROPS_YEAR2"] = 0.82
        constants_for_params["DISRUPTION_CROPS_YEAR3"] = 0.89
        constants_for_params["DISRUPTION_CROPS_YEAR4"] = 0.88
        constants_for_params["DISRUPTION_CROPS_YEAR5"] = 0.84
        constants_for_params["DISRUPTION_CROPS_YEAR6"] = 0.76
        constants_for_params["DISRUPTION_CROPS_YEAR7"] = 0.65
        constants_for_params["DISRUPTION_CROPS_YEAR8"] = 0.5
        constants_for_params["DISRUPTION_CROPS_YEAR9"] = 0.33
        constants_for_params["DISRUPTION_CROPS_YEAR10"] = 0.17
        constants_for_params["DISRUPTION_CROPS_YEAR11"] = 0.08

        return constants_for_params

    # SPECIFIC SCENARIOS

    def get_baseline_scenario(self, constants_for_params):

        constants_for_params["MAX_SEAWEED_AS_PERCENT_KCALS"] = 0
        constants_for_params["SEAWEED_NEW_AREA_PER_MONTH"] = 0
        constants_for_params["SEAWEED_PRODUCTION_RATE"] = 0
        constants_for_params["INDUSTRIAL_FOODS_SLOPE_MULTIPLIER"] = 0

        # these fat and protein values do not produce realistic outputs,
        # so outdoor growing ratios were used instead
        # constants_for_params['INITIAL_SF_FAT'] = 166.07e3 * 351e6/1360e6
        # constants_for_params['INITIAL_SF_PROTEIN'] = 69.25e3 * 351e6/1360e6

        constants_for_params["OG_USE_BETTER_ROTATION"] = False

        constants_for_params["INCLUDE_PROTEIN"] = True
        constants_for_params["INCLUDE_FAT"] = True

        # (no difference between harvests in the different countries!)
        constants_for_params["INITIAL_HARVEST_DURATION_IN_MONTHS"] = 7

        constants_for_params["CULL_ANIMALS"] = False
        constants_for_params["KCAL_SMOOTHING"] = False
        constants_for_params["MEAT_SMOOTHING"] = False
        constants_for_params["STORED_FOOD_SMOOTHING"] = False

        constants_for_params["ADD_CELLULOSIC_SUGAR"] = False
        constants_for_params["ADD_DAIRY"] = True
        constants_for_params["ADD_FISH"] = True
        constants_for_params["ADD_GREENHOUSES"] = False
        constants_for_params["ADD_OUTDOOR_GROWING"] = True
        constants_for_params["ADD_MEAT"] = True
        constants_for_params["ADD_METHANE_SCP"] = False
        constants_for_params["ADD_SEAWEED"] = False
        constants_for_params["ADD_STORED_FOOD"] = True

        constants_for_params["GREENHOUSE_AREA_MULTIPLIER"] = 1 / 4

        return constants_for_params

    def get_resilient_food_scenario(self, constants_for_params):

        # maximize minimum of fat or protein or kcals
        constants_for_params["INCLUDE_PROTEIN"] = True
        constants_for_params["INCLUDE_FAT"] = True

        constants_for_params["MAX_SEAWEED_AS_PERCENT_KCALS"] = 10

        # units: 1000 km^2
        constants_for_params["SEAWEED_NEW_AREA_PER_MONTH"] = 2.0765 * 30

        # percent (seaweed)
        # represents 10% daily growth
        constants_for_params["SEAWEED_PRODUCTION_RATE"] = 100 * (1.1**30 - 1)

        constants_for_params["OG_USE_BETTER_ROTATION"] = True
        constants_for_params["ROTATION_IMPROVEMENTS"] = {}
        constants_for_params["ROTATION_IMPROVEMENTS"]["KCALS_REDUCTION"] = 0.93
        constants_for_params["ROTATION_IMPROVEMENTS"]["FAT_RATIO"] = 1.487
        constants_for_params["ROTATION_IMPROVEMENTS"]["PROTEIN_RATIO"] = 1.108

        constants_for_params["GREENHOUSE_GAIN_PCT"] = 50

        # half values from greenhouse paper due to higher cost
        constants_for_params["GREENHOUSE_AREA_MULTIPLIER"] = 1 / 4
        constants_for_params[
            "INDUSTRIAL_FOODS_SLOPE_MULTIPLIER"
        ] = 1  # default values from CS and SCP papers

        constants_for_params["INITIAL_HARVEST_DURATION_IN_MONTHS"] = 7 + 1
        constants_for_params["DELAY"]["ROTATION_CHANGE_IN_MONTHS"] = 2
        constants_for_params["DELAY"]["INDUSTRIAL_FOODS_MONTHS"] = 3
        constants_for_params["DELAY"]["GREENHOUSE_MONTHS"] = 2
        constants_for_params["DELAY"]["SEAWEED_MONTHS"] = 1

        constants_for_params["CULL_ANIMALS"] = True
        constants_for_params["KCAL_SMOOTHING"] = True
        constants_for_params["MEAT_SMOOTHING"] = True
        constants_for_params["STORED_FOOD_SMOOTHING"] = True

        constants_for_params["ADD_CELLULOSIC_SUGAR"] = True
        constants_for_params["ADD_DAIRY"] = True
        constants_for_params["ADD_FISH"] = True
        constants_for_params["ADD_GREENHOUSES"] = True
        constants_for_params["ADD_OUTDOOR_GROWING"] = True
        constants_for_params["ADD_MEAT"] = True
        constants_for_params["ADD_METHANE_SCP"] = True
        constants_for_params["ADD_SEAWEED"] = True
        constants_for_params["ADD_STORED_FOOD"] = True

        ##### ERROR CHECKING, TO BE REMOVED WHEN SUFFICIENT BY-COUNTRY
        ##### RESILIENT FOOD DATA ARE AVAILABLE
        if constants_for_params["POP"] < 7e9:
            raise RuntimeError(
                "ERROR: CANNOT RUN RESILIENT FOOD SCENARIO WITH BY-COUNTRY"
            )

        return constants_for_params

    def get_no_resilient_food_scenario(self, constants_for_params):

        constants_for_params["MAX_SEAWEED_AS_PERCENT_KCALS"] = 0
        constants_for_params["SEAWEED_NEW_AREA_PER_MONTH"] = 0  # 1000 km^2 (seaweed)
        constants_for_params["SEAWEED_PRODUCTION_RATE"] = 0  # percent (seaweed)

        constants_for_params["OG_USE_BETTER_ROTATION"] = False

        constants_for_params["INCLUDE_PROTEIN"] = True
        constants_for_params["INCLUDE_FAT"] = True

        constants_for_params["GREENHOUSE_GAIN_PCT"] = 0

        constants_for_params[
            "GREENHOUSE_SLOPE_MULTIPLIER"
        ] = 1  # default values from greenhouse paper
        constants_for_params[
            "INDUSTRIAL_FOODS_SLOPE_MULTIPLIER"
        ] = 1  # default values from CS paper

        constants_for_params["INITIAL_HARVEST_DURATION_IN_MONTHS"] = 7

        constants_for_params["CULL_ANIMALS"] = True
        constants_for_params["KCAL_SMOOTHING"] = False
        constants_for_params["MEAT_SMOOTHING"] = True
        constants_for_params["STORED_FOOD_SMOOTHING"] = True

        constants_for_params["ADD_CELLULOSIC_SUGAR"] = False
        constants_for_params["ADD_DAIRY"] = False
        constants_for_params["ADD_FISH"] = True
        constants_for_params["ADD_GREENHOUSES"] = False
        constants_for_params["ADD_OUTDOOR_GROWING"] = True
        constants_for_params["ADD_MEAT"] = False
        constants_for_params["ADD_METHANE_SCP"] = False
        constants_for_params["ADD_SEAWEED"] = False
        constants_for_params["ADD_STORED_FOOD"] = True

        constants_for_params["SEASONALITY"] = [
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
        if constants_for_params["POP"] < 7e9:
            raise RuntimeError(
                "ERROR: CANNOT RUN RESILIENT FOOD SCENARIO WITH BY-COUNTRY. THIS IS BECAUSE WE HAVE NOT YET IMPORTED BY-COUNTRY CROP PRODUCTION IN A NUCLEAR WINTER"
            )
        return constants_for_params
