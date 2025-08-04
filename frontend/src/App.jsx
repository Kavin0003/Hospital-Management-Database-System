import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './components/Login';
import Register from './components/Register';
import Dashboard from './components/Dashboard';
import './index.css';

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if user is logged in
    const token = localStorage.getItem('token');
    const userData = localStorage.getItem('user');
    
    if (token && userData) {
      try {
        setUser(JSON.parse(userData));
      } catch (error) {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
      }
    }
    setLoading(false);
  }, []);

  const handleLogin = (userData) => {
    setUser(userData);
  };

  const handleLogout = () => {
    setUser(null);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <Router>
      <div className="App">
        <Routes>
          <Route 
            path="/login" 
            element={user ? <Navigate to="/dashboard" /> : <Login onLogin={handleLogin} />} 
          />
          <Route 
            path="/register" 
            element={user ? <Navigate to="/dashboard" /> : <Register />} 
          />
          <Route 
            path="/dashboard" 
            element={user ? <Dashboard user={user} onLogout={handleLogout} /> : <Navigate to="/login" />} 
          />
          <Route 
            path="/" 
            element={<Navigate to={user ? "/dashboard" : "/login"} />} 
          />
          {/* Placeholder routes for other pages */}
          <Route 
            path="/patients" 
            element={user ? <div className="p-8"><h1 className="text-2xl">Patients Module - Coming Soon</h1></div> : <Navigate to="/login" />} 
          />
          <Route 
            path="/doctors" 
            element={user ? <div className="p-8"><h1 className="text-2xl">Doctors Module - Coming Soon</h1></div> : <Navigate to="/login" />} 
          />
          <Route 
            path="/appointments" 
            element={user ? <div className="p-8"><h1 className="text-2xl">Appointments Module - Coming Soon</h1></div> : <Navigate to="/login" />} 
          />
          <Route 
            path="/billing" 
            element={user ? <div className="p-8"><h1 className="text-2xl">Billing Module - Coming Soon</h1></div> : <Navigate to="/login" />} 
          />
          <Route 
            path="/staff" 
            element={user ? <div className="p-8"><h1 className="text-2xl">Staff Module - Coming Soon</h1></div> : <Navigate to="/login" />} 
          />
          <Route 
            path="/inventory" 
            element={user ? <div className="p-8"><h1 className="text-2xl">Inventory Module - Coming Soon</h1></div> : <Navigate to="/login" />} 
          />
          <Route 
            path="/medical-records" 
            element={user ? <div className="p-8"><h1 className="text-2xl">Medical Records Module - Coming Soon</h1></div> : <Navigate to="/login" />} 
          />
          <Route 
            path="/feedback" 
            element={user ? <div className="p-8"><h1 className="text-2xl">Feedback Module - Coming Soon</h1></div> : <Navigate to="/login" />} 
          />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
