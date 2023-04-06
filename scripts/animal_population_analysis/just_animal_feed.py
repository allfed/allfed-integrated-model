from src.food_system.calculate_animals_and_feed_over_time import CalculateAnimalOutputs
import plotly.express as px

cao = CalculateAnimalOutputs()
constants_inputs = {}

constants_inputs["COUNTRY_CODE"] = "ARG"
constants_inputs["NMONTHS"] = 120
reduction_in_dairy_calves = 0
use_grass_and_residues_for_dairy = False
feed_ratio = 1

data = {
    "country_code": constants_inputs["COUNTRY_CODE"],
    "reduction_in_beef_calves": 90,
    "reduction_in_dairy_calves": reduction_in_dairy_calves,
    "increase_in_slaughter": 110,
    "reduction_in_pig_breeding": 90,
    "reduction_in_poultry_breeding": 90,
    "months": constants_inputs["NMONTHS"],
    "discount_rate": 30,
    "mother_slaughter": 0,
    "use_grass_and_residues_for_dairy": use_grass_and_residues_for_dairy,
    "keep_dairy": True,
    "feed_ratio": feed_ratio,
}

feed_dairy_meat_results, feed = cao.calculate_feed_and_animals(data)


# plotly to plot species slaughter
fig = px.line(
    feed_dairy_meat_results,
    x="Month",
    y=[
        "Poultry Slaughtered",
        "Pig Slaughtered",
        "Beef Slaughtered",
        "Dairy Slaughtered",
    ],
    title="Species Slaughtered",
)
fig.update_layout(title_text="Species Slaughtered " + constants_inputs["COUNTRY_CODE"])
fig.show()


fig2 = px.line(
    feed_dairy_meat_results,
    x="Month",
    y=["Beef Pop", "Dairy Pop", "Pigs Pop", "Poultry Pop"],
    title="Species Pops",
)
fig2.update_layout(title_text="Species Pops " + constants_inputs["COUNTRY_CODE"])
fig2.show()
