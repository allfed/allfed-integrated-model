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

Now we're in the actual code! If you scroll down, you can see where all the constants are set. But first we need to run the Colab environment. Following along with the instructions,

![step8](https://raw.githubusercontent.com/allfed/allfed-integrated-model/main/readme_content/step8.png)


"Run Anyway"

![step9](https://raw.githubusercontent.com/allfed/allfed-integrated-model/main/readme_content/step9.png)


Hit the black arrow on the left, and press 'enter' inside each entry box as the instructions say.
You will get a nice ascii picture.

Moving on, run the lines up to and including the 'cat' command.

![step10](https://raw.githubusercontent.com/allfed/allfed-integrated-model/main/readme_content/step10.png)

Select all that text the cat command generateds, and copy it.

![step11](https://raw.githubusercontent.com/allfed/allfed-integrated-model/main/readme_content/step11.png)

Navigate to the URL mentioned, hit 'New SSH Key'. Name it something and paste the key in.

![step12](https://raw.githubusercontent.com/allfed/allfed-integrated-model/main/readme_content/step12.png)

Hit 'Add SSH key'. You might have to put your github password in again.

Finally, return to the code to check that it worked.

![step13](https://raw.githubusercontent.com/allfed/allfed-integrated-model/main/readme_content/step13.png)

It should look like message above.
Run the remaining blocks one at a time, be sure they've completed before running the next one.

![step14](https://raw.githubusercontent.com/allfed/allfed-integrated-model/main/readme_content/step14.png)

... and continue to run the blocks, if everything has gone well, you can run each block of the code!

![step15](https://raw.githubusercontent.com/allfed/allfed-integrated-model/main/readme_content/step15.png)

Please let me know if any of these steps go awry! (morgan@allfed.info)

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
