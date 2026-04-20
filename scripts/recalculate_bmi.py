import os
import sys
import django

# =====================================================
# 1. Ensure project root is in Python path
# =====================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# =====================================================
# 2. Django setup
# =====================================================
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "healthapp.settings.prod")
django.setup()

# =====================================================
# 3. Imports (AFTER setup)
# =====================================================
from core.models import Screening

# =====================================================
# 4. Queryset
# =====================================================
qs = Screening.objects.filter(
    screening_type="full"
).select_related("student")

updated = 0
errors = 0

# =====================================================
# 5. Recalculation loop (safe + chunked)
# =====================================================
for s in qs.iterator(chunk_size=500):
    try:
        s.calculate_metrics()

        s.save(update_fields=[
            "bmi",
            "bmi_category",
            "muac_sam",
            "weight_height",
            "age_in_month",
        ])

        updated += 1

    except Exception as e:
        errors += 1
        print(f"[ERROR] Screening ID {s.id} (Student {s.student_id}): {e}")

# =====================================================
# 6. Summary
# =====================================================
print("\n==============================")
print("BMI RECALCULATION COMPLETE")
print("==============================")
print(f"Updated records: {updated}")
print(f"Errors: {errors}")
print("==============================\n")