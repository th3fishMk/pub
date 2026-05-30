import csv
import os
import random
import uuid
from datetime import datetime, timedelta
from typing import TypedDict


# 1. Define Type Structures
class TripRecord(TypedDict):
    employee_id: str
    trip_id: str
    boxes_in_trip: int
    date: str


# 2. Configuration & Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_CSV = os.path.join(BASE_DIR, "..", "data", "employee.csv")
OUTPUT_CSV = os.path.join(BASE_DIR, "..", "data", "employee_trips.csv")

# --- NEW CONFIGURATION FIELDS ---
START_DATE_STR: str = "2026-05-01"
FINISH_DATE_STR: str = "2026-05-31"

BOX_LOWER_BOUND: int = 3  # No trip can have fewer than 3 boxes
BOX_UPPER_BOUND: int = 100  # No trip can have more than 25 boxes


# 3. Helper to assign a consistent "Persona Bias" to an employee
def get_employee_persona(emp_id: str) -> str:
    personas = ["Sprinter", "Hauler", "Average Joe"]
    hash_value = sum(ord(char) for char in emp_id)
    return personas[hash_value % len(personas)]


# 4. Helper to calculate dates between start and finish
def get_date_range(start_str: str, finish_str: str) -> list[str]:
    start_date = datetime.strptime(start_str, "%Y-%m-%d")
    finish_date = datetime.strptime(finish_str, "%Y-%m-%d")

    # Calculate difference in days
    delta = finish_date - start_date
    if delta.days < 0:
        raise ValueError("Finish date cannot be earlier than start date!")

    return [
        (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
        for i in range(delta.days + 1)
    ]


# 5. Core Generator Logic
def generate_productivity_data():
    trip_log: list[TripRecord] = []

    if not os.path.exists(INPUT_CSV):
        print(f"Error: Could not find employee file at: {INPUT_CSV}")
        return

    # Read existing employees
    with open(INPUT_CSV, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        employees = list(reader)

    # Dynamically generate the target timeline
    try:
        date_list = get_date_range(START_DATE_STR, FINISH_DATE_STR)
    except ValueError as e:
        print(e)
        return

    print(
        f"Processing {len(employees)} employees from {START_DATE_STR} to {FINISH_DATE_STR}..."
    )

    for emp in employees:
        emp_id = emp["employee_id"]
        persona = get_employee_persona(emp_id)

        for current_date in date_list:
            # Apply Bias based on Persona
            # Apply Bias based on Persona with WIDE bell curves
            if persona == "Sprinter":
                num_trips = max(1, int(random.gauss(8, 1.5)))
                # Centered at 6, but with a wide spread of 15.0
                avg_boxes = int(random.gauss(6, 15.0))
            elif persona == "Hauler":
                num_trips = max(1, int(random.gauss(3, 0.8)))
                # Centered at 20, but with a massive spread of 25.0
                avg_boxes = int(random.gauss(20, 25.0))
            else:
                # Average Joe
                num_trips = max(1, int(random.gauss(5, 1.2)))
                # Centered at 12, but with a spread of 20.0
                avg_boxes = int(random.gauss(12, 20.0))

            # Generate individual trips
            for _ in range(num_trips):
                # 1. Add normal flight variance around the base target
                raw_boxes = int(random.gauss(avg_boxes, 1.5))

                # 2. ENFORCE BOUNDS: Clip the value to your specific boundaries
                # This keeps the bias generation but cuts off outliers
                bounded_boxes = max(BOX_LOWER_BOUND, min(raw_boxes, BOX_UPPER_BOUND))

                trip_record: TripRecord = {
                    "employee_id": emp_id,
                    "trip_id": str(uuid.uuid4())[:8],
                    "boxes_in_trip": bounded_boxes,
                    "date": current_date,
                }
                trip_log.append(trip_record)

    # 6. Save data
    headers = ["employee_id", "trip_id", "boxes_in_trip", "date"]
    with open(OUTPUT_CSV, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(trip_log)

    print(
        f"Successfully generated {len(trip_log)} records inside boundaries at '{OUTPUT_CSV}'!"
    )


if __name__ == "__main__":
    generate_productivity_data()
