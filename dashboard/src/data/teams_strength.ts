/**
 * FILE: /src/data/teams_strength.ts
 * PURPOSE: Data retriever for team attributes including difficulty ratings, squad stats, and fixture coefficients.
 * USAGE: Used in /src/App.tsx to retrieve active team difficulty values and pass it to child views.
 */
import ts38 from "../../public/dummy-data/2025/38/teams/strengths.json";
import { TeamStrength } from "./types";


export const getTeamsStrength = (season: string, gw: number): TeamStrength[] => {
  console.log(`getTeamsStrength called with: season=${season}, gw=${gw}`);
  return ts38 as unknown as TeamStrength[];
};

