export default function MessageBubble({ message }) {
  const { role, text, sources } = message;
  const isUser = role === "user";

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div
        className={`max-w-[80%] px-4 py-3 rounded-2xl text-sm leading-relaxed
          ${isUser
            ? "bg-blue-500 text-white rounded-br-sm shadow-sm"
            : "bg-gray-50 border border-gray-200 text-gray-700 rounded-bl-sm"
          }`}
      >
        {text === "..." ? (
          <div className="flex items-center gap-2">
            <div className="flex gap-1">
              <span className="w-1.5 h-1.5 bg-gray-300 rounded-full animate-bounce" style={{ animationDelay: "0ms" }} />
              <span className="w-1.5 h-1.5 bg-gray-300 rounded-full animate-bounce" style={{ animationDelay: "150ms" }} />
              <span className="w-1.5 h-1.5 bg-gray-300 rounded-full animate-bounce" style={{ animationDelay: "300ms" }} />
            </div>
            <span className="text-xs text-gray-300">Thinking…</span>
          </div>
        ) : (
          <>
            <p className="whitespace-pre-wrap">{text}</p>
            {sources && sources.length > 0 && (
              <div className="mt-2.5 pt-2 border-t border-gray-200 flex flex-wrap gap-1">
                {sources.map((s, i) => (
                  <span
                    key={i}
                    title={s.text}
                    className="text-xs bg-white border border-gray-200 text-gray-400
                      px-2 py-0.5 rounded-full cursor-help hover:border-gray-300 transition-colors"
                  >
                    chunk {i + 1} · {s.similarity_score}
                  </span>
                ))}
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}