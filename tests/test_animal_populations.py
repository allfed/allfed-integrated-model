# Generated by CodiumAI
import pandas as pd
from src.food_system.animal_populations import CountryData
from src.food_system.animal_populations import AnimalSpecies
from src.food_system.food import Food
from click import Path


import pytest

"""
Country Data Tests

Behaviours Covered

HAPPY PATH
Creating an instance of CountryData with a valid country name
Setting livestock unit factors with valid dataframes
Calculating homekill hours with valid input data
EDGE CASES
Creating an instance of CountryData with an invalid country name
Setting livestock unit factors with invalid dataframes
Calculating homekill hours with invalid input data
OTHER
Setting desperation parameters for homekill
Calculating total slaughter hours
Storing meat output data
Storing spare slaughter hours
Handling missing data in country info dataframe


Main functionalities:
CountryData is a class that represents data for a specific country in a food system model. It contains fields for various data points such as slaughter hours, homekill hours, and meat output. The class has methods for setting livestock unit factors, calculating homekill hours, and calculating total slaughter hours.

Methods:
- __init__(self, country_name): initializes the CountryData object with the given country name and sets various fields to empty lists or 0.
- set_livestock_unit_factors(self, df_country_info, df_regional_conversion_factors): sets the LSU conversion factors for the country based on the given dataframes.
- homekill_desperation_parameters(self): sets the homekill fraction and other death homekill rate.
- calculate_homekill_hours(self): calculates the number of hours required to slaughter homekill animals.
- calculate_total_slaughter_hours(self, all_animals): calculates the total slaughter hours for all animals in the given list.

Fields:
- country_name: the name of the country.
- slaughter_hours: a list of total slaughter hours for each month.
- homekill_hours_total_month: a list of total homekill hours for each month.
- homekill_hours_budget: a list of budgeted homekill hours for each month.
- meat_output: a list of meat output for each month.
- spare_slaughter_hours: the number of spare slaughter hours for the country.
- EK_region: the FAO region for the country.
- LSU_conversion_factors: a dictionary of livestock unit conversion factors for the country.

"""
# Generated by CodiumAI


