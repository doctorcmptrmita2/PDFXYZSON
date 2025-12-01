import { useState, useEffect } from 'react';
import { getTextMap } from '../api/pdfs';
import type { TextMapResponse } from '../types/textMap';

export function useTextMap(pdfUuid: string | null, pageNumber: number) {
  const [textMap, setTextMap] = useState<TextMapResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!pdfUuid || pageNumber < 1) {
      setTextMap(null);
      return;
    }

    setLoading(true);
    setError(null);
    getTextMap(pdfUuid, pageNumber)
      .then(setTextMap)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [pdfUuid, pageNumber]);

  return { textMap, loading, error, setTextMap };
}

