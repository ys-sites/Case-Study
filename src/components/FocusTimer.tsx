import React from 'react';
import { Play, Pause, RotateCcw, X, Bell } from 'lucide-react';

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

  const minutes = Math.floor(timeLeft / 60);
  const seconds = timeLeft % 60;
  const formatted = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-neutral-900/40 backdrop-blur-xs p-4">
      <div className="w-full max-w-sm bg-white dark:bg-neutral-900 border border-neutral-200 dark:border-neutral-800 rounded-xl p-6 shadow-xl relative animate-in fade-in zoom-in-95 duration-150">
        <button
          onClick={onClose}
          className="absolute top-4 right-4 p-1 text-neutral-400 hover:text-neutral-700 dark:hover:text-neutral-200 rounded"
        >
          <X className="w-4 h-4" />
        </button>

        <div className="text-center">
          <div className="inline-flex items-center gap-1.5 text-xs font-semibold uppercase tracking-wider text-neutral-500 mb-2">
            <Bell className="w-3.5 h-3.5" />
            <span>Deep Work Sprint</span>
          </div>

          <div className="font-mono text-5xl font-bold tracking-tight text-neutral-900 dark:text-neutral-50 my-6 tabular-nums">
            {formatted}
          </div>

          {/* Quick preset sprint buttons */}
          <div className="flex justify-center gap-2 mb-6">
            <button
              onClick={() => onReset(15)}
              className="px-2.5 py-1 text-xs font-medium rounded border border-neutral-200 dark:border-neutral-700 hover:bg-neutral-100 dark:hover:bg-neutral-800 transition-colors"
            >
              15 min
            </button>
            <button
              onClick={() => onReset(25)}
              className="px-2.5 py-1 text-xs font-medium rounded border border-neutral-200 dark:border-neutral-700 hover:bg-neutral-100 dark:hover:bg-neutral-800 transition-colors"
            >
              25 min (Standard)
            </button>
            <button
              onClick={() => onReset(45)}
              className="px-2.5 py-1 text-xs font-medium rounded border border-neutral-200 dark:border-neutral-700 hover:bg-neutral-100 dark:hover:bg-neutral-800 transition-colors"
            >
              45 min (Deep)
            </button>
          </div>

          {/* Play/Pause & Reset controls */}
          <div className="flex items-center justify-center gap-3">
            {isRunning ? (
              <button
                onClick={onPause}
                className="flex items-center gap-2 px-5 py-2 text-sm font-semibold text-white bg-neutral-900 hover:bg-neutral-800 dark:bg-neutral-100 dark:text-neutral-900 rounded-lg shadow-sm transition-all"
              >
                <Pause className="w-4 h-4" />
                <span>Pause</span>
              </button>
            ) : (
              <button
                onClick={onStart}
                className="flex items-center gap-2 px-5 py-2 text-sm font-semibold text-white bg-neutral-900 hover:bg-neutral-800 dark:bg-neutral-100 dark:text-neutral-900 rounded-lg shadow-sm transition-all"
              >
                <Play className="w-4 h-4" />
                <span>Start Sprint</span>
              </button>
            )}

            <button
              onClick={() => onReset(25)}
              className="p-2 text-neutral-500 hover:text-neutral-800 dark:hover:text-neutral-200 border border-neutral-200 dark:border-neutral-700 rounded-lg hover:bg-neutral-100 dark:hover:bg-neutral-800 transition-colors"
              title="Reset Timer"
            >
              <RotateCcw className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
