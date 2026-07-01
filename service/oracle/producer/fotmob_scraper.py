from service.oracle.utils.scraper import Scraper
from service.oracle.utils.log import Logger
from service.oracle.config.settings import FOTMOB_FORM
from service.oracle.db.db_redis import RedisDB
import json

FOTMOB_TO_FPL_NAME = {
    "Man United": "Man Utd",
    "Nottm Forest": "Nott'm Forest",
    "Tottenham": "Spurs",
    "Manchester United": "Man Utd",
    "Nottingham Forest": "Nott'm Forest",
    "Tottenham Hotspur": "Spurs",
    "Manchester City": "Man City",
    "Newcastle United": "Newcastle",
    "Brighton and Hove Albion": "Brighton",
    "Wolverhampton Wanderers": "Wolves",
    "West Ham United": "West Ham",
    "Leeds United": "Leeds",
}

LOG = Logger("Fotmob_Scraper", "producer")
DB = RedisDB()

_SCRAPED_DATA = None


def safe_float_str(val, decimal_places=2, with_sign=False):
    if val is None or val == "":
        return "0.0"
    try:
        f_val = float(val)
        fmt = f"+.{decimal_places}f" if with_sign else f".{decimal_places}f"
        return f"{f_val:{fmt}}"
    except (ValueError, TypeError):
        return str(val)


async def _ensure_scraped_data():
    global _SCRAPED_DATA
    if _SCRAPED_DATA is not None:
        return

    LOG.info("Scraping all FotMob tables in a single page load...")
    s = Scraper()
    await s.enable_playwright()
    try:
        # Load FOTMOB_FORM which contains all tables (all, home, away, form, xg)
        await s.page_load(FOTMOB_FORM)

        # Get content of __NEXT_DATA__
        content = await s.browser.page.locator("#__NEXT_DATA__").text_content()
        if not content:
            LOG.error("Failed to get __NEXT_DATA__ from page")
            return

        data = json.loads(content)
        pprops = data.get("props", {}).get("pageProps", {})

        table_list = pprops.get("table", [])
        if not table_list:
            LOG.error("No table data found in pageProps")
            return

        _SCRAPED_DATA = table_list[0]
        LOG.info("Successfully loaded and cached FotMob data")
    except Exception as e:
        LOG.error(f"Error during single-pass FotMob scrape: {e}")
    finally:
        await s.close_page()
        await s.close_browser()


async def home_table_scrap():
    LOG.info("========== START home_table_scrap() ==========")
    await _ensure_scraped_data()
    if _SCRAPED_DATA:
        await _process_and_save("home")
    LOG.info("========== END home_table_scrap() ==========")


async def away_table_scrap():
    LOG.info("========== START away_table_scrap() ==========")
    await _ensure_scraped_data()
    if _SCRAPED_DATA:
        await _process_and_save("away")
    LOG.info("========== END away_table_scrap() ==========")


async def form_table_scrap():
    LOG.info("========== START form_table_scrap() ==========")
    await _ensure_scraped_data()
    if _SCRAPED_DATA:
        await _process_and_save("last_five")
    LOG.info("========== END form_table_scrap() ==========")


async def table_scrap():
    LOG.info("========== START table_scrap() ==========")
    await _ensure_scraped_data()
    if _SCRAPED_DATA:
        await _process_and_save("table")
    LOG.info("========== END table_scrap() ==========")


async def xg_scrap():
    LOG.info("========== START xg_scrap() ==========")
    await _ensure_scraped_data()
    if _SCRAPED_DATA:
        await _process_and_save("xg")
    LOG.info("========== END xg_scrap() ==========")


async def _process_and_save(field_type):
    global _SCRAPED_DATA
    if not _SCRAPED_DATA:
        LOG.error("No scraped data available to process")
        return

    data_dict = _SCRAPED_DATA.get("data", {}) or {}
    table_data = data_dict.get("table", {}) or {}
    team_form_dict = _SCRAPED_DATA.get("teamForm", {}) or {}

    # Map field_type to the JSON table key
    json_key = "all" if field_type == "table" else "form" if field_type == "last_five" else field_type

    rows = table_data.get(json_key, [])
    if not rows:
        LOG.error(f"No rows found in FotMob data for key: {json_key}")
        return

    LOG.info(f"Processing {len(rows)} rows for field: {field_type}")

    for idx, row in enumerate(rows, start=1):
        try:
            name = row.get("shortName") or row.get("name")
            mapped_name = FOTMOB_TO_FPL_NAME.get(name, name)
            tid = await DB.hget_one(f"index:team:{mapped_name}", "tid")
            if not tid:
                # Try with full name as fallback
                name_full = row.get("name")
                mapped_name = FOTMOB_TO_FPL_NAME.get(name_full, name_full)
                tid = await DB.hget_one(f"index:team:{mapped_name}", "tid")

            if not tid:
                LOG.error(f"Could not map team name {name} to FPL tid")
                continue

            # Build common form string
            team_id_str = str(row.get("id"))
            form_list = team_form_dict.get(team_id_str, []) or []
            form_digits = []
            for match in form_list[-5:]:
                res = match.get("resultString")
                if res == "W":
                    form_digits.append("3")
                elif res == "D":
                    form_digits.append("1")
                else:
                    form_digits.append("0")
            form_str = "".join(form_digits)

            if field_type == "xg":
                # xG specific fields
                place_json = {
                    "xg": safe_float_str(row.get("xg"), 2),
                    "xga": safe_float_str(row.get("xgConceded"), 2),
                    "xpts": safe_float_str(row.get("xPoints"), 2),
                    "xg_difference": safe_float_str(row.get("xgDiff"), 2, with_sign=True),
                    "xga_difference": safe_float_str(row.get("xgConcededDiff"), 2, with_sign=True),
                    "xpts_difference": safe_float_str(row.get("xPointsDiff"), 2, with_sign=True),
                }
                await DB.hset_dict(f"team:{tid}:expected", place_json)
            else:
                # For table, home, away, form
                scores = row.get("scoresStr", "0-0").split("-")
                goals = scores[0]
                conceded = scores[1]

                place_json = {
                    "goals": goals,
                    "conceded": conceded,
                    "position": str(row.get("idx", idx)),
                    "played": str(row.get("played", 0)),
                    "win": str(row.get("wins", 0)),
                    "draw": str(row.get("draws", 0)),
                    "loss": str(row.get("losses", 0)),
                    "points": str(row.get("pts", 0)),
                    "form": form_str,
                }

                if field_type == "table":
                    mapped_json = {
                        "goals_for": goals,
                        "goals_against": conceded,
                        "position": str(row.get("idx", idx)),
                        "played": str(row.get("played", 0)),
                        "wins": str(row.get("wins", 0)),
                        "draws": str(row.get("draws", 0)),
                        "losses": str(row.get("losses", 0)),
                        "points": str(row.get("pts", 0)),
                        "form": form_str,
                    }
                    await DB.hset_dict(f"team:{tid}", mapped_json)
                else:
                    await DB.hset_dict(f"team:{tid}:{field_type}", place_json)

            LOG.info(f"[{field_type}] Row {idx}: Saved → {name}")

        except Exception as e:
            LOG.error(f"Error parsing row {idx} for {field_type}: {e}")

    LOG.info(f"Completed table fetch for: {field_type}")
