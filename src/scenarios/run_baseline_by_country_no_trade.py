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

module_path = os.path.abspath(os.path.join('../..'))
if module_path not in sys.path:
    sys.path.append(module_path)

import geopandas as gpd
import geoplot as gplt

#import some python files from this integrated model repository
from src.optimizer.optimizer import Optimizer
from src.utilities.plotter import Plotter
from src.optimizer.parameters import Parameters
from src.scenarios import Scenarios

# country codes for UK + EU 27 countries (used for plotting map)
UK_27_Plus_GBR_countries = ["GBR","AUT","BEL","BGR","HRV","CYP","CZE",\
                            "DNK","EST","FIN","FRA","DEU","GRC","HUN",\
                            "IRL","ITA","LVA","LTU","LUX","MLT","NLD",\
                            "POL","PRT","ROU","SVK","SVN","ESP","SWE"]

NO_TRADE_CSV = \
    '../../data/no_food_trade/computer_readable_combined.csv'

no_trade_table = pd.read_csv(NO_TRADE_CSV)

sum_pop = 0 # initialize to zero population for summing global population

# import the visual map
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

constants_loader = Parameters()
scenarios_loader = Scenarios()


# TODO ADD DEF
def run_optimizer_for_country(country_code,country_data):
    # if(country_code != "BLR" ):
    # if(country_code != "BEN" and country_code != "BLR" ):
    # if(country_code != "BEN" ):
    #     return 0
    # if(country_data["population"]<100e6):
    #     return 0
    # country_data["aq_kcals"] = 9260.0
    # country_data["aq_fat"] = 5780.0
    # country_data["aq_protein"] = 1360.0
    # country_data["grasses_baseline"] = 3908404.227
    # country_data["grasses_y1"] = 2383047.404
    # country_data["grasses_y2"] = 889454.4352
    # country_data["grasses_y3"] = 499371.1723
    # country_data["grasses_y4"] = 524631.5653
    # country_data["grasses_y5"] = 636577.1278
    # country_data["grasses_y6"] = 1038359.14
    # country_data["grasses_y7"] = 1440141.152
    # country_data["grasses_y8"] = 2045074.444
    # country_data["grasses_y9"] = 2745734.002
    # country_data["grasses_y10"] = 3368749.486
    # country_data["dairy"] = 153000.0
    # country_data["chicken"] = 15508.0
    # country_data["pork"] = 7087.0
    # country_data["beef"] = 44064.0
    # country_data["small_animals"] = 22690000.0
    # country_data["medium_animals"] = 3549000.0
    # country_data["large_animals"] = 2593841.0
    # country_data["dairy_cows"] = 623376.0

    # country_data["biofuel_kcals"] = 900000.0
    # country_data["biofuel_fat"] = 220000.0
    # country_data["biofuel_protein"] = 50000.0
    # country_data["feed_kcals"] = 1.23
    # country_data["feed_fat"] = 0.08
    # country_data["feed_protein"] = 0.21
    # country_data["crop_kcals"] = 4922037.004904
    # country_data["crop_fat"] = 319332.173795
    # country_data["crop_protein"] = 473570.074108
    # country_data["seasonality_m1"] = 0.248276
    # country_data["seasonality_m2"] = 0.0
    # country_data["seasonality_m3"] = 0.0
    # country_data["seasonality_m4"] = 0.0
    # country_data["seasonality_m5"] = 0.001724
    # country_data["seasonality_m6"] = 0.001724
    # country_data["seasonality_m7"] = 0.001724
    # country_data["seasonality_m8"] = 0.001724
    # country_data["seasonality_m9"] = 0.0
    # country_data["seasonality_m10"] = 0.248276
    # country_data["seasonality_m11"] = 0.248276
    # country_data["seasonality_m12"] = 0.248276
    # country_data["stocks_kcals"] = 704613.833333
    # country_data["stocks_fat"] = 49550.293333
    # country_data["stocks_protein"] = 39271.213333

    # Belarus
    # Unnamed: 0                       11
    # iso3                            BLR
    # country                     Belarus
    # population                9398861.0
    # aq_kcals                     1920.0
    # aq_fat                       1210.0
    # aq_protein                    280.0
    # grasses_baseline        8019548.671
    # grasses_y1              5041765.351
    # grasses_y2              1856755.082
    # grasses_y3              1068705.706
    # grasses_y4              1071839.351
    # grasses_y5              1250095.079
    # grasses_y6              1977957.551
    # grasses_y7              2705820.024
    # grasses_y8              3808167.157
    # grasses_y9              5127850.073
    # grasses_y10             6314624.603
    # dairy                     7394000.0
    # chicken                    512515.0
    # pork                       402700.0
    # beef                       340500.0
    # small_animals            49491000.0
    # medium_animals            3020100.0
    # large_animals             4335071.0
    # dairy_cows                1485200.0
    # biofuel_kcals              310000.0
    # biofuel_fat                110000.0
    # biofuel_protein             10000.0
    # feed_kcals                     6.37
    # feed_fat                       0.43
    # feed_protein                   1.19
    # crop_kcals          10075758.112022
    # crop_fat                582678.3083
    # crop_protein         1347850.967383
    # seasonality_m1              0.03348
    # seasonality_m2                  0.0
    # seasonality_m3                  0.0
    # seasonality_m4                  0.0
    # seasonality_m5                  0.0
    # seasonality_m6                  0.0
    # seasonality_m7              0.21652
    # seasonality_m8              0.21652
    # seasonality_m9              0.21652
    # seasonality_m10                0.25
    # seasonality_m11             0.03348
    # seasonality_m12             0.03348
    # stocks_kcals         1768197.208333
    # stocks_fat            123251.566667
    # stocks_protein        189816.883333
    # print(country_data)
    # quit()
    constants = {}
    constants['CHECK_CONSTRAINTS'] = False
    # print(country_data['population']/1e6)
    # print(country_data['crop_kcals']/1e6)
    # print(country_data['stocks_kcals']/1e6)
    # print(country_data['stocks_kcals']/1e6)
    #BEN STOCKS 704613.8333333337
    #BLR STOCKS 1768197.2083333333
    # country_data['population'] = 12.1231980*1e6
    # country_data['crop_kcals'] = 4.9220370049043*1e6
    # country_data['stocks_kcals'] = .7046138333333337*1e6

    # country_data["seasonality_m1"] = 0.248276
    # country_data["seasonality_m2"] = 0.0
    # country_data["seasonality_m3"] = 0.0
    # country_data["seasonality_m4"] = 0.0
    # country_data["seasonality_m5"] = 0.001724
    # country_data["seasonality_m6"] = 0.001724
    # country_data["seasonality_m7"] = 0.001724
    # country_data["seasonality_m8"] = 0.001724
    # country_data["seasonality_m9"] = 0.0
    # country_data["seasonality_m10"] = 0.248276
    # country_data["seasonality_m11"] = 0.248276
    # country_data["seasonality_m12"] = 0.248276

    #initialize country specific food system properties 
    inputs_to_optimizer = \
        scenarios_loader.init_country_food_system_properties(country_data)

    inputs_to_optimizer = \
        scenarios_loader.set_country_seasonality_baseline(
            inputs_to_optimizer,
            country_data
        )

    # set params that are true for baseline climate,
    # regardless of whether country or global scenario

    inputs_to_optimizer = \
        scenarios_loader.get_baseline_scenario(inputs_to_optimizer)

    inputs_to_optimizer = \
        scenarios_loader.set_baseline_nutrition_profile(inputs_to_optimizer)

    inputs_to_optimizer = \
        scenarios_loader.set_stored_food_usage_as_may_till_minimum(
            inputs_to_optimizer
        )

    inputs_to_optimizer = \
        scenarios_loader.set_fish_baseline(inputs_to_optimizer)

    inputs_to_optimizer = \
        scenarios_loader.set_waste_to_baseline_prices(inputs_to_optimizer)


    inputs_to_optimizer = \
        scenarios_loader.set_immediate_shutoff(inputs_to_optimizer)

    inputs_to_optimizer = \
        scenarios_loader.set_disruption_to_crops_to_zero(
            inputs_to_optimizer
        )

    # No excess calories
    inputs_to_optimizer["EXCESS_CALORIES"] = \
        np.array([0] * inputs_to_optimizer['NMONTHS'])

    constants['inputs'] = inputs_to_optimizer

    # og = \
    single_valued_constants, multi_valued_constants = \
        constants_loader.computeParameters(constants)

    single_valued_constants["CHECK_CONSTRAINTS"] = False
    optimizer = Optimizer()
    [time_months, time_months_middle, analysis] = \
        optimizer.optimize(single_valued_constants, multi_valued_constants)

    needs_ratio = analysis.percent_people_fed/100

    print("No trade expected kcals/capita/day 2020")
    print(needs_ratio*2100)
    print("")

    # Plotter.plot_fig_s1abcd(analysis, analysis, 72)

    return needs_ratio
    # return og

