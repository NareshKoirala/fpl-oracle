/**
 * FILE: /src/data/players.ts
 * PURPOSE: Data retriever for general FPL player profiles, cost, position, and statistical summaries.
 * USAGE: Used in /src/App.tsx to retrieve active static player details.
 */
import playersData from "../../public/dummy-data/2025/38/players/players.json";
import { Player } from "./types";


export const getPlayers = (season: string, gw: number): Player[] => {
  console.log(`getPlayers called with: season=${season}, gw=${gw}`);
  return playersData as unknown as Player[];
};

