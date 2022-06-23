allfed-integrated-model
==============================

An integrated economic model for resilient foods

# Run the model

### Using Colab (most users use this):
The interactive model runs off colab. It doesn't require any downloading or code, you just need to hit the right buttons as they show up. Here's a demo:

First click on the "notebooks" folder in the allfed-integrated-model directory.

![step2](https://raw.githubusercontent.com/allfed/allfed-integrated-model/main/readme_content/step2.png)

Open 'example_optimize.ipynb'

![step3](https://raw.githubusercontent.com/allfed/allfed-integrated-model/main/readme_content/step3.png)

Click 'Open in Colab'.

![step4](https://raw.githubusercontent.com/allfed/allfed-integrated-model/main/readme_content/step4.png)

Select 'Authorize with github'.

![step5](https://raw.githubusercontent.com/allfed/allfed-integrated-model/main/readme_content/step5.png)

Select 'OK'.

![step6](https://raw.githubusercontent.com/allfed/allfed-integrated-model/main/readme_content/step6.png)

For the repository, select 'allfed/allfed-integrated-model' branch 'main', then click on the item labelled under Path, 'notebooks/example_optimize.ipynb'.

Now follow the instructions in the Jupyter notebook. Run each line of the Jupyter notebook in succession to view results of the paper.

Please let me know if any of these steps go awry! (contact morgan [at] allfed [dot] info)

### From the command line (requires cloned repo):
The integrated model is written in python 3, ensure you have some version of python3, although it has only been tested with python 3.7 or later. Then, install the required packages using pip if not already installed:

```bash
pip install PuLP
pip install numpy
pip install matplotlib
pip install seaborn
pip install scipy
pip install geopandas
```

results from the paper can be rerun using the following commands in the src/ folder

```bash
python run_model.py
python run_model_no_resilient_foods.py
python run_model_before_catastrophe.py
python plot_available_food.py
```

### Using Jupyter (requires cloned repo):
In the notebooks/ folder run:

```bash
jupyter notebook example_optimize.ipynb
```

Then skip the colab section and execute every other cell in order.

# Project Tree

    ├── README.md          <- The top-level README for developers using this project.
    ├── data               <- Data from Monte Carlo runs.
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    ├── figures            <- Generated graphics and figures to be used in reporting
    ├── src                <- Source code for use in this project.
        └── __init__.py    <- Makes src a Python module

--------
