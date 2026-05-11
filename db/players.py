from config.data_struct import PLAYERS
from utils.log import Logger

LOG = Logger("Players_DB")

class Player:
    players = []  # Class variable to hold all player instances
    
    def __init__(self, data: dict):
        self.raw_data = data
        
        self.id = data["id"]
        self.team_code = data["team_code"]
        self.now_cost = data["now_cost"]
        self.web_name = data["web_name"]
        self.total_points = data["total_points"]
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
        dict_copy = PLAYERS["stats"].copy()

        for key in dict_copy:
            if key in self.raw_data:
                dict_copy[key] = self.raw_data[key]

        return dict_copy
    
    def validate_fpl_stats(self):
        dict_copy = PLAYERS["fpl_stats"].copy()

        for key in dict_copy:
            if key in self.raw_data:
                dict_copy[key] = self.raw_data[key]

        return dict_copy
    
    def validate_rank(self):
        dict_copy = PLAYERS["rank"].copy()
        
        for key in dict_copy:
            if key in self.raw_data:
                dict_copy[key] = self.raw_data[key]

        return dict_copy
    
    def validate_expected(self):
        dict_copy = PLAYERS["expected"].copy()

        for key in dict_copy:
            if key in self.raw_data:
                dict_copy[key] = self.raw_data[key]

        return dict_copy
    
    def validate_stats_per_90(self):
        dict_copy = PLAYERS["stats_per_90"].copy()

        for key in dict_copy:
            if key in self.raw_data:
                dict_copy[key] = self.raw_data[key]

        return dict_copy
    
    @classmethod
    def add_player(cls, player):
        cls.players.append(player)
    