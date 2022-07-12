################################# Meat and Dairy ##############################
##                                                                            #
##       Functions and constants relating to meat and dairy production        #
##                                                                            #
###############################################################################

import numpy as np


class MeatAndDairy:
    def __init__(self, inputs_to_optimizer):

        # time from slaughter livestock to it turning into food
        # not functional yet

        self.KG_TO_1000_TONS = 1 / (1e6)
        self.ADD_DAIRY = inputs_to_optimizer["ADD_DAIRY"]

        # we use this spreadsheeet https://docs.google.com/spreadsheets/d / 1ZyDrGI84TwhXj_QNicwjj9EPWLJ-r3xnAYMzKSAfWc0/edit#gid=824870019
        self.NMONTHS = inputs_to_optimizer["NMONTHS"]
        # edible meat, organs, and fat added
        self.MEAT_WASTE = inputs_to_optimizer["WASTE"]["MEAT"]
        self.DAIRY_WASTE = inputs_to_optimizer["WASTE"]["DAIRY"]
        self.ADD_MEAT = inputs_to_optimizer["ADD_MEAT"]
        self.KG_PER_SMALL_ANIMAL = 2.36
        self.KG_PER_MEDIUM_ANIMAL = 24.6
        self.KG_PER_LARGE_ANIMAL = 269.7

        self.LARGE_ANIMAL_KCALS_PER_KG = 2750
        self.LARGE_ANIMAL_FAT_PER_KG = 0.182
        self.LARGE_ANIMAL_PROTEIN_PER_KG = 0.257

        self.SMALL_ANIMAL_KCALS_PER_KG = 1525
        self.SMALL_ANIMAL_FAT_PER_KG = 0.076
        self.SMALL_ANIMAL_PROTEIN_PER_KG = 0.196

        # https://docs.google.com/spreadsheets/d / 1tLFHJpXTStxyfNojP_Wrj0MQowfyKujJUA37ZG1q6pk/edit#gid=300573673
        # this one uses pigs from FAOstat, unlike the other two
        # roww 264, "Nutrition Data From FAOstat" tab
        self.MEDIUM_ANIMAL_KCALS_PER_KG = 3590
        self.MEDIUM_ANIMAL_FAT_PER_KG = 0.34
        self.MEDIUM_ANIMAL_PROTEIN_PER_KG = 0.11

        # DAIRY_PRODUCTION = inputs_to_optimizer['DAIRY_PRODUCTION']
        # DAIRY_WASTE = inputs_to_optimizer['WASTE']['DAIRY']
        # billions of kcals
        # MILK_KCALS_PER_1000_CATTLE_PER_MONTH = ANNUAL_LITERS_PER_COW \
        #     * KCALS_PER_LITER \
        #     / 12 \
        #     / 1e9 \
        #     * 1000 \
        #     * DAIRY_PRODUCTION \
        #     * (1 - DAIRY_WASTE / 100)

        # MILK_KCALS_PER_1000_CATTLE_PER_MONTH = 0.0369 / (1 / 1000 * 1e9 / 4e6) *  (1 - DAIRY_WASTE / 100)
        # https://docs.google.com/spreadsheets/d / 1 - upBP5-iPtBzyjm5zbeGlfuE4FwqLUyR/edit#gid=2007828143
        # per kg, whole milk, per nutrition calculator
        self.MILK_KCALS = 610  # kcals per kg
        self.MILK_FAT = 0.032  # kg per kg
        self.MILK_PROTEIN = 0.033  # kg per kg

        ######## Human Inedible Produced Primary Dairy and Cattle Meat #########
        # 'integrated model 150 tg' tab https://docs.google.com/spreadsheets/d / 1rYcxSe-Z7ztvW-QwTBXT8GABaRmVdDuQ05HXmTHbQ8I/edit#gid=1141282747
        self.human_inedible_feed = inputs_to_optimizer["HUMAN_INEDIBLE_FEED"]

        # dry caloric ton feed/ton milk
        self.INEDIBLE_TO_DAIRY_CONVERSION = 1.44

        # dry caloric ton feed/ton cattle
        # INEDIBLE_TO_CATTLE_CONVERSION = 103.0
        self.INEDIBLE_TO_CATTLE_CONVERSION = 92.6

        # tons meat per month
        self.CHICKEN_AND_PORK_LIMIT = (
            inputs_to_optimizer["TONS_CHICKEN_AND_PORK_ANNUAL"] / 12
        )
        self.TONS_BEEF_MONTHLY_BASELINE = (
            inputs_to_optimizer["TONS_BEEF_ANNUAL"] / 12
        )  # tons a month meat

        INITIAL_MILK_CATTLE = inputs_to_optimizer["INITIAL_MILK_CATTLE"]
        self.INIT_SMALL_ANIMALS = inputs_to_optimizer["INIT_SMALL_ANIMALS"]
        self.INIT_MEDIUM_ANIMALS = inputs_to_optimizer["INIT_MEDIUM_ANIMALS"]

        self.INIT_LARGE_ANIMALS = (
            inputs_to_optimizer["INIT_LARGE_ANIMALS_WITH_MILK_COWS"]
            - INITIAL_MILK_CATTLE
        )

    def calculate_meat_nutrition(self):
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

        INIT_MEAT_KCALS = (
            self.INIT_SMALL_ANIMALS_CULLED * KCALS_PER_SMALL_ANIMAL
            + self.INIT_MEDIUM_ANIMALS_CULLED * KCALS_PER_MEDIUM_ANIMAL
            + self.INIT_LARGE_ANIMALS_CULLED * KCALS_PER_LARGE_ANIMAL
        )
        INIT_MEAT_FAT = (
            self.INIT_SMALL_ANIMALS_CULLED * FAT_PER_SMALL_ANIMAL
            + self.INIT_MEDIUM_ANIMALS_CULLED * FAT_PER_MEDIUM_ANIMAL
            + self.INIT_LARGE_ANIMALS_CULLED * FAT_PER_LARGE_ANIMAL
        )
        INIT_MEAT_PROTEIN = (
            self.INIT_SMALL_ANIMALS_CULLED * PROTEIN_PER_SMALL_ANIMAL
            + self.INIT_MEDIUM_ANIMALS_CULLED * PROTEIN_MEDIUM_ANIMAL
            + self.INIT_LARGE_ANIMALS_CULLED * PROTEIN_PER_LARGE_ANIMAL
        )

        self.INITIAL_MEAT = INIT_MEAT_KCALS * (1 - self.MEAT_WASTE / 100)

        if self.INITIAL_MEAT > 0:
            self.MEAT_FRACTION_FAT = INIT_MEAT_FAT / INIT_MEAT_KCALS
            self.MEAT_FRACTION_PROTEIN = INIT_MEAT_PROTEIN / INIT_MEAT_KCALS
        else:
            self.MEAT_FRACTION_FAT = 0
            self.MEAT_FRACTION_PROTEIN = 0

    # https://docs.google.com/document/d / 1HlML7ptYmRfNJjko5qMfIJJGyLRUBlnCIiEiBMr41cM/edit#heading=h.7wiajnpimw8t
    def calculate_meat_and_dairy_from_excess(self, kcals_fed_to_animals):

        # each unit of excess kcals (with associated fat and protein)
        # are fed first to dairy, then to pigs and chickens, then to cattle

        excess_dry_cal_tons = kcals_fed_to_animals * 1e9 / 4e6
        if np.array(excess_dry_cal_tons < 0).any():
            print("excess_dry_cal_tons per month")
            print(excess_dry_cal_tons)
            print(
                "It appears assigning excess calories to feed or biofuels was attempted, but there were not enough calories to use for the feed and biofuel (because of this, excess was calculated as being negative). \nTry to rerun where the population fed after waste incorporating delayed shutoff to feed in biofuels is above the assigned global population. \nQuitting."
            )
            quit()
        assert np.array(excess_dry_cal_tons >= 0).all()

        # dry caloric ton excess/ton milk
        EDIBLE_TO_DAIRY_CONVERSION = 0.7

        h_e_fed_dairy_limit_food_usage = (
            self.h_e_fed_dairy_limit * EDIBLE_TO_DAIRY_CONVERSION
        )

        # dry caloric ton excess/ton meat
        CHICKEN_PORK_CONVERSION = 4.8

        # monthly in dry caloric tons inedible feed
        CHICKEN_PORK_LIMIT_FOOD_USAGE = (
            self.CHICKEN_AND_PORK_LIMIT * CHICKEN_PORK_CONVERSION
        )

        # dry caloric ton excess/ton meat
        EDIBLE_TO_CATTLE_CONVERSION = 9.8
        h_e_fed_dairy_produced = []
        chicken_pork_maintained = []
        cattle_h_e_maintained = []
        for m in range(0, self.NMONTHS):

            max_dairy = excess_dry_cal_tons[m] / EDIBLE_TO_DAIRY_CONVERSION

            if self.ADD_DAIRY:

                if max_dairy <= self.h_e_fed_dairy_limit[m]:
                    # tons per month dairy
                    h_e_fed_dairy_produced.append(max_dairy)
                    # tons per month meat
                    chicken_pork_maintained.append(0)
                    cattle_h_e_maintained.append(0)
                    continue

                h_e_fed_dairy_produced.append(self.h_e_fed_dairy_limit[m])

                limit_dairy = h_e_fed_dairy_limit_food_usage[m]
            else:
                limit_dairy = 0
                h_e_fed_dairy_produced.append(0)

            for_chicken_pork_cattle = excess_dry_cal_tons[m] - limit_dairy

            assert for_chicken_pork_cattle >= 0

            max_chicken_pork = for_chicken_pork_cattle / CHICKEN_PORK_CONVERSION

            if max_chicken_pork <= self.CHICKEN_AND_PORK_LIMIT:
                # tons per month meat
                chicken_pork_maintained.append(max_chicken_pork)
                # tons per month meat
                cattle_h_e_maintained.append(0)
                continue
            # tons per month meat
            chicken_pork_maintained.append(self.CHICKEN_AND_PORK_LIMIT)
            for_cattle = for_chicken_pork_cattle - CHICKEN_PORK_LIMIT_FOOD_USAGE

            # tons per month meat
            cattle_h_e_maintained.append(for_cattle / EDIBLE_TO_CATTLE_CONVERSION)
            # cattle_h_e_maintained.append(0)

        # assert((ratio_maintained_chicken_pork <= 1).all())
        assert (np.array(h_e_fed_dairy_produced) >= 0).all()

        if not self.ADD_DAIRY:
            h_e_fed_dairy_produced = np.array([0] * self.NMONTHS)

        self.h_e_fed_dairy_produced = h_e_fed_dairy_produced
        self.cattle_h_e_maintained = cattle_h_e_maintained
        self.chicken_pork_maintained = chicken_pork_maintained

    def get_meat_from_human_edible_feed(self):

        present_day_tons_per_month_cattle = self.TONS_BEEF_MONTHLY_BASELINE
        present_day_tons_per_month_chicken_pork = (
            self.CHICKEN_AND_PORK_LIMIT
        )  # tons a month

        # does not consider waste
        ratio_maintained_cattle = (
            np.array(self.cattle_maintained) + np.array(self.cattle_h_e_maintained)
        ) / present_day_tons_per_month_cattle
        self.ratio_not_maintained_cattle = 1 - ratio_maintained_cattle

        # make sure for the months we really care about we're not exceeding present-day cattle meat maintained production
        # assert((ratio_maintained_cattle <= 1)[0:47].all())
        if (ratio_maintained_cattle[0:47] >= 1).any():
            print("")
            print(
                "WARNING: cattle maintained is exceeding 2020 baseline levels in months:"
            )
            print(np.where(ratio_maintained_cattle[0:47] >= 1))
            print(
                "Consider whether the predicted amount of human edible feed fed to animals is reasonable."
            )
            print("")

        self.ratio_not_maintained_cattle[self.ratio_not_maintained_cattle < 0] = 0

        # does not consider waste
        self.ratio_maintained_chicken_pork = (
            np.array(self.chicken_pork_maintained)
            / present_day_tons_per_month_chicken_pork
        )
        if not (self.ratio_maintained_chicken_pork <= 1).all():
            print("DIRE, DIRE WARNING!!")
            print("DIRE, DIRE WARNING!!")
            print("DIRE, DIRE WARNING!!")
            print("DIRE, DIRE WARNING!!")
            print("DIRE, DIRE WARNING!!")
            print("DIRE, DIRE WARNING!!")
            print("DIRE, DIRE WARNING!!")
            print("DIRE, DIRE WARNING!!")
            print("DIRE, DIRE WARNING!!")
            print("DIRE, DIRE WARNING!!")
            print("DIRE, DIRE WARNING!!")
            print("DIRE, DIRE WARNING!!")
            print("DIRE, DIRE WARNING!!")
            print("DIRE, DIRE WARNING!!")
            print("DIRE, DIRE WARNING!!")
            print("DIRE, DIRE WARNING!!")
            print("DIRE, DIRE WARNING!!")
            print("DIRE, DIRE WARNING!!")
            print("DIRE, DIRE WARNING!!")
            print("DIRE, DIRE WARNING!!")
            print("DIRE, DIRE WARNING!!")
            print("DIRE, DIRE WARNING!!")
            print("DIRE, DIRE WARNING!!")
            print("DIRE, DIRE WARNING!!")
            print("DIRE, DIRE WARNING!!")
            print("DIRE, DIRE WARNING!!")
            print("DIRE, DIRE WARNING!!")
            # quit()

        # limit the rate of livestock culling by how long it takes to reduce the maintained livestock to its minimum.

        # chicken pork assumed to maintain ratio between medium and small animal mass
        small_to_medium_ratio = (
            self.INIT_SMALL_ANIMALS
            * self.KG_PER_SMALL_ANIMAL
            / (
                self.INIT_MEDIUM_ANIMALS * self.KG_PER_MEDIUM_ANIMAL
                + self.INIT_SMALL_ANIMALS * self.KG_PER_SMALL_ANIMAL
            )
        )

        # billions kcals monthly
        self.chicken_pork_kcals = (
            np.array(self.chicken_pork_maintained)
            * 1e3
            * (
                self.SMALL_ANIMAL_KCALS_PER_KG * small_to_medium_ratio
                + self.MEDIUM_ANIMAL_KCALS_PER_KG * (1 - small_to_medium_ratio)
            )
            / 1e9
        )

        # thousands tons monthly
        self.chicken_pork_fat = (
            np.array(self.chicken_pork_maintained)
            * 1e3
            * (
                self.SMALL_ANIMAL_FAT_PER_KG * small_to_medium_ratio
                + self.MEDIUM_ANIMAL_FAT_PER_KG * (1 - small_to_medium_ratio)
            )
            / 1e6
        )

        # thousands tons monthly
        self.chicken_pork_protein = (
            np.array(self.chicken_pork_maintained)
            * 1e3
            * (
                self.SMALL_ANIMAL_PROTEIN_PER_KG * small_to_medium_ratio
                + self.MEDIUM_ANIMAL_PROTEIN_PER_KG * (1 - small_to_medium_ratio)
            )
            / 1e6
        )

        # billions kcals monthly
        cattle_h_e_maintained_kcals = (
            np.array(self.cattle_h_e_maintained)
            * 1000
            * self.LARGE_ANIMAL_KCALS_PER_KG
            / 1e9
        )

        # 1000s tons fat
        cattle_h_e_maintained_fat = (
            cattle_h_e_maintained_kcals
            * 1e9
            / self.LARGE_ANIMAL_KCALS_PER_KG
            * self.LARGE_ANIMAL_FAT_PER_KG
            / 1e6
        )

        # 1000s tons protein
        cattle_h_e_maintained_protein = (
            cattle_h_e_maintained_kcals
            * 1e9
            / self.LARGE_ANIMAL_KCALS_PER_KG
            * self.LARGE_ANIMAL_PROTEIN_PER_KG
            / 1e6
        )

        h_e_meat_kcals = np.array(
            cattle_h_e_maintained_kcals + self.chicken_pork_kcals
        ) * (1 - self.MEAT_WASTE / 100)
        h_e_meat_fat = np.array(cattle_h_e_maintained_fat + self.chicken_pork_fat) * (
            1 - self.MEAT_WASTE / 100
        )
        h_e_meat_protein = np.array(
            cattle_h_e_maintained_protein + self.chicken_pork_protein
        ) * (1 - self.MEAT_WASTE / 100)

        if not self.ADD_MEAT:
            h_e_meat_kcals = np.array([0] * self.NMONTHS)
            h_e_meat_fat = np.array([0] * self.NMONTHS)
            h_e_meat_protein = np.array([0] * self.NMONTHS)

        return (
            self.chicken_pork_kcals,
            self.chicken_pork_fat,
            self.chicken_pork_protein,
            h_e_meat_kcals,
            h_e_meat_fat,
            h_e_meat_protein,
        )

    def calculate_meat_dairy_from_human_inedible_feed(self, inputs_to_optimizer):

        # monthly in tons milk (present day value)
        DAIRY_LIMIT = inputs_to_optimizer["TONS_DAIRY_ANNUAL"] / 12
        # CHICKEN_PORK_LIMIT = 250e6 / 12

        # monthly in dry caloric tons inedible feed
        DAIRY_LIMIT_FEED_USAGE = DAIRY_LIMIT * self.INEDIBLE_TO_DAIRY_CONVERSION

        self.dairy_milk_produced = []  # tons
        self.cattle_maintained = []  # tons
        for m in range(0, self.NMONTHS):
            if self.ADD_DAIRY:
                max_dairy = (
                    self.human_inedible_feed[m] / self.INEDIBLE_TO_DAIRY_CONVERSION
                )
                if max_dairy <= DAIRY_LIMIT:
                    self.dairy_milk_produced.append(max_dairy)
                    self.cattle_maintained.append(0)
                    continue
                self.dairy_milk_produced.append(DAIRY_LIMIT)
                inedible_for_cattle = (
                    self.human_inedible_feed[m] - DAIRY_LIMIT_FEED_USAGE
                )
            else:
                self.dairy_milk_produced.append(0)
                inedible_for_cattle = self.human_inedible_feed[m]

            if self.ADD_MEAT:
                self.cattle_maintained.append(
                    inedible_for_cattle / self.INEDIBLE_TO_CATTLE_CONVERSION
                )
            else:
                self.cattle_maintained.append(0)

        self.h_e_fed_dairy_limit = DAIRY_LIMIT - np.array(self.dairy_milk_produced)

    def get_dairy_produced(self):
        # billions kcals
        dairy_milk_kcals = (
            np.array(self.dairy_milk_produced)
            * 1e3
            * self.MILK_KCALS
            / 1e9
            * (1 - self.DAIRY_WASTE / 100)
        )

        # thousands tons
        dairy_milk_fat = (
            np.array(self.dairy_milk_produced)
            / 1e3
            * self.MILK_FAT
            * (1 - self.DAIRY_WASTE / 100)
        )

        # thousands tons
        dairy_milk_protein = (
            np.array(self.dairy_milk_produced)
            / 1e3
            * self.MILK_PROTEIN
            * (1 - self.DAIRY_WASTE / 100)
        )

        return (dairy_milk_kcals, dairy_milk_fat, dairy_milk_protein)

    def get_cattle_maintained(self):

        if self.ADD_MEAT:

            # billions kcals
            cattle_maintained_kcals = (
                np.array(self.cattle_maintained)
                * 1000
                * self.LARGE_ANIMAL_KCALS_PER_KG
                / 1e9
                * (1 - self.MEAT_WASTE / 100)
            )

            # 1000s tons fat
            cattle_maintained_fat = (
                cattle_maintained_kcals
                * 1e9
                * self.LARGE_ANIMAL_FAT_PER_KG
                / self.LARGE_ANIMAL_KCALS_PER_KG
                / 1e6
            )

            # 1000s tons protein
            cattle_maintained_protein = (
                cattle_maintained_kcals
                * 1e9
                * self.LARGE_ANIMAL_PROTEIN_PER_KG
                / self.LARGE_ANIMAL_KCALS_PER_KG
                / 1e6
            )

        else:
            cattle_maintained_kcals = [0] * len(self.cattle_maintained)
            cattle_maintained_fat = [0] * len(self.cattle_maintained)
            cattle_maintained_protein = [0] * len(self.cattle_maintained)

        return (
            cattle_maintained_kcals,
            cattle_maintained_fat,
            cattle_maintained_protein,
        )

    def get_excess(self, inputs_to_optimizer, biofuels, feed):
        ###### Human Edible Produced "Secondary" Dairy and Cattle Meat #######

        # assume animals need and use human levels of fat and protein per kcal
        # units grams per kcal same as units 1000s tons per billion kcals
        fat_used_ls = (
            inputs_to_optimizer["NUTRITION"]["FAT_DAILY"]
            / inputs_to_optimizer["NUTRITION"]["KCALS_DAILY"]
        )

        protein_used_ls = (
            inputs_to_optimizer["NUTRITION"]["PROTEIN_DAILY"]
            / inputs_to_optimizer["NUTRITION"]["KCALS_DAILY"]
        )

        nonshutoff_excess_fat_used = (
            fat_used_ls * inputs_to_optimizer["EXCESS_CALORIES"]
        )

        nonshutoff_excess_protein_used = (
            protein_used_ls * inputs_to_optimizer["EXCESS_CALORIES"]
        )

        # totals human edible used for animal feed and biofuels
        # excess is directly supplied separately from the feed_shutoff used.

        self.excess_kcals = (
            inputs_to_optimizer["EXCESS_CALORIES"]
            + biofuels.biofuels_kcals
            + feed.feed_shutoff_kcals
        )

        self.excess_fat_used = (
            nonshutoff_excess_fat_used + biofuels.biofuels_fat + feed.feed_shutoff_fat
        )

        self.excess_protein_used = (
            nonshutoff_excess_protein_used
            + biofuels.biofuels_protein
            + feed.feed_shutoff_protein
        )

        return (self.excess_kcals, self.excess_fat_used, self.excess_protein_used)

    def get_culled_meat(self, inputs_to_optimizer, feed_shutoff_delay_months):

        if inputs_to_optimizer["CULL_ANIMALS"]:
            self.CULL_DURATION_MONTHS = inputs_to_optimizer["CULL_DURATION_MONTHS"]
            if self.CULL_DURATION_MONTHS != 0:
                meat_culled = (
                    [0] * feed_shutoff_delay_months
                    + [self.INITIAL_MEAT / self.CULL_DURATION_MONTHS]
                    * self.CULL_DURATION_MONTHS
                    + [0]
                    * (
                        self.NMONTHS
                        - self.CULL_DURATION_MONTHS
                        - feed_shutoff_delay_months
                    )
                )
            else:
                meat_culled = [0] * self.NMONTHS
        else:
            meat_culled = [0] * self.NMONTHS
            self.CULL_DURATION_MONTHS = 0

        if not self.ADD_MEAT:
            meat_culled = [0] * self.NMONTHS

        if not inputs_to_optimizer["CULL_ANIMALS"]:
            assert max(meat_culled) == 0

        return meat_culled

    def calculate_animals_culled(self, inputs_to_optimizer):
        if inputs_to_optimizer["CULL_ANIMALS"]:
            self.INIT_SMALL_ANIMALS_CULLED = self.INIT_SMALL_ANIMALS * (
                1 - np.min(self.ratio_maintained_chicken_pork)
            )
            self.INIT_MEDIUM_ANIMALS_CULLED = self.INIT_MEDIUM_ANIMALS * (
                1 - np.min(self.ratio_maintained_chicken_pork)
            )
            self.INIT_LARGE_ANIMALS_CULLED = self.INIT_LARGE_ANIMALS * np.max(
                self.ratio_not_maintained_cattle
            )
        else:
            self.INIT_SMALL_ANIMALS_CULLED = 0
            self.INIT_MEDIUM_ANIMALS_CULLED = 0
            self.INIT_LARGE_ANIMALS_CULLED = 0

    def get_dairy_from_human_edible_feed(self, inputs_to_optimizer):

        if self.ADD_DAIRY:

            h_e_milk_kcals = (
                np.array(self.h_e_fed_dairy_produced)
                * 1e3
                * self.MILK_KCALS
                / 1e9
                * (1 - self.DAIRY_WASTE / 100)
            )

            h_e_milk_fat = (
                np.array(self.h_e_fed_dairy_produced)
                / 1e3
                * self.MILK_FAT
                * (1 - self.DAIRY_WASTE / 100)
            )

            h_e_milk_protein = (
                np.array(self.h_e_fed_dairy_produced)
                / 1e3
                * self.MILK_PROTEIN
                * (1 - self.DAIRY_WASTE / 100)
            )

        else:

            h_e_milk_kcals = np.array([0] * self.NMONTHS)
            h_e_milk_fat = np.array([0] * self.NMONTHS)
            h_e_milk_protein = np.array([0] * self.NMONTHS)

        return (h_e_milk_kcals, h_e_milk_fat, h_e_milk_protein)
