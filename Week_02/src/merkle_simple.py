from __future__ import annotations

import hashlib


def sha256(data: str) -> str:
    """Return the SHA-256 hexadecimal digest of a string."""
    return hashlib.sha256(
        data.encode("utf-8")
    ).hexdigest()


def build_merkle_root(transactions: list[str]) -> str:
    """
    Build a simple binary Merkle Tree and return its root hash.

    This Week 2 implementation intentionally supports
    exactly four transactions.
    """

    if len(transactions) != 4:
        raise ValueError(
            "This Week 2 implementation requires exactly 4 transactions."
        )

    level = [
        sha256(transaction)
        for transaction in transactions
    ]

    while len(level) > 1:
        next_level = []

        for i in range(0, len(level), 2):
            combined = level[i] + level[i + 1]
            parent = sha256(combined)
            next_level.append(parent)

        level = next_level

    return level[0]


if __name__ == "__main__":
    transactions = [
        "tx1: BUY AAPL 10",
        "tx2: SELL MSFT 5",
        "tx3: BUY NVDA 8",
        "tx4: BUY TSLA 3",
    ]

    root = build_merkle_root(transactions)

    print("Merkle Root:")
    print(root)

    with open("merkle_root.txt", "w", encoding="utf-8") as file:
        file.write(root)

    modified_transactions = transactions.copy()
    modified_transactions[2] = "tx3: SELL NVDA 8"

    modified_root = build_merkle_root(
        modified_transactions
    )

    print("\nOriginal Root:")
    print(root)

    print("\nModified Root:")
    print(modified_root)

    print("\nRoot changed:", root != modified_root)