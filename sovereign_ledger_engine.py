# sovereign_ledger_engine.py
# Ledger system for recording and retrieving transactions

from fastapi import APIRouter
from typing import List, Dict

router = APIRouter()

# ⬇️ Transaction history
ledger: List[Dict] = []

# ⬇️ Sovereign Credit Ledger System (Live Balances + Limits)
sovereign_ledger: Dict[str, Dict] = {
    "SARCARD-86524f": {
        "balance": 999999999,
        "credit_limit": 200000000,
        "transactions": []
    },
    "SARCARD-SOV2288": {
        "balance": 0,
        "credit_limit": 100000000,
        "transactions": []
    }
}

# ⬇️ Record a transaction into the ledger
@router.post("/record-transaction")
def record_transaction(card_id: str, amount: float, description: str):
    tx = {
        "card_id": card_id,
        "amount": amount,
        "description": description
    }

    # 🔄 Append to master ledger
    ledger.append(tx)

    # 📌 Also append to individual card history (if card exists)
    if card_id in sovereign_ledger:
        sovereign_ledger[card_id]["transactions"].append(tx)

    return tx

# ⬇️ View all transactions
@router.get("/transactions")
def get_transactions():
    return ledger

# ⬇️ View balances of all cards
@router.get("/balances")
def get_balances():
    return sovereign_ledger

# ⬇️ Export variables for other files
__all__ = ["router", "ledger", "sovereign_ledger"]
