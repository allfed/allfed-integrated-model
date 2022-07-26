################################# Meat and Dairy ##############################
##                                                                            #
##       Functions and constants relating to meat and milk production        #
##                                                                            #
###############################################################################

import numpy as np
from src.food_system.food import Food


class MeatAndDairy:
    def __init__(self, constants_for_params):

        # time from slaughter livestock to it turning into food
        # not functional yet

        self.KG_TO_1000_TONS = 1 / (1e6)
        self.ADD_MILK = constants_for_params["ADD_MILK"]

        # we use this spreadsheeet @Morgan: Link broken
        self.NMONTHS = constants_for_params["NMONTHS"]
        # edible meat, organs, and fat added
        self.ADD_MEAT = constants_for_params["ADD_MEAT"]
        self.KG_PER_SMALL_ANIMAL = 2.36
        self.KG_PER_MEDIUM_ANIMAL = 24.6
        self.KG_PER_LARGE_ANIMAL = 269.7

        self.LARGE_ANIMAL_KCALS_PER_KG = 2750
        self.LARGE_ANIMAL_FAT_PER_KG = 0.182
        self.LARGE_ANIMAL_PROTEIN_PER_KG = 0.257

        self.SMALL_ANIMAL_KCALS_PER_KG = 1525
        self.SMALL_ANIMAL_FAT_PER_KG = 0.076
        self.SMALL_ANIMAL_PROTEIN_PER_KG = 0.196

        # @Morgan: Link broken
        # this one uses pigs from FAOstat, unlike the other two
        # roww 264, "Nutrition Data From FAOstat" tab
        self.MEDIUM_ANIMAL_KCALS_PER_KG = 3590
        self.MEDIUM_ANIMAL_FAT_PER_KG = 0.34
        self.MEDIUM_ANIMAL_PROTEIN_PER_KG = 0.11

        # per kg, whole milk, per nutrition calculator
        self.MILK_KCALS = 610  # kcals per kg
        self.MILK_FAT = 0.032  # kg per kg
        self.MILK_PROTEIN = 0.033  # kg per kg

        # Human Inedible Produced Primary Dairy and Cattle Meat #########
        self.human_inedible_feed = constants_for_params["HUMAN_INEDIBLE_FEED"]

        # dry caloric ton feed/ton milk
        self.INEDIBLE_TO_MILK_CONVERSION = 1.44

        # dry caloric ton feed/ton cattle
        # INEDIBLE_TO_CATTLE_CONVERSION = 103.0
        self.INEDIBLE_TO_CATTLE_CONVERSION = 92.6

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

    def calculated_culled_meat(self):
        KG_TO_1000_TONS = self.KG_TO_1000_TONS

        KCALS_PER_SMALL_ANIMAL = (
            self.SMALL_ANIMAL_KCALS_PER_KG * self.KG_PER_SMALL_ANIMAL / 1e9
        )
        FAT_PER_SMALL_ANIMAL = (
            self.SMALL_ANIMAL_FAT_PER_KG * self.KG_PER_SMALL_ANIMAL * KG_TO_1000_TONS
        )
        PROTEIN_PER_SMALL_ANIMAL = (
            self.SMALL_ANIMAL_PROTEIN_PER_KG
            * self.KG_PER_SMALL_ANIMAL
            * KG_TO_1000_TONS
        )

        KCALS_PER_MEDIUM_ANIMAL = (
            self.MEDIUM_ANIMAL_KCALS_PER_KG * self.KG_PER_MEDIUM_ANIMAL / 1e9
        )
        FAT_PER_MEDIUM_ANIMAL = (
            self.MEDIUM_ANIMAL_FAT_PER_KG * self.KG_PER_MEDIUM_ANIMAL * KG_TO_1000_TONS
        )
        PROTEIN_MEDIUM_ANIMAL = (
            self.MEDIUM_ANIMAL_PROTEIN_PER_KG
            * self.KG_PER_MEDIUM_ANIMAL
            * KG_TO_1000_TONS
        )

        KCALS_PER_LARGE_ANIMAL = (
            self.LARGE_ANIMAL_KCALS_PER_KG * self.KG_PER_LARGE_ANIMAL / 1e9
        )
        FAT_PER_LARGE_ANIMAL = (
            self.LARGE_ANIMAL_FAT_PER_KG * self.KG_PER_LARGE_ANIMAL * KG_TO_1000_TONS
        )
        PROTEIN_PER_LARGE_ANIMAL = (
            self.LARGE_ANIMAL_PROTEIN_PER_KG
            * self.KG_PER_LARGE_ANIMAL
            * KG_TO_1000_TONS
        )

        init_meat_culled_prewaste_kcals = (
            self.init_small_animals_culled * KCALS_PER_SMALL_ANIMAL
            + self.init_medium_animals_culled * KCALS_PER_MEDIUM_ANIMAL
            + self.init_large_animals_culled * KCALS_PER_LARGE_ANIMAL
        )
        init_meat_culled_prewaste_fat = (
            self.init_small_animals_culled * FAT_PER_SMALL_ANIMAL
            + self.init_medium_animals_culled * FAT_PER_MEDIUM_ANIMAL
            + self.init_large_animals_culled * FAT_PER_LARGE_ANIMAL
        )
        init_meat_culled_prewaste_protein = (
            self.init_small_animals_culled * PROTEIN_PER_SMALL_ANIMAL
            + self.init_medium_animals_culled * PROTEIN_MEDIUM_ANIMAL
            + self.init_large_animals_culled * PROTEIN_PER_LARGE_ANIMAL
        )

        self.initial_meat_culled_prewaste = init_meat_culled_prewaste_kcals

        if self.initial_meat_culled_prewaste > 0:
            self.meat_culled_fraction_fat = (
                init_meat_culled_prewaste_fat / init_meat_culled_prewaste_kcals
            )
            self.meat_culled_fraction_protein = (
                init_meat_culled_prewaste_protein / init_meat_culled_prewaste_kcals
            )
        else:
            self.meat_culled_fraction_fat = 0
            self.meat_culled_fraction_protein = 0

    def calculate_meat_and_dairy_from_grain(self, fed_to_animals_prewaste):

        # each unit of excess kcals (with associated fat and protein)
        # are fed first to milk, then to pigs and chickens, then to cattle

        excess_dry_cal_tons = fed_to_animals_prewaste.kcals * 1e9 / 4e6
        if np.array(excess_dry_cal_tons < 0).any():
            print("excess_dry_cal_tons per month")
            print(excess_dry_cal_tons)
            print(
                "It appears assigning excess calories to feed or biofuels was attempted, but there were not enough calories to use for the feed and biofuel (because of this, excess was calculated as being negative). \nTry to rerun where the population fed after waste incorporating delayed shutoff to feed in biofuels is above the assigned global population. \nQuitting."
            )
            quit()
        assert np.array(excess_dry_cal_tons >= 0).all()

        # dry caloric ton excess/ton milk
        EDIBLE_TO_MILK_CONVERSION = 0.7
        grain_fed_milk_limit_food_usage_prewaste = (
            self.grain_fed_milk_limit_prewaste * EDIBLE_TO_MILK_CONVERSION
        )

        # dry caloric ton excess/ton meat
        CHICKEN_PORK_CONVERSION = 4.8

        # monthly in dry caloric tons
        CHICKEN_PORK_LIMIT_FOOD_USAGE_PREWASTE = (
            self.CHICKEN_AND_PORK_LIMIT_PREWASTE * CHICKEN_PORK_CONVERSION
        )

        # dry caloric ton excess/ton meat
        EDIBLE_TO_CATTLE_CONVERSION = 9.8
        grain_fed_milk_produced_prewaste = []
        chicken_pork_maintained_prewaste = []
        cattle_grain_fed_maintained_prewaste = []
        for m in range(self.NMONTHS):

            max_milk = excess_dry_cal_tons[m] / EDIBLE_TO_MILK_CONVERSION

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
                for_chicken_pork_cattle_prewaste / CHICKEN_PORK_CONVERSION
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
                - CHICKEN_PORK_LIMIT_FOOD_USAGE_PREWASTE
            )

            # tons per month meat
            cattle_grain_fed_maintained_prewaste.append(
                for_cattle_prewaste / EDIBLE_TO_CATTLE_CONVERSION
            )

        assert (np.array(grain_fed_milk_produced_prewaste) >= 0).all()

        if not self.ADD_MILK:
            grain_fed_milk_produced_prewaste = np.array([0] * self.NMONTHS)

        print("grain_fed_milk_produced_prewaste")
        print(grain_fed_milk_produced_prewaste)

        print("cattle_grain_fed_maintained_prewaste")
        print(cattle_grain_fed_maintained_prewaste)
        print("chicken_pork_maintained_prewaste")
        print(chicken_pork_maintained_prewaste)
        self.grain_fed_milk_produced_prewaste = grain_fed_milk_produced_prewaste
        self.cattle_grain_fed_maintained_prewaste = cattle_grain_fed_maintained_prewaste
        self.chicken_pork_maintained_prewaste = chicken_pork_maintained_prewaste

    def get_meat_from_human_edible_feed(self):

        present_day_tons_per_month_cattle_prewaste = (
            self.TONS_BEEF_MONTHLY_BASELINE_PREWASTE
        )

        present_day_tons_per_month_chicken_pork_prewaste = (
            self.CHICKEN_AND_PORK_LIMIT_PREWASTE
        )  # tons a month

        # does not consider waste
        ratio_maintained_cattle = (
            np.array(self.cattle_grazing_maintained_prewaste)
            + np.array(self.cattle_grain_fed_maintained_prewaste)
        ) / present_day_tons_per_month_cattle_prewaste
        self.ratio_not_maintained_cattle = 1 - ratio_maintained_cattle

        all_non_negative = np.array(ratio_maintained_cattle >= 0).all()
        assert all_non_negative

        # make sure for the months we really care about we're not
        # exceeding present-day cattle meat maintained production
        # assert((ratio_maintained_cattle <= 1)[0:47].all())
        if (ratio_maintained_cattle[0:47] >= 1).any():
            PRINT_CATTLE_WARNING = True
            if PRINT_CATTLE_WARNING:
                print("")
                print(
                    "WARNING: cattle maintained is exceeding 2020 baseline levels in months:"
                )
                print(np.where(ratio_maintained_cattle[0:47] >= 1))
                print(
                    "Consider whether the predicted amount of human edible feed fed to animals is reasonable."
                )
                print("")

        # TODO: delete me
        # self.ratio_not_maintained_cattle[self.ratio_not_maintained_cattle < 0] = 0

        # does not consider waste
        self.ratio_maintained_chicken_pork = (
            np.array(self.chicken_pork_maintained_prewaste)
            / present_day_tons_per_month_chicken_pork_prewaste
        )

        assert (self.ratio_maintained_chicken_pork >= 0).all()

        all_one_or_lower = (self.ratio_maintained_chicken_pork <= 1).all()

        if not all_one_or_lower:
            print("At least one month has higher chicken and pork above")
            print("baseline levels. This may be surprising if we are running a global")
            print("model, but is to be expected in at least some countries.")
            print("")
        # limit the rate of livestock culling by how long it takes to reduce
        # the maintained livestock to its minimum.
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

        # billions kcals monthly
        self.chicken_pork_prewaste_kcals = (
            np.array(self.chicken_pork_maintained_prewaste)
            * 1e3
            * (
                self.SMALL_ANIMAL_KCALS_PER_KG * small_to_medium_ratio
                + self.MEDIUM_ANIMAL_KCALS_PER_KG * (1 - small_to_medium_ratio)
            )
            / 1e9
        )

        # thousands tons monthly
        self.chicken_pork_prewaste_fat = (
            np.array(self.chicken_pork_maintained_prewaste)
            * 1e3
            * (
                self.SMALL_ANIMAL_FAT_PER_KG * small_to_medium_ratio
                + self.MEDIUM_ANIMAL_FAT_PER_KG * (1 - small_to_medium_ratio)
            )
            / 1e6
        )

        # thousands tons monthly
        self.chicken_pork_prewaste_protein = (
            np.array(self.chicken_pork_maintained_prewaste)
            * 1e3
            * (
                self.SMALL_ANIMAL_PROTEIN_PER_KG * small_to_medium_ratio
                + self.MEDIUM_ANIMAL_PROTEIN_PER_KG * (1 - small_to_medium_ratio)
            )
            / 1e6
        )

        # billions kcals monthly
        cattle_grain_fed_maintained_prewaste_kcals = (
            np.array(self.cattle_grain_fed_maintained_prewaste)
            * 1000
            * self.LARGE_ANIMAL_KCALS_PER_KG
            / 1e9
        )

        # 1000s tons fat
        cattle_grain_fed_maintained_prewaste_fat = (
            cattle_grain_fed_maintained_prewaste_kcals
            * 1e9
            / self.LARGE_ANIMAL_KCALS_PER_KG
            * self.LARGE_ANIMAL_FAT_PER_KG
            / 1e6
        )

        # 1000s tons protein
        cattle_grain_fed_maintained_prewaste_protein = (
            cattle_grain_fed_maintained_prewaste_kcals
            * 1e9
            / self.LARGE_ANIMAL_KCALS_PER_KG
            * self.LARGE_ANIMAL_PROTEIN_PER_KG
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

        if not self.ADD_MEAT:
            grain_fed_meat_kcals = np.array([0] * self.NMONTHS)
            grain_fed_meat_fat = np.array([0] * self.NMONTHS)
            grain_fed_meat_protein = np.array([0] * self.NMONTHS)

        return (
            grain_fed_meat_kcals,
            grain_fed_meat_fat,
            grain_fed_meat_protein,
        )

    def calculate_meat_milk_from_human_inedible_feed(self, constants_for_params):
        # monthly in tons milk (present day value)
        MILK_LIMIT_PREWASTE = constants_for_params["TONS_MILK_ANNUAL"] / 12

        # monthly in dry caloric tons inedible feed
        MILK_LIMIT_FEED_USAGE = MILK_LIMIT_PREWASTE * self.INEDIBLE_TO_MILK_CONVERSION
        self.grazing_milk_produced_prewaste = []  # tons
        self.cattle_grazing_maintained_prewaste = []  # tons
        for m in range(self.NMONTHS):
            if self.ADD_MILK:
                max_milk = (
                    self.human_inedible_feed[m] / self.INEDIBLE_TO_MILK_CONVERSION
                )
                if max_milk <= MILK_LIMIT_PREWASTE:
                    self.grazing_milk_produced_prewaste.append(max_milk)
                    self.cattle_grazing_maintained_prewaste.append(0)
                    continue
                self.grazing_milk_produced_prewaste.append(MILK_LIMIT_PREWASTE)
                inedible_for_cattle = (
                    self.human_inedible_feed[m] - MILK_LIMIT_FEED_USAGE
                )
            else:
                self.grazing_milk_produced_prewaste.append(0)
                inedible_for_cattle = self.human_inedible_feed[m]

            if self.ADD_MEAT:
                self.cattle_grazing_maintained_prewaste.append(
                    inedible_for_cattle / self.INEDIBLE_TO_CATTLE_CONVERSION
                )
            else:
                self.cattle_grazing_maintained_prewaste.append(0)

        # assign the resulting remaining limit to milk past inedible sources
        self.grain_fed_milk_limit_prewaste = MILK_LIMIT_PREWASTE - np.array(
            self.grazing_milk_produced_prewaste
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

        if self.ADD_MEAT:

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
                * self.LARGE_ANIMAL_FAT_PER_KG
                / self.LARGE_ANIMAL_KCALS_PER_KG
                / 1e6
            )

            # 1000s tons protein
            cattle_grazing_maintained_protein = (
                cattle_grazing_maintained_kcals
                * 1e9
                * self.LARGE_ANIMAL_PROTEIN_PER_KG
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

    def get_culled_meat_post_waste(
        self, constants_for_params, feed_shutoff_delay_months
    ):

        if constants_for_params["CULL_ANIMALS"]:
            self.CULL_DURATION_MONTHS = constants_for_params["CULL_DURATION_MONTHS"]
            if self.CULL_DURATION_MONTHS != 0:
                meat_culled_prewaste = (
                    [0] * feed_shutoff_delay_months
                    + [self.initial_meat_culled_prewaste / self.CULL_DURATION_MONTHS]
                    * self.CULL_DURATION_MONTHS
                    + [0]
                    * (
                        self.NMONTHS
                        - self.CULL_DURATION_MONTHS
                        - feed_shutoff_delay_months
                    )
                )
            else:
                meat_culled_prewaste = [0] * self.NMONTHS
        else:
            meat_culled_prewaste = [0] * self.NMONTHS
            self.CULL_DURATION_MONTHS = 0

        if not self.ADD_MEAT:
            meat_culled_prewaste = [0] * self.NMONTHS

        if not constants_for_params["CULL_ANIMALS"]:
            assert max(meat_culled_prewaste) == 0

        return np.array(meat_culled_prewaste) * (1 - self.MEAT_WASTE / 100)

    def calculate_animals_culled(self, constants_for_params):
        if constants_for_params["CULL_ANIMALS"]:
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

    def cap_fat_protein_to_amount_used(
        self,
        feed,
        grain_fed_meat_fat,
        grain_fed_meat_protein,
        grain_fed_milk_fat,
        grain_fed_milk_protein,
    ):
        # NOTE: this whole function is poste-waste.
        # Cap the max created by the amount used, as conversion can't be > 1,
        # but the actual conversion only uses kcals
        # Add a little buffer to be safe -- it's probably at best a 90% conversion ratio.

        # TODO: DELETE THIS IF ALL WORKS OUT WITHOUT ERRORS
        # BEST_POSSIBLE_CONVERSION_RATIO = .9
        BEST_POSSIBLE_CONVERSION_RATIO = 1

        assert feed.all_greater_than_or_equal_to_zero()

        return_grain_fed_meat_fat = np.array([])
        return_grain_fed_meat_protein = np.array([])
        return_grain_fed_milk_fat = np.array([])
        return_grain_fed_milk_protein = np.array([])
        for i in range(self.NMONTHS):
            if (
                grain_fed_milk_fat[i] + grain_fed_meat_fat[i]
                > feed.fat[i] * BEST_POSSIBLE_CONVERSION_RATIO
            ):
                print("greater than!")
                print("month")
                print(i)
                print("grain_fed_milk_fat[i] + grain_fed_meat_fat[i]")
                print(grain_fed_milk_fat[i] + grain_fed_meat_fat[i])
                print("feed.fat[i]")
                print(feed.fat[i])
                adjustment_ratio = (
                    BEST_POSSIBLE_CONVERSION_RATIO
                    * feed.fat[i]
                    / (grain_fed_milk_fat[i] + grain_fed_meat_fat[i])
                )
                return_grain_fed_meat_fat = np.append(
                    return_grain_fed_meat_fat, adjustment_ratio * grain_fed_meat_fat[i]
                )
                return_grain_fed_milk_fat = np.append(
                    return_grain_fed_milk_fat, adjustment_ratio * grain_fed_milk_fat[i]
                )
            else:
                return_grain_fed_meat_fat = np.append(
                    return_grain_fed_meat_fat, grain_fed_meat_fat[i]
                )
                return_grain_fed_milk_fat = np.append(
                    return_grain_fed_milk_fat, grain_fed_milk_fat[i]
                )

            if (
                grain_fed_milk_protein[i] + grain_fed_meat_protein[i]
                > BEST_POSSIBLE_CONVERSION_RATIO * feed.protein[i]
            ):
                adjustment_ratio = (
                    BEST_POSSIBLE_CONVERSION_RATIO
                    * feed.protein[i]
                    / (grain_fed_milk_protein[i] + grain_fed_meat_protein[i])
                )
                return_grain_fed_meat_protein = np.append(
                    return_grain_fed_meat_protein,
                    adjustment_ratio * grain_fed_meat_protein[i],
                )
                return_grain_fed_milk_protein = np.append(
                    return_grain_fed_milk_protein,
                    adjustment_ratio * grain_fed_milk_protein[i],
                )
            else:
                return_grain_fed_meat_protein = np.append(
                    return_grain_fed_meat_protein, grain_fed_meat_protein[i]
                )
                return_grain_fed_milk_protein = np.append(
                    return_grain_fed_milk_protein, grain_fed_milk_protein[i]
                )

        return (
            return_grain_fed_meat_fat,
            return_grain_fed_meat_protein,
            return_grain_fed_milk_fat,
            return_grain_fed_milk_protein,
        )
