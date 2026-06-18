/**
 * FILE: /src/components/ProcessedView.tsx
 * PURPOSE: Advanced data visualization deck for team attack/defense ratings, clean-sheet ratios, differential player tables, and captaincy models.
 * USAGE: Selected as the "processed" view/tab in /src/App.tsx.
 */

import { useState, useMemo, useEffect } from "react";
import { motion, AnimatePresence } from "motion/react";
import { 
  TrendingUp, 
  Sparkles, 
  Search, 
  Scale, 
  Award,
  Flame,
  Home,
  Plane,
  Users,
  Percent,
  Coins,
  BadgeInfo,
  Activity,
  Shield,
  ArrowUpRight,
  ChevronLeft,
  ChevronRight
} from "lucide-react";
import { getProcTeamData } from "../data/proc_team";
import { getProcPlayerData } from "../data/proc_player";

interface ProcessedViewProps {
  selectedSeason: string;
  selectedGW: number;
}

export default function ProcessedView({ selectedSeason, selectedGW }: ProcessedViewProps) {
  const [activeSubTab, setActiveSubTab] = useState<"team" | "player">("team");
  const [searchTerm, setSearchTerm] = useState("");
  const [playerPage, setPlayerPage] = useState(1);
  const [teamPage, setTeamPage] = useState(1);
  const itemsPerPage = 6;

  // Reset pagination pages when season or GW change
  useEffect(() => {
    setPlayerPage(1);
    setTeamPage(1);
  }, [selectedSeason, selectedGW]);

  // 1. Team predictive metrics from strength.json loaded via getProcTeamData
  const processedTeams = useMemo(() => {
    const rawData = getProcTeamData(selectedSeason, selectedGW);
    if (!rawData) return [];
    
    return Object.entries(rawData).map(([teamName, metrics]) => ({
      team_name: teamName,
      expected: metrics.expected,
      real: metrics.real,
      home: metrics.home,
      away: metrics.away,
      last5: metrics.last5
    })).sort((a, b) => b.expected.point - a.expected.point);
  }, [selectedSeason, selectedGW]);

  // 2. Player predictive metrics from processed.json loaded via getProcPlayerData
  const processedPlayers = useMemo(() => {
    const rawData = getProcPlayerData(selectedSeason, selectedGW);
    if (!rawData) return [];
    
    return [...rawData].sort((a, b) => b.xpts - a.xpts);
  }, [selectedSeason, selectedGW]);

  // Search filtered lists
  const filteredTeams = useMemo(() => {
    return processedTeams.filter(t => 
      t.team_name.toLowerCase().includes(searchTerm.toLowerCase())
    );
  }, [processedTeams, searchTerm]);

  const filteredPlayers = useMemo(() => {
    return processedPlayers.filter(p => 
      p.web_name.toLowerCase().includes(searchTerm.toLowerCase()) || 
      p.team.toLowerCase().includes(searchTerm.toLowerCase()) ||
      p.position.toLowerCase().includes(searchTerm.toLowerCase())
    );
  }, [processedPlayers, searchTerm]);

  // Paginated players slice
  const paginatedPlayers = useMemo(() => {
    const start = (playerPage - 1) * itemsPerPage;
    return filteredPlayers.slice(start, start + itemsPerPage);
  }, [filteredPlayers, playerPage]);

  const totalPages = Math.ceil(filteredPlayers.length / itemsPerPage);

  // Paginated teams slice
  const paginatedTeams = useMemo(() => {
    const start = (teamPage - 1) * itemsPerPage;
    return filteredTeams.slice(start, start + itemsPerPage);
  }, [filteredTeams, teamPage]);

  const totalTeamPages = Math.ceil(filteredTeams.length / itemsPerPage);

  return (
    <div className="space-y-6">
      
      {/* HEADER SECTION */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 bg-white/[0.01] p-5 rounded-3xl border border-white/5 backdrop-blur-md">
        <div className="space-y-1">
          <h1 className="text-2xl font-bold tracking-tight text-white flex items-center gap-2 italic">
            <Scale className="text-[#00ff85] h-6 w-6 animate-pulse shrink-0" /> PROCESSED INDEXES
          </h1>
          <p className="text-white/45 text-xs max-w-xl">
            Underlying predictive models comparing teams and player metrics based on current live variance and projection math.
          </p>
        </div>

        {/* Search Input bar */}
        <div className="relative w-full md:w-64">
          <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 text-white/40 h-4 w-4" />
          <input
            id="processed-stats-search"
            type="text"
            placeholder={activeSubTab === "team" ? "Filter squads..." : "Filter players..."}
            value={searchTerm}
            onChange={(e) => {
              setSearchTerm(e.target.value);
              setPlayerPage(1);
              setTeamPage(1);
            }}
            className="w-full bg-white/5 text-white pl-10 pr-4 py-2.5 text-sm rounded-xl border border-white/5 focus:border-[#00ff85]/55 outline-none focus:ring-1 focus:ring-[#00ff85]/20 transition duration-150 placeholder:text-white/35 font-mono"
          />
        </div>
      </div>

      {/* SUB-TABS SELECTOR (Team and Player) */}
      <div className="flex gap-2.5 p-1 bg-white/5 border border-white/5 rounded-2xl w-full sm:w-fit">
        <button
          id="btn-subtab-team"
          onClick={() => {
            setActiveSubTab("team");
            setSearchTerm("");
            setPlayerPage(1);
            setTeamPage(1);
          }}
          className={`flex-1 sm:flex-initial flex items-center justify-center gap-2 px-5 py-2.5 rounded-xl text-xs font-mono font-bold uppercase tracking-wider transition-all duration-200 select-none cursor-pointer ${
            activeSubTab === "team"
              ? "bg-[#00ff85]/10 text-[#00ff85] border border-[#00ff85]/25 shadow-[0_0_15px_rgba(0,255,133,0.1)]"
              : "text-white/50 border border-transparent hover:text-white hover:bg-white/5"
          }`}
        >
          <TrendingUp className="h-4 w-4" />
          <span>Team Projections</span>
        </button>

        <button
          id="btn-subtab-player"
          onClick={() => {
            setActiveSubTab("player");
            setSearchTerm("");
            setPlayerPage(1);
            setTeamPage(1);
          }}
          className={`flex-1 sm:flex-initial flex items-center justify-center gap-2 px-5 py-2.5 rounded-xl text-xs font-mono font-bold uppercase tracking-wider transition-all duration-200 select-none cursor-pointer ${
            activeSubTab === "player"
              ? "bg-[#00ff85]/10 text-[#00ff85] border border-[#00ff85]/25 shadow-[0_0_15px_rgba(0,255,133,0.1)]"
              : "text-white/50 border border-transparent hover:text-white hover:bg-white/5"
          }`}
        >
          <Users className="h-4 w-4" />
          <span>Player Projections</span>
        </button>
      </div>

      <AnimatePresence mode="wait">
        {activeSubTab === "team" ? (
          <motion.div
            key="team-tab"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            transition={{ duration: 0.15 }}
            className="space-y-6"
          >
            {/* Note banner explaining team metrics context */}
            <div className="bg-gradient-to-r from-amber-500/10 to-transparent p-4 rounded-2xl border border-amber-500/15 flex items-start gap-3">
              <BadgeInfo className="h-5 w-5 text-amber-400 shrink-0 mt-0.5" />
              <div className="text-xs text-white/70 space-y-1">
                <span className="font-bold text-amber-300 block uppercase font-mono tracking-wider">Independent Team Baseline Metrics</span>
                <p>
                  These values denote computed absolute squad benchmark capacities (strength, split indices, home/away weights, recent 5 form bias) and are <b className="text-white">not related to or coupled with the upcoming fixture opponent</b>.
                </p>
              </div>
            </div>

            <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
              {paginatedTeams.map((team, idx) => {
                const globalIndex = (teamPage - 1) * itemsPerPage + idx + 1;
                // Calculate derived variables to make the predictions richer
                const ptsVariance = team.expected.point - team.real.point;
                const attVariance = team.expected.attack - team.real.attack;
                const defVariance = team.expected.defence - team.real.defence;

                return (
                  <div 
                    key={team.team_name} 
                    className="clay-card p-5 bg-[#141416]/95 border border-white/5 rounded-3xl space-y-5 relative overflow-hidden transition hover:scale-[1.01] duration-200"
                  >
                    {/* Rank & Team Header */}
                    <div className="flex justify-between items-start">
                      <div className="flex items-center gap-3">
                        <div className="h-8 w-8 rounded-xl bg-gradient-to-br from-emerald-500/20 to-teal-500/5 flex items-center justify-center font-bold font-mono text-xs text-[#00ff85] border border-[#00ff85]/20 shrink-0">
                          #{globalIndex}
                        </div>
                        <div>
                          <h3 className="text-base font-black text-white italic tracking-wide leading-tight">{team.team_name}</h3>
                          <span className="text-[10px] font-mono text-white/35 uppercase tracking-wider block mt-0.5">Model Projections Index</span>
                        </div>
                      </div>

                      <div className="text-right">
                        <div className="text-[10px] font-mono text-white/40 uppercase tracking-widest leading-none">Expected points Index</div>
                        <div className="text-2xl font-black text-[#00ff85] font-mono leading-none mt-1">
                          {team.expected.point.toFixed(2)}
                        </div>
                      </div>
                    </div>

                    {/* Expected Standard vs Real performance row */}
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 bg-white/[0.015] p-3.5 rounded-2xl border border-white/5">
                      {/* Expected index */}
                      <div className="space-y-2 bg-gradient-to-b from-[#00ff85]/10 to-transparent p-3 rounded-xl border border-[#00ff85]/15">
                        <span className="text-[9px] text-[#00ff85] font-mono uppercase tracking-widest block font-bold flex items-center gap-1">
                          <Activity className="h-3 w-3" /> EXPECTED RATING
                        </span>
                        <div className="space-y-1 text-xs">
                          <div className="flex justify-between items-center text-white/70">
                            <span>Points Index:</span>
                            <span className="font-mono font-semibold text-[#00ff85]">{team.expected.point.toFixed(2)}</span>
                          </div>
                          <div className="flex justify-between items-center text-white/70">
                            <span>Attack Rating:</span>
                            <span className="font-mono text-amber-400 font-semibold">{team.expected.attack.toFixed(2)}</span>
                          </div>
                          <div className="flex justify-between items-center text-white/70">
                            <span>Defence Shield:</span>
                            <span className="font-mono text-rose-400 font-semibold">{team.expected.defence.toFixed(2)}</span>
                          </div>
                        </div>
                      </div>

                      {/* Real Performance */}
                      <div className="space-y-2 bg-gradient-to-b from-indigo-500/10 to-transparent p-3 rounded-xl border border-indigo-500/15">
                        <span className="text-[9px] text-indigo-400 font-mono uppercase tracking-widest block font-bold flex items-center gap-1">
                          <Shield className="h-3 w-3" /> ACTUAL STATISTICS
                        </span>
                        <div className="space-y-1 text-xs">
                          <div className="flex justify-between items-center text-white/70">
                            <span>Actual Points:</span>
                            <span className="font-mono font-semibold text-cyan-400">{team.real.point.toFixed(2)}</span>
                          </div>
                          <div className="flex justify-between items-center text-white/70">
                            <span>Real Attack:</span>
                            <span className="font-mono text-white/80 font-medium">{team.real.attack.toFixed(2)}</span>
                          </div>
                          <div className="flex justify-between items-center text-white/70">
                            <span>Real Defence:</span>
                            <span className="font-mono text-white/80 font-medium">{team.real.defence.toFixed(2)}</span>
                          </div>
                        </div>
                      </div>
                    </div>

                    {/* Variety indices of comparison (Var values) */}
                    <div className="grid grid-cols-3 gap-2 py-2 border-y border-white/5 text-[10px] font-mono text-center">
                      <div className="p-2 bg-white/[0.01] rounded-xl border border-white/5">
                        <span className="text-white/30 text-[9px] block uppercase leading-none mb-0.5">PTS VARIANCE</span>
                        <span className={`font-black text-xs ${ptsVariance >= 0 ? 'text-[#00ff85]' : 'text-[#ff005a]'}`}>
                          {ptsVariance >= 0 ? `+${ptsVariance.toFixed(2)}` : ptsVariance.toFixed(2)}
                        </span>
                      </div>
                      <div className="p-2 bg-white/[0.01] rounded-xl border border-white/5">
                        <span className="text-white/30 text-[9px] block uppercase leading-none mb-0.5">ATT VARIANCE</span>
                        <span className={`font-black text-xs ${attVariance >= 0 ? 'text-amber-400' : 'text-[#ff005a]'}`}>
                          {attVariance >= 0 ? `+${attVariance.toFixed(2)}` : attVariance.toFixed(2)}
                        </span>
                      </div>
                      <div className="p-2 bg-white/[0.01] rounded-xl border border-white/5">
                        <span className="text-white/30 text-[9px] block uppercase leading-none mb-0.5">DEF VARIANCE</span>
                        <span className={`font-black text-xs ${defVariance <= 0 ? 'text-emerald-400' : 'text-[#ff005a]'}`}>
                          {defVariance >= 0 ? `+${defVariance.toFixed(2)}` : defVariance.toFixed(2)}
                        </span>
                      </div>
                    </div>

                    {/* Multi-tier splits split stats */}
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                      {/* Home Splits */}
                      <div className="p-3 bg-white/[0.015] rounded-xl border border-white/5 space-y-1.5">
                        <span className="text-[10px] font-bold text-[#00ff85] font-mono tracking-wider uppercase flex items-center gap-1">
                          <Home className="h-3 w-3" /> Home Splits
                        </span>
                        <div className="text-[11px] text-white/60 font-mono space-y-0.5">
                          <div className="flex justify-between">
                            <span>Points:</span>
                            <span className="text-emerald-400 font-bold">{team.home.points.toFixed(2)}</span>
                          </div>
                          <div className="flex justify-between">
                            <span>Attack:</span>
                            <span className="text-white/80">{team.home.attack.toFixed(2)}</span>
                          </div>
                          <div className="flex justify-between">
                            <span>Defence:</span>
                            <span className="text-white/80">{team.home.defence.toFixed(2)}</span>
                          </div>
                        </div>
                      </div>

                      {/* Away Splits */}
                      <div className="p-3 bg-white/[0.015] rounded-xl border border-white/5 space-y-1.5">
                        <span className="text-[10px] font-bold text-violet-400 font-mono tracking-wider uppercase flex items-center gap-1">
                          <Plane className="h-3 w-3" /> Away Splits
                        </span>
                        <div className="text-[11px] text-white/60 font-mono space-y-0.5">
                          <div className="flex justify-between">
                            <span>Points:</span>
                            <span className="text-violet-400 font-bold">{team.away.points.toFixed(2)}</span>
                          </div>
                          <div className="flex justify-between">
                            <span>Attack:</span>
                            <span className="text-white/80">{team.away.attack.toFixed(2)}</span>
                          </div>
                          <div className="flex justify-between">
                            <span>Defence:</span>
                            <span className="text-white/80">{team.away.defence.toFixed(2)}</span>
                          </div>
                        </div>
                      </div>

                      {/* Recent 5 Form */}
                      <div className="p-3 bg-white/[0.015] rounded-xl border border-white/5 space-y-1.5">
                        <span className="text-[10px] font-bold text-amber-500 font-mono tracking-wider uppercase flex items-center gap-1">
                          <Flame className="h-3 w-3" /> L5 Form Split
                        </span>
                        <div className="text-[11px] text-white/60 font-mono space-y-0.5">
                          <div className="flex justify-between">
                            <span>Points:</span>
                            <span className="text-amber-500 font-bold">{team.last5.points.toFixed(2)}</span>
                          </div>
                          <div className="flex justify-between">
                            <span>Attack:</span>
                            <span className="text-white/80">{team.last5.attack.toFixed(2)}</span>
                          </div>
                          <div className="flex justify-between">
                            <span>Defence:</span>
                            <span className="text-white/80">{team.last5.defence.toFixed(2)}</span>
                          </div>
                        </div>
                      </div>
                    </div>

                    {/* Verdict */}
                    <div className="bg-white/5 p-3 rounded-2xl border border-[#00ff85]/10 text-[11px] text-white/45 flex gap-2 font-mono leading-relaxed">
                      <span className="text-[#00ff85] font-bold shrink-0 flex items-center gap-0.5">
                        <Sparkles className="h-3 w-3 shrink-0" /> Oracle Verdict:
                      </span>
                      <span>
                        {team.team_name} expected index rating of <b className="text-white">{team.expected.point.toFixed(2)}</b> is currently {team.expected.point > team.real.point ? "under-yielding relative to on-paper superiority. Positive correction trends imminent." : "fully optimized relative to current goals metrics."}
                      </span>
                    </div>
                  </div>
                );
              })}
            </div>

            {/* Team Pagination Controls */}
            {totalTeamPages > 1 && (
              <div className="flex flex-col sm:flex-row items-center justify-between gap-4 bg-white/[0.01] p-4 rounded-2xl border border-white/5 backdrop-blur-md mt-6">
                <div className="text-xs font-mono text-white/50">
                  Showing <b className="text-[#00ff85]">{(teamPage - 1) * itemsPerPage + 1}</b> - <b className="text-[#00ff85]">{Math.min(teamPage * itemsPerPage, filteredTeams.length)}</b> of <b className="text-[#00ff85]">{filteredTeams.length}</b> teams
                </div>
                <div className="flex items-center gap-2">
                  <button
                    onClick={() => setTeamPage(p => Math.max(1, p - 1))}
                    disabled={teamPage === 1}
                    className="flex items-center justify-center h-9 w-9 rounded-xl border border-white/10 bg-white/5 text-white/70 hover:text-white hover:bg-white/10 disabled:opacity-30 disabled:pointer-events-none transition cursor-pointer select-none"
                    title="Previous Page"
                  >
                    <ChevronLeft className="h-4 w-4" />
                  </button>
                  
                  {/* Page numbers */}
                  <div className="flex items-center gap-1">
                    {Array.from({ length: totalTeamPages }, (_, i) => i + 1).map((pageNum) => {
                      if (
                        pageNum === 1 ||
                        pageNum === totalTeamPages ||
                        Math.abs(pageNum - teamPage) <= 1
                      ) {
                        return (
                          <button
                            key={pageNum}
                            onClick={() => setTeamPage(pageNum)}
                            className={`h-9 min-w-9 px-1.5 rounded-xl border font-mono text-xs font-bold transition select-none cursor-pointer ${
                              teamPage === pageNum
                                ? "bg-[#00ff85]/10 text-[#00ff85] border-[#00ff85]/30 shadow-[0_0_10px_rgba(0,255,133,0.1)]"
                                : "bg-white/5 text-white/50 border-white/10 hover:text-white hover:bg-white/10"
                            }`}
                          >
                            {pageNum}
                          </button>
                        );
                      } else if (
                        pageNum === 2 ||
                        pageNum === totalTeamPages - 1
                      ) {
                        return (
                          <span key={pageNum} className="text-white/30 px-1 font-mono text-xs select-none">
                            ...
                          </span>
                        );
                      }
                      return null;
                    })}
                  </div>

                  <button
                    onClick={() => setTeamPage(p => Math.min(totalTeamPages, p + 1))}
                    disabled={teamPage === totalTeamPages}
                    className="flex items-center justify-center h-9 w-9 rounded-xl border border-white/10 bg-white/5 text-white/70 hover:text-white hover:bg-white/10 disabled:opacity-30 disabled:pointer-events-none transition cursor-pointer select-none"
                    title="Next Page"
                  >
                    <ChevronRight className="h-4 w-4" />
                  </button>
                </div>
              </div>
            )}
          </motion.div>
        ) : (
          <motion.div
            key="player-tab"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            transition={{ duration: 0.15 }}
            className="space-y-6"
          >
            {/* Note banner explaining fixture outcome projections & player metrics */}
            <div className="bg-gradient-to-r from-teal-500/10 to-transparent p-4 rounded-2xl border border-teal-500/15 flex items-start gap-4 justify-between">
              <div className="flex items-start gap-3">
                <BadgeInfo className="h-5 w-5 text-[#00ff85] shrink-0 mt-0.5 animate-pulse" />
                <div className="text-xs text-white/70 space-y-1">
                  <span className="font-bold text-[#00ff85] block uppercase font-mono tracking-wider font-semibold">Fixture-Specific Projections</span>
                  <p>
                    Unlike General Teams, player metrics (such as expected points <b className="text-white">xPts</b> and goal involvements <b className="text-white">xGI</b>) <b className="text-[#00ff85]">are calculated specifically based on their next scheduled match</b>. The algorithm processes the difficulty, home/away advantage, and exact upcoming fixture. Go to the <b className="text-white">Players</b> view to analyze overall seasonal averages and historical statistics.
                  </p>
                </div>
              </div>
              <div className="hidden md:flex flex-col items-end shrink-0 select-none bg-white/5 px-3 py-2 rounded-xl border border-white/5 font-mono text-[10px]">
                <span className="text-white/40 block">Want seasonal averages?</span>
                <span className="text-[11px] font-bold text-teal-400 mt-0.5">Check PL Players View</span>
              </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {paginatedPlayers.map((player, idx) => {
              const xGI = player.xg + player.xa;
              const formXptsVariance = player.xpts - player.form;
              const globalIndex = (playerPage - 1) * itemsPerPage + idx + 1;

              return (
                <div 
                  key={player.id} 
                  className="clay-card p-5 bg-[#141416]/95 border border-white/5 rounded-3xl space-y-5 relative overflow-hidden transition hover:scale-[1.01] duration-200"
                >
                  {/* Subtle ambient light splash in background */}
                  <div className="absolute right-0 top-0 translate-x-12 -translate-y-12 h-24 w-24 rounded-full bg-[#00ff85]/5 filter blur-xl pointer-events-none" />

                  {/* Rank & Player Header */}
                  <div className="flex justify-between items-start">
                    <div className="flex items-center gap-3">
                      <div className="h-8 w-8 rounded-xl bg-gradient-to-br from-blue-500/20 to-violet-500/5 flex items-center justify-center font-bold font-mono text-xs text-[#00ff85] border border-[#00ff85]/20 shrink-0">
                        #{globalIndex}
                      </div>
                      <div>
                        <h3 className="text-base font-black text-white italic tracking-wide leading-tight">{player.web_name}</h3>
                        <div className="flex items-center gap-1.5 mt-1">
                          <span className="text-[10px] font-mono text-white/50">{player.team}</span>
                          <span className="text-white/20 text-[9px] font-mono leading-none">•</span>
                          <span className={`text-[9px] font-mono font-bold px-1.5 py-0.2 rounded ${
                            player.position === "FWD" ? "bg-[#ff005a]/15 text-[#ff005a]" :
                            player.position === "MID" ? "bg-cyan-500/15 text-cyan-400" :
                            player.position === "DEF" ? "bg-indigo-500/15 text-indigo-400" :
                            "bg-amber-500/15 text-amber-505"
                          }`}>
                            {player.position}
                          </span>
                        </div>
                      </div>
                    </div>

                    <div className="text-right">
                      <div className="text-[10px] font-mono text-white/40 uppercase tracking-widest leading-none">xPts Projection</div>
                      <div className="text-2xl font-black text-[#00ff85] font-mono leading-none mt-1">
                        {player.xpts.toFixed(2)}
                      </div>
                    </div>
                  </div>

                  {/* Player metrics table/grid list */}
                  <div className="grid grid-cols-4 gap-2 text-center py-2 bg-white/[0.01] border border-white/5 rounded-xl text-[11px] font-mono">
                    <div>
                      <span className="text-[9px] text-white/30 block uppercase mb-0.5">Cost</span>
                      <b className="text-white leading-none">£{player.cost.toFixed(1)}m</b>
                    </div>
                    <div>
                      <span className="text-[9px] text-white/30 block uppercase mb-0.5">Ownership</span>
                      <b className="text-white leading-none">{player.selected_by_percent}%</b>
                    </div>
                    <div>
                      <span className="text-[9px] text-white/30 block uppercase mb-0.5">Live Form</span>
                      <b className="text-amber-500 leading-none">{player.form.toFixed(1)}</b>
                    </div>
                    <div>
                      <span className="text-[9px] text-white/30 block uppercase mb-0.5">Season Pts</span>
                      <b className="text-white leading-none">{player.total_points}</b>
                    </div>
                  </div>

                  {/* Calculated metrics splits */}
                  <div className="grid grid-cols-2 gap-3">
                    {/* Attacking capabilities */}
                    <div className="bg-white/[0.015] border border-white/5 rounded-xl p-2.5 space-y-2">
                      <span className="text-[10px] text-amber-500 font-mono font-bold block flex items-center gap-1 border-b border-white/5 pb-1 select-none">
                        <Activity className="h-3 w-3 text-amber-400" /> ATTACK INDEX
                      </span>
                      <div className="text-[11px] text-white/70 font-mono space-y-1">
                        <div className="flex justify-between">
                          <span>Exp Goals (xG):</span>
                          <span className="font-bold text-amber-400">{player.xg.toFixed(2)}</span>
                        </div>
                        <div className="flex justify-between">
                          <span>Exp Assists (xA):</span>
                          <span className="font-bold text-violet-400">{player.xa.toFixed(2)}</span>
                        </div>
                        <div className="flex justify-between border-t border-white/5 pt-1 mt-1 text-[#00ff85] font-extrabold text-[12px]">
                          <span>xGI Total:</span>
                          <span>{xGI.toFixed(2)}</span>
                        </div>
                      </div>
                    </div>

                    {/* Creative indicators */}
                    <div className="bg-white/[0.015] border border-white/5 rounded-xl p-2.5 space-y-2">
                      <span className="text-[10px] text-teal-400 font-mono font-bold block flex items-center gap-1 border-b border-white/5 pb-1 select-none">
                        <BadgeInfo className="h-3 w-3 text-teal-400" /> UTILITY METRIC
                      </span>
                      <div className="text-[11px] text-white/70 font-mono space-y-1">
                        <div className="flex justify-between">
                          <span>xCleanSheet:</span>
                          <span className="font-bold text-rose-400">{player.xcleansheet.toFixed(2)}</span>
                        </div>
                        <div className="flex justify-between">
                          <span>ICT Index:</span>
                          <span className="font-bold text-sky-400">{player.ict_index.toFixed(1)}</span>
                        </div>
                        <div className="flex justify-between border-t border-white/5 pt-1 mt-1 text-emerald-400 font-extrabold text-[12px]">
                          <span>Pts per M:</span>
                          <span>{(player.total_points / player.cost).toFixed(1)}</span>
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Live predictions index metrics (variance, pts potential) */}
                  <div className="grid grid-cols-2 gap-2 text-[10px] font-mono text-center">
                    <div className="p-2 bg-white/[0.01] rounded-xl border border-white/5">
                      <span className="text-white/35 uppercase block mb-0.5 leading-none">xPTS / Price Ratio</span>
                      <div className="font-bold text-white text-xs">{(player.xpts / player.cost).toFixed(2)}</div>
                    </div>
                    <div className="p-2 bg-white/[0.01] rounded-xl border border-white/5">
                      <span className="text-white/35 uppercase block mb-0.5 leading-none">Form vs xPts Bias</span>
                      <div className={`font-bold text-xs ${formXptsVariance >= 0 ? "text-[#00ff85]" : "text-rose-455"}`}>
                        {formXptsVariance >= 0 ? `+${formXptsVariance.toFixed(2)}` : `${formXptsVariance.toFixed(2)}`}
                      </div>
                    </div>
                  </div>

                  {/* Summary Oracle Advisory */}
                  <div className="bg-white/5 p-3 rounded-2xl border border-blue-500/10 text-[11px] text-white/45 flex gap-2 font-mono leading-relaxed">
                    <span className="text-teal-400 font-bold shrink-0 flex items-center gap-0.5">
                      <ArrowUpRight className="h-3.5 w-3.5 shrink-0" /> Advice:
                    </span>
                    <span>
                      {player.web_name} shows a clinical processed xPts index of <b>{player.xpts.toFixed(2)}</b>. Model recommends {player.xpts > 7.0 ? "primary captain candidate" : "premium value pick to hold/buy"}.
                    </span>
                  </div>
                </div>
              );
            })}
            </div>

            {/* Pagination Controls */}
            {totalPages > 1 && (
              <div className="flex flex-col sm:flex-row items-center justify-between gap-4 bg-white/[0.01] p-4 rounded-2xl border border-white/5 backdrop-blur-md mt-6">
                <div className="text-xs font-mono text-white/50">
                  Showing <b className="text-[#00ff85]">{(playerPage - 1) * itemsPerPage + 1}</b> - <b className="text-[#00ff85]">{Math.min(playerPage * itemsPerPage, filteredPlayers.length)}</b> of <b className="text-[#00ff85]">{filteredPlayers.length}</b> players
                </div>
                <div className="flex items-center gap-2">
                  <button
                    onClick={() => setPlayerPage(p => Math.max(1, p - 1))}
                    disabled={playerPage === 1}
                    className="flex items-center justify-center h-9 w-9 rounded-xl border border-white/10 bg-white/5 text-white/70 hover:text-white hover:bg-white/10 disabled:opacity-30 disabled:pointer-events-none transition cursor-pointer select-none"
                    title="Previous Page"
                  >
                    <ChevronLeft className="h-4 w-4" />
                  </button>
                  
                  {/* Page numbers */}
                  <div className="flex items-center gap-1">
                    {Array.from({ length: totalPages }, (_, i) => i + 1).map((pageNum) => {
                      if (
                        pageNum === 1 ||
                        pageNum === totalPages ||
                        Math.abs(pageNum - playerPage) <= 1
                      ) {
                        return (
                          <button
                            key={pageNum}
                            onClick={() => setPlayerPage(pageNum)}
                            className={`h-9 min-w-9 px-1.5 rounded-xl border font-mono text-xs font-bold transition select-none cursor-pointer ${
                              playerPage === pageNum
                                ? "bg-[#00ff85]/10 text-[#00ff85] border-[#00ff85]/30 shadow-[0_0_10px_rgba(0,255,133,0.1)]"
                                : "bg-white/5 text-white/50 border-white/10 hover:text-white hover:bg-white/10"
                            }`}
                          >
                            {pageNum}
                          </button>
                        );
                      } else if (
                        pageNum === 2 ||
                        pageNum === totalPages - 1
                      ) {
                        return (
                          <span key={pageNum} className="text-white/30 px-1 font-mono text-xs select-none">
                            ...
                          </span>
                        );
                      }
                      return null;
                    })}
                  </div>

                  <button
                    onClick={() => setPlayerPage(p => Math.min(totalPages, p + 1))}
                    disabled={playerPage === totalPages}
                    className="flex items-center justify-center h-9 w-9 rounded-xl border border-white/10 bg-white/5 text-white/70 hover:text-white hover:bg-white/10 disabled:opacity-30 disabled:pointer-events-none transition cursor-pointer select-none"
                    title="Next Page"
                  >
                    <ChevronRight className="h-4 w-4" />
                  </button>
                </div>
              </div>
            )}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
