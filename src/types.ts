export interface DocumentSnapshot {
  id: string;
  timestamp: number;
  title: string;
  content: string;
  wordCount: number;
}

export interface Document {
  id: string;
  title: string;
  content: string;
  tags: string[];
  category: 'draft' | 'published' | 'archive' | 'note';
  isFavorite: boolean;
  createdAt: number;
  updatedAt: number;
  snapshots: DocumentSnapshot[];
}

export type EditorFontFamily = 'editorial' | 'modern' | 'code';
export type EditorMeasure = 'narrow' | 'standard' | 'wide';
export type ViewMode = 'edit' | 'split' | 'preview';
export type AmbientSoundType = 'none' | 'typewriter' | 'rain' | 'library';

export interface EditorSettings {
  fontFamily: EditorFontFamily;
  fontSize: number; // 15 to 22
  lineHeight: number; // 1.5, 1.75, 2.0
  measure: EditorMeasure; // narrow: 640px, standard: 780px, wide: 940px
  typewriterMode: boolean;
  soundEnabled: boolean;
  ambientSound: AmbientSoundType;
  soundVolume: number; // 0 to 1
  autoSaveInterval: number; // in seconds
}

export interface HeadingItem {
  id: string;
  level: number;
  text: string;
  line: number;
}

export interface DocumentStats {
  words: number;
  characters: number;
  charactersNoSpaces: number;
  paragraphs: number;
  readingTimeMinutes: number;
  readabilityGrade: string;
  fleschScore: number;
}
