/**
 * FILE: /src/main.tsx
 * PURPOSE: The primary entry point for the React 19 application.
 * USAGE: Initialized by index.html to mount the root App component within the browser's DOM under StrictMode.
 */

import {StrictMode} from 'react';
import {createRoot} from 'react-dom/client';
import App from './App.tsx';
import './index.css';

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
