import React, { useState, useMemo } from 'react';
import {
  Plus,
  Search,
  Star,
  Trash2,
  BookOpen,
  X,
  FileText,
  Copy,
  RotateCcw,
} from 'lucide-react';
import { Document } from '../types';

interface SidebarProps {
  documents: Document[];
  currentDocumentId: string;
  onSelectDocument: (id: string) => void;
  onCreateNewDocument: () => void;
  onOpenTemplates: () => void;
  onDeleteDocument: (id: string) => void;
  onDuplicateDocument: (doc: Document) => void;
  onToggleFavorite: (id: string) => void;
  onResetSampleDocs: () => void;
  isOpen: boolean;
  onClose: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({
  documents,
  currentDocumentId,
  onSelectDocument,
  onCreateNewDocument,
  onOpenTemplates,
  onDeleteDocument,
  onDuplicateDocument,
  onToggleFavorite,
  onResetSampleDocs,
  isOpen,
  onClose,
}) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [activeFilter, setActiveFilter] = useState<'all' | 'favorites' | 'draft' | 'published'>('all');
  const [selectedTag, setSelectedTag] = useState<string | null>(null);

  // Collect unique tags
  const allTags = useMemo(() => {
    const set = new Set<string>();
    documents.forEach((d) => d.tags.forEach((t) => set.add(t)));
    return Array.from(set);
  }, [documents]);

  // Filtered documents
  const filteredDocs = useMemo(() => {
    return documents.filter((doc) => {
      if (activeFilter === 'favorites' && !doc.isFavorite) return false;
      if (activeFilter === 'draft' && doc.category !== 'draft') return false;
      if (activeFilter === 'published' && doc.category !== 'published') return false;
      if (selectedTag && !doc.tags.includes(selectedTag)) return false;

      if (searchQuery.trim()) {
        const query = searchQuery.toLowerCase();
        const matchesTitle = doc.title.toLowerCase().includes(query);
        const matchesContent = doc.content.toLowerCase().includes(query);
        const matchesTags = doc.tags.some((t) => t.toLowerCase().includes(query));
        return matchesTitle || matchesContent || matchesTags;
      }
      return true;
    });
  }, [documents, activeFilter, selectedTag, searchQuery]);

  const formatRelativeTime = (timestamp: number) => {
    const diffSec = Math.floor((Date.now() - timestamp) / 1000);
    if (diffSec < 60) return 'just now';
    if (diffSec < 3600) return `${Math.floor(diffSec / 60)}m ago`;
    if (diffSec < 86400) return `${Math.floor(diffSec / 3600)}h ago`;
    return `${Math.floor(diffSec / 86400)}d ago`;
  };

  const getWordCount = (text: string) => {
    return (text.trim().match(/\b[A-Za-z0-9_-]+\b/g) || []).length;
  };

  return (
    <>
      {/* Mobile Backdrop */}
      {isOpen && (
        <div
          onClick={onClose}
          className="fixed inset-0 bg-neutral-900/30 backdrop-blur-xs z-30 lg:hidden"
        />
      )}

      <aside
        className={`fixed lg:static top-0 left-0 bottom-0 z-40 w-72 md:w-80 bg-stone-50 dark:bg-neutral-900/95 border-r border-neutral-200 dark:border-neutral-800 flex flex-col transition-transform duration-200 ease-out ${
          isOpen ? 'translate-x-0' : '-translate-x-full lg:-translate-x-full'
        }`}
      >
        {/* Sidebar Header */}
        <div className="p-4 border-b border-neutral-200/80 dark:border-neutral-800 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="font-editorial text-lg font-semibold text-neutral-900 dark:text-neutral-100">
              Case Briefs & Decks
            </span>
            <span className="text-xs text-neutral-400 font-mono tabular-nums">
              ({documents.length})
            </span>
          </div>
          <button
            onClick={onClose}
            className="p-1 text-neutral-400 hover:text-neutral-700 dark:hover:text-neutral-200 rounded-md hover:bg-neutral-200/50 dark:hover:bg-neutral-800 transition-colors"
            aria-label="Close sidebar"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Action Buttons */}
        <div className="p-3 grid grid-cols-2 gap-2 border-b border-neutral-200/80 dark:border-neutral-800">
          <button
            onClick={() => {
              onCreateNewDocument();
              if (window.innerWidth < 1024) onClose();
            }}
            className="flex items-center justify-center gap-1.5 px-3 py-2 text-xs font-semibold text-white bg-neutral-900 hover:bg-neutral-800 dark:bg-neutral-100 dark:text-neutral-900 dark:hover:bg-white rounded-md transition-all shadow-xs active:scale-98"
          >
            <Plus className="w-3.5 h-3.5" />
            <span>New Brief</span>
          </button>

