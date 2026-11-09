import React from 'react';
import { Play, Pause, RotateCcw, X, Timer, Trophy } from 'lucide-react';

interface FocusTimerProps {
  isOpen: boolean;
  onClose: () => void;
  timeLeft: number;
  isRunning: boolean;
  onStart: () => void;
  onPause: () => void;
  onReset: (minutes: number) => void;
}

export const FocusTimerModal: React.FC<FocusTimerProps> = ({
  isOpen,
  onClose,
  timeLeft,
  isRunning,
  onStart,
  onPause,
  onReset,
}) => {
  if (!isOpen) return null;

  const hours = Math.floor(timeLeft / 3600);
  const minutes = Math.floor((timeLeft % 3600) / 60);
  const seconds = timeLeft % 60;
  const formatted = hours > 0
    ? `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`
    : `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-neutral-900/40 backdrop-blur-xs p-4">
      <div className="w-full max-w-md bg-white dark:bg-neutral-900 border border-neutral-200 dark:border-neutral-800 rounded-xl p-6 shadow-xl relative animate-in fade-in zoom-in-95 duration-150">
        <button
          onClick={onClose}
          className="absolute top-4 right-4 p-1 text-neutral-400 hover:text-neutral-700 dark:hover:text-neutral-200 rounded"
          aria-label="Close Case Timer"
        >
          <X className="w-4 h-4" />
        </button>

        <div className="text-center">
          <div className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-neutral-100 dark:bg-neutral-800 text-[11px] font-semibold uppercase tracking-wider text-neutral-600 dark:text-neutral-300 mb-2">
            <Trophy className="w-3.5 h-3.5 text-amber-500" />
            <span>Case Competition Sprint Timer</span>
          </div>

          <div className="font-mono text-5xl font-bold tracking-tight text-neutral-900 dark:text-neutral-50 my-5 tabular-nums">
            {formatted}
          </div>

          {/* Quick Case Competition Preset Sprint Buttons */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-1.5 mb-6 text-left">
            <button
              onClick={() => onReset(180)}
              className="p-2 rounded-lg border border-neutral-200 dark:border-neutral-700 hover:bg-neutral-50 dark:hover:bg-neutral-800 transition-colors text-center"
            >
              <div className="text-xs font-bold text-neutral-900 dark:text-neutral-100">3 Hours</div>
              <div className="text-[10px] text-neutral-500">Full Sprint</div>
            </button>
            <button
              onClick={() => onReset(45)}
              className="p-2 rounded-lg border border-neutral-200 dark:border-neutral-700 hover:bg-neutral-50 dark:hover:bg-neutral-800 transition-colors text-center"
            >
              <div className="text-xs font-bold text-neutral-900 dark:text-neutral-100">45 Mins</div>
              <div className="text-[10px] text-neutral-500">Diagnosis</div>
            </button>
            <button
              onClick={() => onReset(20)}
              className="p-2 rounded-lg border border-neutral-200 dark:border-neutral-700 hover:bg-neutral-50 dark:hover:bg-neutral-800 transition-colors text-center"
            >
              <div className="text-xs font-bold text-neutral-900 dark:text-neutral-100">20 Mins</div>
              <div className="text-[10px] text-neutral-500">Pitch Practice</div>
            </button>
            <button
              onClick={() => onReset(5)}
              className="p-2 rounded-lg border border-neutral-200 dark:border-neutral-700 hover:bg-neutral-50 dark:hover:bg-neutral-800 transition-colors text-center"
            >
              <div className="text-xs font-bold text-neutral-900 dark:text-neutral-100">5 Mins</div>
              <div className="text-[10px] text-neutral-500">Judge Q&A</div>
            </button>
          </div>

          {/* Play/Pause & Reset Controls */}
          <div className="flex items-center justify-center gap-3">
            {isRunning ? (
              <button
                onClick={onPause}
                className="flex items-center gap-2 px-6 py-2.5 text-sm font-semibold text-white bg-neutral-900 hover:bg-neutral-800 dark:bg-neutral-100 dark:text-neutral-900 rounded-lg shadow-sm transition-all"
              >
                <Pause className="w-4 h-4" />
                <span>Pause</span>
              </button>
            ) : (
              <button
                onClick={onStart}
                className="flex items-center gap-2 px-6 py-2.5 text-sm font-semibold text-white bg-neutral-900 hover:bg-neutral-800 dark:bg-neutral-100 dark:text-neutral-900 rounded-lg shadow-sm transition-all"
              >
                <Play className="w-4 h-4" />
                <span>Start Session</span>
              </button>
            )}

            <button
              onClick={() => onReset(20)}
              className="p-2.5 text-neutral-500 hover:text-neutral-800 dark:hover:text-neutral-200 border border-neutral-200 dark:border-neutral-700 rounded-lg hover:bg-neutral-100 dark:hover:bg-neutral-800 transition-colors"
              title="Reset Timer to 20 Min Pitch"
            >
              <RotateCcw className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
