"""19 Advanced: Composed business workflow tools."""

from datetime import datetime

from _compat import MCPServer

mcp = MCPServer("server-19-composed-workflow")

_inventory = {"A-100": 5, "B-200": 0, "C-300": 12}
_orders: dict[str, dict] = {}


@mcp.tool()
def check_inventory(sku: str) -> dict:
    return {"sku": sku, "available": _inventory.get(sku, 0)}


@mcp.tool()
def create_order(order_id: str, sku: str, qty: int) -> dict:
    if qty <= 0:
        raise ValueError("Quantity must be positive.")
    available = _inventory.get(sku, 0)
    if available < qty:
        raise ValueError("Not enough inventory.")
    _inventory[sku] = available - qty
    order = {
        "order_id": order_id,
        "sku": sku,
        "qty": qty,
        "status": "created",
        "created_at": datetime.utcnow().isoformat() + "Z",
    }
    _orders[order_id] = order
    return order


@mcp.tool()
def cancel_order(order_id: str) -> dict:
    if order_id not in _orders:
        raise ValueError("Order not found.")
    order = _orders[order_id]
    if order["status"] == "cancelled":
        return order
    _inventory[order["sku"]] = _inventory.get(order["sku"], 0) + order["qty"]
    order["status"] = "cancelled"
    return order


@mcp.tool()
def get_order(order_id: str) -> dict:
    if order_id not in _orders:
        raise ValueError("Order not found.")
    return _orders[order_id]


if __name__ == "__main__":
    mcp.run(transport="stdio")

