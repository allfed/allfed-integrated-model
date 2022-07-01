################################Optimizer Model################################
##                                                                            #
## In this model, we estimate the macronutrient production allocated optimally#
##  over time including models for traditional and resilient foods.           #
##                                                                            #
###############################################################################

import os
import sys
import numpy as np
from src.constants import Constants
from src.analysis import Analyzer
from src.validate import Validator
import pulp
from pulp import LpMaximize, LpProblem, LpVariable

module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)

class Optimizer:

    def __init__(self):
        pass

    def optimize(self, single_valued_constants,multi_valued_constants):
        maximize_constraints = []  # used only for validation

        # Create the model to optimize
        model = LpProblem(name="optimization_nutrition", sense=LpMaximize)

        variables = {}

        variables["objective_function"] = LpVariable(name="Least_Humans_Fed_Any_Month", lowBound=0)


        self.single_valued_constants = single_valued_constants
        self.multi_valued_constants = multi_valued_constants

        #### MODEL GENERATION LOOP ####
        self.time_days_monthly = []
        self.time_days_daily = []
        self.time_months = []
        self.time_days_middle = []
        self.time_months_middle = []

        NDAYS = single_valued_constants["NDAYS"]
        NMONTHS = single_valued_constants["NMONTHS"]

        variables["stored_food_start"] = [0] * NMONTHS
        variables["stored_food_end"] = [0] * NMONTHS
        variables["stored_food_eaten"] = [0] * NMONTHS

        variables["seaweed_wet_on_farm"] = [0] * NDAYS
        variables["seaweed_food_produced"] = [0] * NDAYS
        variables["used_area"] = [0] * NDAYS
        variables["seaweed_food_produced_monthly"] = [0] * NMONTHS

        variables["crops_food_storage_no_rotation"] = [0] * NMONTHS
        variables["crops_food_storage_rotation"] = [0] * NMONTHS
        variables["crops_food_eaten_with_rotation"] = [0] * NMONTHS
        variables["crops_food_eaten_no_rotation"] = [0] * NMONTHS

        variables["humans_fed_kcals"] = [0] * NMONTHS
        variables["humans_fed_fat"] = [0] * NMONTHS
        variables["humans_fed_protein"] = [0] * NMONTHS

        for month in range(0, self.single_valued_constants["NMONTHS"]):
            self.time_days_middle.append(single_valued_constants["DAYS_IN_MONTH"] * (month + 0.5))
            self.time_days_monthly.append(single_valued_constants["DAYS_IN_MONTH"] * month)
            self.time_days_monthly.append(single_valued_constants["DAYS_IN_MONTH"] * (month + 1))
            self.time_months.append(month)
            self.time_months.append(month + 1)
            self.time_months_middle.append(month + 0.5)

            if(single_valued_constants["ADD_SEAWEED"]):
                (model, variables) = self.add_seaweed_to_model(model, variables, month)

            if(single_valued_constants["ADD_OUTDOOR_GROWING"]):
                (model, variables) = self.add_outdoor_crops_to_model(model, variables, month)

            if(single_valued_constants["ADD_STORED_FOOD"]):
                (model, variables) = self.add_stored_food_to_model(model, variables, month)

            [model, variables, maximize_constraints] = \
                self.add_objectives_to_model(model, variables, month, maximize_constraints)

        model += variables["objective_function"]
        status = model.solve(pulp.PULP_CBC_CMD(gapRel=0.0001,
            msg = single_valued_constants["VERBOSE"]))
        assert(status == 1)

        if(single_valued_constants["VERBOSE"]):
            print('optimization successful')

        if(single_valued_constants['CHECK_CONSTRAINTS']):
            print('')
            print('VALIDATION')
            print('')
            print('')
            Validator.checkConstraintsSatisfied(
                model,
                status,
                maximize_constraints,
                model.variables(),
                single_valued_constants["VERBOSE"])

        analysis = Analyzer(single_valued_constants)

        show_output = False

        analysis.compute_excess_after_run(model)

        analysis.scenario_is_impossible = False

        analysis.calc_fraction_OG_SF_to_humans(
            model,
            variables["crops_food_eaten_no_rotation"],
            variables["crops_food_eaten_with_rotation"],
            variables["stored_food_eaten"],
            multi_valued_constants["excess_kcals"],
            multi_valued_constants["excess_fat_used"],
            multi_valued_constants["excess_protein_used"]
        )

        if(analysis.scenario_is_impossible):
            if(single_valued_constants["VERBOSE"]):
                print("")
                print("Scenario is impossible")
                print("")
            analysis.people_fed_billions = np.nan
            return [np.nan, np.nan, analysis]

        # if no stored food, will be zero
        analysis.analyze_SF_results(
            variables["stored_food_eaten"],
            show_output
        )
        # extract numeric seaweed results in terms of people fed and raw tons wet
        # if seaweed not added to model, will be zero
        analysis.analyze_seaweed_results(
            variables["seaweed_wet_on_farm"],
            variables["used_area"],
            multi_valued_constants["built_area"],
            variables["seaweed_food_produced"],  # daily
            variables["seaweed_food_produced_monthly"],
            show_output
        )

        # if no cellulosic sugar, will be zero
        analysis.analyze_CS_results(
            multi_valued_constants["production_kcals_CS_per_month"],
        )

        # if no scp, will be zero
        analysis.analyze_SCP_results(
            multi_valued_constants["production_kcals_scp_per_month"],
            multi_valued_constants["production_fat_scp_per_month"],
            multi_valued_constants["production_protein_scp_per_month"],
        )

        # if no fish, will be zero
        analysis.analyze_fish_results(
            multi_valued_constants["production_kcals_fish_per_month"],
            multi_valued_constants["production_fat_fish_per_month"],
            multi_valued_constants["production_protein_fish_per_month"],
        )

        # if no greenhouses, will be zero
        analysis.analyze_GH_results(
            multi_valued_constants["greenhouse_kcals_per_ha"],
            multi_valued_constants["greenhouse_fat_per_ha"],
            multi_valued_constants["greenhouse_protein_per_ha"],
            multi_valued_constants["greenhouse_area"],
            show_output
        )

        # if no outdoor food, will be zero
        analysis.analyze_OG_results(
            variables["crops_food_eaten_no_rotation"],
            variables["crops_food_eaten_with_rotation"],
            variables["crops_food_storage_no_rotation"],
            variables["crops_food_storage_rotation"],
            multi_valued_constants["crops_food_produced"],
            show_output
        )

        # if nonegg nondairy meat isn't included, these results will be zero
        analysis.analyze_meat_dairy_results(
            multi_valued_constants["meat_eaten"],
            multi_valued_constants["dairy_milk_kcals"],
            multi_valued_constants["dairy_milk_fat"],
            multi_valued_constants["dairy_milk_protein"],
            multi_valued_constants["cattle_maintained_kcals"],
            multi_valued_constants["cattle_maintained_fat"],
            multi_valued_constants["cattle_maintained_protein"],
            multi_valued_constants["h_e_meat_kcals"],
            multi_valued_constants["h_e_meat_fat"],
            multi_valued_constants["h_e_meat_protein"],
            multi_valued_constants["h_e_milk_kcals"],
            multi_valued_constants["h_e_milk_fat"],
            multi_valued_constants["h_e_milk_protein"],
            multi_valued_constants["h_e_balance_kcals"],
            multi_valued_constants["h_e_balance_fat"],
            multi_valued_constants["h_e_balance_protein"],
        )

        analysis.analyze_results(model, self.time_months_middle)

        return [self.time_months, self.time_months_middle, analysis]

    def add_seaweed_to_model(self, model, variables, month):
        standard_deviation = self.single_valued_constants["inputs"]["DELAY"]["SEAWEED_MONTHS"]
        sum_food_this_month = []
        #assume that the only harvest opportunity is once a month
        if month > (15 + standard_deviation):
            variables["seaweed_food_produced_monthly"][month] = LpVariable(name="Seaweed_Food_Produced_Monthly_"+str(month)+"_Variable", lowBound=0)
            return (model, variables)

        else:
            for day in np.arange(month*self.single_valued_constants["DAYS_IN_MONTH"], (month + 1)*self.single_valued_constants["DAYS_IN_MONTH"]):
                self.time_days_daily.append(day)
                variables["seaweed_wet_on_farm"][day] = LpVariable(
                    "Seaweed_Wet_On_Farm_"
                    + str(day)
                    + "_Variable",
                    self.single_valued_constants["INITIAL_SEAWEED"],
                    self.single_valued_constants["MAXIMUM_DENSITY"] * self.multi_valued_constants["built_area"][day])

                # food production (using resources)
                variables["seaweed_food_produced"][day] = LpVariable(
                    name="Seaweed_Food_Produced_During_Day_"+str(day)+"_Variable", lowBound=0)

                variables["used_area"][day] = LpVariable(
                    "Used_Area_"+str(day)+"_Variable", self.single_valued_constants["INITIAL_AREA"], self.multi_valued_constants["built_area"][day])

                if(day == 0):  # first Day
                    model += (variables["seaweed_wet_on_farm"][0] == self.single_valued_constants["INITIAL_SEAWEED"],
                              "Seaweed_Wet_On_Farm_0_Constraint")
                    model += (variables["used_area"][0] == self.single_valued_constants["INITIAL_AREA"],
                              "Used_Area_Day_0_Constraint")
                    model += (variables["seaweed_food_produced"][0] == 0,
                              "Seaweed_Food_Produced_Day_0_Constraint")

                else:  # later Days
                    model += (variables["seaweed_wet_on_farm"][day] <= variables["used_area"]
                              [day] * self.single_valued_constants["MAXIMUM_DENSITY"])

                    model += (variables["seaweed_wet_on_farm"][day] ==
                              variables["seaweed_wet_on_farm"][day-1] *
                              (1+self.single_valued_constants["inputs"]["SEAWEED_PRODUCTION_RATE"]/100.)
                              - variables["seaweed_food_produced"][day]
                              - (variables["used_area"][day]-variables["used_area"][day-1]) *
                              self.single_valued_constants["MINIMUM_DENSITY"]
                              * (self.single_valued_constants["HARVEST_LOSS"] / 100),
                              "Seaweed_Wet_On_Farm_"+str(day)+"_Constraint")

                sum_food_this_month.append(variables["seaweed_food_produced"][day])

        variables["seaweed_food_produced_monthly"][month] = LpVariable(
            name="Seaweed_Food_Produced_Monthly_" + str(month) + "_Variable", lowBound=0)

        model += (variables["seaweed_food_produced_monthly"][month] == np.sum(sum_food_this_month),
                  "Seaweed_Food_Produced_Monthly_" + str(month) + "_Constraint")

        return (model, variables)

    # incorporate linear constraints for stored food consumption each month
    def add_stored_food_to_model(self, model, variables, month):
        variables["stored_food_start"][month] = LpVariable(
            "Stored_Food_Start_Month_" + str(month) + "_Variable", 0, self.single_valued_constants["INITIAL_SF_KCALS"])
        variables["stored_food_end"][month] = LpVariable(
            "Stored_Food_End_Month_" + str(month) + "_Variable", 0, self.single_valued_constants["INITIAL_SF_KCALS"])
        variables["stored_food_eaten"][month] = LpVariable(
            "Stored_Food_Eaten_During_Month_" + str(month) + "_Variable", 0, self.single_valued_constants["INITIAL_SF_KCALS"])

        if(month == 0):  # first Month
            model += (variables["stored_food_start"][0] == self.single_valued_constants["INITIAL_SF_KCALS"],
                      "Stored_Food_Start_Month_0_Constraint")
        else:
            model += (variables["stored_food_start"][month] == variables["stored_food_end"][month - 1],
                      "Stored_Food_Start_Month_" + str(month) + "_Constraint")

            ##### helps reduce wild fluctutions in stored food #######
            if(month > 0 and self.single_valued_constants['inputs']["STORED_FOOD_SMOOTHING"]):
                model += (variables["stored_food_eaten"][month] <= variables["stored_food_eaten"][month - 1] * self.single_valued_constants["inputs"]
                          ["FLUCTUATION_LIMIT"], "Small_Change_Plus_SF_Eaten_Month_" + str(month) + "_Constraint")

                model += (variables["stored_food_eaten"][month] >= variables["stored_food_eaten"][month - 1] * (1/self.single_valued_constants["inputs"]
                ["FLUCTUATION_LIMIT"]), "Small_Change_Minus_SF_Eaten_Month_" + str(month) + "_Constraint")
                pass

        model += (variables["stored_food_end"][month] == variables["stored_food_start"][month] -
                  variables["stored_food_eaten"][month], "Stored_Food_End_Month_" + str(month) + "_Constraint")

        return (model, variables)

    # incorporate linear constraints for stored food consumption each month
    def add_outdoor_crops_to_model(self, model, variables, month):

        variables["crops_food_storage_rotation"][month] = \
            LpVariable(
                "Crops_Food_Storage_Rotation_Month_" + str(month) + "_Variable",
                lowBound=0)
        variables["crops_food_storage_no_rotation"][month] = \
            LpVariable(
                "Crops_Food_Storage_No_Rotation_Month_" + str(month) + "_Variable",
                lowBound=0)

        variables["crops_food_eaten_with_rotation"][month] = \
            LpVariable(
                "Crops_Food_Eaten_Rotation_During_Month_" + str(month) + "_Variable",
                lowBound=0
        )
        variables["crops_food_eaten_no_rotation"][month] = \
            LpVariable(
                "Crops_Food_Eaten_No_Rotation_During_Month_" + str(month) + "_Variable",
                lowBound=0)

        if(month == 0):

            model += (
                variables["crops_food_storage_no_rotation"][month] ==
                self.multi_valued_constants["crops_food_produced"][month]
                - variables["crops_food_eaten_no_rotation"][month],
                "Crops_Food_Storage_No_Rotation_" + str(month) + "_Constraint"
            )

            model += (
                variables["crops_food_storage_rotation"][month] == 0,
                "Crops_Food_Storage_Rotation_" + str(month) + "_Constraint"
            )

            model += (
                variables["crops_food_eaten_with_rotation"][month] == 0,
                "Crops_Food_Eaten_Rotation_" + str(month) + "_Constraint"
            )

        elif(month == self.single_valued_constants["NMONTHS"] - 1):
            # haven't dealt with the case of nmonths being less than initial harvest
            assert(month > self.single_valued_constants["inputs"]["INITIAL_HARVEST_DURATION_IN_MONTHS"])

            model += (
                variables["crops_food_storage_no_rotation"][month] == 0,
                "Crops_Food_No_Rotation_None_Left_" + str(month) + "_Constraint"
            )

            model += (
                variables["crops_food_storage_rotation"][month] == 0,
                "Crops_Food_Rotation_None_Left_" + str(month) + "_Constraint"
            )

            model += (
                variables["crops_food_storage_rotation"][month]
                == self.multi_valued_constants["crops_food_produced"][month]
                - variables["crops_food_eaten_with_rotation"][month]
                + variables["crops_food_storage_rotation"][month - 1],
                "Crops_Food_Rotation_Storage_" + str(month) + "_Constraint"
            )

            model += (
                variables["crops_food_storage_no_rotation"][month]
                == variables["crops_food_storage_no_rotation"][month - 1]
                - variables["crops_food_eaten_no_rotation"][month],
                "Crops_Food_No_Rotation_Storage_" + str(month) + "_Constraint")

        elif(month < self.single_valued_constants["inputs"]["INITIAL_HARVEST_DURATION_IN_MONTHS"]):

            model += (
                variables["crops_food_storage_rotation"][month] == 0,
                "Crops_Food_Storage_Rotation" + str(month) + "_Constraint"
            )

            model += (
                variables["crops_food_eaten_with_rotation"][month] == 0,
                "Crops_Food_Eaten_Rotation" + str(month) + "_Constraint"
            )

            model += (
                variables["crops_food_storage_no_rotation"][month]
                == self.multi_valued_constants["crops_food_produced"][month]
                - variables["crops_food_eaten_no_rotation"][month]
                + variables["crops_food_storage_no_rotation"][month - 1],
                "Crops_Food_Storage_No_Rotation_" + str(month) + "_Constraint"
            )

        else:  # now produinputs_to_optimizerg rotation, but can still eat "no rotation" storage

            model += (
                variables["crops_food_storage_rotation"][month]
                == self.multi_valued_constants["crops_food_produced"][month]
                - variables["crops_food_eaten_with_rotation"][month]
                + variables["crops_food_storage_rotation"][month - 1],
                "Crops_Food_Storage_Rotation_" + str(month) + "_Constraint"
            )

            model += (
                variables["crops_food_storage_no_rotation"][month]
                == variables["crops_food_storage_no_rotation"][month - 1]
                - variables["crops_food_eaten_no_rotation"][month],
                "Crops_Food_Storage_No_Rotation_" + str(month) + "_Constraint")

        return (model, variables)

    #### OBJECTIVE FUNCTIONS  ####

    def add_objectives_to_model(self, model, variables, month, maximize_constraints):
        variables["humans_fed_kcals"][month] = \
            LpVariable(name="Humans_Fed_Kcals_" + str(month) + "_Variable", lowBound=0)
        variables["humans_fed_fat"][month] = \
            LpVariable(name="Humans_Fed_Fat_" + str(month) + "_Variable", lowBound=0)
        variables["humans_fed_protein"][month] = \
            LpVariable(name="Humans_Fed_Protein_" + str(month) + "_Variable", lowBound=0)

        if(self.single_valued_constants["ADD_SEAWEED"]):
            # after month 15, enforce maximum seaweed production to prevent
            # a rounding error from full quantity of seaweed
            standard_deviation = self.single_valued_constants["inputs"]["DELAY"]["SEAWEED_MONTHS"]

            if month > (15 + standard_deviation):
               model += (variables["seaweed_food_produced_monthly"][month] * self.single_valued_constants["SEAWEED_KCALS"] ==
                         (self.single_valued_constants["inputs"]["MAX_SEAWEED_AS_PERCENT_KCALS"]/100)
                          * (self.single_valued_constants["POP"] / 1e9 * self.single_valued_constants["KCALS_MONTHLY"]),
                          "Seaweed_Limit_Kcals_" + str(month) + "_Constraint")
            else:
                model += (variables["seaweed_food_produced_monthly"][month] * self.single_valued_constants["SEAWEED_KCALS"] <=
                          (self.single_valued_constants["inputs"]["MAX_SEAWEED_AS_PERCENT_KCALS"]/100)
                          * (self.single_valued_constants["POP"] / 1e9 * self.single_valued_constants["KCALS_MONTHLY"]),
                          "Seaweed_Limit_Kcals_" + str(month) + "_Constraint")

        # finds billions of people fed that month per nutrient

        # stored food eaten*sf_fraction_kcals is in units billions kcals monthly
        # seaweed_food_produced_monthly*seaweed_kcals is in units billions kcals
        # kcals monthly is in units kcals
        CROPS_WASTE = 1-self.single_valued_constants["inputs"]["WASTE"]["CROPS"]/100

        model += (variables["humans_fed_kcals"][month]
                  == (variables["stored_food_eaten"][month] * CROPS_WASTE
                      + variables["crops_food_eaten_no_rotation"][month] * CROPS_WASTE
                      + variables["crops_food_eaten_with_rotation"][month] *
                      self.single_valued_constants["OG_ROTATION_FRACTION_KCALS"] * CROPS_WASTE
                      - self.multi_valued_constants["excess_kcals"][month] * CROPS_WASTE
                      + variables["seaweed_food_produced_monthly"][month] * self.single_valued_constants["SEAWEED_KCALS"]
                      + self.multi_valued_constants["dairy_milk_kcals"][month]
                      + self.multi_valued_constants["cattle_maintained_kcals"][month]
                      + self.multi_valued_constants["meat_eaten"][month]
                      + self.multi_valued_constants["production_kcals_CS_per_month"][month]
                      + self.multi_valued_constants["production_kcals_scp_per_month"][month]
                      + self.multi_valued_constants["greenhouse_area"][month] * self.multi_valued_constants["greenhouse_kcals_per_ha"][month]
                      + self.multi_valued_constants["production_kcals_fish_per_month"][month]
                      + self.multi_valued_constants["h_e_created_kcals"][month]
                      )/self.single_valued_constants["POP_MILLIONS"],
                  "Kcals_Fed_Month_" + str(month) + "_Constraint")

        if(self.single_valued_constants['inputs']['INCLUDE_FAT']):
            # fat monthly is in units thousand tons
            model += (variables["humans_fed_fat"][month] ==
                      (variables["stored_food_eaten"][month] * self.single_valued_constants["SF_FRACTION_FAT"]
                       * CROPS_WASTE
                       + variables["crops_food_eaten_no_rotation"][month]
                       * self.single_valued_constants["OG_FRACTION_FAT"] * CROPS_WASTE
                       + variables["crops_food_eaten_with_rotation"][month]
                       * self.single_valued_constants["OG_ROTATION_FRACTION_FAT"]
                       * CROPS_WASTE
                       - self.multi_valued_constants["excess_fat_used"][month] * CROPS_WASTE
                       + variables["seaweed_food_produced_monthly"][month] * self.single_valued_constants["SEAWEED_FAT"]
                       + self.multi_valued_constants["dairy_milk_fat"][month]
                       + self.multi_valued_constants["cattle_maintained_fat"][month]
                       + self.multi_valued_constants["meat_eaten"][month] * self.single_valued_constants["MEAT_FRACTION_FAT"]
                       + self.multi_valued_constants["production_fat_scp_per_month"][month]
                       + self.multi_valued_constants["greenhouse_area"][month] * self.multi_valued_constants["greenhouse_fat_per_ha"][month]
                       + self.multi_valued_constants["production_fat_fish_per_month"][month]
                       + self.multi_valued_constants["h_e_created_fat"][month])
                      / self.single_valued_constants["FAT_MONTHLY"] / 1e9,
                      "Fat_Fed_Month_" + str(month) + "_Constraint")

        if(self.single_valued_constants['inputs']['INCLUDE_PROTEIN']):

            model += (variables["humans_fed_protein"][month] ==
                      (variables["stored_food_eaten"][month] * self.single_valued_constants["SF_FRACTION_PROTEIN"]
                       * CROPS_WASTE
                       + variables["crops_food_eaten_no_rotation"][month]
                       * self.single_valued_constants["OG_FRACTION_PROTEIN"] * CROPS_WASTE
                       + variables["crops_food_eaten_with_rotation"][month]
                       * self.single_valued_constants["OG_ROTATION_FRACTION_PROTEIN"] * CROPS_WASTE
                       - self.multi_valued_constants["excess_protein_used"][month] * CROPS_WASTE
                       + variables["seaweed_food_produced_monthly"][month] * self.single_valued_constants["SEAWEED_PROTEIN"]
                       + self.multi_valued_constants["dairy_milk_protein"][month]
                       + self.multi_valued_constants["cattle_maintained_protein"][month]
                       + self.multi_valued_constants["production_protein_scp_per_month"][month]
                       + self.multi_valued_constants["meat_eaten"][month] * self.single_valued_constants["MEAT_FRACTION_PROTEIN"]
                       + self.multi_valued_constants["greenhouse_area"][month] * self.multi_valued_constants["greenhouse_protein_per_ha"][month]
                       + self.multi_valued_constants["production_protein_fish_per_month"][month]
                       + self.multi_valued_constants["h_e_created_protein"][month])
                      / self.single_valued_constants["PROTEIN_MONTHLY"] / 1e9,
                      "Protein_Fed_Month_" + str(month) + "_Constraint")

        # no feeding human edible maintained meat or dairy to animals or biofuels

        model += (variables["stored_food_eaten"][month]
                  + variables["crops_food_eaten_no_rotation"][month]
                  + variables["crops_food_eaten_with_rotation"][month]
                  * self.single_valued_constants["OG_ROTATION_FRACTION_KCALS"]
                  >= self.multi_valued_constants["excess_kcals"][month],
                  "Excess_Kcals_Less_Than_SF_And_OG_" + str(month) + "_Constraint")

        if(self.single_valued_constants['inputs']['INCLUDE_FAT']):
            model += (variables["stored_food_eaten"][month] * self.single_valued_constants["SF_FRACTION_FAT"]
                      + variables["crops_food_eaten_no_rotation"][month] * self.single_valued_constants["OG_FRACTION_FAT"]
                      + variables["crops_food_eaten_with_rotation"][month]
                      * self.single_valued_constants["OG_ROTATION_FRACTION_FAT"]
                      >= self.multi_valued_constants["excess_fat_used"][month],
                      "Excess_Fat_Less_Than_SF_And_OG_" + str(month) + "_Constraint")

        if(self.single_valued_constants['inputs']['INCLUDE_PROTEIN']):
            model += (variables["stored_food_eaten"][month] * self.single_valued_constants["SF_FRACTION_PROTEIN"]
                      + variables["crops_food_eaten_no_rotation"][month] * self.single_valued_constants["OG_FRACTION_PROTEIN"]
                      + variables["crops_food_eaten_with_rotation"][month]
                      * self.single_valued_constants["OG_ROTATION_FRACTION_PROTEIN"]
                      >= self.multi_valued_constants["excess_protein_used"][month],
                      "Excess_Protein_Less_Than_SF_And_OG_" + str(month) + "_Constraint")

        ##### helps reduce wild fluctutions in people fed #######
        # if(m > 0 and self.single_valued_constants['inputs']['KCAL_SMOOTHING']):
        if(month > 0 and self.single_valued_constants['inputs']['KCAL_SMOOTHING']):
            model += (variables["humans_fed_kcals"][month - 1] >= variables["humans_fed_kcals"][month] * (1/1.05),
                      "Small_Change_Minus_Humans_Fed_Month_" + str(month) + "_Constraint")
            model += (variables["humans_fed_kcals"][month - 1] <= variables["humans_fed_kcals"][month] * (1.05),
                      "Small_Change_Plus_Humans_Fed_Month_" + str(month) + "_Constraint")

        # maximizes the minimum objective_function value
        # We maximize the minimum humans fed from any month
        # We therefore maximize the minimum ratio of fat per human requirement,
        # protein per human requirement, or kcals per human requirement
        # for all months

        maximizer_string = "Kcals_Fed_Month_" + str(month) + "_Objective_Constraint"
        maximize_constraints.append(maximizer_string)
        model += (variables["objective_function"] <= variables["humans_fed_kcals"][month], maximizer_string)

        if(self.single_valued_constants['inputs']['INCLUDE_FAT']):

            maximizer_string = "Fat_Fed_Month_" + str(month) + "_Objective_Constraint"
            maximize_constraints.append(maximizer_string)
            model += (variables["objective_function"] <= variables["humans_fed_fat"][month], maximizer_string)

        if(self.single_valued_constants['inputs']['INCLUDE_PROTEIN']):
            maximizer_string = "Protein_Fed_Month_" + str(month) + "_Objective_Constraint"
            maximize_constraints.append(maximizer_string)
            model += (variables["objective_function"] <= variables["humans_fed_protein"][month], maximizer_string)

        return [model, variables, maximize_constraints]
