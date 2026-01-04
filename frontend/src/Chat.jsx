import { useEffect, useRef, useState } from "react";
import { sendMessage } from "./api";
import TypingDots from "./TypingDots";
import GraphModal from "./GraphModal";


export default function Chat() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef(null);
  const [graphPath, setGraphPath] = useState(null);


  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const handleSend = async () => {
    if (!input.trim() || loading) return;

    const text = input;
    setInput("");

    setMessages((prev) => [
      ...prev,
      { role: "user", text },
    ]);

    setLoading(true);

    try {
      const data = await sendMessage(text);

    // show reply text
      setMessages((prev) => [
         ...prev,
         { role: "bot", text: data.reply },
    ]);

    // 🔥 open graph popup if path exists
    if (data.path) {
       setGraphPath(data.path);
    }
    } catch {
      setMessages((prev) => [
        ...prev,
        {
          role: "bot",
          text: "❌ Backend error. Please check FastAPI server.",
          error: true,
        },
      ]);
    } finally {
      setLoading(false);
    }
  };
  

  return (
    <div style={styles.page}>
      <div style={styles.card}>
        {/* Header */}
        <div style={styles.header}>
          <h2 style={styles.title}>🧠 Graph Chat Assistant</h2>
          <span style={styles.badge}>Connected to Neo4j</span>
        </div>

        {/* Messages */}
        <div style={styles.chat}>
          {messages.length === 0 && (
            <div style={styles.empty}>
              Ask things like:
              <ul>
                <li>Who owns payment-service?</li>
                <li>What breaks if redis-main goes down?</li>
                <li>How does api-gateway connect to payments-db?</li>
              </ul>
            </div>
          )}

          {messages.map((m, i) => (
            <div
              key={i}
              style={{
                ...styles.row,
                justifyContent:
                  m.role === "user" ? "flex-end" : "flex-start",
              }}
            >
              <div
                style={{
                  ...styles.bubble,
                  background:
                    m.role === "user"
                      ? "#4f46e5"
                      : m.error
                      ? "#7f1d1d"
                      : "#111827",
                }}
              >
                <span style={styles.icon}>
                  {m.role === "user" ? "👤" : "🤖"}
                </span>
                <span>{m.text}</span>
              </div>
            </div>
          ))}

          {loading && <TypingDots />}

          <div ref={bottomRef} />
        </div>

        {/* Input */}
        <div style={styles.inputRow}>
          <input
            style={styles.input}
            placeholder="Ask a question about your infrastructure..."
            value={input}
            disabled={loading}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
          />
          <button
            style={{
              ...styles.button,
              opacity: loading ? 0.6 : 1,
            }}
            onClick={handleSend}
            disabled={loading}
          >
            Send
          </button>
        </div>
      </div>
      <GraphModal
        path={graphPath}
        onClose={() => setGraphPath(null)}
      />
    </div>
  );


}



const styles = {
  page: {
    minHeight: "100vh",
    background:
      "radial-gradient(circle at top, #020617 20%, #000 70%)",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    fontFamily: "Inter, system-ui, sans-serif",
  },
  card: {
    width: "440px",
    background: "#020617",
    border: "1px solid #1f2937",
    borderRadius: "14px",
    padding: "18px",
    boxShadow: "0 30px 60px rgba(0,0,0,0.5)",
  },
  header: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: "12px",
  },
  title: {
    color: "#fff",
    margin: 0,
  },
  badge: {
    fontSize: "11px",
    color: "#22c55e",
    border: "1px solid #14532d",
    padding: "4px 8px",
    borderRadius: "999px",
  },
  chat: {
    height: "360px",
    overflowY: "auto",
    padding: "10px",
    borderRadius: "10px",
    border: "1px solid #1f2937",
    display: "flex",
    flexDirection: "column",
    gap: "10px",
  },
  empty: {
    fontSize: "13px",
    color: "#9ca3af",
  },
  row: {
    display: "flex",
  },
  bubble: {
    display: "flex",
    gap: "8px",
    padding: "10px 14px",
    borderRadius: "12px",
    maxWidth: "85%",
    fontSize: "14px",
    lineHeight: "1.4",
    color: "#e5e7eb",
  },
  icon: {
    opacity: 0.7,
  },
  thinking: {
    fontSize: "13px",
    color: "#9ca3af",
    fontStyle: "italic",
  },
  inputRow: {
    display: "flex",
    gap: "8px",
    marginTop: "12px",
  },
  input: {
    flex: 1,
    padding: "10px",
    borderRadius: "8px",
    border: "1px solid #1f2937",
    background: "#020617",
    color: "#fff",
  },
  button: {
    padding: "10px 16px",
    borderRadius: "8px",
    border: "none",
    background: "#4f46e5",
    color: "#fff",
    cursor: "pointer",
  },
};
