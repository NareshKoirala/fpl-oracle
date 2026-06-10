import ClayCard from '@/app/components/ClayCard';

export default function TablePage() {
  return (
    <div className="space-y-12">
      <div className="space-y-3">
        <h1 className="text-5xl font-bold bg-gradient-to-r from-blue-700 to-cyan-600 bg-clip-text text-transparent">
          Player Table
        </h1>
        <p className="text-lg text-gray-600 font-medium">
          Browse and compare player statistics across seasons and gameweeks
        </p>
      </div>

      <ClayCard title="Player Data" className="min-h-96 flex flex-col justify-center items-center">
        <div className="text-center space-y-3">
          <p className="text-gray-500 text-lg font-medium">
            Comprehensive player statistics
          </p>
          <p className="text-gray-400 text-sm">
            Detailed player performance metrics coming soon
          </p>
        </div>
      </ClayCard>
    </div>
  );
}
