# Semker Frontend

A React TypeScript frontend for the Semker async message processing system.

## Features

- **Three-row layout**: Header, main content area, and footer
- **Backend integration**: Full communication with the FastAPI backend
- **Message management**: Create and view messages with sender information
- **Health monitoring**: Backend health check functionality
- **Responsive design**: Modern UI that works on different screen sizes

## Project Structure

```
src/
├── components/          # React components
│   ├── Header.tsx      # Navigation header
│   ├── MainContent.tsx # Main content area with backend integration
│   └── Footer.tsx      # Footer component
├── services/           # API services
│   └── apiService.ts   # Backend API integration
├── App.tsx             # Main app component
├── App.css             # App-specific styles
├── index.tsx           # Entry point
└── index.css           # Global styles
```

## Available Scripts

- `npm start` - Start development server on http://localhost:3000
- `npm run build` - Build for production
- `npm test` - Run tests
- `npm run eject` - Eject from Create React App (irreversible)

## Backend Integration

The frontend communicates with the FastAPI backend running on port 8000. The API service provides:

- Health checks (`/health`)
- Message creation (`POST /messages`)
- Message listing (`GET /messages`)
- Message status tracking

## Environment Variables

- `REACT_APP_API_URL` - Backend API URL (defaults to http://localhost:8000)

## Getting Started

1. Install dependencies: `npm install`
2. Start the backend server (see backend README)
3. Start the frontend: `npm start`
4. Open http://localhost:3000 in your browser

## Usage

1. **Health Check**: Click "Check Backend Health" to verify backend connectivity
2. **Send Messages**: Fill in sender name (optional) and message content, then click "Send Message"
3. **View Messages**: Click "Refresh Messages" to see all messages from the backend
4. **Real-time Updates**: Messages appear immediately after sending

The frontend automatically handles errors and provides user feedback for all operations.
