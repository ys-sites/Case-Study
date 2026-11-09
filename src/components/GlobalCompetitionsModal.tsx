import React, { useState, useMemo } from 'react';
import { X, Search, Globe, Trophy, ExternalLink, Filter, BookOpen } from 'lucide-react';
import competitionsData from '../data/competitions.json';

interface Competition {
  "#": string;
  Competition: string;
  "Country / region": string;
  "Typical focus": string;
  "Suggested solution model (NOT winner)": string;
  "Evidence status": string;
  "Directory source": string;
}

interface GlobalCompetitionsModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSelectCompetition?: (comp: Competition) => void;
}

export const GlobalCompetitionsModal: React.FC<GlobalCompetitionsModalProps> = ({
  isOpen,
  onClose,
  onSelectCompetition,
}) => {
  const [search, setSearch] = useState('');
  const [selectedFocus, setSelectedFocus] = useState<string>('All');
  const [selectedRegion, setSelectedRegion] = useState<string>('All');

  const competitions = competitionsData as Competition[];

  const focusOptions = useMemo(() => {
    const set = new Set<string>();
    competitions.forEach((c) => {
      if (c['Typical focus']) set.add(c['Typical focus'].trim());
    });
    return ['All', ...Array.from(set).sort()];
  }, [competitions]);

  const regionOptions = useMemo(() => {
    const set = new Set<string>();
    competitions.forEach((c) => {
      if (c['Country / region']) set.add(c['Country / region'].trim());
    });
    return ['All', ...Array.from(set).sort()];
  }, [competitions]);

  const filtered = useMemo(() => {
    return competitions.filter((c) => {
      const matchSearch =
        c.Competition.toLowerCase().includes(search.toLowerCase()) ||
        c['Typical focus'].toLowerCase().includes(search.toLowerCase()) ||
        c['Suggested solution model (NOT winner)'].toLowerCase().includes(search.toLowerCase());
      const matchFocus = selectedFocus === 'All' || c['Typical focus'] === selectedFocus;
      const matchRegion = selectedRegion === 'All' || c['Country / region'] === selectedRegion;
      return matchSearch && matchFocus && matchRegion;
    });
  }, [competitions, search, selectedFocus, selectedRegion]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-fade-in">
      <div className="relative w-full max-w-5xl h-[85vh] flex flex-col bg-stone-50 dark:bg-stone-900 border border-stone-200 dark:border-stone-800 rounded-2xl shadow-2xl overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-stone-200 dark:border-stone-800 bg-white dark:bg-stone-950">
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-xl bg-amber-500/10 text-amber-600 dark:text-amber-400">
              <Trophy className="w-6 h-6" />
            </div>
            <div>
              <h2 className="text-xl font-bold text-stone-900 dark:text-stone-100">
                Global Case Competition Intelligence Directory
              </h2>
              <p className="text-xs text-stone-500 dark:text-stone-400">
                Verified repository of 132+ prestigious university & corporate case challenges worldwide
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-2 rounded-lg text-stone-400 hover:text-stone-600 dark:hover:text-stone-200 hover:bg-stone-100 dark:hover:bg-stone-800 transition"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Filters & Search */}
        <div className="p-6 border-b border-stone-200 dark:border-stone-800 bg-stone-100/50 dark:bg-stone-900/50 space-y-3">
          <div className="flex flex-col sm:flex-row gap-3">
            <div className="relative flex-1">
              <Search className="absolute left-3.5 top-3 w-4 h-4 text-stone-400" />
              <input
                type="text"
                placeholder="Search by competition name, focus area, or solution model..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                className="w-full pl-10 pr-4 py-2 text-sm bg-white dark:bg-stone-950 border border-stone-200 dark:border-stone-800 rounded-xl focus:outline-none focus:ring-2 focus:ring-amber-500 text-stone-900 dark:text-stone-100"
              />
            </div>
            <div className="flex gap-2">
              <select
                value={selectedFocus}
                onChange={(e) => setSelectedFocus(e.target.value)}
                className="px-3 py-2 text-xs bg-white dark:bg-stone-950 border border-stone-200 dark:border-stone-800 rounded-xl focus:outline-none focus:ring-2 focus:ring-amber-500 text-stone-700 dark:text-stone-300"
              >
                <option value="All">All Disciplines</option>
                {focusOptions.filter((f) => f !== 'All').map((f) => (
                  <option key={f} value={f}>{f}</option>
                ))}
              </select>
              <select
                value={selectedRegion}
                onChange={(e) => setSelectedRegion(e.target.value)}
                className="px-3 py-2 text-xs bg-white dark:bg-stone-950 border border-stone-200 dark:border-stone-800 rounded-xl focus:outline-none focus:ring-2 focus:ring-amber-500 text-stone-700 dark:text-stone-300"
              >
                <option value="All">All Regions</option>
                {regionOptions.filter((r) => r !== 'All').map((r) => (
                  <option key={r} value={r}>{r}</option>
                ))}
              </select>
            </div>
          </div>
          <div className="text-xs text-stone-500 dark:text-stone-400 flex items-center justify-between">
            <span>Showing {filtered.length} of {competitions.length} competitions</span>
            <span className="font-mono text-[11px] text-amber-600 dark:text-amber-400">
              Source: data/global_case_competitions_research.csv
            </span>
          </div>
        </div>

        {/* Directory List */}
        <div className="flex-1 overflow-y-auto p-6 space-y-3">
          {filtered.length === 0 ? (
            <div className="text-center py-16 text-stone-400">
              <BookOpen className="w-12 h-12 mx-auto mb-3 opacity-30" />
              <p>No competitions match your search filters.</p>
            </div>
          ) : (
            filtered.map((comp) => (
              <div
                key={comp['#']}
                className="p-4 rounded-xl bg-white dark:bg-stone-950 border border-stone-200 dark:border-stone-800 hover:border-amber-500/50 transition group shadow-xs"
              >
                <div className="flex items-start justify-between gap-4">
                  <div>
                    <div className="flex items-center gap-2 mb-1">
                      <span className="text-xs font-mono px-2 py-0.5 rounded-md bg-stone-100 dark:bg-stone-800 text-stone-600 dark:text-stone-300">
                        #{comp['#']}
                      </span>
                      <h3 className="font-semibold text-stone-900 dark:text-stone-100 group-hover:text-amber-600 dark:group-hover:text-amber-400 transition">
                        {comp.Competition}
                      </h3>
                      <span className="text-xs px-2.5 py-0.5 rounded-full bg-amber-500/10 text-amber-700 dark:text-amber-300 border border-amber-500/20 font-medium">
                        {comp['Typical focus']}
                      </span>
                    </div>
                    <div className="text-xs text-stone-500 dark:text-stone-400 flex items-center gap-2 mb-2">
                      <Globe className="w-3.5 h-3.5" />
                      <span>{comp['Country / region']}</span>
                      <span>•</span>
                      <span>{comp['Evidence status']}</span>
                    </div>
                    <div className="text-xs text-stone-600 dark:text-stone-300 bg-stone-50 dark:bg-stone-900/60 p-2.5 rounded-lg border border-stone-100 dark:border-stone-800 font-mono">
                      <span className="text-amber-600 dark:text-amber-400 font-semibold">Solution Archetype: </span>
                      {comp['Suggested solution model (NOT winner)']}
                    </div>
                  </div>
                  {comp['Directory source'] && (
                    <a
                      href={comp['Directory source']}
                      target="_blank"
                      rel="noreferrer"
                      className="p-2 rounded-lg text-stone-400 hover:text-amber-600 dark:hover:text-amber-400 hover:bg-stone-100 dark:hover:bg-stone-800 transition shrink-0"
                      title="View competition directory source"
                    >
                      <ExternalLink className="w-4 h-4" />
                    </a>
                  )}
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};
