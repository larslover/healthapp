import os
import sys
import django

# ==============================
# Add project root to path (IMPORTANT for PythonAnywhere)
# ==============================
sys.path.append("/home/LarsLover/healthapp")

# ==============================
# Django setup
# ==============================
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "healthapp.settings.prod")
django.setup()

# ==============================
# Imports AFTER setup
# ==============================
from core.models import Screening

# ==============================
# Query
# ==============================
qs = Screening.objects.filter(screening_type="full")

updated = 0

# ==============================
# Recalculate loop
# ==============================
for s in qs.iterator():
    s.calculate_metrics()
    s.save(update_fields=[
        "bmi",
        "bmi_category",
        "muac_sam",
        "weight_height",
        "age_in_month",
    ])
    updated += 1

# ==============================
# Output
# ==============================
print(f"Updated screenings: {updated}")