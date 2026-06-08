"use client";

import { useState } from "react";

const SEASONS: Record<string, number[]> = {
  "2023": Array.from({ length: 38 }, (_, i) => i + 1),
  "2024": Array.from({ length: 38 }, (_, i) => i + 1),
  "2025": [1, 2, 3],
};

export default function Home() {
  const [season, setSeason] = useState<string>("");
  const [gw, setGw] = useState<number | null>(null);

  const gameweeks = season ? SEASONS[season] : [];

  return (
    <div className="flex flex-col items-center justify-start w-full">
      {/* Header */}
      <div className="clay-card w-full max-w-3xl text-center mb-10">
        <h1 className="text-4xl font-bold tracking-tight">FPL‑Oracle Dashboard</h1>
        <p className="text-lg opacity-70 mt-2">
          Predictive analytics for Fantasy Premier League
        </p>
      </div>

      {/* Season Selector */}
      <div className="clay-card w-full max-w-3xl mb-6">
        <label className="block mb-2 font-semibold text-lg">Season</label>
        <select
          className="clay-input w-full cursor-pointer"
          value={season}
          onChange={(e) => {
            setSeason(e.target.value);
            setGw(null);
          }}
        >
          <option value="">Select a season</option>
          {Object.keys(SEASONS).map((s) => (
            <option key={s} value={s}>
              {s}
            </option>
          ))}
        </select>
      </div>

      {/* Gameweek Selector */}
      {season && (
        <div className="clay-card w-full max-w-3xl mb-6">
          <label className="block mb-2 font-semibold text-lg">Gameweek</label>
          <select
            className="clay-input w-full cursor-pointer"
            value={gw ?? ""}
            onChange={(e) => setGw(Number(e.target.value))}
          >
            <option value="">Select a gameweek</option>
            {gameweeks.map((g) => (
              <option key={g} value={g}>
                GW {g}
              </option>
            ))}
          </select>
        </div>
      )}

      {/* Selected Output */}
      {season && gw && (
        <div className="clay-card w-full max-w-3xl text-center">
          <h2 className="text-2xl font-semibold">Selection</h2>
          <p className="mt-2 text-lg">
            Season <strong>{season}</strong> — Gameweek{" "}
            <strong>{gw}</strong>
          </p>
        </div>
      )}
    </div>
  );
}
