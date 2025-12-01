import { FileText } from 'lucide-react';

export function Header() {
  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="px-6 py-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-gradient-to-br from-blue-600 to-purple-600 rounded-lg flex items-center justify-center shadow-md">
            <FileText className="w-6 h-6 text-white" />
          </div>
          <h1 className="text-2xl font-extrabold">
            <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              AeroPdf
            </span>
            <span className="text-gray-700 ml-1">Editör</span>
          </h1>
        </div>
      </div>
    </header>
  );
}

