"""
Convert optimizer output to numpy arrays in order to later interpret and validate them

Created on Tue Jul 22

@author: morgan
"""
import numpy as np
from src.food_system.food import Food
import pulp


class Extractor:
    def __init__(self, constants):
        """
        Initializes an instance of the Extractor class with the given constants.

        Args:
            constants (dict): A dictionary containing the constants used by the Extractor.

        Returns:
            None
        """
        self.constants = constants

    def extract_results(self, model, variables, time_consts):
        """
        Extracts the results from the model and stores them in the Extractor object.
        Args:
            model (pysd.PySD): the PySD model object
            variables (dict): a dictionary of model variables
            time_consts (dict): a dictionary of time constants
        Returns:
            Extractor: the Extractor object with the extracted results stored in its attributes
        """

        # extract the objective optimization results
        self.get_objective_optimization_results(model)

        # extract the nonhuman consumption time constant
        self.nonhuman_consumption = time_consts["nonhuman_consumption"]

        # extract stored food results in terms of people fed and raw tons
        (
            self.stored_food_to_humans,
            self.stored_food_feed,
            self.stored_food_biofuel,
        ) = self.extract_to_humans_feed_and_biofuel(
            variables["stored_food_to_humans"],
            variables["stored_food_feed"],
            variables["stored_food_biofuel"],
            1,
            self.constants["SF_FRACTION_FAT"],
            self.constants["SF_FRACTION_PROTEIN"],
            self.constants,
        )

        # extract numeric seaweed results in terms of people fed and raw tons wet
        (
            self.seaweed_to_humans,
            self.seaweed_feed,
            self.seaweed_biofuel,
        ) = self.extract_to_humans_feed_and_biofuel(
            variables["seaweed_to_humans"],
            variables["seaweed_feed"],
            variables["seaweed_biofuel"],
            self.constants["SEAWEED_KCALS"],
            self.constants["SEAWEED_FAT"],
            self.constants["SEAWEED_PROTEIN"],
            self.constants,
        )

        # extract single cell protein results in terms of people fed and raw tons
        (
            self.scp_to_humans,
            self.scp_feed,
            self.scp_biofuel,
        ) = self.extract_to_humans_feed_and_biofuel(
            variables["methane_scp_to_humans"],
            variables["methane_scp_feed"],
            variables["methane_scp_biofuel"],
            1,
            self.constants["SCP_KCALS_TO_FAT_CONVERSION"],
            self.constants["SCP_KCALS_TO_PROTEIN_CONVERSION"],
            self.constants,
        )

        # extract cellulosic sugar results in terms of people fed and raw tons
        (
            self.cell_sugar_to_humans,
            self.cell_sugar_feed,
            self.cell_sugar_biofuel,
        ) = self.extract_to_humans_feed_and_biofuel(
            variables["cellulosic_sugar_to_humans"],
            variables["cellulosic_sugar_feed"],
            variables["cellulosic_sugar_biofuel"],
            1,
            0,
            0,
            self.constants,
        )

        # extract fish results in terms of billions of people fed
        self.fish = time_consts["fish"].to_humans.in_units_billions_fed()

        # if no greenhouses, plot shows zero
        # extract greenhouse results in terms of people fed and raw tons
        self.greenhouse = self.get_greenhouse_results(
            time_consts["greenhouse_crops"],
        )
        # if no outdoor food, plot shows zero
        # extract outdoor crops results in terms of people fed and raw tons
        self.extract_outdoor_crops_results(
            variables["crops_food_to_humans"],
            variables["crops_food_to_humans_fat"],
            variables["crops_food_to_humans_protein"],
            variables["crops_food_biofuel"],
            variables["crops_food_biofuel_fat"],
            variables["crops_food_biofuel_protein"],
            variables["crops_food_feed"],
            variables["crops_food_feed_fat"],
            variables["crops_food_feed_protein"],
            time_consts["outdoor_crops"].production,
        )

        # if nonegg nonmilk meat isn't included, these results plot shows zero
        # extract meat and milk results in terms of people fed and raw tons
        self.extract_meat_milk_results(
            variables["meat_eaten"],
            time_consts["milk_kcals"],
            time_consts["milk_fat"],
            time_consts["milk_protein"],
        )

        return self

    # order the variables that occur mid-month into a list of numeric values
    def to_monthly_list(self, variables, conversion):
        """
        Converts a list of variables to a monthly list of values.
        Args:
            variables (list): A list of variables to be converted.
            conversion (float): A conversion factor to be applied to each variable.
        Returns:
            np.array: A numpy array of the converted monthly values.
        """
        variable_output = []

        # Check if the variable was not modeled
        if isinstance((variables[0]), int):
            return np.array([0] * len(variables))  # return initial value

        SHOW_OUTPUT = False
        if SHOW_OUTPUT:
            print("Monthly Output for " + str(variables[0]))

        # Loop through each month
        for month in range(0, self.constants["NMONTHS"]):
            val = variables[month]

            # Check if something went wrong and the variable was not added for a certain month
            assert not isinstance(type(val), int)

            # Append the converted variable value to the output list
            variable_output.append(val.varValue * conversion)

            if SHOW_OUTPUT:
                print(" Month " + str(month) + ": " + str(variable_output[month]))

        return np.array(variable_output)

    # order the variables that occur mid-month into a list of numeric values

    def to_monthly_list_outdoor_crops_kcals(
        self, crops_food_eaten, crops_kcals_produced, conversion
    ):
        """
        This function calculates the amount of outdoor crop production that is immediately eaten and the
        amount that is stored for later consumption. If more is eaten than produced, the difference is
        attributed to the eating of stored up crops.

        Args:
            - crops_food_eaten: list of the amount of crops eaten each month
            - crops_kcals_produced: list of the amount of crop production (kcals) each month
            - conversion: conversion factor from kcals to another unit of measurement

        Returns:
            - A list of two lists:
                - The first list contains the amount of outdoor crop production (converted to the specified
                unit of measurement) that is immediately eaten each month.
                - The second list contains the amount of outdoor crop production (converted to the specified
                unit of measurement) that is stored for later consumption each month.
        """

        immediately_eaten_output = []
        new_stored_eaten_output = []
        cf_produced_output = []
        for month in range(0, self.constants["NMONTHS"]):
            cf_produced = crops_kcals_produced[month]
            cf_produced_output.append(cf_produced)
            # print("")
            # print("cf_produced")
            # print(cf_produced)
            cf_eaten = crops_food_eaten[month].varValue
            # print("cf_eaten")
            # print(cf_eaten)

            if cf_produced <= cf_eaten:
                immediately_eaten = cf_produced
                new_stored_crops_eaten = cf_eaten - cf_produced
            else:
                immediately_eaten = cf_eaten
                new_stored_crops_eaten = 0
            # print("immediately_eaten")
            # print(immediately_eaten)
            # print("new_stored_crops_eaten")
            # print(new_stored_crops_eaten)
            immediately_eaten_output.append(immediately_eaten * conversion)
            new_stored_eaten_output.append(new_stored_crops_eaten * conversion)

        # import matplotlib.pyplot as plt

        # plt.figure()
        # plt.plot(self.outdoor_crops_to_humans.in_units_billions_fed().kcals)
        # plt.plot(immediately_eaten_output)
        # plt.plot(new_stored_eaten_output)
        # plt.show()

        return [immediately_eaten_output, new_stored_eaten_output]

    # if greenhouses aren't included, these results will be zero

    def get_greenhouse_results(
        self,
        greenhouse_crops,
    ):
        self.greenhouse_percent_fed = greenhouse_crops

        return self.greenhouse_percent_fed.in_units_billions_fed()

    def create_food_object_from_fat_protein_variables(
        self, production_kcals, production_fat, production_protein
    ):
        """
        This function creates a Food object from the given production_kcals, production_fat, and production_protein.
        Args:
            production_kcals (float): the amount of kcals produced
            production_fat (float): the amount of fat produced
            production_protein (float): the amount of protein produced
        Returns:
            Food: a Food object with kcals, fat, and protein attributes
        """
        # Convert production_kcals, production_fat, and production_protein to monthly lists
        # by dividing them by the corresponding monthly constants
        billions_fed_kcals = self.to_monthly_list(
            production_kcals,
            1 / self.constants["KCALS_MONTHLY"],
        )

        billions_fed_fat = self.to_monthly_list(
            production_fat,
            1 / self.constants["FAT_MONTHLY"] / 1e9,
        )

        billions_fed_protein = self.to_monthly_list(
            production_protein,
            1 / self.constants["PROTEIN_MONTHLY"] / 1e9,
        )

        # Create a Food object with the monthly lists and corresponding units
        return Food(
            kcals=billions_fed_kcals,
            fat=billions_fed_fat,
            protein=billions_fed_protein,
            kcals_units="billion people fed each month",
            fat_units="billion people fed each month",
            protein_units="billion people fed each month",
        )

    def extract_generic_results(
        self, production_kcals, ratio_kcals, ratio_fat, ratio_protein, constants
    ):
        """
        Extracts generic results from production_kcals, ratio_kcals, ratio_fat, ratio_protein, and constants.
        Args:
            production_kcals (float): total production kcals
            ratio_kcals (float): ratio of kcals to production kcals
            ratio_fat (float): ratio of fat to production kcals
            ratio_protein (float): ratio of protein to production kcals
            constants (dict): dictionary of constants used in the calculations
        Returns:
            Food: a Food object containing the extracted results
        """
        # Convert production_kcals, ratio_kcals, ratio_fat, and ratio_protein to monthly lists
        # We would eventually like to do this unit conversion within the UnitConversions class, but we ran into a complication
        # where we're going from percent fed monthly to fat and protein is tricky
        billions_fed_kcals = self.to_monthly_list(
            production_kcals,
            ratio_kcals / self.constants["KCALS_MONTHLY"],
        )

        billions_fed_fat = self.to_monthly_list(
            production_kcals,
            ratio_fat / self.constants["FAT_MONTHLY"] / 1e9,
        )

        billions_fed_protein = self.to_monthly_list(
            production_kcals,
            ratio_protein / self.constants["PROTEIN_MONTHLY"] / 1e9,
        )

        # Return a Food object containing the extracted results
        return Food(
            kcals=billions_fed_kcals,
            fat=billions_fed_fat,
            protein=billions_fed_protein,
            kcals_units="billion people fed each month",
            fat_units="billion people fed each month",
            protein_units="billion people fed each month",
        )

    def extract_outdoor_crops_results(
        self,
        crops_food_to_humans,
        crops_food_to_humans_fat,
        crops_food_to_humans_protein,
        crops_food_biofuel,
        crops_food_biofuel_fat,
        crops_food_biofuel_protein,
        crops_food_feed,
        crops_food_feed_fat,
        crops_food_feed_protein,
        outdoor_crops_production,
    ):
        """
        Extracts results for outdoor crops and assigns them to the corresponding food objects.
        Calculates outdoor crop production for humans and assigns the values to the corresponding food object.
        Validates if immediate and new stored sources add up correctly.
        Calculates and assigns new stored outdoor crops values.
        Calculates and assigns immediate outdoor crops values.
        Validates if the total outdoor growing production has not changed.

        Returns:
            None

        """
        if (
            not isinstance(crops_food_to_humans[0], pulp.pulp.LpVariable)
            and sum(crops_food_to_humans) == 0
        ):
            # if ADD_OUTDOOR_CROPS is false, handle this edgecase
            self.outdoor_crops_to_humans = Food(
                kcals=np.zeros_like(crops_food_to_humans),
                fat=np.zeros_like(crops_food_to_humans),
                protein=np.zeros_like(crops_food_to_humans),
                kcals_units="billion people fed each month",
                fat_units="billion people fed each month",
                protein_units="billion people fed each month",
            )
        else:
            # create the food object for to_humans outdoor crops
            self.outdoor_crops_to_humans = (
                self.create_food_object_from_fat_protein_variables(
                    crops_food_to_humans,
                    crops_food_to_humans_fat,
                    crops_food_to_humans_protein,
                )
            )

        # create the food object for biofuel outdoor crops
        self.outdoor_crops_biofuel = self.create_food_object_from_fat_protein_variables(
            crops_food_biofuel,
            crops_food_biofuel_fat,
            crops_food_biofuel_protein,
        )

        # create the food object for feed outdoor crops
        self.outdoor_crops_feed = self.create_food_object_from_fat_protein_variables(
            crops_food_feed,
            crops_food_feed_fat,
            crops_food_feed_protein,
        )

        # Calculate outdoor crop production for humans
        to_humans_outdoor_crop_production = np.subtract(
            np.subtract(
                outdoor_crops_production.kcals,
                self.outdoor_crops_feed.kcals,
            ),
            self.outdoor_crops_biofuel.kcals,
        )

        if (
            not isinstance(crops_food_to_humans[0], pulp.pulp.LpVariable)
            and sum(crops_food_to_humans) == 0
        ):
            # if ADD_OUTDOOR_CROPS is false, handle this edgecase
            self.outdoor_crops_to_humans = Food(
                kcals=np.zeros_like(crops_food_to_humans),
                fat=np.zeros_like(crops_food_to_humans),
                protein=np.zeros_like(crops_food_to_humans),
                kcals_units="billion people fed each month",
                fat_units="billion people fed each month",
                protein_units="billion people fed each month",
            )
        if (
            not isinstance(crops_food_to_humans[0], pulp.pulp.LpVariable)
            and sum(crops_food_to_humans) == 0
            and np.sum(to_humans_outdoor_crop_production) == 0
        ):
            billions_fed_immediate_outdoor_crops_kcals = np.zeros_like(
                crops_food_to_humans
            )
            billions_fed_new_stored_outdoor_crops_kcals = np.zeros_like(
                crops_food_to_humans
            )
        else:
            # Calculate the amount of outdoor crops that can be fed immediately and the amount that needs to be stored
            [
                billions_fed_immediate_outdoor_crops_kcals,
                billions_fed_new_stored_outdoor_crops_kcals,
            ] = self.calculate_outdoor_crops_kcals(
                crops_food_to_humans, to_humans_outdoor_crop_production
            )

        # Validate if immediate and new stored sources add up correctly
        self.validate_sources_add_up(
            billions_fed_immediate_outdoor_crops_kcals,
            billions_fed_new_stored_outdoor_crops_kcals,
        )

        # Calculate and assign new stored outdoor crops values
        self.set_new_stored_outdoor_crops_values(
            billions_fed_new_stored_outdoor_crops_kcals
        )

        # Calculate and assign immediate outdoor crops values
        self.set_immediate_outdoor_crops_values(
            billions_fed_immediate_outdoor_crops_kcals
        )

        # Validate if the total outdoor growing production has not changed
        self.validate_outdoor_growing_production()

    def calculate_outdoor_crops_kcals(
        self, crops_food_to_humans, to_humans_outdoor_crop_production
    ):
        return self.to_monthly_list_outdoor_crops_kcals(
            crops_food_to_humans,
            to_humans_outdoor_crop_production,
            1 / self.constants["KCALS_MONTHLY"],
        )

    def validate_sources_add_up(
        self,
        billions_fed_immediate_outdoor_crops_kcals,
        billions_fed_new_stored_outdoor_crops_kcals,
    ):
        """
        Validates that the sum of immediate and new stored sources of outdoor crops for humans
        matches the input of outdoor crop for humans.

        Args:
            billions_fed_immediate_outdoor_crops_kcals (list): A list of billions of kcals fed
                from immediate outdoor crops to humans.
            billions_fed_new_stored_outdoor_crops_kcals (list): A list of billions of kcals fed
                from new stored outdoor crops to humans.

        Returns:
            None

        Example:
            >>> extractor = Extractor()
            >>> extractor.outdoor_crops_to_humans.kcals = [1, 2, 3]
            >>> extractor.validate_sources_add_up([0.5, 1, 1.5], [0.5, 1, 1.5])
            None

        Raises:
            AssertionError: If the sum of immediate and new stored sources of outdoor crops for
                humans does not match the input of outdoor crop for humans.
        """
        difference = (
            np.array(billions_fed_immediate_outdoor_crops_kcals)
            + np.array(billions_fed_new_stored_outdoor_crops_kcals)
            - np.array(self.outdoor_crops_to_humans.kcals)
        )
        for element in difference:
            assert np.isclose(
                element, 0, atol=1e-3
            ), """ERROR: Immediate and new stored sources do not add up to the input of outdoor crop for humans"""

    def set_new_stored_outdoor_crops_values(
        self, billions_fed_new_stored_outdoor_crops_kcals
    ):
        """
        Sets the values of new_stored_outdoor_crops attribute of the Extractor class with the given billions_fed_new_stored_outdoor_crops_kcals.
        Args:
            self (Extractor): An instance of the Extractor class.
            billions_fed_new_stored_outdoor_crops_kcals (list): A list of kcals in billions fed to new stored outdoor crops each month.
        Returns:
            None
        """
        # Create a new Food object with the given kcals and zero fat and protein values
        self.new_stored_outdoor_crops = Food(
            kcals=np.array(billions_fed_new_stored_outdoor_crops_kcals),
            fat=np.zeros(len(billions_fed_new_stored_outdoor_crops_kcals)),
            protein=np.zeros(len(billions_fed_new_stored_outdoor_crops_kcals)),
            kcals_units="billion people fed each month",
            fat_units="billion people fed each month",
            protein_units="billion people fed each month",
        )

    def set_immediate_outdoor_crops_values(
        self, billions_fed_immediate_outdoor_crops_kcals
    ):
        """
        Sets the values of immediate outdoor crops in the Extractor object.
        Args:
            self (Extractor): The Extractor object.
            billions_fed_immediate_outdoor_crops_kcals (list): A list of kcals fed to billions of people each month.
        Returns:
            None
        """
        # Create a Food object with kcals, fat, and protein values set to 0.
        # The length of the arrays is the same as the length of the input list.
        self.immediate_outdoor_crops = Food(
            kcals=np.array(billions_fed_immediate_outdoor_crops_kcals),
            fat=np.zeros(len(billions_fed_immediate_outdoor_crops_kcals)),
            protein=np.zeros(len(billions_fed_immediate_outdoor_crops_kcals)),
            kcals_units="billion people fed each month",
            fat_units="billion people fed each month",
            protein_units="billion people fed each month",
        )

    def validate_outdoor_growing_production(self):
        """
        Validates the outdoor growing production by checking if the difference between the outdoor crops to humans and the
        sum of immediate outdoor crops and new stored outdoor crops is equal to zero.
        Args:
            self (Extractor): An instance of the Extractor class.
        Returns:
            None
        """
        # Calculate the difference between outdoor crops to humans and the sum of
        # immediate outdoor crops and new stored outdoor crops
        difference = self.outdoor_crops_to_humans - (
            self.immediate_outdoor_crops + self.new_stored_outdoor_crops
        )
        # Assert that the difference is equal to zero
        assert difference.get_rounded_to_decimal(3).all_equals_zero()

    # if stored food isn't included, these results will be zero
    def extract_meat_milk_results(
        self,
        meat_eaten,
        milk_kcals,
        milk_fat,
        milk_protein,
    ):
        """
        Extracts the results of meat and milk production from various sources and calculates the amount of food
        produced in billions of people fed each month.

        Args:
            meat_eaten (list): List of the amount of culled meat eaten in kg per year
            milk_kcals (list): List of the amount of grazing milk produced in kcal per year
            milk_fat (list): List of the amount of grazing milk produced in fat per year
            milk_protein (list): List of the amount of grazing milk produced in protein per year

        Returns:
            None

        Example:
            >>>
            >>> extractor = Extractor()
            >>> extractor.extract_meat_milk_results(
            >>>     meat_eaten=[1000, 2000, 3000],
            >>>     milk_kcals=[1000, 2000, 3000],
            >>>     milk_fat=[100, 200, 300],
            >>>     milk_protein=[50, 100, 150],
            >>> )
        """

        # Calculate the amount of culled meat eaten in billions of people fed each month
        billions_fed_meat_kcals = self.to_monthly_list(
            meat_eaten,
            1 / self.constants["KCALS_MONTHLY"],
        )

        # Calculate the amount of culled meat grazing in billions of people fed each month
        billions_fed_meat_grazing_kcals = billions_fed_meat_kcals

        # Calculate the amount of fat in culled meat in billions of people fed each month
        billions_fed_meat_fat = self.to_monthly_list(
            meat_eaten,
            self.constants["MEAT_FRACTION_FAT"] / self.constants["FAT_MONTHLY"] / 1e9,
        )

        # Calculate the amount of protein in culled meat in billions of people fed each month
        billions_fed_meat_protein = self.to_monthly_list(
            meat_eaten,
            self.constants["MEAT_FRACTION_PROTEIN"]
            / self.constants["PROTEIN_MONTHLY"]
            / 1e9,
        )

        # Create a Food object for culled meat plus grazing cattle maintained
        self.meat = Food(
            kcals=billions_fed_meat_kcals,
            fat=billions_fed_meat_fat,
            protein=billions_fed_meat_protein,
            kcals_units="billion people fed each month",
            fat_units="billion people fed each month",
            protein_units="billion people fed each month",
        )

        # Calculate the amount of grazing milk in billions of people fed each month
        billions_fed_milk_kcals = np.array(milk_kcals) / self.constants["KCALS_MONTHLY"]

        # Calculate the amount of fat in grazing milk in billions of people fed each month
        billions_fed_milk_fat = np.array(milk_fat) / self.constants["FAT_MONTHLY"] / 1e9

        # Calculate the amount of protein in grazing milk in billions of people fed each month
        billions_fed_milk_protein = (
            np.array(milk_protein) / self.constants["PROTEIN_MONTHLY"] / 1e9
        )

        # Create a Food object for grazing milk
        self.milk = Food(
            kcals=billions_fed_milk_kcals,
            fat=billions_fed_milk_fat,
            protein=billions_fed_milk_protein,
            kcals_units="billion people fed each month",
            fat_units="billion people fed each month",
            protein_units="billion people fed each month",
        )

    def extract_to_humans_feed_and_biofuel(
        self,
        to_humans,
        feed,
        biofuel,
        kcals_ratio,
        fat_ratio,
        protein_ratio,
        constants,
    ):
        amount_to_humans = self.extract_generic_results(
            to_humans,
            kcals_ratio,
            fat_ratio,
            protein_ratio,
            constants,
        )

        amount_feed = self.extract_generic_results(
            feed,
            kcals_ratio,
            fat_ratio,
            protein_ratio,
            constants,
        )

        amount_biofuel = self.extract_generic_results(
            biofuel,
            kcals_ratio,
            fat_ratio,
            protein_ratio,
            constants,
        )

        return (amount_to_humans, amount_feed, amount_biofuel)

    # The optimizer will maximize minimum fat, calories, and protein over any month,
    # but it does not care which sources these come from. The point of this function
    # is to determine the probable contributions to excess calories used for feed and
    # biofuel from appropriate sources (unless this has been updated, it takes it
    # exclusively from outdoor growing and stored food).

    # there is also a constraint to make sure the sources which can be used for feed
    # are not exhausted, and the model will not be able to solve if the usage from
    # biofuels and feed are more than the available stored food and outdoor crop production.

    def get_objective_optimization_results(self, model):
        """
        This function extracts the optimization results for the objective function of the model.
        Args:
            self: instance of the Extractor class
            model: the optimization model to extract results from
        Returns:
            tuple: a tuple containing the optimization results for consumed_kcals, consumed_fat, and consumed_protein
        """

        # Initialize empty lists to store the optimization results
        consumed_kcals = []
        consumed_fat = []
        consumed_protein = []
        order_kcals = []
        order_fat = []
        order_protein = []

        # Loop through all variables in the model
        for var in model.variables():
            # Check if the variable is related to consumed kcals
            if "Humans_Fed_Kcals_" in var.name:
                # Append the optimization result to the consumed_kcals list
                consumed_kcals.append(var.value() / 100 * self.constants["POP"] / 1e9)
                # Extract the order of the variable and append it to the order_kcals list
                order_kcals.append(
                    int(var.name[len("Humans_Fed_Kcals_") :].split("_")[0])
                )

            # Check if the variable is related to consumed fat
            if "Humans_Fed_Fat_" in var.name:
                # Append the optimization result to the consumed_fat list
                consumed_fat.append(var.value() / 100 * self.constants["POP"] / 1e9)
                # Extract the order of the variable and append it to the order_fat list
                order_fat.append(int(var.name[len("Humans_Fed_Fat_") :].split("_")[0]))

            # Check if the variable is related to consumed protein
            if "Humans_Fed_Protein_" in var.name:
                # Append the optimization result to the consumed_protein list
                consumed_protein.append(var.value() / 100 * self.constants["POP"] / 1e9)
                # Extract the order of the variable and append it to the order_protein list
                order_protein.append(
                    int(var.name[len("Humans_Fed_Protein_") :].split("_")[0])
                )

        # Sort the lists based on the order of the variables
        zipped_lists = zip(order_kcals, consumed_kcals)
        sorted_zipped_lists = sorted(zipped_lists)
        consumed_kcals_optimizer = [element for _, element in sorted_zipped_lists]

        zipped_lists = zip(order_fat, consumed_fat)
        sorted_zipped_lists = sorted(zipped_lists)
        consumed_fat_optimizer = [element for _, element in sorted_zipped_lists]

        zipped_lists = zip(order_protein, consumed_protein)
        sorted_zipped_lists = sorted(zipped_lists)
        consumed_protein_optimizer = [element for _, element in sorted_zipped_lists]

        # Return the optimization results as a tuple
        return (
            consumed_kcals_optimizer,
            consumed_fat_optimizer,
            consumed_protein_optimizer,
        )