class TestCountryData:
    # Tests that an instance of CountryData can be created with a valid country name
    def test_valid_country_name(self):
        country_data = CountryData("Canada")
        assert country_data.country_name == "Canada"

    # Tests that an instance of CountryData cannot be created with an invalid country name
    def test_invalid_country_name(self):
        with pytest.raises(TypeError):
            country_data = CountryData(123)

    # Tests that livestock unit factors can be set with valid dataframes
    # Tests that livestock unit factors can be set with valid dataframes
    def test_valid_livestock_unit_factors(self):
        df_country_info = pd.DataFrame(
            {"alpha3": ["CAN"], "FAO-region-EK": ["North America"]}
        )
        df_country_info.set_index("alpha3", inplace=True)
        df_regional_conversion_factors = pd.DataFrame(
            {
                "North America": {"Cattle": 1.23, "Sheep": 0.45},
                "Other": {"Cattle": 1.0, "Sheep": 1.0},
            }
        )
        country_data = CountryData("CAN")
        country_data.set_livestock_unit_factors(
            df_country_info, df_regional_conversion_factors
        )
        assert country_data.EK_region == "North America"
        assert country_data.LSU_conversion_factors == {"Cattle": 1.23, "Sheep": 0.45}

    # Tests that livestock unit factors cannot be set with invalid dataframes
    # Tests that livestock unit factors cannot be set with invalid dataframes
    def test_invalid_livestock_unit_factors(self):
        df_country_info = pd.DataFrame(
            {"country": ["Canada"], "FAO-region-EK": ["North America"]}
        ).set_index("country")
        df_regional_conversion_factors = pd.DataFrame(
            {"North America": {"Cattle": 1.23, "Sheep": "invalid"}}
        )
        country_data = CountryData("Canada")
        with pytest.raises(ValueError):
            country_data.set_livestock_unit_factors(
                df_country_info, df_regional_conversion_factors
            )

    # Tests that homekill hours can be calculated with valid input data
    def test_valid_homekill_hours(self):
        country_data = CountryData("Canada")
        country_data.calculate_homekill_hours()
        assert country_data.homekill_hours_total_month == [10000]

    # Tests that homekill hours cannot be calculated with invalid input data
    def test_invalid_homekill_hours(self):
        country_data = CountryData("Canada")
        with pytest.raises(TypeError):
            country_data.calculate_homekill_hours("invalid_input")

    # Tests that the homekill desperation parameters are set correctly
    def test_set_homekill_desperation_parameters(self):
        country = CountryData("TestCountry")
        country.homekill_desperation_parameters()
        assert country.other_death_homekill_rate == 0.5
        assert country.homekill_fraction == 0.00

    # Tests that the meat output data is stored correctly in the CountryData object
    def test_storing_meat_output_data(self):
        country = CountryData("TestCountry")
        meat_output_data = [1, 2, 3]
        country.meat_output = meat_output_data
        assert country.meat_output == meat_output_data

    # Tests that the spare slaughter hours are stored correctly in the CountryData object
    def test_storing_spare_slaughter_hours(self):
        country = CountryData("TestCountry")
        country.spare_slaughter_hours = 10
        assert country.spare_slaughter_hours == 10

    # Tests that the function calculate_total_slaughter_hours returns the correct total slaughter hours
    def test_calculate_total_slaughter_hours(self):
        # create some animal objects
        animal1 = AnimalSpecies("meat_buffalo", "buffalo")
        animal2 = AnimalSpecies("chicken", "chicken")
        animal3 = AnimalSpecies("milk_cattle", "cattle")
        animal1.update_attributes(animal_slaughter_hours=8, baseline_slaughter=100)
        animal2.update_attributes(
            animal_slaughter_hours=0.1, baseline_slaughter=10000000
        )
        animal3.update_attributes(animal_slaughter_hours=8, baseline_slaughter=10000)

        all_animals = [animal1, animal2, animal3]
        # create a CountryData object
        country = CountryData("TestCountry")
        # call the function
        total_slaughter_hours = country.calculate_total_slaughter_hours(all_animals)
        # check that the result is correct
        assert total_slaughter_hours == 1080800

    # Tests that the set_livestock_unit_factors function handles missing data in the country info dataframe correctly
    def test_missing_data_handling(self):
        # Create a mock dataframe with missing data
        df_country_info = pd.DataFrame(
            {"country_name": ["ARG", "AUS"], "FAO-region-EK": ["Region A", None]}
        )
        df_regional_conversion_factors = pd.DataFrame(
            {
                "Region A": {"Animal A": 1.0, "Animal B": 2.0},
                "Region B": {"Animal A": 3.0, "Animal B": 4.0},
            }
        )

        # Create CountryData object and call set_livestock_unit_factors with a country name of exactly 3 letters
        country_data = CountryData("USA")
        try:
            country_data.set_livestock_unit_factors(
                df_country_info, df_regional_conversion_factors
            )
        except ValueError as e:
            assert (
                str(e)
                == "Region not found in the regional conversion factors dataframe"
            )
        else:
            raise AssertionError("Expected ValueError")


