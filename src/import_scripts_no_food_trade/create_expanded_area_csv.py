from pathlib import Path

import git
import numpy as np
import pandas as pd
from git.types import PathLike


def get_wheat_nutrients(repo_root: PathLike) -> pd.Series:
    """
    Retrieve nutritional information for wheat from
    the "Supplemental_Data.xlsx" file.
    NOTE: other crops are currently not available in the
    expanded area model therefore we specificlly fetch
    wheat only.
    We can refactor this when once we have more data.

    Arguments:
        repo_root (git.PathLike): the working directory of the repository,
            typically fetched via:
            `git.Repo(".", search_parent_directories=True).working_dir`

    Returns:
        pandas.Series: Calories, Fat and Protein per kg of wheat.
    """
    nutrition = pd.read_excel(
        Path(repo_root) / "data" / "Supplemental_Data.xlsx",
        sheet_name="Nutrition",
        usecols="A:D",
    )
    nutrition = nutrition.set_index(nutrition.columns[0])
    nutrition.columns = ["Calories", "Protein", "Fat"]
    wheat_nutrients = nutrition.loc["Wheat", :]
    return wheat_nutrients


def get_expanded_area_monthly(
    repo_root: PathLike, equipment_trade="no trade"
) -> pd.DataFrame:
    """
    Reads the expanded area model output CSV and
    converts appropriate data to a dataframe.


    Arguments:
        repo_root (git.PathLike): the working directory of the repository,
            typically fetched via:
            `git.Repo(".", search_parent_directories=True).working_dir`
        equipment_trade (str, optional): specifies expanded are model scenario.
            Can either be `no_trade` or `export_pool`. Defaults to `no_trade`.

    Returns:
        pandas.DataFrame: additional wheat yields per month per country
            from expanded area during a nuclear winter.
    """
    start_col = {
        "no_trade": 17,
        "export_pool": 128,
    }
    if equipment_trade not in start_col:
        print(f"Unknown equipment trade scenario: {equipment_trade}.")
        print("Using `no_trade`.")
        equipment_trade = "no_trade"
    expanded_area_yields = (
        pd.read_csv(
            Path(repo_root)
            / "data"
            / "no_food_trade"
            / "raw_data"
            / "luisa_expanded_planted_area.csv",
            index_col=False,
            dtype=str,
        )
        .iloc[16:-1, start_col[equipment_trade] : start_col[equipment_trade] + 87]
        .reset_index(drop=True)
    )
    expanded_area_yields.columns = expanded_area_yields.iloc[0]
    expanded_area_yields = expanded_area_yields.drop(expanded_area_yields.index[0])
    # NOTE: using "iloc" and other shenanigans here
    # because when using read_csv parameters `skiprows`
    # and `usecols`, the results were sometimes incorrect;
    # pandas would try to force str to be float for some reason
    # similar to these cases:
    # https://stackoverflow.com/questions/55503007/how-to-remove-the-0-when-reading-csv-with-pandas
    # https://stackoverflow.com/questions/54132508/pandas-adding-decimal-points-when-using-read-csv
    # however, my attempts to fix this failed.
    expanded_area_yields = expanded_area_yields.drop(
        columns=["Annual yield (kg per ha)"]
    ).set_index("Country (ISO 3DIGIT)")
    expanded_area_yields.index.name = "iso3"
    # we want 0=May; the start of the nuclear winter
    expanded_area_yields.columns = np.array(expanded_area_yields.columns, dtype=int) - 1
    expanded_area_yields = expanded_area_yields.drop(columns=-1)
    # we don't need countries with all NaNs
    expanded_area_yields = expanded_area_yields.apply(pd.to_numeric, errors="coerce")
    expanded_area_yields = expanded_area_yields.replace(0, np.nan)
    expanded_area_yields = expanded_area_yields.dropna(axis=0, how="all")
    expanded_area_yields = expanded_area_yields.replace(np.nan, 0)
    return expanded_area_yields


