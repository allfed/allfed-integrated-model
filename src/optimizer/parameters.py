"""
############################### Parameters ####################################
##                                                                            #
##           Calculates all the parameters that feed into the optimizer       #
##                                                                            #
###############################################################################
"""
# TODO: make a couple sub functions that deal with the different parts, where
#      it assigns the returned values to the constants.
import numpy as np
from src.food_system.meat_and_dairy import MeatAndDairy
from src.food_system.outdoor_crops import OutdoorCrops
from src.food_system.seafood import Seafood
from src.food_system.stored_food import StoredFood
from src.food_system.cellulosic_sugar import CellulosicSugar
from src.food_system.greenhouses import Greenhouses
from src.food_system.methane_scp import MethaneSCP
from src.food_system.seaweed import Seaweed
from src.food_system.feed_and_biofuels import FeedAndBiofuels
from src.food_system.food import Food
from src.utilities.print_parameters import PrintParameters
from src.food_system.calculate_animals_and_feed_over_time import CalculateAnimalOutputs


class Parameters:
    def __init__(self):
        self.FIRST_TIME_RUN = True
        self.SIMULATION_STARTING_MONTH = "MAY"
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

    def compute_parameters(self, constants_inputs, scenarios_loader):
        if (
            constants_inputs["DELAY"]["FEED_SHUTOFF_MONTHS"] > 0
            or constants_inputs["DELAY"]["BIOFUEL_SHUTOFF_MONTHS"] > 0
        ):
            assert (
                constants_inputs["ADD_MAINTAINED_MEAT"] is True
            ), "Maintained meat needs to be added for continued feed usage"

        assert self.FIRST_TIME_RUN
        self.FIRST_TIME_RUN = False

        PRINT_SCENARIO_PROPERTIES = True
        if PRINT_SCENARIO_PROPERTIES:
            print(scenarios_loader.scenario_description)

        # ensure every parameter has been initialized for the scenarios_loader
        scenarios_loader.check_all_set()

        # time dependent constants_out as inputs to the optimizer
        time_consts = {}
        constants_out = {}

        print("")
        print("")
        print("")
        constants_out = self.init_scenario(constants_out, constants_inputs)

        # NUTRITION PER MONTH #

        constants_out = self.set_nutrition_per_month(constants_out, constants_inputs)

        # SEAWEED INITIAL VARIABLES #

        constants_out, built_area, growth_rates, seaweed = self.set_seaweed_params(
            constants_out, constants_inputs
        )

        time_consts["built_area"] = built_area
        time_consts["growth_rates_monthly"] = growth_rates

        # FISH #
        time_consts, constants_out = self.init_fish_params(
            constants_out, time_consts, constants_inputs
        )

        # CONSTANTS FOR METHANE SINGLE CELL PROTEIN #
        time_consts, methane_scp = self.init_scp_params(time_consts, constants_inputs)

        # CONSTANTS FOR CELLULOSIC SUGAR #
        time_consts, cellulosic_sugar = self.init_cs_params(
            time_consts, constants_inputs
        )

        # CROP PRODUCTION VARIABLES #

        constants_out, outdoor_crops = self.init_outdoor_crops(
            constants_out, constants_inputs
        )

        # CONSTANTS FOR GREENHOUSES #

        time_consts = self.init_greenhouse_params(
            time_consts, constants_inputs, outdoor_crops
        )

        # STORED FOOD VARIABLES #

        constants_out, stored_food = self.init_stored_food(
            constants_out, constants_inputs, outdoor_crops
        )

        USE_OLD_METHOD_OF_CALCULATING_FEED_USAGE_AND_MEAT = False

        if USE_OLD_METHOD_OF_CALCULATING_FEED_USAGE_AND_MEAT:
            (
                time_consts,
                feed_and_biofuels,
            ) = self.init_feed_and_biofuels_OUTDATED_METHOD(
                time_consts, constants_inputs, outdoor_crops, stored_food
            )

            # LIVESTOCK, MILK INITIAL VARIABLES #

            (
                meat_and_dairy,
                constants_out,
                time_consts,
            ) = self.init_meat_and_dairy_params(
                constants_inputs,
                constants_out,
                time_consts,
                feed_and_biofuels,
                outdoor_crops,
            )

        else:
            (
                feed_and_biofuels,
                meat_and_dairy,
                constants_out,
                time_consts,
            ) = self.init_meat_and_dairy_and_feed_from_breeding_and_cap_possible_feed(
                constants_out,
                constants_inputs,
                time_consts,
                outdoor_crops,
                methane_scp,
                cellulosic_sugar,
                seaweed,
                stored_food,
            )

        # else:
        # # FEED AND BIOFUEL VARIABLES #

        # OTHER VARIABLES #
        constants_out["inputs"] = constants_inputs

        PRINT_FIRST_MONTH_CONSTANTS = False

        if PRINT_FIRST_MONTH_CONSTANTS:
            print_parameters = PrintParameters()
            CONSIDER_WASTE_FOR_PRINTOUT = False
            if CONSIDER_WASTE_FOR_PRINTOUT:
                print_parameters.print_constants_with_waste(
                    self.POP,
                    constants_out,
                    time_consts,
                    feed_and_biofuels,
                    methane_scp,
                    meat_and_dairy,
                )
            else:
                print_parameters.print_constants_no_waste(
                    self.POP,
                    constants_out,
                    time_consts,
                    feed_and_biofuels,
                    methane_scp,
                    meat_and_dairy,
                )
        # self.assert_constants_not_nan(constants_out, time_consts)

        return (constants_out, time_consts)

    def assert_constants_not_nan(self, single_valued_constants, time_consts):
        """
        this is a utility function to
        make sure there's nothing fishy going on with the constants (no nan's)
        (otherwise the linear optimizer will fail in a very mysterious way)
        """

        # assert dictionary single_valued_constants values are all not nan
        for k, v in single_valued_constants.items():
            self.assert_dictionary_value_not_nan(k, v)

        for month_key, month_value in time_consts.items():
            for v in month_value:
                self.assert_dictionary_value_not_nan(month_key, v)

    def assert_dictionary_value_not_nan(self, key, value):
        """
        assert if a dictionary value is not nan.  if it is, assert, and print the key.
        """

        if key == "inputs":
            # inputs to the parameters -- not going to check these are nan here.
            # but, they might be the culprit!
            return

        # all non-integers should be Food types, and must have the following function
        if (
            isinstance(value, int)
            or isinstance(value, float)
            or isinstance(value, bool)
        ):
            assert not (value != value), "dictionary has nan at key" + key
            return

        value.make_sure_not_nan()

    def init_scenario(self, constants_out, constants_inputs):
        """
        Initialize the scenario for some constants_out used for the optimizer.
        """

        # population
        self.POP = constants_inputs["POP"]
        # population in units of millions of people
        self.POP_BILLIONS = constants_inputs["POP"] / 1e9
        constants_out = {}
        constants_out["POP"] = self.POP
        constants_out["POP_BILLIONS"] = self.POP_BILLIONS

        # full months duration of simulation

        # single valued inputs to optimizer
        constants_out["NMONTHS"] = constants_inputs["NMONTHS"]
        constants_out["ADD_FISH"] = constants_inputs["ADD_FISH"]
        constants_out["ADD_SEAWEED"] = constants_inputs["ADD_SEAWEED"]
        constants_out["ADD_MAINTAINED_MEAT"] = constants_inputs["ADD_MAINTAINED_MEAT"]
        constants_out["ADD_CULLED_MEAT"] = constants_inputs["ADD_CULLED_MEAT"]
        constants_out["ADD_MILK"] = constants_inputs["ADD_MILK"]
        constants_out["ADD_STORED_FOOD"] = constants_inputs["ADD_STORED_FOOD"]
        constants_out["ADD_METHANE_SCP"] = constants_inputs["ADD_METHANE_SCP"]
        constants_out["ADD_CELLULOSIC_SUGAR"] = constants_inputs["ADD_CELLULOSIC_SUGAR"]
        constants_out["ADD_GREENHOUSES"] = constants_inputs["ADD_GREENHOUSES"]
        constants_out["ADD_OUTDOOR_GROWING"] = constants_inputs["ADD_OUTDOOR_GROWING"]
        constants_out["STORE_FOOD_BETWEEN_YEARS"] = constants_inputs[
            "STORE_FOOD_BETWEEN_YEARS"
        ]

        return constants_out

    def set_nutrition_per_month(self, constants_out, constants_inputs):
        """
        Set the nutrition per month for the simulation.
        """

        # we will assume a 2100 kcals diet, and scale the "upper safe" nutrition
        # from the spreadsheet down to this "standard" level.
        # we also add 20% loss, according to the sorts of loss seen in this spreadsheet
        KCALS_DAILY = constants_inputs["NUTRITION"]["KCALS_DAILY"]
        FAT_DAILY = constants_inputs["NUTRITION"]["FAT_DAILY"]
        PROTEIN_DAILY = constants_inputs["NUTRITION"]["PROTEIN_DAILY"]
        constants_out["KCALS_DAILY"] = KCALS_DAILY
        constants_out["FAT_DAILY"] = FAT_DAILY
        constants_out["PROTEIN_DAILY"] = PROTEIN_DAILY

        Food.conversions.set_nutrition_requirements(
            kcals_daily=KCALS_DAILY,
            fat_daily=FAT_DAILY,
            protein_daily=PROTEIN_DAILY,
            include_fat=constants_inputs["INCLUDE_FAT"],
            include_protein=constants_inputs["INCLUDE_PROTEIN"],
            population=self.POP,
        )

        constants_out["BILLION_KCALS_NEEDED"] = Food.conversions.billion_kcals_needed
        constants_out["THOU_TONS_FAT_NEEDED"] = Food.conversions.thou_tons_fat_needed
        constants_out[
            "THOU_TONS_PROTEIN_NEEDED"
        ] = Food.conversions.thou_tons_protein_needed

        constants_out["KCALS_MONTHLY"] = Food.conversions.kcals_monthly
        constants_out["PROTEIN_MONTHLY"] = Food.conversions.protein_monthly
        constants_out["FAT_MONTHLY"] = Food.conversions.fat_monthly

        CONVERSION_TO_KCALS = self.POP / 1e9 / KCALS_DAILY
        CONVERSION_TO_FAT = self.POP / 1e9 / FAT_DAILY
        CONVERSION_TO_PROTEIN = self.POP / 1e9 / PROTEIN_DAILY

        constants_out["CONVERSION_TO_KCALS"] = CONVERSION_TO_KCALS
        constants_out["CONVERSION_TO_FAT"] = CONVERSION_TO_FAT
        constants_out["CONVERSION_TO_PROTEIN"] = CONVERSION_TO_PROTEIN

        return constants_out

    def set_seaweed_params(self, constants_out, constants_inputs):
        """
        Set the seaweed parameters.
        """
        seaweed = Seaweed(constants_inputs)

        # determine area built to enable seaweed to grow there
        built_area = seaweed.get_built_area(constants_inputs)

        # determine growth rates
        growth_rates = seaweed.get_growth_rates(constants_inputs)

        constants_out["INITIAL_SEAWEED"] = seaweed.INITIAL_SEAWEED
        constants_out["SEAWEED_KCALS"] = seaweed.SEAWEED_KCALS
        constants_out["HARVEST_LOSS"] = seaweed.HARVEST_LOSS
        constants_out["SEAWEED_FAT"] = seaweed.SEAWEED_FAT
        constants_out["SEAWEED_PROTEIN"] = seaweed.SEAWEED_PROTEIN

        constants_out["MINIMUM_DENSITY"] = seaweed.MINIMUM_DENSITY
        constants_out["MAXIMUM_DENSITY"] = seaweed.MAXIMUM_DENSITY
        constants_out["MAXIMUM_SEAWEED_AREA"] = seaweed.MAXIMUM_SEAWEED_AREA
        constants_out["INITIAL_BUILT_SEAWEED_AREA"] = seaweed.INITIAL_BUILT_SEAWEED_AREA
        constants_out[
            "MAX_SEAWEED_HUMANS_CAN_CONSUME_MONTHLY"
        ] = seaweed.MAX_SEAWEED_HUMANS_CAN_CONSUME_MONTHLY

        return constants_out, built_area, growth_rates, seaweed

    def init_outdoor_crops(self, constants_out, constants_inputs):
        """
        initialize the outdoor crops parameters
        """
        constants_inputs["STARTING_MONTH_NUM"] = self.SIMULATION_STARTING_MONTH_NUM

        outdoor_crops = OutdoorCrops(constants_inputs)
        outdoor_crops.calculate_rotation_ratios(constants_inputs)
        outdoor_crops.calculate_monthly_production(constants_inputs)

        constants_out["OG_FRACTION_FAT"] = outdoor_crops.OG_FRACTION_FAT
        constants_out["OG_FRACTION_PROTEIN"] = outdoor_crops.OG_FRACTION_PROTEIN

        constants_out[
            "OG_ROTATION_FRACTION_KCALS"
        ] = outdoor_crops.OG_ROTATION_FRACTION_KCALS
        constants_out[
            "OG_ROTATION_FRACTION_FAT"
        ] = outdoor_crops.OG_ROTATION_FRACTION_FAT
        constants_out[
            "OG_ROTATION_FRACTION_PROTEIN"
        ] = outdoor_crops.OG_ROTATION_FRACTION_PROTEIN

        return constants_out, outdoor_crops

    def init_stored_food(self, constants_out, constants_inputs, outdoor_crops):
        stored_food = StoredFood(constants_inputs, outdoor_crops)
        if constants_out["ADD_STORED_FOOD"]:
            stored_food.calculate_stored_food_to_use(self.SIMULATION_STARTING_MONTH_NUM)
        else:
            stored_food.set_to_zero()

        constants_out["SF_FRACTION_FAT"] = stored_food.SF_FRACTION_FAT
        constants_out["SF_FRACTION_PROTEIN"] = stored_food.SF_FRACTION_PROTEIN
        constants_out["stored_food"] = stored_food

        return constants_out, stored_food

    def init_fish_params(self, constants_out, time_consts, constants_inputs):
        """
        Initialize seafood parameters, not including seaweed
        """
        seafood = Seafood(constants_inputs)

        (
            production_kcals_fish_per_month,
            production_fat_fish_per_month,
            production_protein_fish_per_month,
        ) = seafood.get_seafood_production(constants_inputs)

        time_consts["production_kcals_fish_per_month"] = production_kcals_fish_per_month
        time_consts[
            "production_protein_fish_per_month"
        ] = production_protein_fish_per_month
        time_consts["production_fat_fish_per_month"] = production_fat_fish_per_month

        constants_out["FISH_KCALS"] = seafood.FISH_KCALS
        constants_out["FISH_FAT"] = seafood.FISH_FAT
        constants_out["FISH_PROTEIN"] = seafood.FISH_PROTEIN

        return time_consts, constants_out

    def init_greenhouse_params(self, time_consts, constants_inputs, outdoor_crops):
        """
        Initialize the greenhouse parameters.
        """
        greenhouses = Greenhouses(constants_inputs)

        greenhouse_area = greenhouses.get_greenhouse_area(
            constants_inputs, outdoor_crops
        )
        time_consts["greenhouse_area"] = greenhouse_area

        if constants_inputs["INITIAL_CROP_AREA_FRACTION"] == 0:
            greenhouse_kcals_per_ha = np.zeros(constants_inputs["NMONTHS"])
            greenhouse_fat_per_ha = np.zeros(constants_inputs["NMONTHS"])
            greenhouse_protein_per_ha = np.zeros(constants_inputs["NMONTHS"])
        else:
            (
                greenhouse_kcals_per_ha,
                greenhouse_fat_per_ha,
                greenhouse_protein_per_ha,
            ) = greenhouses.get_greenhouse_yield_per_ha(constants_inputs, outdoor_crops)
        # post-waste crops food produced
        outdoor_crops.set_crop_production_minus_greenhouse_area(
            constants_inputs, greenhouses.greenhouse_fraction_area
        )
        time_consts["outdoor_crops"] = outdoor_crops
        time_consts["greenhouse_kcals_per_ha"] = greenhouse_kcals_per_ha
        time_consts["greenhouse_fat_per_ha"] = greenhouse_fat_per_ha
        time_consts["greenhouse_protein_per_ha"] = greenhouse_protein_per_ha

        return time_consts

    def init_cs_params(self, time_consts, constants_inputs):
        """
        Initialize the parameters for the cellulosic sugar model
        """

        cellulosic_sugar = CellulosicSugar(constants_inputs)
        cellulosic_sugar.calculate_monthly_cs_production(constants_inputs)

        time_consts["cellulosic_sugar"] = cellulosic_sugar

        return time_consts, cellulosic_sugar

    def init_scp_params(self, time_consts, constants_inputs):
        """
        Initialize the parameters for single cell protein
        """

        methane_scp = MethaneSCP(constants_inputs)
        methane_scp.calculate_monthly_scp_caloric_production(constants_inputs)
        methane_scp.calculate_scp_fat_and_protein_production()

        time_consts["methane_scp"] = methane_scp

        return time_consts, methane_scp

    def init_meat_and_dairy_and_feed_from_breeding_and_cap_possible_feed(
        self,
        constants_out,
        constants_inputs,
        time_consts,
        outdoor_crops,
        methane_scp,
        cellulosic_sugar,
        seaweed,
        stored_food,
    ):
        """
        In the case of a breeding reduction strategy rather than increased slaughter,
        we first calculate the expected amount of livestock if breeding were quickly
        reduced and slaughter only increased slightly, then using that we calculate the
        feed they would use given the expected input animal populations over time.
        """
        feed_and_biofuels = FeedAndBiofuels(constants_inputs)
        meat_and_dairy = MeatAndDairy(constants_inputs)

        # TODO: parametrize these constants in the scenarios so they can be adjusted
        # without messing with the code

        # This function encodes the fact that the use of improved crop rotations ALSO alters the way we treat dairy cattle
        # In particular, if we are using improved crop rotations, part of this is assuming dairy cattle are fully fed by grass
        # If we aren't using improved rotations (a somewhat more pessimistic outcome), we stop breeding cattle entirely and don't use up any of the grass
        # for dairy output.
        if constants_inputs["OG_USE_BETTER_ROTATION"]:
            reduction_in_dairy_calves = 0
            use_grass_and_residues_for_dairy = True
        else:
            reduction_in_dairy_calves = 100
            use_grass_and_residues_for_dairy = False

        cao = CalculateAnimalOutputs()
        feed_ratio = 1
        (
            biofuels_before_cap_prewaste,
            feed_before_cap_prewaste,
            excess_feed_prewaste,
            feed_and_biofuels,
            meat_and_dairy,
            time_consts,
            constants_out,
        ) = self.init_meat_and_dairy_and_feed_from_breeding(
            constants_inputs,
            reduction_in_dairy_calves,
            use_grass_and_residues_for_dairy,
            cao,
            feed_and_biofuels,
            meat_and_dairy,
            feed_ratio,
            constants_out,
            time_consts,
        )

        # this only works for countries that will have enough to provide for combined feed for all the animals.
        combined_nonhuman_consumption_before_cap_or_waste = (
            biofuels_before_cap_prewaste + feed_before_cap_prewaste
        )
        # (
        #     remaining_biofuel_needed,
        #     outdoor_growing_used_for_biofuel,
        #     methane_scp_used_for_biofuel,
        #     cellulosic_sugar_used_for_biofuel,
        # ) = self.calculate_biofuel_components_without_stored_food(
        #     constants_inputs["INCLUDE_FAT"] or constants_inputs["INCLUDE_PROTEIN"],
        #     biofuels_before_cap_prewaste,
        #     seaweed,
        #     cellulosic_sugar,
        #     methane_scp,
        #     outdoor_crops,
        # )
        # (
        #     remaining_feed_needed_from_stored_food,
        #     outdoor_growing_used_for_biofuel,
        #     methane_scp_used_for_biofuel,
        #     cellulosic_sugar_used_for_biofuel,
        # ) = self.calculate_feed_components_without_stored_food(
        #     constants_inputs["INCLUDE_FAT"] or constants_inputs["INCLUDE_PROTEIN"],
        #     biofuels_before_cap_prewaste,
        #     seaweed,
        #     cellulosic_sugar,
        #     methane_scp,
        #     outdoor_crops,
        #     cellulosic_sugar_used_for_biofuel,
        #     methane_scp_used_for_biofuel,
        #     outdoor_growing_used_for_biofuel,
        # )

        # add up the available sources of feed with their appropriate percentages
        # net_feed_available_without_stored_food = (
        #     self.calculate_net_feed_available_without_stored_food(
        #         constants_inputs["INCLUDE_FAT"] or constants_inputs["INCLUDE_PROTEIN"],
        #         combined_nonhuman_consumption_before_cap_or_waste,
        #         outdoor_crops,
        #         methane_scp,
        #         cellulosic_sugar,
        #         seaweed,
        #     )
        # )

        # make sure nonhuman consumption is always less than or equal
        # to outdoor crops+stored food for all nutrients, PRE-WASTE
        # in the case that feed usage is impossibly high, and it's reduced, meat is reduced as well
        # This results in a new value assigned to "culled_meat" (note: "maintained_meat" is an artifact of the
        # old way of calculating meat production)
        ratio = feed_and_biofuels.set_nonhuman_consumption_with_cap(
            constants_inputs,
            outdoor_crops,  # net_feed_available_without_stored_food,
            stored_food,
            biofuels_before_cap_prewaste,
            feed_before_cap_prewaste,
            excess_feed_prewaste,
        )

        if ratio < 1:
            # impossibly high feed demands, we reduced feed, now we have to reduce meat ouput accordingly
            (
                biofuels_before_cap_prewaste,
                feed_before_cap_prewaste,
                excess_feed_prewaste,
                feed_and_biofuels,
                meat_and_dairy,
                time_consts,
                constants_out,
            ) = self.init_meat_and_dairy_and_feed_from_breeding(
                constants_inputs,
                reduction_in_dairy_calves,
                use_grass_and_residues_for_dairy,
                cao,
                feed_and_biofuels,
                meat_and_dairy,
                ratio,
                constants_out,
                time_consts,
            )

        feed_and_biofuels.nonhuman_consumption = (
            feed_and_biofuels.biofuels + feed_and_biofuels.feed
        )

        nonhuman_consumption = feed_and_biofuels.nonhuman_consumption

        # post waste
        time_consts["nonhuman_consumption"] = nonhuman_consumption
        time_consts[
            "excess_feed"
        ] = feed_and_biofuels.get_excess_food_usage_from_percents(
            constants_inputs["EXCESS_FEED_PERCENT"]
        )
        return feed_and_biofuels, meat_and_dairy, constants_out, time_consts

    # def calculate_net_feed_available_without_stored_food_postwaste(
    #     self,
    #     outdoor_crops,
    #     methane_scp,
    #     cellulosic_sugar,
    #     seaweed,
    # ):
    #     """
    #     For now, we will ignore seaweed as a feed source. This is because we don't
    #     have a good way to
    #     accurately estimate what the linear optimizer will predict for the amount of
    #     seaweed monthly
    #     produced
    #     """

    #     max_scp_for_feed = methane_scp.MAX_FRACTION_FEED_CONSUMED_AS_SCP * methane_scp
    #     max_cellulosic_sugar_for_feed = (
    #         cellulosic_sugar.MAX_FRACTION_FEED_CONSUMED_AS_CELLULOSIC_SUGAR
    #         * cellulosic_sugar
    #     )

    #     # TODO: include seaweed as a feed source. Right now it's complicated because
    #     # we haven't distinguished the feed vs human consumption of seaweed
    #     # seaweed.estimate_seaweed_growth_for_estimating_feed_availability()
    #     # max_seaweed_for_feed = seaweed.estimated_seaweed_feed_consumed_after_waste

    #     net_feed_available_without_stored_food_or_seaweed = (
    #         outdoor_crops
    #         + max_scp_for_feed
    #         + max_cellulosic_sugar_for_feed
    #         # + max_seaweed_for_feed
    #     )
    #     net_feed_available_without_stored_food_or_seaweed / outdoor_crops

    #     return net_feed_available_without_stored_food_or_seaweed
    def calculate_biofuel_components_without_stored_food(
        self,
        include_fat_or_protein,
        biofuels_before_cap_prewaste,
        seaweed,
        cellulosic_sugar,
        methane_scp,
        outdoor_crops,
    ):
        assert not include_fat_or_protein, """ERROR: biofuel calculations are not 
        working  yet for scenarios including fat or protein"""

        # first, preference seaweed, then cellulosic_sugar, then methane_scp

        # TODO: ADD SEAWEED
        # cell sugar

        cell_sugar_for_biofuel = (
            cellulosic_sugar.MAX_FRACTION_BIOFUEL_CONSUMED_AS_CELLULOSIC_SUGAR
            * biofuels_before_cap_prewaste.kcals
        )

        cell_sugar_for_biofuel_after_limit = min(
            cell_sugar_for_biofuel, cellulosic_sugar.kcals
        )

        cellulosic_sugar_used_for_biofuel = min(
            cell_sugar_for_biofuel_after_limit, biofuels_before_cap_prewaste.kcals
        )

        remaining_biofuel_needed = (
            biofuels_before_cap_prewaste.kcals - cellulosic_sugar_used_for_biofuel
        )

        # methanescp

        methane_scp_for_biofuel = (
            methane_scp.MAX_FRACTION_BIOFUEL_CONSUMED_AS_METHANE_SCP
            * remaining_biofuel_needed
        )

        methane_scp_for_biofuel_after_limit = min(
            methane_scp_for_biofuel, methane_scp.kcals
        )

        methane_scp_used_for_biofuel = min(
            methane_scp_for_biofuel_after_limit, remaining_biofuel_needed
        )

        remaining_biofuel_needed = (
            biofuels_before_cap_prewaste.kcals - methane_scp_used_for_biofuel
        )

        # outdoor growing

        outdoor_growing_used_for_biofuel = min(
            outdoor_growing.kcals, remaining_biofuel_needed
        )

        remaining_biofuel_needed_from_stored_food = (
            biofuels_before_cap_prewaste.kcals - outdoor_growing_used_for_biofuel
        )

        return (
            remaining_biofuel_needed_from_stored_food,
            outdoor_growing_used_for_biofuel,
            methane_scp_used_for_biofuel,
            cellulosic_sugar_used_for_biofuel,
        )

    def calculate_feed_components_without_stored_food(
        self,
        include_fat_or_protein,
        feeds_before_cap_prewaste,
        seaweed,
        cellulosic_sugar,
        methane_scp,
        outdoor_crops,
        cellulosic_sugar_used_for_biofuel,
        methane_scp_used_for_biofuel,
        outdoor_growing_used_for_biofuel,
    ):
        assert not include_fat_or_protein, """ERROR: feed calculations are not 
        working  yet for scenarios including fat or protein"""

        # first, preference seaweed, then cellulosic_sugar, then methane_scp

        # TODO: ADD SEAWEED
        # cell sugar

        cell_sugar_for_feed = (
            cellulosic_sugar.MAX_FRACTION_FEED_CONSUMED_AS_CELLULOSIC_SUGAR
            * feeds_before_cap_prewaste.kcals
        )

        cell_sugar_for_feed_after_limit = min(
            cell_sugar_for_feed, cellulosic_sugar.kcals
        )

        cellulosic_sugar_used_for_feed = min(
            cell_sugar_for_feed_after_limit, feeds_before_cap_prewaste.kcals
        )

        remaining_feed_needed = (
            feeds_before_cap_prewaste.kcals - cellulosic_sugar_used_for_feed
        )

        # methanescp

        methane_scp_for_feed = (
            methane_scp.MAX_FRACTION_BIOFUEL_CONSUMED_AS_METHANE_SCP
            * remaining_feed_needed
        )

        methane_scp_for_feed_after_limit = min(methane_scp_for_feed, methane_scp.kcals)

        methane_scp_used_for_feed = min(
            methane_scp_for_feed_after_limit, remaining_feed_needed
        )

        remaining_feed_needed = (
            feeds_before_cap_prewaste.kcals - methane_scp_used_for_feed
        )

        # outdoor growing

        outdoor_growing_used_for_feed = min(
            outdoor_growing.kcals, remaining_feed_needed
        )

        remaining_feed_needed_from_stored_food = (
            feeds_before_cap_prewaste.kcals - outdoor_growing_used_for_feed
        )

        return (
            remaining_feed_needed_from_stored_food,
            outdoor_growing_used_for_feed,
            methane_scp_used_for_feed,
            cellulosic_sugar_used_for_feed,
        )

    def calculate_net_feed_available_without_stored_food(
        self,
        include_fat_or_protein,
        combined_feed,
        outdoor_crops,
        methane_scp,
        cellulosic_sugar,
        seaweed,
    ):
        assert not include_fat_or_protein, """ERROR: feed calculations are not working 
        yet for scenarios including fat or protein"""
        """
        For now, we will ignore seaweed as a feed source. This is because we don't have a good way to
        accurately estimate what the linear optimizer will predict for the amount of seaweed monthly
        produced
        """
        cell_sugar_for_feed = (
            cellulosic_sugar.MAX_FRACTION_FEED_CONSUMED_AS_CELLULOSIC_SUGAR
            * combined_nonhuman_consumption_before_cap_or_waste
        )

        max_scp_for_feed = (
            methane_scp.MAX_FRACTION_FEED_CONSUMED_AS_SCP * combined_feed_kcals
        )
        scp_for_feed_after_limit = min(max_scp_for_feed, methane_scp.kcals)

        cell_sugar_for_feed_after_limit = min(
            cell_sugar_for_feed, cellulosic_sugar.kcals
        )

        # TODO: include seaweed as a feed source. Right now it's complicated because
        # we haven't distinguished the feed vs human consumption of seaweed
        # seaweed.estimate_seaweed_growth_for_estimating_feed_availability()
        # max_seaweed_for_feed = seaweed.estimated_seaweed_feed_consumed_after_waste

        # net_feed_available_without_stored_food_or_seaweed = (
        #     outdoor_crops.
        #     + max_scp_for_feed
        #     + max_cellulosic_sugar_for_feed
        #     # + max_seaweed_for_feed
        # )
        # net_feed_available_without_stored_food_or_seaweed / outdoor_crops
        # max_seaweed_feed = seaweed.MAX_SEAWEED_AS_PERCENT_KCALS_FEED

        # net_feed_available_without_stored_food = max_seaweed_food + net_feed_available_without_stored_food_or_seaweed

        return net_feed_available_without_stored_food_or_seaweed

    def init_meat_and_dairy_and_feed_from_breeding(
        self,
        constants_inputs,
        reduction_in_dairy_calves,
        use_grass_and_residues_for_dairy,
        cao,
        feed_and_biofuels,
        meat_and_dairy,
        feed_ratio,
        constants_out,
        time_consts,
    ):
        data = {
            "country_code": constants_inputs["COUNTRY_CODE"],
            "reduction_in_beef_calves": 90,
            "reduction_in_dairy_calves": reduction_in_dairy_calves,
            "increase_in_slaughter": 110,
            "reduction_in_pig_breeding": 90,
            "reduction_in_poultry_breeding": 90,
            "months": constants_inputs["NMONTHS"],
            "discount_rate": 30,
            "mother_slaughter": 0,
            "use_grass_and_residues_for_dairy": use_grass_and_residues_for_dairy,
            "keep_dairy": True,
            "feed_ratio": feed_ratio,
        }
        feed_dairy_meat_results = cao.calculate_feed_and_animals(data)
        # MEAT AND DAIRY from breeding reduction strategy

        meat_and_dairy.calculate_meat_nutrition()

        (
            constants_out["culled_meat"],
            constants_out["CULLED_MEAT_FRACTION_FAT"],
            constants_out["CULLED_MEAT_FRACTION_PROTEIN"],
        ) = meat_and_dairy.calculate_culled_meat(
            np.sum(feed_dairy_meat_results["Poultry Slaughtered"]),
            np.sum(feed_dairy_meat_results["Pig Slaughtered"]),
            np.sum(feed_dairy_meat_results["Beef Slaughtered"]),
        )

        time_consts["max_culled_kcals"] = meat_and_dairy.get_max_slaughter_monthly(
            feed_dairy_meat_results["Beef Slaughtered"],
            feed_dairy_meat_results["Pig Slaughtered"],
            feed_dairy_meat_results["Poultry Slaughtered"],
        )

        # https://www.nass.usda.gov/Charts_and_Maps/Milk_Production_and_Milk_Cows/cowrates.php
        monthly_milk_tons = (
            feed_dairy_meat_results["Dairy Pop"]
            * 24265
            / 2.2046
            / 365
            * 30.4
            / 1000
            / 2
        )
        # cows * pounds per cow per day * punds_to_kg /days in year * days in month /
        # kg_in_tons * ratio_milk_producing_cows
        PRINT_ANNUAL_POUNDS_MILK = False
        if PRINT_ANNUAL_POUNDS_MILK:
            print("annual pounds milk")  # ton to kg, kg to pounds, monthly to annual
            print(
                monthly_milk_tons * 1000 * 2.2046 * 12
            )  # ton to kg, kg to pounds, monthly to annual

        (
            grazing_milk_kcals,
            grazing_milk_fat,
            grazing_milk_protein,
        ) = meat_and_dairy.get_grazing_milk_produced_postwaste(monthly_milk_tons)

        time_consts["grazing_milk_kcals"] = grazing_milk_kcals
        time_consts["grazing_milk_fat"] = grazing_milk_fat
        time_consts["grazing_milk_protein"] = grazing_milk_protein

        time_consts["cattle_grazing_maintained_kcals"] = np.zeros(
            constants_inputs["NMONTHS"]
        )
        time_consts["cattle_grazing_maintained_fat"] = np.zeros(
            constants_inputs["NMONTHS"]
        )
        time_consts["cattle_grazing_maintained_protein"] = np.zeros(
            constants_inputs["NMONTHS"]
        )

        (
            constants_out["KG_PER_SMALL_ANIMAL"],
            constants_out["KG_PER_MEDIUM_ANIMAL"],
            constants_out["KG_PER_LARGE_ANIMAL"],
            constants_out["LARGE_ANIMAL_KCALS_PER_KG"],
            constants_out["LARGE_ANIMAL_FAT_RATIO"],
            constants_out["LARGE_ANIMAL_PROTEIN_RATIO"],
            constants_out["MEDIUM_ANIMAL_KCALS_PER_KG"],
            constants_out["SMALL_ANIMAL_KCALS_PER_KG"],
        ) = meat_and_dairy.get_meat_nutrition()

        time_consts["grain_fed_meat_kcals"] = np.zeros(constants_inputs["NMONTHS"])
        time_consts["grain_fed_meat_fat"] = np.zeros(constants_inputs["NMONTHS"])
        time_consts["grain_fed_meat_protein"] = np.zeros(constants_inputs["NMONTHS"])
        time_consts["grain_fed_milk_kcals"] = np.zeros(constants_inputs["NMONTHS"])
        time_consts["grain_fed_milk_fat"] = np.zeros(constants_inputs["NMONTHS"])
        time_consts["grain_fed_milk_protein"] = np.zeros(constants_inputs["NMONTHS"])

        time_consts["grain_fed_created_kcals"] = np.zeros(constants_inputs["NMONTHS"])
        time_consts["grain_fed_created_fat"] = np.zeros(constants_inputs["NMONTHS"])
        time_consts["grain_fed_created_protein"] = np.zeros(constants_inputs["NMONTHS"])

        # FEED AND BIOFUELS from breeding reduction strategy

        (
            biofuels_before_cap_prewaste,
            feed_before_cap_prewaste,
            excess_feed_prewaste,
        ) = feed_and_biofuels.get_biofuels_and_feed_before_waste_from_animal_pops(
            constants_inputs,
            feed_dairy_meat_results["Combined Feed"],
        )

        PLOT_FEED_BEFORE_WASTE = False

        if PLOT_FEED_BEFORE_WASTE:
            feed_before_cap_prewaste.in_units_percent_fed().plot(
                "feed_before_cap_prewaste"
            )

        return (
            biofuels_before_cap_prewaste,
            feed_before_cap_prewaste,
            excess_feed_prewaste,
            feed_and_biofuels,
            meat_and_dairy,
            time_consts,
            constants_out,
        )

    def init_meat_and_dairy_params(
        self,
        constants_inputs,
        constants_out,
        time_consts,
        feed_and_biofuels,
        outdoor_crops,
    ):
        """
        Meat and dairy are initialized here.
        NOTE: Important convention: anything pre-waste is marked so. Everything else
              that could include waste should be assumed to be post-waste if not marked

        """

        meat_and_dairy = MeatAndDairy(constants_inputs)
        meat_and_dairy.calculate_meat_nutrition()

        time_consts, meat_and_dairy = self.init_grazing_params(
            constants_inputs, time_consts, meat_and_dairy
        )

        time_consts, meat_and_dairy = self.init_grain_fed_meat_params(
            time_consts,
            meat_and_dairy,
            feed_and_biofuels,
            constants_inputs,
            outdoor_crops,
        )

        (
            constants_out,
            time_consts,
            meat_and_dairy,
        ) = self.init_culled_meat_params(
            constants_inputs, constants_out, time_consts, meat_and_dairy
        )

        return meat_and_dairy, constants_out, time_consts

    def init_grazing_params(self, constants_inputs, time_consts, meat_and_dairy):
        if constants_inputs["USE_EFFICIENT_FEED_STRATEGY"]:
            meat_and_dairy.calculate_meat_milk_from_human_inedible_feed(
                constants_inputs
            )
        else:
            meat_and_dairy.calculate_continued_ratios_meat_dairy_grazing(
                constants_inputs
            )

        (
            grazing_milk_kcals,
            grazing_milk_fat,
            grazing_milk_protein,
        ) = meat_and_dairy.get_grazing_milk_produced_postwaste(
            meat_and_dairy.grazing_milk_produced_prewaste
        )

        time_consts["grazing_milk_kcals"] = grazing_milk_kcals
        time_consts["grazing_milk_fat"] = grazing_milk_fat
        time_consts["grazing_milk_protein"] = grazing_milk_protein

        # Post-waste cattle ongoing meat production from grazing
        (
            cattle_grazing_maintained_kcals,
            cattle_grazing_maintained_fat,
            cattle_grazing_maintained_protein,
        ) = meat_and_dairy.get_cattle_grazing_maintained()

        time_consts["cattle_grazing_maintained_kcals"] = cattle_grazing_maintained_kcals
        time_consts["cattle_grazing_maintained_fat"] = cattle_grazing_maintained_fat
        time_consts[
            "cattle_grazing_maintained_protein"
        ] = cattle_grazing_maintained_protein

        return time_consts, meat_and_dairy

    def init_grain_fed_meat_params(
        self,
        time_consts,
        meat_and_dairy,
        feed_and_biofuels,
        constants_inputs,
        outdoor_crops,
    ):
        # APPLY FEED+BIOFUEL WASTE here
        # this is because the total contributed by feed and biofuels is actually
        # applied to
        # the crops and stored food before waste, which means the subtraction of waste
        # happens
        # to the feed and biofuels before subtracting from stored food and crops.
        # any reasonable cap of production should reflect a cap on the actual amount
        # available
        # to humans.

        # "grain" in all cases just means the stored food + outdoor crop production
        # that is human edible and used for feed
        # this calculation is pre-waste for meat and feed
        # Chicken and pork only ever use "grain" as defined above in this model, not
        # grasses

        if constants_inputs["USE_EFFICIENT_FEED_STRATEGY"]:
            meat_and_dairy.calculate_meat_and_dairy_from_grain(
                feed_and_biofuels.fed_to_animals_prewaste
            )
        else:
            meat_and_dairy.calculate_continued_ratios_meat_dairy_grain(
                feed_and_biofuels.fed_to_animals_prewaste, outdoor_crops
            )
        # this calculation is pre-waste for the feed
        # no waste is applied for the grasses either.
        # the milk has had waste applied
        (
            grain_fed_milk_kcals,
            grain_fed_milk_fat,
            grain_fed_milk_protein,
        ) = meat_and_dairy.get_milk_from_human_edible_feed(constants_inputs)

        # post waste
        (
            grain_fed_meat_kcals,
            grain_fed_meat_fat,
            grain_fed_meat_protein,
        ) = meat_and_dairy.get_meat_from_human_edible_feed()

        time_consts["grain_fed_meat_kcals"] = grain_fed_meat_kcals
        time_consts["grain_fed_meat_fat"] = grain_fed_meat_fat
        time_consts["grain_fed_meat_protein"] = grain_fed_meat_protein
        time_consts["grain_fed_milk_kcals"] = grain_fed_milk_kcals
        time_consts["grain_fed_milk_fat"] = grain_fed_milk_fat
        time_consts["grain_fed_milk_protein"] = grain_fed_milk_protein

        grain_fed_created_kcals = grain_fed_meat_kcals + grain_fed_milk_kcals
        grain_fed_created_fat = grain_fed_meat_fat + grain_fed_milk_fat
        grain_fed_created_protein = grain_fed_meat_protein + grain_fed_milk_protein
        time_consts["grain_fed_created_kcals"] = grain_fed_created_kcals
        time_consts["grain_fed_created_fat"] = grain_fed_created_fat
        time_consts["grain_fed_created_protein"] = grain_fed_created_protein

        feed = feed_and_biofuels.feed

        if (grain_fed_created_kcals <= 0).any():
            grain_fed_created_kcals = grain_fed_created_kcals.round(8)
        assert (grain_fed_created_kcals >= 0).all()

        if (grain_fed_created_fat <= 0).any():
            grain_fed_created_fat = grain_fed_created_fat.round(8)
        assert (grain_fed_created_fat >= 0).all()

        if (grain_fed_created_protein <= 0).any():
            grain_fed_created_protein = grain_fed_created_protein.round(8)
        assert (grain_fed_created_protein >= 0).all()

        # True if reproducing xia et al results when directly subtracting feed from
        # produced crops
        SUBTRACTING_FEED_DIRECTLY_FROM_PRODUCTION = False
        if not SUBTRACTING_FEED_DIRECTLY_FROM_PRODUCTION:
            assert (feed.kcals >= grain_fed_created_kcals).all()

        return time_consts, meat_and_dairy

    def init_culled_meat_params(
        self, constants_inputs, constants_out, time_consts, meat_and_dairy
    ):
        # culled meat is based on the amount that wouldn't be maintained (excluding
        # maintained cattle as well as maintained chicken and pork)
        # this calculation is pre-waste for the meat maintained of course (no waste
        # applied to livestock maintained counts from which we determined the amount
        # of meat which can be culled)
        # the actual culled meat returned is post waste
        # NOTE: in the future, the extra caloric gain in reducing livestock populations
        #       slowly and caloric loss from increasing livestock populations slowly
        #       should also be calculated
        meat_and_dairy.calculate_animals_culled(constants_inputs)
        (
            meat_and_dairy.initial_culled_meat_prewaste,
            constants_out["CULLED_MEAT_FRACTION_FAT"],
            constants_out["CULLED_MEAT_FRACTION_PROTEIN"],
        ) = meat_and_dairy.calculate_culled_meat(
            meat_and_dairy.init_small_animals_culled,
            meat_and_dairy.init_medium_animals_culled,
            meat_and_dairy.init_large_animals_culled,
        )

        MAX_RATIO_CULLED_SLAUGHTER_TO_BASELINE = constants_inputs[
            "MAX_RATIO_CULLED_SLAUGHTER_TO_BASELINE"
        ]
        culled_meat = meat_and_dairy.get_culled_meat_post_waste(constants_inputs)

        time_consts["max_culled_kcals"] = meat_and_dairy.calculate_meat_limits(
            MAX_RATIO_CULLED_SLAUGHTER_TO_BASELINE, culled_meat
        )
        constants_out["culled_meat"] = culled_meat

        (
            constants_out["KG_PER_SMALL_ANIMAL"],
            constants_out["KG_PER_MEDIUM_ANIMAL"],
            constants_out["KG_PER_LARGE_ANIMAL"],
            constants_out["LARGE_ANIMAL_KCALS_PER_KG"],
            constants_out["LARGE_ANIMAL_FAT_RATIO"],
            constants_out["LARGE_ANIMAL_PROTEIN_RATIO"],
            constants_out["MEDIUM_ANIMAL_KCALS_PER_KG"],
            constants_out["SMALL_ANIMAL_KCALS_PER_KG"],
        ) = meat_and_dairy.get_meat_nutrition()

        return (constants_out, time_consts, meat_and_dairy)