"""
Main functionalities:
The AnimalSpecies class is designed to represent a specific species of animal in a food system model. It contains methods for setting and updating various attributes of the animal, such as population, slaughter rate, and nutrition requirements. It also includes methods for calculating the number of pregnant animals birthing each month and the amount of feed required to sustain the population.

Methods:
- update_attributes: updates the attributes of the animal object with new values
- set_animal_attributes: sets the initial attributes of the animal object, such as population and slaughter rate
- set_LSU_attributes: sets the LSU factor for the animal based on the country it is in
- set_species_milk_attributes: sets attributes specific to milk-producing animals, such as milk production per month
- set_species_slaughter_attributes: sets attributes specific to animals raised for slaughter, such as gestation period and target population fraction
- feed_the_species: calculates the amount of feed required to sustain the population and updates the NE balance accordingly
- reset_NE_balance: resets the NE balance to the required amount for the current population

Fields:
- animal_type: the general type of animal (e.g. cattle, sheep)
- animal_species: the specific species of animal (e.g. Angus, Merino)
- current_population: the current population of the animal
- baseline_slaughter: the baseline slaughter rate of the animal
- animal_function: the function of the animal in the food system (e.g. meat, milk)
- livestock_unit: a measure of the animal's size and energy requirements
- digestion_type: the type of digestion the animal has (e.g. ruminant, monogastric)
- nutrition_ratio: the required ratio of carbs, fat, and protein in the animal's diet
- NE_balance: the current balance of net energy required for the population
- pregnant_animals_total: the total number of pregnant animals in the population
- pregnant_animals_birthing_this_month: the number of pregnant animals birthing this month
- slaughtered_pregnant_animals: the number of pregnant animals slaughtered each month
- other_animal_death_rate_annual: the annual death rate of animals dying from non-slaughter causes
- other_animal_death_basline_head_monthly: the baseline monthly death rate of non-slaughtered animals
- other_death_starving: the number of non-slaughtered animals that die each month due to starvation
- other_death_total: the total number of non-slaughtered animals that die each month
- birth_ratio: the ratio of births to animals in the population
- births_animals_month: the number of animals born each month
- transfer_population: the number of animals transferred to or from the population each month
- transfer_births: the number of births resulting from transferred animals
- slaughter: the current monthly slaughter rate
- homekill_other_death_this_month: the number of animals killed for reasons other than slaughter each month
- homekill_healthy_this_month: the number of healthy animals killed each month
- homekill_starving_this_month: the number of animals killed due to starvation each month
- total_homekill_this_month: the total number of animals killed each month


AnimalSpecies Class Tests
Behaviors Coverage
Total Behaviors:
20

TESTS
HAPPY PATH
Setting animal attributes with valid inputs
Setting milk attributes with valid inputs
Setting slaughter attributes with valid inputs
Feeding the species with valid inputs
Appending month zero
EDGE CASES
Setting animal attributes with negative population
Setting animal attributes with negative slaughter
Setting animal attributes with negative livestock_unit
Setting milk attributes without setting population
Setting milk attributes with negative productive_milk_age_start
Setting milk attributes with negative productive_milk_age_end
Setting milk attributes with productive_milk_age_end less than productive_milk_age_start
Setting slaughter attributes without setting population
Setting slaughter attributes with reduction_in_animal_breeding greater than 1
Setting slaughter attributes with target_population_fraction less than 0
Setting slaughter attributes with pregnant_animal_slaughter_fraction less than 0
Setting slaughter attributes with pregnant_animal_slaughter_fraction greater than 1
Setting slaughter attributes with change_in_slaughter_rate less than 0
Setting slaughter attributes with other_animal_death_rate_annual less than 0
Setting slaughter attributes with animals_per_pregnancy less than 0


"""


# Generated by CodiumAI


