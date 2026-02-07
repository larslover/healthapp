from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_delete_legacystudent"),
    ]

    operations = [
        migrations.AddField(
            model_name="screening",
            name="screening_year",
            field=models.IntegerField(
                null=True,
                blank=True,
                db_index=True,
            ),
        ),
    ]
