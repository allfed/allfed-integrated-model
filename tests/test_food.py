"""
Test Suite for the food module.
"""
import pytest
from src.food_system.food import Food

def create_food_monthly(kcals=[1,2,1], fat=[1,2,2], protein=[1,2,2]):
    """
    creates a food instance that has monthly values and returns it
    """
    food_monthly = Food(kcals=kcals, fat=fat, protein=protein, kcals_units="kcals each months", fat_units="kcals each months", protein_units="kcals each months")
    return food_monthly


def test_food_init():
    """
    Tests if a instance of the Food class can be created
    """
    assert Food() is not None
    food = Food()
    assert isinstance(food, Food)


def test_validate_if_list_failed():
    """
    Tests if a list cannot be created if it is set up wrong
    """
    with pytest.raises(AssertionError):
        Food(kcals=[1,2,3], fat=[1,2,3], protein=[1,2,3], 
            kcals_units="kcals", fat_units="kcals each months", 
            protein_units="kcals each months")


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
    assert food3.kcals == [2,4,2]
    assert food3.fat == [2,4,4]
    assert food3.protein == [2,4,4]
    assert food3.kcals_units == "kcals each months"
    assert food3.fat_units == "kcals each months"
    assert food3.protein_units == "kcals each months"


def test_failed_addition():
    """
    Tests if two foods with different units create an assertion
    error when added
    """
    food1 = Food(kcals=1, fat=1, protein=1)
    food2 = Food(kcals=1, fat=1, protein=1, kcals_units="g", fat_units="g", protein_units="g")
    with pytest.raises(AssertionError):
        food3 = food1 + food2


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
    assert food3.kcals == [0,0,0]
    assert food3.fat == [0,0,0]
    assert food3.protein == [0,0,0]
    assert food3.kcals_units == "kcals each months"
    assert food3.fat_units == "kcals each months"
    assert food3.protein_units == "kcals each months"


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


def test_multiplication_by_scalar_food():
    """
    Tests if an instance of the Food class can be multiplied by another instance of the Food class
    """
    food1 = Food(kcals=1, fat=1, protein=1)
    food2 = Food(kcals=1, fat=1, protein=1)
    food3 = food1 * food2
    assert food3.kcals == 1
    assert food3.fat == 1
    assert food3.protein == 1


def test_multiplication_monthly_food_by_scalar_food():
    """
    Tests if an instance of the Food class can be multiplied by another instance of the Food class
    """
    food1 = create_food_monthly()
    food2 = Food(kcals=1, fat=1, protein=1)
    food3 = food1 * food2
    assert food3.kcals == [1,2,1]
    assert food3.fat == [1,2,2]
    assert food3.protein == [1,2,2]
    assert food3.kcals_units == "kcals each months"
    assert food3.fat_units == "kcals each months"
    assert food3.protein_units == "kcals each months"


def test_multiplication_monthly_food():
    """
    Tests if an instance of the Food class can be multiplied by another instance of the Food class
    """
    food1 = create_food_monthly()
    food2 = create_food_monthly()
    food3 = food1 * food2
    assert food3.kcals == [1,2,2]
    assert food3.fat == [1,2,4]
    assert food3.protein == [1,2,4]
    assert food3.kcals_units == "kcals each months"
    assert food3.fat_units == "kcals each months"
    assert food3.protein_units == "kcals each months"


def test_failed_multiplication_by_food():
    """
    Multiplies two food sources with different units
    """
    food1 = Food(kcals=1, fat=1, protein=1)
    food2 = Food(kcals=1, fat=1, protein=1, kcals_units="g", fat_units="g", protein_units="g")
    with pytest.raises(AssertionError):
        food3 = food1 * food2


def test_foods_equal():
    """
    Tests if two foods are equal
    """
    food1 = Food(kcals=1, fat=1, protein=1)
    food2 = Food(kcals=1, fat=1, protein=1)
    assert food1 == food2
    assert create_food_monthly() == create_food_monthly()


def test_foods_not_equal():
    """
    Tests if two foods are not equal
    """
    food1 = Food(kcals=1, fat=1, protein=1)
    food2 = Food(kcals=2, fat=2, protein=2)
    assert food1 != food2
    assert create_food_monthly() != create_food_monthly(kcals=[1,2,3])


