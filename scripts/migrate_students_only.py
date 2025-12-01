#!/usr/bin/env python
import sys
import os
import django
from datetime import datetime

# --- Setup Django environment ---
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "healthapp.settings.dev")
django.setup()

from core.models import Student, LegacyStudent, School

# ----------------- Helper Functions -----------------

def parse_date(date_str):
    """Try multiple date formats safely. Return placeholder if missing or invalid."""
    if not date_str:
        # Placeholder for missing DOB
        return datetime(2000, 1, 1).date()
    for fmt in ("%d/%m/%Y", "%d-%m-%Y", "%Y-%m-%d", "%m/%d/%Y", "%m/%d/%y"):
        try:
            return datetime.strptime(str(date_str), fmt).date()
        except (ValueError, TypeError):
            continue
    # Fallback placeholder date if all parsing fails
    return datetime(2000, 1, 1).date()

def safe_attr(obj, field):
    """Safe fetch from flexible LegacyStudent model."""
    return getattr(obj, field, None)

# ----------------- Migration Script -----------------

def migrate_students_only():
    legacy_students = LegacyStudent.objects.all()
    total = legacy_students.count()
    print(f"Found {total} legacy students.\n")

    if total == 0:
        print("No legacy students found.")
        return

    created_count = 0

    for idx, ls in enumerate(legacy_students, 1):
        # ----------------- School -----------------
        school_name = safe_attr(ls, "school_name")
        school_obj = None
        if school_name:
            school_obj, _ = School.objects.get_or_create(name=school_name.strip())

        # ----------------- Student -----------------
        dob = parse_date(safe_attr(ls, "date_of_birth"))

        student = Student.objects.create(
            name=safe_attr(ls, "name") or "Unnamed",
            date_of_birth=dob,
            gender=safe_attr(ls, "gender"),
            father_or_guardian_name=safe_attr(ls, "father_or_guardian_name"),
            mother_name=safe_attr(ls, "mother_name"),
            contact_number=str(safe_attr(ls, "contact_number") or ""),
            address=safe_attr(ls, "address"),
            known_earlier_disease=safe_attr(ls, "known_earlier_disease"),
            school=school_obj
        )
        created_count += 1

        # Flag placeholder DOBs
        if dob == datetime(2000, 1, 1).date():
            print(f"[{idx}/{total}] Placeholder DOB used for {student.name}")
        else:
            print(f"[{idx}/{total}] Created: {student.name}")

    print(f"\nStudent migration complete! Total students created: {created_count}")

if __name__ == "__main__":
    migrate_students_only()
