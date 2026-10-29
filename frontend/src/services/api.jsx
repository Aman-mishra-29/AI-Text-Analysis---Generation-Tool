import axios from "axios";

// ---------------------------------------------------
// Base Configuration
// ---------------------------------------------------
const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api/v1";

// Create Axios Instance
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    "Content-Type": "application/json",
  },
});

// ---------------------------------------------------
// Request Interceptor
// ---------------------------------------------------
api.interceptors.request.use(
  (config) => {
    // Example: Add token if needed in future
    // const token = localStorage.getItem("token");
    // if (token) config.headers.Authorization = `Bearer ${token}`;

    return config;
  },
  (error) => Promise.reject(error)
);

// ---------------------------------------------------
// Response Interceptor
// ---------------------------------------------------
api.interceptors.response.use(
  (response) => response.data,
  (error) => {
    console.error("API Error:", error);

    return Promise.reject(
      error?.response?.data || {
        message: "Something went wrong",
      }
    );
  }
);

// ---------------------------------------------------
// API METHODS
// ---------------------------------------------------

/**
 * Summarize Text
 */
export const summarizeText = async (payload) => {
  return api.post("/summarize/", payload);
};

/**
 * Plagiarism Check
 */
export const checkPlagiarism = async (payload) => {
  return api.post("/plagiarism/", payload);
};

/**
 * Autocorrect Text
 */
export const autocorrectText = async (payload) => {
  return api.post("/autocorrect/", payload);
};

// ---------------------------------------------------
// Export Instance (Optional)
export default api;

export const getHistory = async () => {
  return api.get("/history/");
};