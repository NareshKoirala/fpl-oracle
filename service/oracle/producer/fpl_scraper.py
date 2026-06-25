from service.oracle.utils.scraper import Scraper
from service.oracle.utils.log import Logger
from service.oracle.db.teams import get_teams
from service.oracle.db.players import get_players
from service.oracle.db.gw_fixtures import get_fixtures
from service.oracle.config.settings import FPL_BOOTSTRAP, YAHOO_SPORTS
import asyncio

LOG = Logger("Fpl_Scraper", "producer")


# ---------------------------------------------------------
# API FETCH
# ---------------------------------------------------------


async def api_fetch() -> dict:
    LOG.info("\n========== START api_fetch() ==========")

    data = await Scraper().fetch_request(FPL_BOOTSTRAP)

    if data:
        LOG.info("API data fetched successfully.")
        LOG.info(
            f"Teams: {len(data['teams'])}, "
            f"Players: {len(data['elements'])}, "
            f"Events: {len(data['events'])}"
        )
        LOG.info("========== END api_fetch() ==========\n")
        return data["teams"], data["elements"], data["events"]

    LOG.error("Failed to fetch API data.")
    LOG.info("========== END api_fetch() ==========\n")
    return None


# ---------------------------------------------------------
# MAIN FPL SCRAPER → DB
# ---------------------------------------------------------


async def fpl_data_to_db():
    LOG.info("\n========== START fpl_data_to_db() ==========")

    result = await api_fetch()

    if not result:
        LOG.error("API fetch failed — cannot continue fpl_data_to_db().")
        LOG.info("========== END fpl_data_to_db() ==========\n")
        return

    teams, players, fixtures = result

    LOG.info(f"Inserting {len(teams)} teams into DB...")
    for team in teams:
        await get_teams(team)

    LOG.info(f"Inserting {len(players)} players into DB...")
    for player in players:
        await get_players(player)

    LOG.info(f"Inserting {len(fixtures)} fixtures into DB...")
    for fixture in fixtures:
        await get_fixtures(fixture)

    LOG.info("All FPL bootstrap data inserted successfully.")
    LOG.info("========== END fpl_data_to_db() ==========\n")