          <button
            onClick={() => {
              onOpenTemplates();
              if (window.innerWidth < 1024) onClose();
            }}
            className="flex items-center justify-center gap-1.5 px-3 py-2 text-xs font-medium text-neutral-700 dark:text-neutral-300 bg-white dark:bg-neutral-800 hover:bg-neutral-100 dark:hover:bg-neutral-750 border border-neutral-200 dark:border-neutral-700 rounded-md transition-colors"
          >
            <BookOpen className="w-3.5 h-3.5" />
            <span>Frameworks</span>
          </button>
        </div>

        {/* Search */}
        <div className="p-3 pb-2">
          <div className="relative">
            <Search className="w-3.5 h-3.5 absolute left-3 top-1/2 -translate-y-1/2 text-neutral-400" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search documents or text..."
              className="w-full pl-8 pr-3 py-1.5 text-xs bg-white dark:bg-neutral-800/80 border border-neutral-200 dark:border-neutral-700/80 rounded-md focus:outline-hidden focus:ring-1 focus:ring-neutral-400 dark:focus:ring-neutral-500 placeholder:text-neutral-400 dark:text-neutral-200"
            />
            {searchQuery && (
              <button
                onClick={() => setSearchQuery('')}
                className="absolute right-2.5 top-1/2 -translate-y-1/2 text-neutral-400 hover:text-neutral-600"
              >
                <X className="w-3 h-3" />
              </button>
            )}
          </div>
        </div>

        {/* Filter Tabs (Segmented Control) */}
        <div className="px-3 pb-2">
          <div className="flex items-center gap-1 p-0.5 bg-neutral-200/60 dark:bg-neutral-800 rounded-md text-[11px]">
            <button
              onClick={() => setActiveFilter('all')}
              className={`flex-1 py-1 font-medium rounded transition-colors ${
                activeFilter === 'all'
                  ? 'bg-white dark:bg-neutral-700 text-neutral-900 dark:text-neutral-100 shadow-xs'
                  : 'text-neutral-600 dark:text-neutral-400 hover:text-neutral-900'
              }`}
            >
              All
            </button>
            <button
              onClick={() => setActiveFilter('favorites')}
              className={`flex-1 py-1 font-medium rounded transition-colors ${
                activeFilter === 'favorites'
                  ? 'bg-white dark:bg-neutral-700 text-neutral-900 dark:text-neutral-100 shadow-xs'
                  : 'text-neutral-600 dark:text-neutral-400 hover:text-neutral-900'
              }`}
            >
              Starred
            </button>
            <button
              onClick={() => setActiveFilter('draft')}
              className={`flex-1 py-1 font-medium rounded transition-colors ${
                activeFilter === 'draft'
                  ? 'bg-white dark:bg-neutral-700 text-neutral-900 dark:text-neutral-100 shadow-xs'
                  : 'text-neutral-600 dark:text-neutral-400 hover:text-neutral-900'
              }`}
            >
              Drafts
            </button>
            <button
              onClick={() => setActiveFilter('published')}
              className={`flex-1 py-1 font-medium rounded transition-colors ${
                activeFilter === 'published'
                  ? 'bg-white dark:bg-neutral-700 text-neutral-900 dark:text-neutral-100 shadow-xs'
                  : 'text-neutral-600 dark:text-neutral-400 hover:text-neutral-900'
              }`}
            >
              Ready
            </button>
          </div>
        </div>

        {/* Tag Filters (clean interactive pills only for filtering, zero static pills) */}
        {allTags.length > 0 && (
          <div className="px-3 py-1 flex items-center gap-1 overflow-x-auto no-scrollbar border-b border-neutral-200/60 dark:border-neutral-800/80">
            <button
              onClick={() => setSelectedTag(null)}
              className={`px-2 py-0.5 text-[11px] rounded transition-colors whitespace-nowrap ${
                selectedTag === null
                  ? 'bg-neutral-800 text-white dark:bg-neutral-200 dark:text-neutral-900'
                  : 'text-neutral-500 hover:text-neutral-900 dark:hover:text-neutral-300'
              }`}
            >
              All Tags
            </button>
            {allTags.map((tag) => (
              <button
                key={tag}
                onClick={() => setSelectedTag(selectedTag === tag ? null : tag)}
                className={`px-2 py-0.5 text-[11px] rounded transition-colors whitespace-nowrap ${
                  selectedTag === tag
                    ? 'bg-neutral-800 text-white dark:bg-neutral-200 dark:text-neutral-900'
                    : 'text-neutral-500 hover:text-neutral-900 dark:hover:text-neutral-300'
                }`}
              >
                #{tag}
              </button>
            ))}
          </div>
        )}

