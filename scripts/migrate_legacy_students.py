import sys
import os
import django
from datetime import datetime

# --- Setup Django environment ---
# Ensure the project root is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)

# Set Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "healthapp.settings")

# Setup Django
django.setup()

# --- Import models after setup ---
from core.models import Student, LegacyStudent, School

# --- Helper to parse dates safely ---
def parse_dob(dob_str):
    """Parse a date string into a date object with fallback."""
    if not dob_str:
        return datetime(2000, 1, 1).date()  # default
    for fmt in ("%d/%m/%Y", "%m/%d/%y", "%d-%m-%Y", "%m/%d/%Y"):
        try:
            return datetime.strptime(dob_str, fmt).date()
        except ValueError:
            continue
    return datetime(2000, 1, 1).date()  # fallback

# --- Migration function ---
def migrate_students():
    legacy_qs = LegacyStudent.objects.using('legacy').all()
    total = legacy_qs.count()
    print(f"Found {total} legacy students.")

    for idx, ls in enumerate(legacy_qs, 1):
        # Get or create School instance
        school_obj = None
        if getattr(ls, 'school_name', None):
            school_obj, _ = School.objects.get_or_create(name=ls.school_name)

        # Create Student record
        student, created = Student.objects.get_or_create(
            name=getattr(ls, 'name', "") or "",
            date_of_birth=parse_dob(getattr(ls, 'date_of_birth', None)),
            school=school_obj,
            current_class_section=getattr(ls, 'class_section', "") or "",
            current_teacher=getattr(ls, 'name_teacher', "") or ""
        )

        if created:
            print(f"[{idx}/{total}] Created student: {student.name}")
        else:
            print(f"[{idx}/{total}] Already exists: {student.name}")

if __name__ == "__main__":
    migrate_students()
    print("Migration complete.")
