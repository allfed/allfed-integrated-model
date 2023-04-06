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
    this_simulation["seasonality"] = "country"
    this_simulation["grasses"] = "baseline"
    this_simulation["crop_disruption"] = "zero"
    this_simulation["scenario"] = "no_resilient_foods"
    this_simulation["fish"] = "baseline"

    this_simulation["waste"] = "baseline_in_country"
    this_simulation["nutrition"] = "baseline"
    this_simulation["buffer"] = "baseline"
    this_simulation["shutoff"] = "continued"
    this_simulation["cull"] = "dont_eat_culled"

    # command line argument inputs (optional)
    scenario_runner = ScenarioRunnerNoTrade()
    scenario_runner.run_desired_simulation(this_simulation, args)


if __name__ == "__main__":
    args = sys.argv[1:]
    main(args)
