# AeroPdf - Frontend

Frontend application for AeroPdf built with React + TypeScript + Vite + Tailwind CSS.

## Technology Stack

- React 18+
- TypeScript
- Vite
- Tailwind CSS
- React Router v6

## Setup

1. Install dependencies:

```bash
npm install
```

2. Start development server:

```bash
npm run dev
```

The application will be available at `http://localhost:3001`

## Build

```bash
npm run build
```

## Project Structure

```
frontend/
├── src/
│   ├── main.tsx              # Entry point
│   ├── App.tsx               # Main app component with routing
│   ├── pages/                # Page components
│   │   ├── HomePage.tsx
│   │   └── EditorPage.tsx
│   ├── components/           # Reusable components
│   │   ├── Layout/
│   │   ├── Upload/
│   │   └── Editor/
│   ├── api/                  # API client
│   │   ├── client.ts
│   │   └── pdfs.ts
│   ├── hooks/                # Custom React hooks
│   │   ├── usePdfDocument.ts
│   │   └── useTextMap.ts
│   ├── types/                # TypeScript type definitions
│   │   ├── pdf.ts
│   │   └── textMap.ts
│   └── styles/
│       └── globals.css
├── index.html
├── vite.config.ts
├── tsconfig.json
├── tailwind.config.js
└── package.json
```

## Features

- PDF upload
- Page navigation
- Text block selection and editing
- Real-time coordinate scaling for block overlays
- PDF download

## API Configuration

The frontend expects the backend API to be running at `http://localhost:8001/api`.

To change this, update `API_BASE_URL` in `src/api/client.ts`.

