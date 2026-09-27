from app.db import query


def invoice(order_id):
    rows = query("SELECT total, legacy_id FROM orders WHERE id = ?", order_id)
    return {"order": order_id, "amount": rows[0]["total"]}
