import React, { useState, useEffect, useRef, useMemo } from 'react';
import {
  Document,
  DocumentSnapshot,
  EditorSettings,
  ViewMode,
  HeadingItem,
} from './types';
import { INITIAL_DOCUMENTS, TEMPLATES, DocumentTemplate } from './utils/templates';
import { extractHeadings, calculateStats } from './utils/markdown';
import { soundEngine } from './utils/audio';
import { Header } from './components/Header';
import { Sidebar } from './components/Sidebar';
import { Editor } from './components/Editor';
import { MarkdownPreview } from './components/MarkdownPreview';
import { OutlineDrawer } from './components/OutlineDrawer';
import { FocusTimerModal } from './components/FocusTimer';
import { SettingsModal } from './components/SettingsModal';
import { ExportModal } from './components/ExportModal';
import { TemplatesModal } from './components/TemplatesModal';
import { SnapshotDrawer } from './components/SnapshotDrawer';
import { ShortcutsModal } from './components/ShortcutsModal';
import { CaseSimulatorModal } from './components/CaseSimulatorModal';
import { GlobalCompetitionsModal } from './components/GlobalCompetitionsModal';

const DEFAULT_SETTINGS: EditorSettings = {
  fontFamily: 'editorial',
  fontSize: 17,
  lineHeight: 1.75,
  measure: 'standard',
  typewriterMode: false,
  soundEnabled: true,
  ambientSound: 'none',
  soundVolume: 0.4,
  autoSaveInterval: 2,
};

