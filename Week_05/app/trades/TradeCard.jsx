export default function TradeCard({ trade }) {
  return (
    <article
      style={{
        border: "1px solid #d1d5db",
        borderRadius: "12px",
        padding: "16px",
        marginBottom: "12px",
        backgroundColor: "#ffffff",
      }}
    >
      <div style={{ display: "flex", justifyContent: "space-between", gap: "12px" }}>
        <strong>{trade.symbol}</strong>
        <span
          style={{
            padding: "4px 8px",
            borderRadius: "999px",
            backgroundColor: trade.side === "buy" ? "#dcfce7" : "#fee2e2",
            color: trade.side === "buy" ? "#166534" : "#991b1b",
            textTransform: "uppercase",
            fontSize: "12px",
            fontWeight: 700,
          }}
        >
          {trade.side}
        </span>
      </div>

      <p style={{ margin: "10px 0 4px" }}>
        Price: <strong>{Number(trade.price).toFixed(2)}</strong>
      </p>
      <p style={{ margin: "4px 0" }}>ID: {trade.id}</p>
      <p style={{ margin: "4px 0 0" }}>
        Timestamp: {new Date(trade.timestamp).toISOString()}
      </p>
    </article>
  );
}
