/**
 * FILE: /src/data/team_week.ts
 * PURPOSE: Data retriever and builder for FPL Projected and Actual Team of the Weeks (Dream Teams).
 * USAGE: Used in /src/components/DashboardView.tsx to render the pitch grid, players, prices, and FPL score cards.
 */
import teamWeekData from "../../public/dummy-data/2025/38/teams/week.json";
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

const teamWeek: Record<number, TeamWeek> = {
  1: teamWeekData as unknown as TeamWeek,
};

const actualTeamOfWeek: Record<number, TeamWeek> = {
  1: {
    gw: 38,
    formation: "3-6-1",
    total_points: 142,
    budget: 68.5,
    players: [
      { name: "Hermansen", team: "Leicester", position: "GKP", price: 4.5, points: 7, expected_points: 5.5, is_captain: false, is_vice_captain: false },
      { name: "Dorgu", team: "Lecce", position: "DEF", price: 4.5, points: 18, expected_points: 6.0, is_captain: true, is_vice_captain: false },
      { name: "Diop", team: "Fulham", position: "DEF", price: 4.0, points: 15, expected_points: 4.0, is_captain: false, is_vice_captain: false },
      { name: "Pedro Porro", team: "Tottenham", position: "DEF", price: 5.5, points: 10, expected_points: 5.5, is_captain: false, is_vice_captain: false },
      { name: "B.Fernandes", team: "Man United", position: "MID", price: 8.5, points: 14, expected_points: 7.0, is_captain: false, is_vice_captain: false },
      { name: "J.Palhinha", team: "Bayern", position: "MID", price: 5.5, points: 12, expected_points: 4.5, is_captain: false, is_vice_captain: false },
      { name: "Bowen", team: "West Ham", position: "MID", price: 7.5, points: 12, expected_points: 6.5, is_captain: false, is_vice_captain: false },
      { name: "Madueke", team: "Chelsea", position: "MID", price: 6.5, points: 11, expected_points: 5.0, is_captain: false, is_vice_captain: false },
      { name: "C.Jones", team: "Liverpool", position: "MID", price: 5.5, points: 10, expected_points: 4.5, is_captain: false, is_vice_captain: false },
      { name: "Tavernier", team: "Bournemouth", position: "MID", price: 5.5, points: 10, expected_points: 4.5, is_captain: false, is_vice_captain: false },
      { name: "Watkins", team: "Aston Villa", position: "FWD", price: 9.0, points: 13, expected_points: 8.0, is_captain: false, is_vice_captain: true }
    ]
  }
};

/**
 * In production, this will fetch from a FastAPI endpoint that returns data
 * structured according to the Redis Two-DB Architecture.
 * For now, we map the dummy JSON directly.
 */
export const getTeamWeek = (season: string, gw: number): TeamWeek => {
  console.log(`getTeamWeek called with: season=${season}, gw=${gw}`);
  return teamWeekData as unknown as TeamWeek;
};

// TODO: Replace with real FastAPI call when the backend is ready. Currently returns hardcoded dummy data.
export const getActualTeamOfWeek = (season: string, gw: number): TeamWeek => {
  console.log(`getActualTeamOfWeek called with: season=${season}, gw=${gw}`);
  return actualTeamOfWeek[1];
};


