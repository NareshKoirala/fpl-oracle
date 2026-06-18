/**
 * FILE: /src/data/fixtures.ts
 * PURPOSE: Data retriever and mapper for game fixtures for the active Season and Gameweek.
 * USAGE: Used in /src/App.tsx to retrieve active fixture metadata and pass it to child views.
 */
import fixtures38 from "../../public/dummy-data/2025/38/fixtures/fixtures.json";
import { Fixture } from "./types";


export const getFixtures = (season: string, gw: number): Fixture[] => {
  console.log(`getFixtures called with: season=${season}, gw=${gw}`);
  return fixtures38 as unknown as Fixture[];
};

