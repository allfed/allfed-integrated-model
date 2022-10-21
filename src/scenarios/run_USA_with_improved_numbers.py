"""
This file contains the code for the baseline model by country for with and
without trade scenarios.

Created on Wed Jul 15
@author: morgan
"""
import sys
from src.scenarios.run_model_no_trade import ScenarioRunnerNoTrade


def main(args):
    this_simulation = {}

    this_simulation["scale"] = "country"
    this_simulation["scenario"] = "with_resilient_foods"
    this_simulation["seasonality"] = "no_seasonality"
    this_simulation["grasses"] = "country_nuclear_winter"
    this_simulation["crop_disruption"] = "country_nuclear_winter"
    this_simulation["fish"] = "nuclear_winter"

    this_simulation["waste"] = "baseline_in_country"
    this_simulation["fat"] = "not_required"
    this_simulation["protein"] = "not_required"
    this_simulation["nutrition"] = "catastrophe"
    this_simulation["buffer"] = "zero"
    this_simulation["shutoff"] = "reduce_breeding_USA"
    this_simulation["cull"] = "do_eat_culled"
    this_simulation["meat_strategy"] = "reduce_breeding_USA"

    # command line argument inputs (optional)
    scenario_runner = ScenarioRunnerNoTrade()

    scenario_runner.run_model_no_trade(
        title="Reproduce Xia et al Results",
        create_pptx_with_all_countries=False,
        show_country_figures=False,
        show_map_figures=True,
        add_map_slide_to_pptx=False,
        scenario_option=this_simulation,
        countries_list=["USA"],
        #     "CHN",
        #     "FRA",
        #     "IND",
        #     "ISR",
        #     "PRK",
        #     "PAK",
        #     "RUS",
        #     "F5707+GBR",
        #     "USA",
        # ],
    )


if __name__ == "__main__":
    args = sys.argv[1:]
    main(args)
