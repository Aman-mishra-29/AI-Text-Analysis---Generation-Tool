import React from "react";

const Result = ({
  title = "Result",
  content = "",
  stats = [],
  list = [],
  loading = false,
  error = "",
}) => {
  // ---------------------------------------------------
  // Loading State
  // ---------------------------------------------------
  if (loading) {
    return (
      <div className="mt-6 text-center text-blue-600 font-medium">
        Processing...
      </div>
    );
  }

  // ---------------------------------------------------
  // Error State
  // ---------------------------------------------------
  if (error) {
    return (
      <div className="mt-6 text-red-600 bg-red-100 p-3 rounded">
        {error}
      </div>
    );
  }

  // ---------------------------------------------------
  // Empty State
  // ---------------------------------------------------
  if (!content && list.length === 0) {
    return null;
  }

  return (
    <div className="mt-6">

      {/* Title */}
      <h2 className="text-lg font-semibold text-gray-700 mb-3">
        {title}
      </h2>

      {/* Main Content */}
      {content && (
        <div className="bg-gray-50 p-4 rounded border mb-4 whitespace-pre-wrap">
          {content}
        </div>
      )}

      {/* Stats Section */}
      {stats.length > 0 && (
        <div className="grid grid-cols-2 gap-4 text-sm text-gray-600 mb-4">
          {stats.map((item, index) => (
            <div
              key={index}
              className="p-3 bg-gray-100 rounded"
            >
              <strong>{item.label}:</strong> {item.value}
            </div>
          ))}
        </div>
      )}

      {/* List Section (For plagiarism / corrections) */}
      {list.length > 0 && (
        <div className="space-y-3">

          {list.map((item, index) => (
            <div
              key={index}
              className="p-4 border rounded-lg bg-gray-50"
            >

              {/* Generic Text */}
              {item.text && (
                <p className="mb-2 text-gray-700">
                  {item.text}
                </p>
              )}

              {/* Correction Format */}
              {item.original && (
                <p>
                  <span className="text-red-500 font-medium">
                    {item.original}
                  </span>{" "}
                  →{" "}
                  <span className="text-green-600 font-medium">
                    {item.corrected}
                  </span>
                </p>
              )}

              {/* Message */}
              {item.message && (
                <p className="text-sm text-gray-600">
                  {item.message}
                </p>
              )}

              {/* Similarity Score */}
              {item.similarity !== undefined && (
                <>
                  <div className="flex justify-between mt-2">
                    <span className="font-medium">
                      Similarity:
                    </span>

                    <span
                      className={`font-bold ${
                        item.similarity > 70
                          ? "text-red-600"
                          : item.similarity > 40
                          ? "text-yellow-600"
                          : "text-green-600"
                      }`}
                    >
                      {item.similarity}%
                    </span>
                  </div>

                  {/* Progress Bar */}
                  <div className="w-full bg-gray-200 h-2 rounded mt-2">
                    <div
                      className="h-2 bg-blue-600 rounded"
                      style={{ width: `${item.similarity}%` }}
                    />
                  </div>
                </>
              )}

            </div>
          ))}

        </div>
      )}

    </div>
  );
};

export default Result;