import ClayCard from '@/app/components/ClayCard';

export default function FixturePage() {
  return (
    <div className="space-y-12">
      <div className="space-y-3">
        <h1 className="text-5xl font-bold bg-gradient-to-r from-blue-700 to-cyan-600 bg-clip-text text-transparent">
          Fixtures
        </h1>
        <p className="text-lg text-gray-600 font-medium">
          View upcoming matches and fixture schedules
        </p>
      </div>

      <ClayCard title="Fixture Schedule" className="min-h-96 flex flex-col justify-center items-center">
        <div className="text-center space-y-3">
          <p className="text-gray-500 text-lg font-medium">
            Fixture information and schedules
          </p>
          <p className="text-gray-400 text-sm">
            Upcoming matches and detailed fixture analysis coming soon
          </p>
        </div>
      </ClayCard>
    </div>
  );
}
