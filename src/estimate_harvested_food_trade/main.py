"""
loads relevant data from the previous module, and runs the code in this model based on that input data
"""
if __name__ == "__main__":

    NO_TRADE_CSV = (
        Path(repo_root)
        / "data"
        / "no_food_trade"
        / "computer_readable_combined.csv"
    )

    no_trade_table = pd.read_csv(NO_TRADE_CSV)

    # import the visual map
    world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))

    # oddly, some of these were -99
    world.loc[world.name == "France", "iso_a3"] = "FRA"
    world.loc[world.name == "Norway", "iso_a3"] = "NOR"
    world.loc[world.name == "Kosovo", "iso_a3"] = "KOS"

    # iterate over each country from spreadsheet, and compute that country's nuclear winter and outdoor growing data 

    additional_csv_columns = [] # a list of additional columns produced from this analysis involving partial trade
    for index, country_data in no_trade_table.iterrows():
        