def test_food_failed_equal():
    """
    Tests if comparing two foods with different units fails
    """
    food1 = Food(kcals=1, fat=1, protein=1)
    food2 = Food(kcals=1, fat=1, protein=1, kcals_units="g", fat_units="g", protein_units="g")
    with pytest.raises(AssertionError):
        assert food1 == food2


def test_food_failed_not_equal():
    """
    Tests if comparing two foods with different units fails
    """
    food1 = Food(kcals=1, fat=1, protein=1)
    food2 = Food(kcals=1, fat=1, protein=1, kcals_units="g", fat_units="g", protein_units="g")
    with pytest.raises(AssertionError):
        assert food1 != food2


def test_food_string_representation():
    """
    Tests if the string representation of a food is correct
    """
    food1 = Food()
    assert str(food1) == '    kcals: 0 billion kcals\n    fat: 0  thousand tons\n    protein: 0  thousand tons'


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
    assert food2.kcals == [-1,-2,-1]
    assert food2.fat == [-1,-2,-2]
    assert food2.protein == [-1,-2,-2]
    assert food2.kcals_units == "kcals each months"
    assert food2.fat_units == "kcals each months"
    assert food2.protein_units == "kcals each months"


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
    assert food1.is_list_monthly() == False
    assert create_food_monthly().is_list_monthly() == True


def test_is_never_negative_scalar_food():
    """
    Tests if the is_never_negative method returns the expected result
    """
    food1 = Food(kcals=1, fat=1, protein=1)
    assert food1.is_never_negative() == True


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
    food1 = Food(kcals=-11, fat=1, protein=1, kcals_units="g", fat_units="g", protein_units="g")
    assert food1.is_never_negative() == False


def test_all_greater_than_scalar_food():
    """
    Tests if all nutrients of a food are larger than those of another food
    """
    food1 = Food(kcals=1, fat=1, protein=1)
    food2 = Food(kcals=2, fat=2, protein=2)
    assert food1.all_greater_than(food2) == False
    assert food2.all_greater_than(food1) == True


def test_all_greater_than_monthly_food():
    """
    Tests if all nutrients of a food are larger than those of another food
    """
    food1 = create_food_monthly()
    food2 = create_food_monthly()
    food3 = create_food_monthly(kcals=[5,5,5], fat=[5,5,5], protein=[5,5,5])
    assert food1.all_greater_than(food2) == False
    assert food2.all_greater_than(food1) == False
    assert food1.all_greater_than(food3) == False
    assert food3.all_greater_than(food1) == False


def test_all_greater_than_different_unit():
    """
    Tests if greater than fail when the units are different
    """
    food1 = Food(kcals=1, fat=1, protein=1, kcals_units="g", fat_units="g", protein_units="g")
    food2 = Food(kcals=2, fat=2, protein=2)
    with pytest.raises(AssertionError):
        assert food1.all_greater_than(food2) == False
        assert food2.all_greater_than(food1) == True


def test_all_less_than_scalar_food():
    """
    Tests if all nutrients of a food are smaller than those of another food
    """
    food1 = Food(kcals=1, fat=1, protein=1)
    food2 = Food(kcals=2, fat=2, protein=2)
    assert food1.all_less_than(food2) == True
    assert food2.all_less_than(food1) == False


def test_all_less_than_monthly_food():
    """
    Tests if all nutrients of a food are smaller than those of another food
    """
    food1 = create_food_monthly()
    food2 = create_food_monthly()
    food3 = create_food_monthly(kcals=[5,5,5], fat=[5,5,5], protein=[5,5,5])
    assert food1.all_less_than(food2) == False
    assert food2.all_less_than(food1) == False
    assert food1.all_less_than(food3) == True
    assert food3.all_less_than(food1) == False


def test_all_less_than_different_unit():
    """
    Tests if less than fail when the units are different
    """
    food1 = Food(kcals=1, fat=1, protein=1, kcals_units="g", fat_units="g", protein_units="g")
    food2 = Food(kcals=2, fat=2, protein=2)
    with pytest.raises(AssertionError):
        assert food1.all_less_than(food2) == True
        assert food2.all_less_than(food1) == False


def test_any_greater_than_scalar_food():
    """
    Tests if any nutrient of a food is larger than those of another food
    """
    food1 = Food(kcals=1, fat=1, protein=1)
    food2 = Food(kcals=2, fat=1, protein=1)
    assert food1.any_greater_than(food2) == False
    assert food2.any_greater_than(food1) == True


