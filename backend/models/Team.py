from typing import Tuple
from typing import Dict, List
from utils import HOME, AWAY


class Team:
    def __init__(
        self, name: str, country: str, championship: str, pot: int, logo: str
    ) -> None:
        self.__name = name
        self.__country = country
        self.__championship = championship
        self.__pot = pot
        self.__logo = logo
        self.__opponents = {
            1: {"home": "", "away": ""},
            2: {"home": "", "away": ""},
            3: {"home": "", "away": ""},
            4: {"home": "", "away": ""},
        }

        self.resumes = {}

    # ========== properties =================

    @property
    def opponents(self) -> dict:
        return self.__opponents

    @opponents.setter
    def opponents(self, value: dict) -> None:
        self.__opponents = value

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self) -> None:
        raise Exception("unable to change team name!")

    @property
    def country(self) -> str:
        return self.__country

    @country.setter
    def country(self) -> None:
        raise Exception("unable to change team country!")

    @property
    def championship(self) -> str:
        return self.__championship

    @championship.setter
    def championship(self) -> None:
        raise Exception("unable to change team championship!")

    @property
    def pot(self) -> int:
        return self.__pot

    @pot.setter
    def pot(self) -> None:
        raise Exception("unable to change team pot!")

    @property
    def logo(self) -> str:
        return self.__logo

    @logo.setter
    def logo(self) -> None:
        raise Exception("unable to change team logo!")

    def __str__(self) -> str:
        return f"name:{self.__name};country:{self.country};championship:{self.__championship};pot:{self.__pot};logo:{self.__logo}"

    # ============= methods of instances ================

    def toDict(self) -> dict:
        """tranform current Team instance to dict for json export

        Returns:
            dict: current Team instance as dict
        """
        return {
            "name": self.name,
            "country": self.country,
            "championship": self.championship,
            "pot": self.pot,
            "logo": self.logo,
        }

    def addOpponent(self, opponent, to: str, pot_id: int) -> None:
        """add opponent for current team

        Args:
            opponent (Team): opponent for current team
            to (str): match location
            pot_id (int): pot id

        Raises:
            Exception: if invalid opponent or match location or pot id
        """
        if (
            not isinstance(opponent, Team)
            or to not in [HOME, AWAY]
            or pot_id not in range(1, 5)
        ):
            raise Exception("Invalid opponent for current team!")
        # add opponent found
        self.opponents[pot_id][to] = opponent
        # add team as opponent
        opponent.opponents[self.pot][HOME if to == AWAY else AWAY] = self

    def available(self, pot_id: int, to: str) -> bool:
        """verify if current team is avalaible for location

        Args:
            pot_id (int): pot id
            to (str): match location

        Raises:
            Exception: if Invalid pot id or match location

        Returns:
            bool: True is team is availbe False otherwise
        """
        if pot_id not in range(1, 5) or to not in [HOME, AWAY]:
            raise Exception("Invalid pot id or match location!")
        return not isinstance(self.opponents[pot_id][to], Team)

    def getOpponents(self) -> list:
        """return opponents for current team

        Returns:
            list: list of opponent
        """
        data = list(self.opponents.values())
        opponents = []
        for el in data:
            if el[HOME]:
                opponents.append(el[HOME])
            if el[AWAY]:
                opponents.append(el[AWAY])
        return opponents

    def resume(self) -> None:
        """set occurences of opponents for current team"""
        opponents = self.getOpponents() if self.getOpponents() else []
        occurences = self._occurencesByContry(opponents=opponents.copy())
        self.resumes = occurences

    def validCondWith(self, opponent) -> bool:
        """valid if second condiction is ok for current team with  current opponent

        Args:
            opponent (Team): opponent for current team

        Raises:
            Exception: if opponent is not instance of class Team

        Returns:
            bool: True if condition is ok False otherwise
        """
        if not isinstance(opponent, Team):
            raise Exception("Invalid opponent!")
        Done = True
        opponents = self.getOpponents() if self.getOpponents() else []

        if len(opponents) == 8:
            return False

        if len(opponents) == 0:
            return True

        data = opponents.copy()

        data.append(opponent)

        occurences = self._occurencesByContry(opponents=data)

        for _, appear in occurences.items():
            if appear > 2:
                Done = False
                break

        return Done

    def know(self, opponent) -> bool:
        """verify if current team had already meet current opponent  

        Args:
            opponent (Team): current opponent

        Raises:
            Exception: if current opponent is not instance of class Team

        Returns:
            bool: True if current had alreay meet current opponent.
            False otherwise
        """
        if not isinstance(opponent, Team):
            raise Exception("invalid opponent!")
        opp = list(filter(lambda e: (e.name == opponent.name), self.getOpponents()))
        if len(opp):
            return True
        else:
            return False

    def _occurencesByContry(self, opponents: list) -> dict:
        """return occurences of countries for opponents of current team

        Args:
            countries (list): list of oppoent

        Returns:
            dict: occurences by counties for opponents
        """
        count = {}
        for team in opponents:
            if team.country in list(count.keys()):
                count[team.country] += 1
            else:
                count[team.country] = 1
        return count
