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
        self.failed = 0
        self.pot_pass = []

    # ============== properties ==============

    @property
    def pots(self) -> List[Pot]:
        return self.__pots

    @pots.setter
    def pots(self) -> None:
        raise Exception("unable to change pots from draw")

    # ============== static methods ==============

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

    # ============== methods of instances ==============
    def reset(self) -> None:
        for pot in self.pots:
            for team in pot.teams:
                team.opponents[pot.id][HOME] = ""
                team.opponents[pot.id][AWAY] = ""

    def resetAll(self) -> None:
        for pot in self.pots:
            pot.resetComplete()

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

    def drawComplete(self) -> bool:
        Done = True
        for pot in self.pots:
            if not Done:
                break
            Done = pot.isRight()
            if Done:
                self.pot_pass.append(pot.id)
        if not Done:
            self.resetAll()
            if self.failed > 0:
                print("failed", self.failed + 1)
                self.failed += 1
        print(self.pot_pass)
        self.pot_pass = []
        return Done

    def getData(self) -> dict:
        data = {}
        for pot in self.pots:
            pot.resume()
            pot.toDict()
            for team in pot.teams.copy():
                data[team.name] = team.opponents
                data[team.name]["resume"] = team.resumes
        return data

    def genrateJson(self) -> None:
        data = json.dumps(self.getData(), indent=4, ensure_ascii=False)
        with open(tirages_path_json, "w", encoding="utf-8") as outfile:
            outfile.write(data)
            outfile.close()
        print("done!")

    def makeDrawOnSamePots(self) -> None:
        while not self.drawHasDone():
            for i in range(0, 4):
                pot = self.pots[i]
                while not pot.isCorrect():
                    for team in pot.teams:
                        # get all clubs from differents countries that are free and not have current club as opponent in the same pot
                        opponents = list(
                            filter(
                                lambda t: t.country != team.country
                                and not t.taken(pot=pot.id, to=HOME)  # AWAY=""
                                and not t.has(opponent=team, at=HOME),
                                pot.teams.copy(),
                            )
                        )

                        if len(opponents):
                            opp = random.choice(opponents)
                            team.addOpponent(opponent=opp, to=HOME, pot=opp.pot)
                            opp.addOpponent(opponent=team, to=AWAY, pot=team.pot)
                        else:
                            pot.reset()
                            break
        print("step 1 done!")

    def makeDrawOnDifferentsPots(self, pot_active: Pot, pot_passive: Pot) -> None:
        target = HOME
        # while not pot_active.receiveOpponents(pot_passive=pot_passive):
        for _, team_active in enumerate(pot_active.teams):

            opponents = list(
                filter(
                    lambda t: t.country != team_active.country
                    and not t.taken(pot=pot_active.id, to=target)  # AWAY=""
                    and not t.has(
                        opponent=team_active,
                        at=HOME if target == AWAY else AWAY,
                    )
                    and t.validCondWith(opponent=team_active)
                    and team_active.validCondWith(opponent=t),
                    pot_passive.teams,
                )
            )

            if len(opponents):
                opponent = random.choice(opponents)
                team_active.addOpponent(
                    opponent=opponent, to=target, pot=opponent.pot
                )
                opponent.addOpponent(
                    opponent=team_active,
                    to=HOME if target == AWAY else AWAY,
                    pot=team_active.pot,
                )
                team_active.resume()
                opponent.resume()
                continue
            else:
                    break
                    # pot_active.resetAllMatchAt(target=HOME, pot_id=pot_passive.id)
                    # pot_passive.resetAllMatchAt(target=AWAY, pot_id=pot_active.id)
                    # continue
        pot_active.see.append(pot_passive.id)
        pot_passive.see.append(pot_active.id)

        # return True

    def completeDraw(self) -> None:
        while not self.drawComplete():
            for i in range(0, 4):
                pot = self.pots[i]
                pot.opponents = list(filter(lambda e: e.id != pot.id, self.pots))
            # pot 1 and pot 2
            self.makeDrawOnDifferentsPots(
                pot_active=self.pots[0], pot_passive=self.pots[1]
            )
            self.makeDrawOnDifferentsPots(
                pot_active=self.pots[1], pot_passive=self.pots[0]
            )

            # pot 3 and pot 4
            self.makeDrawOnDifferentsPots(
                pot_active=self.pots[2], pot_passive=self.pots[3]
            )
            self.makeDrawOnDifferentsPots(
                pot_active=self.pots[3], pot_passive=self.pots[2]
            )

            # pot 2 and pot 3
            self.makeDrawOnDifferentsPots(
                pot_active=self.pots[1], pot_passive=self.pots[2]
            )
            self.makeDrawOnDifferentsPots(
                pot_active=self.pots[2], pot_passive=self.pots[1]
            )

            # pot 1 and pot 3
            self.makeDrawOnDifferentsPots(
                pot_active=self.pots[0], pot_passive=self.pots[2]
            )
            self.makeDrawOnDifferentsPots(
                pot_active=self.pots[2], pot_passive=self.pots[0]
            )

            # pot 4 and pot 1
            self.makeDrawOnDifferentsPots(
                pot_active=self.pots[1], pot_passive=self.pots[0]
            )
            self.makeDrawOnDifferentsPots(
                pot_active=self.pots[0], pot_passive=self.pots[1]
            )

            # # pot 2 and pot 4
            # self.makeDrawOnDifferentsPots(
            #     pot_active=self.pots[1], pot_passive=self.pots[3]
            # )
            # self.makeDrawOnDifferentsPots(
            #     pot_active=self.pots[3], pot_passive=self.pots[1]
            # )

            print("Done!")

    def make_draw(self):
        # set opponents from each team on the same pot
        # self.makeDrawOnSamePots()
        # set opponents from each team provide from other pot
        self.completeDraw()
        # generate draw as json file
        self.genrateJson()
