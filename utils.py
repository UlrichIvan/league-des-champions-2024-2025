import json
from enum import Enum


teams_path_json = "data/teams.json"

tirages_path_json = "data/tirages.json"


def load_json(path: str) -> any:
    with open(path, "r") as file:
        teams = json.load(file)
    return teams


HOME = "home"
AWAY = "away"

class MatchKey(Enum):
    pot_1 = "pot_1"
    pot_2 = "pot_2"
    pot_3 = "pot_3"
    pot_4 = "pot_4"
