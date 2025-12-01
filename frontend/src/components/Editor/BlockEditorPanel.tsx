import { useState, useEffect } from 'react';
import type { TextBlock, Word } from '../../types/textMap';

interface BlockEditorPanelProps {
  selectedBlock: TextBlock | null;
  selectedWord: Word | null;
  onSave: (newText: string) => void;
  isSaving: boolean;
}

export function BlockEditorPanel({
  selectedBlock,
  selectedWord,
  onSave,
  isSaving,
}: BlockEditorPanelProps) {
  const [text, setText] = useState('');

  useEffect(() => {
    if (selectedWord) {
      setText(selectedWord.text);
    } else if (selectedBlock) {
      setText(selectedBlock.text);
    } else {
      setText('');
    }
  }, [selectedBlock, selectedWord]);

  const handleSave = () => {
    if (selectedBlock) {
      onSave(text);
    }
  };

  if (!selectedBlock && !selectedWord) {
    return (
      <div className="h-full flex items-center justify-center p-6">
        <div className="text-center text-gray-500">
          <p className="text-lg mb-2">No selection</p>
          <p className="text-sm">Click on a text block or word to edit it</p>
        </div>
      </div>
    );
  }

  return (
    <div className="h-full flex flex-col bg-white">
      <div className="p-4 border-b border-gray-200">
        <h2 className="text-lg font-semibold text-gray-900">
          {selectedWord ? 'Edit Word' : 'Edit Text Block'}
        </h2>
        <div className="mt-2 text-sm text-gray-600">
          {selectedWord ? (
            <>
              <p>Word ID: {selectedWord.id}</p>
              <p>Block: {selectedWord.block_id}</p>
              <p>Page: {selectedBlock?.page_number}</p>
            </>
          ) : (
            <>
              <p>Block ID: {selectedBlock.id}</p>
              <p>Page: {selectedBlock.page_number}</p>
            </>
          )}
        </div>
      </div>

      <div className="flex-1 p-4 overflow-hidden flex flex-col">
        <label
          htmlFor="block-text"
          className="block text-sm font-medium text-gray-700 mb-2"
        >
          Text Content
        </label>
        <textarea
          id="block-text"
          value={text}
          onChange={(e) => setText(e.target.value)}
          className="flex-1 w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 resize-none font-mono text-sm"
          placeholder="Enter text..."
        />
      </div>

      <div className="p-4 border-t border-gray-200">
        <button
          onClick={handleSave}
          disabled={
            isSaving ||
            (selectedWord
              ? text === selectedWord.text
              : selectedBlock
              ? text === selectedBlock.text
              : true)
          }
          className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
        >
          {isSaving ? 'Saving...' : 'Save Changes'}
        </button>
      </div>
    </div>
  );
}

