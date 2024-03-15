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
        super().__init__()

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

        # tonnes dry carb equivalent
        self.ANNUAL_YIELD = self.BASELINE_CROP_KCALS * (1 - self.SEED_PERCENT / 100)

        # 1000 tons fat per billion kcals
        self.OG_FRACTION_FAT = (self.BASELINE_CROP_FAT / 1e3) / (
            self.ANNUAL_YIELD * 4e6 / 1e9
        )

        # 1000 tons protein per billion kcals
        self.OG_FRACTION_PROTEIN = (self.BASELINE_CROP_PROTEIN / 1e3) / (
            self.ANNUAL_YIELD * 4e6 / 1e9
        )
        # if production is zero, then protein fraction is zero
        if self.ANNUAL_YIELD == 0:
            self.OG_FRACTION_PROTEIN = 0
            self.OG_FRACTION_FAT = 0

        self.CROP_WASTE_DISTRIBUTION = constants_for_params["WASTE_DISTRIBUTION"][
            "CROPS"
        ]
        self.CROP_WASTE_RETAIL = constants_for_params["WASTE_RETAIL"]

    def calculate_rotation_ratios(self, constants_for_params):
        # need to use the multiplier on units of kcals to get fat and protein
        if constants_for_params["OG_USE_BETTER_ROTATION"]:
            # deals with the issue of caloric improvement being more than
            # present-day production during the beginning months
            # of the simulation.
            self.OG_KCAL_EXPONENT = constants_for_params["ROTATION_IMPROVEMENTS"][
                "POWER_LAW_IMPROVEMENT"
            ]

            self.OG_ROTATION_FRACTION_KCALS = 1

            self.KCAL_RATIO_ROTATION = 1
            self.FAT_ROTATION_RATIO = constants_for_params["ROTATION_IMPROVEMENTS"][
                "FAT_RATIO"
            ]
            self.PROTEIN_ROTATION_RATIO = constants_for_params["ROTATION_IMPROVEMENTS"][
                "PROTEIN_RATIO"
            ]

            self.OG_ROTATION_FRACTION_FAT = (
                self.OG_FRACTION_FAT * self.FAT_ROTATION_RATIO
            )
            self.OG_ROTATION_FRACTION_PROTEIN = (
                self.OG_FRACTION_PROTEIN * self.PROTEIN_ROTATION_RATIO
            )

            self.FAT_RATIO_ROTATION = self.OG_ROTATION_FRACTION_FAT
            self.PROTEIN_RATIO_ROTATION = self.OG_ROTATION_FRACTION_PROTEIN
        else:
            self.OG_KCAL_EXPONENT = 1
            self.OG_ROTATION_FRACTION_KCALS = 1
            self.OG_ROTATION_FRACTION_FAT = self.OG_FRACTION_FAT
            self.OG_ROTATION_FRACTION_PROTEIN = self.OG_FRACTION_PROTEIN

            self.KCAL_RATIO_ROTATION = 1
            self.FAT_RATIO_ROTATION = self.OG_FRACTION_FAT
            self.PROTEIN_RATIO_ROTATION = self.OG_FRACTION_PROTEIN

    def get_year_1_ratio_using_fraction_harvest_before_may(
        self, first_year_xia_et_al_reduction, seasonality_values, country_iso3
    ):
        """
        This function subtracts off the estimated harvest for the first year for countries where
        """
        if country_iso3 == "ZAF":
            harvest_before_may_this_country = 1
        elif country_iso3 == "JPN":
            harvest_before_may_this_country = 0
        elif country_iso3 == "PRK":
            harvest_before_may_this_country = 0
        elif country_iso3 == "KOR":
            harvest_before_may_this_country = 0
        else:
            harvest_before_may_this_country = sum(seasonality_values[:4])

        fraction_harvest_after_may_nuclear_winter = (
            first_year_xia_et_al_reduction - harvest_before_may_this_country
        )
        if first_year_xia_et_al_reduction < 0:
            first_year_xia_et_al_reduction = 0
        assert (
            first_year_xia_et_al_reduction < 101
        )  # the improvement can't be that much...

        if fraction_harvest_after_may_nuclear_winter < 0:
            fraction_harvest_after_may_nuclear_winter = 0

        if fraction_harvest_after_may_nuclear_winter > 0:
            # if the expected yield for the remaining months is nonzero

            fraction_harvest_after_may = 1 - harvest_before_may_this_country

            assert fraction_harvest_after_may >= 0
            assert fraction_harvest_after_may <= 1

            if fraction_harvest_after_may < 0.25:
                # in this case, we simply don't have much data about the yield in nuclear winter from xia et al
                # year 1 data, and it doesn't make more than a 25% difference in the total yield over a 12 month
                # period, so the yield in these months is assumed to be the same.
                fraction_continued_yields = 1

            else:
                # We have significant harvest during the months May, June, July, August, September, October,
                # November, and December. The ratio of yield to expected in nuclear winter during those months
                # is calculated as the fraction_harvest_after_may_nuclear_winter divided by the
                # fraction_harvest_after_may.

                ratio_yields_nw = fraction_harvest_after_may_nuclear_winter

                fraction_continued_yields = ratio_yields_nw / fraction_harvest_after_may

        else:
            # The fraction of the normal harvest is zero after subtracting yield from normal months.
            # Therefore, the total harvest will be zero.
            fraction_continued_yields = 0

        return fraction_continued_yields

    def calculate_monthly_production(self, constants_for_params):
        # assumption: outdoor crop production is very similar in nutritional
        # profile to stored food
        # reference: row 11, 'outputs' tab
        # https://docs.google.com/spreadsheets/d/19kzHpux690JTCo2IX2UA1faAd7R1QcBK/edit#gid=1815939673
        month_index = self.STARTING_MONTH_NUM - 1
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
        # seasonality does not have a net effect on average production over a year
        assert (SUM < 1.001 and SUM > 0.999) or SUM == 0

        # tons dry carb equivalent
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

        # billions of kcals
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

        MAY_UNTIL_DECEMBER_FIRST_YEAR_REDUCTION = (
            self.get_year_1_ratio_using_fraction_harvest_before_may(
                RATIO_KCALS_POSTDISASTER_1Y,
                constants_for_params["SEASONALITY"],
                constants_for_params["COUNTRY_CODE"],
            )
        )

        # We then  end up at the month reduction appropriate for
        # the month before the next 12 month cycle. That means there are 13 total
        # values and we only keep the first 12 (the 13th index would have been the
        # reduction value we were interpolating towards, but instead we add that in
        # the next array of 12 months)
        y1_to_y2 = np.linspace(
            MAY_UNTIL_DECEMBER_FIRST_YEAR_REDUCTION,
            MAY_UNTIL_DECEMBER_FIRST_YEAR_REDUCTION,
            8,
        )
        y2_to_y3 = np.linspace(
            RATIO_KCALS_POSTDISASTER_2Y, RATIO_KCALS_POSTDISASTER_2Y, 13
        )[:-1]
        y3_to_y4 = np.linspace(
            RATIO_KCALS_POSTDISASTER_3Y, RATIO_KCALS_POSTDISASTER_3Y, 13
        )[:-1]
        y4_to_y5 = np.linspace(
            RATIO_KCALS_POSTDISASTER_4Y, RATIO_KCALS_POSTDISASTER_4Y, 13
        )[:-1]
        y5_to_y6 = np.linspace(
            RATIO_KCALS_POSTDISASTER_5Y, RATIO_KCALS_POSTDISASTER_5Y, 13
        )[:-1]
        y6_to_y7 = np.linspace(
            RATIO_KCALS_POSTDISASTER_6Y, RATIO_KCALS_POSTDISASTER_6Y, 13
        )[:-1]
        y7_to_y8 = np.linspace(
            RATIO_KCALS_POSTDISASTER_7Y, RATIO_KCALS_POSTDISASTER_7Y, 13
        )[:-1]
        y8_to_y9 = np.linspace(
            RATIO_KCALS_POSTDISASTER_8Y, RATIO_KCALS_POSTDISASTER_8Y, 13
        )[:-1]
        y9_to_y10 = np.linspace(
            RATIO_KCALS_POSTDISASTER_9Y, RATIO_KCALS_POSTDISASTER_9Y, 13
        )[:-1]
        y10_to_y11 = np.linspace(
            RATIO_KCALS_POSTDISASTER_10Y, RATIO_KCALS_POSTDISASTER_10Y, 13 + 4
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
        # assert len(self.all_months_reductions) == self.NMONTHS
        PLOT_NO_SEASONALITY_FLAG = False
        if PLOT_NO_SEASONALITY_FLAG:
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

        PLOT_WITH_SEASONALITY_FLAG = False
        if PLOT_WITH_SEASONALITY_FLAG:
            print("Plotting with seasonality")
            # ratios between baseline production and actual production
            ratios = np.divide(
                self.NO_ROT_KCALS_GROWN, self.ANNUAL_YIELD * 4e6 / 1e9 / 12
            )
            Plotter.plot_monthly_reductions_seasonally(ratios)

    def assign_increase_from_increased_cultivated_area(self, constants_for_params):
        # Constants

        N = constants_for_params["INITIAL_HARVEST_DURATION_IN_MONTHS"]
        max_value = constants_for_params["RATIO_INCREASED_CROP_AREA"]
        total_months = (
            constants_for_params["NUMBER_YEARS_TAKES_TO_REACH_INCREASED_AREA"] * 12
        )

        # Create the linspace
        linspace = np.ones(self.NMONTHS)

        # Calculate the increment per month after the delay
        increment = (max_value - 1) / (total_months - N)

        # Update the linspace values
        for i in range(N, total_months):
            linspace[i] = 1 + (i - N) * increment

        # Maintain the value after the specified number of years
        linspace[total_months:] = max_value

        # increase the kcals grown using the increased ratio due to increased area
        for i in range(self.NMONTHS):
            self.KCALS_GROWN[i] = self.KCALS_GROWN[i] * linspace[i]

    def assign_reduction_from_climate_impact(self, constants_for_params):
        self.KCALS_GROWN = []
        self.NO_ROT_KCALS_GROWN = []

        for i in range(self.NMONTHS):
            cycle_index = i % 12
            month_kcals = self.months_cycle[cycle_index]
            baseline_reduction = self.all_months_reductions[i]

            # if there's some very small negative value here, just round it off to zero
            if baseline_reduction <= 0:
                baseline_reduction = round(baseline_reduction, 8)

            assert baseline_reduction >= 0  # 8 decimal places rounding

            if baseline_reduction > 1:
                self.KCALS_GROWN.append(month_kcals * baseline_reduction)
            else:
                self.KCALS_GROWN.append(
                    month_kcals * baseline_reduction**self.OG_KCAL_EXPONENT
                )

            self.NO_ROT_KCALS_GROWN.append(month_kcals * baseline_reduction)

            assert (
                self.KCALS_GROWN[-1] >= month_kcals * baseline_reduction
            ), "ERROR: Relocation has somehow decreased crop production!"

    def set_crop_production_minus_greenhouse_area(
        self, constants_for_params, greenhouse_fraction_area
    ):
        if self.ADD_OUTDOOR_GROWING:
            if constants_for_params["OG_USE_BETTER_ROTATION"]:
                crops_produced = np.array([0] * self.NMONTHS)

                hd = (
                    constants_for_params["INITIAL_HARVEST_DURATION_IN_MONTHS"]
                    + constants_for_params["DELAY"]["ROTATION_CHANGE_IN_MONTHS"]
                )

                crops_produced[hd:] = np.multiply(
                    np.array(self.KCALS_GROWN[hd:]), (1 - greenhouse_fraction_area[hd:])
                )

                crops_produced[:hd] = np.multiply(
                    np.array(self.NO_ROT_KCALS_GROWN[:hd]),
                    (1 - greenhouse_fraction_area[:hd]),
                )

            else:
                crops_produced = np.array(self.NO_ROT_KCALS_GROWN)

        else:
            crops_produced = np.array([0] * self.NMONTHS)

        self.production = Food(
            kcals=np.array(crops_produced) * (1 - self.CROP_WASTE_DISTRIBUTION / 100),
            fat=np.array(self.OG_FRACTION_FAT * crops_produced)
            * (1 - self.CROP_WASTE_DISTRIBUTION / 100),
            protein=np.array(self.OG_FRACTION_PROTEIN * crops_produced)
            * (1 - self.CROP_WASTE_DISTRIBUTION / 100),
            kcals_units="billion kcals each month",
            fat_units="thousand tons each month",
            protein_units="thousand tons each month",
        )

        assert not np.isnan(
            self.production.kcals
        ).any(), """Error: the outdoor crop production expected is
            unknown, cannot compute optimization"""
