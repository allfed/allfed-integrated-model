import subprocess
import tempfile
from pathlib import Path
from random import choice

import git
import yaml

from src.utilities.import_utilities import ImportUtilities


def test_expanded_area_is_better():
    repo_root = git.Repo(".", search_parent_directories=True).working_dir
    cmd = Path(repo_root) / "run_scenarios_from_yaml.sh"
    with open(Path(repo_root) / "scenarios" / "USA_expanded.yaml", "r") as f:
        config = yaml.safe_load(f)
    iu = ImportUtilities()
    country = choice(iu.country_codes)
    config["settings"]["countries"] = country
    pct_people_fed = {}
    for expanded_area_scenario in ["none", "no_trade", "export_pool"]:
        for simulation in config["simulations"]:
            config["simulations"][simulation]["expanded_area"] = expanded_area_scenario
        with tempfile.NamedTemporaryFile(
            mode="w+t", delete_on_close=False, dir=Path(repo_root) / "scenarios"
        ) as tempf:
            yaml.dump(config, tempf)
            result = (
                subprocess.run(
                    [cmd, "False", "False", "False", tempf.name],
                    stdout=subprocess.PIPE,
                )
                .stdout.decode("utf-8")
                .splitlines()
            )
        result = next(filter(lambda line: "iso3" in line, result))
        result = float(result[-result[::-1].find(":") :].strip().replace("%", ""))
        pct_people_fed[expanded_area_scenario] = result
    assert (
        pct_people_fed["no_trade"] >= pct_people_fed["none"]
    ), f"expanded area result worse than without for {country}"
    assert (
        pct_people_fed["export_pool"] >= pct_people_fed["no_trade"]
    ), f"expanded area export pool worse than no trade for {country}"