def test_any_greater_than_monthly_food():
    """
    Tests if any nutrient of a food is larger than those of another food
    """
    food1 = create_food_monthly()
    food2 = create_food_monthly()
    food3 = create_food_monthly(kcals=[5,5,5], fat=[5,5,5], protein=[5,5,5])
    assert food1.any_greater_than(food2) == True
    assert food2.any_greater_than(food1) == True
    assert food1.any_greater_than(food3) == False
    assert food3.any_greater_than(food1) == True


def test_any_greater_than_different_unit():
    """
    Tests if any greater than fail when the units are different
    """
    food1 = Food(kcals=1, fat=1, protein=1, kcals_units="g", fat_units="g", protein_units="g")
    food2 = Food(kcals=2, fat=1, protein=1)
    with pytest.raises(AssertionError):
        assert food1.any_greater_than(food2) == False
        assert food2.any_greater_than(food1) == True


def test_any_less_than_scalar_food():
    """
    Tests if any nutrient of a food is smaller than those of another food
    """
    food1 = Food(kcals=1, fat=1, protein=1)
    food2 = Food(kcals=2, fat=1, protein=1)
    assert food1.any_less_than(food2) == True
    assert food2.any_less_than(food1) == False


def test_any_less_than_monthly_food():
    """
    Tests if any nutrient of a food is smaller than those of another food
    """
    food1 = create_food_monthly()
    food2 = create_food_monthly()
    food3 = create_food_monthly(kcals=[5,5,5], fat=[5,5,5], protein=[5,5,5])
    assert food1.any_less_than(food2) == True
    assert food2.any_less_than(food1) == True
    assert food1.any_less_than(food3) == True
    assert food3.any_less_than(food1) == False


def test_any_less_than_different_unit():
    """
    Tests if any less than fail when the units are different
    """
    food1 = Food(kcals=1, fat=1, protein=1, kcals_units="g", fat_units="g", protein_units="g")
    food2 = Food(kcals=2, fat=1, protein=1)
    with pytest.raises(AssertionError):
        assert food1.any_less_than(food2) == True
        assert food2.any_less_than(food1) == False


def test_all_greater_than_or_equal_scalar_food():
    """
    Tests if all nutrients of a food are larger than or equal those of another food
    """
    food1 = Food(kcals=1, fat=1, protein=1)
    food2 = Food(kcals=1, fat=2, protein=2)
    assert food1.all_greater_than_or_equal(food2) == False
    assert food2.all_greater_than_or_equal(food1) == True


def test_all_greater_than_or_equal_monthly_food():
    """
    Tests if all nutrients of a food are larger than or equal those of another food
    """
    food1 = create_food_monthly()
    food2 = create_food_monthly()
    food3 = create_food_monthly(kcals=[5,5,5], fat=[5,5,5], protein=[5,5,5])
    assert food1.all_greater_than_or_equal(food2) == False
    assert food2.all_greater_than_or_equal(food1) == False
    assert food1.all_greater_than_or_equal(food3) == False
    assert food3.all_greater_than_or_equal(food1) == True


def test_all_greater_than_or_equal_different_unit():
    """
    Tests if all greater than or equal fail when the units are different
    """
    food1 = Food(kcals=1, fat=1, protein=1, kcals_units="g", fat_units="g", protein_units="g")
    food2 = Food(kcals=1, fat=2, protein=2)
    with pytest.raises(AssertionError):
        assert food1.all_greater_than_or_equal(food2) == False
        assert food2.all_greater_than_or_equal(food1) == True


def test_all_less_than_or_equal_scalar_food():
    """
    Tests if all nutrients of a food are smaller than or equal those of another food
    """
    food1 = Food(kcals=1, fat=1, protein=1)
    food2 = Food(kcals=1, fat=2, protein=2)
    assert food1.all_less_than_or_equal(food2) == True
    assert food2.all_less_than_or_equal(food1) == False


def test_all_less_than_or_equal_monthly_food():
    """
    Tests if all nutrients of a food are smaller than or equal those of another food
    """
    food1 = create_food_monthly()
    food2 = create_food_monthly()
    food3 = create_food_monthly(kcals=[2,2,2], fat=[2,2,2], protein=[2,2,2])
    assert food1.all_less_than_or_equal(food2) == False
    assert food2.all_less_than_or_equal(food1) == False
    assert food1.all_less_than_or_equal(food3) == True
    assert food3.all_less_than_or_equal(food1) == False


