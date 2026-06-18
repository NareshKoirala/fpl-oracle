/**
 * FILE: /src/data/types.ts
 * PURPOSE: Global type definitions, schemas, and interfaces for the entire FPL Oracle platform.
 * USAGE: Shared and imported across almost all views, providers, and component files inside the application.
 */
export interface Fixture {
  id: number;
  home_team: string;
  away_team: string;
  prob_home_win: number;
  prob_draw: number;
  prob_away_win: number;
  cs_odds_home: number;
  cs_odds_away: number;
  xg_home: number;
  xg_away: number;
  over_2_5: number;
  season: string;
  gameweek: number;
}

export interface TeamRaw {
  team_name: string;
  played: number;
  wins: number;
  draws: number;
  losses: number;
  goals_scored: number;
  goals_conceded: number;
  points: number;
  xg: number;
  xga: number;
  xpts: number;
  shots_per_game: number;
  shots_conceded_per_game: number;
  big_chances_created: number;
  big_chances_conceded: number;
  possession: number;
  pass_accuracy: number;
  set_piece_goals: number;
  form: string[];
}

export interface TeamStrength {
  team_name: string;
  overall_strength: number;
  attack_strength_home: number;
  attack_strength_away: number;
  defense_strength_home: number;
  defense_strength_away: number;
  expected_points_home: number;
  expected_points_away: number;
  real_points_per_game: number;
  expected_points_per_game: number;
  expected_attack_index: number;
  expected_defense_index: number;
  real_attack_index: number;
  real_defense_index: number;
  last_5_form: string[];
}

export interface Player {
  id: number;
  first_name: string;
  second_name: string;
  web_name: string;
  team: string;
  element_type: string; // GKP, DEF, MID, FWD
  status: string; // a, d, i
  now_cost: number;
  selected_by_percent: string;
  form: string;
  total_points: number;
  goals_scored: number;
  assists: number;
  clean_sheets: number;
  goals_conceded: number;
  own_goals: number;
  penalties_saved: number;
  penalties_missed: number;
  yellow_cards: number;
  red_cards: number;
  saves: number;
  bonus: number;
  bps: number;
  influence: string;
  creativity: string;
  threat: string;
  ict_index: string;
  influence_per_90: string;
  creativity_per_90: string;
  threat_per_90: string;
  ict_index_per_90: string;
  expected_goals: string;
  expected_assists: string;
  expected_goal_involvements: string;
  expected_goals_conceded: string;
  expected_goals_per_90: string;
  expected_assists_per_90: string;
  expected_goal_involvements_per_90: string;
  expected_goals_conceded_per_90: string;
  ict_rank: number;
  influence_rank: number;
  creativity_rank: number;
  threat_rank: number;
  set_pieces: {
    penalties_order: number | null;
    freekicks_order: number | null;
    corners_order: number | null;
  };
}

export interface TeamWeekPlayer {
  name: string;
  team: string;
  position: string;
  price: number;
  points: number;
  expected_points: number;
  is_captain: boolean;
  is_vice_captain: boolean;
}

export interface TeamWeek {
  gw: number;
  formation: string;
  total_points: number;
  budget: number;
  players: TeamWeekPlayer[];
}

export interface TeamProcMetrics {
  expected: {
    attack: number;
    defence: number;
    point: number;
  };
  real: {
    attack: number;
    defence: number;
    point: number;
  };
  home: {
    attack: number;
    defence: number;
    points: number;
  };
  away: {
    attack: number;
    defence: number;
    points: number;
  };
  last5: {
    attack: number;
    defence: number;
    points: number;
  };
}

export type ProcTeamRecords = Record<string, TeamProcMetrics>;

export interface PlayerProcMetrics {
  id: number;
  web_name: string;
  team: string;
  position: string;
  cost: number;
  xpts: number;
  xg: number;
  xa: number;
  xcleansheet: number;
  ict_index: number;
  selected_by_percent: number;
  total_points: number;
  form: number;
}

