/**
 * FILE: /src/components/PredictionCenterCard.tsx
 * PURPOSE: Interactive configuration panel to change active FPL Oracle season and gameweek target.
 * USAGE: Placed as a top configuration header inside /src/components/DashboardView.tsx.
 */

import { useState } from "react";
import { motion, AnimatePresence } from "motion/react";
import { 
  Activity, 
  Sparkles, 
  Calendar, 
  ChevronDown, 
  Zap 
} from "lucide-react";
import { allDataStructure } from "../data/all_data_structure";

interface PredictionCenterCardProps {
  selectedSeason: string;
  selectedGW: number;
  setSelectedSeason: (season: string) => void;
  setSelectedGW: (gw: number) => void;
}

export default function PredictionCenterCard({
  selectedSeason,
  selectedGW,
  setSelectedSeason,
  setSelectedGW
}: PredictionCenterCardProps) {
  const [showSeasonDropdown, setShowSeasonDropdown] = useState(false);
  const [showGWDropdown, setShowGWDropdown] = useState(false);

  const targetSeason = allDataStructure.seasons.find(s => s.id === selectedSeason) || allDataStructure.seasons[0];

  return (
    <div className="relative z-50 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-white/[0.01] p-5 rounded-3xl border border-white/5 backdrop-blur-md">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-white flex items-center gap-2">
          <Activity className="text-[#00ff85] h-6 w-6 animate-pulse" /> FPL-Oracle Prediction Center
        </h1>
        <p className="text-white/40 text-sm mt-0.5">Statistical predictions & machine learning forecasts</p>
      </div>

      <div className="flex flex-wrap items-center gap-3">
        {/* CURRENT BUTTON */}
        <button
          id="current-gw-btn"
          onClick={() => {
            setSelectedSeason("2025");
            setSelectedGW(38);
          }}
          className="clay-btn px-4 py-2 text-sm text-[#00ff85] font-bold bg-[#00ff85]/10 border border-[#00ff85]/20 hover:bg-[#00ff85]/25 cursor-pointer flex items-center gap-1.5 transition duration-150 select-none"
        >
          <Sparkles className="h-3.5 w-3.5" />
          <span>Current</span>
        </button>

        {/* Season Selector */}
        <div className="relative">
          <button
            id="season-selector-btn"
            onClick={() => {
              setShowSeasonDropdown(!showSeasonDropdown);
              setShowGWDropdown(false);
            }}
            className="clay-btn px-4 py-2 text-sm text-neutral-200 font-medium flex items-center gap-2 bg-white/5 cursor-pointer select-none"
          >
            <Calendar className="h-4 w-4 fpl-accent" />
            <span>{selectedSeason === "2025" ? "Season 24/25" : "Season 25/26"}</span>
            <ChevronDown className={`h-4 w-4 transition-transform duration-200 ${showSeasonDropdown ? 'rotate-180' : ''}`} />
          </button>

          <AnimatePresence>
            {showSeasonDropdown && (
              <motion.div
                id="season-dropdown"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: 10 }}
                className="absolute right-0 mt-2 w-48 bg-[#141416] border border-white/5 rounded-2xl shadow-xl z-50 p-1 divide-y divide-white/5"
              >
                {allDataStructure.seasons.map((season) => (
                  <button
                    key={season.id}
                    onClick={() => {
                      setSelectedSeason(season.id);
                      setShowSeasonDropdown(false);
                    }}
                    className="w-full text-left px-3 py-2 text-sm text-white/70 hover:bg-white/5 rounded-xl transition duration-150 cursor-pointer flex justify-between items-center"
                  >
                    <span>{season.name}</span>
                    {selectedSeason === season.id && <div className="h-2 w-2 rounded-full bg-[#00ff85]" />}
                  </button>
                ))}
              </motion.div>
            )}
          </AnimatePresence>
        </div>

        {/* Gameweek Selector */}
        <div className="relative">
          <button
            id="gw-selector-btn"
            onClick={() => {
              setShowGWDropdown(!showGWDropdown);
              setShowSeasonDropdown(false);
            }}
            className="clay-btn px-4 py-2 text-sm text-neutral-200 font-medium flex items-center gap-2 bg-white/5 cursor-pointer select-none"
          >
            <Zap className="h-4 w-4 text-violet-400" />
            <span>GW {selectedGW}</span>
            <ChevronDown className={`h-4 w-4 transition-transform duration-200 ${showGWDropdown ? 'rotate-180' : ''}`} />
          </button>

          <AnimatePresence>
            {showGWDropdown && (
              <motion.div
                id="gw-dropdown"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: 10 }}
                className="absolute right-0 mt-2 w-44 bg-[#141416] border border-white/5 rounded-2xl shadow-xl z-50 p-1 max-h-64 overflow-y-auto"
              >
                <p className="text-[10px] text-white/30 font-mono px-3 py-1 font-bold">AVAILABLE WEEKS</p>
                {targetSeason.gameweeks.map((gw) => (
                  <button
                    key={gw}
                    onClick={() => {
                      setSelectedGW(gw);
                      setShowGWDropdown(false);
                    }}
                    className="w-full text-left px-3 py-2 text-sm text-white/70 hover:bg-white/5 rounded-xl transition duration-150 cursor-pointer flex justify-between items-center"
                  >
                    <span>Gameweek {gw}</span>
                    {selectedGW === gw && <div className="h-2 w-2 rounded-full bg-violet-500" />}
                  </button>
                ))}
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </div>
  );
}
