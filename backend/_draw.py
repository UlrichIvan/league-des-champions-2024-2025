# Ce module contient la classe de tirage au sort.
from backend.models.Team import Team
from typing import List, Dict
from random import shuffle
import json
from utils import tirages_path_json


class Draw:

    def __init__(self, list_teams_from_json: List[dict]) -> None:
        # Définissez les attributs dont vous aurez besoin
        self.__tirages = {}
        self.__teams: List[Team] = []
        self.__pots: Dict[int, List[Team]] = {1: [], 2: [], 3: [], 4: []}
        self.init_tirages(list_teams_from_json)

    # pots
    @property
    def pots(self) -> Dict[int, List[Team]]:
        return self.__pots

    @pots.setter
    def pots(self, pots: Dict[int, List[Team]]) -> None:
        self.__pots = pots

    # tirages
    @property
    def tirages(self) -> dict:
        return self.__tirages

    @tirages.setter
    def tirages(self, tirages: dict) -> None:
        self.__tirages = tirages

    # teams
    @property
    def teams(self) -> List[Team]:
        return self.__teams

    @teams.setter
    def teams(self, teams: List[Team]) -> None:
        self.__teams = teams

    # methods

    def init_tirages(self, teams: list[dict]) -> None:
        for team in teams:
            if team["chapeau"] in self.pots:
                self.pots[team["chapeau"]].append(
                    Team(
                        nom=team["nom"],
                        pays=team["pays"],
                        championnat=team["championnat"],
                        chapeau=team["chapeau"],
                        logo=team["logo"],
                    )
                )
            # init tirages
            if not team["nom"] in self.tirages.keys():
                self.tirages[team["nom"]] = {
                    "pot_1": {},
                    "pot_2": {},
                    "pot_3": {},
                    "pot_4": {},
                    self.TRACKING: [],
                }

    def add_team_to(self, where: str, team: Team, team_opp: Team) -> bool:

        tracking: List[Team] = self.tirages[team.nom][self.TRACKING]

        data = self.tirages[team.nom]

        pot = f"pot_{team_opp.chapeau}"

        data[pot][where] = {}

        data[pot][where].update(
            {
                "nom": team_opp.nom,
                "pays": team_opp.pays,
                "championnat": team_opp.championnat,
                "chapeau": team_opp.chapeau,
                "logo": team_opp.logo,
            }
        )

        tracking.append(team_opp)

        data[self.TRACKING] = tracking

        self.tirages[team.nom] = data

        return True

    def exist_two_teams_from_same_championnat(self, tracking: List[Team]) -> str | None:
        championnat = None
        found = False
        for team_tracked in tracking:
            if found:
                break
            for other_team in tracking:
                if (
                    other_team.nom != team_tracked.nom
                    and team_tracked.championnat == other_team.championnat
                ):
                    found = True
                    championnat = team_tracked.championnat
                    break
                else:
                    continue

        return championnat

    def exist_team_with_championnat_in_tracking(
        self, championnat: str, tracking: List[Team]
    ) -> bool:
        found = False
        for team in tracking:
            if team.championnat == championnat:
                found = True
                break
        return found

    def team_can_be_add(
        self, target: Team, team_opp: Team, chapeau: int, where: str
    ) -> bool:

        tracking: List[Team] = self.tirages[target.nom][self.TRACKING]
        data = self.tirages[target.nom]
        pot = f"pot_{chapeau}"

        exist_two_teams_from_same_championnat = (
            self.exist_two_teams_from_same_championnat(tracking=tracking)
        )

        if where in data[pot]:
            return False

        elif exist_two_teams_from_same_championnat != None:

            if team_opp.championnat == exist_two_teams_from_same_championnat:
                return False
            elif not self.exist_team_with_championnat_in_tracking(
                team_opp.championnat, tracking
            ):
                return True
            else:
                return False
        else:
            return True

    def team_exists_in_tracking(self, team_opp: Team, tracking: List[Team]) -> bool:

        found = False

        if len(tracking) == 0:
            return False

        for team in tracking:
            if team.nom == team_opp.nom:
                found = True
                break

        return found

    # Définissez les méthodes dont vous aurez besoin

    def generate_tirages(self):

        tirages = self.tirages

        # clean tirages
        for club, _ in tirages.items():
            # tirages[club].pop(self.TRACKING)
            tirages[club][self.TRACKING] = len(tirages[club][self.TRACKING])

        self.tirages = tirages

        # Serializing json
        json_object = json.dumps(self.tirages, indent=4, ensure_ascii=False)

        # Writing to sample.json
        with open(tirages_path_json, "w", encoding="utf-8") as outfile:
            outfile.write(json_object)

    def make_draw(self):

        for _, teams in self.pots.items():

            i = 0
            j = 1
            while i < len(teams):
                team = teams[i]
                for chapeau, others_teams in self.pots.items():
                    teams_opp = [
                        team_opp
                        for team_opp in others_teams
                        if team.championnat != team_opp.championnat
                    ]

                    # random opponents
                    shuffle(teams_opp)

                    home = False
                    away = False

                    for team_opp in teams_opp:

                        if home and away:
                            break

                        where = "home" if not home else "away"

                        if (
                            self.team_exists_in_tracking(
                                team_opp=team_opp,
                                tracking=self.tirages[team.nom][self.TRACKING],
                            )
                            or len(self.tirages[team.nom][self.TRACKING]) == 8
                        ):
                            continue

                        elif self.team_can_be_add(
                            target=team,
                            chapeau=chapeau,
                            where=where,
                            team_opp=team_opp,
                        ):

                            if not home and self.team_can_be_add(
                                target=team_opp,
                                team_opp=team,
                                chapeau=team.chapeau,
                                where="away",
                            ):
                                home = self.add_team_to(
                                    where=where,
                                    team=team,
                                    team_opp=team_opp,
                                )

                                self.add_team_to(
                                    where="away", team=team_opp, team_opp=team
                                )
                                continue
                            elif not away and self.team_can_be_add(
                                target=team_opp,
                                team_opp=team,
                                chapeau=team.chapeau,
                                where="home",
                            ):
                                away = self.add_team_to(
                                    where="away", team=team, team_opp=team_opp
                                )
                                self.add_team_to(
                                    where="home", team=team_opp, team_opp=team
                                )
                                continue
                            else:
                                continue

                        else:
                            continue
                i += 1
                j += 1
        if len(self.tirages):
            self.generate_tirages()
            print("Tirage au sort effectué!")
        else:
            print("Tirages lost!")
