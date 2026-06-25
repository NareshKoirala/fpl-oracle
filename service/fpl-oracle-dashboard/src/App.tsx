/**
 * FILE: /src/App.tsx
 * PURPOSE: The orchestrator and layout root of the FPL Oracle Dashboard (React 19, Vite, Tailwind v4).
 * USAGE: Renders the sidebar navigation, header, theme layout, dynamic view switching, and contains season/gameweek states.
 *        It fetches the processed datasets synchronously and transfers them to the sub-views.
 */

import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "motion/react";
import { 
  ExternalLink,
  Award
} from "lucide-react";

import { allDataStructure } from "./data/all_data_structure";
import { CombinedFixture, ProcTeamStrength, CombinedTeam, CombinedPlayer } from "./data/types";

import { getFixtures } from "./data/fixtures";
import { getTeamsStrength } from "./data/teams_strength";
import { getTeamsRaw } from "./data/teams_raw";
import { getPlayers } from "./data/players";
import { getStatusDetail } from "./data/status_detail";

import DashboardView from "./components/DashboardView";
import FixturesView from "./components/FixturesView";
import ProcessedView from "./components/ProcessedView";
import PlayersView from "./components/PlayersView";
import SearchView from "./components/SearchView";
import StandingsView from "./components/StandingsView";
import PredictionCenterCard from "./components/PredictionCenterCard";
import ChelseaHubCard from "./components/ChelseaHubCard";
import DeveloperProfileCard from "./components/DeveloperProfileCard";
import NavigationSidebar from "./components/NavigationSidebar";
import ViewSkeleton from "./components/ViewSkeleton";

type ViewType = "dashboard" | "fixtures" | "processed" | "players" | "search" | "standings";

