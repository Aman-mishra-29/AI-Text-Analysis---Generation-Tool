import React, { useState } from "react";
import axios from "axios"; // ✅ FIX
import Result from "../components/Result";
import TextInput from "../components/TextInput";

const API_BASE_URL = "http://localhost:8000/api/v1";

const Plagiarism = () => {
  const [inputText, setInputText] = useState("");
  const [compareTexts, setCompareTexts] = useState([""]);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [fileName, setFileName] = useState("");

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
  // Handle Comparison Text Change
  // ---------------------------------------------------
  const handleCompareChange = (index, value) => {
    const updated = [...compareTexts];
    updated[index] = value;
    setCompareTexts(updated);
  };

  const addField = () => {
    setCompareTexts([...compareTexts, ""]);
  };

  const removeField = (index) => {
    const updated = compareTexts.filter((_, i) => i !== index);
    setCompareTexts(updated);
  };

  // ---------------------------------------------------
  // Submit Handler
  // ---------------------------------------------------
  const handleSubmit = async () => {
    if (!inputText.trim()) {
      setError("Please enter main text.");
      return;
    }

    const validTexts = compareTexts.filter((t) => t.trim() !== "");

    if (validTexts.length === 0) {
      setError("Please add at least one comparison text.");
      return;
    }

    try {
      setLoading(true);
      setError("");
      setResults(null);

      const response = await axios.post(
        `${API_BASE_URL}/plagiarism/`,
        {
          input_text: inputText, // ✅ IMPORTANT (match backend)
          comparison_texts: validTexts,
        }
      );

      const data = response.data;

      setResults(data);

      // ✅ FIXED HISTORY
      saveToHistory(inputText, data, "Plagiarism");

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
          🔍 Plagiarism Detector
        </h1>

        {/* Input Text */}
        <TextInput
          value={inputText} // ✅ FIX
          onChange={setInputText} // ✅ FIX
          onFileUpload={setFileName}
        />

        {fileName && (
          <p className="text-xs text-gray-500 mb-2">
            Using file: {fileName}
          </p>
        )}

        {/* Comparison Texts */}
        <h2 className="text-lg font-semibold mb-2">
          Compare Against:
        </h2>

        {compareTexts.map((text, index) => (
          <div key={index} className="flex gap-2 mb-2">
            <textarea
              className="w-full p-3 border rounded-lg"
              rows="3"
              placeholder={`Comparison text ${index + 1}`}
              value={text}
              onChange={(e) =>
                handleCompareChange(index, e.target.value)
              }
            />

            {compareTexts.length > 1 && (
              <button
                onClick={() => removeField(index)}
                className="bg-red-500 text-white px-3 rounded-lg"
              >
                ✕
              </button>
            )}
          </div>
        ))}

        <button
          onClick={addField}
          className="mb-4 bg-green-600 text-white px-4 py-2 rounded-lg"
        >
          + Add Text
        </button>

        {/* Clear */}
        <button
          onClick={() => {
            setInputText("");
            setCompareTexts([""]);
            setResults(null);
          }}
          className="mt-2 text-sm text-red-500"
        >
          Clear Input
        </button>

        {/* Submit */}
        <button
          onClick={handleSubmit}
          disabled={loading || !inputText.trim()}
          className="w-full bg-blue-600 text-white py-2 rounded-lg mt-2"
        >
          {loading ? "Checking..." : "Check Plagiarism"}
        </button>

        {/* Error */}
        {error && (
          <div className="mt-4 text-red-600 bg-red-100 p-3 rounded">
            {error}
          </div>
        )}

        {/* Result */}
        <Result
          title="Plagiarism Results"
          list={
            results
              ? results.matches.map(item => ({
                  text: item.compared_text,
                  similarity: item.similarity_score,
                }))
              : []
          }
          stats={
            results
              ? [
                  {
                    label: "Overall Similarity",
                    value: results.overall_similarity + "%",
                  },
                ]
              : []
          }
          loading={loading}
          error={error}
        />

      </div>
    </div>
  );
};

export default Plagiarism;