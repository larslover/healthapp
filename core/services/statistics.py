# core/services/statistics.py
from django.db.models import Count, Q
from core.models import Screening, ScreeningCheck

def get_screening_statistics(
    *,
    screening_year,
    school_id=None,
    class_section=None,
):
    """
    Centralized statistics engine for dashboard & reports.
    Combines Screening and ScreeningCheck data.
    """
    qs = Screening.objects.filter(screening_year=screening_year)

    if school_id:
        qs = qs.filter(school_id=school_id)

    if class_section:
        qs = qs.filter(class_section=class_section)

    # Include ScreeningCheck using select_related
    qs = qs.select_related('checklist')

    # ---- HEADLINE NUMBERS ----
    total_screenings = qs.count()
    total_students = qs.values("student_id").distinct().count()
    total_schools = qs.values("school_id").distinct().count()

    # ---- NUTRITION ----
    bmi_counts = qs.values("bmi_category").annotate(count=Count("id")).order_by("bmi_category")
    muac_counts = qs.values("muac_sam").annotate(count=Count("id"))
    weight_age_counts = qs.values("weight_age").annotate(count=Count("id"))
    length_age_counts = qs.values("length_age").annotate(count=Count("id"))
    weight_height_counts = qs.values("weight_height").annotate(count=Count("id"))

    # ---- VISION ----
    vision_counts = qs.values("vision_problem").annotate(count=Count("id"))

    # ---- AGE SEGMENTS ----
    age_groups = qs.values("age_screening").annotate(count=Count("id"))

    # ---- SCREENING CHECKS ----
    checklist_qs = ScreeningCheck.objects.filter(screening__in=qs)

    # Dynamically get all boolean fields from ScreeningCheck model
    checklist_fields = [
        f.name for f in ScreeningCheck._meta.get_fields()
        if f.get_internal_type() == "BooleanField"
    ]

    checklist_stats = {}
    for field in checklist_fields:
        checklist_stats[field] = checklist_qs.filter(**{field: True}).count()

    stats = {
        "totals": {
            "screenings": total_screenings,
            "students": total_students,
            "schools": total_schools,
        },
        "bmi": list(bmi_counts),
        "muac": list(muac_counts),
        "muac_total": sum(item['count'] for item in muac_counts if item['muac_sam'] != "N/A"),
        "weight_age": list(weight_age_counts),
        "length_age": list(length_age_counts),
        "weight_height": list(weight_height_counts),
        "vision": list(vision_counts),
        "age_groups": list(age_groups),
        # ScreeningCheck stats (dynamic)
        "checklist": checklist_stats
    }

    return stats
