import csv
import random
import uuid
from datetime import datetime, timedelta

type num = int | float
amount_of_people_to_create: int = 60
age_lower_bound: int = 18
age_upper_bound: int = 60
male_names: list[str] = ["James", "John", "Robert", "Michael", "William"]
female_names: list[str] = ["Mary", "Patricia", "Jennifer", "Linda", "Elizabeth"]
last_names: list[str] = ["Smith", "Johnson", "Williams", "Brown", "Jones"]
job_titles: list[str] = [
    "Filler",
]
# Added the pool of possible areas
possible_areas: list[int] = [10, 20, 30, 40, 50, 60, 70, 80, 90]


class Employee:
    employee_id: str
    name: str
    last_name: str
    gender: str
    age: int
    job_title: str
    hire_date: str
    area: int  # <-- Added area attribute type

    def __init__(
        self,
        emp_id: str,
        name: str,
        last_name: str,
        gender: str,
        age: int,
        job_title: str,
        hire_date: str,
        area: int,  # <-- Added area to constructor
    ) -> None:
        self.employee_id = emp_id
        self.name = name
        self.last_name = last_name
        self.gender = gender
        self.age = age
        self.job_title = job_title
        self.hire_date = hire_date
        self.area = area  # <-- Assigned area to self


def create_employee() -> Employee:
    if random.choice([True, False]):
        chosen_name = random.choice(male_names)
        chosen_gender = "Male"
    else:
        chosen_name = random.choice(female_names)
        chosen_gender = "Female"

    random_id: str = str(uuid.uuid4())[:8]
    chosen_last_name: str = random.choice(last_names)
    random_age: int = random.randint(age_lower_bound, age_upper_bound)
    chosen_title: str = random.choice(job_titles)
    random_days_ago: int = random.randint(0, 365 * 5)
    random_date: datetime = datetime.now() - timedelta(days=random_days_ago)
    formatted_hire_date: str = random_date.strftime("%Y-%m-%d")

    # Pick a random area from the allowed list
    chosen_area: int = random.choice(possible_areas)

    return Employee(
        emp_id=random_id,
        name=chosen_name,
        last_name=chosen_last_name,
        gender=chosen_gender,
        age=random_age,
        job_title=chosen_title,
        hire_date=formatted_hire_date,
        area=chosen_area,  # <-- Passed area here
    )


employee_directory: list[Employee] = []
for _ in range(amount_of_people_to_create):
    new_emp = create_employee()
    employee_directory.append(new_emp)
for i, employee in enumerate(employee_directory, start=1):
    print(f"=== Employee #{i} ===")
    print(f"ID:         {employee.employee_id}")
    print(f"Full Name:  {employee.name} {employee.last_name}")
    print(f"Age:        {employee.age}")
    print(f"Job Title:  {employee.job_title}")
    print(f"Hire Date:  {employee.hire_date}")
    print("-" * 25)
csv_filename: str = "data/employee.csv"
headers: list[str] = [
    "employee_id",
    "name",
    "last_name",
    "gender",
    "age",
    "job_title",
    "hire_date",
    "area",
]
with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writeheader()
    for employee in employee_directory:
        writer.writerow(employee.__dict__)
print(f"Successfully saved {len(employee_directory)} employees to '{csv_filename}'!")
