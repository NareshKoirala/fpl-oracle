/**
 * FILE: /src/data/fixtures.ts
 * PURPOSE: Data retriever and mapper for game fixtures for the active Season and Gameweek.
 * USAGE: Used in /src/App.tsx to retrieve active fixture metadata and pass it to child views.
 */
import fixtures38 from "../../public/dummy-data/2025/38/fixtures/fixtures.json";
import { CombinedFixture } from "./types";
import { getScorelines } from "./scorelines";
import { getGoalProbabilityHome, getGoalProbabilityAway } from "./goal_probabilities";

export const getScorelineProb = (fixture: CombinedFixture, home: number, away: number): number => {
  const key = `${home}-${away}`;
  if (fixture && fixture.scoreline && fixture.scoreline[key]) {
    return fixture.scoreline[key];
  }
  const homeFactor = (fixture?.poisson?.[home.toString()] || 15) / 100;
  const awayFactor = (fixture?.poisson?.[away.toString()] || 15) / 100;
  return parseFloat((homeFactor * awayFactor * 100).toFixed(2));
};

// Calculate derived aggregates from the scoreline matrix for a fixture
export const calculateAggregates = (f: CombinedFixture) => {
  let probHome = 0;
  let probDraw = 0;
  let probAway = 0;
  let csHome = 0;
  let csAway = 0;
  let over25 = 0;
  let maxVal = 0;
  let maxLabel = "1-1";

  const axis = [0, 1, 2, 3, 4, 5];
  axis.forEach(h => {
    axis.forEach(a => {
      const p = getScorelineProb(f, h, a);
      if (h > a) probHome += p;
      if (h === a) probDraw += p;
      if (h < a) probAway += p;
      if (a === 0) csHome += p;
      if (h === 0) csAway += p;
      if (h + a > 2.5) over25 += p;
      if (p > maxVal) {
        maxVal = p;
        maxLabel = `${h}-${a}`;
      }
    });
  });

  return {
    probHome: parseFloat(probHome.toFixed(1)),
    probDraw: parseFloat(probDraw.toFixed(1)),
    probAway: parseFloat(probAway.toFixed(1)),
    csHome: parseFloat(csHome.toFixed(1)),
    csAway: parseFloat(csAway.toFixed(1)),
    over25: parseFloat(over25.toFixed(1)),
    maxVal: parseFloat(maxVal.toFixed(1)),
    maxLabel
  };
};

/**
 * In production, this will fetch from a FastAPI endpoint that returns data
 * structured according to the Redis Two-DB Architecture (FixtureRaw, ProcFixturePoisson, etc.).
 * For now, we simulate the API returning CombinedFixture.
 */
export const getFixtures = (season: string, gw: number): CombinedFixture[] => {
  console.log(`getFixtures called with: season=${season}, gw=${gw}`);
  const scorelineMap = getScorelines(season, gw);
  const homePoissonMap = getGoalProbabilityHome(season, gw);
  const awayPoissonMap = getGoalProbabilityAway(season, gw);

  return fixtures38.map((f: any) => {
    // Generate valid scoreline probability object without percent signs
    const rawScoreline = scorelineMap[f.id.toString()] || {};
    const processedScoreline: Record<string, number> = {};
    Object.keys(rawScoreline).forEach(k => {
      processedScoreline[k] = parseFloat((rawScoreline[k] as string).replace('%', ''));
    });

    return {
      id: f.id,
      raw: {
        home_id: f.id * 10,
        away_id: f.id * 10 + 1,
        kickoff_time: "2026-05-18T14:00:00Z",
        finished: false,
        score: "0-0"
      },
      stats: {
        shots_home: 12,
        shots_away: 9,
        xG_home: f.xg_home,
        xG_away: f.xg_away,
        possession_home: 54
      },
      poisson: homePoissonMap[f.id.toString()]?.reduce((acc: any, val: number, idx: number) => {
        acc[idx.toString()] = val;
        return acc;
      }, {}) || { "0": 49.659, "1": 28.305, "2": 8.067, "3": 1.533 },
      scoreline: processedScoreline,
      home_team: {
        name: f.home_team,
        short_name: f.home_team.substring(0, 3).toUpperCase(),
        strength_overall_home: 80,
        strength_overall_away: 75
      },
      away_team: {
        name: f.away_team,
        short_name: f.away_team.substring(0, 3).toUpperCase(),
        strength_overall_home: 78,
        strength_overall_away: 73
      }
    };
  });
};


