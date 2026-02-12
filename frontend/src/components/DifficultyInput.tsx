import React from 'react';
import { MessageSquare } from 'lucide-react';

interface DifficultyInputProps {
  value: string;
  onChange: (value: string) => void;
}

export const DifficultyInput: React.FC<DifficultyInputProps> = ({ value, onChange }) => {
  return (
    <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
      <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
        <MessageSquare className="w-5 h-5" />
        What is the problem?
      </h2>
      <textarea
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder="Describe the difficulties you're facing... (e.g., 'Strong bunker defense', 'Dive composition is overwhelming us', etc.)"
        className="w-full px-4 py-3 bg-gray-900 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-overwatch-orange transition-colors resize-none"
        rows={4}
      />
    </div>
  );
};
