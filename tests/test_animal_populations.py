# Test animal_populations.py using pytest

import pytest
from src.food_system.animal_populations import AnimalSpecies
from src.food_system.food import Food

# Define the fixture for AnimalSpecies
# animal_type, population, slaughter, animal_function, feed_LSU, digestion_type, approximate_feed_conversion, (OPTIONAL: digestion_efficiency = 0.5)
@pytest.fixture
def cattle_animal_species():
    return AnimalSpecies(12,"meat_cattle", 10^8, 10^6, "milk", 1, "ruminant", 0.2)
@pytest.fixture
def chicken_animal_species():
    return AnimalSpecies(12,"chicken", 10^8, 10^6, "meat", 0.008, "monogastric", 1)

# Define the test function
def test_net_energy_required_per_month(chicken_animal_species):
    # Access the animal_species fixture
    animal = chicken_animal_species
    # Call the method being tested
    net_energy = animal.net_energy_required_per_month()
    # Assertion to check if the calculated net energy is a food object
    assert net_energy < 10**(-5) and net_energy > 10**(-6) # reasonable bounds for chicken net energy


def test_feed_required_per_month_individual(chicken_animal_species):
    """
    In the future, this test should be updated to check if the output is a food object  (once the Food class is implemented with carbs/protein/fats)
    """
    # Access the animal_species fixture
    animal = chicken_animal_species
    # Call the method being tested
    feed_required = animal.feed_required_per_month_individual()
    # Assertion to check if the output is a food object
    assert isinstance(feed_required, Food)


def test_init_feed_required_monthly_species(chicken_animal_species):
    """
    In the future, this test should be updated to check if the output is a food object  (once the Food class is implemented with carbs/protein/fats)
    """
    total_months = 12
    # Access the animal_species fixture
    animal = chicken_animal_species
    # Call the method being tested
    animal.init_feed_required_monthly_species(total_months)
    # Assertion to check if the output is a food object

    assert isinstance( animal.feed_balance, Food)
    assert len(animal.feed_balance.kcals) == total_months
    assert len(animal.feed_balance.protein) == total_months
    assert len(animal.feed_balance.fat) == total_months

    # TODO: I need help working out how to use this food object... I'm confused.
    ### This does't work:
    # assert Food.validate_if_list(animal.feed_balance)
    # commented out for now.
    ####### ISSUE ^^^^^^^ ########


def test_feed_the_species(cattle_animal_species):
    # Create an instance of the class or mock the necessary objects
    # Initialize the necessary variables and objects for testing
    animal = cattle_animal_species
    food_input = Food(0, 0, 0)
    food_input.kcals_units = 
    self.feed_balance.kcals_units="billion kcals each month",
    self.feed_balance.fat_units="thousand tons each month",
    self.feed_balance.protein_units="thousand tons  each month",


    # Test case 1: No food required
    # Set up the initial conditions where feed_balance.kcals is 0
    # Call the feed_the_species method with appropriate arguments
    # Assert that the return value matches the expected value
    food_input = Food(12, 5, 4)
    cattle_animal_species.feed_balance.kcals[-1] = 0
    feed_leftover = animal.feed_the_species(food_input)
    assert feed_leftover == food_input

    # # Test case 3: Only using kcals
    # # Set up the initial conditions where feed_balance.fat and feed_balance.protein are 0
    # # Call the feed_the_species method with appropriate arguments
    # # Assert the expected changes in population_fed, food_input, and feed_balance
    # food_input = Food(12, 5, 4)
    # cattle_animal_species.feed_balance[-1].fat = 0
    # cattle_animal_species.feed_balance[-1].protein = 0
    # cattle_animal_species.feed_balance[-1].kcals = 9
    # feed_leftover = animal.feed_the_species(food_input)
    # print(feed_leftover.kcals)
    # print(food_input.kcals)
    # assert feed_leftover.kcals < food_input.kcals



    # # Test case 4: Using protein and fats
    # # Set up the initial conditions where feed_balance.fat > 0 and feed_balance.protein > 0
    # # Call the feed_the_species method with appropriate arguments
    # # Assert the expected changes in population_fed, food_input, and feed_balance
    # cattle_animal_species.feed_balance[-1].fat = 3
    # cattle_animal_species.feed_balance[-1].protein = 1
    # cattle_animal_species.feed_balance[-1].kcals = 7
    # feed_leftover = animal.feed_the_species(food_input)
    # assert feed_leftover.kcals < food_input.kcals



    # Additional test cases: Cover other scenarios and edge cases as needed

    # Cleanup or reset any modified objects or variables if necessary


# Functions:
# AnimalSpecies.__init__
# AnimalSpecies.feed_required_per_month_individual
# AnimalSpecies.feed_required_per_month_species
# AnimalSpecies.feed_the_species
# AnimalSpecies.net_energy_required_per_month
# AnimalSpecies.set_species_milk_attributes
# AnimalSpecies.set_species_slaughter_attributes
# available_feed
# available_grass
# calculate_animal_population
# calculate_births
# calculate_breeding_changes
# calculate_meat_change_in_population
# calculate_milk_change_in_population
# calculate_other_deaths
# calculate_pregnant_animals_birthing
# calculate_pregnant_slaughter
# calculate_retiring_milk_animals
# calculate_slaughter_rate
# change_in_animal_population
# create_animal_objects
# feed_animals
# food_conversion
# read_animal_nutrition_data
# read_animal_options
# read_animal_population_data
# update_animal_objects_with_milk
# update_animal_objects_with_slaughter

