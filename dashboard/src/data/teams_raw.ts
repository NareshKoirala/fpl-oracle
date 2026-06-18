/**
 * FILE: /src/data/teams_raw.ts
 * PURPOSE: Data retriever for raw team parameters, goals scored, conceded, and standings logs.
 * USAGE: Used in /src/App.tsx to retrieve standings data and pass it to child views.
 */
import teamsRawData from "../../public/dummy-data/2025/38/teams/raw.json";
import { TeamRaw } from "./types";


export const getTeamsRaw = (season: string, gw: number): TeamRaw[] => {
  console.log(`getTeamsRaw called with: season=${season}, gw=${gw}`);
  return teamsRawData as unknown as TeamRaw[];
};

