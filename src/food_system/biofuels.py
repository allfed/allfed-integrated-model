################################# Biofuels ####################################
##                                                                            #
##              Functions and constants relating to biofuels                  #
##                                                                            #
###############################################################################


class Biofuels:
    def __init__(self, constants_for_params):
        self.NMONTHS = constants_for_params["NMONTHS"]
        self.BIOFUEL_KCALS = constants_for_params["BIOFUEL_KCALS"]
        self.BIOFUEL_FAT = constants_for_params["BIOFUEL_FAT"]
        self.BIOFUEL_PROTEIN = constants_for_params["BIOFUEL_PROTEIN"]

    def set_biofuel_usage(self, constants_for_params):

        self.biofuel_monthly_usage_KCALS = (
            self.BIOFUEL_KCALS / 12 * 4e6 / 1e9
        )  # billions kcals
        self.biofuel_monthly_usage_FAT = self.BIOFUEL_FAT / 12 / 1e3  # thousand tons
        self.biofuel_monthly_usage_PROTEIN = (
            self.BIOFUEL_PROTEIN / 12 / 1e3
        )  # thousand tons

        # Delayed shutoff BIOFUELS ####
        # "Monthly flows" tab @Morgan: Link broken

        biofuel_delay = constants_for_params["DELAY"]["BIOFUEL_SHUTOFF_MONTHS"]
        self.biofuels_kcals = [self.biofuel_monthly_usage_KCALS] * biofuel_delay + [
            0
        ] * (self.NMONTHS - biofuel_delay)
        self.biofuels_fat = [self.biofuel_monthly_usage_FAT] * biofuel_delay + [0] * (
            self.NMONTHS - biofuel_delay
        )
        self.biofuels_protein = [self.biofuel_monthly_usage_PROTEIN] * biofuel_delay + [
            0
        ] * (self.NMONTHS - biofuel_delay)