# TODO ADD DEF
def get_country_data(country_code, needs_ratio):
    # population = world[world['iso_a3'].apply(lambda x: x == country)]
    
    if(country_code=="SWT"):
        country_code_map = "SWZ"
    else:
        country_code_map = country_code
    country_map = world[world['iso_a3'].apply(lambda x: x == country_code_map)]

    if(len(country_map)==0):
        print("no match")
        print(country_code_map)

    if(len(country_map) == 1):
        # world.loc[world_index, 'needs_ratio'] = needs_ratio

        # cap at 100% fed, surplus is not traded away in this scenario
        kcals_ratio_capped = 1 if needs_ratio >= 1 else needs_ratio
        # fat_ratio_capped = 1 if fat_ratio >= 1 else fat_ratio
        # protein_ratio_capped = 1 if protein_ratio >= 1 else protein_ratio
        world_index = country_map.index
        world.loc[world_index, 'needs_ratio'] = kcals_ratio_capped

    # if('USA' in country_code):
    #     print("HERE")
    #     print(country_map)
    #     quit()

# for index, country_data in world.iterrows():
#     print(country_data)

#iterate over each country from spreadsheet, run the optimizer, plot the result
og_sum = 0
for index, country_data in no_trade_table.iterrows():
    country_code = country_data['iso3']
    country_name = country_data['country']

    print("")
    print(country_name)

    population = country_data['population']

    needs_ratio = run_optimizer_for_country(country_code, country_data)
    # og = run_optimizer_for_country(country_code, country_data)
    # og_sum += og
    # print(og)

    if(country_code=="F5707+GBR"):
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
ax = world.plot(column='needs_ratio', legend=True, cmap='viridis',
                legend_kwds = {
                    'label': 'Fraction Fed',
                    'orientation': "horizontal"
                }
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
plt.title('Fraction of minimum macronutritional needs with no trade')
# plt.savefig(Params.globalEfieldPlots+'Results'+str(r)+'perYearWindow'+str(windowperiod)+'s.png')
plt.show()
plt.close()
quit()
mn = 0
mx = 1
ax = world.plot(column='fat_frac_fed', legend=True, cmap='viridis', legend_kwds={
                'label': 'Fraction Fed', 'orientation': "horizontal"})
pp = gplt.polyplot(world, ax=ax, zorder=1, linewidth=0.1)
# Plotter.formatticklabels(mn,mx,pp)
# plt.rcParams['text.usetex'] = True
plt.title('Fraction of minimum fat needs with no trade')
# plt.savefig(Params.globalEfieldPlots+'Results'+str(r)+'perYearWindow'+str(windowperiod)+'s.png')
plt.show()
plt.close()

mn = 0
mx = 1
ax = world.plot(column='protein_frac_fed', legend=True, cmap='viridis',
                legend_kwds={'label': 'Fraction Fed', 'orientation': "horizontal"})
pp = gplt.polyplot(world, ax=ax, zorder=1, linewidth=0.1)
# Plotter.formatticklabels(mn,mx,pp)
# plt.rcParams['text.usetex'] = True
plt.title('Fraction of minimum protein needs with no trade')
# plt.savefig(Params.globalEfieldPlots+'Results'+str(r)+'perYearWindow'+str(windowperiod)+'s.png')
plt.show()

mn = 0
mx = 1
ax = world.plot(column='min_frac_fed', legend=True, cmap='viridis', legend_kwds={
                'label': 'Fraction Fed', 'orientation': "horizontal"})
pp = gplt.polyplot(world, ax=ax, zorder=1, linewidth=0.1)
# Plotter.formatticklabels(mn,mx,pp)
# plt.rcParams['text.usetex'] = True
plt.title('Smallest fraction of any macronutrient need with no trade')
# plt.savefig(Params.globalEfieldPlots+'Results'+str(r)+'perYearWindow'+str(windowperiod)+'s.png')
plt.show()

