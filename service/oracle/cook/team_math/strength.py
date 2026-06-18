from db.db_redis import RedisDB
from utils.log import Logger

LOG = Logger("Strength", "cook/team_math")
DB = RedisDB()


async def cal_teams_strength():
    LOG.info("\n========== START cal_teams_strength() ==========")

    # -------------------------------
    # 1. Load EPL teams (1–20)
    # -------------------------------
    LOG.info("Loading EPL team IDs...")
    teams_key_map = await DB.get_keys("index:team:*")

    team_ids = []
    for key in teams_key_map:
        value = await DB.hget_all(key)
        team_ids.append(value["tid"])

    LOG.info(f"Loaded {len(team_ids)} teams.")

    # -------------------------------
    # 2. Compute league averages
    # -------------------------------
    LOG.info("Computing league averages...")
    avg = await league_avg_xg(team_ids)

    (
        avg_xg,
        avg_xga,
        avg_xpts,
        avg_rg,
        avg_rga,
        avg_rpts,
        avg_hg,
        avg_hga,
        avg_hpts,
        avg_hp,
        avg_ag,
        avg_aga,
        avg_apts,
        avg_ap,
        avg_fg,
        avg_fga,
        avg_fpts,
        avg_fp,
    ) = avg

    LOG.info("League averages computed.")

    # -------------------------------
    # 3. Compute team strengths
    # -------------------------------
    LOG.info("Calculating strengths for each team...")

    for tid in team_ids:
        LOG.info(f"→ Team {tid}: calculating strength")

        data_ex = await team_data(tid, "expected")
        data_h = await team_data(tid, "home")
        data_a = await team_data(tid, "away")
        data_f = await team_data(tid, "last_five")

        # ----- Overall Strength -----
        overall = cal_overall_strength(avg, data_ex)

        # ----- Home Attack -----
        hg = safe_float(data_h.get("goals"))
        hp = safe_float(data_h.get("played", 1))
        home_attack_raw = hg / hp
        home_attack = home_attack_raw / (avg_hg / avg_hpts)

        # ----- Away Attack -----
        ag = safe_float(data_a.get("goals"))
        ap = safe_float(data_a.get("played", 1))
        away_attack_raw = ag / ap
        away_attack = away_attack_raw / (avg_ag / avg_apts)

        # ----- Home Points -----
        hpts = safe_float(data_h.get("points"))
        home_pts_raw = hpts / hp
        home_pts = home_pts_raw / (avg_hpts / avg_hp)

        # ----- Away Points -----
        apts = safe_float(data_a.get("points"))
        away_pts_raw = apts / ap
        away_pts = away_pts_raw / (avg_apts / avg_ap)

        # ----- Home Defense -----
        hga = safe_float(data_h.get("conceded"))
        home_def_raw = hga / hp
        home_def = (avg_hga / avg_hpts) / home_def_raw

        # ----- Away Defense -----
        aga = safe_float(data_a.get("conceded"))
        away_def_raw = aga / ap
        away_def = (avg_aga / avg_apts) / away_def_raw

        # ----- Last Five Strength -----
        fg = safe_float(data_f.get("goals"))
        fga = safe_float(data_f.get("conceded"))
        fpts = safe_float(data_f.get("points"))
        fp = safe_float(data_f.get("played", avg_fp))

        last5_attack_raw = fg / fp
        last5_def_raw = fga / fp
        last5_pts_raw = fpts / fp

        last5_attack = last5_attack_raw / (avg_fg / avg_fpts)
        last5_def = (avg_fga / avg_fpts) / last5_def_raw
        last5_pts = last5_pts_raw / (avg_fpts / avg_fp)

        # -------------------------------
        # 4. Save to Redis
        # -------------------------------
        await DB.hset_dict(
            f"proc_teams_strength:{tid}",
            {
                **overall,
                "attack_home": f"{home_attack:.2f}",
                "defence_home": f"{home_def:.2f}",
                "points_home": f"{home_pts:.2f}",
                "attack_away": f"{away_attack:.2f}",
                "defence_away": f"{away_def:.2f}",
                "points_away": f"{away_pts:.2f}",
                "attack_last5": f"{last5_attack:.2f}",
                "defence_last5": f"{last5_def:.2f}",
                "points_last5": f"{last5_pts:.2f}",
            },
        )

        LOG.info(f"✓ Finished team {tid}")

    LOG.info("========== END cal_teams_strength() ==========\n")


