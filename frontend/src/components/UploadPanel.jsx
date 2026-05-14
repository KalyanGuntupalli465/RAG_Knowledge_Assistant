import { useRef, useState } from "react";
import { uploadPDF, deleteDocument } from "../api/client";

export default function UploadPanel({ docs, setDocs, activeDoc, setActiveDoc }) {
  const inputRef = useRef();
  const [uploading, setUploading] = useState(false);
  const [dragOver, setDragOver] = useState(false);

  const handleUpload = async (file) => {
    if (!file || !file.name.endsWith(".pdf")) return alert("PDF files only.");
    setUploading(true);
    try {
      const res = await uploadPDF(file);
      const newDoc = {
        collection_name: res.data.collection_name,
        filename: res.data.filename,
        num_chunks: res.data.num_chunks,
      };
      setDocs((prev) => [newDoc, ...prev]);
      setActiveDoc(newDoc);
    } catch (err) {
      alert("Upload failed: " + (err.response?.data?.detail || err.message));
    } finally {
      setUploading(false);
    }
  };

  const handleDelete = async (e, collection_name) => {
    e.stopPropagation();
    if (!confirm("Delete this document?")) return;
    try {
      await deleteDocument(collection_name);
      setDocs((prev) => prev.filter((d) => d.collection_name !== collection_name));
      if (activeDoc?.collection_name === collection_name) setActiveDoc(null);
    } catch (err) {
      alert("Delete failed.");
    }
  };

  return (
    <div className="flex flex-col gap-2">
      {/* Drop zone */}
      <div
        onClick={() => inputRef.current.click()}
        onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
        onDragLeave={() => setDragOver(false)}
        onDrop={(e) => {
          e.preventDefault();
          setDragOver(false);
          handleUpload(e.dataTransfer.files[0]);
        }}
        className={`border-2 border-dashed rounded-xl p-5 text-center cursor-pointer transition-all
          ${dragOver
            ? "border-blue-400 bg-blue-50"
            : "border-gray-200 bg-gray-50 hover:border-gray-300 hover:bg-gray-100"
          }`}
      >
        <input
          ref={inputRef}
          type="file"
          accept=".pdf"
          className="hidden"
          onChange={(e) => handleUpload(e.target.files[0])}
        />
        {uploading ? (
          <div className="flex flex-col items-center gap-2">
            <div className="w-5 h-5 border-2 border-blue-400 border-t-transparent rounded-full animate-spin" />
            <p className="text-xs text-blue-500 font-medium">Uploading & indexing…</p>
          </div>
        ) : (
          <>
            <p className="text-2xl mb-1">📄</p>
            <p className="text-xs text-gray-400">
              Drop PDF or <span className="text-blue-500 underline cursor-pointer">browse</span>
            </p>
          </>
        )}
      </div>

      {/* Document list */}
      {docs.length === 0 ? (
        <p className="text-xs text-gray-300 text-center mt-2">No documents yet</p>
      ) : (
        <div className="flex flex-col gap-1.5 mt-1">
          {docs.map((doc) => {
            const isActive = activeDoc?.collection_name === doc.collection_name;
            return (
              <div
                key={doc.collection_name}
                onClick={() => setActiveDoc(doc)}
                className={`flex items-center gap-2 p-2.5 rounded-xl border cursor-pointer transition-all group
                  ${isActive
                    ? "border-blue-200 bg-blue-50 shadow-sm"
                    : "border-gray-100 bg-gray-50 hover:border-gray-200 hover:bg-white"
                  }`}
              >
                <span className="text-sm">📄</span>
                <div className="flex-1 min-w-0">
                  <p className={`text-xs font-medium truncate ${isActive ? "text-blue-700" : "text-gray-600"}`}>
                    {doc.filename}
                  </p>
                  <p className="text-xs text-gray-300">{doc.num_chunks} chunks</p>
                </div>
                <button
                  onClick={(e) => handleDelete(e, doc.collection_name)}
                  className="opacity-0 group-hover:opacity-100 text-gray-300 hover:text-red-400 transition-all text-xs font-bold"
                >
                  ✕
                </button>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}