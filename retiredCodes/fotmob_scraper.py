from config.settings import (
    FOTMOB_BASE,
    FOTMOB_TEAM_STATS,
    TEAM_STATS_SECTION_CLASS,
    TEAM_STATS_DIV_CLASS,
)


team_stats_dic = {}


async def team_stats_links_scrap():
    LOG.info("Started team_stats_links_scrap()")

    s = Scraper()
    await s.enable_playwright()
    await s.page_load(FOTMOB_TEAM_STATS)

    for key, value in team_stats_dic.items():

        retry_count = 0
        max_retries = 3

        while retry_count < max_retries:
            try:
                data = await s.fetch_playwright(
                    f".{TEAM_STATS_SECTION_CLASS}", value[0]
                )
                section = data.find("section", class_=TEAM_STATS_SECTION_CLASS)
                div = section.find_all("div", class_=TEAM_STATS_DIV_CLASS)
                team_stats_dic[key] = (value[0], div)
                print(
                    f"Stats for {key}: {div}"
                )  # Debug print to check the scraped data
                LOG.info(f"Successfully scraped stats for {key}")
                break  # Exit the retry loop on success
            except Exception as e:
                retry_count += 1
                LOG.error(
                    f"Error scraping stats for {key} (Attempt {retry_count}/{max_retries}): {e}"
                )
                if retry_count == max_retries:
                    LOG.error(
                        f"Failed to scrape stats for {key} after {max_retries} attempts."
                    )


async def team_stats_links():
    LOG.info("Started team_stats_links()")

    s = Scraper()
    await s.enable_playwright()
    await s.page_load(FOTMOB_TEAM_STATS)
    data = await s.fetch_playwright(f".{TEAM_STATS_SECTION_CLASS}")
    section = data.find("section", class_=TEAM_STATS_SECTION_CLASS)
    div = section.find_all("div", class_=TEAM_STATS_DIV_CLASS)

    for box in div:
        key = (
            box.a.h3.text.strip()
            .lower()
            .replace(" ", "_")
            .replace("(", "")
            .replace(")", "")
            .replace("see_all", "")
        )

        value = box.a.get("href")

        team_stats_dic[key] = (FOTMOB_BASE + value, False)

    await s.close_page()  # Close the Playwright page after scraping is done

    LOG.info("Finished team_stats_links()")
