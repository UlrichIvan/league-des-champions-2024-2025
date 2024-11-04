from typing import List, Dict
from backend.models.Pot import Pot
from random import shuffle
from utils import HOME, AWAY
from backend.models.Team import Team
from backend.models.Pot import Pot


class Draw:
    def __init__(self, pots: List[Pot]) -> None:
        self.__pots = pots
        self.__results = []
        self.noFree = []

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

    def set_matches(self) -> None:
        for pot in self.pots:  # current pot
            for team in pot.teams:  # current team from current pot
                for other_pot in self.pots:  # others pots include current pot
                    teams_opp = [
                        team_opp
                        for team_opp in other_pot.teams
                        if team_opp.country != team.country
                    ]  # get all teams from current pot that championship not match with current team

                    # shuffle list of teams opponents to get randow list
                    shuffle(teams_opp)

                    # get needle from current team
                    home, away = team.need(pot_id=other_pot.id)

                    # loop teams from current pot
                    for t in teams_opp:
                        if home and away:
                            break
                        else:
                            t_home, t_away = t.need(pot_id=team.pot)
                            if (
                                not home
                                and not t_away
                                and team.accept(opp=t, where=HOME)
                                and t.accept(opp=team, where=AWAY)
                            ):
                                team.add(t=t, pot_id=t.pot, where=HOME)
                                t.add(t=team, pot_id=team.pot, where=AWAY)
                                home = True
                            elif (
                                not away
                                and not t_home
                                and team.accept(opp=t, where=AWAY)
                                and t.accept(opp=team, where=HOME)
                            ):
                                team.add(t=t, pot_id=t.pot, where=AWAY)
                                t.add(t=team, pot_id=team.pot, where=HOME)
                                away = True
                            else:
                                continue

                if len(team.tracking) == 8:
                    self.results.append(
                        {
                            "name": team.name,
                            "matches": len(team.tracking),
                            "pot": team.pot,
                            "country": team.country,
                        }
                    )

                    pot.remove(t=team)
                    self.removeTeam(team, self.noFree)

                else:
                    if not self.contains(team, self.noFree):
                        self.noFree.append(
                            {
                                "name": team.name,
                                "matches": len(team.tracking),
                                "pot": team.pot,
                                "country": team.country,
                            }
                        )

    def removeTeam(self, team: Team, teams: list) -> None:
        for i, t in enumerate(teams):
            if team.name == t["name"]:
                teams.pop(i)
                break

    def contains(self, team: Team, teams: list) -> bool:
        found = False
        for t in teams:
            if team.name == t["name"]:
                found = True
        return found

    def mathes_not_complete(self) -> bool:
        count = 0
        for pot in self.pots:
            if len(pot.teams):
                count += 1
        return count > 0

    # methods Objects
    def make_draw(self):
        while self.mathes_not_complete():
            self.random_teams()
            self.set_matches()

        print("finish!")

    def random_teams(self) -> None:
        for pot in self.pots:
            teams = pot.teams
            shuffle(teams)
            pot.teams = teams
