import React from "react";
import { BrowserRouter as Router, Routes, Route, NavLink } from "react-router-dom";
import useDarkMode from "./hooks/useDarkMode";

// Pages
import Summarizer from "./pages/Summarizer";
import Plagiarism from "./pages/Plagiarism";
import Autocorrector from "./pages/Autocorrector";
import Dashboard from "./pages/Dashboard";

<Route path="/dashboard" element={<Dashboard />} />

// ---------------------------------------------------
// Navbar Component
// ---------------------------------------------------
const Navbar = () => {
  const [darkMode, setDarkMode] = useDarkMode();
  const linkClass =
    "px-4 py-2 rounded-lg text-sm font-medium transition";

  const activeClass = "bg-blue-600 text-white";
  const inactiveClass =
      "text-gray-700 dark:text-gray-200 hover:bg-gray-200 dark:hover:bg-gray-700";

  return (
    <nav className="bg-white dark:bg-gray-900 shadow-md mb-6">
      <div className="max-w-6xl mx-auto px-4 py-3 flex justify-between items-center">

        {/* Logo */}
        <h1 className="text-lg font-bold text-blue-600 dark:text-white">
          AI Text Toolkit 🚀
        </h1>

        {/* Links */}
        <div className="flex gap-3">
          <NavLink
            to="/"
            className={({ isActive }) =>
              `${linkClass} ${isActive ? activeClass : inactiveClass}`
            }
          >
            Summarizer
          </NavLink>

          <NavLink
            to="/plagiarism"
            className={({ isActive }) =>
              `${linkClass} ${isActive ? activeClass : inactiveClass}`
            }
          >
            Plagiarism
          </NavLink>

          <NavLink
            to="/autocorrect"
            className={({ isActive }) =>
              `${linkClass} ${isActive ? activeClass : inactiveClass}`
            }
          >
            Autocorrect
          </NavLink>

          <NavLink to="/dashboard">Dashboard</NavLink>
          
          {/* 🌙 Dark Mode Toggle */}
          <button
            onClick={() => setDarkMode(!darkMode)}
            className="ml-2 px-3 py-2 rounded-lg bg-gray-200 dark:bg-gray-700 text-sm"
            >
            {darkMode ? "☀️" : "🌙"}
          </button>
          
        </div>
      </div>
    </nav>
  );
};

// ---------------------------------------------------
// 404 Page
// ---------------------------------------------------
const NotFound = () => (
  <div className="text-center mt-20">
    <h1 className="text-3xl font-bold text-red-500">404</h1>
    <p className="text-gray-600 mt-2">Page not found</p>
  </div>
);

// ---------------------------------------------------
// Main App
// ---------------------------------------------------
const App = () => {
  return (
    <Router>
      <div className="min-h-screen bg-gray-100">

        {/* Navbar */}
        <Navbar />

        {/* Routes */}
        <div className="px-4">
          <Routes>
            <Route path="/" element={<Summarizer />} />
            <Route path="/plagiarism" element={<Plagiarism />} />
            <Route path="/autocorrect" element={<Autocorrector />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </div>

      </div>
    </Router>
  );
};

export default App;