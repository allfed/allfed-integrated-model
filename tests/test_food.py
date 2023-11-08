"""
Test Suite for the food module.
"""
import pytest
import numpy as np
from src.food_system.food import Food

Food.conversions.set_nutrition_requirements(
    kcals_daily=100,
    fat_daily=10,
    protein_daily=10,
    include_fat=True,
    include_protein=True,
    population=1000,
)


def create_food_monthly(kcals=[1, 2, 1], fat=[1, 2, 2], protein=[1, 2, 2]):
    """
    creates a food instance that has monthly values and returns it
    """
    food_monthly = Food(
        kcals=np.array(kcals),
        fat=np.array(fat),
        protein=np.array(protein),
        kcals_units="kcals each month",
        fat_units="kcals each month",
        protein_units="kcals each month",
    )
    return food_monthly


def test_get_nutrient_names():
    """
    Tests of the correct nutrients are returned
    """
    assert Food.get_nutrient_names() == ["kcals", "fat", "protein"]


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


def test_food_init():
    """
    Tests if a instance of the Food class can be created
    """
    assert Food() is not None
    food = Food()
    assert isinstance(food, Food)


def test_make_sure_not_a_list():
    """
    Tests not a list detects correctly
    """
    with pytest.raises(AssertionError):
        create_food_monthly().make_sure_not_a_list()


def test_make_sure_is_a_list():
    """
    Tests if make sure is a list function correctly detects
    scalar foods
    """
    food1 = Food(kcals=1, fat=1, protein=1)
    with pytest.raises(AssertionError):
        food1.make_sure_is_a_list()


def test_make_sure_fat_protein_zero_if_kcals_is_zero_scalar_food():
    """
    Tests if the fat and protein values are zero if the kcals value is zero
    """
    food1 = Food(kcals=0, fat=1, protein=1)
    with pytest.raises(AssertionError):
        food1.make_sure_fat_protein_zero_if_kcals_is_zero()


def test_ensure_other_list_zero_if_this_is_zero():
    """
    Tests ensure_other_list_zero_if_this_is_zero

    This test requires both foods to be list type.

    """
    food1 = Food(
        kcals=[0, 0, 0, 0],
        fat=[0, 0, 0, 0],
        protein=[0, 0, 0, 0],
        kcals_units="kcals each month",
        fat_units="kcals each month",
        protein_units="kcals each month",
    )
    food2 = Food(
        kcals=[0, 0, 0, 0],
        fat=[0, 0, 0, 0],
        protein=[0, 0, 0, 0],
        kcals_units="kcals each month",
        fat_units="kcals each month",
        protein_units="kcals each month",
    )
    food1.ensure_other_list_zero_if_this_is_zero(food2)


def test_make_sure_fat_protein_zero_if_kcals_is_zero_monthly_food():
    """
    Tests if the fat and protein values are zero if the kcals value is zero
    """
    food1 = create_food_monthly(kcals=[0, 0, 0], fat=[1, 1, 1], protein=[1, 1, 1])
    with pytest.raises(AssertionError):
        food1.make_sure_fat_protein_zero_if_kcals_is_zero()


def test_make_sure_not_nan_scalar_food():
    """
    Tests if make sure not nan function works correctly
    """
    food1 = Food(kcals=1, fat=1, protein=np.nan)
    with pytest.raises(AssertionError):
        food1.make_sure_not_nan()


def test_min_elementwise():
    """
    Tests if the min_elementwise function produces the correct result
    """
    food1 = create_food_monthly(kcals=[10, 20, 30], fat=[5, 15, 25], protein=[1, 2, 3])
    food2 = create_food_monthly(kcals=[5, 25, 15], fat=[10, 5, 20], protein=[2, 1, 4])

    # Get the minimum Food object using min_elementwise method
    min_food = Food.min_elementwise(food1, food2)

    # Check the values of the resulting Food object
    assert np.array_equal(min_food.kcals, [5, 20, 15]), "Minimum kcals not as expected"
    assert np.array_equal(min_food.fat, [5, 5, 20]), "Minimum fat not as expected"
    assert np.array_equal(
        min_food.protein, [1, 1, 3]
    ), "Minimum protein not as expected"

    # Check the units of the resulting Food object
    assert min_food.kcals_units == "kcals each month", "Kcals units mismatch"
    assert min_food.fat_units == "kcals each month", "Fat units mismatch"
    assert min_food.protein_units == "kcals each month", "Protein units mismatch"


def test_get_remaining_food_needed_and_amount_used():
    demand = Food([2000, 2500], [50, 50], [100, 120], "kcal", "g", "g")
    resource = Food([1500, 2700], [40, 50], [90, 110], "kcal", "g", "g")
    max_fraction = 0.9

    (
        remaining,
        demand_satisfied_by_resource,
    ) = Food.get_remaining_food_needed_and_amount_used(demand, resource, max_fraction)

    expected_satisfied = Food(
        [1500, 0.9 * 2500], [40, 0.9 * 50], [90, 0.9 * 120], "kcal", "g", "g"
    )
    expected_remaining = Food(
        [500, 0.1 * 2500], [10, 0.1 * 50], [10, 0.1 * 120], "kcal", "g", "g"
    )

    assert (
        demand_satisfied_by_resource == expected_satisfied
    ), f"Satisfied demand: \nExpected: \n{expected_satisfied}\nBut got: \n{demand_satisfied_by_resource}\n"
    assert (
        remaining == expected_remaining
    ), f"Remaining resource: \nExpected: \n{expected_result}\nBut got: \n{result}\n"


