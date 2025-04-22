import { BrowserRouter as Router, Route, Routes, Link, Navigate } from 'react-router-dom';
import { useState, useEffect } from 'react';
import LoginPage from './LoginPage';
import RegisterPage from './RegisterPage';
import VideoGenerator from './VideoGenerator';
import HistoryPage from './HistoryPage';
import './App.css';

function App() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    fetch('http://localhost:5000/my-history', { credentials: 'include' })
      .then((res) => {
        if (res.ok) setUser(true);
      });
  }, []);

  const handleLogout = async () => {
    await fetch('http://localhost:5000/logout', {
      method: 'POST',
      credentials: 'include',
    });
    setUser(null);
  };

  return (
    <Router>
      <nav className="navbar">
        {/* <Link to="/">Generate</Link> */}
        {/* {user && <Link to="/history">History</Link>} */}
        {/* {!user ? (
          <>
            <Link to="/login">Login</Link>
            <Link to="/register">Register</Link>
          </>
        ) : (
          <button onClick={handleLogout}>Logout</button>
        )} */}
        {/* {!user ? (
          <>
            <Link to="/login">Login</Link>
            <Link to="/register">Register</Link>
          </>
        ) : (
          <button onClick={handleLogout} className="logout-button">Logout</button>
        )} */}
<div className="nav-links">
    <Link to="/">Generate</Link>
    {user && <Link to="/history">History</Link>}
    {!user && <Link to="/login">Login</Link>}
    {!user && <Link to="/register">Register</Link>}
  </div>
  {user && <button onClick={handleLogout} className="logout-button">Logout</button>}

      </nav>

      <Routes>
        <Route path="/" element={user ? <VideoGenerator /> : <Navigate to="/login" />} />
        <Route path="/login" element={<LoginPage onLogin={() => setUser(true)} />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/history" element={user ? <HistoryPage /> : <Navigate to="/login" />} />
      </Routes>
    </Router>
  );
}

export default App;
