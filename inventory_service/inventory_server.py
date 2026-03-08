"""
CS 4459: Assignment 3 — Inventory Service
Manages the shared inventory database.

Provided endpoints: GET /inventory/available, GET /inventory/summary, GET /access-log
You implement:      POST /process-order (with idempotency)
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from helpers import get_db_connection

app = FastAPI()


# --- Request/Response Models ---

class OrderRequest(BaseModel):
    worker_id: int
    item_id: int
    idempotency_key: str


# ============================================================
#  PROVIDED ENDPOINTS — DO NOT MODIFY
# ============================================================

@app.get("/inventory/available")
def get_available():
    """Returns items currently available for purchase."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT item_id, item_name, quantity FROM inventory WHERE status = 'available' ORDER BY item_id"
    )
    rows = cursor.fetchall()
    conn.close()

    items = [{"item_id": r[0], "item_name": r[1], "quantity": r[2]} for r in rows]
    return {"items": items, "count": len(items)}


@app.get("/inventory/summary")
def get_summary():
    """Returns an overview of inventory state."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM inventory")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM inventory WHERE status = 'available'")
    available = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM inventory WHERE status = 'sold_out'")
    sold = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM order_history")
    orders = cursor.fetchone()[0]

    conn.close()

    return {
        "total_items": total,
        "available": available,
        "sold": sold,
        "orders_processed": orders,
    }


@app.get("/access-log")
def get_access_log():
    """Returns the access audit log for mutual exclusion verification."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT log_id, worker_id, action, timestamp FROM access_log ORDER BY log_id"
    )
    rows = cursor.fetchall()
    conn.close()

    entries = [
        {
            "log_id": r[0],
            "worker_id": r[1],
            "action": r[2],
            "timestamp": r[3].isoformat() if r[3] else None,
        }
        for r in rows
    ]
    return {"entries": entries, "count": len(entries)}


# ============================================================
#  TODO: Implement POST /process-order
# ============================================================
#
# This endpoint must:
#   1. Log entry — Write to access_log with action 'enter'
#      Enter and Exit events must be logged using the following SQL:
#    # "INSERT INTO access_log (worker_id, action) VALUES (%s, 'enter')",
#    #     (order.worker_id,)
#       # "INSERT INTO access_log (worker_id, action) VALUES (%s, 'exit')",
#                # (order.worker_id,)  
#   2. Check idempotency — If idempotency_key already exists in
#      order_history, return the original result with "duplicate": true
#   3. Validate — Check the item exists and is available
#   4. Process — Update inventory and insert into order_history
#   5. Log exit — Write to access_log with action 'exit'

               
#
# See the assignment specification for exact response formats.

@app.post("/process-order")
def process_order(order: OrderRequest):
    # TODO: Implement idempotent order processing
    raise HTTPException(status_code=501, detail="Not implemented")