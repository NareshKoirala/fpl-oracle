# Redis Schema Definition

## 1. Overview
FPL-Oracle uses Redis as its central data store (Pantry). The database is split into two logical instances:
- **DB 0**: Raw Data (scraped straight from sources).
- **DB 1**: Processed Data (computed fields by the Cooks, prefixed with `proc_`).

All records are stored as **Redis Hashes (HASH)**. Lists or nested structures are flattened since Redis Hashes require scalar values (strings). Index keys use **Sets (SET)** for membership lookups via `SADD`.

DB routing is determined automatically: any key starting with `proc_` goes to DB 1, everything else goes to DB 0.

---

## 2. DB 0 — Raw Data Schemas

### Player Data

#### `player:{id}` — HASH (`PLAYER`)
Core identity, pricing, and current season stats.
*Source: FPL bootstrap-static API → elements[]*

| Field | Description |
|---|---|
| `id` | FPL player ID |
| `first_name`, `second_name`, `name` | Names (`name` = web_name display name) |
| `code` | FPL photo/asset code |
| `team_id` | FK → `team:{id}` (mapped from `team_code`) |
| `position` | 1=GK, 2=DEF, 3=MID, 4=FWD (element_type) |
| `status` | a=available, d=doubtful, i=injured, s=suspended, u=unavailable |
| `chance_of_playing` | % chance of playing this round |
| `news` | Injury/suspension news string |
| `cost` | now_cost ÷ 10, stored as float string e.g. `"8.5"` |
| `cost_change_start`, `cost_change_event` | Price change deltas |
| `total_points`, `points_per_game`, `form` | FPL scoring summary |
| `minutes`, `goals_scored`, `assists`, `clean_sheets` | Season totals |
| `goals_conceded`, `own_goals`, `penalties_saved`, `penalties_missed` | Season totals |
| `yellow_cards`, `red_cards`, `saves`, `bonus`, `bps`, `starts` | Season totals |
| `influence`, `creativity`, `threat`, `ict_index` | ICT Index |
| `expected_goals`, `expected_assists`, `expected_goal_involvements`, `expected_goals_conceded` | xStats season totals |
| `expected_goals_per_90`, `expected_assists_per_90`, `expected_goal_involvements_per_90`, `expected_goals_conceded_per_90` | xStats per 90 |
| `goals_conceded_per_90`, `clean_sheets_per_90`, `saves_per_90`, `starts_per_90` | Rate stats |
| `ep_this`, `ep_next` | FPL projected points this/next GW |

---

#### `player:{id}:meta` — HASH (`PLAYER_META`)
Ownership, transfers, set-piece orders, and positional ranks.
*Source: FPL bootstrap-static API → elements[]*

| Field | Description |
|---|---|
| `selected_by_percent` | % of FPL managers who own this player |
| `transfers_in`, `transfers_in_event` | Total / this-GW transfers in |
| `transfers_out`, `transfers_out_event` | Total / this-GW transfers out |
| `value_form`, `value_season` | Value metrics |
| `event_points` | Points scored in current GW |
| `in_dreamteam`, `dreamteam_count` | Dream Team flags |
| `corners_and_indirect_freekicks_order` | Set piece order (1 = first taker, "" = not a taker) |
| `direct_freekicks_order`, `penalties_order` | Set piece orders |
| `selected_rank`, `influence_rank`, `creativity_rank`, `threat_rank`, `ict_index_rank` | Within-position ranks |
| `now_cost_rank`, `form_rank`, `points_per_game_rank` | Within-position ranks |
| `*_rank_type` | Rank scope suffix fields |

---

#### `player:{id}:season:{year}` — HASH (`PLAYER_SEASON`)
Full career season totals per past year (`year` = end year, e.g. `2025` for 2024/25).
*Source: FPL player-summary API → history_past[]*

| Field | Description |
|---|---|
| `season_name` | Raw FPL label e.g. `"2024/25"` |
| `start_cost`, `end_cost` | Price at start/end of season |
| `total_points`, `minutes`, `goals_scored`, `assists` | Season totals |
| `clean_sheets`, `goals_conceded`, `own_goals` | Defensive totals |
| `penalties_saved`, `penalties_missed`, `yellow_cards`, `red_cards` | Disciplinary |
| `saves`, `bonus`, `bps`, `starts` | Misc totals |
| `influence`, `creativity`, `threat`, `ict_index` | ICT totals |
| `expected_goals`, `expected_assists`, `expected_goal_involvements`, `expected_goals_conceded` | xStats |

