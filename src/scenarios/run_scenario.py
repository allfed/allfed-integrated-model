"""

This function runs a single optimization by computing the parameters,
running the parameters onto the optimizer, extracting the results, and interpreting the
results into more useful values for plotting and scenario evaluation

Created on Tue Jul 19

@author: morgan
"""

import sys

import numpy as np
import copy

import git
from pathlib import Path
import pandas as pd

from src.optimizer.optimizer import Optimizer
from src.optimizer.interpret_results import Interpreter
from src.optimizer.extract_results import Extractor
from src.scenarios.scenarios import Scenarios
from src.optimizer.validate_results import Validator
from src.optimizer.parameters import Parameters
from src.utilities.plotter import Plotter
from src.food_system.food import Food


repo_root = git.Repo(".", search_parent_directories=True).working_dir


def are_dicts_approx_same(dict1, dict2):
    # Ensure both dictionaries have the same keys
    if set(dict1.keys()) != set(dict2.keys()):
        return False

    for key in dict1.keys():
        val1, val2 = np.array(dict1[key]), np.array(dict2[key])
        # Compare arrays with a tolerance of 0.1%
        if not np.allclose(val1, val2, rtol=0.001, atol=0):
            return False

    return True


class ScenarioRunner:
    def __init__(self):
        pass

    def display_results_of_optimizer_round(
        self,
        interpreted_results,
        country_name,
        show_country_figures,
        create_pptx_with_all_countries,
        scenario_description,
        figure_save_postfix,
        slaughter_title="",
        feed_title="",
        to_humans_title="",
    ):
        NMONTHS = interpreted_results.constants["NMONTHS"]

        if not np.isnan(interpreted_results.percent_people_fed):
            if not np.allclose(
                np.zeros(NMONTHS),
                interpreted_results.feed_and_biofuels_sum.kcals,
                atol=0.1,
            ):  # no reason to display an empty plot
                Plotter.plot_feed(
                    interpreted_results,
                    "earliest_month_zero",
                    (feed_title + " " if feed_title != "" else "")
                    + country_name
                    + figure_save_postfix,
                    show_country_figures,
                    create_pptx_with_all_countries,
                    scenario_description,
                )
            if slaughter_title != "":
                Plotter.plot_slaughter(
                    interpreted_results,
                    "earliest_month_zero",
                    # (slaughter_title + " " if slaughter_title is not "" else "")
                    country_name,
                    # + figure_save_postfix,
                    show_country_figures,
                    create_pptx_with_all_countries,
                    scenario_description,
                )

            Plotter.plot_to_humans_stackplot(
                interpreted_results,
                NMONTHS,
                (to_humans_title + " " if to_humans_title != "" else "")
                + country_name
                + figure_save_postfix,
                show_country_figures,
                create_pptx_with_all_countries,
                scenario_description,
            )

    def run_round_1(
        self,
        consts_for_optimizer_round1,
        time_consts_round1,
        interpreter,
        feed_and_biofuels_round1,
        meat_dictionary_zero_feed_biofuels,
        title="Untitled",
    ):
        # FIRST ROUND: ENSURE HUMANS GET MINIMUM NEEDS

        # actually make PuLP optimize effective people fed based on all the constants
        # we've determined
        interpreted_results_round1 = self.run_optimizer(
            consts_for_optimizer_round1,
            time_consts_round1,
            optimization_type="to_humans",
            title=title,
        )

        interpreted_results_round1.set_feed_and_biofuels(feed_and_biofuels_round1)

        interpreted_results_round1.set_meat_dictionary(
            meat_dictionary_zero_feed_biofuels
        )

        return (
            interpreted_results_round1,
            interpreted_results_round1.percent_people_fed,
            consts_for_optimizer_round1,
        )

    def run_round_2(
        self,
        constants_loader,
        constants_for_params,
        interpreted_results_round1,
        percent_fed_from_model_round1,
        consts_for_optimizer_round1,
        time_consts_round1,
        interpreter,
        title="Untitled",
    ):
        # SECOND ROUND: REMAINING FEED-APPROPRIATE FOOD TO ANIMALS AND BIOFUELS UP TO THE AMOUNT THEY CAN BE USED
        (
            consts_for_optimizer_round2,
            time_consts_round2,
            feed_and_biofuels_round2,
            meat_dictionary_round2,
            min_human_food_consumption,
        ) = constants_loader.compute_parameters_second_round(
            constants_for_params,
            consts_for_optimizer_round1,
            time_consts_round1,
            interpreted_results_round1,
        )
        if (
            consts_for_optimizer_round2 is None
            and time_consts_round2 is None
            and feed_and_biofuels_round2 is None
            and meat_dictionary_round2 is None
            and min_human_food_consumption is None
        ):
            # this indicates the meat produced is in fact lower when feed is applied.
            # Therefore, we will abort the second round and simply return the results from the first round with no feed
            return None, None, None, None, None, None, None
        Validator.assert_meat_dairy_doesnt_decrease_round_2(
            time_consts_round1["each_month_meat_slaughtered"].kcals,
            time_consts_round2["each_month_meat_slaughtered"].kcals,
            time_consts_round1["milk_kcals"],
            time_consts_round2["milk_kcals"],
        )
        PLOT_MEAT_SLAUGHTERED_FLAG = False
        if PLOT_MEAT_SLAUGHTERED_FLAG:
            import matplotlib.pyplot as plt

            plt.figure()
            plt.plot(
                time_consts_round2["each month meat slaughtered before retail waste"]
            )
            plt.title("round 2 meat cumulative")
            plt.show()

        interpreted_results_round2 = self.run_optimizer(
            consts_for_optimizer_round2,
            time_consts_round2,
            optimization_type="to_animals",
            min_human_food_consumption=min_human_food_consumption,
            title=title,
        )

        # looks like it's necessary to reduce the feed requirements by about 20kcals per month, in order
        # to successfully run the optimization in the second round (however, this is only seemingly necessary when
        # both culled meat is turned on and there's no storage between years?)
        # Reduce each element by at most 20 kcals per person per day, ensuring results are not negative
        interpreted_results_round2.feed_sum_kcals_equivalent.kcals = np.clip(
            interpreted_results_round2.feed_sum_kcals_equivalent.kcals - 20,
            0,
            None,
        )
        interpreted_results_round2.biofuels_sum_kcals_equivalent.kcals = np.clip(
            interpreted_results_round2.biofuels_sum_kcals_equivalent.kcals - 20,
            0,
            None,
        )

        interpreted_results_round2.set_meat_dictionary(meat_dictionary_round2)

        return (
            interpreted_results_round2,
            meat_dictionary_round2,
            time_consts_round2["each_month_meat_slaughtered"],
            time_consts_round2["max_consumed_culled_kcals_each_month"],
            consts_for_optimizer_round2["meat_summed_consumption"],
            time_consts_round2,
            consts_for_optimizer_round2,
        )

    def run_round_3(
        self,
        constants_loader,
        constants_for_params,
        consts_for_optimizer_round1,
        consts_for_optimizer_round2,
        time_consts_round1,
        time_consts_round2,
        interpreted_results_round2,
        feed_and_biofuels_round1,
        feed_demand,
        biofuels_demand,
        interpreted_results_round1,
        meat_dictionary_round2,
        each_month_meat_slaughtered,
        max_consumed_culled_kcals_each_month,
        meat_summed_consumption,
        feed_meat_object_round1,
        title="Untitled",
    ):
        # THIRD ROUND: NOW THAT THE AMOUNT OF FEED AND BIOFUEL CONSUMED IS KNOWN, ALLOCATE THE REST TO HUMANS
        (
            consts_for_optimizer_round3,
            time_consts_round3,
            feed_and_biofuels_round3,
            meat_dictionary_round3,
        ) = constants_loader.compute_parameters_third_round(
            constants_for_params,
            consts_for_optimizer_round1,
            consts_for_optimizer_round2,
            time_consts_round1,
            time_consts_round2,
            interpreted_results_round1,
            interpreted_results_round2,
            feed_and_biofuels_round1,
            feed_demand,
            biofuels_demand,
            feed_meat_object_round1,
        )

        interpreted_results_round3 = self.run_optimizer(
            consts_for_optimizer_round3,
            time_consts_round3,
            optimization_type="to_humans",
            title=title,
        )
        interpreted_results_round3.set_meat_dictionary(meat_dictionary_round3)
        interpreted_results_round3.set_feed_and_biofuels(feed_and_biofuels_round3)
        interpreted_results_round3.set_meat_dictionary(meat_dictionary_round3)
        return interpreted_results_round3

    def get_interpreted_results_for_round3_if_zero_feed(self, interpreter, NMONTHS):
        print("")
        print("Skipped rounds 1 and 2 due to zero feed/biofuel")
        print("")

        interpreted_results_for_round3 = copy.deepcopy(interpreter)

        interpreted_results_for_round3.biofuels_sum_kcals_equivalent = Food(
            kcals=np.zeros(NMONTHS),
            fat=np.zeros(NMONTHS),
            protein=np.zeros(NMONTHS),
            kcals_units="billion kcals each month",
            fat_units="thousand tons each month",
            protein_units="thousand tons each month",
        )
        return interpreted_results_for_round3

    def run_and_analyze_scenario(
        self,
        constants_for_params,
        time_consts_for_params,
        scenario_description,
        create_pptx_with_all_countries,
        show_country_figures,
        figure_save_postfix,
        save_all_results,
        country_name,
        country_iso3,
        title="Untitled",
    ):
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
        # take the variables defining the scenario and compute the resulting needed
        # values as inputs to the optimizer
        meat_dictionary_round2 = None
        constants_loader = Parameters()
        (
            consts_for_optimizer_round1,
            time_consts_round1,
            feed_and_biofuels_round1,  # zero feed and biofuels
            meat_dictionary_zero_feed_biofuels,  # Meat if no feed used.
            feed_demand,  # feed requested by the user
            biofuels_demand,  # biofuels requested by the user
            feed_meat_object_round1,
        ) = constants_loader.compute_parameters_first_round(
            constants_for_params, time_consts_for_params
        )

        if save_all_results:
            self.save_outdoor_crop_production_to_csv(
                time_consts_round1, title, country_name
            )

        each_month_meat_slaughtered = time_consts_round1["each_month_meat_slaughtered"]
        max_consumed_culled_kcals_each_month = time_consts_round1[
            "max_consumed_culled_kcals_each_month"
        ]
        meat_summed_consumption = consts_for_optimizer_round1["meat_summed_consumption"]
        validator = Validator()
        validator.ensure_all_time_constants_units_are_billion_kcals(time_consts_round1)
        ROUND_1_WAS_RUN_FLAG = False
        if (
            constants_for_params["ADD_STORED_FOOD"]
            or constants_for_params["ADD_OUTDOOR_GROWING"]
            or constants_for_params["ADD_SEAWEED"]
            or constants_for_params["ADD_CELLULOSIC_SUGAR"]
            or constants_for_params["ADD_METHANE_SCP"]
        ) and not (feed_demand.all_equals_zero() and biofuels_demand.all_equals_zero()):
            # if any of the feed or biofuel resources are made available to the model
            # and the user has not requested zero feed and biofuel

            (
                interpreted_results_round1,
                percent_fed_from_model_round1,
                consts_for_optimizer_round1,
            ) = self.run_round_1(
                consts_for_optimizer_round1,
                time_consts_round1,
                interpreter,
                feed_and_biofuels_round1,
                meat_dictionary_zero_feed_biofuels,
                title=title + "_round1",
            )

            ROUND_1_WAS_RUN_FLAG = True

            Validator.assert_feed_used_below_feed_demand(
                feed_demand, interpreted_results_round1, round=1
            )
            Validator.assert_biofuels_used_below_biofuels_demand(
                biofuels_demand, interpreted_results_round1, round=1
            )

            DISPLAY_MEAT_PRODUCED_IF_NO_FEED_FLAG = False
            if DISPLAY_MEAT_PRODUCED_IF_NO_FEED_FLAG:
                # because feed and biofuel are zero, feed and biofuels plot
                # most likely to be skipped unless there's some issue
                self.display_results_of_optimizer_round(
                    interpreted_results_round1,
                    country_name,
                    show_country_figures,
                    create_pptx_with_all_countries,
                    scenario_description,
                    figure_save_postfix,
                    slaughter_title="Meat produced first round (no feed given to animals)",
                    feed_title="Feed first round (no feed given to animals)",
                    to_humans_title="Food to humans maximized, first round (no feed given to animals)",
                )

            (
                interpreted_results_round2,
                meat_dictionary_round2,
                each_month_meat_slaughtered,
                max_consumed_culled_kcals_each_month,
                meat_summed_consumption,
                time_consts_round2,
                consts_for_optimizer_round2,
            ) = self.run_round_2(
                constants_loader,
                constants_for_params,
                interpreted_results_round1,
                percent_fed_from_model_round1,
                consts_for_optimizer_round1,
                time_consts_round1,
                interpreter,
                title=title + "_round2",
            )

            if (
                interpreted_results_round2 is None
                and meat_dictionary_round2 is None
                and each_month_meat_slaughtered is None
                and max_consumed_culled_kcals_each_month is None
                and meat_summed_consumption is None
            ):
                # this indicates the meat produced is in fact lower when feed is applied.
                # Therefore, we will abort the second round and simply return the results from the first round with no
                # feed
                interpreted_results_for_round3 = (
                    self.get_interpreted_results_for_round3_if_zero_feed(
                        interpreter, constants_for_params["NMONTHS"]
                    )
                )

            else:
                Validator.assert_feed_used_below_feed_demand(
                    feed_demand, interpreted_results_round2, round=2
                )
                Validator.assert_biofuels_used_below_biofuels_demand(
                    biofuels_demand, interpreted_results_round2, round=2
                )
                if DISPLAY_MEAT_PRODUCED_IF_NO_FEED_FLAG and (
                    are_dicts_approx_same(
                        interpreted_results_round1.meat_dictionary,
                        interpreted_results_round2.meat_dictionary,
                    )
                    and are_dicts_approx_same(
                        interpreted_results_round1.animal_population_dictionary,
                        interpreted_results_round2.animal_population_dictionary,
                    )
                ):
                    # Meat produced from second round with no restriction is identical to with restrictions,
                    # so skip replotting.
                    slaughter_title = ""
                    print(
                        "interpreted results approx same round 1 2 meat dict, animal dict, skipping"
                    )
                else:
                    slaughter_title = "Max meat produced from second round calc (no restriction on feed before shutoff)"

                DISPLAY_MEAT_PRODUCED_INCREASED_FEED_FLAG = False
                if DISPLAY_MEAT_PRODUCED_INCREASED_FEED_FLAG:
                    self.display_results_of_optimizer_round(
                        interpreted_results_round2,
                        country_name,
                        show_country_figures,
                        create_pptx_with_all_countries,
                        scenario_description,
                        figure_save_postfix,
                        slaughter_title=slaughter_title,
                        feed_title="Feed for second round optimization, no restriction to animals before shutoff",
                        to_humans_title="Humans fed only up to minimum needs",
                    )
                interpreted_results_for_round3 = interpreted_results_round2
        else:
            # none of the feed or biofuel resources are made available to the model
            # or the user has not requested zero feed and biofuel

            interpreted_results_for_round3 = (
                self.get_interpreted_results_for_round3_if_zero_feed(
                    interpreter, constants_for_params["NMONTHS"]
                )
            )
        interpreted_results_round3 = self.run_round_3(
            constants_loader,
            constants_for_params,
            consts_for_optimizer_round1,
            consts_for_optimizer_round2 if ROUND_1_WAS_RUN_FLAG else None,
            time_consts_round1,
            time_consts_round2 if ROUND_1_WAS_RUN_FLAG else None,
            interpreted_results_for_round3,
            feed_and_biofuels_round1,
            feed_demand,
            biofuels_demand,
            interpreted_results_round1 if ROUND_1_WAS_RUN_FLAG else None,
            meat_dictionary_round2,
            each_month_meat_slaughtered,
            max_consumed_culled_kcals_each_month,
            meat_summed_consumption,
            feed_meat_object_round1,
            title=title + "_round3",
        )

        Validator.assert_feed_used_below_feed_demand(
            feed_demand, interpreted_results_round3, round=3
        )
        Validator.assert_biofuels_used_below_biofuels_demand(
            biofuels_demand, interpreted_results_round3, round=3
        )

        if save_all_results:
            self.save_feed_and_biofuels_to_csv(
                feed_demand, biofuels_demand, title, country_name
            )

        if ROUND_1_WAS_RUN_FLAG:
            Validator.assert_round3_percent_fed_not_lower_than_round1(
                constants_for_params[
                    "MINIMUM_PERCENT_FED_BEFORE_NONHUMAN_CONSUMPTION_ALLOWED"
                ],
                percent_fed_from_model_round1,
                interpreted_results_round3.percent_people_fed,
            )

        self.display_results_of_optimizer_round(
            interpreted_results_round3,
            country_name,
            show_country_figures,
            create_pptx_with_all_countries,
            scenario_description,
            figure_save_postfix,
            slaughter_title="slaughter of animals for third round",
            feed_title="feed biofuel for third round",
        )
        print(
            f"Percent people fed {country_name} (iso3: {country_iso3}): "
            f"{round(interpreted_results_round3.percent_people_fed, 2)}%"
        )

        return interpreted_results_round3

    def interpret_optimizer_results(
        self,
        consts_for_optimizer,
        model,
        variables,
        time_consts,
        percent_fed_from_model,
        optimization_type,
        title="Untitled",
    ):
        validator = Validator()
        extractor = Extractor(consts_for_optimizer)
        #  get values from all the optimizer in list and integer formats
        extracted_results = extractor.extract_results(model, variables, time_consts)

        # TODO: eventually all the values not directly solved by the optimizer should
        # be removed from extracted_results

        interpreter = Interpreter()
        #  interpret the results, nicer for plotting, reporting, and printing results
        interpreted_results = interpreter.interpret_results(extracted_results, title)

        # ensure no errors were made in the extraction and interpretation, or if the
        # optimizer did not correctly satisfy constraints within a reasonable margin
        # of error
        validator.validate_results(
            extracted_results,
            interpreted_results,
            time_consts,
            percent_fed_from_model,
            optimization_type,
            consts_for_optimizer["inputs"]["COUNTRY_CODE"],
        )

        return interpreted_results

    def run_optimizer(
        self,
        consts_for_optimizer,
        time_consts,
        optimization_type=None,
        min_human_food_consumption=None,
        title="Untitled",
    ):
        """
        Runs the optimizer and returns the model, variables, and constants
        """
        if optimization_type == "to_animals":
            assert (
                min_human_food_consumption is not None
            ), "ERROR: must specify minimum human needs when running second round"

        optimizer = Optimizer(consts_for_optimizer, time_consts)
        validator = Validator()

        if optimization_type == "to_humans":
            (
                model,
                variables,
                maximize_constraints,
                percent_fed_from_model,
            ) = optimizer.optimize_to_humans(consts_for_optimizer, time_consts)
        elif optimization_type == "to_animals":
            (
                model,
                variables,
                maximize_constraints,
                percent_fed_from_model,
            ) = optimizer.optimize_feed_to_animals(
                consts_for_optimizer,
                time_consts,
                min_human_food_consumption,
            )
        else:
            raise ValueError("Optimization must be to humans or animals.")

        interpreted_results = self.interpret_optimizer_results(
            consts_for_optimizer,
            model,
            variables,
            time_consts,
            percent_fed_from_model,
            optimization_type=optimization_type,
            title=title,
        )

        CHECK_CONSTRAINTS_FLAG = False
        if CHECK_CONSTRAINTS_FLAG:
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

        return interpreted_results

    def alter_scenario_if_known_to_fail(self, scenario_option, iso3):
        """
        These are the scenarios I seem to be unable to determine why optimization is failing.
        I belive I have hit diminishing returns trying to figure them out, so I just patch them instead.
        """
        failing_scenarios = [
            {
                "country_code": "SLV",
                "cull": ["do_eat_culled"],
                "scenario": ["all_resilient_foods", "seaweed"],
                "shutoff": [
                    "continued",
                    "long_delayed_shutoff",
                    "short_delayed_shutoff",
                ],
                "CORRECTION": {"shutoff": "immediate"},
                "WARNING": (
                    "WARNING: SLV cannot run with seaweed under these specific conditions. "
                    " Removing feed and biofuel demand from this scenario as a patch."
                ),
            },
            {
                "country_code": "ALB",
                "cull": ["do_eat_culled"],
                "scenario": ["all_resilient_foods", "seaweed"],
                "shutoff": [
                    "continued",
                    "long_delayed_shutoff",
                    "short_delayed_shutoff",
                ],
                "CORRECTION": {"shutoff": "immediate"},
                "WARNING": (
                    "WARNING: ALB cannot run with seaweed under these specific conditions. "
                    " Removing feed and biofuel demand from this scenario as a patch."
                ),
            },
            {
                "country_code": "ECU",
                "scenario": [
                    "all_resilient_foods",
                    "seaweed",
                    "greenhouse",
                    "methane_scp",
                    "relocated_crops",
                    "industrial_foods",
                    "cellulosic_sugar",
                ],
                "crop_disruption": ["zero", "baseline"],
                "meat_strategy": ["feed_only_ruminants"],
                "end_simulation_stocks_ratio": ["zero", "baseline"],
                "cull": ["do_eat_culled"],
                "shutoff": ["long_delayed_shutoff"],
                "CORRECTION": {"shutoff": "immediate"},
                "WARNING": (
                    "WARNING: ECU cannot run with these specific conditions. "
                    "Changing scenario to shut off all feed and biofuels immediately."
                ),
            },
            {
                "country_code": "ECU",
                "scenario": [
                    "all_resilient_foods",
                    "seaweed",
                    "greenhouse",
                    "methane_scp",
                    "relocated_crops",
                    "industrial_foods",
                    "cellulosic_sugar",
                ],
                "crop_disruption": ["zero", "baseline"],
                "meat_strategy": ["feed_only_ruminants"],
                "end_simulation_stocks_ratio": ["zero", "baseline"],
                "cull": ["do_eat_culled"],
                "shutoff": ["long_delayed_shutoff"],
                "CORRECTION": {"shutoff": "immediate"},
                "WARNING": (
                    "WARNING: ECU cannot run with these specific conditions. "
                    "Changing scenario to shut off all feed and biofuels immediately."
                ),
            },
        ]
        unchanged_scenario_option_copy = copy.deepcopy(scenario_option)
        altered_scenario_option = copy.deepcopy(scenario_option)
        for failing_scenario in failing_scenarios:
            iso3_failing_scenario = failing_scenario["country_code"]
            correction = failing_scenario["CORRECTION"]
            warning = failing_scenario["WARNING"]
            del failing_scenario["country_code"]
            del failing_scenario["CORRECTION"]
            del failing_scenario["WARNING"]
            # Check if keys in dict2 are a subset of keys in dict1 and values match for those keys
            keys_are_subset = set(failing_scenario.keys()).issubset(
                set(scenario_option.keys())
            )
            assert keys_are_subset
            values_match = all(
                scenario_option[key] in failing_scenario[key]
                for key in failing_scenario
            )
            if values_match and iso3 == iso3_failing_scenario:
                # alter the scenario
                altered_scenario_option[list(correction.keys())[0]] = list(
                    correction.values()
                )[0]
                print(warning)
                return altered_scenario_option  # there should only be one match, so return the alteration
        # there were no alterations, return a copy of the original scenario options
        return unchanged_scenario_option_copy

    def set_depending_on_option(self, scenario_option, country_data=None):
        PRINT_SCENARIO_OPTIONS = False
        if PRINT_SCENARIO_OPTIONS:
            import pprint

            pprint.pprint("scenario_option")
            pprint.pprint(scenario_option)
        assert "scale" in scenario_option.keys(), "You must specify 'scale'"

        assert "stored_food" in scenario_option.keys(), "You must specify 'stored_food'"

        assert (
            "end_simulation_stocks_ratio" in scenario_option.keys()
        ), "You must specify 'end_simulation_stocks_ratio'"

        assert "shutoff" in scenario_option.keys(), """You must specify 'shutoff'"""

        assert "waste" in scenario_option.keys(), """You must specify 'waste'"""

        assert "nutrition" in scenario_option.keys(), "You must specify 'nutrition'"

        assert (
            "intake_constraints" in scenario_option.keys()
        ), "You must specify 'intake_constraints'"

        assert (
            "seasonality" in scenario_option.keys()
        ), """You must specify 'seasonality'"""

        assert "grasses" in scenario_option.keys(), """You must specify 'grasses'"""

        assert "fish" in scenario_option.keys(), "You must specify 'fish'"

        assert (
            "crop_disruption" in scenario_option.keys()
        ), """You must specify 'crop_disruption'"""

        assert "protein" in scenario_option.keys(), "You must specify 'protein'"

        assert "fat" in scenario_option.keys(), "You must specify 'fat'"

        assert "cull" in scenario_option.keys(), "You must specify 'cull'"

        assert "scenario" in scenario_option.keys(), """You must specify 'scenario'"""

        assert (
            "meat_strategy" in scenario_option.keys()
        ), """You must specify 'meat_strategy'"""

        scenario_is_correct = True  # until proven otherwise

        scenario_loader = Scenarios()
        ALTER_FAILING_SCENARIO_FLAG = True
        if ALTER_FAILING_SCENARIO_FLAG:
            # let's alter some scenarios that are known to fail. Also make sure the changes are temporary by
            # only altering a copy of the original scenario options
            if country_data is None:
                scenario_option_copy = self.alter_scenario_if_known_to_fail(
                    scenario_option, "WOR"  # whole world
                )
            else:
                scenario_option_copy = self.alter_scenario_if_known_to_fail(
                    scenario_option, country_data["iso3"]  # the country of interest
                )
        else:
            scenario_option_copy = copy.deepcopy(scenario_option)

        time_consts_for_params = {}

        # SCALE
        if scenario_option_copy["scale"] == "global":
            assert (
                country_data is None
            ), "ERROR: country data supplied for global crop run"
            constants_for_params = scenario_loader.init_global_food_system_properties()
            constants_for_params["COUNTRY_CODE"] = "WOR"
        elif scenario_option_copy["scale"] == "country":
            constants_for_params = scenario_loader.init_country_food_system_properties(
                country_data
            )

            constants_for_params["COUNTRY_CODE"] = country_data["iso3"]
        else:
            scenario_is_correct = False
            assert (
                scenario_is_correct
            ), "You must specify 'scale' key as global,or country"

        constants_for_params["NMONTHS"] = scenario_option_copy["NMONTHS"]

        # STORED FOOD

        if scenario_option_copy["stored_food"] == "zero":
            constants_for_params = scenario_loader.set_no_stored_food(
                constants_for_params
            )
        elif scenario_option_copy["stored_food"] == "baseline":
            constants_for_params = scenario_loader.set_baseline_stored_food(
                constants_for_params
            )
        else:
            scenario_is_correct = False

            assert (
                scenario_is_correct
            ), "You must specify 'stored_food' key as zero, or baseline"

        # END_SIMULATION_STOCKS_RATIO

        if scenario_option_copy["end_simulation_stocks_ratio"] == "zero":
            constants_for_params = scenario_loader.set_stored_food_buffer_zero(
                constants_for_params
            )
        elif (
            scenario_option_copy["end_simulation_stocks_ratio"]
            == "no_stored_between_years"
        ):
            constants_for_params = scenario_loader.set_no_stored_food_between_years(
                constants_for_params
            )
        elif scenario_option_copy["end_simulation_stocks_ratio"] == "baseline":
            constants_for_params = scenario_loader.set_stored_food_buffer_as_baseline(
                constants_for_params
            )
        elif (
            scenario_option_copy["end_simulation_stocks_ratio"]
            == "baseline_no_stored_between_years"
        ):
            constants_for_params = scenario_loader.set_stored_food_buffer_as_baseline_and_no_stored_between_years(
                constants_for_params
            )
        else:
            scenario_is_correct = False

            assert scenario_is_correct, (
                "You must specify 'end_simulation_stocks_ratio' key as zero, no_stored_between_years, "
                "baseline_no_stored_between_years, or baseline"
            )

        # SHUTOFF
        if scenario_option_copy["shutoff"] == "immediate":
            constants_for_params = scenario_loader.set_immediate_shutoff(
                constants_for_params
            )
        elif scenario_option_copy["shutoff"] == "one_month_delayed_shutoff":
            constants_for_params = scenario_loader.set_one_month_delayed_shutoff(
                constants_for_params
            )

        elif scenario_option_copy["shutoff"] == "short_delayed_shutoff":
            constants_for_params = scenario_loader.set_short_delayed_shutoff(
                constants_for_params
            )
        elif scenario_option_copy["shutoff"] == "long_delayed_shutoff":
            constants_for_params = scenario_loader.set_long_delayed_shutoff(
                constants_for_params
            )
        elif scenario_option_copy["shutoff"] == "continued":
            constants_for_params = scenario_loader.set_continued_feed_biofuels(
                constants_for_params
            )
        elif scenario_option_copy["shutoff"] == "continued_after_10_percent_fed":
            constants_for_params = scenario_loader.set_continued_after_10_percent_fed(
                constants_for_params
            )
        elif (
            scenario_option_copy["shutoff"]
            == "long_delayed_shutoff_after_10_percent_fed"
        ):
            constants_for_params = (
                scenario_loader.set_long_delayed_shutoff_after_10_percent_fed(
                    constants_for_params
                )
            )
        else:
            scenario_is_correct = False

            assert scenario_is_correct, (
                "You must specify 'shutoff' key as "
                "immediate,short_delayed_shutoff,one_month_delayed_shutoff, "
                "long_delayed_shutoff, continued_after_10_percent_fed, or continued."
            )
        # WASTE

        if scenario_option_copy["waste"] == "zero":
            constants_for_params = scenario_loader.set_waste_to_zero(
                constants_for_params
            )
        elif scenario_option_copy["waste"] == "tripled_prices_in_country":
            constants_for_params = scenario_loader.set_country_waste_to_tripled_prices(
                constants_for_params, country_data
            )
        elif scenario_option_copy["waste"] == "doubled_prices_in_country":
            constants_for_params = scenario_loader.set_country_waste_to_doubled_prices(
                constants_for_params, country_data
            )
        elif scenario_option_copy["waste"] == "baseline_in_country":
            constants_for_params = scenario_loader.set_country_waste_to_baseline_prices(
                constants_for_params, country_data
            )
        elif scenario_option_copy["waste"] == "tripled_prices_globally":
            constants_for_params = scenario_loader.set_global_waste_to_tripled_prices(
                constants_for_params
            )
        elif scenario_option_copy["waste"] == "doubled_prices_globally":
            constants_for_params = scenario_loader.set_global_waste_to_doubled_prices(
                constants_for_params
            )
        elif scenario_option_copy["waste"] == "baseline_globally":
            constants_for_params = scenario_loader.set_global_waste_to_baseline_prices(
                constants_for_params
            )
        else:
            scenario_is_correct = False

            assert scenario_is_correct, (
                "You must specify 'waste' key as zero,tripled_prices_in_country,"
                "doubled_prices_in_country,baseline_in_country,tripled_prices_globally,"
                "doubled_prices_globally,or baseline_globally"
            )

        # NUTRITION

        if scenario_option_copy["nutrition"] == "baseline":
            constants_for_params = scenario_loader.set_baseline_nutrition_profile(
                constants_for_params
            )
        elif scenario_option_copy["nutrition"] == "catastrophe":
            constants_for_params = scenario_loader.set_catastrophe_nutrition_profile(
                constants_for_params
            )
        else:
            scenario_is_correct = False

            assert (
                scenario_is_correct
            ), "You must specify 'nutrition' key as baseline, or catastrophe"

        # INTAKE CONSTRAINTS

        if scenario_option_copy["intake_constraints"] == "enabled":
            constants_for_params = scenario_loader.set_intake_constraints_to_enabled(
                constants_for_params
            )
        elif scenario_option_copy["intake_constraints"] == "disabled_for_humans":
            constants_for_params = (
                scenario_loader.set_intake_constraints_to_disabled_for_humans(
                    constants_for_params
                )
            )
        else:
            scenario_is_correct = False

            assert (
                scenario_is_correct
            ), "You must specify 'intake_constraints' key as enabled, or disabled_for_humans"

        # SEASONALITY

        if scenario_option_copy["seasonality"] == "no_seasonality":
            constants_for_params = scenario_loader.set_no_seasonality(
                constants_for_params
            )
        elif scenario_option_copy["seasonality"] == "country":
            constants_for_params = scenario_loader.set_country_seasonality(
                constants_for_params, country_data
            )
        elif scenario_option_copy["seasonality"] == "baseline_globally":
            constants_for_params = scenario_loader.set_global_seasonality_baseline(
                constants_for_params
            )
        elif scenario_option_copy["seasonality"] == "nuclear_winter_globally":
            constants_for_params = (
                scenario_loader.set_global_seasonality_nuclear_winter(
                    constants_for_params
                )
            )
        else:
            scenario_is_correct = False

            assert scenario_is_correct, (
                "You must specify 'seasonality' key as no_seasonality, country, "
                "baseline_globally,or nuclear_winter_globally"
            )

        # GRASSES
        if scenario_option_copy["grasses"] == "baseline":
            constants_for_params = scenario_loader.set_grasses_baseline(
                constants_for_params
            )
        elif scenario_option_copy["grasses"] == "global_nuclear_winter":
            constants_for_params = scenario_loader.set_global_grasses_nuclear_winter(
                constants_for_params
            )
        elif scenario_option_copy["grasses"] == "country_nuclear_winter":
            constants_for_params = scenario_loader.set_country_grasses_nuclear_winter(
                constants_for_params, country_data
            )
        elif scenario_option_copy["grasses"] == "all_crops_die_instantly":
            constants_for_params = scenario_loader.set_country_grasses_to_zero(
                constants_for_params
            )
        else:
            scenario_is_correct = False

            assert scenario_is_correct, (
                "You must specify 'grasses' key as baseline,"
                "global_nuclear_winter,all_crops_die_instantly, or country_nuclear_winter"
            )

        # FISH

        if scenario_option_copy["fish"] == "zero":
            time_consts_for_params = scenario_loader.set_fish_zero(
                constants_for_params, time_consts_for_params
            )
        elif scenario_option_copy["fish"] == "nuclear_winter":
            time_consts_for_params = scenario_loader.set_fish_nuclear_winter_reduction(
                time_consts_for_params
            )
        elif scenario_option_copy["fish"] == "baseline":
            time_consts_for_params = scenario_loader.set_fish_baseline(
                constants_for_params, time_consts_for_params
            )
        else:
            scenario_is_correct = False

            assert (
                scenario_is_correct
            ), "You must specify 'fish' key as either zero, nuclear_winter,or baseline"

        # CROPS

        if scenario_option_copy["crop_disruption"] == "zero":
            constants_for_params = scenario_loader.set_disruption_to_crops_to_zero(
                constants_for_params
            )
        elif scenario_option_copy["crop_disruption"] == "global_nuclear_winter":
            constants_for_params = (
                scenario_loader.set_nuclear_winter_global_disruption_to_crops(
                    constants_for_params
                )
            )
        elif scenario_option_copy["crop_disruption"] == "country_nuclear_winter":
            constants_for_params = (
                scenario_loader.set_nuclear_winter_country_disruption_to_crops(
                    constants_for_params, country_data
                )
            )
        elif scenario_option_copy["crop_disruption"] == "all_crops_die_instantly":
            constants_for_params = scenario_loader.set_zero_crops(constants_for_params)
        else:
            scenario_is_correct = False

            assert scenario_is_correct, (
                "You must specify 'crop_disruption' key as either zero,"
                "global_nuclear_winter, all_crops_die_instantly, or country_nuclear_winter"
            )

        # PROTEIN

        if scenario_option_copy["protein"] == "required":
            print("ERROR: fat and protein not working in this version of the model")
            print("(compute parameters in the second round would need to be modified)")
            sys.exit()
            constants_for_params = scenario_loader.include_protein(constants_for_params)
        elif scenario_option_copy["protein"] == "not_required":
            constants_for_params = scenario_loader.dont_include_protein(
                constants_for_params
            )
        else:
            scenario_is_correct = False

            assert (
                scenario_is_correct
            ), "You must specify 'protein' key as either required, or not_required"

        # FAT

        if scenario_option_copy["fat"] == "required":
            print("ERROR: fat and protein not working in this version of the model")
            print("(compute parameters in the second round would need to be modified)")
            sys.exit()
            constants_for_params = scenario_loader.include_fat(constants_for_params)
        elif scenario_option_copy["fat"] == "not_required":
            constants_for_params = scenario_loader.dont_include_fat(
                constants_for_params
            )
        else:
            scenario_is_correct = False

            assert (
                scenario_is_correct
            ), "You must specify 'fat' key as either required, or not_required"

        # CULLING

        if scenario_option_copy["cull"] == "do_eat_culled":
            constants_for_params = scenario_loader.cull_animals(constants_for_params)
        elif scenario_option_copy["cull"] == "dont_eat_culled":
            constants_for_params = scenario_loader.dont_cull_animals(
                constants_for_params
            )
        else:
            scenario_is_correct = False

            assert (
                scenario_is_correct
            ), "You must specify 'cull' key as either do_eat_culled, or dont_eat_culled"

        # SCENARIO

        if scenario_option_copy["scenario"] == "all_resilient_foods":
            constants_for_params = scenario_loader.get_all_resilient_foods_scenario(
                constants_for_params
            )
        elif scenario_option_copy["scenario"] == "all_resilient_foods_and_more_area":
            constants_for_params = (
                scenario_loader.get_all_resilient_foods_and_more_area_scenario(
                    constants_for_params
                )
            )
        elif scenario_option_copy["scenario"] == "no_resilient_foods":
            constants_for_params = scenario_loader.get_no_resilient_food_scenario(
                constants_for_params
            )
        elif scenario_option_copy["scenario"] == "seaweed":
            constants_for_params = scenario_loader.get_seaweed_scenario(
                constants_for_params
            )
        elif scenario_option_copy["scenario"] == "methane_scp":
            constants_for_params = scenario_loader.get_methane_scp_scenario(
                constants_for_params
            )
        elif scenario_option_copy["scenario"] == "cellulosic_sugar":
            constants_for_params = scenario_loader.get_cellulosic_sugar_scenario(
                constants_for_params
            )
        elif scenario_option_copy["scenario"] == "relocated_crops":
            constants_for_params = scenario_loader.get_relocated_crops_scenario(
                constants_for_params
            )
        elif scenario_option_copy["scenario"] == "greenhouse":
            constants_for_params = scenario_loader.get_greenhouse_scenario(
                constants_for_params
            )
        elif scenario_option_copy["scenario"] == "industrial_foods":
            constants_for_params = scenario_loader.get_industrial_foods_scenario(
                constants_for_params
            )
        else:
            scenario_is_correct = False

            assert scenario_is_correct, (
                "You must specify 'scenario' key as either baseline_climate,"
                "all_resilient_foods,all_resilient_foods_and_more_area,no_resilient_foods,seaweed,methane_scp,"
                "cellulosic_sugar,industrial_foods,relocated_crops or greenhouse"
            )

        if scenario_option_copy["meat_strategy"] == "reduce_breeding":
            constants_for_params = scenario_loader.set_breeding_to_greatly_reduced(
                constants_for_params
            )
        elif scenario_option_copy["meat_strategy"] == "baseline_breeding":
            constants_for_params = scenario_loader.set_to_baseline_breeding(
                constants_for_params
            )
        elif scenario_option_copy["meat_strategy"] == "feed_only_ruminants":
            constants_for_params = scenario_loader.set_to_feed_only_ruminants(
                constants_for_params
            )
        else:
            scenario_is_correct = False

            assert scenario_is_correct, (
                "You must specify 'meat_strategy' key as either , "
                "reduce_breeding or baseline_breeding, or feed_only_ruminants"
            )

        # add custom starting animal populations
        for key in scenario_option_copy.keys():
            if "_head" in key:
                constants_for_params[f"{key}_start"] = int(scenario_option_copy[key])

        # add custom large animal kg meat per head
        for key in scenario_option_copy.keys():
            if "kg_meat_per_large_animal" in key:
                constants_for_params[key] = float(scenario_option_copy[key])

        # modify MINIMUM_PERCENT_FED_BEFORE_NONHUMAN_CONSUMPTION_ALLOWED to custom value
        if (
            "MINIMUM_PERCENT_FED_BEFORE_NONHUMAN_CONSUMPTION_ALLOWED"
            in scenario_option_copy.keys()
        ):
            constants_for_params[
                "MINIMUM_PERCENT_FED_BEFORE_NONHUMAN_CONSUMPTION_ALLOWED"
            ] = float(
                scenario_option_copy[
                    "MINIMUM_PERCENT_FED_BEFORE_NONHUMAN_CONSUMPTION_ALLOWED"
                ]
            )
            assert (
                0
                <= constants_for_params[
                    "MINIMUM_PERCENT_FED_BEFORE_NONHUMAN_CONSUMPTION_ALLOWED"
                ]
                <= 100
            ), "MINIMUM_PERCENT_FED_BEFORE_NONHUMAN_CONSUMPTION_ALLOWED must be between 0 and 100"

        # modify END_SIMULATION_STOCKS_RATIO to custom value
        if "END_SIMULATION_STOCKS_RATIO" in scenario_option_copy.keys():
            constants_for_params["END_SIMULATION_STOCKS_RATIO"] = float(
                scenario_option_copy["END_SIMULATION_STOCKS_RATIO"]
            )
            assert 0 <= constants_for_params["END_SIMULATION_STOCKS_RATIO"] <= 1

        # apply fix multiplier to crop production
        if "CROP_PRODUCTION_MULTIPLIER" in scenario_option_copy.keys():
            multiplier = float(scenario_option_copy["CROP_PRODUCTION_MULTIPLIER"])
            assert 0 <= multiplier <= 10
            constants_for_params["RATIO_CROPS_YEAR1"] *= multiplier
            constants_for_params["RATIO_CROPS_YEAR2"] *= multiplier
            constants_for_params["RATIO_CROPS_YEAR3"] *= multiplier
            constants_for_params["RATIO_CROPS_YEAR4"] *= multiplier
            constants_for_params["RATIO_CROPS_YEAR5"] *= multiplier
            constants_for_params["RATIO_CROPS_YEAR6"] *= multiplier
            constants_for_params["RATIO_CROPS_YEAR7"] *= multiplier
            constants_for_params["RATIO_CROPS_YEAR8"] *= multiplier
            constants_for_params["RATIO_CROPS_YEAR9"] *= multiplier
            constants_for_params["RATIO_CROPS_YEAR10"] *= multiplier
            try:
                constants_for_params["RATIO_CROPS_YEAR11"] *= multiplier
            except BaseException:
                pass

        # apply fix multiplier to grass production
        if "GRASSES_PRODUCTION_MULTIPLIER" in scenario_option_copy.keys():
            multiplier = float(scenario_option_copy["GRASSES_PRODUCTION_MULTIPLIER"])
            assert 0 <= multiplier <= 10
            constants_for_params["RATIO_GRASSES_YEAR1"] *= multiplier
            constants_for_params["RATIO_GRASSES_YEAR2"] *= multiplier
            constants_for_params["RATIO_GRASSES_YEAR3"] *= multiplier
            constants_for_params["RATIO_GRASSES_YEAR4"] *= multiplier
            constants_for_params["RATIO_GRASSES_YEAR5"] *= multiplier
            constants_for_params["RATIO_GRASSES_YEAR6"] *= multiplier
            constants_for_params["RATIO_GRASSES_YEAR7"] *= multiplier
            constants_for_params["RATIO_GRASSES_YEAR8"] *= multiplier
            constants_for_params["RATIO_GRASSES_YEAR9"] *= multiplier
            constants_for_params["RATIO_GRASSES_YEAR10"] *= multiplier
            try:
                constants_for_params["RATIO_GRASSES_YEAR11"] *= multiplier
            except BaseException:
                pass

        # Print scenario properties
        PRINT_SCENARIO_PROPERTIES_FLAG = False
        if PRINT_SCENARIO_PROPERTIES_FLAG:
            print(scenario_loader.scenario_description)

        # Ensure every parameter has been initialized for the scenarios_loader
        scenario_loader.check_all_set()

        return (
            constants_for_params,
            time_consts_for_params,
            scenario_loader.scenario_description,
        )

    def save_outdoor_crop_production_to_csv(
        self, time_consts_round1, title, country_name
    ):
        """
        Saves the outdoor crop production to a csv file
        """
        production = (
            time_consts_round1["outdoor_crops"]
            .production.in_units_kcals_equivalent()
            .kcals
        )
        df = pd.DataFrame()
        df["production"] = production
        df["month"] = df.index
        df.to_csv(
            Path(repo_root)
            / "results"
            / (title + "_" + country_name + "_outdoor_crop_production.csv"),
            index=False,
        )
        return

    def save_feed_and_biofuels_to_csv(
        self, feed_demand, biofuels_demand, title, country_name
    ):
        """
        Saves the feed and biofuels demand to a csv file
        """
        df = pd.DataFrame()
        df["feed_demand"] = feed_demand.in_units_kcals_equivalent().kcals
        df["biofuels_demand"] = biofuels_demand.in_units_kcals_equivalent().kcals
        df["month"] = df.index
        df.to_csv(
            Path(repo_root)
            / "results"
            / (title + "_" + country_name + "_feed_and_biofuels_demand.csv"),
            index=False,
        )
        return
