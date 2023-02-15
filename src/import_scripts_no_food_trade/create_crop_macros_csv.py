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
        self.NUTRITION_XLS = Path(repo_root) / "data" / "Supplemental_Data.xlsx"
        self.PRODUCTION_CSV = (
            Path(repo_root)
            / "data"
            / "no_food_trade"
            / "raw_data"
            / "FAOSTAT_food_production_2020.csv"
        )

        self.TONS_TO_KG = 1e3
        self.KCALS_TO_DRY_CALORIC_TONS = 1 / (4000 * 1000)

        self.KCALS_PER_PERSON = 2100
        self.FAT_PER_PERSON = 47
        self.PROTEIN_PER_PERSON = 53

        self.products, self.nutrition = self.import_nutrients_and_products()

    def import_nutrients_and_products(self):
        # Data Inspection

        xls = pd.ExcelFile(self.NUTRITION_XLS)
        nutrition = pd.read_excel(xls, "Nutrition")[
            ["Item", "Calories", "Protein", "Fat"]
        ]

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

        products = ImportUtilities.import_csv(
            self.PRODUCTION_CSV, production_col_names, iso3_code
        )

        return products, nutrition

    def get_kcals_matching(self, match_strings, products):
        """
        Returns the sum of kcals, fat, and protein for the products that the passed in
        name as a substring of the product name string.
        """
        all_matching_products = pd.DataFrame([])
        for string in match_strings:
            string_lower = string.lower()

            matching_products = products.loc[
                products["Item"].str.contains(string_lower, case=False)
            ]

            all_matching_products = pd.concat(
                [all_matching_products, matching_products]
            )
        all_matching_products.drop_duplicates(subset=["Item"], inplace=True)

        kcals, fat, protein = self.get_nutrients(all_matching_products)
        return kcals

    def get_nutrients(self, products):
        """
        Returns the sum of kcals, fat, and protein for the products passed in.
        """
        kcals_sum = 0
        fat_sum = 0
        protein_sum = 0
        # for each food product, add to each macronutrient total
        for index, product in products.iterrows():
            # find the particular item.
            n = self.nutrition[self.nutrition["Item"] == product["Item"]]

            # if the match could not be found, continue
            if len(n) == 0:
                continue

            # there should never be any duplicate nutrition items
            assert len(n) == 1

            kcals_per_kg = float(n["Calories"])  # kcals / kg
            fat_frac = float(n["Fat"])  # fraction by weight
            protein_frac = float(n["Protein"])  # fraction by weight

            # production Calories is units tons per year
            if np.isnan(product["Value"]):
                tons = 0
            else:
                tons = product["Value"]

            # dry caloric tons per year
            kcals = (
                tons * self.TONS_TO_KG * kcals_per_kg * self.KCALS_TO_DRY_CALORIC_TONS
            )

            # nutrition Fat and protein are percent by weight, converting to grams
            fat = tons * fat_frac  # tons per year
            protein = tons * protein_frac  # tons per year

            kcals_sum += kcals
            fat_sum += fat
            protein_sum += protein

        return [kcals_sum, fat_sum, protein_sum]

    def get_macros_csv(self):
        """
        get the stack of macronutrients that correspond to each country
        """
        iso3_codes = ImportUtilities.country_codes
        country_names = ImportUtilities.country_names

        macros_csv = np.array(
            [
                "iso3",
                "country",
                "crop_kcals",
                "crop_fat",
                "crop_protein",
            ]
        )

        for i in range(0, len(iso3_codes)):
            iso3_code = iso3_codes[i]
            country_name = country_names[i]
            if iso3_code not in self.products.keys():
                print("missing" + iso3_code)
                continue

            products = self.products[iso3_code]

            [kcals_sum, fat_sum, protein_sum] = self.get_nutrients(products)

            new_layer = [
                iso3_code,
                country_name,
                str(kcals_sum),
                str(fat_sum),
                str(protein_sum),
            ]

            macros_csv = ImportUtilities.stack_on_list(macros_csv, new_layer)

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
