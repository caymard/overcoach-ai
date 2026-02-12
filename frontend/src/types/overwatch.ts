// Overwatch data types

export interface Hero {
  key: string;
  name: string;
  portrait: string;
  role: 'tank' | 'damage' | 'support';
}

export interface OverwatchMap {
  name: string;
  screenshot: string;
  gamemodes: string[];
  location?: string;
}

export interface HeroRecommendation {
  name: string;
  role: string;
  reasoning: string;
}

export interface TeamCompositionResponse {
  recommended_team: HeroRecommendation[];
  strategy: string;
  synergies: string;
  alternatives: string[];
  raw_response: string;
}

export interface TeamCompositionRequest {
  map_name?: string;
  enemy_team: string[];
  current_team: string[];
  difficulties?: string;
}

export type TeamSlot = 'tank' | 'damage1' | 'damage2' | 'support1' | 'support2';

export interface TeamState {
  tank: Hero | null;
  damage1: Hero | null;
  damage2: Hero | null;
  support1: Hero | null;
  support2: Hero | null;
}