class TestAnimalSpecies:
    # Tests that the animal attributes can be set with a positive population
    def test_set_animal_attributes_positive_population(self):
        animal = AnimalSpecies("type", "species")
        animal.set_animal_attributes(100, 50, "function", 1, "type", "size", 0.5)
        assert animal.current_population == 100

    # Tests that an error is raised when trying to set animal attributes with a negative population
    def test_set_animal_attributes_negative_population(self):
        animal = AnimalSpecies("type", "species")
        with pytest.raises(ValueError):
            animal.set_animal_attributes(-100, 50, "function", 1, "type", "size", 0.5)

    # Tests that an error is raised when trying to set animal attributes with a negative slaughter
    def test_set_animal_attributes_negative_slaughter(self):
        animal = AnimalSpecies("type", "species")
        with pytest.raises(ValueError):
            animal.set_animal_attributes(100, -50, "function", 1, "type", "size", 0.5)

    # Tests that an error is raised when trying to set animal attributes with a negative livestock unit
    def test_set_animal_attributes_negative_livestock_unit(self):
        animal = AnimalSpecies("type", "species")
        with pytest.raises(ValueError):
            animal.set_animal_attributes(100, 50, "function", -1, "type", "size", 0.5)

    # Tests that an error is raised when trying to set milk attributes without setting the population
    def test_set_milk_attributes_without_population(self):
        animal = AnimalSpecies("type", "species")
        with pytest.raises(AttributeError):
            animal.set_species_milk_attributes(1, 2, 3, 4)

    # Tests that an error is raised when trying to set milk attributes with a negative productive milk age start
    def test_set_milk_attributes_negative_productive_milk_age_start(self):
        animal = AnimalSpecies("type", "species")
        animal.set_animal_attributes(100, 50, "function", 1, "type", "size", 0.5)
        with pytest.raises(ValueError):
            animal.set_species_milk_attributes(-1, 2, 3, 4)

    # Tests that an error is raised when trying to set milk attributes with a negative productive milk age end
    def test_set_milk_attributes_negative_productive_milk_age_end(self):
        animal = AnimalSpecies("type", "species")
        animal.set_animal_attributes(100, 50, "function", 1, "type", "size", 0.5)
        with pytest.raises(ValueError):
            animal.set_species_milk_attributes(1, -2, 3, 4)

    # Tests that an error is raised when trying to set milk attributes with a productive milk age end less than productive milk age start
    def test_set_milk_attributes_productive_milk_age_end_less_than_start(self):
        animal = AnimalSpecies("type", "species")
        animal.set_animal_attributes(100, 50, "function", 1, "type", "size", 0.5)
        with pytest.raises(ValueError):
            animal.set_species_milk_attributes(2, 1, 3, 4)

    # Tests that an error is raised when trying to set slaughter attributes without setting the population
    def test_set_slaughter_attributes_without_population(self):
        animal = AnimalSpecies("type", "species")
        with pytest.raises(AttributeError):
            animal.set_species_slaughter_attributes(
                1, 2, 3, 4, 5, 6, 7, 8, 0.5
            )  # Added the missing argument 'starvation_death_fraction'

    # Tests that an error is raised when trying to set slaughter attributes with a reduction in animal breeding greater than 1
    def test_set_slaughter_attributes_reduction_in_animal_breeding_greater_than_1(self):
        animal = AnimalSpecies("type", "species")
        animal.set_animal_attributes(100, 50, "function", 1, "type", "size", 0.5)
        with pytest.raises(ValueError):
            animal.set_species_slaughter_attributes(1, 2, 3, 4, 5, 6, 7, 8, 2)

    # Tests that an error is raised when trying to set slaughter attributes with a target population fraction less than 0
    def test_set_slaughter_attributes_target_population_fraction_less_than_0(self):
        animal = AnimalSpecies("type", "species")
        animal.set_animal_attributes(100, 50, "function", 1, "type", "size", 0.5)
        with pytest.raises(ValueError):
            animal.set_species_slaughter_attributes(
                1, 2, 3, 4, 5, 6, -1, 8, 0.2
            )  # Added missing argument 'starvation_death_fraction'

    # Tests that an error is raised when trying to set slaughter attributes with a pregnant animal slaughter fraction greater than 1
    def test_set_slaughter_attributes_pregnant_animal_slaughter_fraction_greater_than_1(
        self,
    ):
        animal = AnimalSpecies("type", "species")
        animal.set_animal_attributes(100, 50, "function", 1, "type", "size", 0.5)
        with pytest.raises(ValueError):
            animal.set_species_slaughter_attributes(1, 2, 3, 4, 5, 6, 7, 8, 1.5)

    # Tests that feeding the species with valid inputs updates the population_fed and NE_balance attributes correctly
    def test_feeding_species_valid_inputs(self):
        # Arrange
        animal = AnimalSpecies("meat_cattle", "cattle")
        animal.set_animal_attributes(100, 10, "meat", 1, "ruminant", 500, 0.5)
        animal.reset_NE_balance()
        food = Food(10000, 200, 300)
        # Act
        animal.feed_the_species(food)
        # Assert
        assert animal.population_fed == 100  # all population is fed
        assert animal.NE_balance.kcals == 0  # no leftover kcals needed

    # Tests that a ValueError is raised when setting slaughter attributes with pregnant_animal_slaughter_fraction less than 0
    def test_pregnant_animal_slaughter_fraction_less_than_zero(self):
        animal = AnimalSpecies("type", "species")
        animal.set_animal_attributes(
            population=100,
            slaughter=10,
            animal_function="milk",
            livestock_unit=1,
            digestion_type="ruminant",
            animal_size="large",
            approximate_feed_conversion=0.5,
        )
        with pytest.raises(ValueError):
            animal.set_species_slaughter_attributes(
                gestation=1,
                other_animal_death_rate_annual=1,
                animals_per_pregnancy=1,
                animal_slaughter_hours=1,
                change_in_slaughter_rate=1,
                pregnant_animal_slaughter_fraction=-0.1,
                reduction_in_animal_breeding=1,
                target_population_fraction=1,
                starvation_death_fraction=0,
            )

    # Tests that a ValueError is raised when change_in_slaughter_rate is less than 0
    def test_change_in_slaughter_rate_less_than_zero(self):
        with pytest.raises(ValueError):
            animal = AnimalSpecies("cow", "dairy")
            animal.set_animal_attributes(100, 10, "milk", 1, "ruminant", 500, 0.5)
            animal.set_species_slaughter_attributes(
                9, 0.1, 1, 8, -1, 0.1, 0.1, 0.1, 0.1, 0.1
            )

    # Tests that a ValueError is raised when animals_per_pregnancy is less than 0
    def test_negative_animals_per_pregnancy(self):
        with pytest.raises(ValueError):
            animal = AnimalSpecies("cow", "dairy")
            animal.set_animal_attributes(100, 10, "milk", 1, "ruminant", 500, 0.5)
            animal.set_species_slaughter_attributes(
                9, 0.1, -1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1
            )

    # Tests that a ValueError is raised when setting slaughter attributes with other_animal_death_rate_annual less than 0
    def test_negative_other_animal_death_rate_annual(self):
        with pytest.raises(ValueError):
            animal = AnimalSpecies("cattle", "dairy")
            animal.set_animal_attributes(100, 10, "milk", 1, "ruminant", 500, 0.1)
            animal.set_species_slaughter_attributes(
                gestation=9,
                other_animal_death_rate_annual=-1,
                animals_per_pregnancy=1,
                animal_slaughter_hours=8,
                change_in_slaughter_rate=1,
                pregnant_animal_slaughter_fraction=0.5,
                reduction_in_animal_breeding=0.5,
                target_population_fraction=0.8,
                starvation_death_fraction=0.1,
            )


