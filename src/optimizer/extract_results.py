"""
Convert optimizer output to numpy arrays in order to later interpret and validate them

Created on Tue Jul 22

@author: morgan
"""
import numpy as np
from src.food_system.food import Food


class Extractor:
    def extract_results(file_path):
        """
        Extracts results from a file and returns them as a list of dictionaries.
        Args:
            file_path (str): The path to the file containing the results.
        Returns:
            list: A list of dictionaries containing the extracted results.
        """
        # Open the file in read mode
        with open(file_path, "r") as f:
            # Read the contents of the file
            contents = f.read()
            # Split the contents into lines
            lines = contents.split("\n")
            # Initialize an empty list to store the results
            results = []
            # Loop through each line in the file
            for line in lines:
                # Split the line into key-value pairs
                key_value_pairs = line.split(",")
                # Initialize an empty dictionary to store the key-value pairs
                result = {}
                # Loop through each key-value pair
                for key_value_pair in key_value_pairs:
                    # Split the key-value pair into key and value
                    key, value = key_value_pair.split(":")
                    # Add the key-value pair to the dictionary
                    result[key.strip()] = value.strip()
                # Add the dictionary to the list of results
                results.append(result)
        # Return the list of results
        return results

    def extract_results(self, model, variables, time_consts):
        """
        Extracts various results from the model and stores them in the object.

        Args:
            model (pandas.DataFrame): The model containing the simulation results.
            variables (dict): A dictionary containing the variables used in the simulation.
            time_consts (dict): A dictionary containing the time constants used in the simulation.

        Returns:
            self (object): The object with the extracted results.

        """

        # Extract the objective optimization results from the model
        self.get_objective_optimization_results(model)

        self.nonhuman_consumption = time_consts["nonhuman_consumption"]

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

        # extract numeric seaweed results in terms of people fed and raw
        # tons wet

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

        self.fish = time_consts["fish"].to_humans.in_units_billions_fed()

        # if no greenhouses, plot shows zero
        self.greenhouse = self.get_greenhouse_results(
            time_consts["greenhouse_kcals_per_ha"],
            time_consts["greenhouse_fat_per_ha"],
            time_consts["greenhouse_protein_per_ha"],
            time_consts["greenhouse_area"],
        )

        # Extract outdoor crops results
        # If no outdoor food, plot shows zero
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

        # Extract meat and milk results
        # If nonegg nonmilk meat isn't included, these results plot shows zero
        self.extract_meat_milk_results(
            variables["culled_meat_eaten"],
            time_consts["grazing_milk_kcals"],
            time_consts["grazing_milk_fat"],
            time_consts["grazing_milk_protein"],
            time_consts["cattle_grazing_maintained_kcals"],
            time_consts["cattle_grazing_maintained_fat"],
            time_consts["cattle_grazing_maintained_protein"],
            time_consts["grain_fed_meat_kcals"],
            time_consts["grain_fed_meat_fat"],
            time_consts["grain_fed_meat_protein"],
            time_consts["grain_fed_milk_kcals"],
            time_consts["grain_fed_milk_fat"],
            time_consts["grain_fed_milk_protein"],
        )

        # Store the excess feed
        self.excess_feed = time_consts["excess_feed"]

        return self

    # order the variables that occur mid-month into a list of numeric values
    def to_monthly_list(self, variables, conversion):
        """
        This function takes a list of variables and a conversion factor and returns a list of monthly values.
        Args:
            variables (list): A list of variables to be converted to monthly values.
            conversion (float): A conversion factor to be applied to each variable.

        Returns:
            np.array: A numpy array of monthly values.

        Raises:
            AssertionError: If something went wrong and the variable was not added for a certain month.

        """
        variable_output = []

        # if the variable was not modeled
        if isinstance((variables[0]), int):
            return np.array([0] * len(variables))  # return initial value

        SHOW_OUTPUT = False
        if SHOW_OUTPUT:
            print("Monthly Output for " + str(variables[0]))

        for month in range(0, self.constants["NMONTHS"]):
            val = variables[month]
            # if something went wrong and the variable was not added for a certain month
            assert not isinstance(type(val), int)

            # append the converted variable value to the output list
            variable_output.append(val.varValue * conversion)

            if SHOW_OUTPUT:
                print("    Month " + str(month) + ": " + str(variable_output[month]))

        return np.array(variable_output)

    def to_monthly_list_outdoor_crops_kcals(
        self, crops_food_eaten, crops_kcals_produced, conversion
    ):
        """
        This function takes the total outdoor crop production and limits it by the actual amount
        eaten by people reported by the optimizer. If more is eaten than produced, this difference
        is attributed to the eating of stored up crops. The amount of expected crops produced that
        month that were eaten is assigned to the "immediate" list. The amount eaten beyond the
        production that month is assigned to the new stored list.

        Args:
            self (object): The class object
            crops_food_eaten_no_relocation (list): The amount of crops eaten without relocation
            crops_food_eaten_relocated (list): The amount of crops eaten with relocation
            crops_kcals_produced (list): The amount of crops produced
            conversion (float): The conversion factor to convert the crops to kcals

        Returns:
            list: A list containing the amount of crops immediately eaten and the amount of
            crops stored and eaten later

        Note:
            The validator will check that the sum of immediate and new stored is the same as the
            total amount eaten.
        """

        immediately_eaten_output = []
        new_stored_eaten_output = []
        cf_produced_output = []
        for month in range(0, self.constants["NMONTHS"]):
            cf_produced = crops_kcals_produced[month]
            cf_produced_output.append(cf_produced)

            cf_eaten = crops_food_eaten[month].varValue

            if cf_produced <= cf_eaten:
                immediately_eaten = cf_produced
                new_stored_crops_eaten = cf_eaten - cf_produced
            else:
                immediately_eaten = cf_eaten
                new_stored_crops_eaten = 0

            immediately_eaten_output.append(immediately_eaten * conversion)
            new_stored_eaten_output.append(new_stored_crops_eaten * conversion)

        return [immediately_eaten_output, new_stored_eaten_output]

    # if greenhouses aren't included, these results will be zero

    def get_greenhouse_results(
        self,
        greenhouse_kcals_per_ha,
        greenhouse_fat_per_ha,
        greenhouse_protein_per_ha,
        greenhouse_area,
    ):
        self.greenhouse_percent_fed = Food(
            kcals=np.multiply(
                np.array(greenhouse_area), np.array(greenhouse_kcals_per_ha)
            ),
            fat=np.multiply(np.array(greenhouse_area), np.array(greenhouse_fat_per_ha)),
            protein=np.multiply(
                np.array(greenhouse_area), np.array(greenhouse_protein_per_ha)
            ),
            kcals_units="percent people fed each month",
            fat_units="percent people fed each month",
            protein_units="percent people fed each month",
        )

        return self.greenhouse_percent_fed.in_units_billions_fed()

    def create_food_object_from_fat_protein_variables(
        self, production_kcals, production_fat, production_protein
    ):
        # TODO: double check this math

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
        # we would eventually like to do this unit conversion within the UnitConversions class, but I
        # ran into a complication where we're going from percent fed monthly to fat and protein is tricky

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
        Calculates the results of outdoor crop production and consumption, and stores the results in the class instance.

        Args:
            crops_food_eaten_no_relocation (list): list of monthly food eaten from outdoor crops without relocation
            crops_food_eaten_relocated (list): list of monthly food eaten from outdoor crops with relocation
            outdoor_crops (Food): Food object representing the outdoor crops produced

        Returns:
            None
        """
        # create the food object for to_humans outdoor crops
        self.outdoor_crops_to_humans = (
            self.create_food_object_from_fat_protein_variables(
                crops_food_to_humans,
                crops_food_to_humans_fat,
                crops_food_to_humans_protein,
            )
        )
        # self.outdoor_crops_to_humans.plot("to humans")
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
        # self.outdoor_crops_feed.plot("feed")
        # self.outdoor_crops_biofuel.plot("bio")

        # Calculate outdoor crop production for humans
        to_humans_outdoor_crop_production = np.subtract(
            np.subtract(
                outdoor_crops_production.kcals,
                self.outdoor_crops_feed.kcals,
            ),
            self.outdoor_crops_biofuel.kcals,
        )

        # Calculate the monthly kcals fed from immediate and new stored outdoor crops
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
        difference = (
            np.array(billions_fed_immediate_outdoor_crops_kcals)
            + np.array(billions_fed_new_stored_outdoor_crops_kcals)
            - np.array(self.outdoor_crops_to_humans.kcals)
        )
        decimals = 3
        assert (
            np.round(difference, decimals) == 0
        ).all(), """ERROR: Immediate and new stored sources do not add up to the input of outdoor crop for humans"""

    def set_new_stored_outdoor_crops_values(
        self, billions_fed_new_stored_outdoor_crops_kcals
    ):
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
        self.immediate_outdoor_crops = Food(
            kcals=np.array(billions_fed_immediate_outdoor_crops_kcals),
            fat=np.zeros(len(billions_fed_immediate_outdoor_crops_kcals)),
            protein=np.zeros(len(billions_fed_immediate_outdoor_crops_kcals)),
            kcals_units="billion people fed each month",
            fat_units="billion people fed each month",
            protein_units="billion people fed each month",
        )

    def validate_outdoor_growing_production(self):
        difference = self.outdoor_crops_to_humans - (
            self.immediate_outdoor_crops + self.new_stored_outdoor_crops
        )
        assert difference.get_rounded_to_decimal(3).all_equals_zero()

    # if stored food isn't included, these results will be zero
    def extract_meat_milk_results(
        self,
        culled_meat_eaten,
        grazing_milk_kcals,
        grazing_milk_fat,
        grazing_milk_protein,
        cattle_grazing_maintained_kcals,
        cattle_grazing_maintained_fat,
        cattle_grazing_maintained_protein,
        grain_fed_meat_kcals,
        grain_fed_meat_fat,
        grain_fed_meat_protein,
        grain_fed_milk_kcals,
        grain_fed_milk_fat,
        grain_fed_milk_protein,
    ):
        """
        Extracts results for meat and milk production based on various inputs.

        Args:
            culled_meat_eaten (float): amount of culled meat eaten
            grazing_milk_kcals (list): monthly amount of grazing milk kcals
            grazing_milk_fat (list): monthly amount of grazing milk fat
            grazing_milk_protein (list): monthly amount of grazing milk protein
            cattle_grazing_maintained_kcals (list): monthly amount of cattle grazing maintained kcals
            cattle_grazing_maintained_fat (list): monthly amount of cattle grazing maintained fat
            cattle_grazing_maintained_protein (list): monthly amount of cattle grazing maintained protein
            grain_fed_meat_kcals (float): monthly amount of grain-fed meat kcals
            grain_fed_meat_fat (float): monthly amount of grain-fed meat fat
            grain_fed_meat_protein (float): monthly amount of grain-fed meat protein
            grain_fed_milk_kcals (float): monthly amount of grain-fed milk kcals
            grain_fed_milk_fat (float): monthly amount of grain-fed milk fat
            grain_fed_milk_protein (float): monthly amount of grain-fed milk protein

        Returns:
            None

        This function extracts results for meat and milk production based on various inputs.
        It calculates the amount of meat and milk produced from grazing and grain-fed sources,
        and stores the results in the corresponding Food objects.

        """

        # calculate the amount of kcals from cattle grazing maintained
        billions_fed_cattle_grazing_maintained = (
            np.array(cattle_grazing_maintained_kcals) / self.constants["KCALS_MONTHLY"]
        )

        # calculate the amount of kcals from culled meat eaten
        billions_fed_culled_meat_kcals = self.to_monthly_list(
            culled_meat_eaten,
            1 / self.constants["KCALS_MONTHLY"],
        )

        # calculate the amount of kcals from culled meat and cattle grazing maintained
        billions_fed_culled_meat_grazing_kcals = (
            billions_fed_culled_meat_kcals + billions_fed_cattle_grazing_maintained
        )

        # calculate the amount of fat from culled meat eaten
        billions_fed_culled_meat_fat = self.to_monthly_list(
            culled_meat_eaten,
            self.constants["CULLED_MEAT_FRACTION_FAT"]
            / self.constants["FAT_MONTHLY"]
            / 1e9,
        )

        # calculate the amount of protein from culled meat eaten
        billions_fed_culled_meat_protein = self.to_monthly_list(
            culled_meat_eaten,
            self.constants["CULLED_MEAT_FRACTION_PROTEIN"]
            / self.constants["PROTEIN_MONTHLY"]
            / 1e9,
        )

        # calculate the amount of fat from culled meat and cattle grazing maintained
        billions_fed_culled_meat_grazing_fat = (
            billions_fed_culled_meat_fat
            + np.array(cattle_grazing_maintained_fat)
            / self.constants["FAT_MONTHLY"]
            / 1e9
        )

        # calculate the amount of protein from culled meat and cattle grazing maintained
        billions_fed_culled_meat_grazing_protein = (
            billions_fed_culled_meat_protein
            + np.array(cattle_grazing_maintained_protein)
            / self.constants["PROTEIN_MONTHLY"]
            / 1e9
        )

        # store the results in the corresponding Food object
        self.culled_meat_plus_grazing_cattle_maintained = Food(
            kcals=billions_fed_culled_meat_grazing_kcals,
            fat=billions_fed_culled_meat_grazing_fat,
            protein=billions_fed_culled_meat_grazing_protein,
            kcals_units="billion people fed each month",
            fat_units="billion people fed each month",
            protein_units="billion people fed each month",
        )

        # calculate the amount of kcals from grazing milk
        billions_fed_grazing_milk_kcals = (
            np.array(grazing_milk_kcals) / self.constants["KCALS_MONTHLY"]
        )

        # calculate the amount of fat from grazing milk
        billions_fed_grazing_milk_fat = (
            np.array(grazing_milk_fat) / self.constants["FAT_MONTHLY"] / 1e9
        )

        # calculate the amount of protein from grazing milk
        billions_fed_grazing_milk_protein = (
            np.array(grazing_milk_protein) / self.constants["PROTEIN_MONTHLY"] / 1e9
        )

        # store the results in the corresponding Food object
        self.grazing_milk = Food(
            kcals=billions_fed_grazing_milk_kcals,
            fat=billions_fed_grazing_milk_fat,
            protein=billions_fed_grazing_milk_protein,
            kcals_units="billion people fed each month",
            fat_units="billion people fed each month",
            protein_units="billion people fed each month",
        )

        # calculate the amount of kcals from grain-fed meat
        billions_fed_grain_fed_meat_kcals = (
            grain_fed_meat_kcals / self.constants["KCALS_MONTHLY"]
        )

        # calculate the amount of fat from grain-fed meat
        billions_fed_grain_fed_meat_fat = (
            grain_fed_meat_fat / self.constants["FAT_MONTHLY"] / 1e9
        )

        # calculate the amount of protein from grain-fed meat
        billions_fed_grain_fed_meat_protein = (
            grain_fed_meat_protein / self.constants["PROTEIN_MONTHLY"] / 1e9
        )

        # store the results in the corresponding Food object
        self.grain_fed_meat = Food(
            kcals=billions_fed_grain_fed_meat_kcals,
            fat=billions_fed_grain_fed_meat_fat,
            protein=billions_fed_grain_fed_meat_protein,
            kcals_units="billion people fed each month",
            fat_units="billion people fed each month",
            protein_units="billion people fed each month",
        )

        # calculate the amount of kcals from grain-fed milk
        billions_fed_grain_fed_milk_kcals = (
            grain_fed_milk_kcals / self.constants["KCALS_MONTHLY"]
        )

        # calculate the amount of fat from grain-fed milk
        billions_fed_grain_fed_milk_fat = (
            grain_fed_milk_fat / self.constants["FAT_MONTHLY"] / 1e9
        )

        # calculate the amount of protein from grain-fed milk
        billions_fed_grain_fed_milk_protein = (
            grain_fed_milk_protein / self.constants["PROTEIN_MONTHLY"] / 1e9
        )

        # store the results in the corresponding Food object
        self.grain_fed_milk = Food(
            kcals=billions_fed_grain_fed_milk_kcals,
            fat=billions_fed_grain_fed_milk_fat,
            protein=billions_fed_grain_fed_milk_protein,
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

    def get_objective_optimization_results(self, model):
        """
        This function extracts the optimization results from the given model and returns them in a tuple.
        I spent like five hours trying to figure out why the answer was wrong
        until I finally found an issue with string ordering, fixed it below
        Args:
            self: instance of the class containing the function
            model: the optimization model to extract results from
        Returns:
            tuple: a tuple containing the optimization results for consumed kcals, fat, and protein
        """

        consumed_kcals = []
        consumed_fat = []
        consumed_protein = []
        order_kcals = []
        order_fat = []
        order_protein = []

        # Loop through all variables in the model
        for var in model.variables():
            # Append the optimization result to the consumed_kcals list
            if "Consumed_Kcals_" in var.name:
                consumed_kcals.append(var.value() / 100 * self.constants["POP"] / 1e9)

                order_kcals.append(
                    int(var.name[len("Consumed_Kcals_") :].split("_")[0])
                )

            if "Consumed_Fat_" in var.name:
                order_fat.append(int(var.name[len("Consumed_Fat_") :].split("_")[0]))

                consumed_fat.append(var.value() / 100 * self.constants["POP"] / 1e9)

            if "Consumed_Protein_" in var.name:
                order_protein.append(
                    int(var.name[len("Consumed_Protein_") :].split("_")[0])
                )

                consumed_protein.append(var.value() / 100 * self.constants["POP"] / 1e9)

        zipped_lists = zip(order_kcals, consumed_kcals)
        sorted_zipped_lists = sorted(zipped_lists)
        consumed_kcals_optimizer = [element for _, element in sorted_zipped_lists]

        zipped_lists = zip(order_fat, consumed_fat)
        sorted_zipped_lists = sorted(zipped_lists)
        consumed_fat_optimizer = [element for _, element in sorted_zipped_lists]

        zipped_lists = zip(order_protein, consumed_protein)
        sorted_zipped_lists = sorted(zipped_lists)
        consumed_protein_optimizer = [element for _, element in sorted_zipped_lists]

        return (
            consumed_kcals_optimizer,
            consumed_fat_optimizer,
            consumed_protein_optimizer,
        )
