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
        raise Exception("un able to change team name!")

    # country
    @property
    def country(self) -> str:
        return self.__country

    @country.setter
    def country(self) -> None:
        raise Exception("un able to change team country!")

    # championship
    @property
    def championship(self) -> str:
        return self.__championship

    @championship.setter
    def championship(self) -> None:
        raise Exception("un able to change team championship!")

    # pot
    @property
    def pot(self) -> str:
        return self.__pot

    @pot.setter
    def pot(self) -> None:
        raise Exception("un able to change team pot!")

    # logo
    @property
    def logo(self) -> str:
        return self.__logo

    @logo.setter
    def logo(self) -> None:
        raise Exception("un able to change team logo!")

    # method

    def __str__(self) -> str:
        return f"name:{self.__name};country:{self.country};championship:{self.__championship};pot:{self.__pot};logo:{self.__logo}"

    def saw(self, t) -> bool:

        if not isinstance(t, Team):
            raise Exception("only team object can be opponent!")

        found = False

        for team in self.tracking:
            if team.name == t.name:
                found = True
                break
        return found

    def accept(self, opp, where: str) -> bool:

        if not isinstance(opp, Team):
            raise Exception("only team object can be opponent!")

        teams_from_same_country = self.contains_two_teams_from_same_country()

        pot_key = f"pot_{opp.pot}"

        # team not exists
        if (
            not self.opp_in_tracking(opp=opp)
            and where not in self.matches[pot_key].keys()
            and teams_from_same_country != None
            and not self.find_team_from_contry(opp.country)
            and opp.country != teams_from_same_country
        ) or (
            not self.opp_in_tracking(opp=opp)
            and where not in self.matches[pot_key].keys()
            and teams_from_same_country == None
        ):
            return True

        else:
            return False

    # methods
    def add(self, t, pot_id: int, where: str):

        if not isinstance(t, Team):
            raise Exception("only team object can be opponent!")

        pot_name = f"pot_{pot_id}"

        self.matches[pot_name][where] = {
            "name": t.name,
            "country": t.country,
            "championship": t.championship,
            "pot": t.pot,
            "logo": t.logo,
        }

        self.tracking.append(t)

    def opp_in_tracking(self, opp) -> bool:

        if not isinstance(opp, Team):
            raise Exception("only team can be opponent!")

        found = False
        for team in self.tracking:
            if opp.name == team.name:
                found = True
                break
        return found

    def find_team_from_contry(self, country: str) -> bool:
        found = False
        for team in self.tracking:
            if team.country == country:
                found = True
                break
        return found

    def contains_two_teams_from_same_country(self) -> str | None:
        country = None

        if len(self.tracking) == 0:
            return False

        for team_saved in self.tracking:
            if country:
                break
            for other_team in self.tracking:
                if (
                    other_team.name != team_saved.name
                    and team_saved.country == other_team.country
                ):
                    country = team_saved.country
                    break
                else:
                    continue

        return country

    def need(self, pot_id: int) -> Tuple[bool, bool]:

        pot_name = f"pot_{pot_id}"

        keys = self.matches[pot_name].keys()

        # opponents is complete
        if len(self.tracking) == 8:
            return True, True

        if len(keys) == 0:
            return False, False
        elif (HOME in keys) and (AWAY in keys):
            return True, True
        elif (HOME in keys) and (AWAY not in keys):
            return True, False
        elif (HOME not in keys) and (AWAY in keys):
            return False, True

    def free(self) -> bool:
        return len(self.tracking) < 8
