"""

This function runs a single optimization by computing the parameters,
running the parameters onto the optimizer, extracting the results, and interpreting the
results into more useful values for plotting and scenario evaluation

Created on Tue Jul 19

@author: morgan
"""
from src.optimizer.optimizer import Optimizer
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
        This function runs a scenario by computing the necessary parameters, running the optimizer,
        extracting data from the optimizer, interpreting the results, validating the results, and
        optionally printing an output with people fed.

        Args:
            constants_for_params (dict): A dictionary containing constants for the scenario.
            scenarios_loader (ScenarioLoader): An instance of the ScenarioLoader class.

        Returns:
            dict: A dictionary containing the interpreted results.

        """
        # Create instances of the Interpreter and Validator classes
        interpreter = Interpreter()
        validator = Validator()

        # Compute the necessary parameters for the optimizer
        single_valued_constants, time_consts, feed_biofuels = self.compute_parameters(
            constants_for_params, scenarios_loader
        )

        # Run the optimizer to optimize effective people fed based on all the constants we've determined
        model, variables, single_valued_constants, time_consts = self.run_optimizer(
            single_valued_constants, time_consts
        )

        # Create an instance of the Extractor class
        extractor = Extractor(single_valued_constants)

        # Extract values from the optimizer in list and integer formats
        extracted_results = extractor.extract_results(model, variables, time_consts)

        # TODO: eventually all the values not directly solved by the optimizer should be removed from extracted_results

        # Interpret the results, nicer for plotting, reporting, and printing results
        interpreted_results = interpreter.interpret_results(
            extracted_results, time_consts
        )

        # Ensure no errors were made in the extraction and interpretation, or if the optimizer did not correctly satisfy
        # constraints within a reasonable margin of error
        validator.validate_results(model, extracted_results, interpreted_results)

        # Print the kcals per capita per day if PRINT_NEEDS_RATIO is True
        PRINT_NEEDS_RATIO = False
        if PRINT_NEEDS_RATIO:
            interpreter.print_kcals_per_capita_per_day(interpreted_results)

        # Return the interpreted results
        return interpreted_results

    def compute_parameters(self, constants_for_params, scenarios_loader):
        """
        This function computes the parameters based on the constants and scenarios provided.
        It returns the resulting constants.

        Args:
            constants_for_params (dict): A dictionary containing the constants for the parameters.
            scenarios_loader (ScenariosLoader): An instance of the ScenariosLoader class.

        Returns:
            tuple: A tuple containing the single_valued_constants, time_consts, and feed_and_biofuels.

        """

        # Create an instance of the Parameters class
        constants_loader = Parameters()

        # Compute the parameters using the constants and scenarios provided
        (
            single_valued_constants,
            time_consts,
            feed_and_biofuels,
        ) = constants_loader.compute_parameters(constants_for_params, scenarios_loader)

        # Return the resulting constants
        return single_valued_constants, time_consts, feed_and_biofuels

    def run_optimizer(self, single_valued_constants, time_consts):
        """
        Runs the optimizer and returns the model, variables, and constants

        Args:
            single_valued_constants (dict): A dictionary of single-valued constants
            time_consts (dict): A dictionary of time constants

        Returns:
            tuple: A tuple containing the model, variables, single_valued_constants, and time_consts
        """
        # Create an instance of the Optimizer class
        optimizer = Optimizer(single_valued_constants, time_consts)

        # Create an instance of the Validator class
        validator = Validator()

        # Call the optimize method of the optimizer instance to optimize the model
        # and get the optimized model, variables, maximize_constraints, single_valued_constants, and time_consts
        (
            model,
            variables,
            maximize_constraints,
            single_valued_constants,
            time_consts,
        ) = optimizer.optimize_to_humans(single_valued_constants, time_consts)

        # Set CHECK_CONSTRAINTS to False to skip validation
        CHECK_CONSTRAINTS = False

        # If CHECK_CONSTRAINTS is True, validate the model
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

        # Return the optimized model, variables, single_valued_constants, and time_consts
        return (model, variables, single_valued_constants, time_consts)

    def set_depending_on_option(self, country_data, scenario_option):
        scenario_loader = Scenarios()
        # SCALE

        if scenario_option["scale"] == "global":
            constants_for_params = scenario_loader.init_global_food_system_properties()
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

        # EXCESS
        constants_for_params = scenario_loader.set_excess_to_zero(constants_for_params)

        # BUFFER

        if scenario_option["buffer"] == "zero":
            constants_for_params = scenario_loader.set_stored_food_buffer_zero(
                constants_for_params
            )
        elif scenario_option["buffer"] == "no_stored_between_years":
            constants_for_params = scenario_loader.set_no_stored_food(
                constants_for_params
            )
        elif scenario_option["buffer"] == "baseline":
            constants_for_params = scenario_loader.set_stored_food_buffer_as_baseline(
                constants_for_params
            )
        else:
            scenario_is_correct = False

            assert (
                scenario_is_correct
            ), "You must specify 'buffer' key as zero, no_stored_food, or baseline"

        # SHUTOFF

        if scenario_option["shutoff"] == "immediate":
            constants_for_params = scenario_loader.set_immediate_shutoff(
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
        elif scenario_option["shutoff"] == "reduce_breeding":
            constants_for_params = scenario_loader.reduce_breeding(constants_for_params)
        else:
            scenario_is_correct = False

            assert scenario_is_correct, """You must specify 'shutoff' key as immediate,short_delayed_shutoff,reduce_breeding,
            long_delayed_shutoff,or continued"""

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
        else:
            scenario_is_correct = False

            assert scenario_is_correct, """You must specify 'grasses' key as baseline,
            global_nuclear_winter,or country_nuclear_winter"""

        # FISH

        if scenario_option["fish"] == "nuclear_winter":
            constants_for_params = scenario_loader.set_fish_nuclear_winter_reduction(
                constants_for_params
            )
        elif scenario_option["fish"] == "baseline":
            constants_for_params = scenario_loader.set_fish_baseline(
                constants_for_params
            )
        else:
            scenario_is_correct = False

            assert (
                scenario_is_correct
            ), "You must specify 'fish' key as either nuclear_winter,or baseline"

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
        else:
            scenario_is_correct = False

            assert scenario_is_correct, """You must specify 'crop_disruption' key as either zero,
            global_nuclear_winter,or country_nuclear_winter"""

        # PROTEIN

        if scenario_option["protein"] == "required":
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
        else:
            scenario_is_correct = False

            assert scenario_is_correct, """You must specify 'scenario' key as either baseline_climate,
            all_resilient_foods,all_resilient_foods_and_more_area,no_resilient_foods,seaweed,methane_scp,
            cellulosic_sugar,relocated_crops or greenhouse"""

        if scenario_option["meat_strategy"] == "efficient_meat_strategy":
            constants_for_params = scenario_loader.set_efficient_feed_grazing_strategy(
                constants_for_params
            )
        elif scenario_option["meat_strategy"] == "inefficient_meat_strategy":
            constants_for_params = (
                scenario_loader.set_unchanged_proportions_feed_grazing(
                    constants_for_params
                )
            )
        elif scenario_option["meat_strategy"] == "reduce_breeding":
            constants_for_params = scenario_loader.set_feed_based_on_livestock_levels(
                constants_for_params
            )
        else:
            scenario_is_correct = False

            assert scenario_is_correct, """You must specify 'meat_strategy' key as either efficient_meat_strategy,
            or inefficient_meat_strategy"""

        return constants_for_params, scenario_loader
