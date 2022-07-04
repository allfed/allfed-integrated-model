############################### Stored Food ###################################
##                                                                            #
##       Functions and constants relating to stocks and stored food           #
##                                                                            #
###############################################################################

class StoredFood:

    def __init__(self,inputs_to_optimizer,outdoor_crops):

        # (nuclear event in mid-may)
        # Mike's spreadsheet: https://docs.google.com/spreadsheets/d / 19kzHpux690JTCo2IX2UA1faAd7R1QcBK/edit#gid=806987252

        TONS_DRY_CALORIC_EQIVALENT_SF = \
            inputs_to_optimizer['TONS_DRY_CALORIC_EQIVALENT_SF']

        # billion kcals per unit mass initial
        self.INITIAL_SF_KCALS = TONS_DRY_CALORIC_EQIVALENT_SF * \
            4e6 / 1e9  


        # we know:
        #     units_sf_mass * SF_FRACTION_KCALS=sf_kcals
        # and
        #     units_sf_mass * SF_FRACTION_PROTEIN=sf_protein
        # so
        #     units_sf_mass = sf_kcals/SF_FRACTION_KCALS
        # => assumption listed previously (see outdoor crops.py,
        #                                  calculate_monthly_production()) =>
        #     units_og_mass = og_kcals/SF_FRACTION_KCALS
        #     units_og_mass = og_protein/SF_FRACTION_PROTEIN
        # therefore
        #     og_protein = og_kcals * SF_FRACTION_PROTEIN/SF_FRACTION_KCALS

        self.SF_FRACTION_FAT = outdoor_crops.OG_FRACTION_FAT
        self.SF_FRACTION_PROTEIN = outdoor_crops.OG_FRACTION_PROTEIN

