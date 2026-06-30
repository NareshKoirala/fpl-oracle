/**
 * FILE: /src/data/scorelines.ts
 * PURPOSE: Data retriever and proxy layer for precise scoreline probability distributions.
 * USAGE: Used in /src/components/FixturesView.tsx to populate the predicted outcome matrix of potential scorelines (e.g. "1-1", "2-1").
 */
import scorelinesData from "../dummy-data/2025/38/fixtures/scoreline.json";

export const scorelines = new Proxy(scorelinesData as Record<string, Record<string, string>>, {
  get: (target, prop) => {
    if (typeof prop === "string") {
      if (prop in target) return target[prop];
      const id = parseInt(prop);
      if (!isNaN(id)) {
        const fallbackKey = (((id - 1) % 10) + 1).toString();
        return target[fallbackKey] || {};
      }
    }
    return target[prop as keyof typeof target];
  }
});

/**
 * In production, this will fetch from a FastAPI endpoint that returns data
 * structured according to the Redis Two-DB Architecture.
 * For now, we map the dummy JSON directly.
 */
export const getScorelines = (season: string, gw: number): Record<string, Record<string, string>> => {
  console.log(`getScorelines called with: season=${season}, gw=${gw}`);
  return scorelines;
};


