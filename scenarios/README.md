# Simulation Settings Guide

## Running Simulations

First, ensure you have followed the installation instructions and have the required Python packages installed and activated if using conda/mamba, as well as having done the pip install command as described in the root directory readme.

To run the simulations configured in a YAML file:

```
./run_scenarios_from_yaml.py <show_country_figures> <show_map_figures> <yaml_file> 
```

- `show_country_figures` - True/False to show country-specific figures
- `show_map_figures` - True/False to use colored maps
- `yaml_file` - Path to YAML file containing scenarios

The script will iterate through each scenario, running the simulation with those parameters.

The output from each scenario will be saved with a filename appendix matching the scenario name for later analysis.

## YAML Configuration

The simulation scenarios and parameters are defined in a YAML file such as `scenarios.yaml`. 

The top-level keys in the YAML file are:

- `settings`: Defines general settings like countries to run simulations for.

- `simulations`: Contains a dictionary of named scenarios to run.

Each scenario under `simulations` has:

- A `title` that is displayed when running that scenario.

- Parameter keys like `scale`, `seasonality`, `waste` etc. that match the options described in the README.

For example:

```yaml
settings:
  NMONTHS: 120
  countries:
    - USA
    - India

simulations:
  baseline:
    title: Current Conditions
    scale: country
    seasonality: baseline_globally
    grasses: baseline

  disrupted:  
    title: Disrupted Climate 
    scale: country
    seasonality: nuclear_winter_globally
    grasses: country_nuclear_winter
    crop_disruption: country_nuclear_winter
    fish: nuclear_winter
```

## Allowed Values
- **settings**:
  - `NMONTHS`: The number of months of the simulation to run
  - `countries`: the countries to run

- **simulations**:
  - **scale**: 
    - `global` - Runs simulation for entire world, with continued trade between all countries.
    - `country` - Runs simulation for a specific country

  - **seasonality**:
    - `no_seasonality` - Uses average crop production throughout year
    - `country` - Uses monthly crop production data for that country
    - `baseline_globally` - Uses typical global monthly crop seasonality. Only applies to `global` scale option
    - `nuclear_winter_globally` - Alters monthly seasonality to model nuclear winter conditions based on seasonality from the tropics. Only applies to `global` scale option

  - **grasses**:
    - `baseline` - Uses current grass/grazing production
    - `global_nuclear_winter` - Reduces grass production over time based on global nuclear winter estimates. Only applies to `global` scale option
    - `country_nuclear_winter` - Reduces grass production over time based on country-specific nuclear winter estimates
    - `all_crops_die_instantly` - Sets grass production to 0 immediately

  - **crop_disruption**:
    - `zero` - Uses current crop production
    - `global_nuclear_winter` - Reduces crop production over time based on global nuclear winter estimates. Only applies to `global` scale option
    - `country_nuclear_winter` - Reduces crop production over time based on country-specific nuclear winter estimates
    - `all_crops_die_instantly` - Sets crop production to 0 immediately
    
  - **scenario**:
    - `no_resilient_foods` - Uses current food production only
    - `all_resilient_foods` - Enables scaled up seaweed, cellulosic sugar, methane SCP
    - `all_resilient_foods_and_more_area` - Enables resilient foods and expands cropland area
    - `seaweed` - Enables scaled up seaweed production
    - `methane_scp` - Enables scaled up methane SCP production
    - `cellulosic_sugar` - Enables scaled up cellulosic sugar production
    - `industrial_foods` - Enables scaled up cellulosic sugar and methane_scp production
    - `relocated_crops` - Enables relocation of crops to more optimal growing regions
    - `greenhouse` - Enables expanded greenhouse production
    
  - **fish**:
    - `zero` - No fish production
    - `baseline` - Uses current fish production
    - `nuclear_winter` - Reduces fish production over time based on nuclear winter estimates
    
  - **waste**:
    - `zero` - No food waste
    - `tripled_prices_in_country` - Sets retail/consumption waste based on food prices 3x current level in that country
    - `doubled_prices_in_country` - Sets retail/consumption waste based on food prices 2x current level in that country
    - `baseline_in_country` - Uses current food waste estimates for that country
    - `tripled_prices_globally` - Sets retail/consumption waste based on global food prices 3x current level. Only applies to `global` scale option
    - `doubled_prices_globally` - Sets retail/consumption waste based on global food prices 2x current level. Only applies to `global` scale option
    - `baseline_globally` - Uses current global food waste estimates. Only applies to `global` scale option
    
  - **nutrition**:
    - `baseline` - Uses typical nutritional requirements
    - `catastrophe` - Uses minimum sufficient nutritional requirements

  - **intake_constraints**:
    - `enabled` - Applies constraints on daily intake based on maximum nutritional requirements humans can consume. constraints on feed and biofuels also apply.
    - `disabled_for_humans` - No constraints on percentage of food intake for surviving humans. However, constraints on feed and biofuels still apply.

  - **stored_food**:
    - `zero` - No stored food available at start of simulation
    - `baseline` - All stored food estimated available at start of simulation
    
  - **end_simulation_stocks_ratio**:
    - `zero` - No food stocks maintained at the end of the simulation 
    - `baseline` - Reduces available stored food by current lowest month stocks estimates, to account for the need to maintain a buffer at the end of the simulation
    - `no_stored_food_between_years` - All stored food available at first month, but then no usage of food storage allowed between each 12 month period.

  - **shutoff**:
    - `immediate` - Immediately sets animal feed and biofuel production to 0
    - `short_delayed_shutoff` - Phases out animal feed and biofuel production over a short timeframe (2 mo feed, 1 mo biofuel)
    - `long_delayed_shutoff` - Phases out animal feed and biofuel production over a longer timeframe (3 mo feed, 2 mo biofuel)
    - `continued` - Attempts to run continued animal feed and biofuel production as in present day
    
  - **cull**:
    - `do_eat_culled` - Includes meat from culled animals
    - `dont_eat_culled` - Discards meat from culled animals
    
  - **fat**:
    - `required` - Tracks and requires sufficient fat in diet
    - `not_required` - Does not track fat requirements
    
  - **protein**:
    - `required` - Tracks and requires sufficient protein in diet
    - `not_required` - Does not track protein requirements

  - **meat_strategy**:
    - `reduce_breeding` - Reduce breeding in accordance to "reduced" column in data/no_food_trade/animal_feed_data/species_options.csv. Essentiall, nearly all breeding is stopped immediately after the nuclear winter.
    - `baseline_breeding` - Normal breeding levels to maintain livestock levels, "baseline" column in data/no_food_trade/animal_feed_data/species_options.csv

