# ALLFED Integrated Food System Model

---
![Testing](https://github.com/allfed/allfed-integrated-model/actions/workflows/testing.yml/badge.svg)
[![DOI](https://zenodo.org/badge/380878388.svg)](https://zenodo.org/badge/latestdoi/380878388)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

---
An integrated economic+food supply model for resilient foods in nuclear winter

# Run the model

* You can create a varierety of different scenarios with this model. A collection of possible scenarios are already available in the scenarios folder (e.g. `run_model_with_resilient_foods.py`).
* A scenario is created by creating a new instance of the Scenario class in `scenario.py`. This class contains a collection of methods that provide your model with the parameter value it needs to run. Here you can also change the parameter values if you want to change the model to your specifications.
* Once you got all your parameter values ready you create an Instance of the Parameter class from `parameter.py`. This class allows you to initialize the model with the parameter values you defined.
* Finally to create an instance of the Optimizer class from `optimizer.py` and provide it with your parameters. This will run the model itself and optimize it.

# How the model works in general

![Flow Chart](https://raw.githubusercontent.com/allfed/allfed-integrated-model/main/docs/overview.png)

### Using Colab (most users use this):
The interactive model runs off colab. It doesn't require any downloading or code, you just need to hit the right buttons as they show up. Here's a demo:

First click on the "notebooks" folder in the allfed-integrated-model directory.

![step2](https://raw.githubusercontent.com/allfed/allfed-integrated-model/main/docs/step2.png)

Open 'example_optimize.ipynb'

![step3](https://raw.githubusercontent.com/allfed/allfed-integrated-model/main/docs/step3.png)

Click 'Open in Colab'.

![step4](https://raw.githubusercontent.com/allfed/allfed-integrated-model/main/docs/step4.png)

Select 'Authorize with github'.

![step5](https://raw.githubusercontent.com/allfed/allfed-integrated-model/main/docs/step5.png)

Select 'OK'.

![step6](https://raw.githubusercontent.com/allfed/allfed-integrated-model/main/docs/step6.png)

For the repository, select 'allfed/allfed-integrated-model' branch 'main', then click on the item labelled under Path, 'notebooks/example_optimize.ipynb'.

Now follow the instructions in the Jupyter notebook. Run each line of the Jupyter notebook in succession to view results of the paper.

Please let me know if any of these steps go awry! (contact morgan [at] allfed [dot] info)

#### Dependency management with Anaconda
The integrated model is written in python 3, ensure you have some version of python3, although it has only been tested with python 3.7 or later. Then, install the required packages using conda or miniconda:

You'll also need to install conda or miniconda or similar.

See https://docs.anaconda.com/anaconda/install/index.html for installation instructions.

Once the program is installed on your device, set up a separate environment for the project
(do not use the base environment). This step and the following can be done in two ways:
- using the GUI or
- using the Anaconda Prompt.
For people new to coding the GUI is more intuitive.

##### GUI
1. Open the Anaconda Navigator.
2. Select the tap "Environments".
3. Click "Import" and select the "environment.yml" file from the repository and name the new
    environment. All dependencies will be installed automatically.

##### Anaconda Prompt
1. Open Anaconda Prompt.
2. Type in the following line:
```bash
conda env create -f intmodel.yml
```
The dependencies will be installed automatically and the environment will be name intmodel.

If you close out the terminal and open it later you will want to activate the environment again using

```bash
conda activate intmodel
```

For both versions: Code from this project will only run smoothly when opened in the new
environment and when the working directory is set to the path location of the repository on
your machine.

### Running on command line

results from the paper can be rerun using the following commands in the src/scenarios folder

```bash
python create_fig_1ab.py
python create_fig_2abcde.py
python create_fig_3abcd.py
python run_model_baseline.py
```

for the country-by-country no food trade model, run
```bash
python run_baseline_by_country_no_trade.py
```

### Using Jupyter (requires cloned repo):
In the notebooks/ folder run:

```bash
jupyter notebook example_optimize.ipynb
```

Then skip the colab section and execute every other cell in order.
