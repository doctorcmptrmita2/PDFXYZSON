import type { TextBlock } from '../../types/textMap';

interface TextBlockOverlayProps {
  block: TextBlock;
  pageWidth: number;
  pageHeight: number;
  imageWidth: number;
  imageHeight: number;
  isSelected: boolean;
  onClick: () => void;
}

export function TextBlockOverlay({
  block,
  pageWidth,
  pageHeight,
  imageWidth,
  imageHeight,
  isSelected,
  onClick,
}: TextBlockOverlayProps) {
  // Calculate scale factors
  const scaleX = imageWidth / pageWidth;
  const scaleY = imageHeight / pageHeight;

  // PyMuPDF uses bottom-left origin, but HTML uses top-left
  // Convert coordinates: y = pageHeight - y (flip vertically)
  const x0 = block.bbox.x0 * scaleX;
  const y0 = (pageHeight - block.bbox.y1) * scaleY;
  const width = (block.bbox.x1 - block.bbox.x0) * scaleX;
  const height = (block.bbox.y1 - block.bbox.y0) * scaleY;

  return (
    <div
      className={`absolute border-2 cursor-pointer transition-all ${
        isSelected
          ? 'border-blue-500 bg-blue-100 bg-opacity-30'
          : 'border-transparent hover:border-blue-300 hover:bg-blue-50 hover:bg-opacity-20'
      }`}
      style={{
        left: `${x0}px`,
        top: `${y0}px`,
        width: `${width}px`,
        height: `${height}px`,
      }}
      onClick={onClick}
      title={block.text.substring(0, 50)}
    />
  );
}

