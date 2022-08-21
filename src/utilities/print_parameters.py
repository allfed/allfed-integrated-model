import numpy as np
from src.food_system.food import Food


class PrintParameters:
    def __init__(self):
        pass

    def print_constants_with_waste(
        self,
        population,
        constants,
        time_consts,
        feed_and_biofuels,
        methane_scp,
        meat_and_dairy,
    ):
        print(
            """
            conversion to kcals/person/day:
            million dry caloric tons monthly * 12 = millon dry caloric tons annually
            million dry caloric tons annually * 1e6 = dry caloric tons annually
            dry caloric tons annually * 1e3 = dry caloric kg annually
            dry caloric kg annually * 4e3 = calories annually (1 kg dry caloric just
            means the equivalent of 1 kg of sugar)
            calories annually  / 365 = calories per day
            calories per day / 7.8e9 = calories per person per day globally
            therefore:
            calories per person per day globally =
            million tons dry caloric monthly * 12 * 1e6 * 4e6 / 365 / 7.8e9

            conversion to months worth of food:
            million tons dry caloric * 1e6 = tons dry caloric
            tons dry caloric * 1e3 = kg dry caloric
            kg dry caloric * 4e3 = calories
            calories / 2100 = people fed per day
            people fed per day / 30 = people fed per month
            people fed per month / 7.8e9 = fraction of global population fed for a month
            fraction of global population fed for a month = months global population
            is fed from this food source
            therefore:
            months global population fed = million tons dry caloric *1e6*4e6 /2100/30/7.8e9

            WASTE in percent:
        """
        )
        print(constants["inputs"]["WASTE"])
        AMOUNT_TO_CANCEL_OUT_CROP_WASTE = 0
        AMOUNT_TO_CANCEL_OUT_MEAT_WASTE = 0
        AMOUNT_TO_CANCEL_OUT_MILK_WASTE = 0
        AMOUNT_TO_CANCEL_OUT_FISH_WASTE = 0

        self.print_constants(
            population,
            constants,
            time_consts,
            feed_and_biofuels,
            methane_scp,
            meat_and_dairy,
            AMOUNT_TO_CANCEL_OUT_CROP_WASTE,
            AMOUNT_TO_CANCEL_OUT_MEAT_WASTE,
            AMOUNT_TO_CANCEL_OUT_MILK_WASTE,
            AMOUNT_TO_CANCEL_OUT_FISH_WASTE,
        )

    def print_constants_no_waste(
        self,
        population,
        constants,
        time_consts,
        feed_and_biofuels,
        methane_scp,
        meat_and_dairy,
    ):
        print(
            """
            conversion to kcals/person/day:
            million dry caloric tons monthly * 12 = millon dry caloric tons annually
            million dry caloric tons annually * 1e6 = dry caloric tons annually
            dry caloric tons annually * 1e3 = dry caloric kg annually
            dry caloric kg annually * 4e3 = calories annually (1 kg dry caloric just
             means the equivalent of 1 kg of sugar)
            calories annually  / 365 = calories per day
            calories per day / 7.8e9 = calories per person per day globally
            therefore:
            calories per person per day globally =
            million tons dry caloric monthly * 12 * 1e6 * 4e6 / 365 / 7.8e9

            conversion to months worth of food:
            million tons dry caloric * 1e6 = tons dry caloric
            tons dry caloric * 1e3 = kg dry caloric
            kg dry caloric * 4e3 = calories
            calories / 2100 = people fed per day
            people fed per day / 30 = people fed per month
            people fed per month / 7.8e9 = fraction of global population fed for a month
            fraction of global population fed for a month = months global population
            is fed from this food source
            therefore:
            months global population fed = million tons dry caloric *1e6*4e6 /2100/30/7.8e9

            NOTE: WASTE IS NOT CONSIDERED:
        """
        )
        AMOUNT_TO_CANCEL_OUT_CROP_WASTE = constants["inputs"]["WASTE"]["CROPS"]
        AMOUNT_TO_CANCEL_OUT_MEAT_WASTE = constants["inputs"]["WASTE"]["MEAT"]
        AMOUNT_TO_CANCEL_OUT_MILK_WASTE = constants["inputs"]["WASTE"]["MILK"]
        AMOUNT_TO_CANCEL_OUT_FISH_WASTE = constants["inputs"]["WASTE"]["SEAFOOD"]
        self.print_constants(
            population,
            constants,
            time_consts,
            feed_and_biofuels,
            methane_scp,
            meat_and_dairy,
            AMOUNT_TO_CANCEL_OUT_CROP_WASTE,
            AMOUNT_TO_CANCEL_OUT_MEAT_WASTE,
            AMOUNT_TO_CANCEL_OUT_MILK_WASTE,
            AMOUNT_TO_CANCEL_OUT_FISH_WASTE,
        )

    def print_constants(
        self,
        population,
        constants,
        time_consts,
        feed_and_biofuels,
        methane_scp,
        meat_and_dairy,
        CROP_WASTE,
        MEAT_WASTE,
        MILK_WASTE,
        FISH_WASTE,
    ):
        # used by world population
        print("")
        print("calories consumed per day")
        print(constants["KCALS_DAILY"])
        print("fat consumed per day grams")
        print(constants["FAT_DAILY"])
        print("protein consumed per day grams")
        print(constants["PROTEIN_DAILY"])
        print("")
        print(
            "INITIAL_HUMANS_KCALS "
            + str(population)
            + " people consumed million tons dry caloric monthly"
        )
        print(-population * constants["KCALS_MONTHLY"] / 4e6 / 1e6)
        print(
            "INITIAL_HUMANS_FAT "
            + str(population)
            + " people consumed million tons monthly"
        )
        print(-population * constants["FAT_MONTHLY"] / 1e3)
        print(
            "INITIAL_HUMANS_PROTEIN "
            + str(population)
            + " people consumed million tons monthly"
        )
        print(-population * constants["PROTEIN_MONTHLY"] / 1e3)
        print("")
        # 1000 tons protein or fat per dry caloric ton
        print("INITIAL_HUMANS_FAT consumed percentage")
        print(
            100
            * population
            * constants["FAT_MONTHLY"]
            / 1e3
            / (population * constants["KCALS_MONTHLY"] / 4e6 / 1e6)
        )
        print("INITIAL_HUMANS_PROTEIN consumed percentage")
        print(
            100
            * population
            * constants["PROTEIN_MONTHLY"]
            / 1e3
            / (population * constants["KCALS_MONTHLY"] / 4e6 / 1e6)
        )

        amount_to_cancel_waste = 1 / (1 - CROP_WASTE / 100)

        CFP = time_consts["outdoor_crops"].kcals[0] * amount_to_cancel_waste

        # 1000 tons protein or fat per dry caloric ton
        print("")
        print("INITIAL_OG_KCALS million tons dry caloric monthly")
        print(CFP * 1e9 / 4e6 / 1e6)
        print("INITIAL_OG_FAT million tons monthly")
        print(CFP * constants["OG_FRACTION_FAT"] / 1e3)
        print("INITIAL_OG_PROTEIN million tons monthly")
        print(CFP * constants["OG_FRACTION_PROTEIN"] / 1e3)
        print("")
        print("INITIAL_OG_FAT percentage")
        print(100 * CFP * constants["OG_FRACTION_FAT"] / 1e3 / (CFP * 1e9 / 4e6 / 1e6))
        print("INITIAL_OG_PROTEIN percentage")
        print(
            100 * CFP * constants["OG_FRACTION_PROTEIN"] / 1e3 / (CFP * 1e9 / 4e6 / 1e6)
        )
        if constants["inputs"]["OG_USE_BETTER_ROTATION"]:
            outdoor_crops_RF_KCALS = (
                constants["OG_ROTATION_FRACTION_KCALS"] * amount_to_cancel_waste
            )
            outdoor_crops_RF_FAT = (
                constants["OG_ROTATION_FRACTION_FAT"] * amount_to_cancel_waste
            )
            outdoor_crops_RF_PROTEIN = (
                constants["OG_ROTATION_FRACTION_PROTEIN"] * amount_to_cancel_waste
            )
            print("")
            print("INITIAL_OG_ROTATION_KCALS million tons dry caloric monthly")
            print(CFP * outdoor_crops_RF_KCALS * 1e9 / 4e6 / 1e6)
            print("INITIAL_OG_ROTATION_FAT million tons monthly")
            print(CFP * outdoor_crops_RF_FAT / 1e3)
            print("INITIAL_OG_ROTATION_PROTEIN million tons monthly")
            print(CFP * outdoor_crops_RF_PROTEIN / 1e3)
            print("")
            print("INITIAL_OG_ROTATION_FAT percentage")
            print(
                100
                * CFP
                * outdoor_crops_RF_FAT
                / 1e3
                / (CFP * outdoor_crops_RF_KCALS * 1e9 / 4e6 / 1e6)
            )
            print("INITIAL_OG_ROTATION_PROTEIN percentage")
            print(
                100
                * CFP
                * constants["OG_ROTATION_FRACTION_PROTEIN"]
                / 1e3
                / (CFP * 1e9 / 4e6 / 1e6)
            )
        INITIAL_SF_KCALS = constants["stored_food"].kcals * amount_to_cancel_waste
        SF_FRACTION_FAT = constants["SF_FRACTION_FAT"]
        SF_FRACTION_PROTEIN = constants["SF_FRACTION_PROTEIN"]

        print("")
        print("INITIAL_SF_KCALS million tons dry caloric")
        print(INITIAL_SF_KCALS * 1e9 / 4e6 / 1e6)
        print("INITIAL_SF_FAT million tons")
        print(INITIAL_SF_KCALS * SF_FRACTION_FAT / 1e3)
        print("INITIAL_SF_PROTEIN million tons")
        print(INITIAL_SF_KCALS * SF_FRACTION_PROTEIN / 1e3)
        print("")
        print("INITIAL_SF_FAT percentage")
        print(100 * (SF_FRACTION_FAT / 1e3) / (1e9 / 4e6 / 1e6))
        print("INITIAL_SF_PROTEIN percentage")
        print(100 * (SF_FRACTION_PROTEIN / 1e3) / (1e9 / 4e6 / 1e6))
        if feed_and_biofuels.feed.kcals[0] * amount_to_cancel_waste > 0:
            print("")
            print("INITIAL_FEED_KCALS million tons dry caloric monthly postcap")
            print(
                -feed_and_biofuels.feed.kcals[0]
                * amount_to_cancel_waste
                * 1e9
                / 4e6
                / 1e6
            )
            print("INITIAL_FEED_FAT million tons monthly  postcap")
            print(-feed_and_biofuels.feed.fat[0] * amount_to_cancel_waste / 1e3)
            print("INITIAL_FEED_PROTEIN million tons monthly postcap")
            print(-feed_and_biofuels.feed.protein[0] * amount_to_cancel_waste / 1e3)
            print("")
            print("INITIAL_FEED_fat percentage postcap")
            print(
                100
                * feed_and_biofuels.feed.fat[0]
                * amount_to_cancel_waste
                / 1e3
                / (
                    feed_and_biofuels.feed.kcals[0]
                    * amount_to_cancel_waste
                    * 1e9
                    / 4e6
                    / 1e6
                )
            )
            print("INITIAL_FEED_PROTEIN percentage  postcap")
            print(
                100
                * feed_and_biofuels.feed.protein[0]
                * amount_to_cancel_waste
                / 1e3
                / (
                    feed_and_biofuels.feed.kcals[0]
                    * amount_to_cancel_waste
                    * 1e9
                    / 4e6
                    / 1e6
                )
            )
            print("")

            CPM = np.array(meat_and_dairy.chicken_pork_kcals)[0]
            if CPM > 0:
                print("INITIAL_CH_PK_KCALS million tons dry caloric monthly")
                print(CPM * 1e9 / 4e6 / 1e6 / (1 - MEAT_WASTE / 100))
                print("INITIAL_CH_PK_FAT million tons monthly")
                print(meat_and_dairy.chicken_pork_fat[0] / 1e3 / (1 - MEAT_WASTE / 100))
                print("INITIAL_CH_PK_PROTEIN million tons monthly")
                print(
                    meat_and_dairy.chicken_pork_protein[0]
                    / 1e3
                    / (1 - MEAT_WASTE / 100)
                )
                print("")
                print("INITIAL_CH_PK_FAT percentage")
                print(
                    100
                    * meat_and_dairy.chicken_pork_fat[0]
                    / 1e3
                    / (CPM * 1e9 / 4e6 / 1e6)
                )
                print("INITIAL_CH_PK_PROTEIN percentage")
                print(
                    100
                    * meat_and_dairy.chicken_pork_protein[0]
                    / 1e3
                    / (CPM * 1e9 / 4e6 / 1e6)
                )
                print("")
            else:
                print("(no chicken pork maintained considered yet)")
                print("")
            cattle_grain_fed_kcals = time_consts["grain_fed_meat_kcals"]
            cattle_grain_fed_fat = time_consts["grain_fed_meat_fat"]
            cattle_grain_fed_protein = time_consts["grain_fed_meat_protein"]
            if cattle_grain_fed_kcals[0] > 0:
                print("INITIAL_CATTLE_GRAIN_FED_KCALS million tons dry caloric monthly")

                print(
                    cattle_grain_fed_kcals[0] * 1e9 / 4e6 / 1e6 / (1 - MEAT_WASTE / 100)
                )

                print("INITIAL_CATTLE_GRAIN_FED_FAT million tons monthly")
                print(cattle_grain_fed_fat[0] / 1e3 / (1 - MEAT_WASTE / 100))
                print("INITIAL_CATTLE_GRAIN_FED_PROTEIN million tons monthly")
                print(cattle_grain_fed_protein[0] / 1e3 / (1 - MEAT_WASTE / 100))
                print("")
                print("INITIAL_CATTLE_GRAIN_FED_FAT percentage")
                print(
                    100
                    * cattle_grain_fed_fat[0]
                    / 1e3
                    / (cattle_grain_fed_kcals[0] * 1e9 / 4e6 / 1e6)
                )
                print("INITIAL_CATTLE_GRAIN_FED_PROTEIN percentage")
                print(
                    100
                    * cattle_grain_fed_protein[0]
                    / 1e3
                    / (cattle_grain_fed_kcals[0] * 1e9 / 4e6 / 1e6)
                )
            else:
                print("")
                print("no grain fed cattle")
                print("")
            print("")
            if constants["culled_meat"] > 0:
                print("culled chicken, pork, and cattle total.")
                print("culled_meat")
                print(constants["culled_meat"] / (1 - MEAT_WASTE / 100))
            else:
                print("no culled meat")
                print("")

            GRAZING_CATTLE_KCALS = time_consts["cattle_grazing_maintained_kcals"][0] / (
                1 - MEAT_WASTE / 100
            )
            GRAZING_CATTLE_FAT = time_consts["cattle_grazing_maintained_fat"][0] / (
                1 - MEAT_WASTE / 100
            )
            GRAZING_CATTLE_PROTEIN = time_consts["cattle_grazing_maintained_protein"][
                0
            ] / (1 - MEAT_WASTE / 100)

            if GRAZING_CATTLE_KCALS > 0:
                print(
                    """INITIAL_GRAZING_CATTLE_KCALS million tons dry caloric monthly
                     (cattle meat produced in 2020 monthly)"""
                )
                print(GRAZING_CATTLE_KCALS * 1e9 / 4e6 / 1e6)

                print("INITIAL_GRAZING_CATTLE_FAT million tons monthly")
                print(GRAZING_CATTLE_FAT / 1e3)
                print("INITIAL_GRAZING_CATTLE_PROTEIN million tons monthly")
                print(GRAZING_CATTLE_PROTEIN / 1e3)
                print("")
                print("INITIAL_GRAZING_CATTLE_FAT percentage")
                print(
                    100
                    * GRAZING_CATTLE_FAT
                    / 1e3
                    / (GRAZING_CATTLE_KCALS * 1e9 / 4e6 / 1e6)
                )
                print("INITIAL_GRAZING_CATTLE_PROTEIN percentage")
                print(
                    100
                    * GRAZING_CATTLE_PROTEIN
                    / 1e3
                    / (GRAZING_CATTLE_KCALS * 1e9 / 4e6 / 1e6)
                )
                print("")
            else:
                print("No meat (would be cattle) from inedible sources")
                print("")

            print("")
        else:
            print("No Feed Usage")

        if constants["ADD_MILK"]:
            grazing_milk_kcals = time_consts["grazing_milk_kcals"][0]
            grazing_milk_fat = time_consts["grazing_milk_fat"][0]
            grazing_milk_protein = time_consts["grazing_milk_protein"][0]
            print("INITIAL_GRAZING_MILK_KCALS million tons dry caloric monthly")
            print(grazing_milk_kcals / (1 - MILK_WASTE / 100) * 1e9 / 4e6 / 1e6)

            print("INITIAL_GRAZING_MILK_FAT million tons monthly")
            print(grazing_milk_fat / (1 - MILK_WASTE / 100) / 1e3)
            print("INITIAL_GRAZING_MILK_PROTEIN million tons monthly")
            print(grazing_milk_protein / (1 - MILK_WASTE / 100) / 1e3)
            print("")
            print("INITIAL_GRAZING_MILK_FAT percentage")
            print(
                100
                * grazing_milk_fat
                / (1 - MILK_WASTE / 100)
                / 1e3
                / (grazing_milk_kcals / (1 - MILK_WASTE / 100) * 1e9 / 4e6 / 1e6)
            )
            print("INITIAL_GRAZING_MILK_PROTEIN percentage")
            print(
                100
                * grazing_milk_protein
                / (1 - MILK_WASTE / 100)
                / 1e3
                / (grazing_milk_kcals / (1 - MILK_WASTE / 100) * 1e9 / 4e6 / 1e6)
            )
            print("")
            grain_fed_milk_kcals = time_consts["grain_fed_milk_kcals"][0]
            if (grain_fed_milk_kcals > 0).any():
                grain_fed_milk_fat = time_consts["grain_fed_milk_fat"][0]
                grain_fed_milk_protein = time_consts["grain_fed_milk_protein"][0]
                print("INITIAL_GRAIN_MILK_KCALS million tons dry caloric monthly")
                print(grain_fed_milk_kcals / (1 - MILK_WASTE / 100) * 1e9 / 4e6 / 1e6)

                print("INITIAL_GRAIN_MILK_FAT million tons monthly")
                print(grain_fed_milk_fat / (1 - MILK_WASTE / 100) / 1e3)
                print("INITIAL_GRAIN_MILK_PROTEIN million tons monthly")
                print(grain_fed_milk_protein / (1 - MILK_WASTE / 100) / 1e3)
                print("")
                print("INITIAL_MILK_FAT percentage")
                print(
                    100
                    * grain_fed_milk_fat
                    / (1 - MILK_WASTE / 100)
                    / 1e3
                    / (grain_fed_milk_kcals / (1 - MILK_WASTE / 100) * 1e9 / 4e6 / 1e6)
                )
                print("INITIAL_MILK_PROTEIN percentage")
                print(
                    100
                    * grain_fed_milk_protein
                    / (1 - MILK_WASTE / 100)
                    / 1e3
                    / (grain_fed_milk_kcals / (1 - MILK_WASTE / 100) * 1e9 / 4e6 / 1e6)
                )
                print("")
            else:
                print("no grain fed milk")
                print("")
        if constants["ADD_FISH"]:
            production_kcals_fish_per_month = time_consts[
                "production_kcals_fish_per_month"
            ][0]
            production_fat_fish_per_month = time_consts[
                "production_fat_fish_per_month"
            ][0]
            production_protein_fish_per_month = time_consts[
                "production_protein_fish_per_month"
            ][0]

            print("INITIAL_FISH_KCALS million tons dry caloric monthly")
            print(
                production_kcals_fish_per_month
                / (1 - FISH_WASTE / 100)
                * 1e9
                / 4e6
                / 1e6
            )

            print("INITIAL_FISH_PROTEIN million tons monthly")
            print(production_protein_fish_per_month / (1 - FISH_WASTE / 100) / 1e3)
            print("INITIAL_FISH_FAT million tons monthly")
            print(production_fat_fish_per_month / (1 - FISH_WASTE / 100) / 1e3)
            print("")
            print("INITIAL_FISH_FAT percentage")
            print(
                100
                * production_fat_fish_per_month
                / (1 - FISH_WASTE / 100)
                / 1e3
                / (
                    production_kcals_fish_per_month
                    / (1 - FISH_WASTE / 100)
                    * 1e9
                    / 4e6
                    / 1e6
                )
            )
            print("INITIAL_FISH_PROTEIN percentage")
            print(
                100
                * production_protein_fish_per_month
                / (1 - FISH_WASTE / 100)
                / 1e3
                / (
                    production_kcals_fish_per_month
                    / (1 - FISH_WASTE / 100)
                    * 1e9
                    / 4e6
                    / 1e6
                )
            )
            print("")
            print("")
        if feed_and_biofuels.biofuels.any_greater_than_zero():
            # 1000 tons protein/fat per dry caloric ton
            print("INITIAL_BIOFUEL_KCALS million tons dry caloric monthly")
            print(
                -feed_and_biofuels.biofuels.kcals[0]
                * amount_to_cancel_waste
                * 1e9
                / 4e6
                / 1e6
            )
            print("INITIAL_BIOFUEL_FAT million tons monthly")
            print(-feed_and_biofuels.biofuels.fat[0] * amount_to_cancel_waste / 1e3)
            print("INITIAL_BIOFUEL_PROTEIN million tons monthly")
            print(-feed_and_biofuels.biofuels.protein[0] * amount_to_cancel_waste / 1e3)
            print("INITIAL_BIOFUEL_FAT percentage")
            print(
                100
                * feed_and_biofuels.biofuels.fat[0]
                * amount_to_cancel_waste
                / 1e3
                / (
                    feed_and_biofuels.biofuels.kcals[0]
                    * amount_to_cancel_waste
                    * 1e9
                    / 4e6
                    / 1e6
                )
            )
            print("INITIAL_BIOFUEL_PROTEIN percentage")
            print(
                100
                * feed_and_biofuels.biofuels.protein[0]
                * amount_to_cancel_waste
                / 1e3
                / (
                    feed_and_biofuels.biofuels.kcals[0]
                    * amount_to_cancel_waste
                    * 1e9
                    / 4e6
                    / 1e6
                )
            )
        else:
            print("No biofuel usage")
            print("")

        if constants["ADD_METHANE_SCP"]:
            production_kcals_scp_per_month = time_consts[
                "production_kcals_scp_per_month"
            ]
            production_fat_scp_per_month = time_consts["production_fat_scp_per_month"]
            production_protein_scp_per_month = time_consts[
                "production_protein_scp_per_month"
            ]

            production_scp = Food(
                kcals=production_kcals_scp_per_month,
                fat=production_fat_scp_per_month,
                protein=production_protein_scp_per_month,
                kcals_units="billion kcals each month",
                fat_units="thousand tons each month",
                protein_units="thousand tons each month",
            )

            production_scp.in_units_kcals_grams_grams_per_capita_from_ratio(
                methane_scp.SCP_KCALS_PER_KG,
                methane_scp.SCP_FRAC_PROTEIN,
                methane_scp.SCP_FRAC_FAT,
            )
            print("production scp")
            print(production_scp)
