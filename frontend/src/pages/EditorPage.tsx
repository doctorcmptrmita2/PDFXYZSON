import { useState, useRef, useCallback } from 'react';
import { useParams } from 'react-router-dom';
import { usePdfDocument } from '../hooks/usePdfDocument';
import { useTextMap } from '../hooks/useTextMap';
import { updateBlock, updateWord, downloadPdf } from '../api/pdfs';
import { Toolbar } from '../components/Editor/Toolbar';
import { PageViewer } from '../components/Editor/PageViewer';
import { BlockEditorPanel } from '../components/Editor/BlockEditorPanel';
import type { TextBlock, Word, TextMapResponse } from '../types/textMap';

export function EditorPage() {
  const { pdfUuid } = useParams<{ pdfUuid: string }>();
  const [currentPage, setCurrentPage] = useState(1);
  const [selectedBlock, setSelectedBlock] = useState<TextBlock | null>(null);
  const [selectedWord, setSelectedWord] = useState<Word | null>(null);
  const [editingWordId, setEditingWordId] = useState<string | null>(null);
  const [showWords, setShowWords] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [isDownloading, setIsDownloading] = useState(false);
  const saveTimeoutRef = useRef<NodeJS.Timeout | null>(null);

  const { pdf, loading: pdfLoading, error: pdfError } = usePdfDocument(pdfUuid || null);
  const { textMap, loading: textMapLoading, error: textMapError, setTextMap } = useTextMap(
    pdfUuid || null,
    currentPage
  );

  const handleBlockSelect = (block: TextBlock) => {
    setSelectedBlock(block);
    setSelectedWord(null); // Clear word selection when block is selected
  };

  const handleWordSelect = (word: Word, block: TextBlock) => {
    setSelectedWord(word);
    setSelectedBlock(block); // Also select the parent block
    setEditingWordId(null); // Clear editing state
  };

  const handleWordEdit = (word: Word, block: TextBlock) => {
    setSelectedWord(word);
    setSelectedBlock(block);
    setEditingWordId(word.id); // Start inline editing
  };

  const handleWordEditCancel = () => {
    setEditingWordId(null);
  };

  const handleSave = async (newText: string) => {
    if (!pdfUuid) return;

    setIsSaving(true);
    try {
      let updatedTextMap: TextMapResponse;
      
      // If word is selected, edit word; otherwise edit block
      if (selectedWord) {
        updatedTextMap = await updateWord(
          pdfUuid,
          currentPage,
          selectedWord.id,
          newText
        );
        // Update selected word text
        setSelectedWord({
          ...selectedWord,
          text: newText,
        });
        setEditingWordId(null); // Exit editing mode
      } else if (selectedBlock) {
        updatedTextMap = await updateBlock(
          pdfUuid,
          currentPage,
          selectedBlock.id,
          newText
        );
        // Update selected block text
        setSelectedBlock({
          ...selectedBlock,
          text: newText,
        });
      } else {
        return;
      }
      
      // Update text map
      setTextMap(updatedTextMap);
    } catch (error) {
      alert(error instanceof Error ? error.message : 'Failed to save changes');
    } finally {
      setIsSaving(false);
    }
  };

  // Debounced auto-save for word editing
  const handleWordSave = useCallback(async (wordId: string, newText: string) => {
    if (!pdfUuid) return;

    // Clear existing timeout
    if (saveTimeoutRef.current) {
      clearTimeout(saveTimeoutRef.current);
    }

    // Optimistic update: update UI immediately
    if (selectedWord && selectedWord.id === wordId) {
      setSelectedWord({
        ...selectedWord,
        text: newText,
      });
    }

    // Update text map optimistically
    if (textMap) {
      const updatedBlocks = textMap.blocks.map((block) => {
        if (block.words) {
          const updatedWords = block.words.map((word) =>
            word.id === wordId ? { ...word, text: newText } : word
          );
          return { ...block, words: updatedWords };
        }
        return block;
      });
      setTextMap({ ...textMap, blocks: updatedBlocks });
    }

    // Debounced save (500ms delay)
    setIsSaving(true);
    saveTimeoutRef.current = setTimeout(async () => {
      try {
        const updatedTextMap = await updateWord(
          pdfUuid,
          currentPage,
          wordId,
          newText
        );
        setTextMap(updatedTextMap);
        setEditingWordId(null); // Exit editing mode after save
      } catch (error) {
        // Revert on error - reload text map
        alert(error instanceof Error ? error.message : 'Failed to save changes');
        // Trigger text map reload by changing page temporarily (hacky but works)
        const { getTextMap } = await import('../api/pdfs');
        try {
          const reloadedTextMap = await getTextMap(pdfUuid, currentPage);
          setTextMap(reloadedTextMap);
        } catch (reloadError) {
          console.error('Failed to reload text map:', reloadError);
        }
      } finally {
        setIsSaving(false);
      }
    }, 500);
  }, [pdfUuid, currentPage, selectedWord, textMap, setTextMap]);

  const handleDownload = async () => {
    if (!pdfUuid || !pdf) return;

    setIsDownloading(true);
    try {
      await downloadPdf(pdfUuid, pdf.original_filename);
    } catch (error) {
      alert(error instanceof Error ? error.message : 'Failed to download PDF');
    } finally {
      setIsDownloading(false);
    }
  };

  const handlePageChange = (newPage: number) => {
    setCurrentPage(newPage);
    setSelectedBlock(null); // Clear selection when changing pages
    setSelectedWord(null);
  };

  if (pdfLoading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-gray-500">Loading PDF...</div>
      </div>
    );
  }

  if (pdfError || !pdf) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-red-500">
          {pdfError || 'PDF not found'}
        </div>
      </div>
    );
  }

  return (
    <div className="h-screen flex flex-col">
      <Toolbar
        currentPage={currentPage}
        pageCount={pdf.page_count}
        onPageChange={handlePageChange}
        onDownload={handleDownload}
        isDownloading={isDownloading}
        showWords={showWords}
        onToggleWords={() => setShowWords(!showWords)}
      />

      <div className="flex-1 flex overflow-hidden">
        <div className="flex-1 overflow-hidden">
          {textMapLoading ? (
            <div className="flex items-center justify-center h-full">
              <div className="text-gray-500">Loading page...</div>
            </div>
          ) : textMapError ? (
            <div className="flex items-center justify-center h-full">
              <div className="text-red-500">{textMapError}</div>
            </div>
          ) : (
            <PageViewer
              pdfUuid={pdfUuid!}
              pageNumber={currentPage}
              textMap={textMap}
              selectedBlockId={selectedBlock?.id}
              selectedWordId={selectedWord?.id}
              editingWordId={editingWordId || undefined}
              onBlockSelect={handleBlockSelect}
              onWordSelect={handleWordSelect}
              onWordEdit={handleWordEdit}
              onWordSave={handleWordSave}
              onWordEditCancel={handleWordEditCancel}
              showWords={showWords}
              isSaving={isSaving}
            />
          )}
        </div>

        <div className="w-96 border-l border-gray-200 overflow-hidden">
          <BlockEditorPanel
            selectedBlock={selectedBlock}
            selectedWord={selectedWord}
            onSave={handleSave}
            isSaving={isSaving}
          />
        </div>
      </div>
    </div>
  );
}

