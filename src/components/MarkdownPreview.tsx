import React, { useMemo } from 'react';
import { renderMarkdown } from '../utils/markdown';
import { EditorSettings } from '../types';

interface MarkdownPreviewProps {
  content: string;
  settings: EditorSettings;
}

export const MarkdownPreview: React.FC<MarkdownPreviewProps> = ({
  content,
  settings,
}) => {
  const renderedHtml = useMemo(() => {
    return renderMarkdown(content);
  }, [content]);

  // Width container style matching user preference
  const maxWidthClass =
    settings.measure === 'narrow' ? 'max-w-[640px]' :
    settings.measure === 'wide' ? 'max-w-[940px]' :
    'max-w-[780px]';

  // Font family class
  const fontClass =
    settings.fontFamily === 'editorial' ? 'font-editorial' :
    settings.fontFamily === 'code' ? 'font-code' :
    'font-modern';

  return (
    <div className="h-full overflow-y-auto px-6 py-10 md:px-12 selection:bg-neutral-200 dark:selection:bg-neutral-800">
      <div
        className={`mx-auto ${maxWidthClass} ${fontClass} text-neutral-800 dark:text-neutral-200`}
        style={{
          fontSize: `${settings.fontSize}px`,
          lineHeight: settings.lineHeight,
        }}
        dangerouslySetInnerHTML={{ __html: renderedHtml }}
      />
    </div>
  );
};
