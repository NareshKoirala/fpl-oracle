from config.data_struct import PLAYERS
from utils.log import Logger

LOG = Logger("Players_DB")

class Player:
    players = []  # Class variable to hold all player instances
    
    def __init__(self, data: dict):
        self.raw_data = data
        
        self.id = int(data["id"])
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
        

        check = False
        for player in Player.players:
            if self.id == player.id:
                check = True

        if not check:
            LOG.info(f"Creating player: {self.web_name} with id: {self.id}")
            self.add_player(self)  # Add the player instance to the class variable list
            
    def validate_stats(self):
        return self.valid_check(PLAYERS["stats"].copy())


    def valid_check(self, dict_copy):

        for key, value in dict_copy.items():
            if key in self.raw_data:
                data = self.raw_data[key]
                if data == "" or data == None:
                    data = 0
                dict_copy[key] = float(data) if isinstance(value, int) else data

        return dict_copy
    
    def validate_fpl_stats(self):
        return self.valid_check(PLAYERS["fpl_stats"].copy())

    
    def validate_rank(self):
        return self.valid_check(PLAYERS["rank"].copy())
    
    def validate_expected(self):
        return self.valid_check(PLAYERS["expected"].copy())
    
    def validate_stats_per_90(self):
        return self.valid_check(PLAYERS["stats_per_90"].copy())
    
    @classmethod
    def add_player(cls, player):
        cls.players.append(player)
    