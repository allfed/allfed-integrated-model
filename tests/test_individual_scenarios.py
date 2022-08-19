#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This file runs the scenarios to test if they can be run without creating
error. This is our end to end testing.


Created on Wed Jul 13 11:54:39 2022

@author: florian
"""
import sys

from src.scenarios import run_model_baseline
from src.scenarios import run_model_no_trade_baseline
from src.scenarios import run_model_no_trade_no_resilient_foods
from src.scenarios import run_model_no_resilient_foods
from src.scenarios import run_model_with_resilient_foods


def test_run_model_baseline():
    """
    Runs the baseline model for testing

    Arguments:

    Returns:
        None
    """
    run_model_baseline.run_model_baseline(plot_figures=False)


def test_run_baseline_by_country_no_trade():
    """
    Runs the baseline by country and without trade model for testing

    Arguments:

    Returns:
        None
    """
    run_model_no_trade_baseline.run_baseline_by_country_no_trade(
        plot_map=False,
        show_figures=False,
        create_pptx_with_all_countries=False,
        scenario_option=[],
    )


def test_run_nuclear_winter_by_country_no_trade_no_resilient_foods():
    """
    Runs the baseline by country and without trade model for testing

    Arguments:

    Returns:
        None
    """
    run_model_no_trade_no_resilient_foods.run_nuclear_winter_by_country_no_trade(
        plot_map=False,
        show_figures=False,
        create_pptx_with_all_countries=False,
        scenario_option=[],
    )


def test_run_model_no_resilient_foods():
    """
    Runs the model without resilient food for testing

    Arguments:

    Returns:
        None
    """
    run_model_no_resilient_foods.run_model_no_resilient_foods(plot_figures=False)


def test_run_model_with_resilient_foods():
    """_
    Runs the model without resilient food for testing

    Arguments:

    Returns:
        None
    """
    run_model_with_resilient_foods.run_model_with_resilient_foods(plot_figures=False)


def test_run_monte_carlo():
    """
    Runs the monte carlo model for testing

    Arguments:

    Returns:
        None
    """
    # TBD
    pass


if __name__ == "__main__":
    test_run_model_baseline()
    test_run_baseline_by_country_no_trade()
    test_run_nuclear_winter_by_country_no_trade_no_resilient_foods()
    test_run_model_no_resilient_foods()
    test_run_model_with_resilient_foods()
    test_run_monte_carlo()

    # TODO @li add the with resilient food, no food trade case

    print("All tests passed")
    sys.exit(0)
