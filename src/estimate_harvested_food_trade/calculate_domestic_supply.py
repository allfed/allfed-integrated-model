import numpy as np
import pandas as pd
import geopandas as gpd
from pathlib import Path

from estimate_outdoor_crops_by_country import get_new_columns_outdoor_crops


def add_monthly_reductions_to_trade_table(no_trade_table_no_monthly_reductions):
    """
    Adds new columns representing monthly reductions to the trade table based on external calculations.

    Parameters:
    - no_trade_table_no_monthly_reductions: The original pandas DataFrame without the monthly reduction columns.

    Returns:
    - A pandas DataFrame with new monthly reduction columns added.
    """

    # new_columns is a list of dictionaries returned from get_new_columns_outdoor_crops,
    # where each dictionary represents a new column to be added.
    new_columns = get_new_columns_outdoor_crops(no_trade_table_no_monthly_reductions)

    # Assuming each dictionary in new_columns has the same keys, representing the new column names,
    # and each key's value is a single value to be added to that column for the corresponding row.
    for column_name in new_columns[0].keys():
        # For each column name, extract the corresponding values for all rows and add it to the DataFrame.
        column_values = [row[column_name] for row in new_columns]
        no_trade_table_no_monthly_reductions[column_name] = column_values

    return no_trade_table_no_monthly_reductions


def determine_change_in_trade(matrix, crop_reductions_vector):
    """
    Calculates the expected difference in trade by multiplying a trade matrix with a vector of crop reductions.

    Parameters:
    - matrix: A square numpy array representing the trade matrix.
    - crop_reductions_vector: A numpy array representing the percentage reduction for each country.

    Returns:
    - A numpy array representing the adjusted trade values.
    """
    return matrix @ crop_reductions_vector


def alter_trade_matrix_with_monthly_reduction(trade_matrix, monthly_reduction_vector):
    """
    Adjusts the trade matrix based on monthly reduction factors for each country.

    Parameters:
    - trade_matrix: A square numpy array representing the trade matrix.
    - monthly_reduction_vector: A numpy array representing the monthly reduction for each country.

    Returns:
    - A numpy array representing the adjusted trade matrix.
    """
    monthly_reduction_matrix = np.diag(monthly_reduction_vector)
    return trade_matrix * monthly_reduction_matrix


def import_imports_exports(num_countries):
    """
    Creates an initial trade matrix filled with zeros based on the number of countries involved.

    Parameters:
    - num_countries: An integer representing the number of countries.

    Returns:
    - A square numpy array filled with zeros.
    """
    return np.zeros((num_countries, num_countries))


def calculate_domestic_supply(imports_minus_exports, domestic_production_vector):
    """
    Calculates the domestic supply by adding the net trade impact to the domestic production for each country.

    Parameters:
    - imports_minus_exports: A numpy array representing the difference between imports and exports for each country.
    - domestic_production_vector: A numpy array representing the domestic production for each country.

    Returns:
    - A numpy array representing the domestic supply for each country.
    """
    return imports_minus_exports + domestic_production_vector


def save_domestic_supply_data(original_df, domestic_supply_data, reduction_columns):
    """
    Appends domestic supply data to the original DataFrame and saves it as a CSV file.

    Parameters:
    - original_df: The original pandas DataFrame containing the base data.
    - domestic_supply_data: A list of numpy arrays representing the domestic supply data for each month.
    - reduction_columns: A list of column names in the original DataFrame representing monthly reductions.
    """
    domestic_supply_df = pd.DataFrame(domestic_supply_data).transpose()
    new_column_names = [
        col.replace("monthly_reduction", "domestic_supply") for col in reduction_columns
    ]
    domestic_supply_df.columns = new_column_names
    combined_df = pd.concat([original_df, domestic_supply_df], axis=1)
    repo_root = Path(__file__).parent
    output_path = repo_root / "computer_readable_combined_domestic_supply.csv"
    combined_df.to_csv(output_path, index=False)
    print(f"Saved updated data to {output_path}")


def get_no_trade_table():
    repo_root = Path(__file__).parent
    NO_TRADE_CSV = (
        repo_root / "data" / "no_food_trade" / "computer_readable_combined.csv"
    )
    no_trade_table = pd.read_csv(NO_TRADE_CSV)
    return no_trade_table


def main():
    no_trade_table_no_monthly_reductions = get_no_trade_table()

    no_trade_table = add_monthly_reductions_to_trade_table(
        no_trade_table_no_monthly_reductions
    )

    reduction_columns = [
        col for col in no_trade_table.columns if col.startswith("baseline_reduction_m")
    ]

    num_countries = len(reduction_columns)
    trade_matrix = import_imports_exports(num_countries)

    domestic_supply_monthly = []

    for month_index in range(len(reduction_columns)):
        reduction_column_name = reduction_columns[month_index]
        monthly_reduction_vector = no_trade_table[reduction_column_name].values
        adjusted_trade_matrix = alter_trade_matrix_with_monthly_reduction(
            trade_matrix, monthly_reduction_vector
        )
        change_in_trade = determine_change_in_trade(
            adjusted_trade_matrix, monthly_reduction_vector
        )

        domestic_production_vector = no_trade_table[f"KCALS_GROWN_NO_RELOCATION_m"{month_index}].values

        monthly_domestic_supply = calculate_domestic_supply(
            change_in_trade, domestic_production_vector
        )
        domestic_supply_monthly.append(monthly_domestic_supply)

    # Save the domestic supply data appended to the original DataFrame
    save_domestic_supply_data(
        no_trade_table, domestic_supply_monthly, reduction_columns
    )


if __name__ == "__main__":
    main()
