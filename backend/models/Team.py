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
        return {
            "name": self.name,
            "country": self.country,
            "championship": self.championship,
            "pot": self.pot,
            "logo": self.logo,
        }

    def addOpponent(self, opponent, to: str, pot_id: int) -> None:
        if not isinstance(opponent, Team) or to not in [HOME, AWAY]:
            raise Exception("Invalid opponent!")
        # add opponent found
        self.opponents[pot_id][to] = opponent
        # add team as opponent
        opponent.opponents[self.pot][HOME if to == AWAY else AWAY] = self

    def available(self, pot: int, to: str) -> bool:
        return not isinstance(self.opponents[pot][to], Team)

    def getOpponents(self) -> list:
        data = list(self.opponents.values())
        opponents = []
        for el in data:
            if el[HOME]:
                opponents.append(el[HOME])
            if el[AWAY]:
                opponents.append(el[AWAY])
        return opponents

    def resume(self) -> None:
        opponents = self.getOpponents() if self.getOpponents() else []
        occurences = self._occurencesByContry(countries=opponents.copy())
        self.resumes = occurences

    def resetAllMatches(self, target: str) -> None:
        for pot_id, opp in self.opponents.items():
            t = opp[target]
            if t:
                t.opponents[pot_id][AWAY if target == HOME else HOME] = ""
            opp[target] = ""

    def reset(self) -> None:
        for pot_id, opp in self.opponents.items():
            if pot_id != self.pot and opp[HOME]:
                t = opp[HOME]
                if t:
                    t.opponents[self.pot][AWAY] = ""
                opp[HOME] = ""

    def isComplete(self, target: str) -> bool:
        Done = True
        for pot_id, opp in self.opponents.items():
            if not Done:
                break
            if pot_id != self.pot and opp[target] == "":
                Done = False
                break
        return Done

    def validCondWith(self, opponent) -> bool:
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

        occurences = self._occurencesByContry(countries=data)

        for _, appear in occurences.items():
            if appear > 2:
                Done = False
                break

        return Done

    def know(self, opponent) -> bool:
        if not isinstance(opponent, Team):
            raise Exception("invalid opponent!")
        opp = list(filter(lambda e: (e.name == opponent.name), self.getOpponents()))
        if len(opp):
            return True
        else:
            return False

    def _occurencesByContry(self, countries: list) -> dict:
        count = {}
        for team in countries:
            if team.country in list(count.keys()):
                count[team.country] += 1
            else:
                count[team.country] = 1
        return count
