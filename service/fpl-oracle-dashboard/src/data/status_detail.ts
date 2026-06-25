/**
 * FILE: /src/data/status_detail.ts
 * PURPOSE: Local data provider for FPL Oracle database sync histories, timers, and scheduled tasks.
 * USAGE: Used in /src/App.tsx and /src/components/OracleStatusCard.tsx to present syncing statuses from Redis keys.
 */
export const statusDetail = {
  next_fetch: "2026-06-11 18:08:11",
  last_fetch: "2026-06-10 18:08:11",
  current_gw: "38",
  current_gw_in: "2026-05-24 18:08:11",
  current_gw_end: "2026-05-27 18:08:11"
};

/**
 * In production, this will fetch from a FastAPI endpoint that returns data
 * structured according to the Redis Two-DB Architecture.
 * For now, we map the dummy JSON directly.
 */
export const getStatusDetail = (season: string, gw: number) => {
  console.log(`getStatusDetail called with: season=${season}, gw=${gw}`);
  return statusDetail;
};


