# core/services/statistics.py
from django.db.models import Count, Case, When, IntegerField, Value
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

    qs = qs.select_related("checklist")

    # ---- HEADLINE NUMBERS ----
    total_screenings = qs.count()
    total_students = qs.values("student_id").distinct().count()
    total_schools = qs.values("school_id").distinct().count()

    # ---- BMI (LOGICAL ORDER, NO N/A) ----
    bmi_order = Case(
        When(bmi_category="severe underweight", then=Value(1)),
        When(bmi_category="moderate underweight", then=Value(2)),
        When(bmi_category="mild underweight", then=Value(3)),
        When(bmi_category="normal", then=Value(4)),
        When(bmi_category="overweight", then=Value(5)),
        When(bmi_category="obese", then=Value(6)),
        default=Value(99),
        output_field=IntegerField(),
    )

    bmi_counts = (
        qs.exclude(bmi_category="N/A")
          .values("bmi_category")
          .annotate(
              count=Count("id"),
              sort_order=bmi_order,
          )
          .order_by("sort_order")
    )

    # ---- MUAC ----
    muac_counts = qs.values("muac_sam").annotate(count=Count("id"))

    # ---- WEIGHT FOR HEIGHT (LOGICAL ORDER, NO N/A) ----
    weight_height_order = Case(
        When(weight_height="Severe Acute Malnutrition", then=Value(1)),
        When(weight_height="Moderate Acute Malnutrition", then=Value(2)),
        When(weight_height="Normal", then=Value(3)),
        When(weight_height="Overweight", then=Value(4)),
        When(weight_height="Obese", then=Value(5)),
        default=Value(99),
        output_field=IntegerField(),
    )

    weight_height_counts = (
        qs.exclude(weight_height="N/A")
          .values("weight_height")
          .annotate(
              count=Count("id"),
              sort_order=weight_height_order,
          )
          .order_by("sort_order")
    )

    # ---- VISION ----
    vision_counts = qs.values("vision_problem").annotate(count=Count("id"))

    # ---- AGE SEGMENTS ----
    age_groups = qs.values("age_screening").annotate(count=Count("id"))

    # ---- SCREENING CHECKS ----
    checklist_qs = ScreeningCheck.objects.filter(screening__in=qs)

    checklist_fields = [
        f.name for f in ScreeningCheck._meta.get_fields()
        if f.get_internal_type() == "BooleanField"
    ]

    checklist_stats = {
        field: checklist_qs.filter(**{field: True}).count()
        for field in checklist_fields
    }

    return {
        "totals": {
            "screenings": total_screenings,
            "students": total_students,
            "schools": total_schools,
        },
        "bmi": list(bmi_counts),
        "muac": list(muac_counts),
        "muac_total": sum(
            item["count"] for item in muac_counts if item["muac_sam"] != "N/A"
        ),
        "weight_height": list(weight_height_counts),
        "vision": list(vision_counts),
        "age_groups": list(age_groups),
        "checklist": checklist_stats,
    }
