#!/bin/bash
# @Author Morgan Rivers
# @Date 2022-10-25
#
# Runs a suite of scenarios involved with no food trade globally.
#
# "single" python runs under a single set of assumptions about adaptation (there is
# a default set of assumptions used in the src/scenarios/run_model_defaults_no_trade.py 
# run_model_defaults_no_trade function).
#
# "multi" runs over the complete combination of all scenario options defined in the 
# src/scenarios/run_model_defaults_no_trade.py,
# create_several_maps_with_different_assumptions function.

cd ../src/scenarios

# create a plot for each country with a single set of assumptions
echo ""
echo ""
echo ""
echo "BASELINE"
echo ""
echo ""
python run_model_no_trade_baseline.py single pptx no_plot
echo "================================================="
echo ""
echo ""
echo "NO_RESILIENT_FOODS"
echo ""
echo ""
python run_model_no_trade_no_resilient_foods.py single pptx no_plot
echo "================================================="
echo ""
echo ""
echo "WITH_RESILIENT_FOODS"
echo ""
echo ""
python run_model_no_trade_with_resilient_foods.py single pptx no_plot

# create a map plot for the world with various sets of assumptions
echo ""
echo ""
echo ""
echo "BASELINE"
echo ""
echo ""
python run_model_no_trade_baseline.py multi pptx no_plot
echo "================================================="
echo ""
echo ""
echo "NO_RESILIENT_FOODS"
echo ""
echo ""
python run_model_no_trade_no_resilient_foods.py multi pptx no_plot
echo "================================================="
echo ""
echo ""
echo "WITH_RESILIENT_FOODS"
echo ""
echo ""
echo ""
python run_model_no_trade_with_resilient_foods.py multi pptx no_plot
echo "done"
cd ../../scripts
