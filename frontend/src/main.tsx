import React from 'react';
import ReactDOM from 'react-dom/client';
// @ts-ignore
import AppRoutes from './routes/AppRoutes';
// @ts-ignore
import { AuthProvider } from './features/auth/authContext';
import './index.css';



ReactDOM.createRoot(document.getElementById('root')as HTMLElement).render(
  <React.StrictMode>
    <AuthProvider>
      <AppRoutes />
    </AuthProvider>
  </React.StrictMode>
);
