from typing import List, Dict
from backend.models.Pot import Pot
import random
from utils import HOME, AWAY, tirages_path_json
from backend.models.Team import Team
from backend.models.Pot import Pot
import json


class Draw:
    def __init__(self, pots: List[Pot]) -> None:
        self.__pots = pots
        self.__results = []
        self.failed = 0

    @property
    def tirages(self) -> dict:
        return self.__tirages

    @tirages.setter
    def tirages(self, value: dict) -> None:
        self.__tirages = value

    @property
    def results(self) -> list:
        return self.__results

    @results.setter
    def results(self) -> None:
        raise Exception("unable to change results from draw")

    @property
    def pots(self) -> List[Pot]:
        return self.__pots

    @pots.setter
    def pots(self) -> None:
        raise Exception("unable to change pots from draw")

    @staticmethod
    def get_list_of_pots(pots: Dict[int, List[Team]]) -> List[Pot]:
        list_pots = []

        for id, teams in pots.items():
            list_pots.append(Pot(id=id, teams=teams))
        return list_pots

    @staticmethod
    def sort_teams_by_pots(teams: list) -> Dict[int, List[Team]]:

        pots = {1: [], 2: [], 3: [], 4: []}

        for team in teams:
            team = Team(
                name=team["nom"],
                country=team["pays"],
                pot=team["chapeau"],
                championship=team["championnat"],
                logo=team["logo"],
            )
            pots[team.pot].append(team)
        return pots

    def reset(self) -> None:
        for pot in self.pots:
            for team in pot.teams:
                team.opponents[pot.id][HOME] = ""
                team.opponents[pot.id][AWAY] = ""

    def drawHasDone(self) -> bool:
        Done = True
        for pot in self.pots:
            if not Done:
                break
            Done = pot.isCorrect()
        if not Done:
            if self.failed > 0:
                print("failed", self.failed + 1)
                self.failed += 1
                self.reset()

        return Done

    def getData(self) -> dict:
        data = {}
        for pot in self.pots:
            pot.toJSON()
            for team in pot.teams.copy():
                data[team.name] = team.opponents
        return data

    def genrateJson(self) -> None:
        data = json.dumps(self.getData(), indent=4, ensure_ascii=False)
        with open(tirages_path_json, "w", encoding="utf-8") as outfile:
            outfile.write(data)
            outfile.close()
        print("done!")

    def initDraw(self) -> None:
        while not self.drawHasDone():
            for i in range(0, 4):
                pot = self.pots[i]
                while not pot.isCorrect():
                    for team in pot.teams:
                        # get all clubs from differents countries that are free and not have current club as opponent in the same pot
                        opponents = list(
                            filter(
                                lambda t: t.country != team.country
                                and not t.taken(pot=pot.id)  # AWAY=""
                                and not t.has(opponent=team, at=HOME),
                                pot.teams.copy(),
                            )
                        )

                        if len(opponents):
                            opp = opponents[random.randint(0, len(opponents) - 1)]
                            team.addOpponent(opponent=opp, to=HOME, pot=opp.pot)
                            opp.addOpponent(opponent=team, to=AWAY, pot=team.pot)
                        else:
                            pot.reset()
                            break

        print("firts step done!")

        print("next step begin!!!")

        for i in range(0, 4):
            pot = self.pots[i]
            # current_pot=None
            pots = list(filter(lambda e: e.id != pot.id, self.pots))
            while not pot.isComplete():
                for team in pot.teams:
                    for p in pots:
                        # get all clubs from differents countries that are free and not have current club as opponent in the same pot
                        opponents = list(
                            filter(
                                lambda t: t.country != team.country
                                and not t.taken(pot=pot.id)  # AWAY=""
                                and not t.has(opponent=team, at=HOME)
                                and t.validCondWith(opponent=team)
                                and team.validCondWith(opponent=t),
                                p.teams.copy(),
                            )
                        )

                        if len(opponents):
                            opp = opponents[random.randint(0, len(opponents) - 1)]
                            team.addOpponent(opponent=opp, to=HOME, pot=opp.pot)
                            opp.addOpponent(opponent=team, to=AWAY, pot=team.pot)
                            continue
                        else:
                            pot.init()
                            break

        print("next done begin!!!")

    def make_draw(self):
        self.initDraw()
        self.genrateJson()
