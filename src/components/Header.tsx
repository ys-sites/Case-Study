import React from 'react';
import {
  FileText,
  Columns,
  Eye,
  Sliders,
  Download,
  Maximize2,
  Minimize2,
  Clock,
  Volume2,
  VolumeX,
  History,
  ListTree,
  Sun,
  Moon,
  Menu,
  Trophy,
  Cpu,
} from 'lucide-react';
import { ViewMode, EditorSettings } from '../types';

interface HeaderProps {
  documentTitle: string;
  wordCount: number;
  readingTimeMin: number;
  viewMode: ViewMode;
  setViewMode: (mode: ViewMode) => void;
  zenMode: boolean;
  setZenMode: (zen: boolean) => void;
  onOpenSettings: () => void;
  onOpenExport: () => void;
  onOpenSnapshots: () => void;
  onToggleOutline: () => void;
  outlineOpen: boolean;
  onToggleSidebar: () => void;
  sidebarOpen: boolean;
  isDark: boolean;
  onToggleTheme: () => void;
  settings: EditorSettings;
  onUpdateSettings: (settings: Partial<EditorSettings>) => void;
  onOpenTimer: () => void;
  isTimerRunning: boolean;
  timerFormatted: string;
  onOpenCaseSimulator?: () => void;
  onOpenGlobalCompetitions?: () => void;
}

