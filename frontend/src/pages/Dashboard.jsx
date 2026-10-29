import React, { useEffect, useState } from "react";

const Dashboard = () => {
  const [history, setHistory] = useState([]);

  useEffect(() => {
    const storedHistory =
      JSON.parse(localStorage.getItem("history")) || [];

    setHistory(storedHistory);
  }, []);

  return (
    <div className="min-h-screen p-6 bg-gray-100 dark:bg-gray-900">
      <h1 className="text-2xl font-bold mb-4 dark:text-white">
        📊 History Dashboard
      </h1>

      {history.length === 0 ? (
        <p className="text-gray-500">No history available</p>
      ) : (
        <div className="space-y-4">
          {history.map((item, index) => (
            <div
              key={index}
              className="p-4 bg-white dark:bg-gray-800 rounded shadow"
            >
              <p className="text-sm text-gray-500">{item.type}</p>

              <p className="font-medium dark:text-white">
                {item.input?.slice(0, 100)}...
              </p>

              <p className="text-blue-600 mt-2">
                {String(item.output)?.slice(0, 100)}...
              </p>

              <p className="text-xs text-gray-400 mt-1">
                {new Date(item.date).toLocaleString()}
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Dashboard;