## Detailed Notes

The `scale` setting determines whether the simulation is run for the entire world (`global`) or a single specified country (`country`).

The `seasonality` setting controls whether crop production is assumed constant throughout the year (`no_seasonality`), varies by month based on the selected country's data (`country`), follows typical global seasonal variations (`baseline_globally`), or is altered to match expected conditions under a nuclear winter scenario (`nuclear_winter_globally`).

The `grasses` setting determines grass/grazing production. `baseline` uses current estimates, while `global_nuclear_winter` and `country_nuclear_winter` reduce production over time based on nuclear winter impact estimates. `all_crops_die_instantly` immediately sets grass production to zero.

Similarly, the `crop_disruption` setting controls how crop production is affected. `zero` uses current production, while `global_nuclear_winter` and `country_nuclear_winter` gradually reduce it. `all_crops_die_instantly` sets production to zero immediately.

The `scenario` setting enables different resilient/alternative foods in the simulation. `no_resilient_foods` uses only current production. `all_resilient_foods` scales up seaweed, cellulosic sugar, and methane SCP, while `all_resilient_foods_and_more_area` also expands cropland. Others enable individual resilient foods.

For `fish`, `baseline` uses current production and `nuclear_winter` reduces it over time.

The `waste` setting controls the percent of food wasted at the retail and consumption stages, either based on current estimates or scaled based on food prices.

`nutrition` sets whether typical or minimum nutritional requirements are used.

`buffer` sets the amount of food stocks and buffers available at the start of the simulation.

`shutoff` controls when animal feed and biofuel production are reduced or eliminated.

`cull` determines whether meat from culled animals is included.

`fat` and `protein` control whether meeting fat and protein requirements are tracked.

Finally, `meat_strategy` sets whether feed is prioritized for dairy cows, then to pigs and chickens, then to cattle for beef (`efficient`), or distributed proportionally to present-day ratios of feed (`inefficient`).
