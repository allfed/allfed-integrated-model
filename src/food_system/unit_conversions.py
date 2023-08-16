#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

The idea here is that the code is constantly creating objects with calories, fat, and
protein separately then passing these objects around to other places, so we might as
well create a class which has these 3 properties.

Note that occasionally, this class is instantiated with each nutrient set as an array
where each element of the array is a different month of the simulation, and the total
number of months is NMONTHS, which is also the length of each of the 3 arrays.

Created on Tue Jul 19

@author: morgan
"""
import os
import sys

module_path = os.path.abspath(os.path.join("../.."))
if module_path not in sys.path:
    sys.path.append(module_path)


class UnitConversions:
    """
    This class is used to convert units of nutrients
    """

    def __init__(self):
        self.NUTRITION_PROPERTIES_ASSIGNED = False

    # getters and setters

    def set_nutrition_requirements(
        self,
        kcals_daily,
        fat_daily,
        protein_daily,
        include_fat,
        include_protein,
        population,
    ):
        """
        Returns the macronutrients of the food.

        This is a bit of a confusing function.

        It is normally run from a UnitConversions class in the Food child class

        that Food class contains one UnitConversions object which has had its nutrients
        assigned.

        Then, because this is the parent class, all the functions are inherited.

        So, running get_conversions() (the class function to get the conversions object
        in the child food class), this will obtain all the conversion data instantiated
        through the Food class.
        """

        self.days_in_month = 30

        self.include_fat = include_fat
        self.include_protein = include_protein
        self.exclude_fat = not include_fat
        self.exclude_protein = not include_protein

        self.kcals_daily = kcals_daily
        self.fat_daily = fat_daily
        self.protein_daily = protein_daily

        # kcals per person
        self.kcals_monthly = kcals_daily * self.days_in_month

        # in thousands of tons (grams per ton == 1e6) per month
        self.fat_monthly = fat_daily / 1e6 * self.days_in_month / 1000

        # in thousands of tons (grams per ton == 1e6) per month per person
        self.protein_monthly = protein_daily / 1e6 * self.days_in_month / 1000

        # in billions of kcals per month for population
        self.billion_kcals_needed = self.kcals_monthly * population / 1e9
        # in thousands of tons per month for population
        self.thou_tons_fat_needed = self.fat_monthly * population
        # in thousands of tons per month for population
        self.thou_tons_protein_needed = self.protein_monthly * population

        self.population = population

        self.NUTRITION_PROPERTIES_ASSIGNED = True

    def get_units_from_list_to_total(self):
        """
        gets the units so that they reflect that of a single month
        """
        # Make sure this only happens for monthly food
        assert "each month" in self.kcals_units
        assert "each month" in self.fat_units
        assert "each month" in self.protein_units

        # remove the " each month" part of the units
        kcals_units = self.kcals_units.split(" each month")[0]

        # remove the " each month" part of the units
        fat_units = self.fat_units.split(" each month")[0]

        # remove the " each month" part of the units
        protein_units = self.protein_units.split(" each month")[0]

        return [kcals_units, fat_units, protein_units]

    def set_units_from_list_to_total(self):
        """
        sets the units so that they reflect that of a single month
        """
        # Make sure this only happens for monthly food
        assert "each month" in self.kcals_units
        assert "each month" in self.fat_units
        assert "each month" in self.protein_units
        # remove the " each month" part of the units
        [
            self.kcals_units,
            self.fat_units,
            self.protein_units,
        ] = self.get_units_from_list_to_total()

        self.units = [self.kcals_units, self.fat_units, self.protein_units]

    def get_units_from_list_to_element(self):
        """
        gets the units so that they reflect that of a single month
        """
        # Make sure this only happens for monthly food
        assert "each month" in self.kcals_units
        assert "each month" in self.fat_units
        assert "each month" in self.protein_units

        # replace the " each month" part of the units with "per month"
        kcals_units = self.kcals_units.replace(" each month", " per month")

        # replace the " each month" part of the units with "per month"
        fat_units = self.fat_units.replace(" each month", " per month")

        # replace the " each month" part of the units with "per month"
        protein_units = self.protein_units.replace(" each month", " per month")

        return [kcals_units, fat_units, protein_units]

    def set_units_from_list_to_element(self):
        """
        sets the units so that they reflect that of a single month
        """
        # Make sure this only happens for monthly food
        assert "each month" in self.kcals_units
        assert "each month" in self.fat_units
        assert "each month" in self.protein_units
        [
            self.kcals_units,
            self.fat_units,
            self.protein_units,
        ] = self.get_units_from_list_to_element()

    def get_units_from_element_to_list(self):
        """
        gets the units so that they reflect that of a list of months
        """
        assert "each month" not in self.kcals_units
        assert "each month" not in self.fat_units
        assert "each month" not in self.protein_units
        # add " each month" to units to signify a food list
        kcals_units = self.kcals_units + " each month"

        # add " each month" to units to signify a food list
        fat_units = self.fat_units + " each month"

        # add " each month" to units to signify a food list
        protein_units = self.protein_units + " each month"

        return [kcals_units, fat_units, protein_units]

    def set_units_from_element_to_list(self):
        """
        sets the units so that they reflect that of a list of months
        """
        assert "each month" not in self.kcals_units
        assert "each month" not in self.fat_units
        assert "each month" not in self.protein_units
        [
            self.kcals_units,
            self.fat_units,
            self.protein_units,
        ] = self.get_units_from_element_to_list()

    def get_units(self):
        """
        update and return the unit values as a 3 element array
        """
        self.units = [self.kcals_units, self.fat_units, self.protein_units]

        return self.units

    def set_units(self, kcals_units, fat_units, protein_units):
        """
        Sets the units of the food (for example, billion_kcals,thousand_tons, dry
        caloric tons, kcals/capita/day, or percent of global food supply).
        default units are billion kcals, thousand tons fat, thousand tons protein
        For convenience and as a memory tool, set the units, and make sure that whenever
        an operation on a different food is used, the units are compatible

        """
        # Make sure this can only happen for monthly food if "each month" is in the units
        self.kcals_units = kcals_units
        self.fat_units = fat_units
        self.protein_units = protein_units

        self.units = [kcals_units, fat_units, protein_units]

    # examine properties of units

    def print_units(self):
        """
        Prints the units of the nutrients
        """
        print("    kcals: ", self.kcals_units)
        if self.conversions.include_fat:
            print("    fat: ", self.fat_units)
        if self.conversions.include_protein:
            print("    protein: ", self.protein_units)

    def is_a_ratio(self):
        """
        Returns if units are all "ratio" type
        """

        if (
            "ratio" in self.kcals_units
            and "ratio" in self.fat_units
            and "ratio" in self.protein_units
        ):
            return True
        else:
            return False

    def is_units_percent(self):
        """
        Returns if units are all "percent" type
        """
        if (
            "percent" in self.kcals_units
            and "percent" in self.fat_units
            and "percent" in self.protein_units
        ):
            return True
        else:
            return False

    # CONVERSIONS BETWEEN UNITS

    def in_units_billions_fed(self):
        """
        If the existing units are understood by this function, it tries to convert the
        values and units to billions of people fed.
        """
        # @Morgan: Is there a reason this is done as if,if,if and not as if,elif,else?

        # getting this instance of the UnitConversions from the child class
        conversions = self.get_conversions()

        # okay, okay, maybe the way I did this child/parent thing is not ideal...
        # get the child class so can initialize the Food class
        Food = self.get_Food_class()
        billion_kcal_conversion = 1 / conversions.kcals_monthly
        thou_tons_fat_conversion = 1 / conversions.fat_monthly / 1e9
        thou_tons_protein_conversion = 1 / conversions.protein_monthly / 1e9

        if (
            self.kcals_units == "billion kcals each month"
            and self.fat_units == "thousand tons each month"
            and self.protein_units == "thousand tons each month"
        ):
            return Food(
                kcals=self.kcals * billion_kcal_conversion,
                fat=self.fat * thou_tons_fat_conversion,
                protein=self.protein * thou_tons_protein_conversion,
                kcals_units="billion people fed each month",
                fat_units="billion people fed each month",
                protein_units="billion people fed each month",
            )

        if (
            self.kcals_units == "billion kcals per month"
            and self.fat_units == "thousand tons per month"
            and self.protein_units == "thousand tons per month"
        ):
            return Food(
                kcals=self.kcals * billion_kcal_conversion,
                fat=self.fat * thou_tons_fat_conversion,
                protein=self.protein * thou_tons_protein_conversion,
                kcals_units="billion people fed per month",
                fat_units="billion people fed per month",
                protein_units="billion people fed per month",
            )

        percent_people_kcal_conversion = conversions.population / 1e9 / 100
        percent_people_fat_conversion = conversions.population / 1e9 / 100
        percent_people_protein_conversion = conversions.population / 1e9 / 100

        if (
            self.kcals_units == "percent people fed per month"
            and self.fat_units == "percent people fed per month"
            and self.protein_units == "percent people fed per month"
        ):
            return Food(
                kcals=self.kcals * percent_people_kcal_conversion,
                fat=self.fat * percent_people_fat_conversion,
                protein=self.protein * percent_people_protein_conversion,
                kcals_units="billion people fed per month",
                fat_units="billion people fed per month",
                protein_units="billion people fed per month",
            )
        if (
            self.kcals_units == "percent people fed per month"
            and self.fat_units == "percent people fed per month"
            and self.protein_units == "percent people fed per month"
        ):
            return Food(
                kcals=self.kcals * percent_people_kcal_conversion,
                fat=self.fat * percent_people_fat_conversion,
                protein=self.protein * percent_people_protein_conversion,
                kcals_units="billion people fed per month",
                fat_units="billion people fed per month",
                protein_units="billion people fed per month",
            )
        else:
            print("Error: conversion from these units not known")
            print("From units:")
            self.print_units()
            print("To units:")
            print("    kcals: billion people fed per/each month")
            print("    fat: billion people fed per/each month")
            print("    protein: billion people fed per/each month")
            success = False
            assert success

    def in_units_percent_fed(self):
        """
        If the existing units are understood by this function, it tries to convert the
        values and units to percent of people fed.
        """

        # getting this instance of the UnitConversions from the child class
        conversions = self.get_conversions()

        # okay, okay, maybe the way I did this child/parent thing is not ideal...
        # get the child class so can initialize the Food class
        Food = self.get_Food_class()

        billion_people_kcal_conversion = 100 / conversions.population * 1e9
        billion_people_fat_conversion = 100 / conversions.population * 1e9
        billion_people_protein_conversion = 100 / conversions.population * 1e9

        if (
            self.kcals_units == "billion people fed each month"
            and self.fat_units == "billion people fed each month"
            and self.protein_units == "billion people fed each month"
        ):
            return Food(
                kcals=self.kcals * billion_people_kcal_conversion,
                fat=self.fat * billion_people_fat_conversion,
                protein=self.protein * billion_people_protein_conversion,
                kcals_units="percent people fed each month",
                fat_units="percent people fed each month",
                protein_units="percent people fed each month",
            )
        if (
            self.kcals_units == "billion people fed per month"
            and self.fat_units == "billion people fed per month"
            and self.protein_units == "billion people fed per month"
        ):
            return Food(
                kcals=self.kcals * billion_people_kcal_conversion,
                fat=self.fat * billion_people_fat_conversion,
                protein=self.protein * billion_people_protein_conversion,
                kcals_units="percent people fed per month",
                fat_units="percent people fed per month",
                protein_units="percent people fed per month",
            )

        billion_kcal_conversion = 100 / conversions.billion_kcals_needed
        thou_tons_fat_conversion = 100 / conversions.thou_tons_fat_needed
        thou_tons_protein_conversion = 100 / conversions.thou_tons_protein_needed

        if (
            self.kcals_units == "billion kcals each month"
            and self.fat_units == "thousand tons each month"
            and self.protein_units == "thousand tons each month"
        ):
            return Food(
                kcals=self.kcals * billion_kcal_conversion,
                fat=self.fat * thou_tons_fat_conversion,
                protein=self.protein * thou_tons_protein_conversion,
                kcals_units="percent people fed each month",
                fat_units="percent people fed each month",
                protein_units="percent people fed each month",
            )

        if (
            self.kcals_units == "billion kcals per month"
            and self.fat_units == "thousand tons per month"
            and self.protein_units == "thousand tons per month"
        ):
            return Food(
                kcals=self.kcals * billion_kcal_conversion,
                fat=self.fat * thou_tons_fat_conversion,
                protein=self.protein * thou_tons_protein_conversion,
                kcals_units="percent people fed per month",
                fat_units="percent people fed per month",
                protein_units="percent people fed per month",
            )
        else:
            print("Error: conversion from these units not known")
            print("From units:")
            self.print_units()
            print("To units:")
            print("    kcals: percent people fed per/each month")
            print("    fat: percent people fed per/each month")
            print("    protein: percent people fed per/each month")
            success = False
            assert success

    def in_units_bil_kcals_thou_tons_thou_tons_per_month(self):
        """
        If the existing units are understood by this function, it tries to convert the
        values and units to percent of people fed.
        """

        # getting this instance of the UnitConversions from the child class
        conversions = self.get_conversions()

        # okay, okay, maybe the way I did this child/parent thing is not ideal...
        # get the child class so can initialize the Food class
        Food = self.get_Food_class()

        # million dry caloric tons to billion calories
        million_tons_to_billion_kcals_conversion = 1e6 * 1000 * 4000 / 1e9

        percent_kcal_conversion = (
            conversions.kcals_monthly * conversions.population / 1e9 / 100
        )
        percent_fat_conversion = conversions.fat_monthly * conversions.population / 100
        percent_protein_conversion = (
            conversions.protein_monthly * conversions.population / 100
        )

        if (
            self.kcals_units == "percent people fed each month"
            and self.fat_units == "percent people fed each month"
            and self.protein_units == "percent people fed each month"
        ):
            return Food(
                kcals=self.kcals * percent_kcal_conversion,
                fat=self.fat * percent_fat_conversion,
                protein=self.protein * percent_protein_conversion,
                kcals_units="billion kcals each month",
                fat_units="thousand tons each month",
                protein_units="thousand tons each month",
            )

        if (
            self.kcals_units == "percent people fed per month"
            and self.fat_units == "percent people fed per month"
            and self.protein_units == "percent people fed per month"
        ):
            return Food(
                kcals=self.kcals * percent_kcal_conversion,
                fat=self.fat * percent_fat_conversion,
                protein=self.protein * percent_protein_conversion,
                kcals_units="billion kcals per month",
                fat_units="thousand tons per month",
                protein_units="thousand tons per month",
            )
        if (
            self.kcals_units == "million dry caloric tons each month"
            and self.fat_units == "million tons each month"
            and self.protein_units == "million tons each month"
        ):
            return Food(
                kcals=self.kcals * million_tons_to_billion_kcals_conversion,
                fat=self.fat * 1000,
                protein=self.protein * 1000,
                kcals_units="billion kcals each month",
                fat_units="thousand tons each month",
                protein_units="thousand tons each month",
            )
        if (
            self.kcals_units == "million dry caloric tons"
            and self.fat_units == "million tons"
            and self.protein_units == "million tons"
        ):
            return Food(
                kcals=self.kcals * million_tons_to_billion_kcals_conversion,
                fat=self.fat * 1000,
                protein=self.protein * 1000,
                kcals_units="billion kcals",
                fat_units="thousand tons",
                protein_units="thousand tons",
            )
        else:
            print("Error: conversion from these units not known")
            print("From units:")
            self.print_units()
            print("To units:")
            print("    kcals: billion kcals per/each month")
            print("    fat: thousand tons per/each month")
            print("    protein: thousand tons per/each month")
            success = False
            assert success

    def in_units_kcals_equivalent(self):
        """
        If the existing units are understood by this function, it tries to convert the
        values and units to effective kcals per capita per day for each nutrient.
        """

        # getting this instance of the UnitConversions from the child class
        conversions = self.get_conversions()

        # okay, okay, maybe the way I did this child/parent thing is not ideal...
        # get the child class so can initialize the Food class
        Food = self.get_Food_class()

        billion_people_kcal_conversion = (
            1e9 / conversions.population * conversions.kcals_daily
        )
        billion_people_fat_conversion = (
            1e9 / conversions.population * conversions.kcals_daily
        )
        billion_people_protein_conversion = (
            1e9 / conversions.population * conversions.kcals_daily
        )

        if (
            self.kcals_units == "billion people fed each month"
            and self.fat_units == "billion people fed each month"
            and self.protein_units == "billion people fed each month"
        ):
            return Food(
                kcals=self.kcals * billion_people_kcal_conversion,
                fat=self.fat * billion_people_fat_conversion,
                protein=self.protein * billion_people_protein_conversion,
                kcals_units="kcals per capita per day each month",
                fat_units="effective kcals per capita per day each month",
                protein_units="effective kcals per capita per day each month",
            )
        if (
            self.kcals_units == "billion people fed per month"
            and self.fat_units == "billion people fed per month"
            and self.protein_units == "billion people fed per month"
        ):
            return Food(
                kcals=self.kcals * billion_people_kcal_conversion,
                fat=self.fat * billion_people_fat_conversion,
                protein=self.protein * billion_people_protein_conversion,
                kcals_units="kcals per capita per day per month",
                fat_units="effective kcals per capita per day per month",
                protein_units="effective kcals per capita per day per month",
            )

        percent_kcal_conversion = conversions.kcals_daily / 100
        percent_fat_conversion = conversions.kcals_daily / 100
        percent_protein_conversion = conversions.kcals_daily / 100

        if (
            self.kcals_units == "percent people fed each month"
            and self.fat_units == "percent people fed each month"
            and self.protein_units == "percent people fed each month"
        ):
            return Food(
                kcals=self.kcals * percent_kcal_conversion,
                fat=self.fat * percent_fat_conversion,
                protein=self.protein * percent_protein_conversion,
                kcals_units="kcals per capita per day each month",
                fat_units="effective kcals per capita per day each month",
                protein_units="effective kcals per capita per day each month",
            )
        if (
            self.kcals_units == "percent people fed per month"
            and self.fat_units == "percent people fed per month"
            and self.protein_units == "percent people fed per month"
        ):
            return Food(
                kcals=self.kcals * percent_kcal_conversion,
                fat=self.fat * percent_fat_conversion,
                protein=self.protein * percent_protein_conversion,
                kcals_units="kcals per capita per day per month",
                fat_units="effective kcals per capita per day per month",
                protein_units="effective kcals per capita per day per month",
            )
        else:
            print("Error: conversion from these units not known")
            print("From units:")
            self.print_units()
            print("To units:")
            print("    kcals: kcals per capita per day per/each month")
            print("    effective fat: kcals per capita per day per/each month")
            print("    effective protein: kcals per capita per day per/each month")
            success = False
            assert success

    def in_units_kcals_grams_grams_per_capita_from_ratio(
        self, kcal_ratio, fat_ratio, protein_ratio
    ):
        """
        If the existing units are understood by this function, it tries to convert the
        values and units to kcals per person per day, grams per pseron per day, kcals
        per person per day.
        arguments:
            kcal ratio (float): kcal  per kg of the food being converted
            fat ratio (float): grams per kcal of the food being converted
            kcal ratio (float): grams per kcal of the food being converted

        """

        # getting this instance of the UnitConversions from the child class
        # allows us to get some previously set values like kcals monthly and days in
        # month
        conversions = self.get_conversions()

        # okay, okay, maybe the way I did this child/parent thing is not ideal...
        # get the child class so can initialize the Food class
        Food = self.get_Food_class()

        billion_kcal_conversion = (
            1e9 / conversions.days_in_month / conversions.population * kcal_ratio
        )
        thou_tons_fat_conversion = billion_kcal_conversion * fat_ratio
        thou_tons_protein_conversion = billion_kcal_conversion * protein_ratio

        if (
            self.kcals_units == "billion kcals each month"
            and self.fat_units == "thousand tons each month"
            and self.protein_units == "thousand tons each month"
        ):
            return Food(
                kcals=self.kcals * billion_kcal_conversion,
                fat=self.fat * thou_tons_fat_conversion,
                protein=self.protein * thou_tons_protein_conversion,
                kcals_units="kcals per person per day each month",
                fat_units="grams per person per day each month",
                protein_units="grams per person per day each month",
            )
        if (
            self.kcals_units == "billion kcals per month"
            and self.fat_units == "thousand tons per month"
            and self.protein_units == "thousand tons per month"
        ):
            Food = self.get_Food_class()
            return Food(
                kcals=self.kcals * billion_kcal_conversion,
                fat=self.fat * thou_tons_fat_conversion,
                protein=self.protein * thou_tons_protein_conversion,
                kcals_units="kcals per person per day",
                fat_units="grams per person per day",
                protein_units="grams per person per day",
            )

        else:
            print("Error: conversion from these units not known")
            print("From units:")
            self.print_units()
            print("To units:")
            print("    kcals: kcals per person per day OR per day each month")
            print("    fat: grams per person per day OR per day each month")
            print("    protein: grams per person per day OR per day each month")
            success = False
            assert success

    def in_units_kcals_grams_grams_per_capita(self):
        """
        If the existing units are understood by this function, it tries to convert the
        values and units to kcals per person per day, grams per pseron per day, kcals
        per person per day.
        """

        # getting this instance of the UnitConversions from the child class
        # allows us to get some previously set values like kcals monthly and days in
        # month
        conversions = self.get_conversions()

        # okay, okay, maybe the way I did this child/parent thing is not ideal...
        # get the child class so can initialize the Food class
        Food = self.get_Food_class()

        percent_kcal_conversion = 1 / 100 * conversions.kcals_daily
        percent_fat_conversion = 1 / 100 * conversions.fat_daily
        percent_protein_conversion = 1 / 100 * conversions.protein_daily

        if (
            self.kcals_units == "percent people fed each month"
            and self.fat_units == "percent people fed each month"
            and self.protein_units == "percent people fed each month"
        ):
            return Food(
                kcals=self.kcals * percent_kcal_conversion,
                fat=self.fat * percent_fat_conversion,
                protein=self.protein * percent_protein_conversion,
                kcals_units="kcals per person per day each month",
                fat_units="grams per person per day each month",
                protein_units="grams per person per day each month",
            )
        if (
            self.kcals_units == "percent people fed per month"
            and self.fat_units == "percent people fed per month"
            and self.protein_units == "percent people fed per month"
        ):
            Food = self.get_Food_class()
            return Food(
                kcals=self.kcals * percent_kcal_conversion,
                fat=self.fat * percent_fat_conversion,
                protein=self.protein * percent_protein_conversion,
                kcals_units="kcals per person per day",
                fat_units="grams per person per day",
                protein_units="grams per person per day",
            )

        else:
            print("Error: conversion from these units not known")
            print("From units:")
            self.print_units()
            print("To units:")
            print("    kcals: kcals per person per day OR per day each month")
            print("    fat: grams per person per day OR per day each month")
            print("    protein: grams per person per day OR per day each month")
            success = False
            assert success
