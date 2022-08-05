#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

This function runs a single optimization by computing the parameters,
running the parameters onto the optimizer, extracting the results, and interpreting the 
results into more useful values for plotting and scenario evaluation

Created on Tue Jul 19

@author: morgan
"""
import os
import sys

from pulp import constants

module_path = os.path.abspath(os.path.join("../.."))
if module_path not in sys.path:
    sys.path.append(module_path)

# import some python files from this integrated model repository
from src.optimizer.optimizer import Optimizer
from src.optimizer.parameters import Parameters
from src.optimizer.interpret_results import Interpreter
from src.optimizer.extract_results import Extractor
from src.scenarios.scenarios import Scenarios
from src.optimizer.validate_results import Validator
from src.optimizer.parameters import Parameters


class ScenarioRunner:
    def __init__(self):
        pass

    def run_and_analyze_scenario(self, constants_for_params, scenarios_loader):
        """
        computes params, Runs the optimizer, extracts data from optimizer, interprets
        the results, validates the results, and optionally prints an output with people
        fed.

        arguments: constants from the scenario, scenario loader (to print the aspects
        of the scenario and check no scenario parameter has been set twice or left
        unset)

        returns: the interpreted results
        """
        interpreter = Interpreter()
        validator = Validator()

        # take the variables defining the scenario and compute the resulting needed
        # values as inputs to the optimizer
        (
            single_valued_constants,
            multi_valued_constants,
        ) = self.compute_parameters(constants_for_params, scenarios_loader)

        # actually make PuLP optimize effective people fed based on all the constants
        # we've determined
        (
            model,
            variables,
            single_valued_constants,
            multi_valued_constants,
        ) = self.run_optimizer(single_valued_constants, multi_valued_constants)

        extractor = Extractor(single_valued_constants)
        #  get values from all the optimizer in list and integer formats
        extracted_results = extractor.extract_results(
            model, variables, single_valued_constants, multi_valued_constants
        )

        # TODO: eventually all the values not directly solved by the optimizer should
        # be removed from extracted_results

        #  interpret the results, nicer for plotting, reporting, and printing results
        interpreted_results = interpreter.interpret_results(
            extracted_results, multi_valued_constants
        )

        # ensure no errors were made in the extraction and interpretation, or if the
        # optimizer did not correctly satisfy constraints within a reasonable margin
        # of error
        validator.validate_results(model, extracted_results, interpreted_results)

        PRINT_NEEDS_RATIO = False
        if PRINT_NEEDS_RATIO:
            interpreter.print_kcals_per_capita_per_day(interpreted_results)

        return interpreted_results

    def compute_parameters(self, constants_for_params, scenarios_loader):
        """
        computes the parameters
        returns the resulting constants
        """
        constants = {}
        constants["inputs"] = constants_for_params

        constants_loader = Parameters()

        (
            single_valued_constants,
            multi_valued_constants,
        ) = constants_loader.computeParameters(constants, scenarios_loader)

        return (single_valued_constants, multi_valued_constants)

    def run_optimizer(self, single_valued_constants, multi_valued_constants):
        """
        Runs the optimizer and returns the model, variables, and constants
        """
        optimizer = Optimizer()
        validator = Validator()

        (
            model,
            variables,
            maximize_constraints,
            single_valued_constants,
            multi_valued_constants,
        ) = optimizer.optimize(single_valued_constants, multi_valued_constants)

        CHECK_CONSTRAINTS = False
        if CHECK_CONSTRAINTS:
            print("")
            print("VALIDATION")
            print("")
            print("")
            # check all the mathematically defined constraints in the optimizer are
            # satisfied within reasonable rounding errors
            validator.check_constraints_satisfied(
                model,
                maximize_constraints,
                model.variables(),
            )

        return (model, variables, single_valued_constants, multi_valued_constants)

    def set_depending_on_option(self, country_data, scenario_option):
        scenario_loader = Scenarios()

        if scenario_option["scale"] == "global":
            constants_for_params = scenario_loader.init_global_food_system_properties()
        if scenario_option["scale"] == "country":
            constants_for_params = scenario_loader.init_country_food_system_properties(
                country_data
            )

        if scenario_option["shutoff"] == "immediate":
            constants_for_params = scenario_loader.set_immediate_shutoff(
                constants_for_params
            )
        if scenario_option["shutoff"] == "short_delayed_shutoff":
            constants_for_params = scenario_loader.set_short_delayed_shutoff(
                constants_for_params
            )
        if scenario_option["shutoff"] == "long_delayed_shutoff":
            constants_for_params = scenario_loader.set_long_delayed_shutoff(
                constants_for_params
            )
        if scenario_option["shutoff"] == "continued":
            constants_for_params = scenario_loader.set_continued_feed_biofuels(
                constants_for_params
            )

        if scenario_option["waste"] == "zero":
            constants_for_params = scenario_loader.set_waste_to_zero(
                constants_for_params
            )
        if scenario_option["waste"] == "tripled_prices_in_country":
            constants_for_params = scenario_loader.set_global_waste_to_tripled_prices(
                constants_for_params
            )
        if scenario_option["waste"] == "doubled_prices_in_country":
            constants_for_params = scenario_loader.set_global_waste_to_doubled_prices(
                constants_for_params
            )
        if scenario_option["waste"] == "baseline_in_country":
            constants_for_params = scenario_loader.set_global_waste_to_baseline_prices(
                constants_for_params
            )

        if scenario_option["waste"] == "tripled_prices_globally":
            constants_for_params = scenario_loader.set_country_waste_to_tripled_prices(
                constants_for_params, country_data
            )
        if scenario_option["waste"] == "doubled_prices_globally":
            constants_for_params = scenario_loader.set_country_waste_to_doubled_prices(
                constants_for_params, country_data
            )
        if scenario_option["waste"] == "baseline_globally":
            constants_for_params = scenario_loader.set_country_waste_to_baseline_prices(
                constants_for_params, country_data
            )

        if scenario_option["nutrition"] == "baseline":
            constants_for_params = scenario_loader.set_baseline_nutrition_profile(
                constants_for_params
            )
        if scenario_option["nutrition"] == "catastrophe":
            constants_for_params = scenario_loader.set_catastrophe_nutrition_profile(
                constants_for_params
            )

        if scenario_option["buffer"] == "zero":
            constants_for_params = scenario_loader.set_stored_food_buffer_zero(
                constants_for_params
            )
        if scenario_option["buffer"] == "baseline":
            constants_for_params = scenario_loader.set_stored_food_buffer_as_baseline(
                constants_for_params
            )

        if scenario_option["seasonality"] == "baseline_in_country":
            constants_for_params = scenario_loader.set_country_seasonality_baseline(
                constants_for_params, country_data
            )
        if scenario_option["seasonality"] == "nuclear_winter_in_country":
            constants_for_params = (
                scenario_loader.set_country_seasonality_nuclear_winter(
                    constants_for_params, country_data
                )
            )
        if scenario_option["seasonality"] == "baseline_globally":
            constants_for_params = scenario_loader.set_global_seasonality_baseline(
                constants_for_params
            )
        if scenario_option["seasonality"] == "nuclear_winter_globally":
            constants_for_params = (
                scenario_loader.set_global_seasonality_nuclear_winter(
                    constants_for_params
                )
            )

        if scenario_option["fish"] == "nuclear_winter":
            constants_for_params = scenario_loader.set_fish_nuclear_winter_reduction(
                constants_for_params
            )
        if scenario_option["fish"] == "baseline":
            constants_for_params = scenario_loader.set_fish_baseline(
                constants_for_params
            )

        if scenario_option["crop_disruption"] == "zero":
            constants_for_params = scenario_loader.set_disruption_to_crops_to_zero(
                constants_for_params
            )
        if scenario_option["crop_disruption"] == "nuclear_winter":
            constants_for_params = (
                scenario_loader.set_nuclear_winter_global_disruption_to_crops(
                    constants_for_params
                )
            )

        if scenario_option["protein"] == "required":
            constants_for_params = scenario_loader.include_protein(constants_for_params)
        if scenario_option["protein"] == "not_required":
            constants_for_params = scenario_loader.dont_include_protein(
                constants_for_params
            )

        if scenario_option["fat"] == "required":
            constants_for_params = scenario_loader.include_fat(constants_for_params)
        if scenario_option["fat"] == "not_required":
            constants_for_params = scenario_loader.dont_include_fat(
                constants_for_params
            )

        if scenario_option["cull"] == "do_eat_culled":
            constants_for_params = scenario_loader.cull_animals(constants_for_params)
        if scenario_option["cull"] == "dont_eat_culled":
            constants_for_params = scenario_loader.dont_cull_animals(
                constants_for_params
            )

        if scenario_option["scenario"] == "baseline_climate":
            constants_for_params = scenario_loader.get_baseline_climate_scenario(
                constants_for_params
            )
        if scenario_option["scenario"] == "resilient_food_nuclear_winter":
            constants_for_params = scenario_loader.get_resilient_food_scenario(
                constants_for_params
            )
        if scenario_option["scenario"] == "no_resilient_food_nuclear_winter":
            constants_for_params = scenario_loader.get_no_resilient_food_scenario(
                constants_for_params
            )

        return constants_for_params, scenario_loader