def test_make_sure_not_nan_monthly_food():
    """
    Tests if make sure not nan function works correctly
    """
    food1 = create_food_monthly(kcals=[1, 1, 1], fat=[1, 1, np.nan], protein=[1, 1, 1])
    with pytest.raises(AssertionError):
        food1.make_sure_not_nan()


def test_addition_scalar_food():
    """
    Tests if two instances of the Food class can be added
    """
    food1 = Food(kcals=1, fat=1, protein=1)
    food2 = Food(kcals=1, fat=1, protein=1)
    food3 = food1 + food2
    assert food3.kcals == 2
    assert food3.fat == 2
    assert food3.protein == 2


def test_addition_monthly_food():
    """
    Tests if two monthly food instances can be added
    """
    food1 = create_food_monthly()
    food2 = create_food_monthly()
    food3 = food1 + food2
    assert (food3.kcals == np.array([2, 4, 2])).all()
    assert (food3.fat == np.array([2, 4, 4])).all()
    assert (food3.protein == np.array([2, 4, 4])).all()

    assert food3.kcals_units == "kcals each month"
    assert food3.fat_units == "kcals each month"
    assert food3.protein_units == "kcals each month"


def test_failed_addition():
    """
    Tests if two foods with different units create an assertion
    error when added
    """
    food1 = Food(kcals=1, fat=1, protein=1)
    food2 = Food(
        kcals=1, fat=1, protein=1, kcals_units="g", fat_units="g", protein_units="g"
    )
    with pytest.raises(AssertionError):
        food1 + food2


def test_subtraction_scalar_food():
    """
    Tests if two instances of the Food class can be subtracted
    """
    food1 = Food(kcals=1, fat=1, protein=1)
    food2 = Food(kcals=1, fat=1, protein=1)
    food3 = food1 - food2
    assert food3.kcals == 0
    assert food3.fat == 0
    assert food3.protein == 0


def test_subtraction_monthly_food():
    """
    Tests if two monthly food instances can be subtracted
    """
    food1 = create_food_monthly()
    food2 = create_food_monthly()
    food3 = food1 - food2
    assert (food3.kcals == np.array([0, 0, 0])).all()
    assert (food3.fat == np.array([0, 0, 0])).all()
    assert (food3.protein == np.array([0, 0, 0])).all()

    assert food3.kcals_units == "kcals each month"
    assert food3.fat_units == "kcals each month"
    assert food3.protein_units == "kcals each month"


def test_failed_subtraction():
    """
    Tests if two foods with different units create an assertion
    error when subtracted
    """
    food1 = Food(kcals=1, fat=1, protein=1)
    food2 = Food(
        kcals=1, fat=1, protein=1, kcals_units="g", fat_units="g", protein_units="g"
    )
    with pytest.raises(AssertionError):
        food1 - food2


def test_division_scalar_by_scalar():
    """
    Tests if two instances of the Food class can be divided
    """
    food1 = Food(kcals=1, fat=1, protein=1)
    food2 = Food(kcals=1, fat=1, protein=1)
    food3 = food1 / food2
    assert food3.kcals == 1
    assert food3.fat == 1
    assert food3.protein == 1
    assert food3.kcals_units == "ratio"
    assert food3.fat_units == "ratio"
    assert food3.protein_units == "ratio"


def test_division_scalar_by_monthly():
    """
    Tests if a scalar food object can be divided by a food list
    This shoudl fail.
    """
    food1 = Food(kcals=1, fat=1, protein=1)
    food2 = create_food_monthly()
    with pytest.raises(AssertionError):
        food1 / food2


def test_division_monthly_by_scalar():
    """
    Tests if a food list can be divided by a scalar food object
    This should fail.
    """
    food1 = create_food_monthly()
    food2 = Food(kcals=1, fat=1, protein=1)
    with pytest.raises(AssertionError):
        food1 / food2


def test_division_scalar_by_number():
    """
    Tests if a scalar food object can be divided by a number
    """
    food1 = Food(kcals=1, fat=1, protein=1)
    food2 = food1 / 2
    assert food2.kcals == 0.5
    assert food2.fat == 0.5
    assert food2.protein == 0.5


def test_division_monthly_by_number():
    """
    Tests if a food list can be divided by a number
    This should fail.
    """
    food1 = create_food_monthly()
    food1 / 2


