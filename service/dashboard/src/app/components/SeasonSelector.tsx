'use client';

import { useState } from 'react';
import ClayCard from './ClayCard';

interface Season {
  id: string;
  label: string;
}

const SEASONS: Season[] = [
  { id: 'current', label: 'Current Season' },
  { id: '2025-26', label: '2025–26' },
  { id: '2024-25', label: '2024–25' },
  { id: '2023-24', label: '2023–24' },
  { id: '2022-23', label: '2022–23' },
  { id: '2021-22', label: '2021–22' },
  { id: '2020-21', label: '2020–21' },
];

export default function SeasonSelector() {
  const [isOpen, setIsOpen] = useState(false);
  const [selected, setSelected] = useState(SEASONS[0]);

  const handleSelect = (season: Season) => {
    setSelected(season);
    setIsOpen(false);
  };

  return (
    <ClayCard title="Season" compact>
      <div className="relative w-full">
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="w-full clay-input flex items-center justify-between text-left cursor-pointer active:scale-95"
        >
          <span className="font-semibold text-gray-800">{selected.label}</span>
          <svg
            className={`w-5 h-5 text-blue-600 transition-transform duration-300 flex-shrink-0 ${
              isOpen ? 'rotate-180' : ''
            }`}
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M19 14l-7 7m0 0l-7-7m7 7V3"
            />
          </svg>
        </button>

        {isOpen && (
          <div className="absolute top-full left-0 right-0 mt-4 bg-white/95 backdrop-blur-md rounded-2xl shadow-2xl border border-blue-200/40 z-50 overflow-hidden">
            <div className="max-h-64 overflow-y-auto">
              {SEASONS.map((season) => (
                <button
                  key={season.id}
                  onClick={() => handleSelect(season)}
                  className={`w-full px-5 py-4 text-left font-medium transition-all duration-200 border-b border-blue-100/30 last:border-b-0 ${
                    selected.id === season.id
                      ? 'bg-gradient-to-r from-blue-100 to-cyan-100 text-blue-700 font-semibold'
                      : 'text-gray-700 hover:bg-blue-50/60'
                  }`}
                >
                  {season.label}
                </button>
              ))}
            </div>
          </div>
        )}
      </div>
    </ClayCard>
  );
}
