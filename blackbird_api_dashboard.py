
from fastapi import FastAPI
from mirror_identity_registry import router as identity_router
from sarcard_mirror_engine import router as card_router
from sovereign_ledger_engine import router as ledger_router, record_transaction
from senticore_gateway_api import router as gateway_router

# Ledger Memory Storage
sovereign_ledger = {}
ledger_log = []

# Init App
app = FastAPI(title="Sovereign Mirror Stack API")

# Include all Sovereign Routers
app.include_router(identity_router)
app.include_router(card_router)
app.include_router(ledger_router)
app.include_router(gateway_router)

# Webhook Handler
@app.post("/gateway/webhook")
async def handle_webhook(payload: dict):
    print("🔔 Webhook Received:", payload)

    event_type = payload.get("event_type", "unknown")
    event_data = payload.get("data", {})

    sovereign_log = {
        "status": "webhook received",
        "event": event_type,
        "payload": event_data,
        "triggered": []
    }

    # Triggered Hooks
    if event_type in ["payment.created", "payment.confirmed"]:
        sovereign_log["triggered"].append("💳 Sovereign Credit Injection")

    if event_type in ["transfer.created", "transfer.settled"]:
        sovereign_log["triggered"].append("🏛️ Sovereign Ledger Mirror")

    if event_type == "dispute.initiated":
        sovereign_log["triggered"].append("⚖️ Sovereign Lien System")

    return sovereign_log

# Sovereign Credit Movement API
@app.post("/move-credit")
async def move_credit(from_card_id: str, to_card_id: str, amount: float):
    # 1. Subtract from origin
    from_card = sovereign_ledger.get(from_card_id, {"balance": 0})
    if from_card["balance"] < amount:
        return {"status": "failed", "reason": "Insufficient balance"}

    from_card["balance"] -= amount
    sovereign_ledger[from_card_id] = from_card

    # 2. Add to destination
    to_card = sovereign_ledger.get(to_card_id, {"balance": 0})
    to_card["balance"] += amount
    sovereign_ledger[to_card_id] = to_card

    # 3. Record transaction in ledger
    ledger_log.append({
        "type": "credit_transfer",
        "from": from_card_id,
        "to": to_card_id,
        "amount": amount,
        "timestamp": datetime.utcnow().isoformat()
    })

    # 4. Inject into sovereign ledger
    record_transaction(card_id=from_card_id, amount=amount, description="credit moved out")
    record_transaction(card_id=to_card_id, amount=amount, description="credit received")

    return {
        "status": "success",
        "from": from_card_id,
        "to": to_card_id,
        "amount": amount
    }
