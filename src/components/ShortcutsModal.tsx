import React from 'react';
import { X, Command } from 'lucide-react';

interface ShortcutsModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const ShortcutsModal: React.FC<ShortcutsModalProps> = ({ isOpen, onClose }) => {
  if (!isOpen) return null;

  const shortcuts = [
    { key: 'Cmd/Ctrl + S', description: 'Capture version snapshot' },
    { key: 'Cmd/Ctrl + B', description: 'Bold selected text' },
    { key: 'Cmd/Ctrl + I', description: 'Italicize selected text' },
    { key: 'Cmd/Ctrl + K', description: 'Insert markdown link' },
    { key: 'Tab', description: 'Indent 2 spaces' },
    { key: 'Cmd/Ctrl + Shift + F', description: 'Toggle Zen focus mode' },
    { key: 'Esc', description: 'Exit focus mode or close dialogs' },
  ];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-neutral-900/40 backdrop-blur-xs p-4">
      <div className="w-full max-w-sm bg-white dark:bg-neutral-900 border border-neutral-200 dark:border-neutral-800 rounded-xl p-5 shadow-xl relative animate-in fade-in zoom-in-95 duration-150">
        <div className="flex items-center justify-between pb-3 border-b border-neutral-200 dark:border-neutral-800">
          <div className="flex items-center gap-2">
            <Command className="w-4 h-4 text-neutral-600 dark:text-neutral-400" />
            <h3 className="text-xs font-bold uppercase tracking-wider text-neutral-900 dark:text-neutral-100">
              Keyboard Shortcuts
            </h3>
          </div>
          <button
            onClick={onClose}
            className="p-1 text-neutral-400 hover:text-neutral-700 dark:hover:text-neutral-200 rounded"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        <div className="py-3 space-y-2 text-xs">
          {shortcuts.map((s) => (
            <div key={s.key} className="flex items-center justify-between py-1 border-b border-neutral-100 dark:border-neutral-800/60">
              <span className="text-neutral-600 dark:text-neutral-400">{s.description}</span>
              <kbd className="px-2 py-0.5 rounded bg-neutral-100 dark:bg-neutral-800 font-mono text-[11px] text-neutral-800 dark:text-neutral-200 border border-neutral-200 dark:border-neutral-700">
                {s.key}
              </kbd>
            </div>
          ))}
        </div>

        <div className="pt-2 flex justify-end">
          <button
            onClick={onClose}
            className="px-3 py-1 text-xs font-medium text-neutral-600 dark:text-neutral-400 hover:text-neutral-900 dark:hover:text-neutral-100"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};
