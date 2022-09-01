"""
Scenarios.py: Provides numbers and methods to set the specific scenario to be optimized.
Also makes sure values are never set twice.
"""

import numpy as np
import git

repo_root = git.Repo(".", search_parent_directories=True).working_dir


class Scenarios:
    def __init__(self):
        # used to ensure the properties of scenarios are set twice or left unset
        self.NONHUMAN_CONSUMPTION_SET = False
        self.EXCESS_SET = False
        self.WASTE_SET = False
        self.NUTRITION_PROFILE_SET = False
        self.STORED_FOOD_BUFFER_SET = False
        self.SCALE_SET = False
        self.SEASONALITY_SET = False
        self.GRASSES_SET = False
        self.FISH_SET = False
        self.DISRUPTION_SET = False
        self.GENERIC_INITIALIZED_SET = False
        self.SCENARIO_SET = False
        self.PROTEIN_SET = False
        self.FAT_SET = False
        self.CULLING_PARAM_SET = False
        self.MEAT_STRATEGY_SET = False

        # convenient to understand what scenario is being run exactly
        self.scenario_description = "Scenario properties:\n"

    def check_all_set(self):
        """
        Ensure all properties of scenarios have been set
        """
        assert self.NONHUMAN_CONSUMPTION_SET
        assert self.EXCESS_SET
        assert self.WASTE_SET
        assert self.NUTRITION_PROFILE_SET
        assert self.STORED_FOOD_BUFFER_SET
        assert self.SCALE_SET
        assert self.SEASONALITY_SET
        assert self.GRASSES_SET
        assert self.GENERIC_INITIALIZED_SET
        assert self.FISH_SET
        assert self.DISRUPTION_SET
        assert self.SCENARIO_SET
        assert self.PROTEIN_SET
        assert self.FAT_SET
        assert self.CULLING_PARAM_SET
        assert self.MEAT_STRATEGY_SET

    # INITIALIZATION

    def init_generic_scenario(self):
        assert not self.GENERIC_INITIALIZED_SET
        constants_for_params = {}

        # the following are used for all scenarios
        constants_for_params["NMONTHS"] = 84

        # not used unless smoothing true
        # useful for ensuring output variables don't fluctuate wildly
        constants_for_params["DELAY"] = {}
        constants_for_params["MAX_RATIO_CULLED_SLAUGHTER_TO_BASELINE"] = 1

        constants_for_params["ADD_MILK"] = True
        constants_for_params["ADD_FISH"] = True
        constants_for_params["ADD_OUTDOOR_GROWING"] = True
        constants_for_params["ADD_STORED_FOOD"] = True
        constants_for_params["ADD_MAINTAINED_MEAT"] = True

        self.GENERIC_INITIALIZED_SET = True
        return constants_for_params

    def init_global_food_system_properties(self):
        self.scenario_description += "\ncontinued trade"
        assert not self.SCALE_SET
        self.IS_GLOBAL_ANALYSIS = True

        constants_for_params = self.init_generic_scenario()

        # global human population (2020)
        constants_for_params["POP"] = 7723713182  # (about 7.8 billion)

        # annual tons dry caloric equivalent
        constants_for_params["BASELINE_CROP_KCALS"] = 3898e6 * 1.015

        # annual tons fat
        constants_for_params["BASELINE_CROP_FAT"] = 322e6 * 1.08

        # annual tons protein
        constants_for_params["BASELINE_CROP_PROTEIN"] = 350e6 * 0.94

        # annual tons dry caloric equivalent
        constants_for_params["BIOFUEL_KCALS"] = 623e6

        # annual tons fat
        constants_for_params["BIOFUEL_FAT"] = 124e6

        # annual tons protein
        constants_for_params["BIOFUEL_PROTEIN"] = 32e6

        # annual tons dry caloric equivalent
        constants_for_params["FEED_KCALS"] = 1447.96e6

        # annual tons fat
        constants_for_params["FEED_FAT"] = 60e6

        # annual tons protein
        constants_for_params["FEED_PROTEIN"] = 147e6

        # tons dry caloric monthly
        constants_for_params["HUMAN_INEDIBLE_FEED_BASELINE_MONTHLY"] = 4206 * 1e6 / 12

        # total stocks at the end of the month in dry caloric tons
        # this is total stored food available
        # if all of it were used for the whole earth, including private stocks
        # but not including a 2 month in-transit or the estimated 2 weeks to 1
        # month of stocks in people's homes, grocery stores, and food
        # warehouses
        constants_for_params["END_OF_MONTH_STOCKS"] = {}
        constants_for_params["END_OF_MONTH_STOCKS"]["JAN"] = 1960.922e6 * 1.015
        constants_for_params["END_OF_MONTH_STOCKS"]["FEB"] = 1784.277e6 * 1.015
        constants_for_params["END_OF_MONTH_STOCKS"]["MAR"] = 1624.673e6 * 1.015
        constants_for_params["END_OF_MONTH_STOCKS"]["APR"] = 1492.822e6 * 1.015
        constants_for_params["END_OF_MONTH_STOCKS"]["MAY"] = 1359.236e6 * 1.015
        constants_for_params["END_OF_MONTH_STOCKS"]["JUN"] = 1245.351e6 * 1.015
        constants_for_params["END_OF_MONTH_STOCKS"]["JUL"] = 1246.485e6 * 1.015
        constants_for_params["END_OF_MONTH_STOCKS"]["AUG"] = 1140.824e6 * 1.015
        constants_for_params["END_OF_MONTH_STOCKS"]["SEP"] = 1196.499e6 * 1.015
        constants_for_params["END_OF_MONTH_STOCKS"]["OCT"] = 1487.030e6 * 1.015
        constants_for_params["END_OF_MONTH_STOCKS"]["NOV"] = 1642.406e6 * 1.015
        constants_for_params["END_OF_MONTH_STOCKS"]["DEC"] = 1813.862e6 * 1.015

        # total head count of milk cattle
        constants_for_params["INITIAL_MILK_CATTLE"] = 264e6

        # total head count of small sized animals
        constants_for_params["INIT_SMALL_ANIMALS"] = 28.2e9

        # total head count of medium sized animals
        constants_for_params["INIT_MEDIUM_ANIMALS"] = 3.2e9

        # total head count of large sized animals minus milk cows
        constants_for_params["INIT_LARGE_ANIMALS_WITH_MILK_COWS"] = 1.9e9

        # converting from kcals to dry caloric tons:
        # 4e6 kcals = 1 dry caloric ton
        constants_for_params["FISH_DRY_CALORIC_ANNUAL"] = 27.5e6
        constants_for_params["FISH_FAT_TONS_ANNUAL"] = 4e6
        constants_for_params["FISH_PROTEIN_TONS_ANNUAL"] = 17e6

        # annual tons milk production
        constants_for_params["TONS_MILK_ANNUAL"] = 879e6

        # annual tons chicken and pork production
        constants_for_params["TONS_CHICKEN_AND_PORK_ANNUAL"] = 250e6

        # annual tons cattle beef production
        constants_for_params["TONS_BEEF_ANNUAL"] = 74.2e6

        # Single cell protein fraction of global production
        constants_for_params["SCP_GLOBAL_PRODUCTION_FRACTION"] = 1

        # Cellulosic sugar fraction of global production
        constants_for_params["CS_GLOBAL_PRODUCTION_FRACTION"] = 1

        # seaweed params
        constants_for_params["SEAWEED_NEW_AREA_FRACTION"] = 1
        constants_for_params["SEAWEED_MAX_AREA_FRACTION"] = 1

        constants_for_params["INITIAL_SEAWEED_FRACTION"] = 1
        constants_for_params["INITIAL_BUILT_SEAWEED_FRACTION"] = 1

        # fraction global crop area for entire earth is 1 by definition
        constants_for_params["INITIAL_CROP_AREA_FRACTION"] = 1

        self.SCALE_SET = True
        return constants_for_params

    def init_country_food_system_properties(self, country_data):
        self.scenario_description += "\nno food trade"
        assert not self.SCALE_SET
        self.IS_GLOBAL_ANALYSIS = False

        constants_for_params = self.init_generic_scenario()

        # global human population (2020)
        constants_for_params["POP"] = country_data["population"]

        # This should only be enabled if we're trying to reproduce the method of Xia
        # et al. (2020), they subtract feed directly from production and ignore stored
        # food usage of crops
        # It also only makes sense to enable this if we're not including fat and protein
        SUBTRACT_FEED_DIRECTLY = False

        if SUBTRACT_FEED_DIRECTLY:

            # annual tons dry caloric equivalent
            constants_for_params["BASELINE_CROP_KCALS"] = (
                country_data["crop_kcals"] - country_data["feed_kcals"]
            )

            if constants_for_params["BASELINE_CROP_KCALS"] < 0:
                constants_for_params["BASELINE_CROP_KCALS"] = 0.01
                print("WARNING: Crop production - Feed is set to close to zero!")

        else:
            # annual tons dry caloric equivalent
            constants_for_params["BASELINE_CROP_KCALS"] = country_data["crop_kcals"]

        # annual tons fat
        constants_for_params["BASELINE_CROP_FAT"] = country_data["crop_fat"]

        # annual tons protein
        constants_for_params["BASELINE_CROP_PROTEIN"] = country_data["crop_protein"]

        # annual tons dry caloric equivalent
        constants_for_params["BIOFUEL_KCALS"] = country_data["biofuel_kcals"]

        # annual tons fat
        constants_for_params["BIOFUEL_FAT"] = country_data["biofuel_fat"]

        # annual tons protein
        constants_for_params["BIOFUEL_PROTEIN"] = country_data["biofuel_protein"]

        # annual tons dry caloric equivalent
        constants_for_params["FEED_KCALS"] = country_data["feed_kcals"]

        # annual tons fat
        constants_for_params["FEED_FAT"] = country_data["feed_fat"]

        # annual tons protein
        constants_for_params["FEED_PROTEIN"] = country_data["feed_protein"]

        # tons dry caloric monthly
        constants_for_params["HUMAN_INEDIBLE_FEED_BASELINE_MONTHLY"] = (
            country_data["grasses_baseline"] / 12
        )

        # total head count of milk cattle
        constants_for_params["INITIAL_MILK_CATTLE"] = country_data["dairy_cows"]

        # total head count of small sized animals
        constants_for_params["INIT_SMALL_ANIMALS"] = country_data["small_animals"]

        # these won't be used unless the foods are added to the scenario

        # Single cell protein fraction of global production
        constants_for_params["SCP_GLOBAL_PRODUCTION_FRACTION"] = country_data[
            "percent_of_global_capex"
        ]

        assert 1 >= country_data["initial_seaweed_fraction"] >= 0
        assert 1 >= country_data["new_area_fraction"] >= 0
        assert 1 >= country_data["max_area_fraction"] >= 0
        assert 1 >= country_data["max_area_fraction"] >= 0
        assert 1 >= country_data["initial_built_fraction"] >= 0
        assert 1 >= constants_for_params["SCP_GLOBAL_PRODUCTION_FRACTION"] >= 0

        # if country_data["percent_of_seaweed"] == 0:
        # constants_for_params["ADD_SEAWEED"] = False

        # Cellulosic sugar fraction of global production
        constants_for_params["CS_GLOBAL_PRODUCTION_FRACTION"] = country_data[
            "percent_of_global_production"
        ]
        assert 1 >= constants_for_params["CS_GLOBAL_PRODUCTION_FRACTION"] >= 0

        # 1000s of tons wet
        constants_for_params["INITIAL_SEAWEED_FRACTION"] = country_data[
            "initial_seaweed_fraction"
        ]

        constants_for_params["SEAWEED_NEW_AREA_FRACTION"] = country_data[
            "new_area_fraction"
        ]
        constants_for_params["SEAWEED_MAX_AREA_FRACTION"] = country_data[
            "max_area_fraction"
        ]

        # 1000s of hectares
        constants_for_params["INITIAL_BUILT_SEAWEED_FRACTION"] = country_data[
            "initial_built_fraction"
        ]
        constants_for_params["INITIAL_CROP_AREA_FRACTION"] = country_data[
            "fraction_crop_area_below_lat_23"
        ]

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
        constants_for_params["TONS_MILK_ANNUAL"] = country_data["dairy"]

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

        self.SCALE_SET = True
        return constants_for_params

    # FEED AND BIOFUELS

    def set_immediate_shutoff(self, constants_for_params):
        self.scenario_description += "\nno feed/biofuel"
        assert not self.NONHUMAN_CONSUMPTION_SET

        constants_for_params["DELAY"]["FEED_SHUTOFF_MONTHS"] = 0
        constants_for_params["DELAY"]["BIOFUEL_SHUTOFF_MONTHS"] = 0

        self.NONHUMAN_CONSUMPTION_SET = True
        return constants_for_params

    def set_short_delayed_shutoff(self, constants_for_params):
        self.scenario_description += "\n2month feed, 1month biofuel"
        assert not self.NONHUMAN_CONSUMPTION_SET
        constants_for_params["DELAY"]["FEED_SHUTOFF_MONTHS"] = 2
        constants_for_params["DELAY"]["BIOFUEL_SHUTOFF_MONTHS"] = 1

        self.NONHUMAN_CONSUMPTION_SET = True
        return constants_for_params

    def set_long_delayed_shutoff(self, constants_for_params):
        self.scenario_description += "\n3month feed, 2month biofuel"
        assert not self.NONHUMAN_CONSUMPTION_SET
        constants_for_params["DELAY"]["FEED_SHUTOFF_MONTHS"] = 3
        constants_for_params["DELAY"]["BIOFUEL_SHUTOFF_MONTHS"] = 2

        self.NONHUMAN_CONSUMPTION_SET = True
        return constants_for_params

    def set_continued_feed_biofuels(self, constants_for_params):
        self.scenario_description += "\ncontinued feed/biofuel"
        assert not self.NONHUMAN_CONSUMPTION_SET
        # if there is no food storage, then feed and biofuels when no food is being
        # stored would not make any sense, as the total food available could go negative
        assert (
            "STORE_FOOD_BETWEEN_YEARS" in constants_for_params.keys()
        ), """ERROR : You must assign stored food before setting biofuels"""

        if constants_for_params["STORE_FOOD_BETWEEN_YEARS"]:
            constants_for_params["DELAY"]["FEED_SHUTOFF_MONTHS"] = constants_for_params[
                "NMONTHS"
            ]
            constants_for_params["DELAY"][
                "BIOFUEL_SHUTOFF_MONTHS"
            ] = constants_for_params["NMONTHS"]
        else:
            constants_for_params["DELAY"]["FEED_SHUTOFF_MONTHS"] = 11
            constants_for_params["DELAY"]["BIOFUEL_SHUTOFF_MONTHS"] = 11

        self.NONHUMAN_CONSUMPTION_SET = True
        return constants_for_params

    # MEAT PRODUCTION STRATEGIES

    def set_unchanged_proportions_feed_grazing(self, constants_for_params):
        self.scenario_description += "\nunchanged feed to dairy"
        assert not self.MEAT_STRATEGY_SET

        constants_for_params["USE_EFFICIENT_FEED_STRATEGY"] = False

        self.MEAT_STRATEGY_SET = True
        return constants_for_params

    def set_efficient_feed_grazing_strategy(self, constants_for_params):
        self.scenario_description += "\ndairy cow feed prioritized"
        assert not self.MEAT_STRATEGY_SET

        constants_for_params["USE_EFFICIENT_FEED_STRATEGY"] = True

        self.MEAT_STRATEGY_SET = True
        return constants_for_params

    # EXCESS FEED

    def set_excess_to_zero(self, constants_for_params):
        assert not self.EXCESS_SET
        constants_for_params["EXCESS_FEED_PERCENT"] = np.zeros(
            constants_for_params["NMONTHS"]
        )

        self.EXCESS_SET = True
        return constants_for_params

    def set_excess(self, constants_for_params, excess):
        assert not self.EXCESS_SET
        constants_for_params["EXCESS_FEED_PERCENT"] = excess

        self.EXCESS_SET = True
        return constants_for_params

    # WASTE

    def set_waste_to_zero(self, constants_for_params):
        self.scenario_description += "\nno waste"
        assert not self.WASTE_SET
        constants_for_params["WASTE"] = {}
        constants_for_params["WASTE"]["SUGAR"] = 0  # %
        constants_for_params["WASTE"]["MEAT"] = 0  # %
        constants_for_params["WASTE"]["MILK"] = 0  # %
        constants_for_params["WASTE"]["SEAFOOD"] = 0  # %
        constants_for_params["WASTE"]["CROPS"] = 0  # %
        constants_for_params["WASTE"]["SEAWEED"] = 0  # %

        self.WASTE_SET = True
        return constants_for_params

    def get_total_global_waste(self, retail_waste):
        """
        Calculates the total waste of the global food system by adding retail waste
        to distribution loss.
        """
        assert self.IS_GLOBAL_ANALYSIS

        distribution_loss = {}

        distribution_loss["SUGAR"] = 0.09
        distribution_loss["CROPS"] = 4.96
        distribution_loss["MEAT"] = 0.80
        distribution_loss["MILK"] = 2.12
        distribution_loss["SEAFOOD"] = 0.17
        distribution_loss["SEAWEED"] = distribution_loss["SEAFOOD"]

        total_waste = {}

        total_waste["SUGAR"] = distribution_loss["SUGAR"] + retail_waste
        total_waste["CROPS"] = distribution_loss["CROPS"] + retail_waste
        total_waste["MEAT"] = distribution_loss["MEAT"] + retail_waste
        total_waste["MILK"] = distribution_loss["MILK"] + retail_waste
        total_waste["SEAFOOD"] = distribution_loss["SEAFOOD"] + retail_waste
        total_waste["SEAWEED"] = distribution_loss["SEAWEED"] + retail_waste

        return total_waste

    def set_global_waste_to_tripled_prices(self, constants_for_params):
        self.scenario_description += "\nwaste at 3x price"
        assert self.IS_GLOBAL_ANALYSIS
        assert not self.WASTE_SET
        """
        overall waste, on farm + distribution + retail
        3x prices (note, currently set to 2019, not 2020)
        """
        RETAIL_WASTE = 6.08

        total_waste = self.get_total_global_waste(RETAIL_WASTE)

        constants_for_params["WASTE"] = total_waste

        self.WASTE_SET = True
        return constants_for_params

    def set_global_waste_to_doubled_prices(self, constants_for_params):
        """
        overall waste, on farm + distribution + retail
        2x prices (note, currently set to 2019, not 2020)
        """
        self.scenario_description += "\nwaste at 2x price"
        assert not self.WASTE_SET
        assert self.IS_GLOBAL_ANALYSIS

        RETAIL_WASTE = 10.6

        total_waste = self.get_total_global_waste(RETAIL_WASTE)

        constants_for_params["WASTE"] = total_waste

        self.WASTE_SET = True
        return constants_for_params

    def set_global_waste_to_baseline_prices(self, constants_for_params):
        """
        overall waste, on farm+distribution+retail
        1x prices (note, currently set to 2019, not 2020)
        """
        self.scenario_description += "\nnormal waste"
        assert self.IS_GLOBAL_ANALYSIS
        assert not self.WASTE_SET
        RETAIL_WASTE = 24.98

        total_waste = self.get_total_global_waste(RETAIL_WASTE)

        constants_for_params["WASTE"] = total_waste

        self.WASTE_SET = True
        return constants_for_params

    def get_total_country_waste(self, retail_waste, country_data):
        """
        Calculates the total waste of the global food system by adding retail waste
        to distribution loss.
        """
        assert not self.IS_GLOBAL_ANALYSIS
        distribution_loss = {}

        distribution_loss["SUGAR"] = country_data["distribution_loss_sugar"] * 100
        distribution_loss["CROPS"] = country_data["distribution_loss_crops"] * 100
        distribution_loss["MEAT"] = country_data["distribution_loss_meat"] * 100
        distribution_loss["MILK"] = country_data["distribution_loss_dairy"] * 100
        distribution_loss["SEAFOOD"] = country_data["distribution_loss_seafood"] * 100
        distribution_loss["SEAWEED"] = distribution_loss["SEAFOOD"]
        total_waste = {}

        total_waste["SUGAR"] = distribution_loss["SUGAR"] + retail_waste
        total_waste["CROPS"] = distribution_loss["CROPS"] + retail_waste
        total_waste["MEAT"] = distribution_loss["MEAT"] + retail_waste
        total_waste["MILK"] = distribution_loss["MILK"] + retail_waste
        total_waste["SEAFOOD"] = distribution_loss["SEAFOOD"] + retail_waste
        total_waste["SEAWEED"] = distribution_loss["SEAWEED"] + retail_waste

        return total_waste

    def set_country_waste_to_tripled_prices(self, constants_for_params, country_data):
        """
        overall waste, on farm + distribution + retail
        3x prices (note, currently set to 2019, not 2020)
        """
        self.scenario_description += "\nwaste at 3x price"
        assert not self.WASTE_SET
        assert not self.IS_GLOBAL_ANALYSIS

        RETAIL_WASTE = country_data["retail_waste_price_triple"] * 100

        total_waste = self.get_total_country_waste(RETAIL_WASTE, country_data)

        constants_for_params["WASTE"] = total_waste

        self.WASTE_SET = True
        return constants_for_params

    def set_country_waste_to_doubled_prices(self, constants_for_params, country_data):
        """
        overall waste, on farm + distribution + retail
        2x prices (note, currently set to 2019, not 2020)
        """
        self.scenario_description += "\nwaste at 2x price"
        assert not self.WASTE_SET
        assert not self.IS_GLOBAL_ANALYSIS

        RETAIL_WASTE = country_data["retail_waste_price_double"] * 100
        total_waste = self.get_total_country_waste(RETAIL_WASTE, country_data)

        constants_for_params["WASTE"] = total_waste

        self.WASTE_SET = True
        return constants_for_params

    def set_country_waste_to_baseline_prices(self, constants_for_params, country_data):
        """
        overall waste, on farm+distribution+retail
        1x prices (note, currently set to 2019, not 2020)
        """
        self.scenario_description += "\nbaseline waste"
        assert not self.WASTE_SET
        assert not self.IS_GLOBAL_ANALYSIS

        RETAIL_WASTE = country_data["retail_waste_baseline"] * 100

        total_waste = self.get_total_country_waste(RETAIL_WASTE, country_data)

        constants_for_params["WASTE"] = total_waste

        self.WASTE_SET = True
        return constants_for_params

    # NUTRITION

    def set_baseline_nutrition_profile(self, constants_for_params):
        self.scenario_description += "\nbaseline nutrition"
        assert not self.NUTRITION_PROFILE_SET

        constants_for_params["NUTRITION"] = {}

        # kcals per person per day
        constants_for_params["NUTRITION"]["KCALS_DAILY"] = 2100

        # grams per person per day
        constants_for_params["NUTRITION"]["FAT_DAILY"] = 61.7

        # grams per person per day
        constants_for_params["NUTRITION"]["PROTEIN_DAILY"] = 59.5

        self.NUTRITION_PROFILE_SET = True
        return constants_for_params

    def set_catastrophe_nutrition_profile(self, constants_for_params):
        self.scenario_description += "\nminimum sufficient nutrition"
        assert not self.NUTRITION_PROFILE_SET

        constants_for_params["NUTRITION"] = {}

        # kcals per person per day
        constants_for_params["NUTRITION"]["KCALS_DAILY"] = 2100

        # grams per person per day
        constants_for_params["NUTRITION"]["FAT_DAILY"] = 47

        # grams per person per day
        constants_for_params["NUTRITION"]["PROTEIN_DAILY"] = 51

        self.NUTRITION_PROFILE_SET = True
        return constants_for_params

    # STORED FOOD

    def set_no_stored_food(self, constants_for_params):
        """
        Sets the stored food between years as zero. No food is traded between the
        12 month intervals seasons. Makes more sense if seasonality is assumed zero.

        However, in reality food in transit and food in grocery stores and
        warehouses means there would still likely be some food available at
        the end as a buffer.

        """
        self.scenario_description += "\nfood stored <= 12 months"
        assert not self.STORED_FOOD_BUFFER_SET
        constants_for_params["STORE_FOOD_BETWEEN_YEARS"] = False
        constants_for_params["BUFFER_RATIO"] = 0
        self.STORED_FOOD_BUFFER_SET = True
        return constants_for_params

    def set_stored_food_buffer_zero(self, constants_for_params):
        """
        Sets the stored food buffer as zero -- no stored food left at
        the end of the simulation.

        However, in reality food in transit and food in grocery stores and
        warehouses means there would still likely be some food available at
        the end as a buffer.

        """
        self.scenario_description += "\nall stocks used"
        assert not self.STORED_FOOD_BUFFER_SET
        constants_for_params["STORE_FOOD_BETWEEN_YEARS"] = True
        constants_for_params["BUFFER_RATIO"] = 0

        self.STORED_FOOD_BUFFER_SET = True
        return constants_for_params

    def set_stored_food_buffer_as_baseline(self, constants_for_params):
        """
        Sets the stored food buffer as 100% -- the typical stored food buffer
        in ~2020 left at the end of the simulation.

        """
        self.scenario_description += "\nfew stocks used"
        assert not self.STORED_FOOD_BUFFER_SET
        constants_for_params["STORE_FOOD_BETWEEN_YEARS"] = True
        constants_for_params["BUFFER_RATIO"] = 1

        self.STORED_FOOD_BUFFER_SET = True
        return constants_for_params

    # SEASONALITY

    def set_no_seasonality(self, constants_for_params):
        self.scenario_description += "\nno seasonality"
        assert not self.SEASONALITY_SET

        # most food grown in tropics, so set seasonality to typical in tropics
        # fractional production per month
        constants_for_params["SEASONALITY"] = [1 / 12] * 12

        self.SEASONALITY_SET = True
        return constants_for_params

    def set_global_seasonality_baseline(self, constants_for_params):
        assert self.IS_GLOBAL_ANALYSIS
        self.scenario_description += "\nnormal crop seasons"
        assert not self.SEASONALITY_SET

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
        self.SEASONALITY_SET = True
        return constants_for_params

    def set_global_seasonality_nuclear_winter(self, constants_for_params):
        self.scenario_description += "\nnormal crop seasons"
        assert not self.SEASONALITY_SET
        assert self.IS_GLOBAL_ANALYSIS

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

        self.SEASONALITY_SET = True
        return constants_for_params

    def set_country_seasonality(self, constants_for_params, country_data):
        assert not self.IS_GLOBAL_ANALYSIS
        assert not self.SEASONALITY_SET
        self.scenario_description += "\nnormal crop seasons"
        # fractional production per month
        constants_for_params["SEASONALITY"] = [
            country_data["seasonality_m" + str(i)] for i in range(1, 13)
        ]

        self.SEASONALITY_SET = True
        return constants_for_params

    # GRASS_PRODUCTION

    def set_grasses_baseline(self, constants_for_params):
        self.scenario_description += "\nbaseline grazing"
        assert not self.GRASSES_SET
        for i in range(1, 8):
            constants_for_params["RATIO_GRASSES_YEAR" + str(i)] = 1

        self.GRASSES_SET = True
        return constants_for_params

    def set_global_grasses_nuclear_winter(self, constants_for_params):
        self.scenario_description += "\nreduced grazing"
        assert self.IS_GLOBAL_ANALYSIS
        assert not self.GRASSES_SET

        # tons dry caloric monthly
        constants_for_params["RATIO_GRASSES_YEAR1"] = 0.65
        constants_for_params["RATIO_GRASSES_YEAR2"] = 0.23
        constants_for_params["RATIO_GRASSES_YEAR3"] = 0.14
        constants_for_params["RATIO_GRASSES_YEAR4"] = 0.13
        constants_for_params["RATIO_GRASSES_YEAR5"] = 0.13
        constants_for_params["RATIO_GRASSES_YEAR6"] = 0.19
        constants_for_params["RATIO_GRASSES_YEAR7"] = 0.24
        constants_for_params["RATIO_GRASSES_YEAR8"] = 0.33

        self.GRASSES_SET = True
        return constants_for_params

    def set_country_grasses_nuclear_winter(self, constants_for_params, country_data):
        self.scenario_description += "\nreduced grazing"
        assert not self.IS_GLOBAL_ANALYSIS
        assert not self.GRASSES_SET
        # fractional production per month

        for i in range(1, 8):

            last_year = 5

            # TODO: remove this condition when we get year 6 and 7 of the data
            if i >= last_year:
                y = last_year
            else:
                y = i

            constants_for_params["RATIO_GRASSES_YEAR" + str(i)] = (
                1 + country_data["grasses_reduction_year" + str(y)]
            )

        self.GRASSES_SET = True
        return constants_for_params

    # FISH

    def set_fish_nuclear_winter_reduction(self, constants_for_params):
        """
        Set the fish percentages in every country (or globally) from baseline
        although this is a global number, we don't have the regional number, so
        we use the global instead.
        """
        self.scenario_description += "\nreduced fish"
        assert not self.FISH_SET
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

        self.FISH_SET = True
        return constants_for_params

    def set_fish_baseline(self, constants_for_params):
        self.scenario_description += "\nbaseline fish"
        assert not self.FISH_SET
        # 100% of fishing remains in baseline
        constants_for_params["FISH_PERCENT_MONTHLY"] = np.array(
            [100] * constants_for_params["NMONTHS"]
        )

        self.FISH_SET = True
        return constants_for_params

    # CROP DISRUPTION

    def set_disruption_to_crops_to_zero(self, constants_for_params):
        self.scenario_description += "\nno crop disruption"
        assert not self.DISRUPTION_SET

        for i in range(1, 8):
            constants_for_params["RATIO_CROPS_YEAR" + str(i)] = 1

        self.DISRUPTION_SET = True
        return constants_for_params

    def set_nuclear_winter_global_disruption_to_crops(self, constants_for_params):
        assert self.IS_GLOBAL_ANALYSIS
        self.scenario_description += "\nnuclear winter crops"
        assert not self.DISRUPTION_SET

        constants_for_params["RATIO_CROPS_YEAR1"] = 1 - 0.53
        constants_for_params["RATIO_CROPS_YEAR2"] = 1 - 0.82
        constants_for_params["RATIO_CROPS_YEAR3"] = 1 - 0.89
        constants_for_params["RATIO_CROPS_YEAR4"] = 1 - 0.88
        constants_for_params["RATIO_CROPS_YEAR5"] = 1 - 0.84
        constants_for_params["RATIO_CROPS_YEAR6"] = 1 - 0.76
        constants_for_params["RATIO_CROPS_YEAR7"] = 1 - 0.65
        constants_for_params["RATIO_CROPS_YEAR8"] = 1 - 0.5
        constants_for_params["RATIO_CROPS_YEAR9"] = 1 - 0.33
        constants_for_params["RATIO_CROPS_YEAR10"] = 1 - 0.17
        constants_for_params["RATIO_CROPS_YEAR11"] = 1 - 0.08

        self.DISRUPTION_SET = True
        return constants_for_params

    def set_nuclear_winter_country_disruption_to_crops(
        self, constants_for_params, country_data
    ):
        assert not self.IS_GLOBAL_ANALYSIS
        assert not self.DISRUPTION_SET

        self.scenario_description += "\nnuclear winter crops"

        constants_for_params["RATIO_CROPS_YEAR1"] = (
            1 + country_data["crop_reduction_year1"]
        )
        constants_for_params["RATIO_CROPS_YEAR2"] = (
            1 + country_data["crop_reduction_year2"]
        )
        constants_for_params["RATIO_CROPS_YEAR3"] = (
            1 + country_data["crop_reduction_year3"]
        )
        constants_for_params["RATIO_CROPS_YEAR4"] = (
            1 + country_data["crop_reduction_year4"]
        )
        constants_for_params["RATIO_CROPS_YEAR5"] = (
            1 + country_data["crop_reduction_year5"]
        )
        constants_for_params["RATIO_CROPS_YEAR6"] = (
            1 + country_data["crop_reduction_year5"]
        )
        constants_for_params["RATIO_CROPS_YEAR7"] = (
            1 + country_data["crop_reduction_year5"]
        )
        constants_for_params["RATIO_CROPS_YEAR8"] = (
            1 + country_data["crop_reduction_year5"]
        )
        constants_for_params["RATIO_CROPS_YEAR9"] = (
            1 + country_data["crop_reduction_year5"]
        )
        constants_for_params["RATIO_CROPS_YEAR10"] = (
            1 + country_data["crop_reduction_year5"]
        )
        constants_for_params["RATIO_CROPS_YEAR11"] = (
            1 + country_data["crop_reduction_year5"]
        )

        self.DISRUPTION_SET = True
        return constants_for_params

    # PROTEIN

    def include_protein(self, constants_for_params):
        assert not self.PROTEIN_SET
        self.scenario_description += "\ninclude protein"
        constants_for_params["INCLUDE_PROTEIN"] = True
        self.PROTEIN_SET = True
        return constants_for_params

    def dont_include_protein(self, constants_for_params):
        assert not self.PROTEIN_SET
        self.scenario_description += "\ndon't include protein"
        constants_for_params["INCLUDE_PROTEIN"] = False
        self.PROTEIN_SET = True
        return constants_for_params

    # FAT

    def include_fat(self, constants_for_params):
        assert not self.FAT_SET
        self.scenario_description += "\ninclude fat"
        constants_for_params["INCLUDE_FAT"] = True
        self.FAT_SET = True

        return constants_for_params

    def dont_include_fat(self, constants_for_params):
        assert not self.FAT_SET
        self.scenario_description += "\ndon't include fat"
        constants_for_params["INCLUDE_FAT"] = False
        self.FAT_SET = True
        return constants_for_params

    # SCENARIOS

    def no_resilient_foods(self, constants_for_params):

        constants_for_params["INDUSTRIAL_FOODS_SLOPE_MULTIPLIER"] = 0
        constants_for_params["MAX_SEAWEED_AS_PERCENT_KCALS"] = 0
        constants_for_params["INITIAL_HARVEST_DURATION_IN_MONTHS"] = 8
        constants_for_params["OG_USE_BETTER_ROTATION"] = False
        constants_for_params["ADD_CELLULOSIC_SUGAR"] = False
        constants_for_params["ADD_GREENHOUSES"] = False
        constants_for_params["ADD_METHANE_SCP"] = False
        constants_for_params["ADD_SEAWEED"] = False

        return constants_for_params

    def seaweed(self, constants_for_params):
        constants_for_params["ADD_SEAWEED"] = True
        constants_for_params["DELAY"]["SEAWEED_MONTHS"] = 1
        constants_for_params["MAX_SEAWEED_AS_PERCENT_KCALS"] = 10

        # percent (seaweed)
        # represents 10% daily growth, but is calculated on monthly basis
        constants_for_params["SEAWEED_PRODUCTION_RATE"] = 100 * (1.1**30 - 1)

        return constants_for_params

    def greenhouse(self, constants_for_params):
        constants_for_params["GREENHOUSE_GAIN_PCT"] = 44

        # half values from greenhouse paper due to higher cost
        constants_for_params["DELAY"]["GREENHOUSE_MONTHS"] = 2
        constants_for_params["GREENHOUSE_AREA_MULTIPLIER"] = 1 / 4
        constants_for_params["ADD_GREENHOUSES"] = True
        return constants_for_params

    def relocated_outdoor_crops(self, constants_for_params):
        constants_for_params["OG_USE_BETTER_ROTATION"] = True

        constants_for_params["ROTATION_IMPROVEMENTS"] = {}
        # this may seem confusing. KCALS_REDUCTION is the reduction that would otherwise
        # occur averaging in year 3 globally

        constants_for_params["ROTATION_IMPROVEMENTS"]["POWER_LAW_IMPROVEMENT"] = 0.796
        constants_for_params["ROTATION_IMPROVEMENTS"]["FAT_RATIO"] = 1.647
        constants_for_params["ROTATION_IMPROVEMENTS"]["PROTEIN_RATIO"] = 1.108
        constants_for_params["INITIAL_HARVEST_DURATION_IN_MONTHS"] = 7 + 1
        constants_for_params["DELAY"]["ROTATION_CHANGE_IN_MONTHS"] = 2

        return constants_for_params

    def methane_scp(self, constants_for_params):
        constants_for_params["DELAY"]["INDUSTRIAL_FOODS_MONTHS"] = 3
        constants_for_params[
            "INDUSTRIAL_FOODS_SLOPE_MULTIPLIER"
        ] = 1  # default values from CS and SCP papers

        constants_for_params["ADD_METHANE_SCP"] = True
        return constants_for_params

    def cellulosic_sugar(self, constants_for_params):
        constants_for_params["DELAY"]["INDUSTRIAL_FOODS_MONTHS"] = 3
        constants_for_params[
            "INDUSTRIAL_FOODS_SLOPE_MULTIPLIER"
        ] = 1  # default values from CS and SCP papers

        constants_for_params["ADD_CELLULOSIC_SUGAR"] = True
        return constants_for_params

    def get_all_resilient_foods_scenario(self, constants_for_params):
        self.scenario_description += "\nall resilient foods"
        assert not self.SCENARIO_SET

        constants_for_params = self.relocated_outdoor_crops(constants_for_params)
        constants_for_params = self.methane_scp(constants_for_params)
        constants_for_params = self.cellulosic_sugar(constants_for_params)
        constants_for_params = self.greenhouse(constants_for_params)
        constants_for_params = self.seaweed(constants_for_params)

        self.SCENARIO_SET = True
        return constants_for_params

    def get_seaweed_scenario(self, constants_for_params):
        self.scenario_description += "\nscaled up seaweed"
        assert not self.SCENARIO_SET

        constants_for_params["INDUSTRIAL_FOODS_SLOPE_MULTIPLIER"] = 0

        constants_for_params["INITIAL_HARVEST_DURATION_IN_MONTHS"] = 8

        constants_for_params["OG_USE_BETTER_ROTATION"] = False
        constants_for_params["ADD_CELLULOSIC_SUGAR"] = False
        constants_for_params["ADD_GREENHOUSES"] = False
        constants_for_params["ADD_METHANE_SCP"] = False

        constants_for_params = self.seaweed(constants_for_params)

        self.SCENARIO_SET = True
        return constants_for_params

    def get_methane_scp_scenario(self, constants_for_params):
        self.scenario_description += "\nscaled up methane SCP"
        assert not self.SCENARIO_SET

        constants_for_params["MAX_SEAWEED_AS_PERCENT_KCALS"] = 0

        constants_for_params["INITIAL_HARVEST_DURATION_IN_MONTHS"] = 8

        constants_for_params["OG_USE_BETTER_ROTATION"] = False
        constants_for_params["ADD_CELLULOSIC_SUGAR"] = False
        constants_for_params["ADD_GREENHOUSES"] = False
        constants_for_params["ADD_SEAWEED"] = False

        constants_for_params = self.methane_scp(constants_for_params)

        self.SCENARIO_SET = True
        return constants_for_params

    def get_cellulosic_sugar_scenario(self, constants_for_params):
        self.scenario_description += "\nscaled up cellulosic sugar"
        assert not self.SCENARIO_SET

        constants_for_params["MAX_SEAWEED_AS_PERCENT_KCALS"] = 0

        constants_for_params["INITIAL_HARVEST_DURATION_IN_MONTHS"] = 8

        constants_for_params["OG_USE_BETTER_ROTATION"] = False
        constants_for_params["ADD_METHANE_SCP"] = False
        constants_for_params["ADD_GREENHOUSES"] = False
        constants_for_params["ADD_SEAWEED"] = False

        constants_for_params = self.cellulosic_sugar(constants_for_params)

        self.SCENARIO_SET = True
        return constants_for_params

    def get_relocated_crops_scenario(self, constants_for_params):
        self.scenario_description += "\nscaled up cold crops"
        assert not self.SCENARIO_SET

        constants_for_params["INDUSTRIAL_FOODS_SLOPE_MULTIPLIER"] = 0

        constants_for_params["MAX_SEAWEED_AS_PERCENT_KCALS"] = 0

        constants_for_params["ADD_CELLULOSIC_SUGAR"] = False
        constants_for_params["ADD_GREENHOUSES"] = False
        constants_for_params["ADD_METHANE_SCP"] = False
        constants_for_params["ADD_SEAWEED"] = False

        constants_for_params = self.relocated_outdoor_crops(constants_for_params)

        self.SCENARIO_SET = True
        return constants_for_params

    def get_greenhouse_scenario(self, constants_for_params):
        self.scenario_description += "\nscaled up greenhouses"
        assert not self.SCENARIO_SET

        constants_for_params["INDUSTRIAL_FOODS_SLOPE_MULTIPLIER"] = 0

        constants_for_params["MAX_SEAWEED_AS_PERCENT_KCALS"] = 0

        constants_for_params["INITIAL_HARVEST_DURATION_IN_MONTHS"] = 8

        constants_for_params["OG_USE_BETTER_ROTATION"] = False
        constants_for_params["ADD_CELLULOSIC_SUGAR"] = False
        constants_for_params["ADD_METHANE_SCP"] = False
        constants_for_params["ADD_SEAWEED"] = False

        constants_for_params = self.greenhouse(constants_for_params)

        self.SCENARIO_SET = True
        return constants_for_params

    def get_no_resilient_food_scenario(self, constants_for_params):
        self.scenario_description += "\nno resilient foods"
        assert not self.SCENARIO_SET

        constants_for_params = self.no_resilient_foods(constants_for_params)

        self.SCENARIO_SET = True
        return constants_for_params

    # CULLING

    def cull_animals(self, constants_for_params):
        assert not self.CULLING_PARAM_SET
        self.scenario_description += "\ncull animals"
        constants_for_params["ADD_CULLED_MEAT"] = True
        self.CULLING_PARAM_SET = True

        return constants_for_params

    def dont_cull_animals(self, constants_for_params):
        assert not self.CULLING_PARAM_SET
        self.scenario_description += "\nno culled animals"
        constants_for_params["ADD_CULLED_MEAT"] = False
        self.CULLING_PARAM_SET = True
        return constants_for_params