        {/* Document List */}
        <div className="flex-1 overflow-y-auto px-2 py-2 space-y-1">
          {filteredDocs.length === 0 ? (
            <div className="p-6 text-center text-xs text-neutral-400 space-y-2">
              <FileText className="w-8 h-8 mx-auto text-neutral-300 dark:text-neutral-700 stroke-[1.5]" />
              <p>No documents found</p>
              <button
                onClick={onCreateNewDocument}
                className="text-neutral-900 dark:text-neutral-200 underline underline-offset-2 hover:text-neutral-600"
              >
                Create a blank page
              </button>
            </div>
          ) : (
            filteredDocs.map((doc) => {
              const isSelected = doc.id === currentDocumentId;
              const words = getWordCount(doc.content);

              return (
                <div
                  key={doc.id}
                  onClick={() => {
                    onSelectDocument(doc.id);
                    if (window.innerWidth < 1024) onClose();
                  }}
                  className={`group relative p-2.5 rounded-lg text-left cursor-pointer transition-all ${
                    isSelected
                      ? 'bg-white dark:bg-neutral-800 border border-neutral-200/80 dark:border-neutral-700 shadow-2xs'
                      : 'hover:bg-neutral-200/40 dark:hover:bg-neutral-800/50 border border-transparent'
                  }`}
                >
                  <div className="flex items-start justify-between gap-2">
                    <h4
                      className={`text-xs font-semibold truncate ${
                        isSelected
                          ? 'text-neutral-900 dark:text-neutral-100'
                          : 'text-neutral-700 dark:text-neutral-300'
                      }`}
                    >
                      {doc.title || 'Untitled Draft'}
                    </h4>
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        onToggleFavorite(doc.id);
                      }}
                      className={`p-0.5 rounded transition-colors ${
                        doc.isFavorite
                          ? 'text-amber-500'
                          : 'text-neutral-300 dark:text-neutral-600 hover:text-neutral-500 opacity-0 group-hover:opacity-100'
                      }`}
                      aria-label="Star document"
                    >
                      <Star
                        className={`w-3.5 h-3.5 ${doc.isFavorite ? 'fill-amber-500' : ''}`}
                      />
                    </button>
                  </div>

                  {/* Snippet */}
                  <p className="text-[11px] text-neutral-400 line-clamp-1 mt-1 leading-snug">
                    {doc.content.replace(/^#+\s+/gm, '').replace(/[*_`]/g, '') ||
                      'Empty blank page...'}
                  </p>

                  {/* Clean unboxed metadata with typographic dots as mandated by frontend-design */}
                  <div className="flex items-center gap-2 text-[10px] text-neutral-400 dark:text-neutral-500 mt-2">
                    <span className="font-mono tabular-nums">{words} words</span>
                    <span aria-hidden="true">·</span>
                    <span>{formatRelativeTime(doc.updatedAt)}</span>
                    {doc.tags.length > 0 && (
                      <>
                        <span aria-hidden="true">·</span>
                        <span className="truncate">#{doc.tags[0]}</span>
                      </>
                    )}
                  </div>

                  {/* Quick actions hover toolbar */}
                  <div className="absolute right-2 bottom-2 hidden group-hover:flex items-center gap-1 bg-white dark:bg-neutral-800 pl-1.5 py-0.5 rounded shadow-xs border border-neutral-200/60 dark:border-neutral-700/60">
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        onDuplicateDocument(doc);
                      }}
                      title="Duplicate"
                      className="p-1 text-neutral-400 hover:text-neutral-700 dark:hover:text-neutral-200"
                    >
                      <Copy className="w-3 h-3" />
                    </button>
                    {documents.length > 1 && (
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          onDeleteDocument(doc.id);
                        }}
                        title="Delete"
                        className="p-1 text-neutral-400 hover:text-red-600 dark:hover:text-red-400"
                      >
                        <Trash2 className="w-3 h-3" />
                      </button>
                    )}
                  </div>
                </div>
              );
            })
          )}
        </div>

        {/* Sidebar Footer */}
        <div className="p-3 border-t border-neutral-200/80 dark:border-neutral-800 text-[11px] text-neutral-400 flex items-center justify-between">
          <span>Auto-saved locally</span>
          <button
            onClick={onResetSampleDocs}
            className="flex items-center gap-1 hover:text-neutral-700 dark:hover:text-neutral-200 transition-colors"
            title="Restore sample documents"
          >
            <RotateCcw className="w-3 h-3" />
            <span>Reset Samples</span>
          </button>
        </div>
      </aside>
    </>
  );
};
