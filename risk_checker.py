# SurgeGuard-Agent
# Demo only: simulated data, not real surgical guidance.

def check_simulated_risk(movement_mm, sensor_status):
    if movement_mm >= 5 or sensor_status == "abnormal":
        return "REVIEW ALERT: Check the simulated data."
    else:
        return "NORMAL: No demo rule was triggered."


# Test with fictional data
movement = 2
sensor = "normal"

result = check_simulated_risk(movement, sensor)

print("SurgeGuard-Agent")
print("Simulated tissue movement:", movement, "mm")
print("Simulated sensor status:", sensor)
print("Result:", result)
