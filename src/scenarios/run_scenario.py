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

        extractor = Extractor(single_valued_constants)

        # actually make PuLP optimize effective people fed based on all the constants
        # we've determined
        (
            model,
            variables,
            single_valued_constants,
            multi_valued_constants,
        ) = self.run_optimizer(single_valued_constants, multi_valued_constants)

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

        PRINT_NEEDS_RATIO = True
        if PRINT_NEEDS_RATIO:
            interpreter.print_kcals_per_capita_per_day(interpreted_results)

        """
        seems to be important for with resilient foods code?
        optimizer = Optimizer()
        constants_loader = Parameters()
        constants["inputs"] = constants_for_params
        constants_for_optimizer = copy.deepcopy(constants)
        (
            single_valued_constants,
            multi_valued_constants,
        ) = constants_loader.computeParameters(constants_for_optimizer, scenarios_loader)

        single_valued_constants["CHECK_CONSTRAINTS"] = False
        [time_months, time_months_middle, extractor] = optimizer.optimize(
            single_valued_constants, multi_valued_constants
        )

        SEEMS to be important for monte carlo...
        try:
            single_valued_constants["CHECK_CONSTRAINTS"] = False
            [time_months, time_months_middle, extractor] = optimizer.optimize(
                single_valued_constants, multi_valued_constants
            )
            print(extractor.percent_people_fed)

        except AssertionError as msg:
            print(msg)
            failed_to_optimize = True
            print("Warning: Optimization failed. Continuing.")
            # quit()
            return (np.nan, i)
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
            failed_to_optimize = True
            print("Warning: Optimization failed. Continuing.")
            return (np.nan, i)



        """

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
