export interface BBox {
  x0: number;
  y0: number;
  x1: number;
  y1: number;
}

export interface Word {
  id: string;
  text: string;
  bbox: BBox;
  block_id: string;
}

export interface TextBlock {
  id: string;
  page_number: number;
  bbox: BBox;
  text: string;
  words?: Word[];
}

export interface TextMapResponse {
  pdf_uuid: string;
  page_number: number;
  page_width: number;
  page_height: number;
  blocks: TextBlock[];
}

