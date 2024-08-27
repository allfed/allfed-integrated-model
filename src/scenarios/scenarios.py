"""
Scenarios.py: Provides numbers and methods to set the specific scenario to be optimized.
Also makes sure values are never set twice.
"""

import git
import numpy as np
import pandas as pd
import pytest

repo_root = git.Repo(".", search_parent_directories=True).working_dir


class Scenarios:
    def __init__(self):
        # used to ensure the properties of scenarios are set twice or left unset
        self.NONHUMAN_CONSUMPTION_SET = False
        self.WASTE_SET = False
        self.INTAKE_CONSTRAINTS_SET = False
        self.NUTRITION_PROFILE_SET = False
        self.STORED_FOOD_SET = False
        self.STORED_FOOD_END_SIM_SET = False
        self.SCALE_SET = False
        self.SEASONALITY_SET = False
        self.GRASSES_SET = False
        self.FISH_SET = False
        self.DISRUPTION_SET = False
        self.GENERIC_INITIALIZED_SET = False
        self.SCENARIO_SET = False
        self.PROTEIN_SET = False
        self.FAT_SET = False
        self.CULLING_PARAM_SET = False
        self.MEAT_STRATEGY_SET = False
        self.EXPANDED_AREA_SET = False

        # convenient to understand what scenario is being run exactly
        self.scenario_description = "Scenario properties:\n"

    def check_all_set(self):
        """
        Ensure all properties of scenarios have been set
        """
        assert self.NONHUMAN_CONSUMPTION_SET
        assert self.WASTE_SET
        assert self.INTAKE_CONSTRAINTS_SET
        assert self.NUTRITION_PROFILE_SET
        assert self.STORED_FOOD_SET
        assert self.STORED_FOOD_END_SIM_SET
        assert self.SCALE_SET
        assert self.SEASONALITY_SET
        assert self.GRASSES_SET
        assert self.GENERIC_INITIALIZED_SET
        assert self.FISH_SET
        assert self.DISRUPTION_SET
        assert self.SCENARIO_SET
        assert self.PROTEIN_SET
        assert self.FAT_SET
        assert self.CULLING_PARAM_SET
        assert self.MEAT_STRATEGY_SET
        assert self.EXPANDED_AREA_SET

    # INITIALIZATION

    def init_generic_scenario(self):
        assert not self.GENERIC_INITIALIZED_SET
        constants_for_params = {}

        # the following are used for all scenarios
        constants_for_params["GLOBAL_POP"] = 7.723713182e9  # (about 7.8 billion 2020)

        # GLOBAL CROP AREA
        # UNITS: hectares
        # NOTE: This has been changed to 1.43 billion hectares to match the sum of column "C"
        # "Country Crop Area ('000 Hectares)" column in "Greenhouses" tab
        # in "Integrated Model No Food Trade" Spreadsheet
        constants_for_params["INITIAL_GLOBAL_CROP_AREA"] = 1.43e9

        constants_for_params["DELAY"] = {}

        # The duration from planting to harvest of crops -- this is used to calculate the additional delay before the
        # implementation of relocated crops has an effect on improving yields.
        constants_for_params["INITIAL_HARVEST_DURATION_IN_MONTHS"] = 8

        # This will be added to the initial harvest duration above to further delay relocated crops,
        # it represents how slow people are to realize they need to start planting different crops
        # (note, it's assumed to be a uniform global number)
        constants_for_params["DELAY"]["ROTATION_CHANGE_IN_MONTHS"] = 2

        constants_for_params["ADD_FISH"] = True

        self.GENERIC_INITIALIZED_SET = True
        return constants_for_params

    def init_global_food_system_properties(self):
        self.scenario_description += "\ncontinued trade"
        assert not self.SCALE_SET
        self.IS_GLOBAL_ANALYSIS = True

        constants_for_params = self.init_generic_scenario()

        # global human population (2020)
        constants_for_params["POP"] = 7723713182  # (about 7.8 billion)

        # annual tons dry caloric equivalent
        constants_for_params["BASELINE_CROP_KCALS"] = 3898e6

        # annual tons fat
        constants_for_params["BASELINE_CROP_FAT"] = 322e6

        # annual tons protein
        constants_for_params["BASELINE_CROP_PROTEIN"] = 350e6

        # annual tons dry caloric equivalent
        constants_for_params["BIOFUEL_KCALS"] = 623e6

        # annual tons fat
        constants_for_params["BIOFUEL_FAT"] = 124e6

        # annual tons protein
        constants_for_params["BIOFUEL_PROTEIN"] = 32e6

        # annual tons dry caloric equivalent
        constants_for_params["FEED_KCALS"] = 1447.96e6

        # annual tons fat
        constants_for_params["FEED_FAT"] = 60e6

        # annual tons protein
        constants_for_params["FEED_PROTEIN"] = 147e6

        # tons dry caloric monthly
        constants_for_params["HUMAN_INEDIBLE_FEED_BASELINE_MONTHLY"] = 4206 * 1e6 / 12

        # total stocks at the end of the month in dry caloric tons
        # this is total stored food available
        # if all of it were used for the whole earth, including private stocks
        # but not including a 2 month in-transit or the estimated 2 weeks to 1
        # month of stocks in people's homes, grocery stores, and food
        # warehouses
        constants_for_params["END_OF_MONTH_STOCKS"] = {}
        constants_for_params["END_OF_MONTH_STOCKS"]["JAN"] = 1960.922e6 * 1.015
        constants_for_params["END_OF_MONTH_STOCKS"]["FEB"] = 1784.277e6 * 1.015
        constants_for_params["END_OF_MONTH_STOCKS"]["MAR"] = 1624.673e6 * 1.015
        constants_for_params["END_OF_MONTH_STOCKS"]["APR"] = 1492.822e6 * 1.015
        constants_for_params["END_OF_MONTH_STOCKS"]["MAY"] = 1359.236e6 * 1.015
        constants_for_params["END_OF_MONTH_STOCKS"]["JUN"] = 1245.351e6 * 1.015
        constants_for_params["END_OF_MONTH_STOCKS"]["JUL"] = 1246.485e6 * 1.015
        constants_for_params["END_OF_MONTH_STOCKS"]["AUG"] = 1140.824e6 * 1.015
        constants_for_params["END_OF_MONTH_STOCKS"]["SEP"] = 1196.499e6 * 1.015
        constants_for_params["END_OF_MONTH_STOCKS"]["OCT"] = 1487.030e6 * 1.015
        constants_for_params["END_OF_MONTH_STOCKS"]["NOV"] = 1642.406e6 * 1.015
        constants_for_params["END_OF_MONTH_STOCKS"]["DEC"] = 1813.862e6 * 1.015

        constants_for_params["SEAWEED_GROWTH_PER_DAY"] = {}
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["-3"] = 3.280243527
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["-2"] = 3.334115726
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["-1"] = 3.050423835
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["0"] = 2.835455997
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["1"] = 2.847631746
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["2"] = 3.938247088
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["3"] = 4.461998946
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["4"] = 4.407004285
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["5"] = 4.14288022
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["6"] = 4.019320807
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["7"] = 4.029817721
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["8"] = 3.811881724
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["9"] = 3.499376903
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["10"] = 3.698330595
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["11"] = 3.948105122
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["12"] = 4.1984675
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["13"] = 4.556431237
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["14"] = 4.483116708
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["15"] = 4.307000533
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["16"] = 4.293354108
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["17"] = 4.336405342
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["18"] = 4.124423307
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["19"] = 3.957399801
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["20"] = 3.574110614
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["21"] = 3.562394509
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["22"] = 3.454517899
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["23"] = 3.388982778
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["24"] = 3.450605774
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["25"] = 3.555228229
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["26"] = 3.658816146
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["27"] = 3.424530139
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["28"] = 3.253434988
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["29"] = 3.16820901
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["30"] = 3.144307864
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["31"] = 2.979931609
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["32"] = 3.029277798
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["33"] = 2.871550986
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["34"] = 2.874292984
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["35"] = 2.857490207
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["36"] = 2.855354313
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["37"] = 2.919643632
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["38"] = 3.000525927
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["39"] = 2.919633402
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["40"] = 2.776043444
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["41"] = 2.666282281
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["42"] = 2.583101843
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["43"] = 2.587772481
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["44"] = 2.674921678
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["45"] = 2.764051458
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["46"] = 2.787946778
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["47"] = 2.632984698
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["48"] = 2.358758332
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["49"] = 2.374585305
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["50"] = 2.390295172
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["51"] = 2.387672944
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["52"] = 2.375940434
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["53"] = 2.217004652
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["54"] = 2.145805788
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["55"] = 2.275670886
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["56"] = 2.586299912
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["57"] = 2.689122514
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["58"] = 2.721252781
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["59"] = 2.446378696
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["60"] = 2.153283049
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["61"] = 2.068362713
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["62"] = 2.227272558
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["63"] = 2.319325173
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["64"] = 2.277612993
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["65"] = 2.145133611
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["66"] = 2.05723362
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["67"] = 2.134569407
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["68"] = 2.296677102
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["69"] = 2.652624183
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["70"] = 2.620792141
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["71"] = 2.268458649
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["72"] = 1.862008627
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["73"] = 1.810996449
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["74"] = 2.003809275
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["75"] = 2.352443263
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["76"] = 2.393824763
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["77"] = 2.228708866
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["78"] = 2.117241208
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["79"] = 2.162013353
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["80"] = 2.449212699
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["81"] = 2.707294052
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["82"] = 2.554753816
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["83"] = 2.221274477
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["84"] = 1.929712462
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["85"] = 1.949992597
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["86"] = 2.328284543
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["87"] = 2.682473164
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["88"] = 2.692043127
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["89"] = 2.572977352
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["90"] = 2.524121111
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["91"] = 2.609014029
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["92"] = 2.858934229
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["93"] = 3.056473003
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["94"] = 2.886739232
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["95"] = 2.640633131
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["96"] = 2.596517279
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["97"] = 2.510737035
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["98"] = 2.818730288
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["99"] = 3.13238984
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["100"] = 3.128839607
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["101"] = 3.047094477
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["102"] = 2.965525323
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["103"] = 3.085088736
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["104"] = 3.347156394
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["105"] = 3.647367664
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["106"] = 3.613382371
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["107"] = 3.205683527
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["108"] = 2.914326235
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["109"] = 2.80454008
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["110"] = 3.077436259
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["111"] = 3.581070259
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["112"] = 3.844646941
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["113"] = 3.621240321
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["114"] = 3.34933192
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["115"] = 3.350107884
        constants_for_params["SEAWEED_GROWTH_PER_DAY"]["116"] = 3.65722728

        # total head count of milk cattle
        constants_for_params["INITIAL_MILK_CATTLE"] = 264e6

        # total head count of small sized animals
        constants_for_params["INIT_SMALL_ANIMALS"] = 28.2e9

        # total head count of medium sized animals
        constants_for_params["INIT_MEDIUM_ANIMALS"] = 3.2e9

        # total head count of large sized animals minus milk cows
        constants_for_params["INIT_LARGE_ANIMALS_WITH_MILK_COWS"] = 1.9e9

        # converting from kcals to dry caloric tons:
        # 4e6 kcals = 1 dry caloric ton
        constants_for_params["FISH_DRY_CALORIC_ANNUAL"] = 27.5e6
        constants_for_params["FISH_FAT_TONS_ANNUAL"] = 4e6
        constants_for_params["FISH_PROTEIN_TONS_ANNUAL"] = 17e6

        # annual tons milk production
        constants_for_params["TONS_MILK_ANNUAL"] = 879e6

        # annual tons chicken and pork production
        constants_for_params["TONS_CHICKEN_AND_PORK_ANNUAL"] = 250e6

        # annual tons cattle beef production
        constants_for_params["TONS_BEEF_ANNUAL"] = 74.2e6

        # Single cell protein fraction of global production
        constants_for_params["SCP_GLOBAL_PRODUCTION_FRACTION"] = 1

        # Cellulosic sugar fraction of global production
        constants_for_params["CS_GLOBAL_PRODUCTION_FRACTION"] = 1

        # seaweed params
        constants_for_params["SEAWEED_NEW_AREA_FRACTION"] = 1
        constants_for_params["SEAWEED_MAX_AREA_FRACTION"] = 1
        constants_for_params["ROTATION_IMPROVEMENTS"] = {}
        constants_for_params["ROTATION_IMPROVEMENTS"][
            "POWER_LAW_IMPROVEMENT"
        ] = 0.796  # default for global model

        constants_for_params["INITIAL_SEAWEED_FRACTION"] = 1
        constants_for_params["INITIAL_BUILT_SEAWEED_FRACTION"] = 1

        # fraction global crop area for entire earth is 1 by definition
        constants_for_params["INITIAL_CROP_AREA_FRACTION"] = 1

        # Milk yield in kg per milk-bearing animal per year
        constants_for_params["MILK_YIELD_KG_PER_MILK_BEARING_ANIMAL_PER_YEAR"] = 1099.60

        # Meat yield in kg per animal per year
        constants_for_params["KG_MEAT_PER_PIG"] = 86.0
        constants_for_params["KG_MEAT_PER_CHICKEN"] = 1.65

        constants_for_params["COUNTRY_CODE"] = "WOR"

        self.SCALE_SET = True
        return constants_for_params

    def init_country_food_system_properties(self, country_data):
        self.scenario_description += "\nno food trade"
        assert not self.SCALE_SET
        self.IS_GLOBAL_ANALYSIS = False

        constants_for_params = self.init_generic_scenario()
        # global human population (2020)
        constants_for_params["POP"] = country_data["population"]

        # This should only be enabled if we're trying to reproduce the method of Xia
        # et al. (2020), they subtract feed directly from production and ignore stored
        # food usage of crops
        # It also only makes sense to enable this if we're not including fat and protein
        SUBTRACT_FEED_DIRECTLY = False

        if SUBTRACT_FEED_DIRECTLY:
            # annual tons dry caloric equivalent
            constants_for_params["BASELINE_CROP_KCALS"] = (
                country_data["crop_kcals"] - country_data["feed_kcals"]
            )

            if constants_for_params["BASELINE_CROP_KCALS"] < 0:
                constants_for_params["BASELINE_CROP_KCALS"] = 0.01
                print("WARNING: Crop production - Feed is set to close to zero!")

        else:
            # annual tons dry caloric equivalent
            constants_for_params["BASELINE_CROP_KCALS"] = country_data["crop_kcals"]

        # annual tons fat
        constants_for_params["BASELINE_CROP_FAT"] = country_data["crop_fat"]

        # annual tons protein
        constants_for_params["BASELINE_CROP_PROTEIN"] = country_data["crop_protein"]

        # annual tons dry caloric equivalent
        constants_for_params["BIOFUEL_KCALS"] = country_data["biofuel_kcals"]

        # annual tons fat
        constants_for_params["BIOFUEL_FAT"] = country_data["biofuel_fat"]

        # annual tons protein
        constants_for_params["BIOFUEL_PROTEIN"] = country_data["biofuel_protein"]

        # annual tons dry caloric equivalent
        constants_for_params["FEED_KCALS"] = country_data["feed_kcals"]

        # annual tons fat
        constants_for_params["FEED_FAT"] = country_data["feed_fat"]

        # annual tons protein
        constants_for_params["FEED_PROTEIN"] = country_data["feed_protein"]

        # tons dry caloric monthly
        constants_for_params["HUMAN_INEDIBLE_FEED_BASELINE_MONTHLY"] = (
            country_data["grasses_baseline"] / 12
        )

        # total head count of milk cattle
        constants_for_params["INITIAL_MILK_CATTLE"] = country_data["dairy_cows"]

        # total head count of small sized animals
        constants_for_params["INIT_SMALL_ANIMALS"] = country_data["small_animals"]

        # these won't be used unless the foods are added to the scenario

        # Single cell protein fraction of global production
        constants_for_params["SCP_GLOBAL_PRODUCTION_FRACTION"] = country_data[
            "percent_of_global_capex"
        ]

        # Cellulosic sugar fraction of global production
        constants_for_params["CS_GLOBAL_PRODUCTION_FRACTION"] = country_data[
            "percent_of_global_production"
        ]
        assert 1 >= constants_for_params["CS_GLOBAL_PRODUCTION_FRACTION"] >= 0
        assert 1 >= country_data["initial_seaweed_fraction"] >= 0
        assert 1 >= country_data["new_area_fraction"] >= 0
        assert 1 >= country_data["max_area_fraction"] >= 0
        assert 1 >= country_data["max_area_fraction"] >= 0
        assert 1 >= country_data["initial_built_fraction"] >= 0
        assert 1 >= constants_for_params["SCP_GLOBAL_PRODUCTION_FRACTION"] >= 0

        # https://stackoverflow.com/questions/17106819/accessing-python-dict-values-with-the-key-start-characters
        # all_seaweed_cols = [
        #     v for k, v in country_data.items() if "seaweed_growth_" in k
        # ]
        all_seaweed_col_names = [
            k for k, v in country_data.items() if "seaweed_growth_per_day_" in k
        ]

        constants_for_params["SEAWEED_GROWTH_PER_DAY"] = {}
        for i in range(len(all_seaweed_col_names)):
            # just have the number as a string as the keys for the dictionary
            constants_for_params["SEAWEED_GROWTH_PER_DAY"][
                all_seaweed_col_names[i].replace("seaweed_growth_per_day_", "")
            ] = country_data[all_seaweed_col_names[i]]

        if country_data["initial_seaweed_fraction"] == 0:
            constants_for_params["ADD_SEAWEED"] = False

        # 1000s of tons wet
        constants_for_params["INITIAL_SEAWEED_FRACTION"] = country_data[
            "initial_seaweed_fraction"
        ]

        constants_for_params["SEAWEED_NEW_AREA_FRACTION"] = country_data[
            "new_area_fraction"
        ]
        constants_for_params["SEAWEED_MAX_AREA_FRACTION"] = country_data[
            "max_area_fraction"
        ]

        constants_for_params["POWER_LAW_IMPROVEMENT"] = country_data[
            "power_law_improvement"
        ]

        # 1000s of hectares
        constants_for_params["INITIAL_BUILT_SEAWEED_FRACTION"] = country_data[
            "initial_built_fraction"
        ]
        constants_for_params["INITIAL_CROP_AREA_FRACTION"] = country_data[
            "fraction_crop_area"
        ]
        constants_for_params["INITIAL_CROP_AREA_HA"] = (
            np.array(country_data["crop_area_1000ha"]) * 1000
        )

        # total head count of medium sized animals
        constants_for_params["INIT_MEDIUM_ANIMALS"] = country_data["medium_animals"]

        # total head count of large sized animals minus milk cows
        constants_for_params["INIT_LARGE_ANIMALS_WITH_MILK_COWS"] = country_data[
            "large_animals"
        ]

        # fish kcals per month, billions
        constants_for_params["FISH_DRY_CALORIC_ANNUAL"] = country_data["aq_kcals"]

        # units of 1000s tons fat
        # (so, global value is in the tens of thousands of tons)
        constants_for_params["FISH_FAT_TONS_ANNUAL"] = country_data["aq_fat"]

        # units of 1000s tons protein monthly
        # (so, global value is in the hundreds of thousands of tons)
        constants_for_params["FISH_PROTEIN_TONS_ANNUAL"] = country_data["aq_protein"]

        # annual tons milk production
        constants_for_params["TONS_MILK_ANNUAL"] = country_data["dairy"]

        # annual tons chicken and pork production
        constants_for_params["TONS_CHICKEN_AND_PORK_ANNUAL"] = (
            country_data["chicken"] + country_data["pork"]
        )

        constants_for_params["ROTATION_IMPROVEMENTS"] = {}
        constants_for_params["ROTATION_IMPROVEMENTS"]["POWER_LAW_IMPROVEMENT"] = (
            country_data["power_law_improvement"]
        )

        # annual tons cattle beef production
        constants_for_params["TONS_BEEF_ANNUAL"] = country_data["beef"]

        constants_for_params["END_OF_MONTH_STOCKS"] = {}
        constants_for_params["END_OF_MONTH_STOCKS"]["JAN"] = country_data[
            "stocks_kcals_jan"
        ]
        constants_for_params["END_OF_MONTH_STOCKS"]["FEB"] = country_data[
            "stocks_kcals_feb"
        ]
        constants_for_params["END_OF_MONTH_STOCKS"]["MAR"] = country_data[
            "stocks_kcals_mar"
        ]
        constants_for_params["END_OF_MONTH_STOCKS"]["APR"] = country_data[
            "stocks_kcals_apr"
        ]
        constants_for_params["END_OF_MONTH_STOCKS"]["MAY"] = country_data[
            "stocks_kcals_may"
        ]
        constants_for_params["END_OF_MONTH_STOCKS"]["JUN"] = country_data[
            "stocks_kcals_jun"
        ]
        constants_for_params["END_OF_MONTH_STOCKS"]["JUL"] = country_data[
            "stocks_kcals_jul"
        ]
        constants_for_params["END_OF_MONTH_STOCKS"]["AUG"] = country_data[
            "stocks_kcals_aug"
        ]
        constants_for_params["END_OF_MONTH_STOCKS"]["SEP"] = country_data[
            "stocks_kcals_sep"
        ]
        constants_for_params["END_OF_MONTH_STOCKS"]["OCT"] = country_data[
            "stocks_kcals_oct"
        ]
        constants_for_params["END_OF_MONTH_STOCKS"]["NOV"] = country_data[
            "stocks_kcals_nov"
        ]
        constants_for_params["END_OF_MONTH_STOCKS"]["DEC"] = country_data[
            "stocks_kcals_dec"
        ]

        # Milk yield in kg per milk-bearing animal per year
        constants_for_params["MILK_YIELD_KG_PER_MILK_BEARING_ANIMAL_PER_YEAR"] = (
            country_data["milk_yield_kg_per_milk_bearing_animal_per_year"]
        )

        # Meat yield in kg per animal
        constants_for_params["KG_MEAT_PER_PIG"] = country_data["kg_meat_per_pig"]
        constants_for_params["KG_MEAT_PER_CHICKEN"] = country_data[
            "kg_meat_per_chicken"
        ]

        self.SCALE_SET = True
        return constants_for_params

    # FEED AND BIOFUELS

    def set_immediate_shutoff(self, constants_for_params):
        self.scenario_description += "\nno feed/biofuel"
        assert not self.NONHUMAN_CONSUMPTION_SET
        constants_for_params["DELAY"]["FEED_SHUTOFF_MONTHS"] = 0
        constants_for_params["DELAY"]["BIOFUEL_SHUTOFF_MONTHS"] = 0
        constants_for_params[
            "MINIMUM_PERCENT_FED_BEFORE_NONHUMAN_CONSUMPTION_ALLOWED"
        ] = 100
        self.NONHUMAN_CONSUMPTION_SET = True
        return constants_for_params

    def set_one_month_delayed_shutoff(self, constants_for_params):
        self.scenario_description += "\n1month feed, 1month biofuel"
        assert not self.NONHUMAN_CONSUMPTION_SET
        constants_for_params["DELAY"]["FEED_SHUTOFF_MONTHS"] = 1
        constants_for_params["DELAY"]["BIOFUEL_SHUTOFF_MONTHS"] = 1

        constants_for_params[
            "MINIMUM_PERCENT_FED_BEFORE_NONHUMAN_CONSUMPTION_ALLOWED"
        ] = 100

        self.NONHUMAN_CONSUMPTION_SET = True
        return constants_for_params

    def set_short_delayed_shutoff(self, constants_for_params):
        self.scenario_description += "\n2month feed, 1month biofuel"
        assert not self.NONHUMAN_CONSUMPTION_SET
        constants_for_params["DELAY"]["FEED_SHUTOFF_MONTHS"] = 2
        constants_for_params["DELAY"]["BIOFUEL_SHUTOFF_MONTHS"] = 1

        constants_for_params[
            "MINIMUM_PERCENT_FED_BEFORE_NONHUMAN_CONSUMPTION_ALLOWED"
        ] = 100
        self.NONHUMAN_CONSUMPTION_SET = True
        return constants_for_params

    def set_long_delayed_shutoff(self, constants_for_params):
        self.scenario_description += "\n3month feed, 2month biofuel"
        assert not self.NONHUMAN_CONSUMPTION_SET
        constants_for_params["DELAY"]["FEED_SHUTOFF_MONTHS"] = 3
        constants_for_params["DELAY"]["BIOFUEL_SHUTOFF_MONTHS"] = 2

        constants_for_params[
            "MINIMUM_PERCENT_FED_BEFORE_NONHUMAN_CONSUMPTION_ALLOWED"
        ] = 100

        self.NONHUMAN_CONSUMPTION_SET = True
        return constants_for_params

    def set_continued_feed_biofuels(self, constants_for_params):
        self.scenario_description += "\ncontinued feed/biofuel"
        assert not self.NONHUMAN_CONSUMPTION_SET
        # if there is no food storage, then feed and biofuels when no food is being
        # stored would not make any sense, as the total food available could go negative
        assert (
            "STORE_FOOD_BETWEEN_YEARS" in constants_for_params.keys()
        ), """ERROR : You must assign stored food before setting biofuels"""

        constants_for_params["DELAY"]["FEED_SHUTOFF_MONTHS"] = constants_for_params[
            "NMONTHS"
        ]
        constants_for_params["DELAY"]["BIOFUEL_SHUTOFF_MONTHS"] = constants_for_params[
            "NMONTHS"
        ]
        constants_for_params[
            "MINIMUM_PERCENT_FED_BEFORE_NONHUMAN_CONSUMPTION_ALLOWED"
        ] = 100

        self.NONHUMAN_CONSUMPTION_SET = True
        return constants_for_params

    def set_continued_after_10_percent_fed(self, constants_for_params):
        self.scenario_description += "\ncontinued feed/biofuel after 10% fed"
        assert not self.NONHUMAN_CONSUMPTION_SET
        # if there is no food storage, then feed and biofuels when no food is being
        # stored would not make any sense, as the total food available could go negative
        assert (
            "STORE_FOOD_BETWEEN_YEARS" in constants_for_params.keys()
        ), """ERROR : You must assign stored food before setting biofuels"""

        constants_for_params["DELAY"]["FEED_SHUTOFF_MONTHS"] = constants_for_params[
            "NMONTHS"
        ]
        constants_for_params["DELAY"]["BIOFUEL_SHUTOFF_MONTHS"] = constants_for_params[
            "NMONTHS"
        ]
        constants_for_params[
            "MINIMUM_PERCENT_FED_BEFORE_NONHUMAN_CONSUMPTION_ALLOWED"
        ] = 10

        self.NONHUMAN_CONSUMPTION_SET = True
        return constants_for_params

    def set_long_delayed_shutoff_after_10_percent_fed(self, constants_for_params):
        self.scenario_description += "\ndelayed shutoff feed/biofuel after 10% fed"
        assert not self.NONHUMAN_CONSUMPTION_SET
        # if there is no food storage, then feed and biofuels when no food is being
        # stored would not make any sense, as the total food available could go negative
        assert (
            "STORE_FOOD_BETWEEN_YEARS" in constants_for_params.keys()
        ), """ERROR : You must assign stored food before setting biofuels"""

        constants_for_params["DELAY"]["FEED_SHUTOFF_MONTHS"] = 12
        constants_for_params["DELAY"]["BIOFUEL_SHUTOFF_MONTHS"] = 6
        constants_for_params[
            "MINIMUM_PERCENT_FED_BEFORE_NONHUMAN_CONSUMPTION_ALLOWED"
        ] = 10

        self.NONHUMAN_CONSUMPTION_SET = True
        return constants_for_params

    # MEAT PRODUCTION STRATEGIES

    def set_breeding_to_greatly_reduced(self, constants_for_params):
        self.scenario_description += "\nstop breeding animals immediately"
        assert not self.MEAT_STRATEGY_SET

        constants_for_params["BREEDING_STRATEGY"] = "reduced"

        self.MEAT_STRATEGY_SET = True
        return constants_for_params

    def set_to_baseline_breeding(self, constants_for_params):
        self.scenario_description += "\nunchanged animal breeding"
        assert not self.MEAT_STRATEGY_SET

        constants_for_params["BREEDING_STRATEGY"] = "baseline"

        self.MEAT_STRATEGY_SET = True
        return constants_for_params

    def set_to_feed_only_ruminants(self, constants_for_params):
        self.scenario_description += "\nfeed only ruminants, rest are reduced"
        assert not self.MEAT_STRATEGY_SET

        constants_for_params["BREEDING_STRATEGY"] = "feed_only_ruminants"

        self.MEAT_STRATEGY_SET = True
        return constants_for_params

    # WASTE

    def set_waste_to_zero(self, constants_for_params):
        self.scenario_description += "\nno waste"
        assert not self.WASTE_SET
        constants_for_params["WASTE_DISTRIBUTION"] = {}
        constants_for_params["WASTE_DISTRIBUTION"]["SUGAR"] = 0  # %
        constants_for_params["WASTE_DISTRIBUTION"]["MEAT"] = 0  # %
        constants_for_params["WASTE_DISTRIBUTION"]["MILK"] = 0  # %
        constants_for_params["WASTE_DISTRIBUTION"]["SEAFOOD"] = 0  # %
        constants_for_params["WASTE_DISTRIBUTION"]["CROPS"] = 0
        constants_for_params["WASTE_DISTRIBUTION"]["SEAWEED"] = 0  # %
        constants_for_params["WASTE_RETAIL"] = 0  # %

        self.WASTE_SET = True
        return constants_for_params

    def get_global_distribution_waste(self):
        """
        Calculates the distribution waste of the global food system.
        """
        assert self.IS_GLOBAL_ANALYSIS

        distribution_loss = {}

        distribution_loss["SUGAR"] = 0.09
        distribution_loss["CROPS"] = 4.96
        distribution_loss["MEAT"] = 0.80
        distribution_loss["MILK"] = 2.12
        distribution_loss["SEAFOOD"] = 0.17
        distribution_loss["SEAWEED"] = distribution_loss["SEAFOOD"]

        return distribution_loss

    def set_global_waste_to_tripled_prices(self, constants_for_params):
        self.scenario_description += "\nwaste at 3x price"
        assert self.IS_GLOBAL_ANALYSIS
        assert not self.WASTE_SET
        """
        overall waste, on farm + distribution + retail
        3x prices (note, currently set to 2019, not 2020)
        """

        distribution_waste = self.get_global_distribution_waste()

        constants_for_params["WASTE_DISTRIBUTION"] = distribution_waste

        RETAIL_WASTE = 6.08  # retail waste in units percent
        constants_for_params["WASTE_RETAIL"] = RETAIL_WASTE
        self.WASTE_SET = True
        return constants_for_params

    def set_global_waste_to_doubled_prices(self, constants_for_params):
        """
        overall waste, on farm + distribution + retail
        2x prices (note, currently set to 2019, not 2020)
        """
        self.scenario_description += "\nwaste at 2x price"
        assert not self.WASTE_SET
        assert self.IS_GLOBAL_ANALYSIS

        distribution_waste = self.get_global_distribution_waste()
        constants_for_params["WASTE_DISTRIBUTION"] = distribution_waste

        RETAIL_WASTE = 10.6  # retail waste in units percent
        constants_for_params["WASTE_RETAIL"] = RETAIL_WASTE

        self.WASTE_SET = True
        return constants_for_params

    def set_global_waste_to_baseline_prices(self, constants_for_params):
        """
        overall waste, on farm+distribution+retail
        1x prices (note, currently set to 2019, not 2020)
        """
        self.scenario_description += "\nnormal waste"
        assert self.IS_GLOBAL_ANALYSIS
        assert not self.WASTE_SET

        distribution_waste = self.get_global_distribution_waste()

        constants_for_params["WASTE_DISTRIBUTION"] = distribution_waste

        RETAIL_WASTE = 24.98  # retail waste in units percent
        constants_for_params["WASTE_RETAIL"] = RETAIL_WASTE

        self.WASTE_SET = True
        return constants_for_params

    def get_distribution_waste(self, country_data):
        """
        Calculates the distribution waste of the global food system.
        """
        assert not self.IS_GLOBAL_ANALYSIS
        distribution_loss = {}

        distribution_loss["SUGAR"] = country_data["distribution_loss_sugar"] * 100
        distribution_loss["CROPS"] = country_data["distribution_loss_crops"] * 100
        distribution_loss["MEAT"] = country_data["distribution_loss_meat"] * 100
        distribution_loss["MILK"] = country_data["distribution_loss_dairy"] * 100
        distribution_loss["SEAFOOD"] = country_data["distribution_loss_seafood"] * 100
        distribution_loss["SEAWEED"] = distribution_loss["SEAFOOD"]

        return distribution_loss

    def set_country_waste_to_tripled_prices(self, constants_for_params, country_data):
        """
        overall waste, on farm + distribution + retail
        3x prices (note, currently set to 2019, not 2020)
        """
        self.scenario_description += "\nwaste at 3x price"
        assert not self.WASTE_SET
        assert not self.IS_GLOBAL_ANALYSIS

        distribution_waste = self.get_distribution_waste(country_data)

        constants_for_params["WASTE_DISTRIBUTION"] = distribution_waste

        RETAIL_WASTE = country_data["retail_waste_price_triple"] * 100
        constants_for_params["WASTE_RETAIL"] = RETAIL_WASTE

        self.WASTE_SET = True
        return constants_for_params

    def set_country_waste_to_doubled_prices(self, constants_for_params, country_data):
        """
        overall waste, on farm + distribution + retail
        2x prices (note, currently set to 2019, not 2020)
        """
        self.scenario_description += "\nwaste at 2x price"
        assert not self.WASTE_SET
        assert not self.IS_GLOBAL_ANALYSIS

        distribution_waste = self.get_distribution_waste(country_data)
        constants_for_params["WASTE_DISTRIBUTION"] = distribution_waste

        RETAIL_WASTE = country_data["retail_waste_price_double"] * 100
        constants_for_params["WASTE_RETAIL"] = RETAIL_WASTE

        self.WASTE_SET = True
        return constants_for_params

    def set_country_waste_to_baseline_prices(self, constants_for_params, country_data):
        """
        overall waste, on farm+distribution+retail
        1x prices (note, currently set to 2019, not 2020)
        """
        self.scenario_description += "\nbaseline waste"
        assert not self.WASTE_SET
        assert not self.IS_GLOBAL_ANALYSIS

        distribution_waste = self.get_distribution_waste(country_data)
        constants_for_params["WASTE_DISTRIBUTION"] = distribution_waste

        RETAIL_WASTE = country_data["retail_waste_baseline"] * 100
        constants_for_params["WASTE_RETAIL"] = RETAIL_WASTE
        self.WASTE_SET = True
        return constants_for_params

    # NUTRITION

    def set_baseline_nutrition_profile(self, constants_for_params):
        self.scenario_description += "\nbaseline nutrition"
        assert not self.NUTRITION_PROFILE_SET

        constants_for_params["NUTRITION"] = {}

        # kcals per person per day
        constants_for_params["NUTRITION"]["KCALS_DAILY"] = 2100

        # grams per person per day
        constants_for_params["NUTRITION"]["FAT_DAILY"] = 61.7

        # grams per person per day
        constants_for_params["NUTRITION"]["PROTEIN_DAILY"] = 59.5

        self.NUTRITION_PROFILE_SET = True
        return constants_for_params

    def set_catastrophe_nutrition_profile(self, constants_for_params):
        self.scenario_description += "\nminimum sufficient nutrition"
        assert not self.NUTRITION_PROFILE_SET

        constants_for_params["NUTRITION"] = {}

        # kcals per person per day
        constants_for_params["NUTRITION"]["KCALS_DAILY"] = 2100

        # grams per person per day
        constants_for_params["NUTRITION"]["FAT_DAILY"] = 47

        # grams per person per day
        constants_for_params["NUTRITION"]["PROTEIN_DAILY"] = 51

        self.NUTRITION_PROFILE_SET = True
        return constants_for_params

    # INTAKE CONSTRAINTS

    def set_intake_constraints_to_enabled(self, constants_for_params):
        self.scenario_description += "\n% kcals limit for seaweed,cs,or scp enforced"
        assert not self.INTAKE_CONSTRAINTS_SET
        constants_for_params["MAX_SEAWEED_AS_PERCENT_KCALS_HUMANS"] = 10
        constants_for_params["MAX_CELLULOSIC_SUGAR_AS_PERCENT_KCALS_HUMANS"] = 40
        constants_for_params["MAX_METHANE_SCP_AS_PERCENT_KCALS_HUMANS"] = 50

        constants_for_params["MAX_SEAWEED_AS_PERCENT_KCALS_FEED"] = 10
        constants_for_params["MAX_CELLULOSIC_SUGAR_AS_PERCENT_KCALS_FEED"] = 10
        constants_for_params["MAX_METHANE_SCP_AS_PERCENT_KCALS_FEED"] = 43

        constants_for_params["MAX_SEAWEED_AS_PERCENT_KCALS_BIOFUEL"] = 10
        constants_for_params["MAX_CELLULOSIC_SUGAR_AS_PERCENT_KCALS_BIOFUEL"] = 100
        constants_for_params["MAX_METHANE_SCP_AS_PERCENT_KCALS_BIOFUEL"] = 100

        self.INTAKE_CONSTRAINTS_SET = True
        return constants_for_params

    def set_intake_constraints_to_disabled_for_humans(self, constants_for_params):
        self.scenario_description += "\nno human % kcals limit for seaweed,cs,or scp"
        assert not self.INTAKE_CONSTRAINTS_SET
        constants_for_params["MAX_SEAWEED_AS_PERCENT_KCALS_HUMANS"] = 100
        constants_for_params["MAX_CELLULOSIC_SUGAR_AS_PERCENT_KCALS_HUMANS"] = 100
        constants_for_params["MAX_METHANE_SCP_AS_PERCENT_KCALS_HUMANS"] = 100

        constants_for_params["MAX_SEAWEED_AS_PERCENT_KCALS_FEED"] = 10
        constants_for_params["MAX_CELLULOSIC_SUGAR_AS_PERCENT_KCALS_FEED"] = 10
        constants_for_params["MAX_METHANE_SCP_AS_PERCENT_KCALS_FEED"] = 43

        constants_for_params["MAX_SEAWEED_AS_PERCENT_KCALS_BIOFUEL"] = 10
        constants_for_params["MAX_CELLULOSIC_SUGAR_AS_PERCENT_KCALS_BIOFUEL"] = 100
        constants_for_params["MAX_METHANE_SCP_AS_PERCENT_KCALS_BIOFUEL"] = 100

        self.INTAKE_CONSTRAINTS_SET = True
        return constants_for_params

    # STORED FOOD

    def set_no_stored_food(self, constants_for_params):
        """
        Sets the stored food at start of simulation to zero.

        """
        self.scenario_description += "\nzero stored food used"
        assert not self.STORED_FOOD_SET
        constants_for_params["STORE_FOOD_BETWEEN_YEARS"] = True
        constants_for_params["PERCENT_STORED_FOOD_TO_USE"] = 0
        constants_for_params["ADD_STORED_FOOD"] = False
        self.STORED_FOOD_SET = True
        return constants_for_params

    def set_baseline_stored_food(self, constants_for_params):
        """
        Sets the stored food at start of simulation to the expected amount in the start month.

        """
        self.scenario_description += "\nexpected stored food usage in baseline scenario"
        assert not self.STORED_FOOD_SET
        constants_for_params["STORE_FOOD_BETWEEN_YEARS"] = True
        constants_for_params["PERCENT_STORED_FOOD_TO_USE"] = 100
        constants_for_params["ADD_STORED_FOOD"] = True
        self.STORED_FOOD_SET = True
        return constants_for_params

    # STORED FOOD END SIMULATION

    def set_stored_food_buffer_zero(self, constants_for_params):
        """
        Sets the stored food buffer as zero -- no stored food left at
        the end of the simulation.

        However, in reality food in transit and food in grocery stores and
        warehouses means there would still likely be some food available at
        the end as a buffer.

        """
        self.scenario_description += "\nall stocks used"
        assert not self.STORED_FOOD_END_SIM_SET
        constants_for_params["STORE_FOOD_BETWEEN_YEARS"] = True
        constants_for_params["END_SIMULATION_STOCKS_RATIO"] = 0

        self.STORED_FOOD_END_SIM_SET = True
        return constants_for_params

    def set_no_stored_food_between_years(self, constants_for_params):
        """
        Sets the stored food between years as zero. No food is traded between the
        12 month intervals seasons. Makes more sense if seasonality is assumed zero.
        All expected stored food at start is however available.

        However, in reality food in transit and food in grocery stores and
        warehouses means there would still likely be some food available at
        the end as a buffer.

        """
        self.scenario_description += "\nstored food/stored meat unused after 12 months"
        assert not self.STORED_FOOD_END_SIM_SET
        constants_for_params["STORE_FOOD_BETWEEN_YEARS"] = False
        constants_for_params["END_SIMULATION_STOCKS_RATIO"] = 0
        self.STORED_FOOD_END_SIM_SET = True
        return constants_for_params

    def set_stored_food_buffer_as_baseline(self, constants_for_params):
        """
        Sets the stored food buffer as 100% -- the typical stored food buffer
        in ~2020 left at the end of the simulation.

        """
        self.scenario_description += "\nstocks available at end of simulation"
        assert not self.STORED_FOOD_END_SIM_SET
        constants_for_params["STORE_FOOD_BETWEEN_YEARS"] = True
        constants_for_params["END_SIMULATION_STOCKS_RATIO"] = 1

        self.STORED_FOOD_END_SIM_SET = True
        return constants_for_params

    def set_stored_food_buffer_as_baseline_and_no_stored_between_years(
        self, constants_for_params
    ):
        """
        Sets the stored food buffer as 100% -- the typical stored food buffer
        in ~2020 left at the end of the simulation.

        """
        self.scenario_description += "\nstocks available at end of simulation"
        assert not self.STORED_FOOD_END_SIM_SET
        constants_for_params["STORE_FOOD_BETWEEN_YEARS"] = False
        constants_for_params["END_SIMULATION_STOCKS_RATIO"] = 1

        self.STORED_FOOD_END_SIM_SET = True
        return constants_for_params

    # SEASONALITY

    def set_no_seasonality(self, constants_for_params):
        self.scenario_description += "\nno seasonality"
        assert not self.SEASONALITY_SET

        # most food grown in tropics, so set seasonality to typical in tropics
        # fractional production per month
        constants_for_params["SEASONALITY"] = [1 / 12] * 12

        self.SEASONALITY_SET = True
        return constants_for_params

    def set_global_seasonality_baseline(self, constants_for_params):
        assert self.IS_GLOBAL_ANALYSIS
        self.scenario_description += "\nnormal crop seasons"
        assert not self.SEASONALITY_SET

        # fractional production per month
        constants_for_params["SEASONALITY"] = [
            0.1121,
            0.0178,
            0.0241,
            0.0344,
            0.0338,
            0.0411,
            0.0882,
            0.0791,
            0.1042,
            0.1911,
            0.1377,
            0.1365,
        ]
        self.SEASONALITY_SET = True
        return constants_for_params

    def set_global_seasonality_nuclear_winter(self, constants_for_params):
        self.scenario_description += "\nnormal crop seasons"
        assert not self.SEASONALITY_SET
        assert self.IS_GLOBAL_ANALYSIS

        # most food grown in tropics, so set seasonality to typical in tropics
        # fractional production per month
        constants_for_params["SEASONALITY"] = [
            0.1564,
            0.0461,
            0.0650,
            0.1017,
            0.0772,
            0.0785,
            0.0667,
            0.0256,
            0.0163,
            0.1254,
            0.1183,
            0.1228,
        ]

        self.SEASONALITY_SET = True
        return constants_for_params

    def set_country_seasonality(self, constants_for_params, country_data):
        assert not self.IS_GLOBAL_ANALYSIS
        assert not self.SEASONALITY_SET
        self.scenario_description += "\nnormal crop seasons"
        # fractional production per month
        constants_for_params["SEASONALITY"] = [
            country_data["seasonality_m" + str(i)] for i in range(1, 13)
        ]

        # check that the seasonality sums to one using pytest approx
        assert np.sum(constants_for_params["SEASONALITY"]) == pytest.approx(1.0), (
            "ERROR: Seasonality does not sum to one for country: "
            + country_data["country"]
        )

        # check that each month is between 0 and 1
        for i in range(12):
            assert 0 <= constants_for_params["SEASONALITY"][i] <= 1, (
                "ERROR: Seasonality is not between 0 and 1 for country: "
                + country_data["country"]
            )

        self.SEASONALITY_SET = True
        return constants_for_params

    # GRASS_PRODUCTION

    def set_grasses_baseline(self, constants_for_params):
        self.scenario_description += "\nbaseline grazing"
        assert not self.GRASSES_SET
        for i in range(1, 11):
            constants_for_params["RATIO_GRASSES_YEAR" + str(i)] = 1

        self.GRASSES_SET = True
        return constants_for_params

    def set_global_grasses_nuclear_winter(self, constants_for_params):
        self.scenario_description += "\nreduced grazing"
        assert self.IS_GLOBAL_ANALYSIS
        assert not self.GRASSES_SET

        # tons dry caloric monthly
        constants_for_params["RATIO_GRASSES_YEAR1"] = 0.65
        constants_for_params["RATIO_GRASSES_YEAR2"] = 0.23
        constants_for_params["RATIO_GRASSES_YEAR3"] = 0.14
        constants_for_params["RATIO_GRASSES_YEAR4"] = 0.13
        constants_for_params["RATIO_GRASSES_YEAR5"] = 0.13
        constants_for_params["RATIO_GRASSES_YEAR6"] = 0.19
        constants_for_params["RATIO_GRASSES_YEAR7"] = 0.24
        constants_for_params["RATIO_GRASSES_YEAR8"] = 0.33  # TODO: UPDATE THESE
        constants_for_params["RATIO_GRASSES_YEAR9"] = 0.33  # TODO: UPDATE THESE
        constants_for_params["RATIO_GRASSES_YEAR10"] = 0.33  # TODO: UPDATE THESE

        self.GRASSES_SET = True
        return constants_for_params

    def set_country_grasses_nuclear_winter(self, constants_for_params, country_data):
        self.scenario_description += "\nreduced grazing"
        assert not self.IS_GLOBAL_ANALYSIS
        assert not self.GRASSES_SET
        # fractional production per month
        for i in range(1, 11):
            constants_for_params["RATIO_GRASSES_YEAR" + str(i)] = (
                1 + country_data["grasses_reduction_year" + str(i)]
            )

        self.GRASSES_SET = True
        return constants_for_params

    def set_country_grasses_to_zero(self, constants_for_params):
        self.scenario_description += "\nzero grazing"
        assert not self.IS_GLOBAL_ANALYSIS
        assert not self.GRASSES_SET
        # fractional production per month
        for i in range(1, 11):
            constants_for_params["RATIO_GRASSES_YEAR" + str(i)] = 0

        self.GRASSES_SET = True
        return constants_for_params

    # FISH

    def set_fish_zero(self, constants_for_params, time_consts):
        self.scenario_description += "\nno fish"
        assert not self.FISH_SET
        # 0% of fishing remains in baseline
        time_consts["FISH_PERCENT_MONTHLY"] = np.array(
            [0] * constants_for_params["NMONTHS"]
        )

        self.FISH_SET = True
        return time_consts

    def set_fish_nuclear_winter_reduction(self, time_consts):
        """
        Set the fish percentages in every country (or globally) from baseline
        although this is a global number, we don't have the regional number, so
        we use the global instead.
        """
        self.scenario_description += "\nreduced fish"
        assert not self.FISH_SET
        time_consts["FISH_PERCENT_MONTHLY"] = list(
            np.array(
                [
                    0.0,
                    -0.90909091,
                    -1.81818182,
                    -2.72727273,
                    -3.63636364,
                    -4.54545455,
                    -5.45454545,
                    -6.36363636,
                    -7.27272727,
                    -8.18181818,
                    -9.09090909,
                    -10,
                    -10.0,
                    -12.0,
                    -14.0,
                    -16.0,
                    -18.0,
                    -20.0,
                    -22.0,
                    -24.0,
                    -26.0,
                    -28.0,
                    -30.0,
                    -32.0,
                    -32.0,
                    -32.27272727,
                    -32.54545455,
                    -32.81818182,
                    -33.09090909,
                    -33.36363636,
                    -33.63636364,
                    -33.90909091,
                    -34.18181818,
                    -34.45454545,
                    -34.72727273,
                    -35.0,
                    -35.0,
                    -34.90909091,
                    -34.81818182,
                    -34.72727273,
                    -34.63636364,
                    -34.54545455,
                    -34.45454545,
                    -34.36363636,
                    -34.27272727,
                    -34.18181818,
                    -34.09090909,
                    -34.0,
                    -34.0,
                    -33.90909091,
                    -33.81818182,
                    -33.72727273,
                    -33.63636364,
                    -33.54545455,
                    -33.45454545,
                    -33.36363636,
                    -33.27272727,
                    -33.18181818,
                    -33.09090909,
                    -33.0,
                    -33.0,
                    -32.81818182,
                    -32.63636364,
                    -32.45454545,
                    -32.27272727,
                    -32.09090909,
                    -31.90909091,
                    -31.72727273,
                    -31.54545455,
                    -31.36363636,
                    -31.18181818,
                    -31.0,
                    -31.0,
                    -30.90909091,
                    -30.81818182,
                    -30.72727273,
                    -30.63636364,
                    -30.54545455,
                    -30.45454545,
                    -30.36363636,
                    -30.27272727,
                    -30.18181818,
                    -30.09090909,
                    -30.0,  # TODO: update to correct number for these months
                    -30.0,  # TODO: update to correct number for these months
                    -30.0,  # TODO: update to correct number for these months
                    -30.0,  # TODO: update to correct number for these months
                    -30.0,  # TODO: update to correct number for these months
                    -30.0,  # TODO: update to correct number for these months
                    -30.0,  # TODO: update to correct number for these months
                    -30.0,  # TODO: update to correct number for these months
                    -30.0,  # TODO: update to correct number for these months
                    -30.0,  # TODO: update to correct number for these months
                    -30.0,  # TODO: update to correct number for these months
                    -30.0,  # TODO: update to correct number for these months
                    -30.0,  # TODO: update to correct number for these months
                    -30.0,  # TODO: update to correct number for these months
                    -30.0,  # TODO: update to correct number for these months
                    -30.0,  # TODO: update to correct number for these months
                    -30.0,  # TODO: update to correct number for these months
                    -30.0,  # TODO: update to correct number for these months
                    -30.0,  # TODO: update to correct number for these months
                    -30.0,  # TODO: update to correct number for these months
                    -30.0,  # TODO: update to correct number for these months
                    -30.0,  # TODO: update to correct number for these months
                    -30.0,  # TODO: update to correct number for these months
                    -30.0,  # TODO: update to correct number for these months
                    -30.0,  # TODO: update to correct number for these months
                    -30.0,  # TODO: update to correct number for these months
                    -30.0,  # TODO: update to correct number for these months
                    -30.0,  # TODO: update to correct number for these months
                    -30.0,  # TODO: update to correct number for these months
                    -30.0,  # TODO: update to correct number for these months
                    -30.0,  # TODO: update to correct number for these months
                    -30.0,  # TODO: update to correct number for these months
                    -30.0,  # TODO: update to correct number for these months
                    -30.0,  # TODO: update to correct number for these months
                    -30.0,  # TODO: update to correct number for these months
                    -30.0,  # TODO: update to correct number for these months
                    -30.0,  # TODO: update to correct number for these months
                    -30.0,  # TODO: update to correct number for these months
                    -30.0,  # TODO: update to correct number for these months
                    -30.0,  # TODO: update to correct number for these months
                    -30.0,  # TODO: update to correct number for these months
                    -30.0,  # TODO: update to correct number for these months
                    -30.0,  # TODO: update to correct number for these months
                    -30.0,  # TODO: update to correct number for these months
                    -30.0,  # TODO: update to correct number for these months
                    -30.0,  # TODO: update to correct number for these months
                    -30.0,  # TODO: update to correct number for these months
                    -30.0,  # TODO: update to correct number for these months
                    -30.0,  # TODO: update to correct number for these months
                    -30.0,  # TODO: update to correct number for these months
                    -30.0,  # TODO: update to correct number for these months
                    -30.0,  # TODO: update to correct number for these months
                    -30.0,  # TODO: update to correct number for these months
                    -30.0,  # TODO: update to correct number for these months
                    -30.0,  # TODO: update to correct number for these months
                    -30.0,  # TODO: update to correct number for these months
                    -30.0,  # TODO: update to correct number for these months
                    -30.0,  # TODO: update to correct number for these months
                    -30.0,  # TODO: update to correct number for these months
                    -30.0,  # TODO: update to correct number for these months
                    -30.0,  # TODO: update to correct number for these months
                    -30.0,  # TODO: update to correct number for these months
                    -30.0,  # TODO: update to correct number for these months
                    -30.0,  # TODO: update to correct number for these months
                    -30.0,  # TODO: update to correct number for these months
                    -30.0,  # TODO: update to correct number for these months
                    -30.0,  # TODO: update to correct number for these months
                    -30.0,  # TODO: update to correct number for these months
                ]
            )
            + 100
        )

        self.FISH_SET = True
        return time_consts

    def set_fish_baseline(self, constants_for_params, time_consts):
        self.scenario_description += "\nbaseline fish"
        assert not self.FISH_SET
        # 100% of fishing remains in baseline
        time_consts["FISH_PERCENT_MONTHLY"] = np.array(
            [100] * constants_for_params["NMONTHS"]
        )

        self.FISH_SET = True
        return time_consts

    # CROP DISRUPTION

    def set_disruption_to_crops_to_zero(self, constants_for_params):
        self.scenario_description += "\nno crop disruption"
        assert not self.DISRUPTION_SET
        constants_for_params["ADD_OUTDOOR_GROWING"] = True

        for i in range(1, 11):
            constants_for_params["RATIO_CROPS_YEAR" + str(i)] = 1

        self.DISRUPTION_SET = True
        return constants_for_params

    def set_nuclear_winter_global_disruption_to_crops(self, constants_for_params):
        assert self.IS_GLOBAL_ANALYSIS
        self.scenario_description += "\nnuclear winter crops"
        assert not self.DISRUPTION_SET
        constants_for_params["ADD_OUTDOOR_GROWING"] = True

        constants_for_params["RATIO_CROPS_YEAR1"] = 1 - 0.53
        constants_for_params["RATIO_CROPS_YEAR2"] = 1 - 0.82
        constants_for_params["RATIO_CROPS_YEAR3"] = 1 - 0.89
        constants_for_params["RATIO_CROPS_YEAR4"] = 1 - 0.88
        constants_for_params["RATIO_CROPS_YEAR5"] = 1 - 0.84
        constants_for_params["RATIO_CROPS_YEAR6"] = 1 - 0.76
        constants_for_params["RATIO_CROPS_YEAR7"] = 1 - 0.65
        constants_for_params["RATIO_CROPS_YEAR8"] = 1 - 0.5
        constants_for_params["RATIO_CROPS_YEAR9"] = 1 - 0.33
        constants_for_params["RATIO_CROPS_YEAR10"] = 1 - 0.17
        constants_for_params["RATIO_CROPS_YEAR11"] = 1 - 0.08

        self.DISRUPTION_SET = True
        return constants_for_params

    def set_nuclear_winter_country_disruption_to_crops(
        self, constants_for_params, country_data
    ):
        assert not self.IS_GLOBAL_ANALYSIS
        assert not self.DISRUPTION_SET
        constants_for_params["ADD_OUTDOOR_GROWING"] = True

        self.scenario_description += "\nnuclear winter crops"

        constants_for_params["RATIO_CROPS_YEAR1"] = (
            1 + country_data["crop_reduction_year1"]
        )
        constants_for_params["RATIO_CROPS_YEAR2"] = (
            1 + country_data["crop_reduction_year2"]
        )
        constants_for_params["RATIO_CROPS_YEAR3"] = (
            1 + country_data["crop_reduction_year3"]
        )
        constants_for_params["RATIO_CROPS_YEAR4"] = (
            1 + country_data["crop_reduction_year4"]
        )
        constants_for_params["RATIO_CROPS_YEAR5"] = (
            1 + country_data["crop_reduction_year5"]
        )
        constants_for_params["RATIO_CROPS_YEAR6"] = (
            1 + country_data["crop_reduction_year6"]
        )
        constants_for_params["RATIO_CROPS_YEAR7"] = (
            1 + country_data["crop_reduction_year7"]
        )
        constants_for_params["RATIO_CROPS_YEAR8"] = (
            1 + country_data["crop_reduction_year8"]
        )
        constants_for_params["RATIO_CROPS_YEAR9"] = (
            1 + country_data["crop_reduction_year9"]
        )
        constants_for_params["RATIO_CROPS_YEAR10"] = (
            1 + country_data["crop_reduction_year10"]
        )
        constants_for_params["RATIO_CROPS_YEAR11"] = (
            1 + country_data["crop_reduction_year10"]
        )

        self.DISRUPTION_SET = True
        return constants_for_params

    def set_zero_crops(self, constants_for_params):
        assert not self.DISRUPTION_SET
        constants_for_params["ADD_OUTDOOR_GROWING"] = False

        self.scenario_description += "\ninstant crop failure"

        constants_for_params["RATIO_OF_CROP_YIELDS_FROM_VERY_BEGINNING"] = 0

        constants_for_params["RATIO_CROPS_YEAR1"] = 0
        constants_for_params["RATIO_CROPS_YEAR2"] = 0
        constants_for_params["RATIO_CROPS_YEAR3"] = 0
        constants_for_params["RATIO_CROPS_YEAR4"] = 0
        constants_for_params["RATIO_CROPS_YEAR5"] = 0
        constants_for_params["RATIO_CROPS_YEAR6"] = 0
        constants_for_params["RATIO_CROPS_YEAR7"] = 0
        constants_for_params["RATIO_CROPS_YEAR8"] = 0
        constants_for_params["RATIO_CROPS_YEAR9"] = 0
        constants_for_params["RATIO_CROPS_YEAR10"] = 0
        constants_for_params["RATIO_CROPS_YEAR11"] = 0

        self.DISRUPTION_SET = True
        return constants_for_params

    # EXPANDED AREA
    def set_expanded_area(
        self,
        constants_for_params: dict,
        expanded_area_scenario: str,
        initial_land_clearing_time: int,
        country_data: pd.Series,
    ) -> dict:
        """
        Assign constants regarding expanded planted area to the constants_for_params dictionary.

        Arguments:
            constants_for_params (dict): a dictionary containing the constants for parameters.
            expanded_area_scenario (str): a settings' flag controlling which version of expanded area we use.
                Defaults to no expanded area.
            initial_land_clearing_time (int): since it takes time to clear land for crops, we ignore
                first several months. Defaults to `9`.
            country_data (pandas.Series): a data series take from computer_readable_combined for
                a given country.

        Returns:
            constants_for_params: a modified constants dictionary.
        """
        assert not self.EXPANDED_AREA_SET
        assert not self.IS_GLOBAL_ANALYSIS
        match expanded_area_scenario:
            case "none":
                self.scenario_description += "\nno expanded area"
            case "no_trade":
                self.scenario_description += (
                    "\nexpanded planted area with no equipment trade"
                )
            case "export_pool":
                self.scenario_description += (
                    "\nexpanded planted area with export pool equipment trade"
                )
            case _:
                print(
                    f"WARNING: unrecognised expanded area setting value: {expanded_area_scenario}."
                )
                print("WARNING: defaulting to no expanded area")
                expanded_area_scenario = "none"
                self.scenario_description += "\nno expanded area"
        try:
            initial_land_clearing_time = int(initial_land_clearing_time)
        except ValueError:
            print(
                f"WARNING: invalid value for the `expanded_area_init_land_clearing_time` setting: {initial_land_clearing_time}."
            )
            print("WARNING: defaulting to `9`")
            initial_land_clearing_time = 9
        constants_for_params["EXPANDED_AREA"] = expanded_area_scenario
        constants_for_params["INITIAL_LAND_CLEARING_TIME"] = initial_land_clearing_time
        if expanded_area_scenario == "none":
            self.EXPANDED_AREA_SET = True
            return constants_for_params

        for year in range(1, int((constants_for_params["NMONTHS"] + 1) / 12) + 1):
            key_string = f"expanded_area_{expanded_area_scenario}_kcals_year{year}"
            constants_for_params[key_string] = country_data[key_string]
        self.EXPANDED_AREA_SET = True
        return constants_for_params

    # PROTEIN

    def include_protein(self, constants_for_params):
        assert not self.PROTEIN_SET
        self.scenario_description += "\ninclude protein"
        constants_for_params["INCLUDE_PROTEIN"] = True
        self.PROTEIN_SET = True
        return constants_for_params

    def dont_include_protein(self, constants_for_params):
        assert not self.PROTEIN_SET
        self.scenario_description += "\ndon't include protein"
        constants_for_params["INCLUDE_PROTEIN"] = False
        self.PROTEIN_SET = True
        return constants_for_params

    # FAT

    def include_fat(self, constants_for_params):
        assert not self.FAT_SET
        self.scenario_description += "\ninclude fat"
        constants_for_params["INCLUDE_FAT"] = True
        self.FAT_SET = True

        return constants_for_params

    def dont_include_fat(self, constants_for_params):
        assert not self.FAT_SET
        self.scenario_description += "\ndon't include fat"
        constants_for_params["INCLUDE_FAT"] = False
        self.FAT_SET = True
        return constants_for_params

    # SCENARIOS

    def no_resilient_foods(self, constants_for_params):
        constants_for_params["INDUSTRIAL_FOODS_SLOPE_MULTIPLIER"] = 0
        constants_for_params["RATIO_INCREASED_CROP_AREA"] = 1

        constants_for_params["OG_USE_BETTER_ROTATION"] = False
        constants_for_params["ADD_CELLULOSIC_SUGAR"] = False
        constants_for_params["ADD_GREENHOUSES"] = False
        constants_for_params["ADD_METHANE_SCP"] = False
        constants_for_params["ADD_SEAWEED"] = False

        return constants_for_params

    def seaweed(self, constants_for_params):
        constants_for_params["ADD_SEAWEED"] = True
        constants_for_params["DELAY"]["SEAWEED_MONTHS"] = 1

        return constants_for_params

    def greenhouse(self, constants_for_params):
        constants_for_params["GREENHOUSE_GAIN_PCT"] = 44

        # half values from greenhouse paper due to higher cost
        constants_for_params["DELAY"]["GREENHOUSE_MONTHS"] = 2

        # the greenhouse area of 190 million hectares divided by the total crop area
        # This same fraction is used for the given country, or the globe depending on the "scale"
        # setting.
        constants_for_params["GREENHOUSE_AREA_MULTIPLIER"] = (
            0.19e9 / constants_for_params["INITIAL_GLOBAL_CROP_AREA"]
        )
        constants_for_params["ADD_GREENHOUSES"] = True
        return constants_for_params

    def relocated_outdoor_crops(self, constants_for_params):
        constants_for_params["OG_USE_BETTER_ROTATION"] = True

        # this may seem confusing. KCALS_REDUCTION is the reduction that would otherwise
        # occur averaging in year 3 globally
        constants_for_params["ROTATION_IMPROVEMENTS"]["FAT_RATIO"] = 1.647
        constants_for_params["ROTATION_IMPROVEMENTS"]["PROTEIN_RATIO"] = 1.108
        constants_for_params["RATIO_INCREASED_CROP_AREA"] = 1

        return constants_for_params

    def expanded_area_and_relocated_outdoor_crops(self, constants_for_params):
        constants_for_params["OG_USE_BETTER_ROTATION"] = True

        # this may seem confusing. KCALS_REDUCTION is the reduction that would otherwise
        # occur averaging in year 3 globally
        constants_for_params["ROTATION_IMPROVEMENTS"]["FAT_RATIO"] = 1.647
        constants_for_params["ROTATION_IMPROVEMENTS"]["PROTEIN_RATIO"] = 1.108
        constants_for_params["RATIO_INCREASED_CROP_AREA"] = 72 / 39
        constants_for_params["NUMBER_YEARS_TAKES_TO_REACH_INCREASED_AREA"] = 3

        return constants_for_params

    def methane_scp(self, constants_for_params):
        # (one month delay built into industrial food numbers)
        constants_for_params["DELAY"]["INDUSTRIAL_FOODS_MONTHS"] = 2
        constants_for_params["INDUSTRIAL_FOODS_SLOPE_MULTIPLIER"] = (
            1  # default values from CS and SCP papers
        )

        constants_for_params["ADD_METHANE_SCP"] = True
        return constants_for_params

    def cellulosic_sugar(self, constants_for_params):
        # (one month delay built into industrial food numbers)
        constants_for_params["DELAY"]["INDUSTRIAL_FOODS_MONTHS"] = 2
        constants_for_params["INDUSTRIAL_FOODS_SLOPE_MULTIPLIER"] = (
            1  # default values from CS and SCP papers
        )

        constants_for_params["ADD_CELLULOSIC_SUGAR"] = True
        return constants_for_params

    def get_all_resilient_foods_scenario(self, constants_for_params):
        self.scenario_description += "\nall resilient foods"
        assert not self.SCENARIO_SET
        constants_for_params = self.relocated_outdoor_crops(constants_for_params)
        constants_for_params = self.methane_scp(constants_for_params)
        constants_for_params = self.cellulosic_sugar(constants_for_params)
        constants_for_params = self.greenhouse(constants_for_params)
        constants_for_params = self.seaweed(constants_for_params)

        self.SCENARIO_SET = True
        return constants_for_params

    def get_all_resilient_foods_and_more_area_scenario(self, constants_for_params):
        self.scenario_description += "\nall resilient foods and more area"
        assert not self.SCENARIO_SET

        print(
            "WARNING: There is a known issue where a smaller % minimum needs met occurs"
        )
        print("         if methane scp and cellulosic sugar are included")
        print("         in addition to relocated crops with increased area")
        print("         in some scenarios, compared to no increased area.")

        constants_for_params = self.expanded_area_and_relocated_outdoor_crops(
            constants_for_params
        )

        constants_for_params = self.methane_scp(constants_for_params)
        constants_for_params = self.cellulosic_sugar(constants_for_params)
        constants_for_params = self.greenhouse(constants_for_params)
        constants_for_params = self.seaweed(constants_for_params)

        self.SCENARIO_SET = True
        return constants_for_params

    def get_seaweed_scenario(self, constants_for_params):
        self.scenario_description += "\nscaled up seaweed"
        assert not self.SCENARIO_SET

        constants_for_params["INDUSTRIAL_FOODS_SLOPE_MULTIPLIER"] = 0

        constants_for_params["OG_USE_BETTER_ROTATION"] = False
        constants_for_params["ADD_CELLULOSIC_SUGAR"] = False
        constants_for_params["ADD_GREENHOUSES"] = False
        constants_for_params["ADD_METHANE_SCP"] = False
        constants_for_params["RATIO_INCREASED_CROP_AREA"] = 1

        constants_for_params = self.seaweed(constants_for_params)

        self.SCENARIO_SET = True
        return constants_for_params

    def get_methane_scp_scenario(self, constants_for_params):
        self.scenario_description += "\nscaled up methane SCP"
        assert not self.SCENARIO_SET

        constants_for_params["OG_USE_BETTER_ROTATION"] = False
        constants_for_params["ADD_CELLULOSIC_SUGAR"] = False
        constants_for_params["ADD_GREENHOUSES"] = False
        constants_for_params["ADD_SEAWEED"] = False
        constants_for_params["RATIO_INCREASED_CROP_AREA"] = 1

        constants_for_params = self.methane_scp(constants_for_params)

        self.SCENARIO_SET = True
        return constants_for_params

    def get_cellulosic_sugar_scenario(self, constants_for_params):
        self.scenario_description += "\nscaled up cellulosic sugar"
        assert not self.SCENARIO_SET

        constants_for_params["OG_USE_BETTER_ROTATION"] = False
        constants_for_params["ADD_METHANE_SCP"] = False
        constants_for_params["ADD_GREENHOUSES"] = False
        constants_for_params["ADD_SEAWEED"] = False
        constants_for_params["RATIO_INCREASED_CROP_AREA"] = 1

        constants_for_params = self.cellulosic_sugar(constants_for_params)

        self.SCENARIO_SET = True
        return constants_for_params

    def get_industrial_foods_scenario(self, constants_for_params):
        self.scenario_description += "\nscaled up cellulosic sugar"
        assert not self.SCENARIO_SET

        constants_for_params["OG_USE_BETTER_ROTATION"] = False
        constants_for_params["ADD_GREENHOUSES"] = False
        constants_for_params["ADD_SEAWEED"] = False
        constants_for_params["RATIO_INCREASED_CROP_AREA"] = 1

        constants_for_params = self.methane_scp(constants_for_params)
        constants_for_params = self.cellulosic_sugar(constants_for_params)

        self.SCENARIO_SET = True
        return constants_for_params

    def get_relocated_crops_scenario(self, constants_for_params):
        self.scenario_description += "\nscaled up cold crops"
        assert not self.SCENARIO_SET

        constants_for_params["INDUSTRIAL_FOODS_SLOPE_MULTIPLIER"] = 0

        constants_for_params["ADD_CELLULOSIC_SUGAR"] = False
        constants_for_params["ADD_GREENHOUSES"] = False
        constants_for_params["ADD_METHANE_SCP"] = False
        constants_for_params["ADD_SEAWEED"] = False

        constants_for_params = self.relocated_outdoor_crops(constants_for_params)

        self.SCENARIO_SET = True
        return constants_for_params

    def get_greenhouse_scenario(self, constants_for_params):
        self.scenario_description += "\nscaled up greenhouses"
        assert not self.SCENARIO_SET

        constants_for_params["INDUSTRIAL_FOODS_SLOPE_MULTIPLIER"] = 0

        constants_for_params["RATIO_INCREASED_CROP_AREA"] = 1

        constants_for_params["OG_USE_BETTER_ROTATION"] = False
        constants_for_params["ADD_CELLULOSIC_SUGAR"] = False
        constants_for_params["ADD_METHANE_SCP"] = False
        constants_for_params["ADD_SEAWEED"] = False

        constants_for_params = self.greenhouse(constants_for_params)

        self.SCENARIO_SET = True
        return constants_for_params

    def get_no_resilient_food_scenario(self, constants_for_params):
        self.scenario_description += "\nno resilient foods"
        assert not self.SCENARIO_SET

        constants_for_params = self.no_resilient_foods(constants_for_params)

        self.SCENARIO_SET = True
        return constants_for_params

    # CULLING

    def cull_animals(self, constants_for_params):
        assert not self.CULLING_PARAM_SET
        self.scenario_description += "\nallow meat and milk consumption"
        constants_for_params["ADD_MEAT"] = True
        constants_for_params["ADD_MILK"] = True
        self.CULLING_PARAM_SET = True

        return constants_for_params

    def dont_cull_animals(self, constants_for_params):
        assert not self.CULLING_PARAM_SET
        self.scenario_description += "\nno meat or milk consumption"
        constants_for_params["ADD_MEAT"] = False
        constants_for_params["ADD_MILK"] = False
        self.CULLING_PARAM_SET = True
        return constants_for_params
