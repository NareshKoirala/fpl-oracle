/**
 * FILE: /src/components/SearchView.tsx
 * PURPOSE: Global search interface to fuzzy query players, teams, is-qualified stats, and structural matchups.
 * USAGE: Selected as the "search" view/tab in /src/App.tsx.
 */

import { useState } from "react";
import { 
  Search, 
  User, 
  MapPin, 
  Calendar, 
  Flame, 
  Scale, 
  ArrowRight,
  TrendingUp,
  Award,
  Zap,
  CheckCircle2
} from "lucide-react";
import { Fixture, Player, TeamRaw, TeamStrength } from "../data/types";

interface SearchViewProps {
  selectedSeason: string;
  selectedGW: number;
  fixtures: Fixture[];
  players: Player[];
  teamsRaw: TeamRaw[];
  teamsStrength: TeamStrength[];
}

export default function SearchView({ 
  selectedSeason, 
  selectedGW,
  fixtures,
  players,
  teamsRaw,
  teamsStrength
}: SearchViewProps) {
  const [searchTerm, setSearchTerm] = useState("");

  // Search Results structures
  let matchingPlayers: Player[] = [];
  let matchingTeams: TeamRaw[] = [];
  let matchingFixtures: Fixture[] = [];
  let matchingStrengths: TeamStrength[] = [];

  const activeFixtures = fixtures;
  const activeStrengths = teamsStrength;

  const handleSearch = () => {
    if (!searchTerm.trim()) return;

    const term = searchTerm.toLowerCase();

    // 1. Players Search
    matchingPlayers = players.filter(p => 
      (p.first_name + " " + p.second_name).toLowerCase().includes(term) ||
      p.team.toLowerCase().includes(term) ||
      p.element_type.toLowerCase().includes(term)
    );

    // 2. Teams Search
    matchingTeams = teamsRaw.filter(t => 
      t.team_name.toLowerCase().includes(term)
    );

    // 3. Fixtures Search
    matchingFixtures = activeFixtures.filter(f => 
      f.home_team.toLowerCase().includes(term) ||
      f.away_team.toLowerCase().includes(term)
    );

    // 4. Strengths Search
    matchingStrengths = activeStrengths.filter(s => 
      s.team_name.toLowerCase().includes(term)
    );
  };

  // Perform search on every keystroke for premium immediate feeling!
  handleSearch();

  const totalResults = matchingPlayers.length + matchingTeams.length + matchingFixtures.length + matchingStrengths.length;

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      
      {/* Visual Search Hero panel */}
      <div className="bg-white/[0.01] p-8 rounded-3xl border border-white/5 backdrop-blur-md text-center space-y-4">
        <div>
          <span className="text-[10px] font-mono font-bold text-[#00ff85] tracking-widest uppercase">Oracle Omnipresent Search</span>
          <h1 className="text-3xl font-black text-white mt-1">Cross-Database Global Search</h1>
          <p className="text-white/45 text-sm max-w-md mx-auto mt-1 leading-normal">
            Query across football players, team statistics, fixture probabilities, and tactical power indices instantly
          </p>
        </div>

        {/* Global Input */}
        <div className="relative max-w-lg mx-auto">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-white/40 h-5 w-5" />
          <input
            id="global-search-query"
            type="text"
            placeholder="Type 'Chelsea', 'Haaland', 'City', or 'Forward'..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full bg-white/5 text-white pl-12 pr-4 py-3 rounded-2xl border border-white/5 focus:border-[#00ff85]/50 outline-none focus:ring-2 focus:ring-[#00ff85]/10 text-sm transition duration-150 placeholder:text-white/30"
          />
        </div>
      </div>

      {/* Results grid */}
      <div className="space-y-6">
        {!searchTerm.trim() ? (
          <div className="text-center py-12 border border-dashed border-white/5 rounded-3xl text-white/30 text-xs font-mono">
            🔍 TYPE AT LEAST ONE CHARACTER TO TRIGGER REAL-TIME ORACLE LOOKUPS
          </div>
        ) : totalResults === 0 ? (
          <div className="text-center py-12 border border-dashed border-white/5 rounded-3xl text-white/40 text-xs font-mono">
            ❌ NO MATCHING METRICS IN THE CURRENT MODEL DATABASES
          </div>
        ) : (
          <div className="space-y-8">
            <p className="text-xs font-mono text-white/40 font-bold px-2">
              FOUND {totalResults} MATCHES ACROSS CHANNELS
            </p>

            {/* players segment */}
            {matchingPlayers.length > 0 && (
              <div className="space-y-3">
                <h3 className="text-xs font-mono font-bold text-cyan-400 tracking-wider uppercase px-2 flex items-center gap-1.5">
                  <User className="h-4 w-4" /> PLAYERS MATCHES ({matchingPlayers.length})
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {matchingPlayers.map(p => (
                    <div key={p.id} className="clay-card p-4 border-white/5 bg-white/[0.01] flex justify-between items-center hover:border-[#00ff85]/30 hover:bg-white/[0.03] transition duration-150">
                      <div>
                        <span className="text-[10px] bg-cyan-500/15 text-cyan-400 px-1.5 py-0.5 rounded font-mono font-bold">{p.element_type}</span>
                        <h4 className="text-sm font-bold text-white mt-1.5">{p.first_name} {p.second_name}</h4>
                        <p className="text-[11px] text-white/40 mt-0.5">{p.team} • Price £{p.now_cost}m</p>
                      </div>
                      <div className="text-right font-mono">
                        <span className="text-[10px] text-white/30 uppercase block">Total Points</span>
                        <span className="text-base font-black text-white">{p.total_points}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* teams raw segment */}
            {matchingTeams.length > 0 && (
              <div className="space-y-3">
                <h3 className="text-xs font-mono font-bold text-[#00ff85] tracking-wider uppercase px-2 flex items-center gap-1.5">
                  <Scale className="h-4 w-4" /> TEAM STATS MATCHES ({matchingTeams.length})
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {matchingTeams.map(t => (
                    <div key={t.team_name} className="clay-card p-4 border-white/5 bg-white/[0.01] flex justify-between items-center hover:border-[#00ff85]/30 hover:bg-white/[0.03] transition duration-150">
                      <div>
                        <h4 className="text-sm font-bold text-white">{t.team_name} FC</h4>
                        <div className="flex items-center gap-2 mt-1 text-[11px] text-white/40 font-mono">
                          <span>Played {t.played}</span>
                          <span>•</span>
                          <span>W{t.wins} D{t.draws} L{t.losses}</span>
                        </div>
                      </div>
                      <div className="text-right font-mono">
                        <span className="text-[10px] text-white/30 uppercase block font-semibold text-white/40">Form PPG</span>
                        <span className="text-xs text-white/70 block">xG {t.xg.toFixed(1)}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* strengths metrics segment */}
            {matchingStrengths.length > 0 && (
              <div className="space-y-3">
                <h3 className="text-xs font-mono font-bold text-yellow-500 tracking-wider uppercase px-2 flex items-center gap-1.5">
                  <TrendingUp className="h-4 w-4" /> TACTICAL STRENGTH MATCHES ({matchingStrengths.length})
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {matchingStrengths.map(s => (
                    <div key={s.team_name} className="clay-card p-4 border-white/5 bg-white/[0.01] flex justify-between items-center hover:border-[#00ff85]/30 hover:bg-white/[0.03] transition duration-150">
                      <div>
                        <h4 className="text-sm font-bold text-white">{s.team_name} Power Profile</h4>
                        <p className="text-[11px] text-white/40 mt-1">Overall strength calculation score: <b className="text-white">{s.overall_strength}%</b></p>
                      </div>
                      <div className="text-right font-mono">
                        <span className="text-[10px] text-white/30 uppercase block">Expected PPG</span>
                        <span className="text-sm font-black text-[#00ff85]">{s.expected_points_per_game}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* fixtures segment */}
            {matchingFixtures.length > 0 && (
              <div className="space-y-3">
                <h3 className="text-xs font-mono font-bold text-violet-400 tracking-wider uppercase px-2 flex items-center gap-1.5">
                  <Calendar className="h-4 w-4" /> FIXTURE MATCHES ({matchingFixtures.length})
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {matchingFixtures.map(f => (
                    <div key={f.id} className="clay-card p-4 border-white/5 bg-white/[0.01] flex justify-between items-center hover:border-[#00ff85]/30 hover:bg-white/[0.03] transition duration-150">
                      <div>
                        <h4 className="text-sm font-bold text-white">{f.home_team} vs {f.away_team}</h4>
                        <p className="text-[11px] text-white/40 mt-1">Expected Over 2.5 Chance: <b className="text-white">{f.over_2_5}%</b></p>
                      </div>
                      <div className="text-right font-mono">
                        <span className="text-[10px] text-white/30 uppercase block">Home Win Prob</span>
                        <span className="text-sm font-black text-white">{f.prob_home_win}%</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

          </div>
        )}
      </div>

    </div>
  );
}
