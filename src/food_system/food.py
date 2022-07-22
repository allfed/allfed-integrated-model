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
import numpy as np
import copy

module_path = os.path.abspath(os.path.join("../.."))
if module_path not in sys.path:
    sys.path.append(module_path)

from src.food_system.unit_conversions import UnitConversions
from src.utilities.plotter import Plotter


class Food(UnitConversions):
    """
    A food always has calories, fat, and protein.
    Food applies to biofuels and feed properties as well.

    A food always has units for each nutrient and these need to match when combining
    foods in some way, such as adding up, multiplying, or dividing their nutrients

    Best practice is to alter the food's units to be as specific as possible to prevent
    errors in the calculation.

    Here are some examples of using the food class:

    CONVENTIONS:
        A nutrient with a list of the value for each month, will need to
        have " each month" at the end of the units.
        A nutrient that represents the value for every month must have
        a " per month" at the end of the units.
        A nutrient with a single value all summed up over all time periods must not
        contain any " each month" or " per month" in the units.



    >>> example_food=Food(10,3,1)

    (defaults to billion kcals, thousand tons monthly fat, thousand tons monthly
    protein)

    >>> print(example_food):
        kcals: 10 billion kcals
        fat: 13  thousand tons
        protein: 1  thousand tons

    >>> example_food.set_units(
    >>>     kcals_units = 'ratio minimum global needs per year',
    >>>     fat_units = 'ratio minimum global needs per year',
    >>>     protein_units = 'ratio minimum global needs per year',
    >>> )
    >>> print(example_food):
        kcals: 10 ratio minimum global needs per year
        fat: 3  ratio minimum global needs per year
        protein: 1  ratio minimum global needs per year

    (in order to get a min nutrient, you need to make sure the units are all the same)
    (in reality, you would want to divide the values by the actual global needs above)

    >>> print(example_food.get_min_nutrient())
        ('protein', 1)

    >>> example_food_monthly = example_food / 12
    >>> example_food_monthly.set_units(
    >>>     kcals_units = 'ratio minimum global needs per month',
    >>>     fat_units = 'ratio minimum global needs per month',
    >>>     protein_units = 'ratio minimum global needs per month',
    >>> )

    >>> print(example_food_monthly)
        kcals: 0.8333333333333334 ratio minimum global needs per month
        fat: 0.25  ratio minimum global needs per month
        protein: 0.08333333333333333  ratio minimum global needs per month

    >>> NMONTHS = 3
    >>> example_food_all_months = Food(
    >>>     [example_food_monthly.kcals] * NMONTHS,
    >>>     [example_food_monthly.fat] * NMONTHS,
    >>>     [example_food_monthly.protein] * NMONTHS,
    >>> )
    >>> example_food_all_months.set_units(
    >>>     kcals_units = 'ratio minimum global needs each month',
    >>>     fat_units = 'ratio minimum global needs each month',
    >>>     protein_units = 'ratio minimum global needs each month',
    >>> )
    >>> print(example_food_all_months)
        kcals: [0.8333333333333334, 0.8333333333333334, 0.8333333333333334] ratio
        minimum global needs each month
        fat: [0.25, 0.25, 0.25]  ratio minimum global needs each month
        protein: [0.08333333333333333, 0.08333333333333333, 0.08333333333333333]
        ratio minimum global needs each month

    """

    # public property used to convert between units
    conversions = UnitConversions()

    @classmethod
    def get_Food_class(cls):
        """
        get this class
        """
        return cls

    @classmethod
    def get_conversions(cls):
        """
        return the class conversions object
        this is only used by the parent UnitConversions class
        """
        conversions = cls.conversions

        assert conversions.NUTRITION_PROPERTIES_ASSIGNED, """ERROR: you must 
            assign the conversions property before attempting to convert between
            food units"""

        return conversions

    @classmethod
    def get_nutrient_names(cls):
        """
        Returns the macronutrients of the food.
        """

        return ["kcals", "fat", "protein"]

    @classmethod
    def ratio_one(cls):
        """
        Returns a ratio of one.
        """

        return Food(
            kcals=1,
            fat=1,
            protein=1,
            # these are the default units but they can be overwritten
            kcals_units="ratio",
            fat_units="ratio",
            protein_units="ratio",
        )

    @classmethod
    def ratio_zero(cls):
        """
        Returns a ratio of zero.
        """

        return Food(
            kcals=0,
            fat=0,
            protein=0,
            # these are the default units but they can be overwritten
            kcals_units="ratio",
            fat_units="ratio",
            protein_units="ratio",
        )

    def __init__(
        # these are the default values but they can be overwritten
        self,
        kcals=0,
        fat=0,
        protein=0,
        # these are the default units but they can be overwritten
        kcals_units="billion kcals",
        fat_units="thousand tons",
        protein_units="thousand tons",
    ):
        """
        Initializes the food with the given macronutrients, and set the default units.
        """
        super().__init__()
        self.kcals = kcals
        self.fat = fat
        self.protein = protein

        self.set_units(
            kcals_units,
            fat_units,
            protein_units,
        )

        self.validate_if_list()

        if self.is_list_monthly():
            self.NMONTHS = len(self.kcals)
        else:
            self.NMONTHS = np.nan  # number of months is not a number

    # validation functions

    def validate_if_list(self):
        """
        Runs all the checks to make sure the list is properly set up
        """

        if self.is_list_monthly():
            assert " each month" in self.kcals_units
            assert " each month" in self.fat_units
            assert " each month" in self.protein_units

            # if one of the list types, ensure the following conditions:
            assert (
                len(self.kcals) == len(self.fat) == len(self.protein)
            ), "ERROR: list type food must have same number of months for all nutrients"
            assert (
                type(self.kcals) == type(self.fat) == type(self.protein)
            ), "ERROR: list type food must have same type of list for all nutrients"
            assert (
                len(self.kcals) > 0
            ), "ERROR: list type food must have more than one month"

    def make_sure_not_a_list(self):
        """
        throw an error if any of the food nutrients are a list
        """
        assert type(self.kcals) != list and type(self.kcals) != np.ndarray
        assert type(self.fat) != list and type(self.fat) != np.ndarray
        assert type(self.protein) != list and type(self.protein) != np.ndarray

    def make_sure_is_a_list(self):
        """
        throw an error if any of the food nutrients is not a list, then validate
        list properties
        """
        assert type(self.kcals) == list or type(self.kcals) == np.ndarray
        assert type(self.fat) == list or type(self.fat) == np.ndarray
        assert type(self.protein) == list or type(self.protein) == np.ndarray

    # These are all for mathematical operations on the food's macronutrients, such as
    # adding, subtracting, multiplying, and dividing.

    def __add__(self, other):
        """
        Adds two foods together.
        """
        kcals = self.kcals + other.kcals
        fat = self.fat + other.fat
        protein = self.protein + other.protein

        assert self.units == other.units

        return Food(
            kcals, fat, protein, self.kcals_units, self.fat_units, self.protein_units
        )

    def __sub__(self, other):
        """
        Subtracts two food nutrient quantities from each other.
        """
        kcals = self.kcals - other.kcals
        fat = self.fat - other.fat
        protein = self.protein - other.protein

        assert self.units == other.units

        return Food(
            kcals, fat, protein, self.kcals_units, self.fat_units, self.protein_units
        )

    def __truediv__(self, other):
        """
        Divides a food's macronutrients by a number.
        """
        if type(other) == Food:

            assert self.units == other.units

            return Food(
                self.kcals / other.kcals,
                self.fat / other.fat,
                self.protein / other.protein,
                "ratio",
                "ratio",
                "ratio",
            )

        kcals = self.kcals / other
        fat = self.fat / other
        protein = self.protein / other

        return Food(
            kcals, fat, protein, self.kcals_units, self.fat_units, self.protein_units
        )

    def __mul__(self, other):
        """
        Multiplies a food's macronutrients by a number.
        """
        if type(other) == Food:

            assert self.units == other.units

            return Food(
                self.kcals * other.kcals,
                self.fat * other.fat,
                self.protein * other.protein,
                self.kcals_units,
                self.fat_units,
                self.protein_units,
            )

        if self.is_list_monthly():
            return Food(
                np.array(self.kcals) * other,
                np.array(self.fat) * other,
                np.array(self.protein) * other,
                self.kcals_units,
                self.fat_units,
                self.protein_units,
            )

        kcals = self.kcals * other
        fat = self.fat * other
        protein = self.protein * other

        return Food(
            kcals, fat, protein, self.kcals_units, self.fat_units, self.protein_units
        )

    def __rmul__(self, other):
        """
        Multiplies a food's macronutrients by a number.
        This deals with the case that the argument was called with the number first.
        """
        return self.__mul__(other)

    def __eq__(self, other):
        """
        Returns True if the two foods are equal.
        """

        assert self.units == other.units

        return (
            self.kcals == other.kcals
            and self.fat == other.fat
            and self.protein == other.protein
        )

    def __ne__(self, other):
        """
        Returns False if the two foods are not equal.
        """

        assert self.units == other.units

        return (
            self.kcals != other.kcals
            or self.fat != other.fat
            or self.protein != other.protein
        )

    # functions which access properties of this food

    def plot(self, title="generic food object over time"):
        """
        Use the plotter to plot this food's properties.
        """
        ALTERNATIVE_LAYOUT = False
        if ALTERNATIVE_LAYOUT:
            Plotter.plot_food_alternative(self, title)
        else:
            Plotter.plot_food(self, title)

    def __str__(self):
        """
        Returns a string representation of the food.
        """
        return "    kcals: % s % s\n    fat: % s  % s\n    protein: % s  % s" % (
            self.kcals,
            self.kcals_units,
            self.fat,
            self.fat_units,
            self.protein,
            self.protein_units,
        )

    def __neg__(self):
        """
        Return itself with negative nutrient values.
        """

        return Food(
            kcals=-self.kcals,
            fat=-self.fat,
            protein=-self.protein,
            kcals_units=self.kcals_units,
            fat_units=self.fat_units,
            protein_units=self.protein_units,
        )

    def is_list_monthly(self):
        """
        return whether this is a list
        """
        return type(self.kcals) == list or type(self.kcals) == np.ndarray

    # comparisons between the quantities of nutrients
    # only compares kcals with kcals, fat with fat, and protein with protein, not
    # between the units.

    def is_never_negative(self):

        if self.is_list_monthly():
            self.validate_if_list()

            return (
                (np.array(self.kcals) > 0).all()
                and (np.array(self.fat) > 0).all()
                and (np.array(self.protein) > 0).all()
            )

        return (self.kcals > 0) and (self.fat > 0) and (self.protein > 0)

    def all_greater_than(self, other):
        """
        Returns True if the food's macronutrients are greater than the other food's.
        """
        assert self.units == other.units

        if self.is_list_monthly():

            self.validate_if_list()

            return (
                (np.array(self.kcals - other.kcals) > 0).all()
                and (np.array(self.fat - other.fat) > 0).all()
                and (np.array(self.protein - other.protein) > 0).all()
            )

        return (
            self.kcals > other.kcals
            and self.fat > other.fat
            and self.protein > other.protein
        )

    def all_less_than(self, other):
        """
        Returns True if the food's macronutrients are greater than the other food's.
        """

        assert self.units == other.units

        if self.is_list_monthly():

            self.validate_if_list()

            return (
                (np.array(self.kcals - other.kcals) < 0).all()
                and (np.array(self.fat - other.fat) < 0).all()
                and (np.array(self.protein - other.protein) < 0).all()
            )

        return (
            self.kcals < other.kcals
            and self.fat < other.fat
            and self.protein < other.protein
        )

    def any_greater_than(self, other):
        """
        Returns True if the food's macronutrients are greater than the other food's.
        """

        assert self.units == other.units

        if self.is_list_monthly():

            self.validate_if_list()

            return (
                (np.array(self.kcals - other.kcals) > 0).any()
                or (np.array(self.fat - other.fat) > 0).any()
                or (np.array(self.protein - other.protein) > 0).any()
            )

        return (
            self.kcals > other.kcals
            or self.fat > other.fat
            or self.protein > other.protein
        )

    def any_less_than(self, other):
        """
        Returns True if the food's macronutrients are less than the other food's.
        """

        assert self.units == other.units

        if self.is_list_monthly():

            self.validate_if_list()

            return (
                (np.array(self.kcals - other.kcals) < 0).any()
                or (np.array(self.fat - other.fat) < 0).any()
                or (np.array(self.protein - other.protein) < 0).any()
            )

        return (
            self.kcals < other.kcals
            or self.fat < other.fat
            or self.protein < other.protein
        )

    def all_greater_than_or_equal(self, other):
        """
        Returns True if the food's macronutrients are greater than or equal to
        the other food's.
        """
        assert self.units == other.units

        if self.is_list_monthly():

            self.validate_if_list()

            return (
                (np.array(self.kcals - other.kcals) >= 0).all()
                and (np.array(self.fat - other.fat) >= 0).all()
                and (np.array(self.protein - other.protein) >= 0).all()
            )

        return (
            self.kcals >= other.kcals
            and self.fat >= other.fat
            and self.protein >= other.protein
        )

    def all_less_than_or_equal(self, other):
        """
        Returns True if the food's macronutrients are less than or equal to
        the other food's.
        """

        assert self.units == other.units

        if self.is_list_monthly():

            self.validate_if_list()

            return (
                (np.array(self.kcals - other.kcals) <= 0).all()
                and (np.array(self.fat - other.fat) <= 0).all()
                and (np.array(self.protein - other.protein) <= 0).all()
            )

        return (
            self.kcals <= other.kcals
            and self.fat <= other.fat
            and self.protein <= other.protein
        )

    def any_greater_than_or_equal(self, other):
        """
        Returns True if the food's macronutrients are greater than or equal to
        the other food's.
        """
        assert self.units == other.units

        if self.is_list_monthly():

            self.validate_if_list()

            return (
                (np.array(self.kcals - other.kcals) >= 0).any()
                or (np.array(self.fat - other.fat) >= 0).any()
                or (np.array(self.protein - other.protein) >= 0).any()
            )

        return (
            self.kcals >= other.kcals
            or self.fat >= other.fat
            or self.protein >= other.protein
        )

    def any_less_than_or_equal(self, other):
        """
        Returns True if the food's macronutrients are less than or equal to
        the other food's.
        """

        if self.is_list_monthly():

            self.validate_if_list()

            return (
                (np.array(self.kcals - other.kcals) <= 0).any()
                or (np.array(self.fat - other.fat) <= 0).any()
                or (np.array(self.protein - other.protein) <= 0).any()
            )

        assert self.units == other.units

        return (
            self.kcals <= other.kcals
            or self.fat <= other.fat
            or self.protein <= other.protein
        )

    def equals_zero(self):
        """
        Returns True if the food's macronutrients are equal to zero.
        """
        if self.is_list_monthly():

            self.validate_if_list()

            return (
                (np.array(self.kcals) == 0).all()
                and (np.array(self.fat) == 0).all()
                and (np.array(self.protein) == 0).all()
            )

        return self.kcals == 0 and self.fat == 0 and self.protein == 0

    def all_greater_than_zero(self):
        """
        Returns True if the food's macronutrients are greater than zero.
        """
        if self.is_list_monthly():

            self.validate_if_list()

            return (
                (np.array(self.kcals) > 0).all()
                and (np.array(self.fat) > 0).all()
                and (np.array(self.protein) > 0).all()
            )

        return self.kcals > 0 and self.fat > 0 and self.protein > 0

    def any_greater_than_zero(self):
        """
        Returns True if any of the food's macronutrients are greater than zero.
        """
        if self.is_list_monthly():

            self.validate_if_list()

            return (
                (np.array(self.kcals) > 0).any()
                or (np.array(self.fat) > 0).any()
                or (np.array(self.protein) > 0).any()
            )

        return self.kcals > 0 or self.fat > 0 or self.protein > 0

    def all_greater_than_or_equal_zero(self):
        """
        Returns True if the food's macronutrients are greater than or equal to zero.
        """
        if self.is_list_monthly():

            self.validate_if_list()

            return (
                (np.array(self.kcals) >= 0).all()
                and (np.array(self.fat) >= 0).all()
                and (np.array(self.protein) >= 0).all()
            )

        return self.kcals >= 0 and self.fat >= 0 and self.protein >= 0

    # Helper functions to get properties of the three nutrient values

    def as_list(self):
        """
        Returns the nutrients as an ordered list.
        """
        return np.array([self.kcals, self.fat, self.protein])

    def get_min_nutrient(self):
        """
        Returns the minimum nutrient of the food.

        NOTE: only works on single valued instances of nutrients, not arrays.

        Returns:
        (minimum nutrient name, minimum nutrient value)
        """
        assert self.kcals_units == self.fat_units == self.protein_units

        self.make_sure_not_a_list()

        nutrients_dict = {
            "kcals": self.kcals,
            "fat": self.fat,
            "protein": self.protein,
        }

        # Using min() + list comprehension + values()
        # Finding min value keys in dictionary
        min_nutrient_val = min(nutrients_dict.values())
        min_key = [
            key for key in nutrients_dict if nutrients_dict[key] == min_nutrient_val
        ][0]

        assert min_nutrient_val <= self.kcals
        assert min_nutrient_val <= self.fat
        assert min_nutrient_val <= self.protein

        return (min_key, min_nutrient_val)

    def get_max_nutrient(self):
        """
        Returns the maximum nutrient of the food.

        NOTE: only works on single valued instances of nutrients, not arrays.

        Returns:
        (maximum nutrient name, maximum nutrient value)
        """

        assert self.kcals_units == self.fat_units == self.protein_units

        self.make_sure_not_a_list()

        nutrients_dict = {
            "kcals": self.kcals,
            "fat": self.fat,
            "protein": self.protein,
        }

        # Using max() + list comprehension + values()
        # Finding max value keys in dictionary
        max_nutrient_val = max(nutrients_dict.values())
        max_key = [
            key for key in nutrients_dict if nutrients_dict[key] == max_nutrient_val
        ][0]

        assert max_nutrient_val >= self.kcals
        assert max_nutrient_val >= self.fat
        assert max_nutrient_val >= self.protein

        return (max_key, max_nutrient_val)

    def get_nutrients_sum(self):
        """
        Sum up the nutrients in all the months, then alter the units to remove
         "each month"
        """

        self.validate_if_list()

        food_sum = Food(
            sum(self.kcals),
            sum(self.fat),
            sum(self.protein),
            self.kcals_units,
            self.fat_units,
            self.protein_units,
        )

        food_sum.set_units_from_list_to_total()

        return food_sum

    def get_running_total_nutrients_sum(self):
        """
        Running sum of the nutrients in all the months, don't alter units
        """
        kcals_copy = copy.deepcopy(self.kcals)
        running_sum_kcals = 0
        to_return_kcals = kcals_copy
        for i in range(self.NMONTHS):
            running_sum_kcals += kcals_copy[i]
            to_return_kcals[i] = running_sum_kcals

        fat_copy = copy.deepcopy(self.fat)
        running_sum_fat = 0
        to_return_fat = fat_copy
        for i in range(self.NMONTHS):
            running_sum_fat += fat_copy[i]
            to_return_fat[i] = running_sum_fat

        protein_copy = copy.deepcopy(self.protein)
        running_sum_protein = 0
        to_return_protein = protein_copy
        for i in range(self.NMONTHS):
            running_sum_protein += protein_copy[i]
            to_return_protein[i] = running_sum_protein

        self.validate_if_list()

        return Food(
            to_return_kcals,
            to_return_fat,
            to_return_protein,
            self.kcals_units,
            self.fat_units,
            self.protein_units,
        )

    def get_first_month(self):
        """
        Just get the first month's nutrient values and convert the units from "each" to
        "per"
        """
        return self.get_month(0)

    def get_month(self, index):
        """
        Get the first month's nutrient values, and convert the units from "each" to
        "per"
        """
        self.validate_if_list()

        food_at_month = Food(
            self.kcals[index],
            self.fat[index],
            self.protein[index],
            self.kcals_units,
            self.fat_units,
            self.protein_units,
        )

        food_at_month.set_units_from_list_to_element()

        return food_at_month

    def get_min_all_months(self):
        """
        create a food with the minimum of every month as a total nutrient
        """
        min_all_months = Food(
            kcals=min(self.kcals),
            fat=min(self.fat),
            protein=min(self.protein),
            kcals_units=self.kcals_units,
            fat_units=self.fat_units,
            protein_units=self.protein_units,
        )

        min_all_months.set_units_from_list_to_total()

        return min_all_months

    def negative_values_to_zero(self):
        """
        Replace negative values with zero for each month for all nutrients.
        Also tests that the function worked.

        Returns: the relevant food object with negative values replaced
        """
        if self.is_list_monthly():

            zeroed_food = Food(
                kcals=np.where(self.kcals < 0, 0, self.kcals),
                fat=np.where(self.fat < 0, 0, self.fat),
                protein=np.where(self.protein < 0, 0, self.protein),
                kcals_units=self.kcals_units,
                fat_units=self.fat_units,
                protein_units=self.protein_units,
            )

        else:
            zeroed_food = Food(
                kcals=0 if self.kcals < 0 else self.kcals,
                fat=0 if self.fat < 0 else self.fat,
                protein=0 if self.protein < 0 else self.protein,
                kcals_units=self.kcals_units,
                fat_units=self.fat_units,
                protein_units=self.protein_units,
            )

        assert zeroed_food.all_greater_than_or_equal_zero()

        return zeroed_food
