from utils.log import Logger
from config.data_struct import FPL_FIXTURES
from db.db_redis import RedisDB

LOG = Logger("FPL_Fixtures")
DB = RedisDB()


class FFixtures:

    def __init__(self, raw_data):
        self.raw_data = raw_data

        self.id = raw_data["id"]
        self.db = f"fpl_fixtures:{self.id}"
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
        

        LOG.info(f"Creating fpl_fixtures: {self.name} with tid: {self.id}")

        place_json = {
            "name": str(self.name),
            "deadline_time": str(self.deadline_time),
            "is_current": str(self.is_current),
            "is_previous": str(self.is_previous),
            "is_next": str(self.is_next),
            "finished": str(self.finished),
            "data_checked": str(self.data_checked),
            "most_selected": str(self.most_selected),
            "highest_score": str(self.highest_score),
            "most_transferred_in": str(self.most_transferred_in),
            "top_element": str(self.top_element),
            "most_captained": str(self.most_captained),
            "most_vice_captained": str(self.most_vice_captained),
        }

        DB.hset_dict(self.db, place_json)

    def validate_top_element_info(self):
        temp_dict = {}

        if self.raw_data["top_element_info"] == None:
            return temp_dict

        for k, v in self.raw_data["top_element_info"].items():
            temp_dict[k] = v
            DB.hset_one(self.db, f"top_element_info.{k}", str(v))
        return temp_dict

