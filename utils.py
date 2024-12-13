import json
import os

teams_path_json = "data/teams.json"

tirages_path_json = "data/tirage.json"

draw_pdf_path="data/tirage.pdf"


def path(name: str) -> str:
    """return the absolute path of file into data folder

    Args:
        name (str): name of file into data folder

    Raises:
        Exception: if file not exists inf data folder

    Returns:
        str: absolute path of file if exists in data folder
    """
    path = os.path.dirname(__file__) + f"/data/{name}"

    if os.path.isfile(path=path):
        return os.path.abspath(path)
    else:
        raise Exception("file not exists!")


def load_json(path: str) -> any:
    """load json file

    Args:
        path (str): path to json file

    Returns:
        any: result for json file loaded
    """
    with open(path, "r") as file:
        teams = json.load(file)
    return teams


# location of match during a draw
HOME = "home"
AWAY = "away"
