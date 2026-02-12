import React from 'react';
import { Sparkles, Loader2 } from 'lucide-react';

interface CoachButtonProps {
  onClick: () => void;
  loading: boolean;
  disabled: boolean;
}

export const CoachButton: React.FC<CoachButtonProps> = ({ onClick, loading, disabled }) => {
  return (
    <button
      onClick={onClick}
      disabled={disabled || loading}
      className={`
        w-full py-4 px-8 rounded-xl font-bold text-lg
        flex items-center justify-center gap-3
        transition-all duration-200 shadow-lg
        ${
          disabled || loading
            ? 'bg-gray-700 text-gray-500 cursor-not-allowed'
            : 'bg-gradient-to-r from-green-500 to-emerald-600 text-white hover:from-green-600 hover:to-emerald-700 hover:scale-105 hover:shadow-xl'
        }
      `}
    >
      {loading ? (
        <>
          <Loader2 className="w-6 h-6 animate-spin" />
          <span>Coach AI is thinking...</span>
        </>
      ) : (
        <>
          <Sparkles className="w-6 h-6" />
          <span>Help!</span>
        </>
      )}
    </button>
  );
};
