#################################### Feed #####################################
##                                                                            #
##             Functions and constants relating to animal feed                #
##                                                                            #
###############################################################################

import numpy as np


class Feed:
    def __init__(self, inputs_to_optimizer):
        self.NMONTHS = inputs_to_optimizer["NMONTHS"]
        self.FEED_KCALS = inputs_to_optimizer["FEED_KCALS"]
        self.FEED_FAT = inputs_to_optimizer["FEED_FAT"]
        self.FEED_PROTEIN = inputs_to_optimizer["FEED_PROTEIN"]

        # or, should this be 1543e6?? cell L8 https://docs.google.com/spreadsheets/d / 1rYcxSe-Z7ztvW-QwTBXT8GABaRmVdDuQ05HXmTHbQ8I/edit#gid=1141282747
        self.FEED_MONTHLY_USAGE_KCALS = (
            self.FEED_KCALS / 12 * 4e6 / 1e9
        )  # billions kcals
        self.FEED_MONTHLY_USAGE_FAT = self.FEED_FAT / 12 / 1e3  # thousand tons
        self.FEED_MONTHLY_USAGE_PROTEIN = self.FEED_PROTEIN / 12 / 1e3  # thousand tons

    def get_feed_usage(self, inputs_to_optimizer):
        #### Delayed shutoff FEED ####
        # "Monthly flows" tab https://docs.google.com/spreadsheets/d / 1tLFHJpXTStxyfNojP_Wrj0MQowfyKujJUA37ZG1q6pk/edit#gid=1714403726

        self.feed_shutoff_delay_months = inputs_to_optimizer["DELAY"][
            "FEED_SHUTOFF_MONTHS"
        ]
        self.feed_shutoff_kcals = np.array(
            [self.FEED_MONTHLY_USAGE_KCALS] * self.feed_shutoff_delay_months
            + [0] * (self.NMONTHS - self.feed_shutoff_delay_months)
        )
        self.feed_shutoff_fat = np.array(
            [self.FEED_MONTHLY_USAGE_FAT] * self.feed_shutoff_delay_months
            + [0] * (self.NMONTHS - self.feed_shutoff_delay_months)
        )
        self.feed_shutoff_protein = np.array(
            [self.FEED_MONTHLY_USAGE_PROTEIN] * self.feed_shutoff_delay_months
            + [0] * (self.NMONTHS - self.feed_shutoff_delay_months)
        )

        self.kcals_fed_to_animals = (
            inputs_to_optimizer["EXCESS_CALORIES"] + self.feed_shutoff_kcals
        )

        return (
            self.feed_shutoff_kcals,
            self.feed_shutoff_fat,
            self.feed_shutoff_protein,
        )
