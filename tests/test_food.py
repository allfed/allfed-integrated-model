"""
Test Suite for the food module.
"""
import os
import sys


module_path = os.path.abspath(os.path.join("../.."))
if module_path not in sys.path:
    sys.path.append(module_path)

from src.food_system.food import Food

def test_food_init():
    pass