def test_divison_monthly_by_monthly():
    """
    Tests if a food list can be divided by a food list
    """
    food1 = create_food_monthly()
    food2 = create_food_monthly()
    food3 = food1 / food2
    assert (food3.kcals == [1, 1, 1]).all()
    assert (food3.fat == [1, 1, 1]).all()
    assert (food3.protein == [1, 1, 1]).all()
    assert food3.kcals_units == "ratio each month"
    assert food3.fat_units == "ratio each month"
    assert food3.protein_units == "ratio each month"


def test_getitem():
    """
    Test get item method
    """
    # Should only work for monthly foods
    food1 = Food(kcals=1, fat=1, protein=1)
    with pytest.raises(AssertionError):
        food1[0]
    food2 = create_food_monthly()
    assert food2[0].kcals == 1


def test_multiplication_scalar():
    """
    Tests if an instance of the Food class can be multiplied by a scalar
    """
    food1 = Food(kcals=1, fat=1, protein=1)
    food2 = food1 * 2
    assert food2.kcals == 2
    assert food2.fat == 2
    assert food2.protein == 2


def test_multiplication_by_scalar_food():
    """
    Tests if an instance of the Food class can be multiplied by another instance of the Food class
    """
    food1 = Food(kcals=1, fat=1, protein=1)
    food2 = Food(kcals=1, fat=1, protein=1)
    # list multiplication only works if one or both is a ratios right now
    with pytest.raises(AssertionError):
        food1 * food2


def test_multiplication_monthly_food_by_scalar_food():
    """
    Tests if an instance of the Food class can be multiplied by another instance of the Food class
    """
    food1 = create_food_monthly()
    food2 = Food(
        kcals=1,
        fat=1,
        protein=1,
        kcals_units="ratio",
        fat_units="ratio",
        protein_units="ratio",
    )
    food3 = food1 * food2
    assert (food3.kcals == [1, 2, 1]).all()
    assert (food3.fat == [1, 2, 2]).all()
    assert (food3.protein == [1, 2, 2]).all()
    assert food3.kcals_units == "kcals each month"
    assert food3.fat_units == "kcals each month"
    assert food3.protein_units == "kcals each month"


def test_multiplication_monthly_food():
    """
    Tests if an instance of the Food class can be multiplied by another instance of the Food class
    """
    food1 = create_food_monthly()
    food2 = Food(
        kcals=[1, 1, 2],
        fat=[1, 1, 2],
        protein=[1, 1, 2],
        kcals_units="ratio each month",
        fat_units="ratio each month",
        protein_units="ratio each month",
    )
    food3 = food1 * food2
    assert (food3.kcals == [1, 2, 2]).all()
    assert (food3.fat == [1, 2, 4]).all()
    assert (food3.protein == [1, 2, 4]).all()
    assert food3.kcals_units == "kcals each month"
    assert food3.fat_units == "kcals each month"
    assert food3.protein_units == "kcals each month"


def test_failed_multiplication_by_food():
    """
    Multiplies two food sources with different units
    """
    food1 = Food(kcals=1, fat=1, protein=1)
    food2 = Food(
        kcals=1, fat=1, protein=1, kcals_units="g", fat_units="g", protein_units="g"
    )
    with pytest.raises(AssertionError):
        food1 * food2


def test_multiplication_unit_by_ratio():
    """
    Tests the multiplication of a unit food with a ratio food
    """
    food1 = Food(kcals=1, fat=1, protein=1)
    food2 = Food(
        kcals=1,
        fat=1,
        protein=1,
        kcals_units="ratio",
        fat_units="ratio",
        protein_units="ratio",
    )
    food3 = food1 * food2
    assert food3.kcals == 1
    assert food3.fat == 1
    assert food3.protein == 1


def test_multiplication_ratio_by_unit():
    """
    Tests the multiplication of a ratio food with a unit food
    """
    food1 = Food(
        kcals=1,
        fat=1,
        protein=1,
        kcals_units="ratio",
        fat_units="ratio",
        protein_units="ratio",
    )
    food2 = Food(kcals=1, fat=1, protein=1)
    food3 = food1 * food2
    assert food3.kcals == 1
    assert food3.fat == 1
    assert food3.protein == 1


def test_multiplication_ratio_by_ratio():
    """
    Tests the multiplication of a ratio food with a ratio food
    """
    food1 = Food(
        kcals=1,
        fat=1,
        protein=1,
        kcals_units="ratio",
        fat_units="ratio",
        protein_units="ratio",
    )
    food2 = Food(
        kcals=1,
        fat=1,
        protein=1,
        kcals_units="ratio",
        fat_units="ratio",
        protein_units="ratio",
    )
    food3 = food1 * food2
    assert food3.kcals == 1
    assert food3.fat == 1
    assert food3.protein == 1


def test_foods_equal_scalar():
    """
    Tests if two scalar foods are equal
    """
    food1 = Food(kcals=1, fat=1, protein=1)
    food2 = Food(kcals=1, fat=1, protein=1)
    assert food1 == food2


def test_foods_equal_monthly():
    """
    Tests if two monthly foods are equal
    """
    assert (create_food_monthly() == create_food_monthly()).all()


