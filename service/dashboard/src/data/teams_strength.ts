/**
 * FILE: /src/data/teams_strength.ts
 * PURPOSE: Data retriever for team attributes including difficulty ratings, squad stats, and fixture coefficients.
 * USAGE: Used in /src/App.tsx to retrieve active team difficulty values and pass it to child views.
 */
import ts38 from "../dummy-data/2025/38/teams/strengths.json";
import { ProcTeamStrength } from "./types";

/**
 * In production, this will fetch from a FastAPI endpoint that returns data
 * structured according to the Redis Two-DB Architecture.
 * For now, we map the dummy JSON directly.
 */
export const getTeamsStrength = (season: string, gw: number): ProcTeamStrength[] => {
  console.log(`getTeamsStrength called with: season=${season}, gw=${gw}`);
  return ts38 as unknown as ProcTeamStrength[];
};

