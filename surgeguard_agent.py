
# SurgeGuard-Agent
# Integrated software demo using fictional data only.

from risk_checker import check_simulated_risk
from inventory_checker import check_inventory


def run_surgeguard_demo():
    print("\n=== SURGEGUARD-AGENT DEMO ===")

    # Example simulated sensor information
    movement = 6
    sensor = "normal"

    risk_result = check_simulated_risk(movement, sensor)

    print("\n1. SIMULATED RISK CHECK")
    print("Result:", risk_result)

    # Example fictional inventory request
    print("\n2. MOCK INVENTORY CHECK")
    inventory_result = check_inventory("general supply kits", 8)

    print("Result:", inventory_result)

    print("\n3. PROPOSED ACTION")
    if "REVIEW ALERT" in risk_result or "LOW STOCK" in inventory_result:
        print("Flag for human review. No automatic action taken.")
    else:
        print("No demo rule triggered.")


if __name__ == "__main__":
    run_surgeguard_demo()