def test_foods_not_equal_scalar():
    """
    Tests if two foods are not equal
    """
    food1 = Food(kcals=1, fat=1, protein=1)
    food2 = Food(kcals=2, fat=2, protein=2)
    assert food1 != food2

    assert create_food_monthly() != create_food_monthly(kcals=[1, 2, 3])


def test_food_failed_equal():
    """
    Tests if comparing two foods with different units fails
    """
    food1 = Food(kcals=1, fat=1, protein=1)
    food2 = Food(
        kcals=1, fat=1, protein=1, kcals_units="g", fat_units="g", protein_units="g"
    )
    with pytest.raises(AssertionError):
        assert food1 == food2


def test_food_failed_not_equal():
    """
    Tests if comparing two foods with different units fails
    """
    food1 = Food(kcals=1, fat=1, protein=1)
    food2 = Food(
        kcals=1, fat=1, protein=1, kcals_units="g", fat_units="g", protein_units="g"
    )
    with pytest.raises(AssertionError):
        assert food1 != food2


def test_negation_scalar_food():
    """
    Tests if the negation of a food is correct
    """
    food1 = Food(kcals=1, fat=1, protein=1)
    food2 = -food1
    assert food2.kcals == -1
    assert food2.fat == -1
    assert food2.protein == -1


def test_negation_monthly_food():
    """
    Tests if the negation of a food is correct
    """
    food1 = create_food_monthly()
    food2 = -food1

    assert (food2.kcals == [-1, -2, -1]).all()
    assert (food2.fat == [-1, -2, -2]).all()
    assert (food2.protein == [-1, -2, -2]).all()

    assert food2.kcals_units == "kcals each month"
    assert food2.fat_units == "kcals each month"
    assert food2.protein_units == "kcals each month"


def test_food_failed_negation():
    """
    Tests negatation other way around
    """
    food1 = Food(kcals=1, fat=1, protein=1)
    food2 = -food1
    with pytest.raises(AssertionError):
        assert food2.kcals == 1
        assert food2.fat == 1
        assert food2.protein == 1


def test_is_list_monthly():
    """
    Tests if the is_list_monthly method returns the expected result
    """
    food1 = Food(kcals=1, fat=1, protein=1)
    assert not food1.is_list_monthly()
    assert create_food_monthly().is_list_monthly()


def test_is_never_negative_scalar_food():
    """
    Tests if the is_never_negative method returns the expected result
    """
    food1 = Food(kcals=1, fat=1, protein=1)
    assert food1.is_never_negative()


def test_is_never_negative_monthly_food():
    """
    Tests if the is_never_negative method returns the expected result
    """
    food1 = create_food_monthly()
    assert food1.is_never_negative() == True


def test_is_never_negative_false():
    """
    Tests if the is_never_negative method returns the expected result
    """
    food1 = Food(
        kcals=-11, fat=1, protein=1, kcals_units="g", fat_units="g", protein_units="g"
    )
    assert not food1.is_never_negative()


def test_all_greater_than_scalar_food():
    """
    Tests if all nutrients of a food are larger than those of another food
    """
    food1 = Food(kcals=1, fat=1, protein=1)
    food2 = Food(kcals=2, fat=2, protein=2)
    assert not food1.all_greater_than(food2)
    assert food2.all_greater_than(food1)


def test_all_greater_than_monthly_food():
    """
    Tests if all nutrients of a food are larger than those of another food
    """
    food1 = create_food_monthly()
    food2 = create_food_monthly()
    food3 = create_food_monthly(kcals=[5, 5, 5], fat=[5, 5, 5], protein=[5, 5, 5])
    assert food1.all_greater_than(food2) == False
    assert food2.all_greater_than(food1) == False
    assert food1.all_greater_than(food3) == False
    assert food3.all_greater_than(food1) == True


def test_all_greater_than_different_unit():
    """
    Tests if greater than fail when the units are different
    """
    food1 = Food(
        kcals=1, fat=1, protein=1, kcals_units="g", fat_units="g", protein_units="g"
    )
    food2 = Food(kcals=2, fat=2, protein=2)
    with pytest.raises(AssertionError):
        assert not food1.all_greater_than(food2)
        assert food2.all_greater_than(food1)


def test_all_less_than_scalar_food():
    """
    Tests if all nutrients of a food are smaller than those of another food
    """
    food1 = Food(kcals=1, fat=1, protein=1)
    food2 = Food(kcals=2, fat=2, protein=2)
    assert food1.all_less_than(food2)
    assert not food2.all_less_than(food1)


def test_all_less_than_monthly_food():
    """
    Tests if all nutrients of a food are smaller than those of another food
    """
    food1 = create_food_monthly()
    food2 = create_food_monthly()
    food3 = create_food_monthly(kcals=[5, 5, 5], fat=[5, 5, 5], protein=[5, 5, 5])
    assert food1.all_less_than(food2) == False
    assert food2.all_less_than(food1) == False
    assert food1.all_less_than(food3) == True
    assert food3.all_less_than(food1) == False


