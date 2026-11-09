import React, { useRef, useEffect } from 'react';
import { EditorSettings } from '../types';
import { soundEngine } from '../utils/audio';

interface EditorProps {
  title: string;
  content: string;
  onChangeTitle: (title: string) => void;
  onChangeContent: (content: string) => void;
  settings: EditorSettings;
  onSaveSnapshot?: () => void;
  textareaRef: React.RefObject<HTMLTextAreaElement | null>;
}

export const Editor: React.FC<EditorProps> = ({
  title,
  content,
  onChangeTitle,
  onChangeContent,
  settings,
  onSaveSnapshot,
  textareaRef,
}) => {
  const containerRef = useRef<HTMLDivElement>(null);

  // Typewriter mode scrolling
  const handleScrollToCursor = () => {
    if (!settings.typewriterMode || !textareaRef.current || !containerRef.current) return;
    const textarea = textareaRef.current;
    const container = containerRef.current;

    const selectionStart = textarea.selectionStart;
    const textBeforeCursor = textarea.value.substring(0, selectionStart);
    const lineIndex = textBeforeCursor.split('\n').length - 1;
    const lineHeightPx = settings.fontSize * settings.lineHeight;

    const targetScrollTop = lineIndex * lineHeightPx - container.clientHeight / 2 + 100;
    container.scrollTo({
      top: Math.max(0, targetScrollTop),
      behavior: 'smooth',
    });
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    // Sound feedback
    if (settings.soundEnabled) {
      const isSpace = e.key === ' ';
      const isEnter = e.key === 'Enter';
      soundEngine.playKeyClick(isSpace, isEnter);
    }

    const textarea = textareaRef.current;
    if (!textarea) return;

    // Handle Tab key
    if (e.key === 'Tab') {
      e.preventDefault();
      const start = textarea.selectionStart;
      const end = textarea.selectionEnd;
      const newContent = content.substring(0, start) + '  ' + content.substring(end);
      onChangeContent(newContent);
      setTimeout(() => {
        textarea.selectionStart = textarea.selectionEnd = start + 2;
      }, 0);
      return;
    }

    // Handle Cmd/Ctrl shortcuts
    if (e.metaKey || e.ctrlKey) {
      if (e.key.toLowerCase() === 's') {
        e.preventDefault();
        onSaveSnapshot?.();
        return;
      }

      if (e.key.toLowerCase() === 'b') {
        e.preventDefault();
        wrapSelection('**', '**');
        return;
      }

      if (e.key.toLowerCase() === 'i') {
        e.preventDefault();
        wrapSelection('*', '*');
        return;
      }

      if (e.key.toLowerCase() === 'k') {
        e.preventDefault();
        wrapSelection('[', '](url)');
        return;
      }
    }
  };

  const wrapSelection = (prefix: string, suffix: string) => {
    const textarea = textareaRef.current;
    if (!textarea) return;
    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;
    const selected = content.substring(start, end);
    const replacement = `${prefix}${selected || 'text'}${suffix}`;
    const newContent = content.substring(0, start) + replacement + content.substring(end);
    onChangeContent(newContent);
    setTimeout(() => {
      textarea.selectionStart = start + prefix.length;
      textarea.selectionEnd = start + prefix.length + (selected.length || 4);
      textarea.focus();
    }, 0);
  };

  // Adjust container width and font class
  const maxWidthClass =
    settings.measure === 'narrow' ? 'max-w-[640px]' :
    settings.measure === 'wide' ? 'max-w-[940px]' :
    'max-w-[780px]';

  const fontClass =
    settings.fontFamily === 'editorial' ? 'font-editorial' :
    settings.fontFamily === 'code' ? 'font-code' :
    'font-modern';

  return (
    <div
      ref={containerRef}
      className="h-full overflow-y-auto px-6 py-10 md:px-12 selection:bg-neutral-200 dark:selection:bg-neutral-800"
    >
      <div className={`mx-auto ${maxWidthClass} transition-all`}>
        {/* Title Input */}
        <input
          type="text"
          value={title}
          onChange={(e) => onChangeTitle(e.target.value)}
          placeholder="A New Beginning..."
          className="w-full bg-transparent text-2xl md:text-3xl font-bold tracking-tight text-neutral-900 dark:text-neutral-50 border-none outline-hidden placeholder:text-neutral-300 dark:placeholder:text-neutral-700 mb-6 font-modern transition-colors"
        />

        {/* Writing Canvas Textarea */}
        <textarea
          ref={textareaRef}
          value={content}
          onChange={(e) => {
            onChangeContent(e.target.value);
            handleScrollToCursor();
          }}
          onKeyDown={handleKeyDown}
          onClick={handleScrollToCursor}
          onKeyUp={handleScrollToCursor}
          placeholder="Start writing... Use Markdown for structure (# for heading, > for quotes, ``` for code, - for lists)."
          className={`w-full bg-transparent resize-none border-none outline-hidden text-neutral-800 dark:text-neutral-200 placeholder:text-neutral-300 dark:placeholder:text-neutral-700 min-h-[75vh] ${fontClass}`}
          style={{
            fontSize: `${settings.fontSize}px`,
            lineHeight: settings.lineHeight,
          }}
          autoFocus
          spellCheck={true}
        />
      </div>
    </div>
  );
};
