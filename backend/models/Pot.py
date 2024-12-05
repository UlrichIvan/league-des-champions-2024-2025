from typing import List
from backend.models.Team import Team
from utils import HOME, AWAY


class Pot:
    # instance attribute
    def __init__(self, id: str, teams: List[Team]) -> None:
        self.id = id
        self.teams = teams

    def isCorrect(self) -> bool:
        Done = True
        for team in self.teams:
            home = team.opponents[self.id][HOME]
            away = team.opponents[self.id][AWAY]
            if home == "" or away == "":
                Done = False
                print("failed pot : ", self.id, team.name)
                break
        return Done

    def reset(self) -> None:
        for team in self.teams:
            team.opponents[self.id][HOME] = ""
            team.opponents[self.id][AWAY] = ""

    def toJSON(self) -> None:
        for t in self.teams:
            for _, opp in t.opponents.items():
                if opp[HOME] and opp[AWAY]:
                    opp[HOME] = opp[HOME].toJSON()
                    opp[AWAY] = opp[AWAY].toJSON()