def test_all_less_than_different_unit():
    """
    Tests if less than fail when the units are different
    """
    food1 = Food(
        kcals=1, fat=1, protein=1, kcals_units="g", fat_units="g", protein_units="g"
    )
    food2 = Food(kcals=2, fat=2, protein=2)
    with pytest.raises(AssertionError):
        assert food1.all_less_than(food2)
        assert not food2.all_less_than(food1)


def test_any_greater_than_scalar_food():
    """
    Tests if any nutrient of a food is larger than those of another food
    """
    food1 = Food(kcals=1, fat=1, protein=1)
    food2 = Food(kcals=2, fat=1, protein=1)
    assert not food1.any_greater_than(food2)
    assert food2.any_greater_than(food1)


def test_any_greater_than_monthly_food():
    """
    Tests if any nutrient of a food is larger than those of another food
    """
    food1 = create_food_monthly()
    food2 = create_food_monthly()
    food3 = create_food_monthly(kcals=[5, 5, 5], fat=[5, 5, 5], protein=[5, 5, 5])
    assert food1.any_greater_than(food2) == False
    assert food2.any_greater_than(food1) == False
    assert food1.any_greater_than(food3) == False
    assert food3.any_greater_than(food1) == True


def test_any_greater_than_different_unit():
    """
    Tests if any greater than fail when the units are different
    """
    food1 = Food(
        kcals=1, fat=1, protein=1, kcals_units="g", fat_units="g", protein_units="g"
    )
    food2 = Food(kcals=2, fat=1, protein=1)
    with pytest.raises(AssertionError):
        assert not food1.any_greater_than(food2)
        assert food2.any_greater_than(food1)


def test_any_less_than_scalar_food():
    """
    Tests if any nutrient of a food is smaller than those of another food
    """
    food1 = Food(kcals=1, fat=1, protein=1)
    food2 = Food(kcals=2, fat=1, protein=1)
    assert food1.any_less_than(food2)
    assert not food2.any_less_than(food1)


def test_any_less_than_monthly_food():
    """
    Tests if any nutrient of a food is smaller than those of another food
    """
    food1 = create_food_monthly()
    food2 = create_food_monthly()
    food3 = create_food_monthly(kcals=[5, 5, 5], fat=[5, 5, 5], protein=[5, 5, 5])
    assert food1.any_less_than(food2) == False  # these should be identical
    assert food2.any_less_than(food1) == False
    assert food1.any_less_than(food3) == True
    assert food3.any_less_than(food1) == False


def test_any_less_than_different_unit():
    """
    Tests if any less than fail when the units are different
    """
    food1 = Food(
        kcals=1, fat=1, protein=1, kcals_units="g", fat_units="g", protein_units="g"
    )
    food2 = Food(kcals=2, fat=1, protein=1)
    with pytest.raises(AssertionError):
        assert food1.any_less_than(food2)
        assert not food2.any_less_than(food1)


def test_all_greater_than_or_equal_scalar_food():
    """
    Tests if all nutrients of a food are larger than or equal those of another food
    """
    food1 = Food(kcals=1, fat=1, protein=1)
    food2 = Food(kcals=1, fat=2, protein=2)
    assert not food1.all_greater_than_or_equal_to(food2)
    assert food2.all_greater_than_or_equal_to(food1)


def test_all_greater_than_or_equal_monthly_food():
    """
    Tests if all nutrients of a food are larger than or equal those of another food
    """
    food1 = create_food_monthly()
    food2 = create_food_monthly()
    food3 = create_food_monthly(kcals=[5, 5, 5], fat=[5, 5, 5], protein=[5, 5, 5])
    assert food1.all_greater_than_or_equal_to(food2) == True
    assert food2.all_greater_than_or_equal_to(food1) == True
    assert food1.all_greater_than_or_equal_to(food3) == False
    assert food3.all_greater_than_or_equal_to(food1) == True


def test_all_greater_than_or_equal_different_unit():
    """
    Tests if all greater than or equal fail when the units are different
    """
    food1 = Food(
        kcals=1, fat=1, protein=1, kcals_units="g", fat_units="g", protein_units="g"
    )
    food2 = Food(kcals=1, fat=2, protein=2)
    with pytest.raises(AssertionError):
        assert not food1.all_greater_than_or_equal_to(food2)
        assert food2.all_greater_than_or_equal_to(food1)


def test_all_less_than_or_equal_scalar_food():
    """
    Tests if all nutrients of a food are smaller than or equal those of another food
    """
    food1 = Food(kcals=1, fat=1, protein=1)
    food2 = Food(kcals=1, fat=2, protein=2)
    assert food1.all_less_than_or_equal_to(food2)
    assert not food2.all_less_than_or_equal_to(food1)


def test_all_less_than_or_equal_monthly_food():
    """
    Tests if all nutrients of a food are smaller than or equal those of another food
    """
    food1 = create_food_monthly()
    food2 = create_food_monthly()
    food3 = create_food_monthly(kcals=[2, 2, 2], fat=[2, 2, 2], protein=[2, 2, 2])
    assert food1.all_less_than_or_equal_to(food2) == True
    assert food2.all_less_than_or_equal_to(food1) == True
    assert food1.all_less_than_or_equal_to(food3) == True
    assert food3.all_less_than_or_equal_to(food1) == False


