'use client';

import { useState } from 'react';
import ClayCard from './ClayCard';

interface Gameweek {
  id: number;
  label: string;
}

const GAMEWEEKS: Gameweek[] = Array.from({ length: 38 }, (_, i) => ({
  id: i + 1,
  label: i === 0 ? 'Current (GW 1)' : `GW ${i + 1}`,
}));

export default function GameweekSelector() {
  const [isOpen, setIsOpen] = useState(false);
  const [selected, setSelected] = useState(GAMEWEEKS[0]);

  const handleSelect = (gw: Gameweek) => {
    setSelected(gw);
    setIsOpen(false);
  };

  return (
    <ClayCard title="Gameweek" compact>
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
              {GAMEWEEKS.map((gw) => (
                <button
                  key={gw.id}
                  onClick={() => handleSelect(gw)}
                  className={`w-full px-5 py-4 text-left font-medium transition-all duration-200 border-b border-blue-100/30 last:border-b-0 ${
                    selected.id === gw.id
                      ? 'bg-gradient-to-r from-blue-100 to-cyan-100 text-blue-700 font-semibold'
                      : 'text-gray-700 hover:bg-blue-50/60'
                  }`}
                >
                  {gw.label}
                </button>
              ))}
            </div>
          </div>
        )}
      </div>
    </ClayCard>
  );
}
