from config.data_struct import PLAYERS
from utils.log import Logger
from db.db_redis import RedisDB

LOG = Logger("Players_DB")
DB = RedisDB()


class Player:

    def __init__(self, data: dict):
        self.raw_data = data

        self.id = int(data["id"])
        self.db = f"Players:{self.id}"
        self.team_code = int(data["team_code"])
        self.now_cost = float(data["now_cost"])
        self.web_name = data["web_name"]
        self.total_points = float(data["total_points"])
        self.status = data["status"]
        self.form = data["form"]
        self.element_type = data["element_type"]
        self.stats = self.validate_stats()
        self.fpl_stats = self.validate_fpl_stats()
        self.rank = self.validate_rank()
        self.expected = self.validate_expected()
        self.stats_per_90 = self.validate_stats_per_90()
        

        if not DB.hget_all(self.db):
            LOG.info(f"Creating player: {self.web_name} with id: {self.id}")

            place_json = {
                "team_code": self.team_code,
                "now_cost": self.now_cost,
                "web_name": self.web_name,
                "total_points": self.total_points,
                "status": self.status,
                "form": self.form,
                "element_type": self.element_type,
            }
            DB.hset_one(f'player_name:{self.web_name}', "id", self.id)
            DB.hset_one(f'player_name:{self.web_name}', "club", self.team_code)
            DB.hset_dict(self.db, place_json)

    def validate_stats(self):
        return self.valid_check(PLAYERS["stats"].copy(), "stats")

    def valid_check(self, dict_copy, section):

        for key, value in dict_copy.items():
            if key in self.raw_data:
                data = self.raw_data[key]
                if data == "" or data == None:
                    data = 0
                dict_copy[key] = float(data) if isinstance(value, int) else data
                DB.hset_one(self.db, f"{section}.{key}", dict_copy[key])

        return dict_copy

    def validate_fpl_stats(self):
        return self.valid_check(PLAYERS["fpl_stats"].copy(), "fpl_stats")

    def validate_rank(self):
        return self.valid_check(PLAYERS["rank"].copy(), "rank")

    def validate_expected(self):
        return self.valid_check(PLAYERS["expected"].copy(), "expected")

    def validate_stats_per_90(self):
        return self.valid_check(PLAYERS["stats_per_90"].copy(), "stats_per_90")
