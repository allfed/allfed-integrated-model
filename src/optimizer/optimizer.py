################################Optimizer Model################################
##                                                                            #
## In this model, we estimate the macronutrient production allocated optimally#
##  over time including models for traditional and resilient foods.           #
##                                                                            #
###############################################################################


from multiprocessing.pool import IMapIterator
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

        variables["culled_meat_start"] = [0] * NMONTHS
        variables["culled_meat_end"] = [0] * NMONTHS
        variables["culled_meat_eaten"] = [0] * NMONTHS

        variables["seaweed_wet_on_farm"] = [0] * NMONTHS
        variables["used_area"] = [0] * NMONTHS
        variables["seaweed_food_produced"] = [0] * NMONTHS

        variables["crops_food_storage_no_relocation"] = [0] * NMONTHS
        variables["crops_food_storage_relocated"] = [0] * NMONTHS
        variables["crops_food_eaten_relocated"] = [0] * NMONTHS
        variables["crops_food_eaten_no_relocation"] = [0] * NMONTHS

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

            if single_valued_constants["ADD_CULLED_MEAT"]:
                (model, variables) = self.add_culled_meat_to_model(
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
        ASSERT_SUCCESSFUL_OPTIMIZATION = True
        if ASSERT_SUCCESSFUL_OPTIMIZATION:
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
            self.single_valued_constants["INITIAL_BUILT_SEAWEED_AREA"],
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
                == self.single_valued_constants["INITIAL_BUILT_SEAWEED_AREA"],
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
    def add_stored_food_to_model_only_first_year(self, model, variables, month):

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

        elif month > 12:  # within first year:
            model += (
                variables["stored_food_eaten"][month] == 0,
                "Stored_Food_Eaten_Month_" + str(month) + "_Constraint",
            )

            model += (
                variables["stored_food_start"][month] == 0,
                "Stored_Food_Start_Month_" + str(month) + "_Constraint",
            )

            model += (
                variables["stored_food_end"][month] == 0,
                "Stored_Food_End_Month_" + str(month) + "_Constraint",
            )

        else:
            model += (
                variables["stored_food_start"][month]
                == variables["stored_food_end"][month - 1],
                "Stored_Food_Start_Month_" + str(month) + "_Constraint",
            )

            model += (
                variables["stored_food_end"][month] == 0,
                "Stored_Food_End_Month_" + str(month) + "_Constraint",
            )

        if month <= 12:
            model += (
                variables["stored_food_end"][month]
                == variables["stored_food_start"][month]
                - variables["stored_food_eaten"][month],
                "Stored_Food_Eaten_During_Month_" + str(month) + "_Constraint",
            )

        return (model, variables)

    def add_stored_food_to_model(self, model, variables, month):
        IMITATE_XIA_ET_AL = False
        if IMITATE_XIA_ET_AL:
            return self.add_stored_food_to_model_only_first_year(
                model, variables, month
            )

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

        elif month == self.single_valued_constants["NMONTHS"] - 1:  # last month

            model += (
                variables["stored_food_end"][month] == 0,
                "Stored_Food_End_Month_" + str(month) + "_Constraint",
            )

            model += (
                variables["stored_food_start"][month]
                == variables["stored_food_end"][month - 1],
                "Stored_Food_Start_Month_" + str(month) + "_Constraint",
            )

        else:
            model += (
                variables["stored_food_start"][month]
                == variables["stored_food_end"][month - 1],
                "Stored_Food_Start_Month_" + str(month) + "_Constraint",
            )

        model += (
            variables["stored_food_end"][month]
            == variables["stored_food_start"][month]
            - variables["stored_food_eaten"][month],
            "Stored_Food_Eaten_During_Month_" + str(month) + "_Constraint",
        )
        return (model, variables)

    def add_culled_meat_to_model(self, model, variables, month):
        """
        incorporate linear constraints for culled meat consumption each month
        it's like stored food, but there is a preset limit for how much can be produced
        """
        variables["culled_meat_start"][month] = LpVariable(
            "Culled_Meat_Start_Month_" + str(month) + "_Variable",
            0,
            self.single_valued_constants["culled_meat"],
        )
        variables["culled_meat_end"][month] = LpVariable(
            "Culled_Meat_End_Month_" + str(month) + "_Variable",
            0,
            self.single_valued_constants["culled_meat"],
        )
        variables["culled_meat_eaten"][month] = LpVariable(
            "Culled_Meat_Eaten_During_Month_" + str(month) + "_Variable",
            0,
            self.multi_valued_constants["max_culled_kcals"][month],
        )

        if month == 0:  # first Month
            model += (
                variables["culled_meat_start"][0]
                == self.single_valued_constants["culled_meat"],
                "Culled_Meat_Start_Month_0_Constraint",
            )

        elif month == self.single_valued_constants["NMONTHS"] - 1:  # last month

            model += (
                variables["culled_meat_end"][month] == 0,
                "Culled_Meat_End_Month_" + str(month) + "_Constraint",
            )

            model += (
                variables["culled_meat_start"][month]
                == variables["culled_meat_end"][month - 1],
                "Culled_Meat_Start_Month_" + str(month) + "_Constraint",
            )

        else:
            model += (
                variables["culled_meat_start"][month]
                == variables["culled_meat_end"][month - 1],
                "Culled_Meat_Start_Month_" + str(month) + "_Constraint",
            )

        model += (
            variables["culled_meat_end"][month]
            == variables["culled_meat_start"][month]
            - variables["culled_meat_eaten"][month],
            "Culled_Meat_Eaten_During_Month_" + str(month) + "_Constraint",
        )
        return (model, variables)

    def add_outdoor_crops_to_model_no_relocation(self, model, variables, month):
        IMITATE_XIA_ET_AL = False  # they don't consider storage at all
        if IMITATE_XIA_ET_AL:
            return self.add_outdoor_crops_to_model_no_storage(model, variables, month)

        variables["crops_food_storage_no_relocation"][month] = LpVariable(
            "Crops_Food_Storage_No_Relocation_Month_" + str(month) + "_Variable",
            lowBound=0,
        )
        variables["crops_food_eaten_no_relocation"][month] = LpVariable(
            "Crops_Food_Eaten_No_Relocation_During_Month_" + str(month) + "_Variable",
            lowBound=0,
        )

        if month == 0:

            model += (
                variables["crops_food_storage_no_relocation"][month]
                == self.multi_valued_constants["outdoor_crops"].kcals[month]
                - variables["crops_food_eaten_no_relocation"][month],
                "Crops_Food_Storage_No_Relocation_" + str(month) + "_Constraint",
            )

        elif month == self.single_valued_constants["NMONTHS"] - 1:  # last month
            model += (
                variables["crops_food_storage_no_relocation"][month] == 0,
                "Crops_Food_No_Relocation_None_Left_" + str(month) + "_Constraint",
            )

            model += (
                variables["crops_food_storage_no_relocation"][month]
                == self.multi_valued_constants["outdoor_crops"].kcals[month]
                + variables["crops_food_storage_no_relocation"][month - 1]
                - variables["crops_food_eaten_no_relocation"][month],
                "Crops_Food_No_Relocation_Storage_" + str(month) + "_Constraint",
            )

        else:
            # any month other than the first or last month

            model += (
                variables["crops_food_storage_no_relocation"][month]
                == self.multi_valued_constants["outdoor_crops"].kcals[month]
                - variables["crops_food_eaten_no_relocation"][month]
                + variables["crops_food_storage_no_relocation"][month - 1],
                "Crops_Food_Storage_No_Relocation_" + str(month) + "_Constraint",
            )

        return (model, variables)

    def add_outdoor_crops_to_model_no_storage(self, model, variables, month):
        variables["crops_food_storage_no_relocation"][month] = LpVariable(
            "Crops_Food_Storage_No_Relocation_Month_" + str(month) + "_Variable",
            lowBound=0,
        )
        variables["crops_food_eaten_no_relocation"][month] = LpVariable(
            "Crops_Food_Eaten_No_Relocation_During_Month_" + str(month) + "_Variable",
            lowBound=0,
        )

        if month == 0:

            model += (
                0
                == self.multi_valued_constants["outdoor_crops"].kcals[month]
                - variables["crops_food_eaten_no_relocation"][month],
                "Crops_Food_Storage_No_Relocation_" + str(month) + "_Constraint",
            )

        elif month == self.single_valued_constants["NMONTHS"] - 1:  # last month

            model += (
                0
                == self.multi_valued_constants["outdoor_crops"].kcals[month]
                - variables["crops_food_eaten_no_relocation"][month],
                "Crops_Food_No_Relocation_Storage_" + str(month) + "_Constraint",
            )

        else:
            # any month other than the first or last month

            model += (
                0
                == self.multi_valued_constants["outdoor_crops"].kcals[month]
                - variables["crops_food_eaten_no_relocation"][month],
                "Crops_Food_Storage_No_Relocation_" + str(month) + "_Constraint",
            )
        model += (
            variables["crops_food_storage_no_relocation"][month] == 0,
            "Crops_Food_No_Relocation_None_Left_" + str(month) + "_Constraint",
        )

        return (model, variables)

    # incorporate linear constraints for stored food consumption each month
    def add_outdoor_crops_to_model(self, model, variables, month):
        if not self.single_valued_constants["inputs"]["OG_USE_BETTER_ROTATION"]:
            self.add_outdoor_crops_to_model_no_relocation(model, variables, month)
            return (model, variables)
        # in the more complicated case where relocation occurs, the crops do better
        # than they would otherwise, and they have a different nutritional profile

        variables["crops_food_storage_no_relocation"][month] = LpVariable(
            "Crops_Food_Storage_No_Relocation_Month_" + str(month) + "_Variable",
            lowBound=0,
        )
        variables["crops_food_eaten_no_relocation"][month] = LpVariable(
            "Crops_Food_Eaten_No_Relocation_During_Month_" + str(month) + "_Variable",
            lowBound=0,
        )

        variables["crops_food_storage_relocated"][month] = LpVariable(
            "Crops_Food_Storage_Relocated_Month_" + str(month) + "_Variable", lowBound=0
        )
        variables["crops_food_eaten_relocated"][month] = LpVariable(
            "Crops_Food_Eaten_Relocated_During_Month_" + str(month) + "_Variable",
            lowBound=0,
        )

        if month == 0:  # first month

            model += (
                variables["crops_food_storage_no_relocation"][month]
                == self.multi_valued_constants["outdoor_crops"].kcals[month]
                - variables["crops_food_eaten_no_relocation"][month],
                "Crops_Food_Storage_No_Relocation_" + str(month) + "_Constraint",
            )

            model += (
                variables["crops_food_storage_relocated"][month] == 0,
                "Crops_Food_Storage_Relocated_" + str(month) + "_Constraint",
            )

            model += (
                variables["crops_food_eaten_relocated"][month] == 0,
                "Crops_Food_Eaten_Relocated_" + str(month) + "_Constraint",
            )

        elif month == self.single_valued_constants["NMONTHS"] - 1:  # last month
            # haven't dealt with the case of nmonths being less than initial harvest
            assert (
                month
                > self.single_valued_constants["inputs"][
                    "INITIAL_HARVEST_DURATION_IN_MONTHS"
                ]
            )

            model += (
                variables["crops_food_storage_no_relocation"][month] == 0,
                "Crops_Food_No_Relocation_None_Left_" + str(month) + "_Constraint",
            )

            model += (
                variables["crops_food_storage_relocated"][month] == 0,
                "Crops_Food_Relocated_None_Left_" + str(month) + "_Constraint",
            )

            # note to self: is it a problem that the crops_food_storage_relocated is
            # part of the following equation, and not excluded, as it is set to zero
            # in the assignment above?

            model += (
                variables["crops_food_storage_relocated"][month]
                == self.multi_valued_constants["outdoor_crops"].kcals[month]
                - variables["crops_food_eaten_relocated"][month]
                + variables["crops_food_storage_relocated"][month - 1],
                "Crops_Food_Relocated_Storage_" + str(month) + "_Constraint",
            )

            model += (
                variables["crops_food_storage_no_relocation"][month]
                == variables["crops_food_storage_no_relocation"][month - 1]
                - variables["crops_food_eaten_no_relocation"][month],
                "Crops_Food_No_Relocation_Storage_" + str(month) + "_Constraint",
            )

        elif (
            month
            < self.single_valued_constants["inputs"][
                "INITIAL_HARVEST_DURATION_IN_MONTHS"
            ]
        ):
            # any month up to and including the harvest duration

            model += (
                variables["crops_food_storage_relocated"][month] == 0,
                "Crops_Food_Storage_Rotation" + str(month) + "_Constraint",
            )

            model += (
                variables["crops_food_eaten_relocated"][month] == 0,
                "Crops_Food_Eaten_Rotation" + str(month) + "_Constraint",
            )

            model += (
                variables["crops_food_storage_no_relocation"][month]
                == self.multi_valued_constants["outdoor_crops"].kcals[month]
                - variables["crops_food_eaten_no_relocation"][month]
                + variables["crops_food_storage_no_relocation"][month - 1],
                "Crops_Food_Storage_No_Relocation_" + str(month) + "_Constraint",
            )

        else:  # now producing rotation, but can still eat "no rotation" storage
            # not the first month, not the last month, and is a month after the rotation
            # switch
            model += (
                variables["crops_food_storage_relocated"][month]
                == self.multi_valued_constants["outdoor_crops"].kcals[month]
                - variables["crops_food_eaten_relocated"][month]
                + variables["crops_food_storage_relocated"][month - 1],
                "Crops_Food_Storage_Relocated_" + str(month) + "_Constraint",
            )

            model += (
                variables["crops_food_storage_no_relocation"][month]
                == variables["crops_food_storage_no_relocation"][month - 1]
                - variables["crops_food_eaten_no_relocation"][month],
                "Crops_Food_Storage_No_Relocation_" + str(month) + "_Constraint",
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

        if (
            self.single_valued_constants["ADD_SEAWEED"]
            and self.single_valued_constants["inputs"]["INITIAL_SEAWEED"] > 0
        ):

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
        model += (
            variables["humans_fed_kcals"][month]
            == (
                variables["stored_food_eaten"][month]
                + variables["crops_food_eaten_no_relocation"][month]
                + variables["crops_food_eaten_relocated"][month]
                * self.single_valued_constants["OG_ROTATION_FRACTION_KCALS"]
                - self.multi_valued_constants["nonhuman_consumption"].kcals[month]
                + variables["seaweed_food_produced"][month]
                * self.single_valued_constants["SEAWEED_KCALS"]
                + self.multi_valued_constants["grazing_milk_kcals"][month]
                + self.multi_valued_constants["cattle_grazing_maintained_kcals"][month]
                + variables["culled_meat_eaten"][month]
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

        if self.single_valued_constants["inputs"]["INCLUDE_FAT"]:

            # fat monthly is in units thousand tons
            model += (
                variables["humans_fed_fat"][month]
                == (
                    variables["stored_food_eaten"][month]
                    * self.single_valued_constants["SF_FRACTION_FAT"]
                    + variables["crops_food_eaten_no_relocation"][month]
                    * self.single_valued_constants["OG_FRACTION_FAT"]
                    + variables["crops_food_eaten_relocated"][month]
                    * self.single_valued_constants["OG_ROTATION_FRACTION_FAT"]
                    - self.multi_valued_constants["nonhuman_consumption"].fat[month]
                    + variables["seaweed_food_produced"][month]
                    * self.single_valued_constants["SEAWEED_FAT"]
                    + self.multi_valued_constants["grazing_milk_fat"][month]
                    + self.multi_valued_constants["cattle_grazing_maintained_fat"][
                        month
                    ]
                    + variables["culled_meat_eaten"][month]
                    * self.single_valued_constants["CULLED_MEAT_FRACTION_FAT"]
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
                    + variables["crops_food_eaten_no_relocation"][month]
                    * self.single_valued_constants["OG_FRACTION_PROTEIN"]
                    + variables["crops_food_eaten_relocated"][month]
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
                    + variables["culled_meat_eaten"][month]
                    * self.single_valued_constants["CULLED_MEAT_FRACTION_PROTEIN"]
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
            (
                variables["stored_food_eaten"][month]
                + variables["crops_food_eaten_no_relocation"][month]
                + variables["crops_food_eaten_relocated"][month]
                * self.single_valued_constants["OG_ROTATION_FRACTION_KCALS"]
            )
            / self.single_valued_constants["BILLION_KCALS_NEEDED"]
            * 100
            >= (self.multi_valued_constants["nonhuman_consumption"].kcals[month])
            / self.single_valued_constants["BILLION_KCALS_NEEDED"]
            * 100,
            "Excess_Kcals_Less_Than_stored_food_And_outdoor_crops_"
            + str(month)
            + "_Constraint",
        )

        if self.single_valued_constants["inputs"]["INCLUDE_FAT"]:
            model += (
                (
                    variables["stored_food_eaten"][month]
                    * self.single_valued_constants["SF_FRACTION_FAT"]
                    + variables["crops_food_eaten_no_relocation"][month]
                    * self.single_valued_constants["OG_FRACTION_FAT"]
                    + variables["crops_food_eaten_relocated"][month]
                    * self.single_valued_constants["OG_ROTATION_FRACTION_FAT"]
                )
                / self.single_valued_constants["THOU_TONS_FAT_NEEDED"]
                * 100
                >= self.multi_valued_constants["nonhuman_consumption"].fat[month]
                / self.single_valued_constants["THOU_TONS_FAT_NEEDED"]
                * 100,
                "Excess_Fat_Less_Than_stored_food_And_outdoor_crops_"
                + str(month)
                + "_Constraint",
            )

        if self.single_valued_constants["inputs"]["INCLUDE_PROTEIN"]:
            model += (
                (
                    variables["stored_food_eaten"][month]
                    * self.single_valued_constants["SF_FRACTION_PROTEIN"]
                    + variables["crops_food_eaten_no_relocation"][month]
                    * self.single_valued_constants["OG_FRACTION_PROTEIN"]
                    + variables["crops_food_eaten_relocated"][month]
                    * self.single_valued_constants["OG_ROTATION_FRACTION_PROTEIN"]
                )
                / self.single_valued_constants["THOU_TONS_PROTEIN_NEEDED"]
                * 100
                >= self.multi_valued_constants["nonhuman_consumption"].protein[month]
                / self.single_valued_constants["THOU_TONS_PROTEIN_NEEDED"]
                * 100,
                "Excess_Protein_Less_Than_stored_food_And_outdoor_crops_"
                + str(month)
                + "_Constraint",
            )

        ##### helps reduce wild fluctutions in people fed #######
        # if(m > 0 and self.single_valued_constants['inputs']['KCAL_SMOOTHING']):
        # if month > 0 and self.single_valued_constants["inputs"]["KCAL_SMOOTHING"]:
        #     model += (
        #         variables["humans_fed_kcals"][month - 1]
        #         >= variables["humans_fed_kcals"][month] * (1 / 1.05),
        #         "Small_Change_Minus_Humans_Fed_Month_" + str(month) + "_Constraint",
        #     )
        #     model += (
        #         variables["humans_fed_kcals"][month - 1]
        #         <= variables["humans_fed_kcals"][month] * (1.05),
        #         "Small_Change_Plus_Humans_Fed_Month_" + str(month) + "_Constraint",
        #     )

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
