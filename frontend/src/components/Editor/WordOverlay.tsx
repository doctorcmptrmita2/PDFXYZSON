import type { Word } from '../../types/textMap';

interface WordOverlayProps {
  word: Word;
  pageWidth: number;
  pageHeight: number;
  imageWidth: number;
  imageHeight: number;
  isSelected: boolean;
  isEditing?: boolean;
  onClick: () => void;
  onDoubleClick?: () => void;
}

export function WordOverlay({
  word,
  pageWidth,
  pageHeight,
  imageWidth,
  imageHeight,
  isSelected,
  isEditing = false,
  onClick,
  onDoubleClick,
}: WordOverlayProps) {
  // Calculate scale factors
  const scaleX = imageWidth / pageWidth;
  const scaleY = imageHeight / pageHeight;

  // PyMuPDF uses bottom-left origin (y=0 at bottom), but HTML uses top-left (y=0 at top)
  // Convert coordinates: flip vertically
  // PDF: y0 is bottom, y1 is top (y increases upward)
  // HTML: y0 is top, y1 is bottom (y increases downward)
  const x0 = word.bbox.x0 * scaleX;
  const y0 = (pageHeight - word.bbox.y1) * scaleY;  // Top of word in HTML coordinates
  const width = (word.bbox.x1 - word.bbox.x0) * scaleX;
  const height = (word.bbox.y1 - word.bbox.y0) * scaleY;

  // Don't render overlay if editing (input will be shown instead)
  if (isEditing) {
    return null;
  }

  return (
    <div
      className={`absolute border cursor-pointer transition-all ${
        isSelected
          ? 'border-blue-500 bg-blue-100 bg-opacity-50 shadow-md'
          : 'border-transparent hover:border-blue-400 hover:bg-blue-50 hover:bg-opacity-40'
      }`}
      style={{
        left: `${x0}px`,
        top: `${y0}px`,
        width: `${width}px`,
        height: `${height}px`,
        zIndex: isSelected ? 10 : 1,
      }}
      onClick={(e) => {
        e.stopPropagation(); // Prevent block selection
        onClick();
      }}
      onDoubleClick={(e) => {
        e.stopPropagation();
        if (onDoubleClick) {
          onDoubleClick();
        }
      }}
      title={`${word.text} (Double-click to edit)`}
    />
  );
}

