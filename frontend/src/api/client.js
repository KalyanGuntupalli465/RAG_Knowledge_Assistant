import axios from "axios";

const API = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000",
});

export const uploadPDF = (file) => {
  const form = new FormData();
  form.append("file", file);
  return API.post("/upload", form);
};

export const askQuestion = (collection_name, query, top_k = 5) =>
  API.post("/ask", { collection_name, query, top_k });

export const summarizeDoc = (collection_name) =>
  API.post("/summarize", { collection_name });

export const listDocuments = () => API.get("/documents");

export const deleteDocument = (collection_name) =>
  API.delete(`/documents/${collection_name}`);
