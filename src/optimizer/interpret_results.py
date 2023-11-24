"""
This function takes the raw output of the optimizer food categories and total people fed
and breaks this down into what the amount of each expected food category would be in
order to produce these results.

The evaluation creates more useful values for plotting and scenario evaluation than
exactly what is being optimized in the optimizer.

Created on Tue Jul 19

@author: morgan
"""
import numpy as np
from src.food_system.food import Food
import pandas as pd

import datetime
from datetime import date

import git
from pathlib import Path
import sys

repo_root = git.Repo(".", search_parent_directories=True).working_dir


class Interpreter:
    """
    This class is used to convert between optimization results data and other useful
    ways of interpreting the results, as a diet, or as a total food supply.
    """

    def __init__(self):
        self.show_feed_biofuels = (
            False  # until set to true, this will not show the feed or biofuels
        )

    def set_feed(self, feed_and_biofuels):
        self.show_feed_biofuels = True
        self.feed_and_biofuels = feed_and_biofuels

    def set_meat_dictionary(self, meat_dictionary):
        self.meat_dictionary = {}
        self.animal_population_dictionary = {}
        # Populate your meat production data here, similar to ykcals
        for animal_label, value in meat_dictionary.items():
            if max(value) == 0:
                continue  # don't show zero slaughter or population on the plots
            if "_population" in animal_label:
                self.animal_population_dictionary[animal_label] = value
            else:
                self.meat_dictionary[animal_label] = value

    def interpret_results(self, extracted_results):
        """
        This function takes the raw output of the optimizer food categories and total
        people fed in list form, and converts the naive people fed which includes
        negative feed, into a purely list of values, where the negative feed has been
        subtracted from the sum of outdoor growing and stored food.

        Args:
            extracted_results (object): The raw output of the optimizer food categories and
            total people fed in list form
            time_consts (dict): A dictionary containing time constants

        Returns:
            object: An instance of the Interpreter class

        ANYTHING assigned to "self" here is part of a useful result that will either
        be printed or plotted as a result
        """

        # Assign percent fed from extractor
        self.assign_percent_fed_from_extractor(extracted_results)

        # Assign kcals equivalent from extractor
        self.assign_kcals_equivalent_from_extractor(extracted_results)

        # Assign constants
        self.constants = extracted_results.constants

        # Assign time months middle
        self.assign_time_months_middle(self.constants["NMONTHS"])

        # Assign nonhuman consumption
        self.nonhuman_consumption = extracted_results.nonhuman_consumption

        # Set feed and biofuels
        self.set_feed_and_biofuels(
            extracted_results.seaweed_biofuel,
            extracted_results.scp_biofuel,
            extracted_results.cell_sugar_biofuel,
            extracted_results.stored_food_biofuel,
            extracted_results.outdoor_crops_biofuel,
            extracted_results.seaweed_feed,
            extracted_results.scp_feed,
            extracted_results.cell_sugar_feed,
            extracted_results.stored_food_feed,
            extracted_results.outdoor_crops_feed,
        )

        # Assign interpreted properties
        self.assign_interpreted_properties(extracted_results)

        # Set include fat and protein
        self.include_fat = Food.conversions.include_fat
        self.include_protein = Food.conversions.include_protein

        # Create CSV output
        CREATE_CSV_OUTPUT = True
        if CREATE_CSV_OUTPUT:
            dict = {
                "fish": np.array(self.fish_kcals_equivalent.kcals),
                "cell_sugar": np.array(self.cell_sugar_kcals_equivalent.kcals),
                "scp": np.array(self.scp_kcals_equivalent.kcals),
                "greenhouse": np.array(self.greenhouse_kcals_equivalent.kcals),
                "seaweed": np.array(self.seaweed_kcals_equivalent.kcals),
                "milk": np.array(self.grazing_milk_kcals_equivalent.kcals),
                "meat": np.array(
                    self.culled_meat_plus_grazing_cattle_maintained_kcals_equivalent.kcals
                ),
                "immediate_outdoor_crops": np.array(
                    self.immediate_outdoor_crops_kcals_equivalent.kcals
                ),
                "new_stored_outdoor_crops": np.array(
                    self.new_stored_outdoor_crops_kcals_equivalent.kcals
                ),
                "stored_food": np.array(self.stored_food_kcals_equivalent.kcals),
            }

            df = pd.DataFrame(dict)

            # Saving the dataframe
            year = str(date.today().year)
            month = str(date.today().month)
            day = str(date.today().day)
            hour = str(datetime.datetime.now().hour)
            minute = str(datetime.datetime.now().minute)
            second = str(datetime.datetime.now().second)

            filename = (
                "ykcals"
                + "."
                + year
                + "."
                + month
                + "."
                + day
                + "."
                + hour
                + "."
                + minute
                + "."
                + second
                + ".csv"
            )
            file_location = str(Path(repo_root) / "results" / filename)
            df.to_csv(file_location)

        return self

    def assign_percent_fed_from_extractor(self, extracted_results):
        """
        Assigns the percentage of food fed to humans from each food source extracted from the results.
        Args:
            extracted_results (ExtractedResults): An instance of the ExtractedResults class containing the results
            of the extraction process.
        Returns:
            None
        """
        # Assign the percentage of stored food fed to humans
        self.stored_food = (
            extracted_results.stored_food_to_humans.in_units_percent_fed()
        )

        # Assign the percentage of outdoor crops fed to humans
        self.outdoor_crops = (
            extracted_results.outdoor_crops_to_humans.in_units_percent_fed()
        )

        # Assign the percentage of seaweed fed to humans
        self.seaweed = extracted_results.seaweed_to_humans.in_units_percent_fed()

        # Assign the percentage of cell sugar fed to humans
        self.cell_sugar = extracted_results.cell_sugar_to_humans.in_units_percent_fed()

        # Assign the percentage of SCP fed to humans
        self.scp = extracted_results.scp_to_humans.in_units_percent_fed()

        # Assign the percentage of food from the greenhouse fed to humans
        self.greenhouse = extracted_results.greenhouse.in_units_percent_fed()

        # Assign the percentage of fish fed to humans
        self.fish = extracted_results.fish.in_units_percent_fed()

        # Assign the percentage of culled meat plus grazing cattle maintained fed to humans
        self.culled_meat_plus_grazing_cattle_maintained = (
            extracted_results.culled_meat_plus_grazing_cattle_maintained.in_units_percent_fed()
        )

        # Assign the percentage of grazing milk fed to humans
        self.grazing_milk = extracted_results.grazing_milk.in_units_percent_fed()

        # Assign the percentage of immediate outdoor crops fed to humans
        self.immediate_outdoor_crops = (
            extracted_results.immediate_outdoor_crops.in_units_percent_fed()
        )

        # Assign the percentage of new stored outdoor crops fed to humans
        self.new_stored_outdoor_crops = (
            extracted_results.new_stored_outdoor_crops.in_units_percent_fed()
        )

    def assign_kcals_equivalent_from_extractor(self, extracted_results):
        """
        Assigns the kcals equivalent of various food sources to their respective attributes in the Interpreter object.
        Args:
            extracted_results (ExtractedResults): An object containing the results of the extraction process.
        Returns:
            None
        """
        # Assign kcals equivalent of stored food to humans
        self.stored_food_kcals_equivalent = (
            extracted_results.stored_food_to_humans.in_units_kcals_equivalent()
        )

        # Assign kcals equivalent of seaweed to humans
        self.seaweed_kcals_equivalent = (
            extracted_results.seaweed_to_humans.in_units_kcals_equivalent()
        )

        # Assign kcals equivalent of cell sugar to humans
        self.cell_sugar_kcals_equivalent = (
            extracted_results.cell_sugar_to_humans.in_units_kcals_equivalent()
        )

        # Assign kcals equivalent of SCP to humans
        self.scp_kcals_equivalent = (
            extracted_results.scp_to_humans.in_units_kcals_equivalent()
        )

        # Assign kcals equivalent of greenhouse to its attribute
        self.greenhouse_kcals_equivalent = (
            extracted_results.greenhouse.in_units_kcals_equivalent()
        )

        # Assign kcals equivalent of fish to its attribute
        self.fish_kcals_equivalent = extracted_results.fish.in_units_kcals_equivalent()

        # Assign kcals equivalent of culled meat plus grazing cattle maintained to its attribute
        self.culled_meat_plus_grazing_cattle_maintained_kcals_equivalent = (
            extracted_results.culled_meat_plus_grazing_cattle_maintained.in_units_kcals_equivalent()
        )

        # Assign kcals equivalent of grazing milk to its attribute
        self.grazing_milk_kcals_equivalent = (
            extracted_results.grazing_milk.in_units_kcals_equivalent()
        )

        # Assign kcals equivalent of immediate outdoor crops to its attribute
        self.immediate_outdoor_crops_kcals_equivalent = (
            extracted_results.immediate_outdoor_crops.in_units_kcals_equivalent()
        )

        # Assign kcals equivalent of new stored outdoor crops to its attribute
        self.new_stored_outdoor_crops_kcals_equivalent = (
            extracted_results.new_stored_outdoor_crops.in_units_kcals_equivalent()
        )

    def set_to_humans_properties_kcals_equivalent(self, extracted_results):
        """
        Converts the stored food and outdoor crops to humans properties to their equivalent in kcals.
        Args:
            extracted_results (dict): A dictionary containing the extracted results from the simulation.

        Returns:
            None

        """
        # Convert stored food to humans properties to kcals equivalent
        self.stored_food_to_humans_kcals_equivalent = (
            self.stored_food_to_humans.in_units_kcals_equivalent()
        )

        # Convert outdoor crops to humans properties to kcals equivalent
        self.outdoor_crops_to_humans_kcals_equivalent = (
            self.outdoor_crops_to_humans.in_units_kcals_equivalent()
        )

        # Convert immediate outdoor crops to humans properties to kcals equivalent
        self.immediate_outdoor_crops_to_humans_kcals_equivalent = (
            self.immediate_outdoor_crops_to_humans.in_units_kcals_equivalent()
        )

        # Convert new stored outdoor crops to humans properties to kcals equivalent
        self.new_stored_outdoor_crops_to_humans_kcals_equivalent = (
            self.new_stored_outdoor_crops_to_humans.in_units_kcals_equivalent()
        )

    def assign_time_months_middle(self, NMONTHS):
        """
        This function assigns the middle of each month to a list of time_months_middle.
        Args:
            NMONTHS (int): The number of months to assign the middle of.

        Returns:
            None

        Example:
            >>> interpreter = Interpreter()
            >>> interpreter.assign_time_months_middle(12)
            >>> print(interpreter.time_months_middle)
            [0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5, 11.5]
        """
        # Clear the list to start fresh
        self.time_months_middle = []

        # Loop through each month and add the middle to the list
        for month in range(0, NMONTHS):
            self.time_months_middle.append(month + 0.5)

    def assign_interpreted_properties(self, extracted_results):
        """
        Assigns interpreted properties to the Interpreter object based on the extracted results.
        Args:
            extracted_results (ExtractedResults): The extracted results object to interpret.

        Returns:
            None

        Example:
            >>> extracted_results = ExtractedResults()
            >>> interpreter = Interpreter()
            >>> interpreter.assign_interpreted_properties(extracted_results)
        """
        # Get the sum of humans fed by adding to humans.
        humans_fed_sum = self.get_sum_by_adding_to_humans()

        # Get the percentage of people fed and the constraining nutrient.
        (
            self.percent_people_fed,
            self.constraining_nutrient,
        ) = self.get_percent_people_fed(humans_fed_sum)

        # rounding errors can be introduced by the optimizer. We correct them here.
        # ... at least the ones that we can identify.
        # We also round everything to within 0.1% of its value,
        # in terms of % people fed.
        (
            self.stored_food,
            self.outdoor_crops,
            self.immediate_outdoor_crops,
            self.new_stored_outdoor_crops,
            self.seaweed_rounded,
        ) = self.correct_and_validate_rounding_errors()

        self.kcals_fed = humans_fed_sum.kcals
        self.fat_fed = humans_fed_sum.fat
        self.protein_fed = humans_fed_sum.protein

    def get_mean_min_nutrient(self):
        """
        for finding the minimum of any nutrient in any month
        and then getting the mean people fed in all the months
        This is useful for assessing what would have happened if stored food were not
        a constraint on number of people fed

        returns: the mean people fed in all months
        """
        # this is what the command below does
        # >>> a = np.array([3,2,1])
        # >>> b = np.array([2,2,6])
        # >>> c = np.array([100,100,0])
        # >>> np.min([a,b,c],axis=0)
        # array([2, 2, 0])
        min_fed = np.min([self.kcals_fed, self.fat_fed, self.protein_fed], axis=0)

        mean_fed = np.mean(min_fed)
        return mean_fed

    def get_sum_by_adding_to_humans(self):
        """
        Sums the resulting nutrients from the extracted_results and returns the total.

        Args:
            self: instance of the Interpreter class

        Returns:
            float: the total amount of nutrients that can be fed to humans

        Example:
            >>> interpreter = Interpreter()
            >>> interpreter.stored_food = 100
            >>> interpreter.outdoor_crops = 200
            >>> interpreter.seaweed = 50
            >>> interpreter.cell_sugar = 75
            >>> interpreter.scp = 150
            >>> interpreter.greenhouse = 300
            >>> interpreter.fish = 100
            >>> interpreter.culled_meat_plus_grazing_cattle_maintained = 50
            >>> interpreter.grazing_milk = 25
            >>> interpreter.get_sum_by_adding_to_humans()
            1025.0
        """

        # Sum the resulting nutrients from the extracted_results
        to_humans_fed_sum = (
            self.stored_food
            + self.outdoor_crops
            + self.seaweed
            + self.cell_sugar
            + self.scp
            + self.greenhouse
            + self.fish
            + self.culled_meat_plus_grazing_cattle_maintained
            + self.grazing_milk
        )

        # Return the total amount of nutrients that can be fed to humans
        return to_humans_fed_sum

    def print_kcals_per_person_per_day(self, interpreted_results):
        """
        This function calculates and prints the expected kcals/capita/day for a given scenario result.
        Args:
            interpreted_results (InterpretedResults): An instance of the InterpretedResults class containing
            the interpreted results of a scenario.

        Returns:
            None

        """
        # Calculate the ratio of people fed to total population
        needs_ratio = interpreted_results.percent_people_fed / 100

        print("Expected kcals/person/day")
        print(needs_ratio * 2100)
        print("")

    def get_percent_people_fed(self, humans_fed_sum):
        """
        Calculates the estimated percentage of people fed based on the minimum nutrients required to meet the
        needs of the population in any month, for kcals, fat, and protein.

        Args:
            humans_fed_sum (HumanFedSum): An instance of the HumanFedSum class representing the total amount of
            nutrients available for the population.

        Returns:
            list: A list containing the estimated percentage of people fed and the minimum nutrients required to
            meet their needs.
        """
        assert humans_fed_sum.is_units_percent()

        # Get the minimum nutrients required to meet the needs of the population
        (min_nutrient, percent_people_fed) = humans_fed_sum.get_min_nutrient()

        # Print the nutrients with constraining values and the estimated percentage of people fed
        PRINT_FED = False
        if PRINT_FED:
            print("Nutrients with constraining values are: " + str(min_nutrient))
            print(
                "Estimated percent people fed is "
                + str(round(percent_people_fed, 1))
                + "%"
            )

        # Return the estimated percentage of people fed and the minimum nutrients required to meet their needs
        return [percent_people_fed, min_nutrient]

    def correct_and_validate_rounding_errors(self):
        """
        This function corrects any rounding errors that might have occurred during the optimization process.
        It ensures that the values are rounded to the nearest 3 decimal places and that they are greater than or equal
        to zero.
        The function returns the corrected values for stored_food, outdoor_crops,
        immediate_outdoor_crops, new_stored_outdoor_crops, and seaweed.

        Args:
            None

        Returns:
            tuple: A tuple containing the corrected values for stored_food, outdoor_crops, immediate_outdoor_crops,
            new_stored_outdoor_crops, and seaweed.
        """
        # Ensure that all the outputs have the same number of months
        assert (
            self.stored_food.NMONTHS
            == self.outdoor_crops.NMONTHS
            == self.immediate_outdoor_crops.NMONTHS
            == self.new_stored_outdoor_crops.NMONTHS
            == self.seaweed.NMONTHS
        )

        # Ensure that all the outputs are in percentage units
        assert self.stored_food.is_units_percent()
        assert self.outdoor_crops.is_units_percent()
        assert self.immediate_outdoor_crops.is_units_percent()
        assert self.new_stored_outdoor_crops.is_units_percent()
        assert self.seaweed.is_units_percent()

        # Round the values to the nearest 3 decimal places
        stored_food_rounded = self.stored_food.get_rounded_to_decimal(3)
        outdoor_crops_rounded = self.outdoor_crops.get_rounded_to_decimal(3)
        seaweed_rounded = self.seaweed.get_rounded_to_decimal(3)

        # TODO BUG?? Noticed this is failing at 3 decimal place rounding...
        immediate_outdoor_crops_rounded = (
            self.immediate_outdoor_crops.get_rounded_to_decimal(2)
        )
        new_stored_outdoor_crops_rounded = (
            self.new_stored_outdoor_crops.get_rounded_to_decimal(3)
        )

        # Ensure that all the rounded values are greater than or equal to zero
        assert stored_food_rounded.all_greater_than_or_equal_to_zero()
        assert seaweed_rounded.all_greater_than_or_equal_to_zero()
        assert outdoor_crops_rounded.all_greater_than_or_equal_to_zero()
        assert immediate_outdoor_crops_rounded.all_greater_than_or_equal_to_zero()
        assert new_stored_outdoor_crops_rounded.all_greater_than_or_equal_to_zero()

        # Return the corrected values
        return (
            stored_food_rounded,
            outdoor_crops_rounded,
            immediate_outdoor_crops_rounded,
            new_stored_outdoor_crops_rounded,
            seaweed_rounded,
        )

    def get_month_after_which_is_all_zero(self, variables, nmonths):
        first_month = None  # This will hold the earliest month where all subsequent months are zero

        def check_zeros(array):
            # Find the first index where all subsequent values are zero
            for idx in range(len(array)):
                if np.all(array[idx:] == 0):
                    return idx
            return len(array)  # Return the length of the array if no zeros found

        # Check if variables is a dict or list and iterate accordingly
        iter_vars = variables.values() if isinstance(variables, dict) else variables

        for value in iter_vars:
            if isinstance(value, Food):
                # Check all three arrays in the Food object
                months = [
                    check_zeros(value.kcals),
                    check_zeros(value.fat),
                    check_zeros(value.protein),
                ]
                min_month = min(months)  # Get the earliest month for this Food object
            elif isinstance(value, np.ndarray):
                # Assume it's a numpy array
                min_month = check_zeros(value)
            else:
                print("ERROR! Expected ndarray for this plotting feature.")
                sys.exit()
            # Update first_month if this is the latest month found so far
            if first_month is None or min_month > first_month:
                first_month = min_month
        if first_month == nmonths:
            return first_month
        else:
            return first_month + 1

    def set_feed_and_biofuels(
        self,
        seaweed_used_for_biofuel,
        methane_scp_used_for_biofuel,
        cellulosic_sugar_used_for_biofuel,
        stored_food_used_for_biofuel,
        outdoor_crops_used_for_biofuel,
        seaweed_used_for_feed,
        methane_scp_used_for_feed,
        cellulosic_sugar_used_for_feed,
        stored_food_used_for_feed,
        outdoor_crops_used_for_feed,
    ):
        """
        This function sets the feed and biofuel usage for each month. It takes the
        outdoor crops, methane, and cellulosic sugar that are used for feed and
        biofuels, and the remaining feed and biofuel needed from stored food.
        """
        self.cell_sugar_biofuels = (
            cellulosic_sugar_used_for_biofuel.in_units_percent_fed()
        )
        self.cell_sugar_feed = cellulosic_sugar_used_for_feed.in_units_percent_fed()
        self.scp_biofuels = methane_scp_used_for_biofuel.in_units_percent_fed()
        self.scp_feed = methane_scp_used_for_feed.in_units_percent_fed()

        self.seaweed_biofuels = seaweed_used_for_biofuel.in_units_percent_fed()
        self.seaweed_feed = seaweed_used_for_feed.in_units_percent_fed()

        self.outdoor_crops_biofuels = (
            outdoor_crops_used_for_biofuel.in_units_percent_fed()
        )
        self.outdoor_crops_feed = outdoor_crops_used_for_feed.in_units_percent_fed()
        self.stored_food_biofuels = stored_food_used_for_biofuel.in_units_percent_fed()

        self.stored_food_feed = stored_food_used_for_feed.in_units_percent_fed()

        self.cell_sugar_biofuels_kcals_equivalent = (
            self.cell_sugar_biofuels.in_units_kcals_equivalent()
        )
        self.cell_sugar_feed_kcals_equivalent = (
            self.cell_sugar_feed.in_units_kcals_equivalent()
        )
        self.scp_biofuels_kcals_equivalent = (
            self.scp_biofuels.in_units_kcals_equivalent()
        )
        self.scp_feed_kcals_equivalent = self.scp_feed.in_units_kcals_equivalent()
        self.seaweed_biofuels_kcals_equivalent = (
            self.seaweed_biofuels.in_units_kcals_equivalent()
        )
        self.seaweed_feed_kcals_equivalent = (
            self.seaweed_feed.in_units_kcals_equivalent()
        )
        self.outdoor_crops_biofuels_kcals_equivalent = (
            self.outdoor_crops_biofuels.in_units_kcals_equivalent()
        )
        self.outdoor_crops_feed_kcals_equivalent = (
            self.outdoor_crops_feed.in_units_kcals_equivalent()
        )
        self.stored_food_biofuels_kcals_equivalent = (
            self.stored_food_biofuels.in_units_kcals_equivalent()
        )
        self.stored_food_feed_kcals_equivalent = (
            self.stored_food_feed.in_units_kcals_equivalent()
        )

    def sum_many_results_together(many_results, cap_at_100_percent):
        """
        sum together the results from many different runs of the model
        create a new object summing the results

        returns: the interpreter object with the summed results divided by the
        population in question
        """

        i = 0
        net_pop = 0
        previous_interpreter = []
        for country, interpreter in many_results.items():
            # record some useful values for plotting from the interpreter
            # will check later that these are consistent
            include_fat = interpreter.include_fat
            include_protein = interpreter.include_protein
            time_months_middle = interpreter.time_months_middle

            ADD_FISH = interpreter.constants["ADD_FISH"]
            ADD_CELLULOSIC_SUGAR = interpreter.constants["ADD_CELLULOSIC_SUGAR"]
            ADD_METHANE_SCP = interpreter.constants["ADD_METHANE_SCP"]
            ADD_GREENHOUSES = interpreter.constants["ADD_GREENHOUSES"]
            ADD_SEAWEED = interpreter.constants["ADD_SEAWEED"]
            ADD_MILK = interpreter.constants["ADD_MILK"]
            ADD_CULLED_MEAT = interpreter.constants["ADD_CULLED_MEAT"]
            ADD_OUTDOOR_GROWING = interpreter.constants["ADD_OUTDOOR_GROWING"]
            ADD_STORED_FOOD = interpreter.constants["ADD_STORED_FOOD"]

            # print(interpreter.constants)
            net_pop += interpreter.constants["POP"]
            kcals_daily = interpreter.constants["inputs"]["NUTRITION"]["KCALS_DAILY"]
            # needed to do unit conversions properly
            Food.conversions.set_nutrition_requirements(
                kcals_daily=kcals_daily,
                fat_daily=interpreter.constants["inputs"]["NUTRITION"]["FAT_DAILY"],
                protein_daily=interpreter.constants["inputs"]["NUTRITION"][
                    "PROTEIN_DAILY"
                ],
                include_fat=include_fat,
                include_protein=include_protein,
                population=interpreter.constants["POP"],
            )

            fish = interpreter.fish.in_units_bil_kcals_thou_tons_thou_tons_per_month()
            cell_sugar = (
                interpreter.cell_sugar.in_units_bil_kcals_thou_tons_thou_tons_per_month()
            )
            scp = interpreter.scp.in_units_bil_kcals_thou_tons_thou_tons_per_month()
            greenhouse = (
                interpreter.greenhouse.in_units_bil_kcals_thou_tons_thou_tons_per_month()
            )
            seaweed = (
                interpreter.seaweed.in_units_bil_kcals_thou_tons_thou_tons_per_month()
            )
            grazing_milk = (
                interpreter.grazing_milk.in_units_bil_kcals_thou_tons_thou_tons_per_month()
            )
            cmpgcm = interpreter.culled_meat_plus_grazing_cattle_maintained
            culled_meat_plus_grazing_cattle_maintained = (
                cmpgcm.in_units_bil_kcals_thou_tons_thou_tons_per_month()
            )

            immediate_outdoor_crops = (
                interpreter.immediate_outdoor_crops_to_humans.in_units_bil_kcals_thou_tons_thou_tons_per_month()
            )
            new_stored_outdoor_crops = (
                interpreter.new_stored_outdoor_crops_to_humans.in_units_bil_kcals_thou_tons_thou_tons_per_month()
            )
            stored_food = (
                interpreter.stored_food_to_humans.in_units_bil_kcals_thou_tons_thou_tons_per_month()
            )

            if interpreter.percent_people_fed <= 100:
                ratio_so_adds_to_100_percent = 1
            else:
                # this is always less than 1. The value is the amount so percent people
                # fed would be 100 if all the components are added up
                ratio_so_adds_to_100_percent = 100 / interpreter.percent_people_fed
                assert 0 < ratio_so_adds_to_100_percent < 1

            if cap_at_100_percent:
                fish = fish * ratio_so_adds_to_100_percent
                cell_sugar = cell_sugar * ratio_so_adds_to_100_percent
                scp = scp * ratio_so_adds_to_100_percent
                greenhouse = greenhouse * ratio_so_adds_to_100_percent
                seaweed = seaweed * ratio_so_adds_to_100_percent
                grazing_milk = grazing_milk * ratio_so_adds_to_100_percent
                culled_meat_plus_grazing_cattle_maintained = (
                    culled_meat_plus_grazing_cattle_maintained
                    * ratio_so_adds_to_100_percent
                )
                immediate_outdoor_crops = (
                    immediate_outdoor_crops * ratio_so_adds_to_100_percent
                )
                new_stored_outdoor_crops = (
                    new_stored_outdoor_crops * ratio_so_adds_to_100_percent
                )
                stored_food = stored_food * ratio_so_adds_to_100_percent

            if i == 0:
                fish_cumulative = fish
                cell_sugar_cumulative = cell_sugar
                scp_cumulative = scp
                greenhouse_cumulative = greenhouse
                seaweed_cumulative = seaweed
                grazing_milk_cumulative = grazing_milk
                culled_meat_plus_grazing_cattle_maintained_cumulative = (
                    culled_meat_plus_grazing_cattle_maintained
                )
                immediate_outdoor_crops_cumulative = immediate_outdoor_crops
                new_stored_outdoor_crops_cumulative = new_stored_outdoor_crops
                stored_food_cumulative = stored_food
            else:
                # make sure all the interpreters have the same sets of constants
                assert previous_interpreter.include_fat == include_fat
                assert previous_interpreter.include_protein == include_protein
                assert previous_interpreter.time_months_middle == time_months_middle

                assert ADD_FISH == previous_interpreter.constants["ADD_FISH"]

                assert (
                    ADD_CELLULOSIC_SUGAR
                    == previous_interpreter.constants["ADD_CELLULOSIC_SUGAR"]
                )

                assert (
                    ADD_METHANE_SCP == previous_interpreter.constants["ADD_METHANE_SCP"]
                )

                assert (
                    ADD_GREENHOUSES == previous_interpreter.constants["ADD_GREENHOUSES"]
                )

                assert ADD_SEAWEED == previous_interpreter.constants["ADD_SEAWEED"]

                assert ADD_MILK == previous_interpreter.constants["ADD_MILK"]

                assert (
                    ADD_CULLED_MEAT == previous_interpreter.constants["ADD_CULLED_MEAT"]
                )

                assert (
                    ADD_OUTDOOR_GROWING
                    == previous_interpreter.constants["ADD_OUTDOOR_GROWING"]
                )

                assert (
                    ADD_OUTDOOR_GROWING
                    == previous_interpreter.constants["ADD_OUTDOOR_GROWING"]
                )

                assert (
                    ADD_STORED_FOOD == previous_interpreter.constants["ADD_STORED_FOOD"]
                )

                fish_cumulative = fish_cumulative + fish
                cell_sugar_cumulative = cell_sugar_cumulative + cell_sugar
                scp_cumulative = scp_cumulative + scp
                greenhouse_cumulative = greenhouse_cumulative + greenhouse
                seaweed_cumulative = seaweed_cumulative + seaweed
                grazing_milk_cumulative = grazing_milk_cumulative + grazing_milk
                culled_meat_plus_grazing_cattle_maintained_cumulative = (
                    culled_meat_plus_grazing_cattle_maintained_cumulative
                    + culled_meat_plus_grazing_cattle_maintained
                )
                immediate_outdoor_crops_cumulative = (
                    immediate_outdoor_crops_cumulative + immediate_outdoor_crops
                )
                new_stored_outdoor_crops_cumulative = (
                    new_stored_outdoor_crops_cumulative + new_stored_outdoor_crops
                )
                stored_food_cumulative = stored_food_cumulative + stored_food

            previous_interpreter = interpreter
            i += 1

        # kcals per person per day
        KCALS_DAILY = 2100

        # grams per person per day
        FAT_DAILY = 47

        # grams per person per day
        PROTEIN_DAILY = 51

        Food.conversions.set_nutrition_requirements(
            kcals_daily=KCALS_DAILY,
            fat_daily=FAT_DAILY,
            protein_daily=PROTEIN_DAILY,
            include_fat=include_fat,
            include_protein=include_protein,
            population=net_pop,
        )

        global_results = Interpreter()

        humans_fed_sum = (
            fish_cumulative.in_units_percent_fed()
            + cell_sugar_cumulative.in_units_percent_fed()
            + scp_cumulative.in_units_percent_fed()
            + greenhouse_cumulative.in_units_percent_fed()
            + seaweed_cumulative.in_units_percent_fed()
            + grazing_milk_cumulative.in_units_percent_fed()
            + culled_meat_plus_grazing_cattle_maintained_cumulative.in_units_percent_fed()
            + immediate_outdoor_crops_cumulative.in_units_percent_fed()
            + new_stored_outdoor_crops_cumulative.in_units_percent_fed()
            + stored_food_cumulative.in_units_percent_fed()
        )

        global_results.time_months_middle = time_months_middle
        global_results.include_fat = include_fat
        global_results.include_protein = include_protein
        global_results.kcals_fed = humans_fed_sum.kcals
        global_results.fat_fed = humans_fed_sum.fat
        global_results.protein_fed = humans_fed_sum.protein

        global_results.constants = {}
        global_results.constants["ADD_FISH"] = ADD_FISH
        global_results.constants["ADD_CELLULOSIC_SUGAR"] = ADD_CELLULOSIC_SUGAR
        global_results.constants["ADD_METHANE_SCP"] = ADD_METHANE_SCP
        global_results.constants["ADD_GREENHOUSES"] = ADD_GREENHOUSES
        global_results.constants["ADD_SEAWEED"] = ADD_SEAWEED
        global_results.constants["ADD_MILK"] = ADD_MILK
        global_results.constants["ADD_CULLED_MEAT"] = ADD_CULLED_MEAT
        global_results.constants["ADD_OUTDOOR_GROWING"] = ADD_OUTDOOR_GROWING
        global_results.constants["ADD_OUTDOOR_GROWING"] = ADD_OUTDOOR_GROWING
        global_results.constants["ADD_STORED_FOOD"] = ADD_STORED_FOOD

        global_results.kcals_fed = humans_fed_sum.kcals
        global_results.fat_fed = humans_fed_sum.fat
        global_results.protein_fed = humans_fed_sum.protein

        global_results.fish_kcals_equivalent = (
            fish_cumulative.in_units_percent_fed().in_units_kcals_equivalent()
        )
        global_results.cell_sugar_kcals_equivalent = (
            cell_sugar_cumulative.in_units_percent_fed().in_units_kcals_equivalent()
        )
        global_results.scp_kcals_equivalent = (
            scp_cumulative.in_units_percent_fed().in_units_kcals_equivalent()
        )
        global_results.greenhouse_kcals_equivalent = (
            greenhouse_cumulative.in_units_percent_fed().in_units_kcals_equivalent()
        )
        global_results.seaweed_kcals_equivalent = (
            seaweed_cumulative.in_units_percent_fed().in_units_kcals_equivalent()
        )
        global_results.grazing_milk_kcals_equivalent = (
            grazing_milk_cumulative.in_units_percent_fed().in_units_kcals_equivalent()
        )
        global_results.culled_meat_plus_grazing_cattle_maintained_kcals_equivalent = (
            culled_meat_plus_grazing_cattle_maintained_cumulative.in_units_percent_fed().in_units_kcals_equivalent()
        )
        global_results.immediate_outdoor_crops_to_humans_kcals_equivalent = (
            immediate_outdoor_crops_cumulative.in_units_percent_fed().in_units_kcals_equivalent()
        )
        global_results.new_stored_outdoor_crops_to_humans_kcals_equivalent = (
            new_stored_outdoor_crops_cumulative.in_units_percent_fed().in_units_kcals_equivalent()
        )
        global_results.stored_food_to_humans_kcals_equivalent = (
            stored_food_cumulative.in_units_percent_fed().in_units_kcals_equivalent()
        )
        return global_results
