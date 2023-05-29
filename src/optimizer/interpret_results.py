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

repo_root = git.Repo(".", search_parent_directories=True).working_dir


class Interpreter:
    """
    This class is used to convert between optimization results data and other useful
    ways of interpreting the results, as a diet, or as a total food supply.
    """

    def __init__(self):
        pass

    def interpret_results(self, extracted_results):
        """
        This function takes the raw output of the optimizer food categories and total
        people fed in list form, and converts the naive people fed which includes
        negative feed, into a purely list of values, where the negative feed has been
        subtracted from the sum of outdoor growing and stored food.

        Args:
            extracted_results (list): The raw output of the optimizer food categories and
            total people fed in list form.

        Returns:
            self: The instance of the class.

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
        self.nonhuman_consumption = extracted_results.nonhuman_consumption
        # nonhuman consumption in units percent people fed
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

        # Set include_fat and include_protein
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
                "milk": np.array(self.grazing_milk_kcals_equivalent.kcals)
                + np.array(self.grain_fed_milk_kcals_equivalent.kcals),
                "meat": np.array(
                    self.culled_meat_plus_grazing_cattle_maintained_kcals_equivalent.kcals
                )
                + np.array(self.grain_fed_meat_kcals_equivalent.kcals),
                "immediate_outdoor_crops": np.array(
                    self.immediate_outdoor_crops_kcals_equivalent.kcals
                ),
                "new_stored_outdoor_crops": np.array(
                    self.new_stored_outdoor_crops_kcals_equivalent.kcals
                ),
                "stored_food": np.array(self.stored_food_kcals_equivalent.kcals),
            }

            df = pd.DataFrame(dict)

            # Save the dataframe
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
        This function takes in an object of extracted results and assigns the percentage of food fed to each category
        of food source. It then stores the results in the corresponding instance variables of the object.

        Args:
            self: The object instance
            extracted_results: The object of extracted results

        Returns:
            None
        """

        self.stored_food = (
            extracted_results.stored_food_to_humans.in_units_percent_fed()
        )

        self.outdoor_crops = (
            extracted_results.outdoor_crops_to_humans.in_units_percent_fed()
        )

        self.seaweed = extracted_results.seaweed_to_humans.in_units_percent_fed()

        self.cell_sugar = extracted_results.cell_sugar_to_humans.in_units_percent_fed()

        self.scp = extracted_results.scp_to_humans.in_units_percent_fed()

        self.greenhouse = extracted_results.greenhouse.in_units_percent_fed()
        self.fish = extracted_results.fish.in_units_percent_fed()
        self.culled_meat_plus_grazing_cattle_maintained = (
            extracted_results.culled_meat_plus_grazing_cattle_maintained.in_units_percent_fed()
        )
        self.grazing_milk = extracted_results.grazing_milk.in_units_percent_fed()
        self.grain_fed_meat = extracted_results.grain_fed_meat.in_units_percent_fed()
        self.grain_fed_milk = extracted_results.grain_fed_milk.in_units_percent_fed()
        self.immediate_outdoor_crops = (
            extracted_results.immediate_outdoor_crops.in_units_percent_fed()
        )
        self.new_stored_outdoor_crops = (
            extracted_results.new_stored_outdoor_crops.in_units_percent_fed()
        )

    def assign_kcals_equivalent_from_extractor(self, extracted_results):
        """
        Assigns the kcals equivalent of various food sources to their respective attributes.
        Args:
            self: instance of the class
            extracted_results: an instance of the ExtractedResults class containing the extracted results
        Returns:
            None
        """

        # Assign kcals equivalent of seaweed to seaweed_kcals_equivalent attribute
        self.seaweed_kcals_equivalent = (
            extracted_results.seaweed_to_humans.in_units_kcals_equivalent()
        )

        # Assign kcals equivalent of cell sugar to cell_sugar_kcals_equivalent attribute
        self.cell_sugar_kcals_equivalent = (
            extracted_results.cell_sugar_to_humans.in_units_kcals_equivalent()
        )

        # Assign kcals equivalent of scp to scp_kcals_equivalent attribute
        self.scp_kcals_equivalent = (
            extracted_results.scp_to_humans.in_units_kcals_equivalent()
        )
        # Assign kcals equivalent of greenhouse crops to greenhouse_kcals_equivalent attribute
        self.greenhouse_kcals_equivalent = (
            extracted_results.greenhouse.in_units_kcals_equivalent()
        )

        # Assign kcals equivalent of fish to fish_kcals_equivalent attribute
        self.fish_kcals_equivalent = extracted_results.fish.in_units_kcals_equivalent()

        # Assign kcals equivalent of culled meat plus grazing cattle maintained to culled_meat_plus_grazing_cattle_maintained_kcals_equivalent attribute
        self.culled_meat_plus_grazing_cattle_maintained_kcals_equivalent = (
            extracted_results.culled_meat_plus_grazing_cattle_maintained.in_units_kcals_equivalent()
        )

        # Assign kcals equivalent of grazing milk to grazing_milk_kcals_equivalent attribute
        self.grazing_milk_kcals_equivalent = (
            extracted_results.grazing_milk.in_units_kcals_equivalent()
        )

        # Assign kcals equivalent of grain fed meat to grain_fed_meat_kcals_equivalent attribute
        self.grain_fed_meat_kcals_equivalent = (
            extracted_results.grain_fed_meat.in_units_kcals_equivalent()
        )

        # Assign kcals equivalent of grain fed milk to grain_fed_milk_kcals_equivalent attribute
        self.grain_fed_milk_kcals_equivalent = (
            extracted_results.grain_fed_milk.in_units_kcals_equivalent()
        )

        # Assign kcals equivalent of immediate outdoor crops to immediate_outdoor_crops_kcals_equivalent attribute
        self.immediate_outdoor_crops_kcals_equivalent = (
            extracted_results.immediate_outdoor_crops.in_units_kcals_equivalent()
        )

        # Assign kcals equivalent of new stored outdoor crops to new_stored_outdoor_crops_kcals_equivalent attribute
        self.new_stored_outdoor_crops_kcals_equivalent = (
            extracted_results.new_stored_outdoor_crops.in_units_kcals_equivalent()
        )

    def set_to_humans_properties_kcals_equivalent(self, extracted_results):
        self.stored_food_to_humans_kcals_equivalent = (
            self.stored_food_to_humans.in_units_kcals_equivalent()
        )

        self.outdoor_crops_to_humans_kcals_equivalent = (
            self.outdoor_crops_to_humans.in_units_kcals_equivalent()
        )

        self.immediate_outdoor_crops_to_humans_kcals_equivalent = (
            self.immediate_outdoor_crops_to_humans.in_units_kcals_equivalent()
        )

        self.new_stored_outdoor_crops_to_humans_kcals_equivalent = (
            self.new_stored_outdoor_crops_to_humans.in_units_kcals_equivalent()
        )

    def assign_time_months_middle(self, NMONTHS):
        """
        Assigns the middle of each month to the time_months_middle list.
        Args:
            self (object): The object instance
            NMONTHS (int): The number of months to assign
        Returns:
            None
        """
        # Clear the list to start fresh
        self.time_months_middle = []

        # Loop through each month and append the middle of the month to the list
        for month in range(0, NMONTHS):
            # Add 0.5 to get the middle of the month
            middle_of_month = month + 0.5
            self.time_months_middle.append(middle_of_month)

    def assign_interpreted_properties(self, extracted_results):
        """
        Assigns interpreted properties to the object based on the extracted results.
        Args:
            self: the object to which the properties will be assigned
            extracted_results: the extracted results from which the properties will be derived
        Returns:
            None
        """
        # Get the sum of humans fed by adding to humans
        humans_fed_sum = self.get_sum_by_adding_to_humans()

        # Get the percentage of people fed and the constraining nutrient
        # based on the sum of humans fed
        (
            self.percent_people_fed,
            self.constraining_nutrient,
        ) = self.get_percent_people_fed(humans_fed_sum)
        self.excess_feed = extracted_results.excess_feed

        # Assign the kcals, fat, and protein fed properties from the sum of humans fed
        self.kcals_fed = humans_fed_sum.kcals
        self.fat_fed = humans_fed_sum.fat
        self.protein_fed = humans_fed_sum.protein

    def get_mean_min_nutrient(self):
        """
        Calculates the mean number of people fed in all months, assuming that stored food
        was not a constraint on the number of people fed. This is done by finding the minimum
        of any nutrient in any month and then getting the mean people fed in all the months.

        Returns:
            float: the mean people fed in all months
        """
        # Find the minimum of kcals_fed, fat_fed, and protein_fed for each month
        # and store the resulting array in min_fed
        min_fed = np.min([self.kcals_fed, self.fat_fed, self.protein_fed], axis=0)

        # Calculate the mean of the min_fed array to get the mean number of people fed
        # in all months
        mean_fed = np.mean(min_fed)

        # Return the mean number of people fed in all months
        return mean_fed

    def get_sum_by_adding_to_humans(self):
        """
        Sums the resulting nutrients from the extracted_results and returns the total.

        Args:
            self: An instance of the class containing the extracted_results.

        Returns:
            float: The total sum of nutrients from the extracted_results.

        Example:
            >>> instance = Interpreter()
            >>> instance.get_sum_by_adding_to_humans()
            100.0
        """

        # Sum the extracted_results to get the total nutrients for humans.
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
            + self.grain_fed_meat
            + self.grain_fed_milk
        )

        # Return the total sum of nutrients for humans.
        return to_humans_fed_sum

    def print_kcals_per_capita_per_day(self, interpreted_results):
        """
        This function calculates and prints the expected kcals/capita/day for a given scenario result.

        Args:
            interpreted_results (InterpretedResults): An instance of the InterpretedResults class containing the
            interpreted results of a scenario.

        Returns:
            None
        """

        # Calculate the ratio of people fed to total population
        needs_ratio = interpreted_results.percent_people_fed / 100

        # Calculate and print the expected kcals/capita/day
        print("Expected kcals/capita/day")
        print(needs_ratio * 2100)
        print("")

    def get_percent_people_fed(self, humans_fed_sum):
        """
        Calculates the estimated percentage of people fed based on the minimum nutrients required to meet the needs of the population in any month, for kcals, fat, and protein.

        Args:
            humans_fed_sum (HumanFedSum): An instance of the HumanFedSum class that contains the total amount of nutrients fed to the population.

        Returns:
            list: A list containing the estimated percentage of people fed and the minimum nutrients required to meet their needs.

        Raises:
            AssertionError: If the input argument is not an instance of the HumanFedSum class.

        """
        assert isinstance(
            humans_fed_sum, HumanFedSum
        ), "Input argument must be an instance of the HumanFedSum class."

        # Get the minimum nutrients required to meet the needs of the population
        (min_nutrient, percent_people_fed) = humans_fed_sum.get_min_nutrient()

        # Print the nutrients with constraining values and the estimated percentage of people fed if PRINT_FED is True
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

    def get_increased_excess_to_feed(
        self,
        feed_delay,
        percent_fed,
    ):
        """
        Calculates the excess feed to be added to the diet at a consistent percentage
        in the months of interest (months to calculate diet). The amount of human
        edible feed used can't be more than the excess calories. Because the baseline
        feed usage is higher than in nuclear winter, we don't want to increase feed
        usage before the shutoff.

        Args:
            feed_delay (int): the number of months before the shutoff
            percent_fed (float): the percentage of the population that is fed

        Returns:
            excess_per_month (numpy.ndarray): kcals per month, units percent
        """

        # these months are used to estimate the diet before the full scale-up of
        # resilient foods makes there be way too much food to make sense economically
        N_MONTHS_TO_CALCULATE_DIET = 49

        # rapidly feed more to people until it's close to 2100 kcals, then
        # slowly feed more to people
        SMALL_INCREASE_IN_EXCESS = 0.1
        LARGE_INCREASE_IN_EXCESS = 1.0

        # Get the excess feed per month
        excess_per_month_percent = self.excess_feed.kcals

        # Get the baseline feed usage before the shutoff
        baseline_feed = excess_per_month_percent[:feed_delay]

        # Get the part of the excess feed to leave unchanged
        part_at_end_to_leave_unchanged = excess_per_month_percent[
            N_MONTHS_TO_CALCULATE_DIET:
        ]

        # Get the excess feed after the shutoff
        after_shutoff_feed = excess_per_month_percent[
            feed_delay:N_MONTHS_TO_CALCULATE_DIET
        ]

        # Determine the additional excess to add based on the percentage of the population fed
        if percent_fed < 106 and percent_fed > 100:
            additional_excess_to_add_percent = np.linspace(
                SMALL_INCREASE_IN_EXCESS,
                SMALL_INCREASE_IN_EXCESS,
                N_MONTHS_TO_CALCULATE_DIET - feed_delay,
            )
        else:
            additional_excess_to_add_percent = np.linspace(
                LARGE_INCREASE_IN_EXCESS,
                LARGE_INCREASE_IN_EXCESS,
                N_MONTHS_TO_CALCULATE_DIET - feed_delay,
            )

        # Ensure the length of the additional excess array matches the length of the after shutoff feed array
        assert len(additional_excess_to_add_percent) == len(after_shutoff_feed)

        # Add the additional excess to the excess feed after the shutoff
        new_excess_kcals = after_shutoff_feed + additional_excess_to_add_percent

        # Combine the baseline feed, new excess feed, and unchanged excess feed
        excess_per_month = np.append(
            np.append(baseline_feed, new_excess_kcals),
            part_at_end_to_leave_unchanged,
        )

        return excess_per_month

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
        Sums together the results from many different runs of the model and creates a new object summing the results.
        Args:
            many_results (dict): a dictionary containing the results of many different runs of the model
            cap_at_100_percent (bool): a boolean indicating whether to cap the results at 100 percent
        Returns:
            Interpreter: the interpreter object with the summed results divided by the population in question
        """

        # initialize variables
        i = 0
        net_pop = 0
        previous_interpreter = []

        # loop through each country's interpreter object
        for country, interpreter in many_results.items():
            # record some useful values for plotting from the interpreter
            # will check later that these are consistent
            include_fat = interpreter.include_fat
            include_protein = interpreter.include_protein
            time_months_middle = interpreter.time_months_middle

            # get constants from interpreter object
            ADD_FISH = interpreter.constants["ADD_FISH"]
            ADD_CELLULOSIC_SUGAR = interpreter.constants["ADD_CELLULOSIC_SUGAR"]
            ADD_METHANE_SCP = interpreter.constants["ADD_METHANE_SCP"]
            ADD_GREENHOUSES = interpreter.constants["ADD_GREENHOUSES"]
            ADD_SEAWEED = interpreter.constants["ADD_SEAWEED"]
            ADD_MILK = interpreter.constants["ADD_MILK"]
            ADD_CULLED_MEAT = interpreter.constants["ADD_CULLED_MEAT"]
            ADD_MAINTAINED_MEAT = interpreter.constants["ADD_MAINTAINED_MEAT"]
            ADD_OUTDOOR_GROWING = interpreter.constants["ADD_OUTDOOR_GROWING"]
            ADD_STORED_FOOD = interpreter.constants["ADD_STORED_FOOD"]

            # calculate population
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

            # get values for each food source
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
            grain_fed_milk = (
                interpreter.grain_fed_milk.in_units_bil_kcals_thou_tons_thou_tons_per_month()
            )
            cmpgcm = interpreter.culled_meat_plus_grazing_cattle_maintained
            culled_meat_plus_grazing_cattle_maintained = (
                cmpgcm.in_units_bil_kcals_thou_tons_thou_tons_per_month()
            )
            grain_fed_meat = (
                interpreter.grain_fed_meat.in_units_bil_kcals_thou_tons_thou_tons_per_month()
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
                grain_fed_milk = grain_fed_milk * ratio_so_adds_to_100_percent
                culled_meat_plus_grazing_cattle_maintained = (
                    culled_meat_plus_grazing_cattle_maintained
                    * ratio_so_adds_to_100_percent
                )
                grain_fed_meat = grain_fed_meat * ratio_so_adds_to_100_percent
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
                grain_fed_milk_cumulative = grain_fed_milk
                culled_meat_plus_grazing_cattle_maintained_cumulative = (
                    culled_meat_plus_grazing_cattle_maintained
                )
                grain_fed_meat_cumulative = grain_fed_meat
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
                    ADD_MAINTAINED_MEAT
                    == previous_interpreter.constants["ADD_MAINTAINED_MEAT"]
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
                grain_fed_milk_cumulative = grain_fed_milk_cumulative + grain_fed_milk
                culled_meat_plus_grazing_cattle_maintained_cumulative = (
                    culled_meat_plus_grazing_cattle_maintained_cumulative
                    + culled_meat_plus_grazing_cattle_maintained
                )
                grain_fed_meat_cumulative = grain_fed_meat_cumulative + grain_fed_meat
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
            + grain_fed_milk_cumulative.in_units_percent_fed()
            + culled_meat_plus_grazing_cattle_maintained_cumulative.in_units_percent_fed()
            + grain_fed_meat_cumulative.in_units_percent_fed()
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
        global_results.constants["ADD_MAINTAINED_MEAT"] = ADD_MAINTAINED_MEAT
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
        global_results.grain_fed_milk_kcals_equivalent = (
            grain_fed_milk_cumulative.in_units_percent_fed().in_units_kcals_equivalent()
        )
        global_results.culled_meat_plus_grazing_cattle_maintained_kcals_equivalent = (
            culled_meat_plus_grazing_cattle_maintained_cumulative.in_units_percent_fed().in_units_kcals_equivalent()
        )
        global_results.grain_fed_meat_kcals_equivalent = (
            grain_fed_meat_cumulative.in_units_percent_fed().in_units_kcals_equivalent()
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
