// Overcoach AI API service

import type { TeamCompositionRequest, TeamCompositionResponse } from '../types/overwatch';

const OVERCOACH_BASE_URL = 'http://localhost:8000';

export const overcoachApi = {
  async suggestTeam(request: TeamCompositionRequest): Promise<TeamCompositionResponse> {
    const response = await fetch(`${OVERCOACH_BASE_URL}/suggest`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      throw new Error('Failed to get team suggestion');
    }

    return response.json();
  },

  async healthCheck(): Promise<{ status: string }> {
    const response = await fetch(`${OVERCOACH_BASE_URL}/health`);
    if (!response.ok) throw new Error('Backend not available');
    return response.json();
  },
};
