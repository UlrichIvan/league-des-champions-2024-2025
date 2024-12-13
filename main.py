# Ce module contient les instances de vos classes back et front end.
from backend.Draw import Draw
from frontend.pdf import PDF
from utils import load_json, teams_path_json

# 1.prepare and create instance of draw class

json_teams = load_json(path=teams_path_json)

# order teams by pots
dict_pots = Draw.sort_teams_by_pots(json_teams.copy())

# get list of pot
list_pots = Draw.get_list_of_pots(dict_pots.copy())

draw = Draw(pots=list_pots.copy())

# 2. make draw,generate and export draw as pdf file

pdf = PDF(draw=draw, json_teams=json_teams)

pdf.generate()

pdf.export()
