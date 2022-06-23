import pandas as pd
import numpy as np
import requests
import json
import os
import matplotlib.pyplot as plt
import matplotlib.colors as colors

import geopandas as gpd
import geoplot as gplt
import copy 

NUTRITION_XLS = '../../Supplemental_Data.xlsx'
PRODUCTION_CSV = '../../data/no_food_trade/FAOSTAT_food_production_2020.csv'
POP_CSV = '../../data/no_food_trade/FAOSTAT_population_2020.csv'

TONS_TO_KG = 1e3
TONS_TO_GRAMS = 1e6

KCALS_PER_PERSON = 2100
FAT_PER_PERSON = 47
PROTEIN_PER_PERSON = 53 

# Data Inspection

xls = pd.ExcelFile(NUTRITION_XLS)
nutrition = pd.read_excel(xls, 'Nutrition')[['Item','Calories','Protein','Fat']]

df_pop = pd.read_csv(POP_CSV)[['Area Code (ISO3)', 'Value']]
df_pop['Population'] = df_pop['Value'] * 1000
df_pop.drop(columns='Value', inplace=True)

df_prod = pd.read_csv(PRODUCTION_CSV)[['Area Code (ISO3)', 'Area', 'Element', 'Item Code (FAO)', 'Item', 'Unit', 'Value']]
            #.rename(columns={'Value': 'Production Value'})

# split table by country ('Area')
print(df_prod)
countries = list(df_prod['Area Code (ISO3)'].unique())
# create dictionary containing each table, remove Area column
df_dict = {k: df_prod[df_prod['Area Code (ISO3)'] == k].drop(columns='Area Code (ISO3)') for k in countries}

sum_pop = 0
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
for country, products in df_dict.items(): 
    kcals_sum = 0
    fat_sum = 0
    protein_sum = 0
    for index, product in products.iterrows(): 
        #find the particular item.
        n = nutrition[nutrition['Item'] == product['Item']]

        #if the match could not be found, continue
        if(len(n)==0):
            # print("and... another.")
            continue

        # there should never be any duplicate nutrition items
        assert(len(n)==1)


        kcals_nut = float(n['Calories'])
        fat_nut = float(n['Fat'])
        protein_nut = float(n['Protein'])

        # nutrition Calories is units kcals/kg
        if(np.isnan(product['Value'])):
            tons = 0
        else:
            tons = product['Value']

        kcals = tons / 365 * TONS_TO_KG * kcals_nut 

        # nutrition Fat and protein are percent by weight, converting to grams
        fat = tons / 365 * TONS_TO_GRAMS * fat_nut
        protein = tons / 365 * TONS_TO_GRAMS * protein_nut

        kcals_sum += kcals
        fat_sum += fat
        protein_sum += protein


    # population = world[world['iso_a3'].apply(lambda x: x == country)]
    country_row = world[world['iso_a3'].apply(lambda x: x == country)]
    # print(country_row)
    # if(len(country_row)==0):
    #     print("no match")
    #     print(country)
    # if(len(country_row)>1):
    #     print("")
    #     print("many matches")
    #     print(country)
    #     print(country_row)
    #     print("")
    if(len(country_row)==1):
        population = float(df_pop['Population'][df_pop['Area Code (ISO3)'] == country].iloc[0])
        sum_pop += population

        #this population is too annoying to work with, it double counts china, for example.
        kcals_ratio = float(kcals_sum) / (float(population) * float(KCALS_PER_PERSON))
        fat_ratio = float(fat_sum) / (float(population) * float(FAT_PER_PERSON))
        protein_ratio = float(protein_sum) / (float(population) * float(PROTEIN_PER_PERSON))

        # cap at 100% fed, surplus is not traded away in this scenario
        kcals_ratio_capped = 1 if kcals_ratio >= 1 else kcals_ratio
        fat_ratio_capped = 1 if fat_ratio >= 1 else fat_ratio
        protein_ratio_capped = 1 if protein_ratio >= 1 else protein_ratio
        world_index = country_row.index
        if(kcals_ratio_capped < 1):
            world.loc[world_index,'kcals_frac_fed'] =  kcals_ratio_capped
        if(fat_ratio_capped < 1):
            world.loc[world_index,'fat_frac_fed'] =  fat_ratio_capped
        if(protein_ratio_capped < 1):
            world.loc[world_index,'protein_frac_fed'] =  protein_ratio_capped

        net_min = min([ kcals_ratio_capped,
             fat_ratio_capped,
             protein_ratio_capped])

        if(net_min < 1):
            world.loc[world_index,'min_frac_fed'] = net_min

# world[world['kcals_frac_fed']==0] = np.nan
# world[world['fat_frac_fed']==0] = np.nan
# world[world['protein_frac_fed']==0] = np.nan
# world[world['max_frac_fed']==0] = np.nan
# print(world['max_frac_fed'])
plt.close()
mn = 0
mx = 1
ax = world.plot(column='kcals_frac_fed',legend=True,cmap='viridis',
    legend_kwds={'label': 'Fraction Fed','orientation': "horizontal"}
    # missing_kwds={
    #             "color": "lightgrey",
    #             "edgecolor": "red",
    #             "hatch": "///",
    #             "label": "Missing values",
    # }
)

pp=gplt.polyplot(world,ax=ax,zorder=1,linewidth=0.1)
# Plotter.formatticklabels(mn,mx,pp)
# plt.rcParams['text.usetex'] = True
plt.title('Fraction of minimum caloric needs with no trade')            
# plt.savefig(Params.globalEfieldPlots+'Results'+str(r)+'perYearWindow'+str(windowperiod)+'s.png')
plt.show()
plt.close()

mn = 0
mx = 1
ax=world.plot(column='fat_frac_fed',legend=True,cmap='viridis',legend_kwds={'label': 'Fraction Fed','orientation': "horizontal"})
pp=gplt.polyplot(world,ax=ax,zorder=1,linewidth=0.1)
# Plotter.formatticklabels(mn,mx,pp)
# plt.rcParams['text.usetex'] = True
plt.title('Fraction of minimum fat needs with no trade')            
# plt.savefig(Params.globalEfieldPlots+'Results'+str(r)+'perYearWindow'+str(windowperiod)+'s.png')
plt.show()
plt.close()

mn = 0
mx = 1
ax=world.plot(column='protein_frac_fed',legend=True,cmap='viridis',legend_kwds={'label': 'Fraction Fed','orientation': "horizontal"})
pp=gplt.polyplot(world,ax=ax,zorder=1,linewidth=0.1)
# Plotter.formatticklabels(mn,mx,pp)
# plt.rcParams['text.usetex'] = True
plt.title('Fraction of minimum protein needs with no trade')            
# plt.savefig(Params.globalEfieldPlots+'Results'+str(r)+'perYearWindow'+str(windowperiod)+'s.png')
plt.show()

mn = 0
mx = 1
ax=world.plot(column='min_frac_fed',legend=True,cmap='viridis',legend_kwds={'label': 'Fraction Fed','orientation': "horizontal"})
pp=gplt.polyplot(world,ax=ax,zorder=1,linewidth=0.1)
# Plotter.formatticklabels(mn,mx,pp)
# plt.rcParams['text.usetex'] = True
plt.title('Smallest fraction of any macronutrient need with no trade')            
# plt.savefig(Params.globalEfieldPlots+'Results'+str(r)+'perYearWindow'+str(windowperiod)+'s.png')
plt.show()

print("sum_pop")
print(sum_pop)