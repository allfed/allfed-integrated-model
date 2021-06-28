allfed-integrated-model
==============================

An integrated economic model for resilient foods

# Installation
Dependencies are managed using Poetry - install it if you don't have it: https://python-poetry.org/
To install:
```bash
poetry install
```
# Run the model
From the command line:
```bash
poetry shell
python src/cheri.py
```

Using Jupyter (access via command line):
```bash
poetry run jupyter lab
```
Then navigate to the `notebooks` folder, open `1.0-example-run-cheri.ipynb`, and
execute each cell in order.


# Project Organization

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
    │   └── __init__.py    <- Makes src a Python module
    │   
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io


--------
