"""
################################# Greenhouses #################################
##                                                                            #
##       Functions and constants relating to greenhouse crop productio        #
##                                                                            #`
###############################################################################
"""

import numpy as np


class Greenhouses:
    def __init__(self, constants_for_params):
        """
        Initializes the Greenhouses class with the given constants for parameters.

        Args:
            constants_for_params (dict): A dictionary containing the constants for parameters.

        Returns:
            None

        """
        self.TOTAL_CROP_AREA = (
            constants_for_params["INITIAL_GLOBAL_CROP_AREA"] * constants_for_params["INITIAL_CROP_AREA_FRACTION"]
        )

        # Set the starting month number based on the given constants.
        self.STARTING_MONTH_NUM = constants_for_params["STARTING_MONTH_NUM"]

        # Set the flag for adding greenhouses and the number of months based on the given constants.
        self.ADD_GREENHOUSES = constants_for_params["ADD_GREENHOUSES"]
        self.NMONTHS = constants_for_params["NMONTHS"]

        # If greenhouses are being added, set the greenhouse delay and greenhouse
        # area multiplier based on the given constants.
        if self.ADD_GREENHOUSES:
            # this is in addition to the 5 month delay till harvest
            self.greenhouse_delay = constants_for_params["DELAY"]["GREENHOUSE_MONTHS"]
            self.GREENHOUSE_AREA_MULTIPLIER = constants_for_params[
                "GREENHOUSE_AREA_MULTIPLIER"
            ]
        else:
            self.GREENHOUSE_AREA_MULTIPLIER = 0

    def assign_productivity_reduction_from_climate_impact(
        self, months_cycle, all_months_reductions, exponent, CROP_WASTE_COEFFICIENT
    ):
        """
        Assigns productivity reduction from climate impact to greenhouses.

        Args:
            months_cycle (list): list of monthly cycles
            all_months_reductions (list): list of all months reductions
            exponent (float): exponent value
            CROP_WASTE_COEFFICIENT (float): crop waste value

        Returns:
            None

        Example:
            >>>
            >>> greenhouse = Greenhouses()
            >>> greenhouse.assign_productivity_reduction_from_climate_impact(
            ...     [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            ...     [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2],
            ...     2,
            ...     10
            ... )

        """
        # Calculate monthly kcals
        MONTHLY_KCALS = np.mean(months_cycle) / self.TOTAL_CROP_AREA

        # Calculate kcals grown per hectare before waste
        KCALS_GROWN_PER_HECTARE_BEFORE_WASTE = []
        for i in range(self.NMONTHS):
            baseline_reduction = all_months_reductions[i]

            # Check if baseline reduction is greater than or equal to zero
            assert round(baseline_reduction, 8) >= 0  # 8 decimal places rounding

            # If there's some very small negative value here, just round it off to zero
            if baseline_reduction <= 0:
                baseline_reduction = round(baseline_reduction, 8)

            # Check if baseline reduction is greater than or equal to zero
            assert baseline_reduction >= 0  # 8 decimal places rounding

            # Check if all baseline reductions are greater than or equal to zero
            assert (baseline_reduction >= 0).all()

            # Calculate kcals grown per hectare before waste based on baseline reduction
            if baseline_reduction > 1:
                KCALS_GROWN_PER_HECTARE_BEFORE_WASTE.append(
                    MONTHLY_KCALS * baseline_reduction
                )
            else:
                KCALS_GROWN_PER_HECTARE_BEFORE_WASTE.append(
                    MONTHLY_KCALS * baseline_reduction**exponent
                )

        # this shortens the used duration of the nuclear winter reductions up to the number of modelled months
        all_months_reductions = all_months_reductions[
            0 : len(KCALS_GROWN_PER_HECTARE_BEFORE_WASTE)
        ]

        # Check if kcals grown per hectare before waste is greater than or equal
        # to monthly kcals times all months reductions
        assert (
            KCALS_GROWN_PER_HECTARE_BEFORE_WASTE
            >= MONTHLY_KCALS * all_months_reductions
        ).all(), "ERROR: Relocation has somehow decreased crop production!"

        # Calculate kcals grown per hectare after waste
        self.GH_KCALS_GROWN_PER_HECTARE = CROP_WASTE_COEFFICIENT * np.array(
            KCALS_GROWN_PER_HECTARE_BEFORE_WASTE
        )

    def get_greenhouse_area(self, constants_for_params, outdoor_crops):
        """
        Calculates the area of greenhouses needed to grow crops and returns it as an array.
        Args:
            self (Greenhouses): an instance of the Greenhouses class
            constants_for_params (dict): a dictionary containing constants used in the simulation
            outdoor_crops (OutdoorCrops): an instance of the OutdoorCrops class

        Returns:
            numpy.ndarray: an array containing the area of greenhouses needed to grow crops

        This function calculates the area of greenhouses needed to grow crops. It first checks if there is any crop
        area to
        grow. If there is no crop area, it returns an array of zeros. If there is crop area, it calculates the area of
        greenhouses needed based on the greenhouse area multiplier and the total crop area. If the greenhouse area
        multiplier is not specified, it uses the greenhouse fraction from Australia to calculate the greenhouse area. It
        then assigns the productivity reduction from climate impact and returns the greenhouse area array.
        """
        # greenhouses tab
        # assumption: greenhouse crop production is very similar in nutritional
        # profile to stored food
        # reference:
        # greenhouse paper (scaling of greenhouses in low sunlight scenarios)
        # At constant expansion for 36 months, the cumulative ground coverage
        # will equal 2.5 million km^2 (250 million hectares).
        # Takes 5+36=41 months to reach full output
        # NOTE: the 5 months represents the delay from plant to harvest.

        if self.TOTAL_CROP_AREA == 0:
            self.greenhouse_fraction_area = np.zeros(self.NMONTHS)
            return np.zeros(self.NMONTHS)

        if self.ADD_GREENHOUSES:
            GREENHOUSE_LIMIT_AREA = (
                self.TOTAL_CROP_AREA * self.GREENHOUSE_AREA_MULTIPLIER
            )
            greenhouse_area_long = list(
                np.append(
                    np.append(
                        np.append(
                            np.linspace(0, 0, self.greenhouse_delay),
                            np.linspace(0, 0, 5),
                        ),
                        np.linspace(0, GREENHOUSE_LIMIT_AREA, 37),
                    ),
                    np.linspace(
                        GREENHOUSE_LIMIT_AREA,
                        GREENHOUSE_LIMIT_AREA,
                        len(outdoor_crops.KCALS_GROWN) - 42,
                    ),
                )
            )

            greenhouse_area = np.array(greenhouse_area_long[0 : self.NMONTHS])
            CROP_WASTE_COEFFICIENT = (
                1 - constants_for_params["WASTE_DISTRIBUTION"]["CROPS"] / 100
            ) * (1 - constants_for_params["WASTE_RETAIL"] / 100)
            self.assign_productivity_reduction_from_climate_impact(
                outdoor_crops.months_cycle,
                outdoor_crops.all_months_reductions,
                outdoor_crops.OG_KCAL_EXPONENT,
                CROP_WASTE_COEFFICIENT,
            )
        else:
            self.GH_KCALS_GROWN_PER_HECTARE = [0] * self.NMONTHS
            greenhouse_area = np.array([0] * self.NMONTHS)

        self.greenhouse_fraction_area = greenhouse_area / self.TOTAL_CROP_AREA
        return greenhouse_area

    # SUM_CALORIES is an overestimate by some factor, as it is in current
    # day conditions. We improve accuracy by applying the outdoor growing
    # estimate and decreasing the estimated fat and protein by the same
    # factor that kcals are decreased by
    def get_greenhouse_yield_per_ha(self, constants_for_params, outdoor_crops):
        """
        Calculates the yield per hectare for greenhouses and returns the results.

        Args:
            constants_for_params (dict): A dictionary containing constants for the parameters.
            outdoor_crops (OutdoorCrops): An instance of the OutdoorCrops class.

        Returns:
            tuple: A tuple containing the greenhouse yield per hectare for kcals, fat, and protein.

        Example:
            >>> constants_for_params = {'GREENHOUSE_GAIN_PCT': 10}
            >>> outdoor_crops = OutdoorCrops()
            >>> greenhouses = Greenhouses()
            >>> greenhouses.ADD_GREENHOUSES = True
            >>> greenhouses.NMONTHS = 12
            >>> greenhouses.GH_KCALS_GROWN_PER_HECTARE = [100] * 12
            >>> greenhouses.get_greenhouse_yield_per_ha(constants_for_params, outdoor_crops)
            ([110.0, 110.0, 110.0, 110.0, 110.0, 110.0, 110.0, 110.0, 110.0, 110.0, 110.0, 110.0],
            [22.0, 22.0, 22.0, 22.0, 22.0, 22.0, 22.0, 22.0, 22.0, 22.0, 22.0, 22.0],
            [33.0, 33.0, 33.0, 33.0, 33.0, 33.0, 33.0, 33.0, 33.0, 33.0, 33.0, 33.0])
        """

        # Constants for fat and protein ratios
        KCAL_RATIO = outdoor_crops.KCAL_RATIO_ROTATION
        FAT_RATIO = outdoor_crops.FAT_RATIO_ROTATION
        PROTEIN_RATIO = outdoor_crops.PROTEIN_RATIO_ROTATION

        # If greenhouses are not added, return 0 yield
        if not self.ADD_GREENHOUSES:
            greenhouse_kcals_per_ha = [0] * self.NMONTHS
            greenhouse_fat_per_ha = [0] * self.NMONTHS
            greenhouse_protein_per_ha = [0] * self.NMONTHS
            return (
                greenhouse_kcals_per_ha,
                greenhouse_fat_per_ha,
                greenhouse_protein_per_ha,
            )

        # Calculate the yield for greenhouses
        relocation_kcals_per_ha_long = []
        relocated_fat_per_ha_long = []
        relocation_protein_per_ha_long = []

        for kcals_per_month in self.GH_KCALS_GROWN_PER_HECTARE:
            gh_kcals = (
                kcals_per_month
                * KCAL_RATIO
                * (1 + constants_for_params["GREENHOUSE_GAIN_PCT"] / 100)
            )  # units: billion kcals per month

            relocation_kcals_per_ha_long.append(gh_kcals)

            relocated_fat_per_ha_long.append(FAT_RATIO * gh_kcals)

            relocation_protein_per_ha_long.append(PROTEIN_RATIO * gh_kcals)

        # Return the yield for the number of months specified
        relocation_kcals_per_ha = relocation_kcals_per_ha_long[0 : self.NMONTHS]
        relocation_fat_per_ha = relocated_fat_per_ha_long[0 : self.NMONTHS]
        relocation_protein_per_ha = relocation_protein_per_ha_long[0 : self.NMONTHS]

        return (
            relocation_kcals_per_ha,
            relocation_fat_per_ha,
            relocation_protein_per_ha,
        )
