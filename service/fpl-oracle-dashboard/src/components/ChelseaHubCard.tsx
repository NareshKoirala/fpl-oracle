/**
 * FILE: /src/components/ChelseaHubCard.tsx
 * PURPOSE: Renders fixture predictions, underlying xG charts, and active performance trackers for Chelsea squad.
 * USAGE: Rendered as a dashboard card inside /src/components/DashboardView.tsx to highlight specific team stats.
 */

import { getChelseaHubData } from "../data/chelsea_hub";

interface ChelseaHubCardProps {
  selectedSeason?: string;
  selectedGW?: number;
}

export default function ChelseaHubCard({ selectedSeason, selectedGW }: ChelseaHubCardProps) {
  const data = getChelseaHubData(selectedSeason, selectedGW);

  return (
    <div className="clay-card p-5 border-blue-500/20 bg-blue-950/10 space-y-4 shadow-[inset_0_1px_1px_rgba(255,255,255,0.05),0_10px_30px_rgba(3,70,148,0.15)] select-none animate-fade-in">
      <div className="border-b border-white/5 pb-2.5 flex items-center justify-between">
        <div>
          <span className="text-[10px] font-mono text-cyan-400 font-bold tracking-widest uppercase">{data.title}</span>
          <h4 className="text-sm font-bold text-white mt-0.5 flex items-center gap-1.5">
            <span className="inline-block w-2.4 h-2.4 rounded-full bg-blue-500 animate-pulse" /> {data.subtitle}
          </h4>
        </div>
        <span className="text-lg">💙</span>
      </div>
      
      <div className="space-y-3">
        {data.fixtures.map((fixture, idx) => (
          <div 
            key={idx} 
            className="flex justify-between items-center bg-white/[0.02] border border-white/5 rounded-xl p-2.5 hover:bg-white/[0.04] transition duration-150"
          >
            <div className="min-w-0">
              <div className="flex items-center gap-1.5">
                <span className="text-[9px] font-mono font-black bg-blue-500/15 text-blue-400 border border-blue-500/30 px-1 rounded">{fixture.gw}</span>
                <span className="text-xs font-bold text-white truncate">{fixture.opponent}</span>
              </div>
              {fixture.isLiveOrHighlighted ? (
                <span className="text-[9.5px] font-mono text-[#00ff85] font-semibold mt-0.5 flex items-center gap-1">
                  <span className="inline-block h-1 w-1 rounded-full bg-[#00ff85]" />
                  {fixture.date}
                </span>
              ) : (
                <span className="text-[9.5px] font-mono text-white/40 block mt-0.5">{fixture.date}</span>
              )}
            </div>
            <span className={`text-[10px] font-mono font-black border px-1.5 py-0.5 rounded shrink-0 ${
              fixture.location === "H" 
                ? "bg-emerald-500/10 text-emerald-400 border-emerald-500/20" 
                : "bg-orange-500/10 text-orange-400 border-orange-500/20"
            }`}>
              {fixture.location}
            </span>
          </div>
        ))}
      </div>

      <div className="bg-blue-950/20 border border-blue-500/15 rounded-xl p-2.5 text-center">
        <p className="text-xs text-blue-300 font-medium italic">
          "{data.quote}"
        </p>
      </div>
    </div>
  );
}

