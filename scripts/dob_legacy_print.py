#!/usr/bin/env python
import sys
import os
import django

# --- Setup Django environment ---
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "healthapp.settings.dev")
django.setup()

from core.models import LegacyStudent

def list_legacy_dobs():
    legacy_students = LegacyStudent.objects.all()
    missing_count = 0
    malformed_count = 0

    for ls in legacy_students:
        dob_raw = getattr(ls, "date_of_birth", None)
        if not dob_raw:
            missing_count += 1
            print(f"[MISSING] {ls.name} -> DOB: {dob_raw}")
        else:
            # Optionally, try parsing
            try:
                # Try YYYY-MM-DD style first
                from datetime import datetime
                parsed = None
                for fmt in ("%d/%m/%Y", "%d-%m-%Y", "%Y-%m-%d", "%m/%d/%Y", "%m/%d/%y"):
                    try:
                        parsed = datetime.strptime(str(dob_raw), fmt).date()
                        break
                    except (ValueError, TypeError):
                        continue
                if not parsed:
                    malformed_count += 1
                    print(f"[MALFORMED] {ls.name} -> DOB: {dob_raw}")
            except Exception as e:
                malformed_count += 1
                print(f"[ERROR] {ls.name} -> DOB: {dob_raw} ({e})")

    print(f"\nTotal legacy students: {legacy_students.count()}")
    print(f"Missing DOBs: {missing_count}")
    print(f"Malformed DOBs: {malformed_count}")

if __name__ == "__main__":
    list_legacy_dobs()
