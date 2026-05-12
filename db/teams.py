from config.data_struct import FOTMOB_NAME_MAP, TEAMS
from utils.log import Logger

LOG = Logger("Teams_DB")


class Team:

    teams = []  # Class variable to hold all team instances

    def __init__(self, data: dict):
        self.raw_data = data

        self.name = self.validate_name()
        self.short_name = self.validate_short_name()
        self.tid = int(data["code"])
        self.table = self.validate_table()
        self.expected = self.validate_expected()
        self.strength = self.validate_strength()


        check = False
        for team in Team.teams:
            if self.name == team.name:
                check = True

        if not check:
            LOG.info(f"Creating team: {self.name} with tid: {self.tid}")
            self.add_team(self)  # Add the team instance to the class variable list

    def validate_table(self):
        return TEAMS["table"].copy()

    def validate_expected(self):
        return TEAMS["expected"].copy()

    def validate_strength(self):

        dict_copy = TEAMS["strength"].copy()

        for key in dict_copy:
            if key in self.raw_data:
                dict_copy[key] = float(self.raw_data[key])

        return dict_copy

    def validate_name(self):
        if "name" in self.raw_data and isinstance(self.raw_data["name"], str):
            name = self.raw_data["name"]
            if name in FOTMOB_NAME_MAP:
                name = FOTMOB_NAME_MAP[name]
            return name
        else:
            LOG.error("Invalid or missing 'name' field in team data.")

    def validate_short_name(self):
        if "short_name" in self.raw_data and isinstance(self.raw_data["short_name"], str):
            return self.raw_data["short_name"]
        else:
            LOG.error("Invalid or missing 'short_name' field in team data.")

    @classmethod
    def update_expected(cls, key, data, team_name):

        if key not in TEAMS["expected"]:
            LOG.error(f"{key} is not a valid key in expected data structure.")
            return

        for team in cls.teams:
            if team.name == team_name:
                if key in team.expected:
                    team.expected[key] = data or '' if  isinstance(data, str) else float(0)
                    LOG.info(
                        f"Updated {team_name} : {key} in expected with value {data}"
                    )
                else:
                    LOG.error(
                        f"{key} is not a valid key in {team_name}'s expected data structure."
                    )
                return

        LOG.error(f"{team_name} : {key} in expected was not updated with {data} value")

    @classmethod
    def update_table(cls, key, data, team_name):

        if key not in TEAMS["table"]:
            LOG.error(f"{key} is not a valid key in table data structure.")
            return

        for team in cls.teams:
            if team.name == team_name:
                if key in team.table:
                    team.table[key] = data if isinstance(data, str) or isinstance(data, list) else float(data)
                    LOG.info(f"Updated {team_name} : {key} in table with value {data}")
                else:
                    LOG.error(
                        f"{key} is not a valid key in {team_name}'s table data structure."
                    )
                return

        LOG.error(f"{team_name} : {key} in table was not updated with {data} value")

    @classmethod
    def add_team(cls, team):
        if isinstance(team, Team) and team not in cls.teams:
            cls.teams.append(team)
