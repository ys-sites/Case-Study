import React from 'react';
import { X, History, RotateCcw, Clock, Plus } from 'lucide-react';
import { DocumentSnapshot } from '../types';

interface SnapshotDrawerProps {
  isOpen: boolean;
  onClose: () => void;
  snapshots: DocumentSnapshot[];
  onRestoreSnapshot: (snapshot: DocumentSnapshot) => void;
  onCreateSnapshot: () => void;
}

export const SnapshotDrawer: React.FC<SnapshotDrawerProps> = ({
  isOpen,
  onClose,
  snapshots,
  onRestoreSnapshot,
  onCreateSnapshot,
}) => {
  if (!isOpen) return null;

  const formatDate = (ts: number) => {
    return new Date(ts).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
  };

  return (
    <aside className="no-print fixed top-14 right-0 bottom-0 z-30 w-80 bg-white dark:bg-neutral-900 border-l border-neutral-200 dark:border-neutral-800 shadow-xl flex flex-col transition-all">
      <div className="p-4 border-b border-neutral-200 dark:border-neutral-800 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <History className="w-4 h-4 text-neutral-500" />
          <h3 className="text-xs font-bold uppercase tracking-wider text-neutral-700 dark:text-neutral-300">
            Version Snapshots
          </h3>
        </div>
        <button
          onClick={onClose}
          className="p-1 text-neutral-400 hover:text-neutral-700 dark:hover:text-neutral-200 rounded"
        >
          <X className="w-4 h-4" />
        </button>
      </div>

      <div className="p-3 border-b border-neutral-100 dark:border-neutral-800">
        <button
          onClick={onCreateSnapshot}
          className="w-full flex items-center justify-center gap-1.5 py-2 px-3 text-xs font-semibold text-white bg-neutral-900 hover:bg-neutral-800 dark:bg-neutral-100 dark:text-neutral-900 dark:hover:bg-white rounded-md transition-colors"
        >
          <Plus className="w-3.5 h-3.5" />
          <span>Capture Current Version</span>
        </button>
      </div>

      <div className="flex-1 overflow-y-auto p-3 space-y-2">
        {snapshots.length === 0 ? (
          <div className="text-center py-8 text-xs text-neutral-400 space-y-1">
            <Clock className="w-6 h-6 mx-auto text-neutral-300 dark:text-neutral-700" />
            <p>No snapshots captured yet</p>
            <p className="text-[11px] text-neutral-400">
              Save snapshots before making major structural revisions.
            </p>
          </div>
        ) : (
          snapshots.map((snap) => (
            <div
              key={snap.id}
              className="p-3 rounded-lg border border-neutral-200/80 dark:border-neutral-800 bg-stone-50/50 dark:bg-neutral-800/40 hover:border-neutral-300 dark:hover:border-neutral-700 transition-colors"
            >
              <div className="flex items-center justify-between text-xs font-medium text-neutral-900 dark:text-neutral-100 mb-1">
                <span>{snap.title || 'Snapshot'}</span>
                <span className="font-mono text-[10px] text-neutral-400">
                  {formatDate(snap.timestamp)}
                </span>
              </div>

              <div className="text-[11px] text-neutral-500 font-mono mb-2">
                {snap.wordCount} words
              </div>

              <div className="flex justify-end">
                <button
                  onClick={() => onRestoreSnapshot(snap)}
                  className="flex items-center gap-1 px-2.5 py-1 text-xs font-medium text-neutral-700 dark:text-neutral-300 hover:text-neutral-900 dark:hover:text-white border border-neutral-200 dark:border-neutral-700 rounded hover:bg-white dark:hover:bg-neutral-700 transition-colors"
                >
                  <RotateCcw className="w-3 h-3" />
                  <span>Restore</span>
                </button>
              </div>
            </div>
          ))
        )}
      </div>
    </aside>
  );
};