def test_all_less_than_or_equal_different_unit():
    """
    Tests if all less than or equal fail when the units are different
    """
    food1 = Food(
        kcals=1, fat=1, protein=1, kcals_units="g", fat_units="g", protein_units="g"
    )
    food2 = Food(kcals=1, fat=2, protein=2)
    with pytest.raises(AssertionError):
        assert food1.all_less_than_or_equal_to(food2)
        assert not food2.all_less_than_or_equal_to(food1)


def test_any_greater_than_or_equal_scalar_food():
    """
    Tests if any nutrient of a food is larger than or equal those of another food
    """
    food1 = Food(kcals=1, fat=1, protein=1)
    food2 = Food(kcals=1, fat=2, protein=1)
    assert food1.any_greater_than_or_equal_to(food2)
    assert food2.any_greater_than_or_equal_to(food1)


def test_any_greater_than_or_equal_monthly_food():
    """
    Tests if any nutrient of a food is larger than or equal those of another food
    """
    food1 = create_food_monthly()
    food2 = create_food_monthly()
    food3 = create_food_monthly(kcals=[5, 5, 5], fat=[5, 5, 5], protein=[5, 5, 5])
    assert food1.any_greater_than_or_equal_to(food2) == True
    assert food2.any_greater_than_or_equal_to(food1) == True
    assert food1.any_greater_than_or_equal_to(food3) == False
    assert food3.any_greater_than_or_equal_to(food1) == True


def test_any_greater_than_or_equal_different_unit():
    """
    Tests if any greater than or equal fail when the units are different
    """
    food1 = Food(
        kcals=1, fat=1, protein=1, kcals_units="g", fat_units="g", protein_units="g"
    )
    food2 = Food(kcals=1, fat=2, protein=2)
    with pytest.raises(AssertionError):
        assert food1.any_greater_than_or_equal_to(food2)
        assert not food2.any_greater_than_or_equal_to(food1)


def test_any_less_than_or_equal_scalar_food():
    """
    Tests if any nutrient of a food is smaller than or equal those of another food
    """
    food1 = Food(kcals=1, fat=1, protein=1)
    food2 = Food(kcals=1, fat=2, protein=1)
    food3 = Food(kcals=5, fat=5, protein=5)
    assert food1.any_less_than_or_equal_to(food2)
    assert food2.any_less_than_or_equal_to(food1)
    assert not food3.any_less_than_or_equal_to(food1)


def test_any_less_than_or_equal_monthly_food():
    """
    Tests if any nutrient of a food is smaller than or equal those of another food
    """
    food1 = create_food_monthly()
    food2 = create_food_monthly()
    food3 = create_food_monthly(kcals=[5, 5, 5], fat=[5, 5, 5], protein=[5, 5, 5])
    assert food1.any_less_than_or_equal_to(food2) == True
    assert food2.any_less_than_or_equal_to(food1) == True
    assert food1.any_less_than_or_equal_to(food3) == True
    assert food3.any_less_than_or_equal_to(food1) == False


def test_any_less_than_or_equal_different_unit():
    """
    Tests if any less than or equal fail when the units are different
    """
    food1 = Food(
        kcals=1, fat=1, protein=1, kcals_units="g", fat_units="g", protein_units="g"
    )
    food2 = Food(kcals=1, fat=2, protein=2)
    with pytest.raises(AssertionError):
        assert not food1.any_less_than_or_equal_to(food2)
        assert food2.any_less_than_or_equal_to(food1)


def test_any_equals_zero_scalar_food():
    """
    Tests if a food is equal to zero
    """
    food1 = Food(kcals=1, fat=1, protein=1)
    food2 = Food(kcals=0, fat=0, protein=1)
    assert food1.any_equals_zero() == False
    assert food2.any_equals_zero() == True


def test_any_equals_zero_monthly_food():
    """
    Tests if a food is equal to zero
    """
    food1 = create_food_monthly()
    food2 = create_food_monthly(kcals=[0, 0, 0], fat=[0, 0, 0], protein=[0, 0, 1])
    assert food1.any_equals_zero() == False
    assert food2.any_equals_zero() == True


def test_all_equals_zero_scalar_food():
    """
    Tests if a food is equal to zero
    """
    food1 = Food(kcals=1, fat=1, protein=0)
    food2 = Food(kcals=0, fat=0, protein=0)
    assert not food1.all_equals_zero()
    assert food2.all_equals_zero()


def test_all_equals_zero_monthly_food():
    """
    Tests if a food is equal to zero
    """
    food1 = create_food_monthly()
    food2 = create_food_monthly(kcals=[0, 0, 0], fat=[0, 0, 0], protein=[0, 0, 0])
    assert food1.all_equals_zero() == False
    assert food2.all_equals_zero() == True


