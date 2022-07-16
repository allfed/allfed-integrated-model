############################### Stored Food ###################################
##                                                                            #
##       Functions and constants relating to stocks and stored food           #
##                                                                            #
###############################################################################


class StoredFood:
    def __init__(self, inputs_to_optimizer, outdoor_crops):

        self.end_of_month_stocks = [0] * 12  # initialize the array
        self.end_of_month_stocks[0] = inputs_to_optimizer["END_OF_MONTH_STOCKS"]["JAN"]
        self.end_of_month_stocks[1] = inputs_to_optimizer["END_OF_MONTH_STOCKS"]["FEB"]
        self.end_of_month_stocks[2] = inputs_to_optimizer["END_OF_MONTH_STOCKS"]["MAR"]
        self.end_of_month_stocks[3] = inputs_to_optimizer["END_OF_MONTH_STOCKS"]["APR"]
        self.end_of_month_stocks[4] = inputs_to_optimizer["END_OF_MONTH_STOCKS"]["MAY"]
        self.end_of_month_stocks[5] = inputs_to_optimizer["END_OF_MONTH_STOCKS"]["JUN"]
        self.end_of_month_stocks[6] = inputs_to_optimizer["END_OF_MONTH_STOCKS"]["JUL"]
        self.end_of_month_stocks[7] = inputs_to_optimizer["END_OF_MONTH_STOCKS"]["AUG"]
        self.end_of_month_stocks[8] = inputs_to_optimizer["END_OF_MONTH_STOCKS"]["SEP"]
        self.end_of_month_stocks[9] = inputs_to_optimizer["END_OF_MONTH_STOCKS"]["OCT"]
        self.end_of_month_stocks[10] = inputs_to_optimizer["END_OF_MONTH_STOCKS"]["NOV"]
        self.end_of_month_stocks[11] = inputs_to_optimizer["END_OF_MONTH_STOCKS"]["DEC"]

        # (nuclear event in mid-may)
        # Mike's spreadsheet: https://docs.google.com/spreadsheets/d / 19kzHpux690JTCo2IX2UA1faAd7R1QcBK/edit#gid=806987252

        self.buffer_ratio = inputs_to_optimizer["BUFFER_RATIO"]

        self.SF_FRACTION_FAT = outdoor_crops.OG_FRACTION_FAT
        self.SF_FRACTION_PROTEIN = outdoor_crops.OG_FRACTION_PROTEIN

    def calculate_stored_food_to_use(self, starting_month):
        """
        Calculates and returns total stored food available to use at start of
        simulation. While a baseline scenario will simply use the typical amount of stocks to keep the buffer at a typical usage, other more extreme scenarios should be expected to use a higher percentage of all stored food, eating into the typical buffer.

        Arguments:
            starting_month (int): the month the simulation starts on.
            1=JAN, 2=FEB, ...,  12=DEC.
            (NOT TO BE CONFUSED WITH THE INDEX)

        Returns:
            float: the total stored food in millions of tons dry caloric

        Assumptions:

        buffer_ratio (float): the percent of the typical buffered stored food to keep at the end of the simulation.

        The stocks listed are tabulated at the end of the month.

        The minimum of any beginning month is a reasonable proxy for the very
        lowest levels stocks reach.

        Note: the optimizer will run through the stocks for the duration of
        each month. So, even starting at August (the minimum month), you would
        want to use the difference in stocks at the end of the previous month
        until the end of August to determine the stocks.

        """
        starting_month_index = starting_month - 1  # convert to zero indexed
        buffer_ratio = self.buffer_ratio
        end_of_month_stocks = self.end_of_month_stocks

        # lowest stock levels in baseline scenario (if buffer_ratio == 1)
        lowest_stocks = min(end_of_month_stocks)

        # month before simulation start
        month_before_index = starting_month_index - 1

        stocks_at_start_of_month = end_of_month_stocks[month_before_index]

        # stores at the start of the simulation
        self.TONS_DRY_CALORIC_EQIVALENT_SF = (
            stocks_at_start_of_month - lowest_stocks * buffer_ratio
        )

        # convert to billion kcals
        self.INITIAL_SF_KCALS = self.TONS_DRY_CALORIC_EQIVALENT_SF * 4e6 / 1e9
