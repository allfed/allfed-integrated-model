################################# Run Baseline ################################
##                                                                            #
##         Import the computer readable spreadsheet and run a year 2020       #
##          no trade scenario with the optimizer, then plot the results       #
##                                                                            #
###############################################################################


import pandas as pd
import numpy as np
import requests
import json
import os
import sys
import matplotlib.pyplot as plt
import matplotlib.colors as colors

module_path = os.path.abspath(os.path.join("../.."))
if module_path not in sys.path:
    sys.path.append(module_path)

import geopandas as gpd
import geoplot as gplt

# import some python files from this integrated model repository
from src.optimizer.optimizer import Optimizer
from src.utilities.plotter import Plotter
from src.optimizer.parameters import Parameters
from src.scenarios.scenarios import Scenarios

# country codes for UK + EU 27 countries (used for plotting map)
UK_27_Plus_GBR_countries = [
    "GBR",
    "AUT",
    "BEL",
    "BGR",
    "HRV",
    "CYP",
    "CZE",
    "DNK",
    "EST",
    "FIN",
    "FRA",
    "DEU",
    "GRC",
    "HUN",
    "IRL",
    "ITA",
    "LVA",
    "LTU",
    "LUX",
    "MLT",
    "NLD",
    "POL",
    "PRT",
    "ROU",
    "SVK",
    "SVN",
    "ESP",
    "SWE",
]

NO_TRADE_CSV = "../../data/no_food_trade/computer_readable_combined.csv"

no_trade_table = pd.read_csv(NO_TRADE_CSV)

sum_pop = 0  # initialize to zero population for summing global population

# import the visual map
world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))

constants_loader = Parameters()
scenarios_loader = Scenarios()


def run_optimizer_for_country(country_code, country_data):

    # initialize country specific food system properties
    inputs_to_optimizer = scenarios_loader.init_country_food_system_properties(
        country_data
    )

    inputs_to_optimizer = scenarios_loader.set_country_seasonality_baseline(
        inputs_to_optimizer, country_data
    )

    # set params that are true for baseline climate,
    # regardless of whether country or global scenario

    inputs_to_optimizer = scenarios_loader.get_baseline_scenario(inputs_to_optimizer)

    inputs_to_optimizer = scenarios_loader.set_baseline_nutrition_profile(
        inputs_to_optimizer
    )

    inputs_to_optimizer = scenarios_loader.set_stored_food_usage_as_80_percent_used(
        inputs_to_optimizer
    )

    inputs_to_optimizer = scenarios_loader.set_fish_baseline(inputs_to_optimizer)

    inputs_to_optimizer = scenarios_loader.set_waste_to_baseline_prices(
        inputs_to_optimizer
    )

    inputs_to_optimizer = scenarios_loader.set_immediate_shutoff(inputs_to_optimizer)

    inputs_to_optimizer = scenarios_loader.set_disruption_to_crops_to_zero(
        inputs_to_optimizer
    )

    # No excess calories
    inputs_to_optimizer["EXCESS_CALORIES"] = np.array(
        [0] * inputs_to_optimizer["NMONTHS"]
    )

    constants["inputs"] = inputs_to_optimizer

    (
        single_valued_constants,
        multi_valued_constants,
    ) = constants_loader.computeParameters(constants)
    single_valued_constants["CHECK_CONSTRAINTS"] = False

    optimizer = Optimizer()
    [time_months, time_months_middle, analysis] = optimizer.optimize(
        single_valued_constants, multi_valued_constants
    )

    needs_ratio = analysis.percent_people_fed / 100

    print("No trade expected kcals/capita/day 2020")
    print(needs_ratio * 2100)
    print("")

    # Plotter.plot_fig_s1abcd(analysis, analysis, 72)

    return needs_ratio