---

#### `player:{id}:gw:{gw}` — HASH (`PLAYER_GW`)
Per-gameweek historical performance.
*Source: FPL player-summary API → history[]*

| Field | Description |
|---|---|
| `fixture_id` | FK → `fixture:{id}` |
| `opponent_team_id` | FK → `team:{id}` |
| `was_home` | Boolean string |
| `kickoff_time` | ISO timestamp |
| `minutes`, `goals_scored`, `assists`, `clean_sheets` | GW performance |
| `goals_conceded`, `own_goals`, `penalties_saved`, `penalties_missed` | GW performance |
| `yellow_cards`, `red_cards`, `saves`, `bonus`, `bps`, `starts` | GW performance |
| `influence`, `creativity`, `threat`, `ict_index` | ICT this GW |
| `expected_goals`, `expected_assists`, `expected_goal_involvements`, `expected_goals_conceded` | xStats this GW |
| `total_points` | FPL points scored |
| `value` | Player price at that GW (raw FPL value × 10) |
| `selected`, `transfers_in`, `transfers_out`, `transfers_balance` | Ownership this GW |

---

### Team Data

#### `team:{id}` — HASH (`TEAM`)
Core team identity, FPL strength ratings, and full-season table standing.
*Source: FPL bootstrap-static API → teams[] + FotMob table*

| Field | Description |
|---|---|
| `id` | FPL team ID |
| `name` | Full name e.g. `"Manchester United"` (mapped through `FOTMOB_NAME_MAP`) |
| `short_name` | 3-char code e.g. `"MUN"` |
| `strength_overall_home`, `strength_overall_away` | FPL raw strength (1–5) |
| `strength_attack_home`, `strength_attack_away` | FPL attack strength |
| `strength_defence_home`, `strength_defence_away` | FPL defence strength |
| `position`, `played`, `wins`, `draws`, `losses` | Season table standing |
| `goals_for`, `goals_against`, `points` | Season table standing |

---

#### `team:{id}:expected` — HASH (`TEAM_EXPECTED`)
Expected stats from FotMob xG tables.
*Source: FotMob → xg_scrap()*

| Field | Description |
|---|---|
| `xG`, `xGA`, `xPts`, `xGD` | Season expected stats |
| `xG_difference`, `xGA_difference`, `xPts_difference` | Expected vs actual deltas |

---

#### `team:{id}:form` — HASH (`TEAM_FORM`)
#### `team:{id}:home` — HASH (`TEAM_HOME`)
#### `team:{id}:away` — HASH (`TEAM_AWAY`)
Last 5 matches summary, split by overall / home / away.
*Source: FotMob → form_table_scrap()*

All three share the same field set:

| Field | Description |
|---|---|
| `position`, `played`, `wins`, `draws`, `losses` | Form table standing |
| `goals_for`, `goals_against`, `points` | Form table stats |

---

### Fixtures & Events

#### `fixture:{id}` — HASH (`FIXTURE`)
Raw match data for a single fixture.
*Source: FPL fixtures API*

| Field | Description |
|---|---|
| `id` | Fixture ID |
| `gw` | Gameweek number (event) |
| `home_id`, `away_id` | FK → `team:{id}` |
| `kickoff_time` | ISO timestamp |
| `finished`, `started` | Boolean strings |
| `home_score`, `away_score` | Empty string if not yet played |

---

#### `gw:{gw}` — HASH (`GW`)
FPL gameweek metadata.
*Source: FPL bootstrap-static API → events[]*

| Field | Description |
|---|---|
| `id`, `name` | GW number and label e.g. `"Gameweek 38"` |
| `deadline_time` | ISO timestamp |
| `is_current`, `is_previous`, `is_next` | Boolean strings |
| `finished`, `data_checked` | Boolean strings |
| `highest_score` | Top manager score this GW |
| `most_selected`, `most_transferred_in`, `top_element` | Player IDs |
| `most_captained`, `most_vice_captained` | Player IDs |

---

### System & Status State

#### `status` — HASH
Combined global runtime state and current gameweek details.
*Written by: producer.py, fpl_scraper.py, and cook.py*

