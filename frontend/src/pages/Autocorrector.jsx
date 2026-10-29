import React, { useState } from "react";
import axios from "axios"; // ✅ FIX
import Result from "../components/Result";
import TextInput from "../components/TextInput";

const API_BASE_URL = "http://localhost:8000/api/v1";

const Autocorrector = () => {
  const [text, setText] = useState("");
  const [correctedText, setCorrectedText] = useState("");
  const [corrections, setCorrections] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [fileName, setFileName] = useState(""); // ✅ FIX

  // ---------------------------------------------------
  // Save History
  // ---------------------------------------------------
  const saveToHistory = (input, output, type) => {
    const history = JSON.parse(localStorage.getItem("history")) || [];

    history.unshift({
      type,
      input,
      output,
      date: new Date().toISOString(),
    });

    localStorage.setItem("history", JSON.stringify(history));
  };

  // ---------------------------------------------------
  // Handle Submit
  // ---------------------------------------------------
  const handleSubmit = async () => {
    if (!text.trim()) {
      setError("Please enter text to correct.");
      return;
    }

    try {
      setLoading(true);
      setError("");
      setCorrectedText("");
      setCorrections([]);

      const response = await axios.post(
        `${API_BASE_URL}/autocorrect/`,
        {
          text: text,
        }
      );

      const data = response.data;

      // ✅ FIXED
      setCorrectedText(data.corrected_text);
      setCorrections(data.corrections || []);

      // ✅ FIXED HISTORY
      saveToHistory(text, data.corrected_text, "Autocorrect");

    } catch (err) {
      console.error(err);
      setError(
        err?.response?.data?.detail || "Something went wrong. Try again."
      );
    } finally {
      setLoading(false);
    }
  };

  // ---------------------------------------------------
  // UI
  // ---------------------------------------------------
  return (
    <div className="min-h-screen bg-gray-100 dark:bg-gray-900 p-6">
      <div className="max-w-4xl mx-auto bg-white dark:bg-gray-800 shadow-xl rounded-2xl p-6">

        <h1 className="text-2xl font-bold mb-4 text-gray-800 dark:text-white">
          ✍️ Autocorrect & Grammar Tool
        </h1>

        {/* Input */}
        <TextInput
          value={text}
          onChange={setText}
          onFileUpload={setFileName}
        />

        {fileName && (
          <p className="text-xs text-gray-500 mb-2">
            Using file: {fileName}
          </p>
        )}

        {/* Button */}
        <button
          onClick={handleSubmit}
          disabled={loading || !text.trim()}
          className="mt-4 w-full bg-blue-600 text-white py-2 rounded-lg"
        >
          {loading ? "Processing..." : "Correct Text"}
        </button>

        {/* Clear */}
        <button
          onClick={() => {
            setText("");
            setCorrectedText("");
            setCorrections([]);
          }}
          className="mt-2 text-sm text-red-500"
        >
          Clear Input
        </button>

        {/* Error */}
        {error && (
          <div className="mt-4 text-red-600 bg-red-100 p-3 rounded">
            {error}
          </div>
        )}

        {/* Result */}
        <Result
          title="Corrected Text"
          content={correctedText}
          list={corrections}
          loading={loading}
          error={error}
        />

      </div>
    </div>
  );
};

export default Autocorrector;