"""
Tests if the unit conversion is working as expected.
"""
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


def create_food_monthly(
    kcals=[1, 2, 1],
    fat=[1, 2, 2],
    protein=[1, 2, 2],
    kcals_units="kcals each months",
    fat_units="kcals each months",
    protein_units="kcals each months",
):
    """
    creates a food instance that has monthly values and returns it
    """
    food_monthly = Food(
        kcals=kcals,
        fat=fat,
        protein=protein,
        kcals_units=kcals_units,
        fat_units=fat_units,
        protein_units=protein_units,
    )
    return food_monthly


def test_set_nutrition_requirement_scalar():
    """
    Tests if the function works with a scalar food
    """
    food1 = Food()

    Food.conversions.set_nutrition_requirements(
        kcals_daily=1,
        fat_daily=1,
        protein_daily=1,
        include_fat=True,
        include_protein=True,
        population=1,
    )
    assert Food.conversions.days_in_month == 30
    assert Food.conversions.kcals_daily == 1
    assert Food.conversions.fat_daily == 1
    assert Food.conversions.protein_daily == 1
    assert Food.conversions.kcals_monthly == 30
    assert Food.conversions.fat_monthly == 1 / 1e6 * 30 / 1000
    assert Food.conversions.protein_monthly == 1 / 1e6 * 30 / 1000
    assert Food.conversions.billion_kcals_needed == 30 * 1 / 1e9
    assert Food.conversions.thou_tons_fat_needed == Food.conversions.fat_monthly * 1
    assert (
        Food.conversions.thou_tons_protein_needed
        == Food.conversions.protein_monthly * 1
    )
    assert Food.conversions.population == 1
    assert Food.conversions.NUTRITION_PROPERTIES_ASSIGNED is True


def test_get_units_from_list_to_total():
    """
    Change the units from monthly to single month
    """
    food1 = create_food_monthly()
    units = food1.get_units_from_list_to_total()
    assert units == ["kcals", "kcals", "kcals"]


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
    assert units == ["kcals each months", "kcals each months", "kcals each months"]


def test_set_units():
    """
    Tests if the right units are set
    """
    food1 = create_food_monthly()
    food1.set_units(
        kcals_units="kcals each month",
        fat_units="kcals each month",
        protein_units="kcals each month",
    )
    assert food1.kcals_units == "kcals each month"
    assert food1.fat_units == "kcals each month"
    assert food1.protein_units == "kcals each month"


def test_is_a_ratio_scalar_food():
    """
    Tests if the right units are set
    """
    food1 = Food()
    assert food1.is_a_ratio() is False
    food2 = Food(kcals_units="ratio", fat_units="ratio", protein_units="ratio")
    assert food2.is_a_ratio() is True


def test_is_a_ratio_monthly_food():
    """
    Tests if the right units are set
    """
    food1 = create_food_monthly()
    assert food1.is_a_ratio() is False

    food2 = create_food_monthly(
        kcals_units="ratio each month",
        fat_units="ratio each month",
        protein_units="ratio each month",
    )
    assert food2.is_a_ratio() is True


def test_is_unit_percent_scalar_food():
    """
    Tests if the right units are set
    """
    food1 = Food()
    assert food1.is_units_percent() is False
    food2 = Food(kcals_units="percent", fat_units="percent", protein_units="percent")
    assert food2.is_units_percent() is True


def test_is_unit_percent_monthly_food():
    """
    Tests if the right units are set
    """
    food1 = create_food_monthly(
        kcals_units="percent each month",
        fat_units="percent each month",
        protein_units="percent each month",
    )
    assert food1.is_units_percent() is True
    food2 = create_food_monthly(
        kcals_units="kcals each month",
        fat_units="kcals each month",
        protein_units="kcals each month",
    )
    assert food2.is_units_percent() is False


def test_in_units_billions_fed():
    """
    Tests if the units are correctly converted to billions fed
    """
    # Test conversion from

    Food.conversions.set_nutrition_requirements(
        kcals_daily=2100,
        fat_daily=1,
        protein_daily=1,
        include_fat=True,
        include_protein=True,
        population=1e9,
    )
    food = Food(
        kcals=1,
        protein=10,
        fat=10,
        kcals_units="billion kcals per month",
        fat_units="thousand tons per month",
        protein_units="thousand tons per month",
    )

    food_converted = food.in_units_billions_fed()

    assert food_converted.kcals_units == "billion people fed per month"
    assert food_converted.fat_units == "billion people fed per month"
    assert food_converted.protein_units == "billion people fed per month"

    # 1 billion kcals per month is X billion people fed per month
    # so 1 kcal per month is X people fed per month
    # we know 2100*30 kcal per month is 1 person fed per month
    # so 1 kcal per month is 1/(2100*30) people fed per month

    assert abs(food_converted.kcals - 1 * 1e9 / 30 / 2100 / 1e9) < 1e-9
