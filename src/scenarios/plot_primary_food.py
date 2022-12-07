"""
@author Morgan Rivers
@date 2022-10-25

mari was here >:p

Loads in data from data/resilient_food_primary_results.npy and
data/no_resilient_food_primary_results.npy previously generated files, created by
running run_model_no_resilient_foods.py and run_model_with_resilient_foods.py.
These are the resilient and non-resilient food "primary" production results. Finally,
it plots the results.

Primary production results are considered total food production before waste or
consumption by nonhuman animals or biofuels.


"""

import numpy as np
from src.utilities.plotter import Plotter

resilient_food_primary_production_results = np.load(
    "../data/resilient_food_primary_results.npy", allow_pickle=True
).item()
no_resilient_food_primary_production_results = np.load(
    "../data/no_resilient_food_primary_results.npy", allow_pickle=True
).item()
Plotter.plot_fig_s2abcd(
    resilient_food_primary_production_results,
    no_resilient_food_primary_production_results,
    48,
    72,
)
