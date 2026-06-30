/**
 * FILE: /src/data/teams_raw.ts
 * PURPOSE: Data retriever for raw team parameters, goals scored, conceded, and standings logs.
 * USAGE: Used in /src/App.tsx to retrieve standings data and pass it to child views.
 */
import teamsRawData from "../dummy-data/2025/38/teams/raw.json";
import { CombinedTeam } from "./types";
import { getTeamsStrength } from "./teams_strength";

/**
 * In production, this will fetch from a FastAPI endpoint that returns data
 * structured according to the Redis Two-DB Architecture.
 * For now, we simulate returning CombinedTeam array.
 */
export const getTeamsRaw = (season: string, gw: number): CombinedTeam[] => {
  console.log(`getTeamsRaw called with: season=${season}, gw=${gw}`);
  
  return teamsRawData.map((t: any, index: number) => {
    return {
      id: index + 1,
      raw: {
        name: t.team_name,
        short_name: t.team_name.substring(0, 3).toUpperCase(),
        strength_overall_home: 80,
        strength_overall_away: 75
      },
      expected: {
        xG: t.xg || 1.5,
        xGA: t.xga || 1.2,
        xPts: t.xpts || 1.4
      },
      form: {
        form_string: t.form?.join("") || "WWDLW",
        goals_for: t.goals_scored || 55,
        goals_against: t.goals_conceded || 45,
        points: t.points || 55
      },
      strength: {
        attack_overall_expected: 1.12,
        defence_overall_expected: 0.94,
        point_overall_expected: 1.18
      }
    };
  });
};

