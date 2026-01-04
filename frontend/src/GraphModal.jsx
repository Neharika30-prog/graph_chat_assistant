export default function GraphModal({ path, onClose }) {
  if (!path) return null;

  return (
    <div style={styles.overlay}>
      <div style={styles.modal}>
        <h3>📊 Graph Path</h3>

        <div style={styles.graph}>
          {path.map((node, i) => (
            <div key={i} style={styles.node}>
              {node}
              {i < path.length - 1 && <span style={styles.arrow}>→</span>}
            </div>
          ))}
        </div>

        <button style={styles.close} onClick={onClose}>
          Close
        </button>
      </div>
    </div>
  );
}

const styles = {
  overlay: {
    position: "fixed",
    inset: 0,
    background: "rgba(0,0,0,0.6)",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    zIndex: 50,
  },
  modal: {
    background: "#020617",
    border: "1px solid #1f2937",
    borderRadius: "12px",
    padding: "20px",
    width: "400px",
    color: "#fff",
  },
  graph: {
    display: "flex",
    flexWrap: "wrap",
    gap: "8px",
    margin: "16px 0",
    fontSize: "14px",
  },
  node: {
    background: "#111827",
    padding: "6px 10px",
    borderRadius: "6px",
  },
  arrow: {
    margin: "0 6px",
    color: "#6366f1",
  },
  close: {
    marginTop: "10px",
    padding: "8px 12px",
    background: "#4f46e5",
    border: "none",
    color: "#fff",
    borderRadius: "6px",
    cursor: "pointer",
  },
};