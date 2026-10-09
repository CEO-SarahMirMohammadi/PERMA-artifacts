import TradeCard from "./TradeCard";

const DEFAULT_ENDPOINT = "https://dummyjson.com/products?limit=5";

function normalizeTrade(rawTrade) {
  if (!rawTrade || typeof rawTrade !== "object") {
    return null;
  }

  const priceValue = Number(
    rawTrade.price ?? rawTrade.lastPrice ?? rawTrade.close ?? rawTrade.amount ?? 0
  );

  if (!Number.isFinite(priceValue) || priceValue <= 0) {
    return null;
  }

  const symbol = String(
    rawTrade.symbol ?? rawTrade.ticker ?? rawTrade.asset ?? rawTrade.title ?? "UNKNOWN"
  ).toUpperCase();

  const side = String(
    rawTrade.side ?? rawTrade.tradeType ?? rawTrade.orderSide ?? "buy"
  ).toLowerCase();

  const id = String(
    rawTrade.id ?? rawTrade.tradeId ?? rawTrade.uuid ?? `${symbol}-${Date.now()}`
  );

  const timestamp = rawTrade.timestamp ?? rawTrade.time ?? rawTrade.createdAt ?? new Date().toISOString();

  return {
    id,
    symbol,
    price: priceValue,
    side,
    timestamp: new Date(timestamp).toISOString(),
  };
}

function normalizeTrades(payload) {
  const candidate =
    Array.isArray(payload)
      ? payload
      : Array.isArray(payload?.data)
        ? payload.data
        : Array.isArray(payload?.items)
          ? payload.items
          : Array.isArray(payload?.trades)
            ? payload.trades
            : Array.isArray(payload?.products)
              ? payload.products
              : [];

  if (!candidate.length) {
    return [];
  }

  const normalized = candidate
    .map((trade) => normalizeTrade(trade))
    .filter(Boolean);

  return normalized;
}

async function getTrades() {
  const endpoint = process.env.AZARS_TRADES_URL || DEFAULT_ENDPOINT;
  const response = await fetch(endpoint, { cache: "no-store" });

  if (!response.ok) {
    throw new Error(`Trade fetch failed with status ${response.status}.`);
  }

  const payload = await response.json();
  const normalized = normalizeTrades(payload);

  if (!Array.isArray(normalized) || normalized.length === 0) {
    throw new Error("Trade API returned an unexpected payload shape.");
  }

  return normalized;
}

export default async function TradeListPage() {
  let trades = [];
  let errorMessage = null;

  try {
    trades = await getTrades();
  } catch (error) {
    errorMessage = error.message;
  }

  return (
    <main
      style={{
        maxWidth: "720px",
        margin: "40px auto",
        padding: "24px",
        fontFamily: "Arial, sans-serif",
      }}
    >
      <h1>AZARS Trade List</h1>

      {errorMessage ? (
        <div
          style={{
            border: "1px solid #fecaca",
            borderRadius: "12px",
            backgroundColor: "#fef2f2",
            padding: "16px",
            color: "#991b1b",
          }}
        >
          <strong>Unable to load trade data.</strong>
          <p style={{ margin: "8px 0 0" }}>{errorMessage}</p>
          <p style={{ margin: "8px 0 0" }}>
            Set <code>AZARS_TRADES_URL</code> to the future AZARS API or a trusted public JSON endpoint.
          </p>
        </div>
      ) : (
        <section>
          {trades.map((trade) => (
            <TradeCard key={trade.id} trade={trade} />
          ))}
        </section>
      )}
    </main>
  );
}
