#!/bin/bash
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
