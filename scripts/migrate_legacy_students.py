import sys
import os
import django
from datetime import datetime

# --- Setup Django environment ---
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "healthapp.settings.dev")
django.setup()

from core.models import Student, LegacyStudent, School, Screening, ScreeningCheck

# ----------------- Helper Functions -----------------

def parse_date(date_str):
    """Try multiple date formats safely."""
    if not date_str:
        return None
    for fmt in ("%d/%m/%Y", "%d-%m-%Y", "%Y-%m-%d", "%m/%d/%Y", "%m/%d/%y"):
        try:
            return datetime.strptime(str(date_str), fmt).date()
        except (ValueError, TypeError):
            continue
    return None

def to_bool(value):
    """Convert '1', 'yes', 'true' → True."""
    if value is None:
        return False
    return str(value).strip().lower() in ["1", "true", "yes", "y"]

def safe_attr(obj, field):
    """Safe fetch from flexible LegacyStudent model."""
    return getattr(obj, field, None)

# ----------------- Migration Script -----------------

def migrate_students():
    legacy_qs = LegacyStudent.objects.using('legacy').all()
    total = legacy_qs.count()
    print(f"Found {total} legacy students.")

    if total == 0:
        print("No legacy students found.")
        return

    # ----- CLEAN DEV DB -----
    print("Clearing dev DB Student-related tables...")
    ScreeningCheck.objects.all().delete()
    Screening.objects.all().delete()
    Student.objects.all().delete()

    created_count = 0

    # All fields except id + screening foreign key
    valid_screeningcheck_fields = [
        f.name for f in ScreeningCheck._meta.get_fields()
        if f.concrete and f.name not in ("id", "screening")
    ]

    for idx, ls in enumerate(legacy_qs, 1):

        # ----------------- School -----------------
        school_name = safe_attr(ls, "school_name")
        school_obj = None
        if school_name:
            school_obj, _ = School.objects.get_or_create(name=school_name)

        # ----------------- Student -----------------
        dob = parse_date(safe_attr(ls, "date_of_birth")) or datetime(2000, 1, 1).date()

        student = Student.objects.create(
            name=safe_attr(ls, "name") or "",
            date_of_birth=dob,
            school=school_obj,
            gender=safe_attr(ls, "gender"),
            father_or_guardian_name=safe_attr(ls, "father_or_guardian_name"),
            mother_name=safe_attr(ls, "mother_name"),
            contact_number=str(safe_attr(ls, "contact_number") or ""),
            address=safe_attr(ls, "address"),
            known_earlier_disease=safe_attr(ls, "known_earlier_disease"),
        )
        created_count += 1
        print(f"[{idx}/{total}] Created: {student.name}")

        # ----------------- Screening -----------------
        screen_date = parse_date(safe_attr(ls, "screen_date"))
        if screen_date:
            screening = Screening.objects.create(
                student=student,
                school=school_obj,
                screen_date=screen_date,
                class_section=safe_attr(ls, "class_section"),
                weight=safe_attr(ls, "weight"),
                height=safe_attr(ls, "height"),
                muac=safe_attr(ls, "muac"),
                weight_age=safe_attr(ls, "weight_age"),
                length_age=safe_attr(ls, "length_age"),
                weight_height=safe_attr(ls, "weight_height"),
                vision_both=safe_attr(ls, "Vision_both"),
                vision_left=safe_attr(ls, "VISON_left"),
                vision_right=safe_attr(ls, "VISON_right"),
            )

            # ----------------- ScreeningCheck -----------------
            screening_data = {}
            for field in valid_screeningcheck_fields:
                value = safe_attr(ls, field)
                if field not in ["E9_remarks", "deworming", "vaccination"]:
                    value = to_bool(value)
                screening_data[field] = value

            ScreeningCheck.objects.create(screening=screening, **screening_data)

    print(f"\nMigration complete! Total students created: {created_count}")

if __name__ == "__main__":
    migrate_students()
