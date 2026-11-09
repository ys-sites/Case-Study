import React from 'react';
import { X, BookOpen, Sparkles, PlusCircle } from 'lucide-react';
import { TEMPLATES, DocumentTemplate } from '../utils/templates';

interface TemplatesModalProps {
  isOpen: boolean;
  onClose: () => void;
  onApplyTemplate: (template: DocumentTemplate, asNewDoc: boolean) => void;
}

export const TemplatesModal: React.FC<TemplatesModalProps> = ({
  isOpen,
  onClose,
  onApplyTemplate,
}) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-neutral-900/40 backdrop-blur-xs p-4">
      <div className="w-full max-w-2xl bg-white dark:bg-neutral-900 border border-neutral-200 dark:border-neutral-800 rounded-xl p-6 shadow-xl relative max-h-[85vh] flex flex-col animate-in fade-in zoom-in-95 duration-150">
        <div className="flex items-center justify-between pb-4 border-b border-neutral-200 dark:border-neutral-800 shrink-0">
          <div className="flex items-center gap-2">
            <BookOpen className="w-4 h-4 text-neutral-600 dark:text-neutral-400" />
            <h3 className="text-sm font-bold text-neutral-900 dark:text-neutral-100">
              Blank Page Jumpstarts & Templates
            </h3>
          </div>
          <button
            onClick={onClose}
            className="p-1 text-neutral-400 hover:text-neutral-700 dark:hover:text-neutral-200 rounded"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        <p className="text-xs text-neutral-500 py-3 shrink-0">
          Overcome the blank canvas with clean, battle-tested structural frameworks.
        </p>

        {/* Templates Grid */}
        <div className="flex-1 overflow-y-auto space-y-3 pr-1">
          {TEMPLATES.map((tmpl) => (
            <div
              key={tmpl.id}
              className="p-4 rounded-xl border border-neutral-200 dark:border-neutral-800 hover:border-neutral-300 dark:hover:border-neutral-700 transition-colors bg-stone-50/50 dark:bg-neutral-800/40"
            >
              <div className="flex items-start justify-between gap-4">
                <div>
                  <div className="flex items-center gap-2">
                    <h4 className="text-sm font-semibold text-neutral-900 dark:text-neutral-100">
                      {tmpl.title}
                    </h4>
                    <span className="text-[10px] text-neutral-400 dark:text-neutral-500">
                      · {tmpl.category}
                    </span>
                  </div>
                  <p className="text-xs text-neutral-500 dark:text-neutral-400 mt-1 leading-relaxed">
                    {tmpl.description}
                  </p>
                </div>

                <div className="flex items-center gap-2 shrink-0">
                  <button
                    onClick={() => {
                      onApplyTemplate(tmpl, false);
                      onClose();
                    }}
                    className="px-2.5 py-1.5 text-xs font-medium text-neutral-700 dark:text-neutral-300 bg-white dark:bg-neutral-800 border border-neutral-200 dark:border-neutral-700 rounded-md hover:bg-neutral-100 dark:hover:bg-neutral-700 transition-colors whitespace-nowrap"
                    title="Replace current document"
                  >
                    Insert Here
                  </button>

                  <button
                    onClick={() => {
                      onApplyTemplate(tmpl, true);
                      onClose();
                    }}
                    className="flex items-center gap-1 px-3 py-1.5 text-xs font-semibold text-white bg-neutral-900 hover:bg-neutral-800 dark:bg-neutral-100 dark:text-neutral-900 dark:hover:bg-white rounded-md transition-colors whitespace-nowrap shadow-2xs"
                    title="Open as brand new document"
                  >
                    <PlusCircle className="w-3.5 h-3.5" />
                    <span>New Page</span>
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
