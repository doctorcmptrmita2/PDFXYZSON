import { useState, useEffect } from 'react';
import { getPdfMetadata } from '../api/pdfs';
import type { PdfMetadata } from '../types/pdf';

export function usePdfDocument(pdfUuid: string | null) {
  const [pdf, setPdf] = useState<PdfMetadata | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!pdfUuid) {
      setPdf(null);
      return;
    }

    setLoading(true);
    setError(null);
    getPdfMetadata(pdfUuid)
      .then(setPdf)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [pdfUuid]);

  return { pdf, loading, error };
}

