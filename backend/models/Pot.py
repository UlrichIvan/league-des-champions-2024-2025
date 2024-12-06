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

    def resetAll(self, pot: int) -> None:
        for team in self.teams:
            opp = team.opponents[pot][HOME]
            if opp:
                opp.opponents[self.id][AWAY] = ""
            team.opponents[pot][HOME] = ""

    def init(self) -> bool:
        for team in self.teams:
            for id, opp in team.opponents.items():
                if id != self.id:
                    t = opp[HOME]
                    if t:
                        t.opponents[self.id][AWAY] = ""
                    opp[HOME] = ""

    def isComplete(self) -> bool:
        Done = True
        for team in self.teams:
            for id, opp in team.opponents.items():
                if id != self.id and opp[HOME] == "":
                    Done = False
                    print("failed", team.name)
                    break

        if not Done:
            self.init()
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