def test_all_greater_than_zero_scalar_food():
    """
    Tests if all nutrients of a food are greater than zero
    """
    food1 = Food(kcals=1, fat=1, protein=1)
    food2 = Food(kcals=0, fat=0, protein=0)
    assert food1.all_greater_than_zero()
    assert not food2.all_greater_than_zero()


def test_all_greater_than_zero_monthly_food():
    """
    Tests if all nutrients of a food are greater than zero
    """
    food1 = create_food_monthly()
    food2 = create_food_monthly(kcals=[0, 0, 0], fat=[0, 0, 0], protein=[0, 0, 0])
    assert food1.all_greater_than_zero() == True
    assert food2.all_greater_than_zero() == False


def test_any_greater_than_zero_scalar_food():
    """
    Tests if any nutrient of a food is greater than zero
    """
    food1 = Food(kcals=1, fat=0, protein=0)
    food2 = Food(kcals=0, fat=0, protein=0)
    assert food1.any_greater_than_zero()
    assert not food2.any_greater_than_zero()


def test_any_greater_than_zero_monthly_food():
    """
    Tests if any nutrient of a food is greater than zero
    """
    food1 = create_food_monthly()
    food2 = create_food_monthly(kcals=[0, 0, 0], fat=[0, 0, 0], protein=[0, 0, 0])
    food3 = create_food_monthly(kcals=[0, 1, 0], fat=[0, 0, 0], protein=[0, 0, 0])
    assert food1.any_greater_than_zero() == True
    assert food2.any_greater_than_zero() == False
    assert food3.any_greater_than_zero() == True


def test_all_greater_or_equal_zero_scalar_food():
    """
    Tests if all nutrients of a food are greater or equal to zero
    """
    food1 = Food(kcals=1, fat=0, protein=0)
    food2 = Food(kcals=0, fat=0, protein=0)
    assert food1.all_greater_than_or_equal_to_zero()
    assert food2.all_greater_than_or_equal_to_zero()


def test_all_greater_or_equal_zero_monthly_food():
    """
    Tests if all nutrients of a food are greater or equal to zero
    """
    food1 = create_food_monthly()
    food2 = create_food_monthly(kcals=[0, 0, 0], fat=[0, 0, 0], protein=[0, 0, 0])
    assert food1.all_greater_than_or_equal_to_zero() == True
    assert food2.all_greater_than_or_equal_to_zero() == True


def test_as_numpy_array():
    """
    Tests if the to_list function works
    """
    food_scalar = Food()
    assert (food_scalar.as_numpy_array() == np.array([0, 0, 0])).all()


def test_as_list_monthly():
    """
    Tests if the to_list function works
    """
    # Waiting for clarification on how to test this
    pass


def test_min_nutrient_scalar_food():
    """
    Tests if the get_min_nutrient function works
    """
    food = Food(kcals=1, fat=1, protein=0, kcals_units="thousand tons")
    assert food.get_min_nutrient() == ("protein", 0)


def test_min_nutrient_monthly_food():
    """
    Tests if the get_min_nutrient function works
    """
    food = Food(
        kcals=[1, 1, 1],
        fat=[1, 1, 1],
        protein=[0, 0, 0],
        kcals_units="thousand tons each month",
        protein_units="thousand tons each month",
        fat_units="thousand tons each month",
    )
    assert food.get_min_nutrient() == ("protein", 0)


def test_max_nutrient_scalar_food():
    """
    Tests if the get_max_nutrient function works
    """
    food = Food(kcals=1, fat=0, protein=0, kcals_units="thousand tons")
    assert food.get_max_nutrient() == ("kcals", 1)


def test_max_nutrient_monthly_food():
    """
    Tests if the get_max_nutrient function works
    This should fail, as this is only defined for scalar foods
    """
    food = Food(
        kcals=[1, 1, 1],
        fat=[1, 1, 1],
        protein=[0, 0, 0],
        kcals_units="thousand tons each month",
        protein_units="thousand tons each month",
        fat_units="thousand tons each month",
    )
    with pytest.raises(AssertionError):
        assert food.get_max_nutrient() == ("kcals", 1)


def test_get_nutrients_sum_scalar_food():
    """
    Tests if the get_nutrients_sum function works
    This should fail, as this is only defined for monthly foods
    """
    food = Food()
    with pytest.raises(AssertionError):
        assert food.get_nutrients_sum() == 3


def test_get_nutrients_sum_monthly_food():
    """
    Tests if the get_nutrients_sum function works
    """
    food = create_food_monthly()
    food = food.get_nutrients_sum()
    assert food.kcals == 4
    assert food.fat == 5
    assert food.protein == 5
    assert food.kcals_units == "kcals"
    assert food.protein_units == "kcals"
    assert food.fat_units == "kcals"


def test_get_running_total_nutrients_sum_scalar_food():
    """
    Tests if the get_running_total_nutrients_sum function works
    This should fail, as this is only defined for monthly foods
    """
    food = Food()
    with pytest.raises(AssertionError):
        assert food.get_running_total_nutrients_sum() == 3


