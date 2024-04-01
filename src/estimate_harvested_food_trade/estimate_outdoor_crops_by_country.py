"""
performs the estimate of monthly outdoor crop production based on the yearly reduction in nuclear winter and baseline
crop production
This ignores the reduced area due to planting of greenhouses, or increase yield from greenhouses.   
relocation of crops does affect the trade from these countries however
"""
import pprint
import numpy as np
import pandas as pd
from pathlib import Path
from src.utilities.plotter import Plotter
import yaml


def import_consts_yaml():
    # Assuming 'outdoor_crops_constants.yaml' is in the same directory as your Python script
    with open("outdoor_crops_constants.yaml", "r") as file:
        constants = yaml.safe_load(file)

    return constants


def get_new_columns_outdoor_crops(no_trade_table_no_monthly_reductions):
    constants = import_consts_yaml()
    # Set the starting month number to the simulation starting month number

    # new_columns is a list of dictionaries returned from get_new_columns_outdoor_crops,
    # where each dictionary represents a new column to be added.
    new_columns = []
    for index, country_data in no_trade_table_no_monthly_reductions.iterrows():
        outdoor_crop_parameters = calculate_useful_parameters(constants)

        # Calculate the monthly production for the outdoor crops
        (
            months_cycle,
            all_months_reductions,
        ) = calculate_monthly_production(country_data, outdoor_crop_parameters)

        NMONTHS = len(all_months_reductions)

        KCALS_GROWN_NO_RELOCATION = assign_reduction_from_climate_impact(
            months_cycle,
            all_months_reductions,
            outdoor_crop_parameters["ANNUAL_PRODUCTION"],
            NMONTHS,
            # outdoor_crop_parameters["OG_KCAL_EXPONENT"],
        )

        PLOT_WITH_SEASONALITY_FLAG = False
        if PLOT_WITH_SEASONALITY_FLAG:
            print("Plotting with seasonality")
            # ratios between baseline production and actual production
            ratios = np.divide(
                KCALS_GROWN_NO_RELOCATION,
                outdoor_crop_parameters["ANNUAL_PRODUCTION"] * 4e6 / 1e9 / 1,
            )
            Plotter.plot_monthly_reductions_seasonally(ratios)

        for i in range(len(KCALS_GROWN_NO_RELOCATION)):
            outdoor_crop_parameters[
                f"KCALS_GROWN_NO_RELOCATION_m{i}"
            ] = KCALS_GROWN_NO_RELOCATION[i]
            outdoor_crop_parameters[f"baseline_reduction_m{i}"] = all_months_reductions[
                i
            ]
        new_columns.append(outdoor_crop_parameters)
    return new_columns


