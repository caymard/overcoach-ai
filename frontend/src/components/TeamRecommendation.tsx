import React from 'react';
import type { HeroRecommendation, Hero } from '../types/overwatch';
import { Shield, Swords, Heart, AlertCircle, Sparkles } from 'lucide-react';

interface TeamRecommendationProps {
  recommendations: HeroRecommendation[];
  heroes: Hero[];
}

const roleIcons = {
  tank: Shield,
  damage: Swords,
  support: Heart,
};

const roleColors = {
  tank: 'text-overwatch-tank',
  damage: 'text-overwatch-damage',
  support: 'text-overwatch-support',
};

export const TeamRecommendation: React.FC<TeamRecommendationProps> = ({ recommendations, heroes }) => {
  if (recommendations.length === 0) {
    return null;
  }

  // Check if parsing failed
  const parsingFailed = recommendations[0]?.name.includes('Parsing failed');

  // Helper function to find hero portrait
  const findHeroPortrait = (heroName: string): string | null => {
    const hero = heroes.find(
      (h) => h.name.toLowerCase() === heroName.toLowerCase()
    );
    return hero ? hero.portrait : null;
  };

  return (
    <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
      <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-2">
        <Sparkles className="w-6 h-6 text-overwatch-orange" />
        Recommended Team
      </h2>

      {parsingFailed ? (
        <div className="bg-yellow-900/30 border border-yellow-700 rounded-lg p-4 flex items-start gap-3">
          <AlertCircle className="w-5 h-5 text-yellow-500 flex-shrink-0 mt-0.5" />
          <div className="text-yellow-200 text-sm">
            Unable to parse the response format. Please check the raw response below for the full recommendation.
          </div>
        </div>
      ) : (
        <div className="grid grid-cols-5 gap-4">
          {recommendations.map((hero, index) => {
            const roleKey = hero.role.toLowerCase() as keyof typeof roleIcons;
            const Icon = roleIcons[roleKey] || Swords;
            const colorClass = roleColors[roleKey] || roleColors.damage;
            const portrait = findHeroPortrait(hero.name);

            return (
              <div key={index} className="flex flex-col items-center">
                <div className="w-24 h-24 bg-gray-900 rounded-lg overflow-hidden flex items-center justify-center border-2 border-gray-700 mb-2">
                  {portrait ? (
                    <img
                      src={portrait}
                      alt={hero.name}
                      className="w-full h-full object-cover"
                    />
                  ) : (
                    <Icon className={`w-12 h-12 ${colorClass}`} />
                  )}
                </div>
                <p className="text-sm font-bold text-white text-center">{hero.name}</p>
                <p className={`text-xs ${colorClass} uppercase mb-2`}>{hero.role}</p>
                <p className="text-xs text-gray-400 text-center leading-relaxed">
                  {hero.reasoning}
                </p>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};
