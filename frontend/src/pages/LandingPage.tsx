import { Link } from 'react-router-dom';
import { 
  FileText, 
  Merge, 
  Scissors, 
  RotateCw, 
  Image as ImageIcon,
  Lock,
  Download,
  Upload,
  Zap,
  Shield,
  Edit3,
  FileCheck
} from 'lucide-react';

export function LandingPage() {
  const features = [
    {
      category: 'Organize',
      icon: <Merge className="w-8 h-8" />,
      items: [
        'Merge multiple PDFs',
        'Split PDFs into multiple files',
        'Extract specific pages',
        'Remove pages',
        'Rotate pages',
        'Rearrange pages',
        'Crop PDF pages',
        'Adjust page size/scale'
      ]
    },
    {
      category: 'Convert to PDF',
      icon: <FileText className="w-8 h-8" />,
      items: [
        'Image to PDF',
        'Word/Excel/PowerPoint to PDF',
        'HTML to PDF',
        'Markdown to PDF',
        'Email to PDF',
        'eBook to PDF (EPUB, MOBI)'
      ]
    },
    {
      category: 'Convert from PDF',
      icon: <Download className="w-8 h-8" />,
      items: [
        'PDF to Word',
        'PDF to Image',
        'PDF to HTML',
        'PDF to Markdown',
        'PDF to CSV',
        'PDF to XML'
      ]
    },
    {
      category: 'Sign & Security',
      icon: <Shield className="w-8 h-8" />,
      items: [
        'Add digital signatures',
        'Add/Remove password',
        'Add watermarks',
        'Redact content',
        'Change permissions',
        'Sanitize PDF'
      ]
    },
    {
      category: 'View & Edit',
      icon: <Edit3 className="w-8 h-8" />,
      items: [
        'OCR / Cleanup scans',
        'Add/Extract images',
        'Edit text blocks',
        'Edit individual words',
        'Change metadata',
        'Add page numbers',
        'Remove blank pages'
      ]
    },
    {
      category: 'Advanced',
      icon: <Zap className="w-8 h-8" />,
      items: [
        'Compress PDF',
        'Repair corrupted PDFs',
        'Compare PDFs',
        'Overlay PDFs',
        'Auto-split by size/count',
        'Pipeline processing'
      ]
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 relative overflow-hidden">
      {/* Animated background elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-blue-400 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob"></div>
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-purple-400 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob animation-delay-2000"></div>
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-80 h-80 bg-pink-400 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob animation-delay-4000"></div>
      </div>
      {/* Hero Section */}
      <div className="container mx-auto px-4 py-16 relative z-10">
        <div className="text-center mb-16">
          <div className="inline-flex items-center justify-center w-24 h-24 bg-gradient-to-br from-blue-600 via-purple-600 to-pink-600 rounded-2xl mb-8 shadow-2xl transform hover:scale-110 transition-transform duration-300">
            <FileText className="w-12 h-12 text-white" />
          </div>
          <h1 className="text-7xl font-extrabold mb-2 bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 bg-clip-text text-transparent animate-pulse hover:animate-none transition-all duration-300">
            AeroPdf
          </h1>
          <h2 className="text-5xl font-bold mb-6 bg-gradient-to-r from-gray-700 to-gray-900 bg-clip-text text-transparent">
            Editör
          </h2>
          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto leading-relaxed">
            Professional PDF editing with <span className="font-semibold text-blue-600">50+ powerful operations</span>. 
            Edit, convert, organize, and secure your PDFs with ease.
          </p>
          <div className="flex gap-4 justify-center">
            <Link
              to="/app"
              className="px-8 py-3 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition-colors shadow-lg hover:shadow-xl flex items-center gap-2"
            >
              <Upload className="w-5 h-5" />
              Get Started
            </Link>
            <a
              href="#features"
              className="px-8 py-3 bg-white text-blue-600 rounded-lg font-semibold hover:bg-gray-50 transition-colors shadow-lg hover:shadow-xl border-2 border-blue-600"
            >
              Explore Features
            </a>
          </div>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-16">
          <div className="bg-white rounded-lg p-6 shadow-md text-center">
            <div className="text-3xl font-bold text-blue-600 mb-2">50+</div>
            <div className="text-gray-600">PDF Operations</div>
          </div>
          <div className="bg-white rounded-lg p-6 shadow-md text-center">
            <div className="text-3xl font-bold text-blue-600 mb-2">100%</div>
            <div className="text-gray-600">Free & Open Source</div>
          </div>
          <div className="bg-white rounded-lg p-6 shadow-md text-center">
            <div className="text-3xl font-bold text-blue-600 mb-2">Fast</div>
            <div className="text-gray-600">Real-time Editing</div>
          </div>
          <div className="bg-white rounded-lg p-6 shadow-md text-center">
            <div className="text-3xl font-bold text-blue-600 mb-2">Secure</div>
            <div className="text-gray-600">Privacy First</div>
          </div>
        </div>

        {/* Features Grid */}
        <div id="features" className="mb-16">
          <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
            Powerful PDF Operations
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {features.map((feature, idx) => (
              <div
                key={idx}
                className="bg-white rounded-lg p-6 shadow-md hover:shadow-xl transition-shadow border border-gray-100"
              >
                <div className="flex items-center gap-3 mb-4">
                  <div className="text-blue-600">{feature.icon}</div>
                  <h3 className="text-xl font-semibold text-gray-900">
                    {feature.category}
                  </h3>
                </div>
                <ul className="space-y-2">
                  {feature.items.map((item, itemIdx) => (
                    <li key={itemIdx} className="flex items-start gap-2 text-gray-600">
                      <FileCheck className="w-4 h-4 text-green-500 mt-0.5 flex-shrink-0" />
                      <span className="text-sm">{item}</span>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>

        {/* Key Features Highlight */}
        <div className="bg-white rounded-xl p-8 shadow-lg mb-16">
          <h2 className="text-2xl font-bold text-center text-gray-900 mb-8">
            Key Features
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="inline-flex items-center justify-center w-16 h-16 bg-blue-100 rounded-full mb-4">
                <Edit3 className="w-8 h-8 text-blue-600" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                Word-Level Editing
              </h3>
              <p className="text-gray-600 text-sm">
                Edit individual words directly on the PDF with inline editing. 
                Double-click any word to edit it instantly.
              </p>
            </div>
            <div className="text-center">
              <div className="inline-flex items-center justify-center w-16 h-16 bg-purple-100 rounded-full mb-4">
                <Zap className="w-8 h-8 text-purple-600" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                Real-time Processing
              </h3>
              <p className="text-gray-600 text-sm">
                Fast and efficient PDF processing with instant preview. 
                See your changes immediately.
              </p>
            </div>
            <div className="text-center">
              <div className="inline-flex items-center justify-center w-16 h-16 bg-green-100 rounded-full mb-4">
                <Shield className="w-8 h-8 text-green-600" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                Secure & Private
              </h3>
              <p className="text-gray-600 text-sm">
                All processing happens locally. Your files never leave your device. 
                Complete privacy guaranteed.
              </p>
            </div>
          </div>
        </div>

        {/* CTA Section */}
        <div className="text-center bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl p-12 text-white">
          <h2 className="text-3xl font-bold mb-4">Ready to Get Started?</h2>
          <p className="text-xl mb-8 opacity-90">
            Upload your PDF and start editing right away
          </p>
          <Link
            to="/app"
            className="inline-flex items-center gap-2 px-8 py-4 bg-white text-blue-600 rounded-lg font-semibold hover:bg-gray-100 transition-colors shadow-lg hover:shadow-xl"
          >
            <Upload className="w-5 h-5" />
            Upload PDF Now
          </Link>
        </div>
      </div>
    </div>
  );
}

