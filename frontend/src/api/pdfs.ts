import { apiGet, apiPost, apiPut, apiGetBlob } from './client';
import type { UploadedPdf, PdfMetadata } from '../types/pdf';
import type { TextMapResponse } from '../types/textMap';

export async function uploadPdf(file: File): Promise<UploadedPdf> {
  const formData = new FormData();
  formData.append('file', file);
  return apiPost<UploadedPdf>('/pdfs/', formData);
}

export async function getPdfMetadata(pdfUuid: string): Promise<PdfMetadata> {
  return apiGet<PdfMetadata>(`/pdfs/${pdfUuid}`);
}

export function getPageImageUrl(pdfUuid: string, pageNumber: number): string {
  const baseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8001/api';
  return `${baseUrl}/pdfs/${pdfUuid}/pages/${pageNumber}/image`;
}

export async function getTextMap(
  pdfUuid: string,
  pageNumber: number
): Promise<TextMapResponse> {
  return apiGet<TextMapResponse>(
    `/pdfs/${pdfUuid}/pages/${pageNumber}/text-map`
  );
}

export async function updateBlock(
  pdfUuid: string,
  pageNumber: number,
  blockId: string,
  newText: string
): Promise<TextMapResponse> {
  return apiPut<TextMapResponse>(
    `/pdfs/${pdfUuid}/pages/${pageNumber}/blocks/${blockId}`,
    { new_text: newText }
  );
}

export async function updateWord(
  pdfUuid: string,
  pageNumber: number,
  wordId: string,
  newText: string
): Promise<TextMapResponse> {
  return apiPut<TextMapResponse>(
    `/pdfs/${pdfUuid}/pages/${pageNumber}/words/${wordId}`,
    { new_text: newText }
  );
}

export async function downloadPdf(pdfUuid: string, filename: string): Promise<void> {
  const blob = await apiGetBlob(`/pdfs/${pdfUuid}/download`);
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  window.URL.revokeObjectURL(url);
  document.body.removeChild(a);
}

