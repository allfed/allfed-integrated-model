"""
Test Suite for the food module.
"""
import pytest
from src.food_system.food import Food


def test_food_init():
    """
    Tests if a instance of the Food class can be created
    """
    assert Food() is not None
    food = Food()
    assert isinstance(food, Food)


def test_get_nutrient_names():
    """
    Tests of the correct nutrients are returned
    """
    assert Food.get_nutrient_names() == ['kcals', 'fat', 'protein']


def test_ratio_one():
    """
    Tests if the ratio one method returns the expected result
    """
    test_food = Food.ratio_one()
    assert test_food.kcals == 1
    assert test_food.fat == 1
    assert test_food.protein == 1
    assert test_food.kcals_units == "ratio"
    assert test_food.fat_units == "ratio"
    assert test_food.protein_units == "ratio"


def test_ratio_zero():
    """
    Tests if the ratio zero method returns the expected result
    """
    test_food = Food.ratio_zero()
    assert test_food.kcals == 0
    assert test_food.fat == 0
    assert test_food.protein == 0
    assert test_food.kcals_units == "ratio"
    assert test_food.fat_units == "ratio"
    assert test_food.protein_units == "ratio"


def test_addition():
    """
    Tests if two instances of the Food class can be added
    """
    food1 = Food(kcals=1, fat=1, protein=1)
    food2 = Food(kcals=1, fat=1, protein=1)
    food3 = food1 + food2
    assert food3.kcals == 2
    assert food3.fat == 2
    assert food3.protein == 2


def test_failed_addition():
    """
    Tests if two foods with different units create an assertion
    error when added
    """
    food1 = Food(kcals=1, fat=1, protein=1)
    food2 = Food(kcals=1, fat=1, protein=1, kcals_units="g", fat_units="g", protein_units="g")
    with pytest.raises(AssertionError):
        food3 = food1 + food2


def test_subtraction():
    """
    Tests if two instances of the Food class can be subtracted
    """
    food1 = Food(kcals=1, fat=1, protein=1)
    food2 = Food(kcals=1, fat=1, protein=1)
    food3 = food1 - food2
    assert food3.kcals == 0
    assert food3.fat == 0
    assert food3.protein == 0


def test_failed_subtraction():
    """
    Tests if two foods with different units create an assertion
    error when subtracted
    """
    food1 = Food(kcals=1, fat=1, protein=1)
    food2 = Food(kcals=1, fat=1, protein=1, kcals_units="g", fat_units="g", protein_units="g")
    with pytest.raises(AssertionError):
        food3 = food1 - food2


def test_multiplication_scalar():
    """
    Tests if an instance of the Food class can be multiplied by a scalar
    """
    food1 = Food(kcals=1, fat=1, protein=1)
    food2 = food1 * 2
    assert food2.kcals == 2
    assert food2.fat == 2
    assert food2.protein == 2


def test_multiplication_by_food():
    """
    Tests if an instance of the Food class can be multiplied by another instance of the Food class
    """
    food1 = Food(kcals=1, fat=1, protein=1)
    food2 = Food(kcals=1, fat=1, protein=1)
    food3 = food1 * food2
    assert food3.kcals == 1
    assert food3.fat == 1
    assert food3.protein == 1