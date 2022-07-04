################################# Seafood #####################################
##                                                                            #
##       Functions and constants relating to seafood, excluding seaweed       #
##                                                                            #
###############################################################################

class Seafood:

    def __init__(self,inputs_to_optimizer):
        self.NMONTHS = inputs_to_optimizer['NMONTHS']
        self.ADD_FISH = inputs_to_optimizer['ADD_FISH']

        FISH_WASTE = inputs_to_optimizer['WASTE']['SEAFOOD']

        # fish kcals per month, billions
        self.FISH_KCALS = inputs_to_optimizer["FISH_DRY_CALORIC_ANNUAL"] \
                     * (1 - FISH_WASTE / 100) * 4e6 / 1e9 / 12 

        # units of 1000s tons protein monthly 
        # (so, global value is in the hundreds of thousands of tons)
        self.FISH_PROTEIN = inputs_to_optimizer["FISH_PROTEIN_TONS_ANNUAL"] \
                       / 1e3 / 12

        # units of 1000s tons fat
        # (so, global value is in the tens of thousands of tons)
        self.FISH_FAT = inputs_to_optimizer["FISH_FAT_TONS_ANNUAL"] \
                       / 1e3 / 12

    # includes all seafood (except seaweed), not just fish
    def get_seafood_production(self,inputs_to_optimizer):


        # https://assets.researchsquare.com/files/rs-830419/v1_covered.pdf?c=1631878417

        FISH_PERCENT_EACH_MONTH_LONG = \
            inputs_to_optimizer["FISH_PERCENT_MONTHLY"]

        FISH_PERCENT_EACH_MONTH = FISH_PERCENT_EACH_MONTH_LONG[0:self.NMONTHS]

        if(self.ADD_FISH):
            production_kcals_fish_per_month = []
            production_protein_fish_per_month = []
            production_fat_fish_per_month = []
            for x in FISH_PERCENT_EACH_MONTH:
                production_kcals_fish_per_month.append(x / 100 * self.FISH_KCALS)
                production_protein_fish_per_month.append(
                    x / 100 * self.FISH_PROTEIN)
                production_fat_fish_per_month.append(x / 100 * self.FISH_FAT)
        else:
            production_kcals_fish_per_month = \
                [0] * len(FISH_PERCENT_EACH_MONTH)
            production_protein_fish_per_month = \
                [0] * len(FISH_PERCENT_EACH_MONTH)
            production_fat_fish_per_month = \
                [0] * len(FISH_PERCENT_EACH_MONTH)

        return (production_kcals_fish_per_month,
                production_fat_fish_per_month,
                production_protein_fish_per_month)