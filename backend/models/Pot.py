from typing import List
from backend.models.Team import Team
from utils import HOME, AWAY


class Pot:
    # attributes of instance
    def __init__(self, id: str, teams: List[Team]) -> None:
        self.__id = id
        self.__teams = teams
        self.pots_failed = []
        self.see=[]
        self.opponents=[]

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

    def resetAll(self, pot: int, target: str) -> None:
        """reset all opponents for each team for pot id on step 2 of draw

        Args:
            pot (int): pot id to remove opponents
        """
        for team in self.teams:
            opp = team.opponents[pot][target]
            if opp:
                opp.opponents[self.id][AWAY if target == HOME else HOME] = ""
            team.opponents[pot][target] = ""

    def resetComplete(self) -> None:
        """reset all matches for all team of pot when draw failed on step two of draw"""
        for team in self.teams:
            for id, opp in team.opponents.items():
                t = opp[HOME]
                if id != self.id:
                    if t:
                        t.opponents[self.id][AWAY] = ""
                    team.opponents[id][HOME] = ""

    def resume(self) -> None:
        """resume occurence for each team in the pot on the second step of draw"""
        for team in self.teams:
            team.resume()

    def isComplete(self, last_pot_id: int, target: str) -> bool:
        """valid if each team of current pot has received an opponent from other pot on the second step
        Returns:
            bool: True if done, False otherwise
        """
        Done = True
        for team in self.teams:
            if not team.isComplete(target=target):
                Done = False
                break

        if not Done:
            self.resetAll(pot=last_pot_id, target=target)
            self.pots_failed.append(last_pot_id)
            self.pots_failed = list(set(self.pots_failed))
        return Done

    def reset(self) -> None:
        """reset each team from current pot if draw false on step 1"""
        for team in self.teams:
            team.opponents[self.id][HOME] = ""
            team.opponents[self.id][AWAY] = ""

    def toDict(self) -> None:
        """transform each opponents from each team to dict form for json format"""
        for t in self.teams:
            for _, opp in t.opponents.items():
                if opp[HOME] and opp[AWAY]:
                    opp[HOME] = opp[HOME].toDict()
                    opp[AWAY] = opp[AWAY].toDict()

    def resetAllMatchAt(self, target: str, pot_id: int) -> None:
        for team in self.teams:
            team.opponents[pot_id][target] = ""

    def receiveOpponents(self, pot_passive) -> bool:
        # must be vefify of in [1,2,3,4] later
        if not isinstance(pot_passive, Pot):
            raise Exception("Invalid pot exception!")
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
