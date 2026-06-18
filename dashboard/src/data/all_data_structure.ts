/**
 * STATIC DATA: Season and Gameweek structural configuration.
 * Used in:
 * - src/App.tsx: To coordinate active season and gameweek selections, adjusting dropdown options.
 * - src/components/DashboardView.tsx: To obtain general metadata and helper information for selected seasons.
 * - src/components/PredictionCenterCard.tsx: To retrieve available seasons to execute predictions on.
 */
export const allDataStructure = {
  seasons: [
    { id: "2025", name: "Season 2025", gameweeks: [38, 37, 36], current_gameweek: 38 },
    { id: "2024", name: "Season 2024", gameweeks: [10, 9, 8], current_gameweek: 10 }
  ]
};

export const getAllDataStructure = (season: string, gw: number) => {
  console.log(`getAllDataStructure: season=${season}, gw=${gw}`);
  return allDataStructure;
};

