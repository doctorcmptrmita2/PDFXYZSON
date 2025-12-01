import { useState, useEffect } from 'react';
import { getPageImageUrl } from '../../api/pdfs';
import { TextBlockOverlay } from './TextBlockOverlay';
import { WordOverlay } from './WordOverlay';
import { InlineWordEditor } from './InlineWordEditor';
import type { TextBlock, TextMapResponse, Word } from '../../types/textMap';

interface PageViewerProps {
  pdfUuid: string;
  pageNumber: number;
  textMap: TextMapResponse | null;
  selectedBlockId?: string;
  selectedWordId?: string;
  editingWordId?: string;
  onBlockSelect: (block: TextBlock) => void;
  onWordSelect: (word: Word, block: TextBlock) => void;
  onWordEdit: (word: Word, block: TextBlock) => void;
  onWordSave: (wordId: string, newText: string) => void;
  onWordEditCancel: () => void;
  showWords?: boolean; // Toggle word-level overlays
  isSaving?: boolean;
}

export function PageViewer({
  pdfUuid,
  pageNumber,
  textMap,
  selectedBlockId,
  selectedWordId,
  editingWordId,
  onBlockSelect,
  onWordSelect,
  onWordEdit,
  onWordSave,
  onWordEditCancel,
  showWords = false,
  isSaving = false,
}: PageViewerProps) {
  const [imageUrl, setImageUrl] = useState<string | null>(null);
  const [imageSize, setImageSize] = useState<{ width: number; height: number } | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    setError(null);
    const url = getPageImageUrl(pdfUuid, pageNumber);
    
    // Add timestamp to force refresh after edits
    const imageUrlWithCache = `${url}?t=${Date.now()}`;
    
    const img = new Image();
    img.onload = () => {
      setImageSize({ width: img.naturalWidth, height: img.naturalHeight });
      setImageUrl(imageUrlWithCache);
      setLoading(false);
    };
    img.onerror = () => {
      setError('Failed to load page image');
      setLoading(false);
    };
    img.src = imageUrlWithCache;

    return () => {
      // Cleanup: revoke object URL if we create one
      if (imageUrlWithCache.startsWith('blob:')) {
        URL.revokeObjectURL(imageUrlWithCache);
      }
    };
  }, [pdfUuid, pageNumber]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-gray-500">Loading page...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-red-500">{error}</div>
      </div>
    );
  }

  if (!imageUrl || !imageSize || !textMap) {
    return null;
  }

  return (
    <div className="h-full overflow-auto bg-gray-100 flex items-center justify-center p-4">
      <div className="relative bg-white shadow-lg" style={{ maxWidth: '100%' }}>
        <img
          src={imageUrl}
          alt={`Page ${pageNumber}`}
          className="max-w-full h-auto"
          onLoad={(e) => {
            const img = e.currentTarget;
            setImageSize({ width: img.naturalWidth, height: img.naturalHeight });
          }}
        />
        {textMap.blocks.map((block) => (
          <div key={block.id}>
            <TextBlockOverlay
              block={block}
              pageWidth={textMap.page_width}
              pageHeight={textMap.page_height}
              imageWidth={imageSize.width}
              imageHeight={imageSize.height}
              isSelected={block.id === selectedBlockId}
              onClick={() => onBlockSelect(block)}
            />
            {showWords && block.words && block.words.map((word) => {
              const isEditing = word.id === editingWordId;
              return (
                <div key={word.id}>
                  <WordOverlay
                    word={word}
                    pageWidth={textMap.page_width}
                    pageHeight={textMap.page_height}
                    imageWidth={imageSize.width}
                    imageHeight={imageSize.height}
                    isSelected={word.id === selectedWordId}
                    isEditing={isEditing}
                    onClick={() => onWordSelect(word, block)}
                    onDoubleClick={() => onWordEdit(word, block)}
                  />
                  {isEditing && (
                    <InlineWordEditor
                      word={word}
                      pageWidth={textMap.page_width}
                      pageHeight={textMap.page_height}
                      imageWidth={imageSize.width}
                      imageHeight={imageSize.height}
                      onSave={onWordSave}
                      onCancel={onWordEditCancel}
                      isSaving={isSaving}
                    />
                  )}
                </div>
              );
            })}
          </div>
        ))}
      </div>
    </div>
  );
}