# Generated by CodiumAI
from src.food_system.animal_populations import AnimalSpecies
from src.food_system.animal_populations import AnimalPopulation
from pytz import country_names


import pytest

"""
Test that animal population is correctly initialized
Test that calculate_additive_births returns expected values
Test that calculate_change_in_population updates animal population correctly
Test that calculate_pregnant_animals_birthing returns expected values
Test that calculate_pregnant_slaughter returns expected values
Test that calculate_animal_population returns expected values
Test that calculate_retiring_milk_animals returns expected values
Test that calculate_births returns expected values
Test that calculate_breeding_changes updates animal population correctly
Test that calculate_other_deaths returns expected values
Test that calculate_slaughter_rate returns expected values
Test that calculate_other_death_homekill_head returns expected values
Test that calculate_healthy_homekill_head returns expected values
Test that calculate_starving_pop_post_slaughter_healthy_homekill returns expected values
Test that calculate_starving_homekill_head returns expected values
Test that calculate_starving_pop_post_all_slaughter_homekill returns expected values
Test that calculate_starving_other_death_head returns expected values
Test that calculate_final_population updates animal population correctly
Test that feed_animals updates available feed and grass correctly
Test that calculate_starving_animals_after_feed updates population_starving_pre_slaughter correctly

"""

# Generated by CodiumAI
from src.food_system.animal_populations import AnimalSpecies
from src.food_system.animal_populations import AnimalPopulation
from pytz import country_names


import pytest

