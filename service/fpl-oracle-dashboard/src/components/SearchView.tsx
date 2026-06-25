import { useState, useMemo } from "react";
import { 
  Search, 
  User, 
  Calendar, 
  Scale
} from "lucide-react";
import { CombinedFixture, CombinedPlayer, CombinedTeam } from "../data/types";
import { calculateAggregates } from "../data/fixtures";
import { getPosString } from "../lib/utils";
import { PositionBadge } from "./PositionBadge";

interface SearchViewProps {
  selectedSeason: string;
  selectedGW: number;
  fixtures: CombinedFixture[];
  players: CombinedPlayer[];
  teamsRaw: CombinedTeam[];
}

export default function SearchView({ 
  selectedSeason, 
  selectedGW,
  fixtures,
  players,
  teamsRaw
}: SearchViewProps) {
  const [searchTerm, setSearchTerm] = useState("");

  const activeFixtures = Array.isArray(fixtures) ? fixtures : [];

  const { matchingPlayers, matchingTeams, matchingFixtures } = useMemo(() => {
    if (!searchTerm.trim()) {
      return { matchingPlayers: [], matchingTeams: [], matchingFixtures: [] };
    }
    
    const term = searchTerm.toLowerCase();

    // 1. Players Search
    const foundPlayers = players.filter(p => {
      const posString = getPosString(p.raw.position);
      return p.raw.name.toLowerCase().includes(term) ||
             p.team.name.toLowerCase().includes(term) ||
             posString.toLowerCase().includes(term);
    });

    // 2. Teams Search
    const foundTeams = teamsRaw.filter(t => 
      t.raw.name.toLowerCase().includes(term)
    );

    // 3. Fixtures Search
    const foundFixtures = activeFixtures.filter(f => 
      f.home_team.name.toLowerCase().includes(term) ||
      f.away_team.name.toLowerCase().includes(term)
    );

    return {
      matchingPlayers: foundPlayers,
      matchingTeams: foundTeams,
      matchingFixtures: foundFixtures
    };
  }, [searchTerm, players, teamsRaw, activeFixtures]);

  const totalResults = matchingPlayers.length + matchingTeams.length + matchingFixtures.length;

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
                  {matchingPlayers.map(p => {
                    return (
                      <div key={p.id} className="clay-card p-4 border-white/5 bg-white/[0.01] flex justify-between items-center hover:border-[#00ff85]/30 hover:bg-white/[0.03] transition duration-150">
                        <div>
                          <PositionBadge position={p.raw.position} className="mb-1 block w-fit" />
                          <h4 className="text-sm font-bold text-white mt-1.5">{p.raw.name}</h4>
                          <p className="text-[11px] text-white/40 mt-0.5">{p.team.name} • Price £{(p.raw.cost / 10).toFixed(1)}m</p>
                        </div>
                        <div className="text-right font-mono">
                          <span className="text-[10px] text-white/30 uppercase block">Total Points</span>
                          <span className="text-base font-black text-white">{p.gw.total_points}</span>
                        </div>
                      </div>
                    );
                  })}
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
                    <div key={t.raw.name} className="clay-card p-4 border-white/5 bg-white/[0.01] flex justify-between items-center hover:border-[#00ff85]/30 hover:bg-white/[0.03] transition duration-150">
                      <div>
                        <h4 className="text-sm font-bold text-white">{t.raw.name} FC</h4>
                        <div className="flex items-center gap-2 mt-1 text-[11px] text-white/40 font-mono">
                          <span>Form {t.form.form_string}</span>
                        </div>
                      </div>
                      <div className="text-right font-mono">
                        <span className="text-[10px] text-white/30 uppercase block font-semibold text-white/40">Expected Pts</span>
                        <span className="text-xs text-white/70 block">xPts {t.expected.xPts.toFixed(1)}</span>
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
                  {matchingFixtures.map(f => {
                    const aggs = calculateAggregates(f);
                    return (
                      <div key={f.id} className="clay-card p-4 border-white/5 bg-white/[0.01] flex justify-between items-center hover:border-[#00ff85]/30 hover:bg-white/[0.03] transition duration-150">
                        <div>
                          <h4 className="text-sm font-bold text-white">{f.home_team.name} vs {f.away_team.name}</h4>
                          <p className="text-[11px] text-white/40 mt-1">Expected Over 2.5 Chance: <b className="text-white">{aggs.over25}%</b></p>
                        </div>
                        <div className="text-right font-mono">
                          <span className="text-[10px] text-white/30 uppercase block">Home Win Prob</span>
                          <span className="text-sm font-black text-white">{aggs.probHome}%</span>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            )}

          </div>
        )}
      </div>

    </div>
  );
}
