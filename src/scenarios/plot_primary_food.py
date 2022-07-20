import os
import sys
import numpy as np


module_path = os.path.abspath(os.path.join("../.."))
print(module_path)
if module_path not in sys.path:
    sys.path.append(module_path)

# import some python files from this integrated model repository
from src.utilities.plotter import Plotter

resilient_food_primary_production_analysis = np.load(
    "../data/resilient_food_primary_analysis.npy", allow_pickle=True
).item()
no_resilient_food_primary_production_analysis = np.load(
    "../data/no_resilient_food_primary_analysis.npy", allow_pickle=True
).item()
Plotter.plot_fig_s2abcd(
    resilient_food_primary_production_analysis,
    no_resilient_food_primary_production_analysis,
    48,
    72,
)
