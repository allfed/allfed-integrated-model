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

NO_TRADE_XLS = '../../data/no_food_trade/No_Food_Trade_Data.xlsx'

# Data Inspection

xls = pd.ExcelFile(NO_TRADE_XLS)
aquaculture = pd.read_excel(xls, 'Seafood - excluding seaweeds')[['ISO3 Country Code',"Seafood calories - million tonnes dry caloric, 2020","Seafood fat - million tonnes, 2020","Seafood protein - million tonnes, 2020"]]
grasses = pd.read_excel(xls, 'Outdoor Crop Production Baseline')[['ISO3 Country Code',"Outdoor crop caloric production in 2020 (dry caloric tons)","Outdoor crop fat production in 2020 (tonnes)","Outdoor crop protein production in 2020 (tonnes)"]]
dairy = pd.read_excel(xls, 'Grazing')[['ISO3 Country Code',"Current milk output - '000 tonnes wet value'"]]
population = pd.read_excel(xls, 'Macro data')[['ISO3 Country Code',"Country Population (millions), 2020"]]

df_pop['Population'] = population["Country Population (millions), 2020"] * 1e6
df_pop.drop(columns="Country Population (millions), 2020", inplace=True)

df_prod = pd.read_csv(PRODUCTION_CSV)[['Area Code (ISO3)', 'Area', 'Element', 'Item Code (FAO)', 'Item', 'Unit', 'Value']]
            #.rename(columns={'Value': 'Production Value'})

# split table by country ('Area')
print(df_prod)
countries = list(df_prod['Area Code (ISO3)'].unique())
# create dictionary containing each table, remove Area column
df_dict = {k: df_prod[df_prod['Area Code (ISO3)'] == k].drop(columns='Area Code (ISO3)') for k in countries}

sum_pop = 0
#import the visual map
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
#for each 
for country, products in df_dict.items(): 
    kcals_sum = 0
    fat_sum = 0
    protein_sum = 0


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