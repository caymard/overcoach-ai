import React from 'react';
import type { Hero } from '../types/overwatch';
import { Shield, Swords, Heart } from 'lucide-react';

interface HeroSlotProps {
  hero: Hero | null;
  role: 'tank' | 'damage' | 'support';
  onClick: () => void;
}

const roleIcons = {
  tank: Shield,
  damage: Swords,
  support: Heart,
};

const roleColors = {
  tank: 'bg-overwatch-tank',
  damage: 'bg-overwatch-damage',
  support: 'bg-overwatch-support',
};

export const HeroSlot: React.FC<HeroSlotProps> = ({ hero, role, onClick }) => {
  const Icon = roleIcons[role];

  return (
    <div
      onClick={onClick}
      className="flex flex-col items-center cursor-pointer group"
    >
      <div
        className={`
          w-24 h-24 rounded-lg flex items-center justify-center
          transition-all duration-200 border-2
          ${hero ? 'border-gray-600' : 'border-gray-700 border-dashed'}
          ${!hero && 'hover:border-gray-500 hover:bg-gray-800/50'}
          ${hero && 'hover:scale-105'}
          bg-gray-900
        `}
      >
        {hero ? (
          <img
            src={hero.portrait}
            alt={hero.name}
            className="w-full h-full object-cover rounded-lg"
          />
        ) : (
          <Icon className={`w-10 h-10 text-gray-600 group-hover:text-gray-500`} />
        )}
      </div>
      <div className="mt-2 text-center">
        {hero ? (
          <>
            <p className="text-sm font-medium text-white">{hero.name}</p>
            <p className={`text-xs ${roleColors[role].replace('bg-', 'text-')}`}>
              {role.toUpperCase()}
            </p>
          </>
        ) : (
          <p className="text-xs text-gray-600 uppercase">{role}</p>
        )}
      </div>
    </div>
  );
};
