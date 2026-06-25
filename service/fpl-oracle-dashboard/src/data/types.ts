/**
 * FILE: /src/data/types.ts
 * PURPOSE: Global type definitions, schemas, and interfaces for the entire FPL Oracle platform.
 * USAGE: Matches EXACTLY the FastApi / Redis Two-DB schema from the PDF specification.
 */

// ==========================================
// 1. FASTAPI SCHEMA (PDF COMPLIANT)
// ==========================================

// --- DB 0: RAW DATA ---

export interface PlayerRaw {
  name: string;
  team_id: number;
  position: number; // 1: GKP, 2: DEF, 3: MID, 4: FWD
  cost: number;
  status: string; // "a" (Available), "d" (Doubtful), "i" (Injured)
  chance_of_playing: number;
}

export interface PlayerMeta {
  selected_by_percent: number;
  transfers_in: number;
  transfers_out: number;
  news: string;
}

export interface PlayerSeason {
  minutes: number;
  goals_scored: number;
  assists: number;
  expected_goals: number;
  expected_assists: number;
}

export interface PlayerGw {
  minutes: number;
  goals_scored: number;
  assists: number;
  bps: number;
  total_points: number;
}

export interface PlayerFixture {
  shots: number;
  key_passes: number;
  xG: number;
  xA: number;
  touches: number;
}

export interface TeamRaw {
  name: string;
  short_name: string;
  strength_overall_home: number;
  strength_overall_away: number;
}

export interface TeamExpected {
  xG: number;
  xGA: number;
  xPts: number;
}

export interface TeamForm {
  form_string: string;
  goals_for: number;
  goals_against: number;
  points: number;
}

export interface FixtureRaw {
  home_id: number;
  away_id: number;
  kickoff_time: string; // ISO string e.g., "2026-05-18T14:00:00Z"
  finished: boolean;
  home_score: number | null;
  away_score: number | null;
}

export interface FixtureStats {
  shots_home: number;
  shots_away: number;
  xG_home: number;
  xG_away: number;
  possession_home: number;
  possession_away: number;
}

export interface GameweekRaw {
  id: number;
  name: string;
  deadline_time: string;
  is_previous: boolean;
  is_current: boolean;
  is_next: boolean;
  finished: boolean;
  data_checked: boolean;
  highest_score: number;
  most_captained: number;
  most_selected: number;
  most_transferred_in: number;
  top_element: number;
  most_vice_captained: number;
}

export interface SystemState {
  current_gw: number;
  current_season: number;
  last_producer_run: string;
  last_cook_run: string;
  producer_status: string;
  cook_status: string; // "complete", etc.
}

// --- DB 1: PROCESSED DATA ---

export interface ProcPlayerXp {
  xp_this_gw: number;
  xp_next_gw: number;
  minute_probability: number;
  form_coefficient: number;
  fixture_difficulty: number;
  cs_probability: number;
  captain_score: number;
  computed_at: string;
}

export interface ProcTeamStrength {
  attack_overall_expected: number;
  defence_overall_expected: number;
  point_overall_expected: number;
}

export interface ProcFixturePoisson {
  [goals: string]: number; // goals scored probability e.g. {"0": 49.659, "1": 28.305, ...}
}

export interface ProcFixtureScoreline {
  [scoreline: string]: number; // e.g., {"0-0": 49.659, "1-0": 6.456, ...}
}

export interface ProcTeamOfWeek {
  gk: number;
  def_1: number;
  def_2: number;
  def_3: number;
  def_4: number;
  def_5: number;
  mid_1: number;
  mid_2: number;
  mid_3: number;
  mid_4: number;
  mid_5: number;
  fwd_1: number;
  fwd_2: number;
  fwd_3: number;
  bench_1: number;
  bench_2: number;
  bench_3: number;
  bench_4: number;
  captain: number;
  vice_captain: number;
}

// ==========================================
// 2. COMBINED UI SCHEMAS
// ==========================================

export interface CombinedFixture {
  id: number;
  raw: FixtureRaw;
  stats: FixtureStats;
  poisson: ProcFixturePoisson;
  scoreline: ProcFixtureScoreline;
  home_team: TeamRaw;
  away_team: TeamRaw;
}

export interface CombinedTeam {
  id: number;
  raw: TeamRaw;
  expected: TeamExpected;
  form: TeamForm;
  strength: ProcTeamStrength;
}

export interface CombinedPlayer {
  id: number;
  raw: PlayerRaw;
  meta: PlayerMeta;
  season: PlayerSeason;
  gw: PlayerGw;
  proc: ProcPlayerXp;
  team: TeamRaw;
}