def test_all_less_than_or_equal_different_unit():
    """
    Tests if all less than or equal fail when the units are different
    """
    food1 = Food(kcals=1, fat=1, protein=1, kcals_units="g", fat_units="g", protein_units="g")
    food2 = Food(kcals=1, fat=2, protein=2)
    with pytest.raises(AssertionError):
        assert food1.all_less_than_or_equal(food2) == True
        assert food2.all_less_than_or_equal(food1) == False


def test_any_greater_than_or_equal_scalar_food():
    """
    Tests if any nutrient of a food is larger than or equal those of another food
    """
    food1 = Food(kcals=1, fat=1, protein=1)
    food2 = Food(kcals=1, fat=2, protein=1)
    assert food1.any_greater_than_or_equal(food2) == True
    assert food2.any_greater_than_or_equal(food1) == True


def test_any_greater_than_or_equal_monthly_food():
    """
    Tests if any nutrient of a food is larger than or equal those of another food
    """
    food1 = create_food_monthly()
    food2 = create_food_monthly()
    food3 = create_food_monthly(kcals=[5,5,5], fat=[5,5,5], protein=[5,5,5])
    assert food1.any_greater_than_or_equal(food2) == True
    assert food2.any_greater_than_or_equal(food1) == True
    assert food1.any_greater_than_or_equal(food3) == False
    assert food3.any_greater_than_or_equal(food1) == True


def test_any_greater_than_or_equal_different_unit():
    """
    Tests if any greater than or equal fail when the units are different
    """
    food1 = Food(kcals=1, fat=1, protein=1, kcals_units="g", fat_units="g", protein_units="g")
    food2 = Food(kcals=1, fat=2, protein=2)
    with pytest.raises(AssertionError):
        assert food1.any_greater_than_or_equal(food2) == True
        assert food2.any_greater_than_or_equal(food1) == False


def test_any_less_than_or_equal_scalar_food():
    """
    Tests if any nutrient of a food is smaller than or equal those of another food
    """
    food1 = Food(kcals=1, fat=1, protein=1)
    food2 = Food(kcals=1, fat=2, protein=1)
    food3 = Food(kcals=5, fat=5, protein=5)
    assert food1.any_less_than_or_equal(food2) == True
    assert food2.any_less_than_or_equal(food1) == True
    assert food3.any_less_than_or_equal(food1) == False


def test_any_less_than_or_equal_monthly_food():
    """
    Tests if any nutrient of a food is smaller than or equal those of another food
    """
    food1 = create_food_monthly()
    food2 = create_food_monthly()
    food3 = create_food_monthly(kcals=[5,5,5], fat=[5,5,5], protein=[5,5,5])
    assert food1.any_less_than_or_equal(food2) == True
    assert food2.any_less_than_or_equal(food1) == True
    assert food1.any_less_than_or_equal(food3) == True
    assert food3.any_less_than_or_equal(food1) == False


def test_any_less_than_or_equal_different_unit():
    """
    Tests if any less than or equal fail when the units are different
    """
    food1 = Food(kcals=1, fat=1, protein=1, kcals_units="g", fat_units="g", protein_units="g")
    food2 = Food(kcals=1, fat=2, protein=2)
    with pytest.raises(AssertionError):
        assert food1.any_less_than_or_equal(food2) == False
        assert food2.any_less_than_or_equal(food1) == True


def test_equals_zero_scalar_food():
    """
    Tests if a food is equal to zero
    """
    food1 = Food(kcals=1, fat=1, protein=1)
    food2 = Food(kcals=0, fat=0, protein=0)
    assert food1.equals_zero() == False
    assert food2.equals_zero() == True


def test_equals_zero_monthly_food():
    """
    Tests if a food is equal to zero
    """
    food1 = create_food_monthly()
    food2 = create_food_monthly(kcals=[0,0,0], fat=[0,0,0], protein=[0,0,0])
    assert food1.equals_zero() == False
    assert food2.equals_zero() == True


def test_all_greater_than_zero_scalar_food():
    """
    Tests if all nutrients of a food are greater than zero
    """
    food1 = Food(kcals=1, fat=1, protein=1)
    food2 = Food(kcals=0, fat=0, protein=0)
    assert food1.all_greater_than_zero() == True
    assert food2.all_greater_than_zero() == False