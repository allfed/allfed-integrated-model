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
            ADD_MEAT (float): Edible meat, organs, and fat added for culling.
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

        # edible meat, organs, and fat added
        self.ADD_MEAT = constants_for_params["ADD_MEAT"]

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
        self.human_inedible_feed_dry_caloric_tons_list = np.array([])
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
            self.human_inedible_feed_dry_caloric_tons_list = np.append(
                self.human_inedible_feed_dry_caloric_tons_list,
                [
                    ratio_human_inedible_feed
                    * constants_for_params["HUMAN_INEDIBLE_FEED_BASELINE_MONTHLY"]
                ]
                * 12,
            )

        human_inedible_feed_dry_caloric_tons = Food(
            kcals=self.human_inedible_feed_dry_caloric_tons_list,
            fat=np.zeros(len(self.human_inedible_feed_dry_caloric_tons_list)),
            protein=np.zeros(len(self.human_inedible_feed_dry_caloric_tons_list)),
            kcals_units="million dry caloric tons each month",
            fat_units="million tons each month",
            protein_units="million tons each month",
        )

        self.human_inedible_feed = (
            human_inedible_feed_dry_caloric_tons.in_units_bil_kcals_thou_tons_thou_tons_per_month()
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
        # tons a month meat
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

        self.MEAT_WASTE_DISTRIBUTION = constants_for_params["WASTE_DISTRIBUTION"][
            "MEAT"
        ]
        self.MILK_WASTE_DISTRIBUTION = constants_for_params["WASTE_DISTRIBUTION"][
            "MILK"
        ]

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
                - MEDIUM_ANIMAL_KCALS_PER_KG (float): The number of kilocalories per kilogram of meat for a medium
                    animal.
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

    # CALCULATIONS FOR MEAT AND DAIRY PRODUCTION USING GRAIN AND GRAZING

    # the following two functions are less efficient alternatives for bad adaptation

    def get_milk_produced_postwaste(self, milk_produced_prewaste):
        """
        Calculates the amount of grazing milk produced post-waste, given the amount of grazing milk produced pre-waste.

        Args:
            milk_produced_prewaste (list): A list of the amount of grazing milk produced pre-waste.

        Returns:
            tuple: A tuple containing the amount of grazing milk produced post-waste in billions of kcals, thousands
            of tons of fat, and thousands of tons of protein.

        """
        # Calculate the amount of kcals in grazing milk produced post-waste in billions
        # billions kcals
        milk_kcals = (
            np.array(milk_produced_prewaste)
            * 1e3
            * self.MILK_KCALS
            / 1e9
            * (1 - self.MILK_WASTE_DISTRIBUTION / 100)
        )

        # Calculate the amount of fat in grazing milk produced post-waste in thousands of tons
        # thousands tons
        milk_fat = (
            np.array(milk_produced_prewaste)
            / 1e3
            * self.MILK_FAT
            * (1 - self.MILK_WASTE_DISTRIBUTION / 100)
        )

        # Calculate the amount of protein in grazing milk produced post-waste in thousands of tons
        # thousands tons
        milk_protein = (
            np.array(milk_produced_prewaste)
            / 1e3
            * self.MILK_PROTEIN
            * (1 - self.MILK_WASTE_DISTRIBUTION / 100)
        )

        # Return the calculated values as a tuple
        return (milk_kcals, milk_fat, milk_protein)

    # CULLED MEAT

    def get_max_slaughter_monthly_after_distribution_waste(
        self, small_animals_culled, medium_animals_culled, large_animals_culled
    ):
        """
        Get the maximum number of animals that can be culled in a month and return the
        resulting array for max total calories slaughtered that month.
        """

        slaughtered_meat_monthly = Food(
            kcals=np.zeros(len(small_animals_culled)),
            fat=np.zeros(len(small_animals_culled)),
            protein=np.zeros(len(small_animals_culled)),
            kcals_units="billion kcals each month",
            fat_units="thousand tons each month",
            protein_units="thousand tons each month",
        )

        for m in range(0, len(small_animals_culled)):
            (
                calories,
                fat_ratio,
                protein_ratio,
            ) = self.calculate_meat_after_distribution_waste(
                small_animals_culled[m],
                medium_animals_culled[m],
                large_animals_culled[m],
            )
            meat_slaughtered_this_month = Food(
                kcals=calories,
                fat=calories * fat_ratio,
                protein=calories * protein_ratio,
                kcals_units="billion kcals",
                fat_units="thousand tons",
                protein_units="thousand tons",
            )
            slaughtered_meat_monthly[m] = meat_slaughtered_this_month
            # no negative slaughter rates (addresses rounding errors)
        return slaughtered_meat_monthly

    def calculate_meat_after_distribution_waste(
        self,
        init_small_animals_culled,
        init_medium_animals_culled,
        init_large_animals_culled,
    ):
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
        init_meat_prewaste_kcals = (
            init_small_animals_culled * KCALS_PER_SMALL_ANIMAL
            + init_medium_animals_culled * KCALS_PER_MEDIUM_ANIMAL
            + init_large_animals_culled * KCALS_PER_LARGE_ANIMAL
        )
        # thousand tons
        init_meat_prewaste_fat = (
            init_small_animals_culled * FAT_PER_SMALL_ANIMAL
            + init_medium_animals_culled * FAT_PER_MEDIUM_ANIMAL
            + init_large_animals_culled * FAT_PER_LARGE_ANIMAL
        )
        # thousand tons
        init_meat_prewaste_protein = (
            init_small_animals_culled * PROTEIN_PER_SMALL_ANIMAL
            + init_medium_animals_culled * PROTEIN_MEDIUM_ANIMAL
            + init_large_animals_culled * PROTEIN_PER_LARGE_ANIMAL
        )

        initial_meat_prewaste = init_meat_prewaste_kcals

        if initial_meat_prewaste > 0:
            meat_fraction_fat = init_meat_prewaste_fat / init_meat_prewaste_kcals
            meat_fraction_protein = (
                init_meat_prewaste_protein / init_meat_prewaste_kcals
            )
        else:
            meat_fraction_fat = 0
            meat_fraction_protein = 0

        return (
            initial_meat_prewaste * (1 - self.MEAT_WASTE_DISTRIBUTION / 100),
            meat_fraction_fat,
            meat_fraction_protein,
        )
