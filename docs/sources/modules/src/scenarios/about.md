# About the Scenarios directory

Running a script in scenarios is done after completing import of the scripts, if no_food_trade scenarios are being run. Files in scenarios/ are either utility files used to specify the scenarios or provide an intermediary interface to allow other scripts to run the model in a particular way, scripts used to process and run specific scenarios for the nuclear winter with or without global food trade between trading blocs, or scripts which plot the results of these scenario runs. The scenarios are all either involving full food trade or no food trade between trading blocs, as determined by the trading bloc data in no_food_trade/computer_readable_combined.csv and globally-aggregated data stored in scenarios.py.


Utility files used to specify the scenarios are: scenarios.py
Utility files used to provide an intermediary interface to allow other scripts to run the model in a particular way are: run_model_no_trade.py, run_scenario.py

Scripts used to process and run specific scenarios for the nuclear winter with global food trade between trading blocs: run_model_with_resilient_foods.py, run_model_baseline.py, run_model_no_resilient_foods.py, create_figure_3abcd.py

Scripts which plot the results of these scenario runs:
plot_primary_food.py

Scripts used to process and run specific scenarios for the nuclear winter without global food trade between trading blocs: create_figure_1ab.py, create_figure_2abcde.py, run_model_no_trade_baseline.py, run_model_no_trade_no_resilient_foods.py, run_model_no_trade_with_resilient_foods.py, reproduce_xia_et_al_USA.py, run_USA_with_improved_numbers.py

The files which simply plot results are: plot_primary_food.py

The scenarios are run under a single set of assumptions or multiple sets of assumptions.  use input data stored in data/no_food_trade/computer_readable_combined.csv and use them to ev  The python files in this directory are all the ways that the model can be run.

Overall, the scripts in the scenarios folder interrelate as follows:

 ( run_model_with_resilient_foods.py,
   run_model_baseline.py,
   run_model_no_resilient_foods.py,
   create_figure_3abcd.py )
       ==calls=for=each=scenario==>
            run_scenario.py


 ( create_figure_1ab.py,
   create_figure_2abcde.py,
   reproduce_xia_et_al_USA.py,
   run_USA_with_improved_numbers.py,
   run_model_no_trade_with_resilient_foods.py,
   run_model_no_trade_no_resilient_foods.py,
   run_model_no_trade_baseline.py )
      ==call=with=scenarios=defined==>
          run_model_no_trade.py

 run_model_no_trade.py ==calls=for=each=scenario==> run_scenario.py

In the case of no food trade:
 scenarios.py <==loads== data/no_food_trade/computer_readable_combined.csv

 run_scenario.py <==loads== scenarios.py


Next, the run_scenario.py file calls the optimizer as follows in order to produce results for each scenario:

run_scenario.py 
    ==calls=in=this=order=>
        src/optimizer/parameters.py
        src/optimizer/optimizer.py
        src/optimizer/extract_results.py
        src/optimizer/interpret_results.py
        src/optimizer/validate_results.py

Finally the results are returned from run_scenario back up the call chain in reverse order.