export const Header: React.FC<HeaderProps> = ({
  documentTitle,
  wordCount,
  readingTimeMin,
  viewMode,
  setViewMode,
  zenMode,
  setZenMode,
  onOpenSettings,
  onOpenExport,
  onOpenSnapshots,
  onToggleOutline,
  outlineOpen,
  onToggleSidebar,
  sidebarOpen,
  isDark,
  onToggleTheme,
  settings,
  onUpdateSettings,
  onOpenTimer,
  isTimerRunning,
  timerFormatted,
  onOpenCaseSimulator,
  onOpenGlobalCompetitions,
}) => {
  // If in Zen Mode, header is minimal floating or hidden unless hovered
  if (zenMode) {
    return (
      <div className="fixed top-4 right-4 z-50 flex items-center gap-2 opacity-30 hover:opacity-100 transition-opacity duration-200">
        <button
          onClick={() => setZenMode(false)}
          className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-md bg-neutral-900/90 text-white dark:bg-neutral-100/90 dark:text-neutral-900 shadow-md backdrop-blur-sm transition-transform active:scale-95"
          title="Exit Focus Mode (Esc)"
        >
          <Minimize2 className="w-3.5 h-3.5" />
          <span>Exit Focus</span>
        </button>
      </div>
    );
  }

  return (
    <header className="no-print h-14 border-b border-neutral-200 dark:border-neutral-800 bg-white/80 dark:bg-neutral-900/80 backdrop-blur-md px-4 flex items-center justify-between gap-4 sticky top-0 z-30 transition-colors">
      {/* Zone 1: Brand & Document Title */}
      <div className="flex items-center gap-3 min-w-0">
        <button
          onClick={onToggleSidebar}
          aria-label={sidebarOpen ? "Close documents sidebar" : "Open documents sidebar"}
          className="p-1.5 text-neutral-600 dark:text-neutral-400 hover:text-neutral-900 dark:hover:text-neutral-100 rounded-md hover:bg-neutral-100 dark:hover:bg-neutral-800 transition-colors shrink-0"
        >
          <Menu className="w-4 h-4" />
        </button>

        <a
          href="#"
          onClick={(e) => { e.preventDefault(); onToggleSidebar(); }}
          className="text-sm font-bold tracking-tight text-neutral-900 dark:text-neutral-100 whitespace-nowrap shrink-0 flex items-center gap-2"
        >
          <span className="font-editorial text-base italic font-semibold tracking-tight">Case-Study</span>
          <span className="hidden md:inline-block text-[10px] font-mono px-1.5 py-0.5 rounded bg-neutral-100 dark:bg-neutral-800 text-neutral-600 dark:text-neutral-400 border border-neutral-200 dark:border-neutral-700">
            Strategy Hub
          </span>
        </a>

        <div className="hidden sm:flex items-center text-xs text-neutral-400 dark:text-neutral-500 shrink-0">
          /
        </div>

        <div className="hidden sm:flex items-center gap-2 text-xs text-neutral-500 dark:text-neutral-400 truncate max-w-xs md:max-w-md">
          <span className="font-medium text-neutral-800 dark:text-neutral-200 truncate">
            {documentTitle || 'Untitled Draft'}
          </span>
          <span aria-hidden="true" className="text-neutral-300 dark:text-neutral-700">·</span>
          <span className="font-mono tabular-nums shrink-0">{wordCount.toLocaleString()} words</span>
          <span aria-hidden="true" className="text-neutral-300 dark:text-neutral-700">·</span>
          <span className="font-mono tabular-nums shrink-0">{readingTimeMin} min read</span>
        </div>
      </div>

      {/* Zone 2: View Mode Segmented Controls */}
      <div className="flex items-center gap-1 bg-neutral-100 dark:bg-neutral-800 p-0.5 rounded-lg shrink-0">
        <button
          onClick={() => setViewMode('edit')}
          className={`flex items-center gap-1.5 px-2.5 py-1 text-xs font-medium rounded-md transition-colors whitespace-nowrap ${
            viewMode === 'edit'
              ? 'bg-white dark:bg-neutral-700 text-neutral-900 dark:text-neutral-100 shadow-xs'
              : 'text-neutral-600 dark:text-neutral-400 hover:text-neutral-900 dark:hover:text-neutral-200'
          }`}
          title="Editor Only"
        >
          <FileText className="w-3.5 h-3.5" />
          <span className="hidden md:inline">Write</span>
        </button>
        <button
          onClick={() => setViewMode('split')}
          className={`flex items-center gap-1.5 px-2.5 py-1 text-xs font-medium rounded-md transition-colors whitespace-nowrap ${
            viewMode === 'split'
              ? 'bg-white dark:bg-neutral-700 text-neutral-900 dark:text-neutral-100 shadow-xs'
              : 'text-neutral-600 dark:text-neutral-400 hover:text-neutral-900 dark:hover:text-neutral-200'
          }`}
          title="Side-by-side Editor & Formatted Preview"
        >
          <Columns className="w-3.5 h-3.5" />
          <span className="hidden md:inline">Split</span>
        </button>
        <button
          onClick={() => setViewMode('preview')}
          className={`flex items-center gap-1.5 px-2.5 py-1 text-xs font-medium rounded-md transition-colors whitespace-nowrap ${
            viewMode === 'preview'
              ? 'bg-white dark:bg-neutral-700 text-neutral-900 dark:text-neutral-100 shadow-xs'
              : 'text-neutral-600 dark:text-neutral-400 hover:text-neutral-900 dark:hover:text-neutral-200'
          }`}
          title="Reading Preview"
        >
          <Eye className="w-3.5 h-3.5" />
          <span className="hidden md:inline">Read</span>
        </button>
      </div>

      {/* Zone 3: Studio Controls & Primary Actions */}
      <div className="flex items-center gap-1.5 shrink-0">
        {/* Focus Timer Button */}
        <button
          onClick={onOpenTimer}
          className={`flex items-center gap-1 px-2.5 py-1 text-xs font-medium rounded-md border transition-colors whitespace-nowrap ${
            isTimerRunning
              ? 'border-amber-500/50 bg-amber-50 dark:bg-amber-950/40 text-amber-700 dark:text-amber-300'
              : 'border-neutral-200 dark:border-neutral-800 text-neutral-600 dark:text-neutral-400 hover:bg-neutral-100 dark:hover:bg-neutral-800'
          }`}
          title="Focus Sprint Timer"
        >
          <Clock className="w-3.5 h-3.5" />
          <span className="font-mono tabular-nums">{timerFormatted}</span>
        </button>

        {/* Audio Toggle */}
        <button
          onClick={() => onUpdateSettings({ soundEnabled: !settings.soundEnabled })}
          className={`p-1.5 rounded-md transition-colors ${
            settings.soundEnabled
              ? 'text-neutral-900 dark:text-neutral-100 bg-neutral-100 dark:bg-neutral-800'
              : 'text-neutral-400 hover:text-neutral-600 dark:hover:text-neutral-300'
          }`}
          title={settings.soundEnabled ? 'Typing Sounds: On' : 'Typing Sounds: Muted'}
          aria-label="Toggle typing sounds"
        >
          {settings.soundEnabled ? <Volume2 className="w-4 h-4" /> : <VolumeX className="w-4 h-4" />}
        </button>

        {/* Outline Toggle */}
        <button
          onClick={onToggleOutline}
          className={`p-1.5 rounded-md transition-colors ${
            outlineOpen
              ? 'text-neutral-900 dark:text-neutral-100 bg-neutral-100 dark:bg-neutral-800'
              : 'text-neutral-500 dark:text-neutral-400 hover:text-neutral-900 dark:hover:text-neutral-100 hover:bg-neutral-100 dark:hover:bg-neutral-800'
          }`}
          title="Document Outline & Metrics"
          aria-label="Toggle outline"
        >
          <ListTree className="w-4 h-4" />
        </button>

        {/* Version History Snapshots */}
        <button
          onClick={onOpenSnapshots}
          className="p-1.5 text-neutral-500 dark:text-neutral-400 hover:text-neutral-900 dark:hover:text-neutral-100 hover:bg-neutral-100 dark:hover:bg-neutral-800 rounded-md transition-colors"
          title="Revision History & Snapshots"
          aria-label="View history snapshots"
        >
          <History className="w-4 h-4" />
        </button>

        {/* Typography Settings */}
        <button
          onClick={onOpenSettings}
          className="p-1.5 text-neutral-500 dark:text-neutral-400 hover:text-neutral-900 dark:hover:text-neutral-100 hover:bg-neutral-100 dark:hover:bg-neutral-800 rounded-md transition-colors"
          title="Typography & Canvas Preferences"
          aria-label="Customize typography"
        >
          <Sliders className="w-4 h-4" />
        </button>

        {/* Dark/Light Mode */}
        <button
          onClick={onToggleTheme}
          className="p-1.5 text-neutral-500 dark:text-neutral-400 hover:text-neutral-900 dark:hover:text-neutral-100 hover:bg-neutral-100 dark:hover:bg-neutral-800 rounded-md transition-colors"
          title={isDark ? 'Switch to Light Mode' : 'Switch to Dark Mode'}
          aria-label="Toggle color theme"
        >
          {isDark ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
        </button>

        {/* Global Competitions Directory */}
        {onOpenGlobalCompetitions && (
          <button
            onClick={onOpenGlobalCompetitions}
            className="flex items-center gap-1.5 px-2.5 py-1 text-xs font-medium rounded-md border border-amber-500/30 bg-amber-500/10 text-amber-700 dark:text-amber-400 hover:bg-amber-500/20 transition-colors whitespace-nowrap"
            title="Browse 132+ Global Case Competitions"
          >
            <Trophy className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">Competitions</span>
          </button>
        )}

        {/* Case Simulator & 14-Agent System */}
        {onOpenCaseSimulator && (
          <button
            onClick={onOpenCaseSimulator}
            className="flex items-center gap-1.5 px-2.5 py-1 text-xs font-semibold rounded-md bg-amber-500 hover:bg-amber-600 text-white shadow-xs transition-colors whitespace-nowrap"
            title="Open Case Simulator & 14-Agent Solution Factory"
          >
            <Cpu className="w-3.5 h-3.5" />
            <span>Simulator</span>
          </button>
        )}

        {/* Zen Mode Button */}
        <button
          onClick={() => setZenMode(true)}
          className="hidden lg:flex items-center gap-1 px-2 py-1 text-xs text-neutral-600 dark:text-neutral-400 hover:text-neutral-900 dark:hover:text-neutral-100 hover:bg-neutral-100 dark:hover:bg-neutral-800 rounded-md transition-colors whitespace-nowrap"
          title="Full Screen Focus (Cmd+Shift+F)"
        >
          <Maximize2 className="w-3.5 h-3.5" />
          <span>Focus</span>
        </button>

        {/* Primary Action: Export */}
        <button
          onClick={onOpenExport}
          className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold text-white bg-neutral-900 hover:bg-neutral-800 dark:bg-neutral-100 dark:text-neutral-900 dark:hover:bg-white rounded-md transition-colors whitespace-nowrap shadow-xs active:scale-95"
        >
          <Download className="w-3.5 h-3.5" />
          <span>Export</span>
        </button>
      </div>
    </header>
  );
};
