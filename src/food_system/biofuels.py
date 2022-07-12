################################# Biofuels ####################################
##                                                                            #
##              Functions and constants relating to biofuels                  #
##                                                                            #
###############################################################################


class Biofuels:
    def __init__(self, inputs_to_optimizer):
        self.NMONTHS = inputs_to_optimizer["NMONTHS"]
        self.BIOFUEL_KCALS = inputs_to_optimizer["BIOFUEL_KCALS"]
        self.BIOFUEL_FAT = inputs_to_optimizer["BIOFUEL_FAT"]
        self.BIOFUEL_PROTEIN = inputs_to_optimizer["BIOFUEL_PROTEIN"]

    def get_biofuel_usage(self, inputs_to_optimizer):

        self.BIOFUEL_MONTHLY_USAGE_KCALS = (
            self.BIOFUEL_KCALS / 12 * 4e6 / 1e9
        )  # billions kcals
        self.BIOFUEL_MONTHLY_USAGE_FAT = self.BIOFUEL_FAT / 12 / 1e3  # thousand tons
        self.BIOFUEL_MONTHLY_USAGE_PROTEIN = (
            self.BIOFUEL_PROTEIN / 12 / 1e3
        )  # thousand tons

        # Delayed shutoff BIOFUELS ####
        # "Monthly flows" tab @Morgan: Link broken

        biofuel_delay = inputs_to_optimizer["DELAY"]["BIOFUEL_SHUTOFF_MONTHS"]
        self.biofuels_kcals = [self.BIOFUEL_MONTHLY_USAGE_KCALS] * biofuel_delay + [
            0
        ] * (self.NMONTHS - biofuel_delay)
        self.biofuels_fat = [self.BIOFUEL_MONTHLY_USAGE_FAT] * biofuel_delay + [0] * (
            self.NMONTHS - biofuel_delay
        )
        self.biofuels_protein = [self.BIOFUEL_MONTHLY_USAGE_PROTEIN] * biofuel_delay + [
            0
        ] * (self.NMONTHS - biofuel_delay)

        return (self.biofuels_kcals, self.biofuels_fat, self.biofuels_protein)
