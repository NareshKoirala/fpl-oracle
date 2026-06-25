/**
 * FILE: /src/data/players.ts
 * PURPOSE: Data retriever for general FPL player profiles, cost, position, and statistical summaries.
 * USAGE: Used in /src/App.tsx to retrieve active static player details.
 */
import playersData from "../../public/dummy-data/2025/38/players/players.json";
import { CombinedPlayer } from "./types";

/**
 * In production, this will fetch from a FastAPI endpoint that returns data
 * structured according to the Redis Two-DB Architecture.
 * For now, we simulate returning CombinedPlayer array.
 */
export const getPlayers = (season: string, gw: number): CombinedPlayer[] => {
  console.log(`getPlayers called with: season=${season}, gw=${gw}`);
  
  return playersData.map((p: any, index: number) => {
    return {
      id: p.id || index + 1,
      raw: {
        name: p.web_name || p.first_name + " " + p.second_name,
        team_id: p.team_code || 1,
        position: p.element_type === "FWD" ? 4 : p.element_type === "MID" ? 3 : p.element_type === "DEF" ? 2 : 1,
        cost: p.now_cost * 10,
        status: p.status || "a",
        chance_of_playing: p.chance_of_playing_this_round || 100
      },
      meta: {
        selected_by_percent: parseFloat(p.selected_by_percent) || 0,
        transfers_in: p.transfers_in || 0,
        transfers_out: p.transfers_out || 0,
        news: p.news || ""
      },
      season: {
        minutes: p.minutes || 0,
        goals: p.goals_scored || 0,
        assists: p.assists || 0,
        xG: parseFloat(p.expected_goals) || 0.0,
        xA: parseFloat(p.expected_assists) || 0.0
      },
      gw: {
        minutes: 90,
        goals: 0,
        assists: 0,
        bps: p.bps || 0,
        points: p.total_points || 0
      },
      proc: {
        xp_this_gw: parseFloat(p.ep_this) || 0,
        xp_next_gw: parseFloat(p.ep_next) || 0,
        minute_probability: 90,
        form_coefficient: parseFloat(p.form) || 0,
        fixture_difficulty: 3,
        cs_probability: 0.3,
        captain_score: 0,
        computed_at: new Date().toISOString()
      },
      team: {
        name: p.team || "Unknown",
        short_name: p.team ? p.team.substring(0, 3).toUpperCase() : "UNK",
        strength_overall_home: 1100,
        strength_overall_away: 1050
      }
    };
  });
};

