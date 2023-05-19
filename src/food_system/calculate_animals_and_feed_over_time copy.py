"""
This is a function used to quickly estimate the feed usage and resulting meat when
breeding is changed and slaughter is increased somewhat (or whatever reasonable result
is to be expected in the scenario in question).
"""
from pathlib import Path
import pandas as pd
import numpy as np
import git
from src.food_system.food import Food
import pdb


### DAIRY 
 
# # this set up only kills dairy cows when they are getting to the end of
# # their life.
# current_dairy_slaughter = (
#     current_dairy_cattle / (dairy_life_expectancy) / 12
# )
# current_beef_slaughter = current_cow_slaughter - current_dairy_slaughter
# if current_beef_cattle < current_beef_slaughter:
#     # line below required due to the difference between actual slaughter
#     # and 'slaughter capacity' consider a rewrite of the whole method to
#     # distinuguish between these two. For now, this is thr workaround.
#     actual_beef_slaughter = current_beef_cattle

#     if keep_dairy == 0:
#         current_dairy_slaughter = (
#             current_cow_slaughter - actual_beef_slaughter
#         )


### Work on this section to create the dairy cow -> meat cow transfer. Then treat old dary cows in the meat cow population as normal meat cows.
# # life expetency values
# dairy_life_expectancy = (
#     5.87  # https://www.frontiersin.org/articles/10.3389/fvets.2021.646672/full
# )
# dairy_start_milking_age = 2
# dairy_track_milk_ready_percent = (
#     dairy_life_expectancy - dairy_start_milking_age
# ) / dairy_life_expectancy
# dairy_cows_end_of_life_annual = (
#     total_dairy_cows / dairy_life_expectancy
#     + total_dairy_cows * other_cow_death_rate_annual
# )  # first terms are those being slaughtered once milking is done, then
# # combine this with other death


#import from FAO data/animal class
animals_slaughter_pm = 10000  # FROM FAO
total_animals = 1000000 # FROM FAO


# options set by user (whih are needed in level above)
increase_in_slaughter = 110/100



## these things happen outside of this script, one level up
current_animal_slaughter = (
    animals_slaughter_pm * increase_in_slaughter
)  # measured in head per month


# animals
# these inputs will need to be updated to be dynamic
gestation_period = 9 
reduction_in_breeding = 0.5
animal_slaughter_hours = 4  # resources for slaughter of animal

new_animals = animals_slaughter_pm # assumes steady state (slaughter = births ADD in Other death? to hit replacement rate)
animalGestation = 9
animals_per_litter = 10
other_animal_death_rate_annual = 5 / 100
other_animal_death_rate_monthly = other_animal_death_rate_annual / 12
reduction_in_animal_breeding = 80
mother_slaughter = 50
reduction_in_animal_breeding *= 0.01
months_elapsed = 1

animal_total_death_pm = (
    animals_slaughter_pm + total_animals * other_animal_death_rate_monthly
)

# current toals, basically the same as totals for this scope
current_total_animals = total_animals

# assume steady state popualtion, define birth rates from death rates
new_animals_pm = animal_total_death_pm


# pregnant animals
current_pregnant_animals = new_animals_pm / animals_per_litter
pregnant_animal_slaughter_percent = (
    mother_slaughter / 100
)  # of total percent of animal slaughter



spare_slaughter_hours = 0

# determine birth rates
if np.abs(months_elapsed - gestation_period) <= 0.5:
    new_animals *= 1 - reduction_in_breeding

# Transfer excess slaughter capacity to next animal, current coding method
# only allows poultry -> animal -> cow, there are some small erros here due to
# rounding, and the method is not 100% water tight but errors are within the
# noise

if current_total_animals < current_animal_slaughter:
    spare_slaughter_hours = (
        current_animal_slaughter - current_total_animals - new_animals_pm
    ) * animal_slaughter_hours
else:
    spare_slaughter_hours = 0



other_animal_death = current_total_animals * other_animal_death_rate_monthly

# ## Generate list (before new totals have been calculated)
# magnitude adjust moves the numbers from per thousnad head to per head (or
# other)
# feed adjust turns lbs in to tons


current_total_animals += new_animals_pm - current_animal_slaughter - other_animal_death


# deal with pregnant animals
current_pregnant_animals -= pregnant_animal_slaughter_percent * (
    current_animal_slaughter + other_animal_death
)

if current_total_animals < 0:
    current_total_animals = 0


# should return
# animals slaughtered
# animals born
# animals died other
# slaughter capacity from this animal (from baseline). This will be hard and need to be passed between animals

