export default function TypingDots() {
  return (
    <div style={styles.container}>
      <span>🤖</span>
      <span style={styles.dot}>.</span>
      <span style={{ ...styles.dot, animationDelay: "0.2s" }}>.</span>
      <span style={{ ...styles.dot, animationDelay: "0.4s" }}>.</span>
    </div>
  );
}

const styles = {
  container: {
    display: "flex",
    alignItems: "center",
    gap: "4px",
    color: "#9ca3af",
    fontSize: "14px",
  },
  dot: {
    animation: "blink 1.4s infinite both",
  },
};