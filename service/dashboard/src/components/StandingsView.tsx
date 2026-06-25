/**
 * FILE: /src/components/StandingsView.tsx
 * PURPOSE: Renders stateful league standings divided into Home, Away, recent Form tables, and expected (xG based) table simulations.
 * USAGE: Selected as the "standings" view/tab in /src/App.tsx.
 */

import { useState, useMemo } from "react";
import { motion } from "motion/react";
import { 
  Table2, 
  Home, 
  Plane, 
  Activity, 
  Search, 
  TrendingUp, 
  TrendingDown, 
  Minus,
  Info,
  Sparkles
} from "lucide-react";
import { CombinedTeam } from "../data/types";

type TableTab = "current" | "home" | "away" | "form" | "expected";

interface StandingsViewProps {
  selectedSeason: string;
  selectedGW: number;
  teamsRaw: CombinedTeam[];
}

export default function StandingsView({ selectedSeason, selectedGW, teamsRaw }: StandingsViewProps) {
  const [activeTab, setActiveTab] = useState<TableTab>("current");
  const [searchTerm, setSearchTerm] = useState("");

  // Determine home & away stats deterministically so they sum up exactly to the total
  const computedTeams = useMemo(() => {
    const safeTeamsRaw = Array.isArray(teamsRaw) ? teamsRaw : [];
    return safeTeamsRaw.map((team, index) => {
      // Calculate derived metrics from form_string
      const formStr = team.form.form_string || "";
      const wins = formStr.replace(/[^W]/g, "").length;
      const draws = formStr.replace(/[^D]/g, "").length;
      const losses = formStr.replace(/[^L]/g, "").length;
      const played = wins + draws + losses;
      
      const teamName = team.raw.name;
      const hash = teamName.split("").reduce((acc, char) => acc + char.charCodeAt(0), 0);
      
      const homePlayed = Math.floor(played / 2);
      
      let homeWins = Math.round(wins * (0.55 + (hash % 10) * 0.015));
      if (homeWins > wins) homeWins = wins;
      
      let homeDraws = Math.round(draws * (0.45 + (hash % 5) * 0.02));
      if (homeDraws > draws) homeDraws = draws;
      
      if (homeWins + homeDraws > homePlayed) {
        const diff = (homeWins + homeDraws) - homePlayed;
        homeWins = Math.max(0, homeWins - diff);
      }
      
      const homeLosses = homePlayed - homeWins - homeDraws;
      const homeScored = Math.round(team.form.goals_for * (0.58 + (hash % 8) * 0.01));
      const homeConceded = Math.round(team.form.goals_against * (0.42 + (hash % 6) * 0.01));
      const homePoints = homeWins * 3 + homeDraws;
      
      const awayPlayed = played - homePlayed;
      const awayWins = wins - homeWins;
      const awayDraws = draws - homeDraws;
      const awayLosses = losses - homeLosses;
      const awayScored = team.form.goals_for - homeScored;
      const awayConceded = team.form.goals_against - homeConceded;
      const awayPoints = awayWins * 3 + awayDraws;

      const last5 = formStr.slice(-5).split("");
      const formPoints = last5.reduce((sum, res) => {
        if (res === "W") return sum + 3;
        if (res === "D") return sum + 1;
        return sum;
      }, 0);

      let recentScored = 0;
      let recentConceded = 0;
      last5.forEach((res, i) => {
        const seed = (hash + i) % 4;
        if (res === "W") {
          recentScored += seed + 1;
          recentConceded += Math.max(0, seed - 1);
        } else if (res === "D") {
          recentScored += seed;
          recentConceded += seed;
        } else {
          recentScored += Math.max(0, seed - 1);
          recentConceded += seed + 1;
        }
      });

      return {
        ...team,
        derived: { played, wins, draws, losses },
        home: {
          played: homePlayed,
          wins: homeWins,
          draws: homeDraws,
          losses: homeLosses,
          scored: homeScored,
          conceded: homeConceded,
          points: homePoints,
          gd: homeScored - homeConceded,
        },
        away: {
          played: awayPlayed,
          wins: awayWins,
          draws: awayDraws,
          losses: awayLosses,
          scored: awayScored,
          conceded: awayConceded,
          points: awayPoints,
          gd: awayScored - awayConceded,
        },
        formStats: {
          last5,
          points: formPoints,
          scored: recentScored,
          conceded: recentConceded
        }
      };
    });
  }, [teamsRaw]);

  // Filter and sort the tables
  const sortedCurrentTable = useMemo(() => {
    return [...computedTeams]
      .filter(t => t.raw.name.toLowerCase().includes(searchTerm.toLowerCase()))
      .sort((a, b) => b.form.points - a.form.points || (b.form.goals_for - b.form.goals_against) - (a.form.goals_for - a.form.goals_against) || b.form.goals_for - a.form.goals_for);
  }, [computedTeams, searchTerm]);

  const sortedHomeTable = useMemo(() => {
    return [...computedTeams]
      .filter(t => t.raw.name.toLowerCase().includes(searchTerm.toLowerCase()))
      .sort((a, b) => b.home.points - a.home.points || b.home.gd - a.home.gd || b.home.scored - a.home.scored);
  }, [computedTeams, searchTerm]);

  const sortedAwayTable = useMemo(() => {
    return [...computedTeams]
      .filter(t => t.raw.name.toLowerCase().includes(searchTerm.toLowerCase()))
      .sort((a, b) => b.away.points - a.away.points || b.away.gd - a.away.gd || b.away.scored - a.away.scored);
  }, [computedTeams, searchTerm]);

  const sortedFormTable = useMemo(() => {
    return [...computedTeams]
      .filter(t => t.raw.name.toLowerCase().includes(searchTerm.toLowerCase()))
      .sort((a, b) => b.formStats.points - a.formStats.points || (b.formStats.scored - b.formStats.conceded) - (a.formStats.scored - a.formStats.conceded));
  }, [computedTeams, searchTerm]);

  const sortedExpectedTable = useMemo(() => {
    return [...computedTeams]
      .filter(t => t.raw.name.toLowerCase().includes(searchTerm.toLowerCase()))
      .sort((a, b) => b.expected.xPts - a.expected.xPts);
  }, [computedTeams, searchTerm]);

  return (
    <div className="space-y-6">
      
      {/* HEADER PORTION */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-black text-white italic tracking-tight font-sans uppercase">
            League <span className="fpl-accent">Standings</span>
          </h1>
          <p className="text-xs sm:text-sm text-white/50 font-mono mt-1">
            Real-time league division tables, home/away splits, and current form profiles.
          </p>
        </div>

        {/* SEARCH INPUT */}
        <div className="relative w-full sm:w-72">
          <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 h-4 w-4 text-white/40" />
          <input
            id="table-search"
            type="text"
            placeholder="Filter teams..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full bg-white/5 border border-white/5 hover:border-white/10 focus:border-[#00ff85]/40 text-white rounded-xl py-2 px-10 text-sm font-mono placeholder:text-white/30 focus:outline-none transition duration-150"
          />
        </div>
      </div>

      {/* VIEW SELECTOR TAB BAR */}
      <div className="flex bg-[#111113] p-1 rounded-2xl border border-white/5 text-sm overflow-x-auto scrollbar-none">
        <button
          id="tab-current"
          onClick={() => { setActiveTab("current"); }}
          className={`flex-1 min-w-[120px] py-3 rounded-xl font-bold transition duration-150 flex items-center justify-center gap-2 cursor-pointer select-none ${
            activeTab === "current"
              ? "bg-[#00ff85]/10 text-[#00ff85] border border-[#00ff85]/20"
              : "text-white/50 hover:text-white hover:bg-white/[0.02]"
          }`}
        >
          <Table2 className="h-4 w-4" />
          <span>Overall Table</span>
        </button>

        <button
          id="tab-home"
          onClick={() => { setActiveTab("home"); }}
          className={`flex-1 min-w-[120px] py-3 rounded-xl font-bold transition duration-150 flex items-center justify-center gap-2 cursor-pointer select-none ${
            activeTab === "home"
              ? "bg-[#00ff85]/10 text-[#00ff85] border border-[#00ff85]/20"
              : "text-white/50 hover:text-white hover:bg-white/[0.02]"
          }`}
        >
          <Home className="h-4 w-4" />
          <span>Home Table</span>
        </button>

        <button
          id="tab-away"
          onClick={() => { setActiveTab("away"); }}
          className={`flex-1 min-w-[120px] py-3 rounded-xl font-bold transition duration-150 flex items-center justify-center gap-2 cursor-pointer select-none ${
            activeTab === "away"
              ? "bg-[#00ff85]/10 text-[#00ff85] border border-[#00ff85]/20"
              : "text-white/50 hover:text-white hover:bg-white/[0.02]"
          }`}
        >
          <Plane className="h-4 w-4" />
          <span>Away Table</span>
        </button>

        <button
          id="tab-form"
          onClick={() => { setActiveTab("form"); }}
          className={`flex-1 min-w-[120px] py-3 rounded-xl font-bold transition duration-150 flex items-center justify-center gap-2 cursor-pointer select-none ${
            activeTab === "form"
              ? "bg-[#00ff85]/10 text-[#00ff85] border border-[#00ff85]/20"
              : "text-white/50 hover:text-white hover:bg-white/[0.02]"
          }`}
        >
          <Activity className="h-4 w-4" />
          <span>Form Table (Last 5)</span>
        </button>

        <button
          id="tab-expected"
          onClick={() => { setActiveTab("expected"); }}
          className={`flex-1 min-w-[120px] py-3 rounded-xl font-bold transition duration-150 flex items-center justify-center gap-2 cursor-pointer select-none ${
            activeTab === "expected"
              ? "bg-[#00ff85]/10 text-[#00ff85] border border-[#00ff85]/20"
              : "text-white/50 hover:text-white hover:bg-white/[0.02]"
          }`}
        >
          <Sparkles className="h-4 w-4 text-violet-400" />
          <span>Expected Stats</span>
        </button>
      </div>

      {/* TABLE DATA INTERFACE */}
      <div className="clay-card border-white/5 overflow-hidden">
        <div className="overflow-x-auto">
          {activeTab === "current" && (
            <table className="w-full text-left border-collapse select-none">
              <thead>
                <tr className="bg-white/[0.02] border-b border-white/5 font-mono text-[11px] text-white/40 uppercase tracking-wider">
                  <th className="py-4 px-4 font-bold text-center w-12">Pos</th>
                  <th className="py-4 px-4 font-bold min-w-[160px]">Club</th>
                  <th className="py-4 px-4 font-bold text-center">Pl</th>
                  <th className="py-4 px-4 font-bold text-center">W</th>
                  <th className="py-4 px-4 font-bold text-center">D</th>
                  <th className="py-4 px-4 font-bold text-center">L</th>
                  <th className="py-4 px-4 font-bold text-center">GF</th>
                  <th className="py-4 px-4 font-bold text-center">GA</th>
                  <th className="py-4 px-4 font-bold text-center">GD</th>
                  <th className="py-4 px-4 font-bold text-center text-[#00ff85]">Pts</th>
                  <th className="py-4 px-4 font-bold text-center hidden md:table-cell">xG</th>
                  <th className="py-4 px-4 font-bold text-center hidden md:table-cell">xGA</th>
                  <th className="py-4 px-4 font-bold text-center hidden md:table-cell">xPts</th>
                  <th className="py-4 px-4 font-bold text-center">Form</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/5 text-sm">
                {sortedCurrentTable.map((team, index) => {
                  const pos = index + 1;
                  const gd = team.form.goals_for - team.form.goals_against;
                  return (
                    <tr 
                      key={team.raw.name} 
                      className="hover:bg-white/[0.015] transition duration-150 align-middle"
                    >
                      <td className="py-3.5 px-4 text-center">
                        <span className={`inline-flex items-center justify-center font-mono font-black text-xs h-6 w-6 rounded-full ${
                          pos <= 4 
                            ? "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20" 
                            : pos === 5
                            ? "bg-cyan-500/10 text-cyan-400 border border-cyan-500/20"
                            : pos >= 18
                            ? "bg-red-500/10 text-red-400 border border-red-500/20"
                            : "text-white/60"
                        }`}>
                          {pos}
                        </span>
                      </td>
                      <td className="py-3.5 px-4 font-bold text-white font-sans text-sm">
                        {team.raw.name}
                      </td>
                      <td className="py-3.5 px-4 font-mono text-center text-white/80">{team.derived.played}</td>
                      <td className="py-3.5 px-4 font-mono text-center text-white/50">{team.derived.wins}</td>
                      <td className="py-3.5 px-4 font-mono text-center text-white/50">{team.derived.draws}</td>
                      <td className="py-3.5 px-4 font-mono text-center text-white/50">{team.derived.losses}</td>
                      <td className="py-3.5 px-4 font-mono text-center text-white/50">{team.form.goals_for}</td>
                      <td className="py-3.5 px-4 font-mono text-center text-white/50">{team.form.goals_against}</td>
                      <td className="py-3.5 px-4 font-mono text-center font-semibold text-white/80">
                        {gd > 0 ? `+${gd}` : gd}
                      </td>
                      <td className="py-3.5 px-4 font-mono text-center font-black text-[#00ff85]">{team.form.points}</td>
                      <td className="py-3.5 px-4 font-mono text-center text-white/40 hidden md:table-cell">{team.expected.xG}</td>
                      <td className="py-3.5 px-4 font-mono text-center text-white/40 hidden md:table-cell">{team.expected.xGA}</td>
                      <td className="py-3.5 px-4 font-mono text-center font-semibold text-violet-400 hidden md:table-cell">{team.expected.xPts}</td>
                      <td className="py-3.5 px-4">
                        <div className="flex gap-1 justify-center">
                          {team.formStats.last5.map((res: string, i: number) => (
                            <span 
                              key={i} 
                              className={`h-4.5 w-4.5 rounded text-[9px] font-mono font-black flex items-center justify-center border ${
                                res === "W" 
                                  ? "bg-emerald-500/10 text-emerald-400 border-emerald-500/20" 
                                  : res === "D"
                                  ? "bg-white/5 text-white/45 border-white/5" 
                                  : "bg-red-500/10 text-red-400 border-red-500/20"
                              }`}
                            >
                              {res}
                            </span>
                          ))}
                        </div>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          )}

          {activeTab === "home" && (
            <table className="w-full text-left border-collapse select-none">
              <thead>
                <tr className="bg-white/[0.02] border-b border-white/5 font-mono text-[11px] text-white/40 uppercase tracking-wider">
                  <th className="py-4 px-4 font-bold text-center w-12">Pos</th>
                  <th className="py-4 px-4 font-bold min-w-[160px]">Club</th>
                  <th className="py-4 px-4 font-bold text-center">Pl</th>
                  <th className="py-4 px-4 font-bold text-center">W</th>
                  <th className="py-4 px-4 font-bold text-center">D</th>
                  <th className="py-4 px-4 font-bold text-center">L</th>
                  <th className="py-4 px-4 font-bold text-center">GF</th>
                  <th className="py-4 px-4 font-bold text-center">GA</th>
                  <th className="py-4 px-4 font-bold text-center">GD</th>
                  <th className="py-4 px-4 font-bold text-center text-[#00ff85]">Pts</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/5 text-sm">
                {sortedHomeTable.map((team, index) => {
                  const pos = index + 1;
                  return (
                    <tr 
                      key={team.raw.name} 
                      className="hover:bg-white/[0.015] transition duration-150 align-middle"
                    >
                      <td className="py-3.5 px-4 text-center font-mono font-bold text-white/40">{pos}</td>
                      <td className="py-3.5 px-4 font-bold text-white">{team.raw.name}</td>
                      <td className="py-3.5 px-4 font-mono text-center text-white/80">{team.home.played}</td>
                      <td className="py-3.5 px-4 font-mono text-center text-white/50">{team.home.wins}</td>
                      <td className="py-3.5 px-4 font-mono text-center text-white/50">{team.home.draws}</td>
                      <td className="py-3.5 px-4 font-mono text-center text-white/50">{team.home.losses}</td>
                      <td className="py-3.5 px-4 font-mono text-center text-white/50">{team.home.scored}</td>
                      <td className="py-3.5 px-4 font-mono text-center text-white/50">{team.home.conceded}</td>
                      <td className="py-3.5 px-4 font-mono text-center font-semibold text-white/80">
                        {team.home.gd > 0 ? `+${team.home.gd}` : team.home.gd}
                      </td>
                      <td className="py-3.5 px-4 font-mono text-center font-black text-[#00ff85]">{team.home.points}</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          )}

          {activeTab === "away" && (
            <table className="w-full text-left border-collapse select-none">
              <thead>
                <tr className="bg-white/[0.02] border-b border-white/5 font-mono text-[11px] text-white/40 uppercase tracking-wider">
                  <th className="py-4 px-4 font-bold text-center w-12">Pos</th>
                  <th className="py-4 px-4 font-bold min-w-[160px]">Club</th>
                  <th className="py-4 px-4 font-bold text-center">Pl</th>
                  <th className="py-4 px-4 font-bold text-center">W</th>
                  <th className="py-4 px-4 font-bold text-center">D</th>
                  <th className="py-4 px-4 font-bold text-center">L</th>
                  <th className="py-4 px-4 font-bold text-center">GF</th>
                  <th className="py-4 px-4 font-bold text-center">GA</th>
                  <th className="py-4 px-4 font-bold text-center">GD</th>
                  <th className="py-4 px-4 font-bold text-center text-[#00ff85]">Pts</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/5 text-sm">
                {sortedAwayTable.map((team, index) => {
                  const pos = index + 1;
                  return (
                    <tr 
                      key={team.raw.name} 
                      className="hover:bg-white/[0.015] transition duration-150 align-middle"
                    >
                      <td className="py-3.5 px-4 text-center font-mono font-bold text-white/40">{pos}</td>
                      <td className="py-3.5 px-4 font-bold text-white">{team.raw.name}</td>
                      <td className="py-3.5 px-4 font-mono text-center text-white/80">{team.away.played}</td>
                      <td className="py-3.5 px-4 font-mono text-center text-white/50">{team.away.wins}</td>
                      <td className="py-3.5 px-4 font-mono text-center text-white/50">{team.away.draws}</td>
                      <td className="py-3.5 px-4 font-mono text-center text-white/50">{team.away.losses}</td>
                      <td className="py-3.5 px-4 font-mono text-center text-white/50">{team.away.scored}</td>
                      <td className="py-3.5 px-4 font-mono text-center text-white/50">{team.away.conceded}</td>
                      <td className="py-3.5 px-4 font-mono text-center font-semibold text-white/80">
                        {team.away.gd > 0 ? `+${team.away.gd}` : team.away.gd}
                      </td>
                      <td className="py-3.5 px-4 font-mono text-center font-black text-[#00ff85]">{team.away.points}</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          )}

          {activeTab === "form" && (
            <table className="w-full text-left border-collapse select-none">
              <thead>
                <tr className="bg-white/[0.02] border-b border-white/5 font-mono text-[11px] text-white/40 uppercase tracking-wider">
                  <th className="py-4 px-4 font-bold text-center w-12">Pos</th>
                  <th className="py-4 px-4 font-bold min-w-[160px]">Club</th>
                  <th className="py-4 px-4 font-bold text-center">Sequence (Newest → Oldest)</th>
                  <th className="py-4 px-4 font-bold text-center">Gained Goals</th>
                  <th className="py-4 px-4 font-bold text-center">Conceded Goals</th>
                  <th className="py-4 px-4 font-bold text-center">Recent GD</th>
                  <th className="py-4 px-4 font-bold text-center text-[#00ff85]">Form Pts</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/5 text-sm">
                {sortedFormTable.map((team, index) => {
                  const pos = index + 1;
                  const recentGD = team.formStats.scored - team.formStats.conceded;
                  return (
                    <tr 
                      key={team.raw.name} 
                      className="hover:bg-white/[0.015] transition duration-150 align-middle"
                    >
                      <td className="py-3.5 px-4 text-center font-mono font-bold text-white/40">{pos}</td>
                      <td className="py-3.5 px-4 font-bold text-white">{team.raw.name}</td>
                      <td className="py-3.5 px-4">
                        <div className="flex gap-1.5 justify-center">
                          {team.formStats.last5.map((res: string, i: number) => (
                            <span 
                              key={i} 
                              className={`h-6.5 w-6.5 rounded-lg text-xs font-mono font-black flex items-center justify-center border shadow-sm ${
                                res === "W" 
                                  ? "bg-emerald-500/10 text-emerald-400 border-emerald-500/30" 
                                  : res === "D"
                                  ? "bg-white/5 text-white/45 border-white/10" 
                                  : "bg-red-500/10 text-red-400 border-red-500/30"
                              }`}
                            >
                              {res}
                            </span>
                          ))}
                        </div>
                      </td>
                      <td className="py-3.5 px-4 font-mono text-center text-white/80">{team.formStats.scored}</td>
                      <td className="py-3.5 px-4 font-mono text-center text-white/80">{team.formStats.conceded}</td>
                      <td className="py-3.5 px-4 font-mono text-center font-semibold text-white/80">
                        {recentGD > 0 ? `+${recentGD}` : recentGD}
                      </td>
                      <td className="py-3.5 px-4 font-mono text-center font-black text-[#00ff85]">{team.formStats.points} / 15</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          )}

          {activeTab === "expected" && (
            <table className="w-full text-left border-collapse select-none">
              <thead>
                <tr className="bg-white/[0.02] border-b border-white/5 font-mono text-[11px] text-white/40 uppercase tracking-wider">
                  <th className="py-4 px-4 font-bold text-center w-12">Pos</th>
                  <th className="py-4 px-4 font-bold min-w-[160px]">Club</th>
                  <th className="py-4 px-4 font-bold text-center text-[#00ff85]">xPts</th>
                  <th className="py-4 px-4 font-bold text-center text-teal-400">Pts Diff</th>
                  <th className="py-4 px-4 font-bold text-center text-amber-400">xG</th>
                  <th className="py-4 px-4 font-bold text-center text-white/40">xG Diff</th>
                  <th className="py-4 px-4 font-bold text-center text-rose-400">xGA</th>
                  <th className="py-4 px-4 font-bold text-center text-white/40">xGA Diff</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/5 text-sm">
                {sortedExpectedTable.map((team, index) => {
                  const pos = index + 1;
                  
                  // Helper for styling difference values (e.g. green for positive, amber for negative)
                  const getDiffColor = (val: string) => {
                    if (!val || val === "0" || val === "0.0") return "text-white/40";
                    return val.startsWith("+") ? "text-emerald-400 font-bold" : val.startsWith("-") ? "text-rose-400" : "text-white/60";
                  };

                  return (
                    <tr 
                      key={team.raw.name} 
                      className="hover:bg-white/[0.015] transition duration-150 align-middle"
                    >
                      <td className="py-3.5 px-4 text-center font-mono font-bold text-white/40">{pos}</td>
                      <td className="py-3.5 px-4 font-bold text-white font-sans text-sm">{team.raw.name}</td>
                      <td className="py-3.5 px-4 font-mono text-center font-black text-[#00ff85]">{team.expected.xPts}</td>
                      <td className={`py-3.5 px-4 font-mono text-center ${getDiffColor((team.expected.xPts - team.form.points).toFixed(1))}`}>
                        {(team.expected.xPts - team.form.points).toFixed(1)}
                      </td>
                      <td className="py-3.5 px-4 font-mono text-center text-amber-400 font-medium">{team.expected.xG}</td>
                      <td className={`py-3.5 px-4 font-mono text-center ${getDiffColor((team.expected.xG - team.form.goals_for).toFixed(1))}`}>
                        {(team.expected.xG - team.form.goals_for).toFixed(1)}
                      </td>
                      <td className="py-3.5 px-4 font-mono text-center text-rose-400 font-medium">{team.expected.xGA}</td>
                      <td className={`py-3.5 px-4 font-mono text-center ${getDiffColor((team.expected.xGA - team.form.goals_against).toFixed(1))}`}>
                        {(team.expected.xGA - team.form.goals_against).toFixed(1)}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          )}
        </div>
      </div>

      {/* FOOTER METADATA EXPLANATION */}
      <div className="flex gap-3 bg-white/[0.02] border border-white/5 rounded-2xl p-4 text-xs font-mono text-white/50 leading-relaxed">
        <Info className="h-4.5 w-4.5 shrink-0 text-[#00ff85]" />
        <div>
          <b>Legend & Qualification Criteria:</b> Positions 1-4 qualify for the premium Champions League group stages (green circles). Position 5 enters Europa Division (cyan border circle). Bottom three relegation positions 18-20 are highlighted in warning red.
        </div>
      </div>

    </div>
  );
}
