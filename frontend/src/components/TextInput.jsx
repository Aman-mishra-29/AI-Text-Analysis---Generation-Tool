import React, { useState } from "react";
import * as pdfjsLib from "pdfjs-dist";
import mammoth from "mammoth";

// Required for PDF parsing
pdfjsLib.GlobalWorkerOptions.workerSrc =
  `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjsLib.version}/pdf.worker.min.js`;

const TextInput = ({
  label = "Enter Text",
  placeholder = "Type here...",
  value,
  onChange,
  rows = 5,
  required = false,
  error = "",
  maxLength,
}) => {
  const [fileName, setFileName] = useState("");

  // ---------------------------------------------------
  // Handle File Upload
  // ---------------------------------------------------
  const handleFileUpload = async (file) => {
    if (onFileUpload) {
      onFileUpload(file.name);
    }

    if (!file) return;

    if (file.size > 5 * 1024 * 1024) {
        alert("File too large (max 5MB)");
        return;
    }

    setFileName(file.name);

    if (onFileUpload) {
        onFileUpload(file.name);
    }

    try {
      const fileType = file.type;

      // TXT FILE
      if (fileType === "text/plain") {
        const text = await file.text();
        onChange(text);
      }

      // PDF FILE
      else if (fileType === "application/pdf") {
        const arrayBuffer = await file.arrayBuffer();
        const pdf = await pdfjsLib.getDocument({ data: arrayBuffer }).promise;

        let fullText = "";

        for (let i = 1; i <= pdf.numPages; i++) {
          const page = await pdf.getPage(i);
          const content = await page.getTextContent();
          const strings = content.items.map((item) => item.str);
          fullText += strings.join(" ") + "\n";
        }

        onChange(fullText);
      }

      // DOCX FILE
      else if (
        fileType ===
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
      ) {
        const arrayBuffer = await file.arrayBuffer();
        const result = await mammoth.extractRawText({ arrayBuffer });
        onChange(result.value);
      }

      else {
        alert("Unsupported file type. Please upload PDF, DOCX, or TXT.");
      }

    } catch (err) {
      console.error(err);
      alert("Error reading file.");
    }
  };

  return (
    <div className="w-full mb-4">

      {/* Label */}
      {label && (
        <label className="block text-sm font-medium text-gray-700 mb-1">
          {label} {required && <span className="text-red-500">*</span>}
        </label>
      )}

      {/* File Upload */}
      <div className="mb-2">
        <input
          type="file"
          accept=".txt,.pdf,.docx"
          onChange={(e) => handleFileUpload(e.target.files[0])}
          className="block w-full text-sm text-gray-600 file:mr-4 file:py-2 file:px-4 
          file:rounded-lg file:border-0 file:bg-blue-600 file:text-white 
          hover:file:bg-blue-700"
        />

        {fileName && (
          <p className="text-xs text-gray-500 mt-1">
            Uploaded: {fileName}
          </p>
        )}
      </div>

      {/* Textarea */}
      <textarea
        className={`w-full p-3 border rounded-lg focus:outline-none focus:ring-2 transition
          ${
            error
              ? "border-red-500 focus:ring-red-400"
              : "border-gray-300 focus:ring-blue-500"
          }`}
        placeholder={placeholder}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        rows={rows}
        maxLength={maxLength}
      />

      {/* Character Count */}
      {maxLength && (
        <div className="text-right text-xs text-gray-500 mt-1">
          {value.length}/{maxLength}
        </div>
      )}

      {/* Error */}
      {error && (
        <div className="text-red-600 text-sm mt-1">
          {error}
        </div>
      )}

    </div>
  );
};

export default TextInput;