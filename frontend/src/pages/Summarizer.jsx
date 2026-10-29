import React, { useState } from "react";
import axios from "axios"; // ✅ FIX
import Result from "../components/Result";
import TextInput from "../components/TextInput";

const API_BASE_URL = "http://localhost:8000/api/v1";

const Summarizer = () => {
  const [text, setText] = useState("");
  const [summary, setSummary] = useState("");
  const [inputLength, setInputLength] = useState(0);
  const [summaryLength, setSummaryLength] = useState(0);
  const [maxLength, setMaxLength] = useState(130);
  const [minLength, setMinLength] = useState(30);
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
  // Submit Handler
  // ---------------------------------------------------
  const handleSubmit = async () => {
    if (!text.trim()) {
      setError("Please enter text to summarize.");
      return;
    }

    try {
      setLoading(true);
      setError("");
      setSummary("");

      const response = await axios.post(
        `${API_BASE_URL}/summarize/`,
        {
          text: text,
          max_length: maxLength,
          min_length: minLength,
        }
      );

      const data = response.data;

      setSummary(data.summary);
      setInputLength(data.input_length);
      setSummaryLength(data.summary_length);

      // ✅ Save correct summary
      saveToHistory(text, data.summary, "Summarization");

    } catch (err) {
      console.error(err);
      setError(
        err?.response?.data?.detail || "Something went wrong."
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
      <div className="max-w-5xl mx-auto bg-white dark:bg-gray-800 shadow-xl rounded-2xl p-6">

        <h1 className="text-2xl font-bold mb-4 text-gray-800 dark:text-white">
          📄 Text Summarizer
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

        {/* Controls */}
        <div className="grid grid-cols-2 gap-4 mt-4">
          <div>
            <label className="text-sm font-medium">Max Length</label>
            <input
              type="number"
              value={maxLength}
              onChange={(e) => setMaxLength(Number(e.target.value))}
              className="w-full p-2 border rounded-lg"
            />
          </div>

          <div>
            <label className="text-sm font-medium">Min Length</label>
            <input
              type="number"
              value={minLength}
              onChange={(e) => setMinLength(Number(e.target.value))}
              className="w-full p-2 border rounded-lg"
            />
          </div>
        </div>

        {/* Submit Button */}
        <button
          onClick={handleSubmit}
          disabled={loading || !text.trim()}
          className="mt-4 w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50"
        >
          {loading ? "Generating..." : "Generate Summary"}
        </button>

        {/* Clear */}
        <button
          onClick={() => {
            setText("");
            setSummary("");
          }}
          className="mt-2 text-sm text-red-500 hover:underline"
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
          title="Summary"
          content={summary}
          stats={[
            { label: "Input Length", value: inputLength },
            { label: "Summary Length", value: summaryLength },
          ]}
          loading={loading}
          error={error}
        />

      </div>
    </div>
  );
};

export default Summarizer;