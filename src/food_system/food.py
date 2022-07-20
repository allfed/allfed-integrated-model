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

module_path = os.path.abspath(os.path.join("../.."))
if module_path not in sys.path:
    sys.path.append(module_path)


class Food:
    """
    A food always has calories, fat, and protein.
    Food applies to biofuels and feed properties as well.
    """

    @classmethod
    def get_nutrient_names(cls):
        """
        Returns the macronutrients of the food.
        """
        return ["kcals", "fat", "protein"]

    def __init__(self, kcals=0, fat=0, protein=0):
        self.kcals = kcals
        self.fat = fat
        self.protein = protein

    # These are all for mathematical operations on the food's macronutrients, such as
    # adding, subtracting, multiplying, and dividing.

    def __str__(self):
        """
        Returns a string representation of the food.
        """
        return "    kcals: % s\n    fat: % s\n    protein: % s" % (
            self.kcals,
            self.fat,
            self.protein,
        )

    def __add__(self, other):
        """
        Adds two foods together.
        """
        kcals = self.kcals + other.kcals
        fat = self.fat + other.fat
        protein = self.protein + other.protein
        return Food(kcals, fat, protein)

    def __sub__(self, other):
        """
        Subtracts two food nutrient quantities from each other.
        """
        kcals = self.kcals - other.kcals
        fat = self.fat - other.fat
        protein = self.protein - other.protein
        return Food(kcals, fat, protein)

    def __truediv__(self, other):
        """
        Divides a food's macronutrients by a number.
        """
        kcals = self.kcals / other
        fat = self.fat / other
        protein = self.protein / other

        return Food(kcals, fat, protein)

    def __mul__(self, other):
        """
        Multiplies a food's macronutrients by a number.
        """
        if type(other) == Food:
            return Food(
                self.kcals * other.kcals,
                self.fat * other.fat,
                self.protein * other.protein,
            )
        kcals = self.kcals * other
        fat = self.fat * other
        protein = self.protein * other

        return Food(kcals, fat, protein)

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
        return (
            self.kcals == other.kcals
            and self.fat == other.fat
            and self.protein == other.protein
        )

    def __ne__(self, other):
        """
        Returns False if the two foods are not equal.
        """
        return (
            self.kcals != other.kcals
            or self.fat != other.fat
            or self.protein != other.protein
        )

    def __gt__(self, other):
        """
        Returns True if the food's macronutrients are greater than the other food's.
        """
        return (
            self.kcals > other.kcals
            and self.fat > other.fat
            and self.protein > other.protein
        )

    def __lt__(self, other):
        """
        Returns True if the food's macronutrients are less than the other food's.
        """
        return (
            self.kcals < other.kcals
            and self.fat < other.fat
            and self.protein < other.protein
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

        NOTE: only works on single valued instances of nutrients, not arrays.

        Returns:
        (minimum nutrient name, minimum nutrient value)
        """
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

        return (min_key, min_nutrient_val)

    def get_max_nutrient(self):
        """
        Returns the maximum nutrient of the food.

        NOTE: only works on single valued instances of nutrients, not arrays.

        Returns:
        (maximum nutrient name, maximum nutrient value)
        """
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

        return (max_key, max_nutrient_val)

    def get_nutrients_sum(self):
        return Food(sum(self.kcals), sum(self.fat), sum(self.protein))

    def get_first_month(self):
        return Food(self.kcals[0], self.fat[0], self.protein[0])
