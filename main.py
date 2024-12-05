# Ce module contient les instances de vos classes back et front end.
from backend.Draw import Draw

# from frontend.pdf import PDF
# from utils import load_json, teams_path_json

# load samples success results from Draw
# json_tirages = load_json(path="data/tirage.json")

# json_teams = load_json(path=teams_path_json)

# pdf = PDF(tirages=json_tirages,json_teams=json_teams)

# pdf.generate()
# pdf.export()

from utils import teams_path_json, load_json

# load teams from json file

json_teams = load_json(path=teams_path_json)

# order teams by pots
dict_pots = Draw.sort_teams_by_pots(json_teams.copy())

# get list of pot
list_pots = Draw.get_list_of_pots(dict_pots.copy())

draw = Draw(pots=list_pots.copy())

draw.make_draw()