def get_country_data(country_code, needs_ratio):
    # population = world[world['iso_a3'].apply(lambda x: x == country)]

    if country_code == "SWT":
        country_code_map = "SWZ"
    else:
        country_code_map = country_code
    country_map = world[world["iso_a3"].apply(lambda x: x == country_code_map)]

    if len(country_map) == 0:
        print("no match")
        print(country_code_map)

    if len(country_map) == 1:
        # world.loc[world_index, 'needs_ratio'] = needs_ratio

        # cap at 100% fed, surplus is not traded away in this scenario
        kcals_ratio_capped = 1 if needs_ratio >= 1 else needs_ratio
        # fat_ratio_capped = 1 if fat_ratio >= 1 else fat_ratio
        # protein_ratio_capped = 1 if protein_ratio >= 1 else protein_ratio
        world_index = country_map.index
        world.loc[world_index, "needs_ratio"] = kcals_ratio_capped


# iterate over each country from spreadsheet, run the optimizer, plot the result
og_sum = 0
for index, country_data in no_trade_table.iterrows():
    country_code = country_data["iso3"]
    country_name = country_data["country"]

    print("")
    print(country_name)

    population = country_data["population"]

    needs_ratio = run_optimizer_for_country(country_code, country_data)
    # og = run_optimizer_for_country(country_code, country_data)
    # og_sum += og
    # print(og)

    if country_code == "F5707+GBR":
        for c in UK_27_Plus_GBR_countries:
            get_country_data(c, needs_ratio)
    else:
        get_country_data(country_code, needs_ratio)

##LATER##
# print("og_sum")
# print(og_sum)
# quit()

# world[world['kcals_frac_fed']==0] = np.nan
# world[world['fat_frac_fed']==0] = np.nan
# world[world['protein_frac_fed']==0] = np.nan
# world[world['max_frac_fed']==0] = np.nan
# print(world['max_frac_fed'])
plt.close()
mn = 0
mx = 1
ax = world.plot(
    column="needs_ratio",
    legend=True,
    cmap="viridis",
    legend_kwds={"label": "Fraction Fed", "orientation": "horizontal"}
    # missing_kwds={
    #             "color": "lightgrey",
    #             "edgecolor": "red",
    #             "hatch": "///",
    #             "label": "Missing values",
    # }
)

pp = gplt.polyplot(world, ax=ax, zorder=1, linewidth=0.1)
# Plotter.formatticklabels(mn,mx,pp)
# plt.rcParams['text.usetex'] = True
plt.title("Fraction of minimum macronutritional needs with no trade")
# plt.savefig(Params.globalEfieldPlots+'Results'+str(r)+'perYearWindow'+str(windowperiod)+'s.png')
plt.show()
plt.close()
quit()
mn = 0
mx = 1
ax = world.plot(
    column="fat_frac_fed",
    legend=True,
    cmap="viridis",
    legend_kwds={"label": "Fraction Fed", "orientation": "horizontal"},
)
pp = gplt.polyplot(world, ax=ax, zorder=1, linewidth=0.1)
# Plotter.formatticklabels(mn,mx,pp)
# plt.rcParams['text.usetex'] = True
plt.title("Fraction of minimum fat needs with no trade")
# plt.savefig(Params.globalEfieldPlots+'Results'+str(r)+'perYearWindow'+str(windowperiod)+'s.png')
plt.show()
plt.close()

mn = 0
mx = 1
ax = world.plot(
    column="protein_frac_fed",
    legend=True,
    cmap="viridis",
    legend_kwds={"label": "Fraction Fed", "orientation": "horizontal"},
)
pp = gplt.polyplot(world, ax=ax, zorder=1, linewidth=0.1)
# Plotter.formatticklabels(mn,mx,pp)
# plt.rcParams['text.usetex'] = True
plt.title("Fraction of minimum protein needs with no trade")
# plt.savefig(Params.globalEfieldPlots+'Results'+str(r)+'perYearWindow'+str(windowperiod)+'s.png')
plt.show()

mn = 0
mx = 1
ax = world.plot(
    column="min_frac_fed",
    legend=True,
    cmap="viridis",
    legend_kwds={"label": "Fraction Fed", "orientation": "horizontal"},
)
pp = gplt.polyplot(world, ax=ax, zorder=1, linewidth=0.1)
# Plotter.formatticklabels(mn,mx,pp)
# plt.rcParams['text.usetex'] = True
plt.title("Smallest fraction of any macronutrient need with no trade")
# plt.savefig(Params.globalEfieldPlots+'Results'+str(r)+'perYearWindow'+str(windowperiod)+'s.png')
plt.show()
