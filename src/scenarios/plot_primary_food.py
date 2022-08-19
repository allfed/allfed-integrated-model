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
