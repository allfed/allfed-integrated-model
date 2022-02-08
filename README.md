allfed-integrated-model
==============================

An integrated economic model for resilient foods

# Installation
Dependencies are managed using Poetry - install it if you don't have it: https://python-poetry.org/
To install:
```bash
poetry install
```
Note: windows users will probably have more success installing each dependency u
sing conda, rather than using poetry for dependency management.


# Run the model

### Using Colab (most users use this):
The interactive model runs off colab. It doesn't require any downloading or code, you just need to hit the right buttons as they show up. Here's a demo:

First click on the "notebooks" folder, highlighted in the image below:

![step1](https://raw.githubusercontent.com/allfed/allfed-integrated-model/main/readme_content/step1.png)

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

![step7](https://raw.githubusercontent.com/allfed/allfed-integrated-model/main/readme_content/step7.png)

Now follow the instructions in the Jupyter notebook. Run each line of the Jupyter notebook in succession to view results of the paper.

Please let me know if any of these steps go awry! (contact morgan [at] allfed [dot] info)

### From the command line (requires cloned repo):
```bash
poetry shell
python src/cheri.py
```

### Using Jupyter (requires cloned repo):
```bash
poetry run jupyter lab
```
Then navigate to the `notebooks` folder, open `1.0-example-run-cheri.ipynb`, and
execute each cell in order, ignoring the first cell

# Project Tree

    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── pyproject.toml   <- The dependencies file for reproducing the modelling environment using poetry
    ├── poetry.lock   <- Fixed versions for each dependency
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
        └── __init__.py    <- Makes src a Python module

--------
