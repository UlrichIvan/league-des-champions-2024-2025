from typing import List
from backend.models.Team import Team


class Pot:
    # instance attribute
    def __init__(self, id: str, teams: List[Team]) -> None:
        self.num = id
        self.teams = teams
        self.resumes = {}

    def remove(self, t: Team) -> None:
        for i, team in enumerate(self.teams):
            if team.name == t.name:
                self.teams.pop(i)
                break

    def make_resume(self) -> None:
        for team in self.teams:
            count = len(team.tracking)
            if count in self.resumes.keys():
                self.resumes[count] += 1
            else:
                self.resumes[count] = 1