def calculate_useful_parameters(outdoor_crop_parameters):
    BASELINE_CROP_KCALS = outdoor_crop_parameters["BASELINE_CROP_KCALS"]
    BASELINE_CROP_FAT = outdoor_crop_parameters["BASELINE_CROP_FAT"]
    BASELINE_CROP_PROTEIN = outdoor_crop_parameters["BASELINE_CROP_PROTEIN"]
    STARTING_MONTH_NAME = outdoor_crop_parameters["STARTING_MONTH_NAME"]
    # OG_KCAL_EXPONENT = country_data["OG_KCAL_EXPONENT"]
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
    SEED_PERCENT = 100 * (92 / 3898)

    # tonnes dry carb equivalent
    ANNUAL_PRODUCTION = BASELINE_CROP_KCALS * (1 - SEED_PERCENT / 100)

    # 1000 tons fat per billion kcals
    OG_FRACTION_FAT = (BASELINE_CROP_FAT / 1e3) / (ANNUAL_PRODUCTION * 4e6 / 1e9)

    # 1000 tons protein per billion kcals
    OG_FRACTION_PROTEIN = (BASELINE_CROP_PROTEIN / 1e3) / (
        ANNUAL_PRODUCTION * 4e6 / 1e9
    )
    # if production is zero, then protein fraction is zero
    if ANNUAL_PRODUCTION == 0:
        OG_FRACTION_FAT = 0
        OG_FRACTION_PROTEIN = 0

    # Dictionary of the months to set the starting point of the model to
    months_dict = {
        "JAN": 1,
        "FEB": 2,
        "MAR": 3,
        "APR": 4,
        "MAY": 5,
        "JUN": 6,
        "JUL": 7,
        "AUG": 8,
        "SEP": 9,
        "OCT": 10,
        "NOV": 11,
        "DEC": 12,
    }
    STARTING_MONTH_NUM = months_dict[
        STARTING_MONTH_NAME
    ]  # Starting month number for the simulation

    outdoor_crop_parameters = {}
    outdoor_crop_parameters["STARTING_MONTH_NUM"] = STARTING_MONTH_NUM
    outdoor_crop_parameters["ANNUAL_PRODUCTION"] = ANNUAL_PRODUCTION
    outdoor_crop_parameters["OG_FRACTION_FAT"] = OG_FRACTION_FAT
    outdoor_crop_parameters["OG_FRACTION_PROTEIN"] = OG_FRACTION_PROTEIN
    # outdoor_crop_parameters["OG_KCAL_EXPONENT"] = OG_KCAL_EXPONENT

    return outdoor_crop_parameters


def assign_reduction_from_climate_impact(
    months_cycle,
    all_months_reductions,
    ANNUAL_PRODUCTION,
    NMONTHS,  # , OG_KCAL_EXPONENT
):
    KCALS_GROWN = []
    KCALS_GROWN_NO_RELOCATION = []
    for i in range(NMONTHS):
        cycle_index = i % 12
        month_kcals = months_cycle[cycle_index]
        baseline_reduction = all_months_reductions[i]

        # if there's some very small negative value here, just round it off to zero
        if baseline_reduction <= 0:
            baseline_reduction = round(baseline_reduction, 8)

        assert baseline_reduction >= 0  # 8 decimal places rounding

        # if baseline_reduction > 1:
        # KCALS_GROWN.append(month_kcals * baseline_reduction)
        # else:
        #     KCALS_GROWN.append(month_kcals * baseline_reduction**OG_KCAL_EXPONENT)

        KCALS_GROWN_NO_RELOCATION.append(month_kcals * baseline_reduction)

        # assert (
        # KCALS_GROWN[-1] >= month_kcals * baseline_reduction
        # ), "ERROR: Relocation has somehow decreased crop production!"
    return KCALS_GROWN_NO_RELOCATION  # , KCALS_GROWN


