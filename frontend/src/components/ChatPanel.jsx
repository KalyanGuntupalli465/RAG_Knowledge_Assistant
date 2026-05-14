import { useState, useRef, useEffect } from "react";
import { askQuestion } from "../api/client";
import MessageBubble from "./MessageBubble";

export default function ChatPanel({ activeDoc }) {
  const [chatHistories, setChatHistories] = useState({});
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef();

  // Derive current messages from active doc
  const messages = activeDoc ? (chatHistories[activeDoc.collection_name] || []) : [];

  // Auto-scroll when messages change
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const addMessage = (msg) => {
    setChatHistories((prev) => ({
      ...prev,
      [activeDoc.collection_name]: [...(prev[activeDoc.collection_name] || []), msg],
    }));
  };

  const replaceLastMessage = (msg) => {
    setChatHistories((prev) => {
      const current = prev[activeDoc.collection_name] || [];
      return {
        ...prev,
        [activeDoc.collection_name]: [...current.slice(0, -1), msg],
      };
    });
  };

  const sendMessage = async () => {
    if (!input.trim() || !activeDoc || loading) return;
    const query = input.trim();
    setInput("");

    addMessage({ role: "user", text: query });
    addMessage({ role: "bot", text: "..." });
    setLoading(true);

    try {
      const res = await askQuestion(activeDoc.collection_name, query);
      replaceLastMessage({
        role: "bot",
        text: res.data.answer,
        sources: res.data.sources,
      });
    } catch (err) {
      replaceLastMessage({
        role: "bot",
        text: "Something went wrong. Please try again.",
      });
    } finally {
      setLoading(false);
    }
  };

  if (!activeDoc) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center gap-2 text-gray-300">
        <span className="text-4xl">💬</span>
        <p className="text-sm">Upload and select a document to start chatting</p>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-full">
      {/* Messages */}
      <div className="flex-1 overflow-y-auto flex flex-col gap-3 pr-1 mb-4">
        {messages.length === 0 && (
          <div className="flex flex-col items-center justify-center h-full gap-2 text-gray-300">
            <span className="text-3xl">🔍</span>
            <p className="text-sm">
              Ask anything about <span className="font-medium text-gray-400">{activeDoc.filename}</span>
            </p>
          </div>
        )}
        {messages.map((msg, i) => (
          <MessageBubble key={i} message={msg} />
        ))}
        <div ref={bottomRef} />
      </div>

      {/* Input row */}
      <div className="flex gap-2 border-t border-gray-100 pt-3">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          placeholder="Ask anything about your document…"
          disabled={loading}
          className="flex-1 text-sm border border-gray-200 bg-gray-50 rounded-xl px-4 py-2.5
            focus:outline-none focus:border-blue-300 focus:bg-white disabled:opacity-50 transition-all"
        />
        <button
          onClick={sendMessage}
          disabled={!input.trim() || loading}
          className="px-5 py-2.5 bg-blue-500 text-white text-sm rounded-xl
            hover:bg-blue-600 disabled:opacity-40 transition-colors font-medium shadow-sm"
        >
          Send
        </button>
      </div>
    </div>
  );
}