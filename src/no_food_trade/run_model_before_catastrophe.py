import os
import sys
import numpy as np
module_path = os.path.abspath(os.path.join('../..'))
if module_path not in sys.path:
    sys.path.append(module_path)
from src.optimizer import Optimizer
from src.plotter import Plotter
from src.constants import Constants
import pandas as pd

constants_loader = Constants()
optimizer = Optimizer()

constants = constants_loader.get_before_catastrophe_scenario()

(single_valued_constants, multi_valued_constants) = \
    constants_loader.computeConstants(constants)

NO_TRADE_XLS = '../../data/no_food_trade/No_Food_Trade_Data.xlsx'

# Data Inspection

xls = pd.ExcelFile(NO_TRADE_XLS)

fish = pd.read_excel(xls, 'Seafood - excluding seaweeds')[['ISO3 Country Code',"Seafood calories - million tonnes dry caloric, 2020","Seafood fat - million tonnes, 2020","Seafood protein - million tonnes, 2020"]]
crops = pd.read_excel(xls, 'Outdoor Crop Production Baseline')[['ISO3 Country Code',"Outdoor crop caloric production in 2020 (dry caloric tons)","Outdoor crop fat production in 2020 (tonnes)","Outdoor crop protein production in 2020 (tonnes)"]]
dairy = pd.read_excel(xls, 'Grazing')[['ISO3 Country Code',"Current milk output - '000 tonnes wet value'"]]

# merge fish, crops, dairy, and, meat into a single pandas spreadsheet