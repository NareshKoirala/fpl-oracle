from utils.log import Logger
from config.data_struct import FPL_FIXTURES
from db.db_redis import RedisDB

LOG = Logger("FPL_Fixtures")
DB = RedisDB()


class FFixtures:

    fpl_fixtures = []

    def __init__(self, raw_data):
        self.raw_data = raw_data

        self.id = raw_data["id"]
        self.name = raw_data["name"]
        self.deadline_time = raw_data["deadline_time"]
        self.is_current = raw_data["is_current"]
        self.is_previous = raw_data["is_previous"]
        self.is_next = raw_data["is_next"]
        self.finished = raw_data["finished"]
        self.data_checked = raw_data["data_checked"]
        self.most_selected = raw_data["most_selected"]
        self.highest_score = raw_data["highest_score"]
        self.most_transferred_in = raw_data["most_transferred_in"]
        self.top_element = raw_data["top_element"]
        self.most_captained = raw_data["most_captained"]
        self.most_vice_captained = raw_data["most_vice_captained"]
        self.top_element_info = self.validate_top_element_info()

        check = False
        for fpl_fixtures in FFixtures.fpl_fixtures:
            if self.name == fpl_fixtures.name:
                check = True
                break

        if not check:
            LOG.info(f"Creating fpl_fixtures: {self.name} with tid: {self.id}")
            self.add_ffixtures(self)  # Add the team instance to the class variable list
            DB.hset_one(f"fpl_fixtures:{self.id}", "name", str(self.name))
            DB.hset_one(
                f"fpl_fixtures:{self.id}", "deadline_time", str(self.deadline_time)
            )
            DB.hset_one(f"fpl_fixtures:{self.id}", "is_current", str(self.is_current))
            DB.hset_one(f"fpl_fixtures:{self.id}", "is_previous", str(self.is_previous))
            DB.hset_one(f"fpl_fixtures:{self.id}", "is_next", str(self.is_next))
            DB.hset_one(f"fpl_fixtures:{self.id}", "finished", str(self.finished))
            DB.hset_one(
                f"fpl_fixtures:{self.id}", "data_checked", str(self.data_checked)
            )
            DB.hset_one(
                f"fpl_fixtures:{self.id}", "most_selected", str(self.most_selected)
            )
            DB.hset_one(
                f"fpl_fixtures:{self.id}", "highest_score", str(self.highest_score)
            )
            DB.hset_one(
                f"fpl_fixtures:{self.id}",
                "most_transferred_in",
                str(self.most_transferred_in),
            )
            DB.hset_one(f"fpl_fixtures:{self.id}", "top_element", str(self.top_element))
            DB.hset_one(
                f"fpl_fixtures:{self.id}", "most_captained", str(self.most_captained)
            )
            DB.hset_one(
                f"fpl_fixtures:{self.id}",
                "most_vice_captained",
                str(self.most_vice_captained),
            )

    def validate_top_element_info(self):
        temp_dict = {}

        if self.raw_data["top_element_info"] == None:
            return temp_dict

        for k, v in self.raw_data["top_element_info"].items():
            temp_dict[k] = v
            DB.hset_one(f"fpl_fixtures:{self.id}", f"top_element_info.{k}", str(v))
        return temp_dict

    @classmethod
    def add_ffixtures(cls, fpl_fixtures):
        if isinstance(fpl_fixtures, FFixtures) and fpl_fixtures not in cls.fpl_fixtures:
            cls.fpl_fixtures.append(fpl_fixtures)
