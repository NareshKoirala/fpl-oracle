/**
 * FILE: /src/data/goal_probabilities.ts
 * PURPOSE: Data retriever and getter proxies for goal probability scales for teams.
 * USAGE: Used in /src/components/FixturesView.tsx to retrieve probability weights for goals (0 to 3) from the Redis DB 1 processed keyspace.
 */
import gphData from "../dummy-data/2025/38/fixtures/gph.json";
import gpaData from "../dummy-data/2025/38/fixtures/gpa.json";

export const goalProbabilityHome = new Proxy(gphData as Record<string, number[]>, {
  get: (target, prop) => {
    if (typeof prop === "string") {
      if (prop in target) return target[prop];
      const id = parseInt(prop);
      if (!isNaN(id)) {
        const fallbackKey = (((id - 1) % 10) + 1).toString();
        return target[fallbackKey] || [20, 30, 25, 15, 7, 3];
      }
    }
    return target[prop as keyof typeof target];
  }
});

export const goalProbabilityAway = new Proxy(gpaData as Record<string, number[]>, {
  get: (target, prop) => {
    if (typeof prop === "string") {
      if (prop in target) return target[prop];
      const id = parseInt(prop);
      if (!isNaN(id)) {
        const fallbackKey = (((id - 1) % 10) + 1).toString();
        return target[fallbackKey] || [25, 35, 25, 10, 4, 1];
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
export const getGoalProbabilityHome = (season: string, gw: number): Record<string, number[]> => {
  console.log(`getGoalProbabilityHome called with: season=${season}, gw=${gw}`);
  return goalProbabilityHome;
};

export const getGoalProbabilityAway = (season: string, gw: number): Record<string, number[]> => {
  console.log(`getGoalProbabilityAway called with: season=${season}, gw=${gw}`);
  return goalProbabilityAway;
};


