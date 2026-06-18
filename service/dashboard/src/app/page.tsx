import SeasonSelector from './components/SeasonSelector';
import GameweekSelector from './components/GameweekSelector';
import ClayCard from './components/ClayCard';

export default function Home() {
    return (
        <div className="space-y-12">
            {/* Header */}
            <div className="space-y-3">
                <h1 className="text-5xl font-bold bg-gradient-to-r from-blue-700 to-cyan-600 bg-clip-text text-transparent">
                    FPL‑Oracle Dashboard
                </h1>
                <p className="text-base text-gray-600 font-medium">
                    Advanced analytics and insights for Fantasy Premier League
                </p>
            </div>

            {/* Selectors Grid with extra bottom margin for dropdown space */}
            <div className="grid grid-cols-2 gap-4 pb-20 md:pb-16 relative z-20">
                <SeasonSelector />
                <GameweekSelector />
            </div>

            {/* Analytics Placeholder */}
            <div className="grid grid-cols-1 gap-2 relative z-0">
                <ClayCard title="Analytics & Insights" className="min-h-96 flex flex-col justify-center items-center">
                    <div className="text-center space-y-3">
                        <p className="text-gray-500 text-lg font-medium">
                            Select a season and gameweek to view analytics
                        </p>
                        <p className="text-gray-400 text-sm">
                            Player statistics, performance metrics, and team analysis coming soon
                        </p>
                    </div>
                </ClayCard>
            </div>
        </div>
    );
}
