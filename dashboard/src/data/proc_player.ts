/**
 * FILE: /src/data/proc_player.ts
 * PURPOSE: Data retriever for processed players metrics, containing captaincy algorithms, differentials, and value-for-money calculations.
 * USAGE: Used in /src/components/ProcessedView.tsx to populate advanced player charts and tables.
 */

import processedPlayersData from "../../public/dummy-data/2025/38/players/processed.json";
import { PlayerProcMetrics } from "./types";

export const getProcPlayerData = (season?: string, gw?: number): PlayerProcMetrics[] => {
  console.log(`getProcPlayerData called with: season=${season}, gw=${gw}`);
  return processedPlayersData as PlayerProcMetrics[];
};
