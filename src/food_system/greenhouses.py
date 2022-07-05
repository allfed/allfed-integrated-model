################################# Greenhouses #################################
##                                                                            #
##       Functions and constants relating to greenhouse crop productio        #
##                                                                            #`
###############################################################################

import numpy as np

class Greenhouses:

    def __init__(self,inputs_to_optimizer):
        # 500 million hectares in tropics (for outdoor crops 2020)
        self.TOTAL_CROP_AREA = 500e6  



        self.ADD_GREENHOUSES = inputs_to_optimizer['ADD_GREENHOUSES']
        self.NMONTHS = inputs_to_optimizer['NMONTHS']

        if(self.ADD_GREENHOUSES):
            # this is in addition to the 5 month delay till harvest
            self.greenhouse_delay = inputs_to_optimizer["DELAY"]["GREENHOUSE_MONTHS"]
            self.GREENHOUSE_AREA_MULTIPLIER = inputs_to_optimizer['GREENHOUSE_AREA_MULTIPLIER']
        else:
            self.GREENHOUSE_AREA_MULTIPLIER = 0

    def get_greenhouse_area(self,inputs_to_optimizer):
        # greenhouses tab
        # assumption: greenhouse crop production is very similar in nutritional
        # profile to stored food
        # reference: see https://docs.google.com/spreadsheets/d / 1f9eVD14Y2d9vmLFP3OsJPFA5d2JXBU-63MTz8MlB1rY/edit#gid=756212200
        # greenhouse paper (scaling of greenhouses in low sunlight scenarios)
        # At constant expansion for 36 months, the cumulative ground coverage
        # will equal 2.5 million km^2 (250 million hectares).
        # Takes 5+36=41 months to reach full output
        # NOTE: the 5 months represents the delay from plant to harvest.

        if(self.ADD_GREENHOUSES):
            GREENHOUSE_LIMIT_AREA = self.TOTAL_CROP_AREA * self.GREENHOUSE_AREA_MULTIPLIER

            greenhouse_area_long = \
                list(
                    np.append(
                        np.append(
                            np.append(np.linspace(0, 0, self.greenhouse_delay),
                                      np.linspace(0, 0, 5)),
                            np.linspace(0, GREENHOUSE_LIMIT_AREA, 37)
                        ),
                        np.linspace(GREENHOUSE_LIMIT_AREA,
                                    GREENHOUSE_LIMIT_AREA, len(KCALS_GROWN) - 42)
                    )
                )\

            greenhouse_area = np.array(greenhouse_area_long[0:self.NMONTHS])
            print("CANT DEAL TOTAL CROPS SAD")
            quit()

            MONTHLY_KCALS = np.mean(months_cycle) / self.TOTAL_CROP_AREA

            KCALS_GROWN_PER_HECTARE_BEFORE_WASTE = \
                MONTHLY_KCALS * (1 - (
                    (1 - all_months_reductions[4:])
                    * OG_KCAL_REDUCED
                ))

            self.GH_KCALS_GROWN_PER_HECTARE = (1 - CROP_WASTE / 100) \
                * np.array(KCALS_GROWN_PER_HECTARE_BEFORE_WASTE)
        else:
            self.GH_KCALS_GROWN_PER_HECTARE = [0] * self.NMONTHS
            greenhouse_area = np.array([0] * self.NMONTHS)

        self.greenhouse_fraction_area = greenhouse_area / self.TOTAL_CROP_AREA
        return greenhouse_area

    # for the conversions and numbers, go here
    # https://docs.google.com/document/d / 1HlML7ptYmRfNJjko5qMfIJJGyLRUBlnCIiEiBMr41cM/edit#
    # and here
    # https://docs.google.com/spreadsheets/d / 1rYcxSe-Z7ztvW-QwTBXT8GABaRmVdDuQ05HXmTHbQ8I/edit#gid=1141282747

    # SUM_CALORIES is an overestimate by some factor, as it is in current
    # day conditions. We improve accuracy by applying the outdoor growing
    # estimate and decreasing the estimated fat and protein by the same
    # factor that kcals are decreased by
    def get_greenhouse_yield_per_ha(self, inputs_to_optimizer, outdoor_crops):
        KCAL_RATIO = outdoor_crops.KCAL_RATIO_ROT
        FAT_RATIO = outdoor_crops.FAT_RATIO_ROT
        PROTEIN_RATIO = outdoor_crops.PROTEIN_RATIO_ROT

        if(not self.ADD_GREENHOUSES):
            greenhouse_kcals_per_ha = [0] * self.NMONTHS
            greenhouse_fat_per_ha = [0] * self.NMONTHS
            greenhouse_protein_per_ha = [0] * self.NMONTHS
            return (greenhouse_kcals_per_ha,greenhouse_fat_per_ha,greenhouse_protein_per_ha)
            
        rotation_fat_per_ha_long = []
        rotation_protein_per_ha_long = []
        rotation_kcals_per_ha_long = []
        for kcals_per_month in self.GH_KCALS_GROWN_PER_HECTARE:
            gh_kcals = kcals_per_month * KCAL_RATIO \
                * (1+inputs_to_optimizer["GREENHOUSE_GAIN_PCT"] / 100)

            rotation_kcals_per_ha_long.append(gh_kcals)

            rotation_fat_per_ha_long.append(FAT_RATIO * gh_kcals)

            rotation_protein_per_ha_long.append(PROTEIN_RATIO * gh_kcals)

        rotation_kcals_per_ha = rotation_kcals_per_ha_long[0:self.NMONTHS]
        rotation_fat_per_ha = rotation_fat_per_ha_long[0:self.NMONTHS]
        rotation_protein_per_ha = rotation_protein_per_ha_long[0:self.NMONTHS]

        return (rotation_kcals_per_ha,
                rotation_fat_per_ha,
                rotation_protein_per_ha)
