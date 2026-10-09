
/**
 * Display a single trade.
 *
 * @param {{symbol: string, price: number, side: string, timestamp: string}} props
 * @returns {JSX.Element}
 */
const TradeCard = ({ symbol, price, side, timestamp }) => {
  const normalizedSide = side.toUpperCase();
  const isBuy = normalizedSide === "BUY";

  const formattedPrice = new Intl.NumberFormat("en-US", {
    style: "decimal",
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(price);

  return (
    <article
      style={{
        border: "1px solid #d1d5db",
        borderRadius: "12px",
        padding: "16px",
        maxWidth: "320px",
        fontFamily: "Arial, sans-serif",
      }}
    >
      <header
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        <h2 style={{ margin: 0 }}>{symbol}</h2>

        <span
          style={{
            fontWeight: 700,
            color: isBuy ? "#15803d" : "#b91c1c",
          }}
        >
          {normalizedSide}
        </span>
      </header>

      <p style={{ fontSize: "24px", fontWeight: 700 }}>
        ${formattedPrice}
      </p>

      <p style={{ fontSize: "13px", color: "#6b7280" }}>
        Timestamp: {timestamp}
      </p>
    </article>
  );
};

export default TradeCard;