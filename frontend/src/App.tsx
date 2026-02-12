import { useState, useEffect } from 'react';
import type { Hero, OverwatchMap, TeamState, TeamSlot, TeamCompositionResponse } from './types/overwatch';
import { overfastApi } from './services/overfastApi';
import { overcoachApi } from './services/overcoachApi';
import { HeroSelector } from './components/HeroSelector';
import { MapSelector } from './components/MapSelector';
import { DifficultyInput } from './components/DifficultyInput';
import { CoachButton } from './components/CoachButton';
import { TeamRecommendation } from './components/TeamRecommendation';
import { StrategyDisplay } from './components/StrategyDisplay';
import { Loader2, AlertCircle } from 'lucide-react';

const emptyTeam: TeamState = {
  tank: null,
  damage1: null,
  damage2: null,
  support1: null,
  support2: null,
};

function App() {
  const [heroes, setHeroes] = useState<Hero[]>([]);
  const [maps, setMaps] = useState<OverwatchMap[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [enemyTeam, setEnemyTeam] = useState<TeamState>(emptyTeam);
  const [myTeam, setMyTeam] = useState<TeamState>(emptyTeam);
  const [selectedMap, setSelectedMap] = useState<OverwatchMap | null>(null);
  const [difficulty, setDifficulty] = useState('');

  const [suggesting, setSuggesting] = useState(false);
  const [suggestion, setSuggestion] = useState<TeamCompositionResponse | null>(null);

  // Load heroes and maps on mount
  useEffect(() => {
    const loadData = async () => {
      try {
        setLoading(true);
        const [heroesData, mapsData] = await Promise.all([
          overfastApi.getHeroes(),
          overfastApi.getMaps(),
        ]);
        setHeroes(heroesData);
        setMaps(mapsData);
        setError(null);
      } catch (err) {
        setError('Failed to load data from OverFast API');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, []);

  const handleEnemyHeroSelect = (slot: TeamSlot, hero: Hero | null) => {
    setEnemyTeam((prev) => ({ ...prev, [slot]: hero }));
  };

  const handleMyHeroSelect = (slot: TeamSlot, hero: Hero | null) => {
    setMyTeam((prev) => ({ ...prev, [slot]: hero }));
  };

  const teamToArray = (team: TeamState): string[] => {
    return Object.values(team)
      .filter((hero): hero is Hero => hero !== null)
      .map((hero) => hero.name);
  };

  const handleSuggest = async () => {
    try {
      setSuggesting(true);
      setSuggestion(null);

      const request = {
        map_name: selectedMap?.name || undefined,
        enemy_team: teamToArray(enemyTeam),
        current_team: teamToArray(myTeam),
        difficulties: difficulty || undefined,
      };

      const response = await overcoachApi.suggestTeam(request);
      setSuggestion(response);
    } catch (err) {
      setError('Failed to get suggestion from Coach AI');
      console.error(err);
    } finally {
      setSuggesting(false);
    }
  };

  const canSuggest = teamToArray(enemyTeam).length > 0;

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <Loader2 className="w-12 h-12 animate-spin text-overwatch-orange mx-auto mb-4" />
          <p className="text-white text-lg">Loading Overwatch data...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen py-8 px-4">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-5xl font-bold text-white mb-2 bg-gradient-to-r from-overwatch-orange to-overwatch-blue bg-clip-text text-transparent">
            Overcoach AI
          </h1>
          <p className="text-gray-400 text-lg">Your Overwatch Team Composition Coach</p>
        </div>

        {error && (
          <div className="mb-6 bg-red-900/30 border border-red-700 rounded-lg p-4 flex items-start gap-3">
            <AlertCircle className="w-5 h-5 text-red-500 flex-shrink-0 mt-0.5" />
            <div>
              <p className="text-red-200 font-medium">Error</p>
              <p className="text-red-300 text-sm">{error}</p>
            </div>
          </div>
        )}

        <div className="space-y-6 mb-8">
          <HeroSelector
            title="Enemy Team (required)"
            teamState={enemyTeam}
            onHeroSelect={handleEnemyHeroSelect}
            heroes={heroes}
          />

          <HeroSelector
            title="Your Team (optional)"
            teamState={myTeam}
            onHeroSelect={handleMyHeroSelect}
            heroes={heroes}
          />

          <MapSelector
            maps={maps}
            selectedMap={selectedMap}
            onSelect={setSelectedMap}
          />

          <DifficultyInput value={difficulty} onChange={setDifficulty} />

          <CoachButton
            onClick={handleSuggest}
            loading={suggesting}
            disabled={!canSuggest}
          />

          {!canSuggest && (
            <p className="text-center text-gray-500 text-sm">
              Please select at least one enemy hero to get suggestions
            </p>
          )}
        </div>

        {suggestion && (
          <div className="space-y-6">
            <TeamRecommendation 
              recommendations={suggestion.recommended_team}
              heroes={heroes}
            />
            <StrategyDisplay
              strategy={suggestion.strategy}
              synergies={suggestion.synergies}
            />

            {suggestion.raw_response && (
              <details className="bg-gray-800 rounded-xl p-6 border border-gray-700">
                <summary className="text-white font-bold cursor-pointer">
                  View Raw Response
                </summary>
                <pre className="mt-4 text-sm text-gray-400 whitespace-pre-wrap">
                  {suggestion.raw_response}
                </pre>
              </details>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
