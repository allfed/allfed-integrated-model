"""
############################### Stored Food ###################################
##                                                                            #
##       Functions and constants relating to stocks and stored food           #
##                                                                            #
###############################################################################
"""
from src.food_system.food import Food


class StoredFood:
    def __init__(self, constants_for_params, outdoor_crops):
        """
        Initializes the StoredFood class, a child of the Food class.
    
        Args:
            constants_for_params (dict): A dictionary containing the constants for parameters.
            outdoor_crops (OutdoorCrops): An instance of the OutdoorCrops class.
    
        Returns:
            None
    
        """
        # call the __init__ method of the parent class
        super().__init__()
    
        # initialize the end of month stocks array with zeros
        self.end_of_month_stocks = [0] * 12
        # set the end of month stocks for each month from the constants for parameters
        self.end_of_month_stocks[0] = constants_for_params["END_OF_MONTH_STOCKS"]["JAN"]
        self.end_of_month_stocks[1] = constants_for_params["END_OF_MONTH_STOCKS"]["FEB"]
        self.end_of_month_stocks[2] = constants_for_params["END_OF_MONTH_STOCKS"]["MAR"]
        self.end_of_month_stocks[3] = constants_for_params["END_OF_MONTH_STOCKS"]["APR"]
        self.end_of_month_stocks[4] = constants_for_params["END_OF_MONTH_STOCKS"]["MAY"]
        self.end_of_month_stocks[5] = constants_for_params["END_OF_MONTH_STOCKS"]["JUN"]
        self.end_of_month_stocks[6] = constants_for_params["END_OF_MONTH_STOCKS"]["JUL"]
        self.end_of_month_stocks[7] = constants_for_params["END_OF_MONTH_STOCKS"]["AUG"]
        self.end_of_month_stocks[8] = constants_for_params["END_OF_MONTH_STOCKS"]["SEP"]
        self.end_of_month_stocks[9] = constants_for_params["END_OF_MONTH_STOCKS"]["OCT"]
        self.end_of_month_stocks[10] = constants_for_params["END_OF_MONTH_STOCKS"][
            "NOV"
        ]
        self.end_of_month_stocks[11] = constants_for_params["END_OF_MONTH_STOCKS"][
            "DEC"
        ]
    
        # (nuclear event in mid-may)
    
        # set the buffer ratio from the constants for parameters
        self.buffer_ratio = constants_for_params["BUFFER_RATIO"]
        # set the crop waste percentage from the constants for parameters
        self.CROP_WASTE = constants_for_params["WASTE"]["CROPS"]
    
        # set the stored food fraction of fat and protein from the outdoor crops object
        self.SF_FRACTION_FAT = outdoor_crops.OG_FRACTION_FAT
        self.SF_FRACTION_PROTEIN = outdoor_crops.OG_FRACTION_PROTEIN

    def calculate_stored_food_to_use(self, starting_month):
        """
        Calculates and returns total stored food available to use at start of
        simulation. While a baseline scenario will simply use the typical amount
        of stocks to keep the buffer at a typical usage, other more extreme
        scenarios should be expected to use a higher percentage of all stored food,
        eating into the typical buffer.
    
        Args:
            starting_month (int): The month the simulation starts on. 1=JAN, 2=FEB, ...,  12=DEC.
                (NOT TO BE CONFUSED WITH THE INDEX)
    
        Returns:
            float: The total stored food in millions of tons dry caloric.
    
        Assumptions:
            - buffer_ratio (float): The percent of the typical buffered stored food
              to keep at the end of the simulation.
            - The stocks listed are tabulated at the end of the month.
            - The minimum of any beginning month is a reasonable proxy for the very
              lowest levels stocks reach.
    
        Note:
            The optimizer will run through the stocks for the duration of each month.
            So, even starting at August (the minimum month), you would want to use the
            difference in stocks at the end of the previous month until the end of August
            to determine the stocks.
    
        Args:
            starting_month (int): The month the simulation starts on. 1=JAN, 2=FEB, ...,  12=DEC.
                (NOT TO BE CONFUSED WITH THE INDEX)
    
        Returns:
            float: The total stored food in millions of tons dry caloric.
    
        """
        # convert the starting month to a zero-indexed value
        starting_month_index = starting_month - 1
        # get the buffer ratio from the object
        buffer_ratio = self.buffer_ratio
        # get the end of month stocks from the object
        end_of_month_stocks = self.end_of_month_stocks
    
        # calculate the lowest stock levels in the baseline scenario (if buffer_ratio == 1)
        lowest_stocks = min(end_of_month_stocks)
    
        # calculate the index of the month before the simulation start
        month_before_index = starting_month_index - 1
    
        # calculate the stocks at the start of the simulation
        stocks_at_start_of_month = end_of_month_stocks[month_before_index]
    
        # calculate the total stored food available to use at the start of the simulation
        self.TONS_DRY_CALORIC_EQUIVALENT_SF = (
            stocks_at_start_of_month - lowest_stocks * buffer_ratio
        )
    
        # convert the stored food to billion kcals
        self.INITIAL_SF_KCALS = self.TONS_DRY_CALORIC_EQUIVALENT_SF * 4e6 / 1e9
    
        # create a Food object with the initial available stored food
        self.initial_available = Food(
            kcals=self.INITIAL_SF_KCALS * (1 - self.CROP_WASTE / 100),
            fat=(
                self.INITIAL_SF_KCALS
                * self.SF_FRACTION_FAT
                * (1 - self.CROP_WASTE / 100)
            ),
            protein=(
                self.INITIAL_SF_KCALS
                * self.SF_FRACTION_PROTEIN
                * (1 - self.CROP_WASTE / 100)
            ),
            kcals_units="billion kcals",
            fat_units="thousand tons",
            protein_units="thousand tons",
        )
