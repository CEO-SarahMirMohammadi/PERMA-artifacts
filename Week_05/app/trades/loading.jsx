export default function LoadingTradeList() {
  return (
    <main
      style={{
        maxWidth: "720px",
        margin: "40px auto",
        padding: "24px",
        fontFamily: "Arial, sans-serif",
      }}
    >
      <h1>Loading trades...</h1>
      <div
        style={{
          border: "1px solid #e5e7eb",
          borderRadius: "12px",
          padding: "16px",
          backgroundColor: "#f9fafb",
        }}
      >
        Fetching the latest trade data from the configured endpoint.
      </div>
    </main>
  );
}
