import numpy as np
import pandas as pd


class ImportUtilities:
    """
    This class contains methods for importing data from various sources.
    """

    iso3_no_EU_GBR_TWN = [
        "AFG",
        "ALB",
        "DZA",
        "AGO",
        "ARG",
        "ARM",
        "AUS",
        "AZE",
        "BHR",
        "BGD",
        "BRB",
        "BLR",
        "BEN",
        "BTN",
        "BOL",
        "BIH",
        "BWA",
        "BRA",
        "BRN",
        "BFA",
        "MMR",
        "BDI",
        "CPV",
        "KHM",
        "CMR",
        "CAN",
        "CAF",
        "TCD",
        "CHL",
        "CHN",
        "COL",
        "COD",
        "COG",
        "CRI",
        "CIV",
        "CUB",
        "DJI",
        "DOM",
        "ECU",
        "EGY",
        "SLV",
        "ERI",
        "SWZ",
        "ETH",
        "FJI",
        "GAB",
        "GMB",
        "GEO",
        "GHA",
        "GTM",
        "GIN",
        "GNB",
        "GUY",
        "HTI",
        "HND",
        "IND",
        "IDN",
        "IRN",
        "IRQ",
        "ISR",
        "JAM",
        "JPN",
        "JOR",
        "KAZ",
        "KEN",
        "KOR",
        "PRK",
        "KWT",
        "KGZ",
        "LAO",
        "LBN",
        "LSO",
        "LBR",
        "LBY",
        "MDG",
        "MWI",
        "MYS",
        "MLI",
        "MRT",
        "MUS",
        "MEX",
        "MDA",
        "MNG",
        "MAR",
        "MOZ",
        "NAM",
        "NPL",
        "NZL",
        "NIC",
        "NER",
        "NGA",
        "MKD",
        "NOR",
        "OMN",
        "PAK",
        "PAN",
        "PNG",
        "PRY",
        "PER",
        "PHL",
        "QAT",
        "RUS",
        "RWA",
        "SAU",
        "SEN",
        "SRB",
        "SLE",
        "SGP",
        "SOM",
        "ZAF",
        "SSD",
        "LKA",
        "SDN",
        "SUR",
        "CHE",
        "SYR",
        "TJK",
        "TZA",
        "THA",
        "TGO",
        "TTO",
        "TUN",
        "TUR",
        "TKM",
        "UGA",
        "UKR",
        "ARE",
        "USA",
        "URY",
        "UZB",
        "VEN",
        "VNM",
        "YEM",
        "ZMB",
        "ZWE",
    ]

    eu_27_p_uk_codes = [
        "GBR",
        "AUT",
        "BEL",
        "BGR",
        "HRV",
        "CYP",
        "CZE",
        "DNK",
        "EST",
        "FIN",
        "FRA",
        "DEU",
        "GRC",
        "HUN",
        "IRL",
        "ITA",
        "LVA",
        "LTU",
        "LUX",
        "MLT",
        "NLD",
        "POL",
        "PRT",
        "ROU",
        "SVK",
        "SVN",
        "ESP",
        "SWE",
    ]

    country_names_no_EU_GBR_TWN = [
        "Afghanistan",
        "Albania",
        "Algeria",
        "Angola",
        "Argentina",
        "Armenia",
        "Australia",
        "Azerbaijan",
        "Bahrain",
        "Bangladesh",
        "Barbados",
        "Belarus",
        "Benin",
        "Bhutan",
        "Bolivia (Plurinational State of)",
        "Bosnia and Herzegovina",
        "Botswana",
        "Brazil",
        "Brunei Darussalam",
        "Burkina Faso",
        "Myanmar",
        "Burundi",
        "Cabo Verde",
        "Cambodia",
        "Cameroon",
        "Canada",
        "Central African Republic",
        "Chad",
        "Chile",
        "China",
        "Colombia",
        "Congo",
        "Democratic Republic of the Congo",
        "Costa Rica",
        "Cote d'Ivoire",
        "Cuba",
        "Djibouti",
        "Dominican Republic",
        "Ecuador",
        "Egypt",
        "El Salvador",
        "Eritrea",
        "Eswatini",
        "Ethiopia",
        "Fiji",
        "Gabon",
        "Gambia",
        "Georgia",
        "Ghana",
        "Guatemala",
        "Guinea",
        "Guinea-Bissau",
        "Guyana",
        "Haiti",
        "Honduras",
        "India",
        "Indonesia",
        "Iran (Islamic Republic of)",
        "Iraq",
        "Israel",
        "Jamaica",
        "Japan",
        "Jordan",
        "Kazakhstan",
        "Kenya",
        "Democratic People's Republic of Korea",
        "Republic of Korea",
        "Kuwait",
        "Kyrgyzstan",
        "Lao People's Democratic Republic",
        "Lebanon",
        "Lesotho",
        "Liberia",
        "Libya",
        "Madagascar",
        "Malawi",
        "Malaysia",
        "Mali",
        "Mauritania",
        "Mauritius",
        "Mexico",
        "Republic of Moldova",
        "Mongolia",
        "Morocco",
        "Mozambique",
        "Namibia",
        "Nepal",
        "New Zealand",
        "Nicaragua",
        "Niger",
        "Nigeria",
        "North Macedonia",
        "Norway",
        "Oman",
        "Pakistan",
        "Panama",
        "Papua New Guinea",
        "Paraguay",
        "Peru",
        "Philippines",
        "Qatar",
        "Russian Federation",
        "Rwanda",
        "Saudi Arabia",
        "Senegal",
        "Serbia",
        "Sierra Leone",
        "Singapore",
        "Somalia",
        "South Africa",
        "South Sudan",
        "Sri Lanka",
        "Sudan",
        "Suriname",
        "Switzerland",
        "Syrian Arab Republic",
        "Tajikistan",
        "United Republic of Tanzania",
        "Thailand",
        "Togo",
        "Trinidad and Tobago",
        "Tunisia",
        "Turkiye",
        "Turkmenistan",
        "Uganda",
        "Ukraine",
        "United Arab Emirates",
        "United States of America",
        "Uruguay",
        "Uzbekistan",
        "Venezuela (Bolivarian Republic of)",
        "Viet Nam",
        "Yemen",
        "Zambia",
        "Zimbabwe",
    ]

    eu_27_p_uk_country_names = [
        "United Kingdom",
        "Austria",
        "Belgium",
        "Bulgaria",
        "Croatia",
        "Cyprus",
        "Czech Republic",
        "Denmark",
        "Estonia",
        "Finland",
        "France",
        "Germany",
        "Greece",
        "Hungary",
        "Ireland",
        "Italy",
        "Latvia",
        "Lithuania",
        "Luxembourg",
        "Malta",
        "Netherlands",
        "Poland",
        "Portugal",
        "Romania",
        "Slovakia",
        "Slovenia",
        "Spain",
        "Sweden",
    ]

    countries_with_TWN_F5707_GBR = iso3_no_EU_GBR_TWN + ["TWN", "F5707+GBR"]
    country_names_with_TWN_F5707_GBR = country_names_no_EU_GBR_TWN + [
        "Taiwan",
        "European Union (27) + UK",
    ]
    countries_with_TWN_F5707_GBR_separate = iso3_no_EU_GBR_TWN + ["TWN", "F5707", "GBR"]
    country_names_with_TWN_F5707_GBR_separate = country_names_no_EU_GBR_TWN + [
        "Taiwan",
        "European Union (27)",
        "United Kingdom",
    ]

    countries_with_EU_no_TWN = eu_27_p_uk_codes + iso3_no_EU_GBR_TWN
    country_names_with_EU_no_TWN = (
        eu_27_p_uk_country_names + country_names_no_EU_GBR_TWN
    )

    country_codes = countries_with_EU_no_TWN + ["TWN"]

    country_names = country_names_with_EU_no_TWN + ["Taiwan"]

    def stack_on_list(list, layer):
        """
        This function creates another layer on an existing stack of layers, or creates the first
        layer in the stack. It takes in the original list and the layer to be added, and returns
        the combined original and layer with the list stacked down below it.

        Example:
            If we have an existing list [a,b,c] and we want to add [d,e,f] to it, we can call the
            function like this:
            stack_on_list([a,b,c], [d,e,f])

            This will give us:
            [
                [a,b,c],
                [d,e,f]
            ]

        Args:
            list (numpy.ndarray): The original list to which the layer is to be added
            layer (numpy.ndarray): The layer to be added to the original list

        Returns:
            numpy.ndarray: The combined list with the layer stacked down below it
        """
        if len(list) == 0:
            # If the original list is empty, we simply set it to the layer
            list = layer
        else:
            # If the original list is not empty, we stack the layer below it using numpy's vstack function
            list = np.vstack([list, layer])

        return list

    def add_row_to_csv(nw_csv, country, country_name, reductions):
        """
        Adds a row to a CSV file.

        Args:
            nw_csv (List[List[str]]): The CSV file to add a row to.
            country (str): The country to add to the row.
            country_name (str): The name of the country to add to the row.
            reductions (List[float]): A list of reduction values to add to the row.

        Returns:
            List[List[str]]: The updated CSV file with the new row added.
        """
        # convert to list of strings for saving as csv
        reduction_strings = [str(item) for item in reductions]

        # create the row to save
        to_save_row = np.append(country, np.append(country_name, reduction_strings))

        # add the row to the CSV file
        nw_csv = ImportUtilities.stack_on_list(nw_csv, to_save_row)

        return nw_csv

    def weighted_average_percentages(percentages, weights):
        """
        Calculates the weighted average of a list of percentage reductions.

        Args:
            percentages (list): A list of percentage reductions.
            weights (list): A list of weights corresponding to the percentages.

        Returns:
            float: The weighted average of the percentages.

        Raises:
            AssertionError: If the length of the percentages and weights lists are not equal.
            AssertionError: If the sum of the weights is not between 0.99999 and 1.00001.

        The function calculates the weighted average of a list of percentage reductions.
        Any non-possible number is removed. The remaining are averaged.
        If only non-possible numbers are included, then the result is a non-possible number.

        A percentage reduction is considered non-possible if it is greater than 1e5 or less than -100.

        If there are no valid percentages, the function returns 9.37e36.

        """
        # Check that the lengths of the percentages and weights lists are equal
        assert len(percentages) == len(weights)
        # Check that the sum of the weights is between 0.99999 and 1.00001
        assert sum(weights) <= 1.00001 and sum(weights) > 0.99999

        # Initialize variables
        N_valid_percentages = 0
        mean_value = 0
        rejected_weighting_sum = 0
        non_rejected_weighting_sum = 0

        # Loop through the percentages and weights
        for i in range(0, len(percentages)):
            percentage = percentages[i]
            weight = weights[i]

            # Check that the weight is between 0 and 1
            assert 0 <= weight <= 1

            if percentage > 1e5 or percentage < -100:
                # If this is a nonsensical percentage reduction, add the weight to the rejected_weighting_sum
                rejected_weighting_sum += weight
            else:
                # If this is a sensible percentage reduction, add the percentage times the weight to the mean_value
                # and add the weight to the non_rejected_weighting_sum
                N_valid_percentages += 1
                mean_value += percentage * weight
                non_rejected_weighting_sum += weight

        if N_valid_percentages == 0:
            # If there are no valid percentages, return 9.37e36
            return 9.37e36

        # Calculate the renormalization factor
        renormalization = 1 - rejected_weighting_sum

        if renormalization == 0:
            # If the only nonzero weights were for invalid percentages, return 9.37e36
            return 9.37e36

        # Check that everything not rejected adds up to a weighting of 1
        assert (
            non_rejected_weighting_sum / renormalization >= 0.9999
            and non_rejected_weighting_sum / renormalization <= 1.0001
        )

        # Return the mean value divided by the renormalization factor
        return mean_value / renormalization

    def average_percentages(percentages):
        """
        This function calculates the weighted average of a list of percentages.
        The weightings are set up to be even across all percentages.

        Args:
            percentages (list): A list of percentages to be averaged.

        Returns:
            float: The weighted average of the percentages.
        """

        # Calculate the length of the input list
        array_length = len(percentages)

        # Set up even weightings for the weighted average
        even_weightings = [1 / array_length] * array_length

        # Check that the sum of the weightings is equal to 1
        assert round(sum(even_weightings), 8) == 1

        # Calculate the weighted average using the even weightings
        return ImportUtilities.weighted_average_percentages(
            percentages, even_weightings
        )

    def average_columns(vstack):
        """
        This function takes a vertical stack of columns and returns a single row with the averages of each column.

        Args:
            vstack (numpy.ndarray): A vertical stack of columns.

        Returns:
            list: A single row with the averages of each column.

        Example:
            >>> import numpy as np
            >>> vstack = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
            >>> average_columns(vstack)
            [4.0, 5.0, 6.0]
        """
        row = []
        for i in range(0, len(vstack[0])):
            # Calculate the average of each column using the average_percentages function from ImportUtilities
            reduction = ImportUtilities.average_percentages(vstack[i, :])
            row.append(reduction)
        return row

    def clean_up_eswatini(nw_csv):
        """
        This function changes the country code for Swaziland from the FAOSTAT default to the USDA
        standard for compatibility with other datasets. It does this by finding the index of the
        Swaziland country code in the input numpy array and changing it to the new country code
        for Eswatini.

        Args:
            nw_csv (numpy.ndarray): A numpy array containing country codes and other data

        Returns:
            numpy.ndarray: The input numpy array with the Swaziland country code changed to Eswatini
        """

        # Find the index of the Swaziland country code in the input numpy array
        swaziland_index = np.where(nw_csv[:, 0] == "SWZ")

        # Change the Swaziland country code to the new country code for Eswatini
        nw_csv[swaziland_index, 0] = "SWT"

        # Return the modified numpy array
        return nw_csv

    def import_csv(csv_loc, col_names, iso3_col_name):
        """
        This function imports a CSV file into a pandas dataframe and calls the import_csv_from_df function.

        Args:
            csv_loc (str): The file path of the CSV file to be imported.
            col_names (list): A list of column names to be included in the dataframe.
            iso3_col_name (str): The name of the column containing the ISO3 country codes.

        Returns:
            pandas.DataFrame: A dataframe containing the specified columns from the CSV file.

        Example:
            >>> import_csv('data.csv', ['col1', 'col2', 'col3'], 'iso3_code')
        """

        # Read the CSV file and select the specified columns
        df = pd.read_csv(csv_loc)[col_names]

        # Call the import_csv_from_df function from the ImportUtilities module
        return ImportUtilities.import_csv_from_df(df, iso3_col_name)

    def import_csv_from_df(df, iso3_col_name):
        """
        This function takes a pandas dataframe and a column name as input and returns a dictionary
        containing each table for each unique value in the specified column.

        Args:
            df (pandas.DataFrame): The input dataframe
            iso3_col_name (str): The name of the column containing the unique values

        Returns:
            dict: A dictionary containing each table for each unique value in the specified column
        """

        # get list of unique values in the specified column
        country_codes = list(df[iso3_col_name].unique())

        # create dictionary containing each table, remove the specified column
        input_table = {
            k: df[df[iso3_col_name] == k].drop(columns=iso3_col_name)
            for k in country_codes
        }

        return input_table
