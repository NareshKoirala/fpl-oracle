/**
 * FILE: /src/data/proc_team.ts
 * PURPOSE: Data retriever for processed team metrics, containing defensive ratings, offensive ratings, clean sheet indices, and projections.
 * USAGE: Used in /src/components/ProcessedView.tsx to populate advanced team charts and tables.
 */

import strengthData from "../../public/dummy-data/2025/38/teams/strength.json";
import { ProcTeamRecords } from "./types";

export const getProcTeamData = (season?: string, gw?: number): ProcTeamRecords => {
  console.log(`getProcTeamData called with: season=${season}, gw=${gw}`);
  return strengthData as ProcTeamRecords;
};
