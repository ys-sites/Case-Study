import React from 'react';
import { X, Type, Sliders, Volume2 } from 'lucide-react';
import { EditorSettings, EditorFontFamily, EditorMeasure, AmbientSoundType } from '../types';

interface SettingsModalProps {
  isOpen: boolean;
  onClose: () => void;
  settings: EditorSettings;
  onUpdateSettings: (settings: Partial<EditorSettings>) => void;
}

export const SettingsModal: React.FC<SettingsModalProps> = ({
  isOpen,
  onClose,
  settings,
  onUpdateSettings,
}) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-neutral-900/40 backdrop-blur-xs p-4">
      <div className="w-full max-w-md bg-white dark:bg-neutral-900 border border-neutral-200 dark:border-neutral-800 rounded-xl p-6 shadow-xl relative animate-in fade-in zoom-in-95 duration-150">
        <div className="flex items-center justify-between pb-4 border-b border-neutral-200 dark:border-neutral-800">
          <div className="flex items-center gap-2">
            <Sliders className="w-4 h-4 text-neutral-600 dark:text-neutral-400" />
            <h3 className="text-sm font-bold text-neutral-900 dark:text-neutral-100">
              Typography & Writing Canvas
            </h3>
          </div>
          <button
            onClick={onClose}
            className="p-1 text-neutral-400 hover:text-neutral-700 dark:hover:text-neutral-200 rounded"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        <div className="py-4 space-y-5 text-xs">
          {/* Font Family Selection */}
          <div>
            <label className="block text-neutral-500 mb-2 font-medium">Font Family</label>
            <div className="grid grid-cols-3 gap-2">
              <button
                onClick={() => onUpdateSettings({ fontFamily: 'editorial' as EditorFontFamily })}
                className={`p-2.5 rounded-lg border text-left transition-colors ${
                  settings.fontFamily === 'editorial'
                    ? 'border-neutral-900 dark:border-neutral-100 bg-neutral-100/60 dark:bg-neutral-800 text-neutral-900 dark:text-neutral-100 font-semibold'
                    : 'border-neutral-200 dark:border-neutral-700 text-neutral-600 dark:text-neutral-400 hover:border-neutral-400'
                }`}
              >
                <div className="font-editorial text-sm">Lora Serif</div>
                <div className="text-[10px] text-neutral-400 font-normal">Literary & Books</div>
              </button>

              <button
                onClick={() => onUpdateSettings({ fontFamily: 'modern' as EditorFontFamily })}
                className={`p-2.5 rounded-lg border text-left transition-colors ${
                  settings.fontFamily === 'modern'
                    ? 'border-neutral-900 dark:border-neutral-100 bg-neutral-100/60 dark:bg-neutral-800 text-neutral-900 dark:text-neutral-100 font-semibold'
                    : 'border-neutral-200 dark:border-neutral-700 text-neutral-600 dark:text-neutral-400 hover:border-neutral-400'
                }`}
              >
                <div className="font-modern text-sm">Jakarta Sans</div>
                <div className="text-[10px] text-neutral-400 font-normal">Clean & Modern</div>
              </button>

              <button
                onClick={() => onUpdateSettings({ fontFamily: 'code' as EditorFontFamily })}
                className={`p-2.5 rounded-lg border text-left transition-colors ${
                  settings.fontFamily === 'code'
                    ? 'border-neutral-900 dark:border-neutral-100 bg-neutral-100/60 dark:bg-neutral-800 text-neutral-900 dark:text-neutral-100 font-semibold'
                    : 'border-neutral-200 dark:border-neutral-700 text-neutral-600 dark:text-neutral-400 hover:border-neutral-400'
                }`}
              >
                <div className="font-code text-sm">JetBrains</div>
                <div className="text-[10px] text-neutral-400 font-normal">Technical & Code</div>
              </button>
            </div>
          </div>

          {/* Font Size & Line Height */}
          <div className="grid grid-cols-2 gap-4">
            <div>
              <div className="flex justify-between text-neutral-500 mb-1.5">
                <span className="font-medium">Font Size</span>
                <span className="font-mono">{settings.fontSize}px</span>
              </div>
              <input
                type="range"
                min="15"
                max="22"
                step="1"
                value={settings.fontSize}
                onChange={(e) => onUpdateSettings({ fontSize: Number(e.target.value) })}
                className="w-full accent-neutral-800 dark:accent-neutral-200"
              />
            </div>

            <div>
              <div className="flex justify-between text-neutral-500 mb-1.5">
                <span className="font-medium">Line Height</span>
                <span className="font-mono">{settings.lineHeight}x</span>
              </div>
              <div className="flex gap-1.5">
                {[1.5, 1.75, 2.0].map((lh) => (
                  <button
                    key={lh}
                    onClick={() => onUpdateSettings({ lineHeight: lh })}
                    className={`flex-1 py-1 rounded border text-xs font-mono transition-colors ${
                      settings.lineHeight === lh
                        ? 'bg-neutral-900 text-white dark:bg-neutral-100 dark:text-neutral-900 border-transparent font-medium'
                        : 'border-neutral-200 dark:border-neutral-700 text-neutral-600 dark:text-neutral-400'
                    }`}
                  >
                    {lh}x
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Measure Width */}
          <div>
            <label className="block text-neutral-500 mb-2 font-medium">Reading Column Width</label>
            <div className="grid grid-cols-3 gap-2">
              {[
                { id: 'narrow', label: 'Narrow', width: '640px' },
                { id: 'standard', label: 'Standard', width: '780px' },
                { id: 'wide', label: 'Wide', width: '940px' },
              ].map((m) => (
                <button
                  key={m.id}
                  onClick={() => onUpdateSettings({ measure: m.id as EditorMeasure })}
                  className={`py-1.5 px-2 rounded-lg border text-center transition-colors ${
                    settings.measure === m.id
                      ? 'border-neutral-900 dark:border-neutral-100 bg-neutral-100 dark:bg-neutral-800 text-neutral-900 dark:text-neutral-100 font-semibold'
                      : 'border-neutral-200 dark:border-neutral-700 text-neutral-600 dark:text-neutral-400 hover:border-neutral-400'
                  }`}
                >
                  <div>{m.label}</div>
                  <div className="text-[10px] text-neutral-400 font-mono">{m.width}</div>
                </button>
              ))}
            </div>
          </div>

          {/* Typewriter Scroll Toggle */}
          <div className="flex items-center justify-between py-2 border-t border-neutral-100 dark:border-neutral-800">
            <div>
              <div className="font-medium text-neutral-900 dark:text-neutral-100">
                Typewriter Mode
              </div>
              <div className="text-[11px] text-neutral-500">
                Auto-scrolls the canvas to keep current cursor centered
              </div>
            </div>
            <button
              onClick={() => onUpdateSettings({ typewriterMode: !settings.typewriterMode })}
              className={`w-10 h-5 rounded-full p-0.5 transition-colors ${
                settings.typewriterMode ? 'bg-neutral-900 dark:bg-neutral-100' : 'bg-neutral-300 dark:bg-neutral-700'
              }`}
            >
              <div
                className={`w-4 h-4 rounded-full bg-white dark:bg-neutral-900 transition-transform ${
                  settings.typewriterMode ? 'translate-x-5' : 'translate-x-0'
                }`}
              />
            </button>
          </div>

          {/* Soundscapes */}
          <div className="pt-2 border-t border-neutral-100 dark:border-neutral-800 space-y-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-1.5">
                <Volume2 className="w-3.5 h-3.5 text-neutral-500" />
                <span className="font-medium text-neutral-900 dark:text-neutral-100">
                  Tactile Audio Feedback
                </span>
              </div>
              <button
                onClick={() => onUpdateSettings({ soundEnabled: !settings.soundEnabled })}
                className={`w-10 h-5 rounded-full p-0.5 transition-colors ${
                  settings.soundEnabled ? 'bg-neutral-900 dark:bg-neutral-100' : 'bg-neutral-300 dark:bg-neutral-700'
                }`}
              >
                <div
                  className={`w-4 h-4 rounded-full bg-white dark:bg-neutral-900 transition-transform ${
                    settings.soundEnabled ? 'translate-x-5' : 'translate-x-0'
                  }`}
                />
              </button>
            </div>

            {/* Ambient Ambiance Selection */}
            <div>
              <label className="block text-neutral-500 mb-1.5">Focus Soundscape</label>
              <div className="grid grid-cols-2 gap-2">
                {[
                  { id: 'none', label: 'Silence' },
                  { id: 'rain', label: 'Gentle Rain' },
                ].map((s) => (
                  <button
                    key={s.id}
                    onClick={() => onUpdateSettings({ ambientSound: s.id as AmbientSoundType })}
                    className={`py-1.5 px-2 rounded-lg border text-center transition-colors ${
                      settings.ambientSound === s.id
                        ? 'border-neutral-900 dark:border-neutral-100 bg-neutral-100 dark:bg-neutral-800 text-neutral-900 dark:text-neutral-100 font-semibold'
                        : 'border-neutral-200 dark:border-neutral-700 text-neutral-600 dark:text-neutral-400'
                    }`}
                  >
                    {s.label}
                  </button>
                ))}
              </div>
            </div>

            {/* Volume */}
            <div>
              <div className="flex justify-between text-neutral-500 mb-1">
                <span>Soundscape Volume</span>
                <span className="font-mono">{Math.round(settings.soundVolume * 100)}%</span>
              </div>
              <input
                type="range"
                min="0"
                max="1"
                step="0.05"
                value={settings.soundVolume}
                onChange={(e) => onUpdateSettings({ soundVolume: Number(e.target.value) })}
                className="w-full accent-neutral-800 dark:accent-neutral-200"
              />
            </div>
          </div>
        </div>

        <div className="pt-3 border-t border-neutral-200 dark:border-neutral-800 flex justify-end">
          <button
            onClick={onClose}
            className="px-4 py-1.5 text-xs font-semibold text-white bg-neutral-900 hover:bg-neutral-800 dark:bg-neutral-100 dark:text-neutral-900 dark:hover:bg-white rounded-md transition-colors"
          >
            Done
          </button>
        </div>
      </div>
    </div>
  );
};
