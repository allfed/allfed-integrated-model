import pandas as pd
from src.food_system.animal_populations import CountryData
from src.food_system.animal_populations import AnimalSpecies
from src.food_system.animal_populations import Debugging
from src.food_system.animal_populations import main
from src.food_system.animal_populations import CalculateFeedAndMeat
from src.food_system.animal_populations import AnimalDataReader
from src.food_system.food import Food
from click import Path


### Import kcal per kg data ###

attributes_csv = "species_attributes.csv"
df_animal_attributes = AnimalDataReader.read_animal_nutrition_data(attributes_csv)

# first grab the index 'chicken' and the column 'kcals per kg'
# this is the kcals per kg of chicken
kcals_per_kg_chicken = df_animal_attributes.loc['chicken','kcals per kg']
# get for meat_sheep
kcals_per_kg_sheep = df_animal_attributes.loc['meat_sheep','kcals per kg']
# and for meat_cattle
kcals_per_kg_cattle = df_animal_attributes.loc['meat_cattle','kcals per kg']


### cxhange these values to see how the model responds ###
feed = 0 # billion kcals, shorthand way to apply consistent supply over whole period
grass = 0 # billion kcals, shorthand way to apply consistent supply over whole period
months = 120


grass_object = Debugging.available_grass_function(grass,months)
feed_object = Debugging.available_feed_function(feed,months)

# add manual override of constant feed and grass supply here if required




# Instantiate the class
calculate_instance = CalculateFeedAndMeat('USA', feed_object, grass_object)
animals_killed_for_meat_small,animals_killed_for_meat_medium,animals_killed_for_meat_large = calculate_instance.get_feed_used_and_meat_produced()
# now we can calculate the total kcals of meat produced
total_kcals_meat = ((animals_killed_for_meat_small*kcals_per_kg_chicken)
    + (animals_killed_for_meat_medium*kcals_per_kg_sheep) 
    + (animals_killed_for_meat_large*kcals_per_kg_cattle)) * (1/(10**9))

# and the total kcals of feed used, and grass
feed_used = calculate_instance.feed_used.kcals
grass_used = calculate_instance.grass_used.kcals



## do the same but with polotly
import plotly.graph_objects as go
fig = go.Figure()
fig.add_trace(go.Scatter(y=feed_used, mode='lines', name='feed used'))
fig.add_trace(go.Scatter(y=grass_used, mode='lines', name='grass used'))
fig.add_trace(go.Scatter(y=total_kcals_meat, mode='lines', name='meat produced'))
# add axis labels
fig.update_layout(
    title="Feed and meat production",
    xaxis_title="Months",
    yaxis_title="Billion kcals",
    legend_title="Legend Title",
    font=dict(
        family="Courier New, monospace",
        size=18,
        color="RebeccaPurple"
    )
)

fig.show()



# new graph with the ratio of feed/meat kcals
ratio = []
for i in range(len(feed_used)):
    ratio.append(feed_used[i]/total_kcals_meat[i])

fig = go.Figure()
fig.add_trace(go.Scatter(y=ratio, mode='lines', name='ratio'))
# add axis labels
fig.update_layout(
    title="Ratio of feed to meat production",
    xaxis_title="Months",
    yaxis_title="Ratio",
    legend_title="Legend Title",
    font=dict(
        family="Courier New, monospace",
        size=18,
        color="RebeccaPurple"
    )
)

fig.show()



# do the same as above but for a varibale amount of animals (don't hardcode the [0], [1], [2])
# get the number of animals
num_animals = len(calculate_instance.all_animals)
# create a list of animal names
animal_names = []
for i in range(num_animals):
    animal_names.append(calculate_instance.all_animals[i].animal_type)
# create a list of animal populations
animal_populations = []
for i in range(num_animals):
    animal_populations.append(calculate_instance.all_animals[i].population)

# now plot the animal populations
fig = go.Figure()

for i in range(num_animals):
    fig.add_trace(go.Scatter(y=animal_populations[i], mode='lines', name=animal_names[i]))

# add axis labels
fig.update_layout(
    title="Animal populations",
    xaxis_title="Months",
    yaxis_title="Population",
    legend_title="Legend Title",
    font=dict(
        family="Courier New, monospace",
        size=18,
        color="RebeccaPurple"
    )
)











