# Ce module contient les instances de vos classes back et front end.
# from backend.Draw import Draw
from frontend.pdf import PDF
from utils import load_json

# load samples success results from Draw
json_tirages = load_json(path="data/tirage.json")

pdf = PDF(tirages=json_tirages)

pdf.generate()
pdf.export()


# from utils import teams_path_json, load_json

# # load teams from json file
# json_teams = load_json(teams_path_json)

# # order teams by pots
# dict_pots = Draw.sort_teams_by_pots(json_teams)

# # get list of pot
# list_pots = Draw.get_list_of_pots(dict_pots)

# draw = Draw(pots=list_pots)

# draw.make_draw()
# draw
