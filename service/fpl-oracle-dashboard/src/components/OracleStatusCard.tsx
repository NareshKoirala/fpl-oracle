/**
 * FILE: /src/components/OracleStatusCard.tsx
 * PURPOSE: Renders stateful oracle sync control, countdown markers, and manual background refresh simulations.
 * USAGE: Embedded inside /src/components/NavigationSidebar.tsx to present connection stats.
 */

import { useState, useEffect } from "react";
import { Clock, RefreshCw, AlertTriangle, CheckCircle } from "lucide-react";

interface OracleStatusCardProps {
  statusDetail: {
    next_fetch: string;
    last_fetch: string;
    current_gw: string;
    current_gw_in: string;
    current_gw_end: string;
  };
  selectedSeason: string;
  selectedGW: number;
}

export default function OracleStatusCard({
  statusDetail,
  selectedSeason,
  selectedGW
}: OracleStatusCardProps) {
  // Oracle status defaults to paused ("last_run until the next schedule the oracle would be on pause")
  // Only changing after the manual override is triggered.
  const [isOraclePaused, setIsOraclePaused] = useState(true);
  const [sessionLastFetch, setSessionLastFetch] = useState<string | null>(null);
  const [interactionMessage, setInteractionMessage] = useState<string | null>(null);
  const [systemTime, setSystemTime] = useState(new Date());

  // Keep system timer fresh to reflect lockouts dynamically
  useEffect(() => {
    const timer = setInterval(() => {
      setSystemTime(new Date());
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  const activeLastFetchStr = sessionLastFetch || statusDetail.last_fetch;
  
  // Safe date helper
  const parseDateTime = (str: string) => new Date(str.replace(" ", "T"));
  const lastFetchTime = parseDateTime(activeLastFetchStr);
  const gwInTime = parseDateTime(statusDetail.current_gw_in);
  const gwEndTime = parseDateTime(statusDetail.current_gw_end);

  // 1. Gameweek match window lockout check
  const isBetweenGwPeriod = systemTime >= gwInTime && systemTime <= gwEndTime;

  // 2. 1-hour downtime requirement between fetches
  const diffMs = systemTime.getTime() - lastFetchTime.getTime();
  const diffHours = diffMs / (1000 * 60 * 60);
  const isRecentLockoutActive = diffHours >= 0 && diffHours < 1.0;

  // Cooldown countdown
  const remainingMinutes = isRecentLockoutActive ? Math.ceil(60 - (diffHours * 60)) : 0;

  // Manual Trigger enabled condition
  const canForceFetch = !isBetweenGwPeriod && !isRecentLockoutActive;

  const handleForceFetchClick = () => {
    if (!canForceFetch) return;

    // Direct console log as requested by the developer
    console.log(`Force Fetch Triggered manually (Is Time): season=${selectedSeason}, gw=${selectedGW}`);

    // Update active last run timestamp to now YYYY-MM-DD HH:mm:ss
    const now = new Date();
    const formattedDate = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')} ${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}:${String(now.getSeconds()).padStart(2, '0')}`;
    
    setSessionLastFetch(formattedDate);
    setIsOraclePaused(false); // Activates the oracle to Active/Green!

    setInteractionMessage("Oracle Manual Run Commenced successfully! Sync complete.");
    setTimeout(() => {
      setInteractionMessage(null);
    }, 4000);
  };

  return (
    <div className="clay-card p-5 border-[#00ff85]/10 bg-white/[0.01] space-y-4 shadow-[inset_0_1px_1px_rgba(255,255,255,0.02),0_10px_30px_rgba(0,0,0,0.2)] select-none animate-fade-in relative overflow-hidden">
      {/* Decorative pulse glow based on current state */}
      <div className={`absolute -right-12 -top-12 h-24 w-24 rounded-full filter blur-xl opacity-10 transition duration-500 bg-emerald-500`} />

      {/* Header */}
      <div className="border-b border-white/5 pb-2.5 flex items-center justify-between">
        <div>
          <span className="text-[10px] font-mono text-[#00ff85] font-bold tracking-widest uppercase">System Oracle</span>
          <h4 className="text-sm font-bold text-white mt-0.5">Sync Scheduler Detail</h4>
        </div>
        <span className={`inline-block h-2.5 w-2.5 rounded-full ${isOraclePaused ? "bg-amber-400" : "bg-[#00ff85]"} animate-pulse`} />
      </div>

      {/* Status Indicators */}
      <div className="space-y-2 text-xs text-white/70">
        <div className="flex justify-between items-center bg-white/[0.01] border border-white/5 p-2 rounded-xl">
          <span className="text-white/40 font-mono">Oracle Engine:</span>
          <span className={`font-semibold px-2 py-0.5 rounded text-[11px] ${
            isOraclePaused 
              ? "bg-amber-500/10 text-amber-400 border border-amber-500/20" 
              : "bg-emerald-500/15 text-emerald-400 border border-emerald-500/20 animate-pulse"
          }`}>
            {isOraclePaused ? "Oracle on Pause" : "Fetch Green (Active)"}
          </span>
        </div>

        <div className="flex justify-between items-center bg-white/[0.01] border border-white/5 p-2 rounded-xl">
          <span className="text-white/40 font-mono">Last Run:</span>
          <span className="font-mono text-white/90">{activeLastFetchStr}</span>
        </div>

        <div className="flex justify-between items-center bg-white/[0.01] border border-white/5 p-2 rounded-xl">
          <span className="text-white/40 font-mono">Next Scheduled:</span>
          <span className="font-mono text-[#00ff85] font-semibold">{statusDetail.next_fetch}</span>
        </div>

        <div className="flex justify-between items-center bg-white/[0.01] border border-white/5 p-2 rounded-xl">
          <span className="text-white/40 font-mono">Active Gameweek:</span>
          <span className="text-white font-semibold">GW {statusDetail.current_gw}</span>
        </div>

        {/* GW Windows */}
        <div className="bg-white/[0.01] border border-white/5 p-2 rounded-xl space-y-1">
          <div className="flex justify-between items-center text-[10px] text-white/40 font-mono">
            <span>GW Starts:</span>
            <span className="text-white/80">{statusDetail.current_gw_in}</span>
          </div>
          <div className="flex justify-between items-center text-[10px] text-white/40 font-mono">
            <span>GW Ends:</span>
            <span className="text-white/80">{statusDetail.current_gw_end}</span>
          </div>
        </div>

        {/* Interactive Force Fetch (Is Time Trigger) */}
        <div className="pt-2 border-t border-white/5 mt-3 space-y-2">
          <button
            onClick={handleForceFetchClick}
            disabled={!canForceFetch}
            className={`w-full p-2.5 rounded-xl font-medium transition flex items-center justify-center gap-2 border select-none ${
              canForceFetch
                ? "bg-[#00ff85] text-black border-transparent hover:bg-[#00ff85]/90 hover:scale-[1.01] cursor-pointer"
                : "bg-white/5 text-white/30 border-white/5 cursor-not-allowed"
            }`}
          >
            <RefreshCw className={`h-3.5 w-3.5 ${canForceFetch ? "animate-spin-slow" : ""}`} />
            <span>Force Oracle Run (Is Time)</span>
          </button>

          {/* Validation Messages */}
          {isBetweenGwPeriod && (
            <div className="flex items-start gap-1.5 p-2 rounded bg-amber-500/10 border border-amber-500/15 text-[10px] text-amber-400">
              <AlertTriangle className="h-3.5 w-3.5 shrink-0 mt-0.5 animate-bounce" />
              <span>Disabled: Oracle paused while active gameweek matches are ongoing.</span>
            </div>
          )}

          {!isBetweenGwPeriod && isRecentLockoutActive && (
            <div className="flex items-start gap-1.5 p-2 rounded bg-red-500/10 border border-red-500/15 text-[10px] text-red-400">
              <AlertTriangle className="h-3.5 w-3.5 shrink-0 mt-0.5 animate-pulse" />
              <span>Disabled: Core cooling down. Force Run locked for {remainingMinutes} more minutes.</span>
            </div>
          )}

          {!isBetweenGwPeriod && !isRecentLockoutActive && (
            <div className="flex items-center gap-1.5 p-1.5 rounded bg-emerald-500/10 text-[10.5px] text-emerald-400 font-medium justify-center border border-emerald-500/20">
              <CheckCircle className="h-3 w-3 shrink-0" />
              <span>Available: Secure sync ready.</span>
            </div>
          )}

          {interactionMessage && (
            <div className="text-[11px] text-[#00ff85] text-center font-semibold bg-[#00ff85]/5 border border-[#00ff85]/20 p-2 rounded-lg animate-pulse">
              {interactionMessage}
            </div>
          )}
        </div>

        {/* System Clock (Simplified info block) */}
        <div className="text-[10px] text-white/30 font-mono text-center flex items-center justify-center gap-1 pt-1.5 leading-none">
          <Clock className="h-3 w-3" />
          <span>Clock: {systemTime.toLocaleTimeString()}</span>
        </div>
      </div>
    </div>
  );
}
