"""
################################# Meat and Dairy ##############################
##                                                                            #
##       Functions and constants relating to meat and milk production        #
##                                                                            #
###############################################################################
"""

import numpy as np


class MeatAndDairy:
    def __init__(self, constants_for_params):

        self.KG_TO_1000_TONS = 1 / (1e6)
        self.ADD_MILK = constants_for_params["ADD_MILK"]

        self.NMONTHS = constants_for_params["NMONTHS"]

        # edible meat, organs, and fat added
        self.ADD_MAINTAINED_MEAT = constants_for_params["ADD_MAINTAINED_MEAT"]
        self.ADD_CULLED_MEAT = constants_for_params["ADD_CULLED_MEAT"]

        self.KG_PER_SMALL_ANIMAL = 2.36
        self.KG_PER_MEDIUM_ANIMAL = 24.6
        self.KG_PER_LARGE_ANIMAL = 269.7

        self.LARGE_ANIMAL_KCALS_PER_KG = 2750
        self.LARGE_ANIMAL_FAT_RATIO = 0.182
        self.LARGE_ANIMAL_PROTEIN_RATIO = 0.257

        self.SMALL_ANIMAL_KCALS_PER_KG = 1525
        self.SMALL_ANIMAL_FAT_RATIO = 0.076
        self.SMALL_ANIMAL_PROTEIN_RATIO = 0.196

        # this one uses pigs from FAOstat, unlike the other two
        self.MEDIUM_ANIMAL_KCALS_PER_KG = 3590
        self.MEDIUM_ANIMAL_FAT_RATIO = 0.34
        self.MEDIUM_ANIMAL_PROTEIN_RATIO = 0.11

        # per kg, whole milk, per nutrition calculator
        self.MILK_KCALS = 610  # kcals per kg
        self.MILK_FAT = 0.032  # kg per kg
        self.MILK_PROTEIN = 0.033  # kg per kg

        # Human Inedible Produced Primary Dairy and Cattle Meat #########
        self.human_inedible_feed = np.array([])
        self.ratio_human_inedible_feed = np.array([])
        for i in range(1, 8):

            ratio_human_inedible_feed = constants_for_params[
                "RATIO_GRASSES_YEAR" + str(i)
            ]
            self.ratio_human_inedible_feed = np.append(
                self.ratio_human_inedible_feed, [ratio_human_inedible_feed] * 12
            )
            assert (
                0 <= ratio_human_inedible_feed <= 10000
            ), "Error: Unreasonable ratio of grass production"

            self.human_inedible_feed = np.append(
                self.human_inedible_feed,
                [
                    ratio_human_inedible_feed
                    * constants_for_params["HUMAN_INEDIBLE_FEED_BASELINE_MONTHLY"]
                ]
                * 12,  # this repeats it 12 times (one for each month in the year)
            )

        # dry caloric ton inedible feed/ton milk
        self.INEDIBLE_TO_MILK_CONVERSION = 1.44

        # Dry caloric tons edible feed per ton milk
        self.EDIBLE_TO_MILK_CONVERSION = 0.7

        # dry caloric ton excess edible feed/ton chicken or pork meat
        self.EDIBLE_TO_CHICKEN_PORK_CONVERSION = 4.8

        # Dry caloric tons edible feed per ton cattle meat
        self.EDIBLE_TO_CATTLE_CONVERSION = 9.8

        # dry caloric ton inedible feed/ton cattle
        self.INEDIBLE_TO_CATTLE_CONVERSION = 92.6

        # monthly in tons milk (present day value)
        self.MILK_LIMIT_PREWASTE = constants_for_params["TONS_MILK_ANNUAL"] / 12

        # monthly in dry caloric tons inedible feed
        self.MILK_LIMIT_FEED_USAGE = (
            self.MILK_LIMIT_PREWASTE * self.INEDIBLE_TO_MILK_CONVERSION
        )

        # tons meat per month
        self.CHICKEN_AND_PORK_LIMIT_PREWASTE = (
            constants_for_params["TONS_CHICKEN_AND_PORK_ANNUAL"] / 12
        )
        self.TONS_BEEF_MONTHLY_BASELINE_PREWASTE = (
            constants_for_params["TONS_BEEF_ANNUAL"] / 12
        )  # tons a month meat

        INITIAL_MILK_CATTLE = constants_for_params["INITIAL_MILK_CATTLE"]
        self.INIT_SMALL_ANIMALS = constants_for_params["INIT_SMALL_ANIMALS"]
        self.INIT_MEDIUM_ANIMALS = constants_for_params["INIT_MEDIUM_ANIMALS"]

        self.INIT_LARGE_ANIMALS = (
            constants_for_params["INIT_LARGE_ANIMALS_WITH_MILK_COWS"]
            - INITIAL_MILK_CATTLE
        )

        self.MEAT_WASTE = constants_for_params["WASTE"]["MEAT"]
        self.MILK_WASTE = constants_for_params["WASTE"]["MILK"]

    def calculate_meat_nutrition(self):
        # chicken pork assumed to maintain ratio between medium
        # and small animal mass
        small_to_medium_ratio = (
            self.INIT_SMALL_ANIMALS
            * self.KG_PER_SMALL_ANIMAL
            / (
                self.INIT_MEDIUM_ANIMALS * self.KG_PER_MEDIUM_ANIMAL
                + self.INIT_SMALL_ANIMALS * self.KG_PER_SMALL_ANIMAL
            )
        )

        self.dry_caloric_tons_per_ton_chicken_pork = (
            (
                self.SMALL_ANIMAL_KCALS_PER_KG * small_to_medium_ratio
                + self.MEDIUM_ANIMAL_KCALS_PER_KG * (1 - small_to_medium_ratio)
            )  # now units kcals per kg meat
            * 1000  # now units kcals per ton meat
            / 4e6  # now units dry caloric tons per ton meat
        )

        self.dry_caloric_tons_per_ton_beef = self.LARGE_ANIMAL_KCALS_PER_KG * 1000 / 4e6

        self.thousand_tons_fat_per_ton_chicken_pork = (
            self.SMALL_ANIMAL_FAT_RATIO * small_to_medium_ratio
            + self.MEDIUM_ANIMAL_FAT_RATIO * (1 - small_to_medium_ratio)
        ) / 1000  # now units thousand tons fat per ton meat

        self.thousand_tons_protein_per_ton_chicken_pork = (
            self.SMALL_ANIMAL_PROTEIN_RATIO * small_to_medium_ratio
            + self.MEDIUM_ANIMAL_PROTEIN_RATIO * (1 - small_to_medium_ratio)
        ) / 1000  # now units thousand tons protein per ton meat

        # monthly in dry caloric tons
        self.CHICKEN_PORK_LIMIT_FOOD_USAGE_PREWASTE = (
            self.CHICKEN_AND_PORK_LIMIT_PREWASTE
            * self.dry_caloric_tons_per_ton_chicken_pork
        )

        # monthly in dry caloric tons
        self.BEEF_LIMIT_FOOD_USAGE_PREWASTE = (
            self.TONS_BEEF_MONTHLY_BASELINE_PREWASTE
            * self.dry_caloric_tons_per_ton_beef
        )

    def calculate_meat_limits(
        self, MAX_RATIO_CULLED_SLAUGHTER_TO_BASELINE, culled_meat_initial
    ):
        """
        calculate the baseline levels of meat production, indicating slaughter capacity

        There's no limit on the actual amount eaten, but the amount produced and
        then preserved after culling is assumed to be some multiple of current slaughter
        capacity

        This just means that the limit each month on the amount that could be eaten is
        the sum of the max estimated slaughter capacity each month

        """

        meat_limit = 0
        cumulative_meat_limit = np.zeros(self.NMONTHS)
        for m in range(0, self.NMONTHS):
            meat_limit = (
                meat_limit
                + self.CHICKEN_PORK_LIMIT_FOOD_USAGE_PREWASTE
                + self.BEEF_LIMIT_FOOD_USAGE_PREWASTE
            ) * MAX_RATIO_CULLED_SLAUGHTER_TO_BASELINE

            cumulative_meat_limit[m] = min(meat_limit, culled_meat_initial)

        return cumulative_meat_limit

    # CALCULATIONS FOR MEAT AND DAIRY PRODUCTION USING GRAIN AND GRAZING

    # the following two functions are less efficient alternatives for bad adaptation

    def calculate_continued_ratios_meat_dairy_grazing(self, constants_for_params):

        # This condition is set in the scenarios file as well. They should both be set
        # to the same value.
        # Setting it to true mimics the Xia et al result, but is less accurate.
        # (if subtracting feed directly from outdoor crops)
        SUBTRACT_FEED_DIRECTLY = False

        if SUBTRACT_FEED_DIRECTLY:
            ratio_grazing_meat = 0.46
            ratio_grazing_milk = 0.46

            self.grazing_milk_produced_prewaste = (
                self.MILK_LIMIT_PREWASTE
                * self.ratio_human_inedible_feed
                * ratio_grazing_milk
            )
            self.cattle_grazing_maintained_prewaste = (
                self.TONS_BEEF_MONTHLY_BASELINE_PREWASTE
                * self.ratio_human_inedible_feed
                * ratio_grazing_meat
            )
        else:
            # Portion of grass goes proportional to the ratio of meat cattle to milk cattle
            # total heads precatastrophe.

            heads_dairy_cows = constants_for_params["INITIAL_MILK_CATTLE"]
            # total head count of large sized animals minus milk cows
            total_heads_cattle = constants_for_params[
                "INIT_LARGE_ANIMALS_WITH_MILK_COWS"
            ]

            ratio_grazing_meat = (
                total_heads_cattle - heads_dairy_cows
            ) / total_heads_cattle
            ratio_grazing_milk = 1 - ratio_grazing_meat

            assert 0 <= ratio_grazing_milk <= 1
            assert 0 <= ratio_grazing_meat <= 1

            self.grazing_milk_produced_prewaste = (
                ratio_grazing_milk
                * self.human_inedible_feed
                / self.INEDIBLE_TO_MILK_CONVERSION
            )

            self.cattle_grazing_maintained_prewaste = (
                ratio_grazing_meat
                * self.human_inedible_feed
                / self.INEDIBLE_TO_CATTLE_CONVERSION
            )

    def calculate_continued_ratios_meat_dairy_grain(
        self, fed_to_animals_prewaste, outdoor_crops
    ):

        # This condition is set in the scenarios file as well. They should both be set
        # to the same value.
        # Setting it to true mimics the Xia et al result, but is less accurate.
        # (if subtracting feed directly from outdoor crops)
        SUBTRACT_FEED_DIRECTLY = False

        if SUBTRACT_FEED_DIRECTLY:
            # similar assumption as Xia et al paper.

            ratio_grainfed_meat = 0.54
            ratio_grainfed_milk = 0.54

            self.grain_fed_milk_produced_prewaste = (
                self.MILK_LIMIT_PREWASTE
                * outdoor_crops.all_months_reductions
                * ratio_grainfed_milk
            )
            self.cattle_grain_fed_maintained_prewaste = (
                self.TONS_BEEF_MONTHLY_BASELINE_PREWASTE
                * outdoor_crops.all_months_reductions
                * ratio_grainfed_meat
            )
            self.chicken_pork_maintained_prewaste = (
                self.TONS_BEEF_MONTHLY_BASELINE_PREWASTE
                * outdoor_crops.all_months_reductions
                * ratio_grainfed_meat
            )
        else:
            # Portion of grain goes proportional to usage of feed from meat cattle to
            # usage of feed for chicken/pork precatastrophe.
            # Usage of human edible feed for dairy is ignored as it is small.
            # Usage of human inedible feed for meat is ignored as it is small.
            feed_for_chicken_pork_precatastrophe = (
                self.CHICKEN_AND_PORK_LIMIT_PREWASTE
                * self.EDIBLE_TO_CHICKEN_PORK_CONVERSION
            )
            feed_for_beef_precatastrophe = (
                self.TONS_BEEF_MONTHLY_BASELINE_PREWASTE
                * self.EDIBLE_TO_CATTLE_CONVERSION
            )

            ratio_beef_feed = feed_for_beef_precatastrophe / (
                feed_for_chicken_pork_precatastrophe + feed_for_beef_precatastrophe
            )

            ratio_chicken_pork_feed = 1 - ratio_beef_feed

            assert 0 <= ratio_beef_feed <= 1
            assert 0 <= ratio_chicken_pork_feed <= 1

            excess_dry_cal_tons = fed_to_animals_prewaste.kcals * 1e9 / 4e6

            self.cattle_grain_fed_maintained_prewaste = (
                excess_dry_cal_tons * ratio_beef_feed / self.EDIBLE_TO_CATTLE_CONVERSION
            )

            self.chicken_pork_maintained_prewaste = (
                excess_dry_cal_tons
                * ratio_chicken_pork_feed
                / self.EDIBLE_TO_CHICKEN_PORK_CONVERSION
            )
            self.grain_fed_milk_produced_prewaste = np.array([0] * self.NMONTHS)

    def calculate_meat_and_dairy_from_grain(self, fed_to_animals_prewaste):

        # each unit of excess kcals (with associated fat and protein)
        # are fed first to milk, then to pigs and chickens, then to cattle

        excess_dry_cal_tons = fed_to_animals_prewaste.kcals * 1e9 / 4e6
        if np.array(excess_dry_cal_tons < 0).any():
            print("excess_dry_cal_tons per month")
            print(excess_dry_cal_tons)
            print(
                """It appears assigning excess calories to feed or biofuels was attempted,
                but there were not enough calories to use for the feed and biofuel
                (because of this, excess was calculated as being negative).
                \nTry to rerun where the population fed after waste incorporating
                delayed shutoff to feed in biofuels is above the assigned global population.
                \nQuitting."""
            )
            quit()
        assert np.array(excess_dry_cal_tons >= 0).all()

        # dry caloric ton excess/ton milk
        grain_fed_milk_limit_food_usage_prewaste = (
            self.grain_fed_milk_limit_prewaste * self.EDIBLE_TO_MILK_CONVERSION
        )

        # dry caloric ton excess/ton meat
        grain_fed_milk_produced_prewaste = []
        chicken_pork_maintained_prewaste = []
        cattle_grain_fed_maintained_prewaste = []
        for m in range(self.NMONTHS):

            max_milk = excess_dry_cal_tons[m] / self.EDIBLE_TO_MILK_CONVERSION

            if self.ADD_MILK:

                if max_milk <= self.grain_fed_milk_limit_prewaste[m]:
                    # tons per month milk
                    grain_fed_milk_produced_prewaste.append(max_milk)
                    # tons per month meat
                    chicken_pork_maintained_prewaste.append(0)
                    cattle_grain_fed_maintained_prewaste.append(0)
                    continue

                grain_fed_milk_produced_prewaste.append(
                    self.grain_fed_milk_limit_prewaste[m]
                )

                limit_milk_prewaste = grain_fed_milk_limit_food_usage_prewaste[m]
            else:
                limit_milk_prewaste = 0
                grain_fed_milk_produced_prewaste.append(0)

            for_chicken_pork_cattle_prewaste = (
                excess_dry_cal_tons[m] - limit_milk_prewaste
            )

            assert for_chicken_pork_cattle_prewaste >= 0

            max_chicken_pork_prewaste = (
                for_chicken_pork_cattle_prewaste
                / self.EDIBLE_TO_CHICKEN_PORK_CONVERSION
            )

            if max_chicken_pork_prewaste <= self.CHICKEN_AND_PORK_LIMIT_PREWASTE:
                # tons per month meat
                chicken_pork_maintained_prewaste.append(max_chicken_pork_prewaste)
                # tons per month meat
                cattle_grain_fed_maintained_prewaste.append(0)
                continue

            # tons per month meat
            chicken_pork_maintained_prewaste.append(
                self.CHICKEN_AND_PORK_LIMIT_PREWASTE
            )
            for_cattle_prewaste = (
                for_chicken_pork_cattle_prewaste
                - self.CHICKEN_PORK_LIMIT_FOOD_USAGE_PREWASTE
            )

            # tons per month meat
            cattle_grain_fed_maintained_prewaste.append(
                for_cattle_prewaste / self.EDIBLE_TO_CATTLE_CONVERSION
            )

        assert (np.array(grain_fed_milk_produced_prewaste) >= 0).all()

        if not self.ADD_MILK:
            grain_fed_milk_produced_prewaste = np.array([0] * self.NMONTHS)

        self.grain_fed_milk_produced_prewaste = grain_fed_milk_produced_prewaste
        self.cattle_grain_fed_maintained_prewaste = cattle_grain_fed_maintained_prewaste
        self.chicken_pork_maintained_prewaste = chicken_pork_maintained_prewaste

    def calculate_meat_milk_from_human_inedible_feed(self, constants_for_params):

        self.grazing_milk_produced_prewaste = []  # tons
        self.cattle_grazing_maintained_prewaste = []  # tons
        for m in range(self.NMONTHS):
            if self.ADD_MILK:
                max_milk = (
                    self.human_inedible_feed[m] / self.INEDIBLE_TO_MILK_CONVERSION
                )
                if max_milk <= self.MILK_LIMIT_PREWASTE:
                    self.grazing_milk_produced_prewaste.append(max_milk)
                    self.cattle_grazing_maintained_prewaste.append(0)
                    continue
                self.grazing_milk_produced_prewaste.append(self.MILK_LIMIT_PREWASTE)
                inedible_for_cattle = (
                    self.human_inedible_feed[m] - self.MILK_LIMIT_FEED_USAGE
                )
            else:
                self.grazing_milk_produced_prewaste.append(0)
                inedible_for_cattle = self.human_inedible_feed[m]

            if self.ADD_MAINTAINED_MEAT:
                self.cattle_grazing_maintained_prewaste.append(
                    inedible_for_cattle / self.INEDIBLE_TO_CATTLE_CONVERSION
                )
            else:
                self.cattle_grazing_maintained_prewaste.append(0)
        # assign the resulting remaining limit to milk past inedible sources
        self.grain_fed_milk_limit_prewaste = self.MILK_LIMIT_PREWASTE - np.array(
            self.grazing_milk_produced_prewaste
        )

    def get_milk_from_human_edible_feed(self, constants_for_params):

        if self.ADD_MILK:

            grain_fed_milk_kcals = (
                np.array(self.grain_fed_milk_produced_prewaste)
                * 1e3
                * self.MILK_KCALS
                / 1e9
                * (1 - self.MILK_WASTE / 100)
            )

            grain_fed_milk_fat = (
                np.array(self.grain_fed_milk_produced_prewaste)
                / 1e3
                * self.MILK_FAT
                * (1 - self.MILK_WASTE / 100)
            )

            grain_fed_milk_protein = (
                np.array(self.grain_fed_milk_produced_prewaste)
                / 1e3
                * self.MILK_PROTEIN
                * (1 - self.MILK_WASTE / 100)
            )

        else:

            grain_fed_milk_kcals = np.array([0] * self.NMONTHS)
            grain_fed_milk_fat = np.array([0] * self.NMONTHS)
            grain_fed_milk_protein = np.array([0] * self.NMONTHS)

        return (grain_fed_milk_kcals, grain_fed_milk_fat, grain_fed_milk_protein)

    def get_meat_from_human_edible_feed(self):

        present_day_tons_per_month_chicken_pork_prewaste = (
            self.CHICKEN_AND_PORK_LIMIT_PREWASTE
        )  # tons a month

        # does not consider waste
        ratio_maintained_cattle = (
            np.array(self.cattle_grazing_maintained_prewaste)
            + np.array(self.cattle_grain_fed_maintained_prewaste)
        ) / self.TONS_BEEF_MONTHLY_BASELINE_PREWASTE

        # cannot be negative
        self.ratio_not_maintained_cattle = np.max(
            [1 - ratio_maintained_cattle, np.zeros(len(ratio_maintained_cattle))],
            axis=0,
        )

        all_non_negative = np.array(ratio_maintained_cattle >= 0).all()
        assert all_non_negative

        if (ratio_maintained_cattle >= 1).any():
            PRINT_CATTLE_WARNING = False
            if PRINT_CATTLE_WARNING:
                print("")
                print("WARNING: cattle maintained is exceeding 2020 baseline levels")

        # does not consider waste
        if present_day_tons_per_month_chicken_pork_prewaste > 0:
            self.ratio_maintained_chicken_pork = (
                np.array(self.chicken_pork_maintained_prewaste)
                / present_day_tons_per_month_chicken_pork_prewaste
            )
        else:
            self.ratio_maintained_chicken_pork = np.zeros(
                len(self.chicken_pork_maintained_prewaste)
            )

        assert (self.ratio_maintained_chicken_pork.round(8) >= 0).all()

        # if there's some very small negative value here, just round it off to zero
        if (self.ratio_maintained_chicken_pork <= 0).any():
            self.ratio_maintained_chicken_pork = (
                self.ratio_maintained_chicken_pork.round(8)
            )
        assert (self.ratio_maintained_chicken_pork >= 0).all()

        all_one_or_lower = (self.ratio_maintained_chicken_pork <= 1).all()

        PRINT_CHICKEN_PORK_WARNING = False

        if not all_one_or_lower and PRINT_CHICKEN_PORK_WARNING:
            print("At least one month has higher chicken and pork above")
            print("baseline levels. This may be surprising if we are running a global")
            print("model, but is to be expected in at least some countries.")
            print("")

        # billions kcals monthly
        self.chicken_pork_prewaste_kcals = (
            np.array(self.chicken_pork_maintained_prewaste)
            * self.dry_caloric_tons_per_ton_chicken_pork  # now units dry caloric tons
            * 4e6  # now units kcals
            / 1e9  # now units billion kcals
        )

        # thousands tons monthly
        self.chicken_pork_prewaste_fat = (
            np.array(self.chicken_pork_maintained_prewaste)
            * self.thousand_tons_fat_per_ton_chicken_pork
        )

        # thousands tons monthly
        self.chicken_pork_prewaste_protein = (
            np.array(self.chicken_pork_maintained_prewaste)
            * self.thousand_tons_protein_per_ton_chicken_pork
        )

        # billions kcals monthly
        cattle_grain_fed_maintained_prewaste_kcals = (
            np.array(self.cattle_grain_fed_maintained_prewaste)
            * self.dry_caloric_tons_per_ton_beef
            * 4e6
            / 1e9
        )

        # 1000s tons fat
        cattle_grain_fed_maintained_prewaste_fat = (
            cattle_grain_fed_maintained_prewaste_kcals
            * 1e9
            / self.LARGE_ANIMAL_KCALS_PER_KG
            * self.LARGE_ANIMAL_FAT_RATIO
            / 1e6
        )

        # 1000s tons protein
        cattle_grain_fed_maintained_prewaste_protein = (
            cattle_grain_fed_maintained_prewaste_kcals
            * 1e9
            / self.LARGE_ANIMAL_KCALS_PER_KG
            * self.LARGE_ANIMAL_PROTEIN_RATIO
            / 1e6
        )

        grain_fed_meat_prewaste_kcals = np.array(
            cattle_grain_fed_maintained_prewaste_kcals
            + self.chicken_pork_prewaste_kcals
        )
        grain_fed_meat_prewaste_fat = np.array(
            cattle_grain_fed_maintained_prewaste_fat + self.chicken_pork_prewaste_fat
        )
        grain_fed_meat_prewaste_protein = np.array(
            cattle_grain_fed_maintained_prewaste_protein
            + self.chicken_pork_prewaste_protein
        )

        # used for printing out and debugging
        self.chicken_pork_kcals = self.chicken_pork_prewaste_kcals * (
            1 - self.MEAT_WASTE / 100
        )
        self.chicken_pork_fat = self.chicken_pork_prewaste_fat * (
            1 - self.MEAT_WASTE / 100
        )
        self.chicken_pork_protein = self.chicken_pork_prewaste_protein * (
            1 - self.MEAT_WASTE / 100
        )

        self.cattle_grain_fed_maintained_kcals = (
            cattle_grain_fed_maintained_prewaste_kcals * (1 - self.MEAT_WASTE / 100)
        )
        self.cattle_grain_fed_maintained_fat = (
            cattle_grain_fed_maintained_prewaste_fat * (1 - self.MEAT_WASTE / 100)
        )
        self.cattle_grain_fed_maintained_protein = (
            cattle_grain_fed_maintained_prewaste_protein * (1 - self.MEAT_WASTE / 100)
        )

        # used for printing out and debugging
        self.chicken_pork_kcals = self.chicken_pork_prewaste_kcals * (
            1 - self.MEAT_WASTE / 100
        )
        self.chicken_pork_fat = self.chicken_pork_prewaste_fat * (
            1 - self.MEAT_WASTE / 100
        )
        self.chicken_pork_protein = self.chicken_pork_prewaste_protein * (
            1 - self.MEAT_WASTE / 100
        )

        grain_fed_meat_kcals = grain_fed_meat_prewaste_kcals * (
            1 - self.MEAT_WASTE / 100
        )
        grain_fed_meat_fat = grain_fed_meat_prewaste_fat * (1 - self.MEAT_WASTE / 100)
        grain_fed_meat_protein = grain_fed_meat_prewaste_protein * (
            1 - self.MEAT_WASTE / 100
        )

        if not self.ADD_MAINTAINED_MEAT:
            grain_fed_meat_kcals = np.array([0] * self.NMONTHS)
            grain_fed_meat_fat = np.array([0] * self.NMONTHS)
            grain_fed_meat_protein = np.array([0] * self.NMONTHS)

        return (
            grain_fed_meat_kcals,
            grain_fed_meat_fat,
            grain_fed_meat_protein,
        )

    def get_grazing_milk_produced_postwaste(self):
        # billions kcals
        grazing_milk_kcals = (
            np.array(self.grazing_milk_produced_prewaste)
            * 1e3
            * self.MILK_KCALS
            / 1e9
            * (1 - self.MILK_WASTE / 100)
        )

        # thousands tons
        grazing_milk_fat = (
            np.array(self.grazing_milk_produced_prewaste)
            / 1e3
            * self.MILK_FAT
            * (1 - self.MILK_WASTE / 100)
        )

        # thousands tons
        grazing_milk_protein = (
            np.array(self.grazing_milk_produced_prewaste)
            / 1e3
            * self.MILK_PROTEIN
            * (1 - self.MILK_WASTE / 100)
        )

        return (grazing_milk_kcals, grazing_milk_fat, grazing_milk_protein)

    def get_cattle_grazing_maintained(self):

        if self.ADD_MAINTAINED_MEAT:

            # billions kcals
            cattle_grazing_maintained_kcals = (
                np.array(self.cattle_grazing_maintained_prewaste)
                * 1000
                * self.LARGE_ANIMAL_KCALS_PER_KG
                / 1e9
                * (1 - self.MEAT_WASTE / 100)
            )

            # 1000s tons fat
            cattle_grazing_maintained_fat = (
                cattle_grazing_maintained_kcals
                * 1e9
                * self.LARGE_ANIMAL_FAT_RATIO
                / self.LARGE_ANIMAL_KCALS_PER_KG
                / 1e6
            )

            # 1000s tons protein
            cattle_grazing_maintained_protein = (
                cattle_grazing_maintained_kcals
                * 1e9
                * self.LARGE_ANIMAL_PROTEIN_RATIO
                / self.LARGE_ANIMAL_KCALS_PER_KG
                / 1e6
            )

        else:
            cattle_grazing_maintained_kcals = [0] * len(
                self.cattle_grazing_maintained_prewaste
            )
            cattle_grazing_maintained_fat = [0] * len(
                self.cattle_grazing_maintained_prewaste
            )
            cattle_grazing_maintained_protein = [0] * len(
                self.cattle_grazing_maintained_prewaste
            )

        return (
            cattle_grazing_maintained_kcals,
            cattle_grazing_maintained_fat,
            cattle_grazing_maintained_protein,
        )

    # CULLED MEAT

    def calculated_culled_meat(self):
        KG_TO_1000_TONS = self.KG_TO_1000_TONS

        KCALS_PER_SMALL_ANIMAL = (
            self.SMALL_ANIMAL_KCALS_PER_KG * self.KG_PER_SMALL_ANIMAL / 1e9
        )
        FAT_PER_SMALL_ANIMAL = (
            self.SMALL_ANIMAL_FAT_RATIO * self.KG_PER_SMALL_ANIMAL * KG_TO_1000_TONS
        )
        PROTEIN_PER_SMALL_ANIMAL = (
            self.SMALL_ANIMAL_PROTEIN_RATIO * self.KG_PER_SMALL_ANIMAL * KG_TO_1000_TONS
        )

        KCALS_PER_MEDIUM_ANIMAL = (
            self.MEDIUM_ANIMAL_KCALS_PER_KG * self.KG_PER_MEDIUM_ANIMAL / 1e9
        )
        FAT_PER_MEDIUM_ANIMAL = (
            self.MEDIUM_ANIMAL_FAT_RATIO * self.KG_PER_MEDIUM_ANIMAL * KG_TO_1000_TONS
        )
        PROTEIN_MEDIUM_ANIMAL = (
            self.MEDIUM_ANIMAL_PROTEIN_RATIO
            * self.KG_PER_MEDIUM_ANIMAL
            * KG_TO_1000_TONS
        )

        KCALS_PER_LARGE_ANIMAL = (
            self.LARGE_ANIMAL_KCALS_PER_KG * self.KG_PER_LARGE_ANIMAL / 1e9
        )
        FAT_PER_LARGE_ANIMAL = (
            self.LARGE_ANIMAL_FAT_RATIO * self.KG_PER_LARGE_ANIMAL * KG_TO_1000_TONS
        )
        PROTEIN_PER_LARGE_ANIMAL = (
            self.LARGE_ANIMAL_PROTEIN_RATIO * self.KG_PER_LARGE_ANIMAL * KG_TO_1000_TONS
        )

        # billion kcals
        init_culled_meat_prewaste_kcals = (
            self.init_small_animals_culled * KCALS_PER_SMALL_ANIMAL
            + self.init_medium_animals_culled * KCALS_PER_MEDIUM_ANIMAL
            + self.init_large_animals_culled * KCALS_PER_LARGE_ANIMAL
        )
        # thousand tons
        init_culled_meat_prewaste_fat = (
            self.init_small_animals_culled * FAT_PER_SMALL_ANIMAL
            + self.init_medium_animals_culled * FAT_PER_MEDIUM_ANIMAL
            + self.init_large_animals_culled * FAT_PER_LARGE_ANIMAL
        )
        # thousand tons
        init_culled_meat_prewaste_protein = (
            self.init_small_animals_culled * PROTEIN_PER_SMALL_ANIMAL
            + self.init_medium_animals_culled * PROTEIN_MEDIUM_ANIMAL
            + self.init_large_animals_culled * PROTEIN_PER_LARGE_ANIMAL
        )

        self.initial_culled_meat_prewaste = init_culled_meat_prewaste_kcals

        if self.initial_culled_meat_prewaste > 0:
            self.culled_meat_fraction_fat = (
                init_culled_meat_prewaste_fat / init_culled_meat_prewaste_kcals
            )
            self.culled_meat_fraction_protein = (
                init_culled_meat_prewaste_protein / init_culled_meat_prewaste_kcals
            )
        else:
            self.culled_meat_fraction_fat = 0
            self.culled_meat_fraction_protein = 0

    def get_culled_meat_post_waste(self, constants_for_params):

        if self.ADD_CULLED_MEAT:
            culled_meat_prewaste = self.initial_culled_meat_prewaste
        else:
            culled_meat_prewaste = 0

        return culled_meat_prewaste * (1 - self.MEAT_WASTE / 100)

    def calculate_animals_culled(self, constants_for_params):
        if self.ADD_CULLED_MEAT:
            self.init_small_animals_culled = self.INIT_SMALL_ANIMALS * (
                1 - np.min(self.ratio_maintained_chicken_pork)
            )
            self.init_medium_animals_culled = self.INIT_MEDIUM_ANIMALS * (
                1 - np.min(self.ratio_maintained_chicken_pork)
            )
            self.init_large_animals_culled = self.INIT_LARGE_ANIMALS * np.max(
                self.ratio_not_maintained_cattle
            )
        else:
            self.init_small_animals_culled = 0
            self.init_medium_animals_culled = 0
            self.init_large_animals_culled = 0
