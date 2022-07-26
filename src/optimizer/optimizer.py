################################Optimizer Model################################
##                                                                            #
## In this model, we estimate the macronutrient production allocated optimally#
##  over time including models for traditional and resilient foods.           #
##                                                                            #
###############################################################################


import os
import sys
import numpy as np
import pulp
from pulp import LpMaximize, LpProblem, LpVariable

module_path = os.path.abspath(os.path.join("../.."))
if module_path not in sys.path:
    sys.path.append(module_path)


class Optimizer:
    def __init__(self):
        pass

    def optimize(self, single_valued_constants, multi_valued_constants):
        maximize_constraints = []  # used only for validation

        # Create the model to optimize
        model = LpProblem(name="optimization_nutrition", sense=LpMaximize)

        variables = {}

        variables["objective_function"] = LpVariable(
            name="Least_Humans_Fed_Any_Month", lowBound=0
        )

        self.single_valued_constants = single_valued_constants
        self.multi_valued_constants = multi_valued_constants

        #### MODEL GENERATION LOOP ####
        self.time_months = []

        NMONTHS = single_valued_constants["NMONTHS"]

        variables["stored_food_start"] = [0] * NMONTHS
        variables["stored_food_end"] = [0] * NMONTHS
        variables["stored_food_eaten"] = [0] * NMONTHS

        variables["seaweed_wet_on_farm"] = [0] * NMONTHS
        variables["used_area"] = [0] * NMONTHS
        variables["seaweed_food_produced"] = [0] * NMONTHS

        variables["crops_food_storage_no_rotation"] = [0] * NMONTHS
        variables["crops_food_storage_rotation"] = [0] * NMONTHS
        variables["crops_food_eaten_with_rotation"] = [0] * NMONTHS
        variables["crops_food_eaten_no_rotation"] = [0] * NMONTHS

        variables["humans_fed_kcals"] = [0] * NMONTHS
        variables["humans_fed_fat"] = [0] * NMONTHS
        variables["humans_fed_protein"] = [0] * NMONTHS

        for month in range(0, self.single_valued_constants["NMONTHS"]):
            if single_valued_constants["ADD_SEAWEED"]:
                (model, variables) = self.add_seaweed_to_model(model, variables, month)

            if single_valued_constants["ADD_OUTDOOR_GROWING"]:
                (model, variables) = self.add_outdoor_crops_to_model(
                    model, variables, month
                )

            if single_valued_constants["ADD_STORED_FOOD"]:
                (model, variables) = self.add_stored_food_to_model(
                    model, variables, month
                )

            [model, variables, maximize_constraints] = self.add_objectives_to_model(
                model, variables, month, maximize_constraints
            )

        PRINT_PULP_MESSAGES = False
        model += variables["objective_function"]
        status = model.solve(
            pulp.PULP_CBC_CMD(gapRel=0.0001, msg=PRINT_PULP_MESSAGES, fracGap=0.001)
        )

        assert status == 1, "ERROR: OPTIMIZATION FAILED!"

        return (
            model,
            variables,
            maximize_constraints,
            single_valued_constants,
            multi_valued_constants,
        )

    def add_seaweed_to_model(self, model, variables, month):
        # assume that the only harvest opportunity is once a month
        # format: name, lower bound, upper bound
        variables["seaweed_wet_on_farm"][month] = LpVariable(
            "Seaweed_Wet_On_Farm_" + str(month) + "_Variable",
            self.single_valued_constants["INITIAL_SEAWEED"],
            self.single_valued_constants["MAXIMUM_DENSITY"]
            * self.multi_valued_constants["built_area"][month],
        )

        # food production (using resources)
        variables["seaweed_food_produced"][month] = LpVariable(
            name="Seaweed_Food_Produced_During_Month_" + str(month) + "_Variable",
            lowBound=0,
        )

        variables["used_area"][month] = LpVariable(
            "Used_Area_" + str(month) + "_Variable",
            self.single_valued_constants["INITIAL_AREA"],
            self.multi_valued_constants["built_area"][month],
        )

        if month == 0:  # first Month
            model += (
                variables["seaweed_wet_on_farm"][0]
                == self.single_valued_constants["INITIAL_SEAWEED"],
                "Seaweed_Wet_On_Farm_0_Constraint",
            )
            model += (
                variables["used_area"][0]
                == self.single_valued_constants["INITIAL_AREA"],
                "Used_Area_Month_0_Constraint",
            )
            model += (
                variables["seaweed_food_produced"][0] == 0,
                "Seaweed_Food_Produced_Month_0_Constraint",
            )

        else:  # later Months
            model += (
                variables["seaweed_wet_on_farm"][month]
                <= variables["used_area"][month]
                * self.single_valued_constants["MAXIMUM_DENSITY"]
            )

            model += (
                variables["seaweed_wet_on_farm"][month]
                == variables["seaweed_wet_on_farm"][month - 1]
                * (
                    1
                    + self.single_valued_constants["inputs"]["SEAWEED_PRODUCTION_RATE"]
                    / 100.0
                )
                - variables["seaweed_food_produced"][month]
                - (variables["used_area"][month] - variables["used_area"][month - 1])
                * self.single_valued_constants["MINIMUM_DENSITY"]
                * (self.single_valued_constants["HARVEST_LOSS"] / 100),
                "Seaweed_Wet_On_Farm_" + str(month) + "_Constraint",
            )

        return (model, variables)

    # incorporate linear constraints for stored food consumption each month
    def add_stored_food_to_model(self, model, variables, month):
        variables["stored_food_start"][month] = LpVariable(
            "Stored_Food_Start_Month_" + str(month) + "_Variable",
            0,
            self.single_valued_constants["stored_food"].kcals,
        )
        variables["stored_food_end"][month] = LpVariable(
            "Stored_Food_End_Month_" + str(month) + "_Variable",
            0,
            self.single_valued_constants["stored_food"].kcals,
        )
        variables["stored_food_eaten"][month] = LpVariable(
            "Stored_Food_Eaten_During_Month_" + str(month) + "_Variable",
            0,
            self.single_valued_constants["stored_food"].kcals,
        )

        if month == 0:  # first Month
            model += (
                variables["stored_food_start"][0]
                == self.single_valued_constants["stored_food"].kcals,
                "Stored_Food_Start_Month_0_Constraint",
            )
        else:
            model += (
                variables["stored_food_start"][month]
                == variables["stored_food_end"][month - 1],
                "Stored_Food_Start_Month_" + str(month) + "_Constraint",
            )

            ##### helps reduce wild fluctutions in stored food #######
            if (
                month > 0
                and self.single_valued_constants["inputs"]["STORED_FOOD_SMOOTHING"]
            ):
                model += (
                    variables["stored_food_eaten"][month]
                    <= variables["stored_food_eaten"][month - 1]
                    * self.single_valued_constants["inputs"]["FLUCTUATION_LIMIT"],
                    "Small_Change_Plus_stored_food_Eaten_Month_"
                    + str(month)
                    + "_Constraint",
                )

                model += (
                    variables["stored_food_eaten"][month]
                    >= variables["stored_food_eaten"][month - 1]
                    * (1 / self.single_valued_constants["inputs"]["FLUCTUATION_LIMIT"]),
                    "Small_Change_Minus_stored_food_Eaten_Month_"
                    + str(month)
                    + "_Constraint",
                )

        model += (
            variables["stored_food_end"][month]
            == variables["stored_food_start"][month]
            - variables["stored_food_eaten"][month],
            "Stored_Food_End_Month_" + str(month) + "_Constraint",
        )

        return (model, variables)

    # incorporate linear constraints for stored food consumption each month
    def add_outdoor_crops_to_model(self, model, variables, month):

        variables["crops_food_storage_rotation"][month] = LpVariable(
            "Crops_Food_Storage_Rotation_Month_" + str(month) + "_Variable", lowBound=0
        )
        variables["crops_food_storage_no_rotation"][month] = LpVariable(
            "Crops_Food_Storage_No_Rotation_Month_" + str(month) + "_Variable",
            lowBound=0,
        )

        variables["crops_food_eaten_with_rotation"][month] = LpVariable(
            "Crops_Food_Eaten_Rotation_During_Month_" + str(month) + "_Variable",
            lowBound=0,
        )
        variables["crops_food_eaten_no_rotation"][month] = LpVariable(
            "Crops_Food_Eaten_No_Rotation_During_Month_" + str(month) + "_Variable",
            lowBound=0,
        )
        SCALE = 1

        if month == 0:

            model += (
                variables["crops_food_storage_no_rotation"][month]
                == self.multi_valued_constants["crops_food_produced"][month]
                - variables["crops_food_eaten_no_rotation"][month],
                "Crops_Food_Storage_No_Rotation_" + str(month) + "_Constraint",
            )

            model += (
                variables["crops_food_storage_rotation"][month] == 0,
                "Crops_Food_Storage_Rotation_" + str(month) + "_Constraint",
            )

            model += (
                variables["crops_food_eaten_with_rotation"][month] == 0,
                "Crops_Food_Eaten_Rotation_" + str(month) + "_Constraint",
            )

        elif month == self.single_valued_constants["NMONTHS"] - 1:
            # haven't dealt with the case of nmonths being less than initial harvest
            assert (
                month
                > self.single_valued_constants["inputs"][
                    "INITIAL_HARVEST_DURATION_IN_MONTHS"
                ]
            )

            model += (
                variables["crops_food_storage_no_rotation"][month] == 0,
                "Crops_Food_No_Rotation_None_Left_" + str(month) + "_Constraint",
            )

            model += (
                variables["crops_food_storage_rotation"][month] == 0,
                "Crops_Food_Rotation_None_Left_" + str(month) + "_Constraint",
            )

            model += (
                variables["crops_food_storage_rotation"][month]
                == self.multi_valued_constants["crops_food_produced"][month]
                - variables["crops_food_eaten_with_rotation"][month]
                + variables["crops_food_storage_rotation"][month - 1],
                "Crops_Food_Rotation_Storage_" + str(month) + "_Constraint",
            )

            model += (
                variables["crops_food_storage_no_rotation"][month]
                == variables["crops_food_storage_no_rotation"][month - 1]
                - variables["crops_food_eaten_no_rotation"][month],
                "Crops_Food_No_Rotation_Storage_" + str(month) + "_Constraint",
            )

        elif (
            month
            < self.single_valued_constants["inputs"][
                "INITIAL_HARVEST_DURATION_IN_MONTHS"
            ]
        ):

            model += (
                variables["crops_food_storage_rotation"][month] == 0,
                "Crops_Food_Storage_Rotation" + str(month) + "_Constraint",
            )

            model += (
                variables["crops_food_eaten_with_rotation"][month] == 0,
                "Crops_Food_Eaten_Rotation" + str(month) + "_Constraint",
            )

            model += (
                variables["crops_food_storage_no_rotation"][month]
                == self.multi_valued_constants["crops_food_produced"][month]
                - variables["crops_food_eaten_no_rotation"][month]
                + variables["crops_food_storage_no_rotation"][month - 1],
                "Crops_Food_Storage_No_Rotation_" + str(month) + "_Constraint",
            )

        else:  # now produconstants_for_paramsg rotation, but can still eat "no rotation" storage

            model += (
                variables["crops_food_storage_rotation"][month]
                == self.multi_valued_constants["crops_food_produced"][month]
                - variables["crops_food_eaten_with_rotation"][month]
                + variables["crops_food_storage_rotation"][month - 1],
                "Crops_Food_Storage_Rotation_" + str(month) + "_Constraint",
            )

            model += (
                variables["crops_food_storage_no_rotation"][month]
                == variables["crops_food_storage_no_rotation"][month - 1]
                - variables["crops_food_eaten_no_rotation"][month],
                "Crops_Food_Storage_No_Rotation_" + str(month) + "_Constraint",
            )

        return (model, variables)

    #### OBJECTIVE FUNCTIONS  ####

    def add_objectives_to_model(self, model, variables, month, maximize_constraints):

        variables["humans_fed_kcals"][month] = LpVariable(
            name="Humans_Fed_Kcals_" + str(month) + "_Variable", lowBound=0
        )
        variables["humans_fed_fat"][month] = LpVariable(
            name="Humans_Fed_Fat_" + str(month) + "_Variable", lowBound=0
        )
        variables["humans_fed_protein"][month] = LpVariable(
            name="Humans_Fed_Protein_" + str(month) + "_Variable", lowBound=0
        )

        if self.single_valued_constants["ADD_SEAWEED"]:

            # maximum seaweed percent of calories
            # constraint units: billion kcals per person
            model += (
                variables["seaweed_food_produced"][month]
                * self.single_valued_constants["SEAWEED_KCALS"]
                <= (
                    self.single_valued_constants["inputs"][
                        "MAX_SEAWEED_AS_PERCENT_KCALS"
                    ]
                    / 100
                )
                * (
                    self.single_valued_constants["POP"]
                    * self.single_valued_constants["KCALS_MONTHLY"]
                    / 1e9
                ),
                "Seaweed_Limit_Kcals_" + str(month) + "_Constraint",
            )

        # finds billions of people fed that month per nutrient

        # stored food eaten*sf_fraction_kcals is in units billions kcals monthly
        # seaweed_food_produced*seaweed_kcals is in units billions kcals
        # billions kcals needed is in units billion kcals per month for
        # the whole population

        # print("nonhuman times CROPS_WASTE" + str(month))

        # print(
        #     round(self.multi_valued_constants["nonhuman_consumption"].kcals[month], 5)
        # )

        # print(round(self.multi_valued_constants["grazing_milk_kcals"][month], 5))

        # print(
        #     round(
        #         self.multi_valued_constants["cattle_grazing_maintained_kcals"][month], 5
        #     )
        # )

        # print(round(self.multi_valued_constants["meat_culled"][month], 5))

        # print(
        #     round(
        #         self.multi_valued_constants["production_kcals_cell_sugar_per_month"][
        #             month
        #         ],
        #         3,
        #     )
        # )

        # print(
        #     round(
        #         self.multi_valued_constants["production_kcals_scp_per_month"][month], 5
        #     )
        # )
        # print(round(self.multi_valued_constants["greenhouse_area"][month], 5))
        # print(
        #     round(
        #         self.multi_valued_constants["production_kcals_fish_per_month"][month], 5
        #     )
        # )
        # print(round(self.multi_valued_constants["grain_fed_created_kcals"][month], 5))

        # numbers scaled to percent of per person human needs per month
        model += (
            variables["humans_fed_kcals"][month]
            == (
                variables["stored_food_eaten"][month]
                + variables["crops_food_eaten_no_rotation"][month]
                + variables["crops_food_eaten_with_rotation"][month]
                * self.single_valued_constants["OG_ROTATION_FRACTION_KCALS"]
                - self.multi_valued_constants["nonhuman_consumption"].kcals[month]
                + variables["seaweed_food_produced"][month]
                * self.single_valued_constants["SEAWEED_KCALS"]
                + self.multi_valued_constants["grazing_milk_kcals"][month]
                + self.multi_valued_constants["cattle_grazing_maintained_kcals"][month]
                + self.multi_valued_constants["meat_culled"][month]
                + self.multi_valued_constants["production_kcals_cell_sugar_per_month"][
                    month
                ]
                + self.multi_valued_constants["production_kcals_scp_per_month"][month]
                + self.multi_valued_constants["greenhouse_area"][month]
                * self.multi_valued_constants["greenhouse_kcals_per_ha"][month]
                + self.multi_valued_constants["production_kcals_fish_per_month"][month]
                + self.multi_valued_constants["grain_fed_created_kcals"][month]
            )
            / self.single_valued_constants["BILLION_KCALS_NEEDED"]
            * 100,
            "Kcals_Fed_Month_" + str(month) + "_Constraint",
        )

        # print(round(self.multi_valued_constants["nonhuman_consumption"].fat[month], 5))

        # print(round(self.multi_valued_constants["grazing_milk_fat"][month], 5))

        # print(
        #     round(
        #         self.multi_valued_constants["cattle_grazing_maintained_fat"][month], 5
        #     )
        # )

        # print(round(self.multi_valued_constants["meat_culled"][month], 5))

        # print(
        #     round(self.multi_valued_constants["production_fat_scp_per_month"][month], 5)
        # )
        # print(round(self.multi_valued_constants["greenhouse_area"][month], 5))
        # print(
        #     round(
        #         self.multi_valued_constants["production_fat_fish_per_month"][month], 5
        #     )
        # )
        # print("grain_fed_fat")
        # print(round(self.multi_valued_constants["grain_fed_created_fat"][month], 5))

        if self.single_valued_constants["inputs"]["INCLUDE_FAT"]:
            # fat monthly is in units thousand tons
            model += (
                variables["humans_fed_fat"][month]
                == (
                    variables["stored_food_eaten"][month]
                    * self.single_valued_constants["SF_FRACTION_FAT"]
                    + variables["crops_food_eaten_no_rotation"][month]
                    * self.single_valued_constants["OG_FRACTION_FAT"]
                    + variables["crops_food_eaten_with_rotation"][month]
                    * self.single_valued_constants["OG_ROTATION_FRACTION_FAT"]
                    - self.multi_valued_constants["nonhuman_consumption"].fat[month]
                    + variables["seaweed_food_produced"][month]
                    * self.single_valued_constants["SEAWEED_FAT"]
                    + self.multi_valued_constants["grazing_milk_fat"][month]
                    + self.multi_valued_constants["cattle_grazing_maintained_fat"][
                        month
                    ]
                    + self.multi_valued_constants["meat_culled"][month]
                    * self.single_valued_constants["MEAT_CULLED_FRACTION_FAT"]
                    + self.multi_valued_constants["production_fat_scp_per_month"][month]
                    + self.multi_valued_constants["greenhouse_area"][month]
                    * self.multi_valued_constants["greenhouse_fat_per_ha"][month]
                    + self.multi_valued_constants["production_fat_fish_per_month"][
                        month
                    ]
                    + self.multi_valued_constants["grain_fed_created_fat"][month]
                )
                / self.single_valued_constants["THOU_TONS_FAT_NEEDED"]
                * 100,
                "Fat_Fed_Month_" + str(month) + "_Constraint",
            )

        if self.single_valued_constants["inputs"]["INCLUDE_PROTEIN"]:

            model += (
                variables["humans_fed_protein"][month]
                == (
                    variables["stored_food_eaten"][month]
                    * self.single_valued_constants["SF_FRACTION_PROTEIN"]
                    + variables["crops_food_eaten_no_rotation"][month]
                    * self.single_valued_constants["OG_FRACTION_PROTEIN"]
                    + variables["crops_food_eaten_with_rotation"][month]
                    * self.single_valued_constants["OG_ROTATION_FRACTION_PROTEIN"]
                    - self.multi_valued_constants["nonhuman_consumption"].protein[month]
                    + variables["seaweed_food_produced"][month]
                    * self.single_valued_constants["SEAWEED_PROTEIN"]
                    + self.multi_valued_constants["grazing_milk_protein"][month]
                    + self.multi_valued_constants["cattle_grazing_maintained_protein"][
                        month
                    ]
                    + self.multi_valued_constants["production_protein_scp_per_month"][
                        month
                    ]
                    + self.multi_valued_constants["meat_culled"][month]
                    * self.single_valued_constants["MEAT_CULLED_FRACTION_PROTEIN"]
                    + self.multi_valued_constants["greenhouse_area"][month]
                    * self.multi_valued_constants["greenhouse_protein_per_ha"][month]
                    + self.multi_valued_constants["production_protein_fish_per_month"][
                        month
                    ]
                    + self.multi_valued_constants["grain_fed_created_protein"][month]
                )
                / self.single_valued_constants["THOU_TONS_PROTEIN_NEEDED"]
                * 100,
                "Protein_Fed_Month_" + str(month) + "_Constraint",
            )

        # no feeding human edible maintained meat or milk to animals or biofuels

        model += (
            variables["stored_food_eaten"][month]
            + variables["crops_food_eaten_no_rotation"][month]
            + variables["crops_food_eaten_with_rotation"][month]
            * self.single_valued_constants["OG_ROTATION_FRACTION_KCALS"]
            >= self.multi_valued_constants["nonhuman_consumption"].kcals[month],
            "Excess_Kcals_Less_Than_stored_food_And_outdoor_crops_"
            + str(month)
            + "_Constraint",
        )

        if self.single_valued_constants["inputs"]["INCLUDE_FAT"]:
            model += (
                variables["stored_food_eaten"][month]
                * self.single_valued_constants["SF_FRACTION_FAT"]
                + variables["crops_food_eaten_no_rotation"][month]
                * self.single_valued_constants["OG_FRACTION_FAT"]
                + variables["crops_food_eaten_with_rotation"][month]
                * self.single_valued_constants["OG_ROTATION_FRACTION_FAT"]
                >= self.multi_valued_constants["nonhuman_consumption"].fat[month],
                "Excess_Fat_Less_Than_stored_food_And_outdoor_crops_"
                + str(month)
                + "_Constraint",
            )

        if self.single_valued_constants["inputs"]["INCLUDE_PROTEIN"]:
            model += (
                variables["stored_food_eaten"][month]
                * self.single_valued_constants["SF_FRACTION_PROTEIN"]
                + variables["crops_food_eaten_no_rotation"][month]
                * self.single_valued_constants["OG_FRACTION_PROTEIN"]
                + variables["crops_food_eaten_with_rotation"][month]
                * self.single_valued_constants["OG_ROTATION_FRACTION_PROTEIN"]
                >= self.multi_valued_constants["nonhuman_consumption"].protein[month],
                "Excess_Protein_Less_Than_stored_food_And_outdoor_crops_"
                + str(month)
                + "_Constraint",
            )

        ##### helps reduce wild fluctutions in people fed #######
        # if(m > 0 and self.single_valued_constants['inputs']['KCAL_SMOOTHING']):
        if month > 0 and self.single_valued_constants["inputs"]["KCAL_SMOOTHING"]:
            model += (
                variables["humans_fed_kcals"][month - 1]
                >= variables["humans_fed_kcals"][month] * (1 / 1.05),
                "Small_Change_Minus_Humans_Fed_Month_" + str(month) + "_Constraint",
            )
            model += (
                variables["humans_fed_kcals"][month - 1]
                <= variables["humans_fed_kcals"][month] * (1.05),
                "Small_Change_Plus_Humans_Fed_Month_" + str(month) + "_Constraint",
            )

        # maximizes the minimum objective_function value
        # We maximize the minimum humans fed from any month
        # We therefore maximize the minimum ratio of fat per human requirement,
        # protein per human requirement, or kcals per human requirement
        # for all months

        maximizer_string = "Kcals_Fed_Month_" + str(month) + "_Objective_Constraint"
        maximize_constraints.append(maximizer_string)
        model += (
            variables["objective_function"] <= variables["humans_fed_kcals"][month],
            maximizer_string,
        )

        if self.single_valued_constants["inputs"]["INCLUDE_FAT"]:

            maximizer_string = "Fat_Fed_Month_" + str(month) + "_Objective_Constraint"
            maximize_constraints.append(maximizer_string)
            model += (
                variables["objective_function"] <= variables["humans_fed_fat"][month],
                maximizer_string,
            )

        if self.single_valued_constants["inputs"]["INCLUDE_PROTEIN"]:
            maximizer_string = (
                "Protein_Fed_Month_" + str(month) + "_Objective_Constraint"
            )
            maximize_constraints.append(maximizer_string)
            model += (
                variables["objective_function"]
                <= variables["humans_fed_protein"][month],
                maximizer_string,
            )

        return [model, variables, maximize_constraints]
