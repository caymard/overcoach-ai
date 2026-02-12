import React, { useState, useMemo } from 'react';
import type { Hero } from '../types/overwatch';
import { X, Search } from 'lucide-react';

interface HeroSearchProps {
  heroes: Hero[];
  onSelect: (hero: Hero) => void;
  onClose: () => void;
  filterRole?: 'tank' | 'damage' | 'support';
}

export const HeroSearch: React.FC<HeroSearchProps> = ({
  heroes,
  onSelect,
  onClose,
  filterRole,
}) => {
  const [search, setSearch] = useState('');

  const filteredHeroes = useMemo(() => {
    return heroes.filter((hero) => {
      const matchesSearch = hero.name.toLowerCase().includes(search.toLowerCase());
      const matchesRole = !filterRole || hero.role === filterRole;
      return matchesSearch && matchesRole;
    });
  }, [heroes, search, filterRole]);

  return (
    <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4">
      <div className="bg-gray-900 rounded-xl max-w-2xl w-full max-h-[80vh] overflow-hidden border border-gray-700 shadow-2xl">
        {/* Header */}
        <div className="p-4 border-b border-gray-700 flex items-center justify-between bg-gray-800">
          <h3 className="text-xl font-bold text-white">
            Select {filterRole ? filterRole.toUpperCase() : 'Hero'}
          </h3>
          <button
            onClick={onClose}
            className="p-2 hover:bg-gray-700 rounded-lg transition-colors"
          >
            <X className="w-5 h-5 text-gray-400" />
          </button>
        </div>

        {/* Search */}
        <div className="p-4 border-b border-gray-700">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-500" />
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search hero..."
              className="w-full pl-10 pr-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-overwatch-orange transition-colors"
              autoFocus
            />
          </div>
        </div>

        {/* Heroes Grid */}
        <div className="p-4 overflow-y-auto max-h-96">
          <div className="grid grid-cols-4 gap-3">
            {filteredHeroes.map((hero) => (
              <button
                key={hero.key}
                onClick={() => {
                  onSelect(hero);
                  onClose();
                }}
                className="group relative aspect-square rounded-lg overflow-hidden border-2 border-gray-700 hover:border-overwatch-orange transition-all hover:scale-105"
              >
                <img
                  src={hero.portrait}
                  alt={hero.name}
                  className="w-full h-full object-cover"
                />
                <div className="absolute inset-x-0 bottom-0 bg-gradient-to-t from-black/90 to-transparent p-2">
                  <p className="text-xs font-medium text-white text-center">
                    {hero.name}
                  </p>
                </div>
              </button>
            ))}
          </div>
          {filteredHeroes.length === 0 && (
            <div className="text-center py-8 text-gray-500">
              No heroes found
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
