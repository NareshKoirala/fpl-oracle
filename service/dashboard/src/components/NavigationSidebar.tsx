/**
 * FILE: /src/components/NavigationSidebar.tsx
 * PURPOSE: Side sidebar navigation element presenting available views, sync stats, Chelsea, and developer credentials.
 * USAGE: Rendered as a persistent navigation framework in /src/App.tsx left column.
 */

import { motion } from "motion/react";
import { 
  LayoutDashboard, 
  Calendar, 
  TrendingUp, 
  Users, 
  Table2, 
  Search 
} from "lucide-react";

import OracleStatusCard from "./OracleStatusCard";
import ChelseaHubCard from "./ChelseaHubCard";
import DeveloperProfileCard from "./DeveloperProfileCard";

type ViewType = "dashboard" | "fixtures" | "processed" | "players" | "search" | "standings";

interface NavigationSidebarProps {
  activeView: ViewType;
  setActiveView: (view: ViewType) => void;
  statusDetailData: {
    next_fetch: string;
    last_fetch: string;
    current_gw: string;
    current_gw_in: string;
    current_gw_end: string;
  };
  selectedSeason: string;
  selectedGW: number;
}

const navItems = [
  { id: "dashboard", label: "Dashboard", icon: LayoutDashboard },
  { id: "fixtures", label: "Fixtures", icon: Calendar },
  { id: "processed", label: "Processed", icon: TrendingUp },
  { id: "players", label: "Players", icon: Users },
  { id: "standings", label: "Standings", icon: Table2 },
  { id: "search", label: "Search", icon: Search },
] as const;

export default function NavigationSidebar({
  activeView,
  setActiveView,
  statusDetailData,
  selectedSeason,
  selectedGW
}: NavigationSidebarProps) {
  return (
    <aside className="w-full lg:w-64 shrink-0 flex flex-col gap-5">
      <nav className="flex flex-row lg:flex-col gap-1.5 overflow-x-auto lg:overflow-x-visible pb-2 lg:pb-0 scrollbar-none bg-white/[0.01] p-1.5 rounded-2xl border border-white/5">
        {navItems.map((item) => {
          const isActive = activeView === item.id;
          const Icon = item.icon;
          
          return (
            <button
              key={item.id}
              id={`nav-link-${item.id}`}
              onClick={() => setActiveView(item.id)}
              className={`relative flex items-center gap-3 px-4 py-3 rounded-xl transition duration-150 text-sm font-medium cursor-pointer whitespace-nowrap lg:w-full select-none ${
                isActive 
                  ? "text-white" 
                  : "text-white/50 hover:text-white hover:bg-white/[0.02]"
              }`}
            >
              {isActive && (
                <motion.div
                  layoutId="active-pill"
                  className="absolute inset-0 bg-white/5 border border-white/10 rounded-xl"
                  transition={{ type: "spring", stiffness: 380, damping: 30 }}
                />
              )}

              <Icon className={`h-4.5 w-4.5 z-10 transition-colors ${isActive ? "text-[#00ff85]" : "text-white/40"}`} />
              <span className={`z-10 ${isActive ? "text-[#00ff85] font-semibold" : ""}`}>{item.label}</span>
            </button>
          );
        })}
      </nav>

      {/* Desktop-only Side Cards */}
      <div className="hidden lg:flex lg:flex-col lg:gap-5">
        <OracleStatusCard
          statusDetail={statusDetailData}
          selectedSeason={selectedSeason}
          selectedGW={selectedGW}
        />
        <ChelseaHubCard selectedSeason={selectedSeason} selectedGW={selectedGW} />
        <DeveloperProfileCard />
      </div>
    </aside>
  );
}
