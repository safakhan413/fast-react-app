import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import LoginPage from './LoginPage';
import DataPage from './DataPage';

function App() {
  const accessToken = localStorage.getItem('access_token');

  return (
    <Router>
      <Routes>
        <Route path="/" element={<LoginPage />} />
        <Route
          path="/data"
          element={accessToken ? <DataPage /> : <Navigate to="/" />}
        />
      </Routes>
    </Router>
  );
}

export default App;
