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
        """
        Initializes a new instance of the UnitConversions class.

        Sets the NUTRITION_PROPERTIES_ASSIGNED attribute to False.
        """

        # NUTRITION_PROPERTIES_ASSIGNED is a boolean attribute that indicates whether
        # the nutrition properties have been assigned to the class
        # It is initially set to False
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
        Calculates the monthly nutritional requirements for a given population based on daily intake.

        Args:
            kcals_daily (float): daily caloric intake per person
            fat_daily (float): daily fat intake per person in grams
            protein_daily (float): daily protein intake per person in grams
            include_fat (bool): whether or not to include fat in the calculations
            include_protein (bool): whether or not to include protein in the calculations
            population (int): number of people to calculate nutritional requirements for

        Returns:
            None

        This function calculates the monthly nutritional requirements for a given population based on daily intake.
        It sets several instance variables that can be accessed later.

        """

        # Set the number of days in a month
        self.days_in_month = 30

        # Set whether or not to include fat and protein in the calculations
        self.include_fat = include_fat
        self.include_protein = include_protein
        self.exclude_fat = not include_fat
        self.exclude_protein = not include_protein

        # Set the daily nutritional requirements
        self.kcals_daily = kcals_daily
        self.fat_daily = fat_daily
        self.protein_daily = protein_daily

        # Calculate the monthly nutritional requirements
        self.kcals_monthly = kcals_daily * self.days_in_month
        self.fat_monthly = fat_daily / 1e6 * self.days_in_month / 1000
        self.protein_monthly = protein_daily / 1e6 * self.days_in_month / 1000

        # Calculate the total nutritional requirements for the population
        self.billion_kcals_needed = self.kcals_monthly * population / 1e9
        self.thou_tons_fat_needed = self.fat_monthly * population
        self.thou_tons_protein_needed = self.protein_monthly * population

        # Set the population
        self.population = population

        # Set a flag indicating that the nutrition properties have been assigned
        self.NUTRITION_PROPERTIES_ASSIGNED = True

    def get_units_from_list_to_total(self):
        """
        Gets the units for a single month by removing the " each month" part of the units for kcals, fat, and protein.

        Args:
            self: An instance of the class containing kcals_units, fat_units, and protein_units attributes.

        Returns:
            list: A list of the units for kcals, fat, and protein for a single month.

        Raises:
            AssertionError: If "each month" is not found in kcals_units, fat_units, or protein_units.
        """

        # Make sure this only happens for monthly food
        assert "each month" in self.kcals_units, "kcals_units must contain 'each month'"
        assert "each month" in self.fat_units, "fat_units must contain 'each month'"
        assert (
            "each month" in self.protein_units
        ), "protein_units must contain 'each month'"

        # Remove the " each month" part of the units for kcals, fat, and protein
        kcals_units = self.kcals_units.split(" each month")[0]
        fat_units = self.fat_units.split(" each month")[0]
        protein_units = self.protein_units.split(" each month")[0]

        # Return the units for kcals, fat, and protein for a single month
        return [kcals_units, fat_units, protein_units]

    def set_units_from_list_to_total(self):
        """
        Sets the units for a single month.

        This function removes the " each month" part of the units for kcals, fat, and protein.
        It then sets the units attribute to a list of the units for kcals, fat, and protein for a single month.

        Args:
            None

        Returns:
            None
        """

        # Make sure this only happens for monthly food
        assert "each month" in self.kcals_units
        assert "each month" in self.fat_units
        assert "each month" in self.protein_units

        # Remove the " each month" part of the units for kcals, fat, and protein
        [
            self.kcals_units,
            self.fat_units,
            self.protein_units,
        ] = self.get_units_from_list_to_total()

        # Set the units attribute to a list of the units for kcals, fat, and protein for a single month
        self.units = [self.kcals_units, self.fat_units, self.protein_units]

    def get_units_from_list_to_element(self):
        """
        Gets the units for a single element.

        This function replaces the " each month" part of the units for kcals, fat, and protein with "per month".
        It then returns a list of the units for kcals, fat, and protein for a single element.

        Args:
            self: An instance of the class containing kcals_units, fat_units, and protein_units.

        Returns:
            list: A list of the units for kcals, fat, and protein for a single element.
        """

        # Make sure this only happens for monthly food
        assert "each month" in self.kcals_units
        assert "each month" in self.fat_units
        assert "each month" in self.protein_units

        # Replace the " each month" part of the units for kcals, fat, and protein with "per month"
        kcals_units = self.kcals_units.replace(" each month", " per month")
        fat_units = self.fat_units.replace(" each month", " per month")
        protein_units = self.protein_units.replace(" each month", " per month")

        # Return the units for kcals, fat, and protein for a single element
        return [kcals_units, fat_units, protein_units]

    def set_units_from_list_to_element(self):
        """
        Sets the units for a single element.

        This function sets the kcals_units, fat_units, and protein_units attributes to the units for a single element.
        It first checks that this only happens for monthly food. Then it sets the units by calling the get_units_from_list_to_element() function.

        Args:
            None

        Returns:
            None
        """

        # Make sure this only happens for monthly food
        assert "each month" in self.kcals_units
        assert "each month" in self.fat_units
        assert "each month" in self.protein_units

        # Set the kcals_units, fat_units, and protein_units attributes to the units for a single element
        [
            self.kcals_units,
            self.fat_units,
            self.protein_units,
        ] = self.get_units_from_list_to_element()

    def get_units_from_element_to_list(self):
        """
        Gets the units for a list of months.

        This function takes the units for kcals, fat, and protein and adds " each month" to signify a food list.
        It then returns a list of the units for kcals, fat, and protein for a list of months.

        Returns:
            list: A list of the units for kcals, fat, and protein for a list of months.
        """

        # Make sure this only happens for a single element
        assert "each month" not in self.kcals_units
        assert "each month" not in self.fat_units
        assert "each month" not in self.protein_units

        # Add " each month" to the units for kcals, fat, and protein to signify a food list
        kcals_units = self.kcals_units + " each month"
        fat_units = self.fat_units + " each month"
        protein_units = self.protein_units + " each month"

        # Return the units for kcals, fat, and protein for a list of months
        return [kcals_units, fat_units, protein_units]

    def set_units_from_element_to_list(self):
        """
        Sets the units for a list of months.

        This function sets the kcals_units, fat_units, and protein_units attributes to the units for a list of months.
        It first checks that this is only happening for a single element. Then, it sets the units for each attribute by
        calling the get_units_from_element_to_list() function.

        Args:
            None

        Returns:
            None
        """

        # Make sure this only happens for a single element
        assert "each month" not in self.kcals_units
        assert "each month" not in self.fat_units
        assert "each month" not in self.protein_units

        # Set the kcals_units, fat_units, and protein_units attributes to the units for a list of months
        [
            self.kcals_units,
            self.fat_units,
            self.protein_units,
        ] = self.get_units_from_element_to_list()

    def get_units(self):
        """
        Gets the units for kcals, fat, and protein.

        Updates the units attribute to the current values of kcals_units, fat_units, and protein_units.

        Returns:
            list: A list of the units for kcals, fat, and protein.
        """

        # Update the units attribute to the current values of kcals_units, fat_units, and protein_units
        self.units = [self.kcals_units, self.fat_units, self.protein_units]

        # Return the units for kcals, fat, and protein
        return self.units

    def set_units(self, kcals_units, fat_units, protein_units):
        """
        Sets the units for kcals, fat, and protein.

        Sets the kcals_units, fat_units, and protein_units attributes to the specified units.

        Args:
            kcals_units (str): The units for kcals.
            fat_units (str): The units for fat.
            protein_units (str): The units for protein.

        Returns:
            None
        """

        # Set the kcals_units, fat_units, and protein_units attributes to the specified units
        self.kcals_units = kcals_units
        self.fat_units = fat_units
        self.protein_units = protein_units

        # Update the units attribute to the current values of kcals_units, fat_units, and protein_units
        self.units = [kcals_units, fat_units, protein_units]

        # Examine properties of units
        # (Note: This line of code is not necessary and can be removed)
        # print(self.units)

    def print_units(self):
        """
        Prints the units for kcals, fat, and protein.

        This function prints the units for kcals, and optionally for fat and protein if they are included in the conversions.

        Args:
            None

        Returns:
            None
        """

        # Print the units for kcals
        print("    kcals: ", self.kcals_units)

        # Print the units for fat if it is included in the conversions
        if self.conversions.include_fat:
            print("    fat: ", self.fat_units)

        # Print the units for protein if it is included in the conversions
        if self.conversions.include_protein:
            print("    protein: ", self.protein_units)

    def is_a_ratio(self):
        """
        Checks if the units for kcals, fat, and protein are all "ratio" type.

        Returns:
            bool: True if the units for kcals, fat, and protein are all "ratio" type, False otherwise.
        """

        # Check if the units for kcals, fat, and protein are all "ratio" type
        if (
            "ratio" in self.kcals_units
            and "ratio" in self.fat_units
            and "ratio" in self.protein_units
        ):
            # If all units are "ratio" type, return True
            return True
        else:
            # If any of the units are not "ratio" type, return False
            return False

    def is_units_percent(self):
        """
        Checks if the units for kcals, fat, and protein are all "percent" type.

        Returns:
            bool: True if the units for kcals, fat, and protein are all "percent" type, False otherwise.
        """

        # Check if the units for kcals, fat, and protein are all "percent" type
        if (
            "percent" in self.kcals_units  # Check if kcals units are "percent"
            and "percent" in self.fat_units  # Check if fat units are "percent"
            and "percent" in self.protein_units  # Check if protein units are "percent"
        ):
            return True  # If all units are "percent", return True
        else:
            return False  # If any unit is not "percent", return False

    def in_units_billions_fed(self):
        """
        Converts the values and units to billions of people fed if the existing units are understood by this function.

        Returns:
            Food: A new Food instance with the converted values and units.
        """

        # Get the UnitConversions instance from the child class
        conversions = self.get_conversions()

        # Get the child class so we can initialize the Food class
        Food = self.get_Food_class()

        # Define the conversion factors
        billion_kcal_conversion = 1 / conversions.kcals_monthly
        thou_tons_fat_conversion = 1 / conversions.fat_monthly / 1e9
        thou_tons_protein_conversion = 1 / conversions.protein_monthly / 1e9
        percent_people_kcal_conversion = conversions.population / 1e9 / 100
        percent_people_fat_conversion = conversions.population / 1e9 / 100
        percent_people_protein_conversion = conversions.population / 1e9 / 100

        # Check if the existing units are understood by this function and convert the values and units accordingly
        if (
            self.kcals_units == "billion kcals each month"
            and self.fat_units == "thousand tons each month"
            and self.protein_units == "thousand tons each month"
        ):
            # Convert the values and units to billions of people fed each month
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
            # Convert the values and units to billions of people fed per month
            return Food(
                kcals=self.kcals * billion_kcal_conversion,
                fat=self.fat * thou_tons_fat_conversion,
                protein=self.protein * thou_tons_protein_conversion,
                kcals_units="billion people fed per month",
                fat_units="billion people fed per month",
                protein_units="billion people fed per month",
            )
        if (
            self.kcals_units == "billion kcals each month"
            and self.fat_units == "thousand tons each month"
            and self.protein_units == "thousand tons each month"
        ):
            # Convert the values and units to billions of people fed each month
            return Food(
                kcals=self.kcals * billion_kcal_conversion,
                fat=self.fat * thou_tons_fat_conversion,
                protein=self.protein * thou_tons_protein_conversion,
                kcals_units="billion people fed each month",
                fat_units="billion people fed each month",
                protein_units="billion people fed each month",
            )
        percent_people_kcal_conversion = conversions.population / 1e9 / 100
        percent_people_fat_conversion = conversions.population / 1e9 / 100
        percent_people_protein_conversion = conversions.population / 1e9 / 100

        if (
            self.kcals_units == "percent people fed per month"
            and self.fat_units == "percent people fed per month"
            and self.protein_units == "percent people fed per month"
        ):
            # Convert the values and units to billions of people fed per month
            return Food(
                kcals=self.kcals * percent_people_kcal_conversion,
                fat=self.fat * percent_people_fat_conversion,
                protein=self.protein * percent_people_protein_conversion,
                kcals_units="billion people fed per month",
                fat_units="billion people fed per month",
                protein_units="billion people fed per month",
            )

        if (
            self.kcals_units == "percent people fed each month"
            and self.fat_units == "percent people fed each month"
            and self.protein_units == "percent people fed each month"
        ):
            # Convert the values and units to billions of people fed per month
            return Food(
                kcals=self.kcals * percent_people_kcal_conversion,
                fat=self.fat * percent_people_fat_conversion,
                protein=self.protein * percent_people_protein_conversion,
                kcals_units="billion people fed each month",
                fat_units="billion people fed each month",
                protein_units="billion people fed each month",
            )

        # If the existing units are not understood by this function, print an error message and raise an assertion error
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
        Converts the values and units of a Food instance to percent of people fed, if the existing units are understood by this function.
        Args:
            self (Food): The Food instance to be converted.
        Returns:
            Food: A new Food instance with the converted values and units.
        """

        # Get the UnitConversions instance from the child class
        conversions = self.get_conversions()

        # Get the child class so we can initialize the Food class
        Food = self.get_Food_class()

        # Define the conversion factors
        billion_people_kcal_conversion = 100 / conversions.population * 1e9
        billion_people_fat_conversion = 100 / conversions.population * 1e9
        billion_people_protein_conversion = 100 / conversions.population * 1e9
        billion_kcal_conversion = 100 / conversions.billion_kcals_needed
        thou_tons_fat_conversion = 100 / conversions.thou_tons_fat_needed
        thou_tons_protein_conversion = 100 / conversions.thou_tons_protein_needed

        # Check if the existing units are understood by this function and convert the values and units accordingly
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

        # If the existing units are not understood by this function, print an error message and raise an assertion error
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
        Converts values and units to billion kcals and thousand tons per month if the existing units are understood by this function.
        Args:
            self: An instance of the Food class.
        Returns:
            Food: A new Food instance with the converted values and units.
        """

        # Get the UnitConversions instance from the child class
        conversions = self.get_conversions()

        # Get the child class so we can initialize the Food class
        Food = self.get_Food_class()

        # Define the conversion factors
        million_tons_to_billion_kcals_conversion = 1e6 * 1000 * 4000 / 1e9
        percent_kcal_conversion = (
            conversions.kcals_monthly * conversions.population / 1e9 / 100
        )
        percent_fat_conversion = conversions.fat_monthly * conversions.population / 100
        percent_protein_conversion = (
            conversions.protein_monthly * conversions.population / 100
        )

        # Check if the existing units are understood by this function and convert the values and units accordingly
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

        # If the existing units are not understood by this function, print an error message and raise an assertion error
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
        Converts the values and units to effective kcals per capita per day for each nutrient
        if the existing units are understood by this function.

        Returns:
            Food: A new Food instance with the converted values and units.
        """

        # Get the UnitConversions instance from the child class
        conversions = self.get_conversions()

        # Get the child class so we can initialize the Food class
        Food = self.get_Food_class()

        # Define the conversion factors
        billion_people_kcal_conversion = (
            1e9 / conversions.population * conversions.kcals_daily
        )
        billion_people_fat_conversion = (
            1e9 / conversions.population * conversions.kcals_daily
        )
        billion_people_protein_conversion = (
            1e9 / conversions.population * conversions.kcals_daily
        )
        percent_kcal_conversion = conversions.kcals_daily / 100
        percent_fat_conversion = conversions.kcals_daily / 100
        percent_protein_conversion = conversions.kcals_daily / 100

        # Check if the existing units are understood by this function and convert the values and units accordingly
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

        # If the existing units are not understood by this function, print an error message and raise an assertion error
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
        Converts values and units to kcals per person per day, grams per person per day, kcals per person per day.
        If the existing units are understood by this function, it tries to convert the values and units to kcals per person per day, grams per person per day, kcals per person per day.
        Args:
            self (UnitConversions): instance of the UnitConversions class
            kcal_ratio (float): kcal per kg of the food being converted
            fat_ratio (float): grams per kcal of the food being converted
            protein_ratio (float): grams per kcal of the food being converted
        Returns:
            Food: instance of the Food class with converted units
        Raises:
            AssertionError: if conversion from these units is not known
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
