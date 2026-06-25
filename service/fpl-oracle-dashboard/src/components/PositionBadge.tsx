import { getPosString } from "../lib/utils";

interface PositionBadgeProps {
  position: number | string;
  className?: string;
  withBorder?: boolean;
}

export function PositionBadge({ position, className = "", withBorder = true }: PositionBadgeProps) {
  const posStr = typeof position === "number" ? getPosString(position) : position;
  
  const borderClasses = withBorder ? (
    posStr === "FWD" ? "border border-[#ff005a]/20" :
    posStr === "MID" ? "border border-cyan-500/20" :
    posStr === "DEF" ? "border border-indigo-500/20" :
    "border border-amber-500/20"
  ) : "";

  const colorClasses = 
    posStr === "FWD" ? "bg-[#ff005a]/10 text-[#ff005a]" :
    posStr === "MID" ? "bg-cyan-500/10 text-cyan-400" :
    posStr === "DEF" ? "bg-indigo-500/10 text-indigo-400" :
    "bg-amber-500/10 text-amber-500";

  return (
    <span className={`text-[10px] font-mono font-bold px-1.5 py-0.5 rounded ${colorClasses} ${borderClasses} ${className}`}>
      {posStr}
    </span>
  );
}
