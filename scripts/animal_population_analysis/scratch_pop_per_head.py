import pandas as pd
import numpy as np
import plotly.express as px
from pathlib import Path
import git


repo_root = git.Repo(".", search_parent_directories=True).working_dir

# Load data
animal_feed_data_dir = Path(repo_root) / "data" / "no_food_trade" / "animal_feed_data"
FAO_stat_slaughter_counts_processed_location = Path.joinpath(
    Path(animal_feed_data_dir), "FAO_stat_slaughter_counts_processed.csv"
)
head_count_csv_location = Path.joinpath(
    Path(animal_feed_data_dir), "head_count_csv.csv"
)

# Load data
processed_data_dir = Path(repo_root) / "data" / "no_food_trade" / "processed_data"
pop_csv_location = Path.joinpath(Path(processed_data_dir), "population_csv.csv")

# Load data
df_pop_country = pd.read_csv(pop_csv_location, index_col="iso3")
df_head_country = pd.read_csv(head_count_csv_location, index_col="iso3")
df_slaughter_country = pd.read_csv(
    FAO_stat_slaughter_counts_processed_location, index_col="iso3"
)


# merge all three dataframes
df_pop_head_country = pd.merge(
    df_pop_country, df_head_country, left_index=True, right_index=True
)
df_pop_head_country = pd.merge(
    df_pop_head_country, df_slaughter_country, left_index=True, right_index=True
)


# Calculate per head, small_animals,medium_animals,large_animals,dairy_cows
df_pop_head_country["poultry_per_head"] = (
    df_pop_head_country["small_animals"] / df_pop_head_country["population"]
)
df_pop_head_country["pig_per_head"] = (
    df_pop_head_country["medium_animals"] / df_pop_head_country["population"]
)
df_pop_head_country["beef_per_head"] = (
    df_pop_head_country["large_animals"] / df_pop_head_country["population"]
)
df_pop_head_country["dairy_per_head"] = (
    df_pop_head_country["dairy_cows"] / df_pop_head_country["population"]
)

# slaughter to head ratio, small_animal_slaughter,medium_animal_slaughter,large_animal_slaughter
df_pop_head_country["poultry_slaughter_to_head"] = (
    df_pop_head_country["small_animals"]
    / df_slaughter_country["small_animal_slaughter"]
)
df_pop_head_country["pig_slaughter_to_head"] = (
    df_pop_head_country["medium_animals"]
    / df_slaughter_country["medium_animal_slaughter"]
)
df_pop_head_country["beef_slaughter_to_head"] = (
    df_pop_head_country["large_animals"]
    / df_slaughter_country["large_animal_slaughter"]
)


# plotly to plot head per pop, sorted by beef per head
fig = px.bar(
    df_pop_head_country.sort_values(by="country_x"),
    x="country_x",
    y=["poultry_per_head", "pig_per_head", "beef_per_head", "dairy_per_head"],
    title="Species Per Head",
)
fig.update_layout(title_text="Species Per Head")
fig.show()

# plotly to plot slaughter to head ratio, sorted by beef per head
fig2 = px.bar(
    df_pop_head_country.sort_values(by="country_x"),
    x="country_x",
    y=["poultry_slaughter_to_head", "pig_slaughter_to_head", "beef_slaughter_to_head"],
    title="Slaughter to Head Ratio",
)
fig2.update_layout(title_text="Slaughter to Head Ratio")
# include the country code (index) in the hover text
fig2.show()

# plotly to plot scatter comparing beef per head and slaughter to head ratio, use color to show country
fig3 = px.scatter(
    df_pop_head_country,
    x="large_animals",
    y="large_animal_slaughter",
    title="Beef Per Head vs Slaughter to Head Ratio",
    trendline="ols",
)
# inlcude hover data for country
fig3.update_traces(
    hovertemplate="<b>Country</b>: %{text}<br><b>Beef Pop</b>: %{x}<br><b>Slaughter Count</b>: %{y}"
)
fig3.update_traces(text=df_pop_head_country.index)

# draw a trendline
fig3.update_layout(title_text="Beef Pop vs Slaughter Count")
fig3.show()
