import React from 'react';
import { Lightbulb, Zap } from 'lucide-react';

interface StrategyDisplayProps {
  strategy: string;
  synergies: string;
}

export const StrategyDisplay: React.FC<StrategyDisplayProps> = ({ strategy, synergies }) => {
  return (
    <div className="space-y-4">
      {/* Strategy */}
      <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
        <h3 className="text-xl font-bold text-white mb-3 flex items-center gap-2">
          <Lightbulb className="w-5 h-5 text-blue-400" />
          Counter Strategy
        </h3>
        <p className="text-gray-300 leading-relaxed">{strategy}</p>
      </div>

      {/* Synergies */}
      <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
        <h3 className="text-xl font-bold text-white mb-3 flex items-center gap-2">
          <Zap className="w-5 h-5 text-yellow-400" />
          Key Synergies
        </h3>
        <p className="text-gray-300 leading-relaxed">{synergies}</p>
      </div>
    </div>
  );
};
