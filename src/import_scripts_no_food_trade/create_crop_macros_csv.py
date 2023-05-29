"""
This file contains the code for importing crop production macronutrients
using the production of each crop combined with the nutrition of the crops.

@author: morgan
"""

import pandas as pd
import numpy as np
from src.utilities.import_utilities import ImportUtilities
import git
from pathlib import Path

repo_root = git.Repo(".", search_parent_directories=True).working_dir


class CropMacros:
    def __init__(self):
        """
        Initializes the class with necessary constants and imports nutrient and product data.
        """
        # Set paths to nutrition data and food production data
        self.NUTRITION_XLS = Path(repo_root) / "data" / "Supplemental_Data.xlsx"
        self.PRODUCTION_CSV = (
            Path(repo_root)
            / "data"
            / "no_food_trade"
            / "raw_data"
            / "FAOSTAT_food_production_2020.csv"
        )

        # Set conversion factors
        self.TONS_TO_KG = 1e3
        self.KCALS_TO_DRY_CALORIC_TONS = 1 / (4000 * 1000)

        # Set daily nutrient requirements per person
        self.KCALS_PER_PERSON = 2100
        self.FAT_PER_PERSON = 47
        self.PROTEIN_PER_PERSON = 53

        # Import nutrient and product data
        self.products, self.nutrition = self.import_nutrients_and_products()

    def import_nutrients_and_products(self):
        """
        This function imports nutrition and production data from Excel and CSV files respectively.
        It returns two dataframes: products and nutrition.

        Args:
            self (object): instance of the class

        Returns:
            tuple: a tuple containing two dataframes: products and nutrition
        """

        # Import nutrition data from Excel file
        xls = pd.ExcelFile(self.NUTRITION_XLS)
        nutrition = pd.read_excel(xls, "Nutrition")[
            ["Item", "Calories", "Protein", "Fat"]
        ]

        # Define column names for production data
        iso3_code = "Area Code (ISO3)"
        production_col_names = [
            iso3_code,
            "Area",
            "Element",
            "Item Code (FAO)",
            "Item",
            "Unit",
            "Value",
        ]

        # Import production data from CSV file
        products = ImportUtilities.import_csv(
            self.PRODUCTION_CSV, production_col_names, iso3_code
        )

        # Return the two dataframes
        return products, nutrition

    def get_kcals_matching(self, match_strings, products):
        """
        Returns the sum of kcals, fat, and protein for the products that the passed in
        name as a substring of the product name string.

        Args:
            match_strings (list): A list of strings to match against the product names
            products (pandas.DataFrame): A pandas DataFrame containing product information

        Returns:
            float: The sum of kcals for the matching products

        """
        # Create an empty DataFrame to store all matching products
        all_matching_products = pd.DataFrame([])

        # Loop through each match string
        for string in match_strings:
            # Convert the string to lowercase for case-insensitive matching
            string_lower = string.lower()

            # Filter the products DataFrame to only include products with the match string in the name
            matching_products = products.loc[
                products["Item"].str.contains(string_lower, case=False)
            ]

            # Add the matching products to the all_matching_products DataFrame
            all_matching_products = pd.concat(
                [all_matching_products, matching_products]
            )

        # Remove any duplicate products from the all_matching_products DataFrame
        all_matching_products.drop_duplicates(subset=["Item"], inplace=True)

        # Get the total kcals, fat, and protein for the matching products
        kcals, fat, protein = self.get_nutrients(all_matching_products)

        # Return the total kcals for the matching products
        return kcals

    def get_nutrients(self, products):
        """
        Returns the sum of kcals, fat, and protein for the products passed in.

        Args:
            products (pandas.DataFrame): A DataFrame containing food products and their values.

        Returns:
            list: A list containing the sum of kcals, fat, and protein for the products passed in.
        """

        # Initialize variables to hold the sum of kcals, fat, and protein
        kcals_sum = 0
        fat_sum = 0
        protein_sum = 0

        # For each food product, add to each macronutrient total
        for index, product in products.iterrows():
            # Find the particular item in the nutrition DataFrame
            n = self.nutrition[self.nutrition["Item"] == product["Item"]]

            # If the match could not be found, continue to the next product
            if len(n) == 0:
                continue

            # There should never be any duplicate nutrition items
            assert len(n) == 1

            # Get the kcals, fat, and protein values for the product
            kcals_per_kg = float(n["Calories"])  # kcals / kg
            fat_frac = float(n["Fat"])  # fraction by weight
            protein_frac = float(n["Protein"])  # fraction by weight

            # Production Calories is units tons per year
            if np.isnan(product["Value"]):
                tons = 0
            else:
                tons = product["Value"]

            # Calculate the dry caloric tons per year
            kcals = (
                tons * self.TONS_TO_KG * kcals_per_kg * self.KCALS_TO_DRY_CALORIC_TONS
            )

            # Convert nutrition Fat and protein from percent by weight to grams
            fat = tons * fat_frac  # tons per year
            protein = tons * protein_frac  # tons per year

            # Add the kcals, fat, and protein values to their respective sums
            kcals_sum += kcals
            fat_sum += fat
            protein_sum += protein

        # Return the sum of kcals, fat, and protein for the products passed in
        return [kcals_sum, fat_sum, protein_sum]

    def get_macros_csv(self):
        """
        This function generates a stack of macronutrients that correspond to each country.
        It loops through all the countries and their corresponding ISO3 codes, and for each country,
        it calculates the total kcals, fat, and protein produced by all crops in that country.
        It then adds this information to a numpy array and returns it.

        Returns:
            numpy.ndarray: A numpy array containing the following columns:
                - iso3: The ISO3 code of the country
                - country: The name of the country
                - crop_kcals: The total kcals produced by all crops in the country
                - crop_fat: The total fat produced by all crops in the country
                - crop_protein: The total protein produced by all crops in the country
        """
        # Get the ISO3 codes and country names
        iso3_codes = ImportUtilities.country_codes
        country_names = ImportUtilities.country_names

        # Create the numpy array with the column names
        macros_csv = np.array(
            [
                "iso3",
                "country",
                "crop_kcals",
                "crop_fat",
                "crop_protein",
            ]
        )

        # Loop through all the countries
        for i in range(0, len(iso3_codes)):
            iso3_code = iso3_codes[i]
            country_name = country_names[i]

            # If the country is not in the products dictionary, skip it
            if iso3_code not in self.products.keys():
                print("missing" + iso3_code)
                continue

            # Get the products for the country
            products = self.products[iso3_code]

            # Calculate the total kcals, fat, and protein produced by all crops in the country
            [kcals_sum, fat_sum, protein_sum] = self.get_nutrients(products)

            # Add the information to the numpy array
            new_layer = [
                iso3_code,
                country_name,
                str(kcals_sum),
                str(fat_sum),
                str(protein_sum),
            ]
            macros_csv = ImportUtilities.stack_on_list(macros_csv, new_layer)

        # Return the numpy array
        return macros_csv


if __name__ == "__main__":
    print("importing baseline crop kcals, fat, protein production data...")

    cm = CropMacros()

    macros_csv = cm.get_macros_csv()
    macros_csv = ImportUtilities.clean_up_eswatini(macros_csv)

    np.savetxt(
        Path(repo_root) / "data" / "no_food_trade" / "processed_data/macros_csv.csv",
        macros_csv,
        delimiter=",",
        fmt="%s",
    )
