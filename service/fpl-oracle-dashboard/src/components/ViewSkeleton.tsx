/**
 * FILE: /src/components/ViewSkeleton.tsx
 * PURPOSE: Renders fluid loading placeholders matching the custom layouts of each active tab design.
 * USAGE: Rendered as a transition/loading state wrapper inside /src/App.tsx.
 */

interface ViewSkeletonProps {
  activeView: "dashboard" | "fixtures" | "processed" | "players" | "standings" | "search";
}

export default function ViewSkeleton({ activeView }: ViewSkeletonProps) {
  return (
    <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
      {activeView === "dashboard" ? (
        <>
          {/* Skeletal placeholders for realistic Apple Fitness/Premium load */}
          <div className="col-span-12 lg:col-span-9 h-[500px] bg-white/[0.02] border border-white/5 rounded-3xl animate-pulse flex items-center justify-center">
            <span className="text-white/30 font-mono text-sm tracking-widest uppercase">LOADING FPL PITCH MODEL...</span>
          </div>
          <div className="col-span-12 lg:col-span-3 space-y-6">
            <div className="h-[240px] bg-white/[0.02] border border-white/5 rounded-3xl animate-pulse flex items-center justify-center">
              <span className="text-white/20 font-mono text-xs tracking-wider uppercase">Loading analytics...</span>
            </div>
            <div className="h-[240px] bg-white/[0.02] border border-white/5 rounded-3xl animate-pulse"></div>
          </div>
        </>
      ) : activeView === "fixtures" ? (
        <>
          <div className="col-span-12 lg:col-span-4 h-[550px] bg-white/[0.02] border border-white/5 rounded-3xl animate-pulse flex items-center justify-center">
            <span className="text-white/30 font-mono text-xs tracking-wider uppercase">Loading Fixtures...</span>
          </div>
          <div className="col-span-12 lg:col-span-8 h-[550px] bg-white/[0.02] border border-white/5 rounded-3xl animate-pulse flex items-center justify-center">
            <span className="text-white/30 font-mono text-xs tracking-wider uppercase">Evaluating Simulation...</span>
          </div>
        </>
      ) : activeView === "processed" ? (
        <div className="col-span-12 space-y-5">
          <div className="h-16 bg-white/[0.02] border border-white/5 rounded-2xl animate-pulse"></div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div className="h-44 bg-white/[0.02] border border-white/5 rounded-3xl animate-pulse flex items-center justify-center">
              <span className="text-white/20 font-mono text-xs tracking-wider uppercase">Loading processed index...</span>
            </div>
            <div className="h-44 bg-white/[0.02] border border-white/5 rounded-3xl animate-pulse"></div>
            <div className="h-44 bg-white/[0.02] border border-white/5 rounded-3xl animate-pulse"></div>
          </div>
        </div>
      ) : activeView === "players" ? (
        <>
          <div className="col-span-12 lg:col-span-3 h-[450px] bg-white/[0.02] border border-white/5 rounded-3xl animate-pulse"></div>
          <div className="col-span-12 lg:col-span-9 space-y-4">
            <div className="h-14 bg-white/[0.02] border border-white/5 rounded-2xl animate-pulse"></div>
            <div className="h-[380px] bg-white/[0.02] border border-white/5 rounded-3xl animate-pulse flex items-center justify-center">
              <span className="text-white/20 font-mono text-xs tracking-wider uppercase">Loading player datasets...</span>
            </div>
          </div>
        </>
      ) : activeView === "standings" ? (
        <div className="col-span-12 space-y-6">
          <div className="h-14 bg-white/[0.02] border border-white/5 rounded-2xl animate-pulse"></div>
          <div className="h-[400px] bg-white/[0.02] border border-white/5 rounded-3xl animate-pulse flex items-center justify-center">
            <span className="text-white/20 font-mono text-xs tracking-wider uppercase">Loading league tables...</span>
          </div>
        </div>
      ) : (
        <div className="col-span-12 space-y-6">
          <div className="h-14 bg-white/[0.02] border border-white/5 rounded-2xl animate-pulse"></div>
          <div className="h-[300px] bg-white/[0.02] border border-white/5 rounded-3xl animate-pulse flex items-center justify-center">
            <span className="text-white/20 font-mono text-xs tracking-wider uppercase">Querying models...</span>
          </div>
        </div>
      )}
    </div>
  );
}
