import React, { useState } from 'react';
import type { Hero, TeamState, TeamSlot } from '../types/overwatch';
import { HeroSlot } from './HeroSlot';
import { HeroSearch } from './HeroSearch';

interface HeroSelectorProps {
  title: string;
  teamState: TeamState;
  onHeroSelect: (slot: TeamSlot, hero: Hero | null) => void;
  heroes: Hero[];
}

export const HeroSelector: React.FC<HeroSelectorProps> = ({
  title,
  teamState,
  onHeroSelect,
  heroes,
}) => {
  const [searchOpen, setSearchOpen] = useState(false);
  const [selectedSlot, setSelectedSlot] = useState<TeamSlot | null>(null);

  const handleSlotClick = (slot: TeamSlot) => {
    setSelectedSlot(slot);
    setSearchOpen(true);
  };

  const handleHeroSelect = (hero: Hero) => {
    if (selectedSlot) {
      onHeroSelect(selectedSlot, hero);
    }
  };

  const getRoleForSlot = (slot: TeamSlot): 'tank' | 'damage' | 'support' => {
    if (slot === 'tank') return 'tank';
    if (slot === 'damage1' || slot === 'damage2') return 'damage';
    return 'support';
  };

  return (
    <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
      <h2 className="text-xl font-bold text-white mb-4">{title}</h2>
      <div className="flex gap-4 justify-center flex-wrap">
        <HeroSlot
          hero={teamState.tank}
          role="tank"
          onClick={() => handleSlotClick('tank')}
        />
        <HeroSlot
          hero={teamState.damage1}
          role="damage"
          onClick={() => handleSlotClick('damage1')}
        />
        <HeroSlot
          hero={teamState.damage2}
          role="damage"
          onClick={() => handleSlotClick('damage2')}
        />
        <HeroSlot
          hero={teamState.support1}
          role="support"
          onClick={() => handleSlotClick('support1')}
        />
        <HeroSlot
          hero={teamState.support2}
          role="support"
          onClick={() => handleSlotClick('support2')}
        />
      </div>

      {searchOpen && selectedSlot && (
        <HeroSearch
          heroes={heroes}
          onSelect={handleHeroSelect}
          onClose={() => setSearchOpen(false)}
          filterRole={getRoleForSlot(selectedSlot)}
        />
      )}
    </div>
  );
};
