from typing import List, Dict
from backend.models.Pot import Pot
from random import shuffle, randint
from utils import HOME, AWAY, tirages_path_json
from backend.models.Team import Team
from backend.models.Pot import Pot
import json


class Draw:
    all = []
    indexes = [[], []]
    reset = False

    def __init__(self, pots: List[Pot]) -> None:
        self.__pots = pots
        self.__results = []
        self.noFree = []
        self.__tirages = {}

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
            Draw.all.append(team)
        return pots

    def launch_draw(self) -> None:
        i = 0
        while len(Draw.all):

            pot = self.pots[i]  # get pot

            shuffle(pot.teams)

            for team in pot.teams:  # get team from current pot

                for p in self.pots:

                    opp = list(
                        filter(lambda t: t.championship != team.championship, p.teams)
                    )  # get opponents from others championship

                    shuffle(opp)

                    home, away = team.need_opponent_from_pot(pot_id=p.num)

                    for opp_team in opp:

                        if home == False and away == False:
                            break

                        same_country = (
                            team.get_country_from_same_club()
                        )  # club from same country

                        opp_country = team.get_opp_country(opp_team)

                        if same_country != None:
                            if (
                                same_country == opp_team.country
                                or opp_country == opp_team.country
                            ):
                                continue

                        t_same_country = opp_team.get_country_from_same_club()
                        t_opp_country = opp_team.get_opp_country(team)

                        if t_same_country != None:
                            if (
                                t_same_country == team.country
                                or t_opp_country == team.country
                            ):
                                continue

                        t_home, t_away = opp_team.need_opponent_from_pot(
                            pot_id=team.pot
                        )

                        if home and t_away:
                            team.setMatch(t=opp_team, where=HOME)
                            opp_team.setMatch(t=team, where=AWAY)
                            home = False
                        elif away and t_home:
                            team.setMatch(t=opp_team, where=AWAY)
                            opp_team.setMatch(t=team, where=HOME)
                            away = False
                        else:
                            continue
                if (
                    len(team.matched + team.tracking) == 8
                    and len(
                        list(
                            filter(
                                lambda x: x["name"] == team.name, self.results.copy()
                            )
                        )
                    )
                    == 0
                ):
                    Draw.all = list(
                        filter(lambda x: x.name != team.name, Draw.all.copy())
                    )
                    team.save()
                    self.results.append(
                        {
                            "name": team.name,
                            "trancking": len(team.tracking),
                            "matches": team.matches,
                        }
                    )
                    team.matched = []
                    pot.remove(t=team)
                else:
                    print(
                        "reset!",
                        i,
                        "tracking",
                        len(team.tracking),
                        "all",
                        len(Draw.all),
                    )
                    team.reset()

                    # Draw.reset = True
                    break
            i = randint(0, len(self.pots) - 1)
            # pot.make_resume()

    def set_matches(self) -> None:
        while len(Draw.all):
            self.launch_draw()

    def resume(self, team: Team, size: int) -> None:
        if (
            len(team.tracking) == size
            and len(list(filter(lambda x: x.name == team.name, self.results))) == 0
        ):
            self.results.append(team)
        elif (
            len(team.tracking) != size
            and len(list(filter(lambda x: x.name == team.name, self.noFree))) == 0
        ):
            self.noFree.append(team)

    def removeTeam(self, team: Team, teams: list) -> None:
        for i, t in enumerate(teams):
            if team.name == t.name:
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

    def make_draw(self):
        self.launch_draw()
        self.generate_tirages()
        print("finish!")

    def generate_tirages(self):

        # clean tirages
        for club in self.results:
            # tirages[club].pop(self.TRACKING)
            self.tirages[club["name"]] = club["matches"]

        # Serializing json
        json_object = json.dumps(self.tirages, indent=4, ensure_ascii=False)

        # Writing to sample.json
        with open(tirages_path_json, "w", encoding="utf-8") as outfile:
            outfile.write(json_object)

    def random_teams(self) -> None:
        for pot in self.pots:
            teams = pot.teams
            shuffle(teams)
            pot.teams = teams
