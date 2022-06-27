import pandas as pd
import numpy as np
import os

HEAD_COUNT_CSV = '../../data/no_food_trade/FAOSTAT_animal_stocks_2020.csv'
DAIRY_HEAD_COUNT_CSV = '../../data/no_food_trade/FAOSTAT_cow_heads_2020.csv'

TONS_TO_KG = 1e3
KCALS_TO_DRY_CALORIC_TONS = 1/(4000*1000)

KCALS_PER_PERSON = 2100
FAT_PER_PERSON = 47
PROTEIN_PER_PERSON = 53 

countries = ["AFG","ALB","DZA","AGO","ARG","ARM","AUS","AZE","BHR","BGD","BRB","BLR","BEN","BTN","BOL","BIH","BWA","BRA","BRN","BFA","MMR","BDI","CPV","KHM","CMR","CAN","CAF","TCD","CHL","CHN","COL","COD","COG","CRI","CIV","CUB","DJI","DOM","ECU","EGY","SLV","ERI","SWZ","ETH","F5707","GBR","FJI","GAB","GMB","GEO","GHA","GTM","GIN","GNB","GUY","HTI","HND","IND","IDN","IRN","IRQ","ISR","JAM","JPN","JOR","KAZ","KEN","KOR","PRK","KWT","KGZ","LAO","LBN","LSO","LBR","LBY","MDG","MWI","MYS","MLI","MRT","MUS","MEX","MDA","MNG","MAR","MOZ","NAM","NPL","NZL","NIC","NER","NGA","MKD","NOR","OMN","PAK","PAN","PNG","PRY","PER","PHL","QAT","RUS","RWA","SAU","SEN","SRB","SLE","SGP","SOM","ZAF","SSD","LKA","SDN","SUR","CHE","SYR","TWN","TJK","TZA","THA","TGO","TTO","TUN","TUR","TKM","UGA","UKR","ARE","USA","URY","UZB","VEN","VNM","YEM","ZMB","ZWE"]

country_names = ["Afghanistan","Albania","Algeria","Angola","Argentina","Armenia","Australia","Azerbaijan","Bahrain","Bangladesh","Barbados","Belarus","Benin","Bhutan","Bolivia (Plurinational State of)","Bosnia and Herzegovina","Botswana","Brazil","Brunei Darussalam","Burkina Faso","Myanmar","Burundi","Cabo Verde","Cambodia","Cameroon","Canada","Central African Republic","Chad","Chile","China","Colombia","Congo","Democratic Republic of the Congo","Costa Rica","C?te d'Ivoire","Cuba","Djibouti","Dominican Republic","Ecuador","Egypt","El Salvador","Eritrea","Eswatini","Ethiopia","European Union (27) + UK","UK","Fiji","Gabon","Gambia","Georgia","Ghana","Guatemala","Guinea","Guinea-Bissau","Guyana","Haiti","Honduras","India","Indonesia","Iran (Islamic Republic of)","Iraq","Israel","Jamaica","Japan","Jordan","Kazakhstan","Kenya","Democratic People's Republic of Korea","Republic of Korea","Kuwait","Kyrgyzstan","Lao People's Democratic Republic","Lebanon","Lesotho","Liberia","Libya","Madagascar","Malawi","Malaysia","Mali","Mauritania","Mauritius","Mexico","Republic of Moldova","Mongolia","Morocco","Mozambique","Namibia","Nepal","New Zealand","Nicaragua","Niger","Nigeria","North Macedonia","Norway","Oman","Pakistan","Panama","Papua New Guinea","Paraguay","Peru","Philippines","Qatar","Russian Federation","Rwanda","Saudi Arabia","Senegal","Serbia","Sierra Leone","Singapore","Somalia","South Africa","South Sudan","Sri Lanka","Sudan","Suriname","Switzerland","Syrian Arab Republic","Taiwan","Tajikistan","United Republic of Tanzania","Thailand","Togo","Trinidad and Tobago","Tunisia","Turkiye","Turkmenistan","Uganda","Ukraine","United Arab Emirates","United States of America","Uruguay","Uzbekistan","Venezuela (Bolivarian Republic of)","Viet Nam","Yemen","Zambia","Zimbabwe"]

df_head_counts = pd.read_csv(HEAD_COUNT_CSV)[['Area Code (ISO3)',"Item",'Unit','Value']]
df_dairy_cow_counts = pd.read_csv(DAIRY_HEAD_COUNT_CSV)[['Area Code (ISO3)',"Item",'Unit','Value']]

merge_on = ['Area Code (ISO3)', 'Item Code (FAO)', 'Item', 'Unit']

# tacks on a column at the end with dairy cow for that country. 
# The same dairy cow count is made to be repeated on all the 
# rows of a given country in the left merge.
df_merge = df_head_counts.merge(df_dairy_cow_counts,
                                on='Area Code (ISO3)',
                                how='left')
