################################## Analyzer ###################################
##                                                                            #
##            Extracts the results from the optimizer for                     #
##        plotting. It also converts from a given production excess           #
##       into an expected diet, if all of that excess is used                 #
##                           for feeding animals                              #
##                                                                            #
###############################################################################


from typing import no_type_check
import numpy as np
import os
import sys

module_path = os.path.abspath(os.path.join("../.."))
if module_path not in sys.path:
    sys.path.append(module_path)


class Analyzer:
    def __init__(self, constants):
        self.constants = constants

    # order the variables that occur mid-month into a list of numeric values
    def makeMidMonthlyVars(self, variables, conversion, show_output):
        variable_output = []
        # if the variable was not modeled
        if type(variables[0]) == type(0):
            return np.array([0] * len(variables))  # return initial value

        if show_output:
            print("Monthly Output for " + str(variables[0]))

        for month in range(0, self.constants["NMONTHS"]):
            val = variables[month]

            # if something went wrong and the variable was not added for a certain month
            assert type(val) != type(0)
            variable_output.append(val.varValue * conversion)
            if show_output:
                print("    Month " + str(month) + ": " + str(variable_output[month]))
        return np.array(variable_output)

    # order the variables that occur mid-month into a list of numeric values

    def makeMidMonthlyOGKcals(
        self,
        crops_food_eaten_no_rotation,
        crops_food_eaten_with_rotation,
        crops_kcals_produced,
        conversion,
        show_output,
    ):

        immediately_eaten_output = []
        new_stored_eaten_output = []
        cf_eaten_output = []
        cf_produced_output = []

        # if the variable was not modeled
        if type(crops_food_eaten_no_rotation[0]) == type(0):
            return [
                [0] * len(crops_food_eaten_no_rotation),
                [0] * len(crops_food_eaten_no_rotation),
            ]  # return initial value

        if show_output:
            print("Monthly Output for " + str(variables[0]))

        for month in range(0, self.constants["NMONTHS"]):
            cf_produced = crops_kcals_produced[month]
            cf_produced_output.append(cf_produced)
            cf_eaten = (
                crops_food_eaten_no_rotation[month].varValue
                + crops_food_eaten_with_rotation[month].varValue
                * self.constants["OG_ROTATION_FRACTION_KCALS"]
            )
            cf_eaten_output.append(cf_eaten)

            if cf_produced <= cf_eaten:
                immediately_eaten = cf_produced
                new_stored_crops_eaten = cf_eaten - cf_produced
            else:  # crops_food_eaten < crops_kcals_produced
                immediately_eaten = cf_eaten
                new_stored_crops_eaten = 0

            immediately_eaten_output.append(immediately_eaten * conversion)
            new_stored_eaten_output.append(new_stored_crops_eaten * conversion)
            if show_output:
                print(
                    "    Month "
                    + str(month)
                    + ": imm eaten: "
                    + str(immediately_eaten_output[month])
                    + " new stored eaten: "
                    + str(new_stored_eaten_output[month])
                )

        return [immediately_eaten_output, new_stored_eaten_output]

    # order the variables that occur start and end month into list of numeric values
    def makeStartEndMonthlyVars(
        self, variable_start, variable_end, conversion, show_output
    ):

        # if the variable was not modeled
        if type(variable_start[0]) == type(0):
            # return initial value, all zeros
            return [0] * len(variable_start) * 2

        variable_output = []
        if show_output:
            print("Monthly Output for " + str(variable_start[0]))

        for month in range(0, self.constants["NMONTHS"]):
            val = variable_start[month]
            variable_output.append(val.varValue * conversion)
            val = variable_end[month]
            variable_output.append(val.varValue * conversion)
            if show_output:
                print(
                    "    End Month " + str(month) + ": " + str(variable_output[month])
                )
        return variable_output

    # if greenhouses aren't included, these results will be zero

    def analyze_GH_results(
        self,
        greenhouse_kcals_per_ha,
        greenhouse_fat_per_ha,
        greenhouse_protein_per_ha,
        greenhouse_area,
        show_output,
    ):

        # self.greenhouse_kcals_per_ha = self.makeMidMonthlyVars(
        #   greenhouse_kcals_per_ha,
        #   1,
        #   show_output)
        # self.greenhouse_fat_per_ha = self.makeMidMonthlyVars(
        #   greenhouse_fat_per_ha,
        #   1,
        #   show_output)
        # self.greenhouse_protein_per_ha = self.makeMidMonthlyVars(
        #   greenhouse_protein_per_ha,
        #   1,
        #   show_output)
        self.billions_fed_GH_kcals = np.multiply(
            np.array(greenhouse_area),
            np.array(greenhouse_kcals_per_ha) * 1 / self.constants["KCALS_MONTHLY"],
        )

        self.billions_fed_GH_fat = np.multiply(
            np.array(greenhouse_area),
            np.array(greenhouse_fat_per_ha) * 1 / self.constants["FAT_MONTHLY"] / 1e9,
        )

        self.billions_fed_GH_protein = np.multiply(
            np.array(greenhouse_area),
            np.array(greenhouse_protein_per_ha)
            * 1
            / self.constants["PROTEIN_MONTHLY"]
            / 1e9,
        )

    # if fish aren't included, these results will be zero

    def analyze_fish_results(
        self,
        production_kcals_fish_per_month,
        production_fat_fish_per_month,
        production_protein_fish_per_month,
    ):
        self.billions_fed_fish_kcals = (
            np.array(production_kcals_fish_per_month) / self.constants["KCALS_MONTHLY"]
        )

        self.billions_fed_fish_protein = (
            np.array(production_protein_fish_per_month)
            / self.constants["PROTEIN_MONTHLY"]
            / 1e9
        )

        self.billions_fed_fish_fat = (
            np.array(production_fat_fish_per_month)
            / self.constants["FAT_MONTHLY"]
            / 1e9
        )

    # if outdoor growing isn't included, these results will be zero
    def analyze_OG_results(
        self,
        crops_food_eaten_no_rotation,
        crops_food_eaten_with_rotation,
        crops_food_storage_no_rot,
        crops_food_storage_rot,
        crops_food_produced,
        show_output,
    ):
        self.no_rot = self.makeMidMonthlyVars(
            crops_food_eaten_no_rotation, 1, show_output
        )
        self.rot = self.makeMidMonthlyVars(
            crops_food_eaten_with_rotation,
            self.constants["OG_ROTATION_FRACTION_KCALS"],
            show_output,
        )

        CROPS_WASTE = 1 - self.constants["inputs"]["WASTE"]["CROPS"] / 100
        self.billions_fed_OG_storage_no_rot = self.makeMidMonthlyVars(
            crops_food_storage_no_rot,
            CROPS_WASTE / self.constants["KCALS_MONTHLY"],
            show_output,
        )

        self.billions_fed_OG_storage_rot = self.makeMidMonthlyVars(
            crops_food_storage_rot,
            CROPS_WASTE
            * self.constants["OG_ROTATION_FRACTION_KCALS"]
            / self.constants["KCALS_MONTHLY"],
            show_output,
        )

        # immediate from produced and storage changes account for all eaten
        # but storage can come from produced!
        # we know storage_change + all_eaten = produced
        # if(storage_change>=0):
        #   assert(all_eaten >= storage_change)
        #   eaten_from_stored = storage_change
        #   immediately_eaten = all_eaten - eaten_from_stored
        # else:
        #   eaten_from_stored = 0

        og_produced_kcals = np.concatenate(
            [
                np.array(
                    crops_food_produced[
                        0 : self.constants["inputs"][
                            "INITIAL_HARVEST_DURATION_IN_MONTHS"
                        ]
                    ]
                ),
                np.array(
                    crops_food_produced[
                        self.constants["inputs"]["INITIAL_HARVEST_DURATION_IN_MONTHS"] :
                    ]
                )
                * self.constants["OG_ROTATION_FRACTION_KCALS"],
            ]
        )

        [
            self.billions_fed_immediate_OG_kcals_tmp,
            self.billions_fed_new_stored_OG_kcals_tmp,
        ] = self.makeMidMonthlyOGKcals(
            crops_food_eaten_no_rotation,
            crops_food_eaten_with_rotation,
            og_produced_kcals,
            CROPS_WASTE / self.constants["KCALS_MONTHLY"],
            show_output,
        )

        self.billions_fed_immediate_OG_kcals = np.multiply(
            np.array(self.billions_fed_immediate_OG_kcals_tmp),
            self.OG_SF_fraction_kcals_to_humans,
        )

        self.billions_fed_new_stored_OG_kcals = np.multiply(
            np.array(self.billions_fed_new_stored_OG_kcals_tmp),
            self.OG_SF_fraction_kcals_to_humans,
        )

        self.billions_fed_OG_kcals = np.multiply(
            np.array(
                self.makeMidMonthlyVars(
                    crops_food_eaten_no_rotation,
                    CROPS_WASTE / self.constants["KCALS_MONTHLY"],
                    show_output,
                )
            )
            + np.array(
                self.makeMidMonthlyVars(
                    crops_food_eaten_with_rotation,
                    CROPS_WASTE
                    * self.constants["OG_ROTATION_FRACTION_KCALS"]
                    / self.constants["KCALS_MONTHLY"],
                    show_output,
                )
            ),
            self.OG_SF_fraction_kcals_to_humans,
        )

        self.billions_fed_OG_fat = np.multiply(
            np.array(
                self.makeMidMonthlyVars(
                    crops_food_eaten_no_rotation,
                    CROPS_WASTE
                    * self.constants["OG_FRACTION_FAT"]
                    / self.constants["FAT_MONTHLY"]
                    / 1e9,
                    show_output,
                )
            )
            + np.array(
                self.makeMidMonthlyVars(
                    crops_food_eaten_with_rotation,
                    CROPS_WASTE
                    * self.constants["OG_ROTATION_FRACTION_FAT"]
                    / self.constants["FAT_MONTHLY"]
                    / 1e9,
                    show_output,
                )
            ),
            self.OG_SF_fraction_fat_to_humans,
        )

        # EACH MONTH: 1218263.5 billion kcals per person
        # 1000s tons protein equivalent:
        #

        # CROPS FOOD EATEN BILLION KCALS PER PERSON PER MONTH 1094666.5
        # OG_FRACTION_PROTEIN: 1000 tons protein per billion kcals
        # THOU_TONS_PROTEIN_NEEDED: thousands of tons per month for population
        # OG_FRACTION_PROTEIN: 1000tons/billion kcals
        # PROTEIN_MONTHLY: 1000 tons protein per month per person

        # crops_food_eaten_no_rotation:
        #   crops_food_eaten_no_rotation * OG_FRACTION_PROTEIN
        #   / self.single_valued_constants["THOU_TONS_PROTEIN_NEEDED"]

        #   gives a fraction, So

        #   [crops_food_eaten_no_rotation] == [?]
        #   [OG_FRACTION_PROTEIN] = 1000 tons protein per billion kcals
        #   [THOU_TONS_PROTEIN_NEEDED] = thousands of tons per month for population
        #   so, [?] = [thousands of tons per month for population]/[1000 tons protein per billion kcals]
        #   [?] = [billion kcals per month for population]
        #   [crops_food_eaten_no_rotation] = [billion kcals per month for population]
        #   therefore,
        #   [crops_food_eaten_no_rotation]
        #    * [OG_FRACTION_PROTEIN]
        #    / [PROTEIN_MONTHLY]
        #   gives us
        #   [billions_fed_OG_protein] ==
        #   [billion kcals per month for population]
        #   * [1000tons protein/billion kcals]
        #   / [1000 tons protein per month per person]
        #   so
        #   [billions_fed_OG_protein] ==
        #   [people]

        self.billions_fed_OG_protein = np.multiply(
            np.array(
                self.makeMidMonthlyVars(
                    crops_food_eaten_no_rotation,
                    CROPS_WASTE
                    * self.constants["OG_FRACTION_PROTEIN"]
                    / self.constants["PROTEIN_MONTHLY"]
                    / 1e9,
                    show_output,
                )
            )
            + np.array(
                self.makeMidMonthlyVars(
                    crops_food_eaten_with_rotation,
                    CROPS_WASTE
                    * self.constants["OG_ROTATION_FRACTION_PROTEIN"]
                    / self.constants["PROTEIN_MONTHLY"]
                    / 1e9,
                    show_output,
                )
            ),
            self.OG_SF_fraction_protein_to_humans,
        )
        self.billions_fed_OG_produced_kcals = np.multiply(
            CROPS_WASTE * og_produced_kcals / self.constants["KCALS_MONTHLY"],
            self.OG_SF_fraction_kcals_to_humans,
        )

        self.billions_fed_OG_produced_fat = (
            np.multiply(
                np.concatenate(
                    [
                        np.array(
                            crops_food_produced[
                                0 : self.constants["inputs"][
                                    "INITIAL_HARVEST_DURATION_IN_MONTHS"
                                ]
                            ]
                        )
                        * self.constants["OG_FRACTION_FAT"],
                        np.array(
                            crops_food_produced[
                                self.constants["inputs"][
                                    "INITIAL_HARVEST_DURATION_IN_MONTHS"
                                ] :
                            ]
                        )
                        * self.constants["OG_ROTATION_FRACTION_FAT"],
                    ]
                )
                / self.constants["FAT_MONTHLY"]
                / 1e9,
                self.OG_SF_fraction_fat_to_humans,
            )
            * CROPS_WASTE
        )

        self.billions_fed_OG_produced_protein = (
            np.multiply(
                np.concatenate(
                    [
                        np.array(
                            crops_food_produced[
                                0 : self.constants["inputs"][
                                    "INITIAL_HARVEST_DURATION_IN_MONTHS"
                                ]
                            ]
                        )
                        * self.constants["OG_FRACTION_PROTEIN"],
                        np.array(
                            crops_food_produced[
                                self.constants["inputs"][
                                    "INITIAL_HARVEST_DURATION_IN_MONTHS"
                                ] :
                            ]
                        )
                        * self.constants["OG_ROTATION_FRACTION_PROTEIN"],
                    ]
                )
                / self.constants["PROTEIN_MONTHLY"]
                / 1e9,
                self.OG_SF_fraction_protein_to_humans,
            )
            * CROPS_WASTE
        )

    # if cellulosic sugar isn't included, these results will be zero

    def analyze_CS_results(
        self,
        production_kcals_CS_per_month,
    ):

        self.billions_fed_CS_kcals = (
            np.array(production_kcals_CS_per_month) / self.constants["KCALS_MONTHLY"]
        )

    # if methane scp isn't included, these results will be zero

    def analyze_SCP_results(
        self,
        production_kcals_scp_per_month,
        production_fat_scp_per_month,
        production_protein_scp_per_month,
    ):

        self.billions_fed_SCP_kcals = (
            np.array(production_kcals_scp_per_month) / self.constants["KCALS_MONTHLY"]
        )

        self.billions_fed_SCP_fat = (
            np.array(production_fat_scp_per_month) / self.constants["FAT_MONTHLY"] / 1e9
        )

        self.billions_fed_SCP_protein = (
            np.array(production_protein_scp_per_month)
            / self.constants["PROTEIN_MONTHLY"]
            / 1e9
        )

    # if stored food isn't included, these results will be zero
    def analyze_meat_dairy_results(
        self,
        meat_eaten,
        dairy_milk_kcals,
        dairy_milk_fat,
        dairy_milk_protein,
        cattle_maintained_kcals,
        cattle_maintained_fat,
        cattle_maintained_protein,
        h_e_meat_kcals,
        h_e_meat_fat,
        h_e_meat_protein,
        h_e_milk_kcals,
        h_e_milk_fat,
        h_e_milk_protein,
        h_e_balance_kcals,
        h_e_balance_fat,
        h_e_balance_protein,
    ):

        self.billions_fed_meat_kcals_tmp = np.divide(
            meat_eaten, self.constants["KCALS_MONTHLY"]
        )

        self.billions_fed_meat_kcals = (
            self.billions_fed_meat_kcals_tmp
            + np.array(cattle_maintained_kcals) / self.constants["KCALS_MONTHLY"]
        )

        if self.constants["VERBOSE"]:
            pass

        self.billions_fed_meat_fat_tmp = np.multiply(
            meat_eaten,
            self.constants["MEAT_FRACTION_FAT"] / self.constants["FAT_MONTHLY"] / 1e9,
        )

        self.billions_fed_meat_fat = (
            self.billions_fed_meat_fat_tmp
            + np.array(cattle_maintained_fat) / self.constants["FAT_MONTHLY"] / 1e9
        )

        self.billions_fed_meat_protein_tmp = np.multiply(
            meat_eaten,
            self.constants["MEAT_FRACTION_PROTEIN"]
            / self.constants["PROTEIN_MONTHLY"]
            / 1e9,
        )

        self.billions_fed_meat_protein = (
            self.billions_fed_meat_protein_tmp
            + np.array(cattle_maintained_protein)
            / self.constants["PROTEIN_MONTHLY"]
            / 1e9
        )

        self.billions_fed_milk_kcals = (
            np.array(dairy_milk_kcals) / self.constants["KCALS_MONTHLY"]
        )

        self.billions_fed_milk_fat = (
            np.array(dairy_milk_fat) / self.constants["FAT_MONTHLY"] / 1e9
        )

        self.billions_fed_milk_protein = (
            np.array(dairy_milk_protein) / self.constants["PROTEIN_MONTHLY"] / 1e9
        )

        self.billions_fed_h_e_meat_kcals = (
            h_e_meat_kcals / self.constants["KCALS_MONTHLY"]
        )

        self.billions_fed_h_e_meat_fat = (
            h_e_meat_fat / self.constants["FAT_MONTHLY"] / 1e9
        )

        self.billions_fed_h_e_meat_protein = (
            h_e_meat_protein / self.constants["PROTEIN_MONTHLY"] / 1e9
        )

        self.billions_fed_h_e_milk_kcals = (
            h_e_milk_kcals / self.constants["KCALS_MONTHLY"]
        )

        self.billions_fed_h_e_milk_fat = (
            h_e_milk_fat / self.constants["FAT_MONTHLY"] / 1e9
        )

        self.billions_fed_h_e_milk_protein = (
            h_e_milk_protein / self.constants["PROTEIN_MONTHLY"] / 1e9
        )

        self.billions_fed_h_e_balance_kcals = (
            h_e_balance_kcals / self.constants["KCALS_MONTHLY"]
        )

        self.billions_fed_h_e_balance_fat = (
            h_e_balance_fat / self.constants["FAT_MONTHLY"] / 1e9
        )

        self.billions_fed_h_e_balance_protein = (
            h_e_balance_protein / self.constants["PROTEIN_MONTHLY"] / 1e9
        )

        # useful for plotting meat and dairy

        if self.constants["ADD_MEAT"] and self.constants["VERBOSE"]:
            print("Days non egg, non dairy meat global at start, by kcals")
            print(
                360
                * self.constants["INITIAL_MEAT"]
                / (12 * self.constants["KCALS_MONTHLY"])
            )

    # if stored food isn't included, these results will be zero
    def analyze_SF_results(self, stored_food_eaten, show_output):

        CROPS_WASTE = 1 - self.constants["inputs"]["WASTE"]["CROPS"] / 100

        self.billions_fed_SF_kcals = np.multiply(
            self.makeMidMonthlyVars(
                stored_food_eaten,
                CROPS_WASTE / self.constants["KCALS_MONTHLY"],
                show_output,
            ),
            self.OG_SF_fraction_kcals_to_humans,
        )

        self.sf = self.makeMidMonthlyVars(stored_food_eaten, 1, show_output)

        self.billions_fed_SF_fat = np.multiply(
            self.makeMidMonthlyVars(
                stored_food_eaten,
                CROPS_WASTE
                * self.constants["SF_FRACTION_FAT"]
                / self.constants["FAT_MONTHLY"]
                / 1e9,
                show_output,
            ),
            self.OG_SF_fraction_fat_to_humans,
        )

        self.billions_fed_SF_protein = np.multiply(
            self.makeMidMonthlyVars(
                stored_food_eaten,
                CROPS_WASTE
                * self.constants["SF_FRACTION_PROTEIN"]
                / self.constants["PROTEIN_MONTHLY"]
                / 1e9,
                False,
            ),
            self.OG_SF_fraction_protein_to_humans,
        )

        if self.constants["ADD_STORED_FOOD"] and self.constants["VERBOSE"]:
            print("Days stored food global at start, by kcals")
            print(
                365
                * self.constants["INITIAL_SF_KCALS"]
                / (12 * self.constants["KCALS_MONTHLY"])
            )
            print("Days stored food global at start, by fat")
            print(
                365
                * self.constants["INITIAL_SF_KCALS"]
                * self.constants["SF_FRACTION_FAT"]
                / (12 * self.constants["FAT_MONTHLY"] * 1e9)
            )
            print("Days stored food global at start, by protein")
            print(
                365
                * self.constants["INITIAL_SF_KCALS"]
                * self.constants["SF_FRACTION_PROTEIN"]
                / (12 * self.constants["PROTEIN_MONTHLY"] * 1e9)
            )

    def analyze_seaweed_results(
        self,
        seaweed_wet_on_farm,
        used_area,
        built_area,
        seaweed_food_produced,
        show_output,
    ):

        self.seaweed_built_area = built_area
        self.seaweed_built_area_max_density = (
            np.array(built_area) * self.constants["MAXIMUM_DENSITY"]
        )

        self.seaweed_food_produced = self.makeMidMonthlyVars(
            seaweed_food_produced, 1, show_output
        )

        self.billions_fed_seaweed_kcals = self.makeMidMonthlyVars(
            seaweed_food_produced,
            self.constants["SEAWEED_KCALS"] / self.constants["KCALS_MONTHLY"],
            show_output,
        )

        self.billions_fed_seaweed_fat = self.makeMidMonthlyVars(
            seaweed_food_produced,
            self.constants["SEAWEED_FAT"] / self.constants["FAT_MONTHLY"] / 1e9,
            show_output,
        )

        self.billions_fed_seaweed_protein = self.makeMidMonthlyVars(
            seaweed_food_produced,
            self.constants["SEAWEED_PROTEIN"] / self.constants["PROTEIN_MONTHLY"] / 1e9,
            show_output,
        )

    # The optimizer will maximize minimum fat, calories, and protein over any month, but it does not care which sources these come from. The point of this function is to determine the probable contributions to excess calories used for feed and biofuel from appropriate sources (unless this has been updated, it takes it exclusively from outdoor growing and stored food).
    # there is also a constraint to make sure the sources which can be used for feed are not exhausted, and the model will not be able to solve if the usage from biofuels and feed are more than the available stored food and outdoor crop production.

    def compute_excess_after_run(self, model):

        # I spent like five hours trying to figure out why the answer was wrong
        # until I finally found an issue with string ordering, fixed it below

        humans_fed_kcals = []
        humans_fed_fat = []
        humans_fed_protein = []
        order_kcals = []
        order_fat = []
        order_protein = []
        for var in model.variables():

            if "Humans_Fed_Kcals_" in var.name:
                humans_fed_kcals.append(
                    var.value() / 100 * self.constants["POP_BILLIONS"]
                )

                order_kcals.append(
                    int(var.name[len("Humans_Fed_Kcals_") :].split("_")[0])
                )

            if "Humans_Fed_Fat_" in var.name:
                order_fat.append(int(var.name[len("Humans_Fed_Fat_") :].split("_")[0]))

                humans_fed_fat.append(
                    var.value() / 100 * self.constants["POP_BILLIONS"]
                )

            if "Humans_Fed_Protein_" in var.name:

                order_protein.append(
                    int(var.name[len("Humans_Fed_Protein_") :].split("_")[0])
                )

                humans_fed_protein.append(
                    var.value() / 100 * self.constants["POP_BILLIONS"]
                )

        zipped_lists = zip(order_kcals, humans_fed_kcals)
        sorted_zipped_lists = sorted(zipped_lists)
        self.humans_fed_kcals_optimizer = [
            element for _, element in sorted_zipped_lists
        ]

        zipped_lists = zip(order_fat, humans_fed_fat)
        sorted_zipped_lists = sorted(zipped_lists)
        self.humans_fed_fat_optimizer = [element for _, element in sorted_zipped_lists]

        zipped_lists = zip(order_protein, humans_fed_protein)
        sorted_zipped_lists = sorted(zipped_lists)
        self.humans_fed_protein_optimizer = [
            element for _, element in sorted_zipped_lists
        ]

        # when calculating the excess calories, the amount of human edible feed
        # used can't be more than the excess calories. Because the baseline feed
        # usage is higher than in nuclear winter, we don't want to increase
        # feed usage before the shutoff.

        feed_delay = self.constants["inputs"]["DELAY"]["FEED_SHUTOFF_MONTHS"]
        sum_before = np.sum(
            (
                np.array(self.humans_fed_kcals_optimizer)[:feed_delay]
                - self.constants["POP_BILLIONS"]
            )
        )

        FRACTION_EXCESS_TO_REMOVE_NEXT_TIME = 0.1

        if feed_delay >= self.constants["NMONTHS"]:
            self.excess_after_run = (
                (
                    np.array(self.humans_fed_kcals_optimizer)
                    - self.constants["POP_BILLIONS"]
                )
                * self.constants["KCALS_MONTHLY"]
                * FRACTION_EXCESS_TO_REMOVE_NEXT_TIME
            )
        else:
            # any consistent monthly excess is subtracted
            # also spread out excess calories in pre-"feed shutoff" months
            # to be used in months after feed is shutoff
            # np.array(self.sf+self.rot+self.no_rot) \
            self.excess_after_run = (
                (
                    np.array(self.humans_fed_kcals_optimizer)
                    - self.constants["POP"]
                    / 1e9  # + (sum_before)/(self.constants["NMONTHS"]-feed_delay)
                )
                * self.constants["KCALS_MONTHLY"]
                * FRACTION_EXCESS_TO_REMOVE_NEXT_TIME
            )

    def calc_fraction_OG_SF_to_humans(
        self,
        model,
        crops_food_eaten_no_rotation,
        crops_food_eaten_with_rotation,
        stored_food_eaten,
        excess_calories,
        excess_fat_used,
        excess_protein_used,
    ):

        self.are_excess_kcals = (excess_calories > 0).any()
        CROPS_WASTE = 1 - self.constants["inputs"]["WASTE"]["CROPS"] / 100
        self.excess = excess_calories
        """
        each month:
            (all the sources except using human edible fed food) + (-excess provided) + (meat and dairy from human edible sources)
            =
            (all the sources except using human edible fed food)*(fraction fed to humans) + (meat and dairy from human edible sources) 
        because each month:
            1 + (-excess provided)/(all the sources except using human edible fed food)
            =
            (fraction fed to humans)
        
        so then we let

        (all the sources except using human edible fed food)*(fraction fed to humans)
        ==
        (all the sources except using human edible fed food) + (-excess provided)

        let:
        a = all the sources except using human edible fed food
        b = excess
        c = fraction fed to humans
        d = meat and dairy from human edible sources
        e = humans actually fed from everything together

        Perhaps this (inscrutible?) algebra will be helpful to you

        a-b = a*c => c = (a-b)/a = 1-b/a

        and if:
        a+d-b=e
        a=b-d+e

        then we have

        c = 1 - b/(b-d+e)
        
        """
        SF_kcals = self.makeMidMonthlyVars(
            stored_food_eaten, 1 / self.constants["KCALS_MONTHLY"], False
        )

        SF_fat = self.makeMidMonthlyVars(
            stored_food_eaten,
            self.constants["SF_FRACTION_FAT"] / self.constants["FAT_MONTHLY"] / 1e9,
            False,
        )
        SF_protein = self.makeMidMonthlyVars(
            stored_food_eaten,
            self.constants["SF_FRACTION_PROTEIN"]
            / self.constants["PROTEIN_MONTHLY"]
            / 1e9,
            False,
        )

        OG_kcals = np.array(
            self.makeMidMonthlyVars(
                crops_food_eaten_no_rotation, 1 / self.constants["KCALS_MONTHLY"], False
            )
        ) + np.array(
            self.makeMidMonthlyVars(
                crops_food_eaten_with_rotation,
                self.constants["OG_ROTATION_FRACTION_KCALS"]
                / self.constants["KCALS_MONTHLY"],
                False,
            )
        )
        OG_fat = np.array(
            self.makeMidMonthlyVars(
                crops_food_eaten_no_rotation,
                self.constants["OG_FRACTION_FAT"] / self.constants["FAT_MONTHLY"] / 1e9,
                False,
            )
        ) + np.array(
            self.makeMidMonthlyVars(
                crops_food_eaten_with_rotation,
                self.constants["OG_ROTATION_FRACTION_FAT"]
                / self.constants["FAT_MONTHLY"]
                / 1e9,
                False,
            )
        )

        OG_protein = np.array(
            self.makeMidMonthlyVars(
                crops_food_eaten_no_rotation,
                self.constants["OG_FRACTION_PROTEIN"]
                / self.constants["PROTEIN_MONTHLY"]
                / 1e9,
                False,
            )
        ) + np.array(
            self.makeMidMonthlyVars(
                crops_food_eaten_with_rotation,
                self.constants["OG_ROTATION_FRACTION_PROTEIN"]
                / self.constants["PROTEIN_MONTHLY"]
                / 1e9,
                False,
            )
        )

        total_production = (np.array(OG_kcals) + np.array(SF_kcals)) * self.constants[
            "KCALS_MONTHLY"
        ]

        OG_SF_fraction_kcals_to_feed = np.divide(excess_calories, total_production)

        # if the total production is zero, then the fraction is zero
        OG_SF_fraction_kcals_to_feed = np.where(
            total_production == 0, 0, OG_SF_fraction_kcals_to_feed
        )

        OG_SF_fraction_kcals_to_humans = 1 - OG_SF_fraction_kcals_to_feed

        # it seems impossible for there to be more fat used for feed than actually produced from all the sources, if the optimizer spits out a positive number of people fed in terms of fat.
        # The estimate for amount used for feed divides the excess by all the sources (except human edible feed). If the excess is greater than the sources, we have a problem.
        # The sources actually added to get humans_fed_fat, does however include the excess as a negative number. The excess is added to humans_fat_fed to cancel this. Also, humans_fed_fat includes meat and milk from human edible.
        # So the only reason it doesnt actually go negative is because the optimizer takes an optimization including the human edible fat which pushes it to some positive balance of people fed in terms of fat.
        # So its not impossible, it just means that the part of the excess which required more fat had to come from the animal outputs themselves.
        # By adding a requirement that the fat, calories and protein need to be satisfied before human edible produce meat is taken into account we will have 100% of resources spent on meeting these requirements and 0% going to humans. The optimizer will still

        OG_SF_fraction_fat_to_feed = np.divide(
            excess_fat_used,
            (np.array(OG_fat) + np.array(SF_fat)) * self.constants["FAT_MONTHLY"] * 1e9,
        )

        OG_SF_fraction_fat_to_feed = np.where(
            total_production == 0, 0, OG_SF_fraction_fat_to_feed
        )

        OG_SF_fraction_fat_to_humans = 1 - OG_SF_fraction_fat_to_feed

        OG_SF_fraction_protein_to_feed = np.divide(
            excess_protein_used,
            (np.array(OG_protein) + np.array(SF_protein))
            * self.constants["PROTEIN_MONTHLY"]
            * 1e9,
        )
        OG_SF_fraction_protein_to_feed = np.where(
            total_production == 0, 0, OG_SF_fraction_protein_to_feed
        )

        OG_SF_fraction_protein_to_humans = 1 - OG_SF_fraction_protein_to_feed

        FEED_NAN = np.isnan(OG_SF_fraction_kcals_to_feed).any()

        MORE_THAN_AVAILABLE_USED_FOR_FEED = not (
            OG_SF_fraction_kcals_to_feed <= 1 + 1e-5
        ).all()

        NEGATIVE_FRACTION_FEED = not (OG_SF_fraction_kcals_to_feed >= 0).all()

        if FEED_NAN:
            print("ERROR: Feed not a number")
            quit()

        if MORE_THAN_AVAILABLE_USED_FOR_FEED:
            print("")
            print(
                "ERROR: Attempted to feed more food to animals than exists available outdoor growing fat, calories, or protein. Scenario is impossible."
            )
            quit()

        if NEGATIVE_FRACTION_FEED:
            print("ERROR: fraction feed to humans is negative")
            quit()

        assert (OG_SF_fraction_kcals_to_feed <= 1 + 1e-5).all()

        if (OG_SF_fraction_kcals_to_feed >= 1).any():
            OG_SF_fraction_kcals_to_humans[OG_SF_fraction_kcals_to_feed >= 1] = 0

        assert (OG_SF_fraction_kcals_to_feed >= 0).all()
        if self.constants["inputs"]["INCLUDE_FAT"]:
            assert (OG_SF_fraction_fat_to_feed <= 1 + 1e-5).all()
            assert (OG_SF_fraction_fat_to_feed >= 0).all()
        if self.constants["inputs"]["INCLUDE_PROTEIN"]:
            assert (OG_SF_fraction_protein_to_feed <= 1 + 1e-5).all()
            assert (OG_SF_fraction_protein_to_feed >= 0).all()

        self.OG_SF_fraction_kcals_to_humans = OG_SF_fraction_kcals_to_humans
        self.OG_SF_fraction_fat_to_humans = OG_SF_fraction_fat_to_humans
        self.OG_SF_fraction_protein_to_humans = OG_SF_fraction_protein_to_humans

    def analyze_results(self, model, time_months_middle):

        # number of months after ASRS onset which the variables are represented
        # in data arrays
        self.time_months_middle = time_months_middle

        if not (
            (self.sf + self.rot + self.no_rot - self.excess) * 1e9 / 4e6 / 1e6 >= -1e-5
        ).all():
            print(
                "There are too few calories available to meet the caloric excess provided to the simulator. This is probably because the optimizer seems to have failed to sufficiently meet the constraint to limit total food fed to animals to the sum of stored food and outdoor growing within a reasonable degree of precision. Consider reducing precision. Quitting."
            )
            quit()

        assert (
            (self.sf + self.rot + self.no_rot - self.excess) * 1e9 / 4e6 / 1e6 >= -1e-5
        ).all()
        if (
            (self.sf + self.rot + self.no_rot - self.excess) * 1e9 / 4e6 / 1e6 <= 0
        ).any():
            if True:
                print("")
                print(
                    "WARNING: All of the outdoor growing and stored food is being fed to animals and none to humans in months: "
                )
                print(
                    np.where(
                        (self.sf + self.rot + self.no_rot - self.excess)
                        * 1e9
                        / 4e6
                        / 1e6
                        <= 0
                    )
                )
                print("Double check this is actually reasonable.")
                print("")

        self.kcals_fed = (
            np.array(self.billions_fed_SF_kcals)
            + np.array(self.billions_fed_meat_kcals)
            + np.array(self.billions_fed_seaweed_kcals)
            + np.array(self.billions_fed_milk_kcals)
            + np.array(self.billions_fed_CS_kcals)
            + np.array(self.billions_fed_SCP_kcals)
            + np.array(self.billions_fed_GH_kcals)
            + np.array(self.billions_fed_OG_kcals)
            + np.array(self.billions_fed_fish_kcals)
            + self.billions_fed_h_e_meat_kcals
            + self.billions_fed_h_e_milk_kcals
        )

        self.fat_fed = (
            np.array(self.billions_fed_SF_fat)
            + np.array(self.billions_fed_meat_fat)
            + np.array(self.billions_fed_seaweed_fat)
            + np.array(self.billions_fed_milk_fat)
            + np.array(self.billions_fed_SCP_fat)
            + np.array(self.billions_fed_GH_fat)
            + np.array(self.billions_fed_OG_fat)
            + np.array(self.billions_fed_fish_fat)
            + self.billions_fed_h_e_meat_fat
            + self.billions_fed_h_e_milk_fat
        )

        self.protein_fed = (
            (
                np.array(self.billions_fed_SF_protein)
                + np.array(self.billions_fed_meat_protein)
                + np.array(self.billions_fed_seaweed_protein)
                + np.array(self.billions_fed_milk_protein)
                + np.array(self.billions_fed_GH_protein)
                + np.array(self.billions_fed_SCP_protein)
                + np.array(self.billions_fed_OG_protein)
                + np.array(self.billions_fed_fish_protein)
            )
            + self.billions_fed_h_e_meat_protein
            + self.billions_fed_h_e_milk_protein
        )

        assert (
            abs(
                np.divide(
                    self.kcals_fed - np.array(self.humans_fed_kcals_optimizer),
                    self.kcals_fed,
                )
            )
            < 1e-6
        ).all()
        if self.constants["inputs"]["INCLUDE_FAT"]:
            assert (
                abs(
                    np.divide(
                        self.fat_fed - np.array(self.humans_fed_fat_optimizer),
                        self.fat_fed,
                    )
                )
                < 1e-6
            ).all()

        if self.constants["inputs"]["INCLUDE_PROTEIN"]:

            assert (
                abs(
                    np.divide(
                        self.protein_fed - np.array(self.humans_fed_protein_optimizer),
                        self.protein_fed,
                    )
                )
                < 1e-6
            ).all()

        SF_OG_kcals = np.array(self.billions_fed_SF_kcals) + np.array(
            self.billions_fed_OG_kcals
        )
        SF_OG_fat = np.array(self.billions_fed_SF_fat) + np.array(
            self.billions_fed_OG_fat
        )
        SF_OG_protein = np.array(self.billions_fed_SF_protein) + np.array(
            self.billions_fed_OG_protein
        )

        # if it takes all the available ag production to produce minimum for biofuel and animal feed demands
        division = []

        # divide off the reduction to get
        CROPS_WASTE = 1 - self.constants["inputs"]["WASTE"]["CROPS"] / 100

        for zipped_lists in zip(
            SF_OG_kcals, self.OG_SF_fraction_kcals_to_humans, self.excess
        ):

            if zipped_lists[1] <= 0:
                assert zipped_lists[0] >= -1e-5
                division.append(
                    zipped_lists[2] / self.constants["KCALS_MONTHLY"] * CROPS_WASTE
                )
            else:
                division.append(zipped_lists[0] / zipped_lists[1])

        # a-b==a*c
        # if a==b,c == 0
        # if b>a, we don't have enough stored food and OG to produced food, and should quit.
        # This may happen even if there is plenty of food to go around, because the stored food needs to
        # If we optimize such that stored food is used in one part while culled meat is used in another, and that generates excess calories above world demand

        denominator = (
            SF_OG_kcals
            + self.billions_fed_h_e_meat_kcals
            + self.billions_fed_h_e_milk_kcals
        )

        fractional_difference = np.divide(
            (
                SF_OG_kcals
                + self.billions_fed_h_e_meat_kcals
                + self.billions_fed_h_e_milk_kcals
            )
            - (np.array(division) + self.billions_fed_h_e_balance_kcals),
            denominator,
        )

        fractional_difference = np.where(denominator == 0, 0, fractional_difference)

        assert (abs(fractional_difference) < 1e-6).all()

        if self.constants["inputs"]["INCLUDE_FAT"]:
            division = []
            for zipped_lists in zip(SF_OG_fat, self.OG_SF_fraction_fat_to_humans):

                if zipped_lists[1] <= 0:
                    assert zipped_lists[0] >= -1e-5
                    division.append(0)
                else:
                    division.append(zipped_lists[0] / zipped_lists[1])

            denominator = (
                SF_OG_fat
                + self.billions_fed_h_e_meat_fat
                + self.billions_fed_h_e_milk_fat
            )

            fractional_difference = np.divide(
                (
                    SF_OG_fat
                    + self.billions_fed_h_e_meat_fat
                    + self.billions_fed_h_e_milk_fat
                )
                - (np.array(division) + self.billions_fed_h_e_balance_fat),
                denominator,
            )

            fractional_difference = np.where(denominator == 0, 0, fractional_difference)

            assert (abs(fractional_difference) < 1e-6).all()

        if self.constants["inputs"]["INCLUDE_PROTEIN"]:

            division = []
            for zipped_lists in zip(
                SF_OG_protein, self.OG_SF_fraction_protein_to_humans
            ):

                if zipped_lists[1] <= 0:
                    assert zipped_lists[0] >= -1e-5
                    division.append(0)
                else:
                    division.append(zipped_lists[0] / zipped_lists[1])

            # a separate problem is if we have a primary restriction on protein or fat rather than calories, the rebalancer will try to get the calories the same for each month, but then even if there are enough calories, this will force protein used to be more than is available from outdoor growing and stored food.

            denominator = (
                SF_OG_protein
                + self.billions_fed_h_e_meat_protein
                + self.billions_fed_h_e_milk_protein
            )

            fractional_difference = np.divide(
                (
                    SF_OG_protein
                    + self.billions_fed_h_e_meat_protein
                    + self.billions_fed_h_e_milk_protein
                )
                - (np.array(division) + self.billions_fed_h_e_balance_protein),
                denominator,
            )

            fractional_difference = np.where(denominator == 0, 0, fractional_difference)

            assert (abs(fractional_difference) < 1e-6).all()

        self.percent_people_fed = model.objective.value()

        fed = {
            "fat": np.round(np.min(self.fat_fed), 2),
            "kcals": np.round(np.min(self.kcals_fed), 2),
            "protein": np.round(np.min(self.protein_fed), 2),
        }
        mins = [key for key in fed if all(fed[temp] >= fed[key] for temp in fed)]

        PRINT_FED = False
        if PRINT_FED:
            print(fed)

            print("Nutrients with constraining values are: " + str(mins))
            print(
                "Estimated percent people fed is " + str(self.percent_people_fed) + "%"
            )
        return [self.percent_people_fed, mins]

    # billions of kcals
    def countProduction(self, months):

        kcals = self.kcals_fed * self.constants["KCALS_MONTHLY"]

        kcals_sum = 0
        for month in months:
            kcals_sum = kcals_sum + kcals[month - 1]

        return kcals_sum
