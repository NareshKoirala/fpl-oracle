from utils.log import Logger
from producer.fpl_scraper import fpl_data_to_db, testing
from db.teams import Team
from producer.fotmob_scraper import table_scrap, team_stats_scrap
 

LOG = Logger("Main")
LOG.info("---------------------------Main Started----------------------------------")

#fpl_data_to_db()

#table_scrap()

#team_stats_scrap()

#testing()



#for team in Team.teams:
#    print(f"{team.tid}). {team.name}:- ")
#    print(team.raw_data)




LOG.info("---------------------------Main Closed----------------------------------")