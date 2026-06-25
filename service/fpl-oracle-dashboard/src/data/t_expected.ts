/**
 * FILE: /src/data/t_expected.ts
 * PURPOSE: Data retriever for expected (xG based) coefficients, expected goals scored/conceded, and expected points for teams.
 * USAGE: Used in /src/components/StandingsView.tsx to render the Simulated expected league standings from Redis keys.
 */
import tExpectedData from "../../public/dummy-data/2025/38/teams/expected.json";

/**
 * In production, this will fetch from a FastAPI endpoint that returns data
 * structured according to the Redis Two-DB Architecture.
 * For now, we map the dummy JSON directly.
 */
export const getTExpected = (season: string, gw: number) => {
  console.log(`getTExpected called with: season=${season}, gw=${gw}`);
  return tExpectedData;
};



