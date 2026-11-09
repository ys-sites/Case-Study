import { DocumentStats, HeadingItem } from '../types';

/**
 * Extract markdown headings (#, ##, ###) for real-time table of contents outline.
 */
export function extractHeadings(content: string): HeadingItem[] {
  const lines = content.split('\n');
  const headings: HeadingItem[] = [];

  lines.forEach((line, index) => {
    const match = line.match(/^(#{1,3})\s+(.+)$/);
    if (match) {
      const level = match[1].length;
      const text = match[2].trim();
      const id = text
        .toLowerCase()
        .replace(/[^\w\s-]/g, '')
        .replace(/\s+/g, '-');
      headings.push({
        id: `${id}-${index}`,
        level,
        text,
        line: index + 1,
      });
    }
  });

  return headings;
}

/**
 * Calculate comprehensive writing statistics and readability.
 */
export function calculateStats(content: string): DocumentStats {
  const clean = content.trim();
  if (!clean) {
    return {
      words: 0,
      characters: 0,
      charactersNoSpaces: 0,
      paragraphs: 0,
      readingTimeMinutes: 0,
      readabilityGrade: 'N/A',
      fleschScore: 100,
    };
  }

  const wordsArray = clean.match(/\b[A-Za-z0-9_-]+\b/g) || [];
  const words = wordsArray.length;
  const characters = clean.length;
  const charactersNoSpaces = clean.replace(/\s/g, '').length;

  const paragraphs = clean
    .split(/\n\s*\n/)
    .map((p) => p.trim())
    .filter((p) => p.length > 0).length;

  const sentences = (clean.match(/[.!?]+(\s|$)/g) || []).length || 1;

  // Reading time at average 220 words per minute
  const readingTimeMinutes = Math.max(1, Math.ceil(words / 220));

  // Count syllables roughly for Flesch Reading Ease
  let syllables = 0;
  wordsArray.forEach((word) => {
    const w = word.toLowerCase();
    if (w.length <= 3) {
      syllables += 1;
      return;
    }
    const matches = w.match(/[aeiouy]{1,2}/g);
    const count = matches ? matches.length : 1;
    syllables += Math.max(1, count);
  });

  // Flesch Reading Ease Formula = 206.835 - (1.015 * (words / sentences)) - (84.6 * (syllables / words))
  const wordsPerSentence = words / Math.max(1, sentences);
  const syllablesPerWord = syllables / Math.max(1, words);
  let flesch = 206.835 - 1.015 * wordsPerSentence - 84.6 * syllablesPerWord;
  flesch = Math.max(0, Math.min(100, Math.round(flesch)));

  let readabilityGrade = 'College';
  if (flesch >= 90) readabilityGrade = '5th Grade (Very Easy)';
  else if (flesch >= 80) readabilityGrade = '6th Grade (Easy)';
  else if (flesch >= 70) readabilityGrade = '7th Grade (Fairly Easy)';
  else if (flesch >= 60) readabilityGrade = '8th–9th Grade (Standard)';
  else if (flesch >= 50) readabilityGrade = '10th–12th Grade (Moderate)';
  else if (flesch >= 30) readabilityGrade = 'College (Difficult)';
  else readabilityGrade = 'Academic / Specialist';

  return {
    words,
    characters,
    charactersNoSpaces,
    paragraphs: Math.max(1, paragraphs),
    readingTimeMinutes,
    readabilityGrade,
    fleschScore: flesch,
  };
}

/**
 * Escapes HTML characters to prevent XSS.
 */
function escapeHtml(text: string): string {
  return text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

/**
 * Robust, clean Markdown to HTML parser supporting typography, lists, callouts, tables, and code blocks.
 */
export function renderMarkdown(markdown: string): string {
  if (!markdown) return '';

  let html = markdown;

  // Code blocks ```lang ... ```
  html = html.replace(/```([a-zA-Z0-9_-]*)\n([\s\S]*?)```/g, (_, lang, code) => {
    const escaped = escapeHtml(code.trimEnd());
    const langLabel = lang ? `<span class="text-xs uppercase text-neutral-400 font-mono tracking-wider">${escapeHtml(lang)}</span>` : '';
    return `<div class="my-6 rounded-lg bg-neutral-900 text-neutral-100 p-4 font-mono text-sm overflow-x-auto border border-neutral-800">
      ${langLabel ? `<div class="flex justify-between items-center mb-2 pb-2 border-b border-neutral-800">${langLabel}</div>` : ''}
      <pre><code>${escaped}</code></pre>
    </div>`;
  });

  // Inline code `code`
  html = html.replace(/`([^`]+)`/g, (_, code) => {
    return `<code class="px-1.5 py-0.5 rounded bg-neutral-100 dark:bg-neutral-800 font-mono text-[0.88em] text-amber-700 dark:text-amber-300">${escapeHtml(code)}</code>`;
  });

  // Blockquotes > quote
  html = html.replace(/^\s*>\s+(.+)$/gm, '<blockquote class="border-l-2 border-neutral-300 dark:border-neutral-700 pl-4 py-1 my-4 italic text-neutral-600 dark:text-neutral-400 font-editorial text-lg leading-relaxed">$1</blockquote>');

  // Headings
  html = html.replace(/^###\s+(.+)$/gm, '<h3 class="text-lg font-bold tracking-tight text-neutral-900 dark:text-neutral-100 mt-7 mb-2">$1</h3>');
  html = html.replace(/^##\s+(.+)$/gm, '<h2 class="text-xl font-bold tracking-tight text-neutral-900 dark:text-neutral-100 mt-9 mb-3 pb-1 border-b border-neutral-200/60 dark:border-neutral-800">$1</h2>');
  html = html.replace(/^#\s+(.+)$/gm, '<h1 class="text-3xl font-extrabold tracking-tight text-neutral-900 dark:text-neutral-50 mt-6 mb-4">$1</h1>');

  // Horizontal Rule --- or ***
  html = html.replace(/^(?:---|___|\*\*\*)$/gm, '<hr class="my-8 border-neutral-200 dark:border-neutral-800" />');

  // Bold & Italic
  html = html.replace(/\*\*\*([^*]+)\*\*\*/g, '<strong><em>$1</em></strong>');
  html = html.replace(/\*\*([^*]+)\*\*/g, '<strong class="font-semibold text-neutral-900 dark:text-neutral-100">$1</strong>');
  html = html.replace(/\*([^*]+)\*/g, '<em>$1</em>');
  html = html.replace(/_([^_]+)_/g, '<em>$1</em>');

  // Strike-through ~~text~~
  html = html.replace(/~~([^~]+)~~/g, '<del class="line-through text-neutral-400">$1</del>');

  // Checkbox list items - [ ] or - [x]
  html = html.replace(/^\s*-\s+\[(x|X)\]\s+(.+)$/gm, '<li class="flex items-start gap-2.5 my-1.5 list-none"><input type="checkbox" checked disabled class="mt-1 accent-neutral-800 dark:accent-neutral-200 cursor-default" /><span>$2</span></li>');
  html = html.replace(/^\s*-\s+\[\s\]\s+(.+)$/gm, '<li class="flex items-start gap-2.5 my-1.5 list-none"><input type="checkbox" disabled class="mt-1 cursor-default" /><span>$1</span></li>');

  // Unordered list items - item or * item
  html = html.replace(/^\s*[-*]\s+(.+)$/gm, '<li class="my-1.5 ml-4 list-disc">$1</li>');

  // Ordered list items 1. item
  html = html.replace(/^\s*\d+\.\s+(.+)$/gm, '<li class="my-1.5 ml-4 list-decimal">$1</li>');

  // Wrap consecutive <li> into <ul> or <ol>
  html = html.replace(/(<li[^>]*>.*?<\/li>\s*)+/g, (match) => {
    if (match.includes('list-decimal')) {
      return `<ol class="my-4 pl-2 space-y-1">${match}</ol>`;
    }
    return `<ul class="my-4 pl-2 space-y-1">${match}</ul>`;
  });

  // Links [text](url)
  html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener noreferrer" class="text-neutral-900 dark:text-neutral-100 underline decoration-neutral-400 underline-offset-4 hover:decoration-neutral-900 dark:hover:decoration-neutral-100 transition-colors">$1</a>');

  // Paragraphs for remaining text blocks
  const sections = html.split(/\n{2,}/);
  html = sections
    .map((section) => {
      const trimmed = section.trim();
      if (!trimmed) return '';
      // If already wrapped in HTML block tags, don't wrap in <p>
      if (/^<(h[1-6]|ul|ol|li|blockquote|div|pre|hr)/i.test(trimmed)) {
        return trimmed;
      }
      return `<p class="my-4 leading-relaxed">${trimmed.replace(/\n/g, '<br />')}</p>`;
    })
    .filter(Boolean)
    .join('\n');

  return html;
}

/**
 * Generate a complete standalone HTML document for export
 */
export function generateStandaloneHtml(title: string, markdownContent: string, fontFamily: string): string {
  const bodyHtml = renderMarkdown(markdownContent);
  const fontImport = fontFamily === 'editorial'
    ? `<link href="https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,500;0,600;1,400&display=swap" rel="stylesheet">`
    : `<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">`;
  const fontClass = fontFamily === 'editorial' ? `'Lora', Georgia, serif` : `'Plus Jakarta Sans', system-ui, sans-serif`;

  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${escapeHtml(title)}</title>
  ${fontImport}
  <style>
    body {
      font-family: ${fontClass};
      max-width: 760px;
      margin: 48px auto;
      padding: 0 24px;
      line-height: 1.7;
      color: #1a1a1a;
      background: #fafafa;
    }
    h1 { font-size: 2.25rem; font-weight: 700; margin-top: 2rem; margin-bottom: 1rem; }
    h2 { font-size: 1.5rem; font-weight: 600; margin-top: 2rem; margin-bottom: 0.75rem; border-bottom: 1px solid #e5e5e5; padding-bottom: 0.25rem; }
    h3 { font-size: 1.25rem; font-weight: 600; margin-top: 1.5rem; margin-bottom: 0.5rem; }
    p { margin: 1.25rem 0; }
    blockquote { border-left: 2px solid #ccc; padding-left: 1rem; margin: 1.5rem 0; font-style: italic; color: #555; }
    code { background: #f0f0f0; padding: 2px 5px; border-radius: 3px; font-family: monospace; font-size: 0.9em; }
    pre { background: #1e1e1e; color: #f0f0f0; padding: 1rem; border-radius: 6px; overflow-x: auto; font-family: monospace; }
    ul, ol { padding-left: 1.5rem; margin: 1rem 0; }
    li { margin: 0.35rem 0; }
    hr { border: 0; border-top: 1px solid #e0e0e0; margin: 2rem 0; }
    a { color: #000; text-decoration: underline; }
    @media print {
      body { max-width: 100%; margin: 0; padding: 1cm; background: white; }
    }
  </style>
</head>
<body>
  ${bodyHtml}
</body>
</html>`;
}
