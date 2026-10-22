
# SurgeGuard-Agent
# Fictional hospital inventory demo only.

inventory = {
    "surgical gloves": 20,
    "gauze packs": 12,
    "general supply kits": 5
}

def check_inventory(item, requested_quantity):
    item = item.lower()

    if item not in inventory:
        return f"Item '{item}' was not found in the demo inventory."

    available = inventory[item]

    print("Item:", item)
    print("Available stock:", available)
    print("Requested quantity:", requested_quantity)

    if available < requested_quantity:
        return (
            f"LOW STOCK: Only {available} available. "
            "Prepare a request for human approval."
        )

    return "STOCK AVAILABLE: Request can be reviewed."


# Test with fictional data
result = check_inventory("general supply kits", 8)
print("Result:", result)