def test_get_running_total_nutrients_sum_monthly_food():
    """
    Tests if the get_running_total_nutrients_sum function works
    """
    food = create_food_monthly(kcals=[1, 1, 1], fat=[1, 1, 1], protein=[1, 1, 1])
    food = food.get_running_total_nutrients_sum()
    assert (food.kcals == [1, 2, 3]).all()
    assert (food.fat == [1, 2, 3]).all()
    assert (food.protein == [1, 2, 3]).all()
    # make sure the units aren't changed
    assert food.kcals_units == "kcals each month"
    assert food.protein_units == "kcals each month"
    assert food.fat_units == "kcals each month"


def test_get_month_scalar_food():
    """
    Tests if the get_months function works
    This should fail, as this is only defined for monthly foods
    """
    food = Food()
    with pytest.raises(AssertionError):
        assert food.get_month(1) == 3


def test_get_month_monthly_food():
    """
    Tests if the get_months function works
    """
    food = create_food_monthly(kcals=[1, 1, 1], fat=[1, 1, 1], protein=[1, 1, 1])
    food = food.get_month(1)
    assert food.kcals == 1
    assert food.fat == 1
    assert food.protein == 1
    assert food.kcals_units == "kcals per month"
    assert food.protein_units == "kcals per month"
    assert food.fat_units == "kcals per month"


def test_get_min_all_months_scalar_food():
    """
    Tests if the get_min_all_months function works
    This should fail, as this is only defined for monthly foods
    """
    food = Food()
    with pytest.raises(AssertionError):
        assert food.get_min_all_months() == 3


def test_get_min_all_months_monthly_food():
    """
    Tests if the get_min_all_months function works
    """
    food = create_food_monthly(kcals=[1, 2, 2], fat=[1, 2, 2], protein=[1, 2, 2])
    food = food.get_min_all_months()
    assert food.kcals == 1
    assert food.fat == 1
    assert food.protein == 1
    assert food.kcals_units == "kcals"
    assert food.protein_units == "kcals"
    assert food.fat_units == "kcals"


def test_negative_values_to_zero_scalar_food():
    """
    Tests if the negative_values_to_zero function works
    """
    food = Food(kcals=-1, fat=-1, protein=-1)
    assert food.negative_values_to_zero() == Food(kcals=0, fat=0, protein=0)


def test_negative_values_to_zero_monthly_food():
    """
    Tests if the negative_values_to_zero function works for monthly foods
    """
    food = create_food_monthly(
        kcals=[-1, -1, -1], fat=[-1, -1, -1], protein=[-1, -1, -1]
    )
    food = food.negative_values_to_zero()

    assert (food.kcals == [0, 0, 0]).all()
    assert (food.fat == [0, 0, 0]).all()
    assert (food.protein == [0, 0, 0]).all()
    assert food.kcals_units == "kcals each month"
    assert food.protein_units == "kcals each month"
    assert food.fat_units == "kcals each month"


def test_abs_values():
    """
    Tests if the abs_values method produces a Food object with absolute values of all nutrients.
    """
    food = create_food_monthly(
        kcals=[-10, 20, -30], fat=[-5, -15, 25], protein=[-1, 2, -3]
    )

    # Get the Food object with absolute values using abs_values method
    abs_food = food.abs_values()

    # Check the values of the resulting Food object
    assert np.array_equal(
        abs_food.kcals, [10, 20, 30]
    ), "Absolute kcals not as expected"
    assert np.array_equal(abs_food.fat, [5, 15, 25]), "Absolute fat not as expected"
    assert np.array_equal(
        abs_food.protein, [1, 2, 3]
    ), "Absolute protein not as expected"

    # Check the units of the resulting Food object
    assert abs_food.kcals_units == "kcals each month", "Kcals units mismatch"
    assert abs_food.fat_units == "kcals each month", "Fat units mismatch"
    assert abs_food.protein_units == "kcals each month", "Protein units mismatch"


def test_shift():
    """
    Tests if the shift method works as expected
    """
    # Create a sample Food object
    food = create_food_monthly(
        kcals=[100, 200, 300], fat=[50, 100, 150], protein=[10, 20, 30]
    )

    # Shift by 1 month
    shifted_food = food.shift(1)

    # Expected shifted values
    expected_kcals = [0, 100, 200]
    expected_fat = [0, 50, 100]
    expected_protein = [0, 10, 20]

    # Check the shifted values
    assert np.array_equal(
        shifted_food.kcals, expected_kcals
    ), "Shifted kcals not as expected"
    assert np.array_equal(shifted_food.fat, expected_fat), "Shifted fat not as expected"
    assert np.array_equal(
        shifted_food.protein, expected_protein
    ), "Shifted protein not as expected"

    # Check the units of the shifted Food object
    assert (
        shifted_food.kcals_units == "kcals each month"
    ), "Kcals units mismatch after shifting"
    assert (
        shifted_food.fat_units == "kcals each month"
    ), "Fat units mismatch after shifting"
    assert (
        shifted_food.protein_units == "kcals each month"
    ), "Protein units mismatch after shifting"
