producer (total time takes ~73 sec, with ~29 MB data saved, ~39k keys)
    -> all teams expected (xg, xga, xgdiff, xgadiff, xpts, xptsdiff) using PlayWright and BeautifulSoup
    -> all player season stat in fpl and in season stats
    -> all previous season overall stats of all players 
    -> all teams table data with (played, wins, draw, loss, goaldiff, pts, form) using PlayWright and BeautifulSoup
    -> all teams fpl stats like strenght sep with atk, def, on home and away
    -> all players played games in current season with there in game stats

~500,000 Redis hash fields total data for teams and players to predict a high-end fpl-lineup prediction


cook
    -   teams_cook -> calculate strength for each teams
        {
            attack_overall_expected,
            defence_overall_expected
            point_overall_expected
            attack_overall_real
            defence_overall_real
            point_overall_real
            attack_home
            defence_home
            points_home
            attack_away
            defence_away
            points_away
            attack_last5
            defence_last5
            points_last5
        }

    -   fixture_cook -> calculates different variables for each fixture that gameweek with the current raw data for that week. using the strength of each teams
        {
            home
            away
            diff_h
            diff_a
            win_h
            draw
            win_a
            clean_h
            clean_a
            over_2
            under_2
            xg_h
            xg_a
        }