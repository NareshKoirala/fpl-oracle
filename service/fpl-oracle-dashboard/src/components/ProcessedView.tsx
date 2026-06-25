import { useState, useMemo, useEffect } from "react";
import { motion, AnimatePresence } from "motion/react";
import { 
  TrendingUp, 
  Search, 
  Scale, 
  Users,
  BadgeInfo,
  ChevronLeft,
  ChevronRight
} from "lucide-react";
import { getPosString } from "../lib/utils";
import { PositionBadge } from "./PositionBadge";
import { CombinedTeam, CombinedPlayer } from "../data/types";

interface ProcessedViewProps {
  selectedSeason: string;
  selectedGW: number;
  players: CombinedPlayer[];
  teams: CombinedTeam[];
}

export default function ProcessedView({ selectedSeason, selectedGW, players, teams }: ProcessedViewProps) {
  const [activeSubTab, setActiveSubTab] = useState<"team" | "player">("team");
  const [searchTerm, setSearchTerm] = useState("");
  const [playerPage, setPlayerPage] = useState(1);
  const [teamPage, setTeamPage] = useState(1);
  const itemsPerPage = 8;

  // Reset pagination pages when season or GW change
  useEffect(() => {
    setPlayerPage(1);
    setTeamPage(1);
  }, [selectedSeason, selectedGW]);

  const processedTeams = Array.isArray(teams) ? teams : [];
  const processedPlayers = Array.isArray(players) ? [...players].sort((a, b) => b.proc.xp_this_gw - a.proc.xp_this_gw) : [];

  // Search filtered lists
  const filteredTeams = useMemo(() => {
    return processedTeams.filter(t => 
      t.raw.name.toLowerCase().includes(searchTerm.toLowerCase())
    );
  }, [processedTeams, searchTerm]);

  const filteredPlayers = useMemo(() => {
    return processedPlayers.filter(p => {
      const posString = getPosString(p.raw.position);
      return p.raw.name.toLowerCase().includes(searchTerm.toLowerCase()) || 
             p.team.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
             posString.toLowerCase().includes(searchTerm.toLowerCase());
    });
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

      {/* SUB-TABS SELECTOR */}
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
                  These values denote computed absolute squad benchmark capacities.
                </p>
              </div>
            </div>

            <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
              {paginatedTeams.map((team) => {
                return (
                  <div key={team.raw.name} className="clay-card border-white/5 bg-white/[0.01] p-5 flex flex-col gap-4">
                    <div className="flex justify-between items-center border-b border-white/5 pb-3">
                      <div>
                        <h2 className="text-xl font-bold text-white tracking-tight">{team.raw.name}</h2>
                        <span className="text-[10px] font-mono text-white/40 uppercase tracking-widest">{team.raw.short_name}</span>
                      </div>
                      <div className="text-right">
                        <span className="text-[10px] font-mono text-white/40 uppercase tracking-widest block">Overall Strength</span>
                        <span className="text-2xl font-black font-mono text-[#00ff85]">{Math.round((team.raw.strength_overall_home + team.raw.strength_overall_away) / 2)}</span>
                      </div>
                    </div>
                    
                    <div className="grid grid-cols-3 gap-2">
                      <div className="bg-white/5 p-3 rounded-xl border border-white/5 text-center">
                        <span className="text-[9px] text-white/40 font-mono uppercase block mb-1">Expected Pts</span>
                        <span className="font-bold text-white">{team.expected.xPts.toFixed(2)}</span>
                      </div>
                      <div className="bg-white/5 p-3 rounded-xl border border-white/5 text-center">
                        <span className="text-[9px] text-white/40 font-mono uppercase block mb-1">Expected xG</span>
                        <span className="font-bold text-amber-400">{team.expected.xG.toFixed(2)}</span>
                      </div>
                      <div className="bg-white/5 p-3 rounded-xl border border-white/5 text-center">
                        <span className="text-[9px] text-white/40 font-mono uppercase block mb-1">Expected xGA</span>
                        <span className="font-bold text-rose-400">{team.expected.xGA.toFixed(2)}</span>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>

            {totalTeamPages > 1 && (
              <div className="flex flex-col sm:flex-row items-center justify-between gap-4 bg-white/[0.01] p-4 rounded-2xl border border-white/5 backdrop-blur-md">
                <div className="text-xs font-mono text-white/50">
                  Showing <b className="text-[#00ff85]">{(teamPage - 1) * itemsPerPage + 1}</b> - <b className="text-[#00ff85]">{Math.min(teamPage * itemsPerPage, filteredTeams.length)}</b> of <b className="text-[#00ff85]">{filteredTeams.length}</b> teams
                </div>
                <div className="flex items-center gap-2">
                  <button
                    onClick={() => setTeamPage(p => Math.max(1, p - 1))}
                    disabled={teamPage === 1}
                    className="flex items-center justify-center h-9 w-9 rounded-xl border border-white/10 bg-white/5 text-white/70 hover:text-white hover:bg-white/10 disabled:opacity-30 disabled:pointer-events-none transition cursor-pointer select-none"
                  >
                    <ChevronLeft className="h-4 w-4" />
                  </button>
                  <div className="font-mono text-xs font-bold px-2">{teamPage} / {totalTeamPages}</div>
                  <button
                    onClick={() => setTeamPage(p => Math.min(totalTeamPages, p + 1))}
                    disabled={teamPage === totalTeamPages}
                    className="flex items-center justify-center h-9 w-9 rounded-xl border border-white/10 bg-white/5 text-white/70 hover:text-white hover:bg-white/10 disabled:opacity-30 disabled:pointer-events-none transition cursor-pointer select-none"
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
            <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4">
              {paginatedPlayers.map((player) => {
                return (
                  <div key={player.id} className="clay-card border-white/5 bg-white/[0.01] p-4 flex flex-col justify-between hover:bg-white/[0.03] transition group relative overflow-hidden">
                    <div className="absolute top-0 right-0 w-24 h-24 bg-[#00ff85]/5 rounded-bl-full blur-2xl group-hover:bg-[#00ff85]/10 transition"></div>
                    
                    <div>
                      <div className="flex justify-between items-start mb-3 relative z-10">
                        <PositionBadge position={player.raw.position} className="px-2" />
                      </div>
                      
                      <h3 className="text-base font-bold text-white truncate relative z-10">{player.raw.name}</h3>
                      <div className="text-xs text-white/50 mt-0.5 font-mono relative z-10">{player.team.name}</div>
                    </div>

                    <div className="mt-4 pt-3 border-t border-white/5 flex justify-between items-end relative z-10">
                      <div>
                        <span className="text-[9px] font-mono text-white/40 uppercase block">Expected Pts</span>
                        <span className="text-xl font-black text-[#00ff85] font-mono">{player.proc.xp_this_gw.toFixed(2)}</span>
                      </div>
                      <div className="text-right">
                        <span className="text-[9px] font-mono text-white/40 uppercase block">Cost</span>
                        <span className="text-xs font-bold text-white/80 font-mono">£{(player.raw.cost / 10).toFixed(1)}m</span>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>

            {totalPages > 1 && (
              <div className="flex flex-col sm:flex-row items-center justify-between gap-4 bg-white/[0.01] p-4 rounded-2xl border border-white/5 backdrop-blur-md">
                <div className="text-xs font-mono text-white/50">
                  Showing <b className="text-[#00ff85]">{(playerPage - 1) * itemsPerPage + 1}</b> - <b className="text-[#00ff85]">{Math.min(playerPage * itemsPerPage, filteredPlayers.length)}</b> of <b className="text-[#00ff85]">{filteredPlayers.length}</b> players
                </div>
                <div className="flex items-center gap-2">
                  <button
                    onClick={() => setPlayerPage(p => Math.max(1, p - 1))}
                    disabled={playerPage === 1}
                    className="flex items-center justify-center h-9 w-9 rounded-xl border border-white/10 bg-white/5 text-white/70 hover:text-white hover:bg-white/10 disabled:opacity-30 disabled:pointer-events-none transition cursor-pointer select-none"
                  >
                    <ChevronLeft className="h-4 w-4" />
                  </button>
                  <div className="font-mono text-xs font-bold px-2">{playerPage} / {totalPages}</div>
                  <button
                    onClick={() => setPlayerPage(p => Math.min(totalPages, p + 1))}
                    disabled={playerPage === totalPages}
                    className="flex items-center justify-center h-9 w-9 rounded-xl border border-white/10 bg-white/5 text-white/70 hover:text-white hover:bg-white/10 disabled:opacity-30 disabled:pointer-events-none transition cursor-pointer select-none"
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
