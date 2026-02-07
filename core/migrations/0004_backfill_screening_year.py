from django.db import migrations

def backfill_screening_year(apps, schema_editor):
    Screening = apps.get_model("core", "Screening")

    for s in Screening.objects.exclude(
        screen_date__isnull=True
    ).filter(
        screening_year__isnull=True
    ).iterator():
        s.screening_year = s.screen_date.year
        s.save(update_fields=["screening_year"])

class Migration(migrations.Migration):

    dependencies = [
        ("core", "0003_add_screening_year"),
    ]

    operations = [
        migrations.RunPython(backfill_screening_year),
    ]