def safe_float(v):
    try:
        return float(v)
    except:
        return 0.0


def cal_overall_strength(avg, data):

    xg = safe_float(data.get("xg"))
    xga = safe_float(data.get("xga"))
    xpts = safe_float(data.get("xpts"))

    xg_diff = safe_float(data.get("xg_difference"))
    xga_diff = safe_float(data.get("xga_difference"))
    xpts_diff = safe_float(data.get("xpts_difference"))

    rg = xg + xg_diff
    rga = xga + xga_diff
    rpts = xpts + xpts_diff

    return {
        "attack_overall_expected": f"{(xg / avg[0]):.2f}",
        "defence_overall_expected": f"{(avg[1] / xga):.2f}",
        "point_overall_expected": f"{(xpts / avg[2]):.2f}",
        "attack_overall_real": f"{(rg / avg[3]):.2f}",
        "defence_overall_real": f"{(avg[4] / rga):.2f}",
        "point_overall_real": f"{(rpts / avg[5]):.2f}",
    }


async def league_avg_xg(ids):
    LOG.info("Computing league averages for expected, real, home, away, last5...")

    total_xg = total_xga = total_xpts = 0
    total_rg = total_rga = total_rpts = 0

    total_hg = total_hga = total_hpts = total_hp = 0
    total_ag = total_aga = total_apts = total_ap = 0
    total_fg = total_fga = total_fpts = total_fp = 0

    size = len(ids)

    for tid in ids:
        data_ex = await team_data(tid, "expected")
        data_h = await team_data(tid, "home")
        data_a = await team_data(tid, "away")
        data_f = await team_data(tid, "last_five")

        # Expected
        xg = safe_float(data_ex.get("xg"))
        xga = safe_float(data_ex.get("xga"))
        xpts = safe_float(data_ex.get("xpts"))

        xg_diff = safe_float(data_ex.get("xg_difference"))
        xga_diff = safe_float(data_ex.get("xga_difference"))
        xpts_diff = safe_float(data_ex.get("xpts_difference"))

        total_xg += xg
        total_xga += xga
        total_xpts += xpts

        total_rg += xg + xg_diff
        total_rga += xga + xga_diff
        total_rpts += xpts + xpts_diff

        # Home
        hg = safe_float(data_h.get("goals"))
        hga = safe_float(data_h.get("conceded"))
        hpts = safe_float(data_h.get("points"))
        hp = safe_float(data_h.get("played"))

        total_hg += hg
        total_hga += hga
        total_hpts += hpts
        total_hp += hp

        # Away
        ag = safe_float(data_a.get("goals"))
        aga = safe_float(data_a.get("conceded"))
        apts = safe_float(data_a.get("points"))
        ap = safe_float(data_a.get("played"))

        total_ag += ag
        total_aga += aga
        total_apts += apts
        total_ap += ap

        # Last Five
        fg = safe_float(data_f.get("goals"))
        fga = safe_float(data_f.get("conceded"))
        fpts = safe_float(data_f.get("points"))
        fp = safe_float(data_f.get("played"))

        total_fg += fg
        total_fga += fga
        total_fpts += fpts
        total_fp += fp

    return (
        total_xg / size,
        total_xga / size,
        total_xpts / size,
        total_rg / size,
        total_rga / size,
        total_rpts / size,
        total_hg / size,
        total_hga / size,
        total_hpts / size,
        total_hp / size,
        total_ag / size,
        total_aga / size,
        total_apts / size,
        total_ap / size,
        total_fg / size,
        total_fga / size,
        total_fpts / size,
        total_fp / size,
    )


async def team_fixtures(tid):
    home = await DB.lrange(f"index:fixtures:{tid}:home", -5, -1)
    away = await DB.lrange(f"index:fixtures:{tid}:away", -5, -1)
    return (home, away)


async def team_data(tid, field):
    return await DB.hget_all(f"raw_teams:{tid}:{field}")
