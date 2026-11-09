import React, { useState } from 'react';
import {
  X,
  FileDown,
  Printer,
  Copy,
  Check,
  Code,
  FileText,
} from 'lucide-react';
import { generateStandaloneHtml } from '../utils/markdown';
import { EditorSettings } from '../types';

interface ExportModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  content: string;
  settings: EditorSettings;
}

export const ExportModal: React.FC<ExportModalProps> = ({
  isOpen,
  onClose,
  title,
  content,
  settings,
}) => {
  const [copiedType, setCopiedType] = useState<string | null>(null);

  if (!isOpen) return null;

  const sanitizedTitle = (title.trim() || 'untitled')
    .toLowerCase()
    .replace(/[^\w\s-]/g, '')
    .replace(/\s+/g, '-');

  const downloadFile = (data: string, filename: string, type: string) => {
    const blob = new Blob([data], { type });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const handleDownloadMarkdown = () => {
    downloadFile(content, `${sanitizedTitle}.md`, 'text/markdown;charset=utf-8');
  };

  const handleDownloadPlainText = () => {
    // Strip markdown formatting characters
    const plain = content
      .replace(/^#+\s+/gm, '')
      .replace(/\*\*([^*]+)\*\*/g, '$1')
      .replace(/\*([^*]+)\*/g, '$1')
      .replace(/`([^`]+)`/g, '$1')
      .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1');
    downloadFile(plain, `${sanitizedTitle}.txt`, 'text/plain;charset=utf-8');
  };

  const handleDownloadHtml = () => {
    const html = generateStandaloneHtml(title, content, settings.fontFamily);
    downloadFile(html, `${sanitizedTitle}.html`, 'text/html;charset=utf-8');
  };

  const handlePrint = () => {
    window.print();
  };

  const handleCopy = async (type: 'markdown' | 'text') => {
    try {
      const textToCopy =
        type === 'markdown'
          ? content
          : content.replace(/^#+\s+/gm, '').replace(/[*_`]/g, '');
      await navigator.clipboard.writeText(textToCopy);
      setCopiedType(type);
      setTimeout(() => setCopiedType(null), 2000);
    } catch {
      // Fallback
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-neutral-900/40 backdrop-blur-xs p-4">
      <div className="w-full max-w-md bg-white dark:bg-neutral-900 border border-neutral-200 dark:border-neutral-800 rounded-xl p-6 shadow-xl relative animate-in fade-in zoom-in-95 duration-150">
        <div className="flex items-center justify-between pb-4 border-b border-neutral-200 dark:border-neutral-800">
          <div className="flex items-center gap-2">
            <FileDown className="w-4 h-4 text-neutral-600 dark:text-neutral-400" />
            <h3 className="text-sm font-bold text-neutral-900 dark:text-neutral-100">
              Export & Share Document
            </h3>
          </div>
          <button
            onClick={onClose}
            className="p-1 text-neutral-400 hover:text-neutral-700 dark:hover:text-neutral-200 rounded"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        <div className="py-4 space-y-3">
          {/* File Downloads */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
            <button
              onClick={handleDownloadMarkdown}
              className="flex items-center gap-2.5 p-3 rounded-lg border border-neutral-200 dark:border-neutral-800 hover:bg-neutral-100 dark:hover:bg-neutral-800/80 transition-colors text-left"
            >
              <Code className="w-4 h-4 text-amber-600" />
              <div>
                <div className="font-semibold text-neutral-900 dark:text-neutral-100">Markdown (.md)</div>
                <div className="text-[10px] text-neutral-400">Preserves headings & code</div>
              </div>
            </button>

            <button
              onClick={handleDownloadPlainText}
              className="flex items-center gap-2.5 p-3 rounded-lg border border-neutral-200 dark:border-neutral-800 hover:bg-neutral-100 dark:hover:bg-neutral-800/80 transition-colors text-left"
            >
              <FileText className="w-4 h-4 text-emerald-600" />
              <div>
                <div className="font-semibold text-neutral-900 dark:text-neutral-100">Plain Text (.txt)</div>
                <div className="text-[10px] text-neutral-400">Pure clean prose</div>
              </div>
            </button>

            <button
              onClick={handleDownloadHtml}
              className="flex items-center gap-2.5 p-3 rounded-lg border border-neutral-200 dark:border-neutral-800 hover:bg-neutral-100 dark:hover:bg-neutral-800/80 transition-colors text-left"
            >
              <FileDown className="w-4 h-4 text-blue-600" />
              <div>
                <div className="font-semibold text-neutral-900 dark:text-neutral-100">Web HTML (.html)</div>
                <div className="text-[10px] text-neutral-400">Standalone styled page</div>
              </div>
            </button>

            <button
              onClick={handlePrint}
              className="flex items-center gap-2.5 p-3 rounded-lg border border-neutral-200 dark:border-neutral-800 hover:bg-neutral-100 dark:hover:bg-neutral-800/80 transition-colors text-left"
            >
              <Printer className="w-4 h-4 text-indigo-600" />
              <div>
                <div className="font-semibold text-neutral-900 dark:text-neutral-100">Print / PDF</div>
                <div className="text-[10px] text-neutral-400">High quality print layout</div>
              </div>
            </button>
          </div>

          {/* Quick Copy Section */}
          <div className="pt-3 border-t border-neutral-100 dark:border-neutral-800 space-y-2">
            <div className="text-[11px] font-medium text-neutral-500">Quick Clipboard Actions</div>

            <div className="flex gap-2">
              <button
                onClick={() => handleCopy('markdown')}
                className="flex-1 flex items-center justify-center gap-1.5 py-2 px-3 text-xs font-medium border border-neutral-200 dark:border-neutral-700 rounded-md hover:bg-neutral-100 dark:hover:bg-neutral-800 transition-colors"
              >
                {copiedType === 'markdown' ? (
                  <>
                    <Check className="w-3.5 h-3.5 text-emerald-600" />
                    <span>Copied Markdown!</span>
                  </>
                ) : (
                  <>
                    <Copy className="w-3.5 h-3.5" />
                    <span>Copy Markdown</span>
                  </>
                )}
              </button>

              <button
                onClick={() => handleCopy('text')}
                className="flex-1 flex items-center justify-center gap-1.5 py-2 px-3 text-xs font-medium border border-neutral-200 dark:border-neutral-700 rounded-md hover:bg-neutral-100 dark:hover:bg-neutral-800 transition-colors"
              >
                {copiedType === 'text' ? (
                  <>
                    <Check className="w-3.5 h-3.5 text-emerald-600" />
                    <span>Copied Text!</span>
                  </>
                ) : (
                  <>
                    <Copy className="w-3.5 h-3.5" />
                    <span>Copy Raw Text</span>
                  </>
                )}
              </button>
            </div>
          </div>
        </div>

        <div className="pt-3 border-t border-neutral-200 dark:border-neutral-800 flex justify-end">
          <button
            onClick={onClose}
            className="px-4 py-1.5 text-xs font-semibold text-neutral-700 dark:text-neutral-300 hover:bg-neutral-100 dark:hover:bg-neutral-800 rounded-md transition-colors"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};
