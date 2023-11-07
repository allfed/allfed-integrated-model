"""
Scenarios.py: Provides numbers and methods to set the specific scenario to be optimized.
Also makes sure values are never set twice.
"""

import numpy as np
import git

repo_root = git.Repo(".", search_parent_directories=True).working_dir


class Scenarios:
    def __init__(self):
        """
        Initializes the Scenario class with default values for all properties.
        """
        # used to ensure the properties of scenarios are set twice or left unset
        self.NONHUMAN_CONSUMPTION_SET = False
        self.EXCESS_SET = False
        self.WASTE_SET = False
        self.NUTRITION_PROFILE_SET = False
        self.STORED_FOOD_BUFFER_SET = False
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

        # convenient to understand what scenario is being run exactly
        self.scenario_description = "Scenario properties:\n"

    def check_all_set(self):
        """
        Check that all properties of scenarios have been set.
        Raises:
            AssertionError: If any of the properties have not been set.
        """
        # Check that all properties have been set
        assert self.NONHUMAN_CONSUMPTION_SET
        assert self.EXCESS_SET
        assert self.WASTE_SET
        assert self.NUTRITION_PROFILE_SET
        assert self.STORED_FOOD_BUFFER_SET
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

    def init_generic_scenario(self):
        """
        Initializes the constants for the generic scenario.

        Args:
            self: The object instance.

        Returns:
            dict: A dictionary containing the constants for the generic scenario.
        """
        # Ensure that the function is not called twice
        assert not self.GENERIC_INITIALIZED_SET

        # Create a dictionary to store the constants
        constants_for_params = {}

        # Set the constants that are used for all scenarios
        constants_for_params["NMONTHS"] = 120
        constants_for_params["GLOBAL_POP"] = 7723713182  # (about 7.8 billion)

        # Set the constants that are not used unless smoothing is true
        # These are useful for ensuring output variables don't fluctuate wildly
        constants_for_params["DELAY"] = {}
        constants_for_params["MAX_RATIO_CULLED_SLAUGHTER_TO_BASELINE"] = 1

        # Set the constants that are specific to the generic scenario
        constants_for_params["ADD_MILK"] = True
        constants_for_params["ADD_FISH"] = True
        constants_for_params["ADD_OUTDOOR_GROWING"] = True
        constants_for_params["ADD_STORED_FOOD"] = True
        constants_for_params["ADD_MAINTAINED_MEAT"] = True

        # Set the flag to indicate that the function has been called
        self.GENERIC_INITIALIZED_SET = True

        # Return the dictionary of constants
        return constants_for_params

    def init_global_food_system_properties(self):
        self.scenario_description += "\ncontinued trade"
        assert not self.SCALE_SET
        self.IS_GLOBAL_ANALYSIS = True

        constants_for_params = self.init_generic_scenario()

        # global human population (2020)
        constants_for_params["POP"] = 7723713182  # (about 7.8 billion)

        # annual tons dry caloric equivalent
        constants_for_params["BASELINE_CROP_KCALS"] = 3898e6 * 1.015

        # annual tons fat
        constants_for_params["BASELINE_CROP_FAT"] = 322e6 * 1.08

        # annual tons protein
        constants_for_params["BASELINE_CROP_PROTEIN"] = 350e6 * 0.94

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

        # million tons dry caloric monthly
        constants_for_params["HUMAN_INEDIBLE_FEED_BASELINE_MONTHLY"] = 4206 / 12

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

        self.SCALE_SET = True
        return constants_for_params

    def init_country_food_system_properties(self, country_data):
        """
        Initializes the food system properties for a given country.

        Args:
            self: instance of the class
            country_data (dict): a dictionary containing data for the country

        Returns:
            dict: a dictionary containing constants for the parameters

        Raises:
            AssertionError: if any of the assertions fail
        """

        # Add a description of the scenario to the existing scenario description
        self.scenario_description += "\nno food trade"

        # Ensure that the scale has not been set yet
        assert not self.SCALE_SET

        # Set the global analysis flag to False
        self.IS_GLOBAL_ANALYSIS = False

        # Initialize the generic scenario
        constants_for_params = self.init_generic_scenario()

        # Set the global human population (2020)
        constants_for_params["POP"] = country_data["population"]

        # This should only be enabled if we're trying to reproduce the method of Xia
        # et al. (2020), they subtract feed directly from production and ignore stored
        # food usage of crops
        # It also only makes sense to enable this if we're not including fat and protein
        SUBTRACT_FEED_DIRECTLY = False

        if SUBTRACT_FEED_DIRECTLY:
            # Set the baseline crop kcals to crop kcals minus feed kcals
            constants_for_params["BASELINE_CROP_KCALS"] = (
                country_data["crop_kcals"] - country_data["feed_kcals"]
            )

            # If the baseline crop kcals is negative, set it to a small positive value and print a warning
            if constants_for_params["BASELINE_CROP_KCALS"] < 0:
                constants_for_params["BASELINE_CROP_KCALS"] = 0.01
                print("WARNING: Crop production - Feed is set to close to zero!")

        else:
            # Set the baseline crop kcals to crop kcals
            constants_for_params["BASELINE_CROP_KCALS"] = country_data["crop_kcals"]

        # Set the baseline crop fat to crop fat
        constants_for_params["BASELINE_CROP_FAT"] = country_data["crop_fat"]

        # Set the baseline crop protein to crop protein
        constants_for_params["BASELINE_CROP_PROTEIN"] = country_data["crop_protein"]

        # Set the biofuel kcals to biofuel kcals
        constants_for_params["BIOFUEL_KCALS"] = country_data["biofuel_kcals"]

        # Set the biofuel fat to biofuel fat
        constants_for_params["BIOFUEL_FAT"] = country_data["biofuel_fat"]

        # Set the biofuel protein to biofuel protein
        constants_for_params["BIOFUEL_PROTEIN"] = country_data["biofuel_protein"]

        # Set the feed kcals to feed kcals
        constants_for_params["FEED_KCALS"] = country_data["feed_kcals"]

        # Set the feed fat to feed fat
        constants_for_params["FEED_FAT"] = country_data["feed_fat"]

        # Set the feed protein to feed protein
        constants_for_params["FEED_PROTEIN"] = country_data["feed_protein"]

        # Set the human inedible feed baseline monthly to grasses baseline divided by 12
        constants_for_params["HUMAN_INEDIBLE_FEED_BASELINE_MONTHLY"] = (
            country_data["grasses_baseline"] / 12
        )

        # Set the initial milk cattle to dairy cows
        constants_for_params["INITIAL_MILK_CATTLE"] = country_data["dairy_cows"]

        # Set the initial small animals to small animals
        constants_for_params["INIT_SMALL_ANIMALS"] = country_data["small_animals"]

        # These won't be used unless the foods are added to the scenario

        # Set the single cell protein fraction of global production to percent of global capex
        constants_for_params["SCP_GLOBAL_PRODUCTION_FRACTION"] = country_data[
            "percent_of_global_capex"
        ]

        # Set the cellulosic sugar fraction of global production to percent of global production
        constants_for_params["CS_GLOBAL_PRODUCTION_FRACTION"] = country_data[
            "percent_of_global_production"
        ]

        # Ensure that the cellulosic sugar fraction of global production is between 0 and 1
        assert 1 >= constants_for_params["CS_GLOBAL_PRODUCTION_FRACTION"] >= 0

        # Ensure that the initial seaweed fraction is between 0 and 1
        assert 1 >= country_data["initial_seaweed_fraction"] >= 0

        # Ensure that the new area fraction is between 0 and 1
        assert 1 >= country_data["new_area_fraction"] >= 0

        # Ensure that the max area fraction is between 0 and 1
        assert 1 >= country_data["max_area_fraction"] >= 0

        # Ensure that the max area fraction is between 0 and 1
        assert 1 >= country_data["max_area_fraction"] >= 0

        # Ensure that the initial built fraction is between 0 and 1
        assert 1 >= country_data["initial_built_fraction"] >= 0

        # Ensure that the single cell protein fraction of global production is between 0 and 1
        assert 1 >= constants_for_params["SCP_GLOBAL_PRODUCTION_FRACTION"] >= 0

        # Get all seaweed column names
        all_seaweed_col_names = [
            k for k, v in country_data.items() if "seaweed_growth_per_day_" in k
        ]

        # Set the seaweed growth per day for each month
        constants_for_params["SEAWEED_GROWTH_PER_DAY"] = {}
        for i in range(len(all_seaweed_col_names)):
            # Just have the number as a string as the keys for the dictionary
            constants_for_params["SEAWEED_GROWTH_PER_DAY"][
                all_seaweed_col_names[i].replace("seaweed_growth_per_day_", "")
            ] = country_data[all_seaweed_col_names[i]]

        # If the initial seaweed fraction is 0, set add seaweed to False
        if country_data["initial_seaweed_fraction"] == 0:
            constants_for_params["ADD_SEAWEED"] = False

        # Set the initial seaweed fraction to initial seaweed fraction
        constants_for_params["INITIAL_SEAWEED_FRACTION"] = country_data[
            "initial_seaweed_fraction"
        ]

        # Set the seaweed new area fraction to new area fraction
        constants_for_params["SEAWEED_NEW_AREA_FRACTION"] = country_data[
            "new_area_fraction"
        ]

        # Set the seaweed max area fraction to max area fraction
        constants_for_params["SEAWEED_MAX_AREA_FRACTION"] = country_data[
            "max_area_fraction"
        ]

        # Set the power law improvement to power law improvement
        constants_for_params["POWER_LAW_IMPROVEMENT"] = country_data[
            "power_law_improvement"
        ]

        # Set the initial built seaweed fraction to initial built fraction
        constants_for_params["INITIAL_BUILT_SEAWEED_FRACTION"] = country_data[
            "initial_built_fraction"
        ]

        # Set the initial crop area fraction to fraction crop area
        constants_for_params["INITIAL_CROP_AREA_FRACTION"] = country_data[
            "fraction_crop_area"
        ]

        # Set the initial crop area ha to crop area 1000ha times 100
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
        constants_for_params["ROTATION_IMPROVEMENTS"][
            "POWER_LAW_IMPROVEMENT"
        ] = country_data["power_law_improvement"]

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

        self.SCALE_SET = True
        return constants_for_params

    def set_immediate_shutoff(self, constants_for_params):
        """
        Sets the immediate shutoff of feed and biofuel consumption in the simulation.

        Args:
            constants_for_params (dict): A dictionary containing the simulation parameters.

        Returns:
            dict: The updated dictionary of simulation parameters.

        Raises:
            AssertionError: If the NONHUMAN_CONSUMPTION_SET flag is already set.

        """
        # Add a description of the scenario to the existing scenario description
        self.scenario_description += "\nno feed/biofuel"

        # Ensure that the NONHUMAN_CONSUMPTION_SET flag is not already set
        assert not self.NONHUMAN_CONSUMPTION_SET

        # Update the simulation parameters to set the reduced breeding strategy to False
        # and the feed and biofuel shutoff months to 0
        constants_for_params["REDUCED_BREEDING_STRATEGY"] = False
        constants_for_params["DELAY"]["FEED_SHUTOFF_MONTHS"] = 0
        constants_for_params["DELAY"]["BIOFUEL_SHUTOFF_MONTHS"] = 0

        # Set the NONHUMAN_CONSUMPTION_SET flag to True
        self.NONHUMAN_CONSUMPTION_SET = True

        # Return the updated dictionary of simulation parameters
        return constants_for_params

    def set_short_delayed_shutoff(self, constants_for_params):
        """
        Sets a delayed shutoff for feed and biofuel consumption in the simulation.

        Args:
            constants_for_params (dict): A dictionary containing the simulation parameters.

        Returns:
            dict: The updated dictionary of simulation parameters.

        Raises:
            AssertionError: If NONHUMAN_CONSUMPTION_SET is already True.

        Scenario Description:
            Adds a description of the scenario to the simulation's scenario_description attribute.

        """
        # Add a description of the scenario to the simulation's scenario_description attribute.
        self.scenario_description += "\n2month feed, 1month biofuel"

        # Check that NONHUMAN_CONSUMPTION_SET is False to avoid overwriting previous settings.
        assert not self.NONHUMAN_CONSUMPTION_SET

        # Update the simulation parameters with the delayed shutoff values.
        constants_for_params["REDUCED_BREEDING_STRATEGY"] = False
        constants_for_params["DELAY"]["FEED_SHUTOFF_MONTHS"] = 2
        constants_for_params["DELAY"]["BIOFUEL_SHUTOFF_MONTHS"] = 1

        # Set NONHUMAN_CONSUMPTION_SET to True to avoid overwriting previous settings.
        self.NONHUMAN_CONSUMPTION_SET = True

        # Return the updated dictionary of simulation parameters.
        return constants_for_params

    def set_long_delayed_shutoff(self, constants_for_params):
        """
        Sets a long delayed shutoff for feed and biofuel consumption.

        Args:
            constants_for_params (dict): A dictionary of constants for the parameters.

        Returns:
            dict: The updated dictionary of constants for the parameters.
        """
        # Add scenario description
        self.scenario_description += "\n3month feed, 2month biofuel"

        # Check if non-human consumption is already set
        assert not self.NONHUMAN_CONSUMPTION_SET

        # Set reduced breeding strategy to False
        constants_for_params["REDUCED_BREEDING_STRATEGY"] = False

        # Set feed shutoff months to 3 and biofuel shutoff months to 2
        constants_for_params["DELAY"]["FEED_SHUTOFF_MONTHS"] = 3
        constants_for_params["DELAY"]["BIOFUEL_SHUTOFF_MONTHS"] = 2

        # Set non-human consumption to True
        self.NONHUMAN_CONSUMPTION_SET = True

        # Return the updated dictionary of constants for the parameters
        return constants_for_params

    def reduce_breeding(self, constants_for_params):
        """
        This function reduces breeding/biofuel and sets the delay for feed and biofuel shutoff.
        Args:
            self: instance of the class
            constants_for_params (dict): dictionary containing the parameters for the simulation
        Returns:
            dict: updated dictionary containing the parameters for the simulation
        """
        # Add scenario description
        self.scenario_description += "\nreduced breeding/biofuel"

        # Check if non-human consumption is set
        assert not self.NONHUMAN_CONSUMPTION_SET

        # Check if stored food is assigned before setting biofuels
        assert (
            "STORE_FOOD_BETWEEN_YEARS" in constants_for_params.keys()
        ), """ERROR : You must assign stored food before setting biofuels"""

        # Set reduced breeding strategy to True
        constants_for_params["REDUCED_BREEDING_STRATEGY"] = True

        # Set delay for feed and biofuel shutoff based on stored food availability
        if constants_for_params["STORE_FOOD_BETWEEN_YEARS"]:
            constants_for_params["DELAY"]["FEED_SHUTOFF_MONTHS"] = constants_for_params[
                "NMONTHS"
            ]
            constants_for_params["DELAY"]["BIOFUEL_SHUTOFF_MONTHS"] = 2
        else:
            constants_for_params["DELAY"]["FEED_SHUTOFF_MONTHS"] = 11
            constants_for_params["DELAY"]["BIOFUEL_SHUTOFF_MONTHS"] = 11

        # Set non-human consumption to True
        self.NONHUMAN_CONSUMPTION_SET = True

        # Return updated dictionary
        return constants_for_params

    def set_continued_feed_biofuels(self, constants_for_params):
        """
        Sets the parameters for continued feed/biofuel production strategy and updates the scenario description.
        Args:
            constants_for_params (dict): A dictionary containing the parameters for the simulation.

        Returns:
            dict: A dictionary containing the updated parameters for the simulation.

        Raises:
            AssertionError: If there is no food storage, then feed and biofuels when no food is being
            stored would not make any sense, as the total food available could go negative.
            AssertionError: If stored food is not assigned before setting biofuels.

        """
        # Update the scenario description
        self.scenario_description += "\ncontinued feed/biofuel"

        # Check if non-human consumption is already set
        assert not self.NONHUMAN_CONSUMPTION_SET

        # Check if stored food is assigned before setting biofuels
        assert (
            "STORE_FOOD_BETWEEN_YEARS" in constants_for_params.keys()
        ), """ERROR : You must assign stored food before setting biofuels"""

        # Set the parameters for the simulation
        if constants_for_params["STORE_FOOD_BETWEEN_YEARS"]:
            constants_for_params["REDUCED_BREEDING_STRATEGY"] = False
            constants_for_params["DELAY"]["FEED_SHUTOFF_MONTHS"] = constants_for_params[
                "NMONTHS"
            ]
            constants_for_params["DELAY"][
                "BIOFUEL_SHUTOFF_MONTHS"
            ] = constants_for_params["NMONTHS"]
        else:
            constants_for_params["REDUCED_BREEDING_STRATEGY"] = False
            constants_for_params["DELAY"]["FEED_SHUTOFF_MONTHS"] = 11
            constants_for_params["DELAY"]["BIOFUEL_SHUTOFF_MONTHS"] = 11

        # Set the flag for non-human consumption
        self.NONHUMAN_CONSUMPTION_SET = True

        # Return the updated parameters
        return constants_for_params

    def set_unchanged_proportions_feed_grazing(self, constants_for_params):
        """
        This function sets the unchanged proportions of feed to grazing for a given scenario.
        Args:
            self: instance of the class
            constants_for_params (dict): dictionary containing the constants for the parameters
        Returns:
            dict: updated dictionary containing the constants for the parameters
        """
        # Add a description of the scenario to the existing scenario description
        self.scenario_description += "\nunchanged feed to dairy"

        # Ensure that the meat strategy has not been set before
        assert not self.MEAT_STRATEGY_SET

        # Set the USE_EFFICIENT_FEED_STRATEGY constant to False
        constants_for_params["USE_EFFICIENT_FEED_STRATEGY"] = False

        # Set the meat strategy flag to True
        self.MEAT_STRATEGY_SET = True

        # Return the updated constants dictionary
        return constants_for_params

    def set_efficient_feed_grazing_strategy(self, constants_for_params):
        """
        This function sets the efficient feed grazing strategy for dairy cows by updating the constants_for_params dictionary.
        It also updates the scenario_description attribute of the object to reflect the change in strategy.

        Args:
            self: the object instance
            constants_for_params (dict): a dictionary containing the parameters for the simulation

        Returns:
            dict: the updated constants_for_params dictionary

        Raises:
            AssertionError: if the meat strategy has already been set

        """
        # Update the scenario description to reflect the change in strategy
        self.scenario_description += "\ndairy cow feed prioritized"

        # Ensure that the meat strategy has not already been set
        assert not self.MEAT_STRATEGY_SET

        # Update the constants_for_params dictionary to use the efficient feed strategy
        constants_for_params["USE_EFFICIENT_FEED_STRATEGY"] = True

        # Set the meat strategy flag to True to indicate that it has been set
        self.MEAT_STRATEGY_SET = True

        # Return the updated constants_for_params dictionary
        return constants_for_params

    def set_feed_based_on_livestock_levels(self, constants_for_params):
        """
        Sets the feed based on breeding patterns. This function is not really necessary, but it keeps the pattern I guess.
        Args:
            self: instance of the class
            constants_for_params (dict): dictionary containing the constants for the parameters

        Returns:
            dict: dictionary containing the updated constants for the parameters
        """
        # Add scenario description
        self.scenario_description += "\nfeed based on breeding patterns"

        # Check if meat strategy is already set
        assert not self.MEAT_STRATEGY_SET

        # Set the USE_EFFICIENT_FEED_STRATEGY to undefined
        constants_for_params["USE_EFFICIENT_FEED_STRATEGY"] = np.nan  # undefined

        # Set the meat strategy flag to True
        self.MEAT_STRATEGY_SET = True

        # Return the updated constants for the parameters
        return constants_for_params

    def set_excess_to_zero(self, constants_for_params):
        """
        Sets the excess feed percentage to zero for all months in the constants_for_params dictionary.
        This function should only be called once, as indicated by the EXCESS_SET attribute.

        Args:
            constants_for_params (dict): A dictionary containing the parameters for the simulation.

        Returns:
            dict: The modified constants_for_params dictionary with the excess feed percentage set to zero.

        Raises:
            AssertionError: If the EXCESS_SET attribute is already True, indicating that this function has already been called.
        """
        # Check that the function has not already been called
        assert not self.EXCESS_SET

        # Set the excess feed percentage to zero for all months
        constants_for_params["EXCESS_FEED_PERCENT"] = np.zeros(
            constants_for_params["NMONTHS"]
        )

        # Set the EXCESS_SET attribute to True to indicate that this function has been called
        self.EXCESS_SET = True

        # Return the modified constants_for_params dictionary
        return constants_for_params

    def set_excess(self, constants_for_params, excess):
        assert not self.EXCESS_SET
        constants_for_params["EXCESS_FEED_PERCENT"] = excess

        self.EXCESS_SET = True
        return constants_for_params

    # WASTE

    def set_waste_to_zero(self, constants_for_params):
        """
        Sets the waste percentage for all food types to zero.

        Args:
            constants_for_params (dict): A dictionary containing the constants for the simulation.

        Returns:
            dict: The updated dictionary of constants for the simulation.

        Raises:
            AssertionError: If the waste has already been set.

        """
        # Add scenario description
        self.scenario_description += "\nno waste"

        # Check if waste has already been set
        assert not self.WASTE_SET

        # Set waste percentage for all food types to zero
        constants_for_params["WASTE"] = {}
        constants_for_params["WASTE"]["SUGAR"] = 0  # %
        constants_for_params["WASTE"]["MEAT"] = 0  # %
        constants_for_params["WASTE"]["MILK"] = 0  # %
        constants_for_params["WASTE"]["SEAFOOD"] = 0  # %
        constants_for_params["WASTE"]["CROPS"] = 0  # %
        constants_for_params["WASTE"]["SEAWEED"] = 0  # %

        # Mark waste as set
        self.WASTE_SET = True

        # Return updated constants
        return constants_for_params

    def get_total_global_waste(self, retail_waste):
        """
        Calculates the total waste of the global food system by adding retail waste
        to distribution loss.

        Args:
            retail_waste (float): The amount of waste generated at the retail level.

        Returns:
            dict: A dictionary containing the total waste for each food category.

        Raises:
            AssertionError: If the analysis is not global.

        """
        # Ensure that the analysis is global
        assert self.IS_GLOBAL_ANALYSIS

        # Define the distribution loss for each food category
        distribution_loss = {}
        distribution_loss["SUGAR"] = 0.09
        distribution_loss["CROPS"] = 4.96
        distribution_loss["MEAT"] = 0.80
        distribution_loss["MILK"] = 2.12
        distribution_loss["SEAFOOD"] = 0.17
        distribution_loss["SEAWEED"] = distribution_loss["SEAFOOD"]

        # Calculate the total waste for each food category
        total_waste = {}
        total_waste["SUGAR"] = distribution_loss["SUGAR"] + retail_waste
        total_waste["CROPS"] = distribution_loss["CROPS"] + retail_waste
        total_waste["MEAT"] = distribution_loss["MEAT"] + retail_waste
        total_waste["MILK"] = distribution_loss["MILK"] + retail_waste
        total_waste["SEAFOOD"] = distribution_loss["SEAFOOD"] + retail_waste
        total_waste["SEAWEED"] = distribution_loss["SEAWEED"] + retail_waste

        return total_waste

    def set_global_waste_to_tripled_prices(self, constants_for_params):
        """
        Sets the global waste to tripled prices and updates the constants_for_params dictionary.

        Args:
            self: the instance of the class
            constants_for_params (dict): a dictionary containing the constants for the simulation

        Returns:
            dict: the updated constants_for_params dictionary

        Raises:
            AssertionError: if IS_GLOBAL_ANALYSIS is False or WASTE_SET is True

        """
        # Add scenario description
        self.scenario_description += "\nwaste at 3x price"

        # Check if global analysis is being performed and waste has not been set
        assert self.IS_GLOBAL_ANALYSIS
        assert not self.WASTE_SET

        """
        overall waste, on farm + distribution + retail
        3x prices (note, currently set to 2019, not 2020)
        """
        RETAIL_WASTE = 6.08

        # Calculate total waste
        total_waste = self.get_total_global_waste(RETAIL_WASTE)

        # Update constants_for_params dictionary with total waste
        constants_for_params["WASTE"] = total_waste

        # Set WASTE_SET to True to indicate that waste has been set
        self.WASTE_SET = True

        # Return the updated constants_for_params dictionary
        return constants_for_params

    def set_global_waste_to_doubled_prices(self, constants_for_params):
        """
        Sets the global waste to double the prices of 2019. This includes overall waste, on farm, distribution, and retail.
        Args:
            self: instance of the class
            constants_for_params (dict): dictionary containing the constants for the parameters
        Returns:
            dict: updated dictionary containing the constants for the parameters
        Raises:
            AssertionError: if WASTE_SET is True or IS_GLOBAL_ANALYSIS is False
        """
        # Add scenario description
        self.scenario_description += "\nwaste at 2x price"

        # Check if waste is already set and if global analysis is being performed
        assert not self.WASTE_SET
        assert self.IS_GLOBAL_ANALYSIS

        # Set retail waste to 10.6
        RETAIL_WASTE = 10.6

        # Get total global waste
        total_waste = self.get_total_global_waste(RETAIL_WASTE)

        # Update constants_for_params with total waste
        constants_for_params["WASTE"] = total_waste

        # Set WASTE_SET to True
        self.WASTE_SET = True

        # Return updated constants_for_params
        return constants_for_params

    def set_global_waste_to_baseline_prices(self, constants_for_params):
        """
        Sets the global waste to baseline prices for on farm, distribution, and retail.
        Args:
            self: instance of the class
            constants_for_params (dict): dictionary containing the constants for the parameters
        Returns:
            dict: updated dictionary containing the constants for the parameters
        """
        # Add a description of the scenario to the existing scenario description
        self.scenario_description += "\nnormal waste"

        # Check if the analysis is global and waste has not been set yet
        assert self.IS_GLOBAL_ANALYSIS
        assert not self.WASTE_SET

        # Set the retail waste to a constant value
        RETAIL_WASTE = 24.98

        # Calculate the total waste by calling the get_total_global_waste function
        total_waste = self.get_total_global_waste(RETAIL_WASTE)

        # Update the constants_for_params dictionary with the total waste
        constants_for_params["WASTE"] = total_waste

        # Set the waste flag to True
        self.WASTE_SET = True

        # Return the updated constants_for_params dictionary
        return constants_for_params

    def get_total_country_waste(self, retail_waste, country_data):
        """
        Calculates the total waste of the global food system by adding retail waste
        to distribution loss.

        Args:
            retail_waste (float): The amount of waste generated at the retail level
            country_data (dict): A dictionary containing the distribution loss data for
            different food categories

        Returns:
            dict: A dictionary containing the total waste for different food categories

        Raises:
            AssertionError: If the analysis is global

        """
        # Check if the analysis is not global
        assert not self.IS_GLOBAL_ANALYSIS

        # Calculate distribution loss for different food categories
        distribution_loss = {}
        distribution_loss["SUGAR"] = country_data["distribution_loss_sugar"] * 100
        distribution_loss["CROPS"] = country_data["distribution_loss_crops"] * 100
        distribution_loss["MEAT"] = country_data["distribution_loss_meat"] * 100
        distribution_loss["MILK"] = country_data["distribution_loss_dairy"] * 100
        distribution_loss["SEAFOOD"] = country_data["distribution_loss_seafood"] * 100
        distribution_loss["SEAWEED"] = distribution_loss["SEAFOOD"]

        # Calculate total waste for different food categories
        total_waste = {}
        total_waste["SUGAR"] = distribution_loss["SUGAR"] + retail_waste
        total_waste["CROPS"] = distribution_loss["CROPS"] + retail_waste
        total_waste["MEAT"] = distribution_loss["MEAT"] + retail_waste
        total_waste["MILK"] = distribution_loss["MILK"] + retail_waste
        total_waste["SEAFOOD"] = distribution_loss["SEAFOOD"] + retail_waste
        total_waste["SEAWEED"] = distribution_loss["SEAWEED"] + retail_waste

        return total_waste

    def set_country_waste_to_tripled_prices(self, constants_for_params, country_data):
        """
        Sets the overall waste, on farm + distribution + retail, to 3x prices (note, currently set to 2019, not 2020).
        Args:
            self: instance of the class
            constants_for_params (dict): dictionary containing the constants for the parameters
            country_data (dict): dictionary containing the data for the country
        Returns:
            dict: updated dictionary containing the constants for the parameters
        """
        # Add scenario description
        self.scenario_description += "\nwaste at 3x price"

        # Check if waste has already been set
        assert not self.WASTE_SET

        # Check if global analysis is not being performed
        assert not self.IS_GLOBAL_ANALYSIS

        # Get the retail waste price tripled
        RETAIL_WASTE = country_data["retail_waste_price_triple"] * 100

        # Get the total country waste
        total_waste = self.get_total_country_waste(RETAIL_WASTE, country_data)

        # Update the constants for the parameters with the total waste
        constants_for_params["WASTE"] = total_waste

        # Set waste as set
        self.WASTE_SET = True

        # Return the updated constants for the parameters
        return constants_for_params

    def set_country_waste_to_doubled_prices(self, constants_for_params, country_data):
        """
        Sets the country's waste to double the retail price and updates the constants_for_params dictionary accordingly.
        Args:
            self: instance of the class
            constants_for_params (dict): dictionary containing the constants for the model
            country_data (dict): dictionary containing the data for the country
        Returns:
            dict: updated constants_for_params dictionary
        """
        # Add scenario description to the instance variable
        self.scenario_description += "\nwaste at 2x price"

        # Check that the waste has not already been set and that the analysis is not global
        assert not self.WASTE_SET
        assert not self.IS_GLOBAL_ANALYSIS

        # Calculate the retail waste based on the double price
        RETAIL_WASTE = country_data["retail_waste_price_double"] * 100

        # Calculate the total waste for the country
        total_waste = self.get_total_country_waste(RETAIL_WASTE, country_data)

        # Update the constants_for_params dictionary with the new waste value
        constants_for_params["WASTE"] = total_waste

        # Set the WASTE_SET flag to True to indicate that the waste has been set
        self.WASTE_SET = True

        # Return the updated constants_for_params dictionary
        return constants_for_params

    def set_country_waste_to_baseline_prices(self, constants_for_params, country_data):
        """
        Sets the waste for a country to baseline prices for on-farm, distribution, and retail.
        Args:
            self: instance of the class
            constants_for_params (dict): dictionary of constants for the model
            country_data (dict): dictionary of data for the country
        Returns:
            dict: updated dictionary of constants for the model
        """
        # Add scenario description
        self.scenario_description += "\nbaseline waste"

        # Check that waste has not already been set and that global analysis is not being performed
        assert not self.WASTE_SET
        assert not self.IS_GLOBAL_ANALYSIS

        # Get retail waste from country data and convert to percentage
        RETAIL_WASTE = country_data["retail_waste_baseline"] * 100

        # Calculate total waste for the country
        total_waste = self.get_total_country_waste(RETAIL_WASTE, country_data)

        # Update constants for the model with the calculated waste
        constants_for_params["WASTE"] = total_waste

        # Set waste flag to True
        self.WASTE_SET = True

        # Return updated constants
        return constants_for_params

    def set_baseline_nutrition_profile(self, constants_for_params):
        """
        Sets the baseline nutrition profile for the scenario.

        Args:
            constants_for_params (dict): A dictionary containing the constants for the scenario.

        Returns:
            dict: The updated dictionary of constants for the scenario.

        Raises:
            AssertionError: If the nutrition profile has already been set.

        """
        # Add scenario description
        self.scenario_description += "\nbaseline nutrition"

        # Check if nutrition profile has already been set
        assert not self.NUTRITION_PROFILE_SET

        # Set constants for nutrition profile
        constants_for_params["NUTRITION"] = {}

        # Set kcals per person per day
        constants_for_params["NUTRITION"]["KCALS_DAILY"] = 2100

        # Set grams of fat per person per day
        constants_for_params["NUTRITION"]["FAT_DAILY"] = 61.7

        # Set grams of protein per person per day
        constants_for_params["NUTRITION"]["PROTEIN_DAILY"] = 59.5

        # Mark nutrition profile as set
        self.NUTRITION_PROFILE_SET = True

        # Return updated constants
        return constants_for_params

    def set_catastrophe_nutrition_profile(self, constants_for_params):
        """
        Sets the minimum sufficient nutrition profile for a catastrophe scenario.

        Args:
            constants_for_params (dict): A dictionary containing the constants for the scenario.

        Returns:
            dict: The updated dictionary of constants for the scenario.

        Raises:
            AssertionError: If the nutrition profile has already been set.

        """
        # Add a description of the scenario to the existing scenario description
        self.scenario_description += "\nminimum sufficient nutrition"

        # Check if the nutrition profile has already been set
        assert not self.NUTRITION_PROFILE_SET

        # Set the constants for the nutrition profile
        constants_for_params["NUTRITION"] = {}

        # Set the kcals per person per day
        constants_for_params["NUTRITION"]["KCALS_DAILY"] = 2100

        # Set the grams of fat per person per day
        constants_for_params["NUTRITION"]["FAT_DAILY"] = 47

        # Set the grams of protein per person per day
        constants_for_params["NUTRITION"]["PROTEIN_DAILY"] = 51

        # Mark the nutrition profile as set
        self.NUTRITION_PROFILE_SET = True

        # Return the updated constants dictionary
        return constants_for_params

    def set_no_stored_food(self, constants_for_params):
        """
        This function sets the stored food between years as zero. It assumes that no food is traded between the
        12 month intervals seasons. This makes more sense if seasonality is assumed zero.

        However, in reality food in transit and food in grocery stores and
        warehouses means there would still likely be some food available at
        the end as a buffer.

        Args:
            self: instance of the class
            constants_for_params (dict): dictionary containing the parameters for the simulation

        Returns:
            dict: updated dictionary containing the parameters for the simulation
        """
        # Add a description of the scenario to the instance variable
        self.scenario_description += "\nfood stored <= 12 months"

        # Check if the stored food buffer has already been set
        assert not self.STORED_FOOD_BUFFER_SET

        # Set the parameters to zero
        constants_for_params["STORE_FOOD_BETWEEN_YEARS"] = False
        constants_for_params["BUFFER_RATIO"] = 0

        # Set the stored food buffer flag to True
        self.STORED_FOOD_BUFFER_SET = True

        # Return the updated dictionary
        return constants_for_params

    def set_stored_food_buffer_zero(self, constants_for_params):
        """
        Sets the stored food buffer as zero -- no stored food left at
        the end of the simulation.

        However, in reality food in transit and food in grocery stores and
        warehouses means there would still likely be some food available at
        the end as a buffer.

        Args:
            constants_for_params (dict): A dictionary containing the constants for the simulation.

        Returns:
            dict: A dictionary containing the updated constants for the simulation.

        Raises:
            AssertionError: If the stored food buffer has already been set.

        """
        # Add a description of the scenario to the scenario_description attribute
        self.scenario_description += "\nall stocks used"

        # Check if the stored food buffer has already been set
        assert not self.STORED_FOOD_BUFFER_SET

        # Set the constants for storing food between years and the buffer ratio to zero
        constants_for_params["STORE_FOOD_BETWEEN_YEARS"] = True
        constants_for_params["BUFFER_RATIO"] = 0

        # Set the stored food buffer flag to True
        self.STORED_FOOD_BUFFER_SET = True

        # Return the updated constants
        return constants_for_params

    def set_stored_food_buffer_as_baseline(self, constants_for_params):
        """
        Sets the stored food buffer as 100% -- the typical stored food buffer
        in ~2020 left at the end of the simulation.

        Args:
            self: instance of the class
            constants_for_params (dict): dictionary containing the parameters for the simulation

        Returns:
            dict: updated dictionary containing the parameters for the simulation

        Raises:
            AssertionError: if the stored food buffer has already been set

        """
        # Add a description of the scenario to the scenario description
        self.scenario_description += "\nfew stocks used"

        # Check if the stored food buffer has already been set
        assert not self.STORED_FOOD_BUFFER_SET

        # Set the parameters for the stored food buffer
        constants_for_params["STORE_FOOD_BETWEEN_YEARS"] = True
        constants_for_params["BUFFER_RATIO"] = 1

        # Set the flag to indicate that the stored food buffer has been set
        self.STORED_FOOD_BUFFER_SET = True

        # Return the updated dictionary containing the parameters for the simulation
        return constants_for_params

    def set_no_seasonality(self, constants_for_params):
        """
        Sets the seasonality of the scenario to be constant throughout the year.
        Args:
            constants_for_params (dict): A dictionary containing the constants for the scenario.

        Returns:
            dict: A dictionary containing the updated constants for the scenario.
        """
        # Add a description of the scenario to the scenario_description attribute
        self.scenario_description += "\nno seasonality"

        # Ensure that seasonality has not already been set
        assert not self.SEASONALITY_SET

        # Set seasonality to typical in tropics, where most food is grown
        # Fractional production per month
        constants_for_params["SEASONALITY"] = [1 / 12] * 12

        # Set the SEASONALITY_SET attribute to True to indicate that seasonality has been set
        self.SEASONALITY_SET = True

        # Return the updated constants_for_params dictionary
        return constants_for_params

    def set_global_seasonality_baseline(self, constants_for_params):
        """
        Sets the global seasonality baseline for the crop production model.

        Args:
            constants_for_params (dict): A dictionary containing the constants for the crop production model.

        Returns:
            dict: A dictionary containing the updated constants for the crop production model.

        Raises:
            AssertionError: If the global analysis flag is not set or if seasonality has already been set.

        """
        # Check if global analysis flag is set
        assert self.IS_GLOBAL_ANALYSIS

        # Add description to scenario
        self.scenario_description += "\nnormal crop seasons"

        # Check if seasonality has already been set
        assert not self.SEASONALITY_SET

        # Set fractional production per month
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

        # Set seasonality flag
        self.SEASONALITY_SET = True

        # Return updated constants
        return constants_for_params

    def set_global_seasonality_nuclear_winter(self, constants_for_params):
        """
        Sets the seasonality for a global analysis in the event of a nuclear winter.
        The seasonality is set to typical in the tropics, where most food is grown.
        Args:
            self: instance of the class
            constants_for_params (dict): dictionary containing the constants for the parameters
        Returns:
            dict: dictionary containing the updated constants for the parameters
        """
        # Add a description of the scenario to the scenario_description attribute
        self.scenario_description += "\nnormal crop seasons"

        # Check that seasonality has not already been set and that the analysis is global
        assert not self.SEASONALITY_SET
        assert self.IS_GLOBAL_ANALYSIS

        # Set the fractional production per month for the tropics
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

        # Set the SEASONALITY_SET attribute to True to indicate that seasonality has been set
        self.SEASONALITY_SET = True

        # Return the updated constants_for_params dictionary
        return constants_for_params

    def set_country_seasonality(self, constants_for_params, country_data):
        """
        Sets the seasonal crop production for a given country based on the data provided.
        This function sets the seasonal crop production for a given country based on the data provided.
        It sets the fractional production per month and updates the scenario description.
        Args:
            constants_for_params (dict): A dictionary containing the constants for the model.
            country_data (dict): A dictionary containing the data for the country.
        Returns:
            dict: A dictionary containing the updated constants for the model.
        """
        # Check that the function is not being used for global analysis
        assert not self.IS_GLOBAL_ANALYSIS
        # Check that the seasonality has not already been set
        assert not self.SEASONALITY_SET
        # Update the scenario description
        self.scenario_description += "\nnormal crop seasons"
        # Set the seasonal crop production based on the data provided
        constants_for_params["SEASONALITY"] = [
            country_data["seasonality_m" + str(i)] for i in range(1, 13)
        ]
        # Set the flag to indicate that the seasonality has been set
        self.SEASONALITY_SET = True
        # Return the updated constants
        return constants_for_params

    def set_grasses_baseline(self, constants_for_params):
        """
        Sets the baseline grazing for the simulation by setting the ratio of grasses to 1 for each year in the simulation.
        Args:
            self: the instance of the class
            constants_for_params (dict): a dictionary containing the constants for the simulation

        Returns:
            dict: the updated dictionary of constants for the simulation
        """
        # Add a description of the scenario to the scenario_description attribute
        self.scenario_description += "\nbaseline grazing"

        # Check if the grasses have already been set
        assert not self.GRASSES_SET

        # Set the ratio of grasses to 1 for each year in the simulation
        for i in range(1, int(constants_for_params["NMONTHS"] / 12 + 1)):
            constants_for_params["RATIO_GRASSES_YEAR" + str(i)] = 1

        # Set the GRASSES_SET attribute to True to indicate that the grasses have been set
        self.GRASSES_SET = True

        # Return the updated dictionary of constants for the simulation
        return constants_for_params

    def set_global_grasses_nuclear_winter(self, constants_for_params):
        """
        Sets the ratio of grasses for each year in the case of a nuclear winter scenario.
        Args:
            constants_for_params (dict): dictionary containing the constants for the model

        Returns:
            dict: updated dictionary containing the constants for the model
        """
        # Add a description of the scenario to the scenario_description attribute
        self.scenario_description += "\nreduced grazing"

        # Check that the function is being called in the context of a global
        # analysis and that the grasses have not been set yet
        assert self.IS_GLOBAL_ANALYSIS
        assert not self.GRASSES_SET

        # Set the ratio of grasses for each year
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

        # Set the GRASSES_SET attribute to True to indicate that the grasses have been set
        self.GRASSES_SET = True

        # Return the updated dictionary containing the constants for the model
        return constants_for_params

    def set_country_grasses_nuclear_winter(self, constants_for_params, country_data):
        """
        This function sets the ratio of grasses production for each month of the year
        based on the country's grasses reduction data. It also updates the scenario description
        and sets the GRASSES_SET flag to True.
        Args:
            self: instance of the class
            constants_for_params (dict): dictionary containing the constants for the model
            country_data (dict): dictionary containing the country-specific data
        Returns:
            dict: updated constants_for_params dictionary
        """
        # Update scenario description
        self.scenario_description += "\nreduced grazing"

        # Check if global analysis is not being performed
        assert not self.IS_GLOBAL_ANALYSIS

        # Check if grasses have not been set before
        assert not self.GRASSES_SET

        # Set the ratio of grasses production per month
        for i in range(1, int(constants_for_params["NMONTHS"] / 12 + 1)):
            constants_for_params["RATIO_GRASSES_YEAR" + str(i)] = (
                1 + country_data["grasses_reduction_year" + str(i)]
            )

        # Set the GRASSES_SET flag to True
        self.GRASSES_SET = True

        # Return the updated constants_for_params dictionary
        return constants_for_params

    def set_fish_nuclear_winter_reduction(self, constants_for_params):
        """
        Set the fish percentages in every country (or globally) from baseline
        although this is a global number, we don't have the regional number, so
        we use the global instead.
        """
        self.scenario_description += "\nreduced fish"
        assert not self.FISH_SET
        constants_for_params["FISH_PERCENT_MONTHLY"] = list(
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
        return constants_for_params

    def set_fish_baseline(self, constants_for_params):
        """
        Sets the baseline for fish by updating the constants_for_params dictionary with
        the necessary values. Also updates the scenario_description attribute of the object.
        Args:
            constants_for_params (dict): dictionary containing the constants for the simulation
        Returns:
            dict: updated dictionary with the baseline fish values
        """
        # Update the scenario description
        self.scenario_description += "\nbaseline fish"

        # Check if fish has already been set
        assert not self.FISH_SET

        # Set the fishing percentage to 100% for all months
        constants_for_params["FISH_PERCENT_MONTHLY"] = np.array(
            [100] * constants_for_params["NMONTHS"]
        )

        # Set the FISH_SET attribute to True
        self.FISH_SET = True

        # Return the updated constants_for_params dictionary
        return constants_for_params

    def set_disruption_to_crops_to_zero(self, constants_for_params):
        """
        Sets the disruption to crops to zero for the given constants_for_params.
        Args:
            self: instance of the class
            constants_for_params (dict): dictionary containing the constants for the parameters
        Returns:
            dict: updated dictionary containing the constants for the parameters
        Raises:
            AssertionError: if the disruption has already been set
        """
        # Add a description of the scenario
        self.scenario_description += "\nno crop disruption"

        # Check if the disruption has already been set
        assert not self.DISRUPTION_SET

        # Set the ratio of crops for each year to 1
        for i in range(1, int(constants_for_params["NMONTHS"] / 12 + 1)):
            constants_for_params["RATIO_CROPS_YEAR" + str(i)] = 1

        # Set the disruption flag to True
        self.DISRUPTION_SET = True

        # Return the updated constants_for_params
        return constants_for_params

    def set_nuclear_winter_global_disruption_to_crops(self, constants_for_params):
        """
        This function sets the ratio of crops for each year after a nuclear winter event.
        Args:
            self: instance of the class
            constants_for_params (dict): dictionary containing the constants for the parameters
        Returns:
            constants_for_params (dict): updated dictionary containing the constants for the parameters
        """
        # Check if the analysis is global
        assert self.IS_GLOBAL_ANALYSIS
        # Add scenario description to the existing one
        self.scenario_description += "\nnuclear winter crops"
        # Check if the disruption is not already set
        assert not self.DISRUPTION_SET

        # Set the ratio of crops for each year after a nuclear winter event
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

        # Set the disruption flag to True
        self.DISRUPTION_SET = True
        # Return the updated dictionary
        return constants_for_params

    def set_nuclear_winter_country_disruption_to_crops(
        self, constants_for_params, country_data
    ):
        """
        This function sets the crop reduction ratios for a country in the event of a nuclear winter.
        Args:
            self: instance of the class
            constants_for_params (dict): dictionary containing the constants for the model
            country_data (dict): dictionary containing the crop reduction ratios for a country
        Returns:
            dict: dictionary containing the updated constants for the model
        """
        # Check that the function is not being called for global analysis
        assert not self.IS_GLOBAL_ANALYSIS
        # Check that the disruption set flag is not already set
        assert not self.DISRUPTION_SET

        # Add scenario description to the existing one
        self.scenario_description += "\nnuclear winter crops"

        # Set the crop reduction ratios for each year
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

        # Set the disruption set flag to True
        self.DISRUPTION_SET = True
        # Return the updated constants
        return constants_for_params

    # PROTEIN

    def include_protein(self, constants_for_params):
        """
        This function sets the INCLUDE_PROTEIN parameter to True in the constants_for_params dictionary
        and updates the scenario_description attribute of the object to include the string "include protein".
        Args:
            self: the object instance
            constants_for_params (dict): a dictionary containing the constants and their values

        Returns:
            dict: the updated constants_for_params dictionary
        """
        # Check if protein has already been set
        assert not self.PROTEIN_SET

        # Update scenario description
        self.scenario_description += "\ninclude protein"

        # Set INCLUDE_PROTEIN to True
        constants_for_params["INCLUDE_PROTEIN"] = True

        # Set protein flag to True
        self.PROTEIN_SET = True

        # Return updated constants_for_params dictionary
        return constants_for_params

    def dont_include_protein(self, constants_for_params):
        """
        This function sets the INCLUDE_PROTEIN parameter to False, indicating that protein should not be included in the simulation.
        Args:
            constants_for_params (dict): a dictionary containing the simulation parameters

        Returns:
            dict: a dictionary containing the updated simulation parameters
        """
        # Check that protein has not already been set
        assert not self.PROTEIN_SET

        # Add scenario description
        self.scenario_description += "\ndon't include protein"

        # Set INCLUDE_PROTEIN parameter to False
        constants_for_params["INCLUDE_PROTEIN"] = False

        # Set protein flag to True
        self.PROTEIN_SET = True

        # Return updated simulation parameters
        return constants_for_params

    def include_fat(self, constants_for_params):
        """
        This function includes the 'fat' parameter in the scenario description and sets the 'INCLUDE_FAT' constant to True.
        Args:
            self: the instance of the class
            constants_for_params (dict): a dictionary containing the constants for the parameters

        Returns:
            dict: the updated dictionary containing the constants for the parameters
        """
        # Check that the 'FAT_SET' attribute is False
        assert not self.FAT_SET

        # Add the 'include fat' string to the scenario description
        self.scenario_description += "\ninclude fat"

        # Set the 'INCLUDE_FAT' constant to True
        constants_for_params["INCLUDE_FAT"] = True

        # Set the 'FAT_SET' attribute to True
        self.FAT_SET = True

        # Return the updated dictionary containing the constants for the parameters
        return constants_for_params

    def dont_include_fat(self, constants_for_params):
        """
        This function sets the INCLUDE_FAT parameter to False in the constants_for_params dictionary
        and updates the scenario_description attribute of the object to indicate that fat should not be included.
        Args:
            self: the object instance
            constants_for_params (dict): a dictionary containing the constants for the parameters

        Returns:
            dict: the updated constants_for_params dictionary
        """
        # Ensure that the FAT_SET attribute is False
        assert not self.FAT_SET

        # Update the scenario_description attribute to indicate that fat should not be included
        self.scenario_description += "\ndon't include fat"

        # Set the INCLUDE_FAT parameter to False in the constants_for_params dictionary
        constants_for_params["INCLUDE_FAT"] = False

        # Set the FAT_SET attribute to True
        self.FAT_SET = True

        # Return the updated constants_for_params dictionary
        return constants_for_params

    def no_resilient_foods(self, constants_for_params):
        """
        This function sets the constants for a scenario where there are no resilient foods.
        Resilient foods are foods that can withstand the effects of abrupt sunlight reduction due to volcano, nuclear winter, or asteroid impact.
        This scenario sets the constants such that there are no resilient foods, which can lead to food insecurity and other issues.

        Args:
            constants_for_params (dict): A dictionary containing the constants for the simulation.

        Returns:
            dict: A dictionary containing the updated constants for the simulation.
        """
        # Set constants to zero or false to remove resilient foods
        constants_for_params["INDUSTRIAL_FOODS_SLOPE_MULTIPLIER"] = 0
        constants_for_params["MAX_SEAWEED_AS_PERCENT_KCALS_HUMANS"] = 0
        constants_for_params["MAX_SEAWEED_AS_PERCENT_KCALS_FEED"] = 0
        constants_for_params["MAX_SEAWEED_AS_PERCENT_KCALS_BIOFUEL"] = 0
        constants_for_params["INITIAL_HARVEST_DURATION_IN_MONTHS"] = 8
        constants_for_params["RATIO_INCREASED_CROP_AREA"] = 1
        constants_for_params["DELAY"]["ROTATION_CHANGE_IN_MONTHS"] = 0

        constants_for_params["OG_USE_BETTER_ROTATION"] = False
        constants_for_params["ADD_CELLULOSIC_SUGAR"] = False
        constants_for_params["ADD_GREENHOUSES"] = False
        constants_for_params["ADD_METHANE_SCP"] = False
        constants_for_params["ADD_SEAWEED"] = False

        return constants_for_params

    def seaweed(self, constants_for_params):
        """
        This function adds seaweed to the simulation by modifying the constants_for_params dictionary.
        Args:
            constants_for_params (dict): A dictionary containing the simulation parameters.

        Returns:
            dict: The modified dictionary with seaweed parameters added.
        """
        # Set the ADD_SEAWEED parameter to True
        constants_for_params["ADD_SEAWEED"] = True

        # Set the DELAY parameter for seaweed to 1 month
        constants_for_params["DELAY"]["SEAWEED_MONTHS"] = 1

        # Set the maximum percentage of kcals that can come from seaweed for humans to 30%
        constants_for_params["MAX_SEAWEED_AS_PERCENT_KCALS_HUMANS"] = 30

        # Set the maximum percentage of kcals that can come from seaweed for feed to 10%
        constants_for_params["MAX_SEAWEED_AS_PERCENT_KCALS_FEED"] = 10
        constants_for_params["MAX_SEAWEED_AS_PERCENT_KCALS_BIOFUEL"] = 10

        # Return the modified dictionary
        return constants_for_params

    def low_area_greenhouse(self, constants_for_params):
        """
        This function sets the constants for a low area greenhouse scenario.

        Args:
            constants_for_params (dict): A dictionary containing the constants for the simulation.

        Returns:
            dict: A dictionary containing the updated constants for the simulation.
        """
        # Set the greenhouse gain percentage to 44
        constants_for_params["GREENHOUSE_GAIN_PCT"] = 44

        # Set the delay for the greenhouse months to 2
        # Half values from greenhouse paper due to higher cost
        constants_for_params["DELAY"]["GREENHOUSE_MONTHS"] = 2

        # Set the greenhouse area multiplier to NaN
        # This will be used to indicate a more realistic, smaller greenhouse area ramp
        constants_for_params["GREENHOUSE_AREA_MULTIPLIER"] = np.nan

        # Set the flag to add greenhouses to True
        constants_for_params["ADD_GREENHOUSES"] = True

        # Return the updated constants
        return constants_for_params

    def greenhouse(self, constants_for_params):
        """
        This function sets the constants for the greenhouse scenario.

        Args:
            constants_for_params (dict): A dictionary containing the constants for the scenario.

        Returns:
            dict: A dictionary containing the updated constants for the scenario.
        """
        # Set the greenhouse gain percentage to 44
        constants_for_params["GREENHOUSE_GAIN_PCT"] = 44

        # Set the delay for the greenhouse months to 2
        # Half values from greenhouse paper due to higher cost
        constants_for_params["DELAY"]["GREENHOUSE_MONTHS"] = 2

        # Set the greenhouse area multiplier to 2.4/39
        constants_for_params["GREENHOUSE_AREA_MULTIPLIER"] = 2.4 / 39

        # Set the flag to add greenhouses to True
        constants_for_params["ADD_GREENHOUSES"] = True

        # Return the updated constants
        return constants_for_params

    def relocated_outdoor_crops(self, constants_for_params):
        """
        This function modifies the constants_for_params dictionary to improve the rotation of outdoor crops.
        It sets the OG_USE_BETTER_ROTATION flag to True, and adjusts the FAT_RATIO, PROTEIN_RATIO, INITIAL_HARVEST_DURATION_IN_MONTHS,
        DELAY_ROTATION_CHANGE_IN_MONTHS, and RATIO_INCREASED_CROP_AREA parameters to improve the rotation of outdoor crops.

        Args:
            constants_for_params (dict): A dictionary containing the parameters for the simulation.

        Returns:
            dict: The modified dictionary of parameters.
        """
        # Set the OG_USE_BETTER_ROTATION flag to True
        constants_for_params["OG_USE_BETTER_ROTATION"] = True

        # Adjust the FAT_RATIO and PROTEIN_RATIO parameters to improve the rotation of outdoor crops
        constants_for_params["ROTATION_IMPROVEMENTS"]["FAT_RATIO"] = 1.647
        constants_for_params["ROTATION_IMPROVEMENTS"]["PROTEIN_RATIO"] = 1.108

        # Adjust the INITIAL_HARVEST_DURATION_IN_MONTHS parameter to improve the rotation of outdoor crops
        constants_for_params["INITIAL_HARVEST_DURATION_IN_MONTHS"] = 7 + 1

        # Adjust the DELAY_ROTATION_CHANGE_IN_MONTHS parameter to improve the rotation of outdoor crops
        constants_for_params["DELAY"]["ROTATION_CHANGE_IN_MONTHS"] = 2

        # Adjust the RATIO_INCREASED_CROP_AREA parameter to improve the rotation of outdoor crops
        constants_for_params["RATIO_INCREASED_CROP_AREA"] = 1

        return constants_for_params

    def expanded_area_and_relocated_outdoor_crops(self, constants_for_params):
        """
        This function expands the area of outdoor crops and relocates them to a better location.
        It modifies the constants_for_params dictionary to include the necessary parameters for this process.

        Args:
            constants_for_params (dict): A dictionary containing the necessary parameters for the simulation.

        Returns:
            dict: The modified constants_for_params dictionary.

        """
        # Set OG_USE_BETTER_ROTATION to True to use a better crop rotation
        constants_for_params["OG_USE_BETTER_ROTATION"] = True

        # Set the FAT_RATIO and PROTEIN_RATIO to improve the nutritional value of the crops
        # This may seem confusing. KCALS_REDUCTION is the reduction that would otherwise
        # occur averaging in year 3 globally
        constants_for_params["ROTATION_IMPROVEMENTS"]["FAT_RATIO"] = 1.647
        constants_for_params["ROTATION_IMPROVEMENTS"]["PROTEIN_RATIO"] = 1.108

        # Set the INITIAL_HARVEST_DURATION_IN_MONTHS to 8 months
        constants_for_params["INITIAL_HARVEST_DURATION_IN_MONTHS"] = 7 + 1

        # Set the ROTATION_CHANGE_IN_MONTHS to 2 months
        constants_for_params["DELAY"]["ROTATION_CHANGE_IN_MONTHS"] = 2

        # Set the RATIO_INCREASED_CROP_AREA to 72/39
        constants_for_params["RATIO_INCREASED_CROP_AREA"] = 72 / 39

        # Set the NUMBER_YEARS_TAKES_TO_REACH_INCREASED_AREA to 3 years
        constants_for_params["NUMBER_YEARS_TAKES_TO_REACH_INCREASED_AREA"] = 3

        # Return the modified constants_for_params dictionary
        return constants_for_params

    def methane_scp(self, constants_for_params):
        """
        This function modifies the input dictionary of constants to include a new key-value pair
        that enables the addition of methane SCP to the model. It also modifies two existing keys
        in the dictionary to set default values from CS and SCP papers.

        Args:
            constants_for_params (dict): A dictionary of constants used in the model

        Returns:
            dict: The modified dictionary of constants with the new key-value pair added
        """
        # Set default values for DELAY and INDUSTRIAL_FOODS_SLOPE_MULTIPLIER
        constants_for_params["DELAY"]["INDUSTRIAL_FOODS_MONTHS"] = 3
        constants_for_params["INDUSTRIAL_FOODS_SLOPE_MULTIPLIER"] = 1

        # Enable addition of methane SCP
        constants_for_params["ADD_METHANE_SCP"] = True

        return constants_for_params

    def cellulosic_sugar(self, constants_for_params):
        """
        This function modifies the constants_for_params dictionary to include a delay of 3 months for
        industrial foods and a slope multiplier of 1 for industrial foods. It also sets the ADD_CELLULOSIC_SUGAR
        flag to True.
        Args:
            constants_for_params (dict): A dictionary containing constants for the model parameters
        Returns:
            dict: The modified constants_for_params dictionary
        """
        # Set delay for industrial foods to 3 months
        constants_for_params["DELAY"]["INDUSTRIAL_FOODS_MONTHS"] = 3

        # Set slope multiplier for industrial foods to 1
        constants_for_params["INDUSTRIAL_FOODS_SLOPE_MULTIPLIER"] = 1

        # Set ADD_CELLULOSIC_SUGAR flag to True
        constants_for_params["ADD_CELLULOSIC_SUGAR"] = True

        # Return the modified constants_for_params dictionary
        return constants_for_params

    def get_all_resilient_foods_scenario(self, constants_for_params):
        """
        This function sets the scenario for all resilient foods by calling several other functions
        that modify the constants_for_params argument. It then sets the SCENARIO_SET flag to True
        and returns the modified constants_for_params.

        Args:
            constants_for_params (dict): a dictionary of constants used in the simulation

        Returns:
            dict: the modified constants_for_params with the scenario for all resilient foods set

        Raises:
            AssertionError: if the SCENARIO_SET flag is already True

        """
        # Add scenario description to the existing one
        self.scenario_description += "\nall resilient foods"

        # Ensure that the SCENARIO_SET flag is False
        assert not self.SCENARIO_SET

        # Call several functions to modify the constants_for_params argument
        constants_for_params = self.relocated_outdoor_crops(constants_for_params)
        constants_for_params = self.methane_scp(constants_for_params)
        constants_for_params = self.cellulosic_sugar(constants_for_params)
        constants_for_params = self.low_area_greenhouse(constants_for_params)
        constants_for_params = self.seaweed(constants_for_params)

        # Set the SCENARIO_SET flag to True
        self.SCENARIO_SET = True

        # Return the modified constants_for_params
        return constants_for_params

    def get_all_resilient_foods_and_more_area_scenario(self, constants_for_params):
        """
        This function sets a scenario for all resilient foods and more area. It expands the area and relocates outdoor crops,
        applies methane SCP, cellulosic sugar, greenhouse, and seaweed. It then sets the scenario and returns the constants
        for parameters.

        Args:
            self: instance of the class
            constants_for_params (dict): dictionary of constants for parameters

        Returns:
            dict: dictionary of constants for parameters with the scenario set

        Raises:
            AssertionError: if the scenario set is already True

        """
        # Add scenario description
        self.scenario_description += "\nall resilient foods"

        # Check if scenario is already set
        assert not self.SCENARIO_SET

        # Expand area and relocate outdoor crops
        constants_for_params = self.expanded_area_and_relocated_outdoor_crops(
            constants_for_params
        )

        # Apply methane SCP
        constants_for_params = self.methane_scp(constants_for_params)

        # Apply cellulosic sugar
        constants_for_params = self.cellulosic_sugar(constants_for_params)

        # Apply greenhouse
        constants_for_params = self.greenhouse(constants_for_params)

        # Apply seaweed
        constants_for_params = self.seaweed(constants_for_params)

        # Set scenario
        self.SCENARIO_SET = True

        # Return constants for parameters with scenario set
        return constants_for_params

    def get_seaweed_scenario(self, constants_for_params):
        """
        This function sets the constants for a seaweed scenario and returns them.
        It also updates the scenario description and sets the SCENARIO_SET flag to True.

        Args:
            constants_for_params (dict): a dictionary of constants for the scenario

        Returns:
            dict: a dictionary of updated constants for the seaweed scenario
        """
        # Update the scenario description
        self.scenario_description += "\nscaled up seaweed"

        # Ensure that the scenario has not already been set
        assert not self.SCENARIO_SET

        # Set the constants for the seaweed scenario
        constants_for_params["INDUSTRIAL_FOODS_SLOPE_MULTIPLIER"] = 0
        constants_for_params["INITIAL_HARVEST_DURATION_IN_MONTHS"] = 8
        constants_for_params["OG_USE_BETTER_ROTATION"] = False
        constants_for_params["ADD_CELLULOSIC_SUGAR"] = False
        constants_for_params["ADD_GREENHOUSES"] = False
        constants_for_params["ADD_METHANE_SCP"] = False
        constants_for_params = self.seaweed(constants_for_params)

        # Set the SCENARIO_SET flag to True
        self.SCENARIO_SET = True

        # Return the updated constants for the seaweed scenario
        return constants_for_params

    def get_methane_scp_scenario(self, constants_for_params):
        """
        This function sets up the parameters for a scaled up methane SCP scenario.
        It modifies the constants_for_params dictionary to reflect the new scenario.

        Args:
            constants_for_params (dict): A dictionary containing the parameters for the scenario.

        Returns:
            dict: A dictionary containing the modified parameters for the scenario.
        """
        # Add a description of the scenario to the scenario_description attribute
        self.scenario_description += "\nscaled up methane SCP"

        # Ensure that the scenario set flag is not already set
        assert not self.SCENARIO_SET

        # Modify the constants_for_params dictionary to reflect the new scenario
        constants_for_params["MAX_SEAWEED_AS_PERCENT_KCALS_HUMANS"] = 0
        constants_for_params["MAX_SEAWEED_AS_PERCENT_KCALS_FEED"] = 0
        constants_for_params["MAX_SEAWEED_AS_PERCENT_KCALS_BIOFUEL"] = 0

        constants_for_params["INITIAL_HARVEST_DURATION_IN_MONTHS"] = 8
        constants_for_params["OG_USE_BETTER_ROTATION"] = False
        constants_for_params["ADD_CELLULOSIC_SUGAR"] = False
        constants_for_params["ADD_GREENHOUSES"] = False
        constants_for_params["ADD_SEAWEED"] = False
        constants_for_params = self.methane_scp(constants_for_params)

        # Set the scenario set flag to True
        self.SCENARIO_SET = True

        # Return the modified constants_for_params dictionary
        return constants_for_params

    def get_cellulosic_sugar_scenario(self, constants_for_params):
        """
        This function sets the parameters for a scenario where cellulosic sugar is scaled up.
        Args:
            constants_for_params (dict): a dictionary of parameters for the model

        Returns:
            dict: a dictionary of updated parameters for the model
        """
        # Add a description of the scenario to the scenario_description attribute
        self.scenario_description += "\nscaled up cellulosic sugar"

        # Ensure that the scenario set flag is not already set
        assert not self.SCENARIO_SET

        # Set the maximum percentage of kcals from seaweed to 0 for both humans and feed
        constants_for_params["MAX_SEAWEED_AS_PERCENT_KCALS_HUMANS"] = 0
        constants_for_params["MAX_SEAWEED_AS_PERCENT_KCALS_FEED"] = 0
        constants_for_params["MAX_SEAWEED_AS_PERCENT_KCALS_BIOFUEL"] = 0

        # Set the initial harvest duration in months to 8
        constants_for_params["INITIAL_HARVEST_DURATION_IN_MONTHS"] = 8

        # Set various flags to False to exclude certain features from the scenario
        constants_for_params["OG_USE_BETTER_ROTATION"] = False
        constants_for_params["ADD_METHANE_SCP"] = False
        constants_for_params["ADD_GREENHOUSES"] = False
        constants_for_params["ADD_SEAWEED"] = False

        # Call the cellulosic_sugar function to update the parameters for the scenario
        constants_for_params = self.cellulosic_sugar(constants_for_params)

        # Set the scenario set flag to True
        self.SCENARIO_SET = True

        # Return the updated parameters
        return constants_for_params

    def get_relocated_crops_scenario(self, constants_for_params):
        """
        This function sets up a scenario where cold crops are scaled up and other crops are scaled down.
        It also sets some constants to zero and some to False.
        Args:
            constants_for_params (dict): a dictionary of constants used in the model

        Returns:
            dict: a dictionary of constants used in the model with some constants set to zero and some to False
        """
        # Add a description of the scenario to the existing scenario description
        self.scenario_description += "\nscaled up cold crops"

        # Ensure that the scenario has not already been set
        assert not self.SCENARIO_SET

        # Set some constants to zero
        constants_for_params["INDUSTRIAL_FOODS_SLOPE_MULTIPLIER"] = 0
        constants_for_params["MAX_SEAWEED_AS_PERCENT_KCALS_HUMANS"] = 0
        constants_for_params["MAX_SEAWEED_AS_PERCENT_KCALS_FEED"] = 0
        constants_for_params["MAX_SEAWEED_AS_PERCENT_KCALS_BIOFUEL"] = 0

        # Set some constants to False
        constants_for_params["ADD_CELLULOSIC_SUGAR"] = False
        constants_for_params["ADD_GREENHOUSES"] = False
        constants_for_params["ADD_METHANE_SCP"] = False
        constants_for_params["ADD_SEAWEED"] = False

        # Call the relocated_outdoor_crops function to set up the scenario
        constants_for_params = self.relocated_outdoor_crops(constants_for_params)

        # Set the scenario flag to True
        self.SCENARIO_SET = True

        # Return the updated constants dictionary
        return constants_for_params

    def get_greenhouse_scenario(self, constants_for_params):
        """
        This function sets up a scenario for scaled up greenhouses by modifying the constants_for_params dictionary.
        It also updates the scenario_description attribute of the class instance.
        Args:
            constants_for_params (dict): A dictionary containing the model parameters and their values.

        Returns:
            dict: A dictionary containing the modified model parameters and their values.
        """
        # Update the scenario description
        self.scenario_description += "\nscaled up greenhouses"

        # Ensure that the scenario has not already been set
        assert not self.SCENARIO_SET

        # Modify the constants_for_params dictionary to set up the greenhouse scenario
        constants_for_params["INDUSTRIAL_FOODS_SLOPE_MULTIPLIER"] = 0
        constants_for_params["MAX_SEAWEED_AS_PERCENT_KCALS_HUMANS"] = 0
        constants_for_params["MAX_SEAWEED_AS_PERCENT_KCALS_FEED"] = 0
        constants_for_params["MAX_SEAWEED_AS_PERCENT_KCALS_BIOFUEL"] = 0

        constants_for_params["INITIAL_HARVEST_DURATION_IN_MONTHS"] = 8
        constants_for_params["OG_USE_BETTER_ROTATION"] = False
        constants_for_params["ADD_CELLULOSIC_SUGAR"] = False
        constants_for_params["ADD_METHANE_SCP"] = False
        constants_for_params["ADD_SEAWEED"] = False
        constants_for_params = self.greenhouse(constants_for_params)

        # Set the scenario flag to True
        self.SCENARIO_SET = True

        # Return the modified constants_for_params dictionary
        return constants_for_params

    def get_no_resilient_food_scenario(self, constants_for_params):
        """
        This function sets the scenario to have no resilient foods and returns the updated constants_for_params.
        Args:
            constants_for_params (dict): a dictionary of constants used in the simulation

        Returns:
            dict: the updated constants_for_params with no resilient foods

        Raises:
            AssertionError: if the scenario has already been set

        """
        # Add scenario description
        self.scenario_description += "\nno resilient foods"

        # Check if scenario has already been set
        assert not self.SCENARIO_SET

        # Update constants_for_params to have no resilient foods
        constants_for_params = self.no_resilient_foods(constants_for_params)

        # Set scenario as set
        self.SCENARIO_SET = True

        # Return updated constants_for_params
        return constants_for_params

        # CULLING

    def cull_animals(self, constants_for_params):
        """
        This function sets a flag to cull animals and adds a description to the scenario.
        Args:
            constants_for_params (dict): a dictionary of constants for the simulation

        Returns:
            dict: the updated dictionary of constants for the simulation
        """
        # Check that the culling parameter has not already been set
        assert not self.CULLING_PARAM_SET

        # Add a description of the scenario to the simulation
        self.scenario_description += "\ncull animals"

        # Set the flag to add culled meat
        constants_for_params["ADD_CULLED_MEAT"] = True

        # Set the culling parameter flag to True
        self.CULLING_PARAM_SET = True

        # Return the updated dictionary of constants for the simulation
        return constants_for_params

    def dont_cull_animals(self, constants_for_params):
        """
        This function sets a parameter to prevent the culling of animals and updates the scenario description.
        Args:
            self: instance of the class
            constants_for_params (dict): dictionary of parameters to be used in the simulation

        Returns:
            dict: updated dictionary of parameters
        """
        # Check if the culling parameter has already been set
        assert not self.CULLING_PARAM_SET

        # Update the scenario description to indicate that no animals will be culled
        self.scenario_description += "\nno culled animals"

        # Set the parameter to prevent the culling of animals
        constants_for_params["ADD_CULLED_MEAT"] = False

        # Set the culling parameter to True to indicate that it has been set
        self.CULLING_PARAM_SET = True

        # Return the updated dictionary of parameters
        return constants_for_params