export default function App() {
  const [activeView, setActiveView] = useState<ViewType>("dashboard");
  const [selectedSeason, setSelectedSeason] = useState("2025");
  const [selectedGW, setSelectedGW] = useState(38);
  const [loading, setLoading] = useState(false);

  const statusDetailData = getStatusDetail(selectedSeason, selectedGW);

  // Loaded data states (retrieved via exported const functions)
  const [fixtures, setFixtures] = useState<CombinedFixture[]>([]);
  const [teamsStrength, setTeamsStrength] = useState<ProcTeamStrength[]>([]);
  const [teamsRaw, setTeamsRaw] = useState<CombinedTeam[]>([]);
  const [players, setPlayers] = useState<CombinedPlayer[]>([]);

  useEffect(() => {
    const targetSeason = allDataStructure.seasons.find(s => s.id === selectedSeason) || allDataStructure.seasons[0];
    if (!targetSeason.gameweeks.includes(selectedGW)) {
      setSelectedGW(targetSeason.gameweeks[0]);
    }
  }, [selectedSeason]);

  useEffect(() => {
    setLoading(true);
    try {
      const fixturesData = getFixtures(selectedSeason, selectedGW);
      const strengthData = getTeamsStrength(selectedSeason, selectedGW);
      const rawData = getTeamsRaw(selectedSeason, selectedGW);
      const playersData = getPlayers(selectedSeason, selectedGW);

      setFixtures(fixturesData || []);
      setTeamsStrength(strengthData || []);
      setTeamsRaw(rawData || []);
      setPlayers(playersData || []);
    } catch (error) {
      console.error("Error loading data from exported functions:", error);
    } finally {
      setLoading(false);
    }
  }, [selectedSeason, selectedGW]);


  const targetSeason = allDataStructure.seasons.find(s => s.id === selectedSeason) || allDataStructure.seasons[0];

  // Render view conditionally helper
  const renderActiveView = () => {
    switch (activeView) {
      case "dashboard":
        return (
          <DashboardView 
            selectedSeason={selectedSeason} 
            selectedGW={selectedGW} 
            setSelectedSeason={setSelectedSeason} 
            setSelectedGW={setSelectedGW} 
            fixtures={fixtures}
            teams={teamsRaw}
          />
        );
      case "fixtures":
        return <FixturesView selectedSeason={selectedSeason} selectedGW={selectedGW} fixtures={fixtures} />;
      case "processed":
        return <ProcessedView selectedSeason={selectedSeason} selectedGW={selectedGW} players={players} teams={teamsRaw} />;
      case "players":
        return <PlayersView selectedSeason={selectedSeason} selectedGW={selectedGW} players={players} />;
      case "standings":
        return <StandingsView selectedSeason={selectedSeason} selectedGW={selectedGW} teamsRaw={teamsRaw} />;
      case "search":
        return (
          <SearchView 
            selectedSeason={selectedSeason} 
            selectedGW={selectedGW} 
            fixtures={fixtures}
            teamsRaw={teamsRaw}
            players={players}
          />
        );
      default:
        return (
          <DashboardView 
            selectedSeason={selectedSeason} 
            selectedGW={selectedGW} 
            setSelectedSeason={setSelectedSeason} 
            setSelectedGW={setSelectedGW} 
            fixtures={fixtures}
            teams={teamsRaw}
          />
        );
    }
  };

  return (
    <div className="min-h-screen bg-[#0a0a0b] text-[#e2e2e4] flex flex-col font-sans selection:bg-[#00ff85]/20 selection:text-[#00ff85]">
      
      {/* GLOWING SPACE ACCENT DESIGN */}
      <div className="absolute top-0 left-0 w-full h-[500px] bg-gradient-to-b from-[#00ff85]/[0.02] via-[#00ff85]/[0.005] to-transparent pointer-events-none" />

      {/* STICKY GLASS HEADER */}
      <header className="sticky top-0 z-50 border-b border-white/5 bg-[#0a0a0b]/80 backdrop-blur-md">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-18 flex items-center justify-between">
          
          {/* Logo Brand */}
          <div className="flex items-center gap-3">
            <div className="h-10 w-10 fpl-bg-accent rounded-xl flex items-center justify-center text-[#37003c] font-black text-xl italic select-none shadow-[0_0_15px_rgba(0,255,133,0.3)]">
              O
            </div>
            <div>
              <h1 className="text-lg font-bold tracking-tight italic text-white flex items-center gap-1 leading-none">
                FPL<span className="fpl-accent">ORACLE</span>
              </h1>
              <span className="text-[10px] font-bold text-white/40 block mt-0.5 tracking-wider uppercase font-mono">Predictive Engine</span>
            </div>
          </div>

          {/* Core Analytics Status - Accuracy indicator only */}
          <div className="hidden sm:flex items-center gap-3 text-xs font-mono">
            <div className="flex items-center gap-1.5 bg-white/5 hover:bg-white/10 transition duration-150 px-3 py-1.5 rounded-full border border-white/5">
              <Award className="h-3.5 w-3.5 text-yellow-500" />
              <span className="text-white/60">Oracle Accuracy: <b className="text-white font-semibold">94.6%</b></span>
            </div>
          </div>

        </div>
      </header>

      {/* MASTER PAGE NAVIGATION HUB */}
      <div className="max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-8 flex-1 flex flex-col lg:flex-row gap-8">
        
        {/* SIDE BAR / NAV PANEL */}
        <NavigationSidebar
          activeView={activeView}
          setActiveView={setActiveView}
          statusDetailData={statusDetailData}
          selectedSeason={selectedSeason}
          selectedGW={selectedGW}
        />

        {/* CORE WORKPLACE AREA FOR ACTIVATED TAB VIEW */}
        <main className="flex-1 min-w-0 pb-8 space-y-6">
          {/* Upper Selector Panel in all pages - cleanly refactored */}
          <PredictionCenterCard
            selectedSeason={selectedSeason}
            selectedGW={selectedGW}
            setSelectedSeason={setSelectedSeason}
            setSelectedGW={setSelectedGW}
          />

          <AnimatePresence mode="wait">
            <motion.div
              key={activeView + (loading ? "-loading" : "-loaded")}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              transition={{ duration: 0.2 }}
            >
              {loading ? (
                <ViewSkeleton activeView={activeView} />
              ) : (
                renderActiveView()
              )}
            </motion.div>
          </AnimatePresence>

          {/* Mobile-only Side Cards shown at the very end of the page */}
          <div className="block lg:hidden mt-8 space-y-5">
            <ChelseaHubCard selectedSeason={selectedSeason} selectedGW={selectedGW} />
            <DeveloperProfileCard />
          </div>
        </main>

      </div>

      {/* FOOTER */}
      <footer className="border-t border-white/5 bg-[#0a0a0b] mt-16 text-white/40 py-10 text-xs">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row justify-between items-center gap-6">
          <div className="flex items-center gap-2">
            <div className="h-6 w-6 rounded-md fpl-bg-accent flex items-center justify-center text-[#37003c] font-bold text-xs italic">O</div>
            <span>FPL-Oracle Analytics Dashboard • Stable 2026 Edition</span>
          </div>

          <div className="flex items-center gap-4">
            <span>Built using Outfit typography</span>
            <span className="text-white/10">|</span>
            <span className="flex items-center gap-1 text-white/60 hover:text-white transition cursor-pointer">
              FPL Data API Schema v2 <ExternalLink className="h-3 w-3" />
            </span>
          </div>
        </div>
      </footer>

    </div>
  );
}

