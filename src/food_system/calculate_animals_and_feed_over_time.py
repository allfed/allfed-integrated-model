"""
This is a function used to quickly estimate the feed usage and resulting meat when 
breeding is changed and slaughter is increased somewhat (or whatever reasonable result
is to be expected in the scenario in question).


"""

import pathlib
import pandas as pd
from difflib import diff_bytes
import numpy as np

# from dash import Dash, dcc, html, Output, Input, dash_table  # pip install dash
# import dash_bootstrap_components as dbc  # pip install dash-bootstrap-components

"""
Start main function
"""
# Create dataframes


class CalculateAnimalOutputs:
    def init():
        pass

    def calculate_feed_and_animals(
        reduction_in_beef_calves,
        reduction_in_dairy_calves,
        increase_in_slaughter,
        reduction_in_pig_breeding,
        reduction_in_poultry_breeding,
        months,
        discount_rate,
        mother_slaughter,
        use_grass_and_residues_for_dairy,
        animal_inputs,
    ):  # function arguments come from the component property of the Input (in this case, the sliders)

        tons_to_kcals = (
            (3560 + 3350) / 2 * 1000
        )  # convert tons to kcals (ASSUME CALORIC DENSITY IS HALF MAIZE, HALF SOYBEAN)
        kcals_to_billion_kcals = 1e-9
        feed_unit_adjust = (
            0.000453592 * tons_to_kcals * kcals_to_billion_kcals
        )  # convert pounds to tonnes to billions of kcals
        ## unpack all the dataframe information for ease of use ##
        # pigs
        total_pigs = animal_inputs.dataframe.loc["TotalPigs", "Qty"]
        piglets_pm = animal_inputs.dataframe.loc["PigletsPerMonth", "Qty"]
        pigs_slaughter_pm = animal_inputs.dataframe.loc["SlaughterPerMonth", "Qty"]
        pigGestation = animal_inputs.dataframe.loc["pigGestation", "Qty"]
        piglets_per_litter = animal_inputs.dataframe.loc["PigsPerLitter", "Qty"]

        # poultry
        total_poultry = animal_inputs.dataframe.loc["Broiler Population", "Qty"]
        poultry_slaughter_pm = animal_inputs.dataframe.loc[
            "poultry_slaughter_pm", "Qty"
        ]  # USDA
        chicks_pm = poultry_slaughter_pm  # assume the same, no data
        poultryGestation = animal_inputs.dataframe.loc[
            "Chicken Gestation", "Qty"
        ]  # USDA  # actaully 21 days, let's round to 1 month

        # cows (more complex, as need to split dairy and beef)
        total_calves = animal_inputs.dataframe.loc["Calves under 500 pounds", "Qty"]
        dairy_cows = animal_inputs.dataframe.loc["Milk cows", "Qty"]
        beef_cows = animal_inputs.dataframe.loc["Beef cows", "Qty"]
        beef_steers = animal_inputs.dataframe.loc["Steers 500 pounds and over", "Qty"]
        heifers = animal_inputs.dataframe.loc["Heifers 500 pounds and over", "Qty"]
        bulls = animal_inputs.dataframe.loc["Bulls 500 pounds and over", "Qty"]
        new_calves_per_year = animal_inputs.dataframe.loc["Calf crop", "Qty"]
        cattle_on_feed = animal_inputs.dataframe.loc["Cattle on feed", "Qty"]
        cow_slaughter_pm = animal_inputs.dataframe.loc["CowSlaughter", "Qty"]
        cowGestation = animal_inputs.dataframe.loc["cowGestation", "Qty"]
        calves_per_mother = 1

        #### Calcultaion for cows ratios
        # calaculate number of cows using ratios
        dairy_beef_mother_ratio = dairy_cows / beef_cows
        dairy_heifers = heifers * dairy_beef_mother_ratio
        beef_heifers = heifers - dairy_heifers

        dairy_calves = dairy_beef_mother_ratio * total_calves
        beef_calves = total_calves - dairy_calves
        dairy_calf_steers = dairy_calves / 2
        dairy_calf_girls = dairy_calves / 2

        calves_destined_for_beef_ratio = (
            beef_calves + dairy_calf_steers
        ) / total_calves
        new_beef_calfs = calves_destined_for_beef_ratio * new_calves_per_year
        new_dairy_calfs = new_calves_per_year - new_beef_calfs
        new_beef_calfs_pm = new_beef_calfs / 12
        new_dairy_calfs_pm = new_dairy_calfs / 12

        cattle_in_beef_track = (
            dairy_calf_steers + beef_calves + beef_steers + beef_cows + beef_heifers
        )
        cattle_in_dairy_track = dairy_calf_girls + dairy_cows + dairy_heifers

        # other baseline variables
        dairy_life_expectancy = 5

        ## End cows, and basic animal variable defintiions ##

        # interventions, scale appropriately for maths (i.e convert sliders from % to decimal)
        reduction_in_beef_calves *= 0.01
        reduction_in_dairy_calves *= 0.01
        reduction_in_pig_breeding *= 0.01
        reduction_in_poultry_breeding *= 0.01
        increase_in_slaughter *= 0.01

        # per month values
        other_cow_death_rate = 0.005  # from USDA
        other_pig_death_rate = 0.005  # from USDA
        other_poultry_death_rate = 0.005
        new_beef_calfs_pm = new_beef_calfs / 12
        new_dairy_calfs_pm = new_dairy_calfs / 12
        new_pigs_pm = piglets_pm
        new_poultry_pm = chicks_pm

        # pregnant animals
        current_pregnant_sows = piglets_pm / piglets_per_litter
        current_pregnant_cows = new_beef_calfs_pm / calves_per_mother
        sow_slaughter_percent = mother_slaughter  # of total percent of pig slaughter
        mother_cow_slaughter_percent = (
            mother_slaughter  # of total percent of cow slaughter
        )

        #### Slaughtering ####
        ### Slaughtering variables (currently hardcoded !!)
        # total slaughter capacity
        cow_slaughter_hours = (
            4  # resources/hours of single person hours for slaughter of cow
        )
        pig_slaughter_hours = (
            4  # resources/hours of single person hours for slaughter of pig
        )
        poultry_slaughter_hours = (
            0.08  # resources/hours of single person hours for slaughter of poultry
        )
        total_slaughter_cap_hours = (
            cow_slaughter_pm * cow_slaughter_hours
            + pigs_slaughter_pm * pig_slaughter_hours
            + poultry_slaughter_pm * poultry_slaughter_hours
        )
        skill_transfer_discount_chickens_to_pigs = (100 - discount_rate) / 100  #
        skill_transfer_discount_pigs_to_cows = (100 - discount_rate) / 100  #

        ## Slaughtering Updates, increases from slider
        total_slaughter_cap_hours *= increase_in_slaughter  # measured in hours
        current_cow_slaughter = (
            cow_slaughter_pm * increase_in_slaughter
        )  # measured in head
        current_poultry_slaughter = (
            poultry_slaughter_pm * increase_in_slaughter
        )  # measured in head
        current_pig_slaughter = (
            pigs_slaughter_pm * increase_in_slaughter
        )  # measured in head
        spare_slaughter_hours = 0

        ## define current totals
        # current_beef_feed_cattle = cattle_on_feed
        current_beef_cattle = cattle_in_beef_track
        current_dairy_cattle = cattle_in_dairy_track
        current_total_pigs = total_pigs
        current_total_poultry = total_poultry

        ### FEED #commented out code is bottom up from roam page
        # beef_cow_feed_pm_per_cow = 880 # lbs
        # dairy_cow_feed_pm_per_cow = 1048
        # poultry_feed_pm_per_bird = 20
        # pig_feed_pm_per_pig = 139

        # these feed numbers are top down, calculations in google sheet, working backwards from total feed used and dividing it evenly amongst the animal populations
        beef_cow_feed_pm_per_cow = 137.3117552  # lbs
        if use_grass_and_residues_for_dairy:
            dairy_cow_feed_pm_per_cow = 0
        else:
            dairy_cow_feed_pm_per_cow = 448.3820431
        poultry_feed_pm_per_bird = 4.763762808
        pig_feed_pm_per_pig = 141.8361586
        baseline_feed = (
            current_total_poultry * poultry_feed_pm_per_bird
            + current_total_pigs * pig_feed_pm_per_pig
            + current_beef_cattle * beef_cow_feed_pm_per_cow
            + current_dairy_cattle * dairy_cow_feed_pm_per_cow
        )

        d = []  # create empty list to place variables in to in loop

        # simulate x months
        for i in range(months):

            new_pigs_pm = current_pregnant_sows * piglets_per_litter
            new_beef_calfs_pm = current_pregnant_cows * calves_per_mother

            # determine birth rates
            if np.abs(i - cowGestation) <= 0.5:
                new_beef_calfs_pm *= 1 - reduction_in_beef_calves
                new_dairy_calfs_pm *= 1 - reduction_in_dairy_calves
                current_pregnant_cows *= 1 - reduction_in_beef_calves

            if np.abs(i - pigGestation) <= 0.5:
                new_pigs_pm *= 1 - reduction_in_pig_breeding
                current_pregnant_sows *= 1 - reduction_in_pig_breeding

            if np.abs(i - poultryGestation) <= 0.5:
                new_poultry_pm *= 1 - reduction_in_poultry_breeding

            if new_pigs_pm < 0:
                new_pigs_pm = 0

            if new_beef_calfs_pm < 0:
                new_beef_calfs_pm = 0

            # Transfer excess slaughter capacity to next animal, current coding method only allows poultry -> pig -> cow, there are some small erros here due to rounding, and the method is not 100% water tight but errors are within the noise
            if current_total_poultry < current_poultry_slaughter:
                spare_slaughter_hours = (
                    current_poultry_slaughter - current_total_poultry
                ) * poultry_slaughter_hours
                current_poultry_slaughter = current_total_poultry
                current_pig_slaughter += (
                    spare_slaughter_hours
                    * skill_transfer_discount_chickens_to_pigs
                    / pig_slaughter_hours
                )
            if current_total_pigs < current_pig_slaughter:
                spare_slaughter_hours = (
                    current_pig_slaughter - current_total_pigs
                ) * pig_slaughter_hours
                current_pig_slaughter = current_total_pigs
                current_cow_slaughter += (
                    spare_slaughter_hours
                    * skill_transfer_discount_pigs_to_cows
                    / cow_slaughter_hours
                )

            # this set up only kills dairy cows when they are getting to the end of their life.
            current_dairy_slaughter = current_dairy_cattle / (
                dairy_life_expectancy * 12
            )
            current_beef_slaughter = current_cow_slaughter - current_dairy_slaughter
            if current_beef_cattle < current_beef_slaughter:
                actual_beef_slaughter = current_beef_cattle  # required due to the difference between actual slaughter and 'slaughter capacity' consider a rewrite of the whole method to distinuguish between these two. For now, this is thr workaround.
            else:
                actual_beef_slaughter = current_beef_slaughter

            other_beef_death = other_cow_death_rate * current_beef_cattle
            other_dairy_death = other_cow_death_rate * current_dairy_cattle
            other_pig_death = current_total_pigs * other_pig_death_rate
            other_poultry_death = current_total_poultry * other_poultry_death_rate

            ## Feed
            current_beef_feed = current_beef_cattle * beef_cow_feed_pm_per_cow
            current_dairy_feed = current_dairy_cattle * dairy_cow_feed_pm_per_cow
            current_pig_feed = current_total_pigs * pig_feed_pm_per_pig
            current_poultry_feed = current_total_poultry * poultry_feed_pm_per_bird

            current_feed_combined = (
                current_beef_feed
                + current_dairy_feed
                + current_pig_feed
                + current_poultry_feed
            )

            print(current_poultry_feed * feed_unit_adjust)
            print(current_feed_combined * feed_unit_adjust)

            ### Generate list (before new totals have been calculated)
            # magnitude adjust moves the numbers from per thousnad head to per head (or other)
            # feed adjust turns lbs in to tons
            d.append(
                {
                    "Beef Pop": current_beef_cattle,
                    "Beef Born": new_beef_calfs_pm,
                    "Beef Slaughtered": actual_beef_slaughter,
                    "Beef Slaughtered Hours": actual_beef_slaughter
                    * cow_slaughter_hours,
                    "Beef Slaughtered Hours %": actual_beef_slaughter
                    * cow_slaughter_hours
                    / total_slaughter_cap_hours,
                    "Beef Other Death": other_beef_death,
                    "Beef Feed": current_beef_cattle
                    * beef_cow_feed_pm_per_cow
                    * feed_unit_adjust,
                    "Dairy Pop": current_dairy_cattle,
                    "Dairy Born": new_dairy_calfs_pm,
                    "Dairy Slaughtered": current_dairy_slaughter,
                    "Dairy Slaughtered Hours": current_dairy_slaughter
                    * cow_slaughter_hours,
                    "Dairy Slaughtered Hours %": current_dairy_slaughter
                    * cow_slaughter_hours
                    / total_slaughter_cap_hours,
                    "Dairy Other Death": other_dairy_death,
                    "Dairy Feed": current_dairy_cattle
                    * dairy_cow_feed_pm_per_cow
                    * feed_unit_adjust,
                    "Pigs Pop": current_total_pigs,
                    "Pig Born": new_pigs_pm,
                    "Pig Slaughtered": current_pig_slaughter,
                    "Pig Slaughtered Hours": current_pig_slaughter
                    * pig_slaughter_hours,
                    "Pig Slaughtered Hours %": current_pig_slaughter
                    * pig_slaughter_hours
                    / total_slaughter_cap_hours,
                    "Pigs Feed": current_total_pigs
                    * pig_feed_pm_per_pig
                    * feed_unit_adjust,
                    "Poultry Pop": current_total_poultry,
                    "Poultry Born": new_poultry_pm,
                    "Poultry Slaughtered": current_poultry_slaughter,
                    "Poultry Slaughtered Hours": current_poultry_slaughter
                    * poultry_slaughter_hours,
                    "Poultry Slaughtered Hours %": current_poultry_slaughter
                    * poultry_slaughter_hours
                    / total_slaughter_cap_hours,
                    "Poultry Feed": current_total_poultry
                    * poultry_feed_pm_per_bird
                    * feed_unit_adjust,
                    "Combined Feed": current_feed_combined * feed_unit_adjust,
                    "Combined Saved Feed": (baseline_feed - current_feed_combined)
                    * feed_unit_adjust,
                    "Month": i,
                }
            )

            # some up new totals
            current_beef_cattle += (
                new_beef_calfs_pm - current_beef_slaughter - other_beef_death
            )
            current_dairy_cattle += (
                new_dairy_calfs_pm - current_dairy_slaughter - other_dairy_death
            )
            current_total_poultry += (
                new_poultry_pm - current_poultry_slaughter - other_poultry_death
            )
            current_total_pigs += new_pigs_pm - current_pig_slaughter - other_pig_death

            current_pregnant_sows -= sow_slaughter_percent * (
                current_pig_slaughter + other_pig_death
            )
            current_pregnant_cows -= mother_cow_slaughter_percent * (
                current_beef_slaughter + other_beef_death
            )

            if current_beef_cattle < 0:
                current_beef_cattle = 0
            if current_dairy_cattle < 0:
                current_dairy_cattle = 0

        ### End of loop, start summary

        df_final = pd.DataFrame(d)

        return df_final


class ModelAnimalInputs:
    def __init__(self, dataframe):
        self.dataframe = dataframe


"""
Start main function
"""
# Import CSV to dataframes
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()
df_animals = pd.read_csv(
    DATA_PATH.joinpath("InputDataAndSources.csv"), index_col="Variable"
)

## various scenarios can be used here
df_baseline_vars = pd.read_csv(
    DATA_PATH.joinpath("default_slider_values.csv"), index_col="Variable"
)  # change this to saved model values (optimistic/pessimistic etc.)
