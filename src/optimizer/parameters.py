############################### Parameters ####################################
##                                                                            #
##           Calculates all the parameters that feed into the optimizer       #
##                                                                            #
###############################################################################

# TODO: make a couple sub functions that deal with the different parts, where
#      it assigns the returned values to the constants.

import os
import sys
import numpy as np
from pandas.core import window
from pulp import const

module_path = os.path.abspath(os.path.join("../.."))
if module_path not in sys.path:
    sys.path.append(module_path)

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
from src.food_system.unit_conversions import UnitConversions
from src.utilities.print_parameters import PrintParameters


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

    def computeParameters(self, constants, scenarios_loader):
        if (
            constants["inputs"]["DELAY"]["FEED_SHUTOFF_MONTHS"] > 0
            or constants["inputs"]["DELAY"]["BIOFUEL_SHUTOFF_MONTHS"] > 0
        ):
            assert (
                constants["inputs"]["ADD_MAINTAINED_MEAT"] == True
            ), "Maintained meat needs to be added for continued feed usage to make sense"

        assert self.FIRST_TIME_RUN
        self.FIRST_TIME_RUN = False

        PRINT_SCENARIO_PROPERTIES = True
        if PRINT_SCENARIO_PROPERTIES:
            print(scenarios_loader.scenario_description)

        # ensure every parameter has been initialized for the scenarios_loader
        scenarios_loader.check_all_set()

        constants_for_params = constants["inputs"]

        # time dependent constants as inputs to the optimizer
        time_consts = {}
        constants = {}

        constants = self.init_scenario(constants, constants_for_params)

        #### NUTRITION PER MONTH ####

        # https://docs.google.com/spreadsheets/d / 1RZqSrHNiIEuPQLtx1ebCd_kUcFvEF6Ea46xyzA5wU0s/edit#gid=1516287804

        constants = self.set_nutrition_per_month(constants, constants_for_params)

        ####SEAWEED INITIAL VARIABLES####

        constants, built_area = self.set_seaweed_params(constants, constants_for_params)
        time_consts["built_area"] = built_area

        #### FISH ####
        time_consts, constants = self.init_fish_params(
            constants, time_consts, constants_for_params
        )

        #### CROP PRODUCTION VARIABLES ####

        constants, outdoor_crops = self.init_outdoor_crops(
            constants, constants_for_params
        )

        #### CONSTANTS FOR GREENHOUSES ####

        time_consts = self.init_greenhouse_params(
            time_consts, constants_for_params, outdoor_crops
        )

        #### STORED FOOD VARIABLES ####

        constants, stored_food = self.init_stored_food(
            constants, constants_for_params, outdoor_crops
        )

        #### FEED AND BIOFUEL VARIABLES ####

        time_consts, feed_and_biofuels = self.init_feed_and_biofuels(
            time_consts, constants_for_params, outdoor_crops, stored_food
        )

        ####LIVESTOCK, MILK INITIAL VARIABLES####

        meat_and_dairy, constants, time_consts = self.init_meat_and_dairy_params(
            constants, time_consts, constants_for_params, feed_and_biofuels
        )

        #### CONSTANTS FOR METHANE SINGLE CELL PROTEIN ####

        time_consts, methane_scp = self.init_scp_params(
            time_consts, constants_for_params
        )

        #### CONSTANTS FOR CELLULOSIC SUGAR ####

        time_consts = self.init_cs_params(time_consts, constants_for_params)

        #### OTHER VARIABLES ####

        constants["inputs"] = constants_for_params

        PRINT_FIRST_MONTH_CONSTANTS = False

        if PRINT_FIRST_MONTH_CONSTANTS:
            print_parameters = PrintParameters()
            CONSIDER_WASTE_FOR_PRINTOUT = True
            if CONSIDER_WASTE_FOR_PRINTOUT:
                print_parameters.print_constants_with_waste(
                    self.POP,
                    constants,
                    time_consts,
                    feed_and_biofuels,
                    methane_scp,
                    meat_and_dairy,
                )
            else:
                print_parameters.print_constants_no_waste(
                    self.POP,
                    constants,
                    time_consts,
                    feed_and_biofuels,
                    methane_scp,
                    meat_and_dairy,
                )

        return (constants, time_consts)

    def init_scenario(self, constants, constants_for_params):
        """
        Initialize the scenario for some constants used for the optimizer.
        """

        # population
        self.POP = constants_for_params["POP"]
        # population in units of millions of people
        self.POP_BILLIONS = constants_for_params["POP"] / 1e9
        constants = {}
        constants["POP"] = self.POP
        constants["POP_BILLIONS"] = self.POP_BILLIONS

        # full months duration of simulation

        # single valued inputs to optimizer
        constants["NMONTHS"] = constants_for_params["NMONTHS"]
        constants["ADD_FISH"] = constants_for_params["ADD_FISH"]
        constants["ADD_SEAWEED"] = constants_for_params["ADD_SEAWEED"]
        constants["ADD_MAINTAINED_MEAT"] = constants_for_params["ADD_MAINTAINED_MEAT"]
        constants["ADD_CULLED_MEAT"] = constants_for_params["ADD_CULLED_MEAT"]
        constants["ADD_MILK"] = constants_for_params["ADD_MILK"]
        constants["ADD_STORED_FOOD"] = constants_for_params["ADD_STORED_FOOD"]
        constants["ADD_METHANE_SCP"] = constants_for_params["ADD_METHANE_SCP"]
        constants["ADD_CELLULOSIC_SUGAR"] = constants_for_params["ADD_CELLULOSIC_SUGAR"]
        constants["ADD_GREENHOUSES"] = constants_for_params["ADD_GREENHOUSES"]
        constants["ADD_OUTDOOR_GROWING"] = constants_for_params["ADD_OUTDOOR_GROWING"]

        return constants

    def set_nutrition_per_month(self, constants, constants_for_params):
        """
        Set the nutrition per month for the simulation.
        """

        # we will assume a 2100 kcals diet, and scale the "upper safe" nutrition
        # from the spreadsheet down to this "standard" level.
        # we also add 20% loss, according to the sorts of loss seen in this spreadsheet
        KCALS_DAILY = constants_for_params["NUTRITION"]["KCALS_DAILY"]
        FAT_DAILY = constants_for_params["NUTRITION"]["FAT_DAILY"]
        PROTEIN_DAILY = constants_for_params["NUTRITION"]["PROTEIN_DAILY"]
        constants["KCALS_DAILY"] = KCALS_DAILY
        constants["FAT_DAILY"] = FAT_DAILY
        constants["PROTEIN_DAILY"] = PROTEIN_DAILY

        Food.conversions.set_nutrition_requirements(
            kcals_daily=KCALS_DAILY,
            fat_daily=FAT_DAILY,
            protein_daily=PROTEIN_DAILY,
            include_fat=constants_for_params["INCLUDE_FAT"],
            include_protein=constants_for_params["INCLUDE_PROTEIN"],
            population=self.POP,
        )

        constants["BILLION_KCALS_NEEDED"] = Food.conversions.billion_kcals_needed
        constants["THOU_TONS_FAT_NEEDED"] = Food.conversions.thou_tons_fat_needed
        constants[
            "THOU_TONS_PROTEIN_NEEDED"
        ] = Food.conversions.thou_tons_protein_needed

        constants["KCALS_MONTHLY"] = Food.conversions.kcals_monthly
        constants["PROTEIN_MONTHLY"] = Food.conversions.protein_monthly
        constants["FAT_MONTHLY"] = Food.conversions.fat_monthly

        CONVERSION_TO_KCALS = self.POP / 1e9 / KCALS_DAILY
        CONVERSION_TO_FAT = self.POP / 1e9 / FAT_DAILY
        CONVERSION_TO_PROTEIN = self.POP / 1e9 / PROTEIN_DAILY

        constants["CONVERSION_TO_KCALS"] = CONVERSION_TO_KCALS
        constants["CONVERSION_TO_FAT"] = CONVERSION_TO_FAT
        constants["CONVERSION_TO_PROTEIN"] = CONVERSION_TO_PROTEIN

        return constants

    def set_seaweed_params(self, constants, constants_for_params):
        """
        Set the seaweed parameters.
        """
        seaweed = Seaweed(constants_for_params)

        # determine area built to enable seaweed to grow there
        built_area = seaweed.get_built_area(constants_for_params)

        constants["INITIAL_SEAWEED"] = seaweed.INITIAL_SEAWEED
        constants["SEAWEED_KCALS"] = seaweed.SEAWEED_KCALS
        constants["HARVEST_LOSS"] = seaweed.HARVEST_LOSS
        constants["SEAWEED_FAT"] = seaweed.SEAWEED_FAT
        constants["SEAWEED_PROTEIN"] = seaweed.SEAWEED_PROTEIN

        constants["MINIMUM_DENSITY"] = seaweed.MINIMUM_DENSITY
        constants["MAXIMUM_DENSITY"] = seaweed.MAXIMUM_DENSITY
        constants["MAXIMUM_SEAWEED_AREA"] = seaweed.MAXIMUM_SEAWEED_AREA
        constants["INITIAL_BUILT_SEAWEED_AREA"] = seaweed.INITIAL_BUILT_SEAWEED_AREA

        return constants, built_area

    def init_outdoor_crops(self, constants, constants_for_params):
        """
        initialize the outdoor crops parameters
        """
        constants_for_params["STARTING_MONTH_NUM"] = self.SIMULATION_STARTING_MONTH_NUM

        outdoor_crops = OutdoorCrops(constants_for_params)
        outdoor_crops.calculate_rotation_ratios(constants_for_params)
        outdoor_crops.calculate_monthly_production(constants_for_params)

        constants["OG_FRACTION_FAT"] = outdoor_crops.OG_FRACTION_FAT
        constants["OG_FRACTION_PROTEIN"] = outdoor_crops.OG_FRACTION_PROTEIN

        constants[
            "OG_ROTATION_FRACTION_KCALS"
        ] = outdoor_crops.OG_ROTATION_FRACTION_KCALS
        constants["OG_ROTATION_FRACTION_FAT"] = outdoor_crops.OG_ROTATION_FRACTION_FAT
        constants[
            "OG_ROTATION_FRACTION_PROTEIN"
        ] = outdoor_crops.OG_ROTATION_FRACTION_PROTEIN

        return constants, outdoor_crops

    def init_stored_food(self, constants, constants_for_params, outdoor_crops):
        stored_food = StoredFood(constants_for_params, outdoor_crops)
        if constants["ADD_STORED_FOOD"]:
            stored_food.calculate_stored_food_to_use(self.SIMULATION_STARTING_MONTH_NUM)
        else:
            stored_food.set_to_zero()

        constants["SF_FRACTION_FAT"] = stored_food.SF_FRACTION_FAT
        constants["SF_FRACTION_PROTEIN"] = stored_food.SF_FRACTION_PROTEIN
        constants["stored_food"] = stored_food

        return constants, stored_food

    def init_fish_params(self, constants, time_consts, constants_for_params):
        """
        Initialize seafood parameters, not including seaweed
        """
        seafood = Seafood(constants_for_params)

        (
            production_kcals_fish_per_month,
            production_fat_fish_per_month,
            production_protein_fish_per_month,
        ) = seafood.get_seafood_production(constants_for_params)

        time_consts["production_kcals_fish_per_month"] = production_kcals_fish_per_month
        time_consts[
            "production_protein_fish_per_month"
        ] = production_protein_fish_per_month
        time_consts["production_fat_fish_per_month"] = production_fat_fish_per_month

        constants["FISH_KCALS"] = seafood.FISH_KCALS
        constants["FISH_FAT"] = seafood.FISH_FAT
        constants["FISH_PROTEIN"] = seafood.FISH_PROTEIN

        return time_consts, constants

    def init_greenhouse_params(self, time_consts, constants_for_params, outdoor_crops):
        """
        Initialize the greenhouse parameters.
        """

        greenhouses = Greenhouses(constants_for_params)

        greenhouse_area = greenhouses.get_greenhouse_area(
            constants_for_params, outdoor_crops
        )
        time_consts["greenhouse_area"] = greenhouse_area

        if constants_for_params["INITIAL_CROP_AREA_FRACTION"] == 0:
            greenhouse_kcals_per_ha = np.zeros(constants_for_params["NMONTHS"])
            greenhouse_fat_per_ha = np.zeros(constants_for_params["NMONTHS"])
            greenhouse_protein_per_ha = np.zeros(constants_for_params["NMONTHS"])
        else:

            (
                greenhouse_kcals_per_ha,
                greenhouse_fat_per_ha,
                greenhouse_protein_per_ha,
            ) = greenhouses.get_greenhouse_yield_per_ha(
                constants_for_params, outdoor_crops
            )

        # post-waste crops food produced
        outdoor_crops.set_crop_production_minus_greenhouse_area(
            constants_for_params, greenhouses.greenhouse_fraction_area
        )
        time_consts["outdoor_crops"] = outdoor_crops
        time_consts["greenhouse_kcals_per_ha"] = greenhouse_kcals_per_ha
        time_consts["greenhouse_fat_per_ha"] = greenhouse_fat_per_ha
        time_consts["greenhouse_protein_per_ha"] = greenhouse_protein_per_ha

        return time_consts

    def init_cs_params(self, time_consts, constants_for_params):
        """
        Initialize the parameters for the cellulosic sugar model
        """

        cellulosic_sugar = CellulosicSugar(constants_for_params)
        cellulosic_sugar.calculate_monthly_cs_production(constants_for_params)

        production_kcals_cell_sugar_per_month = (
            cellulosic_sugar.get_monthly_cs_production()
        )
        time_consts[
            "production_kcals_cell_sugar_per_month"
        ] = production_kcals_cell_sugar_per_month

        return time_consts

    def init_scp_params(self, time_consts, constants_for_params):
        """
        Initialize the parameters for single cell protein
        """

        methane_scp = MethaneSCP(constants_for_params)
        methane_scp.calculate_monthly_scp_production(constants_for_params)

        (
            production_kcals_scp_per_month,
            production_fat_scp_per_month,
            production_protein_scp_per_month,
        ) = methane_scp.get_scp_production()
        time_consts["production_kcals_scp_per_month"] = production_kcals_scp_per_month
        time_consts["production_fat_scp_per_month"] = production_fat_scp_per_month
        time_consts[
            "production_protein_scp_per_month"
        ] = production_protein_scp_per_month

        return time_consts, methane_scp

    def init_feed_and_biofuels(
        self, time_consts, constants_for_params, outdoor_crops, stored_food
    ):
        """
        Initialize feed and biofuels parameters.
        """

        feed_and_biofuels = FeedAndBiofuels(constants_for_params)

        # make sure nonhuman consumption is always less than or equal to outdoor crops+stored food for all nutrients, pre-waste
        feed_and_biofuels.set_nonhuman_consumption_with_cap(
            constants_for_params, outdoor_crops, stored_food
        )

        nonhuman_consumption = feed_and_biofuels.nonhuman_consumption

        # post waste
        time_consts["nonhuman_consumption"] = nonhuman_consumption
        time_consts[
            "excess_feed"
        ] = feed_and_biofuels.get_excess_food_usage_from_percents(
            constants_for_params["EXCESS_FEED_PERCENT"]
        )

        return time_consts, feed_and_biofuels

    def init_meat_and_dairy_params(
        self, constants, time_consts, constants_for_params, feed_and_biofuels
    ):
        """
        Meat and dairy are initialized here.
        NOTE: Important convention: anything pre-waste is marked so. Everything else
              that could include waste should be assumed to be post-waste if not marked

        """

        meat_and_dairy = MeatAndDairy(constants_for_params)
        meat_and_dairy.calculate_meat_nutrition()

        time_consts, meat_and_dairy = self.init_grazing_params(
            constants_for_params, time_consts, meat_and_dairy
        )

        time_consts, meat_and_dairy = self.init_grain_fed_meat_params(
            time_consts, meat_and_dairy, feed_and_biofuels, constants_for_params
        )

        (constants, time_consts, meat_and_dairy) = self.init_culled_meat_params(
            constants_for_params, constants, time_consts, meat_and_dairy
        )

        return meat_and_dairy, constants, time_consts

    def init_grazing_params(self, constants_for_params, time_consts, meat_and_dairy):

        meat_and_dairy.calculate_meat_milk_from_human_inedible_feed(
            constants_for_params
        )
        (
            grazing_milk_kcals,
            grazing_milk_fat,
            grazing_milk_protein,
        ) = meat_and_dairy.get_grazing_milk_produced_postwaste()
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
        self, time_consts, meat_and_dairy, feed_and_biofuels, constants_for_params
    ):

        # APPLY FEED+BIOFUEL WASTE here
        # this is because the total contributed by feed and biofuels is actually applied to
        # the crops and stored food before waste, which means the subtraction of waste happens
        # to the feed and biofuels before subtracting from stored food and crops.
        # any reasonable cap of production should reflect a cap on the actual amount available
        # to humans.

        # "grain" in all cases just means the stored food + outdoor crop production that is human edible and used for feed
        # this calculation is pre-waste for meat and feed
        # Chicken and pork only ever use "grain" as defined above in this model, not grasses
        meat_and_dairy.calculate_meat_and_dairy_from_grain(
            feed_and_biofuels.fed_to_animals_prewaste
        )
        # this calculation is pre-waste for the feed
        # no waste is applied for the grasses either.
        # the milk has had waste applied
        (
            grain_fed_milk_kcals,
            grain_fed_milk_fat,
            grain_fed_milk_protein,
        ) = meat_and_dairy.get_milk_from_human_edible_feed(constants_for_params)

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

        assert (feed.kcals >= grain_fed_created_kcals).all()

        return time_consts, meat_and_dairy

    def init_culled_meat_params(
        self, constants_for_params, constants, time_consts, meat_and_dairy
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
        meat_and_dairy.calculate_animals_culled(constants_for_params)
        meat_and_dairy.calculated_culled_meat()

        MAX_RATIO_CULLED_SLAUGHTER_TO_BASELINE = constants_for_params[
            "MAX_RATIO_CULLED_SLAUGHTER_TO_BASELINE"
        ]
        culled_meat = meat_and_dairy.get_culled_meat_post_waste(constants_for_params)

        time_consts["max_culled_kcals"] = meat_and_dairy.calculate_meat_limits(
            MAX_RATIO_CULLED_SLAUGHTER_TO_BASELINE, culled_meat
        )
        constants["culled_meat"] = culled_meat

        constants["CULLED_MEAT_FRACTION_FAT"] = meat_and_dairy.culled_meat_fraction_fat
        constants[
            "CULLED_MEAT_FRACTION_PROTEIN"
        ] = meat_and_dairy.culled_meat_fraction_protein

        constants["KG_PER_SMALL_ANIMAL"] = meat_and_dairy.KG_PER_SMALL_ANIMAL
        constants["KG_PER_MEDIUM_ANIMAL"] = meat_and_dairy.KG_PER_MEDIUM_ANIMAL
        constants["KG_PER_LARGE_ANIMAL"] = meat_and_dairy.KG_PER_LARGE_ANIMAL

        constants[
            "LARGE_ANIMAL_KCALS_PER_KG"
        ] = meat_and_dairy.LARGE_ANIMAL_KCALS_PER_KG
        constants["LARGE_ANIMAL_FAT_RATIO"] = meat_and_dairy.LARGE_ANIMAL_FAT_RATIO
        constants[
            "LARGE_ANIMAL_PROTEIN_RATIO"
        ] = meat_and_dairy.LARGE_ANIMAL_PROTEIN_RATIO

        constants[
            "MEDIUM_ANIMAL_KCALS_PER_KG"
        ] = meat_and_dairy.MEDIUM_ANIMAL_KCALS_PER_KG

        constants[
            "SMALL_ANIMAL_KCALS_PER_KG"
        ] = meat_and_dairy.SMALL_ANIMAL_KCALS_PER_KG
        return (constants, time_consts, meat_and_dairy)