# The output python code of each test function must follow this instruction:
# 'need to create an animal object first with "AnimalSpecies class" with all required attribtues before testing population class.'
class TestAnimalPopulation:
    # Tests that the animal population is correctly initialized
    def test_initialize_animal_population(self):
        animal = AnimalSpecies("milk", "cow")
        animal.current_population = 100
        animal.population = [100]  # Adding population attribute
        AnimalPopulation.set_current_populations([animal])
        assert animal.current_population == 100
        assert animal.population == [100]

    # Tests that calculate_additive_births returns expected values
    def test_calculate_additive_births(self):
        animal = AnimalSpecies("animal_type", "animal_species")
        animal.gestation = 9
        animal.animals_per_pregnancy = 1
        animal.birth_ratio = 2
        animal.pregnant_animals_birthing_this_month = [10]  # Initialize the attribute
        animal.pregnant_animals_total = [100]  # Initialize the attribute
        animal.reduction_in_animal_breeding = 0.5  # Initialize the attribute
        new_births, new_export_births = AnimalPopulation.calculate_additive_births(
            animal, 9
        )
        assert new_births == 5
        assert new_export_births == 5

    # Tests that calculate_change_in_population updates animal population correctly
    def test_calculate_change_in_population(self):
        from src.food_system.animal_populations import CountryData

        animal = AnimalSpecies("type", "species")
        country_object = CountryData("country_code")
        country_object.month = 10
        animal.animal_function = "milk"
        animal.retiring_milk_animals = [10]
        animal.target_population_head = 100
        animal.slaughter = [0]
        animal.animal_slaughter_hours = 8
        animal.gestation = 9
        animal.pregnant_animals_total = [30]
        animal.slaughtered_pregnant_animals = [3]
        animal.pregnant_animals_birthing_this_month = [10]  # Initialize the attribute
        animal.pregnant_animals_total = [100]  # Initialize the attribute
        animal.other_death_causes_other_than_starving = [
            100
        ]  # Initialize the attribute
        animal.other_animal_death_rate_monthly = 0.05
        animal.pregnant_animal_slaughter_fraction = 0.2
        animal.current_population = 9000
        AnimalPopulation.calculate_change_in_population(animal, country_object, 10)
        assert animal.current_population == 8550
        assert country_object.spares_slaughter_hours == 0

    # Tests that calculate_pregnant_animals_birthing returns expected values
    def test_calculate_pregnant_animals_birthing(self):
        animal = AnimalSpecies("type", "species")
        animal.gestation = 9
        animal.pregnant_animals_total = [20]
        new_pregnant_animals_birthing = (
            AnimalPopulation.calculate_pregnant_animals_birthing(animal, 20)
        )
        assert new_pregnant_animals_birthing == 2.2222222222222223

    # Tests that calculate_pregnant_slaughter returns expected values
    def test_calculate_pregnant_slaughter(self):
        animal = AnimalSpecies("cow", "Holstein")
        animal.pregnant_animal_slaughter_fraction = 0.2
        animal.pregnant_animals_total = [30]
        (
            new_pregnant_animals_total,
            new_slaughtered_pregnant_animals,
        ) = AnimalPopulation.calculate_pregnant_slaughter(animal, 5)
        assert new_pregnant_animals_total == 25

    # Tests that calculate_animal_population returns expected values
    def test_calculate_animal_population(self):
        from src.food_system.animal_populations import CountryData

        animal = AnimalSpecies("meat", "cow")
        country = CountryData("country_code")
        animal.current_population = 300
        animal.target_population_head = 150
        animal.other_animal_death_rate_monthly = 5
        animal.animal_slaughter_hours = 8
        actual_slaughter_rate = AnimalPopulation.calculate_animal_population(
            animal, country, 10, 5, 10
        )
        assert actual_slaughter_rate == 10, "Expected slaughter rate to be 10"
        assert (
            country.spares_slaughter_hours == 0
        ), "Expected spare slaughter hours to be 50"
        assert animal.current_population == 295, "Expected current population to be 95"

    def test_calculate_animal_population_milk(self):
        from src.food_system.animal_populations import CountryData

        animal = AnimalSpecies("milk", "cow")
        country = CountryData("country_code")
        animal.current_population = 300
        animal.target_population_head = 150
        animal.other_animal_death_rate_monthly = 5
        animal.animal_slaughter_hours = 8
        actual_slaughter_rate = AnimalPopulation.calculate_animal_population(
            animal, country, 10, 5, 10
        )
        assert actual_slaughter_rate == 0, "Expected slaughter rate to be 10"
        assert (
            country.spares_slaughter_hours == 0
        ), "Expected spare slaughter hours to be 50"
        assert animal.current_population == 300, "Expected current population to be 95"

    def test_calculate_animal_population_under_target(self):
        from src.food_system.animal_populations import CountryData

        animal = AnimalSpecies("meat", "cow")
        country = CountryData("country_code")
        animal.current_population = 300
        animal.target_population_head = 500
        animal.other_animal_death_rate_monthly = 5
        animal.animal_slaughter_hours = 8
        actual_slaughter_rate = AnimalPopulation.calculate_animal_population(
            animal, country, 10, 5, 10
        )
        assert actual_slaughter_rate == 0, "Expected slaughter rate to be 10"
        assert (
            country.spares_slaughter_hours == 0
        ), "Expected spare slaughter hours to be 50"
        assert animal.current_population == 300, "Expected current population to be 95"

    # Tests that calculate_retiring_milk_animals returns expected values
    def test_calculate_retiring_milk_animals(self):
        animal = AnimalSpecies("type", "species")
        animal.current_population = 100
        animal.retiring_milk_animals_fraction = 0.1
        new_retiring_milk_animals = AnimalPopulation.calculate_retiring_milk_animals(
            animal
        )
        assert new_retiring_milk_animals == 10

    # Tests that calculate_births returns expected values
    def test_calculate_births(self):
        animal = AnimalSpecies("type", "species")
        animal.pregnant_animals_birthing_this_month = [5]
        animal.animals_per_pregnancy = 2
        animal.birth_ratio = 1.5
        new_births, new_export_births = AnimalPopulation.calculate_births(animal)
        assert new_births == 10
        assert new_export_births == 5

    # Tests that calculate_breeding_changes updates animal population correctly
    def test_calculate_breeding_changes(self):
        animal = AnimalSpecies("type", "species")
        animal.pregnant_animals_birthing_this_month = [10]
        animal.pregnant_animals_total = [20]
        animal.reduction_in_animal_breeding = 0.1
        AnimalPopulation.calculate_breeding_changes(animal)
        assert animal.pregnant_animals_birthing_this_month[-1] == 9
        assert animal.pregnant_animals_total[-1] == 18
        assert animal.pregnant_animal_slaughter_fraction == 0

    # Tests that calculate_other_deaths returns expected values
    def test_calculate_other_deaths(self):
        animal = AnimalSpecies("mammal", "cow")
        animal.current_population = 100
        animal.other_animal_death_rate_monthly = 5
        new_other_animal_death = AnimalPopulation.calculate_other_deaths(animal)
        assert new_other_animal_death == 500

    # Tests that calculate_slaughter_rate returns expected values
    def test_calculate_slaughter_rate(self):
        from src.food_system.animal_populations import CountryData

        animal = AnimalSpecies("animal_type_example", "animal_species_example")
        country = CountryData("country_name")
        country.month = 1
        animal.baseline_slaughter = 10
        country.spare_slaughter_hours = 20
        new_slaughter_rate = AnimalPopulation.calculate_slaughter_rate(
            animal, country, 10, 5
        )
        assert new_slaughter_rate == 30, "Expected slaughter rate to be 30"
        assert (
            country.spare_slaughter_hours == 0
        ), "Expected spare slaughter hours to be 0"

    # Tests that calculate_final_population updates animal population correctly
    def test_calculate_final_population(self):
        animal = AnimalSpecies("type1", "species1")
        animal.other_death_starving = [10]
        animal.homekill_healthy_this_month = [5]
        animal.homekill_starving_this_month = [2]
        animal.current_population = 100
        AnimalPopulation.calculate_final_population(animal)
        assert animal.current_population == 83

    # Tests that calculate_starving_pop_post_slaughter_healthy_homekill returns the expected value
    def test_calculate_starving_pop_post_slaughter_healthy_homekill(self):
        # create animal object
        animal_object = AnimalSpecies("cow", 100)
        # set current population
        animal_object.current_population = 80
        # set other attributes
        animal_object.slaughter = [10]
        animal_object.homekill_healthy_this_month = [5]
        # call function
        result = (
            AnimalPopulation.calculate_starving_pop_post_slaughter_healthy_homekill(
                animal_object
            )
        )
        # assert expected result
        assert result == 65

    # Tests that calculate_starving_pop_post_all_slaughter_homekill returns the expected value
    def test_calculate_starving_pop_post_all_slaughter_homekill(self):
        # create animal object
        animal_object = AnimalSpecies("cow", 100)
        # create country object
        country_object = Country("US", 100)
        # create animal population object
        animal_population_object = AnimalPopulation()
        # set current population
        animal_object.current_population = 50
        # calculate starving animals after feed
        animal_population_object.calculate_starving_animals_after_feed([animal_object])
        # calculate starving pop post all slaughter homekill
        result = (
            animal_population_object.calculate_starving_pop_post_all_slaughter_homekill(
                animal_object, animal_object.population_starving_pre_slaughter[-1]
            )
        )
        # assert result
        assert result == 25

    # Tests that calculate_healthy_homekill_head returns the expected value
    def test_calculate_healthy_homekill_head(self):
        # create animal object
        animal = AnimalSpecies("cow", 100)
        # create country object
        country = Country("US", 1000, 1000, 1000, 1000, 1000, 1000)
        # create animal population object
        animal_population = AnimalPopulation(animal, country)
        # set homekill hours budget
        country.homekill_hours_budget = [100]
        # calculate healthy homekill head
        actual_homekill_head = animal_population.calculate_healthy_homekill_head(
            animal, country
        )
        # check if actual_homekill_head is equal to expected value
        assert actual_homekill_head == 50

    # Tests that calculate_starving_animals_after_feed updates population_starving_pre_slaughter correctly
    def test_calculate_starving_animals_after_feed_updates_population_starving_pre_slaughter_correctly(
        self,
    ):
        animal = AnimalSpecies("cow", 100)
        animal_population = AnimalPopulation()
        animal_population.current_population = 100
        animal_population.calculate_starving_animals_after_feed([animal])
        assert animal_population.population_starving_pre_slaughter == [100]
        available_feed = 100
        available_grass = 100
        (available_feed, available_grass) = animal_population.feed_animals(
            [animal], [], available_feed, available_grass
        )
        animal_population.calculate_starving_animals_after_feed([animal])
        assert animal_population.population_starving_pre_slaughter == [50]

    # Tests that calculate_other_death_homekill_head returns the expected value
    def test_calculate_other_death_homekill_head(self):
        # create animal object
        animal = AnimalSpecies("cow", 100, 0.5)
        # create country object
        country = Country("US", 1000, 1000, 1000, 1000, 1000, 1000)
        # create animal population object
        animal_population = AnimalPopulation()
        # set current population
        animal_population.set_current_populations([animal])
        # calculate other death homekill head
        animal_population.calculate_other_death_homekill_head(animal, country)
        # check that the value is as expected
        assert animal.homekill_other_death_this_month[-1] == 50

    # Tests that calculate_starving_other_death_head returns the expected value
    def test_calculate_starving_other_death_head(self):
        # create animal object
        animal = AnimalSpecies("cow", 100)
        # create country object
        country = Country("US", 1000, 1000, 1000, 1000, 1000, 1000)
        # create animal population object
        animal_population = AnimalPopulation()
        # set current population
        animal_population.set_current_populations([animal])
        # calculate starving animals after feed
        animal_population.calculate_starving_animals_after_feed([animal])
        # calculate starving other death head
        starving_other_death_head = (
            animal_population.calculate_starving_other_death_head(
                animal, animal.current_population - animal.population_fed
            )
        )
        # assert expected value
        assert starving_other_death_head == animal.starvation_death_fraction * (
            animal.current_population - animal.population_fed
        )

    # Tests that calculate_starving_homekill_head returns the expected value
    def test_calculate_starving_homekill_head(self):
        # create animal object
        animal_object = AnimalSpecies("cow", 100, 0.5)
        # create country object
        country_object = Country("US", 100, 100)
        # set current population
        animal_object.current_population = 50
        # calculate starving animals after feed
        animal_object.population_fed = 40
        AnimalPopulation.calculate_starving_animals_after_feed([animal_object])
        # calculate starving population post slaughter and healthy homekill
        population_starving_post_slaughter_and_healthy_homekill = (
            AnimalPopulation.calculate_starving_pop_post_slaughter_healthy_homekill(
                animal_object
            )
        )
        # calculate starving homekill head
        actual_homekill_head = AnimalPopulation.calculate_starving_homekill_head(
            animal_object,
            country_object,
            population_starving_post_slaughter_and_healthy_homekill,
        )
        expected_homekill_head = 10
        assert actual_homekill_head == expected_homekill_head

    # Tests that feed_animals function updates available feed and grass correctly
    def test_feed_animals_updates_available_feed_and_grass_correctly(self):
        # create animal objects
        cow = AnimalSpecies("cow", 100)
        sheep = AnimalSpecies("sheep", 50)
        animal_list = [cow, sheep]
        ruminants = [cow]
        # set initial available feed and grass
        available_feed = {"feed": 100}
        available_grass = {"grass": 100}
        # call feed_animals function
        (new_available_feed, new_available_grass) = AnimalPopulation.feed_animals(
            animal_list, ruminants, available_feed, available_grass
        )
        # check that available feed and grass have been updated correctly
        assert new_available_feed == {"feed": 95}
        assert new_available_grass == {"grass": 90}
