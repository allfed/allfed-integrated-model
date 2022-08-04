"""
Tests if the unit conversion is working as expected.
"""
from pytest import approx
from pytest import raises

from src.food_system import unit_conversions as uc
from src.food_system.food import Food

def test_initiliaze_unit_conversions():
    """
    Tests if the unit conversion is initialized as expected.
    """
    unit_conversions = uc.UnitConversions()
    assert unit_conversions is not None

# Running unit_conversion_directly does not really work, as it is intented 
# to be used in the food class. Therefore, we need to run the unit conversion
# in the food system class.

def create_food_monthly(kcals=[1,2,1], fat=[1,2,2], protein=[1,2,2]):
    """
    creates a food instance that has monthly values and returns it
    """
    food_monthly = Food(kcals=kcals, fat=fat, protein=protein,
                         kcals_units="kcals each months",
                         fat_units="kcals each months",
                         protein_units="kcals each months")
    return food_monthly


def test_set_nutrition_requirement_scalar():
    """
    Tests if the function works with a scalar food
    """
    food1 = Food()
    food1.set_nutrition_requirements(kcals_daily=1, fat_daily=1, protein_daily=1, population=1)
    assert food1.days_in_month == 30
    assert food1.kcals_daily == 1
    assert food1.fat_daily == 1
    assert food1.protein_daily == 1
    assert food1.kcals_monthly == 30
    assert food1.fat_monthly == 1/1e6*30/1000
    assert food1.protein_monthly == 1/1e6*30/1000
    assert food1.billion_kcals_needed == 30 * 1 / 1e9
    assert food1.thou_tons_fat_needed == food1.fat_monthly * 1 
    assert food1.thou_tons_protein_needed == food1.protein_monthly * 1
    assert food1.population == 1
    assert food1.NUTRITION_PROPERTIES_ASSIGNED == True


def test_get_units_from_list_to_total():
    """
    Change the units from monthly to single month
    """
    food1 = create_food_monthly()
    units = food1.get_units_from_list_to_total()
    assert units == ["kcals","kcals","kcals"]


def test_get_units_from_list_to_total_wrong_input():
    """
    Change the units from monthly to single month
    """
    food1 = Food()
    with raises(AssertionError):
        food1.get_units_from_list_to_total()


def test_set_units_from_list_to_total():
    """
    Change the units from monthly to single month
    """
    food1 = create_food_monthly()
    food1.set_units_from_list_to_total()
    assert food1.kcals_units == "kcals"
    assert food1.fat_units == "kcals"
    assert food1.protein_units == "kcals"


def test_set_units_from_list_to_total_wrong_input():
    """
    Change the units from monthly to single month
    """
    food1 = Food()
    with raises(AssertionError):
        food1.set_units_from_list_to_total()


def test_get_units_from_list_to_element():
    """
    Change the units from monthly to single month
    """
    food1 = create_food_monthly()
    units = food1.get_units_from_list_to_element()
    for unit in units:
        assert "each months" not in unit
        assert "per month" in unit


def test_get_units_from_list_to_element_wrong_input():
    """
    Change the units from monthly to single month
    """
    food1 = Food()
    with raises(AssertionError):
        food1.get_units_from_list_to_element()


def test_set_units_from_list_to_element():
    """
    Change the units from monthly to single month
    """
    food1 = create_food_monthly()
    food1.set_units_from_list_to_element()
    assert "each month" not in food1.kcals_units 
    assert "per month" in food1.kcals_units
    assert "each month" not in food1.fat_units
    assert "per month" in food1.fat_units
    assert "each month" not in food1.protein_units
    assert "per month" in food1.protein_units


def test_set_units_from_list_to_element_wrong_input():
    """
    Change the units from monthly to single month
    """
    food1 = Food()
    with raises(AssertionError):
        food1.set_units_from_list_to_element()


def test_get_units_from_element_to_list():
    """
    Change the units from single month to monthly
    """
    food1 = Food()
    units = food1.get_units_from_element_to_list()
    for unit in units:
        assert "each month" in unit


def test_get_units_from_element_to_list_wrong_input():
    """
    Change the units from single month to monthly
    """
    food1 = create_food_monthly()
    with raises(AssertionError):
        food1.get_units_from_element_to_list()


def test_set_units_from_element_to_list():
    """
    Change the units from single month to monthly
    """
    food1 = Food()
    food1.set_units_from_element_to_list()
    assert "each month" in food1.kcals_units
    assert "each month" in food1.fat_units
    assert "each month" in food1.protein_units


def test_set_units_from_element_to_list_wrong_input():
    """
    Change the units from single month to monthly
    """
    food1 = create_food_monthly()
    with raises(AssertionError):
        food1.set_units_from_element_to_list()


def test_get_units():
    """
    Tests if the right units are returned
    """
    food1 = create_food_monthly()
    units = food1.get_units()
    assert units == ["kcals each months","kcals each months","kcals each months"]


def test_set_units