from django.db.models import Count
from core.models import Screening

def get_screening_statistics(
    *,
    screening_year,
    school_id=None,
    class_section=None,
):
    """
    Centralized statistics engine for dashboard & reports
    """

    qs = Screening.objects.filter(screening_year=screening_year)

    if school_id:
        qs = qs.filter(school_id=school_id)

    if class_section:
        qs = qs.filter(class_section=class_section)

    stats = {
        # ---- HEADLINE NUMBERS ----
        "totals": {
            "screenings": qs.count(),
            "students": qs.values("student_id").distinct().count(),
            "schools": qs.values("school_id").distinct().count(),
        },

        # ---- NUTRITION ----
        "bmi": list(
            qs.values("bmi_category")
              .annotate(count=Count("id"))
              .order_by("bmi_category")
        ),

        "muac": list(
            qs.values("muac_sam")
              .annotate(count=Count("id"))
        ),

        "weight_age": list(
            qs.values("weight_age")
              .annotate(count=Count("id"))
        ),

        "length_age": list(
            qs.values("length_age")
              .annotate(count=Count("id"))
        ),

        "weight_height": list(
            qs.values("weight_height")
              .annotate(count=Count("id"))
        ),

        # ---- VISION ----
        "vision": list(
            qs.values("vision_problem")
              .annotate(count=Count("id"))
        ),

        # ---- AGE SEGMENTS ----
        "age_groups": list(
            qs.values("age_screening")
              .annotate(count=Count("id"))
        ),
    }

    return stats
