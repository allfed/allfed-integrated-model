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
import copy
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
from src.food_system.animal_populations import AnimalPopulation, CalculateFeedAndMeat
from src.optimizer.validate_results import Validator


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

    def compute_parameters_first_round(
        self, constants_inputs, time_consts_inputs, scenarios_loader
    ):
        """
        Computes the parameters for the model based on the inputs and scenarios provided.
        This is relevant for the first round of optimization, with no feed assumed.


        Args:
            constants_inputs (dict): A dictionary containing the constant inputs for the model.
            scenarios_loader (ScenariosLoader): An instance of the ScenariosLoader class containing the scenario inputs.

        Returns:
            tuple: A tuple containing the computed constants, time constants, and feed and biofuels.

        Raises:
            AssertionError: If maintained meat needs to be added for continued feed usage or if the function is not
            run for the first time.

        """
        # Check if function is run for the first time
        assert self.FIRST_TIME_RUN
        self.FIRST_TIME_RUN = False

        # Print scenario properties
        PRINT_SCENARIO_PROPERTIES = False
        if PRINT_SCENARIO_PROPERTIES:
            print(scenarios_loader.scenario_description)

        # Ensure every parameter has been initialized for the scenarios_loader
        scenarios_loader.check_all_set()

        # Time dependent constants_out as inputs to the optimizer
        time_consts = {}

        # Single valued constants (not time dependent) given to optimizer
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
        time_consts = self.init_fish_params(
            time_consts, constants_inputs, time_consts_inputs
        )

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
            feed_biofuels_class,  # zero feed, zero biofuel
            biofuels_demand,  # biofuels requested by the user
            feed_demand,  # feed requested by the user
            meat_dictionary_round1,  # meat if no feed were available
        ) = self.init_meat_and_dairy_and_feed_from_breeding_and_subtract_feed_biofuels_round1(
            constants_out,
            constants_inputs,
            time_consts,
        )

        # Set inputs in constants_out
        constants_out["inputs"] = constants_inputs

        return (
            constants_out,
            time_consts,
            feed_biofuels_class,  # zero feed, zero biofuel
            biofuels_demand,  # biofuels requested by the user
            feed_demand,  # feed requested by the user
            meat_dictionary_round1,
        )

    def get_second_round_kcals_with_redistributed_meat(
        self, round_1_meat_kcals, round_2_meat_kcals
    ):
        """
        Gets a new array of kcals where the sum of kcals from meat remains the same, but the places where the meat was
        originally larger than round 1 is reduced, and the places where the meat was less than round 1 is increased.
        """
        if round_1_meat_kcals.sum() > round_2_meat_kcals.sum():
            print(
                "WARNING: Meat produced from feed is less than produced without feed. Skipping round 2 and setting"
                " feed used to zero."
            )
            return None
        difference = round_2_meat_kcals - round_1_meat_kcals
        strictly_positive_difference = self.fill_negatives_with_positives(difference)

        assert np.all(
            strictly_positive_difference >= -0.001
        )  # make sure it's indeed positive within a rounding error

        # if the adjusted (filled in) map is higher, then we want that to be added to round_2_meat_kcals
        adjustment_to_round2 = strictly_positive_difference - difference

        assert abs(adjustment_to_round2.sum()) <= 0.001
        # the total meat can't go below zero
        assert np.all(adjustment_to_round2 + round_2_meat_kcals >= -0.001)

        new_round_2_meat_kcals = round_2_meat_kcals + adjustment_to_round2

        return new_round_2_meat_kcals

    def fill_negatives_with_positives(self, arr):
        # go backwards through the array and fill any negative values with recent positive values so all values are
        # above zero. Ensure the input is a numpy array
        arr = np.array(arr, dtype=float)  # Use float for precision during adjustments
        # Indices of negative values
        negative_indices = np.where(arr < 0)[0]

        # Work from the end of the array to find positive values
        for neg_idx in negative_indices:
            for i in range(len(arr) - 1, -1, -1):
                # Skip if it's the same index or if the value is not positive
                if i == neg_idx or arr[i] <= 0:
                    continue

                # Calculate the adjustment needed
                adjustment = min(-arr[neg_idx], arr[i])
                arr[neg_idx] += adjustment
                arr[i] -= adjustment

                # Break if the negative value has been fully compensated
                if arr[neg_idx] == 0:
                    break

        return arr

    def init_meat_and_dairy_and_feed_from_breeding_and_subtract_feed_biofuels_round1(
        self,
        constants_out,
        constants_inputs,
        time_consts,
    ):
        # Initialize FeedAndBiofuels and MeatAndDairy objects
        feed_and_biofuels_class = FeedAndBiofuels(constants_inputs)

        (
            biofuels_demand,
            feed_demand,
        ) = feed_and_biofuels_class.get_biofuels_and_feed_from_delayed_shutoff(
            constants_inputs
        )

        # The first round of optimizations both calculates the maximum food animals could use,
        # based on the delayed shutoff from the scenario and the baseline feed usage,
        # and calculates the meat produced if no feed is used at all.

        # This is the first round of optimization, so we don't assume feed or biofuels are used.
        zero_feed = Food(
            kcals=np.zeros(constants_inputs["NMONTHS"]),
            fat=np.zeros(constants_inputs["NMONTHS"]),
            protein=np.zeros(constants_inputs["NMONTHS"]),
            kcals_units=feed_demand.kcals_units,
            fat_units=feed_demand.fat_units,
            protein_units=feed_demand.protein_units,
        )

        zero_biofuels = Food(
            kcals=np.zeros(constants_inputs["NMONTHS"]),
            fat=np.zeros(constants_inputs["NMONTHS"]),
            protein=np.zeros(constants_inputs["NMONTHS"]),
            kcals_units=biofuels_demand.kcals_units,
            fat_units=biofuels_demand.fat_units,
            protein_units=biofuels_demand.protein_units,
        )

        meat_and_dairy = MeatAndDairy(constants_inputs)

        grasses_for_animals = meat_and_dairy.human_inedible_feed

        feed_meat_object_round1 = CalculateFeedAndMeat(
            country_code=constants_inputs["COUNTRY_CODE"],
            available_feed=zero_feed,
            available_grass=grasses_for_animals,
            scenario=constants_inputs["BREEDING_STRATEGY"],  # tries to reduce breeding
        )

        # MEAT AND DAIRY from breeding reduction strategy

        # for first round (zero feed available to animals)
        (
            zero_feed_used,
            meat_dictionary_round1,
            time_consts,
            constants_out,
        ) = self.init_meat_and_dairy_and_feed_from_breeding(
            constants_inputs,
            feed_meat_object_round1,
            feed_and_biofuels_class,
            meat_and_dairy,
            constants_out,
            time_consts,
        )

        assert (
            zero_feed_used.all_equals_zero()
        ), "Error: first round of optimization has no feed used (just maximize to humans)"

        # FEED AND BIOFUELS from breeding reduction strategy

        feed_and_biofuels_class.nonhuman_consumption = zero_biofuels + zero_feed_used
        PLOT_FEED = False

        if PLOT_FEED:
            zero_feed_used.in_units_percent_fed().plot("zero_feed_used")

        assert (
            zero_biofuels.all_equals_zero()
        ), "Error: first round of optimization has no biofuels used (just maximize to humans)"

        # Update feed_and_biofuels_class object with zero of either every month
        feed_and_biofuels_class.biofuel_demand = zero_biofuels

        # Update time_consts dictionary with zero feed or biofuels every month
        time_consts["feed"] = zero_feed_used
        time_consts["biofuel"] = zero_biofuels
        time_consts["nonhuman_consumption"] = zero_feed_used + zero_biofuels

        # Return tuple containing constants_out, time_consts, and feed_and_biofuels_class
        return (
            constants_out,
            time_consts,
            feed_and_biofuels_class,
            meat_dictionary_round1,
            feed_demand,  # the actual demand asked for by the user
            biofuels_demand,  # the actual demand asked for by the user
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
        constants_out["ADD_MEAT"] = constants_inputs["ADD_MEAT"]
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
        constants_out["SEAWEED_WASTE_RETAIL"] = seaweed.SEAWEED_WASTE_RETAIL
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
            "MAX_SEAWEED_AS_PERCENT_KCALS_HUMANS"
        ] = seaweed.MAX_SEAWEED_AS_PERCENT_KCALS_HUMANS

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
        if (
            constants_inputs["ADD_OUTDOOR_GROWING"]
            or constants_inputs["ADD_GREENHOUSES"]
        ):
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
        constants_out["DELAY"] = constants_inputs["DELAY"]
        constants_out["CROP_WASTE_RETAIL"] = outdoor_crops.CROP_WASTE_RETAIL

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

        constants_out["STORED_FOOD_WASTE_RETAIL"] = constants_inputs["WASTE_RETAIL"]

        # return the updated constants_out dictionary and the stored_food object
        return constants_out, stored_food

    def init_fish_params(self, time_consts, constants_inputs, time_consts_inputs):
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

        seafood.set_seafood_production(time_consts_inputs)
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

        time_consts["greenhouse_crops"] = Food(
            kcals=np.multiply(greenhouse_kcals_per_ha, greenhouse_area),
            fat=np.multiply(greenhouse_fat_per_ha, greenhouse_area),
            protein=np.multiply(greenhouse_protein_per_ha, greenhouse_area),
            kcals_units="billion kcals each month",
            fat_units="thousand tons each month",
            protein_units="thousand tons each month",
        )

        # Update the outdoor crops instance with the post-waste crops food produced
        outdoor_crops.set_crop_production_minus_greenhouse_area(
            constants_inputs, greenhouses.greenhouse_fraction_area
        )

        # Update the time constants dictionary with the calculated values
        time_consts["outdoor_crops"] = outdoor_crops

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

        # Add the cellulosic production to the time_consts dictionary
        time_consts["cellulosic_sugar"] = cellulosic_sugar.production
        constants_out["CELL_SUGAR_RETAIL_WASTE"] = cellulosic_sugar.SUGAR_WASTE_RETAIL
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

        constants_out[
            "SCP_KCALS_TO_FAT_CONVERSION"
        ] = methane_scp.SCP_KCALS_TO_FAT_CONVERSION
        constants_out[
            "SCP_KCALS_TO_PROTEIN_CONVERSION"
        ] = methane_scp.SCP_KCALS_TO_PROTEIN_CONVERSION

        # Add the methane_scp object to the time_consts dictionary.
        time_consts["methane_scp"] = methane_scp.production
        constants_out["SCP_RETAIL_WASTE"] = methane_scp.SCP_WASTE_RETAIL

        return constants_out, time_consts, methane_scp

    def init_meat_and_dairy_and_feed_from_breeding(
        self,
        constants_inputs,
        feed_meat_object,
        feed_and_biofuels_class,
        meat_and_dairy,
        constants_out,
        time_consts,
    ):
        constants_out, time_consts = self.calculate_meat_from_feed_results(
            constants_out, time_consts, meat_and_dairy, feed_meat_object
        )

        dairy_population = feed_meat_object.get_total_dairy_cows()

        (
            constants_out,
            time_consts,
        ) = self.calculate_non_meat_and_dairy_from_feed_results(
            constants_inputs,
            constants_out,
            time_consts,
            dairy_population,
            meat_and_dairy,
        )

        feed_used = feed_and_biofuels_class.create_feed_food_from_kcals(
            feed_meat_object.feed_used
        )

        # only used for plotting
        animal_meat_dictionary = self.get_animal_meat_dictionary(
            feed_meat_object, meat_and_dairy
        )

        constants_out["MEAT_WASTE_RETAIL"] = meat_and_dairy.MEAT_WASTE_RETAIL

        return (
            feed_used,
            animal_meat_dictionary,
            time_consts,
            constants_out,
        )

    def get_animal_meat_dictionary(self, feed_meat_object, meat_and_dairy):
        # get the total slaughter by animal size from the all_animals list of animal objects
        animal_meat_dictionary = {}
        for animal in feed_meat_object.all_animals:
            if animal.animal_size == "small":
                this_animal_meat = (
                    meat_and_dairy.get_max_slaughter_monthly_after_distribution_waste(
                        small_animals_culled=np.array(animal.slaughter),
                        medium_animals_culled=np.zeros_like(animal.slaughter),
                        large_animals_culled=np.zeros_like(animal.slaughter),
                    )
                )
            elif animal.animal_size == "medium":
                this_animal_meat = (
                    meat_and_dairy.get_max_slaughter_monthly_after_distribution_waste(
                        small_animals_culled=np.zeros_like(animal.slaughter),
                        medium_animals_culled=np.array(animal.slaughter),
                        large_animals_culled=np.zeros_like(animal.slaughter),
                    )
                )
            elif animal.animal_size == "large":
                this_animal_meat = (
                    meat_and_dairy.get_max_slaughter_monthly_after_distribution_waste(
                        small_animals_culled=np.zeros_like(animal.slaughter),
                        medium_animals_culled=np.zeros_like(animal.slaughter),
                        large_animals_culled=np.array(animal.slaughter),
                    )
                )

            animal_meat_dictionary[
                animal.animal_type
            ] = this_animal_meat.in_units_kcals_equivalent().kcals
            animal_meat_dictionary[
                animal.animal_type + "_population"
            ] = animal.population

        return animal_meat_dictionary

    # THIS MEAT CONSUMPTION PART IS KINDA TRICKY CONCEPTUALLY:
    #   I set two constraints on the meat consumed in the optimizer:
    #     1. culled meat consumed in sum total cannot be greater than the sum total of meat produced
    #     2. culled meat consumed each month cannot be greater than the sum of total meat produced in prior months
    # This allows us to store meat for later consumption, but we can never eat more meat in any month than has
    # been produced thus far.

    # To implement the above, first we take the sum total and set it to "culled meat", a single food constant
    def calculate_meat_from_feed_results(
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

        # Second we simply determine the meat slaughtered in each month
        each_month_meat_slaughtered = (
            meat_and_dairy.get_max_slaughter_monthly_after_distribution_waste(
                small_animals_culled=animals_killed_for_meat_small,
                medium_animals_culled=animals_killed_for_meat_medium,
                large_animals_culled=animals_killed_for_meat_large,
            )
        )
        PLOT_MEAT_SLAUGHTERED = False
        if PLOT_MEAT_SLAUGHTERED:
            each_month_meat_slaughtered.plot("Meat this round")

        # Finally we take the running sum of meat slaughtered over time and set it to the monthly time constant
        # called "max_consumed_culled_kcals"
        # NOTE: The second round may overwrite this value once the meat is redistributed over time (which is to ensure
        # round 2 strictly has more kcals available, as it is required for optimization contstraints to always to be
        #  satisfied in round 2)
        time_consts[
            "max_consumed_culled_kcals_each_month"
        ] = each_month_meat_slaughtered.get_running_total_nutrients_sum().kcals

        time_consts["each_month_meat_slaughtered"] = each_month_meat_slaughtered

        # Calculate the amount of culled meat and update constants_out dictionary
        (
            constants_out["meat_summed_consumption"],
            constants_out["MEAT_FRACTION_FAT"],
            constants_out["MEAT_FRACTION_PROTEIN"],
        ) = meat_and_dairy.calculate_meat_after_distribution_waste(
            np.sum(animals_killed_for_meat_small),
            np.sum(animals_killed_for_meat_medium),
            np.sum(animals_killed_for_meat_large),
        )

        return constants_out, time_consts

    def calculate_non_meat_and_dairy_from_feed_results(
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
            milk_kcals,
            milk_fat,
            milk_protein,
        ) = meat_and_dairy.get_milk_produced_postwaste(monthly_milk_tons)

        # Set grazing milk constants in time_consts
        if constants_inputs["ADD_MILK"]:
            time_consts["milk_kcals"] = milk_kcals
            time_consts["milk_fat"] = milk_fat
            time_consts["milk_protein"] = milk_protein
        else:
            time_consts["milk_kcals"] = np.zeros(len(milk_kcals))
            time_consts["milk_fat"] = np.zeros(len(milk_fat))
            time_consts["milk_protein"] = np.zeros(len(milk_protein))
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

        return constants_out, time_consts

    # ################ SECOND ROUND: AFTER FIRST OPTIMIZATION ##########################
    def compute_parameters_second_round(
        self,
        constants_inputs,
        constants_out,
        time_consts_round1,
        interpreted_results_round1,
    ):
        """
        Compute the parameters for the second round of optimizations, where we now know the amount of feed
        available for animals after humans have used all they need for their minimum nutritional needs.

        """
        time_consts_round2 = copy.deepcopy(time_consts_round1)
        feed_and_biofuels_class = FeedAndBiofuels(constants_inputs)
        (
            biofuels_demand,
            feed_demand,
        ) = feed_and_biofuels_class.get_biofuels_and_feed_from_delayed_shutoff(
            constants_inputs
        )

        meat_and_dairy = MeatAndDairy(constants_inputs)
        grasses_for_animals = meat_and_dairy.human_inedible_feed

        feed_meat_object_second_round = CalculateFeedAndMeat(
            country_code=constants_inputs["COUNTRY_CODE"],
            available_feed=feed_demand,
            available_grass=grasses_for_animals,
            scenario=constants_inputs[
                "BREEDING_STRATEGY"
            ],  # tries to reduce breeding or keep as baseline
        )

        (
            max_feed_that_could_be_used_second_round,
            meat_dictionary_round2,  # if all feed needs were satisfied before feed shutoff
            time_consts_round2,
            constants_out,
        ) = self.init_meat_and_dairy_and_feed_from_breeding(
            constants_inputs,
            feed_meat_object_second_round,
            feed_and_biofuels_class,
            meat_and_dairy,
            constants_out,
            time_consts_round2,
        )

        # Sometimes, the first round has a more efficient slaughtering process that occurs earlier than second round
        # This mostly happens as the animals are starving and populations of animals are altering.
        # As a result, there is more meat slaughtered earlier in the first round with no feed.
        # This function moves any such increase in meat to earlier in the second round, so that the second round
        # Strictly, always, has equal or more meat available, as is required by the second round optimization
        # TODO: get  working with protein and fat
        before_readjust_meat_round2 = copy.deepcopy(
            time_consts_round2["each_month_meat_slaughtered"].kcals
        )

        time_consts_round2[
            "each_month_meat_slaughtered"
        ].kcals = self.get_second_round_kcals_with_redistributed_meat(
            time_consts_round1["each_month_meat_slaughtered"].kcals,
            time_consts_round2["each_month_meat_slaughtered"].kcals,
        )

        if time_consts_round2["each_month_meat_slaughtered"].kcals is None:
            # this indicates the meat produced is in fact lower when feed is applied.
            # Therefore, we will abort the second round and simply return the results from the first round with no feed
            return None, None, None, None, None

        assert np.abs(
            before_readjust_meat_round2.sum()
            - time_consts_round2["each_month_meat_slaughtered"].kcals.sum()
        ) <= 0.001 or (
            before_readjust_meat_round2.sum()
            < time_consts_round1["each_month_meat_slaughtered"].kcals.sum()
        ), (
            "ERROR: meat slaughter timing readjustment has changed the total kcals, even though there was less meat "
            "in round 2 as is normally the case!"
        )

        # Finally we take the running sum of meat slaughtered over time and set it to the monthly time constant
        # called "max_consumed_culled_kcals"
        time_consts_round2["max_consumed_culled_kcals_each_month"] = (
            time_consts_round2["each_month_meat_slaughtered"]
            .get_running_total_nutrients_sum()
            .kcals
        )

        time_consts_round2[
            "max_feed_that_could_be_used"
        ] = max_feed_that_could_be_used_second_round

        time_consts_round2["max_biofuel_that_could_be_used"] = biofuels_demand

        # first round results had no feed or biofuels!
        assert interpreted_results_round1.cell_sugar_biofuels_kcals_equivalent.all_equals_zero(
            rounding_decimals=6
        )
        assert interpreted_results_round1.outdoor_crops_biofuels_kcals_equivalent.all_equals_zero(
            rounding_decimals=6
        )
        assert interpreted_results_round1.scp_biofuels_kcals_equivalent.all_equals_zero(
            rounding_decimals=6
        )
        assert interpreted_results_round1.seaweed_biofuels_kcals_equivalent.all_equals_zero(
            rounding_decimals=6
        )
        assert interpreted_results_round1.stored_food_biofuels_kcals_equivalent.all_equals_zero(
            rounding_decimals=6
        )
        assert (
            interpreted_results_round1.cell_sugar_feed_kcals_equivalent.all_equals_zero(
                rounding_decimals=6
            )
        )
        assert interpreted_results_round1.outdoor_crops_feed_kcals_equivalent.all_equals_zero(
            rounding_decimals=6
        )
        assert interpreted_results_round1.scp_feed_kcals_equivalent.all_equals_zero(
            rounding_decimals=6
        )
        assert interpreted_results_round1.seaweed_feed_kcals_equivalent.all_equals_zero(
            rounding_decimals=6
        )
        assert interpreted_results_round1.stored_food_feed_kcals_equivalent.all_equals_zero(
            rounding_decimals=6
        )
        min_human_food_consumption = self.calculate_human_consumption_for_min_needs(
            constants_inputs, interpreted_results_round1
        )
        PRINT_MINIMUM_NEEDS_FOOD_FOR_HUMANS = False
        if PRINT_MINIMUM_NEEDS_FOOD_FOR_HUMANS:
            print("")
            print("")
            print("MINIMUM HUMAN NEEDS PRINTOUT")
            print("")
            print("")
            for food_name, food in min_human_food_consumption.items():
                print("food_name,food")
                print(food_name)
                print(food)
            print("")
            print("")
            print("END MINIMUM HUMAN NEEDS PRINTOUT")
            print("")
            print("")
        return (
            constants_out,
            time_consts_round2,
            feed_and_biofuels_class,
            meat_dictionary_round2,
            min_human_food_consumption,
        )

    def calculate_human_consumption_for_min_needs(
        self, constants_inputs, interpreted_results_round1
    ):
        """
        We run through each month and determine the amount consumed each month of all foods.
        However, any human consumption which exceeds the starvation percentage is ignored.
        To determine when to start ignoring human consumption, we loop through the different foods
        in the following order of priority for humans to consume:
          First fish, then meat, then dairy, then greenhouse crops, then outdoor crops, then stored food,
          then scp, then cs, then seaweed.

        NOTE: We only use variables set here in the optimizer that are NOT  greenhouses or dairy or fish, because
        greenhouses and dairy and fish are not actually added as variables in the model (they are added as monthly
        constants to sum of human consumption) and they cannot be optimized.
        Furthermore, these foods always go to humans anyway.
        We only add these variables for the purposes of validation in the case
        that they sum up to human caloric minimum needs.
        """

        # We need to determine the limit of minimum human needs, so the rest is available for feed and biofuel.
        # This is equal to calories consumed by the percent of humans fed
        #   (which is the minimum humans fed of any month).
        # The next round of optimization, we will then have the food humans don't eat be fed to animals.
        # This in turn increases meat and dairy to humans. However, the feed used by animals will no longer
        # go to humans.
        MINIMUM_PERCENT_FED_BEFORE_NONHUMAN_CONSUMPTION_ALLOWED = constants_inputs[
            "MINIMUM_PERCENT_FED_BEFORE_NONHUMAN_CONSUMPTION_ALLOWED"
        ]
        fraction_to_feed_people_first = (
            MINIMUM_PERCENT_FED_BEFORE_NONHUMAN_CONSUMPTION_ALLOWED / 100
        )
        if (
            interpreted_results_round1.percent_people_fed
            > MINIMUM_PERCENT_FED_BEFORE_NONHUMAN_CONSUMPTION_ALLOWED
        ):
            kcals_daily_maximum = (
                constants_inputs["NUTRITION"]["KCALS_DAILY"]
                * fraction_to_feed_people_first
            )
        else:
            kcals_daily_maximum = constants_inputs["NUTRITION"]["KCALS_DAILY"] * (
                interpreted_results_round1.percent_people_fed / 100
            )

        # As a Food object with nutrients:
        food_daily_maximum = Food(
            kcals=kcals_daily_maximum,
            fat=kcals_daily_maximum,
            protein=kcals_daily_maximum,
            kcals_units="kcals per person per day",
            fat_units="effective kcals per person per day",
            protein_units="effective kcals per person per day",
        )

        # Initialize arrays to store the monthly consumption for each type of food
        fish_consumption = []
        meat_consumption = []
        dairy_consumption = []
        greenhouse_consumption = []
        outdoor_crops_consumption = []
        stored_food_consumption = []
        scp_consumption = []
        cs_consumption = []
        seaweed_consumption = []

        # TODO: make this function work with fat and protein minimums...
        #       In that case, we would need to consider the amount of food needed to meet human minimum needs, even if
        #       kcals were more than 2100 per day, if fat or protein were still below the minimum.
        for month_index in range(0, constants_inputs["NMONTHS"]):
            remaining_kcals = food_daily_maximum.kcals

            # Function to calculate consumption for each food type
            def consume(food_kcals):
                nonlocal remaining_kcals
                consumed = min(food_kcals, remaining_kcals)
                remaining_kcals -= consumed
                return consumed

            # Calculate consumption for each food type following the order of preference
            fish_consumption.append(
                consume(
                    interpreted_results_round1.fish_kcals_equivalent[month_index].kcals
                )
            )
            meat_consumption.append(
                consume(
                    interpreted_results_round1.meat_kcals_equivalent[month_index].kcals
                )
            )
            dairy_consumption.append(
                consume(
                    interpreted_results_round1.milk_kcals_equivalent[month_index].kcals
                )
            )
            greenhouse_consumption.append(
                consume(
                    interpreted_results_round1.greenhouse_kcals_equivalent[
                        month_index
                    ].kcals
                )
            )
            outdoor_crops_consumption.append(
                consume(
                    interpreted_results_round1.immediate_outdoor_crops_kcals_equivalent[
                        month_index
                    ].kcals
                    + interpreted_results_round1.new_stored_outdoor_crops_kcals_equivalent[
                        month_index
                    ].kcals
                )
            )
            stored_food_consumption.append(
                consume(
                    interpreted_results_round1.stored_food_kcals_equivalent[
                        month_index
                    ].kcals
                )
            )
            scp_consumption.append(
                consume(
                    interpreted_results_round1.scp_kcals_equivalent[month_index].kcals
                )
            )
            cs_consumption.append(
                consume(
                    interpreted_results_round1.cell_sugar_kcals_equivalent[
                        month_index
                    ].kcals
                )
            )
            seaweed_consumption.append(
                consume(
                    interpreted_results_round1.seaweed_kcals_equivalent[
                        month_index
                    ].kcals
                )
            )

        # Convert lists to numpy arrays and create the dictionary
        human_food_consumption = {
            "fish": Food(
                kcals=fish_consumption,
                fat=np.zeros_like(fish_consumption),
                protein=np.zeros_like(fish_consumption),
                kcals_units="kcals per person per day",
                fat_units="effective kcals per person per day",
                protein_units="effective kcals per person per day",
            ),
            "meat": Food(
                kcals=meat_consumption,
                fat=np.zeros_like(meat_consumption),
                protein=np.zeros_like(meat_consumption),
                kcals_units="kcals per person per day",
                fat_units="effective kcals per person per day",
                protein_units="effective kcals per person per day",
            ),
            "dairy": Food(
                kcals=dairy_consumption,
                fat=np.zeros_like(dairy_consumption),
                protein=np.zeros_like(dairy_consumption),
                kcals_units="kcals per person per day",
                fat_units="effective kcals per person per day",
                protein_units="effective kcals per person per day",
            ),
            "greenhouse": Food(
                kcals=greenhouse_consumption,
                fat=np.zeros_like(greenhouse_consumption),
                protein=np.zeros_like(greenhouse_consumption),
                kcals_units="kcals per person per day",
                fat_units="effective kcals per person per day",
                protein_units="effective kcals per person per day",
            ),
            "outdoor_crops": Food(
                kcals=outdoor_crops_consumption,
                fat=np.zeros_like(outdoor_crops_consumption),
                protein=np.zeros_like(outdoor_crops_consumption),
                kcals_units="kcals per person per day",
                fat_units="effective kcals per person per day",
                protein_units="effective kcals per person per day",
            ),
            "stored_food": Food(
                kcals=stored_food_consumption,
                fat=np.zeros_like(stored_food_consumption),
                protein=np.zeros_like(stored_food_consumption),
                kcals_units="kcals per person per day",
                fat_units="effective kcals per person per day",
                protein_units="effective kcals per person per day",
            ),
            "methane_scp": Food(
                kcals=scp_consumption,
                fat=np.zeros_like(scp_consumption),
                protein=np.zeros_like(scp_consumption),
                kcals_units="kcals per person per day",
                fat_units="effective kcals per person per day",
                protein_units="effective kcals per person per day",
            ),
            "cellulosic_sugar": Food(
                kcals=cs_consumption,
                fat=np.zeros_like(cs_consumption),
                protein=np.zeros_like(cs_consumption),
                kcals_units="kcals per person per day",
                fat_units="effective kcals per person per day",
                protein_units="effective kcals per person per day",
            ),
            "seaweed": Food(
                kcals=seaweed_consumption,
                fat=np.zeros_like(seaweed_consumption),
                protein=np.zeros_like(seaweed_consumption),
                kcals_units="kcals per person per day",
                fat_units="effective kcals per person per day",
                protein_units="effective kcals per person per day",
            ),
        }

        self.assert_consumption_within_limits(
            human_food_consumption, kcals_daily_maximum
        )

        Validator.verify_minimum_food_consumption_sum_round2(
            interpreted_results_round1, human_food_consumption
        )

        Validator.verify_food_usage_priorities_round2(
            interpreted_results_round1, human_food_consumption
        )

        return human_food_consumption

    def assert_consumption_within_limits(
        self, human_food_consumption, kcals_daily_maximum
    ):
        """
        Asserts that each Food object in the human_food_consumption dictionary is less than
        or equal to kcals_daily_maximum for all months.
        """
        # Create a Food object representing the maximum daily kcals
        max_food_daily = Food(
            kcals=[kcals_daily_maximum]
            * len(
                human_food_consumption["fish"].kcals
            ),  # Assuming the same length for all food types
            fat=[kcals_daily_maximum] * len(human_food_consumption["fish"].kcals),
            protein=[kcals_daily_maximum] * len(human_food_consumption["fish"].kcals),
            kcals_units="kcals per person per day",
            fat_units="effective kcals per person per day",
            protein_units="effective kcals per person per day",
        )

        # Iterate over each food type and assert consumption is within limits
        for food_type, food_consumption in human_food_consumption.items():
            assert food_consumption.all_less_than_or_equal_to(
                max_food_daily
            ), f"Consumption of {food_type} exceeds maximum allowed in some months."

    # ################ THIRD ROUND: FINAL TO HUMANS CALCULATION ##########################
    def compute_parameters_third_round(
        self,
        constants_inputs,
        constants_out,
        time_consts_round1,
        interpreted_round2,
        feed_and_biofuels_class,
    ):
        # TODO: make this function work with fat and protein minimums...

        time_consts_round3 = copy.deepcopy(time_consts_round1)

        meat_and_dairy = MeatAndDairy(constants_inputs)
        feed_sum_billion_kcals = (
            interpreted_round2.feed_sum_kcals_equivalent.in_units_bil_kcals_thou_tons_thou_tons_per_month()
        )
        biofuel_sum_billion_kcals = (
            interpreted_round2.biofuels_sum_kcals_equivalent.in_units_bil_kcals_thou_tons_thou_tons_per_month()
        )

        grasses_for_animals = meat_and_dairy.human_inedible_feed
        feed_meat_object_third_round = CalculateFeedAndMeat(
            country_code=constants_inputs["COUNTRY_CODE"],
            available_feed=feed_sum_billion_kcals,
            available_grass=grasses_for_animals,
            scenario=constants_inputs["BREEDING_STRATEGY"],
        )

        # final answer as to meat produced from feed
        (
            feed_used_round3,
            meat_dictionary_round3,
            time_consts_round3,
            constants_out,
        ) = self.init_meat_and_dairy_and_feed_from_breeding(
            constants_inputs,
            feed_meat_object_third_round,
            feed_and_biofuels_class,
            meat_and_dairy,
            constants_out,
            time_consts_round3,
        )

        # Update feed_and_biofuels_class_round3 object with their values
        feed_and_biofuels_class.biofuel_demand = biofuel_sum_billion_kcals
        feed_and_biofuels_class.nonhuman_consumption = (
            feed_used_round3 + biofuel_sum_billion_kcals
        )
        # Update time_consts_round2 dictionary
        time_consts_round3["nonhuman_consumption"] = (
            feed_used_round3 + biofuel_sum_billion_kcals
        )
        time_consts_round3["feed"] = feed_used_round3
        time_consts_round3["biofuel"] = biofuel_sum_billion_kcals

        return (
            constants_out,
            time_consts_round3,
            feed_and_biofuels_class,
            meat_dictionary_round3,
        )
