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

            # np arrays are easier to work with than default python lists imho
            # TODO: make sure there's no way to sneakily directly define the .kcals etc
            #       as a default python list type and then get rid of all the casting to
            #       np arrays in the rest of the code
            self.kcals = np.array(self.kcals)
            self.fat = np.array(self.fat)
            self.protein = np.array(self.protein)
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
        assert type(self.kcals) == np.ndarray
        assert type(self.fat) == np.ndarray
        assert type(self.protein) == np.ndarray

    def ensure_other_list_zero_if_this_is_zero(self, other_list):
        """
        Get the value of the elements where the passed in list is zero, otherwise
        returned elements are zero.
        """
        self.make_sure_is_a_list()
        other_list.make_sure_is_a_list()

        assert other_list.NMONTHS == self.NMONTHS

        # values with zeros are zeros in all of our unit systems! How convenient.
        # That's why there's no need to check units.

        # here's an example of what np.where does in this context:
        #   >>> self = np.array([1005,693,0,532,786])   # random numbers
        #   >>> list_with_zeros = np.array([0,1,3,0,5]) # random numbers
        #   >>> replacement = np.array([101,62,23,3,0]) # random numbers
        #   >>>
        #   >>> # replace with the replacement if list_with_zeros is zero
        #   >>> processed_list = np.where(
        #   >>>     list_with_zeros == 0,
        #   >>>     replacement,
        #   >>>     self,
        #   >>> )
        #   >>>
        #   >>> print(processed_list)
        #   [101 693   0   3 786]

        # where self is nonzero, we don't care, so we set it to zero
        processed_list_kcals = np.where(
            self.kcals == 0,
            other_list.kcals,
            0,
        )

        if self.conversions.include_fat:
            processed_list_fat = np.where(
                self.fat == 0,
                other_list.fat,
                0,
            )
        else:
            processed_list_fat = np.zeros(len(processed_list_kcals))

        if self.conversions.include_protein:
            processed_list_protein = np.where(
                self.protein == 0,
                other_list.protein,
                0,
            )
        else:
            processed_list_protein = np.zeros(len(processed_list_kcals))

        processed_list = Food(
            kcals=processed_list_kcals,
            fat=processed_list_fat,
            protein=processed_list_protein,
            kcals_units=self.kcals_units,
            fat_units=self.fat_units,
            protein_units=self.protein_units,
        )

        assert processed_list.all_equals_zero()

    def make_sure_fat_protein_zero_if_kcals_is_zero(self):
        """
        Get the value of the elements where the passed in list is zero, otherwise
        returned elements are zero.
        """

        if self.is_list_monthly():
            self.validate_if_list()
            # where self is nonzero, we don't care, so we set it to zero

            fat_all_the_places_kcals_zero = np.where(
                self.kcals == 0,
                self.fat,
                0,
            )

            protein_all_the_places_kcals_zero = np.where(
                self.kcals == 0,
                self.protein,
                0,
            )

            if self.conversions.include_fat:
                assert (fat_all_the_places_kcals_zero == 0).all()
            if self.conversions.include_protein:
                assert (protein_all_the_places_kcals_zero == 0).all()

        else:

            if self.kcals == 0:
                if self.conversions.include_fat:
                    assert self.fat == 0 or self.conversions.exclude_fat
                if self.conversions.include_protein:
                    assert self.protein == 0 or self.conversions.exclude_protein

    def make_sure_not_nan(self):
        """
        Make sure that the food is not a nan number, or fail the assertion
        """
        if self.is_list_monthly:
            self.validate_if_list()
            assert not np.isnan(self.kcals).any()
            assert not np.isnan(self.fat).any()
            assert not np.isnan(self.protein).any()
        else:
            assert not np.isnan(self.kcals)
            assert not np.isnan(self.fat)
            assert not np.isnan(self.protein)

    # These are all for mathematical operations on the food's macronutrients, such as
    # adding, subtracting, multiplying, and dividing.

    def __add__(self, other):
        """
        Adds two foods together.
        """
        assert self.units == other.units

        kcals = self.kcals + other.kcals
        fat = self.fat + other.fat
        protein = self.protein + other.protein

        return Food(
            kcals, fat, protein, self.kcals_units, self.fat_units, self.protein_units
        )

    def __sub__(self, other):
        """
        Subtracts two food nutrient quantities from each other.
        """
        assert self.units == other.units

        kcals = self.kcals - other.kcals
        fat = self.fat - other.fat
        protein = self.protein - other.protein

        return Food(
            kcals, fat, protein, self.kcals_units, self.fat_units, self.protein_units
        )

    def __truediv__(self, other):
        """
        Divides a food's macronutrients by a number.

        Works for food / food, and food list / food list, and food / number.

        cases:
            this is a food list, other is a food list
            this is a food, other is a food
            this is a food, other is a numberFAILED tests/test_food.py::test_addition_monthly_food - ValueError: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()

        """
        if type(other) == Food:

            assert self.units == other.units

            if self.is_list_monthly():
                assert other.is_list_monthly(), """Error: for food lists, can
                    only divide by food lists at the moment. Consider implementing
                    additional cases."""

                self.validate_if_list()
                other.validate_if_list()

                with np.errstate(divide="ignore"):
                    # ignoring divide by zero warnings
                    # (that's fine, divide by zero expected)
                    return Food(
                        np.divide(self.kcals, other.kcals),
                        np.divide(self.fat, other.fat),
                        np.divide(self.protein, other.protein),
                        "ratio each month",
                        "ratio each month",
                        "ratio each month",
                    )

            assert not other.is_list_monthly(), """Error: for foods, can only divide 
                by foods or numbers at the moment, not food lists. Consider
                implementing additional cases."""

            return Food(
                self.kcals / other.kcals,
                self.fat / other.fat,
                self.protein / other.protein,
                "ratio",
                "ratio",
                "ratio",
            )
        else:
            kcals = self.kcals / other
            fat = self.fat / other
            protein = self.protein / other

            return Food(
                kcals, fat, protein, self.kcals_units, self.fat_units, self.protein_units
            )

    def __getitem__(self, key):
        """
        Returns the value of the macronutrient at the given index or range of indices.

        NOTE: if key is a length 1 index, then this won't properly update units
        to " per month" and may cause an error down the line!
        TODO: Make sure this cannot happen
        """
        self.make_sure_is_a_list()

        self.validate_if_list()

        return Food(
            kcals=self.kcals[key],
            fat=self.fat[key],
            protein=self.protein[key],
            kcals_units=self.kcals_units,
            fat_units=self.fat_units,
            protein_units=self.protein_units,
        )

    def __mul__(self, other):
        """
        Multiplies a food's macronutrients by a number.

        Apologies that this multiplication is rather constrained. I only wrote this
        so that it can multiply ratios with non ratios or ratios with ratios, because
        otherwise unit conversions get confusing.

        there are also many possibilities for the characteristics of the input values
        for self in other:

            this is a food
            this is a food list

            other is a food
            other is a food list
            other is a non food (like an int or a float)

            which gives us the possible combinations:

            this is a food and other is a food
            this is a food and other is a food list
            this is a food and other is non food

            this is a food list and other is a food
            this is a food list and other is a food list
            this is a food list and other is a non food


        units can be complicated when multiplying.

            If other is a non-food, there's no need to check units.
            Otherwise, the multiplication works right now only in the cases:
                this is any units, other is a ratio
                other is a ratio, this is any units
                other is a ratio, this is a ratio

        """
        if not self.is_list_monthly():
            if type(other) == Food:
                # this is a food and other is a food
                if other.is_list_monthly():
                    # this is a food and other is a food list

                    this_is_the_ratio = self.is_a_ratio()

                    assert this_is_the_ratio, """unable to multiply a food by a food list
                     where the non-list food is not a ratio, consider implementing 
                     this feature"""

                    kcals_units = other.kcals_units
                    fat_units = other.fat_units
                    protein_units = other.protein_units

                    return Food(
                        kcals=self.kcals * np.array(other.kcals),
                        fat=self.fat * np.array(other.fat),
                        protein=self.protein * np.array(other.protein),
                        kcals_units=kcals_units,
                        fat_units=fat_units,
                        protein_units=protein_units,
                    )

                this_is_the_ratio = self.is_a_ratio()
                other_is_the_ratio = other.is_a_ratio()

                assert (
                    this_is_the_ratio or other_is_the_ratio
                ), "list multiplication only works if one or both is a ratios right now"

                if this_is_the_ratio:
                    kcals_units = other.kcals_units
                    fat_units = other.fat_units
                    protein_units = other.protein_units

                if other_is_the_ratio:
                    kcals_units = self.kcals_units
                    fat_units = self.fat_units
                    protein_units = self.protein_units

                return Food(
                    self.kcals * other.kcals,
                    self.fat * other.fat,
                    self.protein * other.protein,
                    self.kcals_units,
                    self.fat_units,
                    self.protein_units,
                )

                assert self.get_units() == other.get_units_from_element_to_list()

            # this is a food and other is a non food

            return Food(
                self.kcals * other,
                self.fat * other,
                self.protein * other,
                self.kcals_units,
                self.fat_units,
                self.protein_units,
            )

        self.make_sure_is_a_list()
        self.validate_if_list()

        if type(other) == Food:

            if other.is_list_monthly():
                # this is a food list and other is a food list

                other.validate_if_list()

                this_is_the_ratio = self.is_a_ratio()
                other_is_the_ratio = other.is_a_ratio()

                assert (
                    this_is_the_ratio or other_is_the_ratio
                ), "list multiplication only works if one or both is a ratios right now"

                if this_is_the_ratio:
                    kcals_units = other.kcals_units
                    fat_units = other.fat_units
                    protein_units = other.protein_units

                if other_is_the_ratio:
                    kcals_units = self.kcals_units
                    fat_units = self.fat_units
                    protein_units = self.protein_units

                return Food(
                    kcals=np.multiply(np.array(self.kcals), np.array(other.kcals)),
                    fat=np.multiply(np.array(self.fat), np.array(other.fat)),
                    protein=np.multiply(
                        np.array(self.protein), np.array(other.protein)
                    ),
                    # TODO: @Morgan what's going on here?
                    kcals_units=kcals_units,
                    fat_units=fat_units,
                    protein_units=protein_units,
                )

            # this is a food list and other is a food

            other_is_the_ratio = other.is_a_ratio()

            assert other_is_the_ratio, """unable to multiply a food list by a food
                where the non-list food is not a ratio, consider implementing 
                this feature"""

            kcals_units = self.kcals_units
            fat_units = self.fat_units
            protein_units = self.protein_units

            return Food(
                kcals=self.kcals * other.kcals,
                fat=self.fat * other.fat,
                protein=self.protein * other.protein,
                kcals_units=kcals_units,
                fat_units=fat_units,
                protein_units=protein_units,
            )

        # this is a food list and other is a non food

        return Food(
            np.array(self.kcals) * other,
            np.array(self.fat) * other,
            np.array(self.protein) * other,
            self.kcals_units,
            self.fat_units,
            self.protein_units,
        )

    def __rmul__(self, other):
        """
        Multiplies a food's macronutrients by a number.
        This deals with the case that the argument was called with the number first.
        """
        return self.__mul__(other)

    def __eq__(self, other):
        """
        Returns True if the two foods are equal. This also works
        for comparing monthly foods to each other, as their units
        contain 'each month'.
        """
        assert self.units == other.units
        if self.is_list_monthly():
            return (
                (self.kcals == other.kcals).all()
                and (self.fat == other.fat).all()
                and (self.protein == other.protein).all()
            )
        else:
            return (
                self.kcals == other.kcals
                and self.fat == other.fat
                and self.protein == other.protein
            )

    def __ne__(self, other):
        """
        Returns False if the two foods are not equal. This also works
        for comparing monthly foods to each other, as their units
        contain 'each month'.
        """
        assert self.units == other.units
        if self.is_list_monthly():
            return (
                (self.kcals != other.kcals).all()
                and (self.fat != other.fat).all()
                and (self.protein != other.protein).all()
            )
        else:
            return (
                self.kcals != other.kcals
                and self.fat != other.fat
                and self.protein != other.protein
            )


    def plot(self, title="generic food object over time"):
        """
        Use the plotter to plot this food's properties.
        """
        ALTERNATIVE_LAYOUT = False
        if ALTERNATIVE_LAYOUT:
            saveloc = Plotter.plot_food_alternative(self, title)
        else:
            saveloc = Plotter.plot_food(self, title)

        return saveloc

    def __str__(self):
        """
        Returns a string representation of the food.
        """
        return_string = ""
        kcal_string = "    kcals: % s % s\n" % (
            np.round(self.kcals, 5),
            self.kcals_units,
        )

        return_string = return_string + kcal_string

        if self.conversions.include_fat:
            fat_string = "    fat: % s % s\n" % (np.round(self.fat, 5), self.fat_units)
            return_string = return_string + fat_string

        if self.conversions.include_protein:
            protein_string = "    protein: % s % s\n" % (
                np.round(self.protein, 5),
                self.protein_units,
            )
            return_string = return_string + protein_string

        return return_string

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

    # def is_never_negative(self):
    #     """
    #     Checks wether the food's macronutrients are never negative.

    #     However, only checks for the nutrients that are included.
    #     """
    #     if self.is_list_monthly():
    #         self.validate_if_list()

    #         kcals_greater_than_zero = (np.array(self.kcals) >= 0).all()
    #         fat_greater_than_zero = (np.array(self.fat) >= 0).all() or self.conversions.exclude_fat
    #         protein_greater_than_zero = (np.array(self.protein) >= 0).all() or self.conversions.exclude_protein

    #         return (
    #             kcals_greater_than_zero
    #             and fat_greater_than_zero
    #             and protein_greater_than_zero
    #         )

    #     return (
    #         self.kcals >= 0
    #         and (self.fat >= 0 or self.conversions.exclude_fat)
    #         and (self.protein >= 0 or self.conversions.exclude_protein)
    #     )

    # def all_greater_than(self, other):
    #     """
    #     Returns True if the food's macronutrients are greater than the other food's.

    #     if don't include fat or protein, does not check respective nutrients

    #     """
    #     assert self.units == other.units

    #     if self.is_list_monthly():

    #         self.validate_if_list()

    #         return (
    #             (np.array(self.kcals - other.kcals) > 0).all()
    #             and (np.array(self.fat - other.fat) > 0).all()
    #             and (np.array(self.protein - other.protein) > 0).all()
    #         )

    #     return (
    #         self.kcals > other.kcals
    #         and self.fat > other.fat or self.conversions.exclude_fat
    #         and self.protein > other.protein or self.conversions.exclude_protein
    #     )

    def is_never_negative(self):
        """
        Checks wether the food's macronutrients are never negative.
        """
        if self.is_list_monthly():
            self.validate_if_list()

            return (
                (np.array(self.kcals) >= 0).all()
                and ((np.array(self.fat) >= 0).all() or self.conversions.exclude_fat)
                and (
                    (np.array(self.protein) >= 0).all()
                    or self.conversions.exclude_protein
                )
            )

        return (
            self.kcals >= 0
            and (self.fat >= 0 or self.conversions.exclude_fat)
            and (self.protein >= 0 or self.conversions.exclude_protein)
        )

    def all_greater_than(self, other):
        """
        Returns True if the food's macronutrients are greater than the other food's.
        """
        assert self.units == other.units

        if self.is_list_monthly():

            self.validate_if_list()

            return (
                (np.array(self.kcals - other.kcals) > 0).all()
                and (
                    (np.array(self.fat - other.fat) > 0).all()
                    or self.conversions.exclude_fat
                )
                and (
                    (np.array(self.protein - other.protein) > 0).all()
                    or self.conversions.exclude_protein
                )
            )

        return (
            self.kcals > other.kcals
            and (self.fat > other.fat or self.conversions.exclude_fat)
            and (self.protein > other.protein or self.conversions.exclude_protein)
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
                and (
                    (np.array(self.fat - other.fat) < 0).all()
                    or self.conversions.exclude_fat
                )
                and (
                    (np.array(self.protein - other.protein) < 0).all()
                    or self.conversions.exclude_protein
                )
            )

        return (
            self.kcals < other.kcals
            and (self.fat < other.fat or self.conversions.exclude_fat)
            and (self.protein < other.protein or self.conversions.exclude_protein)
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
                or (
                    (np.array(self.fat - other.fat) > 0).any()
                    and self.conversions.exclude_fat
                )
                or (
                    (np.array(self.protein - other.protein) > 0).any()
                    and self.conversions.exclude_protein
                )
            )

        if self.conversions.include_fat:
            greater_than_fat = self.fat > other.fat
        else:
            greater_than_fat = False

        if self.conversions.include_protein:
            greater_than_protein = self.protein > other.protein
        else:
            greater_than_protein = False

        return self.kcals > other.kcals or greater_than_fat or greater_than_protein

    def any_less_than(self, other):
        """
        Returns True if the food's macronutrients are less than the other food's.
        """

        assert self.units == other.units

        if self.is_list_monthly():

            self.validate_if_list()

            return (
                (np.array(self.kcals - other.kcals) < 0).any()
                or (
                    (np.array(self.fat - other.fat) < 0).any()
                    and self.conversions.exclude_fat
                )
                or (
                    (np.array(self.protein - other.protein) < 0).any()
                    and self.conversions.exclude_protein
                )
            )

        if self.conversions.include_fat:
            less_than_fat = self.fat < other.fat
        else:
            less_than_fat = False

        if self.conversions.include_protein:
            less_than_protein = self.protein < other.protein
        else:
            less_than_protein = False

        return self.kcals < other.kcals or less_than_fat or less_than_protein

    def all_greater_than_or_equal_to(self, other):
        """
        Returns True if the food's macronutrients are greater than or equal to
        the other food's.
        """
        assert self.units == other.units

        if self.is_list_monthly():

            self.validate_if_list()

            return (
                (np.array(self.kcals - other.kcals) >= 0).all()
                and (
                    (np.array(self.fat - other.fat) >= 0).all()
                    or self.conversions.exclude_fat
                )
                and (
                    (np.array(self.protein - other.protein) >= 0).all()
                    or self.conversions.exclude_protein
                )
            )

        return (
            self.kcals >= other.kcals
            and (self.fat >= other.fat or self.conversions.exclude_fat)
            and (self.protein >= other.protein or self.conversions.exclude_protein)
        )

    def all_less_than_or_equal_to(self, other):
        """
        Returns True if the food's macronutrients are less than or equal to
        the other food's.

        cases:
            this is food, other is food
            this is food, other is food list
            this is food list, other is food
            this is food list, other is food list
        """

        # this is food, other is food
        if (not self.is_list_monthly()) and (not other.is_list_monthly()):
            assert self.units == other.units

            return (
                self.kcals <= other.kcals
                and (self.fat <= other.fat or self.conversions.exclude_fat)
                and (self.protein <= other.protein or self.conversions.exclude_protein)
            )

        if (not self.is_list_monthly()) and other.is_list_monthly():
            # this is food, other is food list
            assert self.get_units_from_element_to_list() == other.get_units()

        if self.is_list_monthly() and not other.is_list_monthly():
            # this is food list, other is food
            assert self.get_units() == other.get_units_from_element_to_list()

        # this is food list, other is food list
        if (self.is_list_monthly()) and other.is_list_monthly():
            assert self.units == other.units

        return (
            (self.kcals <= other.kcals).all()
            and ((self.fat <= other.fat).all() or self.conversions.exclude_fat)
            and (
                (self.protein <= other.protein).all()
                or self.conversions.exclude_protein
            )
        )

    def any_greater_than_or_equal_to(self, other):
        """
        Returns True if the food's macronutrients are greater than or equal to
        the other food's.
        """
        assert self.units == other.units

        if self.is_list_monthly():

            self.validate_if_list()

            return (
                (np.array(self.kcals - other.kcals) >= 0).any()
                or (
                    (np.array(self.fat - other.fat) >= 0).any()
                    and self.conversions.exclude_fat
                )
                or (
                    (np.array(self.protein - other.protein) >= 0).any()
                    and self.conversions.exclude_protein
                )
            )

        return (
            self.kcals >= other.kcals
            or (self.fat >= other.fat and self.conversions.exclude_fat)
            or (self.protein >= other.protein and self.conversions.exclude_protein)
        )

    def any_less_than_or_equal_to(self, other):
        """
        Returns True if the food's macronutrients are less than or equal to
        the other food's.
        """

        if self.is_list_monthly():

            self.validate_if_list()

            if self.conversions.include_fat:
                less_than_fat = (self.fat - other.fat <= 0).any()
            else:
                less_than_fat = False

            if self.conversions.include_protein:
                less_than_protein = (self.protein - other.protein <= 0).any()
            else:
                less_than_protein = False

            return (
                (np.array(self.kcals - other.kcals) <= 0).any()
                or less_than_fat
                or less_than_protein
            )

        assert self.units == other.units

        if self.conversions.include_fat:
            less_than_fat = self.fat <= other.fat
        else:
            less_than_fat = False

        if self.conversions.include_protein:
            less_than_protein = self.protein <= other.protein
        else:
            less_than_protein = False

        return self.kcals <= other.kcals or less_than_fat or less_than_protein

    def all_equals_zero(self):
        """
        Returns True if the food's macronutrients are equal to zero.
        """
        if self.is_list_monthly():

            self.validate_if_list()

            return (
                (np.array(self.kcals) == 0).all()
                and ((np.array(self.fat) == 0).all() or self.conversions.exclude_fat)
                and (
                    (np.array(self.protein) == 0).all()
                    or self.conversions.exclude_protein
                )
            )

        return (
            self.kcals == 0
            and (self.fat == 0 or self.conversions.exclude_fat)
            and (self.protein == 0 or self.conversions.exclude_protein)
        )

    def any_equals_zero(self):
        """
        Returns True if the food's macronutrients are equal to zero.
        """
        if self.is_list_monthly():

            self.validate_if_list()

            if self.conversions.include_fat:
                zero_fat = (np.array(self.fat) == 0).any()
            else:
                zero_fat = False

            if self.conversions.include_protein:
                zero_protein = (np.array(self.protein) == 0).any()
            else:
                zero_protein = False

            return (np.array(self.kcals) == 0).any() or zero_fat or zero_protein

        if self.conversions.include_fat:
            zero_fat = self.fat == 0
        else:
            zero_fat = False

        if self.conversions.include_protein:
            zero_protein = self.protein == 0
        else:
            zero_protein = False

        return self.kcals == 0 or zero_fat or zero_protein

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

        return (
            self.kcals > 0
            and (self.fat > 0 or self.conversions.exclude_fat)
            and (self.protein > 0 or self.conversions.exclude_protein)
        )

    def any_greater_than_zero(self):
        """
        Returns True if any of the food's macronutrients are greater than zero.
        """
        if self.is_list_monthly():

            self.validate_if_list()

            if self.conversions.include_fat:
                zero_fat = (np.array(self.fat) > 0).any()
            else:
                zero_fat = False

            if self.conversions.include_protein:
                zero_protein = (np.array(self.protein) > 0).any()
            else:
                zero_protein = False

            return (np.array(self.kcals) > 0).any() or zero_fat or zero_protein

        if self.conversions.include_fat:
            zero_fat = self.fat > 0
        else:
            zero_fat = False

        if self.conversions.include_protein:
            zero_protein = self.protein > 0
        else:
            zero_protein = False

        return self.kcals > 0 or zero_fat or zero_protein

    def all_greater_than_or_equal_to_zero(self):
        """
        Returns True if the food's macronutrients are greater than or equal to zero.
        """
        if self.is_list_monthly():

            self.validate_if_list()

            return (
                (np.array(self.kcals) >= 0).all()
                and ((np.array(self.fat) >= 0).all() or self.conversions.exclude_fat)
                and (
                    (np.array(self.protein) >= 0).all()
                    or self.conversions.exclude_protein
                )
            )

        return (
            self.kcals >= 0
            and (self.fat >= 0 or self.conversions.exclude_fat)
            and (self.protein >= 0 or self.conversions.exclude_protein)
        )

    # Helper functions to get properties of the three nutrient values

    def as_list(self):
        """
        Returns the nutrients as an ordered list.
        """
        return np.array([self.kcals, self.fat, self.protein])

    def get_min_nutrient(self):
        """
        Returns the minimum nutrient of the food.

        Can return the minimum of any month of any nutrient if a food list, or just
        `the minimum of any nutrient if a food

        Returns:
        (minimum nutrient name, minimum nutrient value)
        """
        assert self.kcals_units == self.fat_units == self.protein_units

        if self.is_list_monthly():
            to_find_min_of = self.get_min_all_months()
        else:
            to_find_min_of = self

        nutrients_dict = {}
        nutrients_dict["kcals"] = to_find_min_of.kcals

        if self.conversions.include_fat:
            nutrients_dict["fat"] = to_find_min_of.fat

        if self.conversions.include_protein:
            nutrients_dict["protein"] = to_find_min_of.protein

        # Using min() + list comprehension + values()
        # Finding min value keys in dictionary
        min_nutrient_val = min(nutrients_dict.values())
        min_nutrient_name = [
            key for key in nutrients_dict if nutrients_dict[key] == min_nutrient_val
        ][0]

        assert min_nutrient_val <= to_find_min_of.kcals
        # sometimes, this function causes an error for a single fat or protein
        # because the condition before the "or" is false, but doesn't find this for
        # the other because  the condition before the "or" is true
        assert min_nutrient_val <= to_find_min_of.fat or self.conversions.exclude_fat
        assert (
            min_nutrient_val <= to_find_min_of.protein
            or self.conversions.exclude_protein
        )

        return (min_nutrient_name, min_nutrient_val)

    def get_max_nutrient(self):
        """
        Returns the maximum nutrient of the food.

        NOTE: only works on single valued instances of nutrients, not arrays.

        Returns:
        (maximum nutrient name, maximum nutrient value)
        """

        assert self.kcals_units == self.fat_units == self.protein_units

        self.make_sure_not_a_list()

        nutrients_dict = {}
        nutrients_dict["kcals"] = self.kcals

        if self.conversions.include_fat:
            nutrients_dict["fat"] = self.fat

        if self.conversions.include_protein:
            nutrients_dict["protein"] = self.protein

        # Using max() + list comprehension + values()
        # Finding max value keys in dictionary
        max_nutrient_val = max(nutrients_dict.values())
        max_key = [
            key for key in nutrients_dict if nutrients_dict[key] == max_nutrient_val
        ][0]

        assert max_nutrient_val >= self.kcals
        assert max_nutrient_val >= self.fat or self.conversions.exclude_fat
        assert max_nutrient_val >= self.protein or self.conversions.exclude_protein

        return (max_key, max_nutrient_val)

    def get_nutrients_sum(self):
        """
        Sum up the nutrients in all the months, then alter the units to remove
         "each month"
        """
        assert self.is_list_monthly()

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
        assert self.is_list_monthly()
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
        assert self.is_list_monthly()
        return self.get_month(0)

    def get_month(self, index):
        """
        Get the i month's nutrient values, and convert the units from "each" to
        "per"
        """
        assert self.is_list_monthly()
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
        self.make_sure_is_a_list()
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
            self.validate_if_list()
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

        assert zeroed_food.all_greater_than_or_equal_to_zero()

        return zeroed_food

    def get_rounded_to_decimal(self, decimals):
        """
        Round to the nearest decimal place

        to give you an idea how this works:
            >>> np.round([1,-1,.1,-.1,0.01,-0.01],decimals=1)
            array([ 1. , -1. ,  0.1, -0.1,  0. , -0. ])

        NOTE: only implemented for lists at the moment
        """

        self.make_sure_is_a_list()

        rounded = Food(
            kcals=np.round(self.kcals, decimals=decimals),
            fat=np.round(self.fat, decimals=decimals),
            protein=np.round(self.protein, decimals=decimals),
            kcals_units=self.kcals_units,
            fat_units=self.fat_units,
            protein_units=self.protein_units,
        )

        return rounded


    def replace_if_list_with_zeros_is_zero(self, list_with_zeros, replacement):
        """
        replace with the replacement if list_with_zeros is zero

        arguments: list with zeros ( food list ): a list that has zeros in it
                   replacement ( food list, food, or number ): thing used to replace
                                                               the elements

        returns: itself, but with places list_with_zeros zero replaced with replacement

        """
        self.make_sure_is_a_list()
        list_with_zeros.make_sure_is_a_list()

        # a zero is a zero, in all of our unit systems! How convenient.
        # (this is why we don't check units of list_with_zeros)
        # (luckily we're not converting fahrenheit to celcius or something like that)

        # make sure all the same lengths of the lists
        assert list_with_zeros.NMONTHS == self.NMONTHS

        if type(replacement) == Food:
            if replacement.is_list_monthly():
                assert self.NMONTHS == replacement.NMONTHS
                assert self.get_units() == replacement.get_units()
            else:
                assert self.get_units() == replacement.get_units_from_element_to_list()

        # here's an example of what np.where does in this context:
        #   >>> self = np.array([1005,693,0,532,786])   # random numbers
        #   >>> list_with_zeros = np.array([0,1,3,0,5]) # random numbers
        #   >>>
        #   >>> # random numbers or could be a single number
        #   >>> replacement = np.array([101,62,23,3,0])
        #   >>>
        #   >>> # replace with the replacement if list_with_zeros is zero
        #   >>> processed_list = np.where(
        #   >>>     list_with_zeros == 0,
        #   >>>     replacement,
        #   >>>     self,
        #   >>> )
        #   >>>
        #   >>> print(processed_list)
        #   [101 693   0   3 786]

        if type(replacement) == Food:
            # replacement specified per nutrient
            processed_list_kcals = np.where(
                list_with_zeros.kcals == 0,
                replacement.kcals,
                self.kcals,
            )

            processed_list_fat = np.where(
                list_with_zeros.fat == 0,
                replacement.fat,
                self.fat,
            )

            processed_list_protein = np.where(
                list_with_zeros.protein == 0,
                replacement.protein,
                self.protein,
            )
        else:
            # replacement not specified per nutrient
            processed_list_kcals = np.where(
                list_with_zeros.kcals == 0,
                replacement,
                self.kcals,
            )

            processed_list_fat = np.where(
                list_with_zeros.fat == 0,
                replacement,
                self.fat,
            )

            processed_list_protein = np.where(
                list_with_zeros.protein == 0,
                replacement,
                self.protein,
            )

        processed_list = Food(
            kcals=processed_list_kcals,
            fat=processed_list_fat,
            protein=processed_list_protein,
            kcals_units=self.kcals_units,
            fat_units=self.fat_units,
            protein_units=self.protein_units,
        )

        return processed_list
