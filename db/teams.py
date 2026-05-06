from config.data_struct import FOTMOB_NAME_MAP, TEAMS_KEYS
from utils.log import Logger

LOG = Logger("Teams_DB")


class Team:

    teams = []  # Class variable to hold all team instances

    def __init__(self, data: dict):
        self.data = data
        self.name = self.validate_name()
        self.short_name = self.validate_short_name()
        self.raw_data = self.validate_raw_data()
        self.tid = data["code"]

        check = False
        for team in Team.teams:
            if self.name == team.name:
                check = True

        if not check:
            LOG.info(f"Creating team: {self.name} with tid: {self.tid}")
            self.add_team(self)  # Add the team instance to the class variable list

    def validate_name(self):
        if "name" in self.data and isinstance(self.data["name"], str):
            name = self.data["name"]
            if name in FOTMOB_NAME_MAP:
                name = FOTMOB_NAME_MAP[name]
            return name
        else:
            LOG.error("Invalid or missing 'name' field in team data.")

    def validate_short_name(self):
        if "short_name" in self.data and isinstance(self.data["short_name"], str):
            return self.data["short_name"]
        else:
            LOG.error("Invalid or missing 'short_name' field in team data.")

    def validate_raw_data(self):
        data = {}

        for key in TEAMS_KEYS:
            if key in self.data:
                data[key] = self.data[key]
            else:
                data[key] = 0.0

        return data

    @classmethod
    def update_raw_data(cls, key, data, team_name):

        for index, team in enumerate(cls.teams):
            if team.name == team_name:
                if team.raw_data[key] != data:
                    LOG.info(f"{team_name} : {key} updated with {data} for {team.raw_data[key]}")
                    cls.teams[index].raw_data[key] = data
                return
            
        LOG.error(f"{team_name} : {key} in raw_data was not updated with {data} value")

    @classmethod
    def add_team(cls, team):
        if isinstance(team, Team) and team not in cls.teams:
            cls.teams.append(team)