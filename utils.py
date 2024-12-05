import json
from enum import Enum
import os

teams_path_json = "data/teams.json"

tirages_path_json = "data/tirages.json"


def path(name: str) -> str:

    path = os.path.dirname(__file__) + f"/{name}"

    if os.path.isfile(path=path):
        return os.path.abspath(path)
    else:
        raise Exception("file not exists!")


def load_json(path: str) -> any:
    with open(path, "r") as file:
        teams = json.load(file)
    return teams


HOME = "home"
AWAY = "away"



