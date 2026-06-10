import ClayCard from '@/app/components/ClayCard';

export default function TeamPage() {
  return (
    <div className="space-y-12">
      <div className="space-y-3">
        <h1 className="text-5xl font-bold bg-gradient-to-r from-blue-700 to-cyan-600 bg-clip-text text-transparent">
          Team Analysis
        </h1>
        <p className="text-lg text-gray-600 font-medium">
          Analyze team performance metrics and strategic insights
        </p>
      </div>

      <ClayCard title="Team Data" className="min-h-96 flex flex-col justify-center items-center">
        <div className="text-center space-y-3">
          <p className="text-gray-500 text-lg font-medium">
            Team performance analysis
          </p>
          <p className="text-gray-400 text-sm">
            In-depth team statistics and insights coming soon
          </p>
        </div>
      </ClayCard>
    </div>
  );
}
