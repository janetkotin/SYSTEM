# ============================================
# SAMSS - Student Academic Monitoring System
# IST1025 Coursework Implementation
# ============================================

import json
import os
from datetime import datetime

# ============================================
# DATA MODEL (Structured Class)
# ============================================

class Student:
    """Student structured data model"""

    def __init__(self, student_id, name, program):
        self.id = student_id
        self.name = name
        self.program = program
        self.units = []              # List of unit dictionaries
        self.fees = {"total": 0, "paid": 0, "balance": 0}
        self.registration_date = datetime.now().strftime("%Y-%m-%d")

    def to_dict(self):
        """Convert object to dictionary for JSON storage"""
        return {
            "id": self.id,
            "name": self.name,
            "program": self.program,
            "units": self.units,
            "fees": self.fees,
            "registration_date": self.registration_date
        }

    @classmethod
    def from_dict(cls, data):
        """Recreate object from dictionary"""
        student = cls(data["id"], data["name"], data["program"])
        student.units = data.get("units", [])
        student.fees = data.get("fees", {"total": 0, "paid": 0, "balance": 0})
        student.registration_date = data.get("registration_date", "")
        return student


# ============================================
# FILE HANDLING MODULE
# ============================================

DATA_FILE = "student_records.json"

def load_students():
    """Load students from file"""
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            return {sid: Student.from_dict(sdata) for sid, sdata in data.items()}
    except:
        return {}

def save_students(students):
    """Save students to file"""
    with open(DATA_FILE, "w") as f:
        data = {sid: student.to_dict() for sid, student in students.items()}
        json.dump(data, f, indent=4)


# ============================================
# VALIDATION UTILITIES
# ============================================

def validate_non_empty(value, field):
    if value.strip():
        return True, value.strip()
    return False, f"{field} cannot be empty"

def validate_score(score):
    try:
        score = float(score)
        if 0 <= score <= 100:
            return True, score
        return False, "Score must be 0-100"
    except:
        return False, "Invalid number"


# ============================================
# FUNCTION 1: REGISTRATION
# ============================================

def register_student(students):
    print("\n--- Student Registration ---")

    while True:
        sid = input("Student ID (e.g., IST/2024/001): ").strip().upper()
        valid, msg = validate_non_empty(sid, "Student ID")
        if not valid:
            print(msg)
            continue
        if sid in students:
            print("Student ID already exists!")
            continue
        break

    while True:
        name = input("Full Name: ")
        valid, msg = validate_non_empty(name, "Name")
        if valid:
            break
        print(msg)

    program = input("Program (default BSc IT): ").strip() or "BSc IT"

    students[sid] = Student(sid, name, program)
    print("✓ Student registered successfully!")
    return students


# ============================================
# FUNCTION 2: ADD UNIT SCORES
# ============================================

def add_unit_scores(students):
    print("\n--- Add Unit Scores ---")

    sid = input("Enter Student ID: ").strip().upper()
    if sid not in students:
        print("Student not found!")
        return students

    student = students[sid]

    while True:
        unit_code = input("Unit Code (blank to finish): ").strip().upper()
        if not unit_code:
            break

        unit_name = input("Unit Name: ").strip()

        while True:
            score_input = input("Score (0-100): ")
            valid, result = validate_score(score_input)
            if valid:
                score = result
                break
            print(result)

        student.units.append({
            "code": unit_code,
            "name": unit_name,
            "score": score
        })

        print(f"✓ {unit_code} added")

    return students


# ============================================
# ACADEMIC CALCULATIONS
# ============================================

def compute_average(units):
    if not units:
        return 0
    return sum(u["score"] for u in units) / len(units)

def classify_grade(avg):
    if avg >= 70:
        return "A"
    elif avg >= 60:
        return "B"
    elif avg >= 50:
        return "C"
    elif avg >= 40:
        return "D"
    else:
        return "F"

def assess_risk(avg):
    if avg >= 60:
        return "Low"
    elif avg >= 45:
        return "Moderate"
    else:
        return "High"


# ============================================
# FUNCTION 3: MANAGE FEES
# ============================================

def manage_fees(students):
    print("\n--- Fee Management ---")

    sid = input("Enter Student ID: ").strip().upper()
    if sid not in students:
        print("Student not found!")
        return students

    student = students[sid]

    try:
        total = float(input("Total Fees (KES): ") or 0)
        paid = float(input("Amount Paid (KES): ") or 0)

        if paid > total:
            print("Paid cannot exceed total.")
            return students

        student.fees = {
            "total": total,
            "paid": paid,
            "balance": total - paid
        }

        print("✓ Fees updated")

    except:
        print("Invalid number entered")

    return students


# ============================================
# FUNCTION 4: GENERATE STUDENT REPORT
# ============================================

def generate_report(students):
    print("\n--- Student Report ---")

    sid = input("Enter Student ID: ").strip().upper()
    if sid not in students:
        print("Student not found!")
        return

    student = students[sid]
    avg = compute_average(student.units)
    grade = classify_grade(avg)
    risk = assess_risk(avg)

    print("\n================================")
    print(f"Name: {student.name}")
    print(f"Program: {student.program}")
    print("--------------------------------")
    print("Units:")

    for unit in student.units:
        print(f"{unit['code']} - {unit['score']}%")

    print("--------------------------------")
    print(f"Average: {avg:.2f}%")
    print(f"Grade: {grade}")
    print(f"Risk Level: {risk}")
    print("================================")


# ============================================
# FUNCTION 5: CLASS SUMMARY
# ============================================

def class_summary(students):
    print("\n--- Class Summary ---")

    if not students:
        print("No students registered.")
        return

    for sid, student in students.items():
        avg = compute_average(student.units)
        risk = assess_risk(avg)
        print(f"{sid} | {student.name} | Avg: {avg:.1f}% | Risk: {risk}")


# ============================================
# MENU SYSTEM
# ============================================

def display_menu():
    print("\n========== SAMSS ==========")
    print("1. Register Student")
    print("2. Add Unit Scores")
    print("3. Manage Fees")
    print("4. Generate Student Report")
    print("5. Class Summary")
    print("6. Save & Exit")
    print("===========================")

def main():
    students = load_students()
    print(f"Loaded {len(students)} records.")

    while True:
        display_menu()
        choice = input("Select option (1-6): ")

        if choice == "1":
            students = register_student(students)
        elif choice == "2":
            students = add_unit_scores(students)
        elif choice == "3":
            students = manage_fees(students)
        elif choice == "4":
            generate_report(students)
        elif choice == "5":
            class_summary(students)
        elif choice == "6":
            save_students(students)
            print("Data saved. Goodbye!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
