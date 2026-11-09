import React from 'react';
import { HeadingItem, DocumentStats } from '../types';
import { X, AlignLeft, BarChart2 } from 'lucide-react';

interface OutlineDrawerProps {
  isOpen: boolean;
  onClose: () => void;
  headings: HeadingItem[];
  stats: DocumentStats;
  onJumpToHeading: (heading: HeadingItem) => void;
}

export const OutlineDrawer: React.FC<OutlineDrawerProps> = ({
  isOpen,
  onClose,
  headings,
  stats,
  onJumpToHeading,
}) => {
  if (!isOpen) return null;

  return (
    <aside className="no-print fixed top-14 right-0 bottom-0 z-20 w-72 bg-white dark:bg-neutral-900 border-l border-neutral-200 dark:border-neutral-800 shadow-lg flex flex-col transition-all">
      {/* Header */}
      <div className="p-4 border-b border-neutral-200 dark:border-neutral-800 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <AlignLeft className="w-4 h-4 text-neutral-500" />
          <h3 className="text-xs font-bold uppercase tracking-wider text-neutral-700 dark:text-neutral-300">
            Outline & Metrics
          </h3>
        </div>
        <button
          onClick={onClose}
          className="p-1 text-neutral-400 hover:text-neutral-700 dark:hover:text-neutral-200 rounded hover:bg-neutral-100 dark:hover:bg-neutral-800"
          aria-label="Close outline"
        >
          <X className="w-4 h-4" />
        </button>
      </div>

      {/* Headings List */}
      <div className="flex-1 overflow-y-auto p-4 space-y-1">
        <div className="text-[11px] font-semibold text-neutral-400 uppercase tracking-wider mb-2">
          Document Structure
        </div>

        {headings.length === 0 ? (
          <div className="text-xs text-neutral-400 italic py-4">
            No headings yet. Use `# Heading 1`, `## Heading 2` to structure your thoughts.
          </div>
        ) : (
          headings.map((h) => {
            const indentClass =
              h.level === 1 ? 'pl-0 font-semibold text-neutral-900 dark:text-neutral-100' :
              h.level === 2 ? 'pl-3 text-neutral-700 dark:text-neutral-300 font-medium' :
              'pl-6 text-neutral-500 dark:text-neutral-400';

            return (
              <button
                key={h.id}
                onClick={() => onJumpToHeading(h)}
                className={`w-full text-left py-1 text-xs hover:text-neutral-900 dark:hover:text-white rounded hover:bg-neutral-100 dark:hover:bg-neutral-800/60 truncate transition-colors ${indentClass}`}
                title={`Jump to line ${h.line}`}
              >
                {h.text}
              </button>
            );
          })
        )}

        {/* Writing Metrics Section */}
        <div className="pt-6 mt-6 border-t border-neutral-200 dark:border-neutral-800">
          <div className="flex items-center gap-1.5 text-[11px] font-semibold text-neutral-400 uppercase tracking-wider mb-3">
            <BarChart2 className="w-3.5 h-3.5" />
            <span>Document Statistics</span>
          </div>

          <div className="space-y-2 text-xs">
            <div className="flex justify-between py-1 border-b border-neutral-100 dark:border-neutral-800/60">
              <span className="text-neutral-500">Words</span>
              <span className="font-mono tabular-nums font-medium text-neutral-900 dark:text-neutral-100">
                {stats.words.toLocaleString()}
              </span>
            </div>

            <div className="flex justify-between py-1 border-b border-neutral-100 dark:border-neutral-800/60">
              <span className="text-neutral-500">Characters</span>
              <span className="font-mono tabular-nums font-medium text-neutral-900 dark:text-neutral-100">
                {stats.characters.toLocaleString()}
              </span>
            </div>

            <div className="flex justify-between py-1 border-b border-neutral-100 dark:border-neutral-800/60">
              <span className="text-neutral-500">Paragraphs</span>
              <span className="font-mono tabular-nums font-medium text-neutral-900 dark:text-neutral-100">
                {stats.paragraphs}
              </span>
            </div>

            <div className="flex justify-between py-1 border-b border-neutral-100 dark:border-neutral-800/60">
              <span className="text-neutral-500">Reading Time</span>
              <span className="font-mono tabular-nums font-medium text-neutral-900 dark:text-neutral-100">
                ~{stats.readingTimeMinutes} min
              </span>
            </div>

            <div className="flex justify-between py-1 border-b border-neutral-100 dark:border-neutral-800/60">
              <span className="text-neutral-500">Flesch Score</span>
              <span className="font-mono tabular-nums font-medium text-neutral-900 dark:text-neutral-100">
                {stats.fleschScore} / 100
              </span>
            </div>

            <div className="flex justify-between py-1">
              <span className="text-neutral-500">Target Grade</span>
              <span className="font-medium text-neutral-900 dark:text-neutral-100 text-right">
                {stats.readabilityGrade}
              </span>
            </div>
          </div>
        </div>
      </div>
    </aside>
  );
};
