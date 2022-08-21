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

    country_names_with_EU_no_TWN = eu_27_p_uk_codes + country_names_no_EU_GBR_TWN

    def stack_on_list(list, layer):
        """
        create another layer on an existing stack of layers, or create the first
        layer in the stack

        example: adding [d,e,f] to a stack

        [
            [a,b,c]
        ]

        gives you

        [
            [a,b,c],
            [d,e,f]
        ]

        gets: the original list and the layer
        returns: the combined original and layer with the list stacked down below it

        """
        if len(list) == 0:
            list = layer
        else:
            list = np.vstack([list, layer])

        return list

    def add_row_to_csv(nw_csv, country, country_name, reductions):

        # convert to list of strings for saving as csv
        reduction_strings = [str(item) for item in reductions]

        to_save_row = np.append(country, np.append(country_name, reduction_strings))

        nw_csv = ImportUtilities.stack_on_list(nw_csv, to_save_row)

        return nw_csv

    def weighted_average_percentages(percentages, weights):
        """
        create a weighted average of percentages

        creates an average for a list of percentage reductions.
        Any non-possible number is removed. The remaining are averaged.
        If only non-possible numbers are included, then the result is a non-possible number

        9.37e36 is returned if things are not valid

        """
        assert len(percentages) == len(weights)
        assert sum(weights) <= 1.00001 and sum(weights) > 0.99999

        N_valid_percentages = 0
        mean_value = 0
        rejected_weighting_sum = 0
        non_rejected_weighting_sum = 0
        for i in range(0, len(percentages)):

            percentage = percentages[i]
            weight = weights[i]

            assert 0 <= weight <= 1

            if percentage > 1e5 or percentage < -100:
                # if this is a nonsensical percentage reduction
                rejected_weighting_sum += weight
            else:
                # if this is a sensible percentage reduction
                N_valid_percentages += 1
                mean_value += percentage * weight
                non_rejected_weighting_sum += weight

        if N_valid_percentages == 0:
            return 9.37e36

        # everything not rejected needs to be renormalized
        renormalization = 1 - rejected_weighting_sum
        if renormalization == 0:
            # the only nonzero weights were for invalid percentages
            return 9.37e36
        # make sure everything not rejected adds up to a weighting of 1
        assert (
            non_rejected_weighting_sum / renormalization >= 0.9999
            and non_rejected_weighting_sum / renormalization <= 1.0001
        )

        return mean_value / renormalization

    def average_percentages(percentages):
        """
        set up even weightings for the weighted average
        """

        array_length = len(percentages)

        even_weightings = [1 / array_length] * array_length
        assert round(sum(even_weightings), 8) == 1
        return ImportUtilities.weighted_average_percentages(
            percentages, even_weightings
        )

    def average_columns(vstack):
        """
        average all the columns and return the result as a row

        gets: vertical stack of columns

        returns: a single row with the averages

        """
        row = []
        for i in range(0, len(vstack[0])):
            reduction = ImportUtilities.average_percentages(vstack[i, :])
            row.append(reduction)
        return row

    def clean_up_eswatini(nw_csv):
        """
        change the swaziland country code from the FAOSTAT default to the USDA
        standard for compatibility with other datasets
        """
        swaziland_index = np.where(nw_csv[:, 0] == "SWZ")
        # eswatini recently changed from swaziland
        nw_csv[swaziland_index, 0] = "SWT"

        return nw_csv

    def import_csv(csv_loc, col_names, iso3_col_name):
        """
        import the csv and load into a dictionary
        """

        df = pd.read_csv(csv_loc)[col_names]
        country_codes = list(df[iso3_col_name].unique())
        # create dictionary containing each table, remove Area Code column
        input_table = {
            k: df[df[iso3_col_name] == k].drop(columns=iso3_col_name)
            for k in country_codes
        }

        return input_table
