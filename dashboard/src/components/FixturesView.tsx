/**
 * FILE: /src/components/FixturesView.tsx
 * PURPOSE: Renders fixture list, win/draw/loss probabilities, clean sheet odds, over 2.5 projection, and a scoreline heatmap.
 * USAGE: Selected as the "fixtures" view/tab in /src/App.tsx.
 */

import { useState } from "react";
import { motion, AnimatePresence } from "motion/react";
import { 
  TrendingUp, 
  ChevronRight, 
  Flame, 
  Grid, 
  Clock, 
  Percent, 
  BadgeHelp,
  Calculator,
  ShieldCheck,
  Eye,
  Info,
  X,
  Award
} from "lucide-react";
import { getGoalProbabilityHome, getGoalProbabilityAway } from "../data/goal_probabilities";
import { getScorelines } from "../data/scorelines";
import { Fixture } from "../data/types";

interface FixturesViewProps {
  selectedSeason: string;
  selectedGW: number;
  fixtures: Fixture[];
}

export default function FixturesView({ selectedSeason, selectedGW, fixtures }: FixturesViewProps) {
  const [selectedFixtureId, setSelectedFixtureId] = useState<number | null>(1); // default selection
  const [isMobileFixtureOpen, setIsMobileFixtureOpen] = useState(false);
  
  const activeFixtures = Array.isArray(fixtures) ? fixtures : [];

  const selectedFixture = activeFixtures.find(f => f.id === selectedFixtureId) || activeFixtures[0];

  // Load specific probabilities vectors (6 values representing 0, 1, 2, 3, 4, 5+ goals)
  const gphRaw = getGoalProbabilityHome(selectedSeason, selectedGW)[selectedFixture.id.toString()] || [20, 30, 25, 15, 7, 3];
  const gpaRaw = getGoalProbabilityAway(selectedSeason, selectedGW)[selectedFixture.id.toString()] || [25, 35, 25, 10, 4, 1];

  // Retrieve scorelines heatmap stats
  const scorelineMap = getScorelines(selectedSeason, selectedGW)[selectedFixture.id.toString()] || {};

  // Formulate a proper 0-5 list
  const goalsAxis = [0, 1, 2, 3, 4, 5];

  // Get scoreline likelihood or calculate estimated fallback
  const getScorelineProb = (home: number, away: number): number => {
    const key = `${home}-${away}`;
    if (scorelineMap[key]) {
      return parseFloat(scorelineMap[key]);
    }
    // Simple mock calculation fallback
    const homeFactor = gphRaw[home] / 100;
    const awayFactor = gpaRaw[away] / 100;
    return parseFloat((homeFactor * awayFactor * 100).toFixed(2));
  };

  // Find the single highest probability scoreline
  let maxScorelineLabel = "1-1";
  let maxScorelineVal = 0;
  goalsAxis.forEach(h => {
    goalsAxis.forEach(a => {
      const prob = getScorelineProb(h, a);
      if (prob > maxScorelineVal) {
        maxScorelineVal = prob;
        maxScorelineLabel = `${h}-${a}`;
      }
    });
  });

  const renderFixtureDetailContent = () => {
    if (!selectedFixture) {
      return (
        <div className="clay-card p-8 border-white/5 bg-[#141416] text-center text-white/30 font-mono text-xs">
          Select a fixture matchup to begin simulation
        </div>
      );
    }

    return (
      <div className="clay-card p-6 border-white/5 relative overflow-hidden text-left">
        {/* Subtle accent glow */}
        <div className="absolute top-0 right-0 w-48 h-48 bg-[#00ff85]/5 rounded-full blur-3xl pointer-events-none" />

        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 pb-4 border-b border-white/5 mb-6">
          <div>
            <span className="text-[10px] font-mono text-[#00ff85] tracking-wider uppercase font-bold">Predictive Analytics Panel</span>
            <h1 className="text-2xl font-black text-white mt-0.5">
              {selectedFixture.home_team} vs {selectedFixture.away_team}
            </h1>
          </div>
          <div className="py-1 px-3 bg-white/5 rounded-lg border border-white/5 text-xs font-mono text-white/50 flex items-center gap-1.5 shadow">
            <Calculator className="h-3.5 w-3.5 text-violet-400" /> Over 2.5 Goals: <b className="text-white">{selectedFixture.over_2_5}%</b>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          
          {/* Probability Bars & Clean Sheet Odds */}
          <div className="space-y-6">
            <div>
              <h3 className="text-xs font-mono font-bold text-white/40 uppercase tracking-widest mb-3.5">
                🏆 WIN / DRAW / LOSE OUTCOMES
              </h3>
              <div className="space-y-3.5">
                {/* Home Win */}
                <div>
                  <div className="flex justify-between text-xs text-white/80 font-medium mb-1.5">
                    <span>{selectedFixture.home_team} Win</span>
                    <span className="font-mono text-[#00ff85] font-bold">{selectedFixture.prob_home_win}%</span>
                  </div>
                  <div className="h-2 bg-white/5 rounded-full overflow-hidden">
                    <div style={{ width: `${selectedFixture.prob_home_win}%` }} className="h-full bg-[#00ff85]" />
                  </div>
                </div>

                {/* Draw */}
                <div>
                  <div className="flex justify-between text-xs text-white/80 font-medium mb-1.5">
                    <span>Strategic Draw</span>
                    <span className="font-mono text-[#7c7c8a] font-bold">{selectedFixture.prob_draw}%</span>
                  </div>
                  <div className="h-2 bg-white/5 rounded-full overflow-hidden">
                    <div style={{ width: `${selectedFixture.prob_draw}%` }} className="h-full bg-[#7c7c8a]" />
                  </div>
                </div>

                {/* Away Win */}
                <div>
                  <div className="flex justify-between text-xs text-white/80 font-medium mb-1.5">
                    <span>{selectedFixture.away_team} Win</span>
                    <span className="font-mono text-[#ff005a] font-bold">{selectedFixture.prob_away_win}%</span>
                  </div>
                  <div className="h-2 bg-white/5 rounded-full overflow-hidden">
                    <div style={{ width: `${selectedFixture.prob_away_win}%` }} className="h-full bg-[#ff005a]" />
                  </div>
                </div>
              </div>
            </div>

            {/* Clean Sheet and expected goals */}
            <div className="grid grid-cols-2 gap-4 pt-2">
              <div className="p-3.5 bg-white/[0.01] rounded-2xl border border-white/5">
                <span className="text-[9px] text-[#00ff85] block uppercase font-mono tracking-widest leading-normal">CS Odds: {selectedFixture.home_team}</span>
                <span className="text-lg font-black text-white font-mono">{selectedFixture.cs_odds_home}%</span>
                <p className="text-[10px] text-white/30 mt-1 font-mono">xG: {selectedFixture.xg_home}</p>
              </div>

              <div className="p-3.5 bg-white/[0.01] rounded-2xl border border-white/5">
                <span className="text-[9px] text-[#ff005a] block uppercase font-mono tracking-widest leading-normal">CS Odds: {selectedFixture.away_team}</span>
                <span className="text-lg font-black text-white font-mono">{selectedFixture.cs_odds_away}%</span>
                <p className="text-[10px] text-white/30 mt-1 font-mono">xG: {selectedFixture.xg_away}</p>
              </div>
            </div>

            {/* Model Summary card */}
            <div className="bg-white/5 p-4 rounded-2xl border border-white/5 flex gap-3 text-xs text-white/50">
              <Info className="h-5 w-5 text-[#00ff85] shrink-0" />
              <div>
                Our probability matrices suggest the most expected scoreline for this game is <b>{maxScorelineLabel}</b>, carrying an estimated chance profile of <b>{maxScorelineVal}%</b>.
              </div>
            </div>
          </div>

          {/* Scoreline Probability Matrix Heatmap */}
          <div>
            <div className="flex justify-between items-center mb-3">
              <h3 className="text-xs font-mono font-bold text-white/40 uppercase tracking-widest">
                📊 SCORELINE PROBABILITY MATRIX
              </h3>
            </div>

            {/* Heatmap Grid */}
            <div className="p-4 bg-white/[0.01] rounded-2xl border border-white/5 space-y-3">
              
              {/* Visual grid layout */}
              <div className="relative">
                {/* Away Goals Title on top */}
                <div className="text-[9px] font-mono font-bold text-center text-white/40 mb-1.5 uppercase letter tracking-widest">
                  Away Goals ({selectedFixture.away_team}) →
                </div>

                <div className="flex">
                  {/* Home Goals title on Y-axis */}
                  <div className="text-[9px] font-mono font-bold text-white/40 [writing-mode:vertical-lr] rotate-180 mr-2 flex justify-center uppercase tracking-widest">
                    ← Home Goals ({selectedFixture.home_team})
                  </div>

                  <div className="grid grid-cols-6 gap-1 w-full flex-1">
                    {goalsAxis.map((homeGoals) => (
                      goalsAxis.map((awayGoals) => {
                        const val = getScorelineProb(homeGoals, awayGoals);
                        
                        // Determine background opacity based on probability value
                        // Cap values for aesthetic shading differences (0% - 15%)
                        const brightnessPercent = Math.min(val * 7.5, 90) / 100;

                        return (
                          <div
                            key={`${homeGoals}-${awayGoals}`}
                            style={{ 
                              background: `rgba(0, 255, 133, ${brightnessPercent})`,
                            }}
                            className="aspect-square rounded-md flex flex-col items-center justify-center transition duration-150 group relative border border-white/[0.03]"
                          >
                            <span className="text-[9px] font-mono font-medium text-white/95">
                              {val > 0.5 ? `${Math.round(val)}%` : '-'}
                            </span>

                            {/* Tooltip on hovering cell */}
                            <div className="absolute opacity-0 group-hover:opacity-100 bg-[#141416] text-white text-[10px] py-1 px-2 rounded border border-white/10 pointer-events-none transition duration-150 z-50 shadow-xl font-mono -top-9 left-1/2 -translate-x-1/2 whitespace-nowrap">
                              Score {homeGoals}-{awayGoals}: <b className="text-[#00ff85]">{val}%</b>
                            </div>
                          </div>
                        )
                      })
                    ))}
                  </div>
                </div>

                {/* Axis helper indices */}
                <div className="flex ml-6 mt-1 text-[8px] font-mono text-white/30 justify-around">
                  <span>A:0</span>
                  <span>1</span>
                  <span>2</span>
                  <span>3</span>
                  <span>4</span>
                  <span>5+</span>
                </div>
              </div>

            </div>
          </div>

        </div>
      </div>
    );
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
      
      {/* LEFT COLUMN: Fixtures List */}
      <div className="col-span-12 lg:col-span-4 space-y-4">
        <div className="bg-white/[0.01] p-5 rounded-3xl border border-white/5 backdrop-blur-md">
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <Clock className="text-[#00ff85] h-5 w-5" /> GW{selectedGW} Fixtures List
          </h2>
          <p className="text-white/40 text-xs mt-0.5">Click any matchup for predictive simulations</p>
        </div>

        <div className="space-y-3 max-h-[600px] overflow-y-auto pr-2">
          {activeFixtures.map((f) => {
            const isSelected = f.id === selectedFixtureId;
            return (
              <button
                key={f.id}
                id={`fixture-card-${f.id}`}
                onClick={() => {
                  setSelectedFixtureId(f.id);
                  setIsMobileFixtureOpen(true);
                }}
                className={`w-full text-left p-4 rounded-2xl border transition duration-250 cursor-pointer flex justify-between items-center ${
                  isSelected 
                    ? 'bg-[#00ff85]/10 border-[#00ff85]/30 shadow-md shadow-[#00ff85]/[0.05]' 
                    : 'bg-[#141416]/45 border-white/5 hover:bg-white/[0.02] hover:border-white/10'
                }`}
              >
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <span className="text-sm font-semibold text-white">{f.home_team}</span>
                    <span className="text-[10px] text-white/30 font-mono">v</span>
                    <span className="text-sm font-semibold text-white">{f.away_team}</span>
                  </div>
                  <div className="flex items-center gap-3 text-[10px] text-white/40 font-mono">
                    <span>H-Win: {f.prob_home_win}%</span>
                    <span>•</span>
                    <span>A-Win: {f.prob_away_win}%</span>
                  </div>
                </div>
                <ChevronRight className={`h-4 w-4 transition-transform ${isSelected ? 'translate-x-1 text-[#00ff85]' : 'text-white/30'}`} />
              </button>
            );
          })}
        </div>
      </div>

      {/* RIGHT COLUMN: Active Simulation & Heatmap - HIDDEN ON MOBILE */}
      <div className="hidden lg:block lg:col-span-8 space-y-6">
        {selectedFixture ? renderFixtureDetailContent() : (
          <div className="clay-card p-12 border-white/5 bg-[#141416] text-center text-white/30 font-mono text-xs">
            Select a fixture matchup to begin simulation
          </div>
        )}
      </div>

      {/* MOBILE SIMULATION OVERLAY DIALOG */}
      <AnimatePresence>
        {isMobileFixtureOpen && selectedFixture && (
          <div className="fixed inset-0 z-50 lg:hidden flex items-end sm:items-center justify-center p-4">
            {/* Backdrop */}
            <motion.div 
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setIsMobileFixtureOpen(false)}
              className="absolute inset-0 bg-black/80 backdrop-blur-sm"
              style={{ contentVisibility: "auto" }}
            />
            
            {/* Drawer/Modal content */}
            <motion.div
              initial={{ opacity: 0, y: 100 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: 100 }}
              transition={{ type: "spring", damping: 25, stiffness: 350 }}
              className="relative w-full max-w-4xl bg-[#141416] rounded-t-3xl sm:rounded-3xl border border-white/10 shadow-2xl overflow-hidden max-h-[85vh] flex flex-col z-10"
            >
              {/* Header with Close */}
              <div className="flex justify-between items-center px-6 py-4 border-b border-white/5 bg-white/[0.01]">
                <div className="flex items-center gap-2">
                  <Award className="h-4.5 w-4.5 text-[#00ff85] animate-pulse" />
                  <span className="text-xs font-mono text-[#00ff85] tracking-widest uppercase font-bold">Match Simulation Insights</span>
                </div>
                <button 
                  onClick={() => setIsMobileFixtureOpen(false)}
                  className="p-1.5 rounded-lg bg-white/5 border border-white/5 text-white/50 hover:text-white hover:bg-white/10 transition"
                >
                  <X className="h-4 w-4" />
                </button>
              </div>

              {/* Scrollable content */}
              <div className="overflow-y-auto p-6 space-y-6 flex-1 scrollbar-none">
                {renderFixtureDetailContent()}
              </div>
            </motion.div>
          </div>
        )}
      </AnimatePresence>

    </div>
  );
}
