import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { uploadPdf } from '../api/pdfs';
import { Upload, FileText, Loader2 } from 'lucide-react';

export function HomePage() {
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  const handleFileSelect = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    if (file.type !== 'application/pdf') {
      setError('Please select a PDF file');
      return;
    }

    setUploading(true);
    setError(null);

    try {
      const result = await uploadPdf(file);
      navigate(`/editor/${result.uuid}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to upload PDF');
    } finally {
      setUploading(false);
    }
  };

  const handleDrop = async (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    if (!file || file.type !== 'application/pdf') {
      setError('Please drop a PDF file');
      return;
    }

    setUploading(true);
    setError(null);

    try {
      const result = await uploadPdf(file);
      navigate(`/editor/${result.uuid}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to upload PDF');
    } finally {
      setUploading(false);
    }
  };

  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
  };

  return (
    <div className="container mx-auto px-4 py-16">
      <div className="max-w-2xl mx-auto">
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-br from-blue-500 to-purple-600 rounded-2xl mb-6 shadow-lg transform hover:scale-105 transition-transform">
            <FileText className="w-10 h-10 text-white" />
          </div>
          <h1 className="text-4xl font-extrabold mb-3 bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 bg-clip-text text-transparent">
            Upload PDF to Edit
          </h1>
          <p className="text-gray-600 text-lg">
            Select a PDF file to start editing with <span className="font-semibold text-blue-600">word-level precision</span>
          </p>
        </div>

        <div
          className="border-2 border-dashed border-gray-300 rounded-lg p-12 text-center hover:border-blue-400 transition-colors bg-white"
          onDrop={handleDrop}
          onDragOver={handleDragOver}
        >
          {uploading ? (
            <div className="flex flex-col items-center gap-4">
              <Loader2 className="w-12 h-12 text-blue-600 animate-spin" />
              <p className="text-gray-600">Uploading PDF...</p>
            </div>
          ) : (
            <>
              <Upload className="w-12 h-12 text-gray-400 mx-auto mb-4" />
              <label className="cursor-pointer">
                <input
                  type="file"
                  accept=".pdf"
                  onChange={handleFileSelect}
                  className="hidden"
                  disabled={uploading}
                />
                <div className="space-y-2">
                  <p className="text-lg font-semibold text-gray-700">
                    Click to upload or drag and drop
                  </p>
                  <p className="text-sm text-gray-500">
                    PDF files only
                  </p>
                  <button
                    type="button"
                    className="mt-4 px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                  >
                    Select PDF File
                  </button>
                </div>
              </label>
            </>
          )}
        </div>

        {error && (
          <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700 text-center">
            {error}
          </div>
        )}

        <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-4 text-center">
          <div className="p-4 bg-white rounded-lg shadow-sm">
            <div className="text-2xl font-bold text-blue-600 mb-2">Word-Level</div>
            <div className="text-sm text-gray-600">Edit individual words</div>
          </div>
          <div className="p-4 bg-white rounded-lg shadow-sm">
            <div className="text-2xl font-bold text-blue-600 mb-2">Real-time</div>
            <div className="text-sm text-gray-600">Instant preview</div>
          </div>
          <div className="p-4 bg-white rounded-lg shadow-sm">
            <div className="text-2xl font-bold text-blue-600 mb-2">50+ Tools</div>
            <div className="text-sm text-gray-600">Powerful operations</div>
          </div>
        </div>
      </div>
    </div>
  );
}
