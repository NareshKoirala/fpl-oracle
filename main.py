from utils.log import Logger
from producer.fpl_scraper import fpl_data_to_db
from db.teams import Team
from producer.fotmob_scraper import table_scrap, team_stats_scrap
 

LOG = Logger("Main")
LOG.info("---------------------------Main Running----------------------------------")

LOG.info("Starting fpl_data_to_db")
#fpl_data_to_db()
LOG.info("Finished fpl_data_to_db")

LOG.info("Starting table_scrap")
#table_scrap()
LOG.info("Finished table_scrap")


LOG.info("Starting team_stats_scrap")
team_stats_scrap()
LOG.info("Finished team_stats_scrap")


#for team in Team.teams:
#    print(f"{team.tid}). {team.name}:- ")
#    print(team.raw_data)