def calculate_monthly_production(country_data, outdoor_crop_parameters):
    # assumption: outdoor crop production is very similar in nutritional
    # profile to stored food
    # reference: row 11, 'outputs' tab
    # https://docs.google.com/spreadsheets/d/19kzHpux690JTCo2IX2UA1faAd7R1QcBK/edit#gid=1815939673
    month_index = outdoor_crop_parameters["STARTING_MONTH_NUM"] - 1
    pd.set_option("display.max_rows", None)
    print("country_data")
    print(country_data)
    print(country_data.index)
    JAN_FRACTION = country_data[f"seasonality_m1"]
    FEB_FRACTION = country_data[f"seasonality_m2"]
    MAR_FRACTION = country_data[f"seasonality_m3"]
    APR_FRACTION = country_data[f"seasonality_m4"]
    MAY_FRACTION = country_data[f"seasonality_m5"]
    JUN_FRACTION = country_data[f"seasonality_m6"]
    JUL_FRACTION = country_data[f"seasonality_m7"]
    AUG_FRACTION = country_data[f"seasonality_m8"]
    SEP_FRACTION = country_data[f"seasonality_m9"]
    OCT_FRACTION = country_data[f"seasonality_m10"]
    NOV_FRACTION = country_data[f"seasonality_m11"]
    DEC_FRACTION = country_data[f"seasonality_m12"]

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
    JAN_YIELD = JAN_FRACTION * outdoor_crop_parameters["ANNUAL_PRODUCTION"]
    FEB_YIELD = FEB_FRACTION * outdoor_crop_parameters["ANNUAL_PRODUCTION"]
    MAR_YIELD = MAR_FRACTION * outdoor_crop_parameters["ANNUAL_PRODUCTION"]
    APR_YIELD = APR_FRACTION * outdoor_crop_parameters["ANNUAL_PRODUCTION"]
    MAY_YIELD = MAY_FRACTION * outdoor_crop_parameters["ANNUAL_PRODUCTION"]
    JUN_YIELD = JUN_FRACTION * outdoor_crop_parameters["ANNUAL_PRODUCTION"]
    JUL_YIELD = JUL_FRACTION * outdoor_crop_parameters["ANNUAL_PRODUCTION"]
    AUG_YIELD = AUG_FRACTION * outdoor_crop_parameters["ANNUAL_PRODUCTION"]
    SEP_YIELD = SEP_FRACTION * outdoor_crop_parameters["ANNUAL_PRODUCTION"]
    OCT_YIELD = OCT_FRACTION * outdoor_crop_parameters["ANNUAL_PRODUCTION"]
    NOV_YIELD = NOV_FRACTION * outdoor_crop_parameters["ANNUAL_PRODUCTION"]
    DEC_YIELD = DEC_FRACTION * outdoor_crop_parameters["ANNUAL_PRODUCTION"]

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
    RATIO_KCALS_POSTDISASTER_1Y = country_data["crop_reduction_year1"]
    RATIO_KCALS_POSTDISASTER_2Y = country_data["crop_reduction_year2"]
    RATIO_KCALS_POSTDISASTER_3Y = country_data["crop_reduction_year3"]
    RATIO_KCALS_POSTDISASTER_4Y = country_data["crop_reduction_year4"]
    RATIO_KCALS_POSTDISASTER_5Y = country_data["crop_reduction_year5"]
    RATIO_KCALS_POSTDISASTER_6Y = country_data["crop_reduction_year6"]
    RATIO_KCALS_POSTDISASTER_7Y = country_data["crop_reduction_year7"]
    RATIO_KCALS_POSTDISASTER_8Y = country_data["crop_reduction_year8"]
    RATIO_KCALS_POSTDISASTER_9Y = country_data["crop_reduction_year9"]
    RATIO_KCALS_POSTDISASTER_10Y = country_data["crop_reduction_year10"]

    MAY_UNTIL_DECEMBER_FIRST_YEAR_REDUCTION = (
        get_year_1_ratio_using_fraction_harvest_before_may(
            RATIO_KCALS_POSTDISASTER_1Y,
            country_data["SEASONALITY"],
            country_data["COUNTRY_CODE"],
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
    all_months_reductions = np.array(
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
    # assert len(all_months_reductions) == NMONTHS
    PLOT_NO_SEASONALITY_FLAG = False
    if PLOT_NO_SEASONALITY_FLAG:
        print("Plotting with no seasonality")
        Plotter.plot_monthly_reductions_no_seasonality(all_months_reductions)

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
    months_cycle = (
        month_cycle_starting_january[month_index:]
        + month_cycle_starting_january[0:month_index]
    )

    return months_cycle, all_months_reductions


def get_year_1_ratio_using_fraction_harvest_before_may(
    first_year_xia_et_al_reduction, seasonality_values, country_iso3
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
    assert first_year_xia_et_al_reduction < 101  # the improvement can't be that much...

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


if __name__ == "__main__":
    repo_root = Path(__file__).parent

    NO_TRADE_CSV = (
        Path(repo_root) / "data" / "no_food_trade" / "computer_readable_combined.csv"
    )

    no_trade_table = pd.read_csv(NO_TRADE_CSV)

    for index, country_data in no_trade_table.iterrows():
        pprint.pprint(get_new_columns_outdoor_crops(country_data))
