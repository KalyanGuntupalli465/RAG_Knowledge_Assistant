import { useState } from "react";
import UploadPanel from "./components/UploadPanel";
import ChatPanel from "./components/ChatPanel";
import SummaryPanel from "./components/SummaryPanel";

export default function App() {
  const [docs, setDocs] = useState([]);
  const [activeDoc, setActiveDoc] = useState(null);
  const [tab, setTab] = useState("chat");

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col">
      {/* Top bar */}
      <header className="bg-white border-b border-gray-200 px-6 py-3 flex items-center gap-3 shadow-sm">
        <span className="text-xl">🧠</span>
        <h1 className="text-base font-semibold text-gray-800">RAG Knowledge Assistant</h1>
        {activeDoc && (
          <span className="ml-auto text-xs text-gray-500 bg-gray-100 border border-gray-200 px-3 py-1 rounded-full">
            {activeDoc.filename}
          </span>
        )}
      </header>

      {/* Main layout */}
      <div className="flex flex-1 gap-4 p-5 max-w-6xl mx-auto w-full">

        {/* Left sidebar */}
        <aside className="w-64 shrink-0">
          <div className="bg-white rounded-2xl border border-gray-200 p-4 h-full shadow-sm">
            <p className="text-xs font-semibold text-gray-400 uppercase tracking-widest mb-3">
              Documents
            </p>
            <UploadPanel
              docs={docs}
              setDocs={setDocs}
              activeDoc={activeDoc}
              setActiveDoc={setActiveDoc}
            />
          </div>
        </aside>

        {/* Main panel */}
        <main className="flex-1 bg-white rounded-2xl border border-gray-200 p-5 flex flex-col shadow-sm">
          {/* Tabs */}
          <div className="flex gap-2 mb-4 border-b border-gray-100 pb-3">
            {["chat", "summary"].map((t) => (
              <button
                key={t}
                onClick={() => setTab(t)}
                className={`text-sm px-4 py-1.5 rounded-lg transition-colors capitalize font-medium
                  ${tab === t
                    ? "bg-blue-50 text-blue-600 border border-blue-100"
                    : "text-gray-400 hover:text-gray-600 hover:bg-gray-50"
                  }`}
              >
                {t === "chat" ? "💬 Chat" : "✨ Summary"}
              </button>
            ))}
          </div>

          {/* Tab content */}
          <div className="flex-1 flex flex-col overflow-hidden">
            {tab === "chat"
              ? <ChatPanel activeDoc={activeDoc} />
              : <SummaryPanel activeDoc={activeDoc} />
            }
          </div>
        </main>
      </div>
    </div>
  );
}