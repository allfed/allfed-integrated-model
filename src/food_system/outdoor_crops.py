"""
################################# Outdoor Crops ###############################
##                                                                            #
##       Functions and constants relating to outdoor crop production          #
##                                                                            #
###############################################################################
"""

import numpy as np
from src.utilities.plotter import Plotter
from src.food_system.food import Food


class OutdoorCrops:
    def __init__(self, constants_for_params):
        """
        Initializes the OutdoorCrops class with the given constants for parameters.

        Args:
            constants_for_params (dict): A dictionary containing the following keys:
                - NMONTHS: The number of months in a year.
                - STARTING_MONTH_NUM: The starting month number.
                - BASELINE_CROP_KCALS: The baseline crop calories.
                - BASELINE_CROP_FAT: The baseline crop fat.
                - BASELINE_CROP_PROTEIN: The baseline crop protein.
                - ADD_OUTDOOR_GROWING: A boolean indicating whether outdoor growing is added.

        Returns:
            None
        """

        super().__init__()

        # Set the constants for parameters
        self.NMONTHS = constants_for_params["NMONTHS"]
        self.STARTING_MONTH_NUM = constants_for_params["STARTING_MONTH_NUM"]
        self.BASELINE_CROP_KCALS = constants_for_params["BASELINE_CROP_KCALS"]
        self.BASELINE_CROP_FAT = constants_for_params["BASELINE_CROP_FAT"]
        self.BASELINE_CROP_PROTEIN = constants_for_params["BASELINE_CROP_PROTEIN"]

        self.ADD_OUTDOOR_GROWING = constants_for_params["ADD_OUTDOOR_GROWING"]

        # FAO ALL SUPPLY UTILIZATION SHEET
        # units are millions tons (dry caloric, fat, protein)
        #         year    Kcals    Fat    Protein
        #         2014    3550    225    468
        #         2015    3583    228    478
        #         2016    3682    234    493
        #         2017    3774    246    511
        #         2018    3725    245    498
        #         2019    7087    449    937

        # TREND    2020    3879.2    257    525
        # percent OG redirected to non-eaten seeds
        self.SEED_PERCENT = 100 * (92 / 3898)

        # Calculate the annual yield in tonnes dry carb equivalent
        self.ANNUAL_YIELD = self.BASELINE_CROP_KCALS * (1 - self.SEED_PERCENT / 100)

        # Calculate the fraction of fat in outdoor crops in 1000 tons per billion kcals
        self.OG_FRACTION_FAT = (self.BASELINE_CROP_FAT / 1e3) / (
            self.ANNUAL_YIELD * 4e6 / 1e9
        )

        # Calculate the fraction of protein in outdoor crops in 1000 tons per billion kcals
        self.OG_FRACTION_PROTEIN = (self.BASELINE_CROP_PROTEIN / 1e3) / (
            self.ANNUAL_YIELD * 4e6 / 1e9
        )

        # If production is zero, then protein fraction is zero
        if self.ANNUAL_YIELD == 0:
            self.OG_FRACTION_PROTEIN = 0
            self.OG_FRACTION_FAT = 0

    def calculate_rotation_ratios(self, constants_for_params):
        """
        Calculates the rotation ratios for fat and protein based on the constants provided.
        If OG_USE_BETTER_ROTATION is True, the function uses the ROTATION_IMPROVEMENTS
        constants to calculate the ratios. Otherwise, the original ratios are used.
        Args:
            constants_for_params (dict): A dictionary containing the constants needed for
            the calculation.
        """
        # need to use the multiplier on units of kcals to get fat and protein
        if constants_for_params["OG_USE_BETTER_ROTATION"]:
            # deals with the issue of caloric improvement being more than
            # present-day production during the beginning months
            # of the simulation.
            self.OG_KCAL_EXPONENT = constants_for_params["ROTATION_IMPROVEMENTS"][
                "POWER_LAW_IMPROVEMENT"
            ]

            # Calculate the fat and protein ratios based on the ROTATION_IMPROVEMENTS constants
            self.FAT_ROTATION_RATIO = constants_for_params["ROTATION_IMPROVEMENTS"][
                "FAT_RATIO"
            ]
            self.PROTEIN_ROTATION_RATIO = constants_for_params["ROTATION_IMPROVEMENTS"][
                "PROTEIN_RATIO"
            ]

            # Calculate the rotation fractions for fat and protein
            self.OG_ROTATION_FRACTION_FAT = (
                self.OG_FRACTION_FAT * self.FAT_ROTATION_RATIO
            )
            self.OG_ROTATION_FRACTION_PROTEIN = (
                self.OG_FRACTION_PROTEIN * self.PROTEIN_ROTATION_RATIO
            )

            # Set the fat and protein ratios for rotation
            self.FAT_RATIO_ROTATION = self.OG_ROTATION_FRACTION_FAT
            self.PROTEIN_RATIO_ROTATION = self.OG_ROTATION_FRACTION_PROTEIN
        else:
            # If OG_USE_BETTER_ROTATION is False, use the original ratios
            self.OG_KCAL_EXPONENT = 1
            self.OG_ROTATION_FRACTION_FAT = self.OG_FRACTION_FAT
            self.OG_ROTATION_FRACTION_PROTEIN = self.OG_FRACTION_PROTEIN

            # Set the fat and protein ratios for rotation
            self.FAT_RATIO_ROTATION = self.OG_FRACTION_FAT
            self.PROTEIN_RATIO_ROTATION = self.OG_FRACTION_PROTEIN
        """
        Note: The function does not return anything, but instead modifies the object's
        attributes directly.
        """

    def calculate_monthly_production(self, constants_for_params):
        """
        Calculates the monthly production of outdoor crops based on various parameters.

        Args:
            self: instance of the class
            constants_for_params (dict): dictionary containing various constants used in the calculation

        Returns:
            None

        Raises:
            AssertionError: if the sum of seasonality values is not within a certain range

        """
        # assumption: outdoor crop production is very similar in nutritional
        # profile to stored food
        # reference: row 11, 'outputs' tab
        # https://docs.google.com/spreadsheets/d/19kzHpux690JTCo2IX2UA1faAd7R1QcBK/edit#gid=1815939673

        # get the starting month index
        month_index = self.STARTING_MONTH_NUM - 1

        # get the seasonality values for each month
        JAN_FRACTION = constants_for_params["SEASONALITY"][0]
        FEB_FRACTION = constants_for_params["SEASONALITY"][1]
        MAR_FRACTION = constants_for_params["SEASONALITY"][2]
        APR_FRACTION = constants_for_params["SEASONALITY"][3]
        MAY_FRACTION = constants_for_params["SEASONALITY"][4]
        JUN_FRACTION = constants_for_params["SEASONALITY"][5]
        JUL_FRACTION = constants_for_params["SEASONALITY"][6]
        AUG_FRACTION = constants_for_params["SEASONALITY"][7]
        SEP_FRACTION = constants_for_params["SEASONALITY"][8]
        OCT_FRACTION = constants_for_params["SEASONALITY"][9]
        NOV_FRACTION = constants_for_params["SEASONALITY"][10]
        DEC_FRACTION = constants_for_params["SEASONALITY"][11]

        # calculate the sum of all seasonality values
        SUM = np.sum(
            np.array(
                [
                    JAN_FRACTION,
                    FEB_FRACTION,
                    MAR_FRACTION,
                    APR_FRACTION,
                    MAY_FRACTION,
                    JUN_FRACTION,
                    JUL_FRACTION,
                    AUG_FRACTION,
                    SEP_FRACTION,
                    OCT_FRACTION,
                    NOV_FRACTION,
                    DEC_FRACTION,
                ]
            )
        )

        # check if the sum of seasonality values is within a certain range
        assert (SUM < 1.001 and SUM > 0.999) or SUM == 0

        # calculate the yield for each month
        JAN_YIELD = JAN_FRACTION * self.ANNUAL_YIELD
        FEB_YIELD = FEB_FRACTION * self.ANNUAL_YIELD
        MAR_YIELD = MAR_FRACTION * self.ANNUAL_YIELD
        APR_YIELD = APR_FRACTION * self.ANNUAL_YIELD
        MAY_YIELD = MAY_FRACTION * self.ANNUAL_YIELD
        JUN_YIELD = JUN_FRACTION * self.ANNUAL_YIELD
        JUL_YIELD = JUL_FRACTION * self.ANNUAL_YIELD
        AUG_YIELD = AUG_FRACTION * self.ANNUAL_YIELD
        SEP_YIELD = SEP_FRACTION * self.ANNUAL_YIELD
        OCT_YIELD = OCT_FRACTION * self.ANNUAL_YIELD
        NOV_YIELD = NOV_FRACTION * self.ANNUAL_YIELD
        DEC_YIELD = DEC_FRACTION * self.ANNUAL_YIELD

        # calculate the kcals for each month
        JAN_KCALS_OG = JAN_YIELD * 4e6 / 1e9
        FEB_KCALS_OG = FEB_YIELD * 4e6 / 1e9
        MAR_KCALS_OG = MAR_YIELD * 4e6 / 1e9
        APR_KCALS_OG = APR_YIELD * 4e6 / 1e9
        MAY_KCALS_OG = MAY_YIELD * 4e6 / 1e9
        JUN_KCALS_OG = JUN_YIELD * 4e6 / 1e9
        JUL_KCALS_OG = JUL_YIELD * 4e6 / 1e9
        AUG_KCALS_OG = AUG_YIELD * 4e6 / 1e9
        SEP_KCALS_OG = SEP_YIELD * 4e6 / 1e9
        OCT_KCALS_OG = OCT_YIELD * 4e6 / 1e9
        NOV_KCALS_OG = NOV_YIELD * 4e6 / 1e9
        DEC_KCALS_OG = DEC_YIELD * 4e6 / 1e9

        # get the ratios for kcals post-disaster for each year
        RATIO_KCALS_POSTDISASTER_1Y = constants_for_params["RATIO_CROPS_YEAR1"]
        RATIO_KCALS_POSTDISASTER_2Y = constants_for_params["RATIO_CROPS_YEAR2"]
        RATIO_KCALS_POSTDISASTER_3Y = constants_for_params["RATIO_CROPS_YEAR3"]
        RATIO_KCALS_POSTDISASTER_4Y = constants_for_params["RATIO_CROPS_YEAR4"]
        RATIO_KCALS_POSTDISASTER_5Y = constants_for_params["RATIO_CROPS_YEAR5"]
        RATIO_KCALS_POSTDISASTER_6Y = constants_for_params["RATIO_CROPS_YEAR6"]
        RATIO_KCALS_POSTDISASTER_7Y = constants_for_params["RATIO_CROPS_YEAR7"]
        RATIO_KCALS_POSTDISASTER_8Y = constants_for_params["RATIO_CROPS_YEAR8"]
        RATIO_KCALS_POSTDISASTER_9Y = constants_for_params["RATIO_CROPS_YEAR9"]
        RATIO_KCALS_POSTDISASTER_10Y = constants_for_params["RATIO_CROPS_YEAR10"]

        # create the reduction lists for each year

        # we want to start at 1, then end up at the month reduction appropriate for
        # the month before the next 12 month cycle. That means there are 13 total
        # values and we only keep the first 12 (the 13th index would have been the
        # reduction value we were interpolating towards, but instead we add that in
        # the next array of 12 months)
        y1_to_y2 = np.linspace(1, RATIO_KCALS_POSTDISASTER_1Y, 13)[:-1]
        y2_to_y3 = np.linspace(
            RATIO_KCALS_POSTDISASTER_1Y, RATIO_KCALS_POSTDISASTER_2Y, 13
        )[:-1]
        y3_to_y4 = np.linspace(
            RATIO_KCALS_POSTDISASTER_2Y, RATIO_KCALS_POSTDISASTER_3Y, 13
        )[:-1]
        y4_to_y5 = np.linspace(
            RATIO_KCALS_POSTDISASTER_3Y, RATIO_KCALS_POSTDISASTER_4Y, 13
        )[:-1]
        y5_to_y6 = np.linspace(
            RATIO_KCALS_POSTDISASTER_4Y, RATIO_KCALS_POSTDISASTER_5Y, 13
        )[:-1]
        y6_to_y7 = np.linspace(
            RATIO_KCALS_POSTDISASTER_5Y, RATIO_KCALS_POSTDISASTER_6Y, 13
        )[:-1]
        y7_to_y8 = np.linspace(
            RATIO_KCALS_POSTDISASTER_6Y, RATIO_KCALS_POSTDISASTER_7Y, 13
        )[:-1]
        y8_to_y9 = np.linspace(
            RATIO_KCALS_POSTDISASTER_7Y, RATIO_KCALS_POSTDISASTER_8Y, 13
        )[:-1]
        y9_to_y10 = np.linspace(
            RATIO_KCALS_POSTDISASTER_8Y, RATIO_KCALS_POSTDISASTER_9Y, 13
        )[:-1]
        y10_to_y11 = np.linspace(
            RATIO_KCALS_POSTDISASTER_9Y, RATIO_KCALS_POSTDISASTER_10Y, 13
        )[:-1]

        # this just appends all the reduction lists together
        # this starts on the month of interest (not necessarily january; probably may)
        self.all_months_reductions = np.array(
            list(y1_to_y2)
            + list(y2_to_y3)
            + list(y3_to_y4)
            + list(y4_to_y5)
            + list(y5_to_y6)
            + list(y6_to_y7)
            + list(y7_to_y8)
            + list(y8_to_y9)
            + list(y9_to_y10)
            + list(y10_to_y11)
        )

        # 7 years of reductions should be 12*7 months.
        assert len(self.all_months_reductions) == self.NMONTHS

        PLOT_NO_SEASONALITY = False
        if PLOT_NO_SEASONALITY:
            print("Plotting with no seasonality")
            Plotter.plot_monthly_reductions_no_seasonality(self.all_months_reductions)

        month_cycle_starting_january = [
            JAN_KCALS_OG,
            FEB_KCALS_OG,
            MAR_KCALS_OG,
            APR_KCALS_OG,
            MAY_KCALS_OG,
            JUN_KCALS_OG,
            JUL_KCALS_OG,
            AUG_KCALS_OG,
            SEP_KCALS_OG,
            OCT_KCALS_OG,
            NOV_KCALS_OG,
            DEC_KCALS_OG,
        ]

        # adjust cycle so it starts at the first month of the simulation
        self.months_cycle = (
            month_cycle_starting_january[month_index:]
            + month_cycle_starting_january[0:month_index]
        )

        self.assign_reduction_from_climate_impact(constants_for_params)

        if constants_for_params["RATIO_INCREASED_CROP_AREA"] > 1:
            self.assign_increase_from_increased_cultivated_area(constants_for_params)

        PLOT_WITH_SEASONALITY = False
        if PLOT_WITH_SEASONALITY:
            print("Plotting with seasonality")
            # ratios between baseline production and actual production
            ratios = np.divide(
                self.NO_ROT_KCALS_GROWN, self.ANNUAL_YIELD * 4e6 / 1e9 / 12
            )
            print("ratios")
            print(ratios)
            # Plotter.plot_monthly_reductions_seasonally(ratios)
            Plotter.plot_monthly_reductions_seasonally(ratios)

    def assign_increase_from_increased_cultivated_area(self, constants_for_params):
        """
        This function calculates the increase in crop yield due to an increase in cultivated area.
        It updates the KCALS_GROWN array with the new values.

        Args:
            self (object): The instance of the class
            constants_for_params (dict): A dictionary containing the constants used in the calculation

        Returns:
            None
        """

        # Constants
        N = constants_for_params[
            "INITIAL_HARVEST_DURATION_IN_MONTHS"
        ]  # Initial harvest duration in months
        max_value = constants_for_params[
            "RATIO_INCREASED_CROP_AREA"
        ]  # Maximum value of the ratio
        total_months = (
            constants_for_params["NUMBER_YEARS_TAKES_TO_REACH_INCREASED_AREA"] * 12
        )  # Total months to reach the maximum value

        # Create the linspace
        linspace = np.ones(self.NMONTHS)

        # Calculate the increment per month after the delay
        increment = (max_value - 1) / (total_months - N)

        # Update the linspace values
        for i in range(N, total_months):
            linspace[i] = 1 + (i - N) * increment

        # Maintain the value after the specified number of years
        linspace[total_months:] = max_value

        # Increase the kcals grown using the increased ratio due to increased area
        for i in range(self.NMONTHS):
            self.KCALS_GROWN[i] = self.KCALS_GROWN[i] * linspace[i]

    def assign_reduction_from_climate_impact(self, constants_for_params):
        """
        Assigns the reduction in crop production due to climate impact for each month of the year.
        Args:
            self: instance of the class
            constants_for_params: dictionary containing constants used in the function
        """
        # Initialize the lists to store the kcals grown with and without crop rotation
        self.KCALS_GROWN = []
        self.NO_ROT_KCALS_GROWN = []

        # Loop through each month of the year
        for i in range(self.NMONTHS):
            cycle_index = i % 12
            month_kcals = self.months_cycle[cycle_index]
            baseline_reduction = self.all_months_reductions[i]

            # If the baseline reduction is negative or very small, round it off to zero
            if baseline_reduction <= 0:
                baseline_reduction = round(baseline_reduction, 8)

            # Ensure that the baseline reduction is not negative
            assert baseline_reduction >= 0  # 8 decimal places rounding

            # Calculate the kcals grown with crop rotation
            if baseline_reduction > 1:
                self.KCALS_GROWN.append(month_kcals * baseline_reduction)
            else:
                self.KCALS_GROWN.append(
                    month_kcals * baseline_reduction**self.OG_KCAL_EXPONENT
                )

            # Calculate the kcals grown without crop rotation
            self.NO_ROT_KCALS_GROWN.append(month_kcals * baseline_reduction)

            # Ensure that crop production has not decreased due to relocation
            assert (
                self.KCALS_GROWN[-1] >= month_kcals * baseline_reduction
            ), "ERROR: Relocation has somehow decreased crop production!"

    def set_crop_production_minus_greenhouse_area(
        self, constants_for_params, greenhouse_fraction_area
    ):
        """
        Calculates the crop production minus greenhouse area and sets the production attribute of the class instance.

        Args:
            self (OutdoorCrops): instance of the class
            constants_for_params (dict): dictionary containing constants for parameters
            greenhouse_fraction_area (numpy.ndarray): array containing the fraction of greenhouse area for each month

        Returns:
            None

        Example:
            >>>
            >>> constants_for_params = {"WASTE": {"CROPS": 10}, "OG_USE_BETTER_ROTATION": True, "INITIAL_HARVEST_DURATION_IN_MONTHS": 3, "DELAY": {"ROTATION_CHANGE_IN_MONTHS": 2}}
            >>> greenhouse_fraction_area = np.array([0.5, 0.6, 0.7, 0.8, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2])
            >>> oc = OutdoorCrops()
            >>> oc.set_crop_production_minus_greenhouse_area(constants_for_params, greenhouse_fraction_area)

        """

        # Set the crop waste constant
        self.CROP_WASTE = constants_for_params["WASTE"]["CROPS"]

        # Check if outdoor growing is enabled
        if self.ADD_OUTDOOR_GROWING:
            # Check if better rotation is enabled
            if constants_for_params["OG_USE_BETTER_ROTATION"]:
                # Initialize an array to store the crops produced
                crops_produced = np.array([0] * self.NMONTHS)

                # Calculate the harvest duration
                hd = (
                    constants_for_params["INITIAL_HARVEST_DURATION_IN_MONTHS"]
                    + constants_for_params["DELAY"]["ROTATION_CHANGE_IN_MONTHS"]
                )

                # Calculate the crops produced for each month
                crops_produced[hd:] = np.multiply(
                    np.array(self.KCALS_GROWN[hd:]), (1 - greenhouse_fraction_area[hd:])
                )

                crops_produced[:hd] = np.multiply(
                    np.array(self.NO_ROT_KCALS_GROWN[:hd]),
                    (1 - greenhouse_fraction_area[:hd]),
                )

            else:
                # Use the default crop production values
                crops_produced = np.array(self.NO_ROT_KCALS_GROWN)

        else:
            # No outdoor growing, so no crops produced
            crops_produced = np.array([0] * self.NMONTHS)

        # Calculate the production of food
        self.production = Food(
            kcals=np.array(crops_produced) * (1 - self.CROP_WASTE / 100),
            fat=np.array(self.OG_FRACTION_FAT * crops_produced)
            * (1 - self.CROP_WASTE / 100),
            protein=np.array(self.OG_FRACTION_PROTEIN * crops_produced)
            * (1 - self.CROP_WASTE / 100),
            kcals_units="billion kcals each month",
            fat_units="thousand tons each month",
            protein_units="thousand tons each month",
        )

        # Check if any NaN values are present in the production
        assert not np.isnan(
            self.production.kcals
        ).any(), """Error: the outdoor crop production expected is
            unknown, cannot compute optimization"""