def calculate_yearly_yields(expanded_area_yields_monthly: pd.DataFrame) -> pd.DataFrame:
    """
    Convert monthly values to yearly yields.
    As we want to apply seasonality later on in the code,
    all we need is aggregate yearly values of the additional yields.

    Arguments:
        expanded_area_yields_monthly (pandas.DataFrame): Data frame containing
            monthly yields for each country.

    Returns:
        pandas.DataFrame: a data frame with yearly yields for each country.
    """
    expanded_area_yields_yearly = expanded_area_yields_monthly.copy()
    expanded_area_yields_yearly.columns = pd.to_datetime(
        expanded_area_yields_yearly.columns, unit="M"
    )
    expanded_area_yields_yearly = expanded_area_yields_yearly.T.resample("A").sum().T
    expanded_area_yields_yearly.columns = range(
        len(expanded_area_yields_yearly.columns)
    )
    return expanded_area_yields_yearly


def add_missing_years(expanded_area_yields_yearly: pd.DataFrame) -> pd.DataFrame:
    """
    Complete the data to conform with other data sets.
    As of wrighting this, we have 7 years of expanded area predictions,
    and assuming it plateaus after, we add columns with final 3 years
    to match the 10-year time spand of the other datasets.
    This can (and probably should) be modified to reflect actual
    yield predictions in the final 3 years.

    Arguments:
        expanded_area_yields_monthly (pandas.DataFrame): Data frame containing
            monthly yields for each country.

    Returns:
        pandas.DataFrame: a data frame with yearly yields for each country
            with additional years appended.
    """
    expanded_area_yields_yearly = pd.concat(
        [expanded_area_yields_yearly] + [expanded_area_yields_yearly.iloc[:, -1]] * 3,
        axis=1,
    )
    expanded_area_yields_yearly.columns = range(
        len(expanded_area_yields_yearly.columns)
    )
    return expanded_area_yields_yearly


def main():
    """
    Process expanded planted area model output data and create
    a CSV that can be later merged into the integrated model input files.
    """
    repo_root = git.Repo(".", search_parent_directories=True).working_dir
    print("Processing expanded planted area data.")
    wn = get_wheat_nutrients(repo_root)
    expanded_area_yields = {}
    for scenario in ["no_trade", "export_pool"]:
        eam = get_expanded_area_monthly(repo_root, scenario)
        eay = calculate_yearly_yields(eam)
        eay = add_missing_years(eay)
        # kg to kcal to dry caloric tonne
        eay_kcal = eay.mul(wn["Calories"]).div(4000 * 1000)
        eay_kcal.columns = [
            f"expanded_area_{scenario}_kcals_year" + str(c + 1) for c in eay.columns
        ]
        eay_fat = eay.mul(wn["Fat"]).div(1e3)  # in tonnes
        eay_fat.columns = [
            f"expanded_area_{scenario}_fat_year" + str(c + 1) for c in eay.columns
        ]
        eay_protein = eay.mul(wn["Protein"]).div(1e3)  # in tonnes
        eay_protein.columns = [
            f"expanded_area_{scenario}_protein_year" + str(c + 1) for c in eay.columns
        ]
        eay = pd.concat([eay_kcal, eay_fat, eay_protein], axis=1)
        eay = eay.sort_index()
        expanded_area_yields[scenario] = eay
    expanded_area_yields = pd.concat(expanded_area_yields.values(), axis=1)
    expanded_area_yields.to_csv(
        Path(repo_root)
        / "data"
        / "no_food_trade"
        / "processed_data"
        / "expanded_area.csv"
    )
    print("Saved expanded area macros to:")
    print(
        Path(repo_root)
        / "data"
        / "no_food_trade"
        / "processed_data"
        / "expanded_area.csv"
    )
    assert ~expanded_area_yields.isnull().to_numpy().any()


if __name__ == "__main__":
    main()
