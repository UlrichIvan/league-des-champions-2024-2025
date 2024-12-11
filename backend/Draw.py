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
        self.__failed = 0
        self.__pot_pass = []

    # ============== properties of instances ==============

    @property
    def pots(self) -> List[Pot]:
        return self.__pots

    @pots.setter
    def pots(self) -> None:
        raise Exception("unable to change pots from draw")

    @property
    def failed(self) -> int:
        return self.__failed

    @failed.setter
    def failed(self, value: int) -> None:
        self.__failed = value

    @property
    def pot_pass(self) -> list:
        return self.__pot_pass

    @pot_pass.setter
    def pot_pass(self, value: list) -> None:
        self.__pot_pass = value

    # ============== static methods ==============

    @staticmethod
    def get_list_of_pots(pots: Dict[int, List[Team]]) -> List[Pot]:
        """return list of class Pot

        Args:
            pots (Dict[int, List[Team]]): dict of pots

        Returns:
            List[Pot]: lit of pots
        """
        list_pots = []

        for id, teams in pots.items():
            list_pots.append(Pot(id=id, teams=teams))
        return list_pots

    @staticmethod
    def sort_teams_by_pots(teams: list) -> Dict[int, List[Team]]:
        """sort teams by pots

        Args:
            teams (list): list of teams loader as json file

        Returns:
            Dict[int, List[Team]]: dict of pots with teams
        """

        pots = {1: [], 2: [], 3: [], 4: []}

        for team in teams:
            pots[team["chapeau"]].append(
                Team(
                    name=team["nom"],
                    country=team["pays"],
                    pot=team["chapeau"],
                    championship=team["championnat"],
                    logo=team["logo"],
                )
            )
        return pots

    # ============== methods of instances ==============
    def reset(self) -> None:
        """reset all pots when draw lost on the first step"""
        for pot in self.pots:
            for team in pot.teams:
                team.opponents[pot.id][HOME] = ""
                team.opponents[pot.id][AWAY] = ""

    def reset_all(self) -> None:
        """reset all pots when draw lost on the second step"""
        for pot in self.pots:
            pot.resetComplete(to=HOME)
            pot.resetComplete(to=AWAY)

    def draw_init(self) -> bool:
        """verify if draw is valid for first step(draw for into each pot properly)

        Returns:
            bool: True if draw for first step was ok. False otherwise
        """
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

    def draw_complete(self) -> bool:
        """verify if draw for the second step was done successfully

        Returns:
            bool: True if draw is complete. False otherwise
        """
        Done = True
        for pot in self.pots:
            if not Done:
                break
            Done = pot.isRight()
            if Done:
                self.pot_pass.append(pot.id)
        if not Done:
            self.reset_all()
            if self.failed > 0:
                print("failed", self.failed + 1)
                self.failed += 1
        print("pots success", self.pot_pass)
        self.pot_pass = []
        return Done

    def get_data(self) -> dict:
        """return dict after draw validate

        Returns:
            dict: dict of draw complete
        """
        data = {}
        for pot in self.pots:
            pot.resume()
            pot.toDict()
            for team in pot.teams.copy():
                data[team.name] = team.opponents
                data[team.name]["resume"] = team.resumes
        return data

    def generate_json(self) -> None:
        """save json file for draw when draw is finish and ok"""
        data = json.dumps(self.get_data(), indent=4, ensure_ascii=False)
        with open(tirages_path_json, "w", encoding="utf-8") as outfile:
            outfile.write(data)
            outfile.close()
        print("done!")

    def make_draw_on_same_pots(self) -> None:
        """make draw for between team on same pot"""
        while not self.draw_init():
            for i in range(0, 4):
                pot = self.pots[i]
                while not pot.isCorrect():
                    for team in pot.teams:
                        # get all clubs from differents countries that are free and not have current club as opponent in the same pot
                        opponents = list(
                            filter(
                                lambda t: t.country != team.country
                                and t.available(pot_id=pot.id, to=AWAY)  # AWAY=""
                                and not t.know(opponent=team)
                                and t.validCondWith(opponent=team)
                                and team.validCondWith(opponent=t),
                                pot.teams.copy(),
                            )
                        )

                        if len(opponents):
                            opp = random.choice(opponents)
                            team.addOpponent(opponent=opp, to=HOME, pot_id=opp.pot)
                            # opp.addOpponent(opponent=team, to=AWAY, pot=team.pot)
                        else:
                            pot.reset()
                            break
        print("step 1 done!")

    def make_draw_on_differents_pots(self, pot_active: Pot, pot_passive: Pot) -> None:
        """complete opponents of team into active pot with team passive pot for HOME location

        Args:
            pot_active (Pot): pot which make an action
            pot_passive (Pot): pot that receive an action provide by active pot
        """
        while not pot_active.receiveOpponents(pot_passive=pot_passive):
            for _, team_active in enumerate(pot_active.teams):

                opponents = list(
                    filter(
                        lambda t: t.country != team_active.country
                        and t.available(pot_id=pot_active.id, to=AWAY)  # AWAY=""
                        and not t.know(opponent=team_active)
                        and t.validCondWith(opponent=team_active)
                        and team_active.validCondWith(opponent=t),
                        pot_passive.teams,
                    )
                )

                if len(opponents):
                    opponent = random.choice(opponents)
                    team_active.addOpponent(
                        opponent=opponent, to=HOME, pot_id=opponent.pot
                    )
                    team_active.resume()
                    opponent.resume()
                    continue
                else:
                    pot_active.resetAllMatchAt(target=HOME, pot_id=pot_passive.id)
                    pot_passive.resetAllMatchAt(target=AWAY, pot_id=pot_active.id)
                    break

    def complete_draw(self) -> None:
        """make draw between diffents pots to complete all matches"""
        while not self.draw_complete():
            for i in range(0, 4):
                pot = self.pots[i]
                pot.opponents = list(filter(lambda e: e.id != pot.id, self.pots))
                for opponent in pot.opponents:
                    self.make_draw_on_differents_pots(
                        pot_active=pot, pot_passive=opponent
                    )
                    self.make_draw_on_differents_pots(
                        pot_active=opponent, pot_passive=pot
                    )

        print("step 2 done!")

    def make_draw(self):
        """make draw and create json file"""
        # set opponents from each team on the same pot
        self.make_draw_on_same_pots()
        # set opponents from each team provide from other pot
        self.complete_draw()
        # generate draw as json file
        self.generate_json()
