import os
import sys
import django

# =====================================================
# Setup project path (only if running standalone)
# =====================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

# =====================================================
# Django setup
# =====================================================
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "healthapp.settings.prod")
django.setup()

# =====================================================
# Imports
# =====================================================
from core.models import Screening

# =====================================================
# Queryset (only full screenings)
# =====================================================
qs = Screening.objects.filter(screening_type="full").select_related("student")

updated = 0
errors = 0

# =====================================================
# Recalculate loop
# =====================================================
for screening in qs.iterator(chunk_size=500):
    try:
        # IMPORTANT:
        # Your model's save() already calls calculate_metrics()
        # so we DO NOT need to call it manually here.

        screening.save(update_fields=[
            "bmi",
            "bmi_category",
            "muac_sam",
            "weight_height",
            "age_in_month",
        ])

        updated += 1

    except Exception as e:
        errors += 1
        print(f"[ERROR] Screening ID {screening.id} (Student {screening.student_id}): {e}")

# =====================================================
# Summary
# =====================================================
print("\n==============================")
print("BMI RECALCULATION COMPLETE")
print("==============================")
print(f"Updated records: {updated}")
print(f"Errors: {errors}")
print("==============================\n")