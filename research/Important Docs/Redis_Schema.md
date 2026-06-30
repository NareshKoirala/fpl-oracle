# Redis Schema Definition

## 1. Overview
FPL-Oracle uses Redis as its central data store (Pantry). The database is split into two logical instances:
- **DB 0**: Raw Data (scraped straight from sources).
- **DB 1**: Processed Data (computed fields by the Cooks, prefixed with `proc_`).

All records are stored as **Redis Hashes (HASH)**. Lists or nested structures are flattened since Redis Hashes require scalar values (strings).

---

## 2. DB 0 — Raw Data Schemas

### Player Data
- **`player:{id}`**
  - Core identity, status, pricing, and current season stats (goals, xG, minutes).
  - *Source: FPL bootstrap-static API.*
- **`player:{id}:meta`**
  - Ownership stats, transfer data, set-piece orders, and positional ranks.
  - *Source: FPL bootstrap-static API.*
- **`player:{id}:season:{year}`**
  - Full career season totals for previous years.
  - *Source: FPL player-summary API.*
- **`player:{id}:gw:{gw}`**
  - Per-gameweek historical performance, opponent data, and points.
  - *Source: FPL player-summary API.*

### Team Data
- **`team:{id}`**
  - Core team details, FPL strength ratings, and current season table standings.
  - *Source: FPL API & FotMob.*
- **`team:{id}:expected`**
  - Expected stats for the team (xG, xGA, xPts, xGD) used for strength coefficient calculations.
  - *Source: FotMob xG tables.*
- **`team:{id}:form`**, **`team:{id}:home`**, **`team:{id}:away`**
  - Last 5 matches summary (played, wins, goals for/against) split by overall, home, and away.
  - *Source: FotMob form tables.*

### Fixtures & Events
- **`fixture:{id}`**
  - Specific match data (gameweek, home team, away team, kickoff time, score).
  - *Source: FPL fixtures API.*
- **`gw:{gw}`**
  - Gameweek metadata (deadline time, highest score, most captained player).
  - *Source: FPL bootstrap-static API.*

### System State
- **`system:state`**
  - Global runtime state tracking the current gameweek, season, and the timestamp/status of Producer and Cook runs.

### Indexes (RAW)
- **`index:player_fixtures`** (Sorted Set): Maps players to their fixtures (e.g. `ZADD index:player_fixtures:302 38 373`).
- **`index:team_fixtures`** (Sorted Set): Maps teams to their fixtures (e.g. `ZADD index:team_fixtures:13 38 373`).
- **`index:team_name`**: Maps team name to ID (e.g. `index:team_name:Manchester United` -> `tid: 13`).
- **`index:team_players`**: Maps team to players (e.g. `index:team_players:13 = {302, 415, 188}`).
- **`index:position_players`**: Maps position to players (e.g. `index:position_players:3 = {302, 415}`).
- **`index:season_players`**: Maps season to players (e.g. `index:season_players:2025 = {302, 430, 147}`).
- **`index:season_fixtures`**: Maps season to fixtures (e.g. `index:season_fixtures:2025 = {373, 374, 375}`).

### Raw Dumps (RAW)
- **`raw:fpl:`**: Raw JSON dump from FPL API.
- **`raw:fotmob:`**: Raw JSON dump from FotMob API.

---

## 3. DB 1 — Processed Data Schemas (`proc_`)

### Player & Team Processed
- **`proc_player:{id}:xp`**
  - The Expected Points (xP) model output. Contains `xp_this_gw`, `minute_probability`, `form_coefficient`, and `fixture_difficulty`.
  - *Written by: Analytical Cooks.*
- **`proc_team:{id}:strength`**
  - Computed team attack and defence strength coefficients.

### Fixture Predictions
- **`proc_fixture:{id}:poisson`**
  - Poisson goal probability distribution per fixture (dynamic keys: "0", "1", "2"...).
- **`proc_fixture:{id}:scoreline`**
  - Scoreline probability matrix per fixture (dynamic keys: "0-0", "1-0"...).

### Managerial Output
- **`proc_gw:{gw}:team_of_week`**
  - Predicted Best XI for a gameweek. Flattened schema tracking starting XI positions (gk, def_1... fwd_3), bench order, captain, and vice_captain.

### Indexes (PROC)
- **`proc:index:players`** (SET): Set of processed players (e.g. `proc:index:players = {302, 415, 188}`).
