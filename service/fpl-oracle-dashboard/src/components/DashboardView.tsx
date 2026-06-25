/**
 * FILE: /src/components/DashboardView.tsx
 * PURPOSE: Main hub screen for predictive insights, expected Team of the Week (Dream Team), and high-level KPI indicators.
 * USAGE: Selected as the "dashboard" view/tab in /src/App.tsx.
 */

import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "motion/react";
import { 
  TrendingUp, 
  Tv, 
  User, 
  Award 
} from "lucide-react";
import { allDataStructure } from "../data/all_data_structure";
import { getTeamWeek, getActualTeamOfWeek, TeamWeekPlayer } from "../data/team_week";
import { CombinedFixture, CombinedTeam } from "../data/types";
import { calculateAggregates } from "../data/fixtures";

export default function DashboardView({
  selectedSeason,
  selectedGW,
  setSelectedSeason,
  setSelectedGW,
  fixtures,
  teams
}: {
  selectedSeason: string;
  selectedGW: number;
  setSelectedSeason: (season: string) => void;
  setSelectedGW: (gw: number) => void;
  fixtures: CombinedFixture[];
  teams: CombinedTeam[];
}) {
  const [teamType, setTeamType] = useState<"projected" | "actual">("projected");

  // Retrieve season information
  const targetSeason = allDataStructure.seasons.find(s => s.id === selectedSeason) || allDataStructure.seasons[0];

  const activeFixtures = Array.isArray(fixtures) ? fixtures : [];
  const strengthList = Array.isArray(teams) ? teams : [];

  // Top 3 Attackers & Top 3 Defenders from Strength data
  const topAttackers = [...strengthList]
    .sort((a, b) => b.strength.attack_overall_expected - a.strength.attack_overall_expected)
    .slice(0, 3);

  const topDefenders = [...strengthList]
    .sort((a, b) => b.strength.defence_overall_expected - a.strength.defence_overall_expected)
    .slice(0, 3);

  // Dynamic selection from either Projected optimal squads or Actual Team of the Week datasets
  const getActiveTeamLayout = () => {
    if (teamType === "actual") return getActualTeamOfWeek(selectedSeason, selectedGW);
    return getTeamWeek(selectedSeason, selectedGW);
  };

  const activeTeam = getActiveTeamLayout();
  const pitchPlayers = activeTeam.players;
  const goalkeepers = pitchPlayers.filter(p => p.position === "GKP");
  const defenders = pitchPlayers.filter(p => p.position === "DEF");
  const midfielders = pitchPlayers.filter(p => p.position === "MID");
  const forwards = pitchPlayers.filter(p => p.position === "FWD");

  return (
    <div className="space-y-8">
      <div className="flex flex-col gap-8 w-full">
            
            {/* TOP ROW: Fixture Probabilities & Tactical Strengths Side-by-Side */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              
              {/* Fixture Probabilities Card */}
              <div className="clay-card p-6 border-white/5 flex flex-col h-[270px]">
                <div className="flex justify-between items-center mb-4">
                  <h3 className="text-base font-bold text-white flex items-center gap-2">
                    <TrendingUp className="text-teal-400 h-4.5 w-4.5" /> High-Probability Matchups
                  </h3>
                  <span className="text-[10px] font-mono bg-white/5 px-2 py-0.5 rounded text-white/50">GW {selectedGW} Models</span>
                </div>

                {/* Fixture Scroller */}
                <div className="overflow-y-auto flex-1 space-y-3 pr-1">
                  {activeFixtures.slice(0, 4).map((f) => {
                    const aggs = calculateAggregates(f);
                    const maxProb = Math.max(aggs.probHome, aggs.probDraw, aggs.probAway);
                    let predLabel = "Draw";
                    let predValue = aggs.probDraw;
                    let predColor = "text-white/60";
                    if (aggs.probHome === maxProb) {
                      predLabel = `${f.home_team.name} Win`;
                      predValue = aggs.probHome;
                      predColor = "text-[#00ff85]";
                    } else if (aggs.probAway === maxProb) {
                      predLabel = `${f.away_team.name} Win`;
                      predValue = aggs.probAway;
                      predColor = "text-pink-500";
                    }

                    return (
                      <div key={f.id} className="p-3 bg-white/[0.01] rounded-2xl border border-white/5 hover:border-white/10 transition duration-150">
                        <div className="flex justify-between text-xs font-medium text-white/70 mb-1.5">
                          <span className="truncate">{f.home_team.name} vs {f.away_team.name}</span>
                          <span className={`${predColor} font-mono font-bold`}>{predLabel} ({predValue}%)</span>
                        </div>
                        {/* Probability stacked bar */}
                        <div className="h-2 rounded-full overflow-hidden flex bg-white/5">
                          <div style={{ width: `${aggs.probHome}%` }} className="stat-bar-win h-full" title={`Home Win: ${aggs.probHome}%`} />
                          <div style={{ width: `${aggs.probDraw}%` }} className="stat-bar-draw h-full" title={`Draw: ${aggs.probDraw}%`} />
                          <div style={{ width: `${aggs.probAway}%` }} className="stat-bar-loss h-full" title={`Away Win: ${aggs.probAway}%`} />
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>

              {/* Strength Summaries Card */}
              <div className="clay-card p-6 border-white/5 flex flex-col h-[270px]">
                <div className="flex justify-between items-center mb-4">
                  <h3 className="text-base font-bold text-white flex items-center gap-2">
                    <Tv className="text-yellow-400 h-4.5 w-4.5" /> Threat & Clean Sheet Models
                  </h3>
                  <span className="text-[10px] font-mono bg-white/5 px-2 py-0.5 rounded text-[#00ff85]">Form Metric</span>
                </div>

                <div className="grid grid-cols-2 gap-4 flex-1">
                  {/* Top Attack Index */}
                  <div className="p-3.5 bg-white/[0.01] rounded-2xl border border-white/5">
                    <span className="text-[11px] font-semibold text-white/40 tracking-wider font-mono flex items-center gap-1.5 ">
                      🔥 EXPECTED ATTACK
                    </span>
                    <div className="mt-3 space-y-2">
                      {topAttackers.map((t, idx) => (
                        <div key={idx} className="flex justify-between items-center text-xs">
                          <span className="text-white/70 truncate max-w-[80px]">{t.raw.name}</span>
                          <span className="font-mono text-[#00ff85] font-bold">{t.strength.attack_overall_expected}</span>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Top Defense Index */}
                  <div className="p-3.5 bg-white/[0.01] rounded-2xl border border-white/5">
                    <span className="text-[11px] font-semibold text-white/40 tracking-wider font-mono flex items-center gap-1.5 ">
                      🛡️ EXPECTED DEFENSE
                    </span>
                    <div className="mt-3 space-y-2">
                      {topDefenders.map((t, idx) => (
                        <div key={idx} className="flex justify-between items-center text-xs">
                          <span className="text-white/70 truncate max-w-[80px]">{t.raw.name}</span>
                          <span className="font-mono text-violet-400 font-bold">{t.strength.defence_overall_expected}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>

            </div>

            {/* BOTTOM ROW: Gameweek Analytics / Optimal Squad Pitch Layout */}
            <div className="clay-card p-6 pb-4 border-white/5 w-full">
              <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6">
                <div>
                  <span className="text-xs font-mono text-[#00ff85] font-medium tracking-widest uppercase">Gameweek {selectedGW} Analytics</span>
                  <h2 className="text-xl font-bold text-white flex items-center gap-2 mt-0.5">
                    <Award className="h-5 w-5 text-violet-400" /> Optimal Squad
                  </h2>
                </div>

                {/* Pitch Mode Toggle */}
                <div className="flex bg-neutral-900/80 p-1 rounded-xl border border-white/5 text-xs font-mono self-stretch sm:self-auto">
                  <button
                    id="predict-squad-btn"
                    onClick={() => setTeamType("projected")}
                    className={`flex-1 sm:flex-initial px-3 py-1.5 rounded-lg transition-all duration-150 font-bold ${
                      teamType === "projected"
                        ? "bg-[#00ff85]/15 text-[#00ff85] border border-[#00ff85]/30"
                        : "text-white/40 hover:text-white/80 border border-transparent"
                    }`}
                  >
                    Projected Lineup
                  </button>
                  <button
                    id="totw-btn"
                    onClick={() => setTeamType("actual")}
                    className={`flex-1 sm:flex-initial px-3 py-1.5 rounded-lg transition-all duration-150 font-bold ${
                      teamType === "actual"
                        ? "bg-violet-500/15 text-violet-400 border border-violet-500/30"
                        : "text-white/40 hover:text-white/80 border border-transparent"
                    }`}
                  >
                    Team of the Week
                  </button>
                </div>

                <div className="text-left sm:text-right">
                  <span className="text-[10px] font-mono text-white/40 uppercase tracking-wider">
                    {teamType === "projected" ? "Projected Points" : "Actual Points"}
                  </span>
                  <p className="text-xl font-black text-[#00ff85] font-mono leading-none mt-1">
                    {activeTeam.total_points} PTS
                  </p>
                </div>
              </div>

              {/* Simulated Football Pitch Layout - Height increased and overflow set to visible to fix Goalkeeper and spacing cutoffs */}
              <div className="relative w-full h-[550px] sm:h-[620px] bg-gradient-to-b from-neutral-900 via-emerald-950/10 to-neutral-900 border border-white/5 rounded-3xl p-4 pt-10 pb-6 shadow-inner flex flex-col justify-between overflow-visible">
                {/* Pitch Line markings */}
                <div className="absolute inset-x-0 top-1/2 -translate-y-1/2 h-px bg-white/5 pointer-events-none" />
                <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-28 h-28 rounded-full border border-white/5 pointer-events-none" />
                <div className="absolute top-0 left-1/2 -translate-x-1/2 w-44 h-24 border-b border-x border-white/5 pointer-events-none" />
                <div className="absolute bottom-0 left-1/2 -translate-x-1/2 w-44 h-24 border-t border-x border-white/5 pointer-events-none" />

                {/* FORWARDS */}
                <div className="flex justify-around items-center w-full mt-2 z-10">
                  {forwards.map((p, idx) => (
                    <PlayerPitchNode key={idx} player={p} color="bg-[#00ff85]/10 border-[#00ff85]/40" rowSize={forwards.length} />
                  ))}
                </div>

                {/* MIDFIELDERS */}
                <div className="flex justify-around items-center w-full z-10 py-1">
                  {midfielders.map((p, idx) => (
                    <PlayerPitchNode key={idx} player={p} color="bg-cyan-500/10 border-cyan-500/40" rowSize={midfielders.length} />
                  ))}
                </div>

                {/* DEFENDERS */}
                <div className="flex justify-around items-center w-full z-10 py-1">
                  {defenders.map((p, idx) => (
                    <PlayerPitchNode key={idx} player={p} color="bg-violet-500/10 border-violet-500/40" rowSize={defenders.length} />
                  ))}
                </div>

                {/* GOALKEEPER */}
                <div className="flex justify-around items-center w-full mb-3 z-10 pb-2">
                  {goalkeepers.map((p, idx) => (
                    <PlayerPitchNode key={idx} player={p} color="bg-amber-500/10 border-amber-500/40" rowSize={goalkeepers.length} />
                  ))}
                </div>
              </div>

              <div className="flex justify-between items-center mt-6 pt-4 border-t border-white/5 text-white/40 text-xs font-mono">
                <span>Formation: <b className="text-white">{activeTeam.formation}</b></span>
                <span>Estimated Cost: <b className="text-[#00ff85]">£{activeTeam.budget}m</b></span>
              </div>
            </div>

      </div>
    </div>
  );
}

// Subordinate Node Widget for football pitch layout
function PlayerPitchNode({ player, color, rowSize = 1 }: { player: TeamWeekPlayer; color: string; rowSize?: number; key?: any }) {
  // Dynamic scaling based on count to prevent items from going out of boundaries
  const isCompactMax = rowSize >= 6;
  const isCompactMedium = rowSize >= 5;

  let circleSizes = "h-11 w-11 min-[380px]:h-12 min-[380px]:w-12 sm:h-13 sm:w-13";
  let fontSizes = "text-[8.5px] min-[380px]:text-[10.5px] sm:text-xs";
  let cardWidth = "w-[66px] min-[380px]:w-[80px] sm:w-[95px]";
  let iconSize = "h-4.5 w-4.5 sm:h-5.5 sm:w-5.5";

  if (isCompactMax) {
    circleSizes = "h-7 w-7 min-[380px]:h-8 min-[380px]:w-8 sm:h-10 sm:w-10";
    fontSizes = "text-[7.5px] min-[380px]:text-[8px] sm:text-[9.5px]";
    cardWidth = "w-[48px] min-[380px]:w-[58px] sm:w-[72px]";
    iconSize = "h-3.5 w-3.5 sm:h-4.5 sm:w-4.5";
  } else if (isCompactMedium) {
    circleSizes = "h-8.5 w-8.5 min-[380px]:h-9.5 min-[380px]:w-9.5 sm:h-11.5 sm:w-11.5";
    fontSizes = "text-[8px] min-[380px]:text-[9px] sm:text-[10.5px]";
    cardWidth = "w-[58px] min-[380px]:w-[68px] sm:w-[84px]";
    iconSize = "h-4 w-4 sm:h-5 sm:w-5";
  }

  return (
    <div className="flex flex-col items-center select-none">
      {/* Circle representation with overlay */}
      <div className={`relative ${circleSizes} rounded-full border-2 flex items-center justify-center cursor-pointer shadow-lg transition duration-200 hover:scale-110 ${color}`}>
        <User className={`${iconSize} text-white/90`} />
        {player.is_captain && (
          <span className="absolute -top-1.5 -right-1.5 bg-violet-600 text-white font-mono text-[9px] font-black h-4.5 w-4.5 sm:h-5 sm:w-5 rounded-full flex items-center justify-center border border-white/50">
            C
          </span>
        )}
        {player.is_vice_captain && (
          <span className="absolute -top-1.5 -right-1.5 bg-[#4c4c5a] text-white font-mono text-[9px] font-black h-4.5 w-4.5 sm:h-5 sm:w-5 rounded-full flex items-center justify-center border border-white/50">
            V
          </span>
        )}
      </div>
      {/* Title & metadata panel */}
      <div className={`mt-1.5 sm:mt-2 text-center bg-[#141416]/95 px-1 sm:px-2 py-0.5 sm:py-1 rounded-md border border-white/5 ${cardWidth} shadow-md`}>
        <p className={`${fontSizes} font-bold text-white truncate`}>{player.name}</p>
        <div className="flex items-center gap-1 sm:gap-1.5 justify-center mt-0.5">
          <span className="text-[8px] sm:text-[9px] font-mono text-[#00ff85] font-bold">{player.points} pts</span>
          <span className="text-[8px] sm:text-[9px] font-mono text-white/40">£{player.price}m</span>
        </div>
      </div>
    </div>
  );
}
