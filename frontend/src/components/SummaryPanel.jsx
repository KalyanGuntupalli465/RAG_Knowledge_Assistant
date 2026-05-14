import { useState } from "react";
import { summarizeDoc } from "../api/client";

export default function SummaryPanel({ activeDoc }) {
  const [summary, setSummary] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSummarize = async () => {
    if (!activeDoc) return;
    setLoading(true);
    setSummary("");
    try {
      const res = await summarizeDoc(activeDoc.collection_name);
      setSummary(res.data.summary);
    } catch (err) {
      setSummary("Failed to generate summary. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  if (!activeDoc) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center gap-2 text-gray-300">
        <span className="text-4xl">✨</span>
        <p className="text-sm">Upload and select a document to summarize</p>
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-4 h-full">
      {/* Header row */}
      <div className="flex items-center justify-between">
        <p className="text-sm text-gray-400">
          Document:{" "}
          <span className="font-medium text-gray-600">{activeDoc.filename}</span>
        </p>
        <button
          onClick={handleSummarize}
          disabled={loading}
          className="flex items-center gap-2 px-4 py-2 bg-blue-500 text-white text-sm
            rounded-xl hover:bg-blue-600 disabled:opacity-50 transition-colors shadow-sm font-medium"
        >
          {loading ? (
            <>
              <div className="w-3.5 h-3.5 border-2 border-white border-t-transparent rounded-full animate-spin" />
              Generating…
            </>
          ) : (
            "✨ Generate Summary"
          )}
        </button>
      </div>

      {/* Summary content */}
      {summary ? (
        <div className="flex-1 bg-gray-50 border border-gray-200 rounded-xl p-5
          text-sm text-gray-700 leading-relaxed whitespace-pre-wrap overflow-y-auto">
          {summary}
        </div>
      ) : (
        <div className="flex-1 flex flex-col items-center justify-center gap-2
          border-2 border-dashed border-gray-100 rounded-xl text-gray-300">
          {loading ? (
            <div className="flex flex-col items-center gap-3">
              <div className="w-6 h-6 border-2 border-blue-300 border-t-transparent rounded-full animate-spin" />
              <p className="text-sm text-blue-300">Analyzing document…</p>
            </div>
          ) : (
            <>
              <span className="text-3xl">📋</span>
              <p className="text-sm">Click "Generate Summary" to analyze this document</p>
            </>
          )}
        </div>
      )}
    </div>
  );
}