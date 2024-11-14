from typing import Tuple
from typing import Dict, List
from utils import HOME, AWAY, MatchKey


class Team:
    def __init__(
        self, name: str, country: str, championship: str, pot: str, logo: str
    ) -> None:
        self.__name = name
        self.__country = country
        self.__championship = championship
        self.__pot = pot
        self.__logo = logo
        self.__tracking = []
        self.__matches = {
            "pot_1": {},
            "pot_2": {},
            "pot_3": {},
            "pot_4": {},
        }
        self.__matched = []

    # matched
    @property
    def matched(self) -> list:
        return self.__matched

    @matched.setter
    def matched(self, value: list) -> None:
        self.__matched = value

    # matches
    @property
    def matches(self) -> Dict[MatchKey, dict]:
        return self.__matches

    @matches.setter
    def matches(self, value: Dict[MatchKey, dict]):
        self.__matches = value

    # tracking
    @property
    def tracking(self) -> list:
        return self.__tracking

    @tracking.setter
    def tracking(self, value: list) -> None:
        self.__tracking = value

    # name
    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self) -> None:
        raise Exception("unable to change team name!")

    # country
    @property
    def country(self) -> str:
        return self.__country

    @country.setter
    def country(self) -> None:
        raise Exception("unable to change team country!")

    # championship
    @property
    def championship(self) -> str:
        return self.__championship

    @championship.setter
    def championship(self) -> None:
        raise Exception("unable to change team championship!")

    # pot
    @property
    def pot(self) -> str:
        return self.__pot

    @pot.setter
    def pot(self) -> None:
        raise Exception("unable to change team pot!")

    # logo
    @property
    def logo(self) -> str:
        return self.__logo

    @logo.setter
    def logo(self) -> None:
        raise Exception("unable to change team logo!")

    def __str__(self) -> str:
        return f"name:{self.__name};country:{self.country};championship:{self.__championship};pot:{self.__pot};logo:{self.__logo}"

    # methods

    def removeOpponentInTracking(self, opp) -> None:
        if not isinstance(opp, Team):
            raise Exception("only team object can be opponent!")

        for i, team in enumerate(self.tracking):
            if team.name == opp.name:
                self.tracking.pop(i)
                break

    def dropMatch(self, opp) -> None:
        if not isinstance(opp, Team):
            raise Exception("only team object can be opponent!")

        for _, m in self.matches.items():
            if HOME in m and opp.name == m[HOME]["name"]:
                m.pop(HOME, None)
                break
            elif AWAY in m and opp.name == m[AWAY]["name"]:
                m.pop(AWAY, None)
                break

    def reset(self) -> None:

        for opp_team in self.matched:
            # remove opponent club in tracking and abort macthes with current opponent
            self.dropMatch(opp=opp_team)
            # remove opponent club in tracking and abort macthes with current team
            opp_team.dropMatch(opp=self)
            opp_team.matched = []

        self.matched = []

    def save(self) -> None:

        # updated tracking from opponent
        for opp_team in self.matched:
            opp_team.tracking.append(self)
            opp_team.matched = []

        # update tracking
        self.tracking = self.tracking + self.matched

    # methods
    def setMatch(self, t, where: str):

        if not isinstance(t, Team):
            raise Exception("only team object can be opponent!")

        pot_name = f"pot_{t.pot}"

        self.matches[pot_name][where] = {
            "name": t.name,
            "country": t.country,
            "championship": t.championship,
            "pot": t.pot,
            "logo": t.logo,
        }

        self.matched.append(t)

    def opp_in_tracking(self, opp) -> bool:

        if not isinstance(opp, Team):
            raise Exception("only team can be opponent!")

        found = False
        for team in self.tracking:
            if opp.name == team.name:
                found = True
                break
        return found

    def get_opp_country(self, t) -> str | None:
        found = None
        for team in self.tracking:
            if team.country == t.country:
                found = team.country
                break
        return found

    def get_country_from_same_club(self) -> str | None:

        country = None

        if len(self.tracking) == 0:
            return None

        for team in self.tracking:

            if country != None:
                break

            for t in self.tracking:
                if t.name != team.name and team.country == t.country:
                    country = team.country
                    break
                else:
                    continue

        return country

    def need_opponent_from_pot(self, pot_id: int) -> Tuple[bool, bool]:

        pot_name = f"pot_{pot_id}"

        keys = self.matches[pot_name].keys()

        # opponents is complete
        if len(self.tracking) == 8:
            return False, False

        if len(keys) == 0:
            return True, True
        elif (HOME in keys) and (AWAY in keys):
            return False, False
        elif (HOME in keys) and (AWAY not in keys):
            return False, True
        elif (HOME not in keys) and (AWAY in keys):
            return True, False
