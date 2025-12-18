# scripts/clean_prod_data.py

import os
import django

# --- Setup Django environment ---
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "healthapp.settings.prod")
django.setup()

from django.contrib.auth.models import User
from django.db import transaction
from django.apps import apps

# ⚡ Optional: wrap in a transaction for safety
with transaction.atomic():
    # Keep superusers
    superuser_ids = list(User.objects.filter(is_superuser=True).values_list('id', flat=True))
    print(f"Superusers preserved: {len(superuser_ids)}")

    # Iterate over all models in installed apps
    for model in apps.get_models():
        # Skip Django internal tables and superuser table
        model_name = model._meta.model_name
        app_label = model._meta.app_label

        if app_label in ("auth", "contenttypes", "sessions", "admin"):
            continue

        if model == User:
            # Delete all non-superusers
            deleted, _ = User.objects.exclude(id__in=superuser_ids).delete()
            print(f"Deleted {deleted} non-superuser users")
            continue

        # Delete all data from the model
        deleted, _ = model.objects.all().delete()
        print(f"Deleted {deleted} rows from {app_label}.{model_name}")

print("✅ Data cleanup complete. All app data cleared except superusers.")