# print("df_merge")
# print("df_dairy_cow_counts")
# print("df_head_counts")
# print(len(df_merge))
# print(len(df_dairy_cow_counts))
# print(len(df_head_counts))
# print(df_merge)
# print(df_merge.head())
# print(df_merge.iloc[0])
# quit()
countries_unique = list(df_merge['Area Code (ISO3)'].unique())
# create dictionary containing each table, remove Area column
df_dict = {k: df_merge[df_merge['Area Code (ISO3)'] == k].drop(columns='Area Code (ISO3)') for k in countries_unique}

#for each country create a list of macronutrient values
macros_csv=np.array(["ISO3 Country Code","Country","Outdoor crop caloric production in 2020 (dry caloric tons)",
    "Outdoor crop fat production in 2020 (tonnes)",
    "Outdoor crop protein production in 2020 (tonnes)"])

large_animals = ["Asses","Buffaloes","Camels","Cattle","Horses","Mules"]

medium_animals = ["Goats","Pigs","Sheep"]

small_animals = ["Chickens","Ducks","Geese and guinea fowls",\
                  "Rabbits and hares","Rodents, other","Turkeys"]

small_animal_sum_global = 0
medium_animal_sum_global = 0
large_animal_sum_global = 0
dairy_cow_count_global = 0
for i in range(0,len(countries)):
    country = countries[i]
    country_name = country_names[i]
    if(country not in df_dict.keys()):
        print("missing" + country)
        continue

    head_counts = df_dict[country]
    small_animal_sum = 0
    medium_animal_sum = 0
    large_animal_sum = 0
    #for each food product, add to each macronutrient total
    for index, head_count in df_merge.iterrows(): 
        # print(head_count)
        # print(type(head_count['Value']))
        if("1000" in head_count['Unit_x']):
            multiplier = 1000
        else:
            multiplier = 1

        if(np.isnan(head_count["Value_x"])):
            continue
        if(head_count['Item_x'] in small_animals):
            small_animal_sum += multiplier*int(head_count["Value_x"])
            small_animal_sum_global += multiplier*int(head_count["Value_x"])

        if(head_count['Item_x'] in medium_animals):
            medium_animal_sum += multiplier*int(head_count["Value_x"])
            medium_animal_sum_global += multiplier*int(head_count["Value_x"])

        if(head_count['Item_x'] in large_animals):
            large_animal_sum += multiplier*int(head_count["Value_x"])
            large_animal_sum_global += multiplier*int(head_count["Value_x"])

    if(np.isnan(head_counts.iloc[0]["Value_y"])):
        dairy_cow_count = 0
    else:
        dairy_cow_count = head_counts.iloc[0]["Value_y"]
        dairy_cow_count_global += head_counts.iloc[0]["Value_y"]
print("dairy_cow_count_global")
print(dairy_cow_count_global/1e9)
print("small_animal_sum_global")
print(small_animal_sum_global/1e9)
print("medium_animal_sum_global")
print(medium_animal_sum_global/1e9)
print("large_animal_sum_global")
print(large_animal_sum_global/1e9)
quit()

    # pulp_country = pulp_countries[i]
    # country_name = country_names[i]
    # if(pulp_country not in list(df_pulp_countries["Area Code (ISO3)"])):
    #     print("missing " + country_name)
    #     pulp = 0
    # else:
    #     pulp = float(df_pulp_countries[df_pulp_countries["Area Code (ISO3)"] == pulp_country]["Value"])
    #     # print(pulp)
    # pulp_csv = np.vstack([pulp_csv,[pulp_country,country_name,pulp]])


#add up GBR and F5707 (EU+27) to incorporate GBR (which is the UK),
# and delete GBR

F5707_index = np.where(pulp_csv[:,0] == "F5707")
GBR_index = np.where(pulp_csv[:,0] == "GBR")
F5707_name = pulp_csv[F5707_index][0][1]
F5707_tons = float(pulp_csv[F5707_index][0][2])

GBR_name = pulp_csv[GBR_index][0][1]
GBR_tons = float(pulp_csv[GBR_index][0][2])


pulp_csv[F5707_index,0] = "F5707+GBR" 
pulp_csv[F5707_index,2] = str(F5707_tons+GBR_tons)


swaziland_index = np.where(pulp_csv[:,0]=="SWZ")
# eswatini recently changed from swaziland 
pulp_csv[swaziland_index,0] = "SWT" 
pulp_csv = np.delete(pulp_csv,(GBR_index),axis=0)


print("pulp_csv")
print(pulp_csv)
np.savetxt('../../data/no_food_trade/pulp_csv.csv',pulp_csv,delimiter=",",fmt='%s')