| Field | Description |
|---|---|
| `season` | Active season label e.g. `"2025/2026"` |
| `current_season` | End year of active season e.g. `"2026"` |
| `current` | Active gameweek number |
| `next` | Next gameweek number |
| `last` | Previous gameweek number |
| `current_in` | Deadline date for the active gameweek |
| `next_in` | Deadline date for the next gameweek |
| `last_in` | Deadline date for the previous gameweek |
| `last_fetch` | ISO timestamp of the last FPL API fetch |
| `producer_status` | `"running"` \| `"complete"` \| `"failed"` |
| `last_producer_run` | ISO timestamp of last Producer run |
| `completed` | `"True"` when the Producer has finished its run |
| `last_cook_run` | ISO timestamp of last Cook run |
| `cook_status` | `"running"` \| `"complete"` \| `"failed"` |

---

### Indexes (RAW) — SET

All index keys use `SADD` / `SMEMBERS` for O(1) membership and full-set reads.

| Key | Members | Purpose |
|---|---|---|
| `index:player_fixtures:{pid}` | fixture IDs | All fixtures a player appears in |
| `index:team_fixtures:{tid}` | fixture IDs | All fixtures a team plays in |
| `index:team_players:{tid}` | player IDs | All players on a team |
| `index:position_players:{pos}` | player IDs | All players in a position (1–4) |
| `index:season_players:{year}` | player IDs | All players active in a season |
| `index:season_fixtures:{year}` | fixture IDs | All fixtures in a season |
| `index:team:{name}` *(HASH)* | `tid` field | Reverse lookup: team name → team ID |

> **Note:** `index:team:{name}` is the only index key that is a HASH (not a SET) because it stores a single `tid` value rather than a collection.

---

## 3. DB 1 — Processed Data Schemas (`proc_`)

### Player & Team Processed

#### `proc_player:{id}:xp` — HASH (`PROC_PLAYER_XP`)
Expected Points model output per player.
*Written by: player_cook (Phase 3)*

| Field | Description |
|---|---|
| `xp_this_gw` | Predicted points for current GW |
| `xp_next_gw` | Predicted points for next GW |
| `minute_probability` | Probability of playing ≥1 minute |
| `form_coefficient` | Weighted recent form multiplier |
| `fixture_difficulty` | Difficulty rating for upcoming fixture |
| `cs_probability` | Clean sheet probability (DEF/GK) |
| `captain_score` | Captaincy value score |
| `computed_at` | ISO timestamp of last computation |

---

#### `proc_team:{id}:strength` — HASH (`PROC_TEAM_STRENGTH`)
Cooked team strength coefficients for use in the Poisson model.
*Written by: team_cook → cal_teams_strength()*

| Field | Description |
|---|---|
| `attack_overall_expected` | Attacking strength coefficient |
| `defence_overall_expected` | Defensive strength coefficient |
| `point_overall_expected` | Overall expected points coefficient |

---

### Fixture Predictions

#### `proc_fixture:{id}:poisson` — HASH (dynamic keys)
Poisson goal probability distribution per fixture.
*Written by: fixture_cook → cal_fix_xg()*

Keys are dynamic integer strings: `"0"`, `"1"`, `"2"`, `"3"`... each storing the probability of that goal count occurring.

#### `proc_fixture:{id}:scoreline` — HASH (dynamic keys)
Scoreline probability matrix per fixture.
*Written by: fixture_cook → cal_fix_xg()*

Keys are dynamic scoreline strings: `"0-0"`, `"1-0"`, `"0-1"`, `"1-1"`... each storing the probability of that exact scoreline.

---

### Managerial Output

#### `proc_gw:{gw}:team_of_week` — HASH (`PROC_GW_TEAM_OF_WEEK`)
Predicted Best XI for a gameweek. Fully flattened — all values are player IDs.
*Written by: manager cook (Phase 4)*

| Field | Description |
|---|---|
| `gk` | Goalkeeper player ID |
| `def_1` … `def_5` | Defender player IDs |
| `mid_1` … `mid_5` | Midfielder player IDs |
| `fwd_1` … `fwd_3` | Forward player IDs |
| `bench_1` … `bench_4` | Bench player IDs (in order) |
| `captain`, `vice_captain` | Captain/vice player IDs |

---

### Indexes (PROC) — SET

| Key | Members | Purpose |
|---|---|---|
| `proc:index:players` | player IDs | All players that have been processed and have an `xp` record in DB 1 |
