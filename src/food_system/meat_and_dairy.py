"""
################################# Meat and Dairy ##############################
##                                                                            #
##       Functions and constants relating to meat and milk production        #
##                                                                            #
###############################################################################
"""
from src.food_system.food import Food
import numpy as np


class MeatAndDairy:
    def __init__(self, constants_for_params):
        """
        Initializes the MeatAndDairy class with constants for parameters.

        Args:
            constants_for_params (dict): A dictionary containing constants for parameters.

        Constants:
            KG_TO_1000_TONS (float): Conversion factor from kilograms to 1000 tons.
            ADD_MILK (bool): Whether to add milk or not.
            NMONTHS (int): Number of months.
            ADD_MAINTAINED_MEAT (float): Edible meat, organs, and fat added for maintenance.
            ADD_CULLED_MEAT (float): Edible meat, organs, and fat added for culling.
            KG_PER_SMALL_ANIMAL (float): Kilograms per small animal.
            KG_PER_MEDIUM_ANIMAL (float): Kilograms per medium animal.
            KG_PER_LARGE_ANIMAL (float): Kilograms per large animal.
            LARGE_ANIMAL_KCALS_PER_KG (int): Kilocalories per kilogram for large animals.
            LARGE_ANIMAL_FAT_RATIO (float): Fat ratio for large animals.
            LARGE_ANIMAL_PROTEIN_RATIO (float): Protein ratio for large animals.
            SMALL_ANIMAL_KCALS_PER_KG (int): Kilocalories per kilogram for small animals.
            SMALL_ANIMAL_FAT_RATIO (float): Fat ratio for small animals.
            SMALL_ANIMAL_PROTEIN_RATIO (float): Protein ratio for small animals.
            MEDIUM_ANIMAL_KCALS_PER_KG (int): Kilocalories per kilogram for medium animals.
            MEDIUM_ANIMAL_FAT_RATIO (float): Fat ratio for medium animals.
            MEDIUM_ANIMAL_PROTEIN_RATIO (float): Protein ratio for medium animals.
            MILK_KCALS (int): Kilocalories per kilogram of whole milk.
            MILK_FAT (float): Fat content per kilogram of whole milk.
            MILK_PROTEIN (float): Protein content per kilogram of whole milk.
            human_inedible_feed (numpy.ndarray): Array of human inedible feed.
            ratio_human_inedible_feed (numpy.ndarray): Array of ratios of human inedible feed.
            INEDIBLE_TO_MILK_CONVERSION (float): Conversion factor from inedible feed to milk.
            EDIBLE_TO_MILK_CONVERSION (float): Conversion factor from edible feed to milk.
            EDIBLE_TO_CHICKEN_PORK_CONVERSION (float): Conversion factor from edible feed to chicken or pork meat.
            EDIBLE_TO_CATTLE_CONVERSION (float): Conversion factor from edible feed to cattle meat.
            INEDIBLE_TO_CATTLE_CONVERSION (float): Conversion factor from inedible feed to cattle.
            MILK_LIMIT_PREWASTE (float): Monthly limit of milk production before waste.
            MILK_LIMIT_FEED_USAGE (float): Monthly limit of feed usage for milk production.
            CHICKEN_AND_PORK_LIMIT_PREWASTE (float): Monthly limit of chicken and pork meat production before waste.
            TONS_BEEF_MONTHLY_BASELINE_PREWASTE (float): Monthly baseline limit of beef meat production before waste.
            INITIAL_MILK_CATTLE (float): Initial milk cattle.
            INIT_SMALL_ANIMALS (float): Initial small animals.
            INIT_MEDIUM_ANIMALS (float): Initial medium animals.
            INIT_LARGE_ANIMALS (float): Initial large animals.

        Returns:
            None
        """
        self.KG_TO_1000_TONS = 1 / (1e6)
        self.ADD_MILK = constants_for_params["ADD_MILK"]
        self.NMONTHS = constants_for_params["NMONTHS"]
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
        self.MEDIUM_ANIMAL_KCALS_PER_KG = 3590
        self.MEDIUM_ANIMAL_FAT_RATIO = 0.34
        self.MEDIUM_ANIMAL_PROTEIN_RATIO = 0.11
        self.MILK_KCALS = 610
        self.MILK_FAT = 0.032
        self.MILK_PROTEIN = 0.033
        human_inedible_feed_dry_caloric_tons_list = np.array([])
        self.ratio_human_inedible_feed = np.array([])
        for i in range(1, int(self.NMONTHS / 12) + 1):
            ratio_human_inedible_feed = constants_for_params[
                "RATIO_GRASSES_YEAR" + str(i)
            ]
            self.ratio_human_inedible_feed = np.append(
                self.ratio_human_inedible_feed, [ratio_human_inedible_feed] * 12
            )
            assert (
                0 <= ratio_human_inedible_feed <= 10000
            ), "Error: Unreasonable ratio of grass production"
            human_inedible_feed_dry_caloric_tons_list = np.append(
                human_inedible_feed_dry_caloric_tons_list,
                [
                    ratio_human_inedible_feed
                    * constants_for_params["HUMAN_INEDIBLE_FEED_BASELINE_MONTHLY"]
                ]
                * 12,
            )

        human_inedible_feed_dry_caloric_tons = Food(
            kcals=human_inedible_feed_dry_caloric_tons_list,
            fat=np.zeros(len(human_inedible_feed_dry_caloric_tons_list)),
            protein=np.zeros(len(human_inedible_feed_dry_caloric_tons_list)),
            kcals_units="million dry caloric tons each month",
            fat_units="million tons each month",
            protein_units="million tons each month",
        )

        self.human_inedible_feed = (
            human_inedible_feed_dry_caloric_tons.in_units_bil_kcals_thou_tons_thou_tons_per_month()
        )

        self.INEDIBLE_TO_MILK_CONVERSION = 1.44
        self.EDIBLE_TO_MILK_CONVERSION = 0.7
        self.EDIBLE_TO_CHICKEN_PORK_CONVERSION = 4.8
        self.EDIBLE_TO_CATTLE_CONVERSION = 9.8
        self.INEDIBLE_TO_CATTLE_CONVERSION = 92.6
        self.MILK_LIMIT_PREWASTE = constants_for_params["TONS_MILK_ANNUAL"] / 12
        self.MILK_LIMIT_FEED_USAGE = (
            self.MILK_LIMIT_PREWASTE * self.INEDIBLE_TO_MILK_CONVERSION
        )
        self.CHICKEN_AND_PORK_LIMIT_PREWASTE = (
            constants_for_params["TONS_CHICKEN_AND_PORK_ANNUAL"] / 12
        )
        self.TONS_BEEF_MONTHLY_BASELINE_PREWASTE = (
            constants_for_params["TONS_BEEF_ANNUAL"] / 12
        )
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
        """
        Calculates the nutritional values of meat products based on animal ratios and
        nutritional ratios of small, medium, and large animals.

        Args:
            self: instance of the class

        Returns:
            None

        """
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

        # calculate dry caloric tons per ton of chicken and pork
        self.dry_caloric_tons_per_ton_chicken_pork = (
            (
                self.SMALL_ANIMAL_KCALS_PER_KG * small_to_medium_ratio
                + self.MEDIUM_ANIMAL_KCALS_PER_KG * (1 - small_to_medium_ratio)
            )  # now units kcals per kg meat
            * 1000  # now units kcals per ton meat
            / 4e6  # now units dry caloric tons per ton meat
        )

        # calculate dry caloric tons per ton of beef
        self.dry_caloric_tons_per_ton_beef = self.LARGE_ANIMAL_KCALS_PER_KG * 1000 / 4e6

        # calculate thousand tons of fat per ton of chicken and pork
        self.thousand_tons_fat_per_ton_chicken_pork = (
            self.SMALL_ANIMAL_FAT_RATIO * small_to_medium_ratio
            + self.MEDIUM_ANIMAL_FAT_RATIO * (1 - small_to_medium_ratio)
        ) / 1000  # now units thousand tons fat per ton meat

        # calculate thousand tons of protein per ton of chicken and pork
        self.thousand_tons_protein_per_ton_chicken_pork = (
            self.SMALL_ANIMAL_PROTEIN_RATIO * small_to_medium_ratio
            + self.MEDIUM_ANIMAL_PROTEIN_RATIO * (1 - small_to_medium_ratio)
        ) / 1000  # now units thousand tons protein per ton meat

        # calculate monthly food usage limit for chicken and pork in dry caloric tons
        self.CHICKEN_PORK_LIMIT_FOOD_USAGE_PREWASTE = (
            self.CHICKEN_AND_PORK_LIMIT_PREWASTE
            * self.dry_caloric_tons_per_ton_chicken_pork
        )

        # calculate monthly food usage limit for beef in dry caloric tons
        self.BEEF_LIMIT_FOOD_USAGE_PREWASTE = (
            self.TONS_BEEF_MONTHLY_BASELINE_PREWASTE
            * self.dry_caloric_tons_per_ton_beef
        )

    def get_meat_nutrition(self):
        """
        Returns a tuple containing nutritional information for different sizes of animals.

        Returns:
            tuple: A tuple containing the following nutritional information:
                - KG_PER_SMALL_ANIMAL (float): The weight of meat in kilograms for a small animal.
                - KG_PER_MEDIUM_ANIMAL (float): The weight of meat in kilograms for a medium animal.
                - KG_PER_LARGE_ANIMAL (float): The weight of meat in kilograms for a large animal.
                - LARGE_ANIMAL_KCALS_PER_KG (float): The number of kilocalories per kilogram of meat for a large animal.
                - LARGE_ANIMAL_FAT_RATIO (float): The ratio of fat to meat for a large animal.
                - LARGE_ANIMAL_PROTEIN_RATIO (float): The ratio of protein to meat for a large animal.
                - MEDIUM_ANIMAL_KCALS_PER_KG (float): The number of kilocalories per kilogram of meat for a medium animal.
                - SMALL_ANIMAL_KCALS_PER_KG (float): The number of kilocalories per kilogram of meat for a small animal.
        """
        return (
            self.KG_PER_SMALL_ANIMAL,
            self.KG_PER_MEDIUM_ANIMAL,
            self.KG_PER_LARGE_ANIMAL,
            self.LARGE_ANIMAL_KCALS_PER_KG,
            self.LARGE_ANIMAL_FAT_RATIO,
            self.LARGE_ANIMAL_PROTEIN_RATIO,
            self.MEDIUM_ANIMAL_KCALS_PER_KG,
            self.SMALL_ANIMAL_KCALS_PER_KG,
        )

    def calculate_meat_limits(
        self, MAX_RATIO_CULLED_SLAUGHTER_TO_BASELINE, culled_meat_initial
    ):
        """
        Calculate the baseline levels of meat production, indicating slaughter capacity.

        There's no limit on the actual amount eaten, but the amount produced and
        then preserved after culling is assumed to be some multiple of current slaughter
        capacity. This just means that the limit each month on the amount that could be eaten is
        the sum of the max estimated slaughter capacity each month.

        Args:
            MAX_RATIO_CULLED_SLAUGHTER_TO_BASELINE (float): The maximum ratio of culled meat to baseline meat.
            culled_meat_initial (float): The initial amount of culled meat.

        Returns:
            numpy.ndarray: An array of cumulative meat limits for each month.

        """

        # Calculate the increase in meat production per month in billions of kcals
        per_month_increase = (
            self.CHICKEN_PORK_LIMIT_FOOD_USAGE_PREWASTE * 4e6 / 1e9
            + self.BEEF_LIMIT_FOOD_USAGE_PREWASTE * 4e6 / 1e9
        )

        meat_limit = 0
        cumulative_meat_limit = np.zeros(self.NMONTHS)
        for m in range(0, self.NMONTHS):
            # Calculate the meat limit for the current month
            meat_limit = (
                meat_limit + per_month_increase * MAX_RATIO_CULLED_SLAUGHTER_TO_BASELINE
            )

            # Store the minimum of the meat limit and the initial amount of culled meat
            cumulative_meat_limit[m] = min(meat_limit, culled_meat_initial)

        return cumulative_meat_limit

    def calculate_continued_ratios_meat_dairy_grazing(self, constants_for_params):
        """
        Calculates the ratios of grazing meat and milk produced pre-waste based on the
        number of dairy cows and total heads of cattle precatastrophe.

        Args:
            constants_for_params (dict): dictionary of constants used in the simulation

        Returns:
            None

        Raises:
            AssertionError: if the calculated ratios are not between 0 and 1

        """
        # This condition is set in the scenarios file as well. They should both be set
        # to the same value.
        # Setting it to true mimics the Xia et al result, but is less accurate.
        # (if subtracting feed directly from outdoor crops)
        SUBTRACT_FEED_DIRECTLY = False

        if SUBTRACT_FEED_DIRECTLY:
            # If subtracting feed directly from outdoor crops, set the ratios to 0.46
            ratio_grazing_meat = 0.46
            ratio_grazing_milk = 0.46

            # Calculate the amount of milk produced pre-waste
            self.grazing_milk_produced_prewaste = (
                self.MILK_LIMIT_PREWASTE
                * self.ratio_human_inedible_feed
                * ratio_grazing_milk
            )

            # Calculate the amount of cattle grazing maintained pre-waste
            self.cattle_grazing_maintained_prewaste = (
                self.TONS_BEEF_MONTHLY_BASELINE_PREWASTE
                * self.ratio_human_inedible_feed
                * ratio_grazing_meat
            )
        else:
            # If not subtracting feed directly from outdoor crops, calculate the ratios
            # based on the number of dairy cows and total heads of cattle precatastrophe
            heads_dairy_cows = constants_for_params["INITIAL_MILK_CATTLE"]
            # total head count of large sized animals minus milk cows
            total_heads_cattle = constants_for_params[
                "INIT_LARGE_ANIMALS_WITH_MILK_COWS"
            ]

            ratio_grazing_meat = (
                total_heads_cattle - heads_dairy_cows
            ) / total_heads_cattle
            ratio_grazing_milk = 1 - ratio_grazing_meat

            # Check that the calculated ratios are between 0 and 1
            assert 0 <= ratio_grazing_milk <= 1
            assert 0 <= ratio_grazing_meat <= 1

            # Calculate the amount of milk produced pre-waste
            self.grazing_milk_produced_prewaste = (
                ratio_grazing_milk
                * self.human_inedible_feed
                / self.INEDIBLE_TO_MILK_CONVERSION
            )

            # Calculate the amount of cattle grazing maintained pre-waste
            self.cattle_grazing_maintained_prewaste = (
                ratio_grazing_meat
                * self.human_inedible_feed
                / self.INEDIBLE_TO_CATTLE_CONVERSION
            )

    def calculate_continued_ratios_meat_dairy_grain(
        self, fed_to_animals_prewaste, outdoor_crops
    ):
        """
        Calculates the ratios of grain-fed meat, grain-fed milk, and grain-fed chicken/pork
        maintained pre-waste. The ratios are calculated based on the amount of feed used for
        meat cattle and chicken/pork precatastrophe, and the amount of human-edible feed used
        for dairy. The function also calculates the amount of grain-fed milk produced pre-waste,
        the amount of cattle grain-fed maintained pre-waste, and the amount of chicken/pork
        maintained pre-waste.

        Args:
            fed_to_animals_prewaste (class): an instance of the FedToAnimalsPrewaste class
            outdoor_crops (class): an instance of the OutdoorCrops class

        Returns:
            None
        """

        # This condition is set in the scenarios file as well. They should both be set
        # to the same value.
        # Setting it to true mimics the Xia et al result, but is less accurate.
        # (if subtracting feed directly from outdoor crops)
        SUBTRACT_FEED_DIRECTLY = False

        if SUBTRACT_FEED_DIRECTLY:
            # similar assumption as Xia et al paper.

            ratio_grainfed_meat = 0.54
            ratio_grainfed_milk = 0.54

            # Calculate the amount of grain-fed milk produced pre-waste
            self.grain_fed_milk_produced_prewaste = (
                self.MILK_LIMIT_PREWASTE
                * outdoor_crops.all_months_reductions
                * ratio_grainfed_milk
            )

            # Calculate the amount of cattle grain-fed maintained pre-waste
            self.cattle_grain_fed_maintained_prewaste = (
                self.TONS_BEEF_MONTHLY_BASELINE_PREWASTE
                * outdoor_crops.all_months_reductions
                * ratio_grainfed_meat
            )

            # Calculate the amount of chicken/pork maintained pre-waste
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

            # Calculate the amount of cattle grain-fed maintained pre-waste
            self.cattle_grain_fed_maintained_prewaste = (
                excess_dry_cal_tons * ratio_beef_feed / self.EDIBLE_TO_CATTLE_CONVERSION
            )

            # Calculate the amount of chicken/pork maintained pre-waste
            self.chicken_pork_maintained_prewaste = (
                excess_dry_cal_tons
                * ratio_chicken_pork_feed
                / self.EDIBLE_TO_CHICKEN_PORK_CONVERSION
            )

            # Calculate the amount of grain-fed milk produced pre-waste
            self.grain_fed_milk_produced_prewaste = np.array([0] * self.NMONTHS)

    def calculate_meat_and_dairy_from_grain(self, fed_to_animals_prewaste):
        """
        Calculates the amount of meat and dairy that can be produced from excess grain fed to animals.
        The excess grain is first used to produce milk, then to feed pigs and chickens, and finally to feed cattle.

        Args:
            fed_to_animals_prewaste (np.ndarray): array of kcals fed to animals before waste

        Returns:
            None

        Raises:
            AssertionError: if any of the calculated values are negative

        """

        # Calculate the amount of excess dry caloric tons from the fed_to_animals_prewaste array
        excess_dry_cal_tons = fed_to_animals_prewaste.kcals * 1e9 / 4e6

        # Check if any of the calculated values are negative
        if np.array(excess_dry_cal_tons < 0).any():
            print("excess_dry_cal_tons per month")
            print(excess_dry_cal_tons)
            print(
                """It appears assigning excess calories to feed or biofuels was attempted,
                but there were not enough calories to use for the feed and biofuel
                (because of this, excess was calculated as being negative).
                \nTry to rerun where the population fed after waste incorporating
                delayed shutoff to feed in biofuels is above the assigned global
                population.
                \nQuitting."""
            )
            quit()

        # Check if all the calculated values are non-negative
        assert np.array(excess_dry_cal_tons >= 0).all()

        # Calculate the dry caloric ton excess/ton milk
        grain_fed_milk_limit_food_usage_prewaste = (
            self.grain_fed_milk_limit_prewaste * self.EDIBLE_TO_MILK_CONVERSION
        )

        # Initialize empty lists to store the calculated values
        grain_fed_milk_produced_prewaste = []
        chicken_pork_maintained_prewaste = []
        cattle_grain_fed_maintained_prewaste = []

        # Loop through each month to calculate the dry caloric ton excess/ton meat
        for m in range(self.NMONTHS):
            max_milk = excess_dry_cal_tons[m] / self.EDIBLE_TO_MILK_CONVERSION

            # If the ADD_MILK flag is True and the maximum amount of milk that can be produced is less than or equal to the limit, then only milk is produced
            if self.ADD_MILK:
                if max_milk <= self.grain_fed_milk_limit_prewaste[m]:
                    # tons per month milk
                    grain_fed_milk_produced_prewaste.append(max_milk)
                    # tons per month meat
                    chicken_pork_maintained_prewaste.append(0)
                    cattle_grain_fed_maintained_prewaste.append(0)
                    continue

                # If the maximum amount of milk that can be produced is greater than the limit, then the limit is used to produce milk
                grain_fed_milk_produced_prewaste.append(
                    self.grain_fed_milk_limit_prewaste[m]
                )

                limit_milk_prewaste = grain_fed_milk_limit_food_usage_prewaste[m]
            else:
                limit_milk_prewaste = 0
                grain_fed_milk_produced_prewaste.append(0)

            # Calculate the amount of excess grain that can be used to feed chickens, pigs, and cattle
            for_chicken_pork_cattle_prewaste = (
                excess_dry_cal_tons[m] - limit_milk_prewaste
            )

            # Check if the calculated value is non-negative
            assert for_chicken_pork_cattle_prewaste >= 0

            # Calculate the maximum amount of chicken and pork that can be produced
            max_chicken_pork_prewaste = (
                for_chicken_pork_cattle_prewaste
                / self.EDIBLE_TO_CHICKEN_PORK_CONVERSION
            )

            # If the maximum amount of chicken and pork that can be produced is less than or equal to the limit, then only chicken and pork are produced
            if max_chicken_pork_prewaste <= self.CHICKEN_AND_PORK_LIMIT_PREWASTE:
                # tons per month meat
                chicken_pork_maintained_prewaste.append(max_chicken_pork_prewaste)
                # tons per month meat
                cattle_grain_fed_maintained_prewaste.append(0)
                continue

            # If the maximum amount of chicken and pork that can be produced is greater than the limit, then the limit is used to produce chicken and pork
            # and the remaining excess grain is used to produce cattle
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

        # Check if all the calculated values are non-negative
        assert (np.array(grain_fed_milk_produced_prewaste) >= 0).all()

        # If the ADD_MILK flag is False, then no milk is produced
        if not self.ADD_MILK:
            grain_fed_milk_produced_prewaste = np.array([0] * self.NMONTHS)

        # Store the calculated values in the class variables
        self.grain_fed_milk_produced_prewaste = grain_fed_milk_produced_prewaste
        self.cattle_grain_fed_maintained_prewaste = cattle_grain_fed_maintained_prewaste
        self.chicken_pork_maintained_prewaste = chicken_pork_maintained_prewaste

    def calculate_meat_milk_from_human_inedible_feed(self, constants_for_params):
        """
        Calculates the amount of milk and meat that can be produced from human inedible feed.
        Args:
            self: instance of the class
            constants_for_params: dictionary containing constants used in the calculations
        Returns:
            None
        """
        # Initialize empty lists to store the results
        self.grazing_milk_produced_prewaste = []  # tons
        self.cattle_grazing_maintained_prewaste = []  # tons

        # Loop through each month
        for m in range(self.NMONTHS):
            # Calculate the maximum amount of milk that can be produced from the inedible feed
            if self.ADD_MILK:
                max_milk = (
                    self.human_inedible_feed[m] / self.INEDIBLE_TO_MILK_CONVERSION
                )
                # If the maximum amount of milk is less than or equal to the pre-waste limit, add it to the list
                if max_milk <= self.MILK_LIMIT_PREWASTE:
                    self.grazing_milk_produced_prewaste.append(max_milk)
                    self.cattle_grazing_maintained_prewaste.append(0)
                    continue
                # If the maximum amount of milk is greater than the pre-waste limit, add the pre-waste limit to the list
                self.grazing_milk_produced_prewaste.append(self.MILK_LIMIT_PREWASTE)
                # Calculate the amount of inedible feed that can be used for cattle
                inedible_for_cattle = (
                    self.human_inedible_feed[m] - self.MILK_LIMIT_FEED_USAGE
                )
            else:
                # If milk is not being added, set the milk produced to 0
                self.grazing_milk_produced_prewaste.append(0)
                # Use all of the inedible feed for cattle
                inedible_for_cattle = self.human_inedible_feed[m]

            # Calculate the amount of meat that can be produced from the inedible feed
            if self.ADD_MAINTAINED_MEAT:
                self.cattle_grazing_maintained_prewaste.append(
                    inedible_for_cattle / self.INEDIBLE_TO_CATTLE_CONVERSION
                )
            else:
                # If meat is not being added, set the meat produced to 0
                self.cattle_grazing_maintained_prewaste.append(0)

        # Calculate the remaining limit of milk that can be produced from inedible sources
        self.grain_fed_milk_limit_prewaste = self.MILK_LIMIT_PREWASTE - np.array(
            self.grazing_milk_produced_prewaste
        )

    def get_milk_from_human_edible_feed(self, constants_for_params):
        """
        Calculates the amount of milk produced from human-edible feed, taking into account
        the amount of waste produced during the process.

        Args:
            self (object): The object instance
            constants_for_params (dict): A dictionary containing the constants used in the
            calculations

        Returns:
            tuple: A tuple containing the amount of kcals, fat, and protein produced from
            grain-fed milk

        """
        if self.ADD_MILK:
            # Calculate kcals produced from grain-fed milk
            grain_fed_milk_kcals = (
                np.array(self.grain_fed_milk_produced_prewaste)
                * 1e3
                * self.MILK_KCALS
                / 1e9
                * (1 - self.MILK_WASTE / 100)
            )

            # Calculate fat produced from grain-fed milk
            grain_fed_milk_fat = (
                np.array(self.grain_fed_milk_produced_prewaste)
                / 1e3
                * self.MILK_FAT
                * (1 - self.MILK_WASTE / 100)
            )

            # Calculate protein produced from grain-fed milk
            grain_fed_milk_protein = (
                np.array(self.grain_fed_milk_produced_prewaste)
                / 1e3
                * self.MILK_PROTEIN
                * (1 - self.MILK_WASTE / 100)
            )

        else:
            # If no milk is added, set all values to 0
            grain_fed_milk_kcals = np.array([0] * self.NMONTHS)
            grain_fed_milk_fat = np.array([0] * self.NMONTHS)
            grain_fed_milk_protein = np.array([0] * self.NMONTHS)

        return (grain_fed_milk_kcals, grain_fed_milk_fat, grain_fed_milk_protein)

    def get_meat_from_human_edible_feed(self):
        """
        Calculates the amount of meat that can be obtained from human-edible feed.
        Args:
            self: instance of the class containing the necessary data for calculations
        Returns:
            tuple: a tuple containing the amount of kcals, fat, and protein that can be obtained from the meat
        """
        present_day_tons_per_month_chicken_pork_prewaste = (
            self.CHICKEN_AND_PORK_LIMIT_PREWASTE
        )  # tons a month

        # Calculate the ratio of maintained cattle
        ratio_maintained_cattle = (
            np.array(self.cattle_grazing_maintained_prewaste)
            + np.array(self.cattle_grain_fed_maintained_prewaste)
        ) / self.TONS_BEEF_MONTHLY_BASELINE_PREWASTE

        # Ensure that the ratio of not maintained cattle is non-negative
        self.ratio_not_maintained_cattle = np.max(
            [1 - ratio_maintained_cattle, np.zeros(len(ratio_maintained_cattle))],
            axis=0,
        )

        # Ensure that all values in the ratio of maintained chicken and pork are non-negative
        assert (self.ratio_maintained_chicken_pork.round(8) >= 0).all()

        # If there are some very small negative values in the ratio of maintained chicken and pork, round them off to zero
        if (self.ratio_maintained_chicken_pork <= 0).any():
            self.ratio_maintained_chicken_pork = (
                self.ratio_maintained_chicken_pork.round(8)
            )
        assert (self.ratio_maintained_chicken_pork >= 0).all()

        # Ensure that all values in the ratio of maintained cattle are non-negative
        all_non_negative = np.array(ratio_maintained_cattle >= 0).all()
        assert all_non_negative

        # If the ratio of maintained cattle exceeds 2020 baseline levels, print a warning
        if (ratio_maintained_cattle >= 1).any():
            PRINT_CATTLE_WARNING = False
            if PRINT_CATTLE_WARNING:
                print("")
                print("WARNING: cattle maintained is exceeding 2020 baseline levels")

        # Calculate the ratio of maintained chicken and pork
        if present_day_tons_per_month_chicken_pork_prewaste > 0:
            self.ratio_maintained_chicken_pork = (
                np.array(self.chicken_pork_maintained_prewaste)
                / present_day_tons_per_month_chicken_pork_prewaste
            )
        else:
            self.ratio_maintained_chicken_pork = np.zeros(
                len(self.chicken_pork_maintained_prewaste)
            )

        # Ensure that all values in the ratio of maintained chicken and pork are one or lower
        all_one_or_lower = (self.ratio_maintained_chicken_pork <= 1).all()

        # If at least one month has higher chicken and pork above baseline levels, print a warning
        PRINT_CHICKEN_PORK_WARNING = False
        if not all_one_or_lower and PRINT_CHICKEN_PORK_WARNING:
            print("At least one month has higher chicken and pork above")
            print("baseline levels. This may be surprising if we are running a global")
            print("model, but is to be expected in at least some countries.")
            print("")

        # Calculate the amount of kcals, fat, and protein that can be obtained from chicken and pork
        self.chicken_pork_prewaste_kcals = (
            np.array(self.chicken_pork_maintained_prewaste)
            * self.dry_caloric_tons_per_ton_chicken_pork  # now units dry caloric tons
            * 4e6  # now units kcals
            / 1e9  # now units billion kcals
        )

        # Calculate the amount of fat that can be obtained from chicken and pork
        self.chicken_pork_prewaste_fat = (
            np.array(self.chicken_pork_maintained_prewaste)
            * self.thousand_tons_fat_per_ton_chicken_pork
        )

        # Calculate the amount of protein that can be obtained from chicken and pork
        self.chicken_pork_prewaste_protein = (
            np.array(self.chicken_pork_maintained_prewaste)
            * self.thousand_tons_protein_per_ton_chicken_pork
        )

        # Calculate the amount of kcals that can be obtained from cattle that are fed grain
        cattle_grain_fed_maintained_prewaste_kcals = (
            np.array(self.cattle_grain_fed_maintained_prewaste)
            * self.dry_caloric_tons_per_ton_beef
            * 4e6
            / 1e9
        )

        # Calculate the amount of fat that can be obtained from cattle that are fed grain
        cattle_grain_fed_maintained_prewaste_fat = (
            cattle_grain_fed_maintained_prewaste_kcals
            * 1e9
            / self.LARGE_ANIMAL_KCALS_PER_KG
            * self.LARGE_ANIMAL_FAT_RATIO
            / 1e6
        )

        # Calculate the amount of protein that can be obtained from cattle that are fed grain
        cattle_grain_fed_maintained_prewaste_protein = (
            cattle_grain_fed_maintained_prewaste_kcals
            * 1e9
            / self.LARGE_ANIMAL_KCALS_PER_KG
            * self.LARGE_ANIMAL_PROTEIN_RATIO
            / 1e6
        )

        # Calculate the amount of kcals, fat, and protein that can be obtained from grain-fed meat
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

        # If the option to add maintained meat is not selected, set the amount of kcals, fat, and protein from grain-fed meat to zero
        if not self.ADD_MAINTAINED_MEAT:
            grain_fed_meat_kcals = np.array([0] * self.NMONTHS)
            grain_fed_meat_fat = np.array([0] * self.NMONTHS)
            grain_fed_meat_protein = np.array([0] * self.NMONTHS)

        # Return the amount of kcals, fat, and protein that can be obtained from grain-fed meat
        return (
            grain_fed_meat_kcals,
            grain_fed_meat_fat,
            grain_fed_meat_protein,
        )

    def get_grazing_milk_produced_postwaste(self, grazing_milk_produced_prewaste):
        """
        Calculates the amount of grazing milk produced post-waste, given the amount of grazing milk produced pre-waste.

        Args:
            grazing_milk_produced_prewaste (list): A list of the amount of grazing milk produced pre-waste.

        Returns:
            tuple: A tuple containing the amount of grazing milk produced post-waste in billions of kcals, thousands of tons of fat, and thousands of tons of protein.

        """
        # Calculate the amount of kcals in grazing milk produced post-waste in billions
        grazing_milk_kcals = (
            np.array(grazing_milk_produced_prewaste)
            * 1e3
            * self.MILK_KCALS
            / 1e9
            * (1 - self.MILK_WASTE / 100)
        )

        # Calculate the amount of fat in grazing milk produced post-waste in thousands of tons
        grazing_milk_fat = (
            np.array(grazing_milk_produced_prewaste)
            / 1e3
            * self.MILK_FAT
            * (1 - self.MILK_WASTE / 100)
        )

        # Calculate the amount of protein in grazing milk produced post-waste in thousands of tons
        grazing_milk_protein = (
            np.array(grazing_milk_produced_prewaste)
            / 1e3
            * self.MILK_PROTEIN
            * (1 - self.MILK_WASTE / 100)
        )

        # Return the calculated values as a tuple
        return (grazing_milk_kcals, grazing_milk_fat, grazing_milk_protein)

    def get_cattle_grazing_maintained(self):
        """
        Calculates the kcals, fat, and protein from cattle grazing that is maintained for meat production.
        If ADD_MAINTAINED_MEAT is True, the function calculates the kcals, fat, and protein from cattle grazing that is maintained for meat production.
        If ADD_MAINTAINED_MEAT is False, the function returns 0 for kcals, fat, and protein.
        Args:
            self: instance of the class
        Returns:
            tuple: a tuple containing the kcals, fat, and protein from cattle grazing that is maintained for meat production.
        """
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
            # If ADD_MAINTAINED_MEAT is False, return 0 for kcals, fat, and protein.
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

    def get_max_slaughter_monthly(
        self, small_animals_culled, medium_animals_culled, large_animals_culled
    ):
        """
        Get the maximum number of animals that can be culled in a month and return the
        resulting array for max total calories slaughtered that month.

        Args:
            self (object): instance of the class
            small_animals_culled (list): list of integers representing the number of small animals culled each month
            medium_animals_culled (list): list of integers representing the number of medium animals culled each month
            large_animals_culled (list): list of integers representing the number of large animals culled each month

        Returns:
            list: list of integers representing the maximum total calories that can be slaughtered each month

        Raises:
            None

        """
        # initialize an empty list to store the maximum total calories that can be slaughtered each month
        calories_max_monthly = []
        # iterate over the range of the length of small_animals_culled
        for m in range(0, len(small_animals_culled)):
            # calculate the calories, fat, and protein for the culled meat using the calculate_culled_meat method
            (calories, fat, protein) = self.calculate_culled_meat(
                small_animals_culled[m],
                medium_animals_culled[m],
                large_animals_culled[m],
            )
            # add the maximum of calories and 0 to the calories_max_monthly list to avoid negative values
            calories_max_monthly.append(max(calories, 0))
        # return the list of maximum total calories that can be slaughtered each month
        return calories_max_monthly

    def calculate_culled_meat(
        self,
        init_small_animals_culled,
        init_medium_animals_culled,
        init_large_animals_culled,
    ):
        """
        Calculates the amount of culled meat in billion kcals, thousand tons of fat, and thousand tons of protein
        based on the number of small, medium, and large animals culled.

        Args:
            self (object): instance of the class
            init_small_animals_culled (int): number of small animals culled
            init_medium_animals_culled (int): number of medium animals culled
            init_large_animals_culled (int): number of large animals culled

        Returns:
            tuple: a tuple containing the initial culled meat pre-waste in billion kcals,
            the fraction of culled meat that is fat, and the fraction of culled meat that is protein
        """

        # Conversion factor from kg to thousand tons
        KG_TO_1000_TONS = self.KG_TO_1000_TONS

        # Calculate kcals, fat, and protein per small animal
        KCALS_PER_SMALL_ANIMAL = (
            self.SMALL_ANIMAL_KCALS_PER_KG * self.KG_PER_SMALL_ANIMAL / 1e9
        )
        FAT_PER_SMALL_ANIMAL = (
            self.SMALL_ANIMAL_FAT_RATIO * self.KG_PER_SMALL_ANIMAL * KG_TO_1000_TONS
        )
        PROTEIN_PER_SMALL_ANIMAL = (
            self.SMALL_ANIMAL_PROTEIN_RATIO * self.KG_PER_SMALL_ANIMAL * KG_TO_1000_TONS
        )

        # Calculate kcals, fat, and protein per medium animal
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

        # Calculate kcals, fat, and protein per large animal
        KCALS_PER_LARGE_ANIMAL = (
            self.LARGE_ANIMAL_KCALS_PER_KG * self.KG_PER_LARGE_ANIMAL / 1e9
        )
        FAT_PER_LARGE_ANIMAL = (
            self.LARGE_ANIMAL_FAT_RATIO * self.KG_PER_LARGE_ANIMAL * KG_TO_1000_TONS
        )
        PROTEIN_PER_LARGE_ANIMAL = (
            self.LARGE_ANIMAL_PROTEIN_RATIO * self.KG_PER_LARGE_ANIMAL * KG_TO_1000_TONS
        )

        # Calculate the initial culled meat pre-waste in billion kcals, thousand tons of fat, and thousand tons of protein
        init_culled_meat_prewaste_kcals = (
            init_small_animals_culled * KCALS_PER_SMALL_ANIMAL
            + init_medium_animals_culled * KCALS_PER_MEDIUM_ANIMAL
            + init_large_animals_culled * KCALS_PER_LARGE_ANIMAL
        )
        init_culled_meat_prewaste_fat = (
            init_small_animals_culled * FAT_PER_SMALL_ANIMAL
            + init_medium_animals_culled * FAT_PER_MEDIUM_ANIMAL
            + init_large_animals_culled * FAT_PER_LARGE_ANIMAL
        )
        init_culled_meat_prewaste_protein = (
            init_small_animals_culled * PROTEIN_PER_SMALL_ANIMAL
            + init_medium_animals_culled * PROTEIN_MEDIUM_ANIMAL
            + init_large_animals_culled * PROTEIN_PER_LARGE_ANIMAL
        )

        # Set the initial culled meat pre-waste to the kcals value
        initial_culled_meat_prewaste = init_culled_meat_prewaste_kcals

        # Calculate the fraction of culled meat that is fat and protein
        if initial_culled_meat_prewaste > 0:
            culled_meat_fraction_fat = (
                init_culled_meat_prewaste_fat / init_culled_meat_prewaste_kcals
            )
            culled_meat_fraction_protein = (
                init_culled_meat_prewaste_protein / init_culled_meat_prewaste_kcals
            )
        else:
            culled_meat_fraction_fat = 0
            culled_meat_fraction_protein = 0

        # Return the initial culled meat pre-waste, fraction of culled meat that is fat, and fraction of culled meat that is protein
        return (
            initial_culled_meat_prewaste,
            culled_meat_fraction_fat,
            culled_meat_fraction_protein,
        )

    def get_culled_meat_post_waste(self, constants_for_params):
        """
        Calculates the amount of culled meat post-waste based on the initial amount of culled meat pre-waste and the
        percentage of meat waste.

        Args:
            self: instance of the class containing the function
            constants_for_params: dictionary containing the constants used in the calculation

        Returns:
            float: the amount of culled meat post-waste

        """
        # Check if culled meat should be added to the calculation
        if self.ADD_CULLED_MEAT:
            culled_meat_prewaste = self.initial_culled_meat_prewaste
        else:
            culled_meat_prewaste = 0

        # Calculate the amount of culled meat post-waste
        culled_meat_postwaste = culled_meat_prewaste * (1 - self.MEAT_WASTE / 100)

        return culled_meat_postwaste

    def calculate_animals_culled(self, constants_for_params):
        """
        Calculates the number of animals culled based on the given constants and parameters.

        Args:
            self: instance of the class
            constants_for_params: dictionary containing the constants and parameters

        Returns:
            None

        The function calculates the number of animals culled based on the given constants and parameters.
        If ADD_CULLED_MEAT is True, the function calculates the number of small, medium, and large animals culled
        based on the ratio of maintained chicken and pork and the ratio of not maintained cattle.
        If ADD_CULLED_MEAT is False, the function sets the number of culled animals to 0.

        """
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
