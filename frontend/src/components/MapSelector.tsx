import React, { useState, useMemo } from 'react';
import type { OverwatchMap } from '../types/overwatch';
import { MapPin, ChevronDown } from 'lucide-react';

interface MapSelectorProps {
  maps: OverwatchMap[];
  selectedMap: OverwatchMap | null;
  onSelect: (map: OverwatchMap | null) => void;
}

export const MapSelector: React.FC<MapSelectorProps> = ({
  maps,
  selectedMap,
  onSelect,
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const [search, setSearch] = useState('');

  const filteredMaps = useMemo(() => {
    return maps.filter((map) =>
      map.name.toLowerCase().includes(search.toLowerCase())
    );
  }, [maps, search]);

  return (
    <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
      <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
        <MapPin className="w-5 h-5" />
        Map (optional)
      </h2>

      <div className="relative">
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="w-full flex items-center justify-between px-4 py-3 bg-gray-900 border border-gray-700 rounded-lg text-white hover:border-overwatch-orange transition-colors"
        >
          <span className={selectedMap ? 'text-white' : 'text-gray-500'}>
            {selectedMap ? selectedMap.name : 'Select a map...'}
          </span>
          <ChevronDown className={`w-5 h-5 transition-transform ${isOpen ? 'rotate-180' : ''}`} />
        </button>

        {isOpen && (
          <div className="absolute z-10 w-full mt-2 bg-gray-900 border border-gray-700 rounded-lg shadow-xl max-h-64 overflow-hidden">
            <div className="p-2 border-b border-gray-700">
              <input
                type="text"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="Search map..."
                className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded text-white placeholder-gray-500 focus:outline-none focus:border-overwatch-orange text-sm"
              />
            </div>
            <div className="overflow-y-auto max-h-48">
              {filteredMaps.map((map) => (
                <button
                  key={map.name}
                  onClick={() => {
                    onSelect(map);
                    setIsOpen(false);
                    setSearch('');
                  }}
                  className={`w-full px-4 py-2 text-left hover:bg-gray-800 transition-colors ${
                    selectedMap?.name === map.name ? 'bg-gray-800 text-overwatch-orange' : 'text-white'
                  }`}
                >
                  {map.name}
                </button>
              ))}
              {filteredMaps.length === 0 && (
                <div className="px-4 py-3 text-gray-500 text-sm text-center">
                  No maps found
                </div>
              )}
            </div>
          </div>
        )}
      </div>

      {selectedMap && (
        <div className="mt-4">
          <img
            src={selectedMap.screenshot}
            alt={selectedMap.name}
            className="w-full h-32 object-cover rounded-lg border border-gray-700"
          />
          <div className="mt-2 text-sm text-gray-400">
            {selectedMap.gamemodes.map((mode) => mode.toUpperCase()).join(' • ')}
          </div>
        </div>
      )}
    </div>
  );
};
