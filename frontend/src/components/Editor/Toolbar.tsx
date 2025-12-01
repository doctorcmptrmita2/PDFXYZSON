interface ToolbarProps {
  currentPage: number;
  pageCount: number;
  onPageChange: (newPage: number) => void;
  onDownload: () => void;
  isDownloading?: boolean;
  showWords?: boolean;
  onToggleWords?: () => void;
}

export function Toolbar({
  currentPage,
  pageCount,
  onPageChange,
  onDownload,
  isDownloading = false,
  showWords = false,
  onToggleWords,
}: ToolbarProps) {
  const handlePrevious = () => {
    if (currentPage > 1) {
      onPageChange(currentPage - 1);
    }
  };

  const handleNext = () => {
    if (currentPage < pageCount) {
      onPageChange(currentPage + 1);
    }
  };

  return (
    <div className="bg-white border-b border-gray-200 px-6 py-3 flex items-center justify-between">
      <div className="flex items-center gap-4">
        <button
          onClick={handlePrevious}
          disabled={currentPage <= 1}
          className="px-4 py-2 bg-gray-100 text-gray-700 rounded-md hover:bg-gray-200 disabled:bg-gray-50 disabled:text-gray-400 disabled:cursor-not-allowed transition-colors"
        >
          Previous
        </button>
        <span className="text-sm text-gray-600">
          Page {currentPage} of {pageCount}
        </span>
        <button
          onClick={handleNext}
          disabled={currentPage >= pageCount}
          className="px-4 py-2 bg-gray-100 text-gray-700 rounded-md hover:bg-gray-200 disabled:bg-gray-50 disabled:text-gray-400 disabled:cursor-not-allowed transition-colors"
        >
          Next
        </button>
      </div>

      <div className="flex items-center gap-4">
        {onToggleWords && (
          <button
            onClick={onToggleWords}
            className={`px-4 py-2 rounded-md transition-colors ${
              showWords
                ? 'bg-green-600 text-white hover:bg-green-700'
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
            title="Toggle word-level selection"
          >
            {showWords ? 'Hide Words' : 'Show Words'}
          </button>
        )}
        <button
          onClick={onDownload}
          disabled={isDownloading}
          className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
        >
          {isDownloading ? 'Downloading...' : 'Download PDF'}
        </button>
      </div>
    </div>
  );
}

