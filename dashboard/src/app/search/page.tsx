import ClayCard from '@/app/components/ClayCard';

export default function SearchPage() {
  return (
    <div className="space-y-12">
      <div className="space-y-3">
        <h1 className="text-5xl font-bold bg-gradient-to-r from-blue-700 to-cyan-600 bg-clip-text text-transparent">
          Search
        </h1>
        <p className="text-lg text-gray-600 font-medium">
          Find players and compare statistics across different criteria
        </p>
      </div>

      <ClayCard title="Search Results" className="min-h-96 flex flex-col justify-center items-center">
        <div className="text-center space-y-3">
          <p className="text-gray-500 text-lg font-medium">
            Advanced search functionality
          </p>
          <p className="text-gray-400 text-sm">
            Search and filter players by name, team, position, and more coming soon
          </p>
        </div>
      </ClayCard>
    </div>
  );
}
