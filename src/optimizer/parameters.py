"""
############################### Parameters ####################################
##                                                                            #
##           Calculates all the parameters that feed into the optimizer       #
##                                                                            #
###############################################################################
"""
# TODO: make a couple sub functions that deal with the different parts, where
#      it assigns the returned values to the constants.
from functools import total_ordering
import numpy as np
from pulp import constants
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
from src.food_system.calculate_animals_and_feed_over_time import CalculateAnimalOutputs


class Parameters:
    def __init__(self):
        """
        Initializes the class instance with default values for the simulation starting month and a dictionary of months
        to set the starting point of the model to the months specified in parameters.py.
        """
        self.FIRST_TIME_RUN = True  # Flag to indicate if this is the first time the simulation is being run
        self.SIMULATION_STARTING_MONTH = (
            "MAY"  # Default starting month for the simulation
        )
        # Dictionary of the months to set the starting point of the model to
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
        self.SIMULATION_STARTING_MONTH_NUM = months_dict[
            self.SIMULATION_STARTING_MONTH
        ]  # Starting month number for the simulation

    def compute_parameters(self, constants_inputs, scenarios_loader):
        """
        Computes the parameters for the model based on the inputs and scenarios provided.

        Args:
            constants_inputs (dict): A dictionary containing the constant inputs for the model.
            scenarios_loader (ScenariosLoader): An instance of the ScenariosLoader class containing the scenario inputs.

        Returns:
            tuple: A tuple containing the computed constants, time constants, and feed and biofuels.

        Raises:
            AssertionError: If maintained meat needs to be added for continued feed usage or if the function is not run for the first time.

        """
        # Check if maintained meat needs to be added for continued feed usage
        if (
            constants_inputs["DELAY"]["FEED_SHUTOFF_MONTHS"] > 0
            or constants_inputs["DELAY"]["BIOFUEL_SHUTOFF_MONTHS"] > 0
        ):
            assert (
                constants_inputs["ADD_MAINTAINED_MEAT"] is True
            ), "Maintained meat needs to be added for continued feed usage"

        # Check if function is run for the first time
        assert self.FIRST_TIME_RUN
        self.FIRST_TIME_RUN = False

        # Print scenario properties
        PRINT_SCENARIO_PROPERTIES = True
        if PRINT_SCENARIO_PROPERTIES:
            print(scenarios_loader.scenario_description)

        # Ensure every parameter has been initialized for the scenarios_loader
        scenarios_loader.check_all_set()

        # Time dependent constants_out as inputs to the optimizer
        time_consts = {}
        constants_out = {}

        # Initialize scenario constants
        constants_out = self.init_scenario(constants_out, constants_inputs)

        # Set nutrition per month
        constants_out = self.set_nutrition_per_month(constants_out, constants_inputs)

        # Set seaweed parameters
        constants_out, built_area, growth_rates, seaweed = self.set_seaweed_params(
            constants_out, constants_inputs
        )

        time_consts["built_area"] = built_area
        time_consts["growth_rates_monthly"] = growth_rates

        # Initialize fish parameters
        time_consts = self.init_fish_params(time_consts, constants_inputs)

        # Initialize methane single cell protein constants
        constants_out, time_consts, methane_scp = self.init_scp_params(
            constants_out, time_consts, constants_inputs
        )

        # Initialize cellulose sugar constants
        constants_out, time_consts, cellulosic_sugar = self.init_cs_params(
            constants_out, time_consts, constants_inputs
        )

        # Initialize outdoor crop production variables
        constants_out, outdoor_crops = self.init_outdoor_crops(
            constants_out, constants_inputs
        )

        # Initialize greenhouse constants
        time_consts = self.init_greenhouse_params(
            time_consts, constants_inputs, outdoor_crops
        )

        # Initialize stored food variables
        constants_out, stored_food = self.init_stored_food(
            constants_out, constants_inputs, outdoor_crops
        )

        # Initialize meat and dairy, feed and biofuels from breeding and subtract feed biofuels
        (
            constants_out,
            time_consts,
            feed_and_biofuels,
        ) = self.init_meat_and_dairy_and_feed_from_breeding_and_subtract_feed_biofuels(
            constants_out,
            constants_inputs,
            time_consts,
            outdoor_crops,
            methane_scp,
            cellulosic_sugar,
            seaweed,
            stored_food,
        )

        # Set inputs in constants_out
        constants_out["inputs"] = constants_inputs

        return (constants_out, time_consts, feed_and_biofuels)

    def assert_constants_not_nan(self, single_valued_constants, time_consts):
        """
        This function checks that there are no NaN values in the constants, as the linear optimizer
        will fail in a mysterious way if there are. It does this by iterating through the single_valued_constants
        and time_consts dictionaries and checking each value for NaN.

        Args:
            single_valued_constants (dict): A dictionary of single-valued constants
            time_consts (dict): A dictionary of time constants

        Returns:
            None
        """

        # assert dictionary single_valued_constants values are all not nan
        for k, v in single_valued_constants.items():
            self.assert_dictionary_value_not_nan(k, v)

        # assert dictionary time_consts values are all not nan
        for month_key, month_value in time_consts.items():
            for v in month_value:
                self.assert_dictionary_value_not_nan(month_key, v)

    def assert_dictionary_value_not_nan(self, key, value):
        """
        Asserts if a dictionary value is not NaN. If it is NaN, raises an AssertionError and prints the key.

        Args:
            key (str): The key of the dictionary value being checked.
            value (Any): The value of the dictionary being checked.

        Returns:
            None

        Raises:
            AssertionError: If the value is NaN.

        """

        if key == "inputs":
            # Inputs to the parameters -- not going to check these are NaN here.
            # But, they might be the culprit!
            return

        # All non-integers should be Food types, and must have the following function
        if (
            isinstance(value, int)
            or isinstance(value, float)
            or isinstance(value, bool)
        ):
            assert not (value != value), "Dictionary has NaN at key " + key
            return

        value.make_sure_not_nan()

    def init_scenario(self, constants_out, constants_inputs):
        """
        Initializes the scenario for some constants_out used for the optimizer.

        Args:
            constants_out (dict): A dictionary containing constants used for the optimizer.
            constants_inputs (dict): A dictionary containing input constants.

        Returns:
            dict: A dictionary containing constants used for the optimizer.

        """
        # population
        self.POP = constants_inputs["POP"]
        # population in units of millions of people
        self.POP_BILLIONS = constants_inputs["POP"] / 1e9

        # Add population constants to constants_out dictionary
        constants_out = {}
        constants_out["POP"] = self.POP
        constants_out["POP_BILLIONS"] = self.POP_BILLIONS

        # Add single valued inputs to optimizer to constants_out dictionary
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

        This function sets the nutrition per month for the simulation based on the input constants.
        It assumes a 2100 kcals diet, and scales the "upper safe" nutrition from the spreadsheet down to this "standard" level.
        It also adds 20% loss, according to the sorts of loss seen in this spreadsheet.

        Args:
            self: instance of the class
            constants_out (dict): dictionary containing the output constants
            constants_inputs (dict): dictionary containing the input constants

        Returns:
            dict: dictionary containing the updated output constants
        """

        # get the daily nutrition requirements from the input constants
        KCALS_DAILY = constants_inputs["NUTRITION"]["KCALS_DAILY"]
        FAT_DAILY = constants_inputs["NUTRITION"]["FAT_DAILY"]
        PROTEIN_DAILY = constants_inputs["NUTRITION"]["PROTEIN_DAILY"]

        # set the daily nutrition requirements in the output constants
        constants_out["KCALS_DAILY"] = KCALS_DAILY
        constants_out["FAT_DAILY"] = FAT_DAILY
        constants_out["PROTEIN_DAILY"] = PROTEIN_DAILY

        # set the nutrition requirements in the Food.conversions module
        Food.conversions.set_nutrition_requirements(
            kcals_daily=KCALS_DAILY,
            fat_daily=FAT_DAILY,
            protein_daily=PROTEIN_DAILY,
            include_fat=constants_inputs["INCLUDE_FAT"],
            include_protein=constants_inputs["INCLUDE_PROTEIN"],
            population=self.POP,
        )

        # set the nutrition constants in the output dictionary
        constants_out["BILLION_KCALS_NEEDED"] = Food.conversions.billion_kcals_needed
        constants_out["THOU_TONS_FAT_NEEDED"] = Food.conversions.thou_tons_fat_needed
        constants_out[
            "THOU_TONS_PROTEIN_NEEDED"
        ] = Food.conversions.thou_tons_protein_needed
        constants_out["KCALS_MONTHLY"] = Food.conversions.kcals_monthly
        constants_out["PROTEIN_MONTHLY"] = Food.conversions.protein_monthly
        constants_out["FAT_MONTHLY"] = Food.conversions.fat_monthly

        # calculate the conversion factors and set them in the output dictionary
        CONVERSION_TO_KCALS = self.POP / 1e9 / KCALS_DAILY
        CONVERSION_TO_FAT = self.POP / 1e9 / FAT_DAILY
        CONVERSION_TO_PROTEIN = self.POP / 1e9 / PROTEIN_DAILY
        constants_out["CONVERSION_TO_KCALS"] = CONVERSION_TO_KCALS
        constants_out["CONVERSION_TO_FAT"] = CONVERSION_TO_FAT
        constants_out["CONVERSION_TO_PROTEIN"] = CONVERSION_TO_PROTEIN

        # return the updated output constants
        return constants_out

    def set_seaweed_params(self, constants_out, constants_inputs):
        """
        This function sets the seaweed parameters by calling the Seaweed class methods and
        assigning the resulting values to the constants_out dictionary. It also calculates
        the built_area and growth_rates using the Seaweed class methods and returns them
        along with the constants_out dictionary and the Seaweed object.

        Args:
            constants_out (dict): dictionary containing the output constants
            constants_inputs (dict): dictionary containing the input constants

        Returns:
            tuple: a tuple containing the constants_out dictionary, built_area, growth_rates,
            and the Seaweed object

        """

        # create a Seaweed object using the constants_inputs dictionary
        seaweed = Seaweed(constants_inputs)

        # determine area built to enable seaweed to grow there
        built_area = seaweed.get_built_area(constants_inputs)

        # determine growth rates
        growth_rates = seaweed.get_growth_rates(constants_inputs)

        # assign the Seaweed class constants to the constants_out dictionary
        constants_out["INITIAL_SEAWEED"] = seaweed.INITIAL_SEAWEED
        constants_out["SEAWEED_KCALS"] = seaweed.SEAWEED_KCALS
        constants_out["HARVEST_LOSS"] = seaweed.HARVEST_LOSS
        constants_out["SEAWEED_FAT"] = seaweed.SEAWEED_FAT
        constants_out["SEAWEED_PROTEIN"] = seaweed.SEAWEED_PROTEIN

        # assign the Seaweed class variables to the constants_out dictionary
        constants_out["MINIMUM_DENSITY"] = seaweed.MINIMUM_DENSITY
        constants_out["MAXIMUM_DENSITY"] = seaweed.MAXIMUM_DENSITY
        constants_out["MAXIMUM_SEAWEED_AREA"] = seaweed.MAXIMUM_SEAWEED_AREA
        constants_out["INITIAL_BUILT_SEAWEED_AREA"] = seaweed.INITIAL_BUILT_SEAWEED_AREA
        constants_out[
            "MAX_SEAWEED_AS_PERCENT_KCALS_FEED"
        ] = seaweed.MAX_SEAWEED_AS_PERCENT_KCALS_FEED
        constants_out[
            "MAX_SEAWEED_AS_PERCENT_KCALS_BIOFUEL"
        ] = seaweed.MAX_SEAWEED_AS_PERCENT_KCALS_BIOFUEL
        constants_out[
            "MAX_SEAWEED_HUMANS_CAN_CONSUME_MONTHLY"
        ] = seaweed.MAX_SEAWEED_HUMANS_CAN_CONSUME_MONTHLY

        # return the constants_out dictionary, built_area, growth_rates, and the Seaweed object
        return constants_out, built_area, growth_rates, seaweed

    def init_outdoor_crops(self, constants_out, constants_inputs):
        """
        Initializes the outdoor crops parameters by calculating the rotation ratios and monthly production
        Args:
            constants_out (dict): dictionary containing the output constants
            constants_inputs (dict): dictionary containing the input constants

        Returns:
            tuple: tuple containing the updated constants_out and the outdoor_crops object
        """
        # Set the starting month number to the simulation starting month number
        constants_inputs["STARTING_MONTH_NUM"] = self.SIMULATION_STARTING_MONTH_NUM

        # Create an instance of the OutdoorCrops class with the constants_inputs dictionary
        outdoor_crops = OutdoorCrops(constants_inputs)

        # Calculate the rotation ratios for the outdoor crops
        outdoor_crops.calculate_rotation_ratios(constants_inputs)

        # Calculate the monthly production for the outdoor crops
        outdoor_crops.calculate_monthly_production(constants_inputs)

        # Update the constants_out dictionary with the outdoor crops' fraction of fat and protein
        constants_out["OG_FRACTION_FAT"] = outdoor_crops.OG_FRACTION_FAT
        constants_out["OG_FRACTION_PROTEIN"] = outdoor_crops.OG_FRACTION_PROTEIN

        # Update the constants_out dictionary with the outdoor crops' rotation fraction of kcals, fat, and protein
        constants_out[
            "OG_ROTATION_FRACTION_KCALS"
        ] = outdoor_crops.OG_ROTATION_FRACTION_KCALS
        constants_out[
            "OG_ROTATION_FRACTION_FAT"
        ] = outdoor_crops.OG_ROTATION_FRACTION_FAT
        constants_out[
            "OG_ROTATION_FRACTION_PROTEIN"
        ] = outdoor_crops.OG_ROTATION_FRACTION_PROTEIN
        constants_out["DELAY"] = constants_inputs["DELAY"]

        # Return the updated constants_out dictionary and the outdoor_crops object
        return constants_out, outdoor_crops

    def init_stored_food(self, constants_out, constants_inputs, outdoor_crops):
        """
        Initializes the stored food object and calculates the amount of stored food to use
        based on the simulation starting month number. If ADD_STORED_FOOD is False, the initial
        available stored food is set to zero.

        Args:
            self: the object instance
            constants_out (dict): dictionary containing output constants
            constants_inputs (dict): dictionary containing input constants
            outdoor_crops (list): list of outdoor crop objects

        Returns:
            tuple: a tuple containing the updated constants_out dictionary and the stored_food object
        """
        # create a new stored_food object
        stored_food = StoredFood(constants_inputs, outdoor_crops)

        # calculate the amount of stored food to use if ADD_STORED_FOOD is True
        if constants_out["ADD_STORED_FOOD"]:
            stored_food.calculate_stored_food_to_use(self.SIMULATION_STARTING_MONTH_NUM)
        # if ADD_STORED_FOOD is False, set the initial available stored food to zero
        else:
            stored_food.initial_available = Food(
                kcals=np.zeros(constants_inputs["NMONTHS"]),
                fat=np.zeros(constants_inputs["NMONTHS"]),
                protein=np.zeros(constants_inputs["NMONTHS"]),
                kcals_units="billion kcals each month",
                fat_units="thousand tons each month",
                protein_units="thousand tons each month",
            )

        # update the constants_out dictionary with the stored food fraction of fat and protein
        constants_out["SF_FRACTION_FAT"] = stored_food.SF_FRACTION_FAT
        constants_out["SF_FRACTION_PROTEIN"] = stored_food.SF_FRACTION_PROTEIN

        # add the stored_food object to the constants_out dictionary
        constants_out["stored_food"] = stored_food

        # return the updated constants_out dictionary and the stored_food object
        return constants_out, stored_food

    def init_fish_params(self, time_consts, constants_inputs):
        """
        Initializes seafood parameters, not including seaweed.

        Args:
            constants_out (dict): A dictionary containing constants for output.
            time_consts (dict): A dictionary containing monthly constants.
            constants_inputs (dict): A dictionary containing constants inputted to parameters.

        Returns:
            time_consts (dict): updated time_consts
        """

        # Create a Seafood object using the constants_inputs dictionary
        seafood = Seafood(constants_inputs)

        seafood.set_seafood_production(constants_inputs)
        time_consts["fish"] = seafood

        return time_consts

    def init_greenhouse_params(self, time_consts, constants_inputs, outdoor_crops):
        """
        Initializes the greenhouse parameters and calculates the greenhouse yield per hectare.

        Args:
            time_consts (dict): dictionary containing time constants
            constants_inputs (dict): dictionary containing constant inputs
            outdoor_crops (OutdoorCrops): instance of the OutdoorCrops class

        Returns:
            dict: dictionary containing updated time constants

        """
        # Create an instance of the Greenhouses class
        greenhouses = Greenhouses(constants_inputs)

        # Calculate the greenhouse area
        greenhouse_area = greenhouses.get_greenhouse_area(
            constants_inputs, outdoor_crops
        )
        time_consts["greenhouse_area"] = greenhouse_area

        # Calculate the greenhouse yield per hectare
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

        # Update the outdoor crops instance with the post-waste crops food produced
        outdoor_crops.set_crop_production_minus_greenhouse_area(
            constants_inputs, greenhouses.greenhouse_fraction_area
        )

        # Update the time constants dictionary with the calculated values
        time_consts["outdoor_crops"] = outdoor_crops
        time_consts["greenhouse_kcals_per_ha"] = greenhouse_kcals_per_ha
        time_consts["greenhouse_fat_per_ha"] = greenhouse_fat_per_ha
        time_consts["greenhouse_protein_per_ha"] = greenhouse_protein_per_ha

        return time_consts

    def init_cs_params(self, constants_out, time_consts, constants_inputs):
        """
        Initializes the parameters for the cellulosic sugar model.

        Args:
            time_consts (dict): A dictionary containing time constants.
            constants_inputs (dict): A dictionary containing inputs for the constants.

        Returns:
            tuple: A tuple containing the updated time constants dictionary and the
            calculated cellulosic sugar object.

        This function initializes the parameters for the cellulosic sugar model by
        creating a CellulosicSugar object and calculating the monthly cellulosic sugar
        production using the inputs provided in the constants_inputs dictionary. The
        resulting object is then added to the time_consts dictionary.

        """

        # Create a CellulosicSugar object
        cellulosic_sugar = CellulosicSugar(constants_inputs)

        # Calculate the monthly cellulosic sugar production
        cellulosic_sugar.calculate_monthly_cs_production(constants_inputs)

        constants_out[
            "MAX_CELLULOSIC_SUGAR_HUMANS_CAN_CONSUME_MONTHLY"
        ] = cellulosic_sugar.MAX_CELLULOSIC_SUGAR_HUMANS_CAN_CONSUME_MONTHLY

        constants_out[
            "MAX_CELLULOSIC_SUGAR_AS_PERCENT_KCALS_FEED"
        ] = cellulosic_sugar.MAX_CELLULOSIC_SUGAR_AS_PERCENT_KCALS_FEED
        constants_out[
            "MAX_CELLULOSIC_SUGAR_AS_PERCENT_KCALS_BIOFUEL"
        ] = cellulosic_sugar.MAX_CELLULOSIC_SUGAR_AS_PERCENT_KCALS_BIOFUEL

        # Add the cellulosic production to the time_consts dictionary
        time_consts["cellulosic_sugar"] = cellulosic_sugar.production

        # Return the updated constants_out dictionary, time_consts dictionary and the calculated cellulosic sugar object
        return constants_out, time_consts, cellulosic_sugar

    def init_scp_params(self, constants_out, time_consts, constants_inputs):
        """
        Initializes the parameters for single cell protein.

        Args:
            time_consts (dict): A dictionary containing time constants.
            constants_inputs (dict): A dictionary containing constant inputs.

        Returns:
            tuple: A tuple containing the updated time constants dictionary and the methane_scp object.

        """

        # Create an instance of the MethaneSCP class using the constant inputs.
        methane_scp = MethaneSCP(constants_inputs)

        # Calculate the monthly SCP caloric production using the constant inputs.
        methane_scp.calculate_monthly_scp_caloric_production(constants_inputs)

        # Calculate the SCP fat and protein production.
        methane_scp.calculate_scp_fat_and_protein_production()

        # Add the methane_scp object to the time_consts dictionary.
        time_consts["methane_scp"] = methane_scp

        constants_out[
            "MAX_METHANE_SCP_HUMANS_CAN_CONSUME_MONTHLY"
        ] = methane_scp.MAX_METHANE_SCP_HUMANS_CAN_CONSUME_MONTHLY
        constants_out[
            "MAX_METHANE_SCP_AS_PERCENT_KCALS_FEED"
        ] = methane_scp.MAX_METHANE_SCP_AS_PERCENT_KCALS_FEED
        constants_out[
            "MAX_METHANE_SCP_AS_PERCENT_KCALS_BIOFUEL"
        ] = methane_scp.MAX_METHANE_SCP_AS_PERCENT_KCALS_BIOFUEL

        constants_out[
            "SCP_KCALS_TO_FAT_CONVERSION"
        ] = methane_scp.SCP_KCALS_TO_FAT_CONVERSION
        constants_out[
            "SCP_KCALS_TO_PROTEIN_CONVERSION"
        ] = methane_scp.SCP_KCALS_TO_PROTEIN_CONVERSION

        return constants_out, time_consts, methane_scp

    def init_meat_and_dairy_and_feed_from_breeding_and_subtract_feed_biofuels(
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
        Calculates the expected amount of livestock if breeding were quickly reduced and slaughter only increased slightly,
        then using that we calculate the feed they would use given the expected input animal populations over time.
        Args:
            self: instance of the class
            constants_out (dict): dictionary containing output constants
            constants_inputs (dict): dictionary containing input constants
            time_consts (dict): dictionary containing time constants
            outdoor_crops (dict): dictionary containing outdoor crop constants
            methane_scp (dict): dictionary containing methane SCP constants
            cellulosic_sugar (dict): dictionary containing cellulosic sugar constants
            seaweed (dict): dictionary containing seaweed constants
            stored_food (dict): dictionary containing stored food constants
        Returns:
            tuple: tuple containing constants_out, time_consts, and feed_and_biofuels
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

        # if we have an immediate shutoff, then turn off the feed to animals entirely
        if constants_inputs["DELAY"]["FEED_SHUTOFF_MONTHS"] == 0:
            feed_ratio = 0
        else:
            feed_ratio = 1

        (
            biofuels_prewaste,
            feed_prewaste,
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

        feed_and_biofuels.biofuel = biofuels_prewaste
        feed_and_biofuels.feed = feed_prewaste

        feed_and_biofuels.nonhuman_consumption = (
            feed_and_biofuels.biofuel + feed_and_biofuels.feed
        )

        nonhuman_consumption = feed_and_biofuels.nonhuman_consumption

        # post waste

        time_consts["nonhuman_consumption"] = nonhuman_consumption
        time_consts["feed"] = feed_and_biofuels.feed
        time_consts["biofuel"] = feed_and_biofuels.biofuel

        time_consts[
            "excess_feed"
        ] = feed_and_biofuels.get_excess_food_usage_from_percents(
            constants_inputs["EXCESS_FEED_PERCENT"]
        )

        return (
            constants_out,
            time_consts,
            feed_and_biofuels,
        )

    def add_dietary_constraints_to_scp_and_cs(self, constants_out, time_consts):
        """
        This function adds dietary constraints to SCP and CS, ensuring that they are never greater than the minimum fraction
        able to be eaten by humans. If they are greater, they are reduced to the minimum.

        Args:
            constants_out (dict): A dictionary containing constants
            time_consts (dict): A dictionary containing time constants

        Returns:
            dict: A dictionary containing time constants with dietary constraints added to SCP and CS
        """

        if constants_out["ADD_METHANE_SCP"]:
            # loop through the methane SCP and make sure it's never greater than
            # the minimum fraction able to be eaten by humans.
            # If it is greater, reduce it to the minimum.
            capped_kcals_ratios = np.array([])
            methane_scp = time_consts["methane_scp"]
            methane_scp_fraction = (
                methane_scp.for_humans.in_units_percent_fed().kcals / 100
            )
            capped_kcals_ratios = []
            for month in range(0, len(methane_scp_fraction)):
                capped_kcals_ratios.append(
                    min(
                        methane_scp_fraction[month],
                        methane_scp.MAX_FRACTION_HUMAN_FOOD_CONSUMED_AS_SCP,
                    )
                )
            time_consts["methane_scp"].for_humans = methane_scp.for_humans * np.array(
                capped_kcals_ratios
            )

        if constants_out["ADD_CELLULOSIC_SUGAR"]:
            # loop through the cellulosic sugar and make sure it's never greater than
            # the minimum fraction able to be eaten by humans.
            # If it is greater, reduce it to the minimum.
            capped_kcals_ratios = np.array([])
            cellulosic_sugar = time_consts["cellulosic_sugar"]
            cellulosic_sugar.for_humans.make_sure_is_a_list()
            cellulosic_sugar_fraction = (
                cellulosic_sugar.for_humans.in_units_percent_fed().kcals / 100
            )
            capped_kcals_ratios = []
            for month in range(0, len(cellulosic_sugar_fraction)):
                capped_kcals_ratios.append(
                    min(
                        cellulosic_sugar_fraction[month],
                        cellulosic_sugar.MAX_FRACTION_HUMAN_FOOD_CONSUMED_AS_CS,
                    )
                )

            time_consts[
                "cellulosic_sugar"
            ].for_humans = cellulosic_sugar.for_humans * np.array(capped_kcals_ratios)

        return time_consts

    def calculate_biofuel_components_without_stored_food(
        self,
        include_fat_or_protein,
        biofuels_before_cap_prewaste,
        seaweed,
        cellulosic_sugar,
        methane_scp,
        outdoor_crops,
    ):
        """
        Calculates the components of biofuel production without considering stored food.
        Args:
            include_fat_or_protein (bool): whether to include fat or protein in the calculations
            biofuels_before_cap_prewaste (Food): the amount of biofuels before the cap and pre-waste
            seaweed (Seaweed): the seaweed object
            cellulosic_sugar (CellulosicSugar): the cellulosic sugar object
            methane_scp (MethaneSCP): the methane SCP object
            outdoor_crops (OutdoorCrops): the outdoor crops object
        Returns:
            tuple: a tuple containing the remaining biofuel needed from stored food, the amount of outdoor crops used for biofuel,
            the amount of methane SCP used for biofuel, and the amount of cellulosic sugar used for biofuel
        """
        assert not include_fat_or_protein, """ERROR:" biofuel calculations are not 
        working  yet for scenarios including fat or protein"""

        # first, preference seaweed, then cellulosic_sugar, then methane_scp

        # TODO: ADD SEAWEED
        # cellulosic sugar

        cell_sugar_for_biofuel = (
            cellulosic_sugar.MAX_FRACTION_BIOFUEL_CONSUMED_AS_CELLULOSIC_SUGAR
            * biofuels_before_cap_prewaste.kcals
        )

        # minimum between elements of two 1d arrays
        cell_sugar_for_biofuel_after_limit = np.min(
            [cell_sugar_for_biofuel, cellulosic_sugar.production.kcals], axis=0
        )

        cellulosic_sugar_used_for_biofuel = np.min(
            [cell_sugar_for_biofuel_after_limit, biofuels_before_cap_prewaste.kcals],
            axis=0,
        )

        remaining_biofuel_needed = np.subtract(
            biofuels_before_cap_prewaste.kcals, cellulosic_sugar_used_for_biofuel
        )

        # methanescp

        methane_scp_for_biofuel = (
            methane_scp.MAX_FRACTION_BIOFUEL_CONSUMED_AS_SCP * remaining_biofuel_needed
        )

        methane_scp_for_biofuel_after_limit = np.min(
            [methane_scp_for_biofuel, methane_scp.production.kcals], axis=0
        )

        methane_scp_used_for_biofuel = np.min(
            [methane_scp_for_biofuel_after_limit, remaining_biofuel_needed], axis=0
        )

        remaining_biofuel_needed = np.subtract(
            biofuels_before_cap_prewaste.kcals, methane_scp_used_for_biofuel
        )

        # outdoor growing

        outdoor_crops_used_for_biofuel = np.min(
            [outdoor_crops.production.kcals, remaining_biofuel_needed], axis=0
        )

        remaining_biofuel_needed_kcals = np.subtract(
            biofuels_before_cap_prewaste.kcals, outdoor_crops_used_for_biofuel
        )
        remaining_biofuel_needed_from_stored_food = Food(
            kcals=remaining_biofuel_needed_kcals,
            fat=np.zeros(len(remaining_biofuel_needed_kcals)),
            protein=np.zeros(len(remaining_biofuel_needed_kcals)),
            kcals_units="billion kcals each month",
            fat_units="thousand tons each month",
            protein_units="thousand tons each month",
        )

        return (
            remaining_biofuel_needed_from_stored_food,
            outdoor_crops_used_for_biofuel,
            methane_scp_used_for_biofuel,
            cellulosic_sugar_used_for_biofuel,
        )

    def calculate_feed_components_without_stored_food(
        self,
        include_fat_or_protein,  # boolean indicating whether to include fat or protein in calculations
        feeds_before_cap_prewaste,  # Food object representing the amount of feed available before capping and pre-waste
        max_fraction_feed_consumed_as_cellulosic_sugar,  # maximum fraction of feed that can be consumed as cellulosic sugar
        max_fraction_feed_consumed_as_methane_scp,  # maximum fraction of feed that can be consumed as methane SCP
        cellulosic_sugar_remaining_after_biofuel,  # amount of cellulosic sugar remaining after biofuel production
        methane_scp_remaining_after_biofuel,  # amount of methane SCP remaining after biofuel production
        outdoor_crops_remaining_after_biofuel,  # amount of outdoor crops remaining after biofuel production
    ):
        """
        Calculates the components of feed that can be used without stored food, based on the available feed and biofuel
        production. The function first calculates the amount of cellulosic sugar and methane SCP that can be used for feed,
        and then uses the remaining feed to obtain outdoor crops. If there is still a deficit, the function returns the
        remaining amount of feed needed from stored food.

        Args:
            include_fat_or_protein (bool): Boolean indicating whether to include fat or protein in calculations.
            feeds_before_cap_prewaste (Food): Food object representing the amount of feed available before capping and pre-waste.
            max_fraction_feed_consumed_as_cellulosic_sugar (float): Maximum fraction of feed that can be consumed as cellulosic sugar.
            max_fraction_feed_consumed_as_methane_scp (float): Maximum fraction of feed that can be consumed as methane SCP.
            cellulosic_sugar_remaining_after_biofuel (float): Amount of cellulosic sugar remaining after biofuel production.
            methane_scp_remaining_after_biofuel (float): Amount of methane SCP remaining after biofuel production.
            outdoor_crops_remaining_after_biofuel (float): Amount of outdoor crops remaining after biofuel production.

        Returns:
            Tuple[Food, float, float, float]: A tuple containing the remaining feed needed from stored food, the amount of
            outdoor crops used for feed, the amount of methane SCP used for feed, and the amount of cellulosic sugar used for feed.
        """

        assert not include_fat_or_protein, """ERROR: feed calculations are not 
        working  yet for scenarios including fat or protein"""

        # Calculate the amount of cellulosic sugar that can be used for feed
        cell_sugar_for_feed = (
            max_fraction_feed_consumed_as_cellulosic_sugar
            * feeds_before_cap_prewaste.kcals
        )

        # Limit the amount of cellulosic sugar that can be used for feed based on the amount remaining after biofuel production
        cell_sugar_for_feed_after_limit = np.min(
            [cell_sugar_for_feed, cellulosic_sugar_remaining_after_biofuel], axis=0
        )

        # Calculate the amount of cellulosic sugar used for feed
        cellulosic_sugar_used_for_feed = np.min(
            [cell_sugar_for_feed_after_limit, feeds_before_cap_prewaste.kcals], axis=0
        )

        # Calculate the remaining feed needed after using cellulosic sugar for feed
        remaining_feed_needed = np.subtract(
            feeds_before_cap_prewaste.kcals, cellulosic_sugar_used_for_feed
        )

        # Calculate the amount of methane SCP that can be used for feed
        methane_scp_for_feed = (
            max_fraction_feed_consumed_as_methane_scp * remaining_feed_needed
        )

        # Limit the amount of methane SCP that can be used for feed based on the amount remaining after biofuel production
        methane_scp_for_feed_after_limit = np.min(
            [methane_scp_for_feed, methane_scp_remaining_after_biofuel], axis=0
        )

        # Calculate the amount of methane SCP used for feed
        methane_scp_used_for_feed = np.min(
            [methane_scp_for_feed_after_limit, remaining_feed_needed], axis=0
        )

        # Calculate the remaining feed needed after using methane SCP for feed
        remaining_feed_needed = np.subtract(
            feeds_before_cap_prewaste.kcals, methane_scp_used_for_feed
        )

        # Calculate the amount of outdoor crops used for feed
        outdoor_crops_used_for_feed = np.min(
            [outdoor_crops_remaining_after_biofuel, remaining_feed_needed], axis=0
        )

        # Calculate the remaining feed needed after using outdoor crops for feed
        remaining_feed_needed_kcals = np.subtract(
            feeds_before_cap_prewaste.kcals, outdoor_crops_used_for_feed
        )

        # Create a Food object representing the remaining feed needed from stored food
        remaining_feed_needed_from_stored_food = Food(
            kcals=np.array(remaining_feed_needed_kcals),
            fat=np.zeros(len(remaining_feed_needed_kcals)),
            protein=np.zeros(len(remaining_feed_needed_kcals)),
            kcals_units="billion kcals each month",
            fat_units="thousand tons each month",
            protein_units="thousand tons each month",
        )

        return (
            remaining_feed_needed_from_stored_food,
            outdoor_crops_used_for_feed,
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
        """
        Calculates the net feed available without stored food or seaweed.

        Args:
            include_fat_or_protein (bool): whether to include fat or protein in the calculations
            combined_feed (float): the combined feed available
            outdoor_crops (float): the outdoor crops available
            methane_scp (float): the methane SCP available
            cellulosic_sugar (float): the cellulosic sugar available
            seaweed (float): the seaweed available

        Returns:
            float: the net feed available without stored food or seaweed
        """

        assert not include_fat_or_protein, """ERROR: feed calculations are not working 
        yet for scenarios including fat or protein"""

        """
        For now, we will ignore seaweed as a feed source. This is because we don't have a good way to
        accurately estimate what the linear optimizer will predict for the amount of seaweed monthly
        produced
        """
        # Calculate the cellulosic sugar for feed
        cell_sugar_for_feed = (
            cellulosic_sugar.MAX_FRACTION_FEED_CONSUMED_AS_CELLULOSIC_SUGAR
            * combined_nonhuman_consumption_before_cap_or_waste
        )

        # Calculate the maximum SCP for feed
        max_scp_for_feed = (
            methane_scp.MAX_FRACTION_FEED_CONSUMED_AS_SCP * combined_feed_kcals
        )

        # Calculate the SCP for feed after limit
        scp_for_feed_after_limit = np.min([max_scp_for_feed, methane_scp.kcals], axis=0)

        # Calculate the cellulosic sugar for feed after limit
        cell_sugar_for_feed_after_limit = np.min(
            [cell_sugar_for_feed, cellulosic_sugar.kcals], axis=0
        )

        # TODO: include seaweed as a feed source. Right now it's complicated because
        # we haven't distinguished the feed vs human consumption of seaweed
        # seaweed.estimate_seaweed_growth_for_estimating_feed_availability()
        # max_seaweed_for_feed = seaweed.estimated_seaweed_feed_consumed_after_waste

        # Calculate the net feed available without stored food or seaweed
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
        if constants_inputs["REDUCED_BREEDING_STRATEGY"]:
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
        else:
            data = {
                "country_code": constants_inputs["COUNTRY_CODE"],
                "reduction_in_beef_calves": 0,
                "reduction_in_dairy_calves": 0,
                "increase_in_slaughter": 100,
                "reduction_in_pig_breeding": 0,
                "reduction_in_poultry_breeding": 0,
                "months": constants_inputs["NMONTHS"],
                "discount_rate": 0,
                "mother_slaughter": 0,
                "use_grass_and_residues_for_dairy": use_grass_and_residues_for_dairy,
                "keep_dairy": True,
                "feed_ratio": feed_ratio,
            }
        feed_dairy_meat_results, feed = cao.calculate_feed_and_animals(data)

        constants_out, time_consts = self.calculate_culled_meat_from_feed_results(
            constants_out, time_consts, meat_and_dairy, feed_dairy_meat_results
        )

        (
            constants_out,
            time_consts,
        ) = self.calculate_non_culled_meat_and_dairy_from_feed_results(
            constants_inputs,
            constants_out,
            time_consts,
            feed_dairy_meat_results["Dairy Pop"],
            meat_and_dairy,
        )

        # FEED AND BIOFUELS from breeding reduction strategy

        (
            biofuels_prewaste,
            feed_prewaste,
            excess_feed_prewaste,
        ) = feed_and_biofuels.get_biofuels_and_feed_before_waste_from_animal_pops(
            constants_inputs,
            feed,
        )

        feed_and_biofuels.nonhuman_consumption = biofuels_prewaste + feed_prewaste

        PLOT_FEED_BEFORE_WASTE = False

        if PLOT_FEED_BEFORE_WASTE:
            feed_prewaste.in_units_percent_fed().plot("feed_prewaste")

        time_consts["excess_feed"] = excess_feed_prewaste
        return (
            biofuels_prewaste,
            feed_prewaste,
            feed_dairy_meat_results,
            time_consts,
            constants_out,
        )

        # feed_dairy_meat_results, feed = cao.calculate_feed_and_animals(data)
        # # MEAT AND DAIRY from breeding reduction strategy

        # meat_and_dairy.calculate_meat_nutrition()

        # (
        #     constants_out["culled_meat"],
        #     constants_out["CULLED_MEAT_FRACTION_FAT"],
        #     constants_out["CULLED_MEAT_FRACTION_PROTEIN"],
        # ) = meat_and_dairy.calculate_culled_meat(
        #     np.sum(feed_dairy_meat_results["Poultry Slaughtered"]),
        #     np.sum(feed_dairy_meat_results["Pig Slaughtered"]),
        #     np.sum(feed_dairy_meat_results["Beef Slaughtered"]),
        # )

        # time_consts["max_culled_kcals"] = meat_and_dairy.get_max_slaughter_monthly(
        #     feed_dairy_meat_results["Beef Slaughtered"],
        #     feed_dairy_meat_results["Pig Slaughtered"],
        #     feed_dairy_meat_results["Poultry Slaughtered"],
        # )

        # # https://www.nass.usda.gov/Charts_and_Maps/Milk_Production_and_Milk_Cows/cowrates.php
        # monthly_milk_tons = (
        #     feed_dairy_meat_results["Dairy Pop"]
        #     * 24265
        #     / 2.2046
        #     / 365
        #     * 30.4
        #     / 1000
        #     / 2
        # )
        # # cows * pounds per cow per day * punds_to_kg /days in year * days in month /
        # # kg_in_tons * ratio_milk_producing_cows
        # PRINT_ANNUAL_POUNDS_MILK = False
        # if PRINT_ANNUAL_POUNDS_MILK:
        #     print("annual pounds milk")  # ton to kg, kg to pounds, monthly to annual
        #     print(
        #         monthly_milk_tons * 1000 * 2.2046 * 12
        #     )  # ton to kg, kg to pounds, monthly to annual

        # (
        #     grazing_milk_kcals,
        #     grazing_milk_fat,
        #     grazing_milk_protein,
        # ) = meat_and_dairy.get_grazing_milk_produced_postwaste(monthly_milk_tons)

        # time_consts["grazing_milk_kcals"] = grazing_milk_kcals
        # time_consts["grazing_milk_fat"] = grazing_milk_fat
        # time_consts["grazing_milk_protein"] = grazing_milk_protein

        # time_consts["cattle_grazing_maintained_kcals"] = np.zeros(
        #     constants_inputs["NMONTHS"]
        # )
        # time_consts["cattle_grazing_maintained_fat"] = np.zeros(
        #     constants_inputs["NMONTHS"]
        # )
        # time_consts["cattle_grazing_maintained_protein"] = np.zeros(
        #     constants_inputs["NMONTHS"]
        # )

        # (
        #     constants_out["KG_PER_SMALL_ANIMAL"],
        #     constants_out["KG_PER_MEDIUM_ANIMAL"],
        #     constants_out["KG_PER_LARGE_ANIMAL"],
        #     constants_out["LARGE_ANIMAL_KCALS_PER_KG"],
        #     constants_out["LARGE_ANIMAL_FAT_RATIO"],
        #     constants_out["LARGE_ANIMAL_PROTEIN_RATIO"],
        #     constants_out["MEDIUM_ANIMAL_KCALS_PER_KG"],
        #     constants_out["SMALL_ANIMAL_KCALS_PER_KG"],
        # ) = meat_and_dairy.get_meat_nutrition()

        # time_consts["grain_fed_meat_kcals"] = np.zeros(constants_inputs["NMONTHS"])
        # time_consts["grain_fed_meat_fat"] = np.zeros(constants_inputs["NMONTHS"])
        # time_consts["grain_fed_meat_protein"] = np.zeros(constants_inputs["NMONTHS"])
        # time_consts["grain_fed_milk_kcals"] = np.zeros(constants_inputs["NMONTHS"])
        # time_consts["grain_fed_milk_fat"] = np.zeros(constants_inputs["NMONTHS"])
        # time_consts["grain_fed_milk_protein"] = np.zeros(constants_inputs["NMONTHS"])

        # time_consts["grain_fed_created_kcals"] = np.zeros(constants_inputs["NMONTHS"])
        # time_consts["grain_fed_created_fat"] = np.zeros(constants_inputs["NMONTHS"])
        # time_consts["grain_fed_created_protein"] = np.zeros(constants_inputs["NMONTHS"])

        # # FEED AND BIOFUELS from breeding reduction strategy

        # (
        #     biofuels_before_cap_prewaste,
        #     feed_before_cap_prewaste,
        #     excess_feed_prewaste,
        # ) = feed_and_biofuels.get_biofuels_and_feed_before_waste_from_animal_pops(
        #     constants_inputs,
        #     feed,
        # )

        # feed_and_biofuels.nonhuman_consumption = (
        #     biofuels_before_cap_prewaste + feed_before_cap_prewaste
        # )

        # PLOT_FEED_BEFORE_WASTE = False

        # if PLOT_FEED_BEFORE_WASTE:
        #     feed_before_cap_prewaste.in_units_percent_fed().plot(
        #         "feed_before_cap_prewaste"
        #     )

        # time_consts["excess_feed"] = excess_feed_prewaste

        # return (
        #     biofuels_before_cap_prewaste,
        #     feed_before_cap_prewaste,
        #     meat_and_dairy,
        #     time_consts,
        #     constants_out,
        # )

    def calculate_culled_meat_from_feed_results(
        self, constants_out, time_consts, meat_and_dairy, feed_dairy_meat_results
    ):
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

        return constants_out, time_consts

    def calculate_non_culled_meat_and_dairy_from_feed_results(
        self,
        constants_inputs,
        constants_out,
        time_consts,
        dairy_pop,
        meat_and_dairy,
    ):
        # TODO: parametrize these constants in the scenarios so they can be adjusted
        # without messing with the code

        # https://www.nass.usda.gov/Charts_and_Maps/Milk_Production_and_Milk_Cows/cowrates.php
        monthly_milk_tons = dairy_pop * 24265 / 2.2046 / 365 * 30.4 / 1000 / 2
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

        return constants_out, time_consts

    def init_meat_and_dairy_params(
        self,
        constants_inputs,
        constants_out,
        time_consts,
        feed_and_biofuels,
        outdoor_crops,
    ):
        """
        Initializes meat and dairy parameters.

        Args:
            constants_inputs (dict): dictionary of input constants
            constants_out (dict): dictionary of output constants
            time_consts (dict): dictionary of time constants
            feed_and_biofuels (dict): dictionary of feed and biofuel constants
            outdoor_crops (dict): dictionary of outdoor crop constants

        Returns:
            tuple: tuple containing meat and dairy object, constants_out dictionary, and time_consts dictionary
        """

        # Initialize MeatAndDairy object and calculate meat nutrition
        meat_and_dairy = MeatAndDairy(constants_inputs)
        meat_and_dairy.calculate_meat_nutrition()

        # Initialize grazing parameters
        time_consts, meat_and_dairy = self.init_grazing_params(
            constants_inputs, time_consts, meat_and_dairy
        )

        # Initialize grain-fed meat parameters
        time_consts, meat_and_dairy = self.init_grain_fed_meat_params(
            time_consts,
            meat_and_dairy,
            feed_and_biofuels,
            constants_inputs,
            outdoor_crops,
        )

        # Initialize culled meat parameters
        (
            constants_out,
            time_consts,
            meat_and_dairy,
        ) = self.init_culled_meat_params(
            constants_inputs, constants_out, time_consts, meat_and_dairy
        )

        # Return tuple containing meat and dairy object, constants_out dictionary, and time_consts dictionary
        return meat_and_dairy, constants_out, time_consts

    def init_grazing_params(self, constants_inputs, time_consts, meat_and_dairy):
        """
        Initializes grazing parameters for the simulation.

        Args:
            constants_inputs (dict): A dictionary containing constant inputs for the simulation.
            time_consts (dict): A dictionary containing time constants for the simulation.
            meat_and_dairy (MeatAndDairy): An instance of the MeatAndDairy class.

        Returns:
            tuple: A tuple containing the updated time constants and the updated meat_and_dairy instance.

        """
        # Calculate meat and milk production from human inedible feed if efficient feed strategy is used
        if constants_inputs["USE_EFFICIENT_FEED_STRATEGY"]:
            meat_and_dairy.calculate_meat_milk_from_human_inedible_feed(
                constants_inputs
            )
        # Otherwise, calculate continued ratios of meat and dairy production from grazing
        else:
            meat_and_dairy.calculate_continued_ratios_meat_dairy_grazing(
                constants_inputs
            )

        # Get grazing milk produced post-waste
        (
            grazing_milk_kcals,
            grazing_milk_fat,
            grazing_milk_protein,
        ) = meat_and_dairy.get_grazing_milk_produced_postwaste(
            meat_and_dairy.grazing_milk_produced_prewaste
        )

        # Update time constants with grazing milk production values
        time_consts["grazing_milk_kcals"] = grazing_milk_kcals
        time_consts["grazing_milk_fat"] = grazing_milk_fat
        time_consts["grazing_milk_protein"] = grazing_milk_protein

        # Get post-waste cattle ongoing meat production from grazing
        (
            cattle_grazing_maintained_kcals,
            cattle_grazing_maintained_fat,
            cattle_grazing_maintained_protein,
        ) = meat_and_dairy.get_cattle_grazing_maintained()

        # Update time constants with cattle grazing production values
        time_consts["cattle_grazing_maintained_kcals"] = cattle_grazing_maintained_kcals
        time_consts["cattle_grazing_maintained_fat"] = cattle_grazing_maintained_fat
        time_consts[
            "cattle_grazing_maintained_protein"
        ] = cattle_grazing_maintained_protein

        # Return updated time constants and meat_and_dairy instance
        return time_consts, meat_and_dairy

    def init_grain_fed_meat_params(
        self,
        time_consts,
        meat_and_dairy,
        feed_and_biofuels,
        constants_inputs,
        outdoor_crops,
    ):
        """
        Initializes grain-fed meat parameters by calculating the amount of grain-fed meat and milk
        produced from human-edible feed, and updating the time constants dictionary with the results.

        Args:
            self: instance of the class
            time_consts (dict): dictionary containing time constants
            meat_and_dairy (MeatAndDairy): instance of MeatAndDairy class
            feed_and_biofuels (FeedAndBiofuels): instance of FeedAndBiofuels class
            constants_inputs (dict): dictionary containing constant inputs
            outdoor_crops (OutdoorCrops): instance of OutdoorCrops class

        Returns:
            tuple: updated time constants dictionary and instance of MeatAndDairy class
        """

        # APPLY FEED+BIOFUEL WASTE here
        # this is because the total contributed by feed and biofuels is actually
        # applied to
        # the crops and stored food before waste, which means the subtraction of waste
        # happens
        # to the feed and biofuels before subtracting from stored food and crops.
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
        """
        Initializes the parameters for culled meat, which is based on the amount that wouldn't be maintained
        (excluding maintained cattle as well as maintained chicken and pork). This calculation is pre-waste for
        the meat maintained of course (no waste applied to livestock maintained counts from which we determined
        the amount of meat which can be culled). The actual culled meat returned is post waste.

        Args:
            constants_inputs (dict): dictionary of input constants
            constants_out (dict): dictionary of output constants
            time_consts (dict): dictionary of time constants
            meat_and_dairy (MeatAndDairy): instance of MeatAndDairy class

        Returns:
            tuple: tuple containing updated constants_out, time_consts, and meat_and_dairy
        """

        # Calculate the number of animals culled
        meat_and_dairy.calculate_animals_culled(constants_inputs)

        # Calculate the initial culled meat pre-waste, as well as the fraction of fat and protein
        (
            meat_and_dairy.initial_culled_meat_prewaste,
            constants_out["CULLED_MEAT_FRACTION_FAT"],
            constants_out["CULLED_MEAT_FRACTION_PROTEIN"],
        ) = meat_and_dairy.calculate_culled_meat(
            meat_and_dairy.init_small_animals_culled,
            meat_and_dairy.init_medium_animals_culled,
            meat_and_dairy.init_large_animals_culled,
        )

        # Get the maximum ratio of culled slaughter to baseline
        MAX_RATIO_CULLED_SLAUGHTER_TO_BASELINE = constants_inputs[
            "MAX_RATIO_CULLED_SLAUGHTER_TO_BASELINE"
        ]

        # Get the culled meat post-waste
        culled_meat = meat_and_dairy.get_culled_meat_post_waste(constants_inputs)

        # Calculate the maximum number of calories from culled meat
        time_consts["max_culled_kcals"] = meat_and_dairy.calculate_meat_limits(
            MAX_RATIO_CULLED_SLAUGHTER_TO_BASELINE, culled_meat
        )

        # Update the constants_out dictionary with the culled meat
        constants_out["culled_meat"] = culled_meat

        # Get the nutrition information for small, medium, and large animals
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
