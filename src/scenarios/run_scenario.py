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

from src.optimizer.optimizer import Optimizer
from src.optimizer.interpret_results import Interpreter
from src.optimizer.extract_results import Extractor
from src.scenarios.scenarios import Scenarios
from src.optimizer.validate_results import Validator
from src.optimizer.parameters import Parameters
from src.utilities.plotter import Plotter
from src.food_system.food import Food


class ScenarioRunner:
    def __init__(self):
        pass

    def display_results_of_optimizer_round(
        self,
        interpreted_results,
        country_data,
        show_country_figures,
        create_pptx_with_all_countries,
        scenario_loader,
        figure_save_postfix,
        slaughter_title="",
        feed_title="",
        to_humans_title="",
    ):
        NMONTHS = interpreted_results.constants["NMONTHS"]
        total_biofuels = (
            interpreted_results.cell_sugar_biofuels
            + interpreted_results.scp_biofuels
            + interpreted_results.seaweed_biofuels
            + interpreted_results.outdoor_crops_biofuels
            + interpreted_results.stored_food_biofuels
        )

        total_feed = (
            interpreted_results.cell_sugar_feed
            + interpreted_results.scp_feed
            + interpreted_results.seaweed_feed
            + interpreted_results.outdoor_crops_feed
            + interpreted_results.stored_food_feed
        )
        feed_and_biofuels_sum = total_biofuels + total_feed

        if not np.isnan(interpreted_results.percent_people_fed):
            if not np.allclose(
                np.zeros(NMONTHS),
                feed_and_biofuels_sum.kcals,
                atol=0.1,
            ):  # no reason to display an empty plot
                Plotter.plot_feed(
                    interpreted_results,
                    "earliest_month_zero",
                    (feed_title + " " if feed_title is not "" else "")
                    + country_data["country"]
                    + figure_save_postfix,
                    show_country_figures,
                    create_pptx_with_all_countries,
                    scenario_loader.scenario_description,
                )
            if slaughter_title != "":
                Plotter.plot_slaughter(
                    interpreted_results,
                    "earliest_month_zero",
                    (slaughter_title + " " if slaughter_title is not "" else "")
                    + country_data["country"]
                    + figure_save_postfix,
                    show_country_figures,
                    create_pptx_with_all_countries,
                    scenario_loader.scenario_description,
                )

            Plotter.plot_fig_1ab(
                interpreted_results,
                NMONTHS,
                (to_humans_title + " " if to_humans_title is not "" else "")
                + country_data["country"]
                + figure_save_postfix,
                show_country_figures,
                create_pptx_with_all_countries,
                scenario_loader.scenario_description,
            )

    def run_round_1(
        self,
        single_valued_constants_round1,
        time_consts_round1,
        interpreter,
        feed_and_biofuels_round1,
        meat_dictionary_zero_feed_biofuels,
    ):
        # FIRST ROUND: ENSURE HUMANS GET MINIMUM NEEDS

        # actually make PuLP optimize effective people fed based on all the constants
        # we've determined
        (
            model_round1,
            variables_round1,
            percent_fed_from_model_round1,
        ) = self.run_optimizer(single_valued_constants_round1, time_consts_round1)
        interpreted_results_round1 = self.interpret_optimizer_results(
            single_valued_constants_round1,
            model_round1,
            variables_round1,
            time_consts_round1,
            interpreter,
            percent_fed_from_model_round1,
            optimization_type="to_humans",
        )
        interpreted_results_round1.set_feed_and_biofuels(feed_and_biofuels_round1)
        interpreted_results_round1.set_meat_dictionary(
            meat_dictionary_zero_feed_biofuels
        )

        return (
            interpreted_results_round1,
            percent_fed_from_model_round1,
            single_valued_constants_round1,
        )

    def run_round_2(
        self,
        constants_loader,
        constants_for_params,
        interpreted_results_round1,
        percent_fed_from_model_round1,
        single_valued_constants_round1,
        time_consts_round1,
        interpreter,
        feed_and_biofuels_round1,
        max_feed_that_could_be_used_second_round,
        biofuels_demand,
        meat_dictionary_second_round,
    ):
        # SECOND ROUND: REMAINING FEED-APPROPRIATE FOOD TO ANIMALS AND BIOFUELS UP TO THE AMOUNT THEY CAN BE USED
        min_human_food_consumption = constants_loader.compute_parameters_second_round(
            constants_for_params,
            interpreted_results_round1,
            percent_fed_from_model_round1,
        )

        optimizer_to_animals = Optimizer(
            single_valued_constants_round1, time_consts_round1
        )

        (
            model_round2,
            variables_round2,
            maximize_constraints_round2,
            percent_fed_from_model_round2,
        ) = optimizer_to_animals.optimize_feed_to_animals(
            single_valued_constants_round1,
            time_consts_round1,
            min_human_food_consumption,
        )

        interpreted_results_round2 = self.interpret_optimizer_results(
            single_valued_constants_round1,  # these don't get updated in the second round
            model_round2,
            variables_round2,
            time_consts_round1,  # these don't get updated in the second round
            interpreter,
            percent_fed_from_model_round2,
            optimization_type="to_animals",
        )
        # because the third round is where we view the feed and biofuel results of the second round,
        # just consider the feed used
        # this is for the purposes of debugging and understanding the scenario and doesn't affect starvation
        feed_and_biofuels_round2 = copy.deepcopy(feed_and_biofuels_round1)
        feed_and_biofuels_round2.nonhuman_consumption = (
            max_feed_that_could_be_used_second_round + biofuels_demand
        )

        interpreted_results_round2.set_feed_and_biofuels(feed_and_biofuels_round2)
        interpreted_results_round2.set_meat_dictionary(meat_dictionary_second_round)

        return interpreted_results_round2

    def run_round_3(
        self,
        constants_loader,
        constants_for_params,
        single_valued_constants_round1,
        time_consts_round1,
        interpreted_results_round2,
        feed_and_biofuels_round1,
        interpreter,
    ):
        # THIRD ROUND: NOW THAT THE AMOUNT OF FEED AND BIOFUEL CONSUMED IS KNOWN, ALLOCATE THE REST TO HUMANS

        (
            single_valued_constants_round3,
            time_consts_round3,
            feed_and_biofuels_round3,
            meat_dictionary_round3,
        ) = constants_loader.compute_parameters_third_round(
            constants_for_params,
            single_valued_constants_round1,
            time_consts_round1,
            interpreted_results_round2,
            feed_and_biofuels_round1,
        )

        (
            model,
            variables,
            percent_fed_from_model_round3,
        ) = self.run_optimizer(single_valued_constants_round3, time_consts_round3)
        interpreted_results_round3 = self.interpret_optimizer_results(
            single_valued_constants_round3,
            model,
            variables,
            time_consts_round3,
            interpreter,
            percent_fed_from_model_round3,
            optimization_type="to_humans",
        )
        # interpreter.set_feed_and_biofuels(feed_and_biofuels_round3)
        # interpreter.set_meat_dictionary(meat_dictionary_round3)
        interpreted_results_round3.set_feed_and_biofuels(feed_and_biofuels_round3)
        interpreted_results_round3.set_meat_dictionary(meat_dictionary_round3)

        Validator.assert_fewer_calories_round2_than_round3(
            interpreted_results_round2, interpreted_results_round3
        )

        Validator.assert_feed_used_round3_below_feed_used_round2(
            interpreted_results_round2, interpreted_results_round3
        )

        return interpreted_results_round3

    def run_and_analyze_scenario(
        self,
        constants_for_params,
        time_consts_for_params,
        scenario_loader,
        create_pptx_with_all_countries,
        show_country_figures,
        figure_save_postfix,
        country_data,
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

        constants_loader = Parameters()

        (
            single_valued_constants_round1,
            time_consts_round1,
            feed_and_biofuels_round1,  # zero feed and biofuels
            biofuels_demand,  # biofuels requested by the user
            feed_demand,  # feed requested by the user
            max_feed_that_could_be_used_second_round,  # Max feed used if no limitation before shutoff
            meat_dictionary_zero_feed_biofuels,  # Meat if no feed used.
            meat_dictionary_second_round,  # Meat if all feed used.
        ) = constants_loader.compute_parameters_first_round(
            constants_for_params, time_consts_for_params, scenario_loader
        )
        validator = Validator()
        validator.ensure_all_time_constants_units_are_billion_kcals(time_consts_round1)
        ROUND_1_WAS_RUN_FLAG = False
        if (
            constants_for_params["ADD_STORED_FOOD"]
            or constants_for_params["ADD_OUTDOOR_GROWING"]
            or constants_for_params["ADD_SEAWEED"]
            or constants_for_params["ADD_CELLULOSIC_SUGAR"]
            or constants_for_params["ADD_METHANE_SCP"]
        ) and not (
            max_feed_that_could_be_used_second_round.all_equals_zero()
            and biofuels_demand.all_equals_zero()
        ):
            # if any of the feed or biofuel resources are made available to the model
            # and the user has not requested zero feed and biofuel

            (
                interpreted_results_round1,
                percent_fed_from_model_round1,
                single_valued_constants_round1,
            ) = self.run_round_1(
                single_valued_constants_round1,
                time_consts_round1,
                interpreter,
                feed_and_biofuels_round1,
                meat_dictionary_zero_feed_biofuels,
            )

            ROUND_1_WAS_RUN_FLAG = True

            Validator.assert_feed_used_below_feed_demand(
                feed_demand, interpreted_results_round1, round=1
            )
            Validator.assert_biofuels_used_below_biofuels_demand(
                biofuels_demand, interpreted_results_round1, round=1
            )

            # # Check that the animal populations are never increasing with time
            # Validator.assert_population_not_increasing(
            #     meat_dictionary_zero_feed_biofuels, round=1
            # )

            DISPLAY_MEAT_PRODUCED_IF_NO_FEED = True
            if DISPLAY_MEAT_PRODUCED_IF_NO_FEED:
                # because feed and biofuel are zero, feed and biofuels plot
                # most likely to be skipped unless there's some issue
                self.display_results_of_optimizer_round(
                    interpreted_results_round1,
                    country_data,
                    show_country_figures,
                    create_pptx_with_all_countries,
                    scenario_loader,
                    figure_save_postfix,
                    slaughter_title="Meat produced first round (no feed given to animals)",
                    feed_title="Feed first round (no feed given to animals)",
                    to_humans_title="Food to humans maximized, first round (no feed given to animals)",
                )

            interpreted_results_round2 = self.run_round_2(
                constants_loader,
                constants_for_params,
                interpreted_results_round1,
                percent_fed_from_model_round1,
                single_valued_constants_round1,
                time_consts_round1,
                interpreter,
                feed_and_biofuels_round1,
                max_feed_that_could_be_used_second_round,
                biofuels_demand,
                meat_dictionary_second_round,
            )

            Validator.assert_feed_used_below_feed_demand(
                feed_demand, interpreted_results_round2, round=2
            )
            Validator.assert_biofuels_used_below_biofuels_demand(
                biofuels_demand, interpreted_results_round2, round=2
            )

            if DISPLAY_MEAT_PRODUCED_IF_NO_FEED and (
                interpreted_results_round1.meat_dictionary
                == interpreted_results_round2.meat_dictionary
                and interpreted_results_round1.animal_population_dictionary
                == interpreted_results_round2.animal_population_dictionary
            ):
                # Meat produced from second round with no restriction is identical to with restrictions,
                # so skip replotting.
                slaughter_title = ""
            else:
                slaughter_title = "Max meat produced from second round calc (no restriction on feed before shutoff)"
                # make sure animal populations not increasing
                Validator.assert_population_not_increasing(
                    interpreted_results_round2.meat_dictionary, round=3
                )

            self.display_results_of_optimizer_round(
                interpreted_results_round2,
                country_data,
                show_country_figures,
                create_pptx_with_all_countries,
                scenario_loader,
                figure_save_postfix,
                slaughter_title=slaughter_title,
                feed_title="Feed for second round optimization, no restriction to animals before shutoff",
                to_humans_title="Humans fed only up to minimum needs",
            )
            interpreted_results_for_round3 = interpreted_results_round2
        else:
            # none of the feed or biofuel resources are made available to the model
            # or the user has not requested zero feed and biofuel

            print("")
            print("Skipped rounds 1 and 2 due to zero feed/biofuel")
            print("")

            interpreted_results_for_round3 = copy.deepcopy(interpreter)
            interpreted_results_for_round3.feed_sum_kcals_equivalent = Food(
                kcals=np.zeros(constants_for_params["NMONTHS"]),
                fat=np.zeros(constants_for_params["NMONTHS"]),
                protein=np.zeros(constants_for_params["NMONTHS"]),
                kcals_units="billion kcals each month",
                fat_units="thousand tons each month",
                protein_units="thousand tons each month",
            )

            interpreted_results_for_round3.biofuels_sum_kcals_equivalent = Food(
                kcals=np.zeros(constants_for_params["NMONTHS"]),
                fat=np.zeros(constants_for_params["NMONTHS"]),
                protein=np.zeros(constants_for_params["NMONTHS"]),
                kcals_units="billion kcals each month",
                fat_units="thousand tons each month",
                protein_units="thousand tons each month",
            )

        interpreted_results_round3 = self.run_round_3(
            constants_loader,
            constants_for_params,
            single_valued_constants_round1,
            time_consts_round1,
            interpreted_results_for_round3,
            feed_and_biofuels_round1,
            interpreter,
        )

        Validator.assert_feed_used_below_feed_demand(
            feed_demand, interpreted_results_round3, round=3
        )
        Validator.assert_biofuels_used_below_biofuels_demand(
            biofuels_demand, interpreted_results_round3, round=3
        )

        Validator.assert_population_not_increasing(
            interpreted_results_round3.meat_dictionary, round=3
        )

        Validator.assert_feed_and_biofuel_used_is_zero_if_humans_are_starving(
            interpreted_results_round3
        )
        if ROUND_1_WAS_RUN_FLAG:
            Validator.make_sure_everyone_fed_if_round1_was_above_2100kcals(
                percent_fed_from_model_round1,
                interpreted_results_round3.percent_people_fed,
            )

        self.display_results_of_optimizer_round(
            interpreted_results_round3,
            country_data,
            show_country_figures,
            create_pptx_with_all_countries,
            scenario_loader,
            figure_save_postfix,
        )
        print("")
        print("Percent people fed")
        print(round(interpreted_results_round3.percent_people_fed, 2))
        print("")

        return interpreted_results_round3

    def interpret_optimizer_results(
        self,
        single_valued_constants,
        model,
        variables,
        time_consts,
        interpreter,
        percent_fed_from_model,
        optimization_type,
    ):
        validator = Validator()

        extractor = Extractor(single_valued_constants)
        #  get values from all the optimizer in list and integer formats
        extracted_results = extractor.extract_results(model, variables, time_consts)

        # TODO: eventually all the values not directly solved by the optimizer should
        # be removed from extracted_results

        #  interpret the results, nicer for plotting, reporting, and printing results
        interpreted_results = interpreter.interpret_results(extracted_results)

        # ensure no errors were made in the extraction and interpretation, or if the
        # optimizer did not correctly satisfy constraints within a reasonable margin
        # of error
        validator.validate_results(
            extracted_results,
            interpreted_results,
            time_consts,
            percent_fed_from_model,
            optimization_type,
            single_valued_constants["inputs"]["COUNTRY_CODE"],
        )

        return interpreted_results

    def run_optimizer(self, single_valued_constants, time_consts):
        """
        Runs the optimizer and returns the model, variables, and constants
        """
        optimizer = Optimizer(single_valued_constants, time_consts)
        validator = Validator()

        (
            model,
            variables,
            maximize_constraints,
            percent_fed_from_model,
        ) = optimizer.optimize_to_humans(single_valued_constants, time_consts)

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

        return (model, variables, percent_fed_from_model)

    def set_depending_on_option(self, country_data, scenario_option):
        scenario_loader = Scenarios()

        time_consts_for_params = {}

        # SCALE

        if scenario_option["scale"] == "global":
            constants_for_params = scenario_loader.init_global_food_system_properties()
            constants_for_params["COUNTRY_CODE"] = "global"
        elif scenario_option["scale"] == "country":
            constants_for_params = scenario_loader.init_country_food_system_properties(
                country_data
            )

            constants_for_params["COUNTRY_CODE"] = country_data["iso3"]
        else:
            scenario_is_correct = False
            constants_for_params["COUNTRY_CODE"] = "global"

            assert (
                scenario_is_correct
            ), "You must specify 'scale' key as global,or country"

        constants_for_params["NMONTHS"] = scenario_option["NMONTHS"]

        # STORED FOOD

        if scenario_option["stored_food"] == "zero":
            constants_for_params = scenario_loader.set_no_stored_food(
                constants_for_params
            )
        elif scenario_option["stored_food"] == "baseline":
            constants_for_params = scenario_loader.set_baseline_stored_food(
                constants_for_params
            )
        else:
            scenario_is_correct = False

            assert (
                scenario_is_correct
            ), "You must specify 'stored_food' key as zero, or baseline"

        # END_SIMULATION_STOCKS_RATIO

        if scenario_option["end_simulation_stocks_ratio"] == "zero":
            constants_for_params = scenario_loader.set_stored_food_buffer_zero(
                constants_for_params
            )
        elif (
            scenario_option["end_simulation_stocks_ratio"] == "no_stored_between_years"
        ):
            constants_for_params = scenario_loader.set_no_stored_food_between_years(
                constants_for_params
            )
        elif scenario_option["end_simulation_stocks_ratio"] == "baseline":
            constants_for_params = scenario_loader.set_stored_food_buffer_as_baseline(
                constants_for_params
            )
        else:
            scenario_is_correct = False

            assert (
                scenario_is_correct
            ), "You must specify 'end_simulation_stocks_ratio' key as zero, no_stored_between_years, or baseline"

        # SHUTOFF
        if scenario_option["shutoff"] == "immediate":
            constants_for_params = scenario_loader.set_immediate_shutoff(
                constants_for_params
            )
        elif scenario_option["shutoff"] == "one_month_delayed_shutoff":
            constants_for_params = scenario_loader.set_one_month_delayed_shutoff(
                constants_for_params
            )

        elif scenario_option["shutoff"] == "short_delayed_shutoff":
            constants_for_params = scenario_loader.set_short_delayed_shutoff(
                constants_for_params
            )
        elif scenario_option["shutoff"] == "long_delayed_shutoff":
            constants_for_params = scenario_loader.set_long_delayed_shutoff(
                constants_for_params
            )
        elif scenario_option["shutoff"] == "continued":
            constants_for_params = scenario_loader.set_continued_feed_biofuels(
                constants_for_params
            )
        else:
            scenario_is_correct = False

            assert scenario_is_correct, """You must specify 'shutoff' key as immediate,short_delayed_shutoff,one_month_delayed_shutoff,
            long_delayed_shutoff, or continued"""

        # WASTE

        if scenario_option["waste"] == "zero":
            constants_for_params = scenario_loader.set_waste_to_zero(
                constants_for_params
            )
        elif scenario_option["waste"] == "tripled_prices_in_country":
            constants_for_params = scenario_loader.set_country_waste_to_tripled_prices(
                constants_for_params, country_data
            )
        elif scenario_option["waste"] == "doubled_prices_in_country":
            constants_for_params = scenario_loader.set_country_waste_to_doubled_prices(
                constants_for_params, country_data
            )
        elif scenario_option["waste"] == "baseline_in_country":
            constants_for_params = scenario_loader.set_country_waste_to_baseline_prices(
                constants_for_params, country_data
            )
        elif scenario_option["waste"] == "tripled_prices_globally":
            constants_for_params = scenario_loader.set_global_waste_to_tripled_prices(
                constants_for_params
            )
        elif scenario_option["waste"] == "doubled_prices_globally":
            constants_for_params = scenario_loader.set_global_waste_to_doubled_prices(
                constants_for_params
            )
        elif scenario_option["waste"] == "baseline_globally":
            constants_for_params = scenario_loader.set_global_waste_to_baseline_prices(
                constants_for_params
            )
        else:
            scenario_is_correct = False

            assert scenario_is_correct, """You must specify 'waste' key as zero,tripled_prices_in_country,
            doubled_prices_in_country,baseline_in_country,tripled_prices_globally,
            doubled_prices_globally,or baseline_globally"""

        # NUTRITION

        if scenario_option["nutrition"] == "baseline":
            constants_for_params = scenario_loader.set_baseline_nutrition_profile(
                constants_for_params
            )
        elif scenario_option["nutrition"] == "catastrophe":
            constants_for_params = scenario_loader.set_catastrophe_nutrition_profile(
                constants_for_params
            )
        else:
            scenario_is_correct = False

            assert (
                scenario_is_correct
            ), "You must specify 'nutrition' key as baseline, or catastrophe"

        # INTAKE CONSTRAINTS

        if scenario_option["intake_constraints"] == "enabled":
            constants_for_params = scenario_loader.set_intake_constraints_to_enabled(
                constants_for_params
            )
        elif scenario_option["intake_constraints"] == "disabled_for_humans":
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

        if scenario_option["seasonality"] == "no_seasonality":
            constants_for_params = scenario_loader.set_no_seasonality(
                constants_for_params
            )
        elif scenario_option["seasonality"] == "country":
            constants_for_params = scenario_loader.set_country_seasonality(
                constants_for_params, country_data
            )
        elif scenario_option["seasonality"] == "baseline_globally":
            constants_for_params = scenario_loader.set_global_seasonality_baseline(
                constants_for_params
            )
        elif scenario_option["seasonality"] == "nuclear_winter_globally":
            constants_for_params = (
                scenario_loader.set_global_seasonality_nuclear_winter(
                    constants_for_params
                )
            )
        else:
            scenario_is_correct = False

            assert scenario_is_correct, """You must specify 'seasonality' key as no_seasonality, country,
             baseline_globally,or nuclear_winter_globally"""

        # GRASSES
        if scenario_option["grasses"] == "baseline":
            constants_for_params = scenario_loader.set_grasses_baseline(
                constants_for_params
            )
        elif scenario_option["grasses"] == "global_nuclear_winter":
            constants_for_params = scenario_loader.set_global_grasses_nuclear_winter(
                constants_for_params
            )
        elif scenario_option["grasses"] == "country_nuclear_winter":
            constants_for_params = scenario_loader.set_country_grasses_nuclear_winter(
                constants_for_params, country_data
            )
        elif scenario_option["grasses"] == "all_crops_die_instantly":
            constants_for_params = scenario_loader.set_country_grasses_to_zero(
                constants_for_params
            )
        else:
            scenario_is_correct = False

            assert scenario_is_correct, """You must specify 'grasses' key as baseline,
            global_nuclear_winter,all_crops_die_instantly, or country_nuclear_winter"""

        # FISH

        if scenario_option["fish"] == "zero":
            time_consts_for_params = scenario_loader.set_fish_zero(
                constants_for_params, time_consts_for_params
            )
        elif scenario_option["fish"] == "nuclear_winter":
            time_consts_for_params = scenario_loader.set_fish_nuclear_winter_reduction(
                time_consts_for_params
            )
        elif scenario_option["fish"] == "baseline":
            time_consts_for_params = scenario_loader.set_fish_baseline(
                constants_for_params, time_consts_for_params
            )
        else:
            scenario_is_correct = False

            assert (
                scenario_is_correct
            ), "You must specify 'fish' key as either zero, nuclear_winter,or baseline"

        # CROPS

        if scenario_option["crop_disruption"] == "zero":
            constants_for_params = scenario_loader.set_disruption_to_crops_to_zero(
                constants_for_params
            )
        elif scenario_option["crop_disruption"] == "global_nuclear_winter":
            constants_for_params = (
                scenario_loader.set_nuclear_winter_global_disruption_to_crops(
                    constants_for_params
                )
            )
        elif scenario_option["crop_disruption"] == "country_nuclear_winter":
            constants_for_params = (
                scenario_loader.set_nuclear_winter_country_disruption_to_crops(
                    constants_for_params, country_data
                )
            )
        elif scenario_option["crop_disruption"] == "all_crops_die_instantly":
            constants_for_params = scenario_loader.set_zero_crops(constants_for_params)
        else:
            scenario_is_correct = False

            assert scenario_is_correct, """You must specify 'crop_disruption' key as either zero,
            global_nuclear_winter, all_crops_die_instantly, or country_nuclear_winter"""

        # PROTEIN

        if scenario_option["protein"] == "required":
            print("ERROR: fat and protein not working in this version of the model")
            print("(compute parameters in the second round would need to be modified)")
            sys.exit()
            constants_for_params = scenario_loader.include_protein(constants_for_params)
        elif scenario_option["protein"] == "not_required":
            constants_for_params = scenario_loader.dont_include_protein(
                constants_for_params
            )
        else:
            scenario_is_correct = False

            assert (
                scenario_is_correct
            ), "You must specify 'protein' key as either required, or not_required"

        # FAT

        if scenario_option["fat"] == "required":
            print("ERROR: fat and protein not working in this version of the model")
            print("(compute parameters in the second round would need to be modified)")
            sys.exit()
            constants_for_params = scenario_loader.include_fat(constants_for_params)
        elif scenario_option["fat"] == "not_required":
            constants_for_params = scenario_loader.dont_include_fat(
                constants_for_params
            )
        else:
            scenario_is_correct = False

            assert (
                scenario_is_correct
            ), "You must specify 'fat' key as either required, or not_required"

        # CULLING

        if scenario_option["cull"] == "do_eat_culled":
            constants_for_params = scenario_loader.cull_animals(constants_for_params)
        elif scenario_option["cull"] == "dont_eat_culled":
            constants_for_params = scenario_loader.dont_cull_animals(
                constants_for_params
            )
        else:
            scenario_is_correct = False

            assert (
                scenario_is_correct
            ), "You must specify 'cull' key as either do_eat_culled, or dont_eat_culled"

        # SCENARIO

        if scenario_option["scenario"] == "all_resilient_foods":
            constants_for_params = scenario_loader.get_all_resilient_foods_scenario(
                constants_for_params
            )
        elif scenario_option["scenario"] == "all_resilient_foods_and_more_area":
            constants_for_params = (
                scenario_loader.get_all_resilient_foods_and_more_area_scenario(
                    constants_for_params
                )
            )
        elif scenario_option["scenario"] == "no_resilient_foods":
            constants_for_params = scenario_loader.get_no_resilient_food_scenario(
                constants_for_params
            )
        elif scenario_option["scenario"] == "seaweed":
            constants_for_params = scenario_loader.get_seaweed_scenario(
                constants_for_params
            )
        elif scenario_option["scenario"] == "methane_scp":
            constants_for_params = scenario_loader.get_methane_scp_scenario(
                constants_for_params
            )
        elif scenario_option["scenario"] == "cellulosic_sugar":
            constants_for_params = scenario_loader.get_cellulosic_sugar_scenario(
                constants_for_params
            )
        elif scenario_option["scenario"] == "relocated_crops":
            constants_for_params = scenario_loader.get_relocated_crops_scenario(
                constants_for_params
            )
        elif scenario_option["scenario"] == "greenhouse":
            constants_for_params = scenario_loader.get_greenhouse_scenario(
                constants_for_params
            )
        elif scenario_option["scenario"] == "industrial_foods":
            constants_for_params = scenario_loader.get_industrial_foods_scenario(
                constants_for_params
            )
        else:
            scenario_is_correct = False

            assert scenario_is_correct, """You must specify 'scenario' key as either baseline_climate,
            all_resilient_foods,all_resilient_foods_and_more_area,no_resilient_foods,seaweed,methane_scp,
            cellulosic_sugar,industrial_foods,relocated_crops or greenhouse"""

        if scenario_option["meat_strategy"] == "reduce_breeding":
            constants_for_params = scenario_loader.set_breeding_to_greatly_reduced(
                constants_for_params
            )
        elif scenario_option["meat_strategy"] == "baseline_breeding":
            constants_for_params = scenario_loader.set_to_baseline_breeding(
                constants_for_params
            )
        else:
            scenario_is_correct = False

            assert scenario_is_correct, """You must specify 'meat_strategy' key as either ,
            reduce_breeding or baseline_breeding"""

        return constants_for_params, time_consts_for_params, scenario_loader
