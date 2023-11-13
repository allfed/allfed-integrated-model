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
from src.food_system.animal_populations import CalculateFeedAndMeat


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
            AssertionError: If maintained meat needs to be added for continued feed usage or if the function is not
            run for the first time.

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
        Calculates the expected amount of livestock if breeding were quickly reduced and slaughter only increased
        slightly,
        then using that we calculate the feed they would use given the expected input animal populations over time.

        Args:
            self (object): instance of the class
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

        # Initialize FeedAndBiofuels and MeatAndDairy objects
        feed_and_biofuels = FeedAndBiofuels(constants_inputs)

        (
            biofuels,
            feed,
            excess_feed,
        ) = feed_and_biofuels.get_biofuels_and_feed_from_delayed_shutoff(
            constants_inputs
        )

        meat_and_dairy = MeatAndDairy(constants_inputs)

        grasses_for_animals = meat_and_dairy.human_inedible_feed

        if constants_inputs["REDUCED_BREEDING_STRATEGY"]:
            feed_meat_object = CalculateFeedAndMeat(
                country_code=constants_inputs["COUNTRY_CODE"],
                available_feed=feed,
                available_grass=grasses_for_animals,
                scenario="reduced",  # tries to reduce breeding
            )
        else:
            feed_meat_object = CalculateFeedAndMeat(
                country_code=constants_inputs["COUNTRY_CODE"],
                available_feed=feed,
                available_grass=grasses_for_animals,
                scenario="baseline",  # doesn't try to reduce breeding, baseline animal pops
            )

        # this is just to make sure you know you're running a diet calculation
        assert (
            excess_feed.all_equals_zero()
        ), "if you're running a diet calculation, delete this assert"

        # MEAT AND DAIRY from breeding reduction strategy

        # Initialize variables using the init_meat_and_dairy_and_feed_from_breeding function
        (
            feed_used_with_nutrients,
            time_consts,
            constants_out,
        ) = self.init_meat_and_dairy_and_feed_from_breeding(
            constants_inputs,
            feed_meat_object,
            feed_and_biofuels,
            meat_and_dairy,
            constants_out,
            time_consts,
        )

        # FEED AND BIOFUELS from breeding reduction strategy

        assert feed.all_greater_than_or_equal_to(
            feed_used_with_nutrients
        ), "Error: Animals ate more feed than was available!"

        feed_and_biofuels.nonhuman_consumption = biofuels + feed_used_with_nutrients

        PLOT_FEED = False

        if PLOT_FEED:
            feed.in_units_percent_fed().plot("feed")

        time_consts["excess_feed"] = excess_feed

        # Update feed_and_biofuels object with their values
        feed_and_biofuels.biofuel = biofuels
        feed_and_biofuels.feed = feed_used_with_nutrients
        nonhuman_consumption = feed_and_biofuels.nonhuman_consumption

        # Update time_consts dictionary
        time_consts["nonhuman_consumption"] = nonhuman_consumption
        time_consts["feed"] = feed_and_biofuels.feed
        time_consts["biofuel"] = feed_and_biofuels.biofuel
        time_consts[
            "excess_feed"
        ] = feed_and_biofuels.get_excess_food_usage_from_percents(
            constants_inputs["EXCESS_FEED_PERCENT"]
        )

        # Return tuple containing constants_out, time_consts, and feed_and_biofuels
        return (
            constants_out,
            time_consts,
            feed_and_biofuels,
        )

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
        It assumes a 2100 kcals diet, and scales the "upper safe" nutrition from the spreadsheet down to this
        "standard" level.
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
            constants_out (dict): A dictionary containing the output constants
            constants_inputs (dict): A dictionary containing the input constants

        Returns:
            tuple: A tuple containing the updated constants_out and the outdoor_crops object

        This function initializes the outdoor crops parameters by calculating the rotation ratios and monthly
        production.
        It takes in two dictionaries, constants_out and constants_inputs, which contain the output and input constants
        respectively.
        The function returns a tuple containing the updated constants_out and the outdoor_crops object.

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

        # Update the constants_out dictionary with the outdoor crops' rotation fraction fat, and protein and harvest
        # duration in months
        constants_out[
            "OG_ROTATION_FRACTION_FAT"
        ] = outdoor_crops.OG_ROTATION_FRACTION_FAT
        constants_out[
            "OG_ROTATION_FRACTION_PROTEIN"
        ] = outdoor_crops.OG_ROTATION_FRACTION_PROTEIN

        constants_out["INITIAL_HARVEST_DURATION_IN_MONTHS"] = constants_inputs[
            "INITIAL_HARVEST_DURATION_IN_MONTHS"
        ]
        print("DELAY in parameters")
        print(constants_inputs["DELAY"])
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
        time_consts["methane_scp"] = methane_scp.production

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

    def init_meat_and_dairy_and_feed_from_breeding(
        self,
        constants_inputs,
        feed_meat_object,
        feed_and_biofuels,
        meat_and_dairy,
        constants_out,
        time_consts,
    ):
        constants_out, time_consts = self.calculate_culled_meat_from_feed_results(
            constants_out, time_consts, meat_and_dairy, feed_meat_object
        )

        dairy_population = feed_meat_object.get_total_dairy_cows()

        (
            constants_out,
            time_consts,
        ) = self.calculate_non_culled_meat_and_dairy_from_feed_results(
            constants_inputs,
            constants_out,
            time_consts,
            dairy_population,
            meat_and_dairy,
        )

        feed_used_with_nutrients = feed_and_biofuels.create_feed_food_from_kcals(
            feed_meat_object.feed_used
        )

        return (
            feed_used_with_nutrients,
            time_consts,
            constants_out,
        )

    def calculate_culled_meat_from_feed_results(
        self, constants_out, time_consts, meat_and_dairy, feed_meat_object
    ):
        """
        Calculates the amount of culled meat from feed results and updates the constants_out and time_consts
        dictionaries.

        Args:
            constants_out (dict): dictionary containing constants to be updated
            time_consts (dict): dictionary containing time constants to be updated
            meat_and_dairy (MeatAndDairy): instance of MeatAndDairy class
            feed_dairy_meat_results (dict): dictionary containing feed, dairy, and meat results

        Returns:
            tuple: tuple containing updated constants_out and time_consts dictionaries

        """

        (
            animals_killed_for_meat_small,
            animals_killed_for_meat_medium,
            animals_killed_for_meat_large,
        ) = feed_meat_object.get_meat_produced()

        meat_and_dairy.calculate_meat_nutrition()

        time_consts["max_culled_kcals"] = meat_and_dairy.get_max_slaughter_monthly(
            small_animals_culled=animals_killed_for_meat_small,
            medium_animals_culled=animals_killed_for_meat_medium,
            large_animals_culled=animals_killed_for_meat_large,
        )

        # Calculate the amount of culled meat and update constants_out dictionary
        (
            constants_out["culled_meat"],
            constants_out["CULLED_MEAT_FRACTION_FAT"],
            constants_out["CULLED_MEAT_FRACTION_PROTEIN"],
        ) = meat_and_dairy.calculate_culled_meat(
            np.sum(animals_killed_for_meat_small),
            np.sum(animals_killed_for_meat_medium),
            np.sum(animals_killed_for_meat_large),
        )

        # Calculate the maximum amount of culled meat in kcals and update time_consts dictionary
        time_consts["max_culled_kcals"] = meat_and_dairy.get_max_slaughter_monthly(
            animals_killed_for_meat_small,
            animals_killed_for_meat_medium,
            animals_killed_for_meat_large,
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
        """
        Calculates the non-culled meat and dairy from feed results.
        Args:
            self: instance of the Parameters class
            constants_inputs (dict): dictionary of input constants
            constants_out (dict): dictionary of output constants
            time_consts (dict): dictionary of time constants
            dairy_pop (float): number of dairy cows
            meat_and_dairy (MeatAndDairy): instance of the MeatAndDairy class
        Returns:
            tuple: tuple containing constants_out and time_consts
        """

        # TODO: parametrize these constants in the scenarios so they can be adjusted
        # without messing with the code

        # Calculate monthly milk tons
        # https://www.nass.usda.gov/Charts_and_Maps/Milk_Production_and_Milk_Cows/cowrates.php
        monthly_milk_tons = dairy_pop * 24265 / 2.2046 / 365 * 30.4 / 1000 / 2
        # cows * pounds per cow per day * punds_to_kg /days in year * days in month /
        # kg_in_tons * ratio_milk_producing_cows

        # Print annual pounds milk if PRINT_ANNUAL_POUNDS_MILK is True
        PRINT_ANNUAL_POUNDS_MILK = False
        if PRINT_ANNUAL_POUNDS_MILK:
            print("annual pounds milk")  # ton to kg, kg to pounds, monthly to annual
            print(
                monthly_milk_tons * 1000 * 2.2046 * 12
            )  # ton to kg, kg to pounds, monthly to annual

        # Get grazing milk produced postwaste
        (
            grazing_milk_kcals,
            grazing_milk_fat,
            grazing_milk_protein,
        ) = meat_and_dairy.get_grazing_milk_produced_postwaste(monthly_milk_tons)

        # Set grazing milk constants in time_consts
        time_consts["grazing_milk_kcals"] = grazing_milk_kcals
        time_consts["grazing_milk_fat"] = grazing_milk_fat
        time_consts["grazing_milk_protein"] = grazing_milk_protein

        # Set cattle grazing constants in time_consts
        time_consts["cattle_grazing_maintained_kcals"] = np.zeros(
            constants_inputs["NMONTHS"]
        )
        time_consts["cattle_grazing_maintained_fat"] = np.zeros(
            constants_inputs["NMONTHS"]
        )
        time_consts["cattle_grazing_maintained_protein"] = np.zeros(
            constants_inputs["NMONTHS"]
        )

        # Get meat nutrition constants
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

        # Set grain fed meat and milk constants in time_consts
        time_consts["grain_fed_meat_kcals"] = np.zeros(constants_inputs["NMONTHS"])
        time_consts["grain_fed_meat_fat"] = np.zeros(constants_inputs["NMONTHS"])
        time_consts["grain_fed_meat_protein"] = np.zeros(constants_inputs["NMONTHS"])
        time_consts["grain_fed_milk_kcals"] = np.zeros(constants_inputs["NMONTHS"])
        time_consts["grain_fed_milk_fat"] = np.zeros(constants_inputs["NMONTHS"])
        time_consts["grain_fed_milk_protein"] = np.zeros(constants_inputs["NMONTHS"])

        # Set grain fed created constants in time_consts
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

        if constants_inputs["USE_EFFICIENT_FEED_STRATEGY"]:
            meat_and_dairy.calculate_meat_and_dairy_from_grain(
                feed_and_biofuels.fed_to_animals
            )
        else:
            meat_and_dairy.calculate_continued_ratios_meat_dairy_grain(
                feed_and_biofuels.fed_to_animals, outdoor_crops
            )

        # no waste is applied for the grasses.
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
