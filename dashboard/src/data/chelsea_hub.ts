/**
 * FILE: /src/data/chelsea_hub.ts
 * PURPOSE: Data retriever and mapper for Chelsea-specific news and fixtures.
 * USAGE: Used in /src/components/ChelseaHubCard.tsx to present specific fixture cards.
 */

import chelseaHubData from "../../public/dummy-data/chelsea_hub.json";

export interface ChelseaHubFixture {
  gw: string;
  opponent: string;
  date: string;
  isLiveOrHighlighted: boolean;
  location: "H" | "A";
}

export interface ChelseaHubData {
  title: string;
  subtitle: string;
  quote: string;
  fixtures: ChelseaHubFixture[];
}

export const getChelseaHubData = (season?: string, gw?: number): ChelseaHubData => {
  console.log(`getChelseaHubData called${season ? ` with: season=${season}` : ""}${gw ? `, gw=${gw}` : ""}`);
  return chelseaHubData as ChelseaHubData;
};
