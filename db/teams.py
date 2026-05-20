from config.data_struct import TEAMS
from config.data_maps import FOTMOB_NAME_MAP
from utils.log import Logger
from db.db_redis import RedisDB

LOG = Logger("Teams_DB")
DB = RedisDB()


class Team:


    def __init__(self, data: dict):
        self.raw_data = data

        self.name = self.validate_name()
        self.short_name = self.validate_short_name()
        self.tid = int(data["code"])
        self.table = self.validate_table()
        self.expected = self.validate_expected()
        self.strength = self.validate_strength()
        self.db = f"teams:{self.tid}"


        if not DB.hget_all(self.db):
            LOG.info(f"Creating team: {self.name} with tid: {self.tid}")
            place_json = {
                "name": self.name,
                "short_name": self.short_name
            }
            DB.hset_one(f"team_name:{self.name}", "tid", self.tid)
            DB.hset_dict(self.db, place_json)
            DB.hset_dict(self.db, self.table, "table")
            DB.hset_dict(self.db, self.strength, "strength")
            DB.hset_dict(self.db, self.expected, "expected")


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

