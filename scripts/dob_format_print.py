#!/usr/bin/env python
import os
import sys
import django

# --- Setup Django environment ---
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "healthapp.settings.dev")
django.setup()

from core.models import Student

def check_dob_format():
    students = Student.objects.all()
    total = students.count()
    missing_dob = 0
    malformed_dob = 0

    for student in students:
        dob = getattr(student, "date_of_birth", None)
        if not dob:
            missing_dob += 1
            print(f"[MISSING] {student.name} -> DOB: {dob}")
        else:
            try:
                iso_dob = dob.isoformat()
            except Exception:
                malformed_dob += 1
                print(f"[MALFORMED] {student.name} -> DOB: {dob}")

    print(f"\nTotal students: {total}")
    print(f"Missing DOBs: {missing_dob}")
    print(f"Malformed DOBs: {malformed_dob}")

if __name__ == "__main__":
    check_dob_format()
