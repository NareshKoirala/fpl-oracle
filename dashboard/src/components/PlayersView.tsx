/**
 * FILE: /src/components/PlayersView.tsx
 * PURPOSE: Interactive player dashboard comprising list filters, cost metrics, underlying stats, xPts forecasts, and the dedicated Dossier.
 * USAGE: Selected as the "players" view/tab in /src/App.tsx.
 */

import { useState, useMemo, useEffect } from "react";
import { motion, AnimatePresence } from "motion/react";
import { 
  Search, 
  Filter, 
  Sparkles, 
  User, 
  Percent, 
  HelpCircle,
  Hash,
  Award,
  Shield,
  Coins,
  ChevronDown,
  Skull,
  ChevronLeft,
  ChevronRight,
  TrendingUp,
  Activity,
  Heart,
  Info,
  X
} from "lucide-react";
import { Player } from "../data/types";
import { 
  ResponsiveContainer, 
  RadarChart, 
  PolarGrid, 
  PolarAngleAxis, 
  PolarRadiusAxis, 
  Radar, 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  Tooltip,
  Legend
} from "recharts";

interface PlayersViewProps {
  selectedSeason: string;
  selectedGW: number;
  players: Player[];
}

export default function PlayersView({ selectedSeason, selectedGW, players }: PlayersViewProps) {
  const safePlayers = Array.isArray(players) ? players : [];
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedPosition, setSelectedPosition] = useState("ALL");
  const [selectedTeam, setSelectedTeam] = useState("ALL");
  const [maxPrice, setMaxPrice] = useState(16.0);
  const [selectedPlayerId, setSelectedPlayerId] = useState<number | null>(null);
  
  // Pagination State
  const [page, setPage] = useState(1);
  const itemsPerPage = 12;

  // Active chart view state inside Dossier
  const [dossierChartType, setDossierChartType] = useState<"underlying" | "outcomes">("underlying");
  const [isMobileDossierOpen, setIsMobileDossierOpen] = useState(false);

  // Extract unique teams for dropdown filtering
  const uniqueTeams = useMemo(() => {
    return Array.from(new Set(safePlayers.map(p => p.team))).sort();
  }, [safePlayers]);

  // Reset pagination to page 1 whenever any filter changes
  useEffect(() => {
    setPage(1);
  }, [selectedSeason, selectedGW, searchTerm, selectedPosition, selectedTeam, maxPrice]);

  // Filter player list
  const filteredPlayers = useMemo(() => {
    return safePlayers.filter(p => {
      const fullName = `${p.first_name || ""} ${p.second_name || ""}`.toLowerCase();
      const matchesSearch = fullName.includes(searchTerm.toLowerCase()) || 
                            (p.web_name || "").toLowerCase().includes(searchTerm.toLowerCase());
      const matchesPosition = selectedPosition === "ALL" || p.element_type === selectedPosition;
      const matchesTeam = selectedTeam === "ALL" || p.team === selectedTeam;
      const matchesPrice = p.now_cost <= maxPrice;
      return matchesSearch && matchesPosition && matchesTeam && matchesPrice;
    });
  }, [safePlayers, searchTerm, selectedPosition, selectedTeam, maxPrice]);

  // Set default active player when filtered list or component loads
  const activePlayer = useMemo(() => {
    if (selectedPlayerId !== null) {
      const match = safePlayers.find(p => p.id === selectedPlayerId);
      if (match) return match;
    }
    return filteredPlayers[0] || safePlayers[0];
  }, [filteredPlayers, safePlayers, selectedPlayerId]);

  // Synchronize ID if activePlayer changes
  useEffect(() => {
    if (activePlayer && activePlayer.id !== selectedPlayerId) {
      setSelectedPlayerId(activePlayer.id);
    }
  }, [activePlayer, selectedPlayerId]);

  // Paginated players list
  const paginatedPlayers = useMemo(() => {
    const start = (page - 1) * itemsPerPage;
    return filteredPlayers.slice(start, start + itemsPerPage);
  }, [filteredPlayers, page]);

  const totalPages = Math.ceil(filteredPlayers.length / itemsPerPage);

  // Radar chart data: Underlying Per 90 metrics
  const radarData = useMemo(() => {
    if (!activePlayer) return [];
    return [
      { name: "Influence /90", val: parseFloat(activePlayer.influence_per_90 || "0") },
      { name: "Creativity /90", val: parseFloat(activePlayer.creativity_per_90 || "0") },
      { name: "Threat /90 (scaled)", val: Math.round(parseFloat(activePlayer.threat_per_90 || "0") / 2) },
      { name: "Expected GI /90 (x100)", val: Math.round(parseFloat(activePlayer.expected_goal_involvements_per_90 || "0") * 100) },
      { name: "ICT Index /90 (x10)", val: Math.round(parseFloat(activePlayer.ict_index_per_90 || "0") * 10) }
    ];
  }, [activePlayer]);

  // Outcomes comparison (Expected vs Actual)
  const outcomesData = useMemo(() => {
    if (!activePlayer) return [];
    return [
      { name: "Goals", Expected: parseFloat(activePlayer.expected_goals || "0"), Actual: activePlayer.goals_scored || 0 },
      { name: "Assists", Expected: parseFloat(activePlayer.expected_assists || "0"), Actual: activePlayer.assists || 0 }
    ];
  }, [activePlayer]);

  // Health Status helper
  const getStatusBadge = (status: string) => {
    switch (status?.toLowerCase()) {
      case "a":
        return <span className="inline-flex items-center gap-1 text-[10px] bg-emerald-500/10 text-emerald-400 border border-emerald-500/25 px-2 py-0.5 rounded-full font-mono">● Active</span>;
      case "d":
        return <span className="inline-flex items-center gap-1 text-[10px] bg-amber-500/10 text-amber-400 border border-amber-500/25 px-2 py-0.5 rounded-full font-mono">▲ Doubtful</span>;
      case "i":
      default:
        return <span className="inline-flex items-center gap-1 text-[10px] bg-red-500/10 text-red-400 border border-red-500/25 px-2 py-0.5 rounded-full font-mono">■ Injured</span>;
    }
  };

  const renderDossierContent = () => {
    if (!activePlayer) return null;
    return (
      <div className="space-y-6 text-left">
        {/* Identity Header */}
        <div className="pb-4 border-b border-white/5">
          <div className="flex justify-between items-start">
            <div>
              <span className="text-[10px] font-mono text-violet-400 uppercase tracking-widest font-bold">Player Dossier</span>
              <h2 className="text-xl font-black text-white mt-1 leading-tight">{activePlayer.first_name} {activePlayer.second_name}</h2>
              <div className="flex items-center gap-2 mt-2">
                <span className="text-xs font-medium text-white/40">{activePlayer.team}</span>
                <span className="text-white/20 font-mono">•</span>
                <span className="text-xs font-bold text-[#00ff85]">{activePlayer.element_type}</span>
              </div>
            </div>
            <div>
              {getStatusBadge(activePlayer.status)}
            </div>
          </div>
        </div>

        {/* Dossier Charts Selector Tabs */}
        <div className="space-y-3">
          <div className="flex justify-between items-center">
            <h3 className="text-[10px] font-mono text-white/40 uppercase tracking-wide font-black">Analytical Visualizations</h3>
            <div className="flex bg-white/5 p-0.5 rounded-lg border border-white/5">
              <button
                onClick={() => setDossierChartType("underlying")}
                className={`px-2 py-1 rounded-md text-[9px] font-mono font-bold transition ${
                  dossierChartType === "underlying" 
                    ? "bg-[#00ff85]/10 text-[#00ff85]" 
                    : "text-white/40 hover:text-white"
                }`}
              >
                Underlying /90
              </button>
              <button
                onClick={() => setDossierChartType("outcomes")}
                className={`px-2 py-1 rounded-md text-[9px] font-mono font-bold transition ${
                  dossierChartType === "outcomes" 
                    ? "bg-[#00ff85]/10 text-[#00ff85]" 
                    : "text-white/40 hover:text-white"
                }`}
              >
                Expected vs Real
              </button>
            </div>
          </div>

          {/* Interactive Chart Container */}
          <div className="h-44 w-full bg-white/[0.01] border border-white/5 rounded-2xl flex items-center justify-center p-2 relative overflow-hidden">
            {dossierChartType === "underlying" ? (
              <ResponsiveContainer width="100%" height="100%">
                <RadarChart cx="50%" cy="50%" outerRadius="70%" data={radarData}>
                  <PolarGrid stroke="rgba(255, 255, 255, 0.05)" />
                  <PolarAngleAxis 
                    dataKey="name" 
                    tick={{ fill: 'rgba(255, 255, 255, 0.4)', fontSize: 8, fontFamily: 'monospace' }} 
                  />
                  <PolarRadiusAxis 
                    angle={30} 
                    domain={[0, 'auto']} 
                    tick={{ fill: 'rgba(255, 255, 255, 0.2)', fontSize: 7 }}
                  />
                  <Radar 
                    name={`${activePlayer.web_name} Profile`} 
                    dataKey="val" 
                    stroke="#00ff85" 
                    fill="#00ff85" 
                    fillOpacity={0.15} 
                  />
                  <Tooltip 
                    contentStyle={{ backgroundColor: '#18181b', borderColor: 'rgba(255,255,255,0.1)', borderRadius: '12px' }}
                    labelStyle={{ color: '#ffffff', fontFamily: 'monospace', fontSize: '10px' }}
                    itemStyle={{ color: '#00ff85', fontSize: '10px' }}
                  />
                </RadarChart>
              </ResponsiveContainer>
            ) : (
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={outcomesData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                  <XAxis 
                    dataKey="name" 
                    stroke="rgba(255,255,255,0.3)" 
                    tick={{ fill: 'rgba(255,255,255,0.5)', fontSize: 9, fontFamily: 'monospace' }}
                  />
                  <YAxis 
                    stroke="rgba(255,255,255,0.3)" 
                    tick={{ fill: 'rgba(255,255,255,0.5)', fontSize: 9 }}
                  />
                  <Tooltip 
                    contentStyle={{ backgroundColor: '#18181b', borderColor: 'rgba(255,255,255,0.1)', borderRadius: '12px' }}
                    labelStyle={{ color: '#ffffff', fontFamily: 'monospace', fontSize: '10px' }}
                  />
                  <Legend 
                    iconSize={8}
                    wrapperStyle={{ fontSize: '9px', fontFamily: 'monospace', color: 'rgba(255,255,255,0.5)' }}
                  />
                  <Bar dataKey="Expected" fill="rgba(255, 255, 255, 0.15)" stroke="rgba(255,255,255,0.25)" radius={[4, 4, 0, 0]} />
                  <Bar dataKey="Actual" fill="#00ff85" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            )}
          </div>
        </div>

        {/* Expected vs Actual comparison indexes (Durable numbers) */}
        <div className="space-y-4">
          <h3 className="text-[10px] font-mono text-white/40 uppercase tracking-wide font-black">Expected Metrics Profile</h3>
          <div className="grid grid-cols-2 gap-4">
            <div className="p-3 bg-white/[0.01] border border-white/5 rounded-xl">
              <span className="text-[10px] text-white/30 uppercase block font-mono">Expected Goals (xG)</span>
              <span className="text-base font-black text-white font-mono">{activePlayer.expected_goals || "0.0"}</span>
              <span className="text-[10px] text-white/40 block font-mono mt-0.5">Real Goals: {activePlayer.goals_scored}</span>
            </div>

            <div className="p-3 bg-white/[0.01] border border-white/5 rounded-xl">
              <span className="text-[10px] text-white/30 uppercase block font-mono">Expected Assists (xA)</span>
              <span className="text-base font-black text-white font-mono">{activePlayer.expected_assists || "0.0"}</span>
              <span className="text-[10px] text-white/40 block font-mono mt-0.5">Real Assists: {activePlayer.assists}</span>
            </div>
          </div>

          {/* Advanced underlying stats */}
          <div className="grid grid-cols-2 gap-4">
            <div className="p-3 bg-white/[0.01] border border-white/5 rounded-xl">
              <span className="text-[10px] text-white/30 uppercase block font-mono">Expected GI (xGI)</span>
              <span className="text-base font-black text-white font-mono">{activePlayer.expected_goal_involvements || "0.00"}</span>
              <span className="text-[10px] text-white/40 block font-mono mt-0.5">GI /90: {activePlayer.expected_goal_involvements_per_90 || "0.00"}</span>
            </div>

            <div className="p-3 bg-white/[0.01] border border-white/5 rounded-xl">
              <span className="text-[10px] text-white/30 uppercase block font-mono">Expected GC (xGC)</span>
              <span className="text-base font-black text-white font-mono">{activePlayer.expected_goals_conceded || "0.00"}</span>
              <span className="text-[10px] text-white/40 block font-mono mt-0.5">xGC /90: {activePlayer.expected_goals_conceded_per_90 || "0.00"}</span>
            </div>
          </div>

          {/* Bonus Points and Disciplinary Actions */}
          <div className="p-4 bg-white/[0.01] border border-white/5 rounded-2xl space-y-3">
            <span className="text-[10px] text-white/40 uppercase block font-mono tracking-widest text-center">FPL Performance Registers</span>
            <div className="grid grid-cols-2 gap-4 pt-1 text-center font-mono">
              <div className="border-r border-white/5">
                <span className="text-[9px] text-white/30 uppercase block">Bonus Points (BPS)</span>
                <span className="text-xs font-bold text-[#00ff85] mt-0.5 block">{activePlayer.bonus} pts <span className="text-white/30 font-normal text-[9px]">({activePlayer.bps || 0})</span></span>
              </div>
              <div>
                <span className="text-[9px] text-white/30 uppercase block">Discipline</span>
                <span className="text-xs font-bold text-red-400 mt-0.5 block">
                  💛 {activePlayer.yellow_cards} &nbsp;❤️ {activePlayer.red_cards}
                </span>
              </div>
            </div>

            {activePlayer.element_type === "GKP" && (
              <div className="pt-2 border-t border-white/5 text-center">
                <span className="text-[9px] font-mono text-white/30 uppercase block">Keeper Saves Record</span>
                <span className="text-xs font-bold text-white font-mono">{activePlayer.saves || 0} Saves registered</span>
              </div>
            )}
          </div>

          {/* ICT Metrics summary with animated style indicators */}
          <div className="p-4 bg-white/[0.01] border border-white/5 rounded-2xl space-y-3">
            <span className="text-[10px] text-white/40 uppercase block font-mono tracking-widest text-center">ICT Index Rankings</span>
            <div className="flex justify-between items-center bg-white/5 px-3 py-2 rounded-xl text-xs">
              <span className="text-white/60">Overall ICT Score:</span>
              <span className="font-mono text-[#00ff85] font-bold">{activePlayer.ict_index}</span>
            </div>

            <div className="space-y-2 pt-1 font-mono">
              <div className="flex justify-between text-[11px] text-white/45">
                <span>Influence: {activePlayer.influence}</span>
                <span className="text-[10px] text-white/30">Rank: #{activePlayer.influence_rank}</span>
              </div>
              <div className="flex justify-between text-[11px] text-white/45">
                <span>Creativity: {activePlayer.creativity}</span>
                <span className="text-[10px] text-white/30">Rank: #{activePlayer.creativity_rank}</span>
              </div>
              <div className="flex justify-between text-[11px] text-white/45">
                <span>Threat: {activePlayer.threat}</span>
                <span className="text-[10px] text-white/30">Rank: #{activePlayer.threat_rank}</span>
              </div>
            </div>
          </div>
        </div>

        {/* Set Pieces roles */}
        <div className="space-y-3.5">
          <h3 className="text-[10px] font-mono text-white/40 uppercase tracking-wide font-black">Set-Piece Role Ranking</h3>
          
          <div className="grid grid-cols-3 gap-2 text-center text-xs">
            <div className="p-2.5 bg-white/[0.01] rounded-xl border border-white/5">
              <span className="text-[9px] text-white/30 block uppercase font-mono">Penalties</span>
              <span className="font-black text-white block mt-1">{activePlayer.set_pieces?.penalties_order ? `#${activePlayer.set_pieces.penalties_order}` : '—'}</span>
            </div>

            <div className="p-2.5 bg-white/[0.01] rounded-xl border border-white/5">
              <span className="text-[9px] text-white/30 block uppercase font-mono">Freekicks</span>
              <span className="font-black text-white block mt-1">{activePlayer.set_pieces?.freekicks_order ? `#${activePlayer.set_pieces.freekicks_order}` : '—'}</span>
            </div>

            <div className="p-2.5 bg-white/[0.01] rounded-xl border border-white/5">
              <span className="text-[9px] text-white/30 block uppercase font-mono">Corners</span>
              <span className="font-black text-white block mt-1">{activePlayer.set_pieces?.corners_order ? `#${activePlayer.set_pieces.corners_order}` : '—'}</span>
            </div>
          </div>
        </div>

        {/* Totals panel */}
        <div className="pt-4 border-t border-white/5 flex justify-between items-center text-xs font-mono">
          <span className="text-white/30">ICT Profile Rank: #{activePlayer.ict_rank}</span>
          <span className="text-[#00ff85] bg-[#00ff85]/10 px-2.5 py-0.5 rounded font-black">FORM {activePlayer.form}</span>
        </div>
      </div>
    );
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
      
      {/* LEFT COLUMN: Filters + Live Table + Pagination */}
      <div className="col-span-12 lg:col-span-8 space-y-6">
        
        {/* Filters Panel */}
        <div className="bg-white/[0.01] p-5 rounded-3xl border border-white/5 backdrop-blur-md space-y-4">
          <div className="flex flex-col sm:flex-row gap-4 justify-between items-start sm:items-center">
            <div>
              <h2 className="text-lg font-bold text-white flex items-center gap-2">
                <Filter className="text-[#00ff85] h-5 w-5" /> Filter Assets
              </h2>
              <p className="text-white/40 text-xs">Sift through player metrics with multi-dimensional criteria</p>
            </div>

            {/* Global Search */}
            <div className="relative w-full sm:w-64">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-white/40 h-4 w-4" />
              <input
                id="player-search-bar"
                type="text"
                placeholder="Search players..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full bg-white/5 text-white pl-9 pr-4 py-2.5 text-xs rounded-xl border border-white/5 focus:border-[#00ff85]/55 outline-none focus:ring-1 focus:ring-[#00ff85]/20 transition duration-150 placeholder:text-white/30 font-mono"
              />
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 pt-2">
            {/* Position Select */}
            <div className="space-y-1">
              <label htmlFor="position-filter" className="text-[10px] font-mono font-bold text-white/40 uppercase">POSITION</label>
              <select
                id="position-filter"
                value={selectedPosition}
                onChange={(e) => setSelectedPosition(e.target.value)}
                className="w-full bg-white/5 text-white border border-white/5 rounded-xl px-3 py-2 text-xs outline-none cursor-pointer focus:border-[#00ff85]/40"
              >
                <option value="ALL">All Positions</option>
                <option value="GKP">Goalkeepers</option>
                <option value="DEF">Defenders</option>
                <option value="MID">Midfielders</option>
                <option value="FWD">Forwards</option>
              </select>
            </div>

            {/* Team Select */}
            <div className="space-y-1">
              <label htmlFor="team-filter" className="text-[10px] font-mono font-bold text-white/40 uppercase">TEAM SELECT</label>
              <select
                id="team-filter"
                value={selectedTeam}
                onChange={(e) => setSelectedTeam(e.target.value)}
                className="w-full bg-white/5 text-white border border-white/5 rounded-xl px-3 py-2 text-xs outline-none cursor-pointer focus:border-[#00ff85]/40"
              >
                <option value="ALL">All Teams</option>
                {uniqueTeams.map(t => (
                  <option key={t} value={t}>{t}</option>
                ))}
              </select>
            </div>

            {/* Price Cap Slider */}
            <div className="space-y-1">
              <div className="flex justify-between text-[11px] font-mono font-bold text-white/40 uppercase">
                <label htmlFor="price-slider">PRICE CAP (MAX)</label>
                <span className="text-[#00ff85] font-black">£{maxPrice.toFixed(1)}m</span>
              </div>
              <input
                id="price-slider"
                type="range"
                min="4.0"
                max="16.0"
                step="0.1"
                value={maxPrice}
                onChange={(e) => setMaxPrice(parseFloat(e.target.value))}
                className="w-full h-1 bg-white/5 rounded-lg appearance-none cursor-pointer accent-[#00ff85] mt-3"
              />
            </div>
          </div>
        </div>

        {/* Player List Card */}
        <div className="clay-card border-white/5 overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-white/5 text-[10px] uppercase font-mono tracking-wider text-white/40 bg-white/[0.01]">
                  <th className="py-3 px-5 font-semibold">Player</th>
                  <th className="py-3 px-4 font-semibold text-center">Team/Pos</th>
                  <th className="py-3 px-4 font-semibold text-center">Cost</th>
                  <th className="py-3 px-4 font-semibold text-center">Selected %</th>
                  <th className="py-3 px-4 font-semibold text-center">xPTS Form</th>
                  <th className="py-3 px-4 font-semibold text-center">Total Pts</th>
                  <th className="py-3 px-5 font-semibold text-right">Details</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/5">
                {filteredPlayers.length === 0 ? (
                  <tr>
                    <td colSpan={7} className="py-8 text-center text-xs text-white/30 font-mono">
                      ❌ NO PLAYERS MATCH CHOSEN FILTERS
                    </td>
                  </tr>
                ) : (
                  paginatedPlayers.map((p) => {
                    const isSelected = p.id === activePlayer?.id;
                    return (
                      <tr 
                        key={p.id} 
                        onClick={() => {
                          setSelectedPlayerId(p.id);
                          setIsMobileDossierOpen(true);
                        }}
                        className={`cursor-pointer hover:bg-white/[0.02] transition duration-150 ${isSelected ? 'bg-[#00ff85]/[0.05]' : ''}`}
                      >
                        {/* Name */}
                        <td className="py-3 px-5 font-semibold text-white text-xs">
                          <div className="font-sans font-bold">{p.web_name}</div>
                          <div className="text-[10px] text-white/30 font-mono font-normal mt-0.5">{p.first_name} {p.second_name}</div>
                        </td>

                        {/* Team and Position Badges */}
                        <td className="py-3 px-4 text-center">
                          <div className="inline-flex items-center gap-1.5 justify-center">
                            <span className="text-[10px] font-mono text-white/60 bg-white/5 px-1.5 py-0.5 rounded">
                              {p.team}
                            </span>
                            <span className={`text-[10px] font-mono font-bold px-1.5 py-0.5 rounded ${
                              p.element_type === "FWD" ? "bg-[#ff005a]/10 text-[#ff005a]" :
                              p.element_type === "MID" ? "bg-cyan-500/10 text-cyan-400" :
                              p.element_type === "DEF" ? "bg-indigo-500/10 text-indigo-400" :
                              "bg-amber-500/10 text-amber-500"
                            }`}>
                              {p.element_type}
                            </span>
                          </div>
                        </td>

                        {/* Cost */}
                        <td className="py-3 px-4 text-center font-mono font-bold text-xs text-white/80">
                          £{p.now_cost ? p.now_cost.toFixed(1) : "0.0"}m
                        </td>

                        {/* Selected % */}
                        <td className="py-3 px-4 text-center font-mono text-xs text-white/40">
                          {p.selected_by_percent}%
                        </td>

                        {/* Form */}
                        <td className="py-3 px-4 text-center font-mono text-xs text-[#00ff85] font-black">
                          {p.form}
                        </td>

                        {/* Total Points */}
                        <td className="py-3 px-4 text-center font-mono font-black text-sm text-white">
                          {p.total_points}
                        </td>

                        {/* View Button */}
                        <td className="py-3 px-5 text-right">
                          <div className={`h-4 w-4 rounded-full border border-[#00ff85]/30 flex items-center justify-center inline-block ${
                            isSelected ? 'bg-[#00ff85] text-black font-bold border-transparent text-[10px]' : 'bg-transparent text-transparent'
                          }`}>
                            ✓
                          </div>
                        </td>
                      </tr>
                    );
                  })
                )}
              </tbody>
            </table>
          </div>
        </div>

        {/* Players View Pagination Controls */}
        {totalPages > 1 && (
          <div className="flex flex-col sm:flex-row items-center justify-between gap-4 bg-white/[0.01] p-4 rounded-2xl border border-white/5 backdrop-blur-md">
            <div className="text-xs font-mono text-white/50">
              Showing <b className="text-[#00ff85]">{(page - 1) * itemsPerPage + 1}</b> - <b className="text-[#00ff85]">{Math.min(page * itemsPerPage, filteredPlayers.length)}</b> of <b className="text-[#00ff85]">{filteredPlayers.length}</b> players
            </div>
            <div className="flex items-center gap-2">
              <button
                onClick={() => setPage(p => Math.max(1, p - 1))}
                disabled={page === 1}
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
                    Math.abs(pageNum - page) <= 1
                  ) {
                    return (
                      <button
                        key={pageNum}
                        onClick={() => setPage(pageNum)}
                        className={`h-9 min-w-9 px-1.5 rounded-xl border font-mono text-xs font-bold transition select-none cursor-pointer ${
                          page === pageNum
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
                onClick={() => setPage(p => Math.min(totalPages, p + 1))}
                disabled={page === totalPages}
                className="flex items-center justify-center h-9 w-9 rounded-xl border border-white/10 bg-white/5 text-white/70 hover:text-white hover:bg-white/10 disabled:opacity-30 disabled:pointer-events-none transition cursor-pointer select-none"
                title="Next Page"
              >
                <ChevronRight className="h-4 w-4" />
              </button>
            </div>
          </div>
        )}

      </div>

      {/* RIGHT COLUMN: Dedicated Player Deep Analysis (Visual Dossier Card with charts) - HIDDEN ON MOBILE */}
      <div className="hidden lg:block lg:col-span-4 space-y-6 text-left">
        {activePlayer ? (
          <div className="clay-card p-6 border-white/5 bg-[#141416] space-y-6">
            {renderDossierContent()}
          </div>
        ) : (
          <div className="clay-card p-8 border-white/5 bg-[#141416] text-center text-white/30 font-mono text-xs">
            No player selected
          </div>
        )}
      </div>

      {/* MOBILE DOSSIER OVERLAY DIALOG */}
      <AnimatePresence>
        {isMobileDossierOpen && activePlayer && (
          <div className="fixed inset-0 z-50 lg:hidden flex items-end sm:items-center justify-center p-4">
            {/* Backdrop */}
            <motion.div 
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setIsMobileDossierOpen(false)}
              className="absolute inset-0 bg-black/80 backdrop-blur-sm"
              style={{ contentVisibility: "auto" }}
            />
            
            {/* Drawer/Modal content */}
            <motion.div
              initial={{ opacity: 0, y: 100 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: 100 }}
              transition={{ type: "spring", damping: 25, stiffness: 350 }}
              className="relative w-full max-w-lg bg-[#141416] rounded-t-3xl sm:rounded-3xl border border-white/10 shadow-2xl overflow-hidden max-h-[85vh] flex flex-col z-10"
            >
              {/* Header with Close */}
              <div className="flex justify-between items-center px-6 py-4 border-b border-white/5 bg-white/[0.01]">
                <div className="flex items-center gap-2">
                  <Award className="h-4.5 w-4.5 text-[#00ff85] animate-pulse" />
                  <span className="text-xs font-mono text-[#00ff85] tracking-widest uppercase font-bold">Mobile Dossier Insight</span>
                </div>
                <button 
                  onClick={() => setIsMobileDossierOpen(false)}
                  className="p-1.5 rounded-lg bg-white/5 border border-white/5 text-white/50 hover:text-white hover:bg-white/10 transition"
                >
                  <X className="h-4 w-4" />
                </button>
              </div>

              {/* Scrollable content */}
              <div className="overflow-y-auto p-6 space-y-6 flex-1 scrollbar-none">
                {renderDossierContent()}
              </div>
            </motion.div>
          </div>
        )}
      </AnimatePresence>

    </div>
  );
}
