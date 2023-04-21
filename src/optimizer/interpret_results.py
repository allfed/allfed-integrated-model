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

    def interpret_results(self, extracted_results):
        """
        This function takes the raw output of the optimizer food categories and total
        people fed in list form, and converts the naive people fed which includes
        negative feed, into a purely list of values, where the negative feed has been
        subtracted from the sum of outdoor growing and stored food.

        ANYTHING assigned to "self" here is part of a useful result that will either
        be printed or plotted as a result

        """

        self.assign_percent_fed_from_extractor(extracted_results)
        self.assign_kcals_equivalent_from_extractor(extracted_results)

        # now the same, but in units effective kcals per day
        # all these are just used for plotting only

        self.constants = extracted_results.constants
        self.assign_time_months_middle(self.constants["NMONTHS"])

        self.assign_interpreted_properties(extracted_results)

        self.include_fat = Food.conversions.include_fat
        self.include_protein = Food.conversions.include_protein

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

            # saving the dataframe
            # df.to_csv("ykcals" + self.constants["scenario_name"] + ".csv")
            year = str(date.today().year)
            month = str(date.today().month)
            day = str(date.today().day)
            hour = str(datetime.datetime.now().hour)
            minute = str(datetime.datetime.now().minute)
            second = str(datetime.datetime.now().second)
            df.to_csv(
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

        return self

    def assign_percent_fed_from_extractor(self, extracted_results):
        self.stored_food = extracted_results.stored_food.in_units_percent_fed()

        self.outdoor_crops = extracted_results.outdoor_crops.in_units_percent_fed()

        self.seaweed = extracted_results.seaweed.in_units_percent_fed()

        self.cell_sugar = extracted_results.cell_sugar.in_units_percent_fed()

        self.scp = extracted_results.scp.in_units_percent_fed()

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
        self.stored_food_kcals_equivalent = self.stored_food.in_units_kcals_equivalent()

        self.outdoor_crops_kcals_equivalent = (
            self.outdoor_crops.in_units_kcals_equivalent()
        )

        self.seaweed_kcals_equivalent = (
            extracted_results.seaweed.in_units_kcals_equivalent()
        )
        self.cell_sugar_kcals_equivalent = (
            extracted_results.cell_sugar.in_units_kcals_equivalent()
        )

        self.scp_kcals_equivalent = extracted_results.scp.in_units_kcals_equivalent()

        self.greenhouse_kcals_equivalent = (
            extracted_results.greenhouse.in_units_kcals_equivalent()
        )

        self.fish_kcals_equivalent = extracted_results.fish.in_units_kcals_equivalent()

        self.culled_meat_plus_grazing_cattle_maintained_kcals_equivalent = (
            extracted_results.culled_meat_plus_grazing_cattle_maintained.in_units_kcals_equivalent()
        )

        self.grazing_milk_kcals_equivalent = (
            extracted_results.grazing_milk.in_units_kcals_equivalent()
        )

        self.grain_fed_meat_kcals_equivalent = (
            extracted_results.grain_fed_meat.in_units_kcals_equivalent()
        )

        self.grain_fed_milk_kcals_equivalent = (
            extracted_results.grain_fed_milk.in_units_kcals_equivalent()
        )

        self.immediate_outdoor_crops_kcals_equivalent = (
            self.immediate_outdoor_crops.in_units_kcals_equivalent()
        )

        self.new_stored_outdoor_crops_kcals_equivalent = (
            self.new_stored_outdoor_crops.in_units_kcals_equivalent()
        )

    def assign_time_months_middle(self, NMONTHS):
        self.time_months_middle = []
        for month in range(0, NMONTHS):
            self.time_months_middle.append(month + 0.5)

    def assign_interpreted_properties(self, extracted_results):
        humans_fed_sum = self.get_sum_by_adding_to_humans()

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

        self.excess_feed = extracted_results.excess_feed

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
        sum the resulting nutrients from the extracted_results

        """

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

        return to_humans_fed_sum

    def print_kcals_per_capita_per_day(self, interpreted_results):
        """
        This function prints the ratio of needs to actual needs for a given scenario
        result.
        """

        needs_ratio = interpreted_results.percent_people_fed / 100

        print("Expected kcals/capita/day")
        print(needs_ratio * 2100)
        print("")

    def get_percent_people_fed(self, humans_fed_sum):
        """
        get the minimum nutrients required to meet the needs of the population
         in any month, for kcals, fat, and protein
        """
        assert humans_fed_sum.is_units_percent()
        (min_nutrient, percent_people_fed) = humans_fed_sum.get_min_nutrient()

        PRINT_FED = False
        if PRINT_FED:
            print("Nutrients with constraining values are: " + str(min_nutrient))
            print(
                "Estimated percent people fed is "
                + str(round(percent_people_fed, 1))
                + "%"
            )
        return [percent_people_fed, min_nutrient]

    def correct_and_validate_rounding_errors(self):
        """
        any round error we might expect to be very small and easily fixable is corrected
        here. "small" is with respect to percent people fed

        Note: outdoor_crops_to_humans, stored_food, and seaweed are the only actual outputs of
              the optimizer!
        """
        assert (
            self.stored_food.NMONTHS
            == self.outdoor_crops.NMONTHS
            == self.immediate_outdoor_crops.NMONTHS
            == self.new_stored_outdoor_crops.NMONTHS
            == self.seaweed.NMONTHS
        )

        assert self.stored_food.is_units_percent()
        assert self.outdoor_crops.is_units_percent()
        assert self.immediate_outdoor_crops.is_units_percent()
        assert self.new_stored_outdoor_crops.is_units_percent()
        assert self.seaweed.is_units_percent()

        stored_food_rounded = self.stored_food.get_rounded_to_decimal(3)
        outdoor_crops_rounded = self.outdoor_crops.get_rounded_to_decimal(3)
        seaweed_rounded = self.seaweed.get_rounded_to_decimal(3)

        immediate_outdoor_crops_rounded = (
            self.immediate_outdoor_crops.get_rounded_to_decimal(3)
        )
        new_stored_outdoor_crops_rounded = (
            self.new_stored_outdoor_crops.get_rounded_to_decimal(3)
        )

        # if the value was a little less than zero, when rounded it would no longer be
        # less than zero.

        assert stored_food_rounded.all_greater_than_or_equal_to_zero()
        assert seaweed_rounded.all_greater_than_or_equal_to_zero()
        assert outdoor_crops_rounded.all_greater_than_or_equal_to_zero()
        assert immediate_outdoor_crops_rounded.all_greater_than_or_equal_to_zero()
        assert new_stored_outdoor_crops_rounded.all_greater_than_or_equal_to_zero()

        return (
            stored_food_rounded,
            outdoor_crops_rounded,
            immediate_outdoor_crops_rounded,
            new_stored_outdoor_crops_rounded,
            seaweed_rounded,
        )

    def get_increased_excess_to_feed(
        self,
        feed_delay,
        percent_fed,
    ):
        """
        when calculating the excess calories, the amount of human edible feed
        used can't be more than the excess calories. Because the baseline feed
        usage is higher than in nuclear winter, we don't want to increase
        feed usage before the shutoff.

        this function adds an additional amount of excess at a consistent percentage
        in the months of interest (months to calculate diet)
        """

        # these months are used to estimate the diet before the full scale-up of
        # resilient foods makes there be way too much food to make sense economically
        N_MONTHS_TO_CALCULATE_DIET = 49

        # rapidly feed more to people until it's close to 2100 kcals, then
        # slowly feed more to people
        SMALL_INCREASE_IN_EXCESS = 0.1
        LARGE_INCREASE_IN_EXCESS = 1.0

        excess_per_month_percent = self.excess_feed.kcals

        baseline_feed = excess_per_month_percent[:feed_delay]

        part_at_end_to_leave_unchanged = excess_per_month_percent[
            N_MONTHS_TO_CALCULATE_DIET:
        ]

        after_shutoff_feed = excess_per_month_percent[
            feed_delay:N_MONTHS_TO_CALCULATE_DIET
        ]

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

        assert len(additional_excess_to_add_percent) == len(after_shutoff_feed)

        # don't add any additional feed before the shutoff, that's already at
        # baseline feed levels
        new_excess_kcals = after_shutoff_feed + additional_excess_to_add_percent

        excess_per_month = np.append(
            np.append(baseline_feed, new_excess_kcals),
            part_at_end_to_leave_unchanged,
        )

        # kcals per month, units percent
        return excess_per_month

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
            ADD_MAINTAINED_MEAT = interpreter.constants["ADD_MAINTAINED_MEAT"]
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
                interpreter.immediate_outdoor_crops.in_units_bil_kcals_thou_tons_thou_tons_per_month()
            )
            new_stored_outdoor_crops = (
                interpreter.new_stored_outdoor_crops.in_units_bil_kcals_thou_tons_thou_tons_per_month()
            )
            stored_food = (
                interpreter.stored_food.in_units_bil_kcals_thou_tons_thou_tons_per_month()
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
        global_results.immediate_outdoor_crops_kcals_equivalent = (
            immediate_outdoor_crops_cumulative.in_units_percent_fed().in_units_kcals_equivalent()
        )
        global_results.new_stored_outdoor_crops_kcals_equivalent = (
            new_stored_outdoor_crops_cumulative.in_units_percent_fed().in_units_kcals_equivalent()
        )
        global_results.stored_food_kcals_equivalent = (
            stored_food_cumulative.in_units_percent_fed().in_units_kcals_equivalent()
        )
        return global_results
