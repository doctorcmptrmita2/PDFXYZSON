import { useState, useRef, useEffect } from 'react';
import type { Word } from '../../types/textMap';

interface InlineWordEditorProps {
  word: Word;
  pageWidth: number;
  pageHeight: number;
  imageWidth: number;
  imageHeight: number;
  onSave: (wordId: string, newText: string) => void;
  onCancel: () => void;
  isSaving?: boolean;
}

export function InlineWordEditor({
  word,
  pageWidth,
  pageHeight,
  imageWidth,
  imageHeight,
  onSave,
  onCancel,
  isSaving = false,
}: InlineWordEditorProps) {
  const [text, setText] = useState(word.text);
  const inputRef = useRef<HTMLInputElement>(null);

  // Calculate position - same coordinate transformation as WordOverlay
  const scaleX = imageWidth / pageWidth;
  const scaleY = imageHeight / pageHeight;
  const x0 = word.bbox.x0 * scaleX;
  const y0 = (pageHeight - word.bbox.y1) * scaleY;  // Top of word in HTML coordinates
  const width = Math.max((word.bbox.x1 - word.bbox.x0) * scaleX, 100); // Min 100px width
  const height = (word.bbox.y1 - word.bbox.y0) * scaleY;

  useEffect(() => {
    // Focus input when component mounts
    inputRef.current?.focus();
    inputRef.current?.select();
  }, []);

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      handleSave();
    } else if (e.key === 'Escape') {
      e.preventDefault();
      onCancel();
    }
  };

  const handleSave = () => {
    if (text.trim() !== word.text.trim()) {
      onSave(word.id, text.trim());
    } else {
      onCancel();
    }
  };

  const handleBlur = () => {
    // Small delay to allow save button click
    setTimeout(() => {
      handleSave();
    }, 200);
  };

  return (
    <div
      className="absolute z-50"
      style={{
        left: `${x0}px`,
        top: `${y0}px`,
        width: `${width}px`,
        minWidth: '100px',
      }}
      onClick={(e) => e.stopPropagation()}
    >
      <div className="relative bg-white border-2 border-blue-500 rounded shadow-lg p-1">
        <input
          ref={inputRef}
          type="text"
          value={text}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={handleKeyDown}
          onBlur={handleBlur}
          disabled={isSaving}
          className="w-full px-2 py-1 text-sm border-0 outline-none focus:ring-0 bg-transparent"
          style={{ minHeight: `${height}px` }}
        />
        {isSaving && (
          <div className="absolute top-full left-0 right-0 bg-blue-500 text-white text-xs px-2 py-1 rounded-b">
            Saving...
          </div>
        )}
      </div>
    </div>
  );
}

