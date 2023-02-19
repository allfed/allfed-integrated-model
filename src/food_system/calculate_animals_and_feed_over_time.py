"""
This is a function used to quickly estimate the feed usage and resulting meat when
breeding is changed and slaughter is increased somewhat (or whatever reasonable result
is to be expected in the scenario in question).


"""

import pathlib
import pandas as pd
import numpy as np

# from dash import Dash, dcc, html, Output, Input, dash_table  # pip install dash
# import dash_bootstrap_components as dbc  # pip install dash-bootstrap-components

"""
Start main function
"""
# Create dataframes


class CalculateAnimalOutputs:
    def __init__(self):
        self.animal_inputs = ModelAnimalInputs(df_animals)

    def calculate_feed_and_animals_using_baseline_feed_usage(
        self,
        reduction_in_beef_calves,
        reduction_in_dairy_calves,
        increase_in_slaughter,
        reduction_in_pig_breeding,
        reduction_in_poultry_breeding,
        months,
        discount_rate,
        mother_slaughter,
        use_grass_and_residues_for_dairy,
        baseline_kcals_per_month_feed,
    ):
        """
        the way this function works, is it first calculates the expected feed tons in
         baseline conditions, and compares it to known feed calories in baseline, and
        uses this information to determine the caloric density of feed

        then it calculates the feed usage for the actual scenario.
        """

        tons_to_kcals_first_try = (
            (3560 + 3350) / 2 * 1000
        )  # convert tons to kcals (ASSUME CALORIC DENSITY IS HALF MAIZE, HALF SOYBEAN)

        # assert 0.5 < adjustment_factor < 1.5

        feed_over_time_final = self.calculate_feed_and_animals(
            reduction_in_beef_calves=reduction_in_beef_calves,
            reduction_in_dairy_calves=reduction_in_dairy_calves,
            reduction_in_pig_breeding=reduction_in_pig_breeding,
            reduction_in_poultry_breeding=reduction_in_poultry_breeding,
            increase_in_slaughter=increase_in_slaughter,
            months=months,
            discount_rate=discount_rate,
            mother_slaughter=mother_slaughter,
            use_grass_and_residues_for_dairy=use_grass_and_residues_for_dairy,
            tons_to_kcals=tons_to_kcals_first_try,
        )
        return feed_over_time_final

    def calculate_feed_and_animals(
        self,
        reduction_in_beef_calves,
        reduction_in_dairy_calves,
        increase_in_slaughter,
        reduction_in_pig_breeding,
        reduction_in_poultry_breeding,
        months,
        discount_rate,
        mother_slaughter,
        use_grass_and_residues_for_dairy,
        tons_to_kcals,
    ):
        """

        Inputs:

        reduction_in_beef_calves: Reduction in Beef Birth Rate
        reduction_in_dairy_calves: Reduction in Dairy Birth Rate

        increase_in_slaughter: So 20% indicates an 80% drop in baseline sluaghter rates
        in slaughterhouses

        reduction_in_pig_breeding: Reduction Pig Breeding
        100(=100% reduction) means that all insemination and breeding stops on day 0 (
        with the corresponding drop in birth rate happening 9 months later for cows, 1
         month for chickens, 4 months pigs (as per gestation variables))
        reduction_in_poultry_breeding: Reduction Poultry Breeding

        months: Months to simulate
        discount_rate: discount_rate: Discount Rate for Labour/Technology Transfer
        between species


        mother_slaughter: Proportion of Slaughter which is mothers
        (In a normal slaughtering regime pregnant animals are not killed.
        mother_slaughter is a percentage of how much of the slaughtering capacity
        will be used on pregnant animals.)

        use_grass_and_residues_for_dairy: Whether to Use Residues for Dairy

        tons_to_kcals: calories per ton of feed

        """

        keep_dairy = 0
        steady_state_births = 1

        kcals_to_billion_kcals = 1e-9
        feed_unit_adjust = (
            0.000453592 * tons_to_kcals * kcals_to_billion_kcals
        )  # convert pounds to tonnes to billions of kcals
        # unpack all the dataframe information for ease of use
        # pigs
        total_pigs = self.animal_inputs.dataframe.loc["TotalPigs", "Qty"]
        piglets_pm = self.animal_inputs.dataframe.loc["PigletsPerMonth", "Qty"]
        pigs_slaughter_pm = self.animal_inputs.dataframe.loc["SlaughterPerMonth", "Qty"]
        pigGestation = self.animal_inputs.dataframe.loc["pigGestation", "Qty"]
        piglets_per_litter = self.animal_inputs.dataframe.loc["PigsPerLitter", "Qty"]

        # poultry
        total_poultry = self.animal_inputs.dataframe.loc["Broiler Population", "Qty"]
        poultry_slaughter_pm = self.animal_inputs.dataframe.loc[
            "poultry_slaughter_pm", "Qty"
        ]  # USDA
        chicks_pm = poultry_slaughter_pm  # assume the same, no data
        poultryGestation = self.animal_inputs.dataframe.loc[
            "Chicken Gestation", "Qty"
        ]  # USDA  # actaully 21 days, let's round to 1 month

        # cows (more complex, as need to split dairy and beef)
        total_calves = self.animal_inputs.dataframe.loc[
            "Calves under 500 pounds", "Qty"
        ]
        dairy_cows = self.animal_inputs.dataframe.loc["Milk cows", "Qty"]
        beef_cows = self.animal_inputs.dataframe.loc["Beef cows", "Qty"]
        beef_steers = self.animal_inputs.dataframe.loc[
            "Steers 500 pounds and over", "Qty"
        ]
        heifers = self.animal_inputs.dataframe.loc["Heifers 500 pounds and over", "Qty"]
        new_calves_per_year = self.animal_inputs.dataframe.loc["Calf crop", "Qty"]
        cow_slaughter_pm = self.animal_inputs.dataframe.loc["CowSlaughter", "Qty"]
        cowGestation = self.animal_inputs.dataframe.loc["cowGestation", "Qty"]
        calves_per_mother = 1

        # ### Calcultaion for cows ratios
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
        dairy_track_milk_ready_percent = (
            dairy_cows / cattle_in_dairy_track
        )  # percent of total dairy cows that are producing milk ( probably)

        # other baseline variables
        dairy_life_expectancy = 5

        # # End cows, and basic animal variable definitions ##

        # interventions, scale appropriately for maths (i.e convert sliders from % to
        # decimal)
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

        # ### Slaughtering ####
        # ## Slaughtering variables (currently hardcoded !!)
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

        # # Slaughtering Updates, increases from slider
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

        # # define current totals
        # current_beef_feed_cattle = cattle_on_feed
        current_beef_cattle = cattle_in_beef_track
        current_dairy_cattle = cattle_in_dairy_track
        current_total_pigs = total_pigs
        current_total_poultry = total_poultry

        # ## FEED #commented out code is bottom up from roam page
        # beef_cow_feed_pm_per_cow = 880 # lbs
        # dairy_cow_feed_pm_per_cow = 1048
        # poultry_feed_pm_per_bird = 20
        # pig_feed_pm_per_pig = 139

        # these feed numbers are top down, calculations in google sheet, working
        # backwards from total feed used and dividing it evenly amongst the animal
        # populations
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

        if steady_state_births == 1:
            other_beef_death_ss = other_cow_death_rate * current_beef_cattle
            other_dairy_death_ss = other_cow_death_rate * current_dairy_cattle
            other_pig_death_ss = current_total_pigs * other_pig_death_rate
            other_poultry_death_ss = current_total_poultry * other_poultry_death_rate

            current_dairy_slaughter = current_dairy_cattle / (
                dairy_life_expectancy * 12
            )
            current_beef_slaughter = current_cow_slaughter - current_dairy_slaughter

            new_beef_calfs_pm = current_beef_slaughter + other_beef_death_ss
            new_dairy_calfs_pm = current_dairy_slaughter + other_dairy_death_ss
            new_pigs_pm = current_pig_slaughter + other_pig_death_ss
            new_poultry_pm = current_poultry_slaughter + other_poultry_death_ss

        d = []  # create empty list to place variables in to in loop

        # simulate x months
        for i in range(months):
            if steady_state_births == 0:
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

            # if new_pigs_pm < 0:
            #     new_pigs_pm = 0

            # if new_beef_calfs_pm < 0:
            #     new_beef_calfs_pm = 0

            # ### This is where the issue was!
            # added the new_poultry_pm and new_pigs_pm to the current totals. These
            # were left out and meant that the populations would grow but the slaughter
            if current_total_poultry < current_poultry_slaughter:
                spare_slaughter_hours = (
                    current_poultry_slaughter - current_total_poultry - new_poultry_pm
                ) * poultry_slaughter_hours
                current_poultry_slaughter = current_total_poultry + new_poultry_pm
                current_pig_slaughter += (
                    spare_slaughter_hours
                    * skill_transfer_discount_chickens_to_pigs
                    / pig_slaughter_hours
                )
            if current_total_pigs < current_pig_slaughter:
                spare_slaughter_hours = (
                    current_pig_slaughter - current_total_pigs - new_pigs_pm
                ) * pig_slaughter_hours
                current_pig_slaughter = current_total_pigs + new_pigs_pm
                current_cow_slaughter += (
                    spare_slaughter_hours
                    * skill_transfer_discount_pigs_to_cows
                    / cow_slaughter_hours
                )

            # this set up only kills dairy cows when they are getting to the end of
            # their life.
            current_dairy_slaughter = current_dairy_cattle / (
                dairy_life_expectancy * 12
            )
            current_beef_slaughter = current_cow_slaughter - current_dairy_slaughter
            if current_beef_cattle < current_beef_slaughter:
                # line below required due to the difference between actual slaughter
                # and 'slaughter capacity' consider a rewrite of the whole method to
                # distinuguish between these two. For now, this is thr workaround.
                actual_beef_slaughter = current_beef_cattle

                if keep_dairy == 0:
                    current_dairy_slaughter = (
                        current_cow_slaughter - actual_beef_slaughter
                    )

            else:
                actual_beef_slaughter = current_beef_slaughter

            other_beef_death = other_cow_death_rate * current_beef_cattle
            other_dairy_death = other_cow_death_rate * current_dairy_cattle
            other_pig_death = current_total_pigs * other_pig_death_rate
            other_poultry_death = current_total_poultry * other_poultry_death_rate

            # # Feed
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

            # print(current_poultry_feed * feed_unit_adjust)
            # print(current_feed_combined * feed_unit_adjust)
            # print("month")
            # print(i)
            # print("new_dairy_calfs_pm")
            # print(new_dairy_calfs_pm)
            # print("other_dairy_death")
            # print(other_dairy_death)

            # ## Generate list (before new totals have been calculated)
            # magnitude adjust moves the numbers from per thousnad head to per head (or
            # other)
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
                    "Dairy Cow Pop": dairy_cows,
                    "Dairy Milk Ready Pop": current_dairy_cattle
                    * dairy_track_milk_ready_percent,
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

            # values might be very slightly negative due to overshoot, so set to zero
            # if current_beef_cattle < 0:
            #     current_beef_cattle = 0
            # if current_dairy_cattle < 0:
            #     current_dairy_cattle = 0
            # if current_total_poultry < 0:
            #     current_total_poultry = 0
            # if current_total_pigs < 0:
            #     current_total_pigs = 0

        # ## End of loop, start summary

        df_final = pd.DataFrame(d)
        # print("Combined Feed")
        # import matplotlib.pyplot as plt
        # plt.figure()
        # df_final["Combined Feed"].plot()
        # plt.show()
        return df_final


class ModelAnimalInputs:
    def __init__(self, dataframe):
        self.dataframe = dataframe


"""
Start main function
"""
# Import CSV to dataframes
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../../data").resolve()
df_animals = pd.read_csv(
    DATA_PATH.joinpath("InputDataAndSources.csv"), index_col="Variable"
)
