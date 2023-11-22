#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This file runs the scenarios to test if they can be run without creating
error. This is our end to end testing.


Created on Wed Jul 13 11:54:39 2022

@author: florian and morgan
"""
import sys
import git
import os
from pathlib import Path
from src.scenarios import run_scenarios_from_yaml


def print_banner(text):
    """
    Prints out a Pytest-style banner to format inputted text.
    Used in test_run_all_scenarios() to display which scenario is being tested.

    Arguments:
        text (str): text to be printed in the banner

    Returns:
        None
    """
    banner_width = 196  # Adjust the width of the banner
    padding = max(0, (banner_width - len(text)) // 2)

    # Print the banner with centered text
    print()
    print(f"\033[32m{'>' * padding}{text}{'<' * padding}\033[0m")


def test_run_all_scenarios():
    """
    Runs the nuclear winter with res food by country and without trade model for testing

    Arguments:
        None

    Returns:
        None
    """

    repo_root = git.Repo(".", search_parent_directories=True).working_dir
    # Load data
    scenarios_path = Path(repo_root) / "scenarios"

    # Run all yaml files  in ./scenarios and sub-directories
    for root, dirs, files in os.walk(scenarios_path):
        for file in files:
            if file.endswith(".yaml"):
                file_path = os.path.join(root, file)
                # Tell user which scenario is running
                print_banner(f" RUNNING SCENARIO: {file} ")
                # Run the scenario
                run_scenarios_from_yaml.main(["False", "False", file_path])


if __name__ == "__main__":
    test_run_all_scenarios()

    print("All tests passed")
    sys.exit(0)
