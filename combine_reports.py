
import csv

simulation_file = "SurgeGuard_Simulation_Report.csv"
security_file = "SurgeGuard_Security_Evaluation.csv"
output_file = "SurgeGuard_Combined_Evaluation.csv"

combined_rows = []

# Read healthcare simulation results
with open(simulation_file, "r", encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        combined_row = {
            "Evaluation Type": "Healthcare Simulation",
            **row
        }
        combined_rows.append(combined_row)

# Read security evaluation results
with open(security_file, "r", encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        combined_row = {
            "Evaluation Type": "Security Evaluation",
            **row
        }
        combined_rows.append(combined_row)

# Preserve all columns from both original CSV files
fieldnames = []

for row in combined_rows:
    for column in row:
        if column not in fieldnames:
            fieldnames.append(column)

# Generate combined CSV
with open(output_file, "w", encoding="utf-8-sig", newline="") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=fieldnames,
        extrasaction="ignore"
    )

    writer.writeheader()
    writer.writerows(combined_rows)

simulation_count = sum(
    row["Evaluation Type"] == "Healthcare Simulation"
    for row in combined_rows
)

security_count = sum(
    row["Evaluation Type"] == "Security Evaluation"
    for row in combined_rows
)

print("SURGEGUARD COMBINED EVALUATION")
print("-----------------------------")
print(f"Healthcare simulation records: {simulation_count}")
print(f"Security evaluation records: {security_count}")
print(f"Total records: {len(combined_rows)}")
print(f"CSV saved: {output_file}")
