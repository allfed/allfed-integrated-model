#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This file runs the scenarios to test if they can be run without creating
error. This is our end to end testing.


Created on Wed Jul 13 11:54:39 2022

@author: florian
"""
import sys

from src.scenarios import run_model_no_trade_baseline
from src.scenarios import run_model_no_trade_no_resilient_foods
from src.scenarios import run_model_no_trade_with_resilient_foods
from src.scenarios import run_scenarios_from_yaml


def test_run_baseline_by_country_no_trade():
    """
    Runs the baseline by country and without trade model for testing

    Arguments:

    Returns:
        None
    """
    run_model_no_trade_baseline.main(["single", "no_pptx", "no_plot"])


def test_run_nuclear_winter_by_country_no_trade_no_resilient_foods():
    """
    Runs the nuclear winter by country and without trade model for testing

    Arguments:

    Returns:
        None
    """
    run_model_no_trade_no_resilient_foods.main(["single", "no_pptx", "no_plot"])


def test_run_nuclear_winter_by_country_no_trade_with_resilient_foods():
    """
    Runs the nuclear winter with res food by country and without trade model for testing

    Arguments:

    Returns:
        None
    """
    run_model_no_trade_with_resilient_foods.main(["single", "no_pptx", "no_plot"])


def test_run_argentina():
    """
    Runs the nuclear winter with res food by country and without trade model for testing

    Arguments:

    Returns:
        None
    """

    run_scenarios_from_yaml.main(["False", "False", "argentina.yaml"])  # no plots


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
    test_run_baseline_by_country_no_trade()
    test_run_nuclear_winter_by_country_no_trade_no_resilient_foods()
    test_run_nuclear_winter_by_country_no_trade_with_resilient_foods()
    test_run_monte_carlo()
    test_run_argentina()

    print("All tests passed")
    sys.exit(0)