export default function App() {
  // Theme state
  const [isDark, setIsDark] = useState<boolean>(() => {
    const saved = localStorage.getItem('blankpage_theme');
    if (saved) return saved === 'dark';
    return window.matchMedia('(prefers-color-scheme: dark)').matches;
  });

  // Apply theme to documentElement
  useEffect(() => {
    if (isDark) {
      document.documentElement.classList.add('dark');
      localStorage.setItem('blankpage_theme', 'dark');
    } else {
      document.documentElement.classList.remove('dark');
      localStorage.setItem('blankpage_theme', 'light');
    }
  }, [isDark]);

  // Documents state
  const [documents, setDocuments] = useState<Document[]>(() => {
    try {
      const saved = localStorage.getItem('blankpage_documents');
      if (saved) {
        const parsed = JSON.parse(saved);
        if (Array.isArray(parsed) && parsed.length > 0) return parsed;
      }
    } catch {
      // Fallback
    }
    return INITIAL_DOCUMENTS;
  });

  // Current document ID
  const [currentDocId, setCurrentDocId] = useState<string>(() => {
    const saved = localStorage.getItem('blankpage_current_id');
    if (saved && documents.some((d) => d.id === saved)) return saved;
    return documents[0]?.id || 'doc-1';
  });

  // Settings state
  const [settings, setSettings] = useState<EditorSettings>(() => {
    try {
      const saved = localStorage.getItem('blankpage_settings');
      if (saved) return { ...DEFAULT_SETTINGS, ...JSON.parse(saved) };
    } catch {
      // Fallback
    }
    return DEFAULT_SETTINGS;
  });

  // View & UI states
  const [viewMode, setViewMode] = useState<ViewMode>('split');
  const [zenMode, setZenMode] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [outlineOpen, setOutlineOpen] = useState(false);

  // Modals state
  const [settingsOpen, setSettingsOpen] = useState(false);
  const [exportOpen, setExportOpen] = useState(false);
  const [templatesOpen, setTemplatesOpen] = useState(false);
  const [snapshotsOpen, setSnapshotsOpen] = useState(false);
  const [shortcutsOpen, setShortcutsOpen] = useState(false);
  const [caseSimulatorOpen, setCaseSimulatorOpen] = useState(false);
  const [globalCompetitionsOpen, setGlobalCompetitionsOpen] = useState(false);
  const [toastMessage, setToastMessage] = useState<string | null>(null);

  // Focus Timer state
  const [timerModalOpen, setTimerModalOpen] = useState(false);
  const [timerDuration, setTimerDuration] = useState(25 * 60);
  const [timeLeft, setTimeLeft] = useState(25 * 60);
  const [isTimerRunning, setIsTimerRunning] = useState(false);

  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Save documents to localStorage
  useEffect(() => {
    localStorage.setItem('blankpage_documents', JSON.stringify(documents));
  }, [documents]);

  // Save current ID to localStorage
  useEffect(() => {
    localStorage.setItem('blankpage_current_id', currentDocId);
  }, [currentDocId]);

  // Save settings to localStorage
  useEffect(() => {
    localStorage.setItem('blankpage_settings', JSON.stringify(settings));
    soundEngine.setVolume(settings.soundVolume);

    // Ambient sound control
    if (settings.ambientSound === 'rain') {
      soundEngine.startAmbientRain();
    } else {
      soundEngine.stopAmbient();
    }

    return () => {
      soundEngine.stopAmbient();
    };
  }, [settings]);

  // Current document object
  const currentDoc = useMemo(() => {
    return documents.find((d) => d.id === currentDocId) || documents[0] || INITIAL_DOCUMENTS[0];
  }, [documents, currentDocId]);

  // Document analysis & metrics
  const headings = useMemo(() => {
    return extractHeadings(currentDoc?.content || '');
  }, [currentDoc?.content]);

  const stats = useMemo(() => {
    return calculateStats(currentDoc?.content || '');
  }, [currentDoc?.content]);

  // Focus timer countdown
  useEffect(() => {
    let interval: ReturnType<typeof setInterval> | null = null;
    if (isTimerRunning && timeLeft > 0) {
      interval = setInterval(() => {
        setTimeLeft((prev) => prev - 1);
      }, 1000);
    } else if (timeLeft === 0 && isTimerRunning) {
      setIsTimerRunning(false);
      soundEngine.playChime();
      showToast('Focus Sprint Completed! Take a deep breath.');
    }
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [isTimerRunning, timeLeft]);

  const formattedTimer = useMemo(() => {
    const mins = Math.floor(timeLeft / 60);
    const secs = timeLeft % 60;
    return `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
  }, [timeLeft]);

  const showToast = (msg: string) => {
    setToastMessage(msg);
    setTimeout(() => {
      setToastMessage(null);
    }, 2500);
  };

  // Keyboard shortcuts
  useEffect(() => {
    const handleGlobalKeyDown = (e: KeyboardEvent) => {
      // Toggle Zen Focus with Cmd/Ctrl + Shift + F
      if ((e.metaKey || e.ctrlKey) && e.shiftKey && e.key.toLowerCase() === 'f') {
        e.preventDefault();
        setZenMode((prev) => !prev);
      }
      // Exit Zen or modals with Escape
      if (e.key === 'Escape') {
        if (zenMode) setZenMode(false);
        setSettingsOpen(false);
        setExportOpen(false);
        setTemplatesOpen(false);
        setSnapshotsOpen(false);
        setTimerModalOpen(false);
        setShortcutsOpen(false);
      }
    };
    window.addEventListener('keydown', handleGlobalKeyDown);
    return () => window.removeEventListener('keydown', handleGlobalKeyDown);
  }, [zenMode]);

  // Document update handlers
  const handleUpdateContent = (newContent: string) => {
    setDocuments((prev) =>
      prev.map((doc) =>
        doc.id === currentDocId
          ? {
              ...doc,
              content: newContent,
              updatedAt: Date.now(),
            }
          : doc
      )
    );
  };

  const handleUpdateTitle = (newTitle: string) => {
    setDocuments((prev) =>
      prev.map((doc) =>
        doc.id === currentDocId
          ? {
              ...doc,
              title: newTitle,
              updatedAt: Date.now(),
            }
          : doc
      )
    );
  };

  const handleCreateNewDocument = () => {
    const newDoc: Document = {
      id: `doc-${Date.now()}`,
      title: 'A Blank Page',
      content: '',
      tags: [],
      category: 'draft',
      isFavorite: false,
      createdAt: Date.now(),
      updatedAt: Date.now(),
      snapshots: [],
    };
    setDocuments((prev) => [newDoc, ...prev]);
    setCurrentDocId(newDoc.id);
    setViewMode('edit');
    showToast('Created new blank page');
    setTimeout(() => {
      textareaRef.current?.focus();
    }, 50);
  };

  const handleDeleteDocument = (id: string) => {
    if (documents.length <= 1) return;
    const remaining = documents.filter((d) => d.id !== id);
    setDocuments(remaining);
    if (currentDocId === id) {
      setCurrentDocId(remaining[0].id);
    }
    showToast('Document moved to trash');
  };

  const handleDuplicateDocument = (doc: Document) => {
    const clone: Document = {
      ...doc,
      id: `doc-${Date.now()}`,
      title: `${doc.title} (Copy)`,
      createdAt: Date.now(),
      updatedAt: Date.now(),
    };
    setDocuments((prev) => [clone, ...prev]);
    setCurrentDocId(clone.id);
    showToast('Document duplicated');
  };

  const handleToggleFavorite = (id: string) => {
    setDocuments((prev) =>
      prev.map((d) => (d.id === id ? { ...d, isFavorite: !d.isFavorite } : d))
    );
  };

  const handleCreateSnapshot = () => {
    if (!currentDoc) return;
    const snapshot: DocumentSnapshot = {
      id: `snap-${Date.now()}`,
      timestamp: Date.now(),
      title: currentDoc.title,
      content: currentDoc.content,
      wordCount: stats.words,
    };
    setDocuments((prev) =>
      prev.map((d) =>
        d.id === currentDocId
          ? {
              ...d,
              snapshots: [snapshot, ...d.snapshots.slice(0, 9)], // keep top 10
            }
          : d
      )
    );
    showToast('Version snapshot captured');
  };

  const handleRestoreSnapshot = (snap: DocumentSnapshot) => {
    handleUpdateContent(snap.content);
    handleUpdateTitle(snap.title);
    setSnapshotsOpen(false);
    showToast('Restored previous snapshot');
  };

  const handleApplyTemplate = (template: DocumentTemplate, asNewDoc: boolean) => {
    if (asNewDoc) {
      const newDoc: Document = {
        id: `doc-${Date.now()}`,
        title: template.title,
        content: template.content,
        tags: [...template.tags],
        category: 'draft',
        isFavorite: false,
        createdAt: Date.now(),
        updatedAt: Date.now(),
        snapshots: [],
      };
      setDocuments((prev) => [newDoc, ...prev]);
      setCurrentDocId(newDoc.id);
      showToast(`Loaded ${template.title}`);
    } else {
      handleUpdateTitle(template.title);
      handleUpdateContent(template.content);
      showToast(`Applied ${template.title}`);
    }
  };

  const handleResetSampleDocs = () => {
    setDocuments(INITIAL_DOCUMENTS);
    setCurrentDocId(INITIAL_DOCUMENTS[0].id);
    showToast('Sample documents reset');
  };

  const handleJumpToHeading = (heading: HeadingItem) => {
    if (!textareaRef.current) return;
    const textarea = textareaRef.current;
    const lines = currentDoc.content.split('\n');
    let charIndex = 0;
    for (let i = 0; i < heading.line - 1; i++) {
      charIndex += (lines[i]?.length || 0) + 1;
    }
    textarea.focus();
    textarea.setSelectionRange(charIndex, charIndex + (lines[heading.line - 1]?.length || 0));
    setOutlineOpen(false);
  };

  return (
    <div className="min-h-screen bg-stone-50 dark:bg-neutral-950 text-neutral-900 dark:text-neutral-100 flex flex-col font-modern selection:bg-neutral-200 dark:selection:bg-neutral-800 antialiased">
      {/* 3-Zone Header Contract */}
      <Header
        documentTitle={currentDoc?.title || ''}
        wordCount={stats.words}
        readingTimeMin={stats.readingTimeMinutes}
        viewMode={viewMode}
        setViewMode={setViewMode}
        zenMode={zenMode}
        setZenMode={setZenMode}
        onOpenSettings={() => setSettingsOpen(true)}
        onOpenExport={() => setExportOpen(true)}
        onOpenSnapshots={() => setSnapshotsOpen(true)}
        onToggleOutline={() => setOutlineOpen(!outlineOpen)}
        outlineOpen={outlineOpen}
        onToggleSidebar={() => setSidebarOpen(!sidebarOpen)}
        sidebarOpen={sidebarOpen}
        isDark={isDark}
        onToggleTheme={() => setIsDark(!isDark)}
        settings={settings}
        onUpdateSettings={(newVals) => setSettings((s) => ({ ...s, ...newVals }))}
        onOpenTimer={() => setTimerModalOpen(true)}
        isTimerRunning={isTimerRunning}
        timerFormatted={formattedTimer}
        onOpenCaseSimulator={() => setCaseSimulatorOpen(true)}
        onOpenGlobalCompetitions={() => setGlobalCompetitionsOpen(true)}
      />

      {/* Main Workspace Frame */}
      <div className="flex-1 flex overflow-hidden relative">
        {/* Document Sidebar */}
        <Sidebar
          documents={documents}
          currentDocumentId={currentDocId}
          onSelectDocument={(id) => setCurrentDocId(id)}
          onCreateNewDocument={handleCreateNewDocument}
          onOpenTemplates={() => setTemplatesOpen(true)}
          onDeleteDocument={handleDeleteDocument}
          onDuplicateDocument={handleDuplicateDocument}
          onToggleFavorite={handleToggleFavorite}
          onResetSampleDocs={handleResetSampleDocs}
          isOpen={sidebarOpen}
          onClose={() => setSidebarOpen(false)}
        />

        {/* Editor & Preview Canvas */}
        <main className="flex-1 flex overflow-hidden bg-stone-50/50 dark:bg-neutral-950">
          {/* Write / Editor Panel */}
          {(viewMode === 'edit' || viewMode === 'split') && (
            <div
              className={`h-full flex-1 overflow-hidden ${
                viewMode === 'split' ? 'border-r border-neutral-200 dark:border-neutral-800/80' : ''
              }`}
            >
              <Editor
                title={currentDoc?.title || ''}
                content={currentDoc?.content || ''}
                onChangeTitle={handleUpdateTitle}
                onChangeContent={handleUpdateContent}
                settings={settings}
                onSaveSnapshot={handleCreateSnapshot}
                textareaRef={textareaRef}
              />
            </div>
          )}

          {/* Formatted Reading Preview Panel */}
          {(viewMode === 'preview' || viewMode === 'split') && (
            <div className="h-full flex-1 overflow-hidden bg-white/40 dark:bg-neutral-900/40">
              <MarkdownPreview
                content={currentDoc?.content || ''}
                settings={settings}
              />
            </div>
          )}
        </main>

        {/* Outline & Metrics Drawer */}
        <OutlineDrawer
          isOpen={outlineOpen}
          onClose={() => setOutlineOpen(false)}
          headings={headings}
          stats={stats}
          onJumpToHeading={handleJumpToHeading}
        />

        {/* Snapshots Revision Drawer */}
        <SnapshotDrawer
          isOpen={snapshotsOpen}
          onClose={() => setSnapshotsOpen(false)}
          snapshots={currentDoc?.snapshots || []}
          onRestoreSnapshot={handleRestoreSnapshot}
          onCreateSnapshot={handleCreateSnapshot}
        />
      </div>

      {/* Modals & Dialogs */}
      <FocusTimerModal
        isOpen={timerModalOpen}
        onClose={() => setTimerModalOpen(false)}
        timeLeft={timeLeft}
        isRunning={isTimerRunning}
        onStart={() => setIsTimerRunning(true)}
        onPause={() => setIsTimerRunning(false)}
        onReset={(minutes) => {
          setTimerDuration(minutes * 60);
          setTimeLeft(minutes * 60);
          setIsTimerRunning(false);
        }}
      />

      <SettingsModal
        isOpen={settingsOpen}
        onClose={() => setSettingsOpen(false)}
        settings={settings}
        onUpdateSettings={(newVals) => setSettings((s) => ({ ...s, ...newVals }))}
      />

      <ExportModal
        isOpen={exportOpen}
        onClose={() => setExportOpen(false)}
        title={currentDoc?.title || ''}
        content={currentDoc?.content || ''}
        settings={settings}
      />

      <TemplatesModal
        isOpen={templatesOpen}
        onClose={() => setTemplatesOpen(false)}
        onApplyTemplate={handleApplyTemplate}
      />

      <ShortcutsModal
        isOpen={shortcutsOpen}
        onClose={() => setShortcutsOpen(false)}
      />

      <CaseSimulatorModal
        isOpen={caseSimulatorOpen}
        onClose={() => setCaseSimulatorOpen(false)}
        onLoadCaseIntoEditor={(markdown) => {
          handleUpdateContent(markdown);
          handleUpdateTitle('Championship Strategy Proposal');
          setToastMessage('Case solution loaded into editor');
          setTimeout(() => setToastMessage(null), 3000);
        }}
      />

      <GlobalCompetitionsModal
        isOpen={globalCompetitionsOpen}
        onClose={() => setGlobalCompetitionsOpen(false)}
      />

      {/* Floating Status / Keyboard Help Pill on Desktop */}
      {!zenMode && (
        <footer className="no-print h-7 border-t border-neutral-200/60 dark:border-neutral-800/60 bg-white/50 dark:bg-neutral-900/50 px-4 text-[11px] text-neutral-400 dark:text-neutral-500 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <span>{stats.paragraphs} paragraphs</span>
            <span aria-hidden="true">·</span>
            <span>{stats.characters} characters</span>
            <span aria-hidden="true">·</span>
            <span className="hidden sm:inline font-mono">Flesch {stats.fleschScore}</span>
          </div>

          <div className="flex items-center gap-3">
            <button
              onClick={() => setShortcutsOpen(true)}
              className="hover:text-neutral-800 dark:hover:text-neutral-200 transition-colors"
            >
              Shortcuts (Cmd+K)
            </button>
            <span aria-hidden="true">·</span>
            <span>Case-Study Studio · Academic & Competition Strategy Platform</span>
          </div>
        </footer>
      )}

      {/* Transient Notification Toast */}
      {toastMessage && (
        <div className="fixed bottom-10 left-1/2 -translate-x-1/2 z-50 bg-neutral-900/90 text-white dark:bg-neutral-100/90 dark:text-neutral-900 text-xs px-4 py-2 rounded-lg shadow-lg backdrop-blur-xs animate-in fade-in slide-in-from-bottom-2 duration-150">
          {toastMessage}
        </div>
      )}
    </div>
  );
}
