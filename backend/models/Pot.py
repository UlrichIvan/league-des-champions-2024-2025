from typing import List
from backend.models.Team import Team


class Pot:
    id: int
    teams: List[Team]

    # instance attribute
    def __init__(self, id: str, teams: List[Team]) -> None:
        self.id = id
        self.teams = teams

    def remove(self, t: Team) -> None:
        for i, team in enumerate(self.teams):
            if team.name == t.name:
                self.teams.pop(i)
                break
