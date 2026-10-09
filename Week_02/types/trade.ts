export interface ITrade {
    symbol: string;
    price: number;
    quantity: number;
    timestamp: number;
    side: "BUY" | "SELL";
}