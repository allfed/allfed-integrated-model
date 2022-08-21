"""
This file runs a few tests on some import script functions to make sure they work

Created on Wed Jul 15

@author: morgan
"""
import numpy as np
from src.utilities.import_utilities import ImportUtilities


# should come to 3 average, 1e11 is an unreasonable percentage and should be rejected.
some_random_percentages = [-100, 3, 100, 0, 0, -16, 8, 8, 1e11]
avg = ImportUtilities.average_percentages([1, 2, 3])

weighted_average_percentages = [-100, 3, 150, 0, 0, -16, 4, 4, 1e11]
relative_importance = [1, 0, 2 / 3, 0, 0, 1 / 2, 1, 1, 1]
# multiplied                    -100  3  100  0  0  -8   4  4  np.nan
# actual average without nan: 0 (added all non-nan values)

weightings = np.array(relative_importance) / sum(relative_importance)

avg = ImportUtilities.weighted_average_percentages(
    weighted_average_percentages, weightings
)
assert avg == 0

weighted_average_percentages = [-100, -100, -100]
relative_importance = [1, 1, 1]
# weighted_average_percentages = [-3,3]
# relative_importance          = [1,1]
weightings = np.array(relative_importance) / sum(relative_importance)

avg = ImportUtilities.weighted_average_percentages(
    weighted_average_percentages, weightings
)

assert avg < -99.999 and avg > -100.0001

weighted_average_percentages = [-100, 100, 1e20]
relative_importance = [1, 1, 100]
weightings = np.array(relative_importance) / sum(relative_importance)

avg = ImportUtilities.weighted_average_percentages(
    weighted_average_percentages, weightings
)

assert avg == 0


weighted_average_percentages = [-100, 100, 1e20]
relative_importance = [1, 1, 100]
weightings = np.array(relative_importance) / sum(relative_importance)

# checks that the edge case of no reasonable values comes to nothing
avg = ImportUtilities.average_percentages([1e11, -101, 1e8, 1e26])
assert avg == 9.37e36  # we denote "nothing" by a very large unreasonable value
