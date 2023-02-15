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

    def computeParameters(self, constants_inputs, scenarios_loader):
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

        # print(constants_inputs)
        print("")
        print("")
        print("")
        print("")
        # print(constants_inputs)
        constants_out = self.init_scenario(constants_out, constants_inputs)

        # NUTRITION PER MONTH #

        constants_out = self.set_nutrition_per_month(constants_out, constants_inputs)

        # SEAWEED INITIAL VARIABLES #

        constants_out, built_area = self.set_seaweed_params(
            constants_out, constants_inputs
        )
        # print("constants_out[INITIAL_SEAWEED]")
        # print(constants_out["INITIAL_SEAWEED"])
        time_consts["built_area"] = built_area

        # FISH #
        time_consts, constants_out = self.init_fish_params(
            constants_out, time_consts, constants_inputs
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

        if constants_inputs["REDUCED_BREEDING_STRATEGY"]:
            (
                meat_and_dairy,
                constants_out,
                time_consts,
            ) = self.init_meat_and_dairy_and_feed_from_breeding(
                constants_out,
                constants_inputs,
                time_consts,
                outdoor_crops,
                stored_food,
            )

        else:
            # FEED AND BIOFUEL VARIABLES #

            time_consts, feed_and_biofuels = self.init_feed_and_biofuels(
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

        # CONSTANTS FOR METHANE SINGLE CELL PROTEIN #

        time_consts, methane_scp = self.init_scp_params(time_consts, constants_inputs)

        # CONSTANTS FOR CELLULOSIC SUGAR #

        time_consts = self.init_cs_params(time_consts, constants_inputs)

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

        return (constants_out, time_consts)

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

        constants_out["INITIAL_SEAWEED"] = seaweed.INITIAL_SEAWEED
        constants_out["SEAWEED_KCALS"] = seaweed.SEAWEED_KCALS
        constants_out["HARVEST_LOSS"] = seaweed.HARVEST_LOSS
        constants_out["SEAWEED_FAT"] = seaweed.SEAWEED_FAT
        constants_out["SEAWEED_PROTEIN"] = seaweed.SEAWEED_PROTEIN

        constants_out["MINIMUM_DENSITY"] = seaweed.MINIMUM_DENSITY
        constants_out["MAXIMUM_DENSITY"] = seaweed.MAXIMUM_DENSITY
        constants_out["MAXIMUM_SEAWEED_AREA"] = seaweed.MAXIMUM_SEAWEED_AREA
        constants_out["INITIAL_BUILT_SEAWEED_AREA"] = seaweed.INITIAL_BUILT_SEAWEED_AREA

        return constants_out, built_area

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

        production_kcals_cell_sugar_per_month = (
            cellulosic_sugar.get_monthly_cs_production()
        )
        time_consts[
            "production_kcals_cell_sugar_per_month"
        ] = production_kcals_cell_sugar_per_month

        return time_consts

    def init_scp_params(self, time_consts, constants_inputs):
        """
        Initialize the parameters for single cell protein
        """

        methane_scp = MethaneSCP(constants_inputs)
        methane_scp.calculate_monthly_scp_production(constants_inputs)

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
        self, time_consts, constants_inputs, outdoor_crops, stored_food
    ):
        """
        Initialize feed and biofuels parameters.
        """

        feed_and_biofuels = FeedAndBiofuels(constants_inputs)

        # make sure nonhuman consumption is always less than or equal
        # to outdoor crops+stored food for all nutrients, pre-waste
        (
            biofuels_before_cap_prewaste,
            feed_before_cap_prewaste,
            excess_feed_prewaste,
        ) = feed_and_biofuels.get_biofuels_and_feed_before_waste_from_delayed_shutoff(
            constants_inputs
        )

        PLOT_FEED_BEFORE_WASTE = False

        if PLOT_FEED_BEFORE_WASTE:
            feed_before_cap_prewaste.in_units_percent_fed().plot(
                "feed_before_cap_prewaste using baseline"
            )

        feed_and_biofuels.set_nonhuman_consumption_with_cap(
            constants_inputs,
            outdoor_crops,
            stored_food,
            biofuels_before_cap_prewaste,
            feed_before_cap_prewaste,
            excess_feed_prewaste,
        )

        feed_and_biofuels.nonhuman_consumption = (
            feed_and_biofuels.get_nonhuman_consumption_with_cap_postwaste(
                constants_inputs, feed_and_biofuels.biofuels, feed_and_biofuels.feed
            )
        )

        nonhuman_consumption = feed_and_biofuels.nonhuman_consumption

        # post waste
        time_consts["nonhuman_consumption"] = nonhuman_consumption
        time_consts[
            "excess_feed"
        ] = feed_and_biofuels.get_excess_food_usage_from_percents(
            constants_inputs["EXCESS_FEED_PERCENT"]
        )

        return time_consts, feed_and_biofuels

    def init_meat_and_dairy_and_feed_from_breeding(
        self,
        constants_out,
        constants_inputs,
        time_consts,
        outdoor_crops,
        stored_food,
    ):
        """
        In the case of a breeding reduction strategy rather than increased slaughter,
        we first calculate the expected amount of livestock if breeding were quickly
        reduced and slaughter only increased slightly, then using that we calculate the
        feed they would use given the expected input animal populations over time.
        """
        feed_and_biofuels = FeedAndBiofuels(constants_inputs)
        coa = CalculateAnimalOutputs()
        # TODO: parametrize these constants in the scenarios so they can be adjusted
        # without messing with the code
        # really what we need is an API...
        # important_results = result[["Month","Combined Feed","Beef
        # Slaughtered","Pig Slaughtered","Poultry Slaughtered","Dairy Pop"]]
        feed_per_month_baseline = (
            feed_and_biofuels.feed_per_year_prewaste.kcals / 12 * 4e6 / 1e9
        )
        if constants_inputs["OG_USE_BETTER_ROTATION"]:
            reduction_in_dairy_calves = 0
            use_grass_and_residues_for_dairy = True
        else:
            reduction_in_dairy_calves = 100
            use_grass_and_residues_for_dairy = False

        print("constants_inputs")
        print(constants_inputs)
        quit()

        feed_dairy_meat_results = (
            coa.calculate_feed_and_animals_using_baseline_feed_usage(
                reduction_in_beef_calves=90,
                reduction_in_dairy_calves=reduction_in_dairy_calves,
                reduction_in_pig_breeding=90,
                reduction_in_poultry_breeding=90,
                increase_in_slaughter=110,
                months=constants_inputs["NMONTHS"],
                discount_rate=30,
                mother_slaughter=0,
                use_grass_and_residues_for_dairy=use_grass_and_residues_for_dairy,
                baseline_kcals_per_month_feed=feed_per_month_baseline,
            )
        )

        # MEAT AND DAIRY from breeding reduction strategy

        meat_and_dairy = MeatAndDairy(constants_inputs)
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

        # make sure nonhuman consumption is always less than or equal
        # to outdoor crops+stored food for all nutrients, pre-waste
        feed_and_biofuels.set_nonhuman_consumption_with_cap(
            constants_inputs,
            outdoor_crops,
            stored_food,
            biofuels_before_cap_prewaste,
            feed_before_cap_prewaste,
            excess_feed_prewaste,
        )
        # print("biofuels_before_cap_prewaste")
        # print(biofuels_before_cap_prewaste)
        # print("feed_before_cap_prewaste")
        # print(feed_before_cap_prewaste)
        # print("feed_and_biofuels.biofuels")
        # print(feed_and_biofuels.biofuels)
        # print("feed_and_biofuels.feed")
        # print(feed_and_biofuels.feed)
        feed_and_biofuels.nonhuman_consumption = (
            feed_and_biofuels.get_nonhuman_consumption_with_cap_postwaste(
                constants_inputs, feed_and_biofuels.biofuels, feed_and_biofuels.feed
            )
        )

        nonhuman_consumption = feed_and_biofuels.nonhuman_consumption

        # post waste
        time_consts["nonhuman_consumption"] = nonhuman_consumption
        time_consts[
            "excess_feed"
        ] = feed_and_biofuels.get_excess_food_usage_from_percents(
            constants_inputs["EXCESS_FEED_PERCENT"]
        )
        return meat_and_dairy, constants_out, time_consts

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
