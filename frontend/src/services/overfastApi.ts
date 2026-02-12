// OverFast API service

import type { Hero, OverwatchMap } from '../types/overwatch';

const OVERFAST_BASE_URL = 'https://overfast-api.tekrop.fr';

export const overfastApi = {
  async getHeroes(): Promise<Hero[]> {
    const response = await fetch(`${OVERFAST_BASE_URL}/heroes`);
    if (!response.ok) throw new Error('Failed to fetch heroes');
    return response.json();
  },

  async getMaps(): Promise<OverwatchMap[]> {
    const response = await fetch(`${OVERFAST_BASE_URL}/maps`);
    if (!response.ok) throw new Error('Failed to fetch maps');
    return response.json();
  },
};
