"""Food delivery order queue manager.

Creates orders from a menu, moves them through delivery statuses,
totals the day's revenue and backs the queue up to disk as JSON.
"""
import json
from datetime import datetime

orders = {}
menu = {}
VALID_STATUSES = ["placed", "cooking", "out_for_delivery", "delivered"]
DEFAULT_MENU = {"pizza": 250, "burger": 150, "fries": 90, "coke": 40}


def create_order(customer, items, order_history=None):
    """Create an order and return its ID.

    Raises ValueError if the customer is empty, there are no items,
    or an item is not on the menu.
    """
    if order_history is None:
        order_history = []
    if not customer:
        raise ValueError("Customer name is required")
    if not items:
        raise ValueError("Order must contain at least one item")
    unknown = [item for item in items if item not in menu]
    if unknown:
        raise ValueError(f"Not on the menu: {', '.join(unknown)}")
    total = sum(menu[item] for item in items)
    order_id = max(orders, default=0) + 1
    orders[order_id] = {
        "customer": customer,
        "items": items,
        "total": total,
        "status": "placed",
    }
    order_history.append(order_id)
    return order_id


def update_order_status(order_id, status):
    """Set the status of an existing order.

    Raises ValueError if the status is not one of VALID_STATUSES.
    """
    if status not in VALID_STATUSES:
        raise ValueError(f"Invalid status: {status}")
    try:
        orders[order_id]["status"] = status
    except KeyError:
        print(f"Order {order_id} not found")


def read_menu_config(file="menu.json"):
    """Load the menu from a JSON file, falling back to the default menu."""
    menu.clear()
    try:
        with open(file, encoding="utf-8") as handle:
            menu.update(json.load(handle))
    except (FileNotFoundError, json.JSONDecodeError):
        menu.update(DEFAULT_MENU)


def daily_revenue():
    """Return the total value of delivered orders."""
    return sum(
        o["total"] for o in orders.values() if o["status"] == "delivered"
        )


def backup_orders(file="orders.json"):
    """Save all orders to a JSON file."""
    with open(file, "w", encoding="utf-8") as handle:
        json.dump(orders, handle)


def restore_orders(file="orders.json"):
    """Replace the current orders with those saved by backup_orders."""
    with open(file, encoding="utf-8") as handle:
        saved = json.load(handle)
    orders.clear()
    orders.update({int(key): value for key, value in saved.items()})


def print_queue():
    """Print every order in the queue."""
    print(f"Order queue at {datetime.now()}")
    for order_id, order in orders.items():
        print(order_id, order["customer"], order["status"], order["total"])


def main():
    """Run a short demo of the order queue."""
    read_menu_config()
    asha = create_order("Asha", ["pizza", "coke"])
    ravi = create_order("Ravi", ["burger", "fries"])
    for customer, items in [("Ravi", ["burger", "sushi"]), ("", [])]:
        try:
            create_order(customer, items)
        except ValueError as err:
            print(f"Order rejected: {err}")
    update_order_status(asha, "delivered")
    update_order_status(ravi, "out_for_delivery")
    try:
        update_order_status(ravi, "teleported")
    except ValueError as err:
        print(f"Update rejected: {err}")
    update_order_status(42, "delivered")
    print("Revenue today:", daily_revenue())
    backup_orders()
    restore_orders()
    print_queue()


if __name__ == "__main__":
    main()
