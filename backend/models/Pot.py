from typing import List
from backend.models.Team import Team
from utils import HOME, AWAY


class Pot:
    # attributes of instance
    def __init__(self, id: str, teams: List[Team]) -> None:
        self.__id = id
        self.__teams = teams
        self.pots_failed = []
        self.see = []
        self.opponents = []

    # ============== properties ==============

    @property
    def teams(self) -> list:
        return self.__teams

    @teams.setter
    def teams(self, value: list) -> None:
        self.__teams = value

    @property
    def id(self) -> int:
        return self.__id

    @id.setter
    def id(self, value: int) -> None:
        self.__id = value

    # ============== methods of instances ==============

    def isCorrect(self) -> bool:
        """
        verify if each team has a valid opponent during the first step of draw
        """
        Done = True
        for team in self.teams:
            home = team.opponents[self.id][HOME]
            away = team.opponents[self.id][AWAY]
            if home == "" or away == "":
                Done = False
                print("failed pot : ", self.id, team.name)
                break
        return Done

    def isRight(self) -> bool:
        """
        verify if each team has a valid opponent during the second step of draw
        """
        Done = True
        for team in self.teams:
            for id, opp in team.opponents.items():
                if not Done:
                    break
                if id != self.id and (opp[HOME] == "" or opp[AWAY] == ""):
                    Done = False
                    break
        return Done

    def resetComplete(self, to: str) -> None:
        """reset all matches for all team of pot when draw failed on step two of draw

        Args:
            to (str): match location to reset match ("home" or "away")

        Raises:
            Exception: if match location is not valid
        """
        if to not in [HOME, AWAY]:
            raise Exception("invalid match location set!")
        for team in self.teams:
            for id, opp in team.opponents.items():
                if id != self.id:
                    t = opp[to]
                    if t:
                        t.opponents[self.id][AWAY if to == HOME else HOME] = ""
                    team.opponents[id][to] = ""

    def resume(self) -> None:
        """resume occurences for each team in the pot"""
        for team in self.teams:
            team.resume()

    def reset(self) -> None:
        """reset each team from current pot if draw false on step 1"""
        for team in self.teams:
            team.opponents[self.id][HOME] = ""
            team.opponents[self.id][AWAY] = ""

    def toDict(self) -> None:
        """transform each opponents from each team to dict formmat for json format"""
        for t in self.teams:
            for _, opp in t.opponents.items():
                if opp[HOME] and opp[AWAY]:
                    opp[HOME] = opp[HOME].toDict()
                    opp[AWAY] = opp[AWAY].toDict()

    def resetAllMatchAt(self, target: str, pot_id: int) -> None:
        """_reset all matches for current pot at target(HOME OR AWAY)
        Args:
            target (str): "home" or "where"
            pot_id (int): number of pot

        Raises:
            Exception: if target or pot_id is not valid
        """
        if target not in [HOME, AWAY] or pot_id not in range(1, 5):
            raise Exception("Invalid target or pot number")
        for team in self.teams:
            team.opponents[pot_id][target] = ""

    def receiveOpponents(self, pot_passive) -> bool:
        """verify that all team of current pot had been received oppponent
        for paasive pot

        Args:
            pot_passive (Pot): pot target for current pot

        Raises:
            Exception: if pot_passive is not instance of class Pot

        Returns:
            bool: True if all team of current pot recived opponents form passive pot
        """
        if not isinstance(pot_passive, Pot):
            raise Exception("invalid pot passive")
        Done = True
        for team in self.teams:
            for pot_id, opp in team.opponents.items():
                if not Done:
                    break
                if pot_id == pot_passive.id and opp[HOME] == "":
                    Done = False
                    break
        if not Done:
            self.resetAllMatchAt(target=HOME, pot_id=pot_passive.id)
            pot_passive.resetAllMatchAt(target=AWAY, pot_id=self.id)
        return Done
