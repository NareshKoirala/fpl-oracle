/**
 * FILE: /src/data/t_expected.ts
 * PURPOSE: Data retriever for expected (xG based) coefficients, expected goals scored/conceded, and expected points for teams.
 * USAGE: Used in /src/components/StandingsView.tsx to render the Simulated expected league standings.
 */
import tExpectedData from "../../public/dummy-data/2025/38/teams/expected.json";


export const getTExpected = (season: string, gw: number) => {
  console.log(`getTExpected called with: season=${season}, gw=${gw}`);
  return tExpectedData;